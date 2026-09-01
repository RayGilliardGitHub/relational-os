# SPRINT 13 — PROMPT  (Generalize the adjudication engine + render on the §7L cockpit)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** Sprint 12 proved RelationalOS can *run* the contested-reality lifecycle (claims →
conflictive evidence → UNRESOLVED-or-determination → appeal → reopen → new determination), but its
honest finding is that the **adjudication semantics are per-scenario authored code, not a
configurable engine**. Sprint 13 makes that capability *general* and surfaces it where an executive
would actually ask the question (the §7L cockpit Q7).

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). Read §7K.1 (trade-off / decision
  analysis, organizational learning), §7L (the ten morning questions — Q7 "What are our options?"),
  §7J.9 (cockpit), and §6 (human floor) in full.
- Sprint protocol (mandatory): `/home/rlg/relational-os/PROTOCOL.md`.
- The engine you generalize (read FIRST):
  - `/home/rlg/relational-os/instances/contested_reality/run_full_dispute.py` +
    `conformance_lifecycle.py` (Sprint 12 lifecycle proof) and
    `docs/DISPUTE-RESOLUTION-SPECIFICATION.md` (the 16-section spec; §13 sufficiency table; §16
    honest "B — Partially" assessment). The exact gap it names as the work: **the adjudication
    semantics (epistemic status, lifecycle state machine, generation of resolution options, and the
    value/utility weights) are authored per scenario — a different org's dispute still needs re-coding.**
  - `/home/rlg/relational-os/instances/contested_reality/tradeoff_model.py` + `run_tradeoff_demo.py`
    (Sprint 11 optimizer; the `WEIGHTS` are a documented business-model vector) and the other
    `contested_reality/` experiments (Sprint 9/10) + their conformance gates.
  - The cockpit/§7L render pattern: `/home/rlg/relational-os/instances/sector_scene.py` +
    `instances/configs.py` + `instances/build_all.py` + `instances/conformance_all.py` (how a sector
    emits `cockpit.json` / `cockpit.md` and answers the ten questions), and the S5 reference
    (`sprints/sprint-5/artifacts/`).
- Project invariants & operational recipes: the `relational-os` skill (frozen ontology/URI cap;
  additive fields; single-threaded; plan-before-build; real output; ~$0; footguns incl. `Graph.get`
  one-arg, `evidence` refs are ARRAYS, strict C5 state-machine tables, merge-not-replace, the C2
  temporal-suffix trap, sibling subpackage self-anchoring, two interpreters — plain `python3` for
  demos, Sprint-0 venv `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for
  conformance, runners are CWD-sensitive).

## What Sprint 13 IS and IS NOT
- **IS:** an **additive, configurable adjudication engine** — a generic, rule-driven driver that can
  run a contested-reality lifecycle for ANY org configured for it (org plumbed via `configs.py`/
  `sector_scene.py`-style data, not re-coded per scenario): given a configured business model (weight
  vector, resolution policy, evidence-reconciliation rule, authority assignments, an optional
  `coverage`-style constraint object) and two or more recorded conflicting claims, the engine
  produces a **lifecycle** (state machine + epistemic status + resolution options + a utility ranking,
  all recorded additively), reaching a determination or UNRESOLVED under the configured rule and the
  configuration and the §6 floor. Extend ONE of the existing contested-reality demos *fork-then-reuse* with a config-driven driver (the goal; do not rewrite `ros/`; respect `label` params with a
    `'qk'` default and never change reference output bytes).
- **IS NOT:** a new service, a new URI noun, a schema edit, or a change to the frozen ontology (49
  `$defs`, SPEC v0.22). No change to how Trust updates (S5 deterministic). Nothing auto-executes or
  replaces the human adjudicator; the §6 floor and §7J.9 authority are unchanged. No frontier spend.
- **Optional, additive (do it if it fits the same build, else defer):** render the trade-off +
  lifecycle onto the **§7L cockpit Q7** surface for the configured episode (an additive report line/
  section reusing the existing cockpit/report render path — do not build a new renderer universe), and
  start the **Decision-Learning / realized-cost weights** item (record an additive realized cost on the
  `decision://`, and — deterministically, clamp-bounded — update the business-model weights from
  expected-vs-actual variance so the objective itself is learned over time, not just the ranking).

## The target (what "done" looks like)
1. A **configurable adjudication engine** (e.g. `instances/contested_reality/adjudication_engine.py` +
   a `run_*_engine_demo.py`) that, from imported config (business-model weights, resolution policy,
   evidence-reconciliation rule, authority, constraint object) + ≥2 recorded conflicting claims,
   deterministically runs a lifecycle: epistemic status transitions → conflict/uncertainty → resolution
   options (incl. do-nothing/unresolved) → utility ranking → §6 floor gating → an authorized human
   determination (or UNRESOLVED) → verified outcome → learning. The SAME engine must drive **at least
   two different org scenarios** from config (e.g. reuse the Sprint-12 delivery dispute AND a different
   dispute type) with NO code change between them (only config/data), proving the generalization.
2. Real output: two config-driven lifecycle runs, both ALL PASS, with the state/epistemic/determination
   transitions recorded additively and conformance-green; none of the Sprint-9/10/11/12 demos or the
   sector build regress.
3. Honest documentation (`docs/GENERALIZED-ADJUDICATION.md` or extend the spec): what became
   configurable, what is still authored (any residual hardcoded semantics — say so plainly), and
   whether the §16 "new category" verdict moves from "B — Partially" toward "A" (or not) once
   adjudication is general + cockpit-rendered.
4. If you complete the optional cockpit-Q7 + decision-learning items, document them with real output
   too.
5. Every step signed and on the ledger; the human's determination keeps the authority it requires.

## Mandatory rules
- **Write-first:** `sprints/sprint-13/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication.
- **Additive, #new-noun-unless-documented, keep 49 `$defs` + URI cap + SPEC v0.22.** Re-verify `ros/`,
  the schema, the reference build, and the 12+ sector instances untouched.
- **Single-threaded** per PROTOCOL. **Budget ~$0** — local/deterministic; a local model optional-and-
  contained (reuse `agent_adapter`; parse + fallback-with-log).
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST: all four contested-reality demos + conformance (Sprint 9/10/11/12);
  `instances/build_all.py` + `conformance_all.py`; S5 reference + conformance; `agent_demo`.
- New assertions ALL PASS: the SAME engine runs ≥2 different scenarios from config (no code change
  between them); epistemic-status + lifecycle + determination/UNRESOLVED recorded additively;
  §6 floor + authority preserved; TRUST unchanged by the engine (only the deterministic formula);
  C1–C5 over the new fixtures; non-regression all green.
- Decide-and-document cache for the §16 verdict: state plainly whether the architecture is now
  "B — Partially" or can be argued "A — Yes" (and on what precisely it would still hinge).

## Documentation (roll-forward)
- Add/extend `docs/GENERALIZED-ADJUDICATION.md`; update `instances/README.md`; append an
  "Update after Sprint 13" note to `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`.
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-13/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize the generalized adjudication engine (what became configurable,
where it lives, the two+ config-driven scenarios with real rankings/determinations, verified build +
conformance commands) and give an honest verdict on whether the "new category" §16 assessment moved
toward "A". Write the **next** sprint's self-contained prompt at `sprints/sprint-14/PROMPT.md`. If a
piece cannot be generalized without a new primitive, say so plainly and specify the primitive rather
than faking it.