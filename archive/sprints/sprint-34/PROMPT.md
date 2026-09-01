# SPRINT 34 — PROMPT (a pure, engine-free CONSOLIDATION-AUDIT: verify the reference build stays green as one
# coherent whole, and answer "is the now-two-path decision surface a single framework" across EVERY
# contested-reality org — not just the 13-org Sprint-33 set — with an honest consolidated boundary document.
# NO new capability; `adjudication_engine.py` AND `capacity_rerank.py` stay BYTE-IDENTICAL.)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here; read
before acting; never fabricate; **every documented command MUST be run and its real output captured.**
Sprints 20-33 built and consolidated a configurable, deterministic, recorded-data §7L adjudication engine
(`instances/contested_reality/adjudication_engine.py`, hash `a60f8f7…`), added a recorded
`capacity_constraint` marker + per-option `capacity_infeasible`/`capacity_risk` flags
(`_per_option_capacity_flags`/`_capacity_reason`/`_forecast_closure`), positively inventoried the WHOLE
recorded-data decision surface as reason-not-choice across 11 orgs (Sprint 31, `run_recorded_surface_demo.py`),
built the ONE explicit POLICY-authorized out-of-scope step — a capacity-constrained RE-RANK for the machine
(Sprint 32, NEW pure module `capacity_rerank.py`, hash `f7c6a185…`, `run_capacity_rerank_demo.py`, 13 orgs), and
consolidated the now-TWO-path decision surface (advisory + re-rank) as ONE coherent framework with an
exhaustive-disjoint PATH taxonomy over the 13-org set (Sprint 33, `run_two_path_demo.py`, NO engine/rerank
change). **Sprint 34 is a consolidation-AUDIT: the reference build is a whole, and this sprint verifies it as
such and extends that one-framework answer across every org every runner already exercises (the broader ORG
CATALOG), without adding a single capability.**

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7K.1 (Policy, Trade-off,
  Organizational Learning, Forecast), §7L (the ten morning questions), §7J.11 + §C16 (URI cap), the frozen
  49 `$defs`.
- Protocol: `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-build, real output, ~$0,
  additive, never bump SPEC for a capability-only change; consolidation sprints stay at v0.22).
- Read FIRST, in full:
  - `instances/contested_reality/adjudication_engine.py` — `rank` (frozen, DO NOT TOUCH), `machine_eligible_best`,
    `reconcile`, `run_scenario`, `cockpit_q7q8` (advisory, NO capacity block), `cockpit_s7l` (the Q7/Q8
    `capacity_constraint` block + `_per_option_capacity_flags` + `_capacity_reason` + `_forecast_closure`),
    `record_metric_series` (REQUIRES `name`+`formula` in `fields`), `record_capacity`,
    `record_capacity_requirements`, `render_cockpit_s7l`, `forecast_metric`.
  - `instances/contested_reality/capacity_rerank.py` — Sprint 32's PURE module `capacity_rerank(cfg, sub, *,
    library=None)` (the additive, POLICY-authorized re-rank; DO NOT TOUCH).
  - `instances/contested_reality/run_two_path_demo.py` (Sprint 33 — `_surface`, `_classify`, the
    exhaustive-disjoint PATH classes {ADVISORY-no-capacity, ADVISORY-best-runnable, RE-RANK}),
    `run_capacity_rerank_demo.py` (Sprint 32 — 13 orgs / `build()`), `run_recorded_surface_demo.py` (Sprint 31 —
    11 orgs / `build_orgs()` / the reason-not-choice tally).
  - `instances/contested_reality/adjudication_configs.py` (DELI + INSPECT + COVE + RULE_LIBRARY; the org
    builders in `run_forecast_*.py`/`run_cockpit_*.py`/`run_adjudication_engine_demo.py` define the wider
    ORG CATALOG the demo runners exercise).
  - `instances/contested_reality/artifacts/adjudication/reports/two-path.md` (Sprint-33 consolidated report),
    `sprints/sprint-33/{summary.md,notes/findings.md,plan.md}` (the consolidation + the honest residual), and
    `sprints/sprint-32/{summary.md,notes/findings.md}` (the re-rank build + §16 residual).
- Project invariants (the `relational-os` skill): frozen ontology / URI cap / 49 `$defs` (§C16); additive only;
  single-threaded; plan-before-build; real tool output; ~$0; footguns (`cockpit_q7q8` does NOT carry the
  `capacity_constraint` block — read it from `cockpit_s7l`; `record_metric_series` REQUIRES `name`+`formula`;
  `Graph.get` one-arg; `evidence`/`rules_applied` as ARRAYS; `{**graph.get(u), ...}` merge-not-replace; C2
  temporal-suffix keys; strict C5 tables; `eng.reconcile(sub, cfg)` ARG ORDER; the Sprint-0 venv
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for conformance; runner CWD-sensitivity).

## What Sprint 34 IS and IS NOT
- **IS:** a positive, engine-untouched consolidation-AUDIT. It (1) captures the FULL reference-build green
  baseline (the unified CR demo suite + conformances + build_all + conformance_all + S5 reference + agent) as
  ONE command, (2) extends the Sprint-33 two-path question — "is the decision surface one coherent framework?"
  — from the 13-org set to the ENTIRE ORG CATALOG every CR runner already exercises (the union of all labels
  the CR demo runners drive, NOT just the 13), classifying EVERY org into the same exhaustive-disjoint PATH
  taxonomy and asserting the two-path composition holds for every org that has any capacity recorded, and
  (3) writes ONE consolidated §16 boundary document (the decision-framework cheat-sheet) + updates the docs.
  A survey/audit runner + recorded data ONLY; `adjudication_engine.py` AND `capacity_rerank.py` provably
  byte-identical (hashes `a60f8f7…` + `f7c6a185…` recorded before and after).
- **IS NOT:** a new capability; a change to `rank`/`capacity_rerank`/the engine; a probabilistic/stochastic
  forecast; a new URI/schema/`$defs` edit; a Trust (S5) change; breaking any prior sprint's proof or any reused
  org's default output.

## The target (what "done" looks like)
1. **A new runner** `run_two_path_catalog_demo.py` that (a) `import`s the ORG CATALOG = the union of every org
   the existing CR demo runners already construct (`r32.build()` 13 + the `run_forecast_*`/`run_cockpit_*`/
   `run_adjudication_engine_demo` orgs — enumerate them from those files, do NOT invent new ones), (b) builds
   each fresh in memory, (c) emits a `two_path_surface` + PATH class per org (reusing the Sprint-33
   `_surface`/`_classify` logic), and (d) asserts, over the WHOLE catalog:
   - **advisory never shadowed** — every org with a capacity-recorded best and `needed=False` keeps advisory
     Q8 == `cockpit_q7q8`; every `needed=True` org has replacement ≠ advisory Q8 ≠ machine_eligible_best;
   - **exhaustive-disjoint** over the whole catalog (every org exactly one class; the needed=True set == the
     RE-RANK set);
   - **floor integrity** over the whole catalog (no advisory or re-rank selection floor-gated vs `rank`);
   - **determinism-vs-history** — the Sprint-31 tally (11/11) + the Sprint-32 re-rank results + the Sprint-33
     13-org taxonomy ALL reproduce from the SAME data in this run.
   Exit 0 = ALL PASS. Emits `artifacts/adjudication/reports/two-path-catalog.md`.
2. **No engine / no `capacity_rerank.py` change:** both byte-identical (hash `a60f8f7…` + `f7c6a185…`
   recorded before and after); non-regression green; the reused orgs' default bytes intact.
3. **Honest consolidated boundary doc:** a `docs/DECISION-FRAMEWORK-BOUNDARY.md` (or an additive section in
   `docs/ENGINE-FORECAST-CAPACITY.md` §18) that states plainly, for a reader: the try-it commands (green
   baseline + `run_two_path_demo.py` + `run_two_path_catalog_demo.py`), the two-path framework, the whole-catalog
   taxonomy distribution, and the honest §16 verdict on what is and is not derivable.
4. **Real output:** new runner ALL PASS; full non-regression green; no new noun; frozen 49 `$defs`; SPEC v0.22;
   engine `a60f8f7…` + `capacity_rerank.py` `f7c6a185…` byte-identical.

## Mandatory rules
- **Write-first:** `sprints/sprint-34/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication.
- **Additive/consolidation**: keep frozen functions + `capacity_rerank.py` + the 49 `$defs`/URI cap/SPEC v0.22
  untouched; re-verify `ros/`, schema hash `34264934…`, sector instances, the Sprint-31/32/33 reuse bytes, and
  the engine + `capacity_rerank.py` hashes `a60f8f7…` + `f7c6a185…`.
