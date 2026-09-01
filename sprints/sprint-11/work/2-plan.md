# Sub-sprint 2 — Build `tradeoff_model.py` (the utility engine)

## Objective
A pure, deterministic, stdlib-only utility engine that ranks the adjudication options
{side-employee, side-manager, remote-with-coverage-plan, do-nothing/UNRESOLVED} from recorded
constraints, and applies the §6 human floor to irreversible/unknown-cost options.

## Design decisions
- **Weights ARE the business model** (SPEC §7K.1 "what better means"): documented, sum to 1.0
  (sla .45 / emp .20 / mgr .15 / leave .10 / cost .10). The ranking is *computed* from these +
  the recorded inputs — not authored per case.
- **Five factors** per option, all in [0,1]: sla compliance (on-site >= floor), employee-interest
  satisfaction, manager/staffing satisfaction, accrued-leave utilisation, coordination cost.
- **§6 floor:** an option that is irreversible/unknown-cost is `floor_gated` (minus a documented
  FLOOR_PENALTY) and excluded from the machine's auto-pick. `do-nothing` is never gated.
- **Deterministic ordering:** utility desc, then canonical OPTIONS order (never dict order).
- **Output object:** the trade-off is carried as an additive field on the case, shaped to the
  FROZEN `Recommendation` $def (by/for/options/includes_do_nothing/tradeoff/authority_required/
  confidence/expected_impact/decision + a machine-readable `json` ranking). No new scheme/noun.

## Verification
- `python3 tradeoff_model.py` self-check prints both scenarios' rankings.
  Scenario 1 (coverage KNOWN): remote-with-coverage-plan must rank top; do-nothing must beat the
  SLA-breaking side-employee (do-nothing is never worse than breaching the customer SLA).
  Scenario 2 (coverage UNKNOWN): every staff-changing option must be floor-gated; do-nothing/
  UNRESOLVED is the only machine-eligible direction → human decides, Trust untouched.

## Exit criteria
Self-check runs, rankings are deterministic and match the above expectations. Proceed to
sub-sprint 3 (the demo).