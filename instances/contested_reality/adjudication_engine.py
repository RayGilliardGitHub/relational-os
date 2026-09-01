"""adjudication_engine.py — SPRINT 13: a configurable, generic adjudication engine.

Sprint 12 proved RelationalOS can RUN the contested-reality lifecycle, but its honest verdict was
"B — Partially": the adjudication semantics (epistemic status transitions, the lifecycle state
machine, the generation of resolution options, and the value/utility weights) were authored per
scenario — a different org's dispute still needed re-coding. This module makes that capability
GENERAL: a single, rule-driven, config-consuming driver that runs a contested-reality lifecycle
for ANY org `adjudication_configs.py` configures for it, with NO per-scenario code.

The engine reads an adjudication CONFIG purely as data:
  options        cfg['options']                 the resolution option set (incl. unresolved baseline)
  weights        cfg['weights']  (Σ==1.0)       THE business model — "what 'better' means" (§7K.1)
  factor_scores  cfg['factor_scores'][opt][factor]  each option's modeled value per factor (§7K.1)
  floor_gated    cfg['floor_gated'], cfg['floor_penalty']  the §6 irreversible/unknown-cost gate
  reconcile      cfg['reconcile'] {rule, threshold, support_floor}  the evidence-reconciliation rule
  authority      cfg['authority']               adjudicator + appeal (§7J.9)
  determination_policy  cfg['determination_policy']  the §6 human's authoritative call (adopt or
                                                 override or UNRESOLVED) — declared as org policy

From ≥2 recorded conflicting claims + that config it deterministically runs, over real signed
append-only ledger events:
  claims -> evidence -> reconcile -> conflict/uncertainty -> dispute OPEN ->
  options ranked (utility = Σ_factor weight·score − floor_penalty if gated; unresolved baseline
  never gated) -> §6 gate (machine-eligible pick = top NON-gated) -> advisory decision://
  (contained: no trust://, not a determination) -> authorized human determination (or UNRESOLVED)
  -> verified outcome -> learning.

Everything is additive on the FROZEN `$defs` (49 `$defs`, URI cap, SPEC v0.22). TRUST is only ever
touched by the deterministic S5 question, never by this engine. No new noun; `ros/` untouched.

Usage (from instances/contested_reality):
  python3 run_adjudication_engine_demo.py        # runs both config scenarios, exit 0 = ALL PASS
"""
from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path

from ros.substrate import Substrate, now_iso  # noqa: E402


# ----------------------------------------------------------------------------------------------
# Config validation (the contract) — every violation is loud, never silently coerced.
# ----------------------------------------------------------------------------------------------
def validate_config(cfg: dict) -> None:
    assert len(cfg.get("claims", [])) >= 2, "engine requires >=2 conflicting claims"
    assert "options" in cfg and cfg["options"], "cfg.options required"
    assert any("unres" in o.lower() or o == "do-nothing" for o in cfg["options"]), (
        "cfg.options must include an unresolved / do-nothing baseline")
    w = cfg["weights"]
    assert abs(sum(w.values()) - 1.0) < 1e-9, f"weights must sum to 1.0 (got {sum(w.values())})"
    assert all(isinstance(v, (int, float)) and 0.0 <= v <= 1.0
               for v in w.values()), "weights in [0,1]"
    for opt, scores in cfg["factor_scores"].items():
        assert opt in cfg["options"], f"factor_scores has unknown option {opt!r}"
        for f, s in scores.items():
            assert f in w, f"factor_scores factor {f!r} not in weights"
            assert 0.0 <= s <= 1.0, f"score {s} out of [0,1] for {opt}.{f}"
    for gated in cfg.get("floor_gated", []):
        assert gated in cfg["options"], f"floor_gated option {gated!r} not an option; "
    rc = cfg.get("reconcile") or {}
    rc_is_spec = "rule_spec" in rc
    rc_is_reg = rc.get("rule") in RULES
    assert "reconcile" in cfg and (rc_is_reg or rc_is_spec), (
        "cfg.reconcile must name a registered reconciliation rule OR carry a rule_spec; "
        f"registry rules: {sorted(RULES)}")
    if rc_is_spec:
        compile_rule_spec(rc["rule_spec"])        # loud: an invalid rule-authoring spec is rejected
    assert "authority" in cfg, "cfg.authority required"
    assert cfg["determination_policy"] in ("adopt-eligible-best", "override", "unresolved")


# ----------------------------------------------------------------------------------------------
# Utility — the business model, applied deterministically to the recorded factor scores.
# ----------------------------------------------------------------------------------------------
def rank(cfg: dict, options=None) -> list[dict]:
    """Return all options scored: utility = Σ_factor weight·score − floor_penalty if gated.

    Sorted deterministically (utility desc, then canonical options order — never dict order).
    The unresolved/do-nothing baseline is NEVER floor-gated and is always present (no forced
    winner, §7K.1 trade-off).
    """
    w = cfg["weights"]
    opts = list(options) if options is not None else cfg["options"]
    canonical = list(cfg["options"])
    scored = []
    for opt in opts:
        scores = cfg["factor_scores"].get(opt, {})
        util = sum(w[f] * scores.get(f, 0.0) for f in w)
        gated = opt in cfg.get("floor_gated", set())
        if gated:
            util -= cfg.get("floor_penalty", 0.20)
        scored.append({"option": opt, "utility": round(util, 4), "floor_gated": gated})
    scored.sort(key=lambda r: (-r["utility"], canonical.index(r["option"])))
    return scored


def machine_eligible_best(ranked: list[dict]) -> dict:
    """§6 gate: return the top NON-gated option (the only one the machine may forward to the
    human). If every changing option is gated it returns the unresolved baseline + a flag."""
    elig = [r for r in ranked if not r["floor_gated"]]
    if elig:
        return elig[0]
    baseline = next(r for r in ranked if "unres" in r["option"].lower() or r["option"] == "do-nothing")
    return baseline


# ----------------------------------------------------------------------------------------------
# Evidence reconciliation — CONFIG-AUTHORABLE (Sprint 14). The RULE is selected from config
# (`cfg["reconcile"]["rule"]`) and resolved through a tiny deterministic registry. A NEW rule is
# added by registering a pure function below + selecting it in config — no engine-side change for
# the new rule. The rule computes a per-claim SUPPORT strength; the shared `_derive` turns support
# into the uniform dispute verdicts (disputed/conflict/determined/uncertainty) from the configured
# `support_floor` + `threshold`. Parameters (rule, threshold, support_floor, and any rule-specific
# params like `kinds` / `as_of` / `half_life_days`) are DATA; only the pure support mapping is code.
# ----------------------------------------------------------------------------------------------
def _parse_rfc3339(s: str) -> datetime:
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return datetime.fromisoformat(s)


def _derive(sup: dict, p: dict) -> dict:
    """Uniform dispute verdicts from per-claim support + the configured floors/threshold."""
    threshold = p["threshold"]; floor = p["support_floor"]
    disputed = [u for u, s in sup.items() if s >= floor]
    conflict = len(disputed) >= 2                          # rival claims both credibly supported
    determined = [u for u, s in sup.items() if s >= threshold]
    uncertainty = len(determined) == 0
    return {"claim_support": sup, "conflict": conflict, "uncertainty": uncertainty,
            "disputed": disputed, "determined": determined}


def _supporting_index(claims, sub) -> dict:
    """{claim_uri: [evidence_obj...]} for every claimed uri, from the graph (evidence that
    `supports` a claim). Keeps claims order for deterministic output."""
    out: dict[str, list] = {c["uri"]: [] for c in claims}
    seen: set[str] = set()
    for c in claims:
        for ev_uri in c.get("evidence", []):
            if ev_uri in seen:
                continue
            seen.add(ev_uri)
            e = sub.graph.get(ev_uri) or {}
            if e.get("supports") == c["uri"]:
                out[c["uri"]].append(e)
    return out


def _rule_best_rel(ctx, p) -> dict:
    """best-reliability-threshold: claim support = max reliability of its (graph) supporting refs
    (missing -> 0). VERBATIM Sprint-13 semantics -> deli/cove byte-identical."""
    sup = {}
    for claim in ctx["claims"]:
        best = 0.0
        for ev in ctx["supporting"].get(claim["uri"], []):
            best = max(best, float(ev.get("reliability", 0.0)))
        sup[claim["uri"]] = round(best, 4)
    return _derive(sup, p)


def _rule_strict_anchor(ctx, p) -> dict:
    """strict-anchor-only: only evidence of the configured `kinds` (default [ANCHORED]) counts
    toward a claim's support; all non-anchored (testimony/record) evidence is held inadmissible.
    -> a claim resting only on human records cannot be supported (the honest UNRESOLVED outcome)."""
    allow = set(p.get("kinds", ["ANCHORED"]))
    sup = {}
    for claim in ctx["claims"]:
        best = 0.0
        for ev in ctx["supporting"].get(claim["uri"], []):
            if ev.get("kind") in allow:
                best = max(best, float(ev.get("reliability", 0.0)))
        sup[claim["uri"]] = round(best, 4)
    return _derive(sup, p)


def _rule_recency(ctx, p) -> dict:
    """recency-weighted-threshold: support = max over supporting refs of
    reliability * 0.5**((as_of - captured_at).days / half_life_days). Recency-decays older sources,
    so an ANCIENT high-reliability record loses weight against recent evidence. DETERMINISTIC: the
    `as_of` reference MUST be given in params (never the wall-clock); evidence captured after as_of
    keeps full weight (factor 1.0)."""
    as_of = _parse_rfc3339(p["as_of"])          # explicit, deterministic reference (required)
    half_life = float(p.get("half_life_days", 30.0))
    if half_life <= 0:
        raise ValueError("recency-weighted-threshold requires half_life_days > 0")
    sup = {}
    for claim in ctx["claims"]:
        best = 0.0
        for ev in ctx["supporting"].get(claim["uri"], []):
            try:
                cap = _parse_rfc3339(str(ev.get("captured_at", "")))
            except ValueError:
                cap = as_of                               # no/undateable capture -> treated fresh
            days = max(0, (as_of - cap).days)
            factor = 0.5 ** (days / half_life)
            best = max(best, float(ev.get("reliability", 0.0)) * factor)
        sup[claim["uri"]] = round(best, 4)
    return _derive(sup, p)


# The config-authorable rule registry: name -> pure function. NEW rule = a registry entry + a
# pure function, then select it from config (cfg["reconcile"]["rule"]). No per-scenario code.
RULES = {
    "best-reliability-threshold": _rule_best_rel,
    "strict-anchor-only": _rule_strict_anchor,
    "recency-weighted-threshold": _rule_recency,
}

# ----------------------------------------------------------------------------------------------
# SPRINT 15 — the declarative rule-AUTHORING layer. A RULE can be declared as CONFIG TEXT (a
# `rule_spec` dict) instead of an engine function: the spec selects + configures a FIXED vocabulary
# of pure primitives (`SPEC_VOCAB`), and `compile_rule_spec()` compiles it into the SAME pure
# support map `_derive` consumes. A NEW rule is authored ENTIRELY as a spec dict in config — no new
# engine Python for the rule. The interpreter below (value extraction, admissibility, decay,
# aggregation, the shared `_derive`) is the rule-authoring LANGUAGE, authored once; it is NOT
# extended per rule.
# ----------------------------------------------------------------------------------------------
SPEC_VOCAB = frozenset({"max", "mean", "sum", "count", "weighted-mean", "majority",
                        "bayesian-combine"})
_ADMISSIBLE_KINDS = frozenset({"OBSERVATION", "TESTIMONY", "RECORD", "ANCHORED"})

def _spec_value(ev: dict, field: str) -> float:
    """The scalar each admissible source contributes toward a claim's support (in [0,1])."""
    if field == "reliability":
        return float(ev.get("reliability", 0.0) or 0.0)
    if field == "confidence":
        return float((ev.get("verity") or {}).get("confidence", 0.0) or 0.0)
    if field == "reliability_x_confidence":
        r = float(ev.get("reliability", 0.0) or 0.0)
        c = float((ev.get("verity") or {}).get("confidence", 0.0) or 0.0)
        return r * c
    raise ValueError(f"unknown value_field {field!r}")

def _spec_decay_factor(ev: dict, decay: dict) -> float:
    """Deterministic recency factor `0.5**((as_of - captured_at).days / half_life_days)`.
    Explicit `as_of` only (never the wall-clock); evidence captured after as_of keeps factor 1.0;
    undateable/future capture treated fresh. Same semantics as the registry `recency` rule."""
    as_of = _parse_rfc3339(decay["as_of"])
    half = float(decay.get("half_life_days", 30.0))
    if half <= 0:
        raise ValueError("rule_spec decay requires half_life_days > 0")
    try:
        cap = _parse_rfc3339(str(ev.get("captured_at", "")))
    except ValueError:
        cap = as_of
    days = max(0, (as_of - cap).days)
    return 0.5 ** (days / half)

