# SPRINT 11 — Summary: the optimizer / business-model (trade-off engine)

## What was built (additive only; no new noun; 49 `$defs` intact; SPEC stays v0.22)
A runnable **trade-off / cost-benefit scoring engine** that answers "what does *better* mean here?"
(SPEC §7K.1) and closes Scenario-B gap#3 in `STRESS-TEST-SCENARIOS.md` — the last honest gap left
by Sprints 9/10.

- **`instances/contested_reality/tradeoff_model.py`** — pure, deterministic, stdlib-only utility
  engine. For each adjudication option it computes utility = documented weighted sum of five factors
  (SLA compliance 0.45, employee-interest 0.20, manager/staffing 0.15, leave utilization 0.10,
  coordination cost 0.10) − a §6 floor penalty for an irreversible/unknown-cost option. `do-nothing`
  is always an explicit baseline; weights ARE the business model, the ranking is then computed.
- **`run_tradeoff_demo.py`** — the conflicting-interest scene (Sprint-10 numbers) → computed ranking
  → human determines WITH it in view → the §6 floor binds an unknown-coverage variant → human
  authorizes **UNRESOLVED** (Trust untouched) → an optional **real local model advisory** (Sprint-8
  `agent_adapter`) proven contained. The trade-off rides the `case://` as an additive object in the
  **frozen `Recommendation` $def shape** (incl. machine-readable `json` ranking).
- **`conformance_tradeoff.py`** — C1–C5 gate over `artifacts/tradeoff/fixtures`.
- **Docs:** `docs/TRADE-OFF-IMPLEMENTATION.md`, `instances/README.md` (Sprint-11 bullet),
  STRESS-TEST-SCENARIOS.md ("Update after Sprint 11"), this summary + `notes/findings.md`,
  `sprints/sprint-12/PROMPT.md`.

## Rendered ranking (real output, coverage KNOWN) + chosen determination
```
0.760  remote-with-coverage-plan   <- human determination follows the machine's top (informed)
0.690  side-manager
0.640  do-nothing                  (baseline — always beats breaching the SLA)
0.340  side-employee
```
The machine's computed top equals the Sprint-10 human's hand-chosen defensible middle — the
defensibility is now **computed from the org's own numbers**, not authored. Under UNKNOWN coverage
the §6 floor gates all three staff-changing options → human authorizes **UNRESOLVED** /
`INSUFFICIENT_EVIDENCE`; Trust untouched.

## Advisory model (real output)
```
[advisory] real local model phi4-mini:3.8b-q8_0 pick: 'do-nothing' (confidence 0.7); advisory only
```
Recorded as an effect-free `decision://`; proven unable to set the determination or write Trust.

## Verified commands (all exit 0 = ALL PASS)
From `instances/contested_reality/`: `python3 tradeoff_model.py`; `python3 run_tradeoff_demo.py`;
`<sprint-0-venv>/python conformance_tradeoff.py` → C1–C5, **49 $defs, 17 instances**.
Non-regression: `run_dispute_demo.py` + `conformance_dispute.py`, `run_interest_conflict_demo.py` +
`conformance_interest.py`; from `instances/`: `build_all.py`, `conformance_all.py` → ALL SECTORS
PASS; `agent_demo/run_agent_demo.py` → ALL PASS; `sprint-5/artifacts/run_s5_demo.py` → ALL PASS.
Core integrity: `git status` shows `ros/`, schema, SPEC.md, `configs.py`, `sector_scene.py`
**untouched**.

## Honest verdict
The trade-off is **semi-computed**: the *ranking* is computed deterministically from recorded
constraints/evidence, but the *weights* are the org's stated business model (authored) — exactly the
split §7K.1 describes. This genuinely improves defensibility (the determination is informed by a
reproducible, auditable trade-off from the org's own numbers, and a different weight vector is a
different auditable business model). What cannot yet be computed purely from data is the value
system itself — that needs recorded realized-cost outcome histories (see findings). No fabrication;
all output captured from real runs.

## Open issues
- Weights are authored, not learned (needs a per-determination `realized_cost`/`outcome_value`
  back-fill on `decision://` — additive — to fit/evaluate weights over time).
- Trade-off not yet rendered on the §7L cockpit Q7 surface (a natural next step).