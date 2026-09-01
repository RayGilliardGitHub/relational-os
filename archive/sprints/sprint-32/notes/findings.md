# SPRINT 32 — NOTES / FINDINGS

## Assumptions that mattered
- **NO engine change.** Sprint 32 is the FIRST capability change since Sprint 29 (the earlier per-option
  capacity), but it is built EXACTLY as Sprint 29/30/31: a NEW pure module (`capacity_rerank.py`) + a new
  runner + recorded data. `adjudication_engine.py` sha256 = `a60f8f7…` verified BEFORE and AFTER — identical.
  The re-rank reuses only the engine's PUBLIC/importable surface (`cockpit_s7l`'s `capacity_constraint`
  block + the frozen `rank`), so no engine change was needed — which also maximally preserves "the advisory
  path never re-ranks" (the re-rank lives in a new file, explicitly layered on top).
- **The DEFAULT advisory path must stay reason-not-choice.** The re-rank therefore NEVER overwrites the
  engine's q8.recommendation; it emits an additive `capacity_rerank` block and the runner reports the
  re-ranked selection AS DATA, alongside the unchanged advisory recommendation. This is what keeps the two
  provably distinct: the advisory path never re-ranks (Sprint-31 inventory intact), the re-rank PATH changes
  the recommendation only by explicit POLICY.
- **Which orgs actually re-rank**: from the Sprint-31 11-org set, only `deli-recommend-infcap`
  (`partial-settlement` infeasible) and `inspect-recorded` (`rework-partial-credit` infeasible) have an
  infeasible machine best. `cove-recorded`'s best (`step-therapy-first`) is capacity_risk, NOT infeasible
  (its recorded requirement 28.0 <= available 29.1) — so it is the *unchanged-with-requirements* proof, a
  genuinely useful contrast. To satisfy the prompt's "add INSPECT/COVE variants" (re-rank firing in each
  family) I added `cove-recommend-infcap` (Sprint-30 recommend-infcap pattern: step-therapy-first req 30.0 >
  avail 29.1 -> infeasible -> authorize-generic) and, to prove the fallback branch honestly, `deli-all-infeasible`
  (every non-baseline option infeasible -> unresolved baseline).
- **The fallback's semantics**: the do-nothing/UNRESOLVED baseline is NEVER floor-gated and NEVER flagged, so
  it is always reachable — the fallback flag must mean "no runnable NON-baseline option remains", not "no
  runnable option at all". I fixed the loop to track `nonbaseline_runnable` separately so
  `replacement_is_baseline`/`all_capacity_consuming_infeasible` are True only when the ONLY runnable option
  (by frozen rank) is the baseline, which is the honest "every capacity-consuming option is infeasible" case.

## Verified (real tool output, all exit 0)
- **Green baseline captured FIRST** (Sprint-31 state): all 15 plain-python3 CR demo runners (incl.
  `run_recorded_surface_demo.py`) + all 5 CR conformances (Sprint-0 venv) + `build_all`/`conformance_all`
  (12 sectors) + S5 reference demo + conformance + agent demo + conformance -> ALL PASS. Engine `a60f8f7…`,
  schema `7fc38c8c…`, 49 `$defs`, SPEC v0.22.
- **New runner** `run_capacity_rerank_demo.py` -> **RESULT: ALL PASS**: 4 re-rank orgs each asserted against a
  belt-and-suspenders recompute (re-ranked Q8 == recomputed highest non-infeasible non-gated from frozen
  `rank`); 9 unchanged orgs byte-identical to `cockpit_q7q8`; §6 floor respected (asserted against `rank`);
  determinism on re-run for all 13; advisory-vs-re-rank DISTINCT (engine Q8 == `cockpit_q7q8` even where
  re-rank fires).
- **New-org fixtures pass Sprint-0 C1-C5** (`cove-recommend-infcap`: 23 instances; `deli-all-infeasible`: 26
  instances; C3 ledger content-addressed/signed; C5 legal state-machine tables).
- **Full non-regression still green after the new files.** Engine hash `a60f8f7…` unchanged; schema
  `7fc38c8c…`; 49 `$defs`; SPEC v0.22; `ros/` + schema + sector `configs.py` untouched; no `://qk/` in the
  two new fixture dirs; no new noun.

## Pitfalls encountered
- **`cockpit_q7q8` does NOT carry the capacity_constraint block** — it lives only on `cockpit_s7l`'s q7/q8.
  My first probe read it from `cockpit_q7q8` and got all `-` (no flags); the re-rank module must read the
  `capacity_constraint` from `cockpit_s7l`. (Reason-not-choice uses s7l for the same reason.)
- **`record_metric_series` requires `name` + `formula`** in `fields` (Metric-required). A first probe with a
  name-less series hit `AssertionError`. Add both required keys to any new series.
- **Shell heredoc/one-liner with backticks + quotes** broke `terminal` (the blocklist; the whole command
  became an unparseable payload containing eval-danglers). Fixed by writing the markdown to a temp file with
  `write_file` and appending via `python3 -c` — never inline printf for doc append text.
- **Pyright noise** on the new module/runner (`ros.substrate` unresolved, optional-dict access) is the known,
  expected artifact of the runtime `sys.path` injection + the shared `build_orgs()` — identical to every CR
  runner; not a defect.
- **A first minified `assert all(REQS[o] > avail for ...)` on three options** written as a garbled walrus
  expression failed to parse; rewrote as a clean one-line assertion over the name list. Assertions catch bad
  fixture tuning at runtime (a probe would have caught a req not > available).

## Open issues / next work (the honest frontier after Sprint 32)
- **The ONE remaining out-of-scope step (Sprint 30/31) is now BUILT and PROVEN as an explicit authorized
  POLICY step.** The deterministic advisory label-vs-choice boundary still holds on the default path (the
  Sprint-31 inventory provably stands); the re-rank is the distinct, POLICY-authorized capability.
- **Still not derivable (the honest residual):** a probabilistic/stochastic forecast (the recorded band is a
  spread, never a CI — nothing invents a distribution); a per-option requirement NOT unit-coupled to the
  recorded capacity value (no available figure -> no infeasibility label -> nothing to re-rank); an option
  with no recorded requirement carries no infeasibility label (the machine never invents one); and any choice
  the §6 human must make that recorded data cannot machine-decide (the re-rank is a POLICY choice, not a
  claim of objective best). A future change to any of these is a genuine capability/policy decision requiring
  prompt authorization (as this one did).

No normative gap surfaced -> SPEC stays v0.22.