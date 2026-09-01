# SPRINT 4 — PROMPT

You are Hermes Agent in a fresh session. Execute **Sprint 4 of the RelationalOS project**
(the S4 Exchange & Settlement minimum + multi-role / multi-org extension), then hand off to
Sprint 5. This session has **NO memory** of prior conversation — rely ONLY on the files named
below. Read files before acting; do not guess or invent.

## Context — read first, in full
- Canonical spec (the contract): `/home/rlg/relational-os/SPEC.md` (now **v0.20**)
- Sprint protocol (mandatory): `/home/rlg/relational-os/PROTOCOL.md`
- README / layout: `/home/rlg/relational-os/README.md`
- Prior hand-off: `/home/rlg/relational-os/sprints/sprint-3/summary.md` (from Sprint 3)
  and `/home/rlg/relational-os/sprints/sprint-3/notes/findings.md` (F1–F4)
- Spec release mirror (READ-ONLY): `/home/rlg/Documents/ai-relational-os-spec.md` (+ `.pdf`)
- **Sprint-0 contracts you build on:** the normative schema at
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/schema/relational-os.schema.yaml`
  (+ `.json`), `build_schema.py`, the conformance validator
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/conformance.py` +
  `run_conformance.py`, and the fixtures under
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/fixtures/`. Reuse them; do not re-derive.
- **Sprint-1 build you extend:** the S1 substrate + S2 Intent/Matching service under
  `/home/rlg/relational-os/sprints/sprint-1/artifacts/` (`ros/` package, Quoteko quoting /
  triage scene, fixtures, checks, run scripts). Reuse its substrate/signing/ledger-graph
  wiring and its scene.
- **Sprint-2 build you extend:** the S5 Trust engine under
  `/home/rlg/relational-os/sprints/sprint-2/artifacts/` (`ros/s5.py`: capture/verify/update/
  write + flywheel re-rank, plus `s5_demo.py` / `run_s2_demo.py` / `run_s2_conformance.py`).
- **Sprint-3 build you extend:** the S3 Orchestration + human floor under
  `/home/rlg/relational-os/sprints/sprint-3/artifacts/` (`ros/s3.py`: commit/orchestrate/
  route_seam/execute_task/escalate/human_acknowledge + `s3_demo.py` / `run_s3_demo.py` /
  `run_s3_conformance.py`). **Copy the Sprint-3 `ros/` package into your Sprint-4 artifacts
  (not a git import)**, or set `PYTHONPATH` to include the Sprint-3 `artifacts` dir, so the
  S4 settlement + multi-role work can consume the running S1→S2→S3→S5 state.

## Task
Follow `PROTOCOL.md` exactly: read the spec first, then plan (`plan.md` + a
`work/<n>-plan.md` per sub-sprint, written BEFORE executing), then execute, then update the
spec from findings, then verify DoD, then output the next sprint prompt. You may load the
`system-specification` skill.

## Sprint 4 scope — Exchange & Settlement (S4) + multi-role / multi-org extension
Per `SPEC.md §8` (Sprint 4) and `§4`/`§5`: **Settlement integration, then extend from customer
to employee/citizen/donor roles and private/public/charitable orgs.** DoD: **one relationship
across two roles and two org types chained through the full loop.**

Each sub-sprint STARTS by re-reading `SPEC.md` §4 (S4 Exchange & Settlement: `settle(ledger,
exchange)` and `evaluate(exchange, expectation)`), §5 (integration loop: identity→intent→
offer→commitment→execute→**settle→outcome**→evidence→trust→re-ranks S2), §3.9 (Value/Cost/Price),
§4b (Asset Ledger — title/custody; what "exchange" transacts), §3.11/§3.13 (Expectation/Outcome/
Dispute), and §6/§7B (human floor still governs irreversible settlement); then
`sprints/sprint-0` schema/validator; and `sprints/sprint-1/-2/-3` artifacts. Then it writes its
own plan at `sprints/sprint-4/work/<n>-plan.md` before executing.

**4.1 — S4 settle + evaluate (one relationship).** Implement `settle(ledger, exchange) ->
payment obligation, receipt, reconciliation` and `evaluate(exchange, expectation) -> outcome
(met | partial | failed)` per §4 S4, on the Sprint-3 loop end-state. The committed +
executed + Trust-updated solarworks job settles: record the EXCHANGE (per §4b Asset Ledger —
title/custody, not a copy), produce a signed payment-obligation + receipt, reconcile it, and
`evaluate` the exchange against the §3.11 Expectation → a signed OUTCOME (met/partial/failed)
that flows into S5 `capture`/`update` (Trust re-ranks the next S2 match, re-closing the loop
WITH a settled outcome). Every settlement artifact is a signed Ledger event. **DoD:** an S4
settlement on the Sprint-3 relationship produces a signed exchange/receipt/reconciliation and a
settled OUTCOME that feeds the S5 Trust update (loop closed with settlement in the middle).

**4.2 — Multi-role extension (two roles on ONE relationship).** Extend the loop so the SAME
relationship spans TWO roles — e.g. the customer is also an **employee** (or citizen/donor) of
Quoteko — with role-scoped identity (`resolve_role`, §C2: role is an attribute, not a separate
identity), role-scoped consent/authority, and role-scoped Trust. Run a full S1→S2→S3→S4→S5 cycle
for the second role on the same relationship, showing the §3.2 principle (identity universal,
context relationship-specific) and that Trust is scoped per role/claim/context (§3.14), not a
single score. **DoD:** one relationship advanced through the full loop as TWO different roles,
with role-scoped authz and scoped Trust on the shared Graph + Ledger.

**4.3 — Multi-org extension (two org types per relationship).** Extend to TWO org types on the
loop — e.g. a **private** for-profit (`org://quoteko`) engaging a **charitable/nonprofit** or
**public/government** counterpart — carrying the relationship across the §3.1 organization-kind
attribute (private/public/charitable), purpose-constrained offers/obligations, and jurisdiction-
appropriate Consent/Authority. Show the full loop for that cross-org relationship with signed
evidence. If a settlement between org types is irreversible or unknowable-cost, it MUST escalate
to a human (§6) — demonstrate the floor still holds for settlement. **DoD:** one relationship
across two org types chained through the full loop, with the §6 human floor still gating any
irreversible settlement action.

