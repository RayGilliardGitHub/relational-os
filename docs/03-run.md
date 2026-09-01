# 03 — RUN (Operations: run the system, produce the daily cockpit)

**Audience:** operator. **Goal:** run every runner, know the exit codes and what the
output means, and produce/regenerate the cockpit each morning.
**Grounding:** every command below was executed in Sprint 6 with the real output embedded.

---

## 0. The two interpreters — know which to use

| Runner type | Interpreter | Why |
|---|---|---|
| **Demos / cockpit** (`run_s*_demo.py`) | plain `python3` | the `ros/` package is pure stdlib (no third-party deps) |
| **Conformance** (`run_*_conformance.py`, `run_conformance.py`) | **`conformance venv`** `.venv/bin/python` | needs `jsonschema`/`referencing`/`yaml` |

And an operational note (was a verified pitfall, **FIXED by the post-Sprint-36 reorg**): the
conformance runners were re-anchored to `Path(__file__)` (they used to resolve the Sprint-0
validator by a relative path `../../sprint-0/artifacts` against the cwd, so a bare absolute-path
invocation from the repo root failed with `ModuleNotFoundError: No module named 'conformance'`).
They are now **location-independent** — run from the repo root, the artifacts dir, or anywhere.
The `cd` below is kept for convention, not necessity.

---

## 1. The daily cockpit — one command (do this every morning)

    cd /home/rlg/relational-os/reference
    python3 run_s5_demo.py

**Exit 0 = ALL PASS.** This re-runs the *entire* S1→S5 chain on Quoteko: identity → match →
orchestrate (with the §6 human floor) → settle → Trust flywheel, plus the Business Operating
Layer, then **writes**:

- `graph/current-state.json` — current state (Graph)
- `fixtures/ledger/ledger-quoteko.json` — append-only history (Ledger)
- the repo-root `reports/cockpit.md` + `reports/cockpit.json` — the cockpit + §7L ten answers
- `fixtures/s5/*.json` etc. — regenerated per-kind fixtures (cases, goals, metrics, tasks,
  dependencies, policies, decisions, evidence, trust, …)

Real closing lines of the run (embedded):

    --- Ledger / Graph wiring ---
      ledger hash-chain + signatures: OK | entries 97
      graph current-state objects: 160
    RESULT: ALL PASS

On a clean run the real output ends:
it exits 0, open the cockpit report:

    cat  /home/rlg/relational-os/reports/cockpit.md
    # or: nvim /home/rlg/relational-os/reports/cockpit.md

Meaning of the resolution lines that matter:
- `ledger hash-chain + signatures: OK` → the append-only content-addressed chain and all
  signatures verify (this is the §3.16 integrity backbone).
- `graph current-state objects: 160` → state is a projection of that ledger.
- The `[check:roundtrip]` trio `[PASS] … 160 graph objects rebuilt from 97 events` →
  the whole Graph rebuilds from the whole Ledger (readiness for the audit in `04-audit.md`).

## 2. The demo runners (what drives the system)

The reference build (§1) is `run_s5_demo.py`. The rest of the runnable surface lives under
`instances/`: the **12 sector instances** (`cd instances && python3 build_all.py`), the
**contested-reality adjudication engine demos** (`instances/contested_reality/run_*.py`), and the
**real-LLM agent demo** (`instances/agent_demo/run_agent_demo.py`). All are `__file__`-anchored and
run from the repo root or their own dir. The single green gate that runs all of them is
`python3 tests/run_checks.py` (41 checks, exit 0 = ALL PASS), or the quick gate
`bash scripts/verify.sh`. Historical per-service `run_sN_demo.py` runners from the build-up are
kept under `sprints/` as narrative only — the system's run surface is the reference build +
`instances/`.

## 3. Conformance (the validator over every fixture generation)

The single validator (`schema/conformance.py`) is re-run over every fixture generation by
`schema/run_conformance_all.py`, with the **`.venv` interpreter** (it is `Path(__file__)`-anchored
and runs from anywhere):

| Coverage | Command | Exit / real result |
|---|---|---|
| **All six generations** (the gate) | `/home/rlg/relational-os/.venv/bin/python /home/rlg/relational-os/schema/run_conformance_all.py` | **0 · ALL PASS** · gen-0 156 / gen-1 28 / gen-2 35 / gen-3 55 / gen-4 174 / gen-5 316 instances |
| gen-0 only | `cd /home/rlg/relational-os/schema && .venv/bin/python run_conformance.py` | **0 · ALL PASS** · 156 instances |

The validator reads each generation's fixtures from `data/fixtures/gen-0..4` and the reference
build's own `reference/fixtures` (gen-5). It is the authoritative gate you verify against.

**Expected output shape** — each generation prints the same five checks, e.g. (real):

    === [gen-0] data/fixtures/gen-0 ===
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
and the cockpit reports in place. There is nothing to seed by hand; re-run `reference/run_s5_demo.py`
to recreate them. (This is determinism-by-construction: same code → same content-addressed
state.)

## 5. Day-to-day operating checklist

1. `cd /home/rlg/relational-os/reference`
2. `python3 run_s5_demo.py` → expect `RESULT: ALL PASS`, exit 0.
3. If it fails, stop and treat it as a **real regression** (see below).
4. Weekly / on any doubt: `…/.venv/bin/python schema/run_conformance_all.py` → ALL PASS.
5. Read `reports/cockpit.md`.

**If the demo or conformance FAILS:** this diff build has no network, no moving external
parts — an exit ≠ 0 means something in the workspace changed (an edited schema, `ros/` code,
or fixture, or a missing venv). Diagnostics in `07-troubleshooting.md`.