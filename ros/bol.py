"""BOL — Business Operating Layer (Sprint 5, the product).

Turns the verified S1->S5 chain into the operating system an owner uses every morning:
Cases (universal unit of unresolved work, §7J.3), Goal/Metric (what we optimize toward,
§7J.1), Task & Work Queue (recommendations become action, §7J.4), Exception heartbeat
(§7J.2), Priority & Attention (§7J.5), Dependency & Impact (§7J.6), and the Cockpit
(§7J.9). It answers the §7L ten morning questions with evidence.

IMPORTANT — URI cap (§7J.11 / §C16) and the frozen ontology are honoured here. The
operating layer uses ONLY the five existing first-class schemes already in the schema
and catalog (`case:// goal:// metric:// task:// dependency://`) plus the existing
assemblies already in the `$defs` (`policy:// process:// process_instance:// risk://
escalation://`). Derived values are carried as **additive envelope fields** on those
schema objects (each `$def` is `additionalProperties: true`):
  - Exception (§7J.2)  -> additive fields on the `case://` (expected/actual/variance/
    significance/exception/root_cause/recommended_action/decision/verified_outcome).
  - Priority (§7J.5)   -> additive `priority` + `priority_factors` on the `task://`/`case://`.
  - Recommendation     -> additive `recommendation` fields on the `case://`.
  - Capacity (Q9)      -> additive `assigned_capacity` / worker capacity (no `capacity://`).
  - Learning (§7K.1)   -> a `decision://` learning entry (envelope: expected/actual/
    variance/why/change_future_policy) + a future-policy change on a `policy://`.
No new URI scheme, no new noun.

Every object this layer creates is carried by a signed Ledger event's `state_update`, so
the Graph round-trip reconstructs it (§3.16, full-coverage rule).
"""
from __future__ import annotations

from typing import Any

from .substrate import Substrate, now_iso


# ---------------------------------------------------------------------------
# Deterministic projections over the Append-Only Ledger (§7G.8 / BI mechanics):
# business health is derived from history, never from a hand-set number.
# ---------------------------------------------------------------------------
def project_on_time(substrate: Substrate) -> tuple[int, int]:
    """(on_time, total) over completion OUTCOME events that carry an `on_time` flag."""
    rows = [e for e in substrate.ledger.entries
            if e.get("type") == "OUTCOME" and "on_time" in e]
    on = sum(1 for e in rows if bool(e.get("on_time")))
    return on, len(rows)


def project_settled_value(substrate: Substrate) -> float:
    """Sum of settled EXCHANGE prices recorded on the ledger (§4b)."""
    return round(sum(float(e.get("price", 0.0))
                     for e in substrate.ledger.entries if e.get("type") == "EXCHANGE"), 2)


def project_trust(substrate: Substrate, target: str, context: str) -> float | None:
    """Best scoped Trust for (target, context) from the graph (§3.14)."""
    best = None
    for o in substrate.graph.objects.values():
        if o.get("uri", "").startswith("trust://") and o.get("target") == target \
                and o.get("context") == context:
            best = float(o.get("score", 0.0)) if best is None else max(best, float(o.get("score", 0.0)))
    return best


