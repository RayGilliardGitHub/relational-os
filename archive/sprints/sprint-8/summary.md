# Sprint 8 — SUMMARY — Real-LLM agent inside the RelationalOS chain

**What was built:** a runnable, $0, reproducible demonstration that a **real local LLM agent** can live
inside RelationalOS's control architecture — reason a #8 recommendation + an evidence verification from
**live ledger evidence**, as effect-free signed `decision://` records, be **forced to a signed human
approval** before an irreversible action (provable by ledger ORDER), and **never execute nor set its own
Trust** (the deterministic S5 formula governs the score over the model-classified evidence).

## Verified commands — REAL output (all exit 0)
```
# the standalone demo (tech/VantageCloud)
cd /home/rlg/relational-os/instances/agent_demo
python3 run_agent_demo.py               -> RESULT: ALL PASS
<venv>/python conformance_agent.py      -> AGENT-DEMO CONFORMANCE: ALL PASS  (C1–C5, 69 instances)

# replicate across all 12 sector families
cd /home/rlg/relational-os/instances
python3 build_all_agents.py             -> RESULT: ALL SECTORS PASS

# non-regression
cd /home/rlg/relational-os/sprints/sprint-5/artifacts
python3 run_s5_demo.py                  -> RESULT: ALL PASS
<venv>/python run_s5_conformance.py     -> RESULT: ALL PASS
cd /home/rlg/relational-os/instances
python3 build_all.py                    -> RESULT: ALL SECTORS PASS
<venv>/python conformance_all.py        -> SECTOR CONFORMANCE: ALL SECTORS PASS
```

## What the model actually did (phi4-mini:3.8b-q8_0, local Ollama, $0)
- **#8 recommendation** from live evidence (on-time 0.5 vs 0.95; good-partner Trust 0.79 vs laggard 0.14):
  `option=re-balance to partner_good, confidence=0.85` — reasoned to the correct action.
- **Evidence verify**: `on_time=true, confidence=0.95, procedure=anchored-timestamp`.
- Both recorded as **advisory `decision://`**; §6 floor order `[30 < 31 < 32]` held; agent wrote no
  ACTION and no `trust://`; Trust moved `0.790 → 0.885` purely by the real S5 formula over the model's
  0.95 evidence degree.

## Design (additive, frozen core untouched)
- New `instances/agent_demo/` (stdlib Ollama adapter + prompt templates + `run_agent_sector(label)` +
  conformance gate) + `instances/build_all_agents.py`. **Zero changes** to `ros/`, schema, URI catalog,
  or the reference build — the agent rides the existing chain by the same additive-field pattern the
  brand component used (Sprint 7).

## Honest boundaries
- **Demonstrated:** a real intelligent actor is **bounded by capability+delegation, forced to the §6
  human floor in provable ledger order, and cannot move its own Trust** — the decisive differentiator,
  now with a runnable $0 proof across all 12 sectors.
- **NOT demonstrated:** routing seam, tools, memory, multi-agent, OIDC, production AI, model *accuracy*.
  The demo proves containment + auditability, not recommender quality.
- **Reliability constraint surfaced:** structured output required a strict single-line-JSON prompt; the
  looser prompt made the model return reasoned free text. On failure the code logged `_fallback` and used
  a safe default — no fabrication.

## Delivers (per the review roadmap)
- Closes the `UNK` on `RELATIONALOS-INDISPENSABILITY-TEST.md` Problems 6 & 8 (AI-governance
  differentiator).
- Executes `COMPLETENESS-GAP-ANALYSIS.md` exec-summary item 6-1: "run one real LLM agent inside the
  chain."
- Demonstrates the control architecture can carry a real model — the single strongest claim in the
  indispensability test.

## Key files
- `instances/agent_demo/docs/AGENT-DEMO.md` — full write-up (prompts, parsed output, assertions).
- `instances/agent_demo/agent_adapter.py`, `prompts/*`, `run_agent_demo.py`, `conformance_agent.py`,
  `artifacts/` (fixtures + `model-log.json`).
- `instances/build_all_agents.py`.
- Plans/notes: `sprints/sprint-8/plan.md`, `work/1-plan.md`, `notes/findings.md`.

## Spec status
SPEC stays **v0.22** — additive demonstration only, no normative change, no bump.