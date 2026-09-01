"""reconcile_learning.py — SPRINT 17: decision learning at the RECONCILE layer, honest + additive.

Sprint 13 shipped an OPTIONAL `decision_learning.py` (realized-cost weight learning) that was never
wired into the reconcile RULE choice. This module makes the reconcile layer itself learnable: a
deterministic, clamp-bounded, evidence-gated update of the reconcile `threshold` from a RECORDED,
realized outcome, feeding a NEW named RULE_LIBRARY entry that any org can reuse on a SECOND, distinct
dispute. It implements the §7K.1 loop `Decision -> Expected -> Actual -> Variance -> WHY ->
change-future-policy` at the reconciliation boundary.

The trust-sensitive question this sprint answers is whether "learning" degrades into the machine
moving its own goalposts. It must not, and it does not:
  - it never touches Trust (only the deterministic S5 formula does);
  - it never edits any `determination_policy` (the §6 human's authoritative call stays intact);
  - it never rewrites the ledger (append-only: a NEW rule:// + decision:// + one signed event);
  - it is rebound from an EXPLICIT [lo, hi] and an explicit prior threshold — never the wall-clock,
    never unbounded.

Honest label, applied to every function: this recalibrates the RULE's parameter from a realized
outcome (a bounded, evidence-gated re-authoring), it does NOT learn the answer to any case.

Everything is additive on the frozen 49 $defs / URI cap (SPEC v0.22). `rule://` maps to the frozen
`Rule` $def (kind=PROCEDURE), `decision://` to `Decision`. ~$0 deterministic local Python.

Usage: driven by run_reconcile_learning_demo.py (from instances/contested_reality).
"""
from __future__ import annotations

from ros.substrate import now_iso  # noqa: E402


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def learn_threshold(*, prior_threshold: float, realized_value: float,
                    learning_rate: float, lo: float, hi: float, eps: float = 1e-6) -> dict:
    """Deterministic, clamp-bounded recalibration of the reconcile `threshold` from ONE recorded,
    realized outcome.

    signal = realized_value - prior_threshold   (the §7K.1 variance, at the sufficiency bar)
    If the realized value is BELOW the prior threshold — a determination actually held at support the
    bar demanded MORE of — the threshold was too strong (it risks UNRESOLVED on valid-but-moderately-
    evidenced disputes); LOWER it toward the realized value (relax). If the realized value EXCEEDS
    the bar, the bar was below what outcomes provided; RAISE it (stiffen). Clamp-bounded to [lo, hi].

    Pure: it depends only on the explicit inputs, never the wall-clock, so the same call returns the
    same result on re-run (asserted by the runner). `changed` is evidence-gated: only when the move
    clears `eps`.
    """
    hi = max(lo, hi)
    delta = learning_rate * (realized_value - prior_threshold)
    new = round(_clamp(prior_threshold + delta, lo, hi), 4)
    changed = abs(delta) >= eps and abs(new - prior_threshold) >= eps
    if new > prior_threshold:
        dirn = "raised (stiffer: outcomes exceeded the bar)"
    elif new < prior_threshold:
        dirn = "lowered (relaxed: the bar demanded more than realized determinations held)"
    else:
        dirn = "unchanged (realized value ~= prior threshold)"
    why = (f"reconcile threshold recalibrated {dirn}: prior {prior_threshold:.3f} -> {new:.3f} "
           f"from a realized outcome value {realized_value:.3f} (variance signal "
           f"{delta:+.3f}, learning_rate {learning_rate:g}), clamp-bounded to [{lo:g}, {hi:g}]")
    return {"threshold": new, "prior_threshold": round(prior_threshold, 4),
            "realized_value": round(realized_value, 4), "delta": round(delta, 4),
            "learning_rate": learning_rate, "bound": [round(lo, 4), round(hi, 4)],
            "changed": bool(changed), "eps": eps, "why": why}


def build_learned_library_spec(name: str, *, learned: dict) -> dict:
    """Turn a `learn_threshold` result into a NEW named RULE_LIBRARY rule_spec (aggregate `max`,
    value_field `reliability`) with additive learned-param fields. This is "learning feeds the
    library": the learned artifact IS a reusable named rule spec, not a one-case patch. The extra
    fields ride additively on the spec (the engine's compile_rule_spec preserves unknown fields)."""
    return {"name": name, "aggregate": "max", "value_field": "reliability",
            "admissible_kinds": None,
            "learned_param": "threshold", "learned_threshold": learned["threshold"],
            "prior_threshold": learned["prior_threshold"],
            "calibrated_from": {"realized_value": learned["realized_value"],
                                "delta": learned["delta"],
                                "learning_rate": learned["learning_rate"]},
            "bound": list(learned["bound"]), "why": learned["why"]}