class BolService:
    """Business Operating Layer service over the shared Graph + Ledger."""

    def __init__(self, substrate: Substrate, label: str = "qk"):
        self.substrate = substrate
        self.label = label       # org/path segment for URIs this layer builds (§C1)

    # ---------------------------------------------------------------- helpers
    def _ev(self, kind: str, uri: str, actor: str, i: int, detail: str,
            state_update: list[dict] | None = None) -> dict:
        return {
            "uri": uri, "type": kind,
            "event_id": f"ev-s5-{i}", "correlation_id": f"corr-{self.label}-bol-1",
            "causation_id": f"ev-s5-{max(0, i-1)}", "idempotency_key": f"idem-s5-{i}",
            "signature": f"signed-by-{actor}", "occurred_at": now_iso(),
            "actor": actor, "detail": detail, "state_update": state_update or [],
        }

    def prov(self, i: int, actor: str, detail: str, objs: list[dict],
             uri: str | None = None) -> dict:
        """Record a signed STATE_CHANGE event carrying `objs` as its state delta.
        Every object is thereby covered by a signed history entry (full coverage).
        Objects are DEEP-COPIED into the ledger so each event is an immutable
        snapshot — later in-place edits to a live object (e.g. a Case's history)
        must not retroactively change an earlier signed entry and break its hash."""
        import copy
        snapshot = [copy.deepcopy(o) for o in objs]
        e = self._ev("STATE_CHANGE", uri or f"event://{self.label}/s5-state-{i}", actor, i,
                     detail, snapshot)
        self.substrate.record(e, actor)
        return e

    # ------------------------------------------------------- §7J.5 priority
    def priority(self, impact: float, urgency: float, confidence: float,
                 irreversible: bool, relationship_importance: float,
                 cost_of_delay: float,
                 weights: dict[str, float] | None = None) -> dict:
        """Priority = f(impact, urgency, confidence, irreversibility,
        relationship-importance, cost-of-delay). Deterministic local math (§G.11):
        every axis in [0,1] (irreversibility boolean), weighted sum, clamped to [0,1]."""
        w = weights or {
            "impact": 0.25, "urgency": 0.20, "confidence": 0.10,
            "irreversibility": 0.15, "relationship": 0.15, "cost_of_delay": 0.15,
        }
        score = (w["impact"] * impact + w["urgency"] * urgency
                 + w["confidence"] * confidence
                 + w["irreversibility"] * (1.0 if irreversible else 0.0)
                 + w["relationship"] * relationship_importance
                 + w["cost_of_delay"] * cost_of_delay)
        return {
            "score": round(max(0.0, min(1.0, score)), 3),
            "factors": {
                "impact": impact, "urgency": urgency, "confidence": confidence,
                "irreversibility": irreversible,
                "relationship_importance": relationship_importance,
                "cost_of_delay": cost_of_delay,
            },
            "weights": w,
        }

    # ------------------------------------------------------- §7J.3 case lifecycle
    def open_case(self, uri: str, subject: str, owner: str, actors: list[str],
                  relationships: list[str], i: int, signer: str,
                  **extra) -> dict:
        case = {"uri": uri, "subject": subject, "status": "OPEN",
                "owner": owner, "actors": actors, "relationships": relationships,
                "created_at": now_iso(),
                "history": [{"status": "OPEN", "at": now_iso(), "event": None}]}
        case.update(extra)
        self.prov(i, signer, f"open case {uri} ({subject})", [case])
        return case

    def transition_case(self, case: dict, new_status: str, i: int, signer: str,
                        detail: str, event_uri: str, **extra) -> dict:
        """Record a legal lifecycle transition with signed evidence (each
        transition is its own signed STATE_CHANGE event carrying the updated case)."""
        c = dict(case)
        c["status"] = new_status
        c.setdefault("history", []).append(
            {"status": new_status, "at": now_iso(), "event": event_uri})
        c.update(extra)
        self.prov(i, signer, detail, [c], uri=event_uri)
        return c

    # ------------------------------------------------------- §7J.2 exception
    def exception_heartbeat(self, case: dict, expected: float, actual: float,
                            significance: str, exception: str, root_cause: str,
                            root_cause_status: str, recommended_action: str,
                            metric_uri: str) -> dict:
        """Attach the §7J.2 expectations->_verified-outcome chain as additive fields
        on the case. Returns the case with the exception documented (not yet decided)."""
        c = dict(case)
        c["expected"] = expected
        c["actual"] = round(actual, 3)
        c["variance"] = round(actual - expected, 3)
        c["significance"] = significance
        c["exception"] = exception
        c["root_cause"] = root_cause
        c["root_cause_status"] = root_cause_status       # §7K.2 epistemic status
        c["recommended_action"] = recommended_action
        c["metric"] = metric_uri
        return c

    # ------------------------------------------------------- §7K.1 learning
    def learning_entry(self, uri: str, subject: str, by: str, i: int, signer: str,
                       expected: float, actual: float, why: str,
                       change_future_policy: str) -> dict:
        """Organizational Learning as a `decision://` object with the §7K.1
        Decision->Expected->Actual->Variance->WHY->change-future-policy shape."""
        learning = {
            "uri": uri, "by": by, "authority": f"authority://{self.label}/for-operations",
            "subject": subject,
            "expected": expected, "actual": actual,
            "variance": round(actual - expected, 3),
            "why": why, "change_future_policy": change_future_policy,
            "made_at": now_iso(),
        }
        self.prov(i, signer, f"learning entry {uri}: {why}", [learning])
        return learning

    # ------------------------------------------------------- §7J.6 dependency
    def make_dependency(self, uri: str, fr: str, to: str, kind: str,
                        i: int, signer: str) -> dict:
        d = {"uri": uri, "from": fr, "to": to, "kind": kind}
        self.prov(i, signer, f"dependency {uri}: {fr} {kind} {to}", [d])
        return d

    def impact_analysis(self, uri: str) -> dict:
        """Transitive forward impact (§7J.6): every node that breaks, is blocked,
        or is affected downstream if `uri` fails. Directional on workflow."""
        deps = [d for d in self.substrate.graph.objects.values()
                if d.get("uri", "").startswith("dependency://")]
        for d in deps:
            kind = d.get("kind")
            if kind not in ("REQUIRES", "BLOCKS", "IMPACTS", "ENABLES", "DERIVED_FROM"):
                pass
        impacted: set[str] = set()
        edges: list[tuple[str, str, str]] = []
        stack = [uri]
        while stack:
            n = stack.pop()
            for d in deps:
                if d.get("from") == n:
                    t = d.get("to")
                    edges.append((n, t, d.get("kind", "")))
                    if t not in impacted:
                        impacted.add(t)
                        stack.append(t)
        return {"source": uri, "impacted": sorted(impacted),
                "edges": sorted(edges, key=lambda x: x[0] + x[1])}

    # --------------------------------------------------------- goal/metric loop
    def metric_loop(self, goal: dict, metric: dict, decision_uri: str,
                    action_uri: str, outcome_uri: str, i: int, signer: str) -> dict:
        """§7J.1 Goal->Metric->Actual->Variance->Decision->Action->Outcome: record
        the loop's connective evidence as a signed decision//state change."""
        loop = {
            "uri": decision_uri, "by": signer, "authority": f"authority://{self.label}/for-operations",
            "alternatives": ["do nothing", "rebalance provider allocation"],
            "confidence": 0.85,
            "expected_outcome": f"{metric['uri']} variance reduced toward target",
            "detail": {"goal": goal["uri"], "metric": metric["uri"],
                       "actual": metric.get("actual"), "variance": metric.get("variance"),
                       "action": action_uri, "outcome": outcome_uri},
            "made_at": now_iso(),
        }
        self.prov(i, signer, "goal->metric->variance->decision->action->outcome", [loop])
        return loop