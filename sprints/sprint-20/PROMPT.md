# SPRINT 20 — PROMPT (the honest frontier Sprints 13–19 disclosed: Q6 forecasting and Q9 capacity, recorded AS DATA)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here;
read before acting; never fabricate; **every documented command MUST be run and its real output
captured.** Sprints 13–19 built a configurable adjudication engine (`instances/contested_reality/`
`adjudication_engine.py`): a config-authorable reconciliation RULE (registry → declarative `rule_spec`
DSL), a named cross-org `RULE_LIBRARY` (with `bayesian-combine`), RULE learning, a first-class §7L
Q7/Q8 line (Sprint 18), and then the FULL §7L Q1–Q10 morning cockpit rendered BY the engine, data-only
(Sprint 19). **Sprint 19's own findings (see `sprints/sprint-19/notes/findings.md`, "Residual seams")**
disclosed two honest frontiers: (1) **Q6 "what will happen if we do nothing?"** cannot forecast on the
adjudication orgs because none records a **realized-vs-expected series** on its graph — the cockpit
must truthfully say "cannot forecast from recorded data"; and (2) **Q9 capability/capacity** is
rendered as the holder-of-authority assignment, NOT a **dynamic capacity model**. Sprint 20 closes (a
bounded slice of) both by making an org RECORD the missing data additively on its own graph/ledger so
those §7L questions can be answered AS DATA for a generically-driven org — the same data-only
discipline as Sprints 18/19.

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7J.9 (cockpit/authority),
  §7K.1 (Policy, Trade-off, Organizational Learning, Ownership, Forecast), §7L (the ten morning
  questions, Q1–Q10 with their parenthetical evidence requirements), §7J.11 + §C16 (URI cap); the
  **capacities/caution** lanes in §7J.5/§7K.1 and any reference-cockpit BI-forecast language
  (`sprints/sprint-5/artifacts/reports/cockpit.md` shows the projected-on-time. `ros/bol.py` records
  `metric://` with target/actual/variance, and the sector BI uses recorded realized-vs-expected — the
  pattern to reuse).
- Protocol: `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-build, real output,
  best-effort ~$0, additive, never bump SPEC for a capability-only change).
- Read FIRST, in full:
  - `/home/rlg/relational-os/instances/contested_reality/adjudication_engine.py` — esp. `cockpit_s7l`
    (`q6`, `q9`), `_recorded_forecast_series`, `_graph_objects`, `reconcile`, `render_cockpit_s7l`,
    and the Sprint-18 `cockpit_q7q8` (do NOT rewrite any frozen function). `adjudication_configs.py`
    (DELI/COVE/INSPECT + variants, `RULE_LIBRARY`, `LEARN_HYPER`, `inspect_batch`),
    `reconcile_learning.py` (`record_realized_outcome`, `record_learned_rule`).
  - `run_cockpit_s7l_demo.py` (Sprint 19 runner — how it RECORDS a realized outcome / learning
    decision on a NEW label so the org's own ledger carries it) + `run_cockpit_q7q8_demo.py`.
  - `sprints/sprint-19/summary.md` + `notes/findings.md` (esp. the two Residual-seam paragraphs) and
    `docs/ENGINE-S7L-COCKPIT.md` (§2's Q6/Q9 rows + §6's honest limits).
  - The reference sector BI/forecast pattern: `sprints/sprint-5/artifacts/reports/cockpit.md` (§7L Q6)
    and how `ros/bol.py` + the sector `build_scene` record `metric://` with a realized-vs-expected
    (`target`/`actual`/`variance`) — reuse the RECORDED pattern, don't re-invent.
