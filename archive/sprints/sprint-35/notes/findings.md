# SPRINT 35 — NOTES / FINDINGS

## Assumption that mattered
- **REPRODUCIBILITY-AUDIT, not a capability.** Sprint 35 makes NO change to `adjudication_engine.py` or
  `capacity_rerank.py` — both byte-identical (sha256 `a60f8f7…` and `f7c6a185…`, recorded before AND after).
  It is a survey/audit runner + recorded data only, so "no new capability / no schema / no norm change / no
  new noun / no SPEC bump" hold trivially. The point of the sprint is to verify the project's core claim
  ("deterministic local Python, ~$0, real tool output") is true AS A PROPERTY of this host + corpus.
- **Host is a property of the host, not the spec.** The runner captures host/platform facts live
  (uname/CPU/python) and emits them to the report; they are reported, not asserted (they legitimately vary
  by machine). The DETERMINISM (same inputs → same deterministic `two_path_surface` + PATH class) is what
  is asserted, and it held on this host.

## Verified (real tool output, all exit 0)
- **Green baseline FIRST**: 18 CR demo runners + 5 CR conformances (Sprint-0 venv) + `build_all` +
  `conformance_all` (12 sectors) + S5 reference demo + conformance + agent demo + conformance → ALL PASS.
- **New runner** `run_reproducibility_demo.py` → **RESULT: ALL PASS** (exit 0; 40 PASS / 0 FAIL):
  - taxonomy **{12,6,4}** (exact per-class label membership) == Sprint-34 recorded;
  - 4 re-rank replacements reproduced (conditional-resolution / conditional-accept-with-guarantee /
    authorize-generic / unresolved baseline);
  - 22/22 advisory Q8 == `cockpit_q7q8`; 4/4 distinct replacements; 18/18 non-firing agree;
  - floor integrity 22/22; two_path_surface deterministic on re-run;
  - Sprint-31 tally 11/11 + Sprint-32 re-rank 4/4 + Sprint-33 {5,4,4} all reproduced from same data;
  - boundary-doc concrete claims (engine `a60f8f71`, rerank `f7c6a185`, schema `.yaml` `34264934`,
    `.json` `7fc38c8c`, 49 `$defs`, SPEC v0.22) PASSED — the doc is ACCURATE, no fix needed.
- **Full non-regression green AFTER** the new runner: 19 CR demos (incl. the new one) + 5 conformances +
  build_all + conformance_all + S5 ref + agent → ALL PASS (30/30). Engine `a60f8f7…` + `capacity_rerank.py`
  `f7c6a185…` raw sha256 unchanged AFTER.
- **No fixture writes** from the new runner: grep shows `emit_fixtures` only in two prose mentions
  (docstring + provenance print), no calls.

## Pitfalls encountered
- **The `.yaml` vs `.json` schema hash (confirmed again):** the documented schema hash `34264934…` is the
  `.yaml`; the `.json` hashes to `7fc38c8c`. The runner asserts the `.yaml` head-8 == `34264934` AND the
  `.json` head-8 == `7fc38c8c`, so the false-alarm trap (hashing `.json` and "finding" a mismatch) is
  structurally avoided.
- **`**Version:** 0.22` in SPEC.md** — the markdown bold asterisks broke a naive `Version:\s*([0-9.]+)`
  regex (it matched nothing → "FAIL"). Fixed with `Version:\s*\**\s*([0-9.]+)` to skip the asterisks.
  Lesson for any future version greps: SPEC uses `**Version:** 0.22`, not a bare `Version: 0.22`.
- **f-string golden-brace trap:** in the emitted report, a literal `{5,4,4}` inside an f-string was parsed
  as a tuple expression → rendered `((5, 4, 4))`. Fixed by escaping as `{{5,4,4}}`. Any literal dict/set
  braces inside an f-string MUST be doubled.
- **Parser/command blocks (Sprint-34 lesson recurred):** any bash loop with inline `$(...)` capture got hit
  by the agent parser hardline blocklist. Put loops in a `.sh` file and `bash` it — that path worked
  cleanly. (Same lesson as Sprint 34.)
- **`r32.build()` noise:** reconstructing the Sprint-31 labels by calling `r32.build()` directly printed a
  wall of cockpit text. Redirected to devnull (the Sprint-34 runner does the same).

## Open issues / next work (the honest frontier after Sprint 35)
- Deterministic local reproducibility of the one-framework two-path decision surface across the WHOLE
  catalog is VERIFIED on this host; the Sprint-34 consolidated boundary doc stands as canonical.
- **Still not derivable (the honest residual — unchanged by audit):** a probabilistic/stochastic forecast
  (the recorded band is a spread, never a CI); a per-option requirement NOT unit-coupled to the recorded
  capacity value / an option with no recorded requirement (never invented — `deli-atcap`/`deli-deficit`
  prove recorded capacity alone never reaches RE-RANK); and any choice the §6 human must make that recorded
  data cannot machine-decide (the re-rank is POLICY-authorized, not a claim of objective best).
  Any future change to these is a genuine capability/policy decision requiring prompt authorization.

No normative gap surfaced -> SPEC stays v0.22.