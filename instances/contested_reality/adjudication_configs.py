"""adjudication_configs.py — SPRINT 13: two org scenarios, as pure DATA for the configurable
adjudication engine. Nothing here is imported by the engine's logic — the engine (in
adjudication_engine.py) is fully generic and consumes these dicts. Changing org = changing
data, never code. Each key is documented so an operator can author a third org without
touching the engine.

Two deliberately DIFFERENT orgs:
  A. `deli` — a freight/delivery financial dispute ($18k). Factors: evidence, contractual,
     relationship, cost.
  B. `cove` — a clinical co-pay/coverage dispute (payer vs provider vs patient). Factors:
     medical_necessity, safety, policy, cost. Different options, weights, gated set, authority.
"""
from __future__ import annotations


# ==============================================================================================
# A. DELIVERY — the Sprint-12 $18,000 customer dispute, re-expressed as CONFIG (no engine code)
# ==============================================================================================
DELI = {
    "label": "deli",
    "scene": "delivery",
    "company_name": "Constellar Freight",
    "ledger_name": "db://ledger/adjudication-deli-2026",
    "registrar": "person://deli/registrar",
    "verify": "system://deli/verify",
    "actors": {
        "org://deli/customer": "ORG", "org://deli/company": "ORG", "org://deli/supplier": "ORG",
        "person://deli/registrar": "PERSON", "person://deli/adjudicator": "PERSON",
        "person://deli/appeal": "PERSON", "system://deli/verify": "SYSTEM",
    },
    "relationships": {
        "customer-contract": {"uri": "relationship://deli/customer-contract",
                              "status": "ACTIVE",
                              "participants": ["org://deli/customer", "org://deli/company"],
                              "roles": {"org://deli/customer": ["buyer"],
                                        "org://deli/company": ["provider"]},
                              "purpose": "contracted service delivery with a deadline"},
        "supplier-contract": {"uri": "relationship://deli/supplier-contract",
                              "status": "ACTIVE",
                              "participants": ["org://deli/supplier", "org://deli/company"],
                              "roles": {"org://deli/supplier": ["shipper"],
                                        "org://deli/company": ["customer"]},
                              "purpose": "supplier shipping for the delivery"},
    },
    "obligations": {
        "deliver-due": {"uri": "obligation://deli/deliver-due", "subject": "org://deli/company",
                        "source": "VOLUNTARILY_UNDERTAKEN",
                        "content": "deliver the contracted service by the deadline",
                        "due_by": "2026-08-31T16:00:00-06:00"},
        "pay-due": {"uri": "obligation://deli/pay-due", "subject": "org://deli/customer",
                    "source": "VOLUNTARILY_UNDERTAKEN",
                    "content": "pay the $18,000 invoice on confirmed delivery",
                    "due_by": "2026-09-30T00:00:00-06:00"},
    },
    "appeal_right": "right://deli/cust-appeal",
    "claimants": ["org://deli/customer"],
    "dispute_about": "obligation://deli/deliver-due",
    "dispute": {
        "uri": "dispute://deli/delivery", "about": "obligation://deli/deliver-due",
        "parties": ["org://deli/customer", "org://deli/company", "org://deli/supplier"],
        "status": "OPEN", "fin_impact_usd": 18000,
        "deadline_ref": "resolution expected within 7 business days",
        "interest_blocks": {"customer": "pay only for delivered service",
                            "company": "collect valid invoice; protect reputation",
                            "supplier": "established on-time shipment, not blamed"},
        "constraint_blocks": {"sla_grace_minutes": 15, "refund_auto_cap_usd": 5000,
                              "irreversible": "a full refund/admission is irreversible/unknown-cost "
                                              "-> §6 human floor"},
    },
    "claims": [
        {"uri": "claim://deli/late", "proposer": "org://deli/customer",
         "statement": "the contracted service was NOT delivered on time; signed receipt 16:15 "
                      "past the 16:00 deadline — we should not pay for the late delivery.",
         "evidence": ["evidence://deli/arrival-receipt", "evidence://deli/gps-arrival"]},
        {"uri": "claim://deli/delivered", "proposer": "org://deli/company",
         "statement": "the contracted service WAS delivered and is payable; an independent "
                      "anchored verification confirms delivery liveness.",
         "evidence": ["evidence://deli/third-party-verification"]},
        {"uri": "claim://deli/shipped", "proposer": "org://deli/supplier",
         "statement": "we shipped the consignment on time.",
         "evidence": ["evidence://deli/supplier-shipping"]},
    ],
    "evidence": {
        "gps":    {"uri": "evidence://deli/gps-arrival", "kind": "ANCHORED",
                   "source": "fleet-GPS-livestate", "captured_at": "2026-08-31T16:12:00-06:00",
                   "verity": {"procedure": "gps-timestamp", "confidence": 0.85},
                   "reliability": 0.85, "about": "arrival gate event",
                   "supports": "claim://deli/late"},
        "receipt": {"uri": "evidence://deli/arrival-receipt", "kind": "TESTIMONY",
                    "source": "customer-signed-receipt", "captured_at": "2026-08-31T16:15:00-06:00",
                    "verity": {"procedure": "signed-receipt", "confidence": 0.9},
                    "reliability": 0.9, "about": "delivery receipt", "supports": "claim://deli/late"},
        "anchor":  {"uri": "evidence://deli/third-party-verification", "kind": "ANCHORED",
                    "source": "independent-audit-service",
                    "captured_at": "2026-08-31T17:05:00-06:00",
                    "verity": {"procedure": "anchored-liveness", "confidence": 0.97},
                    "reliability": 0.97, "about": "delivery liveness verification",
                    "supports": "claim://deli/delivered"},
        "shipping": {"uri": "evidence://deli/supplier-shipping", "kind": "RECORD",
                     "source": "supplier-shipping-system",
                     "captured_at": "2026-08-31T15:58:00-06:00",
                     "verity": {"procedure": "shipping-log", "confidence": 0.92},
                     "reliability": 0.92, "about": "ship-out time",
                     "supports": "claim://deli/shipped"},
    },
    # ---- the business model (§7K.1): documented, sum == 1.0 ----
    "weights": {"evidence": 0.35, "contractual": 0.30, "relationship": 0.20, "cost": 0.15},
    # ---- each option's modeled value per factor (data, in [0,1]) ----
    "factor_scores": {
        "accept-customer-refund":    {"evidence": 0.30, "contractual": 0.50, "relationship": 1.00, "cost": 0.20},
        "accept-company-full-payment": {"evidence": 0.70, "contractual": 0.60, "relationship": 0.30, "cost": 0.90},
        "partial-settlement":       {"evidence": 0.65, "contractual": 0.80, "relationship": 0.85, "cost": 0.60},
        "conditional-resolution":   {"evidence": 0.60, "contractual": 0.70, "relationship": 0.70, "cost": 0.70},
        "request-more-evidence":    {"evidence": 0.40, "contractual": 0.40, "relationship": 0.50, "cost": 0.50},
        "escalate":                 {"evidence": 0.50, "contractual": 0.30, "relationship": 0.35, "cost": 0.30},
        "unresolved":               {"evidence": 0.40, "contractual": 0.40, "relationship": 0.40, "cost": 0.40},
        "external-adjudication":    {"evidence": 0.60, "contractual": 0.40, "relationship": 0.20, "cost": 0.10},
    },
    "options": ["accept-customer-refund", "accept-company-full-payment", "partial-settlement",
                "conditional-resolution", "request-more-evidence", "escalate", "unresolved",
                "external-adjudication"],
    "floor_gated": {"accept-customer-refund"},     # a disputed refund admission is irreversible/unknown-cost
    "floor_penalty": 0.20,
    "reconcile": {"rule": "best-reliability-threshold", "threshold": 0.95, "support_floor": 0.55},
    "authority": {"dispute": "authority://deli/adjudicate", "appeal": "authority://deli/adjudicate-appeal",
                  "adjudicator_person": "person://deli/adjudicator", "appeal_person": "person://deli/appeal"},
    "determination_policy": "adopt-eligible-best",
    "resolution_outcome": "partial settlement on the contested delivery; SLA-breach credit applied; "
                          "ledger noted; customer keeps the service",
    "learning": ("conflicting delivery timestamps reach a determination only via an authorized "
                 "adjudicator + independent anchored verification, not the single-source verifier"),
    # ---- the thin-evidence sub-dispute that must resolve UNRESOLVED (no decisive source) ----
    "unresolvable": {
        "claims": [
            {"uri": "claim://deli/u-late", "proposer": "org://deli/customer",
             "statement": "service was delivered late (receipt 16:15).",
             "evidence": ["evidence://deli/u-receipt"]},
            {"uri": "claim://deli/u-on-time", "proposer": "org://deli/company",
             "statement": "service was delivered on time (internal delivery log).",
             "evidence": ["evidence://deli/u-delivery-log"]},
        ],
        "evidence": {
            "u-receipt": {"uri": "evidence://deli/u-receipt", "kind": "TESTIMONY",
                          "source": "customer-signed-receipt",
                          "captured_at": "2026-08-31T16:15:00-06:00",
                          "verity": {"procedure": "signed-receipt", "confidence": 0.7},
                          "reliability": 0.60, "about": "delivery receipt",
                          "supports": "claim://deli/u-late"},
            "u-log": {"uri": "evidence://deli/u-delivery-log", "kind": "RECORD",
                      "source": "company-delivery-log",
                      "captured_at": "2026-08-31T16:05:00-06:00",
                      "verity": {"procedure": "internal-log", "confidence": 0.7},
                      "reliability": 0.70, "about": "delivery log",
                      "supports": "claim://deli/u-on-time"},
        },
        "dispute": {"uri": "dispute://deli/threshold-dispute",
                    "about": "obligation://deli/deliver-due",
                    "parties": ["org://deli/customer", "org://deli/company"],
                    "status": "OPEN", "fin_impact_usd": 18000,
                    "interest_blocks": {"customer": "pay only for delivered service",
                                        "company": "seeks payment for claimed delivery"},
                    "constraint_blocks": {"irreversible": "any award is disputed -> §6 human floor"}},
    },
    "learning_model": {"learning_rate": 0.10, "lo": 0.05, "hi": 0.60,
                       "realized_cost_usd": 6000, "outcome_value": 0.55, "enabled": True},
}


