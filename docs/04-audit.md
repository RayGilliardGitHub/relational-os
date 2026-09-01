# 04 — AUDIT (produce the integrity audits)

**Audience:** auditor / engineer. **Goal:** produce and understand the integrity audit
that exists **today**, and see honestly what is still future.
**Grounding:** SPEC §7F (the audit *layer*), §3.16 (Ledger/Graph contract), §2, and the
conformance validator. Every command below was executed in Sprint 6 with real output embedded.

---

## 1. What an "integrity audit" means in this system

The system's data is split into **history** (append-only, content-addressed, **signed**
ledger) and **state** (graph). An integrity audit checks that:

1. the **ledger hash-chain and signatures** are intact (nothing was tampered with or
   re-ordered — §2/§3.16);
2. the **whole Graph rebuilds from the whole Ledger** (state is a faithful projection of
   history — §3.16 full-coverage rule);
3. every **instance conforms** to the schema, the URI catalog, and RFC 3339 temporal rules
   (§2, Appendix C);
4. unknown fields **round-trip** (they survive any re-write — §2);
5. the **state machines** (Relationship, Case) move only by legal transitions (§3.16, §7J.3).

Together these are **the integrity audit today**. SPEC §7F also specifies a larger
*continuous audit service* (an auditor actor scanning every entity, emitting signed
`audit_finding://` events into a remediation queue) — that is **spec'd, NOT built** in
Sprints 0–5. This manual gives the concrete runnable harness that provides the audit
*checks* today, and maps each §7F.1 check class to the exact check that covers it (the
"today vs future" table is §4).

## 2. The three runnable audit procedures

### 2.1 Ledger integrity — `Ledger.verify()` (hash-chain + signatures)

Exercised by the daily cockpit itself; you do not need extra tooling. After running
`reference/run_s5_demo.py` (`03-run.md §1`), the closing wiring lines are the audit's first result:

    cd /home/rlg/relational-os/reference
    python3 run_s5_demo.py

Real output (embedded):

    --- Ledger / Graph wiring ---
      ledger hash-chain + signatures: OK | entries 97
      graph current-state objects: 160
    RESULT: ALL PASS

`Ledger.verify()` re-derives every entry's `SHA-256(prev_hash ‖ payload)`, checks each
`signature`, and confirms `head_hash` — any break is reported as a chain break at a specific
`event_id` (implementation: `ros/substrate.py`).

### 2.2 Full-state round-trip (whole Graph rebuilds from whole Ledger)

Also reported by the demo's `[check:roundtrip]` trio. Real output (embedded):

    [check:roundtrip] full Sprint-5 state (whole Graph rebuilds from the whole Ledger, §3.16)
      [PASS] ledger hash-chain + signatures intact  — ok
      [PASS] graph state reconstructs to ledger events  — 160 graph objects rebuilt from 97 events
      [PASS] ledger==history & graph==state (not conflated)  — history=True, state-objects=True

The middle check replays every ledger `state_update` into a rebuilt graph and requires
**every current-graph object to be covered** — a missing object means an event that should
have changed state is absent (the §7F "Ledger↔Graph agreement" class). The third check is the
§3.16 **conflation guard**: ledger entries carry `hash`/`signature` (history), graph objects
carry typed URIs and no hashes (state).

### 2.3 Schema / instance / chain / roundtrip / statemachine conformance (C1–C5)

The conformance validator is the system's schema-and-integrity gate. Run it over all six
generations (`.venv` interpreter, any cwd):

    cd /home/rlg/relational-os/reference
    /home/rlg/relational-os/.venv/bin/python schema/run_conformance_all.py
    → exit 0, "RESULT: ALL PASS"

Real head (embedded) — note how each check class maps to a concern:

    === [gen-0] data/fixtures/gen-0 ===
      [PASS] C1 schema structurally valid  — 49 $defs
      [PASS] C2 all fixture instances validate + schemes + RFC3339  — 156 instances
      [PASS] C3 ledger content-addressed + signed
      [PASS] C4 round-trip preserve-unknown
      [PASS] C5 state-machine sequences legal

