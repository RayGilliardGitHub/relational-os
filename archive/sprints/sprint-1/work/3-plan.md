# 1.3 PLAN — Ledger / Graph wiring check

**Spec refs:** §3.16 (Ledger=history, Graph=state — must not conflate), §2 (append-only,
content-addressed, signed), §5 (loop), §7C (graph+ledger implementation model).

## Goal
Show the §5 loop writing a full S1→S2 slice where **Ledger = history** (append-only
content-addressed signed events) and **Graph = current state** (the match + its
status), and prove the round-trip: current Graph state reconstructs to the Ledger
events that produced it.

## Design
- Ledger store (`substrate.append`) keeps an append-only, SHA-256 hash-chained,
  signed event log, each event carrying `event_id, correlation_id, causation_id,
  idempotency_key, signature, occurred_at, ledger_ref` (schema §Event) + a `hash`.
- Graph store (`substrate.state`) is the projection/current-state of the slice: the
  Relationship (status ACTIVE), the current matched `offer://` + its status, the
  intent decision, the human-verification record — i.e. "what is true now."
- Deliberately **separate files/URIs**: the ledger is `db://ledger/quoteko-…` (history);
  the graph is `State(kind=GRAPH)` + the living objects (relationship, offer, decision).
- `roundtrip_check(graph, ledger)` reconstructs each Graph object to the Ledger events
  whose `causation_id`/`ledger_ref`/`of` produced it (replays the slice), and verifies:
  1. every Graph object has at least one producing Ledger event;
  2. the Ledger is a valid hash-chain (no discontinuities);
  3. no Graph object claims to be "history" and no Ledger entry claims to be "state"
     (no conflation — kind fields are distinct).

## DoD (1.3)
- `run_roundtrip_check.py` prints the Graph objects separated from the Ledger history,
  reconstructs each Graph object from its Ledger events, and exits 0 on both ledger
  integrity and reconstruction completeness.
- The wiring is validated under Sprint-0 conformance (the ledger `db://` validates as
  Knowledge; living objects validate each against their $def).