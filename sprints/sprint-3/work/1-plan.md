# SPRINT 3 · SUB-SPRINT 1 — S3 commit -> execute (one relationship)

**DoD:** a committed job advanced through at least 2 agent-worker steps with signed
`decision://` (split) and signed `action://`/`event://` per worker step on the Ledger.

## Build
- Copy Sprint-2 `ros/` package into `sprints/sprint-3/artifacts/ros/` verbatim (not git import).
- Add `ros/s3.py`:
  - `commit(offer, terms, authority, ...) -> commitment:// ` (per §5 `commitment = agree(offer, terms)`),
    status `AGREED`, written to Graph + signed STATE_CHANGE event.
  - `orchestrate(commitment, fleet, trust_scores) -> [Task]` — decompose the committed job
    into bounded, delegable tasks; emit a signed `decision://` for the split (§3.12).
  - `route_seam(task, trust) -> tier {local, private-cloud, frontier}` — §6 routing seam;
    Trust-weighted, deterministic local logic (no model calls, §G.11).
  - Each task is owned by an `agent://` worker; execution is `authorize()`-gated
    (capability-based, §3.4/§7B) and recorded as a signed ACTION `event://`.
- Seed the S3 worker fleet as Actors (`agent://s3`, `agent://w-local`, `agent://w-cloud`,
  `agent://w-frontier`, all `type: AGENT`) + delegated capabilities
  (`delegation://`→`rule://` grants).

## Verify
- `run_s3_demo.py` shows: commit → split decision → ≥2 worker steps executed (authorized,
  signed ACTION events) on the Ledger. Self-check `s3_check` asserts ≥2 worker ACTION events
  + a committed `commitment://` object with status `AGREED`.