# ==============================================================================================
# B. COVERAGE — a clinical payer/provider/patient dispute (a different org + business model)
# ==============================================================================================
COVE = {
    "label": "cove",
    "scene": "coverage",
    "company_name": "Meridian Health Plan",
    "ledger_name": "db://ledger/adjudication-cove-2026",
    "registrar": "person://cove/utilization",
    "verify": "system://cove/verify",
    "actors": {
        "org://cove/payer": "ORG", "person://cove/patient": "PERSON",
        "person://cove/physician": "PERSON", "person://cove/utilization": "PERSON",
        "person://cove/meddir": "PERSON", "system://cove/verify": "SYSTEM",
    },
    "relationships": {
        "coverage-contract": {"uri": "relationship://cove/coverage-contract",
                              "status": "ACTIVE",
                              "participants": ["org://cove/payer", "person://cove/patient"],
                              "roles": {"org://cove/payer": ["insurer"],
                                        "person://cove/patient": ["member"]},
                              "purpose": "insurance coverage for the member"},
        "clinical": {"uri": "relationship://cove/clinical",
                     "status": "ACTIVE",
                     "participants": ["person://cove/physician", "person://cove/patient"],
                     "roles": {"person://cove/physician": ["provider"],
                               "person://cove/patient": ["patient"]},
                     "purpose": "clinical care relationship"},
    },
    "obligations": {
        "furnish-coverage": {"uri": "obligation://cove/furnish-coverage",
                             "subject": "org://cove/payer", "source": "VOLUNTARILY_UNDERTAKEN",
                             "content": "furnish medically-necessary covered care promptly",
                             "due_by": "2026-12-31T00:00:00-06:00"},
        "standard-care": {"uri": "obligation://cove/standard-care",
                          "subject": "person://cove/physician", "source": "IMPOSED",
                          "content": "recommend clinically-appropriate care",
                          "due_by": "2026-12-31T00:00:00-06:00"},
    },
    "appeal_right": "right://cove/patient-appeal",
    "claimants": ["person://cove/patient"],
    "dispute_about": "obligation://cove/furnish-coverage",
    "dispute": {
        "uri": "dispute://cove/coverage", "about": "obligation://cove/furnish-coverage",
        "parties": ["person://cove/patient", "person://cove/physician", "org://cove/payer"],
        "status": "OPEN", "estimated_cost_usd": 42000,
        "deadline_ref": "utilization review decision within 72 hours (urgent)",
        "interest_blocks": {"patient": "access to the treatment the physician deems necessary",
                            "provider": "deliver clinically-appropriate care",
                            "payer": "pay only for covered/evidence-based care"},
        "constraint_blocks": {"formulary": "off-formulary requires prior authorization",
                              "irreversible": "a dispensed drug is irreversible/unknown-cost to "
                                              "the member; a flat denial is a patient-safety "
                                              "unknown-cost -> §6 human floor on both extremes"},
    },
    "claims": [
        {"uri": "claim://cove/medically-necessary", "proposer": "person://cove/physician",
         "statement": "medication X is medically necessary for this member; a peer-reviewed study "
                      "supports its use for the condition.",
         "evidence": ["evidence://cove/clinical-study"]},
        {"uri": "claim://cove/off-formulary", "proposer": "org://cove/payer",
         "statement": "medication X is off-formulary; the formulary policy and comparative "
                      "step-therapy evidence do not require it as first-line.",
         "evidence": ["evidence://cove/formulary-policy", "evidence://cove/step-therapy-studies"]},
    ],
    "evidence": {
        "clinical": {"uri": "evidence://cove/clinical-study", "kind": "ANCHORED",
                     "source": "peer-reviewed-trial", "captured_at": "2026-06-01T00:00:00-06:00",
                     "verity": {"procedure": "external-trials-database", "confidence": 0.9},
                     "reliability": 0.88, "about": "clinical efficacy for the condition",
                     "supports": "claim://cove/medically-necessary"},
        "formulary": {"uri": "evidence://cove/formulary-policy", "kind": "RECORD",
                      "source": "coverage-policy-document", "captured_at": "2026-01-01T00:00:00-06:00",
                      "verity": {"procedure": "policy-version", "confidence": 1.0},
                      "reliability": 1.0, "about": "coverage/formulary classification",
                      "supports": "claim://cove/off-formulary"},
        "step": {"uri": "evidence://cove/step-therapy-studies", "kind": "ANCHORED",
                 "source": "comparative-effectiveness-db", "captured_at": "2026-05-01T00:00:00-06:00",
                 "verity": {"procedure": "meta-analysis", "confidence": 0.8},
                 "reliability": 0.82, "about": "step-therapy comparator efficacy",
                 "supports": "claim://cove/off-formulary"},
    },
    "weights": {"medical_necessity": 0.40, "safety": 0.25, "policy": 0.20, "cost": 0.15},
    "factor_scores": {
        "authorize-off-formulary": {"medical_necessity": 1.00, "safety": 0.90, "policy": 0.20, "cost": 0.10},
        "deny-off-formulary":      {"medical_necessity": 0.20, "safety": 0.20, "policy": 1.00, "cost": 1.00},
        "step-therapy-first":      {"medical_necessity": 0.80, "safety": 0.85, "policy": 0.70, "cost": 0.70},
        "authorize-generic":       {"medical_necessity": 0.75, "safety": 0.80, "policy": 0.75, "cost": 0.60},
        "request-more-evidence":   {"medical_necessity": 0.50, "safety": 0.60, "policy": 0.50, "cost": 0.60},
        "escalate-to-medical-director": {"medical_necessity": 0.60, "safety": 0.70, "policy": 0.50, "cost": 0.60},
        "unresolved":              {"medical_necessity": 0.50, "safety": 0.50, "policy": 0.50, "cost": 0.50},
        "external-peer-review":    {"medical_necessity": 0.60, "safety": 0.60, "policy": 0.55, "cost": 0.40},
    },
    "options": ["authorize-off-formulary", "deny-off-formulary", "step-therapy-first",
                "authorize-generic", "request-more-evidence", "escalate-to-medical-director",
                "unresolved", "external-peer-review"],
    "floor_gated": {"authorize-off-formulary", "deny-off-formulary"},   # both extremes are §6 floor-gated
    "floor_penalty": 0.20,
    "reconcile": {"rule": "best-reliability-threshold", "threshold": 0.90, "support_floor": 0.55},
    "authority": {"dispute": "authority://cove/adjudicate", "appeal": "authority://cove/adjudicate-appeal",
                  "adjudicator_person": "person://cove/utilization", "appeal_person": "person://cove/meddir"},
    "determination_policy": "adopt-eligible-best",
    "resolution_outcome": "step-therapy-first: member begins on the covered step-therapy with a "
                          "documented re-evaluation if response is inadequate; no off-formulary "
                          "spend triggered immediately",
    "learning": ("drug coverage disputes blend clinical-necessity evidence with policy; the "
                 "measured path (step-therapy-first) preserves member safety + plan policy while "
                 "avoiding both an irreversible off-formulary spend and a flat safety-risk denial"),
    "unresolvable": {
        "claims": [
            {"uri": "claim://cove/u-necessary", "proposer": "person://cove/physician",
             "statement": "medication Y is medically necessary for the rare condition.",
             "evidence": ["evidence://cove/u-anecdotal"]},
            {"uri": "claim://cove/u-unproven", "proposer": "org://cove/payer",
             "statement": "no comparative evidence supports medication Y's use.",
             "evidence": ["evidence://cove/u-no-data"]},
        ],
        "evidence": {
            "u-anecdotal": {"uri": "evidence://cove/u-anecdotal", "kind": "TESTIMONY",
                            "source": "physician-case-report",
                            "captured_at": "2026-07-01T00:00:00-06:00",
                            "verity": {"procedure": "case-report", "confidence": 0.6},
                            "reliability": 0.60, "about": "clinical necessity of medication Y",
                            "supports": "claim://cove/u-necessary"},
            "u-no-data": {"uri": "evidence://cove/u-no-data", "kind": "RECORD",
                          "source": "disease-registry", "captured_at": "2026-07-01T00:00:00-06:00",
                          "verity": {"procedure": "registry-review", "confidence": 0.7},
                          "reliability": 0.70, "about": "absence of comparative evidence",
                          "supports": "claim://cove/u-unproven"},
        },
        "dispute": {"uri": "dispute://cove/rare-condition",
                    "about": "obligation://cove/furnish-coverage",
                    "parties": ["person://cove/patient", "org://cove/payer"],
                    "status": "OPEN", "estimated_cost_usd": 210000,
                    "interest_blocks": {"patient": "access to a potentially life-saving drug",
                                        "payer": "spend only on evidenced care"},
                    "constraint_blocks": {"irreversible": "dispensing is irreversible -> §6 floor"}},
    },
    "learning_model": {"learning_rate": 0.10, "lo": 0.05, "hi": 0.60,
                       "realized_cost_usd": 18000, "outcome_value": 0.70, "enabled": True},
}