def record_realized_outcome(sub, cfg, dispute_uri: str, outcome_value: float, signer: str) -> None:
    """APPEND a signed event recording the realized outcome value additively ON the dispute
    (merge-not-replace), so an auditor sees the realized outcome the learner derived its signal from.
    Conservative additive keys (no C2 temporal-suffix traps)."""
    L = cfg["label"]
    d = sub.graph.get(dispute_uri) or {}
    sub.record({
        "uri": f"event://{L}/realized-outcome", "type": "STATE_CHANGE",
        "event_id": f"ev-adj-{L}-realized-outcome",
        "correlation_id": f"corr-adj-{L}-realized-outcome",
        "causation_id": f"ev-adj-{L}-realized-outcome-prev",
        "idempotency_key": f"idem-adj-{L}-realized-outcome",
        "signature": f"signed-by-{signer}", "occurred_at": now_iso(), "actor": signer,
        "detail": "realized outcome of the adjudication recorded for reconcile-rule learning",
        "state_update": [
            {**d, "realized_value": round(outcome_value, 3),
             "realized_why": "post-execution verified outcome value (0..1) of the adopted "
                             "determination"},
            {"uri": f"evidence://{L}/realized-outcome-note", "kind": "RECORD",
             "source": "verified-outcome-capture", "captured_at": now_iso(),
             "verity": {"procedure": "outcome-capture", "confidence": 0.7},
             "reliability": 0.7, "about": "realized outcome value as recorded",
             "supports": None, "learning": "realized outcome captured additively for the "
                                            "reconcile-rule learning step"}]},
        signer)


def record_learned_rule(sub, label: str, *, signer: str, authority: str, learned: dict,
                        learned_spec: dict, realized_value: float, learned_decision_uri: str,
                        prior_reconcile: dict) -> str:
    """APPEND-ONLY signed record of the learned reconcile rule: a NEW `rule://{label}/reconcile-rule`
    (frozen Rule $def, kind=PROCEDURE) + the `decision://{label}/reconcile-learning` (Decision $def,
    `[uri,by,authority]` + `rules_applied` -> the rule), all in ONE signed event appended to the
    immutable ledger. History is NOT rewritten (never touches an existing event). Returns the rule_uri.
    """
    rule_uri = f"rule://{label}/reconcile-rule"
    rule_obj = {
        "uri": rule_uri, "kind": "PROCEDURE",
        "text": (f"evidence-reconciliation threshold procedure for org {label}: supported claims "
                 f"reach DETERMINED at support >= threshold `{learned['threshold']:.3f}` "
                 f"(aggregate `{learned_spec['aggregate']}` over `{learned_spec['value_field']}`), "
                 f"support_floor 0.55; recalibrated from a realized outcome."),
        "applies_to": f"obligation://{label}/inspect-due",
        # additive learned rules (carried on the envelope; no new noun, no schema edit)
        "learned_param": "threshold", "learned_threshold": learned["threshold"],
        "prior_threshold": learned["prior_threshold"],
        "learned_from": learned_decision_uri,
        "calibrated_from": {"realized_value": learned["realized_value"],
                            "variance_delta": learned["delta"]},
        "bound": list(learned["bound"]), "why": learned["why"],
        "prior_reconcile": {k: v for k, v in prior_reconcile.items() if k in ("rule", "threshold",
                                                                              "support_floor")},
    }
    dec_obj = {
        "uri": learned_decision_uri, "by": signer, "authority": authority,
        "alternatives": ["adopt-learned-rule", "keep-prior-rule", "reject-learning"],
        "rules_applied": [rule_uri],
        "confidence": 0.8,
        "expected_outcome": "change future reconcile-determination policy",
        "actual_outcome": ("rule recorded for reuse; determination for the current dispute is "
                           "UNCHANGED and remains the §6 human's call"),
        "evidence": [f"evidence://{label}/realized-outcome-note"],
        "detail": {
            "learning": "the reconcile threshold is recalibrated toward the realized outcome",
            "prior_threshold": learned["prior_threshold"], "learned_threshold": learned["threshold"],
            "realized_value": realized_value, "delta": learned["delta"],
            "bound": list(learned["bound"]), "why": learned["why"],
            "contained": "Trust (S5 only) and determination_policy (the §6 human's call) are "
                         "untouched; history is never rewritten (this is an append)."},
        "made_at": now_iso(),
    }
    sub.record({
        "uri": f"event://{label}/reconcile-learning", "type": "DECISION",
        "event_id": f"ev-adj-{label}-reconcile-learning",
        "correlation_id": f"corr-adj-{label}-reconcile-learning",
        "causation_id": f"ev-adj-{label}-reconcile-learning-prev",
        "idempotency_key": f"idem-adj-{label}-reconcile-learning",
        "signature": f"signed-by-{signer}", "occurred_at": now_iso(), "actor": signer,
        "detail": "decision learning at the reconciliation layer: a NEW rule:// + decision:// "
                  "appended to the immutable ledger (history not rewritten)",
        "state_update": [rule_obj, dec_obj]},
        signer)
    return rule_uri


def learned_threshold_of(spec: dict) -> float:
    """Read the additive learned threshold off a learned rule_spec."""
    return float(spec["learned_threshold"])