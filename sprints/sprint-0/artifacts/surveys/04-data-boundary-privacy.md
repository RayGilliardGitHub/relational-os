# Survey 4 — Employee/Customer Data Boundary: What Sentiment Data Is Ingestible
**Sprint 0 / §7I + §7B | RelationalOS | 2026-09-01**
**DoD:** an intake allow-list + a privacy-policy skeleton, per jurisdiction, under
Consent/Disclosure (§3.19, §7B). **Status per §8:** deliverable #4 — **DONE.**

## The question
§7I ingests sentiment/trend on three populations — business (market), customers
(reputation), employees (employee-reputation, e.g. Glassdoor). The load-bearing boundary:
these signals are **Claims-with-provenance; derived actions never auto-execute** (§7I.4).
This survey fixes what may be legally & ethically **ingested** and *whose* data touches
the system. `CONCLUSION:` the boundary hinges on jurisdiction + special-category + the
identity-vs-context rule (§3.2) and the Disclosure gate (§3.19).

## Jurisdiction reality (as-of 2026-09-01)
- **GDPR (EU)**: Art 6(1) legal basis (legitimate interest OK for some biz/aggregate
  monitoring, with balancing; **consent is not a safe default for employees**, per EDPB —
  imbalance of power); **Art 9(1) bans special categories** (race, politics, religion,
  biometric/health, trade-union, sex life/orientation) unless Art 9(2) exception; **Art 88**
  lets member-state law condition employment processing. Employee monitoring needs
  transparency + DPIA + documented basis — **not** blanket scraping.
- **CCPA/CPRA (California)**: the old employee & B2B **exemptions expired Jan 1 2023** —
  employers must afford employees (and B2B contacts) consumer rights; CPRA added
  **"sensitive personal information"** (incl. some proxies). Applies to "selling/sharing"
  and delete/correct rights. (Morgan Lewis; Securiti; Lexology.)
- **US federal**: **no omnibus privacy law** — sectoral HIPA (PHI), GLBA (financial),
  FCRA (consumer reports). Employment discrimination law (Title VII / EEOC) makes
  protected-class inferencing (race, health, union) from sentiment a **legal risk**.
- **Other US states**: patchwork (VA, CO, CT, UT, TX, WA, etc.), mostly consumer-not-
  employee; treat CA as the strong-employee baseline.

## Intake allow-list (what may be ingested, by population)
Reference Ruled: **employee / customer / market-actor**. Rule set for the intake path.

| Population | ALLOW (ingestible, datamined minimally) | NO-GO (blocked) | Basis |
|---|---|---|---|
| **Market / business** | public co. filings (SEC EDGAR), licensed newswire/headlines, GDELT public-event aggregates, public price/supply data | proprietary/interior data without license; speculator FX-trading auto | §7I.4 never auto-execute |
| **Customer** (reputation) | reviews the business **owns**/has licensed (Yelp Places, Trustpilot-per-license), aggregate ratings, de-identified counts | raw review text w/ full name+contact coupled to the person; protected-class projections; PII not minimized | CCPA/CPRA delete/share rights; §3.2 context-scoped |
| **Employee** (reputation) | **de-identified aggregate sentiment** (e.g. Glassdoor via licensed aggregator, **no** per-employee identity), complaint **tickets the org owns** (consent-gated), voluntary internal surveys w/ consent | coupling review scores to identifiable employees; protected-class inferencing (health/union/politics); biometric/health proxies; any closed-door monitoring without DPIA/notice | GDPR Art 9 + Art 88; EEOC/Title VII; §3.19 no-unconsented employee exposure |
| **All** | signal stored as **Claim-with-provenance + confidence**, baseline-monitored | nothing ingested as capital-T truth (§3.17) | epistemic discipline |

**Three hard rules (architectural):**
1. **Purpose-limitation + Disclosure gate (§3.19):** never infer same-person across
   contexts from sentiment; cross-context linkage is a logged, consented act.
