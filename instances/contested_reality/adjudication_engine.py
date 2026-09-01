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