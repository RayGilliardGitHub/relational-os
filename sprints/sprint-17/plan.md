# Sprint 17 — Decision Learning at the reconciliation layer: the learned rule, honest + additive

**Prompt:** `sprints/sprint-17/PROMPT.md` (read first, in full).
**Baseline:** Sprint-16 state verified green (rule_library / authoring / comparison / adj_engine,
the 4 prior CR demos + conformances, conformance_adjudication 13 labels, sectors build_all +
conformance_all, S5 reference + conformance, agent demo + conformance — all exit 0).
**Invariants:** SPEC hash `d10f00107b5d7eb4` (v0.22), schema json hash `7fc38c8c…` (49 `$defs`),
`ros/` + schema source git-clean. Do not touch these.

## Goal
Turn Sprint 13's optional `decision_learning.py` into an honest **learning step over the
reconcile RULE**: define what "a better reconciliation rule" means from RECORDED, realized outcomes
(not hindsight on the same case), learn one rule parameter (`threshold`) as an additive,
clamp-bounded, evidence-gated update, and prove it is **contained** (no Trust move — S5 only; no
human-authority lowering — determination_policy intact; ledger append-only — no rewrite; explicit
bound). Learning feeds the RULE LIBRARY (a new named spec an org can reuse on a SECOND, distinct
dispute). Render a §7L Q7/Q8 cockpit line. Decide the honest §16 verdict: genuine learning vs
**calibrated re-authoring** (a rule author updating a parameter from outcomes).

## Key facts that shape the design (verified from source + schema)
- `rule://` → `Rule` $def (required `[uri, kind, text]`; kind enum incl. `PROCEDURE`; envelope
  `additionalProperties:true`). I carry the learned reconcile rule there as kind=`PROCEDURE` with
  additive learned-param fields. `policy://` → `Policy` (required `[uri, condition, action]`) is the
  other catalog option; not needed here. **No new noun.**
- `Decision` $def required `[uri, by, authority]`, has `rules_applied` (array of uri) + additive
  envelope → the reconcile-learning decision records + references the learned `rule://`.
- The engine `reconcile` accepts either a registry `rule` name or a `rule_spec` dict; `rule_spec` is
  plain data (`compile_rule_spec` returns `dict(spec)` preserving extra fields) → an additive
  `learned_threshold` field rides cleanly on the spec.
- `RULE_LIBRARY` is a mutable dict in `adjudication_configs.py`; reusing = passing the SAME dict by
  reference inside `reconcile={"rule_spec": RULE_LIBRARY[name], ...}` (identity proof).
- `Graph.get()` takes ONE positional arg; `evidence` refs are ARRAYS; merge-not-replace
  `{**graph.get(u), ...}`; C2 RFC3339 temporal-suffix trap (avoid `*_at/time/due/since` keys on
  additive fields); C5 state-machine tables must be legal walks (engine already emits legal ones).
- Runner CWD-sensitivity: run from `instances/contested_reality/`. Conformance = Sprint-0 venv.

## Build steps (each preceded by a `work/<n>-plan.md`)
1. **Config data** (`adjudication_configs.py`, additive): three org configs
   – `INSPECT_BATCH_A` (label `inspect-learn-a`, learning episode: winning claim support 0.97),
   – `INSPECT_BATCH_B` (label `inspect-learn-b`, SECOND distinct predicate set: winning claim
     support 0.93), with distinct claims/evidence/dispute (no re-run of the same case).
   These use the existing engine unchanged (data only).
2. **`reconcile_learning.py`** (new, additive, pure stdlib): `learn_threshold(prior_threshold,
   realized_value, learning_rate, lo, hi, eps) -> {threshold, delta, changed, bound, why}` and the
   library-feeding helper that turns a learned update into a NEW named `RULE_LIBRARY` spec dict
   (`aggregate=max` + additive `learned_threshold`/`calibrated_from`/`bound`/`why`) + the signed
   append-only record helper (new `rule://` object kind=PROCEDURE + signed `event://{L}/reconcile-learning`
   must be `decision://{L}/reconcile-learning` with `[uri,by,authority]` + `rules_applied`).
   Deterministic (all inputs explicit), clamp-bounded, evidence-gated (`|delta|>=eps`). It never
   touches Trust, never rewrites the ledger, never edits any `determination_policy`.
3. **`run_reconcile_learning_demo.py`** (exit 0 = ALL PASS):
   - Episode A under the initial threshold t0=0.95 (registry `best-reliability-threshold`); record the
     realized outcome value on the dispute additively + a signed event.
   - Learning step: `learn_threshold(0.95, 0.90, 0.8, 0.55, 0.95)` → t' = 0.91, changed=True. Assert
     determinism (recompute). Add the learned spec to `ac.RULE_LIBRARY` + record the signed event.
   - Episode B (distinct dispute) driven with the LEARNED rule: support 0.93. Assert old-t0 would be
     UNRESOLVED (0.93<0.95) and learned-t' DETERMINES → real verdict flip across two distinct disputes.
   - Cross-org reuse: drive `deli-learn` with the SAME learned spec dict (`is`-identity) → library,
     not a one-case patch.
   - Containment contract assertions (real): (a) all trust:// scores stay 0.80 (S5 untouched);
     (b) determination_policy byte-identical before/after learning + determination carries its authority;
     (c) ledger append-only: event count grows, prior events byte-identical (snapshot diff);
     (d) t' in [lo,hi], recompute-identical. Plus no new noun, SPEC v0.22, 49 `$defs`.
   - §7L Q7/Q8 cockpit line: report naming ACTIVE rule, its source (registry/library/learned), and
     whether a learning step changed it this run + why (evidence-gated reason).
   - emit fixtures for the three new labels; render the report.
4. **`conformance_adjudication.py`**: extend labels by 3 (`inspect-learn-a`, `inspect-learn-b`,
   `deli-learn`) → 16 labels. C1–C5 must pass over the new fixtures.
5. **Docs + non-regression + verdict** (additive only, no SPEC bump).

## Definition of Done
New runner ALL PASS; 16-label conformance ALL PASS, 49 `$defs`; full non-regression green (Sprint-16
set unchanged); SPEC v0.22; `ros/`+schema clean; honest §16 verdict (expected: **calibrated
re-authoring**, not autonomous learning). Write `docs/RECONCILE-LEARNING.md`, `instances/README.md`
entry, STRESS-TEST note, RULE-LIBRARY additive appendix, `summary.md`, `notes/findings.md`, and the
next prompt `sprints/sprint-18/PROMPT.md`.