# §7L Q1–Q10 morning cockpit — engine-native render (Sprint 19)
generated 2026-09-01T06:22:47Z  |  all ten questions reported BY `adjudication_engine.cockpit_s7l`/`render_cockpit_s7l`  |  SPEC v0.22, 49 $defs, URI cap

The complete §7L morning test is now a data-only engine render: for ANY generically-driven org the engine answers Q1–Q10 from the org's own graph/ledger/config (Q7/Q8 delegate to the Sprint-18 line by construction). Q6 is honest — it never fabricates a forecast (no recorded realized-vs-expected series -> "cannot forecast from recorded data").

```
# §7L Q1–Q10 cockpit (engine-native) — org deli
ACTIVE reconcile rule: best-reliability-threshold  |  source: registry  |  learned-this-run: False  |  why: unchanged
Q1. what happened?  state/events: 14 recorded events; dispute lifecycle OPEN->EVIDENCE_COLLECTION->CONTESTED->ADJUDICATION->RESOLUTION->ACCEPTED->EXECUTED->VERIFIED->CLOSED; status=RESOLVED lifecycle=CLOSED epistemic=RESOLVED_DETERMINED
Q2. what changed?  life cycle OPEN -> CLOSED; epistemic UNDETERMINED -> RESOLVED_DETERMINED; determination=partial-settlement; claim epistemic={'late': 'disputed', 'delivered': 'disputed', 'shipped': 'disputed'}; significance=determined
Q3. what matters?  prioritized attention (2): claim://deli/late — claim disputed (not DETERMINED); claim://deli/shipped — claim disputed (not DETERMINED)
Q4. what is going wrong?  exceptions (0): none  |  reconcile conflict=True uncertainty=False
Q5. why is it going wrong?  root-cause [epistemic status]: late support=0.9 contested (not determined); delivered support=0.97 support-carrying (DETERMINED under the active rule); shipped support=0.92 contested (not determined)  |  under rule best-reliability-threshold (registry)
Q6. what if we do nothing?  cannot forecast from recorded data (no recorded realized-vs-expected series)
Q7. what are our options?  accept-customer-refund, accept-company-full-payment, partial-settlement, conditional-resolution, request-more-evidence, escalate, unresolved, external-adjudication  |  baseline unresolved  |  machine-eligible best: partial-settlement
Q8. what should we do?  recommendation partial-settlement (authority authority://deli/adjudicate; floor-gated ['accept-customer-refund'])  ->  determination partial-settlement
Q9. who does it, authority/capacity?  adjudicator person://deli/adjudicator (authority authority://deli/adjudicate), obligated party org://deli/company, appeal authority://deli/adjudicate-appeal, actors 7
Q10. did it work, what did we learn?  verified=True status=RESOLVED determination=partial-settlement; outcome=partial settlement on the contested delivery; SLA-breach credit applied; ledger noted; customer keeps the service; learning: evidence://deli/learning-note[conflicting delivery timestamps reach a determination only v…]
```

```
# §7L Q1–Q10 cockpit (engine-native) — org inspect-corroboration
ACTIVE reconcile rule: independent-corroboration  |  source: rule-library  |  learned-this-run: False  |  why: unchanged
Q1. what happened?  state/events: 13 recorded events; dispute lifecycle OPEN->EVIDENCE_COLLECTION->CONTESTED->ADJUDICATION->RESOLUTION->ACCEPTED->EXECUTED->VERIFIED->CLOSED; status=RESOLVED lifecycle=CLOSED epistemic=RESOLVED_DETERMINED
Q2. what changed?  life cycle OPEN -> CLOSED; epistemic UNDETERMINED -> RESOLVED_DETERMINED; determination=rework-partial-credit; claim epistemic={'passed': 'disputed', 'failed': 'disputed'}; significance=determined
Q3. what matters?  prioritized attention (1): claim://inspect/failed — claim disputed (not DETERMINED)
Q4. what is going wrong?  exceptions (0): none  |  reconcile conflict=True uncertainty=False
Q5. why is it going wrong?  root-cause [epistemic status]: passed support=0.9961 support-carrying (DETERMINED under the active rule); failed support=0.931 contested (not determined)  |  under rule independent-corroboration (rule-library)
Q6. what if we do nothing?  cannot forecast from recorded data (no recorded realized-vs-expected series)
Q7. what are our options?  accept-batch, reject-batch-return, rework-partial-credit, conditional-accept-with-guarantee, request-more-evidence, escalate, unresolved  |  baseline unresolved  |  machine-eligible best: rework-partial-credit
Q8. what should we do?  recommendation rework-partial-credit (authority authority://inspect/adjudicate; floor-gated ['accept-batch', 'reject-batch-return'])  ->  determination rework-partial-credit
Q9. who does it, authority/capacity?  adjudicator person://inspect/adjudicator (authority authority://inspect/adjudicate), obligated party org://inspect/company, appeal authority://inspect/adjudicate-appeal, actors 7
Q10. did it work, what did we learn?  verified=True status=RESOLVED determination=rework-partial-credit; outcome=rework-partial-credit: the buyer keeps the batch pending corrective rework and a documented partial credit to the supplier; neither a full rejection nor blanket acceptance is auto-permitted (§6 floor); learning: evidence://inspect-corroboration/learning-note[reliability alone is ambiguous here (fails only if the recon…]
```

