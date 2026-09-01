# SPRINT 6 — SUMMARY (Documentation package)

**Project:** RelationalOS | **Spec:** **v0.22 (unchanged — docs sprint, per protocol)**
**Date:** 2026-09-01 | **Result:** a complete, **verified** documentation package for the
finished S1→S5 system: operations manual (setup + run), system manual, audit manual, BI
manual, owner's manual, a quick-start card, and a troubleshooting/glossary appendix. Every
documented command was executed in this sprint and its **real output embedded**.

## What was produced
`/home/rlg/relational-os/sprints/sprint-6/artifacts/docs/`
- `00-README.md` — index + "what the system is" in one page + reading order + quick-start box.
- `01-system-manual.md` — architecture & data model for an engineer (substrate §3.16, S1–S5
  chain, BOL, URI cap, schema/conformance/EBNF, technology truth, file→artifact map).
- `02-setup.md` — prerequisites (Python 3.12, Sprint-0 venv + deps), create/repair the venv,
  verify the install (run conformance), full directory layout.
- `03-run.md` — run every demo runner (`run_s5_demo.py` = the daily cockpit; per-sprint
  `run_sN_demo.py`, Sprint-1's `run_demo.py`) + every conformance runner (Sprint-0 venv
  interpreter), expected exit codes, regenerate state/fixtures/reports.
- `04-audit.md` — produce the integrity audits (Ledger hash-chain + signatures, full-state
  round-trip, conformance C1–C5) with real PASS output + an explicit §7F.1 "today vs future" map.
- `05-bi-reports.md` — BI today (the §7G.8/§7G.6 projections + health panel + cockpit) with real
  output, and §7G.1–.7 map (P&L/BS/cash-flow = future warehouse).
- `06-user-manual.md` — the owner's manual: the §7L ten questions, the
  exception→case→task→verified-outcome→learning cycle, authority-carrying recommendation,
  do-nothing as a real option, human-oversight discipline (§6 floor).
- `07-troubleshooting.md` — failure modes + fixes, glossary, URI-catalog summary.
- `QUICKSTART.md` — one-page "stand it up in 3 commands and read the cockpit" card.

Plus `plan.md`, `work/1-vocab.md`, and `notes/findings.md` (F6-1…F6-4).

## Verified commands & real outputs (all executed, all exit 0)
- **Daily cockpit + whole build:** `cd …/sprint-5/artifacts && python3 run_s5_demo.py` →
  `RESULT: ALL PASS`, exit 0; writes `graph/current-state.json`,
  `fixtures/ledger/ledger-quoteko.json`, `reports/cockpit.md` (+`.json`). Ledger wiring:
  `ledger hash-chain + signatures: OK | entries 97`, `graph current-state objects: 160`;
  round-trip **160 graph objects rebuilt from 97 events**.
- **Conformance (all six generations, ONE validator):** `.venv/bin/python run_s5_conformance.py`
  → `RESULT: ALL PASS`, exit 0; Sprint-0 **156** / -1 **28** / -2 **35** / -3 **55** / -4 **174** /
  -5 **316** instances; checks C1 (schema 49 `$defs`) · C2 (instances+scheme+RFC3339) · C3
  (ledger chain+signed) · C4 (round-trip preserve-unknown) · C5 (state machines).
- **Per-sprint demos** (S1 `run_demo.py`, S2/3/4 `run_sN_demo.py`, S5 `run_s5_demo.py`): all
  `RESULT: ALL PASS`, exit 0. **Per-generation conformance runners** (s0..s5): all exit 0.
- **BI snapshot** (`python3 …/bi_snapshot.py` over the emitted fixtures):
  `project_on_time → 6/7 = 0.857`, `project_settled_value → USD 24850.0`,
  `project_trust(solarworks,cust-cxn) → 1.0`; ledger 97 events all signed; 160 graph objects
  all round-trip covered.
- **Venv/deps:** `python3` and venv are both Python 3.12.3; deps import "deps OK".
All capture files: `sprints/sprint-6/work/captures/`.

## Key operational corrections surfaced (F6-1…F6-3)
- **Cwd-sensitive runners:** conformance runners resolve the Sprint-0 validator relative to the
  **working directory**; run them from inside `sprint-5/artifacts/`. `COMPLETE.md`'s "cd does
  not matter" is inaccurate here — corrected in the docs.
- **Sprint-1 demo name** is `run_demo.py` (not `run_s1_demo.py`).
- **Sprint-0 venv ships without `bin/pip`** — works anyway; deps present.

## Decided future-deployment boundaries (unchanged from spec)
Today's runnable system is the deterministic local chain + BOL. **Future (spec'd, not built):**
§7F continuous audit service + `audit_finding://` remediation queue (today: conformance +
`Ledger.verify()` + round-trip), §7G BI warehouse (today: ledger projections + cockpit),
§7H external gateway, §7E frontends/IoT, confidential-compute anchoring, real graph/ledger
store + redundancy, real S2/S4 connectors, AI root-cause/forecast over real data, and the §8
Phase-B backlog. The integrity audit today = conformance C1–C5 + `Ledger.verify()` + full-state
round-trip; BI today = the §7G.8 projections + the cockpit health/attention/§7L panels.

## SPEC correctness
- `SPEC.md` held at **v0.22**; schema + `ros/` code + fixtures **untouched**; frozen ontology
  and URI cap respected (no new nouns). No Version/Review‑Log change (docs-only corrections were
  about build-artifact operation, not the spec).

## Hand-off
The completed S1→S5 project now closes with a user-facing manual. Start with
`/home/rlg/relational-os/sprints/sprint-6/artifacts/docs/QUICKSTART.md` and the index
`/home/rlg/relational-os/sprints/sprint-6/artifacts/docs/00-README.md`. No next-sprint prompt
is required — this completes the project's story.