2. **Minimum PII:** ingest **aggregates and de-identified counts** by default; preserve
   privacy by design (§7B).
3. **Dual-bound:** any derived sentiment→action enters as a **Decision** (§3.12) with
   alternatives+confidence and, where irreversible/unknowable-cost, escalates to a human
   (§3.19, §7B, §7I.4). An employee never *sees* a coupling of their review to their record.

## Privacy-policy skeleton (RelationalOS — the customer/employee-facing artifact)
```
# Privacy & Consent Policy — RelationalOS (skeleton)
## 1. What we process
  Relationship graph, ledger events, and ingested EXTERNAL signals (news, public
  filings, licensed review aggregates) — all as CLAIMS WITH PROVENANCE, not facts.
## 2. Lawful bases (per jurisdiction)
  - EU: Art 6(1)(f) legitimate interest (balancing test on file) for biz/aggregate
          monitoring; Art 9 special categories NEVER unless Art 9(2) exception + DPIA.
  - US-CA: CPRA consumer rights (employee exemptions expired 2023-01-01).
  - US-Fed: sectoral (HIPAA/GLBA/FCRA) respected; no omnibus law.
## 3. Your data & the Disclosure gate
  Identity is universal; CONTEXT is relationship-specific (§3.2). Cross-context linkage
  of the same person is a LOGGED, CONSENTED, REVOCABLE act — never a default inference.
## 4. Employee-specific
  Aggregates only; no per-employee sentiment→record coupling; DPIA where monitoring;
  no protected-class inference (anti-discrimination).
## 5. Consent, rights, retention
  Consent is scoped/duration-bound/revocable (§3.7); rights: access/appeal/privacy/
  refuse/delete/correct per jurisdiction; data-minimization + right-to-forget (§4a).
## 6. Automated decisions
  Recommendations require a Decision with alternatives+confidence; irreversible or
  unknowable-cost actions ALWAYS escalate to a human (§3.19). No auto-execution.
## 7. Security & regulated data
  Confidential-compute evidence anchoring where used (§7B); regulated data (PHI/financial/
  biometric) jurisdiction-tagged and gated.
## 8. Accountability, disputes, contact
  DPO/contact; dispute→evidence→adjudication (§3.13); audit findings (`audit_finding://`).
## 9. Version control
  Policy is a rule:// object, versioned (§3.19), with effective range.
```

## Findings for spec (feed notes/findings.md)
- §7I.6 "no unmoderated access to employee personal data beyond Consent/Disclosure" is
  **confirmed and sharpened**: (a) CPRA makes the employee exemption expired — employees
  have consumer rights; (b) GDPR Art 9 makes most *sensitive* sentiment (health, union,
  politics) **banned** for this purpose, not merely "regulated"; (c) EEOC adds
  discrimination risk to protected-class inferencing.
- **Spec action (Appendix G.17 / §7I.6, bump-only):** state the defaults — *ingest
  aggregates/de-identified counts; treat Glassdoor as sensitive employee data; never
  infer protected classes; couple review scores to identity only under a logged DPIA +
  purpose-limited consent.* Add a pointer that the allow-list + privacy skeleton shipped
  in Sprint-0 (§7I backlog → operational intake policy).

## References
1. GDPR — Art 9 (special categories), Art 88 (employment), EDPB guidance — gdpr-info.eu;
   splitforge.app "HR/Payroll GDPR"; sorainen.com GDPR employment
2. CPRA/CCPA — employee & B2B exemptions expired 2023-01-01 — Morgan Lewis (morganlewis.com);
   securiti.ai "CPRA Employee Data"; lexology.com
3. US federal — no omnibus privacy law; sectoral (HIPAA/GLBA/FCRA); EEOC/Title VII context
4. EDPB / monitoring — employee-monitoring.net (Dereter), gdprhub.eu

---
*All four gating surveys complete.*