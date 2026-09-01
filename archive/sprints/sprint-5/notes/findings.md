# SPRINT 5 — FINDINGS (feeds the v0.22 spec update)

Collected during the Sprint-5 Business Operating Layer build (Quoteko scene, on the
Sprint-4 S1->S5 end-state). Real tool output only; single-threaded; ~$0 local computation.

## F1 — The operating layer is a PURE assembly: zero schema / ontology / URI change (confirms §7J.11 / §C16 / §7K.3)
The entire BOL — Case lifecycle, Goal/Metric, Task, Dependency, Exception heartbeat,
Priority, Recommendation, Q9 capacity, and Organizational Learning — was represented using
ONLY the existing `$defs` and the frozen URI set. Schema artifacts byte-identical (49
`$defs`); validator unmodified. Conformance re-validates over all SIX generations:
Sprint-0 **156**, Sprint-1 **28**, Sprint-2 **35**, Sprint-3 **55**, Sprint-4 **174**,
Sprint-5 **316** — ALL PASS, exit 0. This is the strongest confirmation of the URI cap:
- **Exception** (§7J.2), **Priority** (§7J.5), **Recommendation** (§7J.9), and Q9
  **capacity** are carried as **additive envelope fields** on `case://`/`task://`
  (each `$def` is `additionalProperties: true`) — no `exception:// priority://
  recommendation:// capacity://` URI, exactly as §7J.11 declares.
- **Learning** (§7K.1) is recorded as a `decision://` object (Decision->Expected->Actual->
  Variance->WHY->change-future-policy) + a future-policy change on a `policy://` — no new noun.
- **Dependencies** (`dependency://`) with a transitive impact analysis; **Capacity** shown
  in Q9 as an additive field (there is no `capacity://` scheme in the catalog).

## F2 — Signed state deltas must be IMMUTABLE snapshots (deep copies) (additive clarification to §5 / §3.16)
A Case that accrues state (its `history` lifecycle list) is a **single live object**. If a
transition does a SHALLOW copy (`dict(case)`) and appends to the shared `history` list, the
append mutates the case object already embedded in an EARLIER signed ledger event's
embedded `state_update` — so that earlier event's stored payload no longer matches its
content-address, and the §3.16 hash-chain breaks retroactively (verified: chain break at the
second S5 event; fixed by deep-copying every object into the signed event in the operating
layer's `state_update`). Generalizes the Sprint-1/Sprint-4 closure-copy convention: any
object that is **mutated after first signing** (Case history, updated Policy, re-scored
Metric) must be provided to the ledger as a **deep copy**, so each signed event is an
immutable snapshot. Addressed by a normative sentence in §3.16.

## F3 — Ledger projections round to the Metric's stated precision (operational, doc note)
`project_on_time` reads the signed completion OUTCOME events directly; the Metric stores
`actual` rounded to 3 decimals. The conformance projection check must round to the same
precision (tolerance-aware) — a bookkeeping precision note, not a spec change.

## F4 — The §7L acceptance test is now answerable end-to-end for one company (confirms §7L, §8 MVP / Sprint 5 DoD)
For Quoteko the ten morning questions are answered **with evidence from the ledger/graph**:
health (3 ledger-projected metrics), priority-ordered attention, an AI recommendation with
the authority it requires (#8 -> assigned authorized `task://` under `authority://`), #9
(owner + delegation-bounded authority + capacity), and #10 (a **verified outcome** — the
rallied, re-allocated solarworks delivery settled and captured/verified on time, forward-
period on-time = 1.0 — plus a **Learning** entry + updated `policy://`). This is the product
gate in §7L/§8: an operating system, not an architecture.

## F5 — The §6 human floor and the S1->S5 flywheel are intact under the operating layer (confirms, no change)
The BOL consumes, and does not disturb, the verified chain: all re-used Sprint-1..4 checks
(S1 authz, Ledger/Graph round-trip, S5 Trust flywheel, S3 orchestration + escalation-Ledger-
ORDER floor, S4 settlement + multi-role + multi-org) still pass unchanged on the full
Sprint-5 state (97 ledger events -> **160 graph objects** from a full-state rebuild). The
operating decisions (provider re-allocation Policy v2/v3) are ordinary signed `decision://`/
`policy://` changes; the irreversible settlement floor is untouched.

## F6 — Capacity is a Q9 answer but has no URI scheme in the catalog (additive clarification to §7J.5/§C16)
`capacity://` exists as a `$def` but is NOT in `x-uri-catalog` (unlike `risk://`, which is).
Q9 "capacity" is therefore expressed as an **additive field** on the assigned `task://`
(`assigned_capacity`) rather than a `capacity://` object. Addressed by a clarifying sentence
in §7J.5 noting capacity (like priority and exception) is carried as a derived/additive
field, not a new URI scheme.

## Net spec impact (v0.21 -> v0.22)
- **URI cap + frozen ontology: unchanged, respected** — no new nouns, no new URI schemes.
- **Schema + validator: NOT modified** (byte-identical, 49 `$defs`); conformance exits 0 over
  all SIX generations.
- Three additive normative clarifications:
  1. §3.16 — signed state deltas are immutable snapshots (deep-copied); a mutating operating
     object's changes must never retroactively alter an earlier signed entry (F2).
  2. §7J.5 / §C16 — Exception/Priority/Recommendation and Q9 capacity are additive fields on
     `case://`/`task://`; there is no `capacity:// priority:// exception:// recommendation://`
     URI scheme (F1/F6).
  3. §8 — the S1->S5 platform chain is marked COMPLETE; Sprint 5 (Business Operating Layer)
     built and verified, and the §7L test is answerable for one company (F4).
- Version bumped to **0.22**; Version/Review Log entry appended.