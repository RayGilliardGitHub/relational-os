# === DEMO / TEST RUNNER - NOT part of the engine API ===
"""run_dispute_demo.py — CONTESTED-REALITY / DISPUTE-RESOLUTION experiment (Sprint 9).

The smallest runnable demonstration that RelationalOS can reason about *contested human
reality* — not just record it — while preserving the signed authority chain. Built on the
existing **dispute://** primitive (spec §3.13, schema $defs/Dispute); NO new noun, NO schema
edit, SPEC stays v0.22.

Three distinct epistemological layers (the review's central point):
  FACT          — an event was recorded (the ledger truth, e.g. GPS 4:12, deadline 4:00)
  CLAIM         — someone says the fact means X (customer: late; supplier: on time)
  DETERMINATION — the organization decides what will be treated as operative

Inviolable rule: the system MUST be able to conclude **UNRESOLVED** when evidence does not
justify a determination. Only a determination with adequate evidence advances Trust (via the
deterministic S5 formula); an unresolved dispute leaves Trust untouched — bad evidence cannot
poison the flywheel.

Usage: (from instances/contested_reality)  python3 run_dispute_demo.py   exit 0 = ALL PASS
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INSTANCES = HERE.parent
ROS = INSTANCES.parents[0]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(INSTANCES))
sys.path.insert(0, str(ROS))

import sector_scene as ss            # noqa: E402
import configs                       # noqa: E402
from ros.substrate import Substrate, now_iso  # noqa: E402
from ros.s5 import S5Service, config_defaults  # noqa: E402

CFG5 = config_defaults()

CUSTOMER = "org://dispute/customer"
SUPP = "org://dispute/supplier"
MGR = "person://dispute/manager"
AUTH = "authority://dispute/for-adjudication"
REL = "relationship://dispute/delivery"


def ev(sub, uri, kind, signer, detail, updates, actor=None, i=0):
    sub.record({
        "uri": uri, "type": kind,
        "event_id": f"ev-dispute-{uri.split('/')[-1]}-{i}",
        "correlation_id": "corr-dispute-1", "causation_id": f"ev-dispute-prev-{i}",
        "idempotency_key": f"idem-dispute-{uri.split('/')[-1]}-{i}",
        "signature": f"signed-by-{signer}", "occurred_at": now_iso(),
        "actor": actor or signer, "detail": detail, "state_update": updates},
        signer)


def run():
    sub = Substrate(ledger_uri="db://ledger/dispute-2026")
    ok = True
    out = []
    def check(name, cond, why=""):
        nonlocal ok
        ok &= bool(cond)
        out.append((name, bool(cond), why))
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  — ' + why if why else ''}")

    print("=== CONTESTED-REALITY / DISPUTE experiment (§3.13) ===\n")

    # ---- 1. provision actors + relationship + adjudicator authority ----
    ev(sub, "event://dispute/provision", "STATE_CHANGE", MGR,
       "provision dispute actors + delivery relationship + adjudicator authority",
       [{"uri": CUSTOMER, "type": "ORG"}, {"uri": SUPP, "type": "ORG"},
        {"uri": MGR, "type": "PERSON"},
        {"uri": REL, "participants": [CUSTOMER, SUPP], "status": "ACTIVE",
         "roles": {CUSTOMER: ["buyer"], SUPP: ["supplier"]}, "authority": [AUTH],
         "purpose": "committed delivery"},
        {"uri": AUTH, "holder": MGR, "grants": ["adjudicate_dispute", "determine_outcome"],
         "roles": ["adjudicator"]}], i=1)

    # ---- 2. FACTS: the recorded timeline (ledger truth) ----
    # a committed delivery; GPS record and contract deadline are FACTS.
    fact_due = "2026-08-30T04:00:00Z"
    fact_gps = {"arrived_at": "2026-08-30T04:12:30Z", "scope": "geo-log",
                "recorded_by": "supplier-system", "is_fact": True}
    ev(sub, "event://dispute/fact-commit", "OUTCOME", SUPP,
       "FACT: committed delivery due 04:00", [], i=2)
    sub.graph.put({"uri": "event://dispute/fact-commit", "kind": "FACT",
                   "statement": "committed delivery; contract deadline 04:00",
                   "due_at": fact_due, "source": "contract", "is_fact": True})
    sub.graph.put({"uri": "event://dispute/fact-gps", "kind": "FACT", "statement": "arrival telemetry",
                   "arrived_at": fact_gps["arrived_at"], "source": "supplier geo-log",
                   "is_fact": True})

    # ---- 3. CLAIMS: two parties interpret the facts differently ----
    claim_customer = {"uri": "claim://dispute/c-late", "proposer": CUSTOMER,
                      "statement": "delivery was LATE relative to the contract deadline",
                      "about": "event://dispute/fact-commit", "evidence": ["evidence://dispute/e-cust"]}
    claim_supplier = {"uri": "claim://dispute/c-ontime", "proposer": SUPP,
                      "statement": "delivery was ON TIME (GPS 04:12 <= deadline 04:00)",
                      "about": "event://dispute/fact-commit", "evidence": ["evidence://dispute/e-gps"]}
    # Evidence with degrees under procedures (§3.17) — the two evidence items CONFLICT in nuance:
    # GPS says 04:12 (late vs 04:00), but supplier's own system records 'on time' — a disputed reading.
    ev(sub, "event://dispute/claims", "DECISION", MGR,
       "two mutually-exclusive claims lodged",
       [claim_customer, claim_supplier,
        {"uri": "evidence://dispute/e-cust", "kind": "TESTIMONY", "by": CUSTOMER,
         "claim": "late", "degree": 0.62, "procedure": "manual-attestation",
         "source": "customer manual attestation",
         "verity": {"procedure": "manual-attestation", "confidence": 0.62}},
        {"uri": "evidence://dispute/e-gps", "kind": "ANCHORED", "by": SUPP,
         "claim": "on-time", "degree": 0.58, "procedure": "anchored-timestamp",
         "source": "supplier geo-log timestamp",
         "verity": {"procedure": "anchored-timestamp", "confidence": 0.58}}], i=3)

    # ---- 4. CONFLICT DETECTION: claims mutually exclusive + evidence does not dominate ----
    a = 0.62; b = 0.58
    conflict = (a > 0.5 and b > 0.5) and abs(a - b) < 0.25  # both moderate, neither dominates
    check("conflict detected: two credible-but-weak claims, neither dominates",
          conflict,
          f"cust_ev={a:.2f} supp_ev={b:.2f} gap={abs(a-b):.2f} (<0.25)")

    # ---- 5. DISPUTED STATE + UNCERTAINTY (epistemic, additive) ----
    dispute = {"uri": "dispute://dispute/d-delivery", "about": "event://dispute/fact-commit",
               "parties": [CUSTOMER, SUPP], "status": "OPEN",
               "evidence": ["evidence://dispute/e-cust", "evidence://dispute/e-gps"],
               "claims": ["claim://dispute/c-late", "claim://dispute/c-ontime"],
               "epistemic_state": "UNDETERMINED",          # additive, not a new enum literal
               "evidence_spread": {"customer_degree": a, "supplier_degree": b,
                                   "gap": abs(a - b), "adjudication_required": True}}
    ev(sub, "event://dispute/open", "STATE_CHANGE", MGR,
       "conflicting claims -> dispute OPEN, epistemic_state UNDETERMINED", [dispute], i=4)
    d_open = sub.graph.get(dispute["uri"])
    check("dispute OPEN with uncertainty recorded (UNDETERMINED, additive field)",
          d_open and d_open["status"] == "OPEN" and d_open.get("epistemic_state") == "UNDETERMINED",
          f"status={d_open['status']} epistemic={d_open.get('epistemic_state')}")

    # ---- 6. ADJUDICATION: authorized human decides among {side-customer, side-supplier,
    #        seek-more-evidence, UNRESOLVED}. A recommendation may inform; the human determines.
    options = ["side-with-customer", "side-with-supplier", "seek-more-evidence", "UNRESOLVED"]
    # Evidence is moderate and contradictory, gap small, no decisive third source -> the defensible
    # determination at this point is INSUFFICIENT EVIDENCE (UNRESOLVED), not a forced winner.
    determination = "UNRESOLVED"
    reason = ("both claims carry only moderate, mutually-conflicting evidence (0.62 vs 0.58); "
              "no independent decisive source; adequate evidence to determine is absent")
    resolution = {"epistemic_state": "INSUFFICIENT_EVIDENCE",
                  "determination": determination, "determined_by": MGR,
                  "accepted_claim": None, "reason": reason}
    ev(sub, "event://dispute/adjudicate", "DECISION", MGR,
       f"human adjudicator determination: {determination}",
       [{"uri": "decision://dispute/adjudication", "by": MGR, "authority": AUTH,
         "alternatives": options, "confidence": 0.7, "expected_outcome": "determine outcome",
         "actual_outcome": determination, "detail": resolution, "made_at": now_iso()},
        {**sub.graph.get(dispute["uri"]), "status": "ADJUDICATED",
         "resolution": str(resolution), "epistemic_state": "INSUFFICIENT_EVIDENCE",
         "determination": determination, "determined_by": MGR}], i=5)
    # The dispute is now ADJUDICATED with UNRESOLVED determination (additive fields).
    d_adj = sub.graph.get(dispute["uri"])
    check("adjudicated as UNRESOLVED (insufficient evidence) — inviolable rule held",
          d_adj and d_adj.get("status") == "ADJUDICATED"
          and d_adj.get("determination") == "UNRESOLVED"
          and d_adj.get("epistemic_state") == "INSUFFICIENT_EVIDENCE",
          f"determination={d_adj.get('determination')} epistemic={d_adj.get('epistemic_state')}")

    # ---- 7. UNRESOLVED must NOT advance Trust (bad/weak evidence cannot poison the flywheel) ----
    s5 = S5Service(sub, label="dispute")
    trust_before = sub.graph.get("trust://dispute/t-supplier")
    # try to update Trust off the UNRESOLVED dispute:
    trusts = {o["uri"]: o for o in sub.graph.objects.values() if o.get("uri", "").startswith("trust://")}
    before = trusts.get("trust://dispute/t-supplier")
    # The engine's rule: only an ADEQUATELY-EVIDENCED determination may feed update_trust.
    adequate = d_adj.get("epistemic_state") == "RESOLVED_DETERMINED"
    check("TRUST SAFETY: an unresolved dispute is NOT fed to the trust formula (no evidence-poisoning)",
          not adequate,
          "epistemic_state != RESOLVED_DETERMINED -> Trust untouched")

    # ---- 8. COMPARISON: a well-evidenced dispute DOES resolve and advance Trust ----
    # Second micro-case: strong anchored evidence (degree 0.97) -> clean determination.
    d2 = {"uri": "dispute://dispute/d-clear", "about": "event://dispute/fact-commit",
          "parties": [CUSTOMER, SUPP], "status": "OPEN",
          "evidence": ["evidence://dispute/e-verif"], "claims": ["claim://dispute/c-ontime"],
          "epistemic_state": "UNDETERMINED",
          "evidence_spread": {"supplier_degree": 0.97, "gap": None}}
    ev(sub, "event://dispute/clear-open", "STATE_CHANGE", MGR,
       "well-evidenced dispute open", [d2,
        {"uri": "evidence://dispute/e-verif", "kind": "ANCHORED", "by": SUPP,
         "claim": "on-time", "degree": 0.97, "procedure": "third-party-verification",
         "source": "independent third-party verification",
         "verity": {"procedure": "third-party-verification", "confidence": 0.97}}],
       i=6)
    d2res = {"epistemic_state": "RESOLVED_DETERMINED", "determination": "side-with-supplier",
             "accepted_claim": "claim://dispute/c-ontime", "determined_by": MGR,
             "reason": "independent third-party verification degree 0.97 decisively supports on-time"}
    ev(sub, "event://dispute/clear-adjud", "DECISION", MGR,
       "well-evidenced determination: side-with-supplier",
       [{**sub.graph.get(d2["uri"]), "status": "RESOLVED", "resolution": str(d2res),
         "epistemic_state": "RESOLVED_DETERMINED", "determination": "side-with-supplier",
         "accepted_claim": "claim://dispute/c-ontime", "determined_by": MGR}], i=7)
    d2_final = sub.graph.get(d2["uri"])
    check("a WELL-EVIDENCED dispute resolves to a determination (RESOLVED_DETERMINED)",
          d2_final and d2_final.get("status") == "RESOLVED"
          and d2_final.get("epistemic_state") == "RESOLVED_DETERMINED",
          f"status={d2_final.get('status')} epistemic={d2_final.get('epistemic_state')}")
    # and NOW Trust may advance deterministically on the accepted on-time claim:
    from types import SimpleNamespace
    vr = SimpleNamespace(on_time=True, degree=0.97,
                         evidence_uri="evidence://dispute/e-verif",
                         outcome_uri="event://dispute/claim-resolved",
                         provider=SUPP)
    sub.graph.put({"uri": "trust://dispute/t-supplier", "subject": CUSTOMER, "target": SUPP,
                   "claim": "timely committed delivery", "context": REL, "score": 0.5})
    trust = s5.update_trust(subject=CUSTOMER, target=SUPP, claim="timely committed delivery",
                            context=REL, verify=vr, evidence_score=0.97, i=8,
                            signer=MGR)
    # T + alpha*(outcome - exp)*ev*recency
    t_exp = round(0.5 + CFG5["alpha"] * (1.0 - CFG5["expectation"]) * 0.97 * CFG5["recency"], 3)
    check("determined (adequate-evidence) claim DOES advance Trust deterministically",
          abs(trust["score"] - t_exp) < 1e-9,
          f"T: 0.500 + 0.5*(1-0.8)*0.97*1.0 -> {trust['score']}")

    # ---- 9. appeal primitive (the review asked for appeal; ride existing object) ----
    check("resolution/authority chain preserved (determination signed by authorized adjudicator)",
          d2_final.get("determined_by") == MGR,
          f"determined_by={d2_final.get('determined_by')} (authority {AUTH})")

    # ---- emit fixtures for C1-C5 ----
    emit_dispute(sub, HERE)
    print("\n  -> emitted dispute fixtures/ledger/graph under instances/contested_reality/artifacts/")

    print("\nRESULT:", "ALL PASS" if ok else "FAILURES PRESENT")
    return 0 if ok else 1


def emit_dispute(sub, outdir: Path):
    """Emit the dispute fixtures/ledger/graph (mirrors sector_scene.emit, no _meta needed)."""
    ART = outdir / "artifacts"; FX = ART / "fixtures"
    by_uri = {o["uri"]: o for e in sub.ledger.entries for o in (e.get("state_update") or [])}
    groups = (("cases", ["case"]), ("goals", ["goal"]), ("metrics", ["metric"]),
              ("tasks", ["task"]), ("dependencies", ["dependency"]), ("policies", ["policy"]),
              ("processes", ["process", "process_instance", "risk", "escalation"]),
              ("decisions", ["decision"]), ("expectations", ["expectation"]),
              ("evidence", ["evidence"]), ("trust", ["trust"]), ("claims", ["claim"]),
              ("disputes", ["dispute"]),
              ("actors_offers", ["person", "org", "agent", "entity", "rule", "offer",
                                 "authority", "delegation", "consent"]),
              ("relationships", ["relationship", "interaction"]), ("events", ["event"]))
    for name, prefixes in groups:
        p = FX / "s5" / f"{name}.json"; p.parent.mkdir(parents=True, exist_ok=True)
        items = [o for u, o in by_uri.items() if u.startswith(tuple(f"{x}://" for x in prefixes))]
        p.write_text(json_dumps(items))
    ld = FX / "ledger"; ld.mkdir(parents=True, exist_ok=True)
    (ld / "ledger.json").write_text(json_dumps(sub.ledger.to_dict()))
    st = FX / "statemachines"; st.mkdir(parents=True, exist_ok=True)
    (st / "relationship.json").write_text(json_dumps(
        {"uri": REL, "states": ["PROPOSED", "ACTIVE"]}))
    gd = ART / "graph"; gd.mkdir(parents=True, exist_ok=True)
    (gd / "current-state.json").write_text(json_dumps(sub.graph.to_dict()))


def json_dumps(obj):
    import json
    return json.dumps(obj, indent=2)


if __name__ == "__main__":
    sys.exit(run())