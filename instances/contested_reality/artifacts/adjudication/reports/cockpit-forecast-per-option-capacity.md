# §7L PER-OPTION capacity_infeasible — from a RECORDED per-option requirement — engine-native render (Sprint 29)
generated 2026-09-01T05:31:06Z  |  `adjudication_engine._per_option_capacity_flags`/`cockpit_s7l`  |  a NEW REPLAYABLE recorder `record_capacity_requirements` appends an additive `capacity_requirements` map on the SAME authority:// object that carries the recorded `capacity` {value, unit, load} — so AVAILABLE = recorded capacity VALUE − recorded load, unit-coupled by construction — and the Q7/Q8 `capacity_constraint` block now labels a SPECIFIC option `capacity_infeasible` iff its RECORDED requirement > available, else `capacity_risk` as today. Baseline (do-nothing/UNRESOLVED) never flagged; `reason`/`flag` still come from the frozen org-level `_capacity_reason`; no re-rank, no removal, no §6 overrule — the Q8 recommendation stays EXACTLY equal to `cockpit_q7q8` even when SOME option is infeasible.  |  SPEC v0.22, 49 $defs, URI cap

Sprint 28 proved the marker at-headroom/at-capacity/deficit but left `capacity_infeasible` STRUCTURALLY UNREACHABLE (no per-option requirement was ever recorded). Sprint 29 makes the recorded capacity PER-OPTION. `deli-infcap` records an at-capacity org (cap 500.0 res/day, load 1.3 -> available 498.7); its three heavy options record 499.0 > 498.7 -> `capacity_infeasible`, its four lighter options <= available -> `capacity_risk`. `deli-deficit-inf` records a deficit org (lower-is-better latency, cap 30.0, load 0.9 -> available 29.1); its three heavy options record 30.0 > 29.1 -> `capacity_infeasible`, its four lighter -> `capacity_risk`. Both keep `reason` at-capacity / deficit from the org-level rule (agreeing with each org's Q9 `capacity_planning_attention` BY CONSTRUCTION). The marker is still a LABEL — a name on the trade-off, never a choice: no option removed, no re-rank, no overrule of the §6 human — the Q8 recommendation provably stays `partial-settlement`.

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

## §16 verdict

**Sprint 28's frontier is closed: the Q7/Q8 `capacity_constraint` marker can now reach `capacity_infeasible` for a SPECIFIC option, from a RECORDED per-option requirement and recorded available number only.** A new REPLAYABLE recorder `record_capacity_requirements` appends the per-option requirement map on the SAME authority:// object as the recorded `capacity` — so AVAILABLE = recorded capacity VALUE − recorded load, unit-coupled by construction — and the block labels an option `capacity_infeasible` iff its recorded requirement > available, else `capacity_risk`. Proven on real orgs: `deli-infcap` (at-capacity; heavy 499.0 > 498.7 -> infeasible) and `deli-deficit-inf` (deficit; heavy 30.0 > 29.1 -> infeasible), each with some `capacity_risk` and the baseline never flagged. It is still a LABEL and only additive data: no option is removed, the frozen `rank`/`machine_eligible_best`/`cockpit_q7q8` are untouched, the §6 human always rules — the Q8 recommendation is provably UNCHANGED even when a SPECIFIC option is infeasible. Orgs that record NO per-option requirement keep the Sprint-28 block byte-identical (strict superset; no `per_option_requirements`/`available_capacity` key). **Still not derivable (the honest frontier):** a genuinely capacity-constrained OPTIMIZATION that RE-RANKS the recommendation for the machine stays out of scope of the deterministic advisory stance (the marker never CHOOSES), and a per-option requirement that is NOT unit-coupled to the capacity remains non-derivable (an org with no recorded capacity value/load, or an option with no recorded requirement, carries no infeasibility label — the engine never invents one).

_Additive; frozen ontology, SPEC v0.22, 49 $defs, URI cap. A RECORDED per-option capacity requirement now lets the marker name a single infeasible option; it never re-ranks, never removes, never overrules the §6 human or the floor-gated recommendation._
