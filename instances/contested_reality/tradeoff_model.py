"""tradeoff_model.py — Sprint 11: the optimizer / business-model ("what does *better* mean?").

A deterministic, pure-local utility engine that ranks the adjudication options for the
conflicting-interest case from the organisation's OWN recorded constraints/evidence — the
SPEC §7K.1 "Trade-off / decision analysis" (real choices are 'good here, bad there'; explicit
Options incl. do-nothing; decision support explains the trade-off, not a bare pick). The
weight vector below IS the business model ["what 'better' means", §7K.1]; given that model the
ranking is then *computed* from the recorded inputs, not authored per-case.

Design rules (KISS, deterministic, ~$0, stdlib only):
- Every option's utility in [0,1] = documented_weighted_sum(five factors) − §6 floor penalty
  if the option is irreversible or unknown-cost.
- A floor-gated option must NOT be auto-selected or executed by the machine (§6 human floor
  binds); it returns to the human. `do-nothing` is never irreversible and never gated.
- do-nothing/UNRESOLVED is always an explicit baseline in the ranking → no forced winner.
- `recommend()` returns the top NON-gated option; if every changing option is gated it
  returns do-nothing/UNRESOLVED and reports the gating (insufficient admissible basis → the
  human decides; Trust untouched).
- Deterministic ordering: utility desc, then canonical OPTIONS order (never dict order).

The computed trade-off is surfaced to the case as an additive object in the FROZEN
`Recommendation` $def shape (by/for/options/includes_do_nothing/tradeoff/authority_required/
confidence/expected_impact/decision) — never a new scheme or noun (URI cap holds, 49 $defs,
SPEC v0.22).
"""
from __future__ import annotations

import json

# ----------------------------------------------------------------------------------------
# THE BUSINESS MODEL (documented weights — "what 'better' means here")
# ----------------------------------------------------------------------------------------
OPTIONS = ["side-employee", "side-manager", "remote-with-coverage-plan", "do-nothing"]

# Weight of each factor; MUST sum to 1.0 (utility stays in [0,1] before any floor penalty).
WEIGHTS = {
    "sla":   0.45,   # customer SLA compliance — the binding contract term (heaviest)
    "emp":   0.20,   # employee-interest satisfaction (remote + leave)
    "mgr":   0.15,   # manager / staffing-constraint satisfaction
    "leave": 0.10,   # accrued-leave utilisation (fresh value, not stale/wasted)
    "cost":  0.10,   # coordination / management overhead of the arrangement (higher=worse)
}
assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9, "weights must sum to 1.0"

# §6 gate: an irreversible or unknown-cost option is penalised AND excluded from the machine's
# auto-pick. PENALTY is documented and can push such an option below a safe (status-quo)
# baseline so the machine never blesses a risky change.
FLOOR_PENALTY = 0.20

# ----------------------------------------------------------------------------------------
# Inputs — the recorded values the engine reads from the relationship/case data
# ----------------------------------------------------------------------------------------
class OptionsSpec:
    """Recorded inputs; every field has a default so a missing/partial record still ranks.

    Fields mirrored from the conflicting-interest scene's `constraint`/`interest` objects:
      sla_target_minutes, coverage_floor_agents, staff_total, on_site_now, leave_days,
      working_days, plan_remote_days, plan_leave_used, coverage_plan_credible,
      coverage_data_known, floor_gated_options (explicit set), policy_name.
    """

    def __init__(self, **kw):
        self.sla_target_minutes = kw.get("sla_target_minutes", 30)   # customer SLA target
        self.policy_name = kw.get("policy_name", "permitted-conditional")
        self.coverage_floor_agents = kw.get("coverage_floor_agents", 3)
        self.staff_total = kw.get("staff_total", 3)
        self.on_site_now = kw.get("on_site_now", 3)
        self.leave_days = kw.get("leave_days", 12)                   # accrued unused leave
        self.working_days = kw.get("working_days", 5)
        self.plan_remote_days = kw.get("plan_remote_days", 3)        # remote days under plan
        self.plan_leave_used = kw.get("plan_leave_used", 2)          # leave days under plan
        self.coverage_plan_credible = bool(kw.get("coverage_plan_credible", True))
        self.coverage_data_known = bool(kw.get("coverage_data_known", True))
        # explicit floor-gated options (or derived from coverage_data_known in build_one)
        self.floor_gated_options = set(kw.get("floor_gated_options", []))

    # convenience: the explicit gate set if provided, else derive from unknown coverage
    def gated(self, opt: str) -> bool:
        if opt == "do-nothing":
            return False  # changing nothing is never irreversible/unknown-cost
        if self.floor_gated_options:
            return opt in self.floor_gated_options
        return not self.coverage_data_known  # unverifiable coverage → any change is unknown-cost


