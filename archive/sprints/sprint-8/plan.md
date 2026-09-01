# AGENT DEMO — PLAN — Real-LLM-Agent inside the RelationalOS chain

Full scope: `/home/rlg/Downloads/completeness-review/SCOPE-REAL-AGENT-DEMO.md`. This is the
plan gate (PROTOCOL: write first, single-threaded, real tool output only).

## Objective
Demonstrate that a **real local LLM agent** can: (a) produce the #8 recommendation **reasoned from
live ledger evidence**; (b) classify evidence for `S5.verify`; (c) do both ONLY as effect-free
`decision://` records (advisory); (d) be forced to a signed human approval before an irreversible
action, provable by ledger ORDER (escalate < human < release); (e) leave a tamper-evident audit
trail; (f) never inflate its own Trust (update_trust stays deterministic on the model-classified
evidence). Zero change to `ros/`, schema, URI catalog, or the reference build.

## How it works (additive, rides the existing scene)
Reuse the existing `sector_scene.build_scene` to produce the full verified delivery-exception
scene (which already contains the §6 floor in correct order). THEN run an **agent overlay** on the
same instance that takes the real model's judgement for the recommendation and for verification,
records each as signed `decision://`, and asserts the control properties. This keeps the verified
`ros/` chain untouched while the model genuinely reasons from that scene's ledger.

## Sub-sprints
1. **Plan gate** (this file + `work/1-plan.md`).
2. **`agent_adapter.py`** — pure-stdlib Ollama client (urllib), JSON structured output, max_tokens
   ≥2048, deterministic tier, safe fallback + explicit log on malformed output. (test with a live call.)
3. **Prompts** — `recommend.json` (evidence-driven #8: options, rationale, confidence 0–1, risk)
   and `verify.json` (on-time/late classification + confidence). Versioned templates.
4. **`run_agent_demo.py`** — build `tech` scene; inject model → `decision://<L>/agent-recommend`
   (advisory) and `decision://<L>/agent-verify`; run deterministic `update_trust` on the model's
   classified evidence; assert: agent decision is effect-free (no ACTION by agent), §6 ordering
   `escalate < human < release` holds, Trust update used the deterministic formula. Emit fixtures.
5. **Conformance + replicate** — `conformance_agent.py` (C1–C5 gate over emitted fixtures) +
   `build_all_agents.py` (run the agent pathway across all 12 sectors, ALL PASS).
6. **Non-regression** — reference `run_s5_demo.py`/`run_s5_conformance.py` plus sector
   `build_all.py`/`conformance_all.py` still ALL PASS.
7. **Doc + findings + summary** — `AGENT-DEMO.md` (prompts, parsed model output, ledger ordering,
   honest conclusion incl. any model failure), `notes/findings.md`, `summary.md`. SPEC stays v0.22.

## Definition of Done
- Ollama (localhost, phi4-mini or similar) produces a **structured** recommendation from live
  ledger evidence; parsed + validated; recorded as signed `decision://`.
- Same for verification classification → feeds deterministic `update_trust`; model does NOT set its
  own Trust.
- §6 floor still enforced **by ledger order** and asserted green.
- G1 run_agent_demo ALL PASS · G2 conformance ALL PASS (C1–C5) · G3 build_all_agents ALL SECTORS
  PASS · G4 reference non-regression ALL PASS · G5 sector non-regression ALL PASS.
- `AGENT-DEMO.md` states exactly what was/wasn't demonstrated; honest if the model fails structured
  output.

## Exit criteria
As above + every command's real output captured; no fabricated model text; fallback logged, not hidden.