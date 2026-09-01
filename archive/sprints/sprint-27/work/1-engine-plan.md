# Sprint 27 — work/1-engine-plan.md

**Goal.** Additive capacity-constraint marker on the Q7/Q8 trade-off, derived from recorded numbers
only, without touching frozen functions or altering the Q8 ranking.

## Steps
1. Add `_capacity_reason(capacity_obj, bh, direction)` — the shared deterministic rule returning
   `(label, flag)` (headroom / at-capacity / deficit), extracted from the Sprint-26 rule.
2. Refactor the Sprint-26 Q9 `capacity_planning_attention` block inside `cockpit_s7l` to call
   `_capacity_reason` (must yield BYTE-IDENTICAL `_flag`/`_label`, hence identical `why`/`flag`).
3. Add a Sprint-27 block after the Q9 capacity blocks, before Q10:
   ```
   if capacity_recorded and q9_capacity and bh is not None and fca.get("threshold") is not None:
       label, _ = _capacity_reason(q9_capacity, bh, fca.get("direction","higher-is-better"))
       flags = {}
       if label != "headroom":
           for o in cfg.get("options", []):
               if o != q7.get("baseline"):
                   flags[o] = "capacity_risk"   # never capacity_infeasible (no recorded per-option req)
       cc = {"recorded_capacity": "<value> <unit> (load <load>)",
             "horizon_band": {"low": bh["low"], "high": bh["high"]},
             "reason": label,
             "options_flagged": flags,
             "flag": label != "headroom",
             "note": "derived capacity-constraint reason from recorded numbers only — never an "
                     "invented figure, never a directive, never an option removal; the Q8 "
                     "recommendation is UNCHANGED (the §6 human always rules)"}
       q7["capacity_constraint"] = dict(cc)
       q8["capacity_constraint"] = dict(cc)
   ```
4. `capacity_constraint` present ONLY on the capacity-recording org (all keys C2-safe: nothing ends in
   `at|time|deadline|expires|expiry|effective|due|since`).
5. `render_cockpit_s7l` needs NO change (its Q7/Q8 lines are generic; the new block is dict-only).

## Verify (after edit)
- `python3 -c "import ast; ast.parse(open('adjudication_engine.py').read())"` passes.
- Sprint-26 runner `run_forecast_horizon2_demo.py` still ALL PASS (global byte-identity of Q3/Q9).
- Q8 `capacity_constraint.reason` == Q9 `capacity_planning_attention` label (by construction via the
  shared helper).