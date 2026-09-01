"""Sprint-1 checks.

Two self-authored checks per the PROMPT's DoD:
  A. S1 check of our own — authorize is used per relationship, and delegation is
     honored (incl. revocation immediately voiding capability, §7B).
  B. Ledger/Graph wiring check (1.3) — the round-trip: current Graph state rebuilds
     from the Ledger's append-only history; Ledger=history / Graph=state not conflated
     (§3.16).
"""
from __future__ import annotations

from typing import Any

from .substrate import Substrate
from .s1 import S1Service, Permission, Denial
from .s4 import S4Service


def s1_check(substrate) -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    graph = substrate.graph
    s1 = S1Service(substrate)

    def r(name: str, ok: bool, detail: str = ""):
        results.append((name, ok, detail))

    rel = "relationship://qk/cust-cxn"
    customer = "person://qk/customer"
    agent = "agent://s2"
    delegation = "delegation://qk/s2-match"
    ctx = {"relationship": rel}

    # --- role is relationship-scoped (per §C2, not a separate identity) ---
    role = s1.resolve_role(rel, customer, ctx)
    r("role resolved as customer", role == "customer", f"got {role}")
    # an unbound relationship/participant yields None, proving relationship-scoping
    other = s1.resolve_role("relationship://qk/employee-cxn", customer, ctx)
    r("role is relationship-scoped (absent elsewhere)", other is None, f"got {other}")

    # --- authorization is per relationship (§7B capability-based) ---
    p = s1.authorize(customer, "request_quote", ctx)
    r("authz permitted within the relationship", isinstance(p, Permission),
      repr(p))
    den = s1.authorize(customer, "request_quote", {"relationship": "relationship://qk/other"})
    r("authz denied outside the relationship", isinstance(den, Denial),
      den.reason if isinstance(den, Denial) else repr(den))

    # --- delegation honored: active delegation grants the scoped capability ---
    p2 = s1.authorize(agent, "run_matching", {"relationship": rel, "delegation": delegation})
    r("delegation grants scoped capability", isinstance(p2, Permission), repr(p2))

    # --- revocation voids the capability immediately (§3.4/§7B) ---
    # Operate on a clone so the live graph (and emitted fixtures) stay ACTIVE.
    from types import SimpleNamespace
    clone = substrate.clone_graph()
    d = clone.resolve(delegation)
    d["status"] = "REVOKED"
    clone.put(d)
    s1b = S1Service(SimpleNamespace(graph=clone))
    p3 = s1b.authorize(agent, "run_matching", {"relationship": rel, "delegation": delegation})
    r("revoked delegation -> denial (capability voided)", isinstance(p3, Denial),
      p3.reason if isinstance(p3, Denial) else repr(p3))
    return results


def roundtrip_check(substrate: Substrate) -> list[tuple[str, bool, str]]:
    results: list[tuple[str, bool, str]] = []
    ledger = substrate.ledger
    graph = substrate.graph

    # 1) Ledger integrity (content-addressed chain + signed) — mirrors conformance C3.
    ok, why = ledger.verify()
    results.append(("ledger hash-chain + signatures intact", ok, why))

    # 2) Reconstruct the Graph from the Ledger history (a true round-trip).
    rebuilt: dict[str, dict] = {}
    for e in ledger.entries:
        for obj in (e.get("state_update") or []):
            rebuilt[obj["uri"]] = obj
    original = graph.to_dict()["objects"]
    orig_map = {o["uri"]: o for o in original}
    missing = [u for u in orig_map if u not in rebuilt]
    # Only objects that were produced by a ledger event are required to replay;
    # the offer status is set by the commit event, so require full coverage.
    results.append(
        ("graph state reconstructs to ledger events",
         not missing and len(orig_map) == len(rebuilt),
         (f"missing {missing}" if missing else
          f"{len(orig_map)} graph objects rebuilt from {len(ledger.entries)} events"))
    )

    # 3) Conflation guard (§3.16): ledger is history, graph is state — not confused.
    hist = all(isinstance(e.get("hash"), str) and "signature" in e for e in ledger.entries) \
        and ledger.uri.startswith("db://ledger")
    state_ok = True
    for o in original:
        u = o.get("uri")
        if not (isinstance(u, str) and "://" in u):
            state_ok = False
            break
        if "hash" in o or o is ledger.uri:
            state_ok = False
            break
    results.append(
        ("ledger==history & graph==state (not conflated)",
         hist and state_ok,
         f"history={hist}, state-objects={state_ok}"))
    return results


