# §7L recorded whole-series band-variance source → do-nothing expected-impact — engine-native render (Sprint 24)
generated 2026-09-01T05:08:28Z  |  `adjudication_engine.cockpit_s7l`/`render_cockpit_s7l`  |  recorded `metric://` series + recorded point-`variance` values + the recorded `band_variance` source ('last' default vs 'all'/'minmax' = recorded whole-series max |variance|) -> Q8/trade-off do-nothing priced as a projected BAND (worst ± σ) WHERE the data exists; the default last-point behavior is byte-identical to Sprint 23  |  SPEC v0.22, 49 $defs, URI cap

The band's VARIANCE SOURCE is now a RECORDED, additive `band_variance` parameter on the metric:// object: absent/'last' uses the last recorded point's variance (Sprint-23 default, byte-identical); 'all'/'minmax' use the recorded WHOLE-SERIES choice (the largest recorded |variance| across the recorded points). An org whose measured spread WIDENED over time can thus price a do-nothing band from the recorded worst-case spread, and one that CONVERGED can tighten it — still honest: every sigma is a recorded point variance magnitude, never a probability/confidence interval, never the wall-clock.

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

--- deli-varmax ---
```
# §7L Q1–Q10 cockpit (engine-native) — org deli-varmax
ACTIVE reconcile rule: best-reliability-threshold  |  source: registry  |  learned-this-run: False  |  why: unchanged
Q1. what happened?  state/events: 15 recorded events; dispute lifecycle OPEN->EVIDENCE_COLLECTION->CONTESTED->ADJUDICATION->RESOLUTION->ACCEPTED->EXECUTED->VERIFIED->CLOSED; status=RESOLVED lifecycle=CLOSED epistemic=RESOLVED_DETERMINED
Q2. what changed?  life cycle OPEN -> CLOSED; epistemic UNDETERMINED -> RESOLVED_DETERMINED; determination=partial-settlement; claim epistemic={'late': 'disputed', 'delivered': 'disputed', 'shipped': 'disputed'}; significance=determined
Q3. what matters?  prioritized attention (3): claim://deli-varmax/late — claim disputed (not DETERMINED); claim://deli-varmax/shipped — claim disputed (not DETERMINED); metric://deli-varmax/m-on-time [forecast] — forecast: projected to fall below 0.95 (target) — worst 0.8 at period 3 — recorded band 0.62…0.98 (± σ 0.18); worst side 0.62 below target 0.95 — band σ from the recorded whole-series max |variance| (band_variance all) — horizon-wide recorded band 0.62…1.02 across 3 projection periods (band_periods/band_horizon, same recorded σ)
Q4. what is going wrong?  exceptions (0): none  |  reconcile conflict=True uncertainty=False
Q5. why is it going wrong?  root-cause [epistemic status]: late support=0.9 contested (not determined); delivered support=0.97 support-carrying (DETERMINED under the active rule); shipped support=0.92 contested (not determined)  |  under rule best-reliability-threshold (registry)
Q6. what if we do nothing?  project (holding the recorded trend) from last actual 0.86 + mean delta -0.02: period 1 -> 0.84; period 2 -> 0.82; period 3 -> 0.8  |  recorded variance -0.03
Q7. what are our options?  accept-customer-refund, accept-company-full-payment, partial-settlement, conditional-resolution, request-more-evidence, escalate, unresolved, external-adjudication  |  baseline unresolved  |  machine-eligible best: partial-settlement
Q8. what should we do?  recommendation partial-settlement (authority authority://deli-varmax/adjudicate; floor-gated ['accept-customer-refund'])  ->  determination partial-settlement
    trade-off / do-nothing expected-impact: forecast-driven do-nothing cost: metric://deli-varmax/m-on-time projects to worst 0.8 (period 3) below recorded target 0.95 by 0.15 — doing nothing lets the recorded trend deteriorate — recorded band 0.62…0.98 (± σ 0.18); worst side 0.62 below target 0.95 — the whole recorded spread is priced as bad — band σ from the recorded whole-series max |variance| (band_variance all) — horizon-wide recorded band 0.62…1.02 across 3 projection periods (band_periods/band_horizon, same recorded σ) (baseline unresolved, priced=True, on-target=False) |  recorded band 0.62…0.98 (± σ 0.18, crosses=True)
Q9. who does it, authority/capacity?  adjudicator person://deli-varmax/adjudicator (authority authority://deli-varmax/adjudicate), obligated party org://deli-varmax/company, appeal authority://deli-varmax/adjudicate-appeal, actors 7
Q10. did it work, what did we learn?  verified=True status=RESOLVED determination=partial-settlement; outcome=partial settlement on the contested delivery; SLA-breach credit applied; ledger noted; customer keeps the service; learning: evidence://deli-varmax/learning-note[conflicting delivery timestamps reach a determination only v…]
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

**The do-nothing expected-impact now prices the recorded WHOLE-SERIES spread as data WHERE the org records it.** For any org that records a realized-vs-expected `metric://` series whose points carry numeric `variance` values AND records `band_variance` on the metric object, the Q8/trade-off do-nothing baseline's projected band is priced from the recorded worst-case spread: sigma = the largest recorded |variance| across the recorded points (the whole-series choice), worst (per the recorded `direction`) ± sigma -> low…high, the recorded `expected` last value the anchor, and whether the worst side crosses the recorded threshold explicit on the Q3 attention `why` and the do-nothing summary. The recorded source is named additively (`band.source`, `band_variance` on the closure/q8/do_nothing, and an honest summary phrase). It is deterministic and data-only: every possible sigma is a recorded point variance magnitude — a pure function of the recorded `points` list, never invented, never the wall-clock. An org that records NO `band_variance` keeps the Sprint-23 last-point band BYTE-IDENTICAL (no source key), and a no-variance series / no-data org keeps the single-point / fallback unchanged. The Q8 recommendation is UNCHANGED: the band prices attention and the do-nothing baseline, it never overrules the §6-floor-gated machine-eligible best. What is still not derivable: an org that does not record variances (or does not record a band_variance choice) is priced at the last-point band / single point — the engine reports the recorded reality and does not manufacture a spread — and this remains a recorded-spread range, NOT a probabilistic confidence interval from a model (a stochastic/adaptive forecast stays out of the deterministic ~$0 stance).

_Additive; frozen ontology, SPEC v0.22, 49 $defs. The band prices the recorded do-nothing spread; it never overrules the §6 human or the floor-gated recommendation._
