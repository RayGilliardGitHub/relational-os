"""Build the Sprint-1 S1→S2 slice for Quoteko, emit fixtures + ledger + graph.

Runs S1 (resolve_identity, authenticate, authorize, resolve_role) then S2
(infer_intent, match_offers) for role=customer on the quoting/triage domain, with a
human verification floor, writing every step as a signed, content-addressed Ledger
event and landing current state on the Graph. Emits validated fixtures.
"""
from __future__ import annotations

import json
from pathlib import Path

from ros.substrate import Substrate
from ros.s1 import S1Service
from ros.s2 import S2Service

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"
LEDGER_DIR = FIXTURES / "ledger"
SM_DIR = FIXTURES / "statemachines"
GRAPH_DIR = HERE / "graph"
SLC_DIR = FIXTURES / "s1s2"

ROLE_PARTICIPANT = "person://qk/customer"
ROLE_OTHER = "person://qk/customer"

T = ["2026-09-01T10:%02d:00Z" % m for m in range(0, 16)]


def _ev(kind: str, uri: str, actor: str, i: int, detail: str,
        state_update: list[dict] | None = None) -> dict:
    return {
        "uri": uri,
        "type": kind,
        "event_id": f"ev-qk-{i}",
        "correlation_id": "corr-qk-quote-1",
        "causation_id": f"ev-qk-{max(0, i-1)}",
        "idempotency_key": f"idem-qk-{i}",
        "signature": f"signed-by-{actor}",
        "occurred_at": T[i],
        "actor": actor,
        "detail": detail,
        "state_update": state_update or [],
    }


