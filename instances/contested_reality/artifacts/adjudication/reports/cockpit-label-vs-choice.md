# §7L label-vs-choice — the RECOMMENDED option made `capacity_infeasible` — engine-native render (Sprint 30)
generated 2026-09-01T05:08:28Z  |  `adjudication_engine._per_option_capacity_flags`/`cockpit_s7l`  |  NO engine change (hash a60f8f7…): Sprint 29's recorder already labels ANY option `capacity_infeasible` when its RECORDED per-option requirement > available. The point of Sprint 30 is to drive the SHARPEST boundary on a real org: the recorded capacity says the machine-eligible best / Q8 recommendation itself (`partial-settlement`) CANNOT run (recorded requirement 499.0 > available 498.7), yet the cockpit provably STILL recommends partial-settlement (exactly `cockpit_q7q8`). The marker is a REASON, never a CHOICE — the §6 human always rules.  |  SPEC v0.22, 49 $defs, URI cap

Sprint 29 let the marker NAME a specific infeasible option but never had the RECOMMENDED option be that one. `deli-recommend-infcap` records an at-capacity org (cap 500.0 res/day, load 1.3 -> available 498.7) and a per-option requirement map in which `partial-settlement` — the machine-eligible best (utility 0.7275, non-gated) — records 499.0 > 498.7 => `capacity_infeasible` ON THE RECOMMENDED OPTION; the other 6 non-baseline options <= available => `capacity_risk`; the baseline unresolved records no requirement => never flagged. The Q7/Q8 `capacity_constraint` block (reason `at-capacity`, flag True, available 498.7) labels this — and the engine STILL surfaces Q8 recommendation `partial-settlement` + machine-eligible best `partial-settlement`, EXACTLY equal to `cockpit_q7q8`. The §6 human must choose the replacement (or overrule); the marker never does.

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

Q8 capacity_constraint: reason=headroom  flag=False  recorded_capacity=500.0 resolutions/day (load 0.72)  horizon_band={'low': 0.62, 'high': 1.02}
  options_flagged={}
  note: derived capacity-constraint reason from recorded numbers only — never an invented figure, never a directive, never an option removal; the Q8 recommendation is UNCHANGED (the §6 human always rules)

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

--- deli-infcap ---
```
# §7L Q1–Q10 cockpit (engine-native) — org deli-infcap
ACTIVE reconcile rule: best-reliability-threshold  |  source: registry  |  learned-this-run: False  |  why: unchanged
Q1. what happened?  state/events: 17 recorded events; dispute lifecycle OPEN->EVIDENCE_COLLECTION->CONTESTED->ADJUDICATION->RESOLUTION->ACCEPTED->EXECUTED->VERIFIED->CLOSED; status=RESOLVED lifecycle=CLOSED epistemic=RESOLVED_DETERMINED
Q2. what changed?  life cycle OPEN -> CLOSED; epistemic UNDETERMINED -> RESOLVED_DETERMINED; determination=partial-settlement; claim epistemic={'late': 'disputed', 'delivered': 'disputed', 'shipped': 'disputed'}; significance=determined
Q3. what matters?  prioritized attention (3): claim://deli-infcap/late — claim disputed (not DETERMINED); claim://deli-infcap/shipped — claim disputed (not DETERMINED); metric://deli-infcap/m-on-time [forecast] — forecast: projected to fall below 0.95 (target) — worst 0.8 at period 3 — recorded band 0.62…0.98 (± σ 0.18); worst side 0.62 below target 0.95 — band σ from the recorded whole-series max |variance| (band_variance all) — horizon-wide recorded band 0.62…1.02 across 3 projection periods (band_periods/band_horizon, same recorded σ)
Q4. what is going wrong?  exceptions (0): none  |  reconcile conflict=True uncertainty=False
Q5. why is it going wrong?  root-cause [epistemic status]: late support=0.9 contested (not determined); delivered support=0.97 support-carrying (DETERMINED under the active rule); shipped support=0.92 contested (not determined)  |  under rule best-reliability-threshold (registry)
Q6. what if we do nothing?  project (holding the recorded trend) from last actual 0.86 + mean delta -0.02: period 1 -> 0.84; period 2 -> 0.82; period 3 -> 0.8  |  recorded variance -0.03
Q7. what are our options?  accept-customer-refund, accept-company-full-payment, partial-settlement, conditional-resolution, request-more-evidence, escalate, unresolved, external-adjudication  |  baseline unresolved  |  machine-eligible best: partial-settlement
Q8. what should we do?  recommendation partial-settlement (authority authority://deli-infcap/adjudicate; floor-gated ['accept-customer-refund'])  ->  determination partial-settlement
    trade-off / do-nothing expected-impact: forecast-driven do-nothing cost: metric://deli-infcap/m-on-time projects to worst 0.8 (period 3) below recorded target 0.95 by 0.15 — doing nothing lets the recorded trend deteriorate — recorded band 0.62…0.98 (± σ 0.18); worst side 0.62 below target 0.95 — the whole recorded spread is priced as bad — band σ from the recorded whole-series max |variance| (band_variance all) — horizon-wide recorded band 0.62…1.02 across 3 projection periods (band_periods/band_horizon, same recorded σ) (baseline unresolved, priced=True, on-target=False) |  recorded band 0.62…0.98 (± σ 0.18, crosses=True)
Q9. who does it, authority/capacity?  adjudicator person://deli-infcap/adjudicator (authority authority://deli-infcap/adjudicate), obligated party org://deli-infcap/company, appeal authority://deli-infcap/adjudicate-appeal, actors 7, capacity 500.0 resolutions/day (load 1.3)
Q10. did it work, what did we learn?  verified=True status=RESOLVED determination=partial-settlement; outcome=partial settlement on the contested delivery; SLA-breach credit applied; ledger noted; customer keeps the service; learning: evidence://deli-infcap/learning-note[conflicting delivery timestamps reach a determination only v…]
```

