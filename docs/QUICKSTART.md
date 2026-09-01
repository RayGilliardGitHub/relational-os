# RelationalOS — QUICKSTART (stand it up + read the cockpit in 3 commands)

**Prereq:** Python 3.12 with the `conformance venv` present and its deps (`jsonschema`,
`referencing`, `yaml`/`pyyaml`) installed. See `02-setup.md` if the venv is missing.

Run all three from the terminal. Except where noted, **run from inside the
repo root.**

## 1 · Build the full system (S1→S5 + Business Operating Layer + cockpit)

    cd /home/rlg/relational-os/reference
    python3 run_s5_demo.py

**Verified output (real, Sprint 6):** exits `0` and prints `RESULT: ALL PASS`. It
re-runs every prior Sprint-1..4 check (no regression), finishes the operating-layer
personas (Case lifecycle, exception heartbeat, Learning, goals/metrics, priority,
dependencies, health panel, cockpit), and writes:

    graph/current-state.json                  current state (Graph = state)
    fixtures/ledger/ledger-quoteko.json       append-only history (Ledger = history)
    reports/cockpit.md  (+ cockpit.json)      the daily cockpit + §7L ten answers

Final wiring lines it prints:

    ledger hash-chain + signatures: OK | entries 97
    graph current-state objects: 160
    RESULT: ALL PASS

## 2 · Prove the schema/validator over all SIX fixture generations

    cd /home/rlg/relational-os/reference
    /home/rlg/relational-os/.venv/bin/python schema/run_conformance_all.py

**Verified output:** exits `0` and prints `RESULT: ALL PASS`, running the single
conformance validator over all six fixture generations (gen-0 **156** / -1 **28** / -2
**35** / -3 **55** / -4 **174** / -5 **316** instances), checks **C1** schema · **C2**
instances+scheme+RFC3339 · **C3** ledger content-addressed+signed · **C4** round-trip ·
**C5** state machines.

> Use the **`.venv` interpreter** (`.venv/bin/python`) for any conformance run —
> it has `jsonschema`/`referencing`/`yaml`. The conformance runners are `Path(__file__)`
> **-anchored (location-independent since the reorg), so run them from the repo root or anywhere**.

## 3 · Read the cockpit report

    nvim /home/rlg/relational-os/reports/cockpit.md
    # or: cat  /home/rlg/relational-os/reports/cockpit.md

The cockpit shows: **Business health** (3 ledger-projected metrics: on-time CRITICAL,
customer-trust OK, settled-value WARN) · **Prioritized attention** (2 tasks) · the
**AI recommendation (#8)** with its required authority and an explicit **do-nothing**
option · the **verified outcome (#10) + Learning**, and the **§7L ten morning questions
answered with evidence** (see `06-user-manual.md` for how to read them).

---

**That's it.** Three commands — build, prove, read — all verified to exit 0.

- Full operational detail: `02-setup.md` (installing) and `03-run.md` (all runners).
- What the audits are and how to produce them: `04-audit.md`.
- What BI exists today vs the future warehouse: `05-bi-reports.md`.
- Owner's guide to the ten questions: `06-user-manual.md`.
- If a step fails: `07-troubleshooting.md`.