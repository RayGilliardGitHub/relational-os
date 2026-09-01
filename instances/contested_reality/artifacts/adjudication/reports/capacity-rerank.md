# §7L Q8 capacity-constrained RE-RANK for the machine — by the frozen `rank` utility (Sprint 32, an authorized POLICY step on top of the unchanged reason-not-choice advisory)
generated 2026-09-01T05:08:28Z  |  `capacity_rerank.capacity_rerank` (new, additive) + engine `cockpit_s7l` advisory  |  NO engine change (hash a60f8f7…); SPEC v0.22, 49 $defs, URI cap, no new noun.

The advisory path NEVER re-ranks: for every org the engine's Q8 recommendation still equals `cockpit_q7q8`. The re-rank is the deliberate, additively-built step the Sprint 31 prompt explicitly authorized: when an org's machine-eligible best is `capacity_infeasible` from RECORDED per-option `capacity_requirements`, BY POLICY the machine picks the highest-utility option (frozen `rank`) that is neither floor-gated nor `capacity_infeasible`. Respects the §6 floor (a floor-gated option is never auto-picked); never invents a requirement; the do-nothing/UNRESOLVED baseline is the honest fallback when every capacity-consuming option is infeasible (and it SAYS so).

--- deli-recommend-infcap ---
  needed: True  |  prior machine best: 'partial-settlement' (flag 'capacity_infeasible')
  re-ranked replacement: 'conditional-resolution'  | replacement_is_baseline: False  | all_capacity_consuming_infeasible: False
  recorded descriptors: ['capacity', 'capacity_requirements']  | available_capacity: 498.7  | per_option_requirements: {'partial-settlement': 499.0, 'conditional-resolution': 200.0, 'accept-customer-refund': 200.0, 'accept-company-full-payment': 200.0, 'external-adjudication': 100.0, 'request-more-evidence': 50.0, 'escalate': 80.0}
  policy: capacity-constrained re-rank for the machine (authorized POLICY step): from the frozen rank utility ordering, the highest-utility option that is neither floor-gated nor capacity_infeasible
  why: the recorded capacity says the machine's prior best cannot run under capacity: prior best `partial-settlement` records a per-option requirement of 499.0 against an available capacity of 498.7 (recorded capacity VALUE minus recorded load, same unit), so the forward advisory engineered it `capacity_infeasible`; BY AUTHORIZED POLICY the machine picks the highest-utility option that is neither floor-gated nor capacity_infeasible -> `conditional-resolution`.

--- inspect-recorded ---
  needed: True  |  prior machine best: 'rework-partial-credit' (flag 'capacity_infeasible')
  re-ranked replacement: 'conditional-accept-with-guarantee'  | replacement_is_baseline: False  | all_capacity_consuming_infeasible: False
  recorded descriptors: ['capacity', 'capacity_requirements']  | available_capacity: 498.7  | per_option_requirements: {'accept-batch': 510.0, 'reject-batch-return': 500.0, 'rework-partial-credit': 499.0, 'conditional-accept-with-guarantee': 200.0, 'request-more-evidence': 100.0, 'escalate': 150.0}
  policy: capacity-constrained re-rank for the machine (authorized POLICY step): from the frozen rank utility ordering, the highest-utility option that is neither floor-gated nor capacity_infeasible
  why: the recorded capacity says the machine's prior best cannot run under capacity: prior best `rework-partial-credit` records a per-option requirement of 499.0 against an available capacity of 498.7 (recorded capacity VALUE minus recorded load, same unit), so the forward advisory engineered it `capacity_infeasible`; BY AUTHORIZED POLICY the machine picks the highest-utility option that is neither floor-gated nor capacity_infeasible -> `conditional-accept-with-guarantee`.

--- cove-recommend-infcap ---
  needed: True  |  prior machine best: 'step-therapy-first' (flag 'capacity_infeasible')
  re-ranked replacement: 'authorize-generic'  | replacement_is_baseline: False  | all_capacity_consuming_infeasible: False
  recorded descriptors: ['capacity', 'capacity_requirements']  | available_capacity: 29.1  | per_option_requirements: {'authorize-off-formulary': 30.0, 'deny-off-formulary': 30.0, 'step-therapy-first': 30.0, 'authorize-generic': 25.0, 'request-more-evidence': 10.0, 'escalate-to-medical-director': 15.0, 'external-peer-review': 20.0}
  policy: capacity-constrained re-rank for the machine (authorized POLICY step): from the frozen rank utility ordering, the highest-utility option that is neither floor-gated nor capacity_infeasible
  why: the recorded capacity says the machine's prior best cannot run under capacity: prior best `step-therapy-first` records a per-option requirement of 30.0 against an available capacity of 29.1 (recorded capacity VALUE minus recorded load, same unit), so the forward advisory engineered it `capacity_infeasible`; BY AUTHORIZED POLICY the machine picks the highest-utility option that is neither floor-gated nor capacity_infeasible -> `authorize-generic`.

