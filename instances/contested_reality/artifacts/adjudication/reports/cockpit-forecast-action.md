# §7L forecast → attention → expected-impact — engine-native render (Sprint 21)
generated 2026-09-01T06:22:47Z  |  `adjudication_engine.cockpit_s7l`/`render_cockpit_s7l`  |  recorded `metric://` series + recorded threshold -> Q3 forecast attention + Q8 do-nothing expected-impact  |  SPEC v0.22, 49 $defs, URI cap

The recorded Q6 forecast is now CONNECTED to the org's decision surface: when its horizon projection crosses a recorded threshold it becomes a Q3 attention item (tagged `forecast`), and the Q8/trade-off's do-nothing baseline is priced from the same deterministic projection. An org without a recorded series keeps today's Q3/Q8/trade-off exactly.

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

**The recorded-data forecast now closes the loop from Q6 ("what if we do nothing?") through Q3 ("so it becomes attention") to Q8 ("what should we do, priced") AS DATA where the data exists.** A deteriorating recorded series (projection crossing its recorded target/threshold) is itself prioritized attention — the "do nothing and it gets worse" signal now surfaces on Q3, and the Q8/trade-off prices the do-nothing baseline from that same projection. It is all deterministic and data-only: threshold resolution (explicit `forecast_threshold` additive field > metric `target` > last `actual`), the crossing test, and the do-nothing summary derive exclusively from the recorded `metric://` series via the Sprint-20 `forecast_metric`; never the wall-clock. The Q8 recommendation is UNCHANGED — the forecast prices attention and the do-nothing baseline but never overrules the §6-floor-gated machine-eligible best, and the determination stays the §6 human's `determination_policy` call. An on-target/flat recorded control adds no forecast attention and prices do-nothing as on-target; an org with no recorded series keeps today's fallback exactly. What is still not derivable: an org that has NOT recorded a realized-vs-expected series cannot be made to produce a forecast or a forecast-driven attention/cost — the cockpit reports the recorded reality and does not manufacture certainty — and a richer/adaptive forecast model (beyond the deterministic last-actual + mean-delta projection) remains out of scope of the honest, deterministic, ~$0 stance.

_Additive; frozen ontology, SPEC v0.22, 49 $defs. The forecast prices attention + do-nothing; it never overrules the §6 human or the floor-gated recommendation._
