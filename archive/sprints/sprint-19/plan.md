# SPRINT 19 — PLAN

**Goal.** Make the generic adjudication engine render the FULL §7L Q1–Q10 morning
cockpit for ANY configured org, data-only, by adding `cockpit_s7l(cfg, sub, *,
library=None) -> dict` + `render_cockpit_s7l(...) -> str` to
`instances/contested_reality/adjudication_engine.py` (the ONE permitted engine file).
Q7/Q8 delegate to the Sprint-18 `cockpit_q7q8` line by construction (strict superset).
Additive; frozen 49 `$defs`; URI cap; SPEC v0.22; `ros/` + schema untouched. ~$0.

## Why this and how (the ten questions → recorded-data evidence)
The org's own graph/ledger/config carry everything. Live source: the lifecycle events in
`sub.ledger` (Q1/Q2), the `dispute://` current state + `epistemic_state` + `verified`
(Q4/Q10), the `reconcile(...)` per-claim support (`claim_support`, `determined`,
`disputed`, `conflict`, `uncertainty`) computed from the recorded evidence (Q5), the
`claim://*.epistemic_status` recorded on the claims (Q5), the dispute `determination` /
`resolution_outcome` + recorded `evidence://<label>/learning-note` & the optional
`decision://<label>/reconcile-learning` (Q10), the org's `authority` + the obligation the
dispute is `about` (its `subject`) + the actor roster (Q9). Q6 is honest: forecast only
if a recorded realized-vs-expected series exists on the graph; for the adjudication orgs
none does → explicit "cannot forecast from recorded data". No wall-clock, no invented
numbers.

## Steps
1. **Baseline (DONE).** All 6 curated runners, `conformance_adjudication.py`, the 4 prior
   CR demos + conformances, `build_all`/`conformance_all`, S5 demo+conformance, agent
   demo+conformance — ALL PASS. Schema `7fc38c8c`, 49 `$defs`, SPEC v0.22.
2. **Implement** `cockpit_s7l` + `render_cockpit_s7l` (appended to the engine; reuse
   `_cockpit_active_rule`, `cockpit_q7q8`, `rank`, `machine_eligible_best`,
   `render_tradeoff`, `reconcile`). Q7/Q8 = the Sprint-18 q7/q8 blocks verbatim.
3. **Runner** `run_cockpit_s7l_demo.py`, exit 0 = ALL PASS. Drives deli (registry) +
   inspect-learn-b (learned-this-run, reconcile-learning recorded on ITS OWN ledger) +
   deli-learn (learned, not-this-run) + inspect-corroboration (rule-library). Asserts
   (a) all ten Q present w/ required evidence, (b) Q7/Q8 == `cockpit_q7q8` on same org,
   (c) deterministic on re-run, (d) agreement with Sprint-16/17/18 report lines,
   (e) Q5 epistemic + Q10 verified/learning from real graph/ledger, (f) Q6 no-fabrication.
   Emits `cockpit-s7l-engine.{md,json}` report + fixtures.
4. **Verify** non-regression: rerun the 6 curated runners + conformance + sector + S5 +
   agent; deli/cove byte-identical up to the clock (strip timestamps, diff two runs).
5. **Docs** (no SPEC bump): `docs/ENGINE-S7L-COCKPIT.md` (new) + additive appendix in
   `docs/ENGINE-Q7Q8-COCKPIT.md`; `instances/README.md` Sprint-19 entry; append
   "Update after Sprint 19" to `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`.
6. **Summary** `sprints/sprint-19/{summary.md,notes/findings.md,plan.md,work/*.md}`; write
   `sprints/sprint-20/PROMPT.md`; final message per PROMPT hand-off.

## Verification / DoD
- New runner exit 0 ALL PASS with assertions a–f.
- Full non-regression exit 0 everywhere; deli/cove byte-identical up to clock; schema
  `7fc38c8c`, 49 `$defs`, SPEC v0.22, `ros/` untouched, no new noun.

## Footguns to respect
- Only modify `adjudication_engine.py` (append), never rewrite the frozen functions.
- `Graph.get` one-arg + `(graph.get(u) or {})`; `evidence`/`rules_applied` are ARRAYS;
  MERGE (spread) never REPLACE; no additive field key ending in `at|time|deadline|expires|
  expiry|effective|due|since` (C2 temporal-suffix trap); `eng.reconcile(sub, cfg)` ARG
  ORDER; `[0]`-index `parents` for the Sprint-0 path if needed; runner is CWD-sensitive
  (cd into `instances/contested_reality`); venv python for conformance, python3 for demos.