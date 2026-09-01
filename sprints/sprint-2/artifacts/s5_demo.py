"""Build the Sprint-2 S5 (Trust engine) slice on the Sprint-1 Quoteko scene.

Extends make_fixtures' S1→S2 substrate with the §5 trust loop: capture two
outcome instances (one good, one bad) of the same objective outcome class
("roofing job completed by its committed deadline"), verify each as a claim per
§3.17, then update + persist scoped Trust per §5. Emits validated fixtures
(evidence/claim/expectation/trust/event + updated ledger + graph).
"""
from __future__ import annotations

import json
from pathlib import Path

from ros.substrate import Substrate
from ros.s1 import S1Service
from ros.s2 import S2Service
from ros.s5 import S5Service, config_defaults
import make_fixtures as mf

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"
LEDGER_DIR = FIXTURES / "ledger"
SM_DIR = FIXTURES / "statemachines"
GRAPH_DIR = HERE / "graph"

CTX = "relationship://qk/cust-cxn"
SUBJ = "org://quoteko"
CLAIM = "roofing & repair reliability"

PROVENANCE = {"source": "signed provider job-completion record + S5 anchor",
              "procedure": "completion-anchor-conformance", "confidence": 0.98}


def _trusts_on_graph(sub) -> list[dict]:
    return [o for o in sub.graph.objects.values()
            if o.get("uri", "").startswith("trust://")]


def build_s2() -> tuple[Substrate, list, list]:
    """Run the full Trust-engine demo; return (substrate, before_ranking, after_ranking)."""
    sub = mf.build()          # Sprint-1 scene: S1 substrate + S2 match + seeded trust
    s5 = S5Service(sub)
    s2 = S2Service(sub)
    s1 = S1Service(sub)

    identity = sub._meta["identity"]
    intent = sub._meta["intent"]                       # keys [roofing, repair]
    offers = [o for o in sub.graph.objects.values() if o.get("uri", "").startswith("offer://")]

    # Create the shared expectation for the outcome class (§3.11)
    expectation = s5.make_expectation("expectation://qk/e-on-time",
                                      "contracted roofing job",
                                      "complete by committed deadline",
                                      "2026-09-20T00:00:00Z")
    sub.record(s5._ev("STATE_CHANGE", "event://qk/expect-on-time", "agent://s5", 900,
                      "register expectation for on-time roofing completion",
                      [expectation]), "agent://s5")

    # BEFORE ranking (S2, seeded T1 trusts) — flywheel baseline
    before = s2.match_offers(intent, offers, _trusts_on_graph(sub), trust_floor=0.5)

    # --- capture + verify + update, two instances of the same outcome class ---
    jobs = [
        # norcrete: completed LATE -> bad outcome
        {"uri": "event://qk/outcome-norcrete", "job": "job-norcrete",
         "provider": "org://qk/norcrete",
         "committed_deadline": "2026-09-20T00:00:00Z",
         "actual_completed_at": "2026-09-22T00:00:00Z"},   # 2 days late
        # solarworks: completed ON TIME -> good outcome
        {"uri": "event://qk/outcome-solarworks", "job": "job-solarworks",
         "provider": "org://qk/solarworks",
         "committed_deadline": "2026-09-25T00:00:00Z",
         "actual_completed_at": "2026-09-24T00:00:00Z"},   # 1 day early
    ]
    cfg = config_defaults()
    for idx, job in enumerate(jobs):
        ev_id_base = 1000 + idx * 10
        evidence, on_time = s5.capture(
            job, PROVENANCE, signer=job["provider"], i=ev_id_base)
        statement = (f"{job['provider']} completed {job['job']} by its committed "
                     f"deadline (on-time roofing completion)")
        vr = s5.verify(evidence, statement, job, i=ev_id_base + 1)
        s5.update_trust(subject=SUBJ, target=job["provider"], claim=CLAIM,
                        context=CTX, verify=vr,
                        evidence_score=vr.degree, i=ev_id_base + 2,
                        alpha=cfg["alpha"], expectation=cfg["expectation"],
                        recency=cfg["recency"])

    # AFTER ranking (S2 re-run, updated trusts from the graph)
    after = s2.match_offers(intent, offers, _trusts_on_graph(sub), trust_floor=0.5)

    sub._meta["before"] = [m.to_dict() for m in before]
    sub._meta["after"] = [m.to_dict() for m in after]
    sub._meta["identity"] = identity
    return sub, [m.to_dict() for m in before], [m.to_dict() for m in after]


def emit_s2_fixtures(sub: Substrate) -> dict[str, Path]:
    FIXTURES.mkdir(parents=True, exist_ok=True)

    # validated S5 instances grouped by scheme (each maps to a $def)
    by_uri = {}
    for e in sub.ledger.entries:
        for obj in e.get("state_update") or []:
            by_uri[obj["uri"]] = obj

    def dump_grp(name, prefixes):
        items = [o for u, o in by_uri.items()
                 if u.startswith(tuple(f"{p}://" for p in prefixes))]
        p = FIXTURES / "s5" / f"{name}.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(items, indent=2))
        return p

    files = [
        dump_grp("evidence", ["evidence"]),
        dump_grp("claim", ["claim"]),
        dump_grp("expectation", ["expectation"]),
        dump_grp("trust", ["trust"]),
        dump_grp("events", ["event"]),
        dump_grp("relationship", ["relationship", "interaction", "consent",
                                  "delegation", "authority"]),
        dump_grp("actors_offers", ["person", "org", "agent", "entity", "rule", "offer"]),
        dump_grp("decisions", ["decision"]),
    ]
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    lf = LEDGER_DIR / "ledger-quoteko.json"
    lf.write_text(json.dumps(sub.ledger.to_dict(), indent=2))
    files.append(lf)

    SM_DIR.mkdir(parents=True, exist_ok=True)
    rf = SM_DIR / "relationship.json"
    rf.write_text(json.dumps({"uri": "relationship://qk/cust-cxn",
                              "states": ["PROPOSED", "ACTIVE"]}))
    files.append(rf)

    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    gf = GRAPH_DIR / "current-state.json"
    gf.write_text(json.dumps(sub.graph.to_dict(), indent=2))
    files.append(gf)
    return {f.name: f for f in files}


if __name__ == "__main__":
    sub, before, after = build_s2()
    emitted = emit_s2_fixtures(sub)
    for name, path in emitted.items():
        print(f"  wrote {name} -> file://{path}")
    print("\nBEFORE:", [(m["provider"], m["score"]) for m in before])
    print("AFTER :", [(m["provider"], m["score"]) for m in after])
    print("EVENTS:", len(sub.ledger.entries), "| GRAPH:", len(sub.graph.objects))