Q8 capacity_constraint: reason=at-capacity  flag=True  recorded_capacity=500.0 resolutions/day (load 1.3)  horizon_band={'low': 0.62, 'high': 1.02}
  available_capacity=498.7 (recorded capacity VALUE − recorded load, same unit)
  options_flagged={'accept-customer-refund': 'capacity_infeasible', 'accept-company-full-payment': 'capacity_infeasible', 'partial-settlement': 'capacity_risk', 'conditional-resolution': 'capacity_risk', 'request-more-evidence': 'capacity_risk', 'escalate': 'capacity_risk', 'external-adjudication': 'capacity_infeasible'}
  per_option_requirements={'accept-customer-refund': 499.0, 'accept-company-full-payment': 499.0, 'external-adjudication': 499.0, 'partial-settlement': 200.0, 'conditional-resolution': 200.0, 'request-more-evidence': 50.0, 'escalate': 100.0}
  note: derived capacity-constraint reason from recorded numbers only — never an invented figure, never a directive, never an option removal; the Q8 recommendation is UNCHANGED (the §6 human always rules)

--- deli-deficit-inf ---
```
# §7L Q1–Q10 cockpit (engine-native) — org deli-deficit-inf
ACTIVE reconcile rule: best-reliability-threshold  |  source: registry  |  learned-this-run: False  |  why: unchanged
Q1. what happened?  state/events: 17 recorded events; dispute lifecycle OPEN->EVIDENCE_COLLECTION->CONTESTED->ADJUDICATION->RESOLUTION->ACCEPTED->EXECUTED->VERIFIED->CLOSED; status=RESOLVED lifecycle=CLOSED epistemic=RESOLVED_DETERMINED
Q2. what changed?  life cycle OPEN -> CLOSED; epistemic UNDETERMINED -> RESOLVED_DETERMINED; determination=partial-settlement; claim epistemic={'late': 'disputed', 'delivered': 'disputed', 'shipped': 'disputed'}; significance=determined
Q3. what matters?  prioritized attention (3): claim://deli-deficit-inf/late — claim disputed (not DETERMINED); claim://deli-deficit-inf/shipped — claim disputed (not DETERMINED); metric://deli-deficit-inf/m-latency [forecast] — forecast: projected to rise above 16.0 (target) — worst 24.0 at period 3 — recorded band 16.0…32.0 (± σ 8.0); worst side 32.0 above target 16.0 — band σ from the recorded whole-series max |variance| (band_variance all) — horizon-wide recorded band 12.0…32.0 across 3 projection periods (band_periods/band_horizon, same recorded σ)
Q4. what is going wrong?  exceptions (0): none  |  reconcile conflict=True uncertainty=False
Q5. why is it going wrong?  root-cause [epistemic status]: late support=0.9 contested (not determined); delivered support=0.97 support-carrying (DETERMINED under the active rule); shipped support=0.92 contested (not determined)  |  under rule best-reliability-threshold (registry)
Q6. what if we do nothing?  project (holding the recorded trend) from last actual 18.0 + mean delta 2.0: period 1 -> 20.0; period 2 -> 22.0; period 3 -> 24.0  |  recorded variance 8.0
Q7. what are our options?  accept-customer-refund, accept-company-full-payment, partial-settlement, conditional-resolution, request-more-evidence, escalate, unresolved, external-adjudication  |  baseline unresolved  |  machine-eligible best: partial-settlement
Q8. what should we do?  recommendation partial-settlement (authority authority://deli-deficit-inf/adjudicate; floor-gated ['accept-customer-refund'])  ->  determination partial-settlement
    trade-off / do-nothing expected-impact: forecast-driven do-nothing cost: metric://deli-deficit-inf/m-latency projects to worst 24.0 (period 3) above recorded target 16.0 by 8.0 — doing nothing lets the recorded trend deteriorate — recorded band 16.0…32.0 (± σ 8.0); worst side 32.0 above target 16.0 — the whole recorded spread is priced as bad — band σ from the recorded whole-series max |variance| (band_variance all) — horizon-wide recorded band 12.0…32.0 across 3 projection periods (band_periods/band_horizon, same recorded σ) (baseline unresolved, priced=True, on-target=False) |  recorded band 16.0…32.0 (± σ 8.0, crosses=True)
Q9. who does it, authority/capacity?  adjudicator person://deli-deficit-inf/adjudicator (authority authority://deli-deficit-inf/adjudicate), obligated party org://deli-deficit-inf/company, appeal authority://deli-deficit-inf/adjudicate-appeal, actors 7, capacity 30.0 resolutions/day (load 0.9)
Q10. did it work, what did we learn?  verified=True status=RESOLVED determination=partial-settlement; outcome=partial settlement on the contested delivery; SLA-breach credit applied; ledger noted; customer keeps the service; learning: evidence://deli-deficit-inf/learning-note[conflicting delivery timestamps reach a determination only v…]
```

