# SPRINT 19 — PROMPT (the full §7L ten-question cockpit rendered BY the engine: Q1–Q10, data-only)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** Sprints 15–18 made the evidence-reconciliation RULE authorable (`rule_spec`), a named
cross-org RULE LIBRARY, learnable, and then surfaced a **first-class §7L Q7/Q8 cockpit line INSIDE the
generic engine** (`adjudication_engine.cockpit_q7q8`/`render_cockpit_q7q8` reports the ACTIVE rule +
source + learned-or-not + why for ANY configured org — data-only, from the org's own config + ledger,
verified in `docs/ENGINE-Q7Q8-COCKPIT.md`). Sprint 19 takes the same data-only discipline to the WHOLE
ten-question morning test: make `adjudication_engine.py` render the complete **§7L Q1–Q10 cockpit** for
any generically-driven org — Q1 state/events, Q2 change, Q3 attention, Q4 exceptions, Q5 root-cause
WITH epistemic status, Q6 forecast ("if nothing changes"), Q7 options+trade-off, Q8 recommendation with
authority, Q9 ownership/capability/authority, Q10 verified outcome + organizational learning — all read
off the org's own graph/ledger/config, no per-org Python. This is the §7L gate (§7L, §7J.9 cockpit):
"today the questions are answered with evidence and #8 becomes authorized work."

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7J.9 (cockpit/authority),
  §7K.1 (Policy, Trade-off, Organizational Learning, Ownership, Forecast), §7L (the ten morning questions,
  Q1–Q10 with their parenthetical evidence requirements), §7J.11 + §C16 (URI cap).
- Protocol: `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-build, real output,
  best-effort ~$0, additive, never bump SPEC for a capability-only change).
- Read FIRST, in full:
  - `/home/rlg/relational-os/instances/contested_reality/adjudication_engine.py` (esp. `rank`,
    `machine_eligible_best`, `render_tradeoff`, the Sprint-18 `cockpit_q7q8`/`render_cockpit_q7q8` +
    `_cockpit_active_rule` — build the full cockpit as a strict superset of those, do NOT rewrite them),
    `adjudication_configs.py` (`RULE_LIBRARY`, DELI/COVE/INSPECT + their variants, `LEARN_HYPER`),
    `reconcile_learning.py`.
  - `run_cockpit_q7q8_demo.py` (Sprint 18 runner — study HOW it drives ≥2 orgs, records the reconcile-
    learning decision, and asserts determinism/agreement), `run_reconcile_learning_demo.py`,
    `run_rule_library_demo.py`.
  - Sprint-18 `sprints/sprint-18/summary.md` + `notes/findings.md` and `docs/ENGINE-Q7Q8-COCKPIT.md`;
    the runner-report lines in `artifacts/adjudication/reports/cockpit-q7-rule-library.md` and
    `cockpit-q7-q8-reconcile-learning.md`.
  - The sector cockpit render that already answers some §7L questions on the reference build:
    `sprints/sprint-5/artifacts/reports/cockpit.md` + the operating-layer `ros/bol.py`
    (`BolService`) and `docs/` manuals in `sprints/sprint-6/artifacts/docs/` (05-bi / 06-user) for how
    attention/Q3 + verified-outcome/Q10 are already represented — reuse, don't re-invent.
- Project invariants: the `relational-os` skill — frozen ontology / URI cap / 49 `$defs` (§C16:
  only `case:// goal:// metric:// task:// dependency://` plus the existing `rule://`/`decision://`/
  `evidence://`/`claim://`/`dispute://` already minted by the adjudication orgs); additive only;
  single-threaded; plan-before-build; real tool output; ~$0; footguns (Graph.get one-arg,
  `evidence`/`rules_applied` as ARRAYS, `{**graph.get(u), ...}` merge-not-replace, C2 RFC3339
  temporal-suffix keys — never name an additive field ending in `at|time|deadline|expires|expiry|
  effective|due|since` — strict C5 tables, `eng.reconcile(sub, cfg)` ARG ORDER, the Sprint-0 venv
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for conformance, runner
  CWD-sensitivity).

