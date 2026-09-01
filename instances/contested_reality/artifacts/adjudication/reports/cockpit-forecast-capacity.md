# §7L recorded-data Q6 forecast + Q9 capacity — engine-native render (Sprint 20)
generated 2026-09-01T06:27:57Z  |  `adjudication_engine.cockpit_s7l`/`render_cockpit_s7l`  |  recorded `metric://` realized-vs-expected series + additive `capacity` field  |  SPEC v0.22, 49 $defs, URI cap

An org that RECORDS the missing data on its own graph/ledger (a metric:// realized-vs-expected series + a capacity field on its authority://) gets a deterministic Q6 forecast and a Q9 capacity number, where the data exists; an org that has not recorded them keeps the honest no-data fallback. Both still pass the full §7L Q1–Q10 cockpit.

--- deli-forecast ---
```
# §7L Q1–Q10 cockpit (engine-native) — org deli-forecast
ACTIVE reconcile rule: best-reliability-threshold  |  source: registry  |  learned-this-run: False  |  why: unchanged
Q1. what happened?  state/events: 16 recorded events; dispute lifecycle OPEN->EVIDENCE_COLLECTION->CONTESTED->ADJUDICATION->RESOLUTION->ACCEPTED->EXECUTED->VERIFIED->CLOSED; status=RESOLVED lifecycle=CLOSED epistemic=RESOLVED_DETERMINED
Q2. what changed?  life cycle OPEN -> CLOSED; epistemic UNDETERMINED -> RESOLVED_DETERMINED; determination=partial-settlement; claim epistemic={'late': 'disputed', 'delivered': 'disputed', 'shipped': 'disputed'}; significance=determined
Q3. what matters?  prioritized attention (3): claim://deli-forecast/late — claim disputed (not DETERMINED); claim://deli-forecast/shipped — claim disputed (not DETERMINED); metric://deli-forecast/m-on-time [forecast] — forecast: projected to fall below 0.95 (target) — worst 0.8 at period 3 — recorded band 0.71…0.89 (± σ 0.09); worst side 0.71 below target 0.95 — horizon-wide recorded band 0.71…0.93 across 3 projection periods (band_periods/band_horizon, same recorded σ)
Q4. what is going wrong?  exceptions (0): none  |  reconcile conflict=True uncertainty=False
Q5. why is it going wrong?  root-cause [epistemic status]: late support=0.9 contested (not determined); delivered support=0.97 support-carrying (DETERMINED under the active rule); shipped support=0.92 contested (not determined)  |  under rule best-reliability-threshold (registry)
Q6. what if we do nothing?  project (holding the recorded trend) from last actual 0.86 + mean delta -0.02: period 1 -> 0.84; period 2 -> 0.82; period 3 -> 0.8  |  recorded variance -0.09
Q7. what are our options?  accept-customer-refund, accept-company-full-payment, partial-settlement, conditional-resolution, request-more-evidence, escalate, unresolved, external-adjudication  |  baseline unresolved  |  machine-eligible best: partial-settlement
Q8. what should we do?  recommendation partial-settlement (authority authority://deli-forecast/adjudicate; floor-gated ['accept-customer-refund'])  ->  determination partial-settlement
    trade-off / do-nothing expected-impact: forecast-driven do-nothing cost: metric://deli-forecast/m-on-time projects to worst 0.8 (period 3) below recorded target 0.95 by 0.15 — doing nothing lets the recorded trend deteriorate — recorded band 0.71…0.89 (± σ 0.09); worst side 0.71 below target 0.95 — the whole recorded spread is priced as bad — horizon-wide recorded band 0.71…0.93 across 3 projection periods (band_periods/band_horizon, same recorded σ) (baseline unresolved, priced=True, on-target=False) |  recorded band 0.71…0.89 (± σ 0.09, crosses=True)
Q9. who does it, authority/capacity?  adjudicator person://deli-forecast/adjudicator (authority authority://deli-forecast/adjudicate), obligated party org://deli-forecast/company, appeal authority://deli-forecast/adjudicate-appeal, actors 7, capacity 1.0 obligations (load 0.6)
Q10. did it work, what did we learn?  verified=True status=RESOLVED determination=partial-settlement; outcome=partial settlement on the contested delivery; SLA-breach credit applied; ledger noted; customer keeps the service; learning: evidence://deli-forecast/learning-note[conflicting delivery timestamps reach a determination only v…]
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

**Q6 and Q9 are now answered AS DATA for any org that records them.** A generically-driven org appends a realized-vs-expected `metric://` series and an additive capacity field to its own ledger (merge-not-replace, signed, immutable), and `cockpit_s7l.q6` projects a deterministic 'if nothing changes' forecast from the recorded values while `.q9` reports the recorded capacity — never the wall-clock, never an invented number. Where an org has not recorded them, the cockpit stays honest: Q6 says it cannot forecast, Q9 reports no capacity. The §7L morning cockpit is now data-grounded on every one of the ten questions WHERE the data exists; the honest remaining limit is that a no-data org cannot be forced to forecast or measured for capacity — the engine reports the recorded reality, it does not manufacture one. Q7/Q8 stay the Sprint-18 line (delegated by construction); #8 remains §6-floor-gated; the determination is the §6 human's call; S5 alone moves Trust.

_Additive; frozen ontology, SPEC v0.22, 49 $defs. Trust only moved by S5._
