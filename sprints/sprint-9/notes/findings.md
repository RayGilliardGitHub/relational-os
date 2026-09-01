# Sprint 9 — Findings (contested-reality / dispute experiment)

Date: 2026-09-01.

## What was discovered / demonstrated
- **The three-layer epistemology runs.** A Fact (recorded event), a Claim (interpretation), and a
  Determination (operative decision) are three distinct objects and can be carried through a dispute
  lifecycle. Facts correctly ride `event://` (there is NO `fact://` scheme — a fact IS a recorded
  event), claims `claim://`, evidence `evidence://`, decision `decision://`, dispute `dispute://`.
- **The inviolable rule holds:** UNRESOLVED ("insufficient evidence") is reachable and is NOT treated
  as a forced winner — the key result the review demanded.
- **TRUST SAFETY is real:** an unresolved dispute does NOT advance Trust; only a well-evidenced
  determination does (via the deterministic S5 formula). This is the direct mitigation of failure
  F2 (bad evidence poisoning the flywheel) at its core.
- **Schema-safe by construction:** the frozen `Dispute.status` enum [OPEN, ADJUDICATED, RESOLVED] was
  untouched; the epistemic state (`UNDETERMINED` / `INSUFFICIENT_EVIDENCE` / `RESOLVED_DETERMINED`)
  is an **additive envelope field** — the project's established pattern. No new noun, no schema edit,
  SPEC stays v0.22. C1–C5 PASS with 49 `$defs`.

## Decisions
1. **Reuse the existing `dispute://`, don't add a `dispute://`-adjacent new noun.** Spec §3.13 already
   defines Dispute; the gap was runnable semantics + the missing epistemic states, which are additive.
2. **Epistemic state as additive fields, not new enum literals.** Keeps the frozen schema byte-identical
   while representing the three epistemic outcomes the reviews call for.
3. **Facts ride `event://`.** No `fact://` scheme exists in the URI catalog and none was added; a fact is
   a recorded event, per §3.16.

## Pitfalls discovered (worth recording)
1. **Schema required-field errors are the honest check, not noise.** Conformance caught that (a)
   Evidence `kind` is a constrained enum [OBSERVATION, TESTIMONY, RECORD, ANCHORED] (my `REASONED` was
   invalid → use TESTIMONY for manual attestation), (b) Evidence requires `source`, and (c) Dispute
   requires `about`. All fixed by conforming, not by editing the schema.
2. **State transitions must MERGE, not replace.** When recording an adjudication, passing a fresh dict
   `{"uri":..., "status":...}` REPLACED the dispute object and dropped its required `about`/`parties`/
   `evidence`/`claims`. Fix: spread the existing object first (`{**graph.get(uri), ...}`). This is a
   general RelationalOS lesson: an update to an existing envelope object must preserve required fields /
   preserve-unknown (§2).

## Honest limits (unchanged)
- This resolves a *contested fact* (delivery outcome), not a *conflicting interest* (the remote-work
  employee-vs-manager case remains unmodeled: interests, negotiation, constraint trade-offs).
- Appeal is not a full workflow; no autonomous agent; one dispute shape at reference scale.

## Spec impact
**None.** SPEC stays v0.22 — additive demonstration only, no schema edit, no version bump.