def _spec_admissible(ev: dict, spec: dict) -> bool:
    kinds = spec.get("admissible_kinds")
    if kinds is None:
        return True
    return ev.get("kind") in kinds

def _spec_source(ev: dict, spec: dict) -> tuple[float, float]:
    """(transformed scalar incl. optional recency decay, weight=confidence) for one admissible source."""
    val = _spec_value(ev, spec.get("value_field", "reliability"))
    if spec.get("decay"):
        val *= _spec_decay_factor(ev, spec["decay"])
    weight = float((ev.get("verity") or {}).get("confidence", 0.0) or 0.0)
    return val, weight

def _aggregate(op: str, sources: list[tuple], spec: dict) -> float:
    """Aggregate the admissible per-source (val, weight) pairs into one per-claim support scalar."""
    n = len(sources)
    if op == "max":
        return round(max((s[0] for s in sources), default=0.0), 4)
    if op == "sum":
        return round(sum(s[0] for s in sources), 4)
    if op == "mean":
        return round((sum(s[0] for s in sources) / n) if n else 0.0, 4)
    if op == "count":
        return float(n)
    if op == "weighted-mean":
        wsum = sum(s[1] for s in sources)
        return round((sum(s[0] * s[1] for s in sources) / wsum) if wsum else 0.0, 4)
    if op == "majority":
        thresh = spec.get("source_threshold", 0.85)
        votes = sum(1 for s in sources if s[0] >= thresh)
        return round((votes / n) if n else 0.0, 4)
    if op == "bayesian-combine":
        # Reliability-likelihood posterior (Sprint 16): each admissible source value v is treated
        # as P(claim | source_i) — an INDEPENDENT likelihood given the claim — and combined under
        # Bayes with an explicit authoring prior: O = odds(prior) * prod_i (v_i / (1 - v_i)),
        # posterior = O / (1 + O). EXPRESSES WHAT `max` CANNOT: many weak-but-independent sources
        # can raise support ABOVE every single source (true corroboration synthesis), not merely
        # be bounded by the strongest witness. DETERMINISTIC: all params explicit (never the
        # wall-clock); the per-source weight (confidence) is deliberately unused — each independent
        # source contributes ONE equal likelihood (distinct from `weighted-mean`).
        prior = spec.get("prior")
        if not (isinstance(prior, (int, float)) and 0.0 < prior < 1.0):
            raise ValueError("bayesian-combine requires 0 < prior < 1 (explicit, authored)")
        if n == 0:
            return round(float(prior), 4)          # no evidence -> the prior
        odds = prior / (1.0 - prior)
        for (v, _w) in sources:
            if v >= 1.0:
                return 1.0                          # a certain source pins the claim in the support
            if v <= 0.0:
                return 0.0                          # a source proving the claim false
            odds *= v / (1.0 - v)
        return round(odds / (1.0 + odds), 4)
    raise ValueError(f"unknown aggregate op {op!r}")

def compile_rule_spec(spec: dict) -> dict:
    """Validate a declarative rule-authoring spec loudly (never silently coerce); return a verified
    copy. The spec is DATA; this compiler is the interpreter, authored once, not per rule."""
    if not isinstance(spec, dict) or "aggregate" not in spec:
        raise ValueError("rule_spec must be a dict with an `aggregate` op — got "
                         + json.dumps(spec, default=str)[:200])
    op = spec["aggregate"]
    if op not in SPEC_VOCAB:
        raise ValueError(f"unknown aggregate op {op!r}; rule-authoring vocabulary: {sorted(SPEC_VOCAB)}")
    vf = spec.get("value_field", "reliability")
    if vf not in ("reliability", "confidence", "reliability_x_confidence"):
        raise ValueError(f"unknown value_field {vf!r}")
    kinds = spec.get("admissible_kinds")
    if kinds is not None:
        bad = [k for k in kinds if k not in _ADMISSIBLE_KINDS]
        if bad:
            raise ValueError(f"unknown evidence kind(s) {bad}; admissible kinds: {sorted(_ADMISSIBLE_KINDS)}")
    if op == "majority":
        st = spec.get("source_threshold", 0.85)
        if not (0.0 <= st <= 1.0):
            raise ValueError("majority requires 0 <= source_threshold <= 1")
    if op == "bayesian-combine":
        prior = spec.get("prior")
        if not (isinstance(prior, (int, float)) and 0.0 < prior < 1.0):
            raise ValueError("bayesian-combine requires an explicit 0 < prior < 1 "
                             "(got %r)" % (prior,))
    if spec.get("decay") is not None:
        _parse_rfc3339(spec["decay"]["as_of"])      # loud: as_of must be RFC3339
        if float(spec["decay"].get("half_life_days", 30.0)) <= 0:
            raise ValueError("rule_spec decay requires half_life_days > 0")
    return dict(spec)                               # verified copy

def _spec_support(ctx: dict, params: dict, spec: dict) -> dict:
    """Compiled spec rule body: per-claim support from the configured admittance + value + decay +
    aggregation, then the SHARED `_derive` (identical dispute semantics to any registry rule)."""
    op = spec["aggregate"]
    sup: dict[str, float] = {}
    for claim in ctx["claims"]:
        sources = []
        for ev in ctx["supporting"].get(claim["uri"], []):
            if not _spec_admissible(ev, spec):
                continue
            sources.append(_spec_source(ev, spec))
        sup[claim["uri"]] = _aggregate(op, sources, spec)
    return _derive(sup, params)


def normalize_reconcile(rc: dict) -> dict:
    """Reconcile params support BOTH shapes: {rule, params:{...}} (Sprint-14, explicit) and the
    legacy {rule, threshold, support_floor,...} (Sprint-13) — non-`rule` keys merge into params."""
    params = dict(rc.get("params") or {})
    for k, v in rc.items():
        if k not in ("rule", "params"):
            params.setdefault(k, v)
    return params


def reconcile(sub: Substrate, cfg: dict) -> dict:
    """Return {claim_support:{uri:float}, conflict:bool, uncertainty:bool, disputed:[uris],
    determined:[uris]} via the CONFIGURED rule. A rule is EITHER a registry name
    (cfg["reconcile"]["rule"], Sprint 14) OR a declarative rule-authoring spec
    (cfg["reconcile"]["rule_spec"], Sprint 15). Both land on the shared `_derive`.
    Loud on an unknown registry rule or an invalid spec — never silently coerced."""
    rc = cfg["reconcile"]
    if "rule_spec" in rc:                       # Sprint 15: a rule authored as config text
        spec = compile_rule_spec(rc["rule_spec"])
        params = normalize_reconcile(rc)
        ctx = {"claims": cfg["claims"], "supporting": _supporting_index(cfg["claims"], sub), "sub": sub}
        return _spec_support(ctx, params, spec)
    rule = rc["rule"]
    fn = RULES.get(rule)
    if fn is None:
        raise ValueError(f"unknown reconciliation rule {rule!r}; available: {sorted(RULES)}")
    params = normalize_reconcile(rc)
    ctx = {"claims": cfg["claims"], "supporting": _supporting_index(cfg["claims"], sub), "sub": sub}
    return fn(ctx, params)


# ----------------------------------------------------------------------------------------------
# The minimal signed event helper (appends to the append-only ledger + applies state_update).
# ----------------------------------------------------------------------------------------------
def _ev(sub: Substrate, uri: str, kind: str, signer: str, detail: str,
        updates: list[dict], i: int) -> None:
    sub.record({
        "uri": uri, "type": kind,
        "event_id": f"ev-adj-{uri.split('/')[-1]}-{i}",
        "correlation_id": f"corr-adj-{uri.split('/')[-1]}",
        "causation_id": f"ev-adj-prev-{i}",
        "idempotency_key": f"idem-adj-{uri.split('/')[-1]}-{i}",
        "signature": f"signed-by-{signer}", "occurred_at": now_iso(),
        "actor": signer, "detail": detail, "state_update": updates}, signer)


