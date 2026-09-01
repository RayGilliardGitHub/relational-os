# §7L directional forecast → attention → expected-impact — engine-native render (Sprint 22)
generated 2026-09-01T06:22:47Z  |  `adjudication_engine.cockpit_s7l`/`render_cockpit_s7l`  |  recorded `metric://` series + recorded `direction` (default `higher-is-better`) + recorded threshold -> Q3 forecast attention + Q8 do-nothing expected-impact, BOTH directions  |  SPEC v0.22, 49 $defs, URI cap

The forecast→attention→expected-impact closure now serves BOTH directions as data: a recorded metric's `direction` (default `higher-is-better` for rate/quality = min below threshold; explicit `lower-is-better` for cost/latency/defect/risk = max above ceiling) decides which crossing flags a Q3 forecast attention item and how the Q8/trade-off prices the do-nothing baseline (below-target vs above-ceiling). An org without a recorded series keeps today's Q3/Q8/trade-off exactly.

--- deli-forecast ---
```
# §7L Q1–Q10 cockpit (engine-native) — org deli-forecast
ACTIVE reconcile rule: best-reliability-threshold  |  source: registry  |  learned-this-run: False  |  why: unchanged
Q1. what happened?  state/events: 15 recorded events; dispute lifecycle OPEN->EVIDENCE_COLLECTION->CONTESTED->ADJUDICATION->RESOLUTION->ACCEPTED->EXECUTED->VERIFIED->CLOSED; status=RESOLVED lifecycle=CLOSED epistemic=RESOLVED_DETERMINED
Q2. what changed?  life cycle OPEN -> CLOSED; epistemic UNDETERMINED -> RESOLVED_DETERMINED; determination=partial-settlement; claim epistemic={'late': 'disputed', 'delivered': 'disputed', 'shipped': 'disputed'}; significance=determined
Q3. what matters?  prioritized attention (3): claim://deli-forecast/late — claim disputed (not DETERMINED); claim://deli-forecast/shipped — claim disputed (not DETERMINED); metric://deli-forecast/m-on-time [forecast] — forecast: projected to fall below 0.95 (target) — worst 0.8 at period 3 — recorded band 0.71…0.89 (± σ 0.09); worst side 0.71 below target 0.95 — horizon-wide recorded band 0.71…0.93 across 3 projection periods (band_periods/band_horizon, same recorded σ)
Q4. what is going wrong?  exceptions (0): none  |  reconcile conflict=True uncertainty=False
Q5. why is it going wrong?  root-cause [epistemic status]: late support=0.9 contested (not determined); delivered support=0.97 support-carrying (DETERMINED under the active rule); shipped support=0.92 contested (not determined)  |  under rule best-reliability-threshold (registry)
Q6. what if we do nothing?  project (holding the recorded trend) from last actual 0.86 + mean delta -0.02: period 1 -> 0.84; period 2 -> 0.82; period 3 -> 0.8  |  recorded variance -0.09
Q7. what are our options?  accept-customer-refund, accept-company-full-payment, partial-settlement, conditional-resolution, request-more-evidence, escalate, unresolved, external-adjudication  |  baseline unresolved  |  machine-eligible best: partial-settlement
Q8. what should we do?  recommendation partial-settlement (authority authority://deli-forecast/adjudicate; floor-gated ['accept-customer-refund'])  ->  determination partial-settlement
    trade-off / do-nothing expected-impact: forecast-driven do-nothing cost: metric://deli-forecast/m-on-time projects to worst 0.8 (period 3) below recorded target 0.95 by 0.15 — doing nothing lets the recorded trend deteriorate — recorded band 0.71…0.89 (± σ 0.09); worst side 0.71 below target 0.95 — the whole recorded spread is priced as bad — horizon-wide recorded band 0.71…0.93 across 3 projection periods (band_periods/band_horizon, same recorded σ) (baseline unresolved, priced=True, on-target=False) |  recorded band 0.71…0.89 (± σ 0.09, crosses=True)
Q9. who does it, authority/capacity?  adjudicator person://deli-forecast/adjudicator (authority authority://deli-forecast/adjudicate), obligated party org://deli-forecast/company, appeal authority://deli-forecast/adjudicate-appeal, actors 7
Q10. did it work, what did we learn?  verified=True status=RESOLVED determination=partial-settlement; outcome=partial settlement on the contested delivery; SLA-breach credit applied; ledger noted; customer keeps the service; learning: evidence://deli-forecast/learning-note[conflicting delivery timestamps reach a determination only v…]
```

