# RelationalOS — Documentation package (index)

**Version:** documented against SPEC v0.22 (2026-09-01) and the verified Sprints 0–5 build
| **Package:** `docs/` | **Spec release mirror (read-only):** `/home/rlg/Documents/ai-relational-os-spec.md` (+ `.pdf`)

This is the operating, user, and system documentation for the completed RelationalOS
platform — a specification and a working S1–S5 reference build that surfaces as a
**Business Operating Layer** (BOL) with a daily **cockpit**. Every command in this package
was executed in Sprint 6 and its real output is embedded; nothing is hypothetical.

> **This package is part of the development workspace. The canonical spec is
> `SPEC.md` (v0.22). The sprint-by-sprint build chain is under `sprints/`. Everything
> here documents the real, running artifacts — a deterministic local Python build that
> costs ~$0 per run (no frontier-API spend).**

---

## What RelationalOS is, in one page

RelationalOS models relationships among **Actors** (Person, Organization, Agent, System)
as a chain of five services (**S1** Identity/Auth/AuthZ → **S2** Intent/Matching → **S3**
Orchestration/Execution → **S4** Exchange/Settlement → **S5** Trust/verification) that all
read and write **one shared relationship Graph (state)** and **one append-only,
content-addressed, signed Ledger (history)**. The ontology's spine is

    ACTOR → RELATIONSHIP → INTERACTION → EVENT → STATE  ↘ EVIDENCE → TRUST

The **moat** is a flywheel: a verified outcome is captured, its evidence anchored, scoped
Trust updated, and that Trust re-prices and re-routes the next match — so the system gets
smarter every time it is used, and no single service can copy the accumulated
evidence-and-decision history attached to its relationships (SPEC §1, §3.16).

On top of that chain, a **Business Operating Layer** (SPEC §7J/§7K) turns the substrate
into something an owner uses every morning: **Cases** (universal unit of unresolved work),
**Goals/Metrics** (what we optimize toward), **Tasks** (recommendations become assigned,
authorized work), **Dependencies** (directional workflow links with impact analysis), and
derived **Exception / Priority / Recommendation** fields. The **cockpit** (§7J.9) shows
business health, prioritized attention, and an AI recommendation that carries the authority
it requires — and it answers the **§7L ten morning questions with evidence** for the
fictional company Quoteko.