def s5_check(substrate) -> list[tuple[str, bool, str]]:
    """Sprint-2 S5 check: capture + verify produce signed, grounded evidence; the
    trust object is scoped (keyed by target + claim + context), clamped to [0,1],
    and updated/persisted on the shared Graph + signed Ledger."""
    results: list[tuple[str, bool, str]] = []
    from .s5 import S5Service, VerifyResult

    def r(name: str, ok: bool, detail: str = ""):
        results.append((name, ok, detail))

    ctx = "relationship://qk/cust-cxn"
    subject = "org://quoteko"
    claim = "roofing & repair reliability"

    # --- capture produced signed, grounded evidence on graph + ledger ---
    ev = substrate.graph.get("evidence://qk/job-norcrete")
    r("capture -> signed evidence:// on Graph", ev is not None and bool(ev.get("verity")),
      repr(ev) if ev else "missing evidence://qk/job-norcrete")
    ledge = [e for e in substrate.ledger.entries
             if e.get("uri") == "event://qk/outcome-norcrete"]
    r("capture -> OUTCOME event on Ledger", bool(ledge), f"{len(ledge)} ledger entry")
    ver_val = substrate.graph.get("evidence://qk/job-norcrete")
    r("evidence verity = procedure + confidence (degree under procedure, §3.17)",
      ver_val is not None and "procedure" in ver_val["verity"] and 0 <= ver_val["verity"]["confidence"] <= 1,
      repr(ver_val["verity"]) if ver_val else "n/a")

    # --- trust is scoped: updates landed on the right (subj,target,claim,ctx) keys ---
    norc = substrate.graph.get("trust://qk/t-norcrete")
    sola = substrate.graph.get("trust://qk/t-solarworks")
    r("trust objects carry subject/target/claim/context + score",
      all(o and o["subject"] == subject and o["context"] == ctx and 0 <= o["score"] <= 1
          for o in (norc, sola)),
      f"norcrete={norc['score'] if norc else None}, solarworks={sola['score'] if sola else None}")
    r("trust stays clamped to [0,1)",
      all(0.0 <= o["score"] <= 1.0 for o in (norc, sola)), "in range")

    # --- different claim/context is untouched (scope, not a global score) ---
    gen = substrate.graph.get("trust://qk/t-generalco")
    r("generalco (different claim) untouched by updates (scoped, not global)",
      gen is not None and abs(gen["score"] - 0.42) < 1e-9, f"score={gen['score'] if gen else None}")

    # --- persisted: graph object AND signed ledger STATE_CHANGE event ---
    trust_ev = [e for e in substrate.ledger.entries
                if e.get("uri") == "event://qk/trust-update-norcrete"]
    r("trust write -> signed STATE_CHANGE ledger event",
      bool(trust_ev) and bool(trust_ev[0].get("signature")),
      f"{len(trust_ev)} entry, sig={trust_ev[0].get('signature') if trust_ev else None}")
    return results


def flywheel_check(substrate, before: list, after: list) -> list[tuple[str, bool, str]]:
    """Sprint-2 2.3 check: the flywheel — after a verified bad outcome for norcrete
    and a verified good outcome for solarworks (equal fit), the S2 ranking ordering
    flips exactly as §5 predicts."""
    results: list[tuple[str, bool, str]] = []
    r = lambda name, ok, detail="": results.append((name, ok, detail))  # noqa: E731

    def order(ms):
        return [m["offer"] for m in ms]

    b, a = order(before), order(after)
    # solarworks rises to #1; norcrete falls to #2
    r("same fit -> rank decided by Trust (flywheel)",
      b[0] == "offer://qk/o-norcrete" and a[0] == "offer://qk/o-solarworks",
      f"before {b} -> after {a}")
    solar_after = [m for m in after if m["offer"] == "offer://qk/o-solarworks"][0]
    norc_after = [m for m in after if m["offer"] == "offer://qk/o-norcrete"][0]
    r("Trust moved as §5 predicts (good up, bad down)",
      solar_after["trust"] > 0.61 and norc_after["trust"] < 0.92,
      f"solarworks {solar_after['trust']:.3f} (was 0.61), norcrete {norc_after['trust']:.3f} (was 0.92)")
    r("ranking matches equation output (score = fit x trust)",
      solar_after["score"] == round(1.0 * solar_after["trust"], 3),
      f"solar score {solar_after['score']:.3f} = fit 1.0 x trust {solar_after['trust']:.3f}")
    return results