--- deli-forecast-flat ---
```
# §7L Q1–Q10 cockpit (engine-native) — org deli-forecast-flat
ACTIVE reconcile rule: best-reliability-threshold  |  source: registry  |  learned-this-run: False  |  why: unchanged
Q1. what happened?  state/events: 15 recorded events; dispute lifecycle OPEN->EVIDENCE_COLLECTION->CONTESTED->ADJUDICATION->RESOLUTION->ACCEPTED->EXECUTED->VERIFIED->CLOSED; status=RESOLVED lifecycle=CLOSED epistemic=RESOLVED_DETERMINED
Q2. what changed?  life cycle OPEN -> CLOSED; epistemic UNDETERMINED -> RESOLVED_DETERMINED; determination=partial-settlement; claim epistemic={'late': 'disputed', 'delivered': 'disputed', 'shipped': 'disputed'}; significance=determined
Q3. what matters?  prioritized attention (2): claim://deli-forecast-flat/late — claim disputed (not DETERMINED); claim://deli-forecast-flat/shipped — claim disputed (not DETERMINED)
Q4. what is going wrong?  exceptions (0): none  |  reconcile conflict=True uncertainty=False
Q5. why is it going wrong?  root-cause [epistemic status]: late support=0.9 contested (not determined); delivered support=0.97 support-carrying (DETERMINED under the active rule); shipped support=0.92 contested (not determined)  |  under rule best-reliability-threshold (registry)
Q6. what if we do nothing?  project (holding the recorded trend) from last actual 0.96 + mean delta 0.0: period 1 -> 0.96; period 2 -> 0.96; period 3 -> 0.96  |  recorded variance 0.01
Q7. what are our options?  accept-customer-refund, accept-company-full-payment, partial-settlement, conditional-resolution, request-more-evidence, escalate, unresolved, external-adjudication  |  baseline unresolved  |  machine-eligible best: partial-settlement
Q8. what should we do?  recommendation partial-settlement (authority authority://deli-forecast-flat/adjudicate; floor-gated ['accept-customer-refund'])  ->  determination partial-settlement
    trade-off / do-nothing expected-impact: on-target: metric://deli-forecast-flat/m-on-time projection stays at/above recorded target 0.95 (worst 0.96) — no forecast-driven cost to doing nothing — recorded band 0.95…0.97 (± σ 0.01); worst side stays safe of the threshold — the spread confirms on-target — horizon-wide recorded band 0.95…0.97 across 3 projection periods (band_periods/band_horizon, same recorded σ) (baseline unresolved, priced=True, on-target=True) |  recorded band 0.95…0.97 (± σ 0.01, crosses=False)
Q9. who does it, authority/capacity?  adjudicator person://deli-forecast-flat/adjudicator (authority authority://deli-forecast-flat/adjudicate), obligated party org://deli-forecast-flat/company, appeal authority://deli-forecast-flat/adjudicate-appeal, actors 7
Q10. did it work, what did we learn?  verified=True status=RESOLVED determination=partial-settlement; outcome=partial settlement on the contested delivery; SLA-breach credit applied; ledger noted; customer keeps the service; learning: evidence://deli-forecast-flat/learning-note[conflicting delivery timestamps reach a determination only v…]
```