# ==============================================================================================
# C. INSPECTION — a goods-QC dispute whose OUTCOME turns on WHICH reconciliation RULE is chosen
# (Sprint-14 proof: config-authorable rule layer). Same economics/options/authority across every
# rule variant; only `reconcile` (the rule + its params) differs between `inspect-best` /
# `inspect-anchor` / `inspect-rec`. A new rule is a registry entry + this org is re-run as a data
# change alone. NOT added to SCENARIOS (driven by run_rule_comparison_demo.py instead) so the
# deli/cove Sprint-13 demo stays byte-identical.
# ==============================================================================================
INSPECT = {
    "label": "inspect",
    "scene": "inspection",
    "company_name": "Vigilant Quality Assurance",
    "ledger_name": "db://ledger/adjudication-inspect-2026",
    "registrar": "person://inspect/registrar",
    "verify": "system://inspect/verify",
    "actors": {
        "org://inspect/buyer": "ORG", "org://inspect/company": "ORG",
        "org://inspect/supplier": "ORG", "person://inspect/registrar": "PERSON",
        "person://inspect/adjudicator": "PERSON", "person://inspect/appeal": "PERSON",
        "system://inspect/verify": "SYSTEM",
    },
    "relationships": {
        "qc-contract": {"uri": "relationship://inspect/qc-contract", "status": "ACTIVE",
                        "participants": ["org://inspect/buyer", "org://inspect/company"],
                        "roles": {"org://inspect/buyer": ["client"],
                                  "org://inspect/company": ["inspector"]},
                        "purpose": "independent batch inspection + acceptance decision"},
        "supply-contract": {"uri": "relationship://inspect/supply-contract", "status": "ACTIVE",
                            "participants": ["org://inspect/supplier", "org://inspect/buyer"],
                            "roles": {"org://inspect/supplier": ["supplier"],
                                      "org://inspect/buyer": ["receiver"]},
                            "purpose": "goods supply subject to QC acceptance"},
    },
    "obligations": {
        "inspect-due": {"uri": "obligation://inspect/inspect-due", "subject": "org://inspect/company",
                        "source": "VOLUNTARILY_UNDERTAKEN",
                        "content": "declare pass/fail on the batch by the acceptance deadline",
                        "due_by": "2026-10-15T00:00:00-06:00"},
        "accept-due": {"uri": "obligation://inspect/accept-due", "subject": "org://inspect/buyer",
                       "source": "VOLUNTARILY_UNDERTAKEN",
                       "content": "accept a conforming batch and pay upon acceptance",
                       "due_by": "2026-11-30T00:00:00-06:00"},
    },
    "appeal_right": "right://inspect/buyer-appeal",
    "claimants": ["org://inspect/buyer"],
    "dispute_about": "obligation://inspect/inspect-due",
    "dispute": {
        "uri": "dispute://inspect/inspection", "about": "obligation://inspect/inspect-due",
        "parties": ["org://inspect/buyer", "org://inspect/company", "org://inspect/supplier"],
        "status": "OPEN", "fin_impact_usd": 54000,
        "deadline_ref": "QC acceptance decision within 10 business days",
        "interest_blocks": {"buyer": "take only a conforming batch; avoid a defective line",
                            "company": "protect its inspection reputation; bill only for passed work",
                            "supplier": "not blamed for a batch the inspection cleared"},
        "constraint_blocks": {"irreversible": "rejecting/returning the whole batch is irreversible/"
                              "unknown-cost -> §6 floor; accepting an unproven defective line is an "
                              "unknown-cost roll-out risk -> §6 floor"},
    },
    "claims": [
        {"uri": "claim://inspect/passed", "proposer": "org://inspect/company",
         "statement": "the batch passed QC inspection; an automated machine pass signal and an "
                      "independent process audit support acceptance.",
         "evidence": ["evidence://inspect/proof-system", "evidence://inspect/proof-audit"]},
        {"uri": "claim://inspect/failed", "proposer": "org://inspect/buyer",
         "statement": "the batch failed inspection; a resident inspector's signed finding records a "
                      "defect, and accepting on stale audit records would be unsafe.",
         "evidence": ["evidence://inspect/fail-inspector"]},
    ],
    "evidence": {
        "proof-system": {"uri": "evidence://inspect/proof-system", "kind": "ANCHORED",
                         "source": "automated-inspection-livestate",
                         "captured_at": "2026-08-29T10:00:00-06:00",
                         "verity": {"procedure": "machine-inspection-log", "confidence": 0.84},
                         "reliability": 0.84, "about": "automated pass signal",
                         "supports": "claim://inspect/passed"},
        "proof-audit": {"uri": "evidence://inspect/proof-audit", "kind": "RECORD",
                        "source": "annual-auditor-sign-off",
                        "captured_at": "2026-07-10T09:00:00-06:00",
                        "verity": {"procedure": "independent-audit", "confidence": 0.97},
                        "reliability": 0.97, "about": "auditor sign-off on the inspection process",
                        "supports": "claim://inspect/passed"},
        "fail-inspector": {"uri": "evidence://inspect/fail-inspector", "kind": "TESTIMONY",
                           "source": "resident-inspector-testimony",
                           "captured_at": "2026-08-30T14:00:00-06:00",
                           "verity": {"procedure": "signed-inspection-note", "confidence": 0.90},
                           "reliability": 0.90, "about": "resident inspector's defect finding",
                           "supports": "claim://inspect/failed"},
    },
    "weights": {"evidence_compliance": 0.35, "cost": 0.25, "relationship": 0.20, "schedule": 0.20},
    "factor_scores": {
        "accept-batch":                    {"evidence_compliance": 1.00, "cost": 0.90, "relationship": 0.30, "schedule": 0.40},
        "reject-batch-return":            {"evidence_compliance": 0.30, "cost": 0.10, "relationship": 0.20, "schedule": 0.50},
        "rework-partial-credit":          {"evidence_compliance": 0.80, "cost": 0.50, "relationship": 0.70, "schedule": 0.50},
        "conditional-accept-with-guarantee": {"evidence_compliance": 0.70, "cost": 0.50, "relationship": 0.60, "schedule": 0.60},
        "request-more-evidence":          {"evidence_compliance": 0.40, "cost": 0.50, "relationship": 0.50, "schedule": 0.50},
        "escalate":                       {"evidence_compliance": 0.50, "cost": 0.30, "relationship": 0.40, "schedule": 0.40},
        "unresolved":                     {"evidence_compliance": 0.50, "cost": 0.50, "relationship": 0.50, "schedule": 0.50},
    },
    "options": ["accept-batch", "reject-batch-return", "rework-partial-credit",
                "conditional-accept-with-guarantee", "request-more-evidence", "escalate", "unresolved"],
    "floor_gated": {"accept-batch", "reject-batch-return"},   # both extremes are §6 human-floor gated
    "floor_penalty": 0.20,
    # NOTE: `reconcile` is overridden per-variant (see inspect_variant below) — this is the field
    # the config-authorable rule layer makes user-selected.
    "reconcile": {"rule": "best-reliability-threshold", "threshold": 0.92, "support_floor": 0.55},
    "authority": {"dispute": "authority://inspect/adjudicate", "appeal": "authority://inspect/adjudicate-appeal",
                  "adjudicator_person": "person://inspect/adjudicator", "appeal_person": "person://inspect/appeal"},
    "determination_policy": "adopt-eligible-best",
    "resolution_outcome": ("rework-partial-credit: the buyer keeps the batch pending corrective "
                           "rework and a documented partial credit to the supplier; neither a full "
                           "rejection nor blanket acceptance is auto-permitted (§6 floor)"),
    "learning": ("reliability alone is ambiguous here (fails only if the reconciliation rule admits "
                 "the resident testimony vs demands anchored-only vs recency-decays the old audit); "
                 "the adjudicator must state which rule the determination is reached under"),
}