## What Sprint 19 IS and IS NOT
- **IS:** a generic `cockpit_s7l(cfg, sub, *, library=None) -> dict` + `render_cockpit_s7l(...) -> str`
  in `adjudication_engine.py` that renders ALL TEN §7L questions for ANY configured org, data-only:
  Q1 (recorded state/events over the period, from the ledger), Q2 (change/delta from the graph+ledger),
  Q3 (prioritized attention — the flagged exception/case analogue), Q4 (exceptions/adjudications OPEN/
  UNRESOLVED), Q5 (root-cause WITH epistemic status — the disputed claims' `epistemic_status`), Q6
  (forecast "if nothing changes" — a deterministic projection from recorded realized values, never the
  wall-clock), Q7 (delegate to the Sprint-18 Q7 line: options + baseline + machine-eligible best),
  Q8 (delegate to the Sprint-18 Q8 line: recommendation with authority + determination), Q9 (ownership/
  capability/authority — read from the org's actors/authority/obligations in the graph), Q10 (verified
  outcome + organizational learning — read from the org's verified `decision://`/`evidence://` and the
  recorded `learning`). Prove it with a runner that drives ≥2 different orgs (e.g. `deli` registry, an
  `inspect-learn-b` learned rule) and asserts Q1–Q10 are all present + deterministic + agree with the
  existing Q7/Q8 engine line and the runner-report lines.
- **IS NOT:** a new service, a new URI noun, a schema/`$defs` edit, a Trust change (S5), a change that
  lets the machine overrule the §6 human, a re-implementation of `run_scenario`/`reconcile`, or an
  attempt to answer §7L questions the recorded data genuinely cannot support (Q6 forecast honesty: if
  there is no recorded realized-vs-expected series the forecast must say so plainly — never invent a
  number). No frontier spend. ~$0 deterministic local Python.

## The target (what "done" looks like)
1. A generic `cockpit_s7l(cfg, sub, *, library=None) -> dict` (all ten questions; q1..q10 keys each
   with the evidence the spec asks for) and `render_cockpit_s7l(...) -> str` (a plain-text §7L Q1–Q10
   cockpit) in `adjudication_engine.py`, valid for ANY org config incl. a learned `RULE_LIBRARY` entry.
   It MUST be a strict superset of the Sprint-18 Q7/Q8 functions (Q7/Q8 re-use them by construction),
   and it MUST NOT change the frozen schema/ontology or the byte-identity of existing orgs.
2. A runner (e.g. `run_cockpit_s7l_demo.py`, exit 0 = ALL PASS) that drives ≥2 orgs with different
   rules sources (a registry org `deli` and a learned-this-run org `inspect-learn-b`; optionally a
   rule-library org `inspect-corroboration`) and ASSERTS: (a) all ten §7L questions present with the
   required evidence; (b) Q7/Q8 of `cockpit_s7l` equal the Sprint-18 `cockpit_q7q8` line on the same
   org; (c) deterministic (identical on re-run); (d) the engine-native cockpit AGREES with the existing
   Sprint-16/17/18 runner-report lines where they overlap; (e) Q5's epistemic status and Q10's
   verified/learning fields come from the org's real graph/ledger (not authored literals); (f) Q6
   never fabricates a forecast (no recorded series -> an explicit "cannot forecast from recorded data").
3. **Real output:** new runner ALL PASS; non-regression: the existing `run_cockpit_q7q8_demo.py` /
   `run_reconcile_learning_demo.py` / `run_rule_library_demo.py` / `run_rule_authoring_demo.py` /
   `run_rule_comparison_demo.py` / `run_adjudication_engine_demo.py` still ALL PASS (re-verify
   deli/cove byte-identical up to the clock); C1–C5 over any new fixtures green; full non-regression
   green; no new noun, 49 `$defs`, SPEC v0.22.
4. **Honest docs** (`docs/ENGINE-S7L-COCKPIT.md` + an additive appendix in
   `ENGINE-Q7Q8-COCKPIT.md`): the engine now renders the FULL §7L morning cockpit, data-only; what each
   of Q1–Q10 shows (and the evidence behind it); which questions the recorded data richly supports vs
   which are honest "not derivable from recorded data" (esp. Q6); and a §16-style verdict answering:
   **has RelationalOS ''#8 becomes authorized work'' (§7L's gate) — does the engine turn Q8 into an
   authorized, verified, learned outcome with the human owning the determination?** Say plainly.

## Mandatory rules
- **Write-first:** `sprints/sprint-19/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication.
- **Additive:** the ONLY engine file you may modify is
  `instances/contested_reality/adjudication_engine.py` (add the `cockpit_s7l`/`render_cockpit_s7l`
  functions — do NOT rewrite `reconcile`/`run_scenario`/`_derive`/`SPEC_VOCAB`/`_aggregate`/`cockpit_q7q8`,
  which are frozen by Sprints 13–18). Keep 49 `$defs` + URI cap + SPEC v0.22. Re-verify `ros/`, the
  schema (`sprints/sprint-0/artifacts/schema/relational-os.schema.json` hash `7fc38c8c…`), the reference
  build, and the 12+ sector instances untouched. deli/cove byte-identical up to the clock.
- **Single-threaded** per PROTOCOL. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (Sprint-18 state): the 6 curated runners in `instances/contested_reality/`
  (`run_cockpit_q7q8_demo.py` etc.), `conformance_adjudication.py` (16 labels), the 4 prior CR demos +
  conformances, `build_all.py` + `conformance_all.py`, S5 reference + conformance, `agent_demo` +
  conformance.
- New assertions ALL PASS: the full §7L Q1–Q10 cockpit render is correct + deterministic for ≥2 orgs
  with different rule sources; Q7/Q8 match the Sprint-18 engine line; Q5 epistemic status + Q10
  verified/learning come from the org's real graph/ledger; Q6 never fabricates; it agrees with the
  Sprint-16/17/18 report lines where they overlap; the engine's render is produced WITHOUT per-org
  Python.
- Full non-regression green; SPEC v0.22; 49 `$defs`; `ros/` + schema clean.

## Documentation (roll-forward)
- Add `docs/ENGINE-S7L-COCKPIT.md`; append a Sprint-19 entry to `instances/README.md`; append an
  "Update after Sprint 19" note to `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`;
  append an additive note to `docs/ENGINE-Q7Q8-COCKPIT.md` (the Q7/Q8 line is now part of the full
  engine §7L cockpit).
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-19/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize what the engine-native §7L Q1–Q10 cockpit reports per org (the
ten questions and the recorded-data evidence each answers with), how it is generic and data-only, the
≥2-org proof of correctness + agreement with the prior runner-report lines, the honest §16 verdict on
whether th §7L gate ("#8 becomes authorized, verified, learned work with the human owning the
determination") is met, and the verified build + conformance commands. Write the **next** sprint's
self-contained prompt at `sprints/sprint-20/PROMPT.md`.