--- deli-cost ---
```
# §7L Q1–Q10 cockpit (engine-native) — org deli-cost
ACTIVE reconcile rule: best-reliability-threshold  |  source: registry  |  learned-this-run: False  |  why: unchanged
Q1. what happened?  state/events: 15 recorded events; dispute lifecycle OPEN->EVIDENCE_COLLECTION->CONTESTED->ADJUDICATION->RESOLUTION->ACCEPTED->EXECUTED->VERIFIED->CLOSED; status=RESOLVED lifecycle=CLOSED epistemic=RESOLVED_DETERMINED
Q2. what changed?  life cycle OPEN -> CLOSED; epistemic UNDETERMINED -> RESOLVED_DETERMINED; determination=partial-settlement; claim epistemic={'late': 'disputed', 'delivered': 'disputed', 'shipped': 'disputed'}; significance=determined
Q3. what matters?  prioritized attention (3): claim://deli-cost/late — claim disputed (not DETERMINED); claim://deli-cost/shipped — claim disputed (not DETERMINED); metric://deli-cost/m-latency [forecast] — forecast: projected to rise above 16.0 (target) — worst 24.0 at period 3 — recorded band 16.0…32.0 (± σ 8.0); worst side 32.0 above target 16.0 — horizon-wide recorded band 12.0…32.0 across 3 projection periods (band_periods/band_horizon, same recorded σ)
Q4. what is going wrong?  exceptions (0): none  |  reconcile conflict=True uncertainty=False
Q5. why is it going wrong?  root-cause [epistemic status]: late support=0.9 contested (not determined); delivered support=0.97 support-carrying (DETERMINED under the active rule); shipped support=0.92 contested (not determined)  |  under rule best-reliability-threshold (registry)
Q6. what if we do nothing?  project (holding the recorded trend) from last actual 18.0 + mean delta 2.0: period 1 -> 20.0; period 2 -> 22.0; period 3 -> 24.0  |  recorded variance 8.0
Q7. what are our options?  accept-customer-refund, accept-company-full-payment, partial-settlement, conditional-resolution, request-more-evidence, escalate, unresolved, external-adjudication  |  baseline unresolved  |  machine-eligible best: partial-settlement
Q8. what should we do?  recommendation partial-settlement (authority authority://deli-cost/adjudicate; floor-gated ['accept-customer-refund'])  ->  determination partial-settlement
    trade-off / do-nothing expected-impact: forecast-driven do-nothing cost: metric://deli-cost/m-latency projects to worst 24.0 (period 3) above recorded target 16.0 by 8.0 — doing nothing lets the recorded trend deteriorate — recorded band 16.0…32.0 (± σ 8.0); worst side 32.0 above target 16.0 — the whole recorded spread is priced as bad — horizon-wide recorded band 12.0…32.0 across 3 projection periods (band_periods/band_horizon, same recorded σ) (baseline unresolved, priced=True, on-target=False) |  recorded band 16.0…32.0 (± σ 8.0, crosses=True)
Q9. who does it, authority/capacity?  adjudicator person://deli-cost/adjudicator (authority authority://deli-cost/adjudicate), obligated party org://deli-cost/company, appeal authority://deli-cost/adjudicate-appeal, actors 7
Q10. did it work, what did we learn?  verified=True status=RESOLVED determination=partial-settlement; outcome=partial settlement on the contested delivery; SLA-breach credit applied; ledger noted; customer keeps the service; learning: evidence://deli-cost/learning-note[conflicting delivery timestamps reach a determination only v…]
```