# --- Sprint 14: the SAME org, a DIFFERENT chosen reconciliation rule (config data only) ---------
def inspect_variant(label: str, reconcile: dict) -> dict:
    """Return INSPECT with a new label (for clean, per-rule fixtures) and a new reconcile block.
    EVERYTHING else is identical to INSPECT — this is the proof that a rule choice changes the
    outcome with zero engine-side change: only data differs."""
    v = dict(INSPECT); v["label"] = label
    for k in ("actors", "relationships", "obligations", "claims", "evidence", "dispute",
              "factor_scores", "options", "floor_gated"):
        v[k] = INSPECT[k]
    v["reconcile"] = reconcile
    return v


INSPECT_BEST = inspect_variant("inspect-best",
    {"rule": "best-reliability-threshold", "threshold": 0.92, "support_floor": 0.55})
INSPECT_ANCHOR = inspect_variant("inspect-anchor",
    {"rule": "strict-anchor-only", "params": {"kinds": ["ANCHORED"],
                                              "threshold": 0.92, "support_floor": 0.55}})
INSPECT_RECENCY = inspect_variant("inspect-rec",
    {"rule": "recency-weighted-threshold",
     "params": {"as_of": "2026-08-31T12:00:00-06:00", "half_life_days": 21,
                "threshold": 0.92, "support_floor": 0.55}})