# ----------------------------------------------------------------------------------------------
# The generic lifecycle — runs ANY configured scenario. Returns (ok, checks, dispute_uri, sub).
# ----------------------------------------------------------------------------------------------
def run_scenario(cfg: dict, sub: Substrate, *, i_base: int = 100,
                 unresolved: bool = False) -> tuple[bool, list[tuple], str, Substrate]:
    """Drive one configured episode (or its `unresolvable` thin-evidence sub-dispute) through the
    lifecycle. NO per-scenario code — everything comes from `cfg`."""
    L = cfg["label"]; A = cfg["authority"]
    ok = True; checks: list[tuple] = []
    def check(name, cond, why=""):
        nonlocal ok
        ok &= bool(cond)
        checks.append((name, bool(cond), why))
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}{'  — ' + why if why else ''}")

    n = {"i": i_base}
    def ev(uri, kind, signer, detail, updates):
        _ev(sub, uri, kind, signer, detail, updates, n["i"]); n["i"] += 1

    # ---- provision: actors, relationships, authority, obligations, right of appeal ----
    prov_updates = [{"uri": a, "type": t} for a, t in cfg["actors"].items()]
    prov_updates += list(cfg["relationships"].values())
    prov_updates += list(cfg["obligations"].values())
    prov_updates += [{"uri": A["dispute"], "holder": A["adjudicator_person"], "grants": ["adjudicate"], "roles": ["adjudicator"]},
                     {"uri": A["appeal"], "holder": A["appeal_person"], "grants": ["adjudicate_appeal"], "roles": ["appeal-adjudicator"]},
                     {"uri": cfg["appeal_right"], "holder": cfg["claimants"][0], "type": "APPEAL",
                      "subject": "DUPLICATE", "scope": [cfg["dispute_about"]],
                      "purpose": "right to appeal the determination"}]
    ev("event://%s/provision" % L, "STATE_CHANGE", cfg["registrar"],
       "provision actors, relationships, obligations, adjudicator+appeal authority, appeal right",
       prov_updates)

    # ---- the ≥2 conflicting claims ----
    claims = [dict(c) for c in cfg["claims"]]
    if unresolved:  # thin-evidence variant (the sub-dispute config carries its own claims/evidence)
        claims = [dict(c) for c in cfg["unresolvable"]["claims"]]
        for c in claims:
            c["epistemic_status"] = "claimed"
    else:
        for c in claims:
            c["epistemic_status"] = "claimed"
    ev("event://%s/claims" % L, "STATE_CHANGE", cfg["registrar"],
       "record %d conflicting claims" % len(claims), claims)
    for c in claims:
        assert (sub.graph.get(c["uri"]) or {}).get("statement") == c["statement"], c["uri"]

    # ---- the conflicting evidence with provenance + reliability ----
    evf = cfg["unresolvable"]["evidence"] if unresolved else cfg["evidence"]
    ev("event://%s/evidence" % L, "STATE_CHANGE", cfg["registrar"],
       "record conflicting evidence with provenance + reliability", list(evf.values()))
    # mark substantive claims disputed once contradictory evidence attaches
    for c in claims:
        ev("event://%s/claim-advance" % L, "STATE_CHANGE", cfg["registrar"],
           f"evidence attaches -> claim disputed",
           [{**sub.graph.get(c["uri"]), "epistemic_status": "disputed"}])

    # ---- conflict detection + uncertainty via the configured reconciliation rule ----
    rec = reconcile(sub, cfg)
    rc_params = normalize_reconcile(cfg["reconcile"])
    _rc = cfg["reconcile"]
    _rule_lab = _rc["rule"] if "rule" in _rc else f"spec:{_rc['rule_spec'].get('name', 'unnamed')}"
    check("CONFLICT/UNCERTAINTY via the configured reconciliation rule",
          rec["conflict"] or rec["uncertainty"],
          f"reconcile[{_rule_lab}, floor={rc_params.get('support_floor', 0.0):g}, "
          f"threshold={rc_params.get('threshold', 0.0):.2f}] disputed={rec['disputed']} "
          f"conflict={rec['conflict']} uncertainty={rec['uncertainty']} "
          f"determined={rec['determined']}")

    # ---- dispute OPEN ----
    dbase = cfg["unresolvable"]["dispute"] if unresolved else cfg["dispute"]
    dispute = {**dbase,
               "lifecycle_state": "OPEN", "epistemic_state": "UNDETERMINED",
               "determination": None, "resolution_type": None, "reopened": False,
               "available_resolutions": list(cfg["options"]),
               "conflict": {"detected": rec["conflict"], "uncertainty": rec["uncertainty"],
                            "claim_support": rec["claim_support"]}}
    ev("event://%s/open-dispute" % L, "STATE_CHANGE", cfg["registrar"],
       "dispute OPEN with parties/about + additive lifecycle/epistemic + resolutions", [dispute])
    du = dispute["uri"]
    d = sub.graph.get(du)
    check("DISPUTE OPEN, parties+about recorded; UNRESOLVED is an available resolution",
          d and d["status"] == "OPEN" and d.get("about") is not None
          and any("unres" in o.lower() or o == "do-nothing"
                  for o in (d.get("available_resolutions") or [])),
          f"status={d['status']} lifecycle={d.get('lifecycle_state')}")
    ev("event://%s/lifecycle-advance" % L, "STATE_CHANGE", cfg["registrar"],
       "conflicting evidence gathered -> EVIDENCE_COLLECTION -> CONTESTED",
       [{**sub.graph.get(du), "lifecycle_state": "EVIDENCE_COLLECTION"},
        {**sub.graph.get(du), "lifecycle_state": "CONTESTED"}])

    # ---- resolution options ranked (utilities + §6 gate) ----
    ranked = rank(cfg)
    best = machine_eligible_best(ranked)
    check("OPTIONS RANKED incl. unresolved/do-nothing baseline (no forced winner)",
          any("unres" in r["option"].lower() or r["option"] == "do-nothing"
              for r in ranked) and ("unres" in best["option"].lower()
                                    or "do-nothing" == best["option"] or not best["floor_gated"]),
          f"machine-eligible best = {best['option']}@{best['utility']:.3f}; "
          f"gated={[r['option'] for r in ranked if r['floor_gated']]}")

    # ---- advisory decision:// (contained: no trust://, not a determination) ----
    adv = {"uri": f"decision://{L}/agent-advisory", "by": cfg["registrar"],
           "authority": A["dispute"], "alternatives": cfg["options"], "confidence": 0.7,
           "expected_outcome": "inform determination", "actual_outcome": best["option"],
           "detail": {"ranking": ranked, "machine_eligible_best": best,
                      "tradeoff": render_tradeoff(cfg, ranked)},
           "made_at": now_iso()}
    ev("event://%s/agent-advisory" % L, "DECISION", cfg["registrar"],
       "AI/machine advisory on options (contained: informational only)", [adv])
    adv_trust = [e for e in sub.ledger.entries if e.get("uri") == f"event://{L}/agent-advisory"
                 and any(o.get("uri", "").startswith("trust://") for o in (e.get("state_update") or []))]
    check("ADVISORY IS CONTAINED: recommendation != determination; cannot set Trust",
          not adv_trust and (sub.graph.get(adv["uri"]) or {}).get("by") == cfg["registrar"],
          f"trust_writes={len(adv_trust)}")

    # ---- the §6 authoritative human determination (policy-declared) ----
    if unresolved or rec["uncertainty"] or cfg["determination_policy"] == "unresolved":
        determination, det_kind = "UNRESOLVED", "INSUFFICIENT_EVIDENCE"
        ev("event://%s/adjudicate-unresolved" % L, "DECISION", A["adjudicator_person"],
           "adjudicator determines UNRESOLVED (insufficient admissible basis); case stays OPEN; "
           "Trust untouched",
           [{"uri": f"decision://{L}/unresolved", "by": A["adjudicator_person"],
             "authority": A["dispute"], "alternatives": cfg["options"], "confidence": 0.6,
             "expected_outcome": "resolve conflict", "actual_outcome": "unresolved",
             "detail": {"determination": "UNRESOLVED", "epistemic_state": "INSUFFICIENT_EVIDENCE",
                        "reason": "no admissible source reaches the configured sufficiency "
                                  "threshold; awarding either side is not justified by the basis"},
             "made_at": now_iso()},
            {**sub.graph.get(du), "status": "OPEN", "lifecycle_state": "UNRESOLVED",
             "epistemic_state": "INSUFFICIENT_EVIDENCE", "determination": "UNRESOLVED"}])
        d = sub.graph.get(du)
        check("UNRESOLVED IS VALID: no forced winner; case stays OPEN; epistemic=INSUFFICIENT_EVIDENCE",
              d and d.get("determination") == "UNRESOLVED"
              and d.get("epistemic_state") == "INSUFFICIENT_EVIDENCE" and d.get("status") == "OPEN",
              f"determination={d.get('determination')} epistemic={d.get('epistemic_state')}")
    else:
        policy = cfg["determination_policy"]
        if policy == "adopt-eligible-best":
            determination = best["option"]
        elif policy == "override":  # the §6 adjudicator overrides to a declared (non-gated) option
            determination = cfg["determination"]
            assert determination in cfg["options"], "override determination must be an option"
            assert ("unres" in determination.lower() or determination == "do-nothing"
                    or determination not in cfg.get("floor_gated", set())), (
                "override to a floor-gated option must go through the §6 human floor explicitly")
        else:
            raise ValueError(f"unknown determination_policy {policy!r}")
        ev("event://%s/adjudicate" % L, "DECISION", A["adjudicator_person"],
           f"authorized human determination: {determination} (ranking in view)",
           [{"uri": f"decision://{L}/determination", "by": A["adjudicator_person"],
             "authority": A["dispute"], "alternatives": cfg["options"],
             "confidence": 0.8, "evidence": [e for evf in (cfg["unresolvable"]["evidence"] if unresolved
                                                           else cfg["evidence"]).values()
                                             for e in ([evf["uri"]] if evf.get("supports") else [])],
             "expected_outcome": determination, "actual_outcome": determination,
             "detail": {"determination": determination, "machine_eligible_best": best["option"]},
             "made_at": now_iso()},
            {**sub.graph.get(du), "status": "ADJUDICATED", "lifecycle_state": "ADJUDICATION",
             "epistemic_state": "RESOLVED_DETERMINED", "determination": determination,
             "resolution_type": determination}])
        # resolve -> accept -> execute -> verify -> close (additive lifecycle)
        ev("event://%s/resolution" % L, "STATE_CHANGE", A["adjudicator_person"],
           f"resolution {determination} executed -> ACCEPTED -> EXECUTED",
           [{**sub.graph.get(du), "lifecycle_state": "RESOLUTION"},
            {**sub.graph.get(du), "lifecycle_state": "ACCEPTED"},
            {**sub.graph.get(du), "lifecycle_state": "EXECUTED",
             "resolution_outcome": cfg["resolution_outcome"]}])
        ev("event://%s/verify" % L, "DECISION", cfg["verify"],
           "outcome verification on completed execution -> VERIFIED -> CLOSED",
           [{**sub.graph.get(du), "lifecycle_state": "VERIFIED"},
            {**sub.graph.get(du), "lifecycle_state": "CLOSED", "status": "RESOLVED",
             "verified": True}])
        ev("event://%s/learn" % L, "STATE_CHANGE", cfg["registrar"],
           "organizational learning: recorded", [
               {"uri": f"evidence://{L}/learning-note", "kind": "RECORD",
                "source": "post-resolution-postmortem", "captured_at": now_iso(),
                "verity": {"procedure": "postmortem", "confidence": 0.6},
                "reliability": 0.6, "about": "what was learned", "supports": None,
                "learning": cfg["learning"]}])
        d = sub.graph.get(du)
        check("LIFECYCLE REACHES CLOSED with verified outcome + learning",
              d and d.get("lifecycle_state") == "CLOSED"
              and d.get("epistemic_state") == "RESOLVED_DETERMINED",)
        check("AUTHORITY PRESERVED (§7J.9): determination carries the authority it requires",
              (sub.graph.get(f"decision://{L}/determination") or {}).get("authority") == A["dispute"],
              "adjudicated under authority://%s/adjudicate" % L)

    return ok, checks, du, sub


def rec_support_floor(cfg: dict) -> float:
    p = normalize_reconcile(cfg["reconcile"])
    return float(p.get("support_floor", p.get("threshold", 0.9)))


def render_tradeoff(cfg: dict, ranked: list[dict]) -> str:
    w = cfg["weights"]
    head = f"trade-off[{cfg['scene']}; business-model {dict(w)}]"
    lines = [head]
    for r in ranked:
        gate = " FLOOR-GATED" if r["floor_gated"] else ""
        lines.append(f"  {r['utility']:.3f}  {r['option']}{gate}")
    best = machine_eligible_best(ranked)
    lines.append(f"  => machine-eligible best (non-gated): {best['option']} "
                 f"(gated: {[r['option'] for r in ranked if r['floor_gated']]})")
    return "\n".join(lines)


def emit_fixtures(sub: Substrate, outdir: Path, cfg: dict) -> None:
    L = cfg["label"]
    ART = outdir / "artifacts/adjudication"; FX = ART / "fixtures"
    by_uri = {o["uri"]: o for e in sub.ledger.entries for o in (e.get("state_update") or [])}
    groups = (("disputes", ["dispute"]), ("claims", ["claim"]), ("evidence", ["evidence"]),
              ("policies", ["policy"]), ("decisions", ["decision"]),
              ("expectations", ["expectation"]), ("trust", ["trust"]),
              ("actors_offers", ["person", "org", "agent", "entity", "system", "rule",
                                 "authority", "delegation", "consent", "obligation", "right"]),
              ("relationships", ["relationship", "interaction"]), ("events", ["event"]))
    for name, prefixes in groups:
        p = FX / L / f"{name}.json"; p.parent.mkdir(parents=True, exist_ok=True)
        items = [o for u, o in by_uri.items() if u.startswith(tuple(f"{x}://" for x in prefixes))]
        p.write_text(json.dumps(items, indent=2))
    ld = FX / L / "ledger"; ld.mkdir(parents=True, exist_ok=True)
    (ld / "ledger.json").write_text(json.dumps(sub.ledger.to_dict(), indent=2))
    st = FX / L / "statemachines"; st.mkdir(parents=True, exist_ok=True)
    _du = (cfg.get("dispute") or {}).get("uri", "dispute://%s/main" % L)
    (st / "dispute.json").write_text(json.dumps(
        {"uri": _du,
         "states": ["OPEN", "EVIDENCE_COLLECTION", "CONTESTED", "ADJUDICATION", "RESOLUTION",
                    "ACCEPTED", "EXECUTED", "VERIFIED", "CLOSED"]}, indent=2))
    rel = next(iter(cfg["relationships"].values()))
    (st / "relationship.json").write_text(json.dumps(
        {"uri": rel["uri"], "states": ["PROPOSED", "ACTIVE"]}, indent=2))
    gd = ART / "graph"; gd.mkdir(parents=True, exist_ok=True)
    (gd / "current-state.json").write_text(json.dumps(sub.graph.to_dict(), indent=2))


# ----------------------------------------------------------------------------------------------
# SPRINT 18 — the §7L Q7/Q8 cockpit line, FIRST-CLASS in the engine. The ACTIVE reconcile rule +
# its source + learned-or-not this run + the evidence-gated why are rendered BY THE ENGINE for ANY
# generically-driven org (registry rule, hand-authored RULE_LIBRARY spec, or a learned library entry
# added this run). It is data-only (reads `cfg` + the org's own ledger/graph; `library`, when given,
# is a plain dict of named rule specs) so no per-org engine Python is needed. Only additive.
# The Q7 (options incl. do-nothing baseline + trade-off) and Q8 (recommendation w/ authority +
# determination) line is the §7L surface the runner-report cluster (Sprints 16/17) rendered per-org;
# this is the same line as a generic engine render, a superset built on the shared surface
# (`rank`/`machine_eligible_best`/`render_tradeoff`).
# ----------------------------------------------------------------------------------------------
def _cockpit_active_rule(cfg: dict, library: dict | None = None) -> dict:
    """Data-only classification of the ACTIVE reconcile rule + its source class.

    Source classes: `registry` (an engine RULES function named in `reconcile`), `learned` (a
    rule_spec carrying the Sprint-17 additive learned fields — a learned library entry), `rule-library`
    (a rule_spec that matches a provided library entry by `is`-identity or by `name`), and
    `rule-spec-authored` (any other declarative spec). `registry-unknown` guards a registry name the
    engine does not know (loud but non-fatal to the cockpit). Never hotter than the config data.
    """
    rc = cfg["reconcile"]
    if "rule" in rc:
        name = rc["rule"]
        source = "registry" if rc["rule"] in RULES else "registry-unknown"
        return {"active_rule": name, "source": source}
    spec = rc["rule_spec"]
    name = spec.get("name") or "anonymous-rule-spec"
    if ("learned_param" in spec) or ("learned_threshold" in spec):
        return {"active_rule": name, "source": "learned"}
    if library is not None:
        for entry in library.values():
            if entry is spec or (isinstance(entry, dict) and entry.get("name") == name):
                return {"active_rule": name, "source": "rule-library"}
    return {"active_rule": name, "source": "rule-spec-authored"}


