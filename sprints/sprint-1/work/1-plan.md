# 1.1 PLAN — S1 Substrate (thin)

**Spec refs:** §4 S1, §3.19 (identity≠authn≠authz), §3.4/§7B (capability authz +
delegation revocation), §3.16 (Ledger/Graph), Appendix F, Sprint-0 schema §3 primitives.

## Goal
A runnable Python service implementing the four S1 functions that read/write the
shared Relationship Graph (state) + append-only Ledger (history) exactly per the
Sprint-0 schema:
- `resolve_identity(subject, evidence) -> person://|org://|agent://` — map a subject
  + evidence to a canonical Identity Actor (reuse an `entity://` canonical-resolution
  record where helpful).
- `authenticate(identity, credentials) -> verif_score` — prove the identity; return a
  0..1 confidence.
- `authorize(identity, action, context) -> permission | denial` — capability-based
  (§7B): build a bounded capability from the relationship's authority/consent and any
  active delegation; return a permission object or a denial. **Delegation revocation
  must immediately void the capability** (§7B).
- `resolve_role(relationship, context) -> role` — read the relationship's `roles`
  attribute for a participant in context (role is an attribute, §C2).

## Design
- Module `artifacts/ros/substrate.py` — a tiny in-memory Graph + append-only Ledger
  store. Ledger entries are content-addressed (SHA-256 over previous-hash + payload),
  signed by the responsible service, RFC3339 timestamps, preserve-unknown on rewrite.
- Module `artifacts/ros/s1.py` — the four functions, operating over the substrate.
- Module `artifacts/ros/checks/s1_check.py` — the self-authored S1 conformance check:
  1. every authorized action corresponds to an ACTIVE relationship capability
     (authority/consent/delegation);
  2. a delegation that is REVOKED/EXPIRED yields a denial (negative test);
  3. role resolution is per-relationship (a customer role is not the employee role in
     another relationship).
- A seed scenario (`make_s1_fixtures.py`) writes actors, the customer relationship,
  consent, authority, a delegation to `agent://s2`, a seeded scoped Trust, and the
  first ledger events.

## DoD (1.1)
- `resolve_identity + resolve_role` resolve a real customer against the ledger → URI + role.
- `authenticate` returns a verif score; `authorize` returns a capability for a
  permitted action and a DENIAL for a non-permitted action.
- Revoking the delegation to `agent://s2` turns a prior ALLOW into DENY (delegation honored).
- Fixtures emitted validate under the Sprint-0 conformance validator pointed at
  Sprint-1 fixtures (exit 0); Sprint-0 run still exits 0.