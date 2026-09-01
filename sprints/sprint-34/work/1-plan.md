# SPRINT 34 — work/1-plan: reference-build green baseline FIRST (before any new artifact)

## Goal
Prove the reference build is green as currently shipped (Sprint-33 state) BEFORE building the new runner —
so any later non-regression delta is attributable only to the new runner's presence. This also records the
engine + `capacity_rerank.py` hashes, the schema hash, the 49 `$defs`, and SPEC v0.22 as the "before" state.

## Steps (run in order, exit 0 = PASS, real output captured)
1. **Hashes/invariants (before)**: sha256 of `adjudication_engine.py` == `a60f8f7…` and `capacity_rerank.py`
   == `f7c6a185…`; schema `.yaml` sha256 == `34264934…`; `$defs` == 49; SPEC v0.22.
2. **CR demo runners** (from the CR dir, plain `python3`): the 11 `run_forecast_*.py` +
   `run_cockpit_q7q8_demo.py` + `run_cockpit_s7l_demo.py` + `run_recorded_surface_demo.py` +
   `run_capacity_rerank_demo.py` + `run_two_path_demo.py` + `run_adjudication_engine_demo.py` → ALL PASS.
3. **All 5 CR conformances** (Sprint-0 venv): conformance_adjudication, conformance_dispute,
   conformance_interest, conformance_lifecycle, conformance_tradeoff → ALL PASS.
4. **Sector build + conformance**: `build_all.py` (python3) + `conformance_all.py` (Sprint-0 venv) → ALL PASS.
5. **S5 reference**: `run_s5_demo.py` + `run_s5_conformance.py` (Sprint-5 artifacts) → ALL PASS.
6. **Agent demo + conformance**: the agent sector demo + its conformance → ALL PASS.

## Pitfalls (from the runbook)
- CR runners + instance runners are CWD-sensitive: run each from the dir it computes relative paths from
  (CR runners from their own dir; build_all from `instances/`; S5 from `sprints/sprint-5/artifacts/`).
- Conformance uses the Sprint-0 venv `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python` and must
  `cd` into the dir where the validator's relative path resolves.
- Do NOT cascade inline pipes/giant one-liners (parser blocklist): run one command per step, small.