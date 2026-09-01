# Sprint 4 — work/2-plan (4.2: TWO roles on ONE relationship)

**Input:** 4.1 end-state on `relationship://qk/cust-cxn`.

**Design — role is an attribute, not a separate identity (§3.2, §C2):**
- Extend the SAME relationship's `roles` map so the same actor is BOTH `customer` and
  `employee`. No new `person://`, no new relationship — one relationship, two roles.
- **Role-scoped identity:** query the resolved role by named role (customer vs employee) from
  the relationship's role map.
- **Role-scoped authority:** add per-role authorities to the relationship envelope
  (`authority_by_role`), and `authorize_for_role(identity, action, rel, role)` grants only the
  actions the role's own authority covers. Assert the negative: customer role DENIES an
  employee action and vice-versa.
- **Role-scoped Trust (§3.14):** keyed Trust `(subject,target,claim,context)` with the employee
  context `relationship://qk/cust-cxn?role=employee` (same scheme — schema-valid query param).
  The customer-role Trust (target=solarworks, roofing claim) and the employee-role Trust
  (target=org://quoteko, payroll claim) are DISTINCT scoped values on the same Graph.

**Full loop for the second (employee) role on the SAME relationship:**
S1 role/`authorize_for_role` (employee) → S2 intent/match (payroll/benefits, scoped Trust) →
S3 commit + worker-execute a reversible micro-task (auto-run) → S4 settle a payroll
disbursement (EXCHANGE + obligation + receipt + reconciliation) → S5 capture/verify → employee-
role Trust update (rises) → S2 re-ranks the next employee-role match.

**Checks (4.2):** one relationship carries two roles; role-scoped authz grants/denies per role;
employee-role Trust updated on the `?role=employee` scope; customer-role Trust untouched;
full employee loop closed (S4 in the middle).