The five checks: **C1** schema structurally valid (draft 2020-12, 49 `$defs`); **C2**
per-instance schema + Appendix-C URI-kind compliance + RFC 3339 temporal (jsonschema ships no
date-time checker, so conformance enforces RFC 3339 itself); **C3** ledger content-addressed
SHA-256 chain + signature presence; **C4** round-trip preserve-unknown (an unknown field must
survive a parse→dump rewrite — `additionalProperties: true`); **C5** Relationship and Case
state-machine legality.

## 3. A representative PASS and how to read a FAIL

A FAIL in any check is **not a documentation typo** — this is a deterministic local build with
no moving external parts; every PASS above repros. A `[FAIL]` means one of:
- **C2** — a fixture instance violates its `$def`, uses a URI outside the Appendix-C catalog,
  or has a malformed RFC 3339 timestamp (the message names the object and the offending field).
- **C3** — a ledger hash-chain break or an unsigned event (the message names the `event_id`).
- **C4** — round-tripping is broken (unknown fields dropped).
- **C5** — an illegal Relationship/Case state transition.
- **C1** — the schema itself became structurally invalid (schema was edited).

All of these indicate the **workspace** changed (schema, `ros/` code, or a fixture), or a
venv/deps problem. Diagnostics in `07-troubleshooting.md`.

## 4. §7F.1 check classes → what covers them today vs future

SPEC §7F.1 lists nine check classes the audit layer looks for. Honest mapping:

| §7F.1 check class | Covered **today** by | Status |
|---|---|---|
| Schema conformance | conformance **C2** (schema + URI catalog + RFC 3339) | ✅ built |
| Ledger ↔ Graph agreement | **round-trip 2.2** + conformance **C3** | ✅ built |
| Referential integrity (no orphan URIs) | conformance **C2** (URI-kind compliance vs Appendix C) | ⚠️ partial — a true orphan scan is future |
| Timing anomaly (clock-order, dup IDs, chain discontinuities) | conformance **C3** (chain) + `Ledger.verify()` | ⚠️ partial — event-order/dup-ID scanning is future |
| Missing records (ACTIVE↔Consent, Commitment↔Expectation, …) | **none** | 🔮 future (needs the continuous auditor) |
| Trust setup (seeded, bounded, [0,1], recency) | `checks.s5_check` / `business_health_check` in the demo | ⚠️ partial (harness-level, per-scene) |
| Authority/Delegation completeness | `checks.s1_check` / `s3_check` / `escalate_check` | ⚠️ partial (per-scene asserts, not a sweep) |
| Evidence completeness & health | `checks.s5_check` (evidence anchored/grounded) | ⚠️ partial |
| Versioning integrity (gapless revisions) | **none** | 🔮 future |
| Security/compliance (disclosure linkage, revocations, reg data) | `checks.s1_check` (revocation voids capability) | ⚠️ partial |
| Per-entity **continuous** auditor + signed `audit_finding://` events + remediation queue (§7F.2) | **none** | 🔮 future deployment |

**Bottom line:** today's integrity audit **IS** conformance (C1–C5) + `Ledger.verify()` +
the full-state round-trip — all real, all exit 0. The always-on, per-entity continuous
auditor and its findings queue are specified (§7F) but NOT built; deploy them (per §G.14:
Great Expectations/dbt test + OPA/Rego + Prefect sweeps + `audit_finding://` output) when the
real graph/ledger store replaces the reference build.

## 5. Quick audit procedure (run this on demand)

    cd /home/rlg/relational-os/reference
    python3 run_s5_demo.py                                  # 2.1 + 2.2: ledger verify + round-trip
    /home/rlg/relational-os/.venv/bin/python schema/run_conformance_all.py  # 2.3: C1–C5 all six generations

Both exit 0, ALL PASS, when intact. That is the whole on-demand audit.

**Future deployment:** the always-on audit service (§7F), findings-as-signed-events, and the
remediation queue — see `01-system-manual.md §9`.