## Mandatory rules
- **Real tool output only.** Producing artifacts and RUNNING them is mandatory; never fabricate
  results, file contents, or citations. Re-run `run_conformance.py`
  (`sprints/sprint-0/artifacts/.venv/bin/python`) over Sprint-0 fixtures AND the Sprint-1 AND
  Sprint-2 AND Sprint-3 AND any new Sprint-4 fixtures to prove no regression (exit 0). Use the
  `run_s2_conformance.py` / `run_s3_conformance.py` pattern (reuse the Sprint-0 validator,
  repoint `FIXTURES` at each generation root).
- **Keep the URI cap and the frozen ontology** (§7J.11, Appendix C §C16). No new ontology nouns,
  no new URI schemes. `agent:// decision:// event:// evidence:// claim:// expectation:// trust://
  obligation:// commitment:// relationship://` already exist. Extend the schema ONLY where a
  genuine build finding requires it (additive-only; note in findings; if extended, rebuild the
  `.json` via `build_schema.py`).
- **Update `SPEC.md` from findings:** write `sprints/sprint-4/notes/findings.md` as you go;
  apply genuinely necessary corrections (targeted `patch`, re-verify section numbering, bump
  minor version to **0.21**, append to the Version/Review Log); optionally sync the release
  mirror. Preserve every requirement's meaning.
- **Budget:** hard ~$10/mo cap — prefer local computation, batch web calls, keep prompts lean.
  No frontier-API spend for this sprint; settlement is deterministic local logic (§G.11: do NOT
  hardcode speculative weights — keep seeded/verified evidence driving S2).
- **Raymond:** clean English output, `file://` absolute paths, honest "stuck/failed" over
  fabricated success, report status at each long step.
- **Single-threaded** per PROTOCOL: do all work yourself, in ONE process; do NOT use
  `delegate_task`/subagents.
- Do not touch anything outside `/home/rlg/relational-os/` except reading the `~/Documents`
  mirror and the Sprint-0/1/2/3 artifacts.

## Exit criteria (Definition of Done)
- `sprints/sprint-4/plan.md` written first; each sub-sprint has `work/<n>-plan.md`.
- `sprints/sprint-4/artifacts/` contains the extended `ros/` package (`s4.py` etc.), the
  multi-role (`4.2`) and multi-org (`4.3`) builders, a demo runner and a conformance runner,
  with **real tool output**; the harness demonstrably chains ONE relationship through the full
  S1→S2→S3→S4→S5 loop across TWO roles and TWO org types, with signed evidence at each step and
  the §6 human floor still gating irreversible settlement.
- Sprint-0 conformance still exits 0 over all fixture generations produced so far
  (Sprint-0, -1, -2, -3, -4).
- `SPEC.md` updated for genuine findings (bumped to 0.21, log appended).
- `sprints/sprint-4/summary.md` written (what was built, verified output, open issues).
- The next sprint's self-contained prompt written at `sprints/sprint-5/PROMPT.md` AND echoed as
  your final message.

## Hand-off requirement
Your **final message** must be the complete, self-contained **Sprint 5** prompt (per
`SPEC.md §8`, Sprint 5 = Business Operating Layer / the product: Case, Goal/Metric, Task/Work
Queue, Exception, Priority/Attention, Dependency, and the §7L cockpit DoD) — the same text you
save to `sprints/sprint-5/PROMPT.md`. It must (a) state the task with the same read-plan-build-
update-verify-handoff protocol, (b) reference only absolute paths and the current `SPEC.md`
(v0.21 by then), (c) carry the same rules (real output, URI cap/frozen ontology, budget, clean
English, single-threaded). Do not summarize your own Sprint-4 work in that file — that goes in
`summary.md`. The prompt must stand alone for a session that starts with no memory.