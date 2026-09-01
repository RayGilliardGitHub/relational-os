# Northglen Bank — a RelationalOS instance for the financial sector (dogfood trial)

This is a **working, validated instance of the RelationalOS platform for a company in the
financial-sector family**, stood up by following the Sprint-6 documentation package
(`sprints/sprint-6/artifacts/docs/`) — the manuals' own practice was used to build it. It
is real: constructed with the unmodified `ros/` package, its fixtures pass the Sprint-0
conformance audits (C1–C5, exit 0), and it produces its own cockpit with the §7L ten morning
questions answered with evidence.

## The company (fictional, financial sector)
| Actor | URI | Role in the scene |
|---|---|---|
| **Northglen Bank** | `org://fin/northglen` | a regional commercial bank (FOR_PROFIT) — the owner/operator |
| Zephyr Manufacturing | `org://fin/zephyr` | the corporate client (borrower) taking a working-capital facility |
| Adamvale | `org://fin/adamvale` | correspondent counterparty — **reliable, settles on time** |
| Kaplen | `org://fin/kaplen` | correspondent counterparty — **laggard, missed its committed settlement deadline** |
| Treasurer | `person://fin/treasurer` | the human approver (§6 floor) |
| Ops agent | `agent://fin/treasury-ops` | delegated, capability-bound worker |

Outcome class: **"committed funding tranche settled by its committed deadline."** The scene
is the financial analogue of the reference build's on-time-delivery operating loop: an
on-time-settlement exception, a case, a re-allocation task (#8) to the verified counterparty
and a gate on the laggard, a verified outcome (#10), and a learning-driven policy change.

## What it exercises (S1→S5 + BOL, all real PASS)
- **S1** role is relationship-scoped and authorization is capability-based and delegation-bound;
  revoking the delegation voids the capability immediately (§7B).
- **Ledger/Graph** round-trip: the whole Graph rebuilds from the whole Ledger (§3.16);
  83 graph objects from 55 signed events.
- **S2/S5 flywheel**: a verified on-time good settlement (adamvale) vs two late settlements
  (kaplen) re-ranks the next funding match to adamvale — scoped Trust, never a global score.
- **§6 human floor**: releasing a committed funding tranche is irreversible/unknowable-cost;
  the ledger order is provably `escalate < human < release` (indices 31 < 32 < 33) — the
  action ran only after the treasurer's signed decision.
- **S4 settlement**: obligation + receipt + reconciliation ride ONE signed EXCHANGE event.
- **BOL**: case lifecycle OPEN→TRIAGE→ASSIGNED→IN_PROGRESS→BLOCKED→RESOLVED→CLOSED,
  exception heartbeat (CRITICAL, root SUPPORTED), #8 assigned authorized task, verified
  outcome, Learning decision + policy v3.
- **Cockpit + §7L**: business health (3 ledger-projected metrics), priority-ordered
  attention, AI recommendation incl. do-nothing, and the ten questions answered with evidence.

## How to run it (the manuals' own procedures applied)
    cd /home/rlg/relational-os/instances/financial
    python3 run_fin.py                          # builds S1->S5 + BOL + cockpit; exit 0 = ALL PASS
    /home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python run_fin_conformance.py  # C1-C5, exit 0
    python3 bi_snapshot.py                      # BI projections from the emitted ledger

Verified outputs (embedded in this run):
- `run_fin.py` → **RESULT: ALL PASS**, exit 0. Ledger hash-chain OK (55 entries), graph
  83 objects, round-trip PASS, §6 floor 31<32<33, case lifecycle complete, cockpit written.
- `run_fin_conformance.py` → **NORTHGLEN CONFORMANCE: ALL PASS**, exit 0; C1 (49 `$defs`),
  C2 (70 instances, schemes + RFC 3339), C3 (ledger content-addressed + signed), C4
  (round-trip preserve-unknown), C5 (state machines).
- `bi_snapshot.py` → on_time 2/4 = 0.500, settled value USD 5,700,000, adamvale Trust 0.79,
  kaplen Trust 0.14; 55 ledger entries all signed, 83 graph objects.

## Produced artifacts (under `instances/financial/artifacts/`)
- `graph/current-state.json` — current state (Graph = state)
- `fixtures/ledger/ledger-northglen.json` — append-only signed history (Ledger = history)
- `fixtures/s5/*.json` — per-kind fixture groups (cases, goals, metrics, tasks, policies, …)
- `fixtures/statemachines/` — relationship + case state-machine fixtures (C5)
- `reports/cockpit.md` (+ `.json`) — the financial company's cockpit + §7L answers

## What the dogfood trial found (gaps the manuals did not spell out)
1. **The manuals' procedures transfer cleanly** to a brand-new company: the venv-interpreter
   rule, run-from-the-artifacts-dir rule, the conformance gate as the audit, and the BI
   snapshot read all worked on a non-Quoteko instance with zero changes to the schema or
   `ros/` code.
2. **The reference S1/S2/S3 services are scene-hardwired to Quoteko** (e.g. `offer://qk/o-*`,
   `relationship://qk/cust-cxn`, `org://quoteko` inside `S5.make_expectation`). A genuinely
   new sector instance is therefore driven through the **operating layer** (`BolService`) plus
   the **generic S4/S5** (settlement + Trust), which the manuals already describe as the
   reusable surface. The S1 role/authz, S2 matching, and §6 floor are still exercised — via
   their generic methods.
3. **Reused S4/S5 emit `qk` in some URI labels** (`asset://money/qk-escrow-…`,
   `trust://qk/t-…`, `obligation://qk/…`, `event://qk/s4-exchange-…`) even for a Northglen
   instance. This is a harmless build artifact — conformance and round-tripping govern by
   scheme, so every object still validates. A production instance would parameterize the
   org segment in the service classes.
4. **cwd/relative-path sensitivity is real and re-confirmed**: the instance conformance
   runner must resolve the Sprint-0 validator by a correct parents index (here `parents[1]`)
   — a reminder that these reference runners are not robust to being relocated.

Boundaries held: **no change** to `SPEC.md` (still v0.22), no change to the frozen ontology
or the `ros/` code — this instance is pure new data + a new scene builder over the existing
platform.

## Cross-references
- The manuals used: `sprints/sprint-6/artifacts/docs/02-setup.md`, `03-run.md`,
  `04-audit.md`, `05-bi-reports.md`, `06-user-manual.md`.
- Platform closing hand-off: `sprints/COMPLETE.md`; spec `SPEC.md` (v0.22).