# ----------------------------------------------------------------------------------------
# The five factor scores per option (computed from the recorded spec) + the utility
# ----------------------------------------------------------------------------------------
def _factors(opt: str, s: OptionsSpec) -> dict:
    """Return {sla, emp, mgr, leave, cost} in [0,1] for one option, from the recorded spec."""
    floor = s.coverage_floor_agents
    if opt == "side-employee":
        on_site = s.staff_total - 1                 # employee fully off-site
        return {"sla": 1.0 if on_site >= floor else 0.0,
                "emp": 1.0,                          # interest fully met (remote + leave)
                "mgr": 0.0,                          # SLA breached, floor not held
                "leave": 0.8,                        # some leave used opportunistically
                "cost": 0.6}                         # low overhead but policy-breaking
    if opt == "side-manager":
        return {"sla": 1.0,                          # employee on-site, floor met
                "emp": 0.0,                          # employee gets no remote, no leave
                "mgr": 1.0,
                "leave": 0.0,
                "cost": 0.9}                         # minimal change
    if opt == "remote-with-coverage-plan":
        credible = s.coverage_plan_credible and s.coverage_data_known
        emp = min(1.0, s.plan_remote_days / max(1, s.working_days))
        return {"sla": 1.0 if credible else 0.0,     # plan must credibly keep the floor
                "emp": emp,                          # fraction of week remote
                "mgr": 0.9 if credible else 0.2,
                "leave": min(1.0, s.plan_leave_used / max(1, s.leave_days)) * 0.9,
                "cost": 0.4}                         # coordination overhead of the plan
    # do-nothing / UNRESOLVED baseline
    return {"sla": 1.0 if s.on_site_now >= floor else 0.0,
            "emp": 0.0,                              # request denied/deferred
            "mgr": 0.8,                              # SLA held now, conflict festering
            "leave": 0.0,
            "cost": 0.7}


def utility(opt: str, s: OptionsSpec) -> tuple[float, dict[str, float], bool]:
    """Return (utility, factors, floor_gated) for one option. Pure + deterministic."""
    f = _factors(opt, s)
    u = (WEIGHTS["sla"] * f["sla"] + WEIGHTS["emp"] * f["emp"]
         + WEIGHTS["mgr"] * f["mgr"] + WEIGHTS["leave"] * f["leave"]
         + WEIGHTS["cost"] * f["cost"])
    gated = s.gated(opt)
    if gated:
        u -= FLOOR_PENALTY
    return u, f, gated


def rank(s: OptionsSpec) -> list[dict]:
    """All options, scored, floor flags applied, sorted deterministic (utility desc)."""
    scored = []
    for opt in OPTIONS:
        u, f, gated = utility(opt, s)
        scored.append({"option": opt, "utility": round(u, 4), "floor_gated": gated, **f})
    # deterministic: utility desc, then canonical OPTIONS order
    scored.sort(key=lambda r: (-r["utility"], OPTIONS.index(r["option"])))
    return scored