def cockpit_q7q8(cfg: dict, sub, *, library: dict | None = None) -> dict:
    """Structured §7L Q7/Q8 cockpit report for a configured org, generic + data-only.

    Returns the ACTIVE reconcile rule, its SOURCE class, whether a learning step CHANGED it this run,
    and the evidence-gated WHY — read from the org's OWN ledger (`decision://<label>/reconcile-learning`
    recorded this run), not from any runner side-table — plus the §7L Q7 options/trade-off and the Q8
    recommendation (with the authority it requires) and the authorized determination.
    Deterministic: depends only on `cfg` + the `sub` graph + the optional data `library`.
    """
    L = cfg["label"]
    rule = _cockpit_active_rule(cfg, library)
    active_rule, source = rule["active_rule"], rule["source"]
    # learned-this-run + the evidence-gated why, read from the org's own ledger.
    lrn = sub.graph.get(f"decision://{L}/reconcile-learning") or {}
    learned_this_run = source == "learned" and bool(lrn)
    if learned_this_run:
        why = ((lrn.get("detail") or {}).get("why")
               or (cfg["reconcile"]["rule_spec"].get("why") or "unchanged"))
    else:
        why = "unchanged"
    # §7L Q7 (options incl. do-nothing/UNRESOLVED baseline) + Q8 (recommendation + determination).
    ranked = rank(cfg)
    best = machine_eligible_best(ranked)
    dispute_uri = (cfg.get("dispute") or {}).get("uri") or f"dispute://{L}/main"
    determination = (sub.graph.get(dispute_uri) or {}).get("determination") or "UNRESOLVED"
    baseline = next((o for o in cfg["options"]
                     if "unres" in o.lower() or o == "do-nothing"), cfg["options"][0])
    return {
        "label": L,
        "dispute_uri": dispute_uri,
        "active_rule": active_rule,
        "source": source,
        "learned_this_run": learned_this_run,
        "why": why,
        "determination": determination,
        "q7": {"options": list(cfg["options"]), "baseline": baseline,
               "machine_eligible_best": best["option"],
               "tradeoff": render_tradeoff(cfg, ranked)},
        "q8": {"recommendation": best["option"],
               "authority": cfg["authority"]["dispute"],
               "determination": determination,
               "floor_gated": [r["option"] for r in ranked if r["floor_gated"]]},
    }


def render_cockpit_q7q8(cfg: dict, sub, *, library: dict | None = None) -> str:
    """Render the engine-native §7L Q7/Q8 cockpit line as plain text for one org.

    Carries BOTH §7L questions: Q7 (what are our options? — the resolution set incl. the
    do-nothing/UNRESOLVED baseline + machine-eligible best) and Q8 (what should we do? — the
    recommendation with the authority it requires, and the authorized determination), plus the ACTIVE
    rule + source + learned-or-not + why. Identical inputs -> identical output (deterministic).
    """
    c = cockpit_q7q8(cfg, sub, library=library)
    ln = "True" if c["learned_this_run"] else "False"
    return "\n".join([
        f"# §7L Q7/Q8 cockpit (engine-native) — org {c['label']}",
        f"Q7 options: {', '.join(c['q7']['options'])}  |  baseline: {c['q7']['baseline']}  |  "
        f"machine-eligible best: {c['q7']['machine_eligible_best']}",
        f"Q8 recommendation: {c['q8']['recommendation']} (authority {c['q8']['authority']}; "
        f"floor-gated: {c['q8']['floor_gated']})  ->  determination: {c['determination']}",
        f"ACTIVE reconcile rule: {c['active_rule']}  |  source: {c['source']}  |  "
        f"learned-this-run: {ln}",
        f"why: {c['why']}",
    ])


# ----------------------------------------------------------------------------------------------
# SPRINT 19 — the FULL §7L Q1–Q10 morning cockpit, rendered BY the engine for ANY configured org.
# `cockpit_s7l(cfg, sub, *, library=None)` returns a structured dict of all TEN §7L questions
# (Q1 state/events, Q2 change, Q3 attention, Q4 exceptions, Q5 root-cause WITH epistemic status,
# Q6 forecast-if-nothing-changes, Q7 options+trade-off, Q8 recommendation w/ authority,
# Q9 ownership/capability/authority, Q10 verified outcome + learning), each answered with the
# recorded-data evidence the org's OWN graph/ledger/config carry. `render_cockpit_s7l(...)` is the
# plain-text §7L Q1–Q10 cockpit. It is a STRICT SUPERSET of the Sprint-18 `cockpit_q7q8` line:
# Q7 and Q8 are delegated to that function by construction (same dict blocks), so the engine's
# Q7/Q8 line is byte-identical whichever function drives it. No per-org Python; additive; frozen
# 49 `$defs`/URI cap; SPEC v0.22. Deterministic (identical inputs -> identical dict + render).
# Q6 NEVER fabricates: a forecast is only produced when a recorded realized-vs-expected SERIES
# exists on the org's graph; otherwise it plainly says "cannot forecast from recorded data".
# ----------------------------------------------------------------------------------------------
def _ledger_dispute_walk(sub, dispute_uri: str) -> list[str]:
    """The recorded lifecycle_state walk on `dispute_uri`, from the append-only ledger, in order.
    Collects every `lifecycle_state` value observed on the dispute across state_update objects."""
    walk: list[str] = []
    seen: set[str] = set()
    for e in getattr(sub.ledger, "entries", []) or []:
        for o in (e.get("state_update") or []):
            if o.get("uri") != dispute_uri:
                continue
            ls = o.get("lifecycle_state")
            if ls and ls not in seen:
                seen.add(ls)
                walk.append(ls)
    return walk


def _recorded_forecast_series(sub) -> list[dict]:
    """A recorded realized-vs-expected time series on the org's graph, if any. Returns [] when
    none exists (the honest no-forecast case). We look for any graph object carrying a list of
    per-period realized/expected points (e.g. a `metric://` with a `points`/`series` list). Never
    the wall-clock, never an invented number."""
    series = []
    for o in (sub.graph.to_dict() or {}).get("objects", []):
        for key in ("points", "series", "realized_series"):
            pts = o.get(key)
            if isinstance(pts, list) and pts and all(isinstance(p, dict) for p in pts):
                series.append({"uri": o.get("uri"), "key": key, "points": pts})
                break
    return series


def _graph_objects(sub) -> list[dict]:
    d = sub.graph.to_dict() or {}
    objs = d.get("objects")
    if isinstance(objs, list):
        return objs
    # fallback: a uri-value map
    out = []
    for u, o in d.items():
        if isinstance(o, dict) and "uri" in o:
            out.append(o)
    return out


