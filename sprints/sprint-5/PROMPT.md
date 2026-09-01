# SPRINT 5 — PROMPT

You are Hermes Agent in a fresh session. Execute **Sprint 5 of the RelationalOS project**
(the S5… no — the **Business Operating Layer**, the product: Case, Goal/Metric, Task/Work
Queue, Exception, Priority/Attention, Dependency, and the §7L cockpit), then produce the
final hand-off. This session has **NO memory** of prior conversation — rely ONLY on the
files named below. Read files before acting; do not guess or invent.

## Context — read first, in full
- Canonical spec (the contract): `/home/rlg/relational-os/SPEC.md` (now **v0.21**)
- Sprint protocol (mandatory): `/home/rlg/relational-os/PROTOCOL.md`
- README / layout: `/home/rlg/relational-os/README.md`
- Prior hand-off: `/home/rlg/relational-os/sprints/sprint-4/summary.md` (Sprint 4's what-was-
  built / verified-output / open-issues) and `/home/rlg/relational-os/sprints/sprint-4/notes/findings.md`
- Spec release mirror (READ-ONLY): `/home/rlg/Documents/ai-relational-os-spec.md` (+ `.pdf`)
- **Sprint-0 contracts you build on:** the normative schema at
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/schema/relational-os.schema.yaml`
  (+ `.json`), `build_schema.py`, the conformance validator
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/conformance.py` +
  `run_conformance.py`, and the fixtures under
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/fixtures/`. Reuse them; do not re-derive.
- **Sprint-1 build you extend:** `/home/rlg/relational-os/sprints/sprint-1/artifacts/`
  (`ros/` substrate + S2 Intent/Matching, `make_fixtures.py`).
- **Sprint-2 build you extend:** `/home/rlg/relational-os/sprints/sprint-2/artifacts/`
  (`ros/s5.py` Trust engine, `s5_demo.build_s2()`, `run_s2_demo.py` /
  `run_s2_conformance.py`).
- **Sprint-3 build you extend:** `/home/rlg/relational-os/sprints/sprint-3/artifacts/`
  (`ros/s3.py` Orchestration + human floor, `s3_demo.build_s3()`).
- **Sprint-4 build you extend:** `/home/rlg/relational-os/sprints/sprint-4/artifacts/`
  (`ros/s4.py` Exchange & Settlement + multi-role / multi-org, `s4_demo.build_s4()` which
  chains S1→S2→S3→S4→S5 and already carries TWO roles + TWO org types). **Copy the Sprint-4
  `ros/` package and its builders into your Sprint-5 artifacts (not a git import)**, or set
  `PYTHONPATH` to include the Sprint-4 `artifacts` dir, so the operating-layer work consumes
  the already-running S1→S5 state.

## Task
Follow `PROTOCOL.md` exactly: read the spec first, then plan (`plan.md` + a
`work/<n>-plan.md` per sub-sprint, written BEFORE executing), then execute, then update the
spec from findings, then verify DoD, then output the summary + next-sprint prompt (for the
final sprint, write the project's closing hand-off). You may load the `system-specification`
skill.

## Sprint 5 scope — Business Operating Layer (the product), per SPEC.md §7J/§7K/§7L/§8
This is the FINAL sprint and the product pivot: turn the verified chain into an operating
system an owner actually uses every morning. Remark: the sprint label "S5" below refers to
the sprint number, NOT service S5 (Accountability & Trust) — those names collide; the spec's
roadmap (§8) calls this "Sprint 5 — Business Operating Layer".

**DoD (per SPEC.md §8 Sprint 5 and §7L):** the **cockpit (§7J.9) shows business health,
prioritized attention (exceptions→cases→tasks), and an AI recommendation with the authority
it requires**, and ONE end-to-end **exception→case→task→verified-outcome** cycle closes and
records a `Learning` entry (§7K.1 Organizational Learning). Concretely: the §7L ten-morning-
question test is ANSWERED WITH EVIDENCE for the fictional Quoteko company — #8 (what should
we do) becomes an assigned, authorized Task, #9 (who does it, with authority+capacity) is
satisfied, and #10 (did it work, what did we learn) records a learned outcome in the ledger.

Each sub-sprint STARTS by re-reading SPEC.md §7J (Goals/Metrics/Targets, Exception Management,
Case lifecycle, Task & Work Queue, Priority/Attention, Dependency & Impact, SLA-as-assembly,
Risk/Capacity, the Cockpit), §7K (operating semantics incl. Policy execution, Ownership,
Escalation, Approval, Acknowledgement, Organizational Learning), §7L (the ten questions), §8
(Sprint 5 roadmap + the §7L cockpit DoD), Appendix F §7J/§7K objects (Case, Goal, Metric,
Task, Dependency + derived Exception/Priority/SLA/Risk/Capacity/Policy/Escalation"), and the
`§7J.11` URI cap / `§C16` frozen ontology. Then `sprints/sprint-0` schema/validator; and
`sprints/sprint-1/-2/-3/-4` artifacts. Then it writes its own plan at
`sprints/sprint-5/work/<n>-plan.md` before executing.

**5.1 — Case-led loop on the running chain (the product, not a new service).** Open a Case
(§7J.3) on the verified Quoteko state — e.g. an Exception over a Trust/Outcome discrepancy,
or a discovered problem from the ledger — and drive it through `OPEN → TRIAGE → ASSIGNED →
IN_PROGRESS → (BLOCKED) → RESOLVED → CLOSED`, each with evidence. Build the §7J.2 exception
heartbeat (`EXPECTED → ACTUAL → VARIANCE → SIGNIFICANCE → EXCEPTION → ROOT → RECOMMENDED
ACTION → DECISION → EXECUTION → VERIFIED OUTCOME`). **DoD:** an `Exception → Case → Task →
verified outcome` cycle, with a `Learning` entry (Decision→Expected→Actual→Variance→WHY→
change-future-policy, §7K.1) recorded on the ledger.

**5.2 — Goals / Metrics / Priority / Dependency.** Build a Metric loop
(`Goal → Metric → Actual → Variance → Decision → Action → Outcome`, §7J.1) for Quoteko,
compute Priority = f(impact, urgency, confidence, irreversibility, relationship-importance,
cost-of-delay) (§7J.5), and represent Dependencies (`requires, blocks, enables, derived_from,
impacts`, §7J.6) with an impact analysis. **DoD:** the cockpit's business-health panel derives
from ledger-projected Metrics, priority-ordered attention is computable, and dependency →
impact is shown for at least one exception-to-case-to-task chain.

**5.3 — The Cockpit — the §7L test answered with evidence.** Produce the cockpit output for
Quoteko: health, prioritized attention (the "seven things today," §7J.2), and an AI
recommendation carrying the authority it requires (§7J.9). Answer the §7L ten questions **with
evidence from the ledger/graph** (1 what happened, 2 what changed, 3 what matters, 4 what's
going wrong, 5 why, 6 what if we do nothing, 7 what are our options incl. do-nothing, 8 what
should we do → becomes assigned authorized work, 9 who does it + authority/capacity, 10 did it
work + what we learned). **DoD:** #8 becomes an assigned, authorized Task in the ledger that
closes in a verified, learned outcome, and #9/#10 are answered.

## Mandatory rules
- **Real tool output only.** Producing artifacts and RUNNING them is mandatory; never
  fabricate results, file contents, or citations. Re-run `run_conformance.py`
  (`sprints/sprint-0/artifacts/.venv/bin/python`) over Sprint-0 fixtures AND the Sprint-1,
  Sprint-2, Sprint-3, Sprint-4 AND any new Sprint-5 fixtures to prove no regression
  (exit 0). Use the `run_s4_conformance.py` pattern (reuse the Sprint-0 validator, repoint
  `FIXTURES` at each generation root).
- **Keep the URI cap and the frozen ontology** (§7J.11, Appendix C §C16). The operating layer
  is written with the EXISTING `case:// goal:// metric:// task:// dependency://` schemes
  (added in Sprint 0) plus assemblies — Exception, Priority, SLA, Risk, Capacity, Policy,
  Escalation, Process, ProcessInstance are already in the schema (`$defs`); do NOT add new
  URI schemes or new ontology nouns. Extend the schema ONLY where a genuine build finding
  requires it (additive-only; note in findings; if extended, rebuild the `.json` via
  `build_schema.py`).
