# work/3 — conformance + full non-regression

**Objective.** Prove the config-authorable rule layer is fully schema-valid on the frozen ontology
and that nothing else in the build regressed.

## Plan
- Extend `conformance_adjudication.py` labels to (`deli`, `cove`, `inspect-best`, `inspect-anchor`,
  `inspect-rec`) → C1–C5 over the new rule-variant fixtures (Sprint-0 venv).
- Re-run the whole green suite after the engine change:
  - adjudication engine demo (deli/cove — must still reproduce) + adjudication conformance (5 labels)
  - the four prior contested-reality demos + conformances (dispute, interest, tradeoff, lifecycle)
  - sectors `build_all.py` + `conformance_all.py`
  - S5 reference demo + all-six conformance
  - agent demo + conformance
- Frozen-ontology checks: SPEC.md hash (v0.22) unchanged; `relational-os.schema.json` hash unchanged
  with 49 `$defs`; `ros/` git-clean (untouched); new fixtures mint NO URI scheme outside the
  established §3/C16 base + operating-noun cap.

## DoD (real output)
- `conformance_adjudication.py` → 5/5 labels ALL PASS (C1–C5, 24/23 instances green).
- adjudication demo → RESULT: ALL PASS (deli/cove reproduce; Trust/authority/determinism intact).
- all four prior CR suites, sectors, S5, agent → ALL PASS (see work/3 verification output).
- SPEC/schema hashes + 49 `$defs` + `ros/` untouched, no new URI scheme.