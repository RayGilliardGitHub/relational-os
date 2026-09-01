# §7L Q3-attention horizon-wide suffix + Q9 capacity-planning — engine-native render (Sprint 26)
generated 2026-09-01T06:22:47Z  |  `adjudication_engine._forecast_closure`/`cockpit_s7l`  |  recorded `metric://` series + recorded point-`variance` + the recorded `band_variance` source + a recorded authority `capacity` -> (1) the q3 forecast-driven attention `why` now names the SAME record-wide horizon band (band_horizon) that Q6/Q8/do-nothing carry — appended as a STRICT PREFIX suffix; (2) a Q9 `capacity_planning_attention` flag/reason derived from recorded capacity + load + the horizon band (headroom / at-capacity / deficit), ONLY where a capacity is recorded. Additive; default orgs byte-identical to Sprint 25 except the additive Q3 suffix + the capacity-only key.  | SPEC v0.22, 49 $defs, URI cap

The human's FIRST attention line (Q3) now names the recorded whole-horizon worst case (band_horizon) verbatim with Q6/Q8/do-nothing — the same recorded σ applied to every projection period, never a new model. And where the org records a numeric `capacity`, Q9 adds a data-only capacity-planning reason (headroom/at-capacity/deficit from recorded numbers only) — never a fabricated figure, never a directive.

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

--- deli-varmax-cap ---
```
# §7L Q1–Q10 cockpit (engine-native) — org deli-varmax-cap
ACTIVE reconcile rule: best-reliability-threshold  |  source: registry  |  learned-this-run: False  |  why: unchanged
Q1. what happened?  state/events: 16 recorded events; dispute lifecycle OPEN->EVIDENCE_COLLECTION->CONTESTED->ADJUDICATION->RESOLUTION->ACCEPTED->EXECUTED->VERIFIED->CLOSED; status=RESOLVED lifecycle=CLOSED epistemic=RESOLVED_DETERMINED
Q2. what changed?  life cycle OPEN -> CLOSED; epistemic UNDETERMINED -> RESOLVED_DETERMINED; determination=partial-settlement; claim epistemic={'late': 'disputed', 'delivered': 'disputed', 'shipped': 'disputed'}; significance=determined
Q3. what matters?  prioritized attention (3): claim://deli-varmax-cap/late — claim disputed (not DETERMINED); claim://deli-varmax-cap/shipped — claim disputed (not DETERMINED); metric://deli-varmax-cap/m-on-time [forecast] — forecast: projected to fall below 0.95 (target) — worst 0.8 at period 3 — recorded band 0.62…0.98 (± σ 0.18); worst side 0.62 below target 0.95 — band σ from the recorded whole-series max |variance| (band_variance all) — horizon-wide recorded band 0.62…1.02 across 3 projection periods (band_periods/band_horizon, same recorded σ)
Q4. what is going wrong?  exceptions (0): none  |  reconcile conflict=True uncertainty=False
Q5. why is it going wrong?  root-cause [epistemic status]: late support=0.9 contested (not determined); delivered support=0.97 support-carrying (DETERMINED under the active rule); shipped support=0.92 contested (not determined)  |  under rule best-reliability-threshold (registry)
Q6. what if we do nothing?  project (holding the recorded trend) from last actual 0.86 + mean delta -0.02: period 1 -> 0.84; period 2 -> 0.82; period 3 -> 0.8  |  recorded variance -0.03
Q7. what are our options?  accept-customer-refund, accept-company-full-payment, partial-settlement, conditional-resolution, request-more-evidence, escalate, unresolved, external-adjudication  |  baseline unresolved  |  machine-eligible best: partial-settlement
Q8. what should we do?  recommendation partial-settlement (authority authority://deli-varmax-cap/adjudicate; floor-gated ['accept-customer-refund'])  ->  determination partial-settlement
    trade-off / do-nothing expected-impact: forecast-driven do-nothing cost: metric://deli-varmax-cap/m-on-time projects to worst 0.8 (period 3) below recorded target 0.95 by 0.15 — doing nothing lets the recorded trend deteriorate — recorded band 0.62…0.98 (± σ 0.18); worst side 0.62 below target 0.95 — the whole recorded spread is priced as bad — band σ from the recorded whole-series max |variance| (band_variance all) — horizon-wide recorded band 0.62…1.02 across 3 projection periods (band_periods/band_horizon, same recorded σ) (baseline unresolved, priced=True, on-target=False) |  recorded band 0.62…0.98 (± σ 0.18, crosses=True)
Q9. who does it, authority/capacity?  adjudicator person://deli-varmax-cap/adjudicator (authority authority://deli-varmax-cap/adjudicate), obligated party org://deli-varmax-cap/company, appeal authority://deli-varmax-cap/adjudicate-appeal, actors 7, capacity 500.0 resolutions/day (load 0.72)
Q10. did it work, what did we learn?  verified=True status=RESOLVED determination=partial-settlement; outcome=partial settlement on the contested delivery; SLA-breach credit applied; ledger noted; customer keeps the service; learning: evidence://deli-varmax-cap/learning-note[conflicting delivery timestamps reach a determination only v…]
```