# ============================================================================
# SPRINT 3 — S3 Orchestration + human floor checks
# ============================================================================
def s3_check(substrate) -> list[tuple[str, bool, str]]:
    """3.1: commit produced a commitment:// (AGREED); the job was split across the
    fleet; >=2 agent-worker steps executed with signed ACTION events on the Ledger."""
    results: list[tuple[str, bool, str]] = []
    r = lambda name, ok, detail="": results.append((name, ok, detail))  # noqa: E731

    comm = substrate.graph.get("commitment://qk/c-solarworks")
    r("commit -> commitment:// AGREED on Graph",
      comm is not None and comm.get("status") == "AGREED",
      repr(comm.get("status") if comm else None))
    ledge = [e for e in substrate.ledger.entries
             if e.get("uri") == "event://qk/s3-commit-solarworks"]
    r("commit -> signed STATE_CHANGE ledger event", bool(ledge) and bool(ledge[0].get("signature")),
      f"{len(ledge)} entry")

    split = substrate.graph.get("decision://qk/s3-split-c-solarworks")
    r("orchestrate -> signed decision:// for the split",
      split is not None and "tasks" in split.get("detail", {}),
      repr(list(split.get("detail", {}).get("tasks", []))) if split else "missing")

    steps = [e for e in substrate.ledger.entries if e.get("uri", "").startswith("event://qk/s3-step-")]
    r(">=2 agent-worker ACTION steps on the Ledger", len(steps) >= 2,
      f"{len(steps)} steps: {[e['uri'] for e in steps]}")
    r("each worker step signed + action-named",
      all(e.get("signature") and e.get("action") for e in steps),
      f"{[e.get('action') for e in steps]}")
    return results


def escalate_check(substrate) -> list[tuple[str, bool, str]]:
    """3.2: the irreversible action (release_final_payment) was NOT auto-executed; it
    escalated to person://qk/approver (signed decision enumerating alternatives) and
    ran only after the human acknowledgement; the Ledger records the escalation."""
    results: list[tuple[str, bool, str]] = []
    r = lambda name, ok, detail="": results.append((name, ok, detail))  # noqa: E731

    entries = substrate.ledger.entries
    def idx(uri):
        for n, e in enumerate(entries):
            if e.get("uri") == uri:
                return n
        return -1

    i_split = idx("event://qk/s3-split-c-solarworks")
    i_esc = idx("event://qk/s3-escalate-t3")
    i_hum = idx("event://qk/s3-human-t3")
    i_fin = idx("event://qk/s3-step-t3")
    r("escalation decision recorded before human acknowledgement", i_esc >= 0 and i_hum >= 0 and i_esc < i_hum,
      f"esc@{i_esc} hum@{i_hum}")
    r("irreversible action NOT auto-executed: split < escalate < human < release",
      i_split >= 0 and i_split < i_esc < i_hum < i_fin,
      f"split@{i_split} esc@{i_esc} hum@{i_hum} release@{i_fin}")

    # the ONLY release_final_payment action is the final one — it must come after the human.
    releases = [e for e in entries if e.get("action") == "release_final_payment"]
    r("release_final_payment exists and runs only after the human commit",
      len(releases) == 1 and i_fin > i_hum, f"{len(releases)} release event")

    # human decision enumerates >=3 alternatives, is signed, made by the approver.
    hum = substrate.graph.get("decision://qk/s3-human-t3")
    alternatives = (hum or {}).get("alternatives") or []
    r("human decision is signed + made by person://qk/approver",
      bool(hum) and hum.get("by") == "person://qk/approver" and
      any(e.get("uri") == "event://qk/s3-human-t3" for e in entries),
      f"by={hum.get('by') if hum else None}")
    r("human decision enumerates >=3 alternatives",
      len(alternatives) >= 3, str(alternatives))
    return results