def build() -> Substrate:
    sub = Substrate(ledger_uri="db://ledger/quoteko-2026")
    s1 = S1Service(sub)
    s2 = S2Service(sub)

    # ------------------------------------------------------------------ seed
    actors = [
        {"uri": "person://qk/customer", "type": "PERSON"},
        {"uri": "person://qk/approver", "type": "PERSON",
         "identity": {"attestations": ["employee"]}},
        {"uri": "org://quoteko", "type": "ORG"},
        {"uri": "org://qk/norcrete", "type": "ORG"},
        {"uri": "org://qk/solarworks", "type": "ORG"},
        {"uri": "org://qk/generalco", "type": "ORG"},
        {"uri": "agent://s1", "type": "AGENT"},
        {"uri": "agent://s2", "type": "AGENT"},
    ]
    canonical = {
        "uri": "entity://qk/canon-customer",
        "canonical": "person://qk/customer",
        "aliases": ["qk-customer-8832", "C. Rivera"],
        "kind": "PERSON",
    }
    relationship = {
        "uri": "relationship://qk/cust-cxn",
        "participants": ["person://qk/customer", "org://quoteko"],
        "roles": {"person://qk/customer": ["customer"],
                  "org://quoteko": ["service_provider"]},
        "context": {"organization": "org://quoteko",
                    "relationship": "relationship://qk/cust-cxn",
                    "role": "customer", "jurisdiction": "US-NM",
                    "time": T[0], "purpose": "purpose://qk/quoting",
                    "rules": ["rule://qk/tos"]},
        "purpose": "property-services quoting/triage",
        "status": "ACTIVE",
        "created_at": T[0],
        "effective_from": T[0],
        "authority": ["authority://qk/for-matching"],
    }
    consent = {"uri": "consent://qk/match-data",
               "granted_by": "person://qk/customer",
               "granted_for": "match my quote request to vetted service offers",
               "scope": ["permission://qk/read-profile", "permission://qk/present-offers"],
               "duration": {"effective": T[0], "expires": "2027-09-01T00:00:00Z"},
               "revocable": True,
               "status": "GRANTED"}
    delegation = {"uri": "delegation://qk/s2-match",
                  "grantor": "org://quoteko",
                  "grantee": "agent://s2",
                  "scope": ["rule://qk/s2-run-matching"],
                  "status": "ACTIVE"}
    authority = {"uri": "authority://qk/for-matching",
                 "grants": ["request_quote"],
                 "holder": "org://quoteko"}
    trusts = [
        {"uri": "trust://qk/t-norcrete", "subject": "org://quoteko",
         "target": "org://qk/norcrete", "claim": "roofing & repair reliability",
         "context": "relationship://qk/cust-cxn", "score": 0.92,
         "updated_at": T[0]},
        {"uri": "trust://qk/t-solarworks", "subject": "org://quoteko",
         "target": "org://qk/solarworks", "claim": "roofing & repair reliability",
         "context": "relationship://qk/cust-cxn", "score": 0.61,
         "updated_at": T[0]},
        {"uri": "trust://qk/t-generalco", "subject": "org://quoteko",
         "target": "org://qk/generalco", "claim": "roofing reliability",
         "context": "relationship://qk/cust-cxn", "score": 0.42,
         "updated_at": T[0]},
    ]
    offers = [
        {"uri": "offer://qk/o-norcrete", "provider": "org://qk/norcrete",
         "service": "flat-roof replacement & repair", "capability_keys": ["roofing", "repair"],
         "price": 12400, "currency": "USD", "terms": "fixed-price, 2yr warranty",
         "status": "AVAILABLE"},
        {"uri": "offer://qk/o-solarworks", "provider": "org://qk/solarworks",
         "service": "roof replacement + solar", "capability_keys": ["roofing", "repair", "solar"],
         "price": 18900, "currency": "USD", "terms": "fixed-price, 5yr warranty",
         "status": "AVAILABLE"},
        {"uri": "offer://qk/o-generalco", "provider": "org://qk/generalco",
         "service": "roof patch", "capability_keys": ["roofing"],
         "price": 9800, "currency": "USD", "terms": "time-and-materials",
         "status": "AVAILABLE"},
    ]
    evidence = {"uri": "evidence://qk/e-oidc", "kind": "ANCHORED",
                "source": "OIDC assertion + attestation",
                "verity": {"procedure": "oidc-verification", "confidence": 0.98},
                "captured_at": T[0]}
    # rules object referenced by relationship context
    rules_obj = {"uri": "rule://qk/tos", "kind": "POLICY",
                 "text": "vetted contractors; human-accept required for committed hire"}
    s2match_rule = {"uri": "rule://qk/s2-run-matching", "kind": "POLICY",
                    "text": "S2 agent may run capability-bound matching under Quoteko",
                    "grants": ["run_matching"]}

    seed = actors + [canonical, relationship, consent, delegation, authority,
                     evidence, rules_obj, s2match_rule] + trusts + offers
    sub.record(_ev("ACTION", "event://qk/provision", "agent://s1", 0,
                   "provision Quoteko quote domain substrate and registry", seed),
               signer="agent://s1")

    # ------------------------------------------------------------------ S1
    # identity / authentication / role / authorization (thin substrate)
    identity = s1.resolve_identity("qk-customer-8832", ["oide-assertion"])
    auth_score = s1.authenticate(identity, {"attestations": ["oide-verified"]})
    role = s1.resolve_role("relationship://qk/cust-cxn", identity, {})
    perm = s1.authorize(identity, "request_quote",
                        {"relationship": "relationship://qk/cust-cxn"})
    sub.record(_ev("ACTION", "event://qk/request", identity, 1,
                   "customer submits urgent quote request",
                   [{"uri": "interaction://qk/req-quote", "of": "relationship://qk/cust-cxn",
                     "kind": "REQUEST", "events": ["event://qk/request"]}]),
               signer=identity)
    sub.record(_ev("ACTION", "event://qk/identity-resolved", "agent://s1", 2,
                   f"resolve_identity -> {identity} (canonical), authn score {auth_score}"),
               signer="agent://s1")
    sub.record(_ev("DECISION", "event://qk/role-resolved", "agent://s1", 3,
                   f"resolve_role -> {role} in relationship://qk/cust-cxn"),
               signer="agent://s1")
    # authorization is a capability hand-off, not a durable graph object; it is
    # recorded in the event detail (state captured) and not reified as a URI.
    sub.record(_ev("DECISION", "event://qk/authorized", "agent://s1", 4,
                   f"authorize request_quote -> {perm.target} ({getattr(perm, 'capability', None)})"),
               signer="agent://s1")

    # ------------------------------------------------------------------ S2
    intent = s2.infer_intent(identity, {
        "request": "My roof is leaking near the chimney — urgent, please quote ASAP.",
        "budget": 15000})
    intent_obj = {"uri": "decision://qk/intent", "by": "agent://s2",
                  "authority": "delegation://qk/s2-match",
                  "alternatives": ["defer", "request more detail"],
                  "confidence": 0.9,
                  "expected_outcome": "quote matched and verified",
                  "detail": intent,
                  "made_at": T[5]}
    sub.record(_ev("DECISION", "event://qk/intent", "agent://s2", 5,
                   f"infer_intent -> {intent['need']} urgency={intent['urgency']}",
                   [intent_obj]), signer="agent://s2")

    # Trust-weighted matching (§5): score = fit × scoped trust; floor 0.5.
    matches = s2.match_offers(intent, offers, trusts, trust_floor=0.5)

    # each match is a signed Event (type DECISION) with its score; rejected below floor.
    for i, m in enumerate(matches):
        evk = 6 + i
        decision = {"uri": f"decision://qk/match-{i+1}",
                    "by": "agent://s2", "authority": "delegation://qk/s2-match",
                    "alternatives": ["do nothing"], "confidence": 0.85,
                    "expected_outcome": m.offer_uri,
                    "detail": m.to_dict(), "made_at": T[evk]}
        sub.record(_ev("DECISION", f"event://qk/match-{i+1}", "agent://s2", evk,
                       f"match #{i+1}: {m.offer_uri} score={m.score:.2f} (fit {m.fit:.2f} x trust {m.trust:.2f})",
                       [decision]), signer="agent://s2")
    # trust-floor rejection shown as a signed decision
    floor = [o for o in offers if o["uri"] == "offer://qk/o-generalco"][0]
    sub.record(_ev("DECISION", "event://qk/floor", "agent://s2", 8,
                   f"reject offer://qk/o-generalco (trust 0.42 < floor 0.5)",
                   [{"uri": "decision://qk/floor-generalco", "by": "agent://s2",
                     "authority": "delegation://qk/s2-match", "confidence": 0.99,
                     "detail": {"offer": floor["uri"], "rejected": "below trust floor"},
                     "made_at": T[8]}]), signer="agent://s2")

    # human verification floor (§6/§7B) — hiring is irreversible, human must accept
    top = matches[0]
    sub.record(_ev("ACTION", "event://qk/present", "agent://s2", 9,
                   f"present ranked offers to customer for verification: "
                   f"{', '.join(m.offer_uri for m in matches)}"),
               signer="agent://s2")
    human = _ev("DECISION", "event://qk/human-accept", identity, 10,
                f"human verified & accepted {top.offer_uri} -> engage",
                [{"uri": "decision://qk/human-accept", "by": identity,
                  "authority": "authority://qk/for-matching",
                  "alternatives": [matches[1].offer_uri], "confidence": 1.0,
                  "expected_outcome": f"hire {top.provider}",
                  "actual_outcome": "accepted", "made_at": T[10]}])
    human["state_update"][0]["evidence"] = [evidence["uri"]]
    sub.record(human, signer=identity)

    # commit current state on the graph (offer status -> COMMITTED)
    committed = dict(top.to_dict())
    accepted_offer = dict([o for o in offers if o["uri"] == top.offer_uri][0])
    accepted_offer["status"] = "COMMITTED"
    accepted_offer["matched_by"] = "agent://s2"
    accepted_offer["verified_by"] = identity
    accepted_offer["verified_at"] = T[11]
    sub.record(_ev("STATE_CHANGE", "event://qk/commit", "agent://s2", 11,
                   f"commit matched offer {top.offer_uri} as current state",
                   [accepted_offer]), signer="agent://s2")

    # keep the summary of rankings for the caller
    sub._meta = {
        "identity": identity, "authn_score": auth_score, "role": role,
        "perm": perm, "intent": intent, "matches": [m.to_dict() for m in matches],
        "top": top.to_dict(), "rejected": floor["uri"],
        "offer_status": accepted_offer["status"],
    }
    return sub