**Honest limits (spec'd, not built in Sprints 0–5):** the §7F continuous audit *service*
and audit-finding queue, the §7G BI *warehouse* (SQL/P&L/balance-sheet/cash-flow), the §7H
external gateway, the §7E frontends/IoT channel, confidential-compute anchoring, and the
§8 Phase-B backlog are all specified but **not built**. Today the runnable system is the
deterministic local chain + operating layer; where a manual implies a larger service, it
says so and gives the command that produces the working analogue **today**. See each
document's "Future deployment" notes.

---

## Who each document is for, and reading order

| Document | Reader | Purpose |
|---|---|---|
| **`QUICKSTART.md`** | Everyone | One page: stand the platform up in 3 commands and read the cockpit. **Start here.** |
| `00-README.md` | Everyone | This index. |
| **`01-system-manual.md`** | Engineer / architect | Architecture, data model, URI cap, technology truth, file→artifact map. |
| **`02-setup.md`** | Operator | Prerequisites, venv, verifying the install, full directory layout. |
| **`03-run.md`** | Operator | Run every demo + conformance runner and the daily cockpit; expected exit codes. |
| **`04-audit.md`** | Auditor / engineer | Produce the integrity audits (ledger verify, full-state round-trip, conformance C1–C5). |
| **`05-bi-reports.md`** | Owner / analyst | Produce the BI the system supports today (ledger projections, health panel, cockpit) vs the future warehouse. |
| **`06-user-manual.md`** | Owner | The §7L ten morning questions, the exception→case→task→verified-outcome→learning cycle, human-oversight discipline, do-nothing as a real option. |
| **`07-troubleshooting.md`** | Operator | Failure modes + fixes, glossary, URI-catalog summary. |

**Recommended paths:**
- **Operator (set it up and keep it running):** `QUICKSTART.md` → `02-setup.md` → `03-run.md` → `04-audit.md` → `07-troubleshooting.md`.
- **Owner (read it every morning):** `QUICKSTART.md` → `06-user-manual.md` → `05-bi-reports.md`.
- **Engineer (keep the audits and BI coming):** `QUICKSTART.md` → `01-system-manual.md` → `04-audit.md` → `05-bi-reports.md` → `07-troubleshooting.md`.

---

## Quick-start box (3 commands)

Run from the project root `/home/rlg/relational-os` with Python 3.12 available:

    # 1. Debug-build the whole S1→S5 state + the Business Operating Layer + the cockpit
    cd /home/rlg/relational-os/reference
    python3 run_s5_demo.py                       # exit 0 = ALL PASS (verified)

    # 2. Prove the schema/validator over all SIX fixture generations (uses the `conformance venv`)
    /home/rlg/relational-os/.venv/bin/python /home/rlg/relational-os/schema/run_conformance_all.py   # exit 0 = ALL PASS

    # 3. Read the cockpit report it just wrote
    nvim /home/rlg/relational-os/reports/cockpit.md

All three were executed in Sprint 6 and exited 0. Full detail in `02-setup.md` and `03-run.md`.

> **Multi-sector instances (added after Sprint 6):** the same procedures were used to
> provision **working instances for all 12 sector families** of SPEC Appendix B under
> `/home/rlg/relational-os/instances/` (each passes the conformance audits C1–C5, exit 0).
> That provisioning surfaced a genuine build defect and fixed it: the reference
> `ros/bol.py`/`ros/s4.py`/`ros/s5.py` hardcoded a construction `qk` URI segment, now
> parameterized as a `label` (default `'qk'`, byte-identical — reference re-verified).
> See `instances/README.md` and the SPEC Version/Review Log.

> **Branding component (Sprint 7 — built):** each sector instance now carries a
> **company-branding component** — the About-section / marketing / FAQ / **design
> language** set common to real company home pages (tagline, mission/vision/values, about,
> history, leadership, products, testimonials, trust, fast-facts, locations, FAQ, contact,
> careers, investors, press, ESG/philanthropy, legal, nav, cookie consent, color/typography/
> logo/tone) — carried as **additive `brand` fields on the company `org://` actor** (URI cap
> held; not a new noun) so that **every generated cockpit/BI report carries the brand.**
> Each instance also emits a **`branding.md`** marketing artifact. See `instances/README.md`.
> The build prompt that produced it: `/home/rlg/relational-os/sprints/sprint-7/PROMPT.md`.

> **Reorg note (post-Sprint-36):** the conformance runners were **re-anchored** to `Path(__file__)`
> (were CWD-bound on `../../sprint-0/artifacts`), so they are now **location-independent** — run them from
> the repo root, the artifacts dir, or anywhere. The green gate is `python3 tests/run_checks.py` (full build,
> exit 0 = ALL PASS) or `bash scripts/verify.sh` (quick daily-cockpit + conformance-all-six). See
> `03-run.md`/`07-troubleshooting.md`.

---

## Absolute paths for the key real artifacts

- Spec: `/home/rlg/relational-os/SPEC.md` (v0.22) · release mirror `/home/rlg/Documents/ai-relational-os-spec.md` (+ `.pdf`)
- Sprint-0 schema (49 `$defs`): `/home/rlg/relational-os/schema/relational-os.schema.yaml` (+ `.json`)
- EBNF grammar: `/home/rlg/relational-os/schema/relational-os-lifecycle.ebnf`
- Conformance validator: `/home/rlg/relational-os/schema/conformance.py`
- `conformance venv` (interpreter for conformance): `/home/rlg/relational-os/.venv/bin/python`
- **Canonical `ros/` package (S1–S5 + BOL substrate): `/home/rlg/relational-os/ros/`** (promoted from its origin `/home/rlg/relational-os/ros/`, byte-identical; reorg)
- Green gate / test suite: `/home/rlg/relational-os/tests/run_checks.py` · `/home/rlg/relational-os/scripts/verify.sh`
- Daily demo + cockpit producer: `/home/rlg/relational-os/reference/reference/run_s5_demo.py`
- Cockpit report: `/home/rlg/relational-os/reports/cockpit.md` (+ `cockpit.json`)
- Current state graph: `/home/rlg/relational-os/reference/graph/current-state.json`
- Ledger fixture: `/home/rlg/relational-os/reference/fixtures/ledger/ledger-quoteko.json`
- Fixtures per generation: `/home/rlg/relational-os/data/fixtures/`
- Closing hand-off: `/home/rlg/relational-os/sprints/COMPLETE.md`