- Project invariants: the `relational-os` skill — frozen ontology / URI cap / 49 `$defs` (§C16);
  additive only; single-threaded; plan-before-build; real tool output; ~$0; footguns (Graph.get
  one-arg, `evidence`/`rules_applied` as ARRAYS, `{**graph.get(u), ...}` merge-not-replace, C2
  RFC3339 temporal-suffix keys — never name an additive field ending in `at|time|deadline|expires|
  expiry|effective|due|since` — strict C5 tables, `eng.reconcile(sub, cfg)` ARG ORDER, the Sprint-0
  venv `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for conformance, runner
  CWD-sensitivity, the `[0]`-indexed `parents` for the Sprint-0 path).

## What Sprint 20 IS and IS NOT
- **IS:** make the two questions a generically-driven org's recorded data can now support (Q6 forecast,
  Q9 capacity) be answered AS DATA, plus a small new capability or forecast SURFACE that any configured
  org can record. Deliver a REPLAYABLE way for an org to record — additively, on its own
  graph/ledger, no schema/new-noun — (i) a small realized-vs-expected **metric series** (a `metric://`
  object with per-period `target`/`actual`/`variance`, the reference pattern) and (ii) an additive
  **capacity** field on the authority/actor the §7L Q9 reads, so `cockpit_s7l`'s `q6` can forecast a
  deterministic projection ("if nothing changes") from a RECORDED series and its `q9` can report
  capacity. Add a generic `forecast_metric(cfg, sub, metric_uri, horizon)` (deterministic projection
  from the recorded series only — never the wall-clock, never invented numbers; an exhausted/absent
  series must say so plainly) and extend `cockpit_s7l`'s `q6`/`q9` and `render_cockpit_s7l` to consume
  the recorded data when present (while keeping the honest no-data fallback). Prove it with a runner
  (`run_forecast_capacity_demo.py`) that drives ≥2 orgs (e.g. a NEW org/label like `deli-forecast`
  with a recorded `metric://` series + a capacity field on its adjudicator, and an existing org without
  them) and asserts: both orgs still pass the full §7L Q1–Q10 cockpit; the org WITH recorded data answers
  Q6 with a deterministic forecast and Q9 with a capacity number; the org WITHOUT them still says the
  honest fallback; determinism on re-run; and that `ros/`, the schema, and deli/cove (and the other
  existing org fixtures) are byte-identical up to the clock afterwards.
- **IS NOT:** a new service, a new URI noun, a schema/`$defs` edit, a Trust change (S5), a change that
  lets the machine overrule the §6 human, a re-implementation of `run_scenario`/`reconcile`/`cockpit_q7q8`,
  or any attempt to forecast Q6 with a wall-clock/best-guess. **The §L gate** ("#8 becomes authorized
  work") is NOT re-litigated — Sprint 19 met it; this sprint hardens Q6/Q9 to data. No frontier spend.

## The target (what "done" looks like)
1. A recorded-data capacity + forecast SURFACE, additive on the frozen ontology: a small generic
   `forecast_metric(cfg, sub, metric_uri, *, horizon)` that computes a **deterministic projection** from
   a recorded `metric://` realized-vs-expected series (last recorded actual → forward periods, with the
   projected result labelled as a projection and the recorded variance shown); returns an honest
   "cannot project — no recorded realized-vs-expected series" when absent. Optionally a direction-of-
   travel / simple trend (mean of recorded deltas) — all from recorded values only. Doc in
   `references/` + `docs/`.
2. `cockpit_s7l`/`render_cockpit_s7l` extended so Q6 uses the recorded series (a real forecast when one
   exists, else the existing honest fallback) and Q9 reads an additive **capacity** field (a number +
   units, e.g. "1.0 obligations" or a load) recorded on the authority/actor — with the no-field
   fallback unchanged. Q7/Q8 stay delegated to the Sprint-18 line (byte-identical). No rewrite of any
   frozen function.
3. A runner (`run_forecast_capacity_demo.py`, exit 0 = ALL PASS) that drives ≥2 orgs (new recorded-data
   org + an existing org) and asserts: full §7L Q1–Q10 present on both; the recorded-data org forecasts
   Q6 (deterministic, from recorded series only) and reports Q9 capacity; the no-data org returns the
   honest fallback for Q6 and no-capacity Q9; determinism; agreement between `cockpit_s7l.q6/q9` and the
   record on the org's graph; and **non-regression** (the 6 curated CR runners, `conformance_adjudication.py`
   16 labels, the 4 prior CR demos + conformances, sector `build_all.py` + `conformance_all.py`, S5
   reference + conformance, agent demo + conformance all exit 0; deli/cove byte-identical up to the
   clock).