- **Update `SPEC.md` from findings:** write `sprints/sprint-5/notes/findings.md` as you go;
  apply genuinely necessary corrections (targeted `patch`, re-verify section numbering, bump
  minor version to **0.22**, append to the Version/Review Log). Preserve every requirement's
  meaning. This is the final sprint, so also make sure §8's roadmap reflects a COMPLETE
  S1→S5 chain (all five platform sprints done).
- **Budget:** hard ~$10/mo cap — prefer local computation, batch web calls, keep prompts
  lean. No frontier-API spend; the operating layer is deterministic local logic over the
  ledger/graph (§G.11).
- **Raymond:** clean English output, `file://` absolute paths, honest "stuck/failed" over
  fabricated success, report status at each long step.
- **Single-threaded** per PROTOCOL: do all work yourself, in ONE process; do NOT use
  `delegate_task`/subagents.
- Do not touch anything outside `/home/rlg/relational-os/` except reading the `~/Documents`
  mirror and the Sprint-0/1/2/3/4 artifacts.

## Exit criteria (Definition of Done)
- `sprints/sprint-5/plan.md` written first; each sub-sprint has `work/<n>-plan.md`.
- `sprints/sprint-5/artifacts/` contains the extended `ros/` package (e.g. `bol.py` — the
  operating layer — reusing Case/Goal/Metric/Task/Dependency), the Exception heartbeat, a
  cockpit/report generator, a demo runner and a conformance runner, with **real tool output**;
  the harness demonstrably answers the §7L ten questions WITH evidence for Quoteko, turns #8
  into assigned authorized work that closes in a verified, learned outcome (#10), and shows
  health + prioritized attention in the cockpit.
- Sprint-0 conformance still exits 0 over all fixture generations produced so far
  (Sprint-0, -1, -2, -3, -4, -5).
- `SPEC.md` updated for genuine findings (bumped to 0.22, log appended; roadmap marks the
  S1→S5 chain complete).
- `sprints/sprint-5/summary.md` written (what was built, verified output, open issues —
  including what remains for a real deployment vs this deterministic local build).
- The next-sprint prompt is NOT required (final sprint); instead write a closing hand-off at
  `sprints/COMPLETE.md` describing the finished chain, its proven loops, the cockpit, and how
  to run each demo/conformance runner.

## Hand-off requirement
Your **final message** must summarize the finished Sprint 5 (what was built, the verified
§7L/cockpit output) AND point to `sprints/COMPLETE.md` (the project's closing hand-off),
plus the absolute path to `sprints/sprint-5/summary.md`. This completes the pipeline that
began with Sprint 0's spec/schema/validator and, through Sprints 1–4, built and verified the
S1–S5 service chain — now surfaced as a working Business Operating Layer.