RULE_VARIANTS = [INSPECT_BEST, INSPECT_ANCHOR, INSPECT_RECENCY]


# --- Sprint 15: rules authored ENTIRELY as a declarative rule-spec (config TEXT, no engine fn) ----
# A `reconcile` block may carry `rule_spec` (a rule declared as data) instead of a registry `rule`
# name. `inspect-anchor-spec` / `inspect-rec-spec` re-express the registry behaviors
# (`strict-anchor-only`, `recency-weighted-threshold`) as specs to prove a spec is the SAME engine,
# not a different one (parity). `inspect-majority` is a GENUINELY NEW spec-only rule
# (`majority-of-sources`) that was never a registry function: a claim is supported only to the
# fraction of its admissible sources whose individual reliability clears `source_threshold` — a
# corroboration-by-many-independent-sources semantics instead of "one star witness suffices". It enters the system purely
# as this config dict — zero new engine Python for it.
def inspect_spec_variant(label: str, spec: dict, extra_reconcile: dict) -> dict:
    v = dict(INSPECT); v["label"] = label
    for k in ("actors", "relationships", "obligations", "claims", "evidence", "dispute",
              "factor_scores", "options", "floor_gated"):
        v[k] = INSPECT[k]
    rc = {"rule_spec": spec}; rc.update(extra_reconcile)
    v["reconcile"] = rc
    return v