4. **Honest docs** (`docs/ENGINE-FORECAST-CAPACITY.md` + additive note in `docs/ENGINE-S7L-COCKPIT.md`):
   how Q6/Q9 are now answered from recorded data when present; the deterministic projection rule; the
   honest fallback; and a §16-style verdict: **do the recorded-data Q6 forecast and Q9 capacity now make
   the §7L morning cockpit fully data-grounded on every one of the ten questions (where the data
   exists)? Say plainly, including what is still not derivable.**
5. **Real output:** new runner ALL PASS; full non-regression green; no new noun, 49 `$defs`, SPEC v0.22.

## Mandatory rules
- **Write-first:** `sprints/sprint-20/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication.
- **Additive:** the ONLY engine file you may modify is
  `instances/contested_reality/adjudication_engine.py` (add `forecast_metric` + extend `cockpit_s7l`'s
  q6/q9 + `render_cockpit_s7l` — do NOT rewrite `reconcile`/`run_scenario`/`_derive`/`SPEC_VOCAB`/
  `_aggregate`/`cockpit_q7q8`, frozen by Sprints 13–19). Keep 49 `$defs` + URI cap + SPEC v0.22.
  Re-verify `ros/`, the schema (`sprints/sprint-0/artifacts/schema/relational-os.schema.json` hash
  `7fc38c8c…`), the reference build, and the 12+ sector instances untouched. deli/cove byte-identical
  up to the clock.
- **Single-threaded** per PROTOCOL. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST (Sprint-19 state): `run_cockpit_s7l_demo.py` + the 6 curated runners,
  `conformance_adjudication.py` (16 labels), the 4 prior CR demos + conformances, `build_all.py` +
  `conformance_all.py`, S5 reference + conformance, `agent_demo` + conformance.
- New assertions ALL PASS: the recorded-data org forecasts Q6 + reports Q9 capacity from its own
  graph/ledger; the no-data org keeps the honest fallback; full §7L Q1–Q10 still renders on both;
  deterministic; agreement with the recorded graph; every forecast is derived from recorded series
  values only (no wall-clock / no invented number).
- Full non-regression green; SPEC v0.22; 49 `$defs`; `ros/` + schema clean.

## Documentation (roll-forward)
- Add `docs/ENGINE-FORECAST-CAPACITY.md`; append a Sprint-20 entry to `instances/README.md`; append an
  "Update after Sprint 20" note to `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`;
  append an additive note to `docs/ENGINE-S7L-COCKPIT.md` (the Q6/Q9 rows now show recorded-data answers
  where they exist); reference the new build in `references/` if useful.
- Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces (log it then).
- Write `sprints/sprint-20/summary.md` + `notes/findings.md`.

## Hand-off requirement
Your **final message** must summarize what the recorded-data Q6 forecast and Q9 capacity surface reports
per org (the deterministic projection rule; the honest fallback when no series/capacity is recorded;
which questions are now fully data-grounded), how it is generic + additive (recorded `metric://` +
capacity field, no new noun, frozen 49 `$defs`), the ≥2-org proof (recorded-data org forecasts + reports
capacity; no-data org keeps the fallback; both full §7L), the honest §16 verdict on whether the §7L
morning cockpit is now data-grounded on all ten questions (where the data exists), and the verified
build + conformance commands. Write the **next** sprint's self-contained prompt at
`sprints/sprint-21/PROMPT.md`.