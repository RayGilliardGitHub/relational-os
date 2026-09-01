# Sprint 13 — summary

**Goal.** Generalize the Sprint-12 contested-reality adjudication (which was per-scenario authored
code) into a configurable, rule-driven engine, and render the trade-off + lifecycle onto the §7L
cockpit Q7. Done — additive, frozen ontology, SPEC v0.22, ~$0.

## What was built (instances/contested_reality/)
- `adjudication_engine.py` — a **generic** engine (validates config, reconciles evidence via a named
  config-parameterized rule, ranks options from the business-model weights with the §6 floor gate,
  drives the lifecycle: claims→evidence→conflict/uncertainty→dispute OPEN→ranked options→advisory
  `decision://`→authorized human determination or UNRESOLVED→verified outcome→learning; emits C1–C5
  fixtures). Zero per-scenario code.
- `adjudication_configs.py` — two org scenarios as pure DATA: **deli** (Constellar Freight $18k
  delivery → *partial-settlement*) and **cove** (Meridian Health Plan clinical coverage →
  *step-therapy-first*), each with its own weights/options/factor-scores/floor-gate/authority and a
  thin-evidence **UNRESOLVED** sub-dispute.
- `run_adjudication_engine_demo.py` — drives BOTH orgs through the SAME engine (the generalization
  proof), asserts ALL PASS, emits fixtures + the §7L cockpit Q7 report.
- `conformance_adjudication.py` — C1–C5 over both fixtures (Sprint-0 venv).
- `decision_learning.py` — optional realized-cost / Decision-Learning: expected-vs-actual variance
  drives a clamp-bounded, additive re-weighting of the business model + a recorded `realized_cost_usd`
  on the `decision://`.
- `docs/GENERALIZED-ADJUDICATION.md` — the honest write-up + §16 verdict.

## Verified output (all exit 0, ALL PASS)
- Engine demo (both orgs): resulter `RESULT: ALL PASS` — deli → partial-settlement@0.728 (refund gated),
  cove → step-therapy-first@0.777 (both extremes gated); each also a UNRESOLVED sub-dispute; Trust
  untouched; rankings deterministic; authority preserved; decision-learning committed (deli
  variance +0.177/$6k; cove +0.078/$18k).
- `conformance_adjudication.py`: `ADJUDICATION-ENGINE CONFORMANCE: ALL PASS` (C1–C5, 49 `$defs` intact).
- **Full non-regression (all exit 0):** S5 reference demo + all-six conformance; CR dispute/interest/
  tradeoff/lifecycle demos + conformance; agent demo + conformance; sectors `build_all.py` +
  `conformance_all.py`. No reference-byte change; `ros/` untouched; `configs.SECTORS` unchanged.
- Cockpit Q7 rendered: `artifacts/adjudication/reports/cockpit-q7.{md,json}` + per-label.

## §16 verdict
Moves from **B — Partially** to **B+ — materially toward A**. The two things §16 named as missing
(configurable adjudication + §7L cockpit render) are now demonstrated by real output. Still not a
clean "A": the value model (weights + factor scores) is authored organizational judgment (§7K.1, by
design) and a genuinely new evidence-combination rule needs a new rule function (only one rule is
parameterized) — the user-authorable dispute-DSL is the natural Sprint 14 step.

## Open issues / next work
- A user-authorable dispute DSL: config-authorable rule functions (not just rule parameters).
- Optionally: thread the learned weights back into a third demo org to show drift explicitly.

## Docs touched (no SPEC bump)
- `contested_reality/docs/GENERALIZED-ADJUDICATION.md` (new)
- `instances/README.md` (Sprint-13 entry)
- `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` ("Update after Sprint 13")
- `sprints/sprint-13/plan.md`, `work/1–4-plan.md`, `notes/findings.md`, `summary.md`
- `sprints/sprint-14/PROMPT.md` (next prompt)