```
# §7L Q1–Q10 cockpit (engine-native) — org inspect-learn-b
ACTIVE reconcile rule: calibrated-threshold-091  |  source: learned  |  learned-this-run: True  |  why: reconcile threshold recalibrated lowered (relaxed: the bar demanded more than realized determinations held): prior 0.950 -> 0.910 from a realized outcome value 0.900 (variance signal -0.040, learning_rate 0.8), clamp-bounded to [0.55, 0.95]
Q1. what happened?  state/events: 14 recorded events; dispute lifecycle OPEN->EVIDENCE_COLLECTION->CONTESTED->ADJUDICATION->RESOLUTION->ACCEPTED->EXECUTED->VERIFIED->CLOSED; status=RESOLVED lifecycle=CLOSED epistemic=RESOLVED_DETERMINED
Q2. what changed?  life cycle OPEN -> CLOSED; epistemic UNDETERMINED -> RESOLVED_DETERMINED; determination=rework-partial-credit; claim epistemic={'passed': 'disputed', 'failed': 'disputed'}; significance=determined
Q3. what matters?  prioritized attention (1): claim://inspect-lb/failed — claim disputed (not DETERMINED)
Q4. what is going wrong?  exceptions (0): none  |  reconcile conflict=True uncertainty=False
Q5. why is it going wrong?  root-cause [epistemic status]: passed support=0.93 support-carrying (DETERMINED under the active rule); failed support=0.88 contested (not determined)  |  under rule calibrated-threshold-091 (learned)
Q6. what if we do nothing?  cannot forecast from recorded data (no recorded realized-vs-expected series)
Q7. what are our options?  accept-batch, reject-batch-return, rework-partial-credit, conditional-accept-with-guarantee, request-more-evidence, escalate, unresolved  |  baseline unresolved  |  machine-eligible best: rework-partial-credit
Q8. what should we do?  recommendation rework-partial-credit (authority authority://inspect/adjudicate; floor-gated ['accept-batch', 'reject-batch-return'])  ->  determination rework-partial-credit
Q9. who does it, authority/capacity?  adjudicator person://inspect/adjudicator (authority authority://inspect/adjudicate), obligated party org://inspect/company, appeal authority://inspect/adjudicate-appeal, actors 7
Q10. did it work, what did we learn?  verified=True status=RESOLVED determination=rework-partial-credit; outcome=batch beta accepted (winning claim support 0.93) — resolvable ONLY under a reconcile threshold that the learning episode's realized outcome recalibrated below 0.95.; learning: evidence://inspect-learn-b/learning-note[reliability alone is ambiguous here (fails only if the recon…]; decision://inspect-learn-b/reconcile-learning[the reconcile threshold is recalibrated toward the realized …]
```

```
# §7L Q1–Q10 cockpit (engine-native) — org deli-learn
ACTIVE reconcile rule: calibrated-threshold-091  |  source: learned  |  learned-this-run: False  |  why: unchanged
Q1. what happened?  state/events: 14 recorded events; dispute lifecycle OPEN->EVIDENCE_COLLECTION->CONTESTED->ADJUDICATION->RESOLUTION->ACCEPTED->EXECUTED->VERIFIED->CLOSED; status=RESOLVED lifecycle=CLOSED epistemic=RESOLVED_DETERMINED
Q2. what changed?  life cycle OPEN -> CLOSED; epistemic UNDETERMINED -> RESOLVED_DETERMINED; determination=partial-settlement; claim epistemic={'late': 'disputed', 'delivered': 'disputed', 'shipped': 'disputed'}; significance=determined
Q3. what matters?  prioritized attention (1): claim://deli/late — claim disputed (not DETERMINED)
Q4. what is going wrong?  exceptions (0): none  |  reconcile conflict=True uncertainty=False
Q5. why is it going wrong?  root-cause [epistemic status]: late support=0.9 contested (not determined); delivered support=0.97 support-carrying (DETERMINED under the active rule); shipped support=0.92 support-carrying (DETERMINED under the active rule)  |  under rule calibrated-threshold-091 (learned)
Q6. what if we do nothing?  cannot forecast from recorded data (no recorded realized-vs-expected series)
Q7. what are our options?  accept-customer-refund, accept-company-full-payment, partial-settlement, conditional-resolution, request-more-evidence, escalate, unresolved, external-adjudication  |  baseline unresolved  |  machine-eligible best: partial-settlement
Q8. what should we do?  recommendation partial-settlement (authority authority://deli/adjudicate; floor-gated ['accept-customer-refund'])  ->  determination partial-settlement
Q9. who does it, authority/capacity?  adjudicator person://deli/adjudicator (authority authority://deli/adjudicate), obligated party org://deli/company, appeal authority://deli/adjudicate-appeal, actors 7
Q10. did it work, what did we learn?  verified=True status=RESOLVED determination=partial-settlement; outcome=partial settlement on the contested delivery; SLA-breach credit applied; ledger noted; customer keeps the service; learning: evidence://deli-learn/learning-note[conflicting delivery timestamps reach a determination only v…]
```

## §16 verdict

**The §7L gate is met at the engine-render level.** The ten morning questions are now answered by `adjudication_engine.cockpit_s7l` with recorded-data evidence for any configured org, data-only; #8 (Q8's recommendation) is machine-eligible-best, §6-floor-gated, carries the authority it requires, and the determination is the §6 human's call that closes in a verified, learned outcome (Q10). The honest limits: Q6 cannot forecast on these orgs because no realized-vs-expected series is recorded (it says so plainly); Q9 capability is the holder-of-authority assignment, not a dynamic capacity model; and the cockpit reports the recorded state — it does not manufacture certainty where the evidence is UNRESOLVED.

_Additive; frozen ontology, SPEC v0.22, 49 $defs. Trust only moved by S5._