def cockpit_s7l(cfg: dict, sub, *, library: dict | None = None) -> dict:
    """The complete §7L Q1–Q10 morning cockpit for ANY configured org, data-only.

    All ten questions are answered from the org's own graph/ledger/config — no per-org engine
    Python. Q7/Q8 ARE the Sprint-18 `cockpit_q7q8` blocks (strict superset by construction).
    Deterministic: depends only on `cfg` + the `sub` graph/ledger + the optional data `library`.
    """
    L = cfg["label"]
    # ---- Sprint-18 surface: ACTIVE rule + source + learned-or-not + why, and Q7/Q8 -------------
    base = cockpit_q7q8(cfg, sub, library=library)
    du = base["dispute_uri"]
    d = sub.graph.get(du) or {}
    rec = reconcile(sub, cfg)                    # per-claim support + conflict/uncertainty verdicts
    graph_objs = {o.get("uri"): o for o in _graph_objects(sub) if o.get("uri")}

    # ---- which claims/evidence to report (the recorded-dispute predicates) ----------------------
    claims_src = cfg["claims"]
    claims = []
    for c in claims_src:
        go = sub.graph.get(c["uri"]) or c
        claims.append({
            "uri": c["uri"], "proposer": c.get("proposer"),
            "statement": go.get("statement") or c.get("statement"),
            "epistemic_status": go.get("epistemic_status") or "claimed",
            "support": rec["claim_support"].get(c["uri"]),
        })
    evidences = [sub.graph.get(ev["uri"]) or ev for ev in
                 (cfg["unresolvable"]["evidence"].values()
                  if d.get("epistemic_state") == "INSUFFICIENT_EVIDENCE" and d.get("lifecycle_state") == "UNRESOLVED"
                  else cfg["evidence"].values())]

    # ---- decisions + recorded learning on this org's ledger ------------------------------------
    lrn_note = graph_objs.get(f"evidence://{L}/learning-note") or {}
    lrn_dec = graph_objs.get(f"decision://{L}/reconcile-learning") or {}
    learn_entries = []
    if lrn_note.get("learning"):
        learn_entries.append({"uri": lrn_note["uri"], "learning": lrn_note["learning"]})
    if lrn_dec.get("detail") or lrn_dec.get("uri"):
        dt = lrn_dec.get("detail") or {}
        learn_entries.append({"uri": lrn_dec.get("uri"),
                              "learning": dt.get("learning") or dt.get("why") or "reconcile-rule recorded",
                              "learned_threshold": dt.get("learned_threshold")})

    # ---- Q1 state/events over the period --------------------------------------------------------
    entries = getattr(sub.ledger, "entries", []) or []
    events = [{"uri": e.get("uri"), "type": e.get("type"), "actor": e.get("actor"),
               "detail": e.get("detail")} for e in entries if str(e.get("uri", "")).startswith("event://")]
    q1 = {
        "event_count": len(events),
        "events": [ev["uri"] for ev in events],
        "lifecycle_walk": _ledger_dispute_walk(sub, du),
        "status": d.get("status"), "lifecycle_state": d.get("lifecycle_state"),
        "epistemic_state": d.get("epistemic_state"),
        "evidence": "state/events read off the org's append-only ledger + current dispute state",
    }

    # ---- Q2 change/delta over the period --------------------------------------------------------
    q2 = {
        "recorded_deltas": {
            "dispute_open": bool(events),                       # events recorded this period
            "claims_recorded": len(claims),
            "evidence_recorded": len(evidences),
            "lifecycle_from_to": ([q1["lifecycle_walk"][0]] if q1["lifecycle_walk"] else ["(none)"])
                                 + (["->"] if len(q1["lifecycle_walk"]) > 1 else [])
                                 + ([q1["lifecycle_walk"][-1]] if len(q1["lifecycle_walk"]) > 1 else []),
            "epistemic_from_to": "UNDETERMINED -> %s" % d.get("epistemic_state")
                                 if d.get("epistemic_state") else None,
            "determination": d.get("determination") or "UNRESOLVED",
            "claim_epistemic_deltas": {c["uri"]: c["epistemic_status"] for c in claims},
        },
        "significance": ("determined" if d.get("determination") and d.get("determination") != "UNRESOLVED"
                         else "still-undetermined"),
        "evidence": "delta + significance reconstructed from the recorded life cycle + claim epistemic_status",
    }

    # ---- Q3 prioritized attention (the §7J.5/attention analogue) ---------------------------------
    # Sprint 21: a recorded forecast whose horizon projection crosses a recorded threshold is
    # ITSELF attention ("do nothing and it gets worse"), attached as a forecast-driven item.
    fca = _forecast_closure(cfg, sub)
    attention = []
    if d.get("status") in ("OPEN", "RESOLVED") and d.get("determination") == "UNRESOLVED":
        attention.append({"item": du, "why": "dispute OPEN / UNRESOLVED (no determination yet)"})
    for c in claims:
        if rec.get("determined") and c["uri"] in rec["determined"]:
            continue
        if c["epistemic_status"] in ("claimed", "disputed", "unresolved"):
            attention.append({"item": c["uri"], "why": "claim %s (not DETERMINED)" % c["epistemic_status"]})
    if fca.get("attention_item"):
        attention.append(fca["attention_item"])
    q3_evidence = ("attention = recorded OPEN/UNRESOLVED dispute + non-DETERMINED claims (§7J.5 analogue)"
                   if not fca.get("attention_item") else
                   "attention = recorded OPEN/UNRESOLVED dispute + non-DETERMINED claims "
                   "+ a forecast-driven item when the recorded series' projection crosses a "
                   "recorded threshold (§7J.5 analogue)")
    q3 = {"prioritized": attention, "count": len(attention), "evidence": q3_evidence}

    # ---- Q4 exceptions ---------------------------------------------------------------------------
    exceptions = []
    if d.get("status") == "OPEN" or d.get("lifecycle_state") == "UNRESOLVED":
        exceptions.append({"uri": du, "exception": "OPEN/UNRESOLVED",
                           "epistemic_state": d.get("epistemic_state")})
    if rec.get("uncertainty"):
        exceptions.append({"uri": du, "exception": "uncertainty",
                           "claim_support": {k: v for k, v in rec["claim_support"].items() if v is not None}})
    q4 = {"exceptions": exceptions, "conflict": rec.get("conflict"), "uncertainty": rec.get("uncertainty"),
          "evidence": "exceptions = recorded OPEN/UNRESOLVED disputes + reconcile conflict/uncertainty (§7J.2 analogue)"}

    # ---- Q5 root-cause WITH epistemic status -----------------------------------------------------
    root = []
    for c in claims:
        if c["uri"] in (rec.get("determined") or []):
            root.append({**c, "role": "support-carrying (DETERMINED under the active rule)"})
        elif c["epistemic_status"] in ("disputed", "claimed", "unresolved"):
            root.append({**c, "role": "contested (not determined)"})
    q5 = {
        "root_cause": root,
        "reconcile": {"determined": rec.get("determined"), "disputed": rec.get("disputed"),
                      "conflict": rec.get("conflict"), "uncertainty": rec.get("uncertainty"),
                      "claim_support": rec["claim_support"]},
        "active_rule": base["active_rule"], "rule_source": base["source"],
        "evidence": "root-cause = recorded claim epistemic_status + per-claim support from the configured reconcile rule (§7K.2)",
    }

    # ---- Q6 forecast "if nothing changes" (honest; a projection only when a series is recorded) -----
    # Reuses the same `fca` closure that drove Q3's attention + Q8's do-nothing pricing, so the three
    # questions agree by construction (identical projection, threshold, crossing).
    q6 = fca["q6"]

    # ---- Q7/Q8 delegate to the Sprint-18 line (strict superset by construction) ------------------
    q7 = base["q7"]; q8 = base["q8"]
    # Sprint 21 (additive): where a recorded series exists, price the do-nothing baseline of the
    # trade-off from the SAME deterministic projection that drove Q3 attention + Q6 (Q6→Q3→Q8
    # connected as data). Purely additive fields on the Sprint-18 dicts; the no-data fallback is
    # untouched (absent). The Q8 recommendation is UNCHANGED — the forecast never overrules the
    # §6-floor-gated machine-eligible best, it only prices attention + do-nothing.
    if fca.get("available"):
        q7["tradeoff_do_nothing_impact"] = fca["do_nothing"]["summary"]
        q8["forecast"] = fca["forecast"]
        q8["do_nothing_expected_impact"] = fca["do_nothing"]

    # ---- Q9 ownership / capability / authority ----------------------------------------------------
    ob_uri = cfg.get("dispute_about") or (cfg.get("dispute") or {}).get("about")
    ob = sub.graph.get(ob_uri) or {}
    ob_subjects = ob.get("subject") if isinstance(ob.get("subject"), list) else [ob.get("subject")]
    auth_obj = sub.graph.get(cfg["authority"].get("dispute")) or {}
    recorded_cap = auth_obj.get("capacity") or {}
    if isinstance(recorded_cap, dict) and "value" in recorded_cap:
        q9_capacity = {k: recorded_cap[k] for k in ("value", "unit", "load") if k in recorded_cap}
        q9_capacity["status"] = recorded_cap.get("status", "recorded")
        capability_txt = ("determination authority held by the §6 human adjudicator; obligated party = "
                          "dispute subject; recorded capacity %s %s (load %s)"
                          % (q9_capacity["value"], q9_capacity.get("unit", ""),
                             q9_capacity.get("load", "—")))
        capacity_recorded = True
    else:
        q9_capacity = None
        capability_txt = ("determination authority held by the §6 human adjudicator; obligated party = "
                          "dispute subject")
        capacity_recorded = False
    ownership = {
        "determination_authority": cfg["authority"].get("dispute"),
        "adjudicator": cfg["authority"].get("adjudicator_person"),
        "adjudicator_role_present": bool(graph_objs.get(cfg["authority"].get("adjudicator_person"))),
        "obligated_party": ob_subjects,
        "obligation": ob_uri,
        "appeal_authority": cfg["authority"].get("appeal"),
        "actors": sorted(cfg["actors"].keys()),
        "capacity_recorded": capacity_recorded,
        "capacity": q9_capacity,
        "capability": capability_txt,
        "evidence": ("ownership/authority read from cfg.authority + the recorded obligation the dispute is "
                     "about (§7K.1/§7J.9); capacity read from the recorded additive field on the authority "
                     "object when present"),
    }
    q9 = ownership

    # Sprint 25 (additive): Q9 CAPACITY-ATTENTION from the recorded horizon-wide band. When the
    # recorded-variance band exists (a band_horizon rides the closure) AND the recorded threshold is
    # numeric, add an additive `band_capacity_attention` flag: whether the record-wide HORIZON range
    # (the whole-horizon worst case, band_horizon low..high) signals the recorded threshold — a
    # data-only capacity-attention flag/reason, NEVER an invented capacity number (the recorded
    # `capacity` may be referenced in `why` but is never mutated/invented when absent). No-band /
    # no-data orgs carry NO key -> byte-identical.
    bh = fca.get("band_horizon") if (fca.get("available") and fca.get("band_horizon") is not None) else None
    if bh is not None and fca.get("threshold") is not None:
        _dir = fca.get("direction", "higher-is-better")
        _thr = fca["threshold"]; _ts = fca.get("threshold_source", "threshold")
        _lo, _hi = bh["low"], bh["high"]
        if _dir == "lower-is-better":
            _hz_cross = _hi is not None and _hi > _thr        # high above ceiling -> attention
            _side = "highest side %s above %s %s" % (_hi, _ts, _thr)
        else:
            _hz_cross = _lo is not None and _lo < _thr        # low below target -> attention
            _side = "lowest side %s below %s %s" % (_lo, _ts, _thr)
        _capref = ""
        if capacity_recorded and q9_capacity:
            _capref = (", recorded capacity %s %s (load %s)"
                       % (q9_capacity.get("value"), q9_capacity.get("unit", ""),
                          q9_capacity.get("load", "—")))
        _why = ("horizon-wide recorded band %s…%s across %d projection periods — %s — %s the "
                "recorded %s threshold%s"
                % (_lo, _hi, len(fca.get("band_periods") or []), _side,
                   "signals" if _hz_cross else "stays safe of", _dir.split("-")[0], _capref))
        q9["band_capacity_attention"] = {
            "flag": bool(_hz_cross), "why": _why,
            "low": _lo, "high": _hi, "crosses": bool(_hz_cross)}

    # Sprint 26 (additive): Q9 CAPACITY-PLANNING attention — a data-only flag/reason emitted ONLY
    # where the org RECORDS a numeric `capacity` on its authority object AND a band + numeric
    # threshold exist. ONE deterministic rule from recorded numbers only:
    #   at-capacity when the recorded load >= 1.0; deficit when the horizon band's worst-side
    #   magnitude (low for higher-is-better, high for lower-is-better) reaches/exceeds the recorded
    #   capacity VALUE; otherwise headroom. `why` states the recorded capacity value/unit/load and the
    #   horizon-wide band, and labels headroom / at-capacity / deficit as a derived REASON — NEVER a
    #   fabricated capacity number, NEVER a directive. Orgs that record NO capacity carry NO key
    #   (byte-identical superset of Sprint 25); `band_capacity_attention` is untouched.
    if (capacity_recorded and q9_capacity is not None
            and bh is not None and fca.get("threshold") is not None):
        # Sprint 27: the reason/flag now come from the SHARED `_capacity_reason` helper (the same
        # sole deterministic rule), so the Q9 `capacity_planning_attention` label and the new
        # Q7/Q8 `capacity_constraint.reason` AGREE BY CONSTRUCTION — one rule, recorded numbers
        # only (output byte-identical to Sprint 26).
        _label, _flag = _capacity_reason(
            q9_capacity, bh, fca.get("direction", "higher-is-better"))
        _cap_txt = "%s %s (load %s)" % (q9_capacity.get("value"), q9_capacity.get("unit", ""),
                                        q9_capacity.get("load", "—"))
        _why = ("capacity-planning: recorded capacity %s vs the horizon-wide recorded band "
                "%s…%s across %d projection periods — derived %s from recorded numbers only "
                "(not a directive, no invented capacity)"
                % (_cap_txt, bh["low"], bh["high"], len(fca.get("band_periods") or []), _label))
        q9["capacity_planning_attention"] = {"flag": _flag, "why": _why}

    # Sprint 27 (additive): make the recorded capacity a data-only CONSTRAINT on the §7L Q7/Q8
    # trade-off. ONLY where the org records a numeric capacity AND a band + numeric threshold exist
    # (the same condition that emits Q9 `capacity_planning_attention`), add a parallel additive
    # `capacity_constraint` block on BOTH `q7` (the trade-off) and `q8` (the recommendation) that:
    #   - names the recorded capacity value/unit/load and the horizon-wide recorded band;
    #   - derives ONE reason label from recorded numbers only via the SHARED `_capacity_reason`
    #     rule -> `reason` always equals the Q9 `capacity_planning_attention` label BY CONSTRUCTION
    #     (headroom / at-capacity / deficit);
    #   - in `options_flagged`, marks any capacity-consuming (non-baseline) option `capacity_risk`
    #     ONLY when the reason is not headroom; NEVER `capacity_infeasible` (no per-option capacity
    #     requirement is ever recorded, so infeasibility is never derivable) and NEVER the baseline
    #     (do-nothing/UNRESOLVED consumes no capacity). In headroom, no option is flagged.
    # It NEVER removes an option, NEVER changes the frozen `rank`/`machine_eligible_best`, NEVER
    # overrules the §6 human, and NEVER invents a capacity figure or a per-option requirement —
    # a label/default, recorded-data only. A genuinely capacity-constrained optimization that
    # re-ranks the recommendation stays explicitly out of scope (deterministic advisory stance).
    # C2-safe (no `at|time|deadline|expires|expiry|effective|due|since` suffix on any key).
    if (capacity_recorded and q9_capacity is not None
            and bh is not None and fca.get("threshold") is not None):
        _cclabel, _ccflag = _capacity_reason(
            q9_capacity, bh, fca.get("direction", "higher-is-better"))
        _reqs = auth_obj.get("capacity_requirements") if isinstance(auth_obj, dict) else None
        _cc_base = q7.get("baseline")
        if isinstance(_reqs, dict) and _reqs:
            # Sprint 29 (additive): a RECORDED per-option requirement exists -> label a SPECIFIC
            # option `capacity_infeasible` (its requirement > available capacity, available = the
            # recorded capacity VALUE − the recorded load, same unit) vs `capacity_risk` otherwise.
            # The per-option rule is exercised ONLY here (a no-requirements org keeps today's block
            # byte-identical); the baseline is never flagged; `reason`/`flag` still come from the
            # org-level `_capacity_reason` rule unchanged.
            _cc_flags = _per_option_capacity_flags(
                q9_capacity, _reqs, cfg.get("options", []), _cc_base,
                non_headroom=(_cclabel != "headroom"))
        else:
            _cc_flags = {}
            if _cclabel != "headroom":
                for _o in cfg.get("options", []):
                    if _o != _cc_base:
                        _cc_flags[_o] = "capacity_risk"
        _cc_cap_txt = "%s %s (load %s)" % (q9_capacity.get("value"),
                                           q9_capacity.get("unit", ""),
                                           q9_capacity.get("load", "—"))
        _cc = {
            "recorded_capacity": _cc_cap_txt,
            "horizon_band": {"low": bh["low"], "high": bh["high"]},
            "reason": _cclabel,
            "flag": _ccflag,
            "options_flagged": _cc_flags,
            "note": ("derived capacity-constraint reason from recorded numbers only — never an "
                     "invented figure, never a directive, never an option removal; the Q8 "
                     "recommendation is UNCHANGED (the §6 human always rules)"),
        }
        if isinstance(_reqs, dict) and _reqs:
            # Sprint 29 (additive): name the RECORDED per-option requirements + the derived available
            # capacity on the block so every capacity_infeasible/capacity_risk label traces to a
            # recorded number (available = recorded capacity VALUE − recorded load, same unit). Field
            # keys C2-safe (no temporal suffix). A no-requirements org carries NONE of these.
            _cc["per_option_requirements"] = dict(_reqs)
            _avail = None
            _v_n = _num(q9_capacity.get("value")) if isinstance(q9_capacity, dict) else None
            _l_n = _num(q9_capacity.get("load")) if isinstance(q9_capacity, dict) else None
            if _v_n is not None and _l_n is not None:
                _avail = round(_v_n - _l_n, 4)
            if _avail is not None:
                _cc["available_capacity"] = _avail
        q7["capacity_constraint"] = dict(_cc)
        q8["capacity_constraint"] = dict(_cc)

    # ---- Q10 verified outcome + organizational learning -------------------------------------------
    q10 = {
        "verified": bool(d.get("verified")),
        "lifecycle_state": d.get("lifecycle_state"),
        "status": d.get("status"),
        "determination": d.get("determination"),
        "resolution_outcome": d.get("resolution_outcome") or cfg.get("resolution_outcome"),
        "learning_entries": learn_entries,
        "evidence": "verified + outcome + learning read from the recorded dispute state + evidence://<label>/learning-note and decision://<label>/reconcile-learning on the org's ledger",
    }

    return {
        "label": L, "dispute_uri": du,
        # Sprint-18 surface reused verbatim (strict superset):
        "active_rule": base["active_rule"], "source": base["source"],
        "learned_this_run": base["learned_this_run"], "why": base["why"],
        "determination": base["determination"],
        "q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5, "q6": q6,
        "q7": q7, "q8": q8, "q9": q9, "q10": q10,
    }