- **ORG CATALOG is derived from EXISTING runners only** — if an org is not already exercised by a CR demo
  runner, do not invent it (a capability or new fixture would be out of scope).
- **Single-threaded** per PROTOCOL — no subagents. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST: every CR demo runner (`run_two_path_demo.py`, `run_capacity_rerank_demo.py`,
  `run_recorded_surface_demo.py`, the `run_forecast_*` set, `run_cockpit_s7l/q7q8_demo.py`,
  `run_adjudication_engine_demo.py`) + all 5 CR conformances (Sprint-0 venv) + `build_all.py` +
  `conformance_all.py` + S5 reference demo + conformance + agent demo + conformance.
- New `run_two_path_catalog_demo.py` ALL PASS over the WHOLE org catalog.
- Full non-regression green after the new runner; SPEC v0.22; 49 `$defs`; `ros/` + schema clean; schema hash
  `34264934…`; engine `a60f8f7…` AND `capacity_rerank.py` `f7c6a185…` byte-identical (record both).

## Documentation (roll-forward)
- Additive consolidated boundary doc (or §18 in `docs/ENGINE-FORECAST-CAPACITY.md`) + an
  `instances/README.md` Sprint-34 entry + a "Update after Sprint 34" note in
  `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` + `sprints/sprint-34/summary.md` +
  `notes/findings.md`. Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces. Update the
  `relational-os` skill's Sprint-34 note.

## Hand-off requirement
Your **final message** must summarize: the whole-catalog PATH distribution (how many orgs per class across
EVERY org the CR runners exercise, not just the 13), the composition proof over the whole catalog (the
advisory is never shadowed — replacement ≠ advisory Q8 ≠ machine_eligible_best where the re-rank fires; they
agree where it doesn't), the floor integrity, the exhaustive-disjoint taxonomy, that the one-framework answer
now holds across the whole catalog (Sprint-31 + Sprint-32 + Sprint-33 all reproduce from the SAME recorded
data), the byte-identical default (`a60f8f7…` + `f7c6a185…` unchanged; no new noun; frozen 49 `$defs`), the
honest §16 verdict (the two-path decision surface is ONE coherent framework across the whole catalog, WHILE
the deterministic advisory label-vs-choice boundary still holds), what is STILL not derivable (a
probabilistic/stochastic forecast; a per-option requirement NOT unit-coupled to the recorded capacity value /
an option with no recorded requirement — the machine never invents one; any choice the §6 human must make that
recorded data cannot machine-decide — the re-rank is POLICY-authorized, not a claim of objective best), and the
verified build + conformance commands. Write the **next** sprint's self-contained prompt at
`sprints/sprint-35/PROMPT.md` (reference only absolute paths and the current SPEC.md).