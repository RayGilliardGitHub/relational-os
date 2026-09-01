# TRADE-OFF / BUSINESS-MODEL implementation — Sprint 11

The optimizer: **what does "better" mean here?** This experiment closes the last honest gap left
open by Sprints 9 and 10 — Scenario B gap#3 in `STRESS-TEST-SCENARIOS.md` and the SPEC §7K.1
"Trade-off / decision analysis" (options incl. do-nothing; decision support explains the trade-off,
not a bare pick). It lives alongside the dispute (Sprint 9) and conflicting-interest (Sprint 10)
experiments in `instances/contested_reality/`.

## What was added (additive only, no new noun, SPEC stays v0.22)
- **`tradeoff_model.py`** — a pure, deterministic, stdlib-only utility engine. For each
  adjudication option it computes a utility in [0,1] as a **documented weighted sum of five
  factors** (customer-SLA compliance 0.45, employee-interest satisfaction 0.20, manager/staffing
  satisfaction 0.15, accrued-leave utilisation 0.10, coordination cost 0.10) from the **recorded**
  constraint/interest data, minus a §6 floor penalty for an irreversible/unknown-cost option.
  The weights ARE the business model (§7K.1 "what 'better' means"); the ranking is then *computed*,
  not authored per case.
- **`run_tradeoff_demo.py`** — the runnable demo: a conflicting-interest scene (same numbers as
  Sprint 10: 30-min SLA, 3-agent floor, 12 leave days) → case OPEN → computed ranking → the human
  adjudicator selects WITH the ranking in view → an unknown-coverage variant where the **§6 floor
  binds** every staff-changing option → the human authorizes **UNRESOLVED** (Trust untouched) → an
  optional **real local model advisory** (Sprint-8 `agent_adapter`) proven contained.
- **`conformance_tradeoff.py`** — C1–C5 gate over `artifacts/tradeoff/fixtures`.

The trade-off rides the case as an **additive object in the frozen `Recommendation` $def shape**
(`by/for/options/includes_do_nothing/tradeoff/authority_required/confidence/expected_impact/decision`
+ a machine-readable `json` ranking). **No `recommendation://` scheme/noun** (not in the frozen URI
catalog); 49 `$defs` and the URI cap intact.

## The computed trade-off (real output, coverage KNOWN)
```
trade-off[permitted-conditional; sla≤30min; floor 3/3 agents; leave 12d; coverage_known=True]
  0.760  remote-with-coverage-plan   (sla=1.0 emp=0.6 mgr=0.9 leave=0.1 cost=0.4)
  0.690  side-manager                (sla=1.0 emp=0.0 mgr=1.0 leave=0.0 cost=0.9)
  0.640  do-nothing                  (sla=1.0 emp=0.0 mgr=0.8 leave=0.0 cost=0.7)
  0.340  side-employee               (sla=0.0 emp=1.0 mgr=0.0 leave=0.8 cost=0.6)
  => machine-eligible best: remote-with-coverage-plan (all-change-gated: False)
```
The machine's top is `remote-with-coverage-plan` — the same defensible middle the Sprint-10 human
adjudicator chose by hand, now **computed from the org's own numbers**. Notably `do-nothing` (0.64)
beats the SLA-breaking `side-employee` (0.34): do-nothing is never worse than breaching the customer
SLA. The human determination in the demo follows the top non-gated option (informed, not authored).

## The §6 floor (real output, coverage UNKNOWN)
```
trade-off[permitted-conditional; sla≤30min; floor 3/3 agents; leave 12d; coverage_known=False]
  0.640  do-nothing                        (sla=1.0 emp=0.0 mgr=0.8 leave=0.0 cost=0.7)
  0.490  side-manager FLOOR-GATED          (sla=1.0 emp=0.0 mgr=1.0 leave=0.0 cost=0.9)
  0.140  side-employee FLOOR-GATED         (sla=0.0 emp=1.0 mgr=0.0 leave=0.8 cost=0.6)
  0.005  remote-with-coverage-plan FLOOR-GATED  (sla=0.0 emp=0.6 mgr=0.2 leave=0.1 cost=0.4)
  => machine-eligible best: do-nothing (all-change-gated: True)
```
When remote-day coverage is unverified, every staff-changing option is unknown-cost → **floor-gated**:
the machine may not auto-select or execute it (§6). Its only eligible direction is `do-nothing`/
UNRESOLVED; the human authorizes **UNRESOLVED** (`epistemic_state=INSUFFICIENT_EVIDENCE`), the case
stays OPEN, and **Trust is untouched** (same safety as Sprints 9/10).

## The advisory model is contained (real local model output)
```
[advisory] real local model phi4-mini:3.8b-q8_0 pick: 'do-nothing' (confidence 0.7); advisory only
```
Recorded as an effect-free `decision://to/agent-advisory` (type DECISION, never an ACTION). Checks
prove it cannot set the determination (the human's UNRESOLVED stands), never wrote a `trust://`
object, and conserves the authority it holds (§7J.9). If the model picked a floor-gated option it
would be contained (flagged, not actioned). Parse + fallback-with-log — never a fabricated answer.
In this run the real model independently agreed with the engine's eligible pick.

## Verified commands (exit 0, ~$0, deterministic)
| command (from instances/contested_reality) | result |
|---|---|
| `python3 tradeoff_model.py` | RESULT: ALL PASS (self-check) |
| `python3 run_tradeoff_demo.py` | RESULT: ALL PASS |
| `<sprint-0-venv>/python conformance_tradeoff.py` | TRADE-OFF CONFORMANCE: ALL PASS (C1–C5, 49 $defs, 17 instances) |
| `python3 run_dispute_demo.py` / `python3 run_interest_conflict_demo.py` | ALL PASS (non-regression) |
| `conformance_dispute.py` / `conformance_interest.py` | ALL PASS (non-regression) |
| (from instances/) `python3 build_all.py`, `conformance_all.py` | ALL SECTORS PASS |
| (from agent_demo/) `python3 run_agent_demo.py` | RESULT: ALL PASS |
| (from sprint-5/artifacts) `python3 run_s5_demo.py` | RESULT: ALL PASS |

## Honest verdict
The trade-off is **semi-computed**: the *ranking* is computed deterministically from recorded
constraints/evidence, but the **weights and factor scores are the org's stated business model**
(authorship), exactly as §7K.1 anticipates — the optimizer must know what "better" means before it
can optimize. Defensibility therefore improved: the conflicting-interest determination is now
**informed by a reproducible, documented trade-off from the org's own numbers** and can be audited
(a different weight vector is a different, auditable business model), not "authored from thin air".
What is still not computed from recorded data alone is the *choice of weights* — that is an
organizational policy decision the machine cannot infer from current primitives. To make even the
weights emerge from data would need recorded outcome histories (realized costs of prior
arrangements) feeding a learned objective — see `notes/findings.md` and Sprint 12.