def render_cockpit_s7l(cfg: dict, sub, *, library: dict | None = None) -> str:
    """The complete §7L Q1–Q10 morning cockpit for one org, plain text, data-only. Identical
    inputs -> identical output (deterministic). Q7/Q8 lines are the Sprint-18 engine lines."""
    c = cockpit_s7l(cfg, sub, library=library)
    L = c["label"]
    q1 = c["q1"]; q2 = c["q2"]; q3 = c["q3"]; q4 = c["q4"]; q5 = c["q5"]
    q6 = c["q6"]; q7 = c["q7"]; q8 = c["q8"]; q9 = c["q9"]; q10 = c["q10"]
    ln = "True" if c["learned_this_run"] else "False"
    lines = [f"# §7L Q1–Q10 cockpit (engine-native) — org {L}"]
    lines.append(f"ACTIVE reconcile rule: {c['active_rule']}  |  source: {c['source']}  |  "
                 f"learned-this-run: {ln}  |  why: {c['why']}")
    lines.append("Q1. what happened?  state/events: %d recorded events; dispute lifecycle "
                 "%s; status=%s lifecycle=%s epistemic=%s"
                 % (q1["event_count"], ("->".join(q1["lifecycle_walk"]) if q1["lifecycle_walk"] else "(none)"),
                    q1["status"], q1["lifecycle_state"], q1["epistemic_state"]))
    frm = q2["recorded_deltas"]["lifecycle_from_to"]
    lines.append("Q2. what changed?  life cycle %s; epistemic %s; determination=%s; "
                 "claim epistemic=%s; significance=%s"
                 % (" ".join(frm), q2["recorded_deltas"]["epistemic_from_to"],
                    q2["recorded_deltas"]["determination"],
                    {k.split("/")[-1]: v for k, v in q2["recorded_deltas"]["claim_epistemic_deltas"].items()},
                    q2["significance"]))
    lines.append("Q3. what matters?  prioritized attention (%d): %s"
                 % (q3["count"], "; ".join(
                     (i["item"] + " [" + i.get("tag", "state") + "] — " + i["why"])
                     if i.get("tag") else i["item"] + " — " + i["why"]
                     for i in q3["prioritized"]) or "nothing flagged"))
    lines.append("Q4. what is going wrong?  exceptions (%d): %s  |  reconcile conflict=%s uncertainty=%s"
                 % (len(q4["exceptions"]),
                    "; ".join(x["uri"] + " (" + x["exception"] + ")" for x in q4["exceptions"]) or "none",
                    q4["conflict"], q4["uncertainty"]))
    rc_desc = "; ".join("%s support=%s %s" % (r["uri"].split("/")[-1], r.get("support"), r["role"])
                        for r in q5["root_cause"]) or "(none)"
    lines.append("Q5. why is it going wrong?  root-cause [epistemic status]: %s  |  under rule %s (%s)"
                 % (rc_desc, q5["active_rule"], q5["rule_source"]))
    if q6["forecast_available"]:
        proj = "; ".join("period %s -> %s" % (p["period"], p["projected"]) for p in q6["projections"])
        lines.append("Q6. what if we do nothing?  project (holding the recorded trend) from last actual "
                     "%s + mean delta %s: %s  |  recorded variance %s" %
                     (q6["last_actual"], q6["mean_delta"], proj, q6.get("recorded_variance")))
    else:
        lines.append("Q6. what if we do nothing?  %s" % q6["forecast"])
    lines.append("Q7. what are our options?  %s  |  baseline %s  |  machine-eligible best: %s"
                 % (", ".join(q7["options"]), q7["baseline"], q7["machine_eligible_best"]))
    lines.append("Q8. what should we do?  recommendation %s (authority %s; floor-gated %s)  ->  "
                 "determination %s"
                 % (q8["recommendation"], q8["authority"], q8["floor_gated"], c["determination"]))
    if q8.get("do_nothing_expected_impact"):
        dn = q8["do_nothing_expected_impact"]
        band_txt = ""
        if dn.get("band"):
            _b = dn["band"]
            band_txt = (" |  recorded band %s…%s (± σ %s, crosses=%s)"
                        % (_b["low"], _b["high"], _b["sigma"], _b["crosses"]))
        lines.append("    trade-off / do-nothing expected-impact: %s (baseline %s, priced=%s, "
                     "on-target=%s)%s"
                     % (dn["summary"], dn.get("baseline"), dn.get("priced"),
                        dn.get("on_target"), band_txt))
    lines.append("Q9. who does it, authority/capacity?  adjudicator %s (authority %s), obligated "
                 "party %s, appeal %s, actors %s%s"
                 % (q9["adjudicator"], q9["determination_authority"],
                    ", ".join(o or "?" for o in (q9["obligated_party"] or [])),
                    q9["appeal_authority"], len(q9["actors"]),
                    (", capacity %s %s (load %s)" % (q9["capacity"]["value"], q9["capacity"].get("unit", ""),
                                                     q9["capacity"].get("load", "—")))
                    if q9.get("capacity_recorded") and q9.get("capacity") else ""))
    lrn = "; ".join("%s[%s]" % (e["uri"], e["learning"][:60] + ("…" if len(e["learning"]) > 60 else ""))
                    for e in q10["learning_entries"]) or "(none recorded)"
    lines.append("Q10. did it work, what did we learn?  verified=%s status=%s determination=%s; "
                 "outcome=%s; learning: %s"
                 % (q10["verified"], q10["status"], q10["determination"],
                    q10["resolution_outcome"] or "(none recruited)", lrn))
    return "\n".join(lines)

# ----------------------------------------------------------------------------------------------
# SPRINT 21 — forecast → attention → expected-impact closure (additive). Sprint 20 made the
# recorded Q6 forecast + Q9 capacity answered AS DATA via `forecast_metric` and a recorded
# `metric://` realized-vs-expected series + an additive `capacity` field, but disclosed the next
# honest frontier: the Q6 projection is COMPUTED and RENDERED but not CONNECTED to the org's
# decision surface. Sprint 21 closes a bounded slice — the recorded forecast DRIVES the §7L Q3
# attention and the Q8 expected-impact / trade-off do-nothing baseline, deterministically and
# data-only: when the recorded series' horizon projection crosses a recorded threshold the cockpit
# adds a **forecast-driven attention item** (tagged `forecast`: "do nothing and it gets worse" is
# itself attention, §7J.5), and ".q8"/the trade-off carry the projected cost of doing nothing from
# that same deterministic projection. No-data orgs keep today's Q3/Q8/trade-off exactly. ADDITIVE:
# the frozen `cockpit_q7q8`/`render_tradeoff`/`rank`/`machine_eligible_best` are untouched; the
# closure enriches the `base`-returned q7/q8 dicts in place (additive fields) and extends `cockpit_
# s7l`'s `.q3` + `render_cockpit_s7l`. The Q8 recommendation stays the §6-floor-gated machine-
# eligible best — the forecast never overrules the §6 pick, it only prices attention + do-nothing.
# 49 `$defs`/URI cap/SPEC v0.22; never the wall-clock, never an invented number.
# ----------------------------------------------------------------------------------------------
def _num(x):
    """Numeric coercion helper (float/None). Used for the recorded forecast threshold."""
    try:
        if x is None:
            return None
        return round(float(x), 4)
    except (TypeError, ValueError):
        return None


# Sprint 26 (additive): the horizon-wide recorded-band phrase, SHARED so the Q3 forecast-driven
# attention `why` and the Q8/do-nothing summary name the SAME record-wide worst case VERBATIM by
# construction. `{lo}`/`{hi}`/`{n}` are the band_horizon min-low/max-high and the count of
# projection periods (pure recorded data). Appended AFTER the Sprint-23/24 single-worst band phrase
# (+ any Sprint-24 band_source phrase) so the old string stays a strict prefix. C2-safe (no
# `at|time|deadline|expires|expiry|effective|due|since` suffix on any generated key).
_HORIZON_BAND_PHRASE = (" — horizon-wide recorded band {lo}…{hi} across {n} projection periods "
                        "(band_periods/band_horizon, same recorded σ)")


# Sprint 27 (additive): the shared deterministic CAPACITY-REASON rule. Extracted from the Sprint-26
# Q9 `capacity_planning_attention` rule so the Q9 capacity reason and the new Q7/Q8
# `capacity_constraint` reason AGREE BY CONSTRUCTION (one helper, one rule). Inputs are recorded
# numbers only: the recorded authority `capacity` {value, unit, load}, the closure's record-wide
# horizon band (`band_horizon` {low, high}), and the recorded metric `direction`. Returns
# (label, flag):
#   headroom      default — recorded load < 1.0 AND the horizon band's worst-side magnitude is
#                 below/at the recorded capacity value, OR the comparison is not derivable (no
#                 numeric load / capacity / worst-side).
#   at-capacity   recorded load >= 1.0.
#   deficit       the horizon band's worst-side magnitude (band_horizon low for higher-is-better,
#                 high for lower-is-better) reaches/exceeds the recorded capacity VALUE.
# The worst-side magnitude and the capacity VALUE may be in different units; the rule STATES the
# recorded numbers and LABELS the effect as a derived reason — never an invented figure, never a
# directive. C2-safe (returned keys carry no temporal suffix; the helper itself returns labels).
def _capacity_reason(capacity_obj: dict, band_horizon: dict,
                     direction: str = "higher-is-better"):
    cap_n = _num(capacity_obj.get("value")) if isinstance(capacity_obj, dict) else None
    load_n = _num(capacity_obj.get("load")) if isinstance(capacity_obj, dict) else None
    wsm = (band_horizon.get("high") if direction == "lower-is-better"
           else band_horizon.get("low"))
    at_cap = load_n is not None and load_n >= 1.0
    deficit = cap_n is not None and wsm is not None and wsm >= cap_n
    if deficit:
        return "deficit", True
    if at_cap:
        return "at-capacity", True
    return "headroom", False


def _per_option_capacity_flags(capacity_obj: dict, requirements: dict, options: list,
                               baseline: str, non_headroom: bool) -> dict:
    """Sprint 29 (additive): the per-option capacity LABEL from ONE recorded rule. AVAILABLE
    capacity = recorded authority `capacity.value` − recorded `capacity.load` (both recorded, the
    SAME unit by construction — the authority holds the capacity AND the per-option requirements).
    An option whose RECORDED requirement > available is `capacity_infeasible`; otherwise it is
    `capacity_risk` only when `non_headroom` (a consumer/at-or-under-available option at/over
    capacity is risky). The baseline (do-nothing/UNRESOLVED) is NEVER flagged (consumes none). The
    engine never invents a requirement — an option not present in the recorded `requirements` dict is
    simply not flagged for infeasibility (it stays `capacity_risk` when non_headroom, byte-compatible
    with Sprint 28). Pure + deterministic; never the wall-clock. C2-safe (returned keys are option
    names; `available_capacity` has no temporal suffix)."""
    value_n = _num(capacity_obj.get("value")) if isinstance(capacity_obj, dict) else None
    load_n = _num(capacity_obj.get("load")) if isinstance(capacity_obj, dict) else None
    available = None
    if value_n is not None and load_n is not None:
        available = round(value_n - load_n, 4)
    flags: dict[str, str] = {}
    for opt in options:
        if opt == baseline:
            continue                       # do-nothing/UNRESOLVED consumes no capacity (never flagged)
        req = _num(requirements.get(opt)) if isinstance(requirements, dict) else None
        if req is not None and available is not None and req > available:
            flags[opt] = "capacity_infeasible"
        elif non_headroom:
            flags[opt] = "capacity_risk"
    return flags