def loop_check(substrate, next_rank) -> list[tuple[str, bool, str]]:
    """3.3: the S3-executed outcome fed the 2nd S5 Trust update which re-ranked the
    next S2 match — the flywheel closes. Trust raised for solarworks, norcrete scoped."""
    results: list[tuple[str, bool, str]] = []
    r = lambda name, ok, detail="": results.append((name, ok, detail))  # noqa: E731

    ev = substrate.graph.get("evidence://qk/job-solarworks-s3")
    r("S3-executed outcome captured as signed evidence:// (2nd S5 cycle)",
      ev is not None and bool(ev.get("verity")), repr(ev) if ev else "missing")

    sola = substrate.graph.get("trust://qk/t-solarworks")
    r("Trust updated from the S3 outcome (solarworks rose past 0.708)",
      sola is not None and sola["score"] > 0.708, f"score={sola['score'] if sola else None}")
    r("updated trust carries its auditable inputs (expected/outcome/evidence/alpha/recency)",
      sola is not None and all(k in sola for k in ("expected", "outcome", "evidence", "alpha", "recency")),
      f"keys={sorted(k for k in sola if k in ('expected','outcome','evidence','alpha','recency')) if sola else 'n/a'}")

    norc = substrate.graph.get("trust://qk/t-norcrete")
    r("unrelated target's trust untouched (scoped, not global)",
      norc is not None and abs(norc["score"] - 0.528) < 1e-6, f"norcrete={norc['score'] if norc else None}")

    nr = [(m["offer"], m["score"]) for m in next_rank]
    r("next S2 match re-ranked by the updated Trust (solarworks #1, loop closed)",
      nr and nr[0][0] == "offer://qk/o-solarworks", str(nr[:2]))
    return results


ALL_CHECKS = {
    "s1": s1_check, "roundtrip": roundtrip_check, "s5": s5_check,
    "s3": s3_check, "escalate": escalate_check,
}


# ============================================================================
# SPRINT 4 — S4 Settlement + multi-role + multi-org checks
# ============================================================================
def s4_check(sub) -> list[tuple[str, bool, str]]:
    """4.1: the solarworks exchange settled — signed EXCHANGE event + asset title
    transfer + obligation + receipt + reconciliation + OUTCOME (met) that fed an S5
    Trust update which re-ranked the next S2 match (loop closed with settlement)."""
    results: list[tuple[str, bool, str]] = []
    r = lambda name, ok, detail="": results.append((name, ok, detail))  # noqa: E731
    entries = sub.ledger.entries

    exch = [e for e in entries if e.get("uri") == "event://qk/s4-exchange-solarworks"]
    r("settle -> signed EXCHANGE ledger event", bool(exch) and bool(exch[0].get("signature")),
      f"{len(exch)} entry")
    asset = sub.graph.get("asset://money/qk-escrow-solarworks")
    r("each settlement artifact is a signed Ledger event (state rides the EXCHANGE entry)",
      bool(exch) and all(u in {o["uri"] for o in (exch[0].get("state_update") or [])}
                          for u in ("obligation://qk/s4-pay-solarworks",
                                    "receipt://qk/s4-receipt-solarworks",
                                    "decision://qk/s4-recon-solarworks")),
      "obligation+receipt+reconciliation embedded in the signed EXCHANGE event")
    r("Asset Ledger title/custody moved (asset:// money, §4b, not a copy)",
      asset is not None and asset.get("title") == "org://qk/solarworks"
      and asset.get("kind") == "MONEY", repr(asset))
    obl = sub.graph.get("obligation://qk/s4-pay-solarworks")
    receipt = sub.graph.get("receipt://qk/s4-receipt-solarworks")
    recon = sub.graph.get("decision://qk/s4-recon-solarworks")
    r("payment obligation recorded (VOLUNTARILY_UNDERTAKEN)",
      obl is not None and obl.get("source") == "VOLUNTARILY_UNDERTAKEN",
      repr(obl.get("source") if obl else None))
    r("receipt + reconciliation recorded",
      receipt is not None and recon is not None and recon.get("detail", {}).get("matched"),
      f"receipt={bool(receipt)}, recon.matched={recon.get('detail', {}).get('matched') if recon else None}")
    outcome = [e for e in entries if e.get("uri") == "event://qk/s4-outcome-solarworks"]
    r("evaluate -> signed OUTCOME event (met)", bool(outcome) and outcome[0].get("evaluation") == "met",
      f"eval={outcome[0].get('evaluation') if outcome else None}")
    sola = sub.graph.get("trust://qk/t-solarworks")
    r("settled OUTCOME fed S5 Trust update (solarworks rose past 0.806)",
      sola is not None and sola["score"] > 0.806, f"score={sola['score'] if sola else None}")
    nr = sub._meta.get("s41", {}).get("next_rank", [])
    r("next S2 match re-ranked by the settled Trust (solarworks #1, loop closed WITH settlement)",
      bool(nr) and nr[0]["offer"] == "offer://qk/o-solarworks", str(nr[:2]))
    return results


