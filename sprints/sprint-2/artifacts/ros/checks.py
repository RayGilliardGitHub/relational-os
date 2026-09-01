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


ALL_CHECKS = {"s1": s1_check, "roundtrip": roundtrip_check, "s5": s5_check}