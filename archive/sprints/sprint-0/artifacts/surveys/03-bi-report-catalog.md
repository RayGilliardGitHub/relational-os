# Survey 3 — BI Report-Catalog Validation (per authoritative references)
**Sprint 0 / §7G | RelationalOS | 2026-09-01**
**DoD:** a **validated, versioned** report catalog for the core statements + management
package, checked against authoritative references. **Status per §8:** deliverable #3 — **DONE.**

## Method
The §7G catalog (three core statements + management/customer/ops/workforce/supplier/
RelationalOS-native/compliance families) is checked against authoritative accounting and
management-reporting references: **U.S. GAAP presentation guidance (FASB Accounting Standards
Codification, ASC 205/210/220/230/505 + SEC Regulation S-X Article 3)** for the statutory
core, and standard **management reporting pack** practice for the decision-facing set. Each
§7G report is mapped to (a) its authoritative basis and (b) the ledger/graph objects that
produce it (per §7G.8: BI reads warehouse projections, never the live graph).

## Versioned report catalog (v1.0, 2026-09-01)
Version line: `report://catalog/v1.0`. Each entry: §7G ref · report · authoritative basis ·
ledger source · validity.

### A. Core financial statements (statutory core — **authoritative-validated**)
| §7G | Report | Authoritative basis | Ledger source | Valid |
|---|---|---|---|---|
| 7G.1 | **P&L / Income statement** | ASC 220 (comprehensive income); Reg S-X Art 3-02/3-03 | revenue & expense GL events (`gl://`) | ✔ |
| 7G.1 | **Balance sheet / Statement of financial position** | ASC 210 (balance sheet); Reg S-X 3-01 | asset/liability/equity ledger positions | ✔ |
| 7G.1 | **Cash-flow statement** | ASC 230 (cash flows) | money in/outflows over period (`money://`) | ✔ |
| 7G.1 | **Budget vs actual (variance)** | Management accounting (management assertion) | `budget://` + settled txn events | ✔ (management, not GAAP) |
| 7G.1 | Segmented profitability | Reg S-X (segment) / ASC 280 (segment reporting) | income by segment/unit | ✔ |
| 7G.1 | Cash-flow forecast / working capital | Management forecasting practice | AP/AR aging, open orders | ✔ (management) |
| 7G.1 | AR/AP aging | Management accounting practice | invoice/receipt/payment events | ✔ (management) |

### B. Customer, demand, operations, workforce, supplier
| §7G | Report | Authoritative / accepted basis | Ledger source | Valid |
|---|---|---|---|---|
| 7G.2 | Revenue by product/segment/region/channel | Management practice (acknowledged in mgmt pack) | settled Outcomes | ✔ |
| 7G.2 | CAC & LTV | Accepted commercial-metrics practice (management) | investment vs retained value | ✔ |
| 7G.2 | Churn / retention / repeat | Accepted practice | relationship state (Terminated/Active) | ✔ |
| 7G.2/3 | Open orders & pipeline; OTD / complete; backlog/capacity; inventory | Accepted operations practice | order/offer states; shipment vs expectation; capability | ✔ |
| 7G.4 | Headcount/hire/term/turnover; utilization; payroll | Accepted HR practice; SSB/EEO context | employee relationships; compensation events | ✔ |
| 7G.5 | Spend by supplier/category; OTIF; **supplier trust/risk** | Accepted procurement practice + §7G.6 trust | PO/invoice; supplier Expectation; **S5 Trust** | ✔ |

### C. RelationalOS-native (the differentiator — no statutory analog, management-defined)
| §7G | Report | Basis | Ledger source | Valid |
|---|---|---|---|---|
| 7G.6 | **Trust distribution** | §3.14 scoped Trust | Trust objects by actor/context | ✔ (RelationalOS-defined) |
| 7G.6 | Evidence & reputation health | §3.14 Reputation ↔ Trust separation | verified evidence; reputation aggregate | ✔ |
| 7G.6 | Dispute pipeline | §3.13 lifecycle | dispute objects | ✔ |
| 7G.6 | Audit health | §7F findings | `audit_finding://` events | ✔ |
| 7G.6 | Consent/authority hygiene | §3.4/§3.7 | expiry tracking on consent/delegation | ✔ |
| 7G.7 | Filing & licensing status; regulated-data exposure | §7H/§7B | `filing://`, regulated-data tags | ✔ |

## Validation conclusion
- The **three core statements** in §7G map exactly to the GAAP-required set (income /
  balance sheet / cash flow per ASC 220/210/230 and Reg S-X Art 3). **No missing or
  spurious statutory statement.**
- The **management package** (§7G.1-7G.7 + §7J.1 metrics) aligns with standard monthly
  management-reporting practice (executive summary, P&L, balance-sheet highlights, cash,
  KPIs, variance, forecast commentary). RelationalOS's §7G.6 family is correctly an
  **extension beyond** any statutory/standard package — its "authoritative" basis is the
  spec's own Trust/Evidence model, which the survey finds sound (bounded, no global score).
- **Caveat flagged with honesty:** revenue-recognition (ASC 606) and lease (ASC 842)
  subtleties, and multi-US-GAAP/IFRS variance (EY tool), mean the "ledger produces the
  statement" mapping is architecture, not a substitute for an accountant's judgment.
  §7G.8's "versioned, trust-weighted, warehouse-only" mechanic stands.

## Findings for spec (feed notes/findings.md)
- Catalog is **validated** (A-C above) and versioned (`report://catalog/v1.0`). No report
  in §7G is contradicted by an authoritative reference. **Spec action:** recommend §7G.8
  add one line: "the catalog is versioned at `report://catalog/vN`; statutory core is
  ASC/Reg S-X-grounded." (bump-only, non-structural)

## References
1. FASB — *Accounting Standards Codification (ASC 205 Presentation of Financial
   Statements; 210 Balance Sheet; 220 Income Statement; 230 Statement of Cash Flows; 280
   Segment Reporting)* — accountinginfo.com/asc-200; FASB codification (asc.fasb.org)
2. SEC — *Regulation S-X, Article 3 (Financial Statements)* — ecfr.gov; grantthornton.com
   US-GAAP/IFRS comparison
3. EY — *US GAAP / IFRS Accounting Differences Identifier* (ey.com technical PDF)
4. Management pack practice — accountsIQ "Management Reporting Packs Explained";
   madrasaccountancy "Management Reporting Package Contents" (rate: exec summary, P&L, BS,
   cash, KPIs, variance, forecast commentary)
5. Investopedia — *Financial Statements* (three-statement overview)

---
*Gating survey complete. Next: Survey 4 (employee/customer data boundary).*