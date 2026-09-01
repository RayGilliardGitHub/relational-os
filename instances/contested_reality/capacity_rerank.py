"""capacity_rerank.py — SPRINT 32 (new, additive): the capacity-constrained RE-RANK of the §7L Q8
recommendation for the machine, BY THE FROZEN `rank` UTILITY, as an EXPLICIT authorized POLICY step.

The default advisory path (Sprint 31's reason-not-choice inventory) NEVER re-ranks: the engine's
`cockpit_s7l` q8 `capacity_constraint` block labels — even the recommended option —
`capacity_infeasible` from recorded data, but the Q8 recommendation provably stays the frozen
`rank` output (the §6 human always rules). This module is the SEPARATE, deliberate step the Sprint
31/30 prompt explicitly asked for: when an org's machine-eligible best is `capacity_infeasible`
from RECORDED per-option `capacity_requirements`, and BY AUTHORIZED POLICY the machine may pick a
replacement, compute the highest-utility option that is neither floor-gated nor
`capacity_infeasible` — a deterministic next-best-not-infeasible rule by the frozen `rank` utility.

Additive + generic + deterministic + honest:
- NO change to adjudication_engine.py (hash a60f8f7… stays). Reuses ONLY the engine's public,
  importable surface: `cockpit_s7l` (the recorded `capacity_constraint` block it renders from the
  org's own graph), `rank` (frozen), and the recorded `authority://` capacity fields.
- Never invents a requirement or a capacity figure; never a probabilistic/stochastic call; never
  the wall-clock (identical inputs -> identical block).
- Respects the §6 floor: a floor-gated option is NEVER auto-picked.
- When every capacity-consuming (non-baseline) option is infeasible or floor-gated, it falls back
  to the do-nothing/UNRESOLVED baseline and SAYS so (`replacement_is_baseline` = True).
- The advisory q8.recommendation is never overwritten here — the re-ranked selection is reported as
  DATA in the returned block (`replacement`), and the demo surfaces it plainly alongside the
  engine's unchanged advisory recommendation.

Reason-not-choice is preserved: on the DEFAULT path the marker stays a REASON never a CHOICE; the
re-rank is the new, named, authorized capability layered on top (a POLICY/user decision), proven
distinct by `needed=False` orgs being byte-identical to `cockpit_q7q8`.

~$0, deterministic local Python, frozen 49 $defs / URI cap / SPEC v0.22. No new noun.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INSTANCES = HERE.parent
S5 = INSTANCES.parents[0] / "sprints/sprint-5/artifacts"
for _p in (str(HERE), str(INSTANCES), str(S5)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import adjudication_engine as eng  # noqa: E402

# The recorded descriptors the re-rank reads (the SAME data the engine's advisory capacity block
# renders) — named so every re-rank traces to a recorded number.
RECORDED_DESCRIPTORS = ["capacity", "capacity_requirements"]
POLICY_TEXT = (
    "capacity-constrained re-rank for the machine (authorized POLICY step): from the frozen rank "
    "utility ordering, the highest-utility option that is neither floor-gated nor capacity_infeasible"
)


def capacity_rerank(cfg: dict, sub, *, library: dict | None = None) -> dict:
    """Compute the authorized capacity-constrained re-rank for one configured org.

    Reads the SAME recorded capacity data the engine renders on the advisory path: the
    `capacity_constraint` block on the engine's `cockpit_s7l` q8 (present only when the org records a
    numeric authority `capacity` AND a band AND a threshold), whose `options_flagged` maps each
    capacity-consuming option to `capacity_infeasible` / `capacity_risk` from recorded per-option
    `capacity_requirements` vs `available = capacity.value - capacity.load`.

    Returns a deterministic dict (never None for a capacity-recorded org; for an org with no
    recorded capacity the runnable-check is trivially `needed=False` with an honest reason):
      needed                    bool  — True when the machine-eligible best is capacity_infeasible
                                        AND a runnable replacement exists under the frozen rank order
      prior_machine_best        str   — the frozen `rank`/`machine_eligible_best` output (unchanged)
      prior_best_capacity_flag  str   — 'capacity_infeasible' | 'capacity_risk' | None
      recorded_descriptors      list  — the recorded data the re-rank used
      available_capacity        num|None — recorded capacity.value − recorded load (same unit)
      per_option_requirements   dict  — recorded {option: requirement}
      replacement               str   — the re-ranked selection (highest non-infeasible non-gated);
                                        == prior_machine_best when needed=False
      replacement_is_baseline   bool  — True only when every capacity-consuming option is
                                        infeasible/floor-gated, so it fell back to do-nothing/UNRESOLVED
      all_capacity_consuming_infeasible bool — True when no runnable non-baseline remains
      floor_respected           bool  — True (a floor-gated option is never auto-picked)
      policy                    str   — the explicit POLICY stance
      reason / why / note       str   — plain-language honesty about prior-infeasible -> replacement
    Deterministic: depends only on cfg + sub graph + optional data library.
    """
    c = eng.cockpit_s7l(cfg, sub, library=library)
    q7, q8 = c["q7"], c["q8"]
    cc = q8.get("capacity_constraint")
    prior = q7["machine_eligible_best"]
    baseline = q7["baseline"]

    if not isinstance(cc, dict):
        return {
            "needed": False,
            "prior_machine_best": prior,
            "prior_best_capacity_flag": None,
            "recorded_descriptors": [],
            "available_capacity": None,
            "per_option_requirements": None,
            "replacement": prior,                      # unchanged
            "replacement_is_baseline": False,
            "all_capacity_consuming_infeasible": False,
            "floor_respected": True,
            "policy": POLICY_TEXT,
            "reason": "no recorded authority capacity -> nothing to capacity-constrain; "
                      "the advisory Q8 recommendation is unchanged.",
            "why": "no recorded capacity", "note": "",
        }

    flags = cc.get("options_flagged") or {}
    reqs = cc.get("per_option_requirements") or {}
    avail = cc.get("available_capacity")
    prior_flag = flags.get(prior)

    if prior_flag != "capacity_infeasible":
        # prior best is runnable (or no flag) -> NOTHING to re-rank; Q8 stays the frozen rank output.
        return {
            "needed": False,
            "prior_machine_best": prior,
            "prior_best_capacity_flag": prior_flag,
            "recorded_descriptors": list(RECORDED_DESCRIPTORS),
            "available_capacity": avail,
            "per_option_requirements": dict(reqs) if reqs else None,
            "replacement": prior,                      # UNCHANGED
            "replacement_is_baseline": False,
            "all_capacity_consuming_infeasible": False,
            "floor_respected": True,
            "policy": POLICY_TEXT,
            "reason": "the machine's prior best is runnable under recorded capacity "
                      f"(flag={prior_flag!r}) -> no re-rank needed; the advisory Q8 recommendation "
                      "is unchanged.",
            "why": "prior best runnable", "note": "",
        }

    # The machine's prior best IS capacity_infeasible -> BY AUTHORIZED POLICY pick the next-best.
    # Walk the frozen rank utility ordering; the highest-utility option that is neither floor-gated
    # nor capacity_infeasible is the replacement. The do-nothing/UNRESOLVED baseline is never gated
    # and never capacity_infeasible, so it is always reachable as the honest last-resort fallback
    # when EVERY capacity-consuming (non-baseline) option is infeasible or floor-gated.
    replacement = None
    baseline_fallback = None
    nonbaseline_runnable = False
    for rk in eng.rank(cfg):                    # frozen rank utility ordering
        opt = rk["option"]
        if rk["floor_gated"] or flags.get(opt) == "capacity_infeasible":
            continue                            # floor-gated never auto-picked; infeasible skipped
        if opt == baseline:
            baseline_fallback = opt             # remember do-nothing/UNRESOLVED as the last resort
            continue
        replacement = opt                       # a runnable non-baseline beats any later option
        nonbaseline_runnable = True
        break
    if replacement is None:
        replacement = baseline_fallback if baseline_fallback is not None else baseline
    all_blocked = not nonbaseline_runnable

    prior_req = reqs.get(prior) if reqs else None
    why = (
        "the recorded capacity says the machine's prior best cannot run under capacity: "
        f"prior best `{prior}` records a per-option requirement of {prior_req} against an "
        f"available capacity of {avail} (recorded capacity VALUE minus recorded load, same unit), "
        f"so the forward advisory engineered it `capacity_infeasible`; BY AUTHORIZED POLICY the "
        f"machine picks the highest-utility option that is neither floor-gated nor "
        f"capacity_infeasible -> `{replacement}`."
    )
    return {
        "needed": True,
        "prior_machine_best": prior,
        "prior_best_capacity_flag": prior_flag,
        "recorded_descriptors": list(RECORDED_DESCRIPTORS),
        "available_capacity": avail,
        "per_option_requirements": dict(reqs) if reqs else None,
        "replacement": replacement,
        "replacement_is_baseline": bool(replacement == baseline),
        "all_capacity_consuming_infeasible": bool(all_blocked),
        "floor_respected": True,
        "policy": POLICY_TEXT,
        "reason": "capacity-constrained re-rank for the machine (authorized POLICY): the recorded "
                  "capacity says the machine's prior best cannot run under capacity, so the machine "
                  "picks the highest-utility option that is not capacity_infeasible."
        ,
        "why": why, "note": "",
    }


__all__ = ["capacity_rerank", "RECORDED_DESCRIPTORS", "POLICY_TEXT"]