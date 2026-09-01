# Sprint 17 — findings (dated)

**2026-09-01 (Sprint 17 build — decision learning at the reconcile layer: the learned rule, honest
+ additive)**

- **A bounded, evidence-gated parameter learner at the reconcile layer is a clean additive feature —
  and it is honestly CALIBRATED RE-AUTHORING, not autonomous learning.** `learn_threshold(prior,
  realized, lr, [lo, hi])` moves the reconcile `threshold` toward a recorded realized outcome value
  by `lr·(realized − prior)`, clamped to an explicit `[lo, hi]`, flagged `changed` only when
  `|delta| >= eps`, deterministic (depends only on the explicit inputs, never the wall-clock). It
  learns the RULE's parameter, never the answer to a case. That is the truthful name for this:
  a bounded author (the calibrator) updating a rule parameter from outcomes. It does NOT move Trust,
  does NOT edit `determination_policy`, does NOT rewrite history — all asserted, not claimed.
- **The realized-outcome → threshold signal is defensible and produces a real, meaningful move.** When
  a determination actually holds at support the bar demanded more of (realized 0.90 < prior threshold
  0.95), the threshold was too strong (it risks UNRESOLVED on valid-but-moderately-evidenced
  disputes) and is LOWERED toward the realized value. Episode A (winning support 0.97) under 0.95 →
  0.90 realized → learned **0.91**. Correct direction, explicit why, clamp-bounded.
- **The learning→library→future-dispute flow is real (2 DISTINCT disputes, not a re-run).** The
  learned rule is a NEW named `RULE_LIBRARY` spec `calibrated-threshold-091` (aggregate `max` +
  additive `learned_threshold`/`calibrated_from`/`bound`/`why`), recorded as an append-only signed
  `rule://…/reconcile-rule` (kind=PROCEDURE) + `decision://…/reconcile-learning` (`rules_applied` →
  the rule). Episode B (`inspect-learn-b`, a genuinely DIFFERENT predicate set — its claim/evidence
  URIs are disjoint from A's, so it is not the same case re-run) is driven once under the learned rule:
  winning-claim support **0.93** → the OLD 0.95 leaves it UNRESOLVED (`determined=[]`, uncertainty
  True); the LEARNED 0.91 DETERMINES `rework-partial-credit` (CLOSED). Cross-dispute flip, only the
  learned threshold differs (verified as a derived reconcile of the SAME evidence under the old rule).
- **Containment held under real assertion, including a genuine ledger-append proof.** Event count
  grew 13 → 15 and every PRIOR event was byte-identical (`hashA0 == hashA1[:13]` element-wise) —
  real append-only, no rewrite. The trust:// scores stayed 0.80 everywhere (S5 only);
  `determination_policy` was byte-identical before vs after learning and no learning decision carries
  such a key; each determination kept its configured `authority://`. A bug I caught early: comparing
  ledger append-only by slicing a JSON *string* at a char count is nonsense (compares unrelated bytes) —
  the correct proof is element-wise: `entries_before == entries_after[:n_before]`.
- **The learned artifact validates cleanly on the FROZEN catalog — no new noun, no schema edit.**
  `rule://` maps to the frozen `Rule` $def (kind=PROCEDURE, required `[uri, kind, text]`),
  `decision://` to `Decision` ($def required `[uri, by, authority]`, with a built-in `rules_applied`
  ref), and `event://` to `Event`. Conformance `conformance_adjudication.py` now validates **16 labels**
  (13 prior + `inspect-learn-a`, `inspect-learn-b`, `deli-learn`) C1–C5 ALL PASS, 49 `$defs`; the new
  fixtures mint only catalog schemes (incl. `rule`). Additive keys avoided the C2 temporal-suffix trap
  (`realized_why`, `calibrated_from`, `bound` — none end in at/time/due/since/…).
- **Config footguns repeated this sprint:** `Graph.get()` takes ONE positional arg (use `(g.get(u) or
  {})`); `eng.reconcile(sub, cfg)` arg ORDER (I passed them swapped once and got a confusing
  `'Substrate' object is not subscriptable`); building a shallow clone of a shared config dict and
  mutating a nested sub-dict corrupts the SHARED original (deep-copy `unresolvable` per batch); a
  `set(generator_of_lists)` raises `TypeError: unhashable type: 'list'` (compare claim/evidence URI
  sets instead).
- **Invariants held.** SPEC hash `d10f00107b5d7eb4` (v0.22), schema json hash `7fc38c8c0a6e5b76`
  (49 `$defs`), `ros/` + schema source git-clean; full non-regression green (rule_library / authoring /
  comparison / adj_engine, the 4 prior CR demos + conformances, sectors build_all + conformance_all,
  S5 reference demo + conformance, agent demo + conformance — all exit 0).

## Decisions recorded (boundary of what the machine may and may not move)
- Keep SPEC v0.22 (capability/build change, no normative gap → PROTOCOL). No schema edit; the learned
  rule rides the frozen `Rule` $def + additive params; the learning layer is data + a small pure
  stdlib module under `instances/contested_reality/`.
- The learned rule is added to `ac.RULE_LIBRARY` at runtime in the runner and reused by `is`-identity
  on the future dispute (B) AND a cross-org (`deli-learn`) — the library grows from learning, and a
  learned entry is provably a reusable named spec, not a one-case patch.
- **Honest verdict: CALIBRATED RE-AUTHORING, not autonomous learning.** The machine may deterministically
  recalibrate a reconcile parameter within explicit bounds and record it as an append-only, reusable
  library artifact; it may NOT move Trust (S5 only), may NOT edit `determination_policy` (the §6
  human's authoritative call), and may NOT rewrite the ledger. That boundary is asserted by the demo.
- `ros/` untouched; the layer is entirely `instances/contested_reality/`.