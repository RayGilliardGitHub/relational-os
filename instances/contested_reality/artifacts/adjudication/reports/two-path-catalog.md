# §7L TWO-PATH DECISION SURFACE over the ENTIRE ORG CATALOG — CONSOLIDATION-AUDIT (Sprint 34)
generated 2026-09-01T06:22:47Z  |  `run_two_path_catalog_demo.build_catalog` (22 orgs = the union every CR demo runner constructs) + Sprint-33 `_surface`/`_classify` + engine `cockpit_s7l` advisory + `capacity_rerank.capacity_rerank`  |  NO engine change (hash a60f8f7…) and `capacity_rerank.py` (sha256 f7c6a185…) BYTE-IDENTICAL; SPEC v0.22, schema 34264934…, 49 $defs, no new noun.

The Sprint-33 one-framework answer now holds over the WHOLE catalog: every one of these **22 orgs** (the union of every org the run_forecast_*/run_cockpit_*/run_adjudication_engine_demo/r32 runners already construct) is exactly one PATH class — **ADVISORY-no-capacity** (12), **ADVISORY-best-runnable** (6), **RE-RANK** (4) — the advisory Q8 == `cockpit_q7q8` for every org (never shadowed), the re-rank fires only where the machine best is `capacity_infeasible` and picks a provably-distinct replacement, floors are respected everywhere, and every derived label traces to recorded data (reason-not-choice).

--- cove — ADVISORY-no-capacity ---
  advisory: machine_eligible_best='step-therapy-first', Q8 recommendation='step-therapy-first', floor_gated=['authorize-off-formulary', 'deny-off-formulary']
  capacity_constraint.options_flagged=None
  rerank: needed=False, prior_machine_best='step-therapy-first', replacement='step-therapy-first', replacement_is_baseline=False

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

--- deli-atcap — ADVISORY-best-runnable ---
  advisory: machine_eligible_best='partial-settlement', Q8 recommendation='partial-settlement', floor_gated=['accept-customer-refund']
  capacity_constraint.options_flagged={'accept-customer-refund': 'capacity_risk', 'accept-company-full-payment': 'capacity_risk', 'partial-settlement': 'capacity_risk', 'conditional-resolution': 'capacity_risk', 'request-more-evidence': 'capacity_risk', 'escalate': 'capacity_risk', 'external-adjudication': 'capacity_risk'}
  rerank: needed=False, prior_machine_best='partial-settlement', replacement='partial-settlement', replacement_is_baseline=False

--- deli-cost — ADVISORY-no-capacity ---
  advisory: machine_eligible_best='partial-settlement', Q8 recommendation='partial-settlement', floor_gated=['accept-customer-refund']
  capacity_constraint.options_flagged=None
  rerank: needed=False, prior_machine_best='partial-settlement', replacement='partial-settlement', replacement_is_baseline=False

--- deli-cost-flat — ADVISORY-no-capacity ---
  advisory: machine_eligible_best='partial-settlement', Q8 recommendation='partial-settlement', floor_gated=['accept-customer-refund']
  capacity_constraint.options_flagged=None
  rerank: needed=False, prior_machine_best='partial-settlement', replacement='partial-settlement', replacement_is_baseline=False

--- deli-deficit — ADVISORY-best-runnable ---
  advisory: machine_eligible_best='partial-settlement', Q8 recommendation='partial-settlement', floor_gated=['accept-customer-refund']
  capacity_constraint.options_flagged={'accept-customer-refund': 'capacity_risk', 'accept-company-full-payment': 'capacity_risk', 'partial-settlement': 'capacity_risk', 'conditional-resolution': 'capacity_risk', 'request-more-evidence': 'capacity_risk', 'escalate': 'capacity_risk', 'external-adjudication': 'capacity_risk'}
  rerank: needed=False, prior_machine_best='partial-settlement', replacement='partial-settlement', replacement_is_baseline=False

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

--- deli-forecast-flat — ADVISORY-no-capacity ---
  advisory: machine_eligible_best='partial-settlement', Q8 recommendation='partial-settlement', floor_gated=['accept-customer-refund']
  capacity_constraint.options_flagged=None
  rerank: needed=False, prior_machine_best='partial-settlement', replacement='partial-settlement', replacement_is_baseline=False

--- deli-infcap — ADVISORY-best-runnable ---
  advisory: machine_eligible_best='partial-settlement', Q8 recommendation='partial-settlement', floor_gated=['accept-customer-refund']
  capacity_constraint.options_flagged={'accept-customer-refund': 'capacity_infeasible', 'accept-company-full-payment': 'capacity_infeasible', 'partial-settlement': 'capacity_risk', 'conditional-resolution': 'capacity_risk', 'request-more-evidence': 'capacity_risk', 'escalate': 'capacity_risk', 'external-adjudication': 'capacity_infeasible'}
  rerank: needed=False, prior_machine_best='partial-settlement', replacement='partial-settlement', replacement_is_baseline=False

