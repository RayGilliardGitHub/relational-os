# 2.3-PLAN — Trust re-ranks S2 (the flywheel)

## Goal
Re-run Sprint-2 `match_offers` after the 2.2 Trust write and show the ranking ordering
changes exactly as the §5 equation predicts (same fit, different Trust → different rank).

## Design
`match_offers` scores `fit(intent∩capability) × scoped Trust`, floor 0.5. For this
intent (keys `[roofing, repair]`) both norcrete and solarworks have **fit = 1.0**
(equal fit), so ranking is determined purely by Trust.
- Before: norcrete 0.92 (#1, score 0.92) > solarworks 0.61 (#2, score 0.61).
- After (from 2.2): solarworks 0.708 (#1, score 0.708) > norcrete 0.528 (#2, score 0.528).
- generalco 0.42 still < floor 0.5 (rejected both times) — and stays above the
  equation-clamp demonstration by remaining below floor.

Flywheel demonstrated: a verified good outcome raised solarworks above norcrete; a
verified bad outcome dropped norcrete below solarworks. Both remain ≥ floor so the
re-rank (not a drop-out) is what changes.

## Steps
1. Record "before" `match_offers` ranking using the seeded trusts.
2. Re-run `match_offers` with the post-update trusts read from the Graph.
3. Assert: solarworks moves #2→#1, norcrete #1→#2; final scores equal the equation
   outputs; the ordering change is monotone-consistent with `delta = alpha*(outcome−exp)`.

## Done
- Harness shows before/after Trust AND before/after S2 ranking and asserts the
  ordering changed as the equation predicts.