def _forecast_closure(cfg: dict, sub) -> dict:
    """Deterministic forecast→attention→expected-impact data for `cockpit_s7l`, derived ONLY from
    the recorded `metric://` realized-vs-expected series (Sprint 20 `forecast_metric`).

    Returns (never the wall-clock, never an invented number):
      available        bool  — a recorded series exists
      series_uri       str|None, threshold, threshold_source ('forecast_threshold'/'target'/...
                           'last-actual'), projections, worst, worst_period, crossing
      attention_item   the Q3 forecast-tagged item to append (or None)
      q6               the exact Q6 cockpit dict (so Q3/Q6/Q8 agree by construction)
      do_nothing       the Q8/trade-off do-nothing expected-impact block (or None)
    Sprint 23 (additive): when the last recorded point carries a numeric `variance`, the closure also
    carries `recorded_variance` + `band` (worst ± sigma -> low/high, `crosses` = worst side crosses
    the threshold) + the recorded `expected_last` anchor, on the closure, `q8["forecast"]`, and the
    do-nothing block, and the summary/attention-why name the band. A recorded-data spread, NOT a
    confidence interval. No variance -> band absent -> output byte-identical to Sprint 22.
    Sprint 24 (additive): the band's VARIANCE SOURCE is a RECORDED, additive `band_variance` field on
    the metric:// object. Absent / "last" / unknown -> the last recorded point's variance (EXACTLY
    Sprint 23). "all" / "minmax" -> the recorded WHOLE-SERIES choice: the largest recorded |variance|
    across the recorded points -> sigma may WIDEN (or narrow) vs the last point, still ONLY recorded
    point values. When a whole-series choice is active the band carries `source`, the closure /
    q8["forecast"] / do-nothing carry `band_variance`, and the summary/why name the source. Default
    orgs keep the Sprint-23 band (no source key) byte-identical.
    Sprint 25 (additive): the SAME recorded sigma is applied to EVERY projection period -> the closure,
    q8["forecast"], and do-nothing also carry `band_periods` ({period, low, high} per projected value)
    + `band_horizon` ({low: min period low, high: max period high} — the record-wide horizon-wide
    worst-case), and the do-nothing summary appends an additive phrase naming that range (appended
    AFTER the Sprint-23/24 single-worst band phrase, keeping it a strict prefix). This makes the
    horizon-wide worst case explicit AS DATA; it still never invents a sigma (every bound is projected
    value ± the recorded sigma). No-band orgs carry none of these keys (byte-identical).
    Crossing rule: the direction is a RECORDED, additive `direction` field on the `metric://` object
    (`"higher-is-better"` is the default, keeping the Sprint-21 rate/quality case byte-identical;
    an org may record `"lower-is-better"` for a cost/latency/defect/risk case). higher-is-better:
    `min(projection) < threshold`; lower-is-better: `max(projection) > threshold`. Threshold in
    recorded order: explicit `forecast_threshold` additive field -> the metric's own `target` ->
    the last recorded `actual` (so a targetless declining series still flags)."""
    fap_uri, fap_metric = _recorded_metric_with_series(sub)
    if not fap_uri:
        q6 = {"forecast_available": False,
              "forecast": "cannot forecast from recorded data (no recorded realized-vs-expected series)",
              "evidence": "no realized-vs-expected series on the org's graph; a single realized value "
                          "is not a forecast series"}
        return {"available": False, "series_uri": None, "q6": q6,
                "attention_item": None, "do_nothing": None}
    fc = forecast_metric(cfg, sub, fap_uri, horizon=3)
    # ---- recorded threshold, in order: forecast_threshold -> target -> last actual --------------
    thr = _num(fap_metric.get("forecast_threshold"))
    thr_src = "forecast_threshold"
    if thr is None:
        thr = _num(fap_metric.get("target"))
        thr_src = "target"
    if thr is None:
        thr = fc["last_actual"]
        thr_src = "last-actual"
    projs = [p["projected"] for p in fc["projections"]]
    # ---- recorded direction (Sprint 22): additive `direction` on the metric object --------------
    # higher-is-better (default) = rate/quality: lower is worse; lower-is-better = cost/latency/
    # defect/risk: higher is worse. Normalized defensively; an unrecorded/unknown value defaults to
    # higher-is-better so the Sprint-21 behavior is byte-identical.
    direction = str(fap_metric.get("direction") or "higher-is-better").strip().lower()
    if direction != "lower-is-better":
        direction = "higher-is-better"
    if direction == "lower-is-better":
        worst = max(projs) if projs else None
    else:
        worst = min(projs) if projs else None
    worst_period = (next(p["period"] for p in fc["projections"] if p["projected"] == worst)
                    if worst is not None else None)
    if direction == "lower-is-better":
        crossing = worst is not None and thr is not None and worst > thr
    else:
        crossing = worst is not None and thr is not None and worst < thr
    # ---- Sprint 23 (additive): the recorded-variance projected band ------------------------------
    # The do-nothing expected-impact is priced as a BAND (worst ± the RECORDED variance) instead of a
    # single point, derived ONLY from recorded data. The recorded variance used is the last recorded
    # point's `variance` (`forecast_metric.recorded_variance`), taken as a MAGNITUDE (sigma). When the
    # last point carries NO variance (or no recordable numeric variance) the band is ABSENT and the
    # output keeps the Sprint-22 single-point behavior BYTE-IDENTICAL. `crosses` is whether the WORST
    # side of the band crosses the threshold in the metric's direction (higher-is-better: low <
    # threshold; lower-is-better: high > threshold). This is a recorded-data spread, NOT a confidence
    # interval and never a wall-clock/probabilistic claim.
    rv = _num(fc.get("recorded_variance"))
    band = None
    # Sprint 24 (additive): the band's VARIANCE SOURCE is a RECORDED, additive `band_variance`
    # parameter on the metric:// object. Absent / "last"/unknown -> the LAST recorded point's
    # variance (EXACTLY Sprint 23, byte-identical). "all"/"minmax" -> the recorded WHOLE-SERIES
    # choice: the largest recorded |variance| across the recorded points (the recorded worst-case
    # spread), still only recorded point values — never invented. Every possible sigma is a
    # recorded point variance magnitude.
    bv = str(fap_metric.get("band_variance") or "").strip().lower()
    if bv in ("all", "minmax"):
        band_source = bv
        _bv_pts = next((fap_metric[k] for k in ("points", "series", "realized_series")
                        if isinstance(fap_metric.get(k), list) and fap_metric[k]), [])
        _mags = [abs(v) for _p in _bv_pts if isinstance(_p, dict)
                 for v in [_num(_p.get("variance"))] if v is not None]
        src_variance = _num(max(_mags)) if _mags else rv   # recorded max |variance| (fallback: last)
    else:
        band_source = None                                 # no `source` key (Sprint-23 byte-identical)
        src_variance = rv
    if src_variance is not None:
        sigma = round(abs(src_variance), 4)
        low = round((worst - sigma), 4) if worst is not None else None
        high = round((worst + sigma), 4) if worst is not None else None
        if direction == "lower-is-better":
            band_crosses = (low is not None and high is not None and thr is not None
                            and high > thr)
        else:
            band_crosses = (low is not None and high is not None and thr is not None
                            and low < thr)
        band = {"worst": worst, "sigma": sigma, "low": low, "high": high,
                "crosses": bool(band_crosses)}
        if band_source is not None:
            band["source"] = band_source    # additive: name the recorded whole-series source when used
        # Sprint 25 (additive): the SAME recorded sigma applied to EVERY projection period -> a
        # per-period band + the record-wide (horizon-wide) worst-case range. Still derived ONLY from
        # recorded series/projection values + the recorded sigma (one recorded point |variance|
        # magnitude, never invented). `band_horizon` is the whole-horizon worst case: min of the
        # period lows and max of the period highs — it can WIDEN beyond the single-worst point's band
        # when an EARLIER projection period's value at its own ± sigma exceeds the worst point's band
        # (e.g. a declining rate's earlier periods sit higher), yet every bound is a pure function of
        # the recorded points + the recorded threshold + the recorded sigma.
        band_periods = [
            {"period": p["period"],
             "low": round(float(p["projected"]) - sigma, 4),
             "high": round(float(p["projected"]) + sigma, 4)}
            for p in fc["projections"]]
        band_horizon = {"low": min(bp["low"] for bp in band_periods),
                        "high": max(bp["high"] for bp in band_periods)}
    else:
        band_periods = None
        band_horizon = None
    q6 = {"forecast_available": True,
          "forecast": "deterministic projection from the recorded realized-vs-expected series",
          "metric": fap_uri,
          "direction": direction,
          "last_actual": fc["last_actual"], "mean_delta": fc["mean_delta"],
          "horizon": fc["horizon"], "projections": fc["projections"],
          "recorded_variance": fc["recorded_variance"],
          "evidence": "recorded realized-vs-expected series on the org's graph (metric://); "
                      "projection = last recorded actual + mean of recorded deltas, forward "
                      "periods, labelled a projection; never the wall-clock"}
    attention_item = None
    if crossing and direction == "lower-is-better":
        attention_item = {"item": fap_uri,
                          "why": ("forecast: projected to rise above {} ({}) — worst {} at period {}"
                                  .format(thr if thr is not None else "?", thr_src,
                                          worst, worst_period)),
                          "tag": "forecast"}
    elif crossing:
        attention_item = {"item": fap_uri,
                          "why": ("forecast: projected to fall below {} ({}) — worst {} at period {}"
                                  .format(thr if thr is not None else "?", thr_src,
                                          worst, worst_period)),
                          "tag": "forecast"}
    # Sprint 23 (additive): when a recorded-variance band exists, the attention `why` names the band
    # so "the projected spread itself crosses" is surfaced, not just the single worst point.
    if band is not None and attention_item is not None:
        _side = ("{} above {} {}"
                 .format(band["high"], thr_src, thr) if direction == "lower-is-better"
                 else "{} below {} {}".format(band["low"], thr_src, thr))
        attention_item["why"] += (" — recorded band {low}…{high} (± σ {sigma}); worst side {side}"
                                  .format(low=band["low"], high=band["high"],
                                          sigma=band["sigma"], side=_side))
        if band_source is not None:
            attention_item["why"] += (" — band σ from the recorded whole-series max |variance| "
                                      "(band_variance {})".format(band_source))
        # Sprint 26 (additive): name the horizon-wide range on the Q3 attention `why` too — the SAME
        # recorded σ applied to EVERY projection period, so the record-wide worst case (band_horizon
        # min-low/max-high) is visible at the FIRST attention line, exactly as Q6/Q8/do-nothing carry
        # it. Appended AFTER the Sprint-23/24 single-worst band phrase (+ the Sprint-24 source phrase)
        # so the old string stays a strict prefix; shares the do-nothing summary's constant so
        # Q3/Q8/do-nothing agree verbatim by construction. band_horizon is set whenever `band` is, but
        # guard anyway. No-band / no-data orgs never reach here (no suffix, unchanged).
        if band_horizon is not None:
            attention_item["why"] += _HORIZON_BAND_PHRASE.format(
                lo=band_horizon["low"], hi=band_horizon["high"], n=len(band_periods))
    baseline = next((o for o in cfg.get("options", [])
                     if "unres" in o.lower() or o == "do-nothing"), None)
    if crossing and direction == "lower-is-better":
        gap = round(float(worst) - float(thr), 4)
        summary = ("forecast-driven do-nothing cost: {} projects to worst {} (period {}) above "
                   "recorded {} {} by {} — doing nothing lets the recorded trend deteriorate"
                   .format(fap_uri, worst, worst_period, thr_src, thr, gap))
        on_target = False
    elif crossing:
        gap = round(float(thr) - float(worst), 4)
        summary = ("forecast-driven do-nothing cost: {} projects to worst {} (period {}) below "
                   "recorded {} {} by {} — doing nothing lets the recorded trend deteriorate"
                   .format(fap_uri, worst, worst_period, thr_src, thr, gap))
        on_target = False
    elif direction == "lower-is-better":
        summary = ("on-target: {} projection stays at/below recorded {} {} (worst {}) — "
                   "no forecast-driven cost to doing nothing"
                   .format(fap_uri, thr_src, thr, worst))
        on_target = True
    else:
        summary = ("on-target: {} projection stays at/above recorded {} {} (worst {}) — "
                   "no forecast-driven cost to doing nothing"
                   .format(fap_uri, thr_src, thr, worst))
        on_target = True
    # Sprint 23 (additive): append the recorded band to the do-nothing summary when present, so the
    # expected-impact is priced as the recorded spread (not a single point), still from recorded data.
    if band is not None:
        if band["crosses"]:
            _side = ("{} above {} {}"
                     .format(band["high"], thr_src, thr) if direction == "lower-is-better"
                     else "{} below {} {}".format(band["low"], thr_src, thr))
            summary += (" — recorded band {low}…{high} (± σ {sigma}); worst side {side} — the whole "
                        "recorded spread is priced as bad"
                        .format(low=band["low"], high=band["high"],
                                sigma=band["sigma"], side=_side))
        else:
            summary += (" — recorded band {low}…{high} (± σ {sigma}); worst side stays safe of the "
                        "threshold — the spread confirms on-target"
                        .format(low=band["low"], high=band["high"], sigma=band["sigma"]))
        if band_source is not None:
            summary += (" — band σ from the recorded whole-series max |variance| (band_variance {})"
                        .format(band_source))
        # Sprint 25 (additive): name the horizon-wide range too — the SAME sigma applied to EVERY
        # projection period, so the whole-horizon worst case (record-wide low..high) is explicit,
        # still only from recorded values + the recorded sigma. Appended AFTER the Sprint-23/24
        # single-worst band phrase -> the old string stays a strict prefix. Sprint 26: the phrase is
        # the SHARED `_HORIZON_BAND_PHRASE` constant so the Q3 attention `why` and this summary name
        # the SAME horizon-wide recorded band verbatim (output byte-identical to Sprint 25).
        summary += _HORIZON_BAND_PHRASE.format(
            lo=band_horizon["low"], hi=band_horizon["high"], n=len(band_periods))
    do_nothing = {"baseline": baseline, "priced": True, "on_target": on_target,
                  "summary": summary, "metric": fap_uri, "direction": direction}
    res = {"available": True, "series_uri": fap_uri, "threshold": thr,
           "threshold_source": thr_src, "projections": fc["projections"], "worst": worst,
           "worst_period": worst_period, "crossing": crossing, "direction": direction,
           "attention_item": attention_item, "q6": q6, "do_nothing": do_nothing,
           "forecast": {"projections": fc["projections"], "threshold": thr,
                        "source": thr_src, "worst": worst, "crossing": crossing,
                        "direction": direction}}
    # Sprint 23 (additive): ride the recorded variance / band / expected anchor on the closure, the
    # q8 `forecast` block, and the do-nothing expected-impact — ONLY when a band exists, so the
    # no-variance single-point output stays byte-identical.
    if band is not None:
        res["recorded_variance"] = rv
        res["expected_last"] = fc.get("expected_last")
        res["band"] = band
        res["band_periods"] = band_periods
        res["band_horizon"] = band_horizon
        res["forecast"]["recorded_variance"] = rv
        res["forecast"]["expected_last"] = fc.get("expected_last")
        res["forecast"]["band"] = band
        res["forecast"]["band_periods"] = band_periods
        res["forecast"]["band_horizon"] = band_horizon
        do_nothing["variance"] = rv
        do_nothing["expected_last"] = fc.get("expected_last")
        do_nothing["band"] = band
        do_nothing["band_periods"] = band_periods
        do_nothing["band_horizon"] = band_horizon
    # Sprint 24 (additive): ride the recorded whole-series band_variance SOURCE on the closure, the
    # q8 `forecast` block, and the do-nothing expected-impact too — ONLY when a whole-series choice
    # is active (default orgs carry no such key -> byte-identical to Sprint 23). The band dict's own
    # `source` (when set) already names the recorded source; this rides the same fact one level up.
    if band_source is not None:
        res["band_variance"] = band_source
        res["forecast"]["band_variance"] = band_source
        do_nothing["band_variance"] = band_source
    return res


