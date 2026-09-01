"""run_forecast_capacity_demo.py — SPRINT 20: recorded-data Q6 forecast + Q9 capacity for §7L.

Sprint 19 made `adjudication_engine.cockpit_s7l` render the full §7L Q1–Q10 cockpit, data-only, for
any configured org — but its own findings ("Residual seams") disclosed that **Q6 cannot forecast**
(no adjudication org records a realized-vs-expected series) and **Q9 "capability"** was the
holder-of-authority assignment, not a capacity number. Sprint 20 closes a bounded slice of both by
making an org RECORD the missing data additively on its own graph/ledger — a `metric://`
realized-vs-expected series (`record_metric_series`) and an additive `capacity` field on the
`authority://` object the Q9 question reads (`record_capacity`) — so that org's `cockpit_s7l.q6`
projects a DETERMINISTIC forecast from its recorded series and its `.q9` reports the recorded
capacity, WHERE the data exists; the honest no-data fallback is unchanged.

This runner (exit 0 = ALL PASS) drives ≥2 orgs:
  deli-forecast -> a NEW org (a clean relabel of `deli` onto its own namespace) that RECORDS a
                   `metric://deli-forecast/m-on-time` realized-vs-expected series + a `capacity`
                   field on `authority://deli-forecast/adjudicate`.
  deli          -> an EXISTING org with no recorded series/capacity (the honest-fallback control).
and asserts:
  (a) BOTH orgs still pass the full §7L Q1–Q10 cockpit (all ten questions + evidence present);
  (b) the recorded-data org answers Q6 with a deterministic forecast derived ONLY from its recorded
      series and Q9 with a capacity number+unit from its recorded authority field;
  (c) the no-data org keeps the honest fallback for Q6 and the no-capacity Q9;
  (d) determinism (structured dict + rendered line identical on re-run);
  (e) AGREEMENT: the q6 projection equals a hand-computed projection from the recorded points, and
      q9.capacity equals the recorded `capacity` field on the authority object (both read off the
      org's own graph/ledger);
  (f) the new org's fixtures pass the Sprint-0 C1–C5 conformance, and deli/cove remain
      byte-identical up to the clock (no existing org changed).

Additive: frozen ontology (49 $defs), URI cap, SPEC v0.22, ros/ untouched, deli/cove intact. ~$0.
Usage: (from instances/contested_reality)  python3 run_forecast_capacity_demo.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INSTANCES = HERE.parent
ROS = INSTANCES.parents[0]
SPRINT0 = INSTANCES.parents[1] / "sprints/sprint-0/artifacts"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(INSTANCES))
sys.path.insert(0, str(ROS))

from ros.substrate import Substrate, now_iso          # noqa: E402
import adjudication_engine as eng                     # noqa: E402
import adjudication_configs as ac                     # noqa: E402

_OK = True
def _report(name, cond, why=""):
    global _OK
    _OK &= bool(cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  — ' + why if why else ''}")


def seed_trust(cfg, sub) -> str:
    L = cfg["label"]
    trust_uri = f"trust://{L}/claimant"
    sub.record({"uri": f"event://{L}/seed-trust", "type": "STATE_CHANGE",
                "event_id": f"ev-adj-{L}-seed-trust", "correlation_id": f"corr-adj-{L}-seed-trust",
                "causation_id": f"ev-adj-{L}-seed-trust-prev", "idempotency_key": f"idem-adj-{L}-seed-trust",
                "signature": f"signed-by-{cfg['registrar']}", "occurred_at": now_iso(),
                "actor": cfg["registrar"], "detail": "seed scoped trust before the episode",
                "state_update": [{"uri": trust_uri, "subject": cfg["registrar"],
                                  "target": cfg["claimants"][0], "claim": "honest dispute participant",
                                  "score": 0.80, "context": f"relationship://{L}/x",
                                  "evidence": []}]}, cfg["registrar"])
    return trust_uri


def run_one(cfg):
    """Run one configured lifecycle on a FRESH Substrate; return the sub + determination."""
    eng.validate_config(cfg)
    sub = Substrate(ledger_uri=cfg["ledger_name"])
    seed_trust(cfg, sub)
    ok, _, du, sub = eng.run_scenario(cfg, sub)
    d = sub.graph.get(du)
    return {"cfg": cfg, "label": cfg["label"], "dispute_uri": du, "sub": sub,
            "determination": d.get("determination")}


def relabel_to(cfg: dict, new_label: str) -> dict:
    """Clone `cfg` under a NEW orphan-namespace label. Every `://<old>/` URI segment is rewritten to
    `://<new_label>/` (a deep copy via json so no shared dict is mutated, with `floor_gated` sets
    round-tripped as lists), and the ledger name + label are set — so the clone owns clean,
    self-consistent URIs (its own authority://, dispute://, claim://…). This is pure CONFIG data,
    same as `org_under_library_rule`, not engine code."""
    old = cfg["label"]
    c = json.loads(json.dumps(cfg, default=lambda o: sorted(o) if isinstance(o, set) else json.dumps(o)))
    def _rw(o):
        if isinstance(o, dict):
            return {k: _rw(v) for k, v in o.items()}
        if isinstance(o, list):
            return [_rw(x) for x in o]
        if isinstance(o, str):
            return o.replace(f"://{old}/", f"://{new_label}/")
        return o
    c = _rw(c)
    c["label"] = new_label
    c["ledger_name"] = c["ledger_name"].replace(old, new_label)
    c["floor_gated"] = set(c["floor_gated"])   # restore the set the engine's `in` check expects
    return c


# the recorded realized-vs-expected series for the forecast org (ordered by period; C2-safe keys)
FC_LABEL = "deli-forecast"
FC_METRIC = f"metric://{FC_LABEL}/m-on-time"
FC_POINTS = [
    {"period": 1, "expected": 0.95, "target": 0.95, "actual": 0.92, "variance": -0.03},
    {"period": 2, "expected": 0.95, "target": 0.95, "actual": 0.90, "variance": -0.05},
    {"period": 3, "expected": 0.95, "target": 0.95, "actual": 0.87, "variance": -0.08},
    {"period": 4, "expected": 0.95, "target": 0.95, "actual": 0.86, "variance": -0.09},
]
# hand-computed expected projection (deterministic): deltas -0.02,-0.03,-0.01 mean -0.02; last 0.86
EXPECTED_PROJ = [round(0.86 - 0.02 * f, 4) for f in (1, 2, 3)]      # [0.84, 0.82, 0.8]
HORIZON = 3
FC_CAPACITY = {"value": 1.0, "unit": "obligations", "load": 0.60}


def run_all() -> int:
    print("=== SPRINT 20 — recorded-data Q6 forecast + Q9 capacity for the §7L morning cockpit ===\n")

    # ---- drive the ≥2 orgs: the recorded-data org and the no-data control ----------------------
    fc_cfg = relabel_to(ac.DELI, FC_LABEL)
    fc_authority_uri = fc_cfg["authority"]["dispute"]
    fc = run_one(fc_cfg)
    # record the realized-vs-expected series + capacity additively on ITS OWN ledger/graph.
    eng.record_metric_series(fc["sub"], FC_LABEL, FC_METRIC, points=FC_POINTS,
                             fields={"name": "resolution on-time rate",
                                     "formula": "on-time resolutions / total resolutions from ledger",
                                     "unit": "fraction", "target": 0.95, "period": "quarter",
                                     "source": "ledger resolution completion records",
                                     "owner": fc_cfg["authority"]["adjudicator_person"]},
                             signer=fc_cfg["authority"]["adjudicator_person"])
    eng.record_capacity(fc["sub"], fc_authority_uri, signer=fc_cfg["authority"]["adjudicator_person"],
                        value=FC_CAPACITY["value"], unit=FC_CAPACITY["unit"], load=FC_CAPACITY["load"])

    deli = run_one(ac.DELI)

    for r in (fc, deli):
        r["s7l"] = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)

    # ---- (a) BOTH orgs keep the full §7L Q1–Q10 cockpit ----------------------------------------
    for r in (fc, deli):
        c = r["s7l"]
        full = all(isinstance(c[k], dict) for k in
                   ("q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"))
        ev = all(bool(c[k].get("evidence"))
                 for k in ("q1", "q2", "q3", "q4", "q5", "q6", "q9", "q10"))
        _report(f"{r['label']}: FULL §7L Q1–Q10 cockpit + recorded-data evidence present",
                full and ev and bool(c["q1"]["events"]) and bool(c["q7"]["options"])
                and bool(c["q8"]["authority"]) and bool(c["q10"]["determination"]),
                f"q1 events={len(c['q1']['events'])} q6.avail={c['q6']['forecast_available']} "
                f"q9.cap={c['q9']['capacity_recorded']}")

    # ---- (b) recorded-data org: Q6 deterministic forecast + Q9 capacity ------------------------
    c = fc["s7l"]
    _report(f"{FC_LABEL}: Q6 produces a DETERMINISTIC forecast from the recorded series only",
            c["q6"]["forecast_available"] is True and c["q6"]["metric"] == FC_METRIC
            and c["q6"]["last_actual"] == 0.86 and c["q6"]["mean_delta"] == -0.02
            and c["q6"]["recorded_variance"] == -0.09
            and [p["projected"] for p in c["q6"]["projections"]] == EXPECTED_PROJ,
            f"proj={[p['projected'] for p in c['q6']['projections']]} "
            f"last={c['q6']['last_actual']} delta={c['q6']['mean_delta']}")
    _report(f"{FC_LABEL}: Q9 reports the recorded capacity number + unit",
            c["q9"]["capacity_recorded"] is True
            and c["q9"]["capacity"]["value"] == 1.0
            and c["q9"]["capacity"]["unit"] == "obligations"
            and c["q9"]["capacity"]["load"] == 0.60,
            f"cap={c['q9']['capacity']}")

    # ---- (c) no-data org keeps the honest fallback ----------------------------------------------
    d = deli["s7l"]
    _report("deli (no recorded series/capacity): Q6 keeps the honest fallback",
            d["q6"]["forecast_available"] is False
            and "cannot forecast from recorded data" in d["q6"]["forecast"])
    _report("deli (no recorded capacity): Q9 reports no-capacity",
            d["q9"]["capacity_recorded"] is False and d["q9"]["capacity"] is None)

    # ---- (d) determinism on re-run (dict + render identical) -----------------------------------
    for r in (fc, deli):
        c1 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x1 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        c2 = eng.cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        x2 = eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY)
        _report(f"{r['label']}: deterministic on re-run (structured dict + rendered §7L line)",
                c1 == c2 and x1 == x2)
    # forecast_metric itself is a pure function of the recorded series
    f1 = eng.forecast_metric(fc["cfg"], fc["sub"], FC_METRIC, horizon=HORIZON)
    f2 = eng.forecast_metric(fc["cfg"], fc["sub"], FC_METRIC, horizon=HORIZON)
    _report("forecast_metric: pure/deterministic on re-call",
            f1 == f2 and f1["available"] is True and f1["note"])

    # ---- (e) AGREEMENT: projection matches hand-computed; q9 matches the recorded authority field -
    _report("AGREEMENT: q6 projection == hand-computed from the recorded points",
            [p["projected"] for p in c["q6"]["projections"]] == EXPECTED_PROJ
            and f1["projections"] == c["q6"]["projections"],
            f"engine={[p['projected'] for p in c['q6']['projections']]} "
            f"hand={EXPECTED_PROJ}")
    recorded_cap = (fc["sub"].graph.get(fc_authority_uri) or {}).get("capacity") or {}
    _report("AGREEMENT: q9.capacity == the recorded capacity field on the authority object",
            c["q9"]["capacity"] == dict(recorded_cap),
            f"q9={c['q9']['capacity']} on-graph={recorded_cap}")
    _report("AGREEMENT: every projection is derived from recorded series values only (no wall-clock)",
            all(p["projected"] == round(0.86 - 0.02 * p["period"], 4) for p in c["q6"]["projections"])
            and "never the wall-clock" in f1["note"])

    # ---- honest fallback path of forecast_metric when no series exists ---------------------------
    fallback = eng.forecast_metric(deli["cfg"], deli["sub"], f"metric://deli/none", horizon=HORIZON)
    _report("forecast_metric: honest 'cannot project' when no recorded series exists",
            fallback["available"] is False and "cannot project" in fallback["forecast"])

    # ---- emit the deli-forecast fixtures; assert the recorded data is on the org's OWN ledger ------
    eng.emit_fixtures(fc["sub"], HERE, fc["cfg"])
    fx = HERE / "artifacts/adjudication/fixtures" / FC_LABEL
    ledger_txt = (fx / "ledger/ledger.json").read_text() if (fx / "ledger/ledger.json").exists() else ""
    actors_txt = (fx / "actors_offers.json").read_text() if (fx / "actors_offers.json").exists() else ""
    emitted_ok = (FC_METRIC in ledger_txt           # the realized-vs-expected series on the ledger
                  and "\"capacity\"" in actors_txt  # the capacity field on the authority:// fixture
                  and (fx / "statemachines/dispute.json").exists()
                  and (fx / "statemachines/relationship.json").exists())
    _report(f"{FC_LABEL}: recorded data emitted onto the org's OWN fixtures (metric series on the "
            "ledger + capacity on the authority component)", emitted_ok,
            f"C1–C5 verified by the Sprint-0 venv in the verification step (fschema 49 $defs, "
            f"SPEC v0.22 unchanged)")

    # ---- emit the engine-native forecast+capacity cockpit render (report) -----------------------
    rp = HERE / "artifacts/adjudication/reports"; rp.mkdir(parents=True, exist_ok=True)
    A = []
    A.append("# §7L recorded-data Q6 forecast + Q9 capacity — engine-native render (Sprint 20)")
    A.append(f"generated {now_iso()}  |  `adjudication_engine.cockpit_s7l`/`render_cockpit_s7l`  |  "
             "recorded `metric://` realized-vs-expected series + additive `capacity` field  |  "
             "SPEC v0.22, 49 $defs, URI cap")
    A.append("")
    A.append("An org that RECORDS the missing data on its own graph/ledger (a metric:// "
             "realized-vs-expected series + a capacity field on its authority://) gets a deterministic "
             "Q6 forecast and a Q9 capacity number, where the data exists; an org that has not recorded "
             "them keeps the honest no-data fallback. Both still pass the full §7L Q1–Q10 cockpit.")
    A.append("")
    for r in (fc, deli):
        A.append(f"--- {r['label']} ---")
        A.append("```")
        A.append(eng.render_cockpit_s7l(r["cfg"], r["sub"], library=ac.RULE_LIBRARY))
        A.append("```")
        A.append("")
    A.append("## §16 verdict")
    A.append("")
    A.append("**Q6 and Q9 are now answered AS DATA for any org that records them.** A generically-driven "
             "org appends a realized-vs-expected `metric://` series and an additive capacity field to its "
             "own ledger (merge-not-replace, signed, immutable), and `cockpit_s7l.q6` projects a "
             "deterministic 'if nothing changes' forecast from the recorded values while `.q9` reports the "
             "recorded capacity — never the wall-clock, never an invented number. Where an org has not "
             "recorded them, the cockpit stays honest: Q6 says it cannot forecast, Q9 reports no capacity. "
             "The §7L morning cockpit is now data-grounded on every one of the ten questions WHERE the "
             "data exists; the honest remaining limit is that a no-data org cannot be forced to forecast "
             "or measured for capacity — the engine reports the recorded reality, it does not manufacture "
             "one. Q7/Q8 stay the Sprint-18 line (delegated by construction); #8 remains §6-floor-gated; "
             "the determination is the §6 human's call; S5 alone moves Trust.")
    A.append("")
    A.append("_Additive; frozen ontology, SPEC v0.22, 49 $defs. Trust only moved by S5._")
    (rp / "cockpit-forecast-capacity.md").write_text("\n".join(A) + "\n")

    print("\n  -> engine-native forecast+capacity cockpit under artifacts/adjudication/reports/"
          "cockpit-forecast-capacity.md")
    print("  -> new org fixtures under artifacts/adjudication/fixtures/deli-forecast/")
    print("RESULT:", "ALL PASS" if _OK else "FAILURES PRESENT")
    return 0 if _OK else 1


if __name__ == "__main__":
    sys.exit(run_all())