SPEC_ANCHOR_SPEC = inspect_spec_variant("inspect-anchor-spec",
    {"name": "strict-anchor-only", "aggregate": "max", "value_field": "reliability",
     "admissible_kinds": ["ANCHORED"]},
    {"threshold": 0.92, "support_floor": 0.55})
SPEC_REC_SPEC = inspect_spec_variant("inspect-rec-spec",
    {"name": "recency-weighted-threshold", "aggregate": "max", "value_field": "reliability",
     "decay": {"as_of": "2026-08-31T12:00:00-06:00", "half_life_days": 21}},
    {"threshold": 0.92, "support_floor": 0.55})
SPEC_MAJORITY_SPEC = inspect_spec_variant("inspect-majority",
    {"name": "majority-of-sources", "aggregate": "majority", "value_field": "reliability",
     "admissible_kinds": None, "source_threshold": 0.92},
    {"threshold": 0.92, "support_floor": 0.55})

SPEC_AUTHORED_RULES = [SPEC_ANCHOR_SPEC, SPEC_REC_SPEC, SPEC_MAJORITY_SPEC]


# ==============================================================================================
# E. SPRINT 16 — the RULE LIBRARY: named rule specs defined ONCE, reused by reference by ANY org.
# Each entry is a declarative `rule_spec` dict exactly as the engine accepts. An org reuses a
# library rule by name: `reconcile = {"rule_spec": RULE_LIBRARY["<name>"], threshold, support_floor}`.
# This is the proof the DSL is a real cross-org language, not inspect-only: the SAME dict object is
# shared by several orgs, and a new primitive (`bayesian-combine`) is authored once here and then
# usable as data by every org.
# ==============================================================================================
RULE_LIBRARY = {
    "strict-anchor-only": {
        "name": "strict-anchor-only", "aggregate": "max", "value_field": "reliability",
        "admissible_kinds": ["ANCHORED"]},
    "recency-weighted-threshold": {
        "name": "recency-weighted-threshold", "aggregate": "max", "value_field": "reliability",
        "decay": {"as_of": "2026-08-31T12:00:00-06:00", "half_life_days": 21}},
    "majority-of-sources": {
        "name": "majority-of-sources", "aggregate": "majority", "value_field": "reliability",
        "admissible_kinds": None, "source_threshold": 0.92},
    # the genuinely NEW Sprint-16 primitive as a library rule: a claim's support is the Bayesian
    # posterior of its admissible source values (each an independent likelihood) against an
    # explicit authoring `prior`. Many weak-but-independent sources can exceed ANY single strong
    # one — the corroboration-synthesis semantics `max` can never express.
    "independent-corroboration": {
        "name": "independent-corroboration", "aggregate": "bayesian-combine",
        "value_field": "reliability", "admissible_kinds": None, "prior": 0.6},
}


