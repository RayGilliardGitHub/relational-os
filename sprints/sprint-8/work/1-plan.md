# AGENT DEMO — SUB-SPRINT 1 plan — planning gate

Everything below is set before code. Per PROTOCOL, this precedes the build.

## What runs first (verification anchor)
- Start from the verified baseline (already green from the completeness work):
  `cd instances && python3 build_all.py` → ALL SECTORS PASS; conformance_all → ALL PASS.
- Confirm Ollama is up + `phi4-mini` responds (done in scope: returned `OK`).

## Build order
1. `instances/agent_demo/agent_adapter.py` — pure-stdlib HTTP client to
   `POST localhost:11434/api/chat` (or /generate), asks for JSON, parses, schema-validates,
   max_tokens≥2048, fallback on malformed/empty with explicit log. Offer `build()` + `chat_json()`.
2. `instances/agent_demo/prompts/recommend.json` + `verify.json` — evidence-driven templates.
3. `instances/agent_demo/run_agent_demo.py` — imports `sector_scene`+`configs`, builds the `tech`
   scene, then runs the agent overlay:
   - read live evidence (project_on_time, trust map, case exception, options) from the built scene
   - call model → parse recommendation → record `decision://tech/agent-recommend` (signed,
     advisory, effect-free)
   - call model → classify rally evidence → record `decision://tech/agent-verify`; feed
     `S5Service.verify`-style degree into the deterministic `update_trust` on the rally outcome
   - assert: (i) agent recorded only decision:// (no ACTION, no trust write by agent);
     (ii) §6 floor order escalate < human < release; (iii) trust-update is the deterministic
     formula result; (iv) model's confidence is a real float in [0,1].
   - emit fixtures/ledger/graph.
4. `instances/agent_demo/conformance_agent.py` — Sprint-0-venv C1–C5 gate over emitted fixtures.
5. `instances/build_all_agents.py` — run the model pathway for every `configs.SECTORS` label,
   ALL PASS or FAILURES.

## Verify (all real output)
G1 `cd instances/agent_demo && python3 run_agent_demo.py` → RESULT ALL PASS
G2 `cd instances/agent_demo && <venv>/python conformance_agent.py` → C1–C5 ALL PASS
G3 `cd instances && python3 build_all_agents.py` → ALL SECTORS PASS
G4 `cd sprints/sprint-5/artifacts && python3 run_s5_demo.py` + venv run_s5_conformance.py → ALL PASS
G5 `cd instances && python3 build_all.py` + venv conformance_all.py → ALL SECTORS PASS
G6 (appendix) temperature sweep note + malformed-fallback log, recorded honestly

## Exit criteria
- A real model produced the #8 recommendation from live ledger evidence, recorded as decision://
  with its own confidence.
- §6 floor enforced by ledger order; irreversible action did not run without the human decision.
- Update_trust used the deterministic formula over model-classified evidence (model never set its own rank).
- G1–G5 all exit 0; AGENT-DEMO.md written with prompts + parsed output; SPEC stays v0.22.
- If the model fails structured output: fallback logs + summary records the honest failure instead
  of fabricating success.