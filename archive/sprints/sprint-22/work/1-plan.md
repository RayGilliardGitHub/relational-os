# work/1-plan.md — Sprint 22, build step 1: the additive directional crossing

**Scope.** Extend `_forecast_closure` in `instances/contested_reality/adjudication_engine.py` ONLY.
Frozen functions untouched.

**Change 1 — read the recorded direction.**
`direction = str(fap_metric.get("direction") or "higher-is-better").strip().lower()`.
Guard: normalize `"higher-is-better"` (default) / `"lower-is-better"`; anything else → treat as
higher-is-better (documented; no wall-clock).

**Change 2 — worst per direction.**
- higher-is-better: `worst = min(projs)`
- lower-is-better:  `worst = max(projs)`
`worst_period` = the period of that worst projection (same as today).

**Change 3 — crossing per direction.**
- higher-is-better: `worst < thr`  (Sprint-21 unchanged)
- lower-is-better:  `worst > thr`

**Change 4 — attention why.** Directional wording (fall vs rise above).

**Change 5 — do-nothing summary + gap.** Gap orientation + "below recorded … by" vs "above recorded …
by" per direction; on-target "stays at/above" vs "stays at/below". Same else clause structure so the
no-data path is untouched.

**Change 6 — record direction additively** on the closure dict, `q8["forecast"]`, `do_nothing`.

**Byte-identity proof.** Default direction == higher-is-better path must produce the EXACT Sprint-21
strings. I will copy today's higher-is-better strings verbatim into the higher branch; the lower branch
is new. Verify by diffing the runner output against baseline.

**C2/temporal-key safety.** `direction` ends in neither a temporal suffix nor triggers the temporal
probe; the metric object already passes C1–C5 in Sprint 21, and will again (assert conformance on the
`deli-cost` fixtures).

**Gate before moving on:** `run_forecast_action_demo.py` still ALL PASS (byte-identical) after the
engine change, before the new runner exists.