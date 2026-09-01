# 02 — SETUP (Operations: install & verify)

**Audience:** operator. **Goal:** from an empty machine to a working, verifiable system.
**Grounding:** the real artifacts under `/home/rlg/relational-os`. Every command below was
executed in Sprint 6; its real output is embedded.

---

## 1. Prerequisites

- **Python 3.12** (the plain interpreter, used for the demo/cockpit runners). Verified:
  `python3 --version` → `Python 3.12.3`.
- The **Sprint-0 virtual environment** with the schema dependencies **`jsonschema`**,
  **`referencing`**, and **`yaml` (PyYAML)** available to its interpreter. This venv is used
  for every **conformance** run. Verified present:

      python3 --version                                      → Python 3.12.3
      sprints/sprint-0/artifacts/.venv/bin/python --version  → Python 3.12.3

  Its site-packages include (verified): `jsonschema 4.26.0`, `referencing 0.37.0`,
  `pyyaml 6.0.3`, plus `rpds`, `attrs`, `typing_extensions`. Interpreter:
  `/home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python`.

- Nothing else is required. The build and all runners are deterministic local Python — no
  network access, no API keys, no frontier spend (~$0/run).

## 2. Directory layout (what you are installing)

Everything lives under one workspace root, `/home/rlg/relational-os/`:

```
relational-os/
  SPEC.md            working spec v0.22 — THE contract
  PROTOCOL.md        sprint lifecycle
  README.md          workspace index (→ this docs package)
  docs/              supporting research / reference
  sprints/
    COMPLETE.md      project closing hand-off (Sprints 0–5)
    sprint-N/        one dir per sprint
      PROMPT.md      the self-contained build prompt (Sprint 6 = this documentation sprint)
      plan.md · work/ · notes/findings.md · summary.md
      artifacts/
        schema/…     Sprint-0: relational-os.schema.yaml/.json, .ebnf, build_schema.py
        conformance.py  Sprint-0 validator (C1–C5)
        run_conformance.py  Sprint-0 runner (fixtures under its own artifacts/fixtures)
        make_fixtures.py    generator (Sprint-0)
        surveys/      Sprint-0: 4 commissioned surveys (01-data-licensing … 04-data-boundary-privacy)
        .venv/        Sprint-0 venv (jsonschema/referencing/yaml)
        fixtures/     instances; per-generation 156 / 28 / 35 / 55 / 174 / 316
        ros/          package (Sprint-5 end-state): substrate.py · s1..s5.py · bol.py · checks.py
                     (canonical copy now lives at the repo ROOT `/ros/`; the sprint-5 one is its origin snapshot — reorg)
        run_s5_demo.py          daily cockpit producer
        run_s5_conformance.py   validator over all SIX generations
        s3_demo.py · s4_demo.py · s5_demo.py · bol_demo.py   scene builders
        graph/current-state.json        produced Graph (state)
        fixtures/ledger/ledger-quoteko.json  produced Ledger (history)
        reports/cockpit.md | .json       the daily cockpit + §7L answers
```

File-by-file detail of the key end-state (`sprint-5/artifacts/`): see `01-system-manual.md §8`.

## 3. How to create/repair the venv, if missing

The venv already exists at `sprints/sprint-0/artifacts/.venv/`. If it is missing or its
deps are gone, recreate it **inside** the Sprint-0 artifacts directory (conformance paths
expect it there) — Python 3.12 required (`python3 -m venv` ships the schema deps via `pip`):

    cd /home/rlg/relational-os/sprints/sprint-0/artifacts
    python3 -m venv .venv
    .venv/bin/python -m pip install jsonschema referencing pyyaml

> Note: the shipped venv does **not** include `pip` in `bin/` (a verified quirk), so if it
> works you do not need pip at all — conformance only needs the three packages present under
> `.venv/lib/python3.12/site-packages/`. Use the block above only to rebuild a broken venv.

Verify the three deps import under the venv interpreter:

    /home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python \
        -c "import jsonschema, referencing, yaml; print('deps OK')"
    → deps OK

## 4. Verify the install (run the conformance gate)

The single strongest "is this installed correctly?" test is the conformance runner over all
six fixture generations. Run it with the **Sprint-0 venv interpreter** — it is
`Path(__file__)`-**anchored, so it runs from the repo root or anywhere** (post-reorg; it was
formerly CWD-bound on `../../sprint-0/artifacts`):

    cd /home/rlg/relational-os/sprints/sprint-5/artifacts
    /home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python run_s5_conformance.py
    → exit 0, "RESULT: ALL PASS"

The same command works from `/home/rlg/relational-os` directly (no `cd` needed).

Real (embedded) tail of that run:

    === [sprint-5] sprint-5/artifacts/fixtures ===
      [PASS] C1 schema structurally valid  — 49 $defs
      [PASS] C2 all fixture instances validate + schemes + RFC3339  — 316 instances
      [PASS] C3 ledger content-addressed + signed
      [PASS] C4 round-trip preserve-unknown
      [PASS] C5 state-machine sequences legal
    RESULT: ALL PASS

Per-generation C2 instance counts verified in Sprint 6: Sprint-0 **156**, Sprint-1 **28**,
Sprint-2 **35**, Sprint-3 **55**, Sprint-4 **174**, Sprint-5 **316** — all **ALL PASS**, exit 0,
one shared validator (no regression over any generation).

## 5. Next steps

- Once conformance passes, the installation is verified. Run the full daily cockpit per
  `03-run.md §1` (or `QUICKSTART.md`).
- To run an audit: `04-audit.md`. To produce BI: `05-bi-reports.md`.
- If a step fails: `07-troubleshooting.md`.