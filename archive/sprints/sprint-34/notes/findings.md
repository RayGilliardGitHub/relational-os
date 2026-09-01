# SPRINT 34 — NOTES / FINDINGS

## Assumptions that mattered
- **Consolidation-ADUIT, not a capability.** Sprint 34 makes NO change to `adjudication_engine.py` or
  `capacity_rerank.py` — both byte-identical (sha256 `a60f8f7…` and `f7c6a185…` recorded before AND after).
  It is a survey/audit runner + recorded data only, so "no new capability / no schema / no norm change / no
  new noun / no SPEC bump" hold trivially.
- **The ORG CATALOG is derived from the EXISTING runners, not invented.** The union of every org the CR demo
  runners construct = **22 distinct labels**: the 13-org `r32.build()` set + `deli-forecast-flat`/`deli-cost`/
  `deli-cost-flat` (forecast/direction family) + `deli-atcap`/`deli-deficit` (`run_forecast_horizon4_demo.
  build_orgs`) + `cove` (base COVE from `run_adjudication_engine_demo` SCENARIOS) + `inspect-corroboration`/
  `inspect-learn-b`/`deli-learn` (the cockpit learned-rule orgs). Each is built fresh in memory via its OWN
  existing builder (r32.build / the forecast construction / build_orgs / the cockpit learned construction /
  base-covered `run_one(ac.COVE)`).
- **Classification is exhaustive-disjoint by construction, then asserted.** The Sprint-33 `_classify` is a
  pure function of recorded data: capacity block absent → ADVISORY-no-capacity; present + best
  `capacity_infeasible` → RE-RANK; else ADVISORY-best-runnable. I assert every catalog org maps to exactly
  one class and `needed == (path == RE-RANK)`.
- **The two new best-runnable orgs expose a clean boundary instance.** `deli-atcap`/`deli-deficit` record an
  authority `capacity` but NO per-option `capacity_requirements`, so the machine best is `capacity_risk` —
  never `capacity_infeasible` — and there is provably nothing to re-rank. This is the honest "recorded
  capacity alone cannot reach RE-RANK; a recorded per-option requirement is required" data point.
- **Fixture bytes are not the "reused-org bytes".** As in Sprint 33, CR fixture files carry `now_iso()`
  timestamps and wander run-to-run; the meaningful byte-identity is (i) engine + `capacity_rerank.py` sha256
  (verified) and (ii) the deterministic q7/q8/re-rank OUTPUT (proven by the determinism-vs-history
  assertions). My new runner writes NO fixtures (0 `emit_fixtures` calls) — confirmed: only the report +
  the runner files are new/untracked; no new fixture dir.

## Verified (real tool output, all exit 0)
- **Green baseline FIRST** (Sprint-33 state): all 17 CR demo runners (11 forecast + cockpit q7q8/s7l +
  recorded-surface + capacity-rerank + two-path + adjudication-engine) ALL PASS; all 5 CR conformances
  (Sprint-0 venv) ALL PASS; `build_all` + `conformance_all` (12 sectors) ALL PASS; S5 reference demo +
  conformance ALL PASS; agent demo + conformance ALL PASS. Engine `a60f8f7…`, `capacity_rerank.py`
  `f7c6a185…`, schema `34264934…` (yaml sha256), 49 `$defs`, SPEC v0.22.
- **New runner** `run_two_path_catalog_demo.py` → **RESULT: ALL PASS** over the WHOLE 22-org catalog:
  - (a) advisory never shadowed — 22/22 advisory Q8 == `cockpit_q7q8`; 4/4 RE-RANK orgs pick a
    provably-distinct replacement (≠ advisory Q8 ≠ machine_eligible_best); 18/18 non-firing orgs agree
    (replacement == advisory Q8);
  - (b) exhaustive-disjoint taxonomy **{12 ADVISORY-no-capacity, 6 ADVISORY-best-runnable, 4 RE-RANK}**;
    needed == (RE-RANK) for all 22; no-capacity orgs carry no capacity_constraint block; best-runnable orgs do;
  - (c) floor integrity 22/22 (asserted against the frozen `rank`);
  - (d) determinism 22/22 + Sprint-31 tally 11/11 + Sprint-32 4 firings + Sprint-33 {5,4,4} ALL reproduced.
- **Full non-regression green AFTER** the new runner: 18 CR demos (incl. the new one) + 5 conformances +
  build_all + conformance_all + S5 ref + agent → ALL PASS. Engine `a60f8f7…` + `capacity_rerank.py`
  `f7c6a185…` raw sha256 unchanged after; schema `34264934…`; 49 `$defs`; SPEC v0.22; no new noun; no new
  fixture dirs.

## Pitfalls encountered
- **The whole-catalog taxonomy is NOT the 13-org set + a fixed fraction.** The 9 added orgs split 7/2, not
  6/3: the three forecast control orgs (deli-forecast-flat, deli-cost, deli-cost-flat) + cove + three cockpit
  orgs carry NO recorded capacity (7 no-capacity), while only deli-atcap/deli-deficit carry capacity (2
  best-runnable). I asserted the distribution rather than assuming it — it came out {12,6,4}.
- **Building `inspect-learn-b`/`deli-learn` requires the learned-rule construction** (learn_threshold from
  LEARN_HYPER + build_learned_library_spec + RULE_LIBRARY inject + record_learned_rule on inspect-learn-b's
  OWN ledger, so learned-this-run reads True). I replicated the cockpit construction exactly; the learned
  orgs are no-capacity (no capacity recorded), so they classify ADVISORY-no-capacity regardless — but
  building them faithfully is what keeps the catalog the TRUE union.
- **Parser blocklist** hit on a compound loop with inline `$(...)` capture (same Sprint-33 lesson). Split into
  small sequential commands; a simple `for` loop with `grep RESULT` after redirect (no inline substitution in
  the loop head) is fine.
- **Pyright `reportMissingImports` on `ros.substrate`** in the new runner — the known, expected artifact of
  the runtime `sys.path` injection (identical to every CR runner); not a defect.

## Open issues / next work (the honest frontier after Sprint 34)
- The two-path decision surface is ONE coherent recorded-data framework across the WHOLE ORG CATALOG (22
  orgs); the deterministic advisory label-vs-choice boundary still holds on the default path.
- **Still not derivable (the honest residual — unchanged by audit):** a probabilistic/stochastic forecast
  (the recorded band is a spread, never a CI); a per-option requirement NOT unit-coupled to the recorded
  capacity value (no available figure → no infeasibility label → nothing to re-rank); an option with no
  recorded requirement carries no infeasibility label (the machine never invents one — `deli-atcap`/
  `deli-deficit` prove recorded capacity alone never reaches RE-RANK); and any choice the §6 human must make
  that recorded data cannot machine-decide (the re-rank is POLICY-authorized, not a claim of objective best).
  Any future change to these is a genuine capability/policy decision requiring prompt authorization.

No normative gap surfaced -> SPEC stays v0.22.