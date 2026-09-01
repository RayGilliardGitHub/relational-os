"""decision_learning.py — SPRINT 13 (optional, additive): realized-cost / Decision Learning
(§7K.1 Decision→Expected→Actual→Variance→WHY→change-future-decision-policy; §7J.9 Cockpit).

Deterministic, clamp-bounded update of the business-model weights from the variance between the
computed EXPECTED utility of the option the adjudicator chose and a RECORDED realized outcome
value, so the objective itself (the weight vector) is learned over time — not just the ranking.
Additive only: records `realized_cost_usd`, `outcome_value`, `expected_utility/variance`, and the
`learned_weights` on the `decision://` and the dispute; never rewrites history, never touches
Trust, never touches the frozen schema.
"""
from __future__ import annotations

from ros.substrate import now_iso  # noqa: E402


def _mean_factor(cfg: dict, factor: str) -> float:
    """Mean of a factor's score across ALL options (the baseline the chosen option is compared
    against). Deterministic from config data."""
    vals = [s.get(factor, 0.0) for s in cfg["factor_scores"].values()]
    return sum(vals) / len(vals) if vals else 0.0


def _factor(cfg, opt, f) -> float:
    return cfg["factor_scores"].get(opt, {}).get(f, 0.0)


def update_weights(cfg: dict, chosen_utility: float, outcome_value: float) -> tuple[dict, float]:
    """Return (new_weights, variance). new_w[f] = clamp(w[f] + lr·variance·(chosen_score_f −
    mean_f), lo, hi), then renormalised to sum 1.0. Fully deterministic + clamp-bounded."""
    lm = cfg["learning_model"]
    lr, lo, hi = lm["learning_rate"], lm["lo"], lm["hi"]
    variance = chosen_utility - outcome_value
    chosen = None
    # the chosen option = the one whose utility == chosen_utility (deterministic lookup)
    for opt, scores in cfg["factor_scores"].items():
        util = sum(cfg["weights"][f] * scores.get(f, 0.0) for f in cfg["weights"])
        if abs(util - chosen_utility) < 1e-9:
            chosen = opt
            break
    if chosen is None:
        return dict(cfg["weights"]), variance      # no change when the chosen option is unknown
    w = dict(cfg["weights"])
    for f in w:
        delta = lr * variance * (_factor(cfg, chosen, f) - _mean_factor(cfg, f))
        w[f] = max(lo, min(hi, w[f] + delta))
    total = sum(w.values())
    if total > 0:
        w = {k: v / total for k, v in w.items()}
    return w, variance


def record_learning(cfg: dict, chosen_uri: str, chosen_utility: float, sub, dispute_uri: str) -> dict:
    """Append a learning event: realised cost + outcome value + variance + learned weights, carried
    additively on the chosen decision:// and the dispute. Merge-not-replace. Returns a detail dict."""
    L = cfg["label"]; lm = cfg["learning_model"]
    new_w, variance = update_weights(cfg, chosen_utility, lm["outcome_value"])
    d = sub.graph.get(chosen_uri) or {}
    detail = {
        "expected_utility": round(chosen_utility, 4),
        "outcome_value": lm["outcome_value"],
        "variance": round(variance, 4),
        "realized_cost_usd": lm["realized_cost_usd"],
        "learning_rate": lm["learning_rate"],
        "why": (f"chosen option (utility {chosen_utility:.3f}) realised {lm['outcome_value']:.2f} "
                f"-> variance {variance:+.3f}; weights cautiously re-weighted toward factors that "
                "distinguish well-performing options, clamp-bounded + renormalized"),
    }
    sub.record({
        "uri": f"event://{L}/decision-learning", "type": "STATE_CHANGE",
        "event_id": f"ev-adj-{L}-decision-learning",
        "correlation_id": f"corr-adj-{L}-decision-learning",
        "causation_id": f"ev-adj-{L}-decision-learning-prev",
        "idempotency_key": f"idem-adj-{L}-decision-learning",
        "signature": "signed-by-%s" % cfg["registrar"], "occurred_at": now_iso(),
        "actor": cfg["registrar"],
        "detail": "organizational learning: realized-cost / expected-vs-actual weight update",
        "state_update": [
            {**d, "realized_cost_usd": lm["realized_cost_usd"],
             "outcome_value": lm["outcome_value"], "expected_utility": round(chosen_utility, 4),
             "variance": round(variance, 4), "learned_weights": new_w,
             "_learned_from_weight_update": detail["why"]},
            {**sub.graph.get(dispute_uri), "learned_weights": new_w,
             "learning": cfg.get("learning", "")},
        ]},
        cfg["registrar"])
    return detail