def _forecast_closure_marker(cfg: dict, sub) -> dict:
    """Alias for parity/legibility; keeps the closure call site readable and identical-inputs-
    identical-outputs deterministic. Simply delegates to `_forecast_closure`."""
    return _forecast_closure(cfg, sub)


# ----------------------------------------------------------------------------------------------
# SPRINT 20 — recorded-data Q6 forecast + Q9 capacity for the §7L morning cockpit (additive).
# Sprint 19's honest limit (see its findings "Residual seams"): Q6 cannot forecast on the
# adjudication orgs because none records a realized-vs-expected series, and Q9 "capability" was
# the holder-of-authority assignment, not a capacity number. Sprint 20 closes a bounded slice of
# both by making the org RECORD the missing data additively on its own graph/ledger — a `metric://`
# realized-vs-expected series and an additive `capacity` field on the authority:// object the Q9
# question reads — so `cockpit_s7l`'s q6 can PROJECT deterministically from the recorded series and
# its q9 can report the recorded capacity number, WHERE the data exists, with the honest no-data
# fallback unchanged. Generic + data-only: one identical engine path for any configured org.
# Additive only; the frozen `reconcile`/`run_scenario`/`_derive`/`SPEC_VOCAB`/`_aggregate`/
# `rank`/`machine_eligible_best`/`render_tradeoff`/`cockpit_q7q8`/`cockpit_s7l`/`render_cockpit_s7l`
# are untouched; 49 `$defs`/URI cap/SPEC v0.22. Never the wall-clock, never an invented number.
# ----------------------------------------------------------------------------------------------
def _recorded_metric_with_series(sub) -> tuple:
    """(metric_uri, metric_obj) for the first `metric://` object on the org's graph carrying a
    non-empty realized-vs-expected `points`/`series`/`realized_series` list of dicts; else (None, {}).
    Deterministic (first in graph order). Never the wall-clock."""
    for o in _graph_objects(sub):
        uri = o.get("uri", "")
        if not isinstance(uri, str) or not uri.startswith("metric://"):
            continue
        for key in ("points", "series", "realized_series"):
            pts = o.get(key)
            if isinstance(pts, list) and pts and all(isinstance(p, dict) for p in pts):
                return uri, o
    return None, {}


def forecast_metric(cfg: dict, sub, metric_uri: str, *, horizon: int = 3) -> dict:
    """Deterministic projection for Q6 from a RECORDED realized-vs-expected series only.

    Reads the `metric://` object's `points` list (per-period dicts each carrying `actual`, and
    optionally `target`/`expected`/`variance`), and projects forward purely from the recorded
    values: projected(f) = last recorded actual + mean(recorded consecutive deltas) * f, for
    f in 1..horizon. The projected value is LABELLED a projection (never expanded to an outcome),
    and the last RECORDED variance is shown alongside. DETERMINISTIC: a pure function of the
    recorded points + the explicit `horizon` — never the wall-clock, never an invented number.
    When no such series exists the return says so plainly (`available: False`)."""

    def _num(x):
        try:
            return round(float(x), 4)
        except (TypeError, ValueError):
            return None

    if not isinstance(horizon, int) or horizon < 1:
        raise ValueError("forecast_metric requires an integer horizon >= 1")
    m = sub.graph.get(metric_uri) or {}
    pts = next((m[k] for k in ("points", "series", "realized_series")
                if isinstance(m.get(k), list) and m[k] and all(isinstance(p, dict) for p in m[k])), None)
    if not pts:
        return {"available": False, "metric": metric_uri,
                "forecast": "cannot project — no recorded realized-vs-expected series on %s" % metric_uri}
    actuals = []
    for p in pts:
        a = _num(p.get("actual"))
        if a is None:
            return {"available": False, "metric": metric_uri,
                    "forecast": ("cannot project — recorded series on %s has a non-numeric actual"
                                 % metric_uri)}
        actuals.append(a)
    last_actual = actuals[-1]
    # mean of consecutive recorded deltas (direction of travel); 0 when the series has one point
    deltas = [actuals[i] - actuals[i - 1] for i in range(1, len(actuals))]
    mean_delta = round(sum(deltas) / len(deltas), 4) if deltas else 0.0
    projections = [{"period": f, "projected": round(last_actual + mean_delta * f, 4)}
                   for f in range(1, horizon + 1)]
    last_pt = pts[-1]
    return {
        "available": True,
        "metric": metric_uri,
        "unit": m.get("unit"),
        "target": _num(m.get("target")),
        "last_actual": last_actual,
        "mean_delta": mean_delta,
        "horizon": horizon,
        "projections": projections,
        "recorded_variance": _num(last_pt.get("variance")),
        "expected_last": _num(last_pt.get("expected")),
        "note": "deterministic projection from the recorded series only (holds the recorded trend); "
                "a projection, not an outcome; never the wall-clock",
    }


def record_metric_series(sub, label: str, metric_uri: str, *, points: list, fields: dict,
                         signer: str) -> str:
    """REPLAYABLE recorder: append the org's own realized-vs-expected `metric://` series to its
    immutable ledger, additively (no new noun, no schema edit). `points` is the ordered per-period
    list ({period,target,expected,actual,variance,...}); `fields` carries the Metric-required
    `name`/`formula` + unit/target/period/source/owner/etc. The metric object's `actual`/`variance`
    are set to the LAST recorded point so the §7L Q9/BI read sees a single current value too.
    C2-safe keys only (no temporal suffix). Returns the signed event uri."""
    assert metric_uri.startswith("metric://"), "metric_uri must be a metric:// URI"
    assert isinstance(points, list) and points, "points must be a non-empty list"
    for p in points:
        assert isinstance(p, dict) and "actual" in p, "each point needs an `actual`"
    assert "name" in fields and "formula" in fields, "fields needs the Metric-required name + formula"
    last = points[-1]
    metric_obj = {"uri": metric_uri, "actual": round(float(last["actual"]), 4),
                  "variance": last.get("variance"), "points": list(points),
                  **{k: fields[k] for k in fields if k not in ("actual", "variance", "points")}}
    ev_uri = f"event://{label}/record-metric-series"
    sub.record({
        "uri": ev_uri, "type": "STATE_CHANGE",
        "event_id": f"ev-adj-{label}-record-metric-series",
        "correlation_id": f"corr-adj-{label}-record-metric-series",
        "causation_id": f"ev-adj-{label}-record-metric-series-prev",
        "idempotency_key": f"idem-adj-{label}-record-metric-series",
        "signature": f"signed-by-{signer}", "occurred_at": now_iso(), "actor": signer,
        "detail": "record a realized-vs-expected metric series additively on the org's ledger so the "
                  "§7L Q6 can project from recorded data",
        "state_update": [metric_obj]}, signer)
    return ev_uri


def record_capacity(sub, authority_uri: str, *, value, unit: str, signer: str,
                    load=None) -> str:
    """REPLAYABLE recorder: append an additive `capacity` field ({value,unit,load,status}) on the
    `authority://` object the §7L Q9 reads, MERGE-not-replace (the authority's required fields ride
    along via `{**graph.get(uri), ...}` → preserve-unknown). Returns the signed event uri."""
    assert authority_uri.startswith("authority://"), "capacity is recorded on an authority:// object"
    obj = {**sub.graph.get(authority_uri),
           "capacity": {"value": value, "unit": unit, "load": load, "status": "recorded"}}
    label = authority_uri.split("/")[-2]
    ev_uri = f"event://{label}/record-capacity"
    sub.record({
        "uri": ev_uri, "type": "STATE_CHANGE",
        "event_id": f"ev-adj-{label}-record-capacity",
        "correlation_id": f"corr-adj-{label}-record-capacity",
        "causation_id": f"ev-adj-{label}-record-capacity-prev",
        "idempotency_key": f"idem-adj-{label}-record-capacity",
        "signature": f"signed-by-{signer}", "occurred_at": now_iso(), "actor": signer,
        "detail": "record the authority's additive capacity field so the §7L Q9 can report it as data",
        "state_update": [obj]}, signer)
    return ev_uri


def record_capacity_requirements(sub, authority_uri: str, *, requirements: dict, signer: str) -> str:
    """REPLAYABLE recorder (Sprint 29): append an additive `capacity_requirements` map on the
    SAME `authority://` object that already carries the additive `capacity` field. `requirements`
    is {option_name: recorded_nonneg_amount} in the SAME recorded unit as the authority `capacity`
    (unit-coupled BY CONSTRUCTION: the authority holds both the {value, unit, load} capacity and the
    per-option requirements, so `available = capacity.value - capacity.load` and every per-option
    label derive from the same recorded unit). MERGE-not-replace (preserve-unknown rides the existing
    fields along). C2-safe: key `capacity_requirements` carries no temporal suffix. Returns the
    signed event uri."""
    assert authority_uri.startswith("authority://"), "per-option capacity is recorded on an authority:// object"
    assert isinstance(requirements, dict) and requirements, "capacity_requirements must be a non-empty dict"
    for _k, _v in requirements.items():
        assert isinstance(_v, (int, float)) and _v >= 0.0, \
            f"capacity requirement for {_k!r} must be a non-negative number (got {_v!r})"
    obj = {**sub.graph.get(authority_uri),
           "capacity_requirements": dict(requirements)}
    label = authority_uri.split("/")[-2]
    ev_uri = f"event://{label}/record-capacity-requirements"
    sub.record({
        "uri": ev_uri, "type": "STATE_CHANGE",
        "event_id": f"ev-adj-{label}-record-capacity-requirements",
        "correlation_id": f"corr-adj-{label}-record-capacity-requirements",
        "causation_id": f"ev-adj-{label}-record-capacity-requirements-prev",
        "idempotency_key": f"idem-adj-{label}-record-capacity-requirements",
        "signature": f"signed-by-{signer}", "occurred_at": now_iso(), "actor": signer,
        "detail": "record the authority's additive per-option capacity requirements so the Q7/Q8 "
                  "capacity_constraint can label a specific option capacity_infeasible vs capacity_risk "
                  "from recorded numbers only",
        "state_update": [obj]}, signer)
    return ev_uri
