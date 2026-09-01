# Sprint 8 — Findings (real-LLM agent demo)

Date: 2026-09-01.

## What worked
- A **real local LLM** (phi4-mini via Ollama, localhost:11434, ~$0) produced a structured #8
  recommendation and an evidence-verify classification from **live ledger evidence**, both as
  effect-free signed `decision://` records.
- The **§6 human floor was enforced by ledger order** (escalate < human < release = 30 < 31 < 32) even
  with the real agent present; the agent never wrote an ACTION and never wrote a `trust://` object.
- The deterministic `S5.update_trust` formula governed the score over the model-classified evidence
  (model classifier, formula decides). All 12 sectors ran the pathway green; conformance C1–C5 and the
  reference/sector builds did not regress.

## Decisions taken
1. **Additive overlay, not a new subsystem.** The agent rides the existing sector_scene chain and
   writes only `decision://`; zero changes to `ros/`, schema, URI catalog, reference build. Same pattern
   as the brand component (Sprint 7) — this is the project's established way to extend without touching
   the frozen core.
2. **Advisory-only boundary as a *tested property*.** Instead of asserting "the agent never acted," the
   runner asserts "the two AI overlay events produced no ACTION and no trust write" — this is the honest,
   correct formulation (the base scene legitimately has the *delegated* ops agent execute a human-approved
   ACTION).

## Pitfalls discovered (worth recording)
1. **Structured output is prompt-sensitive.** A loose "return a JSON object" prompt made phi4-mini return
   reasoned free text (invalid JSON); a **strict single-line-JSON** instruction ("EXACTLY one JSON object,
   no markdown, no prose, one logical line") reliably returned parseable JSON. Lesson: for local small
   models, the structured-output contract must be enforced in the prompt, and the parse must still
   fall back + log rather than fabricate.
2. **Modlulename shadowing footgun reappeared**; also `S2Service.Match` uses `.offer_uri`, `S5.capture`
   returns (evidence, bool). (Already in the relational-os skill's footgun list; re-confirmed here.)
3. **sys.path for a one-dir subpackage**: `build_all_agents.py` (run from `instances/`) could not import
   `agent_adapter` until `run_agent_demo.py` added its own dir to `sys.path`. Keep subpackage modules
   self-anchored via `Path(__file__).resolve().parent`.

## Honest limits (unchanged from scope)
- First real agent run at **reference scale, one operating loop** (delivery exception). No routing seam,
  tools, memory, multi-agent, OIDC, or production AI.
- **No accuracy claim** — the demo proves containment + auditability, not that the model is a good
  recommender. When the model failed structured output (loose prompt), the code logged `_fallback` and
  used a safe default — no fabrication.

## Spec impact
**None.** SPEC stays v0.22 — this is an additive demonstration, no normative change, no version bump.