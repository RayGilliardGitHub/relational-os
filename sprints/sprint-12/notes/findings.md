# Sprint 12 — notes / findings

Date: 2026-08-31.

## What the build surfaced
- **The 16-section review request mapped almost entirely onto things already built additively.**
  That is the headline finding: contested reality does not need a new ontology. Every demanded
  semantic is a native `$def` (Claim/Evidence/Dispute/Decision/Trust/Obligation/Right) or an additive
  envelope field (epistemic_status, interest/constraint blocks, conflict object, lifecycle_state,
  resolution_type, reopening flags, the `Recommendation`-shape tradeoff). 49 `$defs` + URI cap
  byte-identical; C1–C5 passes on every generation (now 4 contested-reality fixture sets).
- **The `evidence` refs on Claim/Decision/Trust are ARRAYS** (`evidence: [{ref}]`), not single
  strings — the validator caught the single-string error. Conform; don't edit the schema.
- **Epistemic status is a property, not evidence that changes.** Putting `epistemic_status` on the
  claim (not re-classifying evidence) keeps "whether the org determined it" separate from "what the
  evidence is" — exactly the review's insistence that Determination ≠ Evidence.
- **Reopen is additive and non-destructive.** A wrong determination is superseded by a new `decision://`
  (higher authority), with `supersedes` linking back; the original is never rewritten. This is the
  single cleanest proof that the ledger is history, not state.
- **Error vs deception is representable and cheap.** A `reliability_note` (signal) on evidence vs a
  Trust effect only via the S5 deterministic formula over an adequately-evidenced determination. The
  proof asserts an overturned *honest* claim does not depress scoped Trust.
- **UNRESOLVED is monotonically safe** — stays OPEN, no forced winner, Trust untouched, propagates
  (no determination → no remedy → escalate/external). This was already Sprint-9's invariant; the
  lifecycle proof re-asserts it as a *state*, not a prose note.
- **The real local model responded** on the lifecycle proof (`phi4-mini:3.8b-q8_0`, advisory pick
  `partial-settlement`), agreeing with the machine's top — and the containment assertions held.

## Decisions taken
- Made the review's 16 sections the shape of `DISPUTE-RESOLUTION-SPECIFICATION.md`; kept the final
  assessment honest (B — Partially) rather than claiming A.
- `epistemic_status` vocabulary on claims; lifecycle + epistemic additively on `dispute://`; the
  frozen `Dispute.status` enum untouched (OPEN/ADJUDICATED/RESOLVED) — added fields carry the rest.
- Emitted a legal `statemachines/dispute.json` walk (OPEN→…→CLOSED) for C5; the APPEALED/REOPENED/
  UNRESOLVED/SETTLED/ESCALATED states are additive lifecycle states, not schema transition rows.
- Repurposed Sprint 12 from the earlier "Decision Learning" idea to this lifecycle spec+proof (the
  review's request superseded it); decision-learning is carried forward to Sprint 13 open items.

## Honest limits / open gaps
- **Adjudication semantics are still per-scenario authored**, not a configurable engine. A different
  org's dispute still needs re-coding of the option set + utility weights (the value model is authored,
  per §7K.1's own acknowledgement). This is the main generalization work remaining.
- The trade-off/lifecycle is not yet rendered on the §7L cockpit Q7 surface.
- Decision Learning (realized-cost weights) from the Sprint-11 finding is still open.
- The verification `CONTESTED → ADJUDICATION` step currently embodies a *reconciliation rule of
  thumb* (an anchored third party outranks conflicting timestamps); a general conflicting-evidence
  weighting policy is not yet a configurable rule.