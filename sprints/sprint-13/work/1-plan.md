# work/1-plan.md — configurable adjudication engine + two org scenarios

**Objective.** Build the generic, config-driven engine and prove it drives ≥2 different org
scenarios with NO code change (only config/data). Additive, frozen ontology, `adj` label,
no `ros/` change, not in `configs.SECTORS`.

## Files
| file | purpose |
|---|---|
| `instances/contested_reality/adjudication_engine.py` | generic engine + config validator + lifecycle driver |
| `instances/contested_reality/adjudication_configs.py` | two scenario configs as pure data (delivery, coverage) |
| `instances/contested_reality/run_adjudication_engine_demo.py` | runs both scenarios through the engine, asserts ALL PASS, emits fixtures |
| `instances/contested_reality/conformance_adjudication.py` | C1–C5 gate over the emitted fixtures (Sprint-0 venv) |

## The config schema (the contract the engine consumes — all data, no code)
`cfg` keys:
- `label`, `scene`, `company_name`, `ledger_name`, `deadline_ref`
- `claims`: list of ≥2 conflicting claim dicts `{uri, proposer, statement, evidence:[...]}`
- `evidence`: dict `{name: {uri, kind, source, captured_at, verity.procedure/confidence, reliability, supports:[claim_uri or None]}}`
- `options`: list of resolution option strings (must include the `unresolved`/do-nothing baseline)
- `weights`: `{factor: weight}` summing to 1.0 — THE business model (§7K.1 "what better means")
- `factor_scores`: `{opt: {factor: score}}`, scores in [0,1] — each option's modeled value per factor
- `floor_gated`: set of irreversible/unknown-cost options (§6) — never includes the unresolved baseline
- `floor_penalty`: documented scalar subtracted from a gated option's utility
- `reconcile`: `{rule: str, threshold: float, support_floor: float}` — the evidence-reconciliation rule
- `authority`: `{dispute, appeal, adjudicator_person, appeal_person}` URIs
- `interests` / `constraints`: additive blocks
- `determination_policy`: `"adopt-eligible-best"` or `"override"` + `determination` (the §6 human's
  authoritative call, declared as org policy — the engine never fabricates it)
- `unresolvable`: optional second dispute config that must resolve UNRESOLVED (insufficient basis)

## Reconciliation rule (deterministic, named, parameterized)
Rule `"best-reliability-threshold"`: a claim's support = max reliability of its supporting evidence
refs (None → 0). A claim is DISPUTED (has credible support) if support ≥ `support_floor`;
CONFLICT is detected when ≥2 rival claims are both disputed; UNCERTAINTY holds when no claim's
support ≥ `threshold` (single-scenario; the verifier can't reach CLEAR) → that dispute is UNRESOLVED.
Otherwise the claim(s) at/above `threshold` become DETERMINED.

## Engine lifecycle (generic — identical for any config)
provision → claims → evidence → reconcile(claims) → conflict/uncertainty →
dispute OPEN (additive lifecycle/epistemic/discovery) → options ranked
(utility = Σ_factor weight·score − floor_penalty if gated; do-nothing baseline never gated) →
machine-eligible pick = top NON-gated → advisory `decision://` (proves no trust write, not a
determination) → accepted human determination (policy: adopt-eligible-best or override; else
UNRESOLVED when no claim reaches threshold) → verified outcome + learning → (both) → ledger
reconstruction + fixtures. Trust object seeded up-front; engine asserts Trust unchanged.

## Assertions (ALL PASS)
- same engine object drives both scenarios (signature: `engine = AdjudicationEngine(); for cfg in
  configs: engine.run(scene_of(cfg), ...)` — literally the identical call)
- different options/weights/determinations between the two scenes
- ranking deterministic (re-run identical)
- floor-gated options excluded from machine pick; baseline (unresolved) present and never gated
- advertised determination is a non-gated option (or UNRESOLVED for the thin-evidence dispute)
- advisory wrote no `trust://`; authority preserved on every `decision://`
- TRUST unchanged by the engine
- US state machine + dispute.states fully legal for C5

## Success
`run_adjudication_engine_demo.py` → ALL PASS, exit 0; both scenes' fixtures emitted under
`artifacts/adjudication/fixtures/`.