Q8 capacity_constraint: reason=deficit  flag=True  recorded_capacity=30.0 resolutions/day (load 0.9)  horizon_band={'low': 12.0, 'high': 32.0}
  available_capacity=29.1 (recorded capacity VALUE − recorded load, same unit)
  options_flagged={'accept-customer-refund': 'capacity_infeasible', 'accept-company-full-payment': 'capacity_infeasible', 'partial-settlement': 'capacity_risk', 'conditional-resolution': 'capacity_risk', 'request-more-evidence': 'capacity_risk', 'escalate': 'capacity_risk', 'external-adjudication': 'capacity_infeasible'}
  per_option_requirements={'external-adjudication': 30.0, 'accept-company-full-payment': 30.0, 'accept-customer-refund': 30.0, 'partial-settlement': 20.0, 'conditional-resolution': 20.0, 'request-more-evidence': 10.0, 'escalate': 15.0}
  note: derived capacity-constraint reason from recorded numbers only — never an invented figure, never a directive, never an option removal; the Q8 recommendation is UNCHANGED (the §6 human always rules)

--- deli-recommend-infcap ---
```
# §7L Q1–Q10 cockpit (engine-native) — org deli-recommend-infcap
ACTIVE reconcile rule: best-reliability-threshold  |  source: registry  |  learned-this-run: False  |  why: unchanged
Q1. what happened?  state/events: 17 recorded events; dispute lifecycle OPEN->EVIDENCE_COLLECTION->CONTESTED->ADJUDICATION->RESOLUTION->ACCEPTED->EXECUTED->VERIFIED->CLOSED; status=RESOLVED lifecycle=CLOSED epistemic=RESOLVED_DETERMINED
Q2. what changed?  life cycle OPEN -> CLOSED; epistemic UNDETERMINED -> RESOLVED_DETERMINED; determination=partial-settlement; claim epistemic={'late': 'disputed', 'delivered': 'disputed', 'shipped': 'disputed'}; significance=determined
Q3. what matters?  prioritized attention (3): claim://deli-recommend-infcap/late — claim disputed (not DETERMINED); claim://deli-recommend-infcap/shipped — claim disputed (not DETERMINED); metric://deli-recommend-infcap/m-on-time [forecast] — forecast: projected to fall below 0.95 (target) — worst 0.8 at period 3 — recorded band 0.62…0.98 (± σ 0.18); worst side 0.62 below target 0.95 — band σ from the recorded whole-series max |variance| (band_variance all) — horizon-wide recorded band 0.62…1.02 across 3 projection periods (band_periods/band_horizon, same recorded σ)
Q4. what is going wrong?  exceptions (0): none  |  reconcile conflict=True uncertainty=False
Q5. why is it going wrong?  root-cause [epistemic status]: late support=0.9 contested (not determined); delivered support=0.97 support-carrying (DETERMINED under the active rule); shipped support=0.92 contested (not determined)  |  under rule best-reliability-threshold (registry)
Q6. what if we do nothing?  project (holding the recorded trend) from last actual 0.86 + mean delta -0.02: period 1 -> 0.84; period 2 -> 0.82; period 3 -> 0.8  |  recorded variance -0.03
Q7. what are our options?  accept-customer-refund, accept-company-full-payment, partial-settlement, conditional-resolution, request-more-evidence, escalate, unresolved, external-adjudication  |  baseline unresolved  |  machine-eligible best: partial-settlement
Q8. what should we do?  recommendation partial-settlement (authority authority://deli-recommend-infcap/adjudicate; floor-gated ['accept-customer-refund'])  ->  determination partial-settlement
    trade-off / do-nothing expected-impact: forecast-driven do-nothing cost: metric://deli-recommend-infcap/m-on-time projects to worst 0.8 (period 3) below recorded target 0.95 by 0.15 — doing nothing lets the recorded trend deteriorate — recorded band 0.62…0.98 (± σ 0.18); worst side 0.62 below target 0.95 — the whole recorded spread is priced as bad — band σ from the recorded whole-series max |variance| (band_variance all) — horizon-wide recorded band 0.62…1.02 across 3 projection periods (band_periods/band_horizon, same recorded σ) (baseline unresolved, priced=True, on-target=False) |  recorded band 0.62…0.98 (± σ 0.18, crosses=True)
Q9. who does it, authority/capacity?  adjudicator person://deli-recommend-infcap/adjudicator (authority authority://deli-recommend-infcap/adjudicate), obligated party org://deli-recommend-infcap/company, appeal authority://deli-recommend-infcap/adjudicate-appeal, actors 7, capacity 500.0 resolutions/day (load 1.3)
Q10. did it work, what did we learn?  verified=True status=RESOLVED determination=partial-settlement; outcome=partial settlement on the contested delivery; SLA-breach credit applied; ledger noted; customer keeps the service; learning: evidence://deli-recommend-infcap/learning-note[conflicting delivery timestamps reach a determination only v…]
```

