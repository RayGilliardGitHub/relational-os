# Sub-sprint 1 — Plan + build the consolidated lifecycle proof

## Objective
Build `instances/contested_reality/run_full_dispute.py`: one financial/customer dispute ($18,000,
delivery) with four conflicting timestamp evidence items, executed as the ENTIRE contested-reality
lifecycle over real signed ledger events. Reuse `tradeoff_model` (Sprint 11) for the resolution
trade-off and `agent_adapter` (Sprint 8) for the optional contained model advisory. All additive on
the frozen $defs (Claim/Evidence/Dispute/Decision/Trust/Obligation); no new noun, 49 $defs, SPEC v0.22.

## The lifecycle the script must run (as a real event chain)
provision actors/authority/obligations → customer claim + company claim + supplier claim → attach
conflicting evidence (GPS 16:12 / contract 16:00 / customer receipt 16:15 / supplier 15:58) →
conflict detection (on-time vs late contradicted) → uncertainty → epistemic status on claims →
dispute OPEN (parties/about + additive lifecycle/epistemic/determination) → interests/obligations/
constraints → resolution options incl do-nothing + settlement → machine trade-off + advisory model →
authorized human determination (MGR, authority preserved) → outcome → verification → learning →
APPEAL → REOPEN on new evidence (clock mis-set discovered) → reassessment → NEW determination
(partial settlement) with history preserved (no rewrite) → Trust error-vs-deception handled → full
audit-reconstructable ledger → UNRESOLVED variant (insufficient basis; Trust untouched).

## Key correctness rules (from the skill's footguns)
- `graph.get(uri)` one-arg; use `(graph.get(uri) or {})`.
- MERGE not REPLACE on updates: `{**graph.get(uri), "status": ..., ...}` preserves required fields.
- Evidence.kind enum [OBSERVATION, TESTIMONY, RECORD, ANCHORED]; must have `source`.
- Dispute requires about/parties/status; status enum frozen [OPEN, ADJUDICATED, RESOLVED] — carry
  lifecycle/epistemic/determination additively.
- Claim requires proposer/statement. Decision requires by/authority.
- C2 temporal-suffix trap: new additive keys must not end in at|time|deadline|expires|expiry|
  effective|due|since (use `captured_at` only where the schema already declares it; custom flags use
  suffixes like `_known/_status/_ref/_ok`). NOTE: `due_by` and `captured_at` are schema-declared.
- Emit statemachines/dispute.json as a fully legal walk for C5.

## Verification
`python3 run_full_dispute.py` → RESULT: ALL PASS with ~12 assertions covering: contradictory claims
preserved; contradictory evidence preserved; uncertainty modelled; epistemic status tracked;
determination reachable; UNRESOLVED valid + Trust-safe; AI cannot determine/bypass authority; reopen
reassesses without history rewrite; Trust error-vs-deception kept distinct; authority/signature
preserved; full chain reconstructable from ledger.

## Exit criteria
Script ALL PASS; fixtures emitted under artifacts/lifecycle/; then conformance (sub-sprint 2).