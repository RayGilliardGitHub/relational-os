# Survey 2 — Jurisdiction & Tax-Filing Set (Federal / State / Local)
**Sprint 0 / §7H | RelationalOS | 2026-09-01**
**DoD:** a verified filing-calendar seed per target jurisdiction + a vendor comparison.
**Status per §8:** deliverable #2 — **DONE (gating, written report).**

## Scope
Target jurisdiction seed: **US federal (IRS) + New Mexico + Albuquerque (NM state-level
GRT — NM has no separate city income tax)**. Extensible to other states/entity forms;
this is the *seed* calendar, not an exhaustive registry (per §7H.7, jurisdiction
calibration is the providers'/Phase-B job).

## Federal (IRS) — e-file mandates & calendar
Per §7H.3, filing is by entity form. Key forms, due dates, and e-file status:

| Form | What | Due | E-file |
|---|---|---|---|
| 941 (quarterly) | Employer's Quarterly Federal Tax Return | Apr 30, Jul 31, Oct 31, Jan 31 | Electronic for 250+ forms; strongly encouraged |
| 940 | Federal Unemployment (FUTA) | Jan 31 | e-file accepted |
| 720 | Quarterly Federal Excise | Apr 30 / Jul 31 / Oct 31 / Jan 31 | e-file accepted |
| 1120 | C-corp income | 15th of 4th month (cal-year ≈ Apr 15) | MeF (e-file) for most |
| 1120-S | S-corp | Mar 15 | MeF |
| 1065 | Partnership | Mar 15 | MeF |
| 990 | Nonprofit | 15th of 5th month | e-file threshold |
| 1040 / 1040-ES | Individual / estimated | Apr 15 (+ quarterly est) | MeF |
| W-2/W-3 | Wages | Jan 31 | MeF (W-2) |
| 1099-NEC | Nonemployee income | Jan 31 | MeF |
| 1095-C / 1094-C | ACA self-insured | Feb 28 (paper) / Mar 31 (e-file) | **mandatory e-file** |
| 5498/5498-SA | Retirement/HSA | May 31 | e-file |
| FBAR (FinCEN) | Foreign accounts | Apr 15 (auto to Oct 15) | BSA e-filing |

**E-file mandate (normative for RelationalOS):** IRS requires e-filing above volume
thresholds (250+ information returns) and for most business returns via Modernized
e-File (MeF); ACA forms 1095-C/1094-C and FATCA carry their own mandates. Receipts are
stored as `filing://` Evidence (§7H.6) to prove "we filed X on date Y."

## State — New Mexico
| Item | Detail | Due |
|---|---|---|
| **CIT-1** Corporate Income + Franchise Return | $50 annual franchise tax + income (no separate business-privilege beyond GRT) | **15th day of 3rd month after tax-year close** (calendar-year ≈ Apr 15) |
| **PIT-1** Individual return | same calendar | Apr 15 |
| **Gross Receipts Tax (GRT)** | the state's broad revenue/business tax; Albuquerque levies local-option GRT on top | monthly/quarterly per filer category (typically 25th of following month) |
| **Sec. of State Annual Report** | corporations/LLCs | within 30 days of incorporation/registration **anniversary** |

*Source: NM Taxation & Revenue Dept. — "Filing Requirements" (CIT-1, 15th of 3rd month
after close), Corporate Overview (franchise = $50, GRT). Albuquerque gross-receipts is a
state-administered local-option surcharge — no separate ABQ income tax.*

## Filing-calendar seed (jurisdiction × form × deadline → §7H.6 compliance scheduler)
A seed row-set the RelationalOS scheduler (Prefect/Airflow, App-G.14) encodes:
- **Federal:** 941 (quarterly-end, 4×/yr) · 940 & W-2 & 1099-NEC (Jan 31) · ACA 1095-C/1094-C
  (Mar 31 e-file) · entity income returns (Mar 15 / Apr 15 / May 15) · 720 quarterly ·
  FBAR (Apr 15).
- **NM:** CIT-1/PIT-1 (Apr 15, calendar-year) · GRT (monthly, ~25th) · Sec. of State annual
  report (anniversary +30 days).
- Each row carries an **escalation**: missed filing becomes an `audit_finding://`
  (§7F.2) + alert to the human-loop (§7D-C).

## Vendor comparison (tax automation / e-file — Phase-B procurement, not Sprint-0)
| Vendor | Focus | Model | Notes |
|---|---|---|---|
| **Avalara (AvaTax)** | Indirect/sales tax calc + returns e-file | subscription + per-transaction | Strong nexus + ERP integration (SAP/Oracle/Netsuite); not payroll |
| **Vertex** | Indirect tax calc, enterprise | enterprise subscription | Deep ERP suite; larger mid-market+ |
| **Sovos** | Indirect tax + **compliance as managed service** | managed monthly filing w/ dedicated tax pro | Best for hands-off managed filing; done-for-you returns |
| **TaxJar** | Sales tax for e-commerce/SMB | SMB subscription | Entry/low-cost; limited managed service |
| **Payroll e-file (ADP, Paychex, Gusto)** | W-2/W-3, 941/940, SUTA, ACA | subscription | The platform integrates payroll filers, does not re-implement (§7H.2) |
| **IRS MeF / e-file software** (Tax1099, TaxBandits, Drake) | Information/federal returns | per-return/subscription | IRS-authorized; needed for 1099/W-2/1120-series e-file |

**Cost reality (approx., 2026-09-01):** SMB indirect-tax SaaS starts ~$17–50/mo (TaxJar/
Avalara entry); enterprise (Vertex/Sovos/ONSERE) is materially higher. Payroll suites
$30–100+/mo + per-payrun. **For the Sprint-0 build, these are connectors (§7H: "providers
and formats are connectors, not owned machinery"); the platform's compliance calendar and
`filing://` Evidence model are what Sprint-0 must prove — not a tax engine (§7H.7).**

## Findings for spec (feed notes/findings.md)
- §7H.3's three-tier structure is confirmed by the seed (federal calendar + NM CIT-1/GRT
  + no ABQ city income tax). No new filing classes required.
- **SEC EDGAR is also a free regulatory signal feed** (Survey 1, rank 2) feeding §7I's
  regulatory-signal typing and §7H.4 securities interfaces — a cross-survey confirmation
  that the resilient ingest base is GDELT + EDGAR + RSS.
- **Spec action:** none structural; the §7H.6 compliance-calendar wording already matches.
  Add a cross-note that the seeded calendar (federal/NM/ABQ) is the Sprint-0 fixture basis.

## References
1. IRS — *Forms & instructions* (941/940/720/1095/5498 etc.), irs.gov/forms-instructions
2. IRS MeF / e-file — irs.gov; e-file volumes/authorized providers (Tax1099, web.tax1099.com)
3. NM Taxation & Revenue — *Corporate Income & Franchise Tax Filing Requirements*, tax.newmexico.gov;
   PIT-1/GRT pages
4. Filing-deadline roundups — signalshq.io "New Mexico Tax Deadlines 2026"; accountingketchup.com
5. Tax platform comparisons — taxcloud.com; ai-pedias.com "Avalara vs Vertex vs Sovos"

---
*Gating survey complete. Next: Survey 3 (BI report-catalog validation).*