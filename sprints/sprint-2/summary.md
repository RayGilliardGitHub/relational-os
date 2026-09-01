# SPRINT 2 — SUMMARY

**Project:** RelationalOS | **Spec:** v0.18 → **v0.19** | **Date:** 2026-09-01
**Result:** Sprint 2 complete — S5 Trust engine minimum (capture → verify →
update → flywheel) built and **verified** on the Sprint-1 Quoteko scene.

## What was built (all under `sprints/sprint-2/artifacts/`)
Extends the Sprint-1 S1→S2 substrate (`ros/` package reused) with the **S5
Accountability & Trust** service, `ros/s5.py`, wired to the shared Graph + Ledger:

- **2.1 S5 capture + verify** — `capture(outcome, provenance) → signed evidence://`
  and `verify(evidence, statement) → {claim, degree, procedure}` for ONE crisp,
  objective outcome class (**"roofing job completed by its committed deadline"**,
  verified via an anchored completion record per §3.17). Produces real `evidence://`,
  `claim://`, `expectation://`, and OUTCOME `event://` objects, all signed. Verify
  returns a bounded *degree* under a *procedure* — no capital-T truth overclaim.
- **2.2 S5 Trust update + write** — `update(Trust, evidence, weight, recency) →
  trust://` per §5 `T_{k+1}=clamp(T_k + alpha*(outcome_k−expectation_k)*evidence_k,
  0, 1)`, keyed `(subject, target, claim, context)` per §3.14 (NOT a global score).
  Cold-start T1 = Sprint-1 seeded `trust://`. Updated Trust is WRITTEN to the Graph
  + a signed STATE_CHANGE ledger event, carrying its update inputs
  (`expected/outcome/evidence/alpha/recency`) as additive envelope fields.
- **2.3 Trust re-ranks S2 (the flywheel)** — re-runs `match_offers` after the update.
  Equal-fit offers (both fit=1.0) re-rank purely by Trust.

## Verified output (ran this sprint, real tool output)
`run_s2_demo.py` → **exit 0, ALL PASS**:
- Capture/verify: `evidence://qk/job-norcrete` (ANCHORED, confidence 0.98), claims
  recorded; norcrete `on_time=False`, solarworks `on_time=True`.
- Trust update: **norcrete 0.92 → 0.528** (bad outcome, −0.392),
  **solarworks 0.61 → 0.708** (good outcome, +0.098), all clamped [0,1];
  **generalco 0.42 untouched** (different claim ⇒ scope, not global).
- Flywheel: match ranking flips `[norcrete, solarworks] → [solarworks, norcrete]`;
  score = fit×trust matches the equation output.
- Self-authored checks PASS: `s1` (6/6), `roundtrip` (3/3, Graph rebuilds from Ledger),
  `s5` (7/7), `flywheel` (3/3).

`run_s2_conformance.py` → **exit 0**: reuses the Sprint-0 validator verbatim over all
three fixture generations — Sprint-0 **156**, Sprint-1 **28**, Sprint-2 **35** — ALL PASS
(non-regression proven by the same gate).

## What the spec gained (v0.18 → v0.19)
- **URI cap / frozen ontology respected** — no new nouns, no new URI schemes. Schema
  artifacts (`sprints/sprint-0/artifacts/schema/`, v0.17) left **unchanged**.
- One normative clarification added to **§5** (finding F3): the persisted `trust://`
  object must carry its last update's inputs as additive envelope fields (auditable);
  `Trust.evidence` is an array of `evidence://` refs. Found by a genuine build detail
  (bare-string `evidence` failed C2), then fixed in the implementation.
- Full findings: `sprints/sprint-2/notes/findings.md` (F1–F3). Version bumped 0.18→0.19;
  Version/Review Log entry appended.

## Open issues / notes
- Trust updates are grounded on ONE objective outcome class in ONE relationship; the
  multi-class, multi-relationship, reputation-aggregation and dispute→adjudication
  paths remain the §7D-B "Trust closure" Phase-B scope (spec `§10.Q1–Q3`).
- `alpha`/`recency` are the §5 learning-rate parameters (same across both updates);
  the demonstrated rank change is driven by the seeded/verified evidence, not by
  hardcoding speculative weights (§G.11).
- Release mirror (`~/Documents/ai-relational-os-spec.md/.pdf`) not re-synced
  (optional step, consistent with Sprint 1).
- Subagents were NOT used (mandatory single-threaded rule honored); the Sprint-0 venv
  was reused as runtime. Budget ~$0 (local computation only; no web/API spend).

## Hand-off
`/home/rlg/relational-os/sprints/sprint-3/PROMPT.md` written (Orchestration S3 + human
floor) and echoed as this sprint's final message. Ready for a fresh `/new` session to run
Sprint 3 against the now-**0.19** spec.