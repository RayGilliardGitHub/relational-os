# SPRINT 35 — PROMPT (a pure, engine-free REPRODUCIBILITY-AUDIT: verify the two-path decision framework's
# deterministic local-Python claims hold on this host and across the WHOLE corpus, and the Sprint-34
# consolidated boundary doc stands as the canonical reference. NO new capability; `adjudication_engine.py`
# AND `capacity_rerank.py` stay BYTE-IDENTICAL.)

You are Hermes Agent in a **fresh session** with **NO memory**. Rely ONLY on the files named here; read
before acting; never fabricate; **every documented command MUST be run and its real output captured.**
Sprints 31-34 built and audited a configurable, deterministic, recorded-data two-path §7L adjudication
engine (`instances/contested_reality/adjudication_engine.py`, hash `a60f8f7…`) + the capacity-constrained
RE-RANK (`capacity_rerank.py`, hash `f7c6a185…`), positively inventoried the whole recorded-data decision
surface as reason-not-choice (Sprint 31), proved the two paths compose as ONE coherent framework over 13 orgs
(Sprint 33), and AUDITED that one-framework answer over the ENTIRE 22-org ORG CATALOG (Sprint 34,
`run_two_path_catalog_demo.py`). **Sprint 35 is a REPRODUCIBILITY-AUDIT**: the project's core claim is
"deterministic local Python, ~$0, real tool output only," so this sprint verifies that claim holds as a
property of the actual host + corpus — no new capability, no engine/module change.

## Context — read first, in full
- Canonical spec: `/home/rlg/relational-os/SPEC.md` (v0.22). §6 (human floor), §7K.1, §7L (the ten morning
  questions), §7J.11 + §C16 (URI cap), the frozen 49 `$defs`.
- Protocol: `/home/rlg/relational-os/PROTOCOL.md` (single-threaded, plan-before-build, real output, additive,
  never bump SPEC for a capability-only change; consolidation/audit sprints stay at v0.22).
- Read FIRST, in full:
  - `instances/contested_reality/run_two_path_catalog_demo.py` (Sprint 34 — the 22-org ORG CATALOG builder +
    the whole-catalog two-path proof), `run_two_path_demo.py` (Sprint 33), `run_capacity_rerank_demo.py`
    (Sprint 32), `run_recorded_surface_demo.py` (Sprint 31), `run_cockpit_s7l_demo.py` + `run_cockpit_q7q8_demo.py`,
    and the `run_forecast_*.py` set (the org builders / ORG CATALOG source).
  - `instances/contested_reality/adjudication_engine.py` (hash `a60f8f7…`, DO NOT TOUCH),
    `capacity_rerank.py` (hash `f7c6a185…`, DO NOT TOUCH), `adjudication_configs.py`.
  - `instances/contested_reality/docs/DECISION-FRAMEWORK-BOUNDARY.md` (the Sprint-34 consolidated boundary
    cheat-sheet, the canonical reference to verify against) + `instances/contested_reality/docs/ENGINE-FORECAST-CAPACITY.md`
    (§17/§18) + `artifacts/adjudication/reports/two-path-catalog.md` (the whole-catalog report).
  - `sprints/sprint-34/{summary.md,notes/findings.md,plan.md}` + `sprints/sprint-33/summary.md` (the honest residual).
- Project invariants (the `relational-os` skill): frozen ontology / URI cap / 49 `$defs` (§C16); additive only;
  single-threaded; plan-before-build; real tool output; ~$0; footguns (two interpreters: plain `python3` for
  demos, the Sprint-0 venv `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` for
  conformance; runner CWD-sensitivity; `Graph.get` one-arg; `evidence`/`rules_applied` ARRAYS;
  `{**graph.get(u), ...}` merge-not-replace; C2 temporal-suffix keys; strict C5 tables; `eng.reconcile(sub,
  cfg)` ARG ORDER).

