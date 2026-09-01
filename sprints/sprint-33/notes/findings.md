# SPRINT 33 — NOTES / FINDINGS

## Assumptions that mattered
- **Consolidation, not capability.** Sprint 33 makes NO change to the engine or to `capacity_rerank.py` —
  both byte-identical (verified sha256 `a60f8f7…` and `f7c6a185…` before AND after). It is a survey/audit
  runner + recorded data only, so the "no new capability / no schema / no norm change / no new noun /
  no SPEC bump" invariants hold trivially.
- **The two paths are defined by the SAME recorded data, not by machinery.** The ADVISORY (a REASON, never a
  CHOICE) and the RE-RANK (the authorized POLICY step) both read the engine's recorded `capacity_constraint`
  block + the frozen `rank`. The consolidation is therefore a VIEW over one dataset, which is exactly what the
  "determinism vs history" assertion proves (Sprint-31 tally + Sprint-32 re-rank results both reproduce in this
  run).
- **Classification is exhaustive-disjoint by construction, then asserted.** The class is a pure function of
  recorded data: capacity block absent → ADVISORY-no-capacity; present + best `capacity_infeasible` → RE-RANK;
  else ADVISORY-best-runnable. I assert the class is in the 3-set, each org maps to exactly one, and `needed
  == (path == RE-RANK)` — so an org can never be two classes.
- **Fixture bytes are not the "reused-org bytes" to preserve.** CR fixture files carry `now_iso()` timestamps,
  so every run of ANY demo re-emits them with fresh bytes (this predates Sprint 33). The meaningful
  byte-identity is (i) engine + `capacity_rerank.py` sha256 (verified) and (ii) the deterministic q7/q8/re-rank
  OUTPUT given the same recorded descriptors (proven by the determinism-vs-history assertions). My new runner
  writes NO fixtures (built fresh in memory), so it cannot alter any reused org's recorded data — confirmed: no
  new fixture dir appeared.

## Verified (real tool output, all exit 0)
- **Green baseline FIRST** (Sprint-32 state): 16 plain-python3 CR demo runners + all 5 CR conformances
  (Sprint-0 venv) + `build_all` + `conformance_all` (12 sectors) + S5 reference demo + conformance + agent
  demo + conformance → ALL PASS. Engine `a60f8f7…`, `capacity_rerank.py` `f7c6a185…`, schema `34264934…`,
  49 `$defs`, SPEC v0.22.
- **New runner** `run_two_path_demo.py` → **RESULT: ALL PASS**: (a) composition — advisory Q8 == `cockpit_q7q8`
  for 13/13; 4 RE-RANK orgs pick a provably-different replacement ≠ machine_eligible_best; 9 unchanged agree
  (replacement == advisory Q8); (b) floor integrity 13/13 (asserted against `rank`); (c) exhaustive-disjoint
  taxonomy {5 ADVISORY-no-capacity, 4 ADVISORY-best-runnable, 4 RE-RANK}; (d) determinism 13/13 +
  Sprint-31 tally 11/11 + Sprint-32 re-rank results reproduced.
- **Full non-regression green AFTER** the new runner: 17 CR demos + conformances + build_all + conformance_all
  + S5 ref + agent demo + conformance → ALL PASS.
- Admin: no new fixture dirs; engine `a60f8f7…` + `capacity_rerank.py` `f7c6a185…` raw sha256 unchanged after.

## Pitfalls encountered
- **The long one-liner verification command tripped the terminal parser's blocklist** (oversized/malformed
  inline with nested subshells + cut/find pipelines). I split it into small sequential commands — sha256sum
  line, per-org fixture-hash loop, spec/defs grep — each clean. Lesson (consistent with the runbook's "never
  inline printf for doc append"): keep any compound verification in short, simple commands, not one giant
  pipe.
- **Compiler's `now_iso()` means fixture bytes wander run-to-run** (noted above). I did NOT try to preserve
  fixture-file bytes as a Sprint-33 claim; the honest invariance is engine/module hashes + deterministic
  output, both verified.
- **Pyright `reportMissingImports` on `ros.substrate`** in the new runner is the known, expected artifact of
  the runtime `sys.path` injection (identical to every CR runner); not a defect, `lint`/`lsp_diagnostics`
  clean for the Python itself.

## Open issues / next work (the honest frontier after Sprint 33)
- The two-path decision surface is now ONE coherent, provably-composable recorded-data framework; the
  deterministic advisory label-vs-choice boundary still holds on the default path.
- **Still not derivable (the honest residual — unchanged by consolidation):** a probabilistic/stochastic
  forecast (the recorded band is a spread, never a CI — nothing invents a distribution); a per-option
  requirement NOT unit-coupled to the recorded capacity value (no available figure → no infeasibility label →
  nothing to re-rank); an option with no recorded requirement carries no infeasibility label (the machine
  never invents one); and any choice the §6 human must make that recorded data cannot machine-decide (the
  re-rank is POLICY-authorized, not a claim of objective best). Any future change to these is a genuine
  capability/policy decision requiring prompt authorization.

No normative gap surfaced -> SPEC stays v0.22.