--- deli-all-infeasible ---
  needed: True  |  prior machine best: 'partial-settlement' (flag 'capacity_infeasible')
  re-ranked replacement: 'unresolved'  | replacement_is_baseline: True  | all_capacity_consuming_infeasible: True
  recorded descriptors: ['capacity', 'capacity_requirements']  | available_capacity: 499.0  | per_option_requirements: {'accept-customer-refund': 500.0, 'accept-company-full-payment': 500.0, 'partial-settlement': 500.0, 'conditional-resolution': 500.0, 'request-more-evidence': 500.0, 'escalate': 500.0, 'external-adjudication': 500.0}
  policy: capacity-constrained re-rank for the machine (authorized POLICY step): from the frozen rank utility ordering, the highest-utility option that is neither floor-gated nor capacity_infeasible
  why: the recorded capacity says the machine's prior best cannot run under capacity: prior best `partial-settlement` records a per-option requirement of 500.0 against an available capacity of 499.0 (recorded capacity VALUE minus recorded load, same unit), so the forward advisory engineered it `capacity_infeasible`; BY AUTHORIZED POLICY the machine picks the highest-utility option that is neither floor-gated nor capacity_infeasible -> `unresolved`.

--- cove-recorded ---
  needed: False  |  prior machine best: 'step-therapy-first' (flag 'capacity_risk')
  re-ranked replacement: 'step-therapy-first'  | replacement_is_baseline: False  | all_capacity_consuming_infeasible: False
  recorded descriptors: ['capacity', 'capacity_requirements']  | available_capacity: 29.1  | per_option_requirements: {'authorize-off-formulary': 30.0, 'deny-off-formulary': 30.0, 'step-therapy-first': 28.0, 'authorize-generic': 25.0, 'request-more-evidence': 10.0, 'escalate-to-medical-director': 15.0, 'external-peer-review': 20.0}
  policy: capacity-constrained re-rank for the machine (authorized POLICY step): from the frozen rank utility ordering, the highest-utility option that is neither floor-gated nor capacity_infeasible
  why: prior best runnable

--- deli-infcap ---
  needed: False  |  prior machine best: 'partial-settlement' (flag 'capacity_risk')
  re-ranked replacement: 'partial-settlement'  | replacement_is_baseline: False  | all_capacity_consuming_infeasible: False
  recorded descriptors: ['capacity', 'capacity_requirements']  | available_capacity: 498.7  | per_option_requirements: {'accept-customer-refund': 499.0, 'accept-company-full-payment': 499.0, 'external-adjudication': 499.0, 'partial-settlement': 200.0, 'conditional-resolution': 200.0, 'request-more-evidence': 50.0, 'escalate': 100.0}
  policy: capacity-constrained re-rank for the machine (authorized POLICY step): from the frozen rank utility ordering, the highest-utility option that is neither floor-gated nor capacity_infeasible
  why: prior best runnable

--- deli-deficit-inf ---
  needed: False  |  prior machine best: 'partial-settlement' (flag 'capacity_risk')
  re-ranked replacement: 'partial-settlement'  | replacement_is_baseline: False  | all_capacity_consuming_infeasible: False
  recorded descriptors: ['capacity', 'capacity_requirements']  | available_capacity: 29.1  | per_option_requirements: {'external-adjudication': 30.0, 'accept-company-full-payment': 30.0, 'accept-customer-refund': 30.0, 'partial-settlement': 20.0, 'conditional-resolution': 20.0, 'request-more-evidence': 10.0, 'escalate': 15.0}
  policy: capacity-constrained re-rank for the machine (authorized POLICY step): from the frozen rank utility ordering, the highest-utility option that is neither floor-gated nor capacity_infeasible
  why: prior best runnable

--- inspect-nodata ---
  needed: False  |  prior machine best: 'rework-partial-credit' (flag None)
  re-ranked replacement: 'rework-partial-credit'  | replacement_is_baseline: False  | all_capacity_consuming_infeasible: False
  recorded descriptors: []  | available_capacity: None  | per_option_requirements: None
  policy: capacity-constrained re-rank for the machine (authorized POLICY step): from the frozen rank utility ordering, the highest-utility option that is neither floor-gated nor capacity_infeasible
  why: no recorded capacity

## §16 verdict

**The ONE remaining frontier from Sprint 31 — a capacity-constrained, re-ranked Q8 recommendation under recorded capacity — is now DERIVABLE, as an explicit authorized POLICY step distinct from the deterministic advisory label-vs-choice boundary.** The advisory path still labels (even the RECOMMENDED option `capacity_infeasible`) and never re-ranks (the Sprint-31 reason-not-choice inventory stands — proven here: every engine Q8 recommendation == `cockpit_q7q8`, including the orgs where re-rank fires). The re-rank computes, from RECORDED per-option `capacity_requirements` + the frozen `rank` ordering, the highest-utility option that is neither floor-gated nor `capacity_infeasible`; it changes the Q8 recommendation only under the machine's explicit POLICY, never on the advisory path, and it respects the §6 floor. Deterministic, additive (new module, engine byte-identical, hash a60f8f7…), honest (fallback to the do-nothing baseline is stated).

**Still not derivable (the honest residual):** a probabilistic/stochastic forecast (the recorded band is a spread, not a CI, and nothing here invents a distribution); a per-option requirement that is NOT unit-coupled to the recorded capacity value (no available figure to subtract -> no infeasibility label -> nothing to re-rank); an option with no recorded requirement carries no infeasibility label (the machine never invents one for it); and any choice the §6 human must make that recorded data cannot machine-decide (the re-rank is POLICY-authorized, not a claim of objective best). No SPEC bump (v0.22).

_Additive; frozen ontology, SPEC v0.22, 49 $defs, URI cap. The reason-not-choice advisory stands on the default path (Sprint-31 inventory intact); the re-rank is the authorized, distinct 're-rank for the machine' POLICY capability._
