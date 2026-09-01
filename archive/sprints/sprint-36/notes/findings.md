# SPRINT 36 — NOTES / FINDINGS

## Assumption that mattered
- **CORPUS-CONSISTENCY note, not a capability.** Sprint 36 makes NO change to `adjudication_engine.py` or
  `capacity_rerank.py` — both byte-identical (sha256 `a60f8f7…` and `f7c6a185…`, recorded before AND after).
  It is a survey/audit runner + recorded data + doc consolidation only, so "no new capability / no schema /
  no norm change / no new noun / no SPEC bump" hold trivially. Its point is to (a) prove the Sprint-35
  reproducibility FIGURE reproduces from the CURRENT corpus in a fresh run, and (b) prove the two boundary
  docs (`DECISION-FRAMEWORK-BOUNDARY.md` + `ENGINE-FORECAST-CAPACITY.md` §17/§18) are mutually consistent and
  consistent with the live corpus.
- **Clean reuse beats duplication the first time we noticed a trap.** Rather than copy the 22-org survey into
  the new runner, `run_corpus_consistency_demo.py` literally imports `run_reproducibility_demo` and calls
  `run_all()` — the Sprint-35 figure re-run IS the Sprint-35 runner, so there is exactly one source of truth
  for the determinism assertions and no risk of a second copy silently diverging.
- **The boundary cheat-sheet asserts the MECHANISM, not the value list.** My first draft of (b) required
  `DECISION-FRAMEWORK-BOUNDARY.md` to literally name the 4 re-rank replacement options
  (conditional-resolution / conditional-accept-with-guarantee / authorize-generic / unresolved). The doc does
  NOT name them — it states "4 RE-RANK firings, provably-distinct replacement" (a mechanism claim) and points
  to `two-path-catalog.md` (its §1 report) for the detail. Requiring the values in the cheat-sheet was a false
  positive, NOT a doc bug. Fixed the audit: assert the cheat-sheet's count + mechanism claim, AND assert the
  detail report it cites records the 4 live replacement values. That is the faithful corpus-consistency check.

## Verified (real tool output, all exit 0)
- **Green baseline FIRST**: 19 CR demo runners (the 18 canonical + `run_reproducibility_demo`) + 5 CR
  conformances (Sprint-0 venv) + `build_all` + `conformance_all` (12 sectors) + S5 reference demo + conformance
  + agent demo + conformance → ALL PASS.
- **New runner** `run_corpus_consistency_demo.py` → **RESULT: ALL PASS** (exit 0):
  - (a) Sprint-35 reproducibility FIGURE re-run from the CURRENT corpus reproduces byte-identical: taxonomy
    **{12,6,4}** (exact per-class membership), 4 re-rank replacements, **22/22** advisory Q8 == `cockpit_q7q8`,
    floor integrity 22/22, two_path_surface deterministic on re-run, Sprint-31 11/11 + Sprint-32 4/4 +
    Sprint-33 {5,4,4} all reproduced;
  - (b) cross-doc/corpus: DECISION-FRAMEWORK-BOUNDARY.md §3's 12/6/4 class org lists parse and each == the
    live per-class set; it states the 4-firings mechanism + the cited `two-path-catalog.md` records all 4
    replacement values == live; ENGINE-FORECAST-CAPACITY.md §18 states {12,6,4}=22 + the 9-added split + same
    hashes; §17's 13-org {5,4,4} orgs are the live subset; the two docs are mutually consistent; NO drifted
    number, NO stale org list → NO doc fix needed.
- **Full non-regression green AFTER**: 20 CR demos (incl. the new one) + 5 conformances + build_all +
  conformance_all + S5 ref + agent → ALL PASS. Engine `a60f8f7…` + `capacity_rerank.py` `f7c6a185…` raw sha256
  unchanged AFTER.
- **No fixture writes** from the new runner: `grep -c emit_fixtures run_corpus_consistency_demo.py` = 2, both
  prose mentions (docstring + provenance print), no calls.

## Pitfalls encountered
- **The `.yaml` vs `.json` schema hash (confirmed a third time):** the documented hash `34264934…` is the
  `.yaml`; the `.json` is `7fc38c8c`. The runner asserts the `.yaml` head-8 == `34264934` AND the `.json`
  == `7fc38c8c`, so the false-alarm trap stays structurally avoided.
- **`**Version:** 0.22` in SPEC.md:** the bold asterisks still break a naive `Version:\s*([0-9.]+)` regex; use
  `Version:\s*\**\s*([0-9.]+)`.
- **f-string golden-brace trap (recurred):** any literal `{5,4,4}` inside an emitted f-string must be doubled
  `{{5,4,4}}`, else Python parses it as a tuple expression.
- **Parser blocklist on inline `$(...)` (recurred):** put the 19/20-demo loops in `.sh` files and `bash` them —
  that path works cleanly.
- **Doc-parsing brittleness → first-run false positives:** the assert helper parsed the §3 taxonomy table with
  a regex over `| **<count>** | <orgs> |` cells. It worked, but the "doc must name each replacement value"
  checks FAILED simply because the cheat-sheet never enumerates those values (it delegates to
  `two-path-catalog.md`). Re-typed those 4 checks to assert the mechanism claim + the cited report's recorded
  values → ALL PASS without touching the (accurate) doc. Lesson: an audit must check the claims a doc ACTUALLY
  makes, not claims it delegates to the detail report.

## Open issues / next work (the honest frontier after Sprint 36)
- The Sprint-35 reproducibility record is reproducible AS A FIGURE from the current corpus, and the two
  boundary docs are mutually consistent + consistent with the live corpus (verified, no doc fix needed).
- **Still not derivable (the honest residual — unchanged by audit):** a probabilistic/stochastic forecast
  (the recorded band is a spread, never a CI); a per-option requirement NOT unit-coupled to the recorded
  capacity value / an option with no recorded requirement (never invented — `deli-atcap`/`deli-deficit` prove
  recorded capacity alone never reaches RE-RANK); and any choice the §6 human must make that recorded data
  cannot machine-decide (the re-rank is POLICY-authorized, not a claim of objective best). Any future change
  to these is a genuine capability/policy decision requiring prompt authorization.
- **The series ends here (PROTOCOL step 8).** Sprints 20–36 have built and re-audited the whole recorded-data
  §7L two-path decision surface; every derivable seam is closed and the boundary is honestly stated (the
  probabilistic/stochastic frontier, non-unit-coupled per-option capacity, and the §6-human floor). A sprint
  37 would be only another ritual re-audit over byte-identical inputs — it would add no new capability, no
  new proof, and no new audit surface. Per PROTOCOL, write `sprints/sprint-36/COMPLETE.md`, write NO
  `sprint-37/PROMPT.md`, and say plainly "nothing new left for a sprint; series ends here."

No normative gap surfaced -> SPEC stays v0.22.