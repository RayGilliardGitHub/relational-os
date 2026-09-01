# work/4 — plan: documentation + hand-off

Do FIRST: work/3 done — 13-label conformance ALL PASS, all prior CR demos + conformances green,
sectors build+conformance green, S5 + agent green, invariants (49 $defs, SPEC v0.22, ros clean, no
new scheme). All verified real output above.

## Docs to write/update (no SPEC bump)
1. **NEW** `instances/contested_reality/docs/USER-AUTHORABLE-RULE-LIBRARY.md` — the Sprint-16
   write-up: the new `bayesian-combine` primitive (semantics, what it expresses the old vocab could
   not, determinism + strictness), the named cross-org RULE_LIBRARY + the `is`-identity reuse proof,
   orgs driven (majority on inspect+deli; independent-corroboration on inspect+cove), the verdict
   flip at 0.98 (max UNRESOLVED → bayesian rework-partial-credit), the §7L Q7 active-rule/source
   surface, the updated expressiveness frontier + §16 verdict, and the precise residual dependence
   on a builtin.
2. **Append** an "Update after Sprint 16" note to the verification/frontier section of
   `instances/contested_reality/docs/USER-AUTHORABLE-RULE-DSL.md` (new primitive + broadened frontier).
3. **Append** a Sprint-16 entry to `instances/README.md` (under the contested-reality section).
4. **Append** an "Update after Sprint 16" block to
   `/home/rlg/Downloads/completeness-review/STRESS-TEST-SCENARIOS.md`.
5. `sprints/sprint-16/summary.md` + `notes/findings.md` (dated packet, mirroring Sprint 15's shape).
6. **NEW** `sprints/sprint-17/PROMPT.md` (the next self-contained sprint prompt).

## Final verification before declaring done
Re-run `run_rule_library_demo.py` (ALL PASS) once more after all docs, and confirm the exact
hand-off claims (new primitive; library across >=2 orgs; Q7 active rule + source; §16 with precise
residual seam). Clean English, absolute file:// paths.

DoD: all docs present + honest; summary + findings written; next prompt written; all real commands
exit 0.