Q9 capacity_planning_attention: flag=False  why=capacity-planning: recorded capacity 500.0 resolutions/day (load 0.72) vs the horizon-wide recorded band 0.62…1.02 across 3 projection periods — derived headroom from recorded numbers only (not a directive, no invented capacity)

--- deli-flat2 ---
```
# §7L Q1–Q10 cockpit (engine-native) — org deli-flat2
ACTIVE reconcile rule: best-reliability-threshold  |  source: registry  |  learned-this-run: False  |  why: unchanged
Q1. what happened?  state/events: 15 recorded events; dispute lifecycle OPEN->EVIDENCE_COLLECTION->CONTESTED->ADJUDICATION->RESOLUTION->ACCEPTED->EXECUTED->VERIFIED->CLOSED; status=RESOLVED lifecycle=CLOSED epistemic=RESOLVED_DETERMINED
Q2. what changed?  life cycle OPEN -> CLOSED; epistemic UNDETERMINED -> RESOLVED_DETERMINED; determination=partial-settlement; claim epistemic={'late': 'disputed', 'delivered': 'disputed', 'shipped': 'disputed'}; significance=determined
Q3. what matters?  prioritized attention (2): claim://deli-flat2/late — claim disputed (not DETERMINED); claim://deli-flat2/shipped — claim disputed (not DETERMINED)
Q4. what is going wrong?  exceptions (0): none  |  reconcile conflict=True uncertainty=False
Q5. why is it going wrong?  root-cause [epistemic status]: late support=0.9 contested (not determined); delivered support=0.97 support-carrying (DETERMINED under the active rule); shipped support=0.92 contested (not determined)  |  under rule best-reliability-threshold (registry)
Q6. what if we do nothing?  project (holding the recorded trend) from last actual 0.96 + mean delta 0.0: period 1 -> 0.96; period 2 -> 0.96; period 3 -> 0.96  |  recorded variance None
Q7. what are our options?  accept-customer-refund, accept-company-full-payment, partial-settlement, conditional-resolution, request-more-evidence, escalate, unresolved, external-adjudication  |  baseline unresolved  |  machine-eligible best: partial-settlement
Q8. what should we do?  recommendation partial-settlement (authority authority://deli-flat2/adjudicate; floor-gated ['accept-customer-refund'])  ->  determination partial-settlement
    trade-off / do-nothing expected-impact: on-target: metric://deli-flat2/m-on-time projection stays at/above recorded target 0.95 (worst 0.96) — no forecast-driven cost to doing nothing (baseline unresolved, priced=True, on-target=True)
Q9. who does it, authority/capacity?  adjudicator person://deli-flat2/adjudicator (authority authority://deli-flat2/adjudicate), obligated party org://deli-flat2/company, appeal authority://deli-flat2/adjudicate-appeal, actors 7
Q10. did it work, what did we learn?  verified=True status=RESOLVED determination=partial-settlement; outcome=partial settlement on the contested delivery; SLA-breach credit applied; ledger noted; customer keeps the service; learning: evidence://deli-flat2/learning-note[conflicting delivery timestamps reach a determination only v…]
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

**Q3 and Q9 capacity attention now carry the recorded whole-horizon worst case AS DATA where it exists.** Q3's forecast-driven attention `why` appends the exact `band_horizon` range (same shared constant as the do-nothing summary -> verbatim by construction) behind the Sprint-23/24/25 single-worst phrase, which stays a strict prefix. Where the org records a numeric `capacity`, Q9's `capacity_planning_attention` states the recorded capacity value/unit/load vs the horizon-wide band and labels headroom / at-capacity / deficit as a derived REASON from recorded numbers only — never an invented capacity value, never a directive. A no-capacity org / no-band / no-data org carries no new key (byte-identical superset). The Q8 recommendation is UNCHANGED: attention + capacity reasoning never overrule the §6-floor-gated machine-eligible best. **Still not derivable:** an org with no recorded point variances cannot be priced as a band (correct); an org that records no capacity gets no capacity-planning line (correct); and this remains a recorded-spread range, NOT a probabilistic confidence interval (a stochastic/adaptive forecast stays out of the deterministic ~$0 stance).

_Additive; frozen ontology, SPEC v0.22, 49 $defs. Q3 + Q9 capacity attention price the recorded whole-horizon spread as data; they never overrule the §6 human or the floor-gated recommendation._
