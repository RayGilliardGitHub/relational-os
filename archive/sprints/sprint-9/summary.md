# Sprint 9 — SUMMARY — Contested-Reality / Dispute-Resolution experiment

**What was built:** the smallest runnable demonstration that RelationalOS can *reason about contested
reality*, not just record it — the capability ChatGPT's review elevated to the #1 development priority.
It treats **Fact / Claim / Determination** as distinct layers, carries a dispute through a lifecycle on
the existing `dispute://` primitive, and upholds the **inviolable rule that UNRESOLVED ("insufficient
evidence") is a legal outcome** — while keeping Trust safe from weak/conflicting evidence.

## Verified commands — REAL output (all exit 0)
```
cd /home/rlg/relational-os/instances/contested_reality
python3 run_dispute_demo.py               -> RESULT: ALL PASS   (7 assertions)
<venv>/python conformance_dispute.py      -> DISPUTE-DEMO CONFORMANCE: ALL PASS  (C1-C5, 14 instances)
# non-regression
cd /home/rlg/relational-os/sprints/sprint-5/artifacts
python3 run_s5_demo.py                    -> RESULT: ALL PASS
<venv>/python run_s5_conformance.py       -> RESULT: ALL PASS
cd /home/rlg/relational-os/instances
python3 build_all.py                      -> RESULT: ALL SECTORS PASS
<venv>/python conformance_all.py          -> SECTOR CONFORMANCE: ALL SECTORS PASS
```

## What was demonstrated (REAL)
- **Fact/Claim/Determination separation:** recorded events (facts), parties' interpretations (claims),
  and the organization's operative decision (determination) are distinct objects.
- **UNRESOLVED is legal:** a dispute with two credible-but-weak conflicting claims (0.62 vs 0.58, gap
  0.04, no decisive third source) is adjudicated to **determination=UNRESOLVED, epistemic state
  INSUFFICIENT_EVIDENCE** — not a forced winner. (The inviolable rule.)
- **Trust safety (failure-F2 mitigation):** an unresolved dispute does NOT advance Trust; only a
  well-evidenced determination (third-party verify 0.97) does, deterministically:
  `0.500 + 0.5·(1−0.8)·0.97·1.0 → 0.597`.
- **Authority preserved:** determination is signed by the authorized adjudicator.
- **Schema-safe:** frozen `Dispute.status` enum untouched; epistemic state is additive fields
  (UNDETERMINED / INSUFFICIENT_EVIDENCE / RESOLVED_DETERMINED). No new noun, no schema edit, 49 `$defs`
  intact, SPEC stays v0.22.

## Honest boundaries
- **Demonstrated:** the system can hold two conflicting realities, record uncertainty, refuse to
  over-claim, and only let adequate evidence move the Trust it is built on. Minimum viable proof of the
  contested-reality frontier.
- **Not demonstrated:** the conflicting-*interest* case (remote-work employee-vs-manager with a shared
  SLA — interests, negotiation, constraint trade-offs are not yet modeled); a full appeal workflow; an
  autonomous agent as adjudicator; any production surface.

## Delivers (per the review roadmap)
- Executes the **re-prioritized #1** in `COMPLETENESS-GAP-ANALYSIS.md`: the contested-reality /
  dispute-resolution engine.
- Directly addresses ChatGPT's core finding: RelationalOS handles accountable execution well but
  contested reality poorly — the experiment is the first runnable evidence that the gap is reachable.
- Mitigates the review's F2 (conflicting evidence / trust-poisoning) at its root.

## Key files
- `instances/contested_reality/run_dispute_demo.py` — the experiment (both UNRESOLVED + RESOLVED paths).
- `instances/contested_reality/docs/CONTESTED-REALITY-EXPERIMENT.md` — the write-up.
- `instances/contested_reality/conformance_dispute.py`, `artifacts/`.
- `sprints/sprint-9/plan.md`, `work/1-plan.md`, `notes/findings.md`.

## Spec status
SPEC stays **v0.22**. Additive demonstration; no schema edit, no normative change, no version bump.