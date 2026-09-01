# SPRINT 32 — SUMMARY: the capacity-constrained RE-RANK of the §7L Q8 recommendation for the machine, BY THE FROZEN `rank` UTILITY, as an EXPLICIT authorized POLICY step (built because THIS prompt asked for it)

## Goal
Sprint 30/31 closed the INVENTORY on the whole recorded-data §7L decision surface as reason-not-choice:
every derived label traces to a RECORDED descriptor and the Q8 recommendation provably stays the frozen
`rank` output (the marker is a REASON, never a CHOICE). They named the ONE remaining out-of-scope step
EXACTLY: a **capacity-constrained OPTIMIZATION that RE-RANKS the Q8 recommendation for the machine** — a
deliberate "re-rank for the machine" POLICY / user decision, NOT a label, whose seam is recorded per-option
`capacity_requirements` (already present) + a deterministic next-best-non-infeasible rule by the frozen
`rank` utility (the only missing piece). **Sprint 32 builds exactly that, because its prompt explicitly
asked for it.** It is additive, deterministic, generic, and provably DISTINCT from the unchanged
reason-not-choice advisory. **NO engine change** — `adjudication_engine.py` is byte-identical (sha256
`a60f8f7…` confirmed before and after); the re-rank is a NEW pure module + a new runner + recorded data,
the Sprint 29/30/31 proof shape. No new noun; frozen 49 `$defs`; SPEC v0.22; `ros/` + schema + sector
`configs.py` untouched; ~$0.

## The build: `capacity_rerank.py` (new module) + `run_capacity_rerank_demo.py` (new runner, exit 0 = ALL PASS)
`capacity_rerank(cfg, sub, *, library=None)` reuses ONLY the engine's public surface: the `capacity_constraint`
block `cockpit_s7l` renders from recorded data (present iff the org records a numeric authority `capacity`
+ a band + a threshold; its `options_flagged` labels each capacity-consuming option `capacity_infeasible` /
`capacity_risk` from recorded per-option `capacity_requirements` vs available = capacity.value − load) and
the frozen `rank(cfg)` utility. When the machine-eligible best IS `capacity_infeasible`, it walks the frozen
`rank` ordering and picks the **first option that is neither floor-gated nor `capacity_infeasible`** — the
highest-utility non-infeasible non-gated option. It emits an additive `capacity_rerank` block (`prior_machine_best`,
`prior_best_capacity_flag`, `recorded_descriptors`, `available_capacity`, `per_option_requirements`,
`replacement`, `replacement_is_baseline`, `all_capacity_consuming_infeasible`, `floor_respected`, `policy`,
`why`), respects the §6 floor (a floor-gated option is never auto-picked), never invents a requirement, and
falls back to the do-nothing/UNRESOLVED baseline (stating so) when every capacity-consuming option is
infeasible. It NEVER overwrites the engine's advisory Q8 recommendation — the re-ranked selection is
reported AS DATA.

## What is proven (all real exit-0 output)
Drives **13 orgs** (the eleven Sprint-31 orgs byte-identical + NEW `cove-recommend-infcap` + NEW
`deli-all-infeasible`; new labels, no fixture overwrite):
- **RE-RANK fires** (machine best `capacity_infeasible` → a replacement is chosen):
  `deli-recommend-infcap` `partial-settlement` → `conditional-resolution`; `inspect-recorded`
  `rework-partial-credit` → `conditional-accept-with-guarantee`; `cove-recommend-infcap` (NEW)
  `step-therapy-first` → `authorize-generic`; `deli-all-infeasible` (NEW — EVERY capacity-consuming option
  infeasible) → `unresolved` baseline with `replacement_is_baseline` True + `all_capacity_consuming_infeasible`
  True (the honest fallback is SAID). For each, the re-ranked Q8 == the recomputed highest non-infeasible
  non-gated utility option by the frozen `rank` (belt-and-suspenders recompute asserted).
- **UNCHANGED** (best NOT infeasible → byte-identical to `cockpit_q7q8`): the nine other orgs, incl.
  `cove-recorded` (best `step-therapy-first` = capacity_risk, runnable) and the no-data org `inspect-nodata`.
- **The advisory path NEVER re-ranks**: even where re-rank fires, the engine's Q8 recommendation still
  equals `cockpit_q7q8` — the Sprint-31 reason-not-choice inventory provably stands untouched; the re-rank
  is the distinct, authorized POLICY step, reported as DATA.
- **Determinism** (dict equality on re-run for all 13 orgs); **§6 floor respected** (replacement never in
  `floor_gated` — asserted against the frozen `rank`); the two NEW fixture dirs pass **Sprint-0 C1-C5**.

## Verification (all exit 0, plain python3 + Sprint-0 venv for conformance)
- NEW runner: `python3 run_capacity_rerank_demo.py` → **RESULT: ALL PASS**.
- New-org fixtures `cove-recommend-infcap` + `deli-all-infeasible` pass C1-C5 (Sprint-0 venv, conformance
  FIXTURES pointed at each dir → ALL PASS: C1 49 `$defs`; C2 23 / 26 instances; C3-C5 pass).
- Full non-regression (captured twice — green Sprint-31 baseline first, again after the new files):
  all 15 plain-python3 CR demo runners + all 5 CR conformances + `build_all`/`conformance_all` (12 sectors)
  + S5 reference demo + conformance + agent demo + conformance → ALL PASS.
- Invariants: engine raw sha256 `a60f8f7…` UNCHANGED; schema `7fc38c8c…`; **49 `$defs`**; SPEC v0.22;
  `ros/` + schema + sector `configs.py` untouched; no `://qk/` in the two new fixture dirs; no new noun.

## Documents rolled forward
`docs/ENGINE-FORECAST-CAPACITY.md` §16 · `docs/ENGINE-S7L-COCKPIT.md` §14 · `instances/README.md` Sprint-32
entry · `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md` "Update after Sprint 32" · the
engine-native report `artifacts/adjudication/reports/capacity-rerank.md` · the `relational-os` skill note.
No SPEC bump (v0.22).

## Honest §16 verdict
**Sprint 30/31's ONE remaining frontier — a capacity-constrained, re-ranked Q8 recommendation under recorded
capacity — is now DERIVABLE, as an explicit authorized POLICY step distinct from the deterministic advisory
label-vs-choice boundary.** The advisory path still labels (even the RECOMMENDED option `capacity_infeasible`)
and NEVER re-ranks: the Sprint-31 reason-not-choice inventory provably stands (every engine Q8 recommendation
== `cockpit_q7q8`, including the orgs where re-rank fires). The re-rank computes, from RECORDED per-option
`capacity_requirements` + the frozen `rank` ordering, the highest-utility option that is neither floor-gated
nor `capacity_infeasible`; it changes the Q8 recommendation only under the machine's explicit POLICY, never
on the advisory path; it respects the §6 floor; and it is deterministic + additive (new module, engine
byte-identical hash `a60f8f7…`). **Still not derivable (the honest residual):** a probabilistic/stochastic
forecast (the recorded band remains a spread, never a CI — nothing invents a distribution); a per-option
requirement NOT unit-coupled to the recorded capacity value (no available figure → no infeasibility label →
nothing to re-rank); an option with no recorded requirement carries no infeasibility label (the machine never
invents one for it); and any choice the §6 human must make that recorded data cannot machine-decide (the
re-rank is POLICY-authorized, not a claim of objective best). No SPEC bump (v0.22), no new noun.