def write_fixtures(sub: Substrate) -> dict[str, Path]:
    meta = sub._meta
    # validated instances under fixtures/s1s2/ (each maps to a $def by URI scheme)
    SLC_DIR.mkdir(parents=True, exist_ok=True)
    by_uri = {}
    for e in sub.ledger.entries:
        for obj in e.get("state_update") or []:
            by_uri[obj["uri"]] = obj

    def dump_grp(name, prefixes):
        items = [o for u, o in by_uri.items()
                 if u.startswith(tuple(f"{p}://" for p in prefixes))]
        (SLC_DIR / f"{name}.json").write_text(json.dumps(items, indent=2))
        return (SLC_DIR / f"{name}.json")

    files = [dump_grp("actors", ["person", "org", "agent", "entity", "evidence", "rule"]),
             dump_grp("relationship", ["relationship", "consent", "delegation",
                                       "authority", "trust", "interaction"]),
             dump_grp("offers", ["offer"]),
             dump_grp("decisions", ["decision"]),
             dump_grp("events", ["event"])]

    # ledger (db://) — C3 validated chain
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    lf = LEDGER_DIR / "ledger-quoteko.json"
    lf.write_text(json.dumps(sub.ledger.to_dict(), indent=2))
    files.append(lf)

    # statemachine (C5)
    SM_DIR.mkdir(parents=True, exist_ok=True)
    rf = SM_DIR / "relationship.json"
    rf.write_text(json.dumps({"uri": "relationship://qk/cust-cxn", "states": ["PROPOSED", "ACTIVE"]}))
    files.append(rf)

    # graph current-state (separate from ledger history) — my own round-trip artifact
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    gf = GRAPH_DIR / "current-state.json"
    gf.write_text(json.dumps(sub.graph.to_dict(), indent=2))
    files.append(gf)

    sm = {"meta": meta, "n_events": len(sub.ledger.entries), "head_hash": sub.ledger.head_hash}
    return {f.name: f for f in files}


if __name__ == "__main__":
    sub = build()
    emitted = write_fixtures(sub)
    for name, path in emitted.items():
        print(f"  wrote {name} -> file://{path}")
    print("EVENTS:", sub._meta["identity"], "| role", sub._meta["role"],
          "| top", sub._meta["top"])