Q8 capacity_constraint: reason=at-capacity  flag=True  recorded_capacity=500.0 resolutions/day (load 1.3)  horizon_band={'low': 0.62, 'high': 1.02}
  available_capacity=498.7 (recorded capacity VALUE − recorded load, same unit)
  options_flagged={'accept-customer-refund': 'capacity_risk', 'accept-company-full-payment': 'capacity_risk', 'partial-settlement': 'capacity_infeasible', 'conditional-resolution': 'capacity_risk', 'request-more-evidence': 'capacity_risk', 'escalate': 'capacity_risk', 'external-adjudication': 'capacity_risk'}
  per_option_requirements={'partial-settlement': 499.0, 'conditional-resolution': 200.0, 'accept-customer-refund': 200.0, 'accept-company-full-payment': 200.0, 'external-adjudication': 100.0, 'request-more-evidence': 50.0, 'escalate': 80.0}
  note: derived capacity-constraint reason from recorded numbers only — never an invented figure, never a directive, never an option removal; the Q8 recommendation is UNCHANGED (the §6 human always rules)

## §16 verdict

**The marker is a REASON, never a CHOICE — at its sharpest.** A RECORDED per-option requirement now makes the frozen machine-eligible best / Q8 recommendation itself (`partial-settlement`) `capacity_infeasible` (recorded 499.0 > available 498.7), and the cockpit provably STILL recommends partial-settlement — exactly `cockpit_q7q8`, no re-rank, no removal, no §6 overrule. The marker LABELS 'the recorded capacity says the recommended option can't run'; it does NOT pick a replacement; the §6 human always rules. The seven Sprint-29 orgs stay byte-identical (a no-requirements org keeps today's block exactly; a no-capacity org carries no `capacity_constraint`). This is generic + additive — recorded `metric://` series + recorded point-`variance` + the recorded `band_variance` source + a recorded authority `capacity` + a recorded per-option `capacity_required` descriptor; no new noun, frozen 49 `$defs`.

**Still not derivable (the honest frontier):** a capacity-constrained OPTIMIZATION that RE-RANKS the recommendation for the machine stays out of scope of the deterministic advisory stance — the marker never CHOOSES; choosing a different option for the machine is a policy / user decision, not a label. A per-option requirement that is NOT unit-coupled to the recorded capacity / an option with no recorded requirement remains non-derivable (the engine never invents one). No SPEC bump (v0.22).

_Additive; frozen ontology, SPEC v0.22, 49 $defs, URI cap. The sharpest label-vs-choice boundary is now demonstrated AS DATA: the recorded capacity says the recommended option can't run, and the Q8 recommendation provably stays unchanged._
