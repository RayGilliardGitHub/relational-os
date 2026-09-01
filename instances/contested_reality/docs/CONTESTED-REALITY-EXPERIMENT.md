# CONTESTED-REALITY-EXPERIMENT — Dispute & Resolution inside RelationalOS

**Sprint 9.** The experiment ChatGPT's review called for and elevated to the #1 priority: can
RelationalOS reason about *contested human reality* — not just record it — while preserving the signed
authority chain, AND with the inviolable right to conclude **UNRESOLVED**?

## The problem (from the review)

> RelationalOS currently handles accountable execution much better than it handles contested human
> reality. It can record disagreement, but cannot yet reason about disagreement.

Organizations live where parties disagree. The system's nouns (interest, conflict, dispute, negotiation)
exist, but the review's distinction holds: **having the nouns is not enough.** This experiment adds the
*runnable semantics* — while changing no noun, no schema, and no Verified service.

## What was built (smallest runnable form)

A self-contained engine at `instances/contested_reality/run_dispute_demo.py`, using the **existing
`dispute://` primitive** (spec §3.13, schema `$defs/Dispute`) and the real substrate + S5. It treats
three things as **distinct layers**, per the review's epistemology:

```
FACT          — an event was recorded (e.g. "GPS 04:12", "contract deadline 04:00")
CLAIM         — someone says the fact means X ("late" / "on time")
DETERMINATION — the organization decides what will be treated as operative
```

Facts ride `event://` (a fact IS a recorded event — no new scheme). Claims ride `claim://`,
evidence `evidence://`, decisions `decision://`, and the dispute itself `dispute://`.

## The inviolable rule (demonstrated)

> **The system MUST be able to conclude UNRESOLVED when the evidence does not justify a determination.**

Because the frozen `Dispute.status` enum is `[OPEN, ADJUDICATED, RESOLVED]` (a schema edit is forbidden),
the **epistemic state** is represented as additive envelope fields on the existing object —
`epistemic_state ∈ {UNDETERMINED, INSUFFICIENT_EVIDENCE, RESOLVED_DETERMINED}` + a string `resolution`
+ `determination`. This is exactly the additive-field pattern the project uses for
Exception/Priority/Recommendation — no new noun, no schema change, SPEC stays v0.22.

## What the run actually proved (REAL, all PASS)

Two dispute branches exercised:

**Branch 1 — UNRESOLVED (the inviolable case):** two credible-but-weak, mutually-conflicting claims
(customer testimony 0.62 vs supplier anchored GPS 0.58; gap 0.04). No independent decisive source.
- conflict detected (neither dominates)
- dispute OPEN, epistemic_state UNDETERMINED
- adjudicated → **determination=UNRESOLVED**, epistemic_state=INSUFFICIENT_EVIDENCE
- **TRUST SAFETY: an unresolved dispute is NOT fed to the trust formula** — weak or bad evidence
  cannot poison the flywheel (the review's F2 point: evidence-conflict is existential)

**Branch 2 — RESOLVED (the determined case):** independent third-party verification at degree 0.97.
- dispute RESOLVED, epistemic_state=RESOLVED_DETERMINED, determination="side-with-supplier"
- ONLY here does Trust advance deterministically: `0.500 + 0.5·(1−0.8)·0.97·1.0 → 0.597`
- determination signed by the authorized adjudicator (authority preserved)

## Verified commands (REAL output, all exit 0)

```
cd /home/rlg/relational-os/instances/contested_reality
python3 run_dispute_demo.py               -> RESULT: ALL PASS        (7 assertions, all PASS)
<venv>/python conformance_dispute.py      -> DISPUTE-DEMO CONFORMANCE: ALL PASS  (C1–C5, 14 instances)

# non-regression
cd /home/rlg/relational-os/sprints/sprint-5/artifacts
python3 run_s5_demo.py                    -> RESULT: ALL PASS
<venv>/python run_s5_conformance.py       -> RESULT: ALL PASS
cd /home/rlg/relational-os/instances
python3 build_all.py                      -> RESULT: ALL SECTORS PASS
<venv>/python conformance_all.py          -> SECTOR CONFORMANCE: ALL SECTORS PASS
```

## Honest assessment — what this does and does not prove

**Demonstrated:**
- The three-layer epistemology (Fact/Claim/Determination) is representable and runnable.
- The system can detect conflicting-but-weak evidence, open a disputed state with recorded
  uncertainty, and adjudicate to a determination **or honestly leave it UNRESOLVED** — the inviolable rule.
- **Trust is guarded:** only a well-evidenced determination advances Trust (deterministic S5 formula);
  an unresolved dispute leaves it untouched. This is the F2 fix at its core: bad evidence does not
  silently corrupt the flywheel.
- Authority preserved: the determination is signed by the authorized adjudicator.

**What this MINIMAL experiment does NOT yet do (honest limits):**
- **Interests/negotiation/constraint trade-offs** are still not modeled (the remote-work conflict's
  "employee vs manager interests under a shared SLA" remains out). This experiment resolves a
  *contested fact*, not a *conflicting interest*. **→ Addressed in Sprint 10:** the conflicting-
  interest (remote-work, Scenario B) case is now runnable — see the companion
  `docs/CONFLICTING-INTEREST-EXPERIMENT.md` (`run_interest_conflict_demo.py`), which models two
  interest objects under a shared SLA/staffing/policy constraint, a defensible conditional
  determination, the reachable UNRESOLVED outcome, and a first-class signed appeal re-adjudicated by
  a higher authority.
- **Appeal** is represented only as an existing-object attitude, not a full appeal workflow.
  **→ Partly addressed in Sprint 10:** an appeal is now a signed, queryable, re-adjudicated step
  (native `right://` type=APPEAL) in the conflicting-interest case.
- **No autonomous agent** — the adjudicator is a human; a model could *recommend* but does not yet.
- It is one dispute shape (contested delivery outcome), at reference scale, local.

## Conclusion

The review said the word **relational** "starts earning its place" only if RelationalOS can take a
messy, contested, multi-party situation and turn it into a defensible, evidence-backed resolution —
**while preserving authority, uncertainty, disagreement, and human judgment — and while allowed to
conclude UNRESOLVED.** This experiment demonstrates the minimum viable version of that: the system
can now hold two conflicting realities, record the uncertainty, refuse to over-claim, and only let
adequate evidence move the trust it is built on. It is the first runnable evidence that the
contested-reality frontier is reachable, and it identifies precisely what remains (interests,
negotiation, appeal) for the next step.