# SPRINT 1 — SUMMARY

**Project:** RelationalOS | **Spec:** v0.17 → **v0.18** | **Date:** 2026-09-01
**Result:** Sprint 1 complete — S1 substrate + S2 Intent/Matching minimum built and **verified**.

## What was built (all under `sprints/sprint-1/artifacts/`)
A runnable Python service (`ros/` package) implementing the S1→S2 loop for **one role
(customer)** on **one domain (Quoteko quoting/triage)** for a fictional company
(`org://quoteko`) with three vetted contractors.

- **1.1 S1 substrate (thin)** — `ros/s1.py`: `resolve_identity` (via an `entity://`
  canonical record), `authenticate` (attestation-based verif score), `authorize`
  (**capability-based** per §7B, delegation-aware, revocation voids capability),
  `resolve_role` (relationship attribute per §C2).
- **1.2 S2 Intent/Matching** — `ros/s2.py`: `infer_intent` (need + capability keys +
  urgency, recorded as a `decision://` — no new URI noun) and `match_offers`
  (**Trust-weighted per §5**: `fit × scoped Trust`, trust floor, signed Event per
  match). **Human-escalation floor** engages: the customer must record a signed
  acceptance before an irreversible hire is committed (§6/§7B).
- **1.3 Ledger/Graph wiring** — `ros/substrate.py`: content-addressed (SHA-256 over
  prev-hash + payload), signed, RFC3339, preserve-unknown; **Ledger = history / Graph =
  state** kept distinct (§3.16); `ros/checks.py` round-trip check rebuilds the Graph
  from the Ledger.

## Verified output (ran this sprint, real tool output)
- `run_demo.py` → **exit 0, ALL PASS**: identity `person://qk/customer`, role `customer`,
  Trust-weighted ranking `o-norcrete 0.92 / o-solarworks 0.61 / o-generalco rejected
  (trust 0.42 < floor 0.5)`, human accepted `o-norcrete`, status `COMMITTED`; S1 check
  (6/6 pass incl. revocation-int→denial) and round-trip check (3/3 pass).
- `run_s1_conformance.py` → **exit 0**: Sprint-1 fixtures **28 instances ALL PASS**
  (C1–C5) through the **reused** Sprint-0 validator; then Sprint-0's own **156 fixtures
  non-regression ALL PASS**.
- `SPEC.md` re-verified: all 26 numbered section headings intact after patching; version
  bumped 0.17→0.18; Version/Review Log entry appended.

## What the spec gained (v0.17 → v0.18)
- **URI cap / frozen ontology respected** — no new nouns, no new URI schemes. Schema
  artifacts (`sprints/sprint-0/artifacts/schema/`) left unchanged (still v0.17).
- One normative clarification added to **§3.4** (finding F6): delegation/consent `scope`
  is URI refs to `rule://`/`permission://` objects carrying `grants`, never bare
  strings; a `REVOKED`/`EXPIRED` delegation voids the capability. Found by a genuine
  build failure against the (correct) schema, then fixed in the implementation.
- Full findings: `sprints/sprint-1/notes/findings.md` (F1–F6).

## Open issues / notes
- **Defined of Trust is S2=ranked by seeded scoped Trust (T1), not yet updated by S5 —
  that is Sprint 2.** The trust floor and §5 `score = fit × trust` stand in; the engine
  to *write* Trust from verified outcomes is next.
- **Release mirror not synced** (`~/Documents/ai-relational-os-spec.md/.pdf`) — optional
  step, left for when a release copy is wanted (consistent with Sprint 0).
- Subagents were NOT used (mandatory single-threaded rule honored); the Sprint-0 venv
  was reused as the runtime (it carries jsonschema/yaml for the conformance validator).
  Budget ~$0 (local computation only; no web/API spend).

## Hand-off
`/home/rlg/relational-os/sprints/sprint-2/PROMPT.md` written (Trust engine minimum) and
echoed as this sprint's final message. Ready for a fresh `/new` session to run Sprint 2
against the now-0.18 spec.