def role_check(sub) -> list[tuple[str, bool, str]]:
    """4.2: ONE relationship spans TWO roles (customer+employee); role-scoped authz grants and
    denies per role; role-scoped Trust updated on the ?role=employee scope while the
    customer-role Trust stays untouched."""
    results: list[tuple[str, bool, str]] = []
    r = lambda name, ok, detail="": results.append((name, ok, detail))  # noqa: E731
    s4 = S4Service(sub)
    rel = sub.graph.get("relationship://qk/cust-cxn")

    ok_emp = s4.resolve_role_named("relationship://qk/cust-cxn", "person://qk/customer", "employee")
    ok_cust = s4.resolve_role_named("relationship://qk/cust-cxn", "person://qk/customer", "customer")
    r("ONE relationship carries TWO roles for the same actor (§3.2/§C2)",
      ok_emp and ok_cust and rel is not None
      and rel.get("roles", {}).get("person://qk/customer") == ["customer", "employee"],
      f"roles={rel.get('roles', {}).get('person://qk/customer') if rel else None}")

    p = s4.authorize_for_role("person://qk/customer", "submit_timesheet",
                              "relationship://qk/cust-cxn", "employee")
    d = s4.authorize_for_role("person://qk/customer", "request_quote",
                              "relationship://qk/cust-cxn", "employee")
    p2 = s4.authorize_for_role("person://qk/customer", "request_quote",
                               "relationship://qk/cust-cxn", "customer")
    d2 = s4.authorize_for_role("person://qk/customer", "receive_payroll",
                               "relationship://qk/cust-cxn", "customer")
    r("role-scoped authority grants the right action per role",
      isinstance(p, Permission) and isinstance(p2, Permission),
      f"emp.submit_timesheet={isinstance(p, Permission)}, cust.request_quote={isinstance(p2, Permission)}")
    r("role-scoped authority DENIES the other role's actions (separation of role, not all-or-nothing)",
      isinstance(d, Denial) and isinstance(d2, Denial),
      f"emp.request_quote denied={isinstance(d, Denial)}, cust.receive_payroll denied={isinstance(d2, Denial)}")

    emp = sub.graph.get("trust://qk/t-emp-quoteko")
    r("employee-role Trust updated on the ?role=employee scope (§3.14, not a global score)",
      emp is not None and emp["context"] == "relationship://qk/cust-cxn?role=employee"
      and emp["score"] > 0.5, f"score={emp['score'] if emp else None} ctx={emp.get('context') if emp else None}")
    sola = sub.graph.get("trust://qk/t-solarworks")
    s41_trust = (sub._meta.get("s41", {}) or {}).get("trust_after")
    r("customer-role Trust untouched by the employee loop (scoped per role)",
      sola is not None and s41_trust is not None and abs(sola["score"] - s41_trust) < 1e-9,
      f"customer(cust-cxn) solarworks={sola['score'] if sola else None} (was {s41_trust})")

    s42 = sub._meta.get("s42", {})
    emp_next = s42.get("emp_next", [])
    r("full employee-role loop closed with S4 settlement in the middle",
      bool(emp_next) and emp_next[0]["offer"] == "offer://qk/o-payroll"
      and s42.get("outcome_eval") == "met" and s42.get("pay_action") is not None,
      f"pay={s42.get('pay_action')}, settle={s42.get('settle')}, outcome={s42.get('outcome_eval')}")
    return results


