# §7L recorded-capacity CONSTRAINT on the Q7/Q8 trade-off — engine-native render (Sprint 27)
generated 2026-09-01T05:08:28Z  |  `adjudication_engine._capacity_reason`/`cockpit_s7l`  |  recorded authority `capacity` {value, unit, load} + the record-wide horizon band (band_horizon) + the recorded threshold -> an additive `capacity_constraint` block on Q7 AND Q8, emitted ONLY where a numeric capacity + band + threshold are recorded. It names the recorded capacity/load/band, derives ONE reason (headroom / at-capacity / deficit) from recorded numbers only — the SAME rule as the Sprint-26 Q9 capacity_planning_attention label (shared `_capacity_reason`, agree by construction) — and in `options_flagged` marks capacity-consuming non-baseline options `capacity_risk` when _not_ headroom (NEVER `capacity_infeasible`: no per-option requirement is ever recorded). A label/default, never a removal, never a directive; the Q8 recommendation is provably UNCHANGED. Additive; the capacity org carries ONLY this block; no-capacity orgs are byte-identical.  |  SPEC v0.22, 49 $defs, URI cap

The recorded capacity now reaches the §7L Q7/Q8 trade-off as a data-only REASON: the org's recorded capacity/load and the whole-horizon recorded band are named ON the trade-off, and any option the recorded numbers put at- or over-capacity is flagged `capacity_risk` — never removed, never re-ranked, never overruling the §6 human. When the recorded data shows headroom (as here: capacity 500 ≫ horizon 0.62…1.02, load 0.72), no option is flagged. The Q8 recommendation + machine-eligible best stay the frozen `rank` output.

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

Q8 capacity_constraint: reason=headroom  flag=False  recorded_capacity=500.0 resolutions/day (load 0.72)  horizon_band={'low': 0.62, 'high': 1.02}  options_flagged={}
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

## §16 verdict

**The recorded capacity now reaches the Q7/Q8 trade-off as a data-only REASON.** Where the org records a numeric `capacity` (plus a band + numeric threshold), both Q7 and Q8 carry an additive `capacity_constraint` block naming the recorded capacity value/unit/load and the horizon-wide recorded band, with one deterministic REASON derived from recorded numbers only via the SAME shared rule as the Q9 `capacity_planning_attention` label (agree by construction): headroom / at-capacity (load >= 1.0) / deficit (horizon worst-side >= capacity value). In headroom no option is flagged; at at-capacity/deficit the capacity-consuming non-baseline options are marked `capacity_risk` — never `capacity_infeasible`, because a per-option capacity requirement is never recorded. It is a label/default: it NEVER removes an option, NEVER changes the frozen `rank`/`machine_eligible_best`, and NEVER overrules the §6 human — the Q8 recommendation is provably UNCHANGED (asserted EQUAL to `cockpit_q7q8` for every org, and the Q7 option set unchanged). The default is byte-identical: a no-capacity / no-band / no-data org carries NO `capacity_constraint` key. **What is still not derivable (the honest frontier):** the marker is a reason, not a choice — it never CHOOSES a different option for the machine (the §6 human always does), and a genuinely capacity-constrained optimization that RE-RANKS the recommendation stays explicitly out of scope of the deterministic advisory stance (it cannot, without a recorded per-option capacity requirement, ever reach `capacity_infeasible`).

_Additive; frozen ontology, SPEC v0.22, 49 $defs. `capacity_constraint` labels what the recorded capacity makes risky on the trade-off; it never overrules the §6 human or the floor-gated recommendation._
