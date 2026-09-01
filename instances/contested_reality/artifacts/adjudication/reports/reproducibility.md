# §7L TWO-PATH DECISION SURFACE — REPRODUCIBILITY-AUDIT (Sprint 35)
generated 2026-09-01T05:31:06Z  |  `run_reproducibility_demo.py`  |  engine-free audit: `adjudication_engine.py` (hash a60f8f7…) + `capacity_rerank.py` (sha256 f7c6a185…) BYTE-IDENTICAL; schema 34264934…, 49 $defs, SPEC v0.22, no new noun.

## Host / platform (live)
- uname: Linux 7.0.0-30-generic x86_64 (node dad)
- python: CPython 3.12.3
- cpu count: 20

## Whole-catalog two-path determinism (rebuilt fresh in memory; NO fixture writes)
The two-path survey over the whole 22-org catalog is deterministic and EQUALS the Sprint-34 recorded results: taxonomy **12 ADVISORY-no-capacity / 6 ADVISORY-best-runnable / 4 RE-RANK = 22 orgs**, 22/22 advisory Q8 == `cockpit_q7q8` (never shadowed), 4/4 RE-RANK orgs pick a provably-distinct replacement ({'inspect-recorded': 'conditional-accept-with-guarantee', 'deli-recommend-infcap': 'conditional-resolution', 'deli-all-infeasible': 'unresolved', 'cove-recommend-infcap': 'authorize-generic'}), 18/18 non-firing orgs agree, floor integrity 22/22, two_path_surface identical on re-run, and the Sprint-31 tally (11/11) + Sprint-32 re-rank (4/4) + Sprint-33 13-org taxonomy ({5,4,4}) all reproduce from the SAME recorded data.

## Boundary-doc concrete claims verified (live)
- engine sha256 head-8 **a60f8f71** == recorded a60f8f7…
- capacity_rerank.py sha256 head-8 **f7c6a185** == recorded f7c6a185…
- schema .yaml sha256 head-8 **34264934** == recorded 34264934… (.json is 7fc38c8c — the documented hash is the .yaml)
- 49 $defs; SPEC v0.22

## Honest §16 verdict
Deterministic local reproducibility of the one-framework two-path decision surface across the whole catalog is VERIFIED on this host (~$0, real tool output only). The still-not-derivable residual is unchanged: a probabilistic/stochastic forecast (the recorded band is a spread, never a CI — nothing invents a distribution); a per-option requirement NOT unit-coupled to the recorded capacity / an option with no recorded requirement (never invented); and any §6-human choice that recorded data cannot machine-decide (the re-rank is POLICY-authorized, not a claim of objective best). No SPEC bump (v0.22).
