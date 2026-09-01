# SPRINT 3 — SUMMARY

**Project:** RelationalOS | **Spec:** v0.19 → **v0.20** | **Date:** 2026-09-01
**Result:** Sprint 3 complete — S3 Orchestration & Execution (+ human-escalation floor)
built and **verified** end-to-end, with a full S1→S5 cycle on ONE relationship closing
the §5 flywheel.

## What was built (all under `sprints/sprint-3/artifacts/`)
Extends the Sprint-2 state (`s5_demo.build_s2()`, which itself reuses the Sprint-1 `ros/`
substrate + S5 trust loop) with the **S3 Orchestration** service, `ros/s3.py`:

- **3.1 commit → execute across the fleet.** `commit(offer, terms, authority) → commitment://`
  (§5 `commitment = agree(offer, terms)`, status AGREED); `orchestrate(...) → [Task]` decomposes
  the committed job across a 3-worker agent fleet (`agent://w-local` / `w-cloud` / `w-frontier`)
  over the §6 routing seam (local / private-cloud / frontier, Trust-weighted, deterministic —
  no speculative weights per §G.11); the split is recorded as a signed `decision://`. Each
  worker step is a **capability-gated** (delegation-bounded, §3.4/§7B) signed ACTION `event://`.
  DoD met: ≥2 agent-worker steps with signed decisions/actions on the Ledger (3 executed).
- **3.2 Human-escalation floor (irreversibility).** `release_final_payment` —
  `irreversible(failure)==true` OR `cost(failure)==unknowable` — **escalated** to
  `person://qk/approver` and NOT auto-executed; the signed human DECISION enumerated 4
  alternatives (release-in-full / hold-pending-inspection / release-partial / open-dispute)
  and committed the action; the irreversible ACTION ran only after that acknowledgement, and
  the Ledger recorded the escalation. A separate cheap reversible micro-action
  (`prepare_work_order_and_schedule`) auto-executed by a worker. Both §6 branches demonstrated.
- **3.3 Full S1→S5 cycle (one relationship).** `relationship://qk/cust-cxn`: S1 identity/role/
  authz → S2 intent/match (Trust-weighted) → S3 commit + fleet execute → 2nd S5 capture of the
  S3-executed OUTCOME as signed `evidence://` → scoped Trust update (solarworks 0.708→**0.806**)
  → S2 re-ranks the NEXT cycle (solarworks #1) — the loop closes.

## Verified output (ran this sprint, real tool output)
`run_s3_demo.py` → **exit 0, ALL PASS**:
- Sprint-2 checks re-pass unchanged: `s1` (6/6), `roundtrip` (3/3, Graph rebuilds from Ledger),
  `s5` (7/7), `flywheel` (3/3).
- New Sprint-3 checks: `s3` (5/5: commitment AGREED + signed, split decision, ≥2 worker steps
  signed+action-named), `escalate` (5/5: escalation precedes human; irreversible action NOT
  auto-executed — `split@22 < esc@25 < hum@26 < release@27`; approver-signed decision with ≥3
  alternatives; release only after the human commit), `loop` (5/5: S3 outcome → evidence → Trust
  0.708→0.806 → next S2 match solarworks #1; envelope fields carried; norcrete scoped untouched).
- Ledger hash-chain + signatures OK; 31 events; 56 graph objects.

`run_s3_conformance.py` → **exit 0**: reuses the Sprint-0 validator verbatim over all FOUR
fixture generations — Sprint-0 **156**, Sprint-1 **28**, Sprint-2 **35**, Sprint-3 **55** — ALL
PASS (non-regression proven by the same gate).

## What the spec gained (v0.19 → v0.20)
- **URI cap / frozen ontology respected** — no new nouns, no new URI schemes. Schema artifacts
  (`sprints/sprint-0/artifacts/schema/`, v0.17) left **unchanged** (validator not edited).
- Two genuine, additive normative clarifications added to **§6** (from F2/F4):
  (1) the human-escalation floor **overrides** the routing seam — the closed task keeps its
  capability `seam_tier` for audit while its executable `tier` is forced to a human until
  signed acceptance; (2) escalation compliance is auditable purely from the signed append-only
  Ledger event ORDER (the irreversible ACTION must follow the approver's signed DECISION,
  which follows an escalation DECISION) — no separate flag.
- Full findings: `sprints/sprint-3/notes/findings.md` (F1–F4). Version bumped 0.19→0.20;
  Version/Review Log entry appended.

## Open issues / notes
- The orchestration is deterministic local routing (no real model tier running); a real
  deployment binds `route_seam` to a LiteLLM router (§G.4) over local/private-cloud/frontier.
  The human floor is the same logic either way.
- One relationship, one role (customer) vs one org type (private) in this sprint; the
  multi-role/multi-org + Settlement (S4 `settle`/`evaluate`) is exactly Sprint 4.
- Release mirror (`~/Documents/ai-relational-os-spec.md/.pdf`) not re-synced (optional,
  consistent with Sprints 1–2).
- Subagents NOT used (mandatory single-threaded rule honored); Sprint-0 venv reused as runtime.
  Budget ~$0 (local computation only; no web/API spend).

## Hand-off
`/home/rlg/relational-os/sprints/sprint-4/PROMPT.md` written (Settlement S4 + multi-role/multi-
org extension) and echoed as this sprint's final message. Ready for a fresh `/new` session to
run Sprint 4 against the now-**0.20** spec (S4 = Settlement, DoD: one relationship across TWO
roles and TWO org types chained through the full loop).