# 05 — BI REPORTS (produce the business intelligence)

**Audience:** owner / analyst / engineer. **Goal:** what "BI" means in this system, the
commands that produce it **today** (all real/verified), and an honest map of the §7G report
catalog to built-vs-future.
**Grounding:** SPEC §7G (BI layer), §7L (ten questions), the ledger projections in
`ros/bol.py`, and the produced cockpit. Every command below was executed in Sprint 6.

---

## 1. What "BI" means here

SPEC §7G defines BI as a reporting service that turns the Relationship Graph + Ledger into
standard business intelligence. Its core discipline (§7G.8, §7C): the **ledger is the
audit-grade source of truth**, and BI reads **queryable projections** over ledger events —
never hand-set numbers. That is exactly what the verified build does: business health is
**derived from history**, not put in by hand.

Today the runnable BI is the **deterministic ledger projection layer** in `ros/bol.py`
plus the cockpit's health/attention panels. The full §7G.1–.7 catalog (P&L, balance sheet,
cash-flow, and the rest) needs the production BI warehouse (SQL transforms + Metabase/
Superset) — that is **future deployment**, mapped in §4.

## 2. The projection functions (the BI core) — `ros/bol.py`

| Function | What it computes | Source |
|---|---|---|
| `project_on_time(substrate)` | `(on_time, total)` share of completion `OUTCOME` ledger events carrying an `on_time` flag | ledger |
| `project_settled_value(substrate)` | sum of settled `EXCHANGE` event prices | ledger |
| `project_trust(substrate, target, context)` | best scoped Trust for `(target, context)` on the graph (§3.14 keying) | graph |

These are what the business-health panel is built from. **To see them on the live emitted
data** (the actual ledger/graph the demo produced), run this standalone reader from the
project root (plain `python3`):

    cd /home/rlg/relational-os
    python3 archive/sprints/sprint-6/work/captures/bi_snapshot.py

Real output (embedded; reads `reference/fixtures/ledger/ledger-quoteko.json` +
`graph/current-state.json`):

    project_on_time      -> 6/7 completions on time = 0.857
    project_settled_value -> USD 24850.0
    project_trust(solarworks, cust-cxn) -> 1.0
    ledger entries = 97 | all content-addressed+signed = True
    graph objects  = 160
    round-trip: 160 graph objects covered by state_update (OK, none missing)

(recomputed from the same fixtures the cockpit reports against — a reproducible BI read).

## 3. The daily BI: the cockpit report

The **one command that produces today's BI** is the daily cockpit (`03-run.md §1`):

    cd /home/rlg/relational-os/reference
    python3 run_s5_demo.py          # exit 0 = ALL PASS; writes reports/cockpit.md + .json

> **Branding (Sprint 7):** in the **sector instances** the BI/cockpit is branded — the
> header identifies **who the report is for** (`Company — tagline`), a `## Brand` appendix
> rides each report, and `cockpit.json` carries the brand. The Financial v1
> `bi_snapshot.py` prints the label line `Northglen Bank — Funding that lands on the date.`
> See `instances/README.md`.

### 3.1 Business-health table (real content of `reports/cockpit.md`)

    # Quoteko — Business Operating Layer cockpit
    generated 2026-08-31T23:38:16Z  |  ledger events 97  graph objects 160

    ## Business health (ledger-projected metrics)
    | metric | unit | target | actual | variance | status |
    |---|---|---|---|---|---|
    | On-time delivery rate (`metric://qk/m-on-time`) | fraction | 0.95 | 0.857 | -0.093 | CRITICAL |
    | Customer-trust score (`metric://qk/m-customer-trust`) | score | 0.9 | 1.0 | 0.1 | OK |
    | Settled value (`metric://qk/m-settled-value`) | USD | 25000.0 | 24850.0 | -150.0 | WARN |

Interpreting: target/actual/variance come from the **ledger projections** (on-time = 6/7,
settled value = sum of EXCHANGE prices, trust = best scoped value). Status is a relative
variance rule (≥0 OK, ≥−5% WARN, otherwise CRITICAL).

### 3.2 Prioritized attention (real)

    ## Prioritized attention — 2 things requiring attention today
    - **0.69** re-balance provider allocation (`task://qk/t-provider-rebalance`)
    - **0.58** rallied follow-on delivery (solarworks) (`task://qk/t-followup-routed`)

Priorities are the deterministic §7J.5 score `f(impact, urgency, confidence, irreversibility,
relationship-importance, cost-of-delay)`.

### 3.3 The §7L ten answers (real, abridged)

The cockpit embeds all ten morning questions answered **with evidence**; a representative
answer (full text in `reports/cockpit.md`, also embedded in `06-user-manual.md §2`):

    1. WHAT HAPPENED?  On-time contracted completions 6/7 (0.857); solarworks settled on
       time (ev evidence://qk/job-routed-solarworks), norcrete late; settled value 24850.0.
       [ledger evidence]
    8. WHAT SHOULD WE DO?  -> assigned, authorized Task task://qk/t-provider-rebalance under
       authority://qk/for-operations.  [recommendation]
    10. DID IT WORK, AND WHAT DID WE LEARN?  Yes — rallied delivery verified on time (forward
       on-time 1.0); Learning entry decision://qk/s5-learning-on-time; provider-allocation
       policy v3 updated (change-future-policy).  [verified outcome + organisational learning]

## 4. §7G report catalog → built today vs future

| §7G report | Status today | Where / future |
|---|---|---|
| Business-health panel (on-time, trust, settled value) | ✅ **built** | `reports/cockpit.md`; `ros/bol.py` projections |
| Prioritized attention / AI recommendation incl. do-nothing | ✅ **built** | cockpit (answers §7J.9, §7L #3/#7/#8) |
| RelationalOS-native operational metrics (on-time, trust distribution per relationship, exceptions) | ✅ **built (minor subset)** | the three projections cover delivered-on-time, scoped trust, settled value |
| **§7G.1 P&L / balance sheet / cash-flow** (and budget-vs-actual, segmented, aging) | 🔮 **future** | needs the BI warehouse (GL/ledger events → SQL/dbt → Metabase/Superset), per §7G.8/§G.15 |
| §7G.2–.7 (customer/demand, ops, workforce, supplier, compliance; full trust/evidence/dispute/payroll catalogs) | 🔮 **future** | production warehouse + the §7F audit feed (§7G.6 audit-health) |
| Warehouse separation (BI reads projections, not the live graph under load) | 🔮 **future** | §7C/§7G.8; today fence is not needed at reference size |

**Bottom line:** today's BI **is** the cockpit — health table, prioritized attention, AI
recommendation, and ten evidence-made answers, all derived from ledger projections. The
standard financial statements and the breadth catalog (§7G.1–.7) are spec'd but **future
deployment**; deploy the warehouse (ClickHouse/Postgres + dbt + Metabase/Superset, §G.15)
when the real store replaces the reference build. Until then, `05-bi-reports.md` + the
cockpit are the working BI.