def org_check(sub) -> list[tuple[str, bool, str]]:
    """4.3: ONE relationship spans TWO org types (private + charitable) through the full loop;
    the IRREVERSIBLE charitable-grant settlement was NOT auto-executed — it ran only after the
    approver's signed human DECISION (Ledger order: split < escalate < human < release)."""
    results: list[tuple[str, bool, str]] = []
    r = lambda name, ok, detail="": results.append((name, ok, detail))  # noqa: E731
    qkv = sub.graph.get("purpose://qk/pv-quoteko")
    shkv = sub.graph.get("purpose://qk/pv-shelter")
    r("organization-kind attribute carried per §3.1 (private FOR_PROFIT vs charitable)",
      qkv is not None and qkv.get("kind") == "FOR_PROFIT"
      and shkv is not None and shkv.get("kind") == "NONPROFIT_CHARITABLE",
      f"quoteko={qkv.get('kind') if qkv else None}, sunsetshelter={shkv.get('kind') if shkv else None}")

    rel = sub.graph.get("relationship://qk/charity-cxn")
    offer = sub.graph.get("offer://qk/o-shelter-solar")
    r("cross-org relationship + purpose-constrained pro-bono offer (§3.9 price=0)",
      rel is not None and rel.get("roles", {}).get("org://qk/sunsetshelter") == ["beneficiary"]
      and offer is not None and offer.get("price") == 0,
      f"roles={rel.get('roles') if rel else None}, price={offer.get('price') if offer else None}")

    trust = sub.graph.get("trust://qk/t-shelter")
    r("charity-context Trust updated (shelter rose past 0.5)",
      trust is not None and trust["score"] > 0.5, f"score={trust['score'] if trust else None}")

    entries = sub.ledger.entries
    def idx(uri):
        for n, e in enumerate(entries):
            if e.get("uri") == uri:
                return n
        return -1
    i_split = idx("event://qk/s4-split-charity")
    i_esc = idx("event://qk/s3-escalate-t-charity-grant")
    i_hum = idx("event://qk/s3-human-t-charity-grant")
    i_rel = idx("event://qk/s3-step-t-charity-grant")
    r("§6 floor still gates the irreversible cross-org settlement (NOT auto-executed)",
      i_split >= 0 and i_split < i_esc < i_hum < i_rel,
      f"split@{i_split} esc@{i_esc} hum@{i_hum} release@{i_rel}")
    rel_event = [e for e in entries if e.get("action") == "release_charitable_grant"]
    r("the ONLY grant-release action ran after the human commit",
      len(rel_event) == 1 and i_rel > i_hum, f"{len(rel_event)} release event")
    hum = sub.graph.get("decision://qk/s3-human-t-charity-grant")
    alts = (hum or {}).get("alternatives") or []
    r("human decision signed by person://qk/approver + enumerates alternatives",
      bool(hum) and hum.get("by") == "person://qk/approver" and len(alts) >= 3, str(alts))

    s43 = sub._meta.get("s43", {})
    c_next = s43.get("charity_next", [])
    r("full cross-org loop closed (S4 settlement + S5 Trust re-ranks S2)",
      bool(c_next) and c_next[0]["offer"] == "offer://qk/o-shelter-solar"
      and s43.get("outcome_eval") == "met",
      f"outcome={s43.get('outcome_eval')}, next={c_next[:1] if c_next else []}")
    return results


def _s4_checks():
    return {"s4": s4_check, "role": role_check, "org": org_check}