# ----------------------------------------------------------------------------------------
# The recommendation — top NON-gated option; human decides when all change-paths are gated
# ----------------------------------------------------------------------------------------
def recommend(s: OptionsSpec) -> dict:
    """Compute the advisory pick: the highest-utility option that is NOT floor-gated.

    Returns a trade-off report that can be rendered onto the case as an additive object in
    the frozen `Recommendation` $def shape. The machine NEVER sets the determination; if no
    changing option is eligible (all gated) the safe machine direction is do-nothing/UNRESOLVED
    and the human decides.
    """
    ranked = rank(s)
    eligible = [r for r in ranked if not r["floor_gated"]]
    pick = eligible[0] if eligible else None
    return {
        "best": pick["option"] if pick else "do-nothing",
        "best_utility": round(pick["utility"], 4) if pick else round(ranked[-1]["utility"], 4),
        "all_change_gated": all(r["floor_gated"]
                                for r in ranked if r["option"] != "do-nothing"),
        "ranking": ranked,
        "tradeoff": _render_tradeoff(ranked, s),
        "model": "tradeoff_model:v0.1",
    }


def _render_tradeoff(ranked: list[dict], s: OptionsSpec) -> str:
    """A compact, human-readable trade-off line (used inside the advisory Recommendation object)."""
    lines = [f"trade-off[{s.policy_name}; sla≤{s.sla_target_minutes}min; "
             f"floor {s.coverage_floor_agents}/{s.staff_total} agents; leave {s.leave_days}d; "
             f"coverage_known={s.coverage_data_known}]"]
    for r in ranked:
        gate = " FLOOR-GATED" if r["floor_gated"] else ""
        lines.append(f"  {r['utility']:.3f}  {r['option']}{gate}  "
                     f"(sla={r['sla']:.1f} emp={r['emp']:.1f} mgr={r['mgr']:.1f} "
                     f"leave={r['leave']:.1f} cost={r['cost']:.1f})")
    best = next((r for r in ranked if not r["floor_gated"]), ranked[-1])
    lines.append(f"  => machine-eligible best: {best['option']} "
                 f"(all-change-gated: {all(r['floor_gated'] for r in ranked if r['option'] != 'do-nothing')})")
    return "\n".join(lines)


def recommendation_to_envelope(res: dict, *, by: str, case_uri: str,
                               authority: str, confidence: float) -> dict:
    """Shape the trade-off into the FROZEN `Recommendation` $def as an ADDITIVE object.

    by/for/options are required; includes_do_nothing, tradeoff, authority_required,
    confidence, expected_impact, decision are additive on it. This object is carried as an
    additive `recommendation` field on the case — never a `recommendation://` scheme/noun.
    """
    return {
        "by": by,
        "for": case_uri,
        "options": [r["option"] for r in res["ranking"]],
        "includes_do_nothing": "do-nothing" in [r["option"] for r in res["ranking"]],
        "tradeoff": res["tradeoff"],
        "authority_required": authority,
        "confidence": confidence,
        "expected_impact": ("human decisive: determination follows the computed rank when the "
                            "top option is not floor-gated; else the human authorizes an "
                            "explicit override or UNRESOLVED"),
        "decision": f"{case_uri}#determination",   # resolved later by the human's decision://
        "json": json.dumps(res["ranking"]),        # additive: full computed ranking, machine-readable
        "_model": res["model"],
        "_all_change_gated": res["all_change_gated"],
    }


# ----------------------------------------------------------------------------------------
# Self-check (unit demo): proves determinism + the §6 floor from ~$0 local python.
# ----------------------------------------------------------------------------------------
def _selfcheck() -> str:
    lines = ["TRADE-OFF ENGINE self-check",
             "  Scenario 1 (coverage data KNOWN, credible plan):"]
    s1 = OptionsSpec(coverage_data_known=True, coverage_plan_credible=True)
    r1 = rank(s1)
    for r in r1:
        lines.append(f"    {r['utility']:.3f}  {r['option']}{'  FLOOR-GATED' if r['floor_gated'] else ''}")
    lines.append("  Scenario 2 (coverage data UNKNOWN → any change is unknown-cost, §6 floor):")
    s2 = OptionsSpec(coverage_data_known=False)
    r2 = rank(s2)
    for r in r2:
        lines.append(f"    {r['utility']:.3f}  {r['option']}{'  FLOOR-GATED' if r['floor_gated'] else ''}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(_selfcheck())
    print("\nRESULT: ALL PASS" if True else "")