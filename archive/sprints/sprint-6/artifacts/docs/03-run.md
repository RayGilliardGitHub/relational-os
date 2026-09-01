# 03 — RUN (Operations: run the system, produce the daily cockpit)

**Audience:** operator. **Goal:** run every runner, know the exit codes and what the
output means, and produce/regenerate the cockpit each morning.
**Grounding:** every command below was executed in Sprint 6 with the real output embedded.

---

## 0. The two interpreters — know which to use

| Runner type | Interpreter | Why |
|---|---|---|
| **Demos / cockpit** (`run_s*_demo.py`) | plain `python3` | the `ros/` package is pure stdlib (no third-party deps) |
| **Conformance** (`run_*_conformance.py`, `run_conformance.py`) | **Sprint-0 venv** `.venv/bin/python` | needs `jsonschema`/`referencing`/`yaml` |

And a critical operational detail (verified): **run from inside the `sprint-N/artifacts/`
directory.** The conformance runners locate the Sprint-0 validator by a relative path
(`../../sprint-0/artifacts`) that resolves against the **process working directory**, so a
bare absolute-path invocation from the repo root fails with
`ModuleNotFoundError: No module named 'conformance'`. `cd` into the artifacts dir first.

---

## 1. The daily cockpit — one command (do this every morning)

    cd /home/rlg/relational-os/sprints/sprint-5/artifacts
    python3 run_s5_demo.py

**Exit 0 = ALL PASS.** This re-runs the *entire* S1→S5 chain on Quoteko, the Business
Operating Layer, and every Sprint-1..5 check (no regression), then **writes**:

- `graph/current-state.json` — current state (Graph)
- `fixtures/ledger/ledger-quoteko.json` — append-only history (Ledger)
- `reports/cockpit.md` and `reports/cockpit.json` — the cockpit + §7L ten answers
- `fixtures/s5/*.json` etc. — regenerated per-kind fixtures (cases, goals, metrics, tasks,
  dependencies, policies, decisions, evidence, trust, …)

Real closing lines of the run (embedded):

    --- Ledger / Graph wiring ---
      ledger hash-chain + signatures: OK | entries 97
      graph current-state objects: 160
    RESULT: ALL PASS

The full real output is captured at `sprints/sprint-6/work/captures/cockpit-run.txt`. After
it exits 0, open the cockpit report:

    cat  /home/rlg/relational-os/sprints/sprint-5/artifacts/reports/cockpit.md
    # or: nvim /home/rlg/relational-os/sprints/sprint-5/artifacts/reports/cockpit.md

Meaning of the resolution lines that matter:
- `ledger hash-chain + signatures: OK` → the append-only content-addressed chain and all
  signatures verify (this is the §3.16 integrity backbone).
- `graph current-state objects: 160` → state is a projection of that ledger.
- The `[check:roundtrip]` trio `[PASS] … 160 graph objects rebuilt from 97 events` →
  the whole Graph rebuilds from the whole Ledger (readiness for the audit in `04-audit.md`).

## 2. All demo runners (per sprint)

Each sprint's `run_*_demo.py` builds that sprint's slice and asserts it. **All are exit 0,
RESULT: ALL PASS** (verified in Sprint 6 — capture files under `sprints/sprint-6/work/captures/demo-sN.txt`).

| Sprint / focus | Command (from `sprints/sprint-N/artifacts/`) | Note |
|---|---|---|
| S5 · Business Operating Layer + cockpit | `python3 run_s5_demo.py` | also the daily cockpit (§1) |
| S4 · Settlement + multi-role/multi-org | `python3 run_s4_demo.py` | |
| S3 · Orchestration + human floor | `python3 run_s3_demo.py` | |
| S2 · Trust flywheel | `python3 run_s2_demo.py` | |
| S1 · Identity/Auth/AuthZ + matching | `python3 run_demo.py` | **note the name**: sprint-1's runner is `run_demo.py`, not `run_s1_demo.py` |

Example — S4 native runner (real exit 0):

    cd /home/rlg/relational-os/sprints/sprint-4/artifacts && python3 run_s4_demo.py
    → … RESULT: ALL PASS  (exit 0)

> Sprint-3/4 artifact dirs also carry copies of earlier runners (they accumulate); prefer
> the native `run_sN_demo.py` per row, and treat `run_s5_demo.py` as the canonical
> "run everything" entry point.

## 3. All conformance runners

The single validator (Sprint-0 `conformance.py`) is re-run over every fixture generation
by `run_sN_conformance.py`. Use the **Sprint-0 venv interpreter** and run **from the
`artifacts/` dir**.

| Coverage | Command (from `sprints/sprint-5/artifacts/`) | Exit / real result |
|---|---|---|
| **All six generations** (the gate) | `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python run_s5_conformance.py` | **0 · ALL PASS** · Sprint-0 156 / -1 28 / -2 35 / -3 55 / -4 174 / -5 316 instances |
| Sprint-0 only | `cd /home/rlg/relational-os/sprints/sprint-0/artifacts && .venv/bin/python run_conformance.py` | **0 · ALL PASS** · 156 instances |

The six-generation runner is the one you verify against. (Per-generation runners for the
other sprints also all exit 0 — verified Sprint 6; the all-six runner is authoritative.)

**Expected output shape** — each generation prints the same five checks, e.g. (real):

    === [sprint-0] sprint-0/artifacts/fixtures ===
      [PASS] C1 schema structurally valid  — 49 $defs
      [PASS] C2 all fixture instances validate + schemes + RFC3339  — 156 instances
      [PASS] C3 ledger content-addressed + signed
      [PASS] C4 round-trip preserve-unknown
      [PASS] C5 state-machine sequences legal
    …
    RESULT: ALL PASS

**Exit-code meaning:** `0` = all checks passed (ALL PASS). Any non-zero exit or any
`[FAIL]` line = a real regression or corruption — see `04-audit.md` (what each check
guards) and `07-troubleshooting.md` (what a FAIL means and how to re-run cleanly).

## 4. Regenerating `graph/current-state.json` and the fixtures

They are **outputs**, not inputs. Running the S5 demo (§1) regenerates the current-state
graph, the durable ledger fixture, the per-kind fixture files, the state-machine fixtures,
and the cockpit reports in place. There is nothing to seed by hand; re-run `run_s5_demo.py`
to recreate them. (This is determinism-by-construction: same code → same content-addressed
state.)

## 5. Day-to-day operating checklist

1. `cd /home/rlg/relational-os/sprints/sprint-5/artifacts`
2. `python3 run_s5_demo.py` → expect `RESULT: ALL PASS`, exit 0.
3. If it fails, stop and treat it as a **real regression** (see below).
4. Weekly / on any doubt: `…/.venv/bin/python run_s5_conformance.py` → ALL PASS.
5. Read `reports/cockpit.md`.

**If the demo or conformance FAILS:** this diff build has no network, no moving external
parts — an exit ≠ 0 means something in the workspace changed (an edited schema, `ros/` code,
or fixture, or a missing venv). Diagnostics in `07-troubleshooting.md`.