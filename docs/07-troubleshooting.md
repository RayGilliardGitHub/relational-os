# 07 — TROUBLESHOOTING & GLOSSARY (appendix)

**Audience:** operator / engineer. **Goal:** diagnose the common failure modes of the
reference build, fix them, and re-run cleanly; plus a glossary and the URI catalog summary.

---

## 1. Failure modes and fixes

> **Principle:** this is a deterministic, local, no-network build. There is no flakiness, no
> load, no external service. A non-zero exit or a `[FAIL]` means the **workspace changed**
> (schema/`ros/` code/fixture) or the environment (venv) is broken. Do not treat a FAIL as a
> transient. Diagnose below.

### F1. `ModuleNotFoundError: No module named 'conformance'` (or similar) on a conformance run
- **Historical cause (FIXED by the post-Sprint-36 reorg):** the conformance runners used to resolve the
  conformance validator by a relative path (`../../sprint-0/artifacts`) against the **current working
  directory**, so they only worked from inside the `artifacts/` directory.
- **Now:** the runners are re-anchored to `Path(__file__)` and are location-independent — run
  `python3 tests/run_checks.py` (full gate) from anywhere, or a conformance runner from the repo root.
- **If it still fails today:** the `conformance venv` is missing/broken (rebuild per `02-setup.md`) or the
  workspace changed — a FAIL is a real regression, never a transient (see the principle above).
- **Historical repro (Sprint 6, pre-fix):** the first attempt from `/home/rlg/relational-os` failed with
  exactly this error; running from the artifacts dir exited 0.

### F2. `ModuleNotFoundError: No module named 'jsonschema' / 'referencing' / 'yaml'`
- **Cause:** you ran a **conformance** runner with plain `python3` instead of the Sprint-0
  venv interpreter, or the venv is missing/deps removed.
- **Fix:** use `/home/rlg/relational-os/.venv/bin/python` for any
  conformance run (demos use plain `python3`). If the venv is broken, recreate it:
      cd /home/rlg/relational-os/schema
      python3 -m venv .venv
      .venv/bin/python -m pip install jsonschema referencing pyyaml
- **Verify:** `.venv/bin/python -c "import jsonschema, referencing, yaml; print('deps OK')"` → `deps OK`.

### F3. A conformance check prints `[FAIL] …`
- **C2** — a fixture instance violates its `$def`, uses a URI outside the Appendix-C catalog,
  or has a malformed RFC 3339 timestamp. The message names the object and (for temporal) the
  offending field.
- **C3** — ledger **chain break** or an **unsigned event**; the message names the `event_id`.
  This is the serious one (§3.16 integrity). If you edited a fixture or an emitted ledger,
  restore it; the chain only verifies when un-edited.
- **C4** — round-trip preserve-unknown broken (an unknown field was dropped on rewrite).
- **C5** — an illegal Relationship/Case state transition.
- **C1** — the schema became structurally invalid (it was edited).
- **Meaning:** this is a **real regression/corruption**, not a typo in these docs — the same
  code has passed deterministically across all earlier runs. Find what changed (see F5).

### F4. The demo (`reference/run_s5_demo.py`) exits non-zero or prints `FAILURES PRESENT`
- Same principle: the demo asserts real invariants (authz, ledger/round-trip, Trust flywheel
  re-ranking, §6 human floor order in the ledger, settlement artifacts, BOL lifecycle).
  A FAIL is a real regression — likely an edited `ros/` module, schema, or fixture, not a
  transient. Identify via the `[FAIL] …` line's `why` text.

### F5. How to re-run cleanly (get back to a known-good gate)
Conformance is the authoritative gate. Restore a clean workspace (or your working copy), then:

    cd /home/rlg/relational-os/reference
    /home/rlg/relational-os/.venv/bin/python schema/run_conformance_all.py   # expect ALL PASS
    python3 run_s5_demo.py                                 # expect ALL PASS, exit 0

