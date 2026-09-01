# work/3-plan.md — conformance + full non-regression + §16 verdict

**Objective.** Prove the generalized engine adds no schema/ontology drift and no regression, then
decide-and-document where the §16 "new category" verdict now sits.

## Conformance over the new fixtures
- `conformance_adjudication.py` (Sprint-0 venv) runs C1–C5 over BOTH `deli` and `cove` fixtures.
  Result: `ADJUDICATION-ENGINE CONFORMANCE: ALL PASS`, exit 0, `49 $defs` intact (schema untouched).
- Two fixes the validator surfaced (all schema-compliant, no schema edit):
  - `Relationship` requires `status` -> added `status: ACTIVE`.
  - `Obligation.source` is a frozen enum `[IMPOSED, VOLUNTARILY_UNDERTAKEN]` -> replaced the
    non-member `PROFESSIONAL_STANDARD` with `IMPOSED`.

## Full non-regression suite (all exit 0 = ALL PASS)
S5 reference demo + all-six conformance; contested-reality dispute/interest/tradeoff/lifecycle
demos + conformance; **new** adjudication-engine demo + conformance; agent demo + conformance;
sectors `build_all.py` + `conformance_all.py`. Every step green; no reference-byte change.

## §16 verdict (decide + document)
Judge whether the Sprint-12 "B — Partially" verdict moves toward "A — Yes" now that adjudication is
a general configurable capability and is cockpit-rendered (the two things §16 said were missing).
Honest conclusion: materially stronger, but still not unqualified "A" — see
`docs/GENERALIZED-ADJUDICATION.md` for the precise hinge.