--- deli-cost-flat ---
```
# §7L Q1–Q10 cockpit (engine-native) — org deli-cost-flat
ACTIVE reconcile rule: best-reliability-threshold  |  source: registry  |  learned-this-run: False  |  why: unchanged
Q1. what happened?  state/events: 15 recorded events; dispute lifecycle OPEN->EVIDENCE_COLLECTION->CONTESTED->ADJUDICATION->RESOLUTION->ACCEPTED->EXECUTED->VERIFIED->CLOSED; status=RESOLVED lifecycle=CLOSED epistemic=RESOLVED_DETERMINED
Q2. what changed?  life cycle OPEN -> CLOSED; epistemic UNDETERMINED -> RESOLVED_DETERMINED; determination=partial-settlement; claim epistemic={'late': 'disputed', 'delivered': 'disputed', 'shipped': 'disputed'}; significance=determined
Q3. what matters?  prioritized attention (2): claim://deli-cost-flat/late — claim disputed (not DETERMINED); claim://deli-cost-flat/shipped — claim disputed (not DETERMINED)
Q4. what is going wrong?  exceptions (0): none  |  reconcile conflict=True uncertainty=False
Q5. why is it going wrong?  root-cause [epistemic status]: late support=0.9 contested (not determined); delivered support=0.97 support-carrying (DETERMINED under the active rule); shipped support=0.92 contested (not determined)  |  under rule best-reliability-threshold (registry)
Q6. what if we do nothing?  project (holding the recorded trend) from last actual 8.0 + mean delta 0.0: period 1 -> 8.0; period 2 -> 8.0; period 3 -> 8.0  |  recorded variance 1.0
Q7. what are our options?  accept-customer-refund, accept-company-full-payment, partial-settlement, conditional-resolution, request-more-evidence, escalate, unresolved, external-adjudication  |  baseline unresolved  |  machine-eligible best: partial-settlement
Q8. what should we do?  recommendation partial-settlement (authority authority://deli-cost-flat/adjudicate; floor-gated ['accept-customer-refund'])  ->  determination partial-settlement
    trade-off / do-nothing expected-impact: on-target: metric://deli-cost-flat/m-latency projection stays at/below recorded target 10.0 (worst 8.0) — no forecast-driven cost to doing nothing — recorded band 7.0…9.0 (± σ 1.0); worst side stays safe of the threshold — the spread confirms on-target — horizon-wide recorded band 7.0…9.0 across 3 projection periods (band_periods/band_horizon, same recorded σ) (baseline unresolved, priced=True, on-target=True) |  recorded band 7.0…9.0 (± σ 1.0, crosses=False)
Q9. who does it, authority/capacity?  adjudicator person://deli-cost-flat/adjudicator (authority authority://deli-cost-flat/adjudicate), obligated party org://deli-cost-flat/company, appeal authority://deli-cost-flat/adjudicate-appeal, actors 7
Q10. did it work, what did we learn?  verified=True status=RESOLVED determination=partial-settlement; outcome=partial settlement on the contested delivery; SLA-breach credit applied; ledger noted; customer keeps the service; learning: evidence://deli-cost-flat/learning-note[conflicting delivery timestamps reach a determination only v…]
```

--- deli ---
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

## §16 verdict

**The forecast→attention→expected-impact loop now closes AS DATA for both metric directions.** For an org that records a realized-vs-expected `metric://` series + a `direction` (default `higher-is-better`), Q6 projects the deterministic if-nothing-changes trajectory via the Sprint-20 `forecast_metric`; Q3 turns a projection that crosses a recorded threshold INTO attention in the correct orientation (a rate/quality metric that is projected to fall below its target; a cost/latency/defect/risk metric that is projected to rise above its ceiling); and Q8/the trade-off price the do-nothing baseline from that same projection (below-target vs above-ceiling). It is all deterministic and data-only — direction, threshold resolution (explicit `forecast_threshold` > metric `target` > last `actual`), the crossing test, and the do-nothing summary derive exclusively from the recorded series + the recorded direction; never the wall-clock. The higher-is-better default keeps Sprint 21 byte-identical. The Q8 recommendation is UNCHANGED — the forecast prices attention and the do-nothing baseline but never overrules the §6-floor-gated machine-eligible best, and the determination stays the §6 human's `determination_policy` call. What is still not derivable: an org that has NOT recorded a realized-vs-expected series cannot be made to produce a forecast or a forecast-driven attention/cost — the cockpit reports the recorded reality and does not manufacture certainty — and a richer/adaptive forecast model (beyond the deterministic last-actual + mean-delta projection) remains out of scope of the honest, deterministic, ~$0 stance.

_Additive; frozen ontology, SPEC v0.22, 49 $defs. The forecast prices attention + do-nothing in either direction; it never overrules the §6 human or the floor-gated recommendation._