--- deli-learn — ADVISORY-no-capacity ---
  advisory: machine_eligible_best='partial-settlement', Q8 recommendation='partial-settlement', floor_gated=['accept-customer-refund']
  capacity_constraint.options_flagged=None
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

--- inspect-corroboration — ADVISORY-no-capacity ---
  advisory: machine_eligible_best='rework-partial-credit', Q8 recommendation='rework-partial-credit', floor_gated=['accept-batch', 'reject-batch-return']
  capacity_constraint.options_flagged=None
  rerank: needed=False, prior_machine_best='rework-partial-credit', replacement='rework-partial-credit', replacement_is_baseline=False

--- inspect-learn-b — ADVISORY-no-capacity ---
  advisory: machine_eligible_best='rework-partial-credit', Q8 recommendation='rework-partial-credit', floor_gated=['accept-batch', 'reject-batch-return']
  capacity_constraint.options_flagged=None
  rerank: needed=False, prior_machine_best='rework-partial-credit', replacement='rework-partial-credit', replacement_is_baseline=False

--- inspect-nodata — ADVISORY-no-capacity ---
  advisory: machine_eligible_best='rework-partial-credit', Q8 recommendation='rework-partial-credit', floor_gated=['accept-batch', 'reject-batch-return']
  capacity_constraint.options_flagged=None
  rerank: needed=False, prior_machine_best='rework-partial-credit', replacement='rework-partial-credit', replacement_is_baseline=False

--- inspect-recorded — RE-RANK ---
  advisory: machine_eligible_best='rework-partial-credit', Q8 recommendation='rework-partial-credit', floor_gated=['accept-batch', 'reject-batch-return']
  capacity_constraint.options_flagged={'accept-batch': 'capacity_infeasible', 'reject-batch-return': 'capacity_infeasible', 'rework-partial-credit': 'capacity_infeasible', 'conditional-accept-with-guarantee': 'capacity_risk', 'request-more-evidence': 'capacity_risk', 'escalate': 'capacity_risk'}
  rerank: needed=True, prior_machine_best='rework-partial-credit', replacement='conditional-accept-with-guarantee', replacement_is_baseline=False

## whole-catalog taxonomy
**12 ADVISORY-no-capacity / 6 ADVISORY-best-runnable / 4 RE-RANK = 22 orgs.** Sprint-33's 13-org {5,4,4} is the strict subset; the 9 added are 7 no-capacity (these carry no capacity_constraint block) + 2 best-runnable (deli-atcap, deli-deficit — recorded capacity but NO per-option requirements, so best is `capacity_risk`, never `capacity_infeasible`, nothing to re-rank).

## §16 verdict

**The two-path decision surface is ONE coherent recorded-data framework across the ENTIRE catalog — not just the 13-org Sprint-33 set.** For all 22 orgs the reason-not-choice ADVISORY reproduces the Sprint-31 inventory (marker never re-ranks; advisory Q8 == `cockpit_q7q8`), the POLICY-authorized RE-RANK reproduces the Sprint-32 results (4 firings, provably-distinct replacement, 18 unchanged where the advisory already holds) from the SAME recorded data, and every org falls into exactly one exhaustive-disjoint PATH class. Floor integrity holds everywhere; the re-rank never shadows the advisory; and the boundary stays honest: the deterministic advisory labels (even the recommended option capacity_infeasible) and never re-ranks, while the re-rank CHANGES the Q8 recommendation only under the machine's explicit POLICY — reported as DATA, never overwriting the engine's advisory Q8.

**Still not derivable (the honest residual — unchanged by this audit):** a probabilistic/stochastic forecast (the recorded band is a spread, never a CI; nothing invents a distribution); a per-option requirement NOT unit-coupled to the recorded capacity value (no available figure -> no infeasibility label -> nothing to re-rank); an option with no recorded requirement carries no infeasibility label (the machine never invents one); and any choice the §6 human must make that recorded data cannot machine-decide (the re-rank is POLICY-authorized, not a claim of objective best). No SPEC bump (v0.22).

_CONSOLIDATION-AUDIT; engine `a60f8f7…` + `capacity_rerank.py` `f7c6a185…` BYTE-IDENTICAL; frozen ontology, schema 34264934…, SPEC v0.22, 49 $defs, URI cap, no new noun. The two-path decision surface is ONE coherent recorded-data framework across the whole catalog._
