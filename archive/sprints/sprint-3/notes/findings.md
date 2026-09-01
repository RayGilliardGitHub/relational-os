# SPRINT 3 — FINDINGS (feeds the v0.20 spec update)

Collected during the S3 Orchestration + human-floor build (Quoteko scene). Real tool output
only. All executed single-threaded; no subagents; ~$0 local computation.

## F1 — The orchestration builds entirely on existing Sprint-0 contracts (confirms spec, no schema change)
`commit(offer, terms, authority) -> commitment://`, `orchestrate(...) -> [Task]` (recorded
as an existing-scheme `decision://`), `route_seam(task, trust) -> tier`, and per-worker
`execute_task` (signature ACTION `event://`) all run using ONLY the Sprint-0 `$defs`
(Commitment, Decision, Event, Actor, Delegation, Rule) and existing URI schemes
(`commitment:// decision:// event:// agent:// evidence:// claim:// trust:// relationship://
delegation:// rule:// authority:// person:// org:// offer://`). **No schema or ontology/URI
extension was needed** — the frozen ontology and §7J.11/§C16 URI cap held. The split plan and
worker steps embed in signed ledger events exactly like the Sprint-1/2 state-delta convention;
the Sprint-0 validator reuses verbatim (C1–C5, exit 0) over all four fixture generations.

## F2 — The human-escalation floor OVERRIDES the routing seam; the seam's tier must stay auditable (genuine clarification, additive to §6)
An irreversible/unknowable-cost task (release_final_payment) is still ROUTED by capability to
the best tier (frontier) by the seam, but its **executable** tier is overridden to a human by
the floor. These must be recorded separately (`seam_tier` = routed-to capability tier, kept for
audit; `tier` = governing executable tier = human until signed acceptance). A single "tier"
field conflates "where the model runs" with "who may execute". This is implicit in §6 but worth
making explicit so an audit can confirm both that the task was routed to best capability AND
was not auto-run. **Addressed** by a normative sentence in §6.

## F3 — Capability-based authz gated every worker step; no grant => no action event (confirms §3.4/§7B)
Each `agent://` worker executes only under ITS OWN bounded delegation (`delegation://` →
`rule://` grants); `execute_task` calls `authorize()` with the worker's delegation in the
context, so a worker attempting an action outside its grant yields a Denial and **no** ACTION
event is recorded. The fleet is therefore capability-bounded, not a privileged army (mirrors
the §7A-2 droid-army hedge at the agent level).

## F4 — Irreversibility compliance is auditable purely from Ledger ORDER (genuine clarification, additive to §6)
The strongest proof that an irreversible action was "NOT auto-executed" comes from the
append-only history alone: the irreversible ACTION event's index must be strictly AFTER the
approver's signed human DECISION event, and an escalation DECISION event must precede that
human commit (verified by the `escalate` check: `split@22 < esc@25 < hum@26 < release@27`). No
separate boolean flag is needed for enforcement — it is a property of the signed event order.
Worth stating as a checkable normative property.

## Net spec impact (v0.19 -> v0.20)
- URI cap and frozen ontology: **unchanged, respected** — no new nouns or URI schemes.
- Schema (`sprints/sprint-0/artifacts/schema/`): **NOT extended**; validator unchanged
  (still v0.17 artifacts, 49 $defs).
- Two additive normative clarifications added to **§6** (F2: the floor overrides the seam tier
  with `seam_tier`/executable `tier` kept distinct for audit; F4: escalation compliance is
  auditable from the signed append-only ledger event ORDER — the irreversible ACTION event
  must follow the approver's signed DECISION). Version bump to **0.20**; Version/Review Log
  entry appended.
- Conformance: Sprint-0 (156), Sprint-1 (28), Sprint-2 (35), Sprint-3 (**55**) — **ALL PASS,
  exit 0**, one shared validator (no regression over any generation).