def org_under_library_rule(cfg: dict, label: str, rule_name: str, params: dict) -> dict:
    """Return a copy of `cfg` under a NEW label whose `reconcile` reuses the NAMED RULE_LIBRARY
    spec (the SAME shared dict) plus flat threshold/support_floor params. Everything else is the
    org's own data — only the rule differs. deli/cove original configs are untouched."""
    v = dict(cfg); v["label"] = label
    for k in ("actors", "relationships", "obligations", "claims", "evidence", "dispute",
              "factor_scores", "options", "floor_gated"):
        v[k] = cfg[k]
    v["reconcile"] = {"rule_spec": RULE_LIBRARY[rule_name]}
    v["reconcile"].update(params)
    return v

# --- Sprint 16 library-reuse org variants (cross-org rule reuse; new labels only) ---------------
# `majority-of-sources` on a SECOND, genuinely different org (freight) — not just inspect.
DELI_MAJORITY = org_under_library_rule(
    DELI, "deli-majority", "majority-of-sources", {"threshold": 0.92, "support_floor": 0.55})
# The NEW `independent-corroboration` (bayesian-combine) on inspect at reconcile threshold 0.98:
# single-source max (0.97) clears nothing -> UNRESOLVED; the two weak independent witnesses
# (0.84 anchored + 0.97 record) combine to a posterior ~0.9961 that DOES clear 0.98 -> DETERMINED.
# That is exactly what `max` cannot do, and the verdict flip the new primitive produces.
INSPECT_CORROBORATION = org_under_library_rule(
    INSPECT, "inspect-corroboration", "independent-corroboration",
    {"threshold": 0.98, "support_floor": 0.55})
# The SAME new library rule usable as data by a genuinely different second org (clinical).
COVE_CORROBORATION = org_under_library_rule(
    COVE, "cove-corroboration", "independent-corroboration", {"threshold": 0.90, "support_floor": 0.55})

LIBRARY_REUSE = [DELI_MAJORITY, INSPECT_CORROBORATION, COVE_CORROBORATION]


SCENARIOS = [DELI, COVE]


# ==============================================================================================
# F. SPRINT 17 — distinct batch disputes on the SAME goods-QC org, for the reconcile-LEARNING
# step. Two genuinely DIFFERENT predicate sets (batch alpha = the LEARNING episode whose realized
# outcome recalibrates the reconcile threshold; batch beta = the SECOND, future dispute re-driven
# under the learned rule). Same org economics/options/weights/authority as INSPECT; only the
# dispute + claims + evidence + label differ (the generic engine, data-only). Also the cross-org
# reuse target (`deli-learn`).
# ==============================================================================================
def inspect_batch(label: str, dispute_uri: str, claims, evidence, resolution_outcome) -> dict:
    """Clone INSPECT under a new label + a DIFFERENT dispute/claims/evidence (a distinct batch:
    a genuinely different predicate set, NOT a re-run of the same case). Everything else — actors,
    relationships, obligations, economics, options, weights, factor_scores, floor_gated, authority,
    the default reconcile — is reused from INSPECT unchanged."""
    v = dict(INSPECT); v["label"] = label
    for k in ("actors", "relationships", "obligations", "factor_scores", "options", "floor_gated",
              "weights"):
        v[k] = INSPECT[k]
    v["dispute"] = dict(INSPECT["dispute"]); v["dispute"]["uri"] = dispute_uri
    v["dispute_about"] = INSPECT["dispute_about"]; v["appeal_right"] = INSPECT["appeal_right"]
    v["claims"] = list(claims); v["evidence"] = dict(evidence)
    v["resolution_outcome"] = resolution_outcome
    # a thin-evidence sub-dispute for the `unresolved` variant (never driven here; structurally
    # valid so the field exists — built fresh, never mutates any shared config).
    base_name = dispute_uri.rsplit("/")[-1]
    u_claims = []
    for c in list(claims):
        uc = dict(c); uc["uri"] = "claim://%s/u-%s" % (label, c["uri"].rsplit("/")[-1])
        uc["evidence"] = ["evidence://%s/u-%s" % (label, e.rsplit("/")[-1]) for e in c["evidence"]]
        u_claims.append(uc)
    u_ev = {e["uri"].rsplit("/")[-1]: dict(e) for e in evidence.values()}
    for k, e in u_ev.items():
        e["uri"] = "evidence://%s/u-%s" % (label, e["uri"].rsplit("/")[-1])
        e["supports"] = "claim://%s/u-%s" % (label, e["supports"].rsplit("/")[-1])
    v["unresolvable"] = {"claims": u_claims, "evidence": u_ev,
                         "dispute": {"uri": "dispute://%s/u-%s" % (label, base_name),
                                     "about": dispute_uri.rsplit("/", 1)[0] + "/" + base_name,
                                     "parties": list(INSPECT["dispute"]["parties"]),
                                     "status": "OPEN",
                                     "constraint_blocks": dict(INSPECT["dispute"].get("constraint_blocks", {}))}}
    return v