If you have no local edits and still see a FAIL, snapshot and report it — it is a genuine
issue (the released reference build passed all six generations: gen-0 156 / -1 28 / -2 35 /
-3 55 / -4 174 / -5 316 instances).

### F6. The cockpit report is stale or missing
- **Cause:** `reports/cockpit.md(+.json)` are **outputs** written by `reference/run_s5_demo.py`.
- **Fix:** re-run `cd /home/rlg/relational-os/reference && python3 run_s5_demo.py`;
  it regenerates `graph/current-state.json`, the ledger fixture, and the reports in place.

---

## 2. Glossary

| Term | Meaning (cite) |
|---|---|
| **Actor** | Person / Organization / Agent / System — every entity that acts (SPEC §3.0). |
| **Relationship** | A durable bond, potentially years, holding many interactions (not a transaction) (§3.16). |
| **Interaction / Event / State** | A discrete episode; its atomic record; current relational truth (§3.16). |
| **Ledger / Graph** | History (append-only, content-addressed, signed) / State (current truth). Never conflated (§3.16). |
| **Content-addressed** | Each ledger entry's `hash = SHA-256(prev_hash ‖ payload)`; tampering breaks the chain (§2, §3.16). |
| **S1–S5** | Identity/Auth/AuthZ; Intent/Matching; Orchestration/Execution; Exchange/Settlement; Trust engine (§4). |
| **Business Operating Layer (BOL)** | Goals, Metrics, Cases, Exceptions, Tasks, Priority, Dependency (§7J). |
| **Case** | Universal unit of unresolved business work; lifecycle OPEN…CLOSED (§7J.3). |
| **Exception** | EXPECTED→ACTUAL→VARIANCE→…→VERIFIED heartbeat; additive field on `case://` (§7J.2). |
| **Priority** | f(impact, urgency, confidence, irreversibility, relationship-importance, cost-of-delay) (§7J.5). |
| **Trust** | Scoped, keyed `(subject, target, claim, context)` — never a global score (§3.14). |
| **Trust flywheel** | Verified outcome → evidence → scoped Trust update → re-ranked next match (§5/Sprints 1–5). |
| **§6 human floor** | Irreversible/unknowable-cost actions escalate to a human before execution; provable from ledger event order (§6/§7A). |
| **Round-trip** | Unknown fields MUST survive re-write (§2, Appendix C). |
| **URI cap / frozen ontology** | Only `case:// goal:// metric:// task:// dependency://` added; derived values are additive fields, never new nouns (§7J.11, §C16). |
| **§7L ten questions** | The Business Indispensability Test: ten morning questions answered with evidence (§7L). |
| **Cockpit** | The daily surface: health, attention, AI recommendation (§7J.9). |
| **Do-nothing** | An explicit, costed option in every recommendation (§7K.1). |
| **§7F / §7G / §7H / §7E** | (Future) continuous audit service; BI warehouse; external gateway; frontends/IoT — see per-doc "Future" notes. |

## 3. URI catalog summary (Appendix C, frozen)

Only five first-class operating nouns were added (Sprint 0): `case:// goal:// metric://
task:// dependency://`. Everything else the operating layer needs — Exception, Priority,
Recommendation, capacity — is an **additive envelope field** on those objects; Learning is a
`decision://` + a `policy://` change. The broad catalog (identity / relationship /
domain-object) includes `person:// org:// agent:// system://`, `relationship://`,
`interaction:// event://`, `expectation:// claim:// evidence:// decision://`, `delegation://
consent:// dispute:// right:// obligation:// commitment:// rule:// purpose:// trust://
reputation:// resource:// asset://`, and more. New schemes MUST be additive (§C16) so
resolvers and round-tripping stay valid.

## 4. BI/audit cross-references
- Audit: produce the integrity audit → `04-audit.md` (real commands + §7F.1 mapping).
- BI: produce today's reports → `05-bi-reports.md` (projections + health table + §7G mapping).
- Owner's daily reading → `06-user-manual.md`.
- Stand up + read the cockpit in 3 commands → `QUICKSTART.md`.