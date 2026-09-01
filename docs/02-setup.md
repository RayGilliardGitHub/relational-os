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
      .venv/bin/python --version  → Python 3.12.3

  Its site-packages include (verified): `jsonschema 4.26.0`, `referencing 0.37.0`,
  `pyyaml 6.0.3`, plus `rpds`, `attrs`, `typing_extensions`. Interpreter:
  `/home/rlg/relational-os/.venv/bin/python`.

- Nothing else is required. The build and all runners are deterministic local Python — no
  network access, no API keys, no frontier spend (~$0/run).

## 2. Directory layout (what you are installing)

Everything lives under one workspace root, `/home/rlg/relational-os/`:

```
relational-os/
  SPEC.md            working spec v0.22 — THE contract
  PROTOCOL.md        the (development) lifecycle — optional to run the system
  README.md          workspace index (→ this docs package)
  docs/              this manual package
  ros/               CANONICAL package: substrate.py · s1..s5.py · bol.py · checks.py
  schema/            validator + schema: conformance.py · run_conformance.py ·
                     run_conformance_all.py (all six generation gate) ·
                     relational-os.schema.{yaml,json} · relational-os-lifecycle.ebnf
  reference/         the reference build + its produced data: run_s5_demo.py · s3/s4/s5/bol_demo.py ·
                     fixtures/ (gen-5 corpus) · graph/
  reports/           produced cockpit report: cockpit.md · cockpit.json
  data/fixtures/     the rest of the validator corpus: gen-0/ · gen-1/ · gen-2/ · gen-3/ · gen-4/
  tests/run_checks.py  the full green gate (41 checks; exit 0 = ALL PASS)
  scripts/verify.sh    the quick gate (daily cockpit + all-six conformance)
  instances/         sector instances (12) + contested_reality + agent_demo
  sprints/           NARRATIVE build history (PROMPT/plan/work/notes/summary + historical artifacts)
```

File-by-file detail of the canonical system (`ros/`, `schema/`, `reference/`): see `01-system-manual.md §8`.

## 3. How to create/repair the venv, if missing

The venv already exists at `schema/.venv/`. If it is missing or its
deps are gone, recreate it **inside** the Sprint-0 artifacts directory (conformance paths
expect it there) — Python 3.12 required (`python3 -m venv` ships the schema deps via `pip`):

    cd /home/rlg/relational-os/schema
    python3 -m venv .venv
    .venv/bin/python -m pip install jsonschema referencing pyyaml

> Note: the shipped venv does **not** include `pip` in `bin/` (a verified quirk), so if it
> works you do not need pip at all — conformance only needs the three packages present under
> `.venv/lib/python3.12/site-packages/`. Use the block above only to rebuild a broken venv.

Verify the three deps import under the venv interpreter:

    /home/rlg/relational-os/.venv/bin/python \
        -c "import jsonschema, referencing, yaml; print('deps OK')"
    → deps OK

## 4. Verify the install (run the conformance gate)

The single strongest "is this installed correctly?" test is the conformance runner over all
six fixture generations. Run it with the **`.venv` interpreter** — it is
`Path(__file__)`-**anchored, so it runs from the repo root or anywhere** (post-reorg; it was
formerly CWD-bound on `../../sprint-0/artifacts`):

    cd /home/rlg/relational-os/reference
    /home/rlg/relational-os/.venv/bin/python schema/run_conformance_all.py
    → exit 0, "RESULT: ALL PASS"

The same command works from `/home/rlg/relational-os` directly (no `cd` needed).

Real (embedded) tail of that run:

    === [gen-5] reference/fixtures ===
      [PASS] C1 schema structurally valid  — 49 $defs
      [PASS] C2 all fixture instances validate + schemes + RFC3339  — 316 instances
      [PASS] C3 ledger content-addressed + signed
      [PASS] C4 round-trip preserve-unknown
      [PASS] C5 state-machine sequences legal
    RESULT: ALL PASS

Per-generation C2 instance counts verified in Sprint 6: gen-0 **156**, gen-1 **28**,
gen-2 **35**, gen-3 **55**, gen-4 **174**, gen-5 **316** — all **ALL PASS**, exit 0,
one shared validator (no regression over any generation).

## 5. Next steps

- Once conformance passes, the installation is verified. Run the full daily cockpit per
  `03-run.md §1` (or `QUICKSTART.md`).
- To run an audit: `04-audit.md`. To produce BI: `05-bi-reports.md`.
- If a step fails: `07-troubleshooting.md`.