CONF_LABEL_A = "inspect-learn-a"
CONF_LABEL_B = "inspect-learn-b"

INSPECT_BATCH_A = inspect_batch(
    CONF_LABEL_A,
    "dispute://inspect-la/batch-alpha",
    [
        {"uri": "claim://inspect-la/passed", "proposer": "org://inspect/company",
         "statement": "batch alpha passed QC inspection; the automated machine pass signal and an "
                      "independent auditor's sign-off both support acceptance.",
         "evidence": ["evidence://inspect-la/machine-pass", "evidence://inspect-la/audit-signoff"]},
        {"uri": "claim://inspect-la/failed", "proposer": "org://inspect/buyer",
         "statement": "batch alpha failed inspection; a resident inspector's signed note records a "
                      "defect.",
         "evidence": ["evidence://inspect-la/resident-note"]},
    ],
    {
        "machine-pass": {"uri": "evidence://inspect-la/machine-pass", "kind": "ANCHORED",
                         "source": "automated-inspection-livestate",
                         "captured_at": "2026-08-29T10:00:00-06:00",
                         "verity": {"procedure": "machine-inspection-log", "confidence": 0.85},
                         "reliability": 0.92, "about": "automated pass signal for batch alpha",
                         "supports": "claim://inspect-la/passed"},
        "audit-signoff": {"uri": "evidence://inspect-la/audit-signoff", "kind": "RECORD",
                          "source": "annual-auditor-sign-off",
                          "captured_at": "2026-07-10T09:00:00-06:00",
                          "verity": {"procedure": "independent-audit", "confidence": 0.95},
                          "reliability": 0.97, "about": "auditor sign-off on batch alpha",
                          "supports": "claim://inspect-la/passed"},
        "resident-note": {"uri": "evidence://inspect-la/resident-note", "kind": "TESTIMONY",
                          "source": "resident-inspector-testimony",
                          "captured_at": "2026-08-30T14:00:00-06:00",
                          "verity": {"procedure": "signed-inspection-note", "confidence": 0.90},
                          "reliability": 0.90, "about": "resident inspector's defect finding",
                          "supports": "claim://inspect-la/failed"},
    },
    "batch alpha accepted with a documented partial rework; the determination held at a realized "
    "value of 0.90 (a 10% rework), which is BELOW the reconcile threshold it was driven under.",
)

INSPECT_BATCH_B = inspect_batch(
    CONF_LABEL_B,
    "dispute://inspect-lb/batch-beta",
    [
        {"uri": "claim://inspect-lb/passed", "proposer": "org://inspect/company",
         "statement": "batch beta passed QC inspection; the automated machine pass signal supports "
                      "acceptance.",
         "evidence": ["evidence://inspect-lb/beta-machine-pass"]},
        {"uri": "claim://inspect-lb/failed", "proposer": "org://inspect/buyer",
         "statement": "batch beta failed inspection; a resident inspector's note records a defect.",
         "evidence": ["evidence://inspect-lb/beta-resident-note"]},
    ],
    {
        "beta-machine-pass": {"uri": "evidence://inspect-lb/beta-machine-pass", "kind": "ANCHORED",
                              "source": "automated-inspection-livestate",
                              "captured_at": "2026-09-02T10:00:00-06:00",
                              "verity": {"procedure": "machine-inspection-log", "confidence": 0.84},
                              "reliability": 0.93, "about": "automated pass signal for batch beta",
                              "supports": "claim://inspect-lb/passed"},
        "beta-resident-note": {"uri": "evidence://inspect-lb/beta-resident-note", "kind": "TESTIMONY",
                               "source": "resident-inspector-testimony",
                               "captured_at": "2026-09-03T14:00:00-06:00",
                               "verity": {"procedure": "signed-inspection-note", "confidence": 0.88},
                               "reliability": 0.88, "about": "resident inspector's defect finding",
                               "supports": "claim://inspect-lb/failed"},
    },
    "batch beta accepted (winning claim support 0.93) — resolvable ONLY under a reconcile "
    "threshold that the learning episode's realized outcome recalibrated below 0.95.",
)

INSPECT_BATCHES = [INSPECT_BATCH_A, INSPECT_BATCH_B]

# The deterministic, clamp-bounded hyper-parameters of the reconcile-learning step (data, not code).
LEARN_HYPER = {"learning_rate": 0.8, "threshold_lo": 0.55, "threshold_hi": 0.95, "eps": 1e-6,
               "realized_value_a": 0.90, "initial_threshold": 0.95}

# Both batch episodes are driven under the INITIAL reconcile threshold (0.95) — the rule whose
# parameter the learning step recalibrates from episode A's realized outcome. Episode B's lifecycle
# is then re-driven (in the runner) under the LEARNED threshold; the config baseline here is the
# honest 0.95 so the old-rule-vs-learned flip is shown on the SAME evidence.
INITIAL_RECONCILE = {"rule": "best-reliability-threshold", "threshold": 0.95, "support_floor": 0.55}
INSPECT_BATCH_A["reconcile"] = dict(INITIAL_RECONCILE)
INSPECT_BATCH_B["reconcile"] = dict(INITIAL_RECONCILE)