## What Sprint 35 IS and IS NOT
- **IS:** a positive, engine-untouched REPRODUCIBILITY-AUDIT. It (1) verifies the determinism claim holds on
  THIS host by re-running the whole-catalog two-path runner + the other CR demo runners (and confirming
  byte-identical deterministic output vs the Sprint-34 recorded results), (2) verifies the CR corpus' green
  baseline as one command (demos + conformances + build_all + conformance_all + S5 reference + agent) with
  real exit-0 output, (3) verifies the Sprint-34 consolidated boundary cheat-sheet (`DECISION-FRAMEWORK-BOUNDARY.md`)
  is ACCURATE against the live code (every cited command runs, every cited hash/def/version matches, the
  quoted taxonomy + residual match the runner's own assertions), and (4) writes a short
  `sprints/sprint-35/reproducibility.md` recording host/platform info + the verified determinism + build
  results. A survey/audit runner(s) + recorded data ONLY; `adjudication_engine.py` AND `capacity_rerank.py`
  provably byte-identical (hashes `a60f8f7…` + `f7c6a185…` recorded before and after).
- **IS NOT:** a new capability; a change to `rank`/`capacity_rerank`/the engine; a probabilistic/stochastic
  forecast; a new URI/schema/`$defs` edit; a Trust (S5) change; breaking any prior sprint's proof or any reused
  org's default output.

## The target (what "done" looks like)
1. **A new runner** `run_reproducibility_demo.py` that (a) captures host/platform facts (`uname`, Python
   version, CPU) from the live system, (b) re-runs the Sprint-34 whole-catalog two-path survey over the 22-org
   catalog and asserts the deterministic `two_path_surface` + PATH class for EVERY org EQUALS the Sprint-34
   recorded results (the {12,6,4} taxonomy, the 4 re-rank replacements, the 22/22 advisory-Q8-==-cockpit_q7q8,
   the Sprint-31/32/33 reproductions), and (c) asserts the Sprint-34 consolidated boundary doc's concrete
   claims against the live engine/module (hashes `a60f8f7…`+`f7c6a185…`, schema `34264934…`, 49 `$defs`, SPEC
   v0.22, the taxonomy numbers). Exit 0 = ALL PASS. Emits `artifacts/adjudication/reports/reproducibility.md`.
2. **No engine / no `capacity_rerank.py` change:** both byte-identical (hash `a60f8f7…` + `f7c6a185…`
   recorded before and after); non-regression green; reused orgs' default bytes intact.
3. **Green baseline verified as one whole** (the exact whole-build command set from the boundary doc, each
   exit 0).
4. **Real output:** new runner ALL PASS; the boundary doc verified-accurate (any discrepancy is a doc bug to
   fix in `DECISION-FRAMEWORK-BOUNDARY.md`, not a code change); frozen 49 `$defs`; schema `34264934…`; SPEC v0.22.
5. **Documentation:** `sprints/sprint-35/summary.md` + `notes/findings.md` + a `reproducibility.md` +
   `sprints/sprint-36/PROMPT.md`; if the audit found any stale/missing line in the boundary doc, fix it with
   a targeted edit only.

## Mandatory rules
- **Write-first:** `sprints/sprint-35/plan.md` FIRST, then `work/<n>-plan.md` before each build step.
- **Real tool output only**; honest "stuck/failed" over fabrication. On a doc discrepancy, report it plainly
  and fix the DOC, never the code.
- **Additive/audit**: keep frozen functions + `capacity_rerank.py` + the 49 `$defs`/URI cap/SPEC v0.22
  untouched; re-verify `ros/`, schema `34264934…`, sector instances, the Sprint-31/32/33/34 reuse bytes, and
  the engine + `capacity_rerank.py` hashes `a60f8f7…` + `f7c6a185…`.
- **Single-threaded** per PROTOCOL — no subagents. **Budget ~$0** — deterministic local Python only.
- **Raymond:** clean English, absolute `file://` paths, report status at each long step.

## Verification / Definition of Done (real output, all exit 0)
- Green baseline FIRST: every CR demo runner (18 incl. the new one) + all 5 CR conformances (Sprint-0 venv) +
  `build_all.py` + `conformance_all.py` + S5 reference demo + conformance + agent demo + conformance.
- New `run_reproducibility_demo.py` ALL PASS (captures host facts; re-produces the 22-org catalog determinism;
  verifies the boundary doc's concrete claims).
- Full non-regression green after the new runner; SPEC v0.22; 49 `$defs`; `ros/` + schema clean; schema hash
  `34264934…`; engine `a60f8f7…` AND `capacity_rerank.py` `f7c6a185…` byte-identical (record both).

## Documentation (roll-forward)
Additive `reproducibility.md` + an `instances/README.md` Sprint-35 entry + a "Update after Sprint 35" note in
`/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` + `sprints/sprint-35/summary.md` +
`notes/findings.md`. Do NOT bump SPEC (v0.22) unless a genuine normative gap surfaces. Update the
`relational-os` skill's Sprint-35 note.

## Hand-off requirement
Your **final message** must summarize: the host/platform facts captured, the true determinism of the two-path
framework over the whole 22-org catalog on THIS host (the {12,6,4} taxonomy + 4 re-rank replacements + the
22/22 advisory non-shadowing all reproduced byte-identical), the whole-build green baseline as one command,
whether the Sprint-34 consolidated boundary doc stands as accurate (and any doc fix made), the byte-identical
default (`a60f8f7…` + `f7c6a185…` unchanged; no new noun; frozen 49 `$defs`; schema `34264934…`; SPEC v0.22),
the honest §16 verdict (deterministic local reproducibility of the one-framework two-path decision surface
across the whole catalog is verified on this host, WHILE the still-not-derivable residual is unchanged:
probabilistic/stochastic forecast; a per-option requirement NOT unit-coupled to recorded capacity / an option
with no recorded requirement — never invented; any §6-human choice recorded data cannot machine-decide), and
the verified build + conformance commands. Write the **next** sprint's self-contained prompt at
`sprints/sprint-36/PROMPT.md` (reference only absolute paths and the current SPEC.md).