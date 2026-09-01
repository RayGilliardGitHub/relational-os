# SPRINT 7 — SUB-SPRINT 1 plan — planning gate (before any code/content)

**Purpose:** the PROTOCOL mandates a `work/<n>-plan.md` before drafting code or content.
This sub-sprint is that gate. Everything below is laid out before the first edit.

## What will be built (in order)
1. **`configs.py`** — extend `mk()` to accept and store an additive `brand` dict; add a
   `BRANDS` table (12 sector families); pass `brand=BRANDS[label]` into each of the 12
   `SECTORS` entries (11 existing + new **`finb`** Financial). Brand keys avoid the C2
   RFC3339 probe suffixes (`at|time|deadline|expires|expiry|effective|due|since` endings).
2. **`sector_scene.py`** —
   - `build_scene`: add `"brand": cfg["brand"]` onto the company `org://` actor dict.
   - new `write_branding(sub, outdir)` → per-instance `artifacts/reports/branding.md`
     (About, Mission/Vision/Values, FAQ, Contact, Design language) rendered from `brand`.
   - `write_cockpit`: lead header `# Company — tagline …`; append `## Brand` appendix
     (about, mission, values, products, FAQ, contact, design language); put `brand` into
     `cockpit.json`.
   - `run_checks`: add a check that the `org://` company actor carries `brand` and that
     `branding.md` exists.
3. **`build_all.py`** — call `ss.write_branding` after `write_cockpit`. (Verify 12 build.)
4. **Financial v1** — `financial/fin_demo.py`: brand block on `BANK` actor, write
   `branding.md`, `## Brand` appendix in its cockpit; `financial/bi_snapshot.py`: brand
   label line (company + tagline). Re-verify `run_fin.py` + `run_fin_conformance.py`.
5. **Reference non-regression** — `run_s5_demo.py` + `run_s5_conformance.py` still ALL PASS
   (no `ros/` or schema change; brand rides only the sector instances).

## Verify commands (all real output)
- `cd /home/rlg/relational-os/instances && python3 build_all.py` → ALL SECTORS PASS, exit 0
- `cd /home/rlg/relational-os/instances && /home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python conformance_all.py` → ALL PASS, exit 0
- `cd /home/rlg/relational-os/sprints/sprint-5/artifacts && python3 run_s5_demo.py` → ALL PASS
- `cd /home/rlg/relational-os/sprints/sprint-5/artifacts && /home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python run_s5_conformance.py` → ALL PASS
- `cd /home/rlg/relational-os/instances/financial && python3 run_fin.py` → ALL PASS
- `cd /home/rlg/relational-os/instances/financial && /home/rlg/relational-os/sprints/sprint-0/artifacts/.venv/bin/python run_fin_conformance.py` → ALL PASS
- `cd /home/rlg/relational-os/instances/financial && python3 bi_snapshot.py` → brand label line

## Exit criteria for this sub-sprint
- plan.md AND this work plan exist; building begins only after this is accepted.
- No `delegate_task`/subagents; single thread. SPEC untouched (stays v0.22).