# §7L TWO-PATH DECISION SURFACE — the reason-not-choice ADVISORY + the POLICY-authorized capacity-constrained RE-RANK, consolidated as ONE coherent recorded-data framework (Sprint 33)
generated 2026-09-01T05:56:03Z  |  `run_two_path_demo._surface` + engine `cockpit_s7l` advisory + `capacity_rerank.capacity_rerank`  |  NO engine change (hash a60f8f7…) and `capacity_rerank.py` (sha256 f7c6a185…) BYTE-IDENTICAL; SPEC v0.22, 49 $defs, no new noun.

Every org is exactly one PATH class: **ADVISORY-no-capacity** (no recorded authority capacity -> nothing to constrain/re-rank), **ADVISORY-best-runnable** (capacity recorded, machine best NOT capacity_infeasible -> the advisory stands, re-rank needed=False), **RE-RANK** (best capacity_infeasible from recorded per-option capacity_requirements -> by authorized POLICY the machine picks the highest-utility option that is neither floor-gated nor capacity_infeasible). The two paths are proven to compose: the re-rank NEVER shadows the advisory (advisory Q8 == `cockpit_q7q8` for every org), and where it fires its replacement is a provably DIFFERENT option; where needed=False they agree (replacement == advisory Q8).

--- cove-recommend-infcap — RE-RANK ---
  advisory: machine_eligible_best='step-therapy-first', Q8 recommendation='step-therapy-first', floor_gated=['authorize-off-formulary', 'deny-off-formulary']
  capacity_constraint.options_flagged={'authorize-off-formulary': 'capacity_infeasible', 'deny-off-formulary': 'capacity_infeasible', 'step-therapy-first': 'capacity_infeasible', 'authorize-generic': 'capacity_risk', 'request-more-evidence': 'capacity_risk', 'escalate-to-medical-director': 'capacity_risk', 'external-peer-review': 'capacity_risk'}
  rerank: needed=True, prior_machine_best='step-therapy-first', replacement='authorize-generic', replacement_is_baseline=False

--- cove-recorded — ADVISORY-best-runnable ---
  advisory: machine_eligible_best='step-therapy-first', Q8 recommendation='step-therapy-first', floor_gated=['authorize-off-formulary', 'deny-off-formulary']
  capacity_constraint.options_flagged={'authorize-off-formulary': 'capacity_infeasible', 'deny-off-formulary': 'capacity_infeasible', 'step-therapy-first': 'capacity_risk', 'authorize-generic': 'capacity_risk', 'request-more-evidence': 'capacity_risk', 'escalate-to-medical-director': 'capacity_risk', 'external-peer-review': 'capacity_risk'}
  rerank: needed=False, prior_machine_best='step-therapy-first', replacement='step-therapy-first', replacement_is_baseline=False

--- deli — ADVISORY-no-capacity ---
  advisory: machine_eligible_best='partial-settlement', Q8 recommendation='partial-settlement', floor_gated=['accept-customer-refund']
  capacity_constraint.options_flagged=None
  rerank: needed=False, prior_machine_best='partial-settlement', replacement='partial-settlement', replacement_is_baseline=False

--- deli-all-infeasible — RE-RANK ---
  advisory: machine_eligible_best='partial-settlement', Q8 recommendation='partial-settlement', floor_gated=['accept-customer-refund']
  capacity_constraint.options_flagged={'accept-customer-refund': 'capacity_infeasible', 'accept-company-full-payment': 'capacity_infeasible', 'partial-settlement': 'capacity_infeasible', 'conditional-resolution': 'capacity_infeasible', 'request-more-evidence': 'capacity_infeasible', 'escalate': 'capacity_infeasible', 'external-adjudication': 'capacity_infeasible'}
  rerank: needed=True, prior_machine_best='partial-settlement', replacement='unresolved', replacement_is_baseline=True

--- deli-deficit-inf — ADVISORY-best-runnable ---
  advisory: machine_eligible_best='partial-settlement', Q8 recommendation='partial-settlement', floor_gated=['accept-customer-refund']
  capacity_constraint.options_flagged={'accept-customer-refund': 'capacity_infeasible', 'accept-company-full-payment': 'capacity_infeasible', 'partial-settlement': 'capacity_risk', 'conditional-resolution': 'capacity_risk', 'request-more-evidence': 'capacity_risk', 'escalate': 'capacity_risk', 'external-adjudication': 'capacity_infeasible'}
  rerank: needed=False, prior_machine_best='partial-settlement', replacement='partial-settlement', replacement_is_baseline=False

--- deli-flat2 — ADVISORY-no-capacity ---
  advisory: machine_eligible_best='partial-settlement', Q8 recommendation='partial-settlement', floor_gated=['accept-customer-refund']
  capacity_constraint.options_flagged=None
  rerank: needed=False, prior_machine_best='partial-settlement', replacement='partial-settlement', replacement_is_baseline=False

--- deli-forecast — ADVISORY-no-capacity ---
  advisory: machine_eligible_best='partial-settlement', Q8 recommendation='partial-settlement', floor_gated=['accept-customer-refund']
  capacity_constraint.options_flagged=None
  rerank: needed=False, prior_machine_best='partial-settlement', replacement='partial-settlement', replacement_is_baseline=False

--- deli-infcap — ADVISORY-best-runnable ---
  advisory: machine_eligible_best='partial-settlement', Q8 recommendation='partial-settlement', floor_gated=['accept-customer-refund']
  capacity_constraint.options_flagged={'accept-customer-refund': 'capacity_infeasible', 'accept-company-full-payment': 'capacity_infeasible', 'partial-settlement': 'capacity_risk', 'conditional-resolution': 'capacity_risk', 'request-more-evidence': 'capacity_risk', 'escalate': 'capacity_risk', 'external-adjudication': 'capacity_infeasible'}
  rerank: needed=False, prior_machine_best='partial-settlement', replacement='partial-settlement', replacement_is_baseline=False

--- deli-recommend-infcap — RE-RANK ---
  advisory: machine_eligible_best='partial-settlement', Q8 recommendation='partial-settlement', floor_gated=['accept-customer-refund']
  capacity_constraint.options_flagged={'accept-customer-refund': 'capacity_risk', 'accept-company-full-payment': 'capacity_risk', 'partial-settlement': 'capacity_infeasible', 'conditional-resolution': 'capacity_risk', 'request-more-evidence': 'capacity_risk', 'escalate': 'capacity_risk', 'external-adjudication': 'capacity_risk'}
  rerank: needed=True, prior_machine_best='partial-settlement', replacement='conditional-resolution', replacement_is_baseline=False

--- deli-varmax — ADVISORY-no-capacity ---
  advisory: machine_eligible_best='partial-settlement', Q8 recommendation='partial-settlement', floor_gated=['accept-customer-refund']
  capacity_constraint.options_flagged=None
  rerank: needed=False, prior_machine_best='partial-settlement', replacement='partial-settlement', replacement_is_baseline=False

--- deli-varmax-cap — ADVISORY-best-runnable ---
  advisory: machine_eligible_best='partial-settlement', Q8 recommendation='partial-settlement', floor_gated=['accept-customer-refund']
  capacity_constraint.options_flagged={}
  rerank: needed=False, prior_machine_best='partial-settlement', replacement='partial-settlement', replacement_is_baseline=False

--- inspect-nodata — ADVISORY-no-capacity ---
  advisory: machine_eligible_best='rework-partial-credit', Q8 recommendation='rework-partial-credit', floor_gated=['accept-batch', 'reject-batch-return']
  capacity_constraint.options_flagged=None
  rerank: needed=False, prior_machine_best='rework-partial-credit', replacement='rework-partial-credit', replacement_is_baseline=False

--- inspect-recorded — RE-RANK ---
  advisory: machine_eligible_best='rework-partial-credit', Q8 recommendation='rework-partial-credit', floor_gated=['accept-batch', 'reject-batch-return']
  capacity_constraint.options_flagged={'accept-batch': 'capacity_infeasible', 'reject-batch-return': 'capacity_infeasible', 'rework-partial-credit': 'capacity_infeasible', 'conditional-accept-with-guarantee': 'capacity_risk', 'request-more-evidence': 'capacity_risk', 'escalate': 'capacity_risk'}
  rerank: needed=True, prior_machine_best='rework-partial-credit', replacement='conditional-accept-with-guarantee', replacement_is_baseline=False

## §16 verdict

**The two paths are now a SINGLE coherent recorded-data decision framework — they compose without one silently overriding the other.** For all 13 orgs the reason-not-choice ADVISORY report reproduces the Sprint-31 inventory (11/11 q7/q8 == `cockpit_q7q8`; the marker never re-ranks) AND the POLICY-authorized RE-RANK reproduces the Sprint-32 results (4 firings with a provably-different replacement, 9 unchanged where the advisory already holds) — from the SAME recorded data, so the consolidation is a VIEW, not a rewrite. Every org is exactly one exhaustive-disjoint PATH class; neither the advisory nor the re-rank ever picks a floor-gated option; and the boundary stays honest: the deterministic advisory labels (even the recommended option capacity_infeasible) and never re-ranks, while the re-rank CHANGES the Q8 recommendation only under the machine's explicit POLICY — reported as DATA, never overwriting the engine's advisory Q8.

**Still not derivable (the honest residual — unchanged by consolidation):** a probabilistic/stochastic forecast (the recorded band is a spread, never a CI; nothing invents a distribution); a per-option requirement NOT unit-coupled to the recorded capacity value (no available figure -> no infeasibility label -> nothing to re-rank); an option with no recorded requirement carries no infeasibility label (the machine never invents one); and any choice the §6 human must make that recorded data cannot machine-decide (the re-rank is POLICY-authorized, not a claim of objective best). No SPEC bump (v0.22).

_Additive consolidation; engine `a60f8f7…` + `capacity_rerank.py` `f7c6a185…` BYTE-IDENTICAL; frozen ontology, SPEC v0.22, 49 $defs, URI cap, no new noun. The two-path decision surface is ONE coherent recorded-data framework._
