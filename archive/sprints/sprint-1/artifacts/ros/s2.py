"""S2 — Intent & Matching (first revenue service; one domain: quoting/triage).

§4 S2: infer_intent(subject, evidence) -> intent graph; match_offers(intent, offers,
trust_scores) -> ranked matches (Trust-weighted per §5). Each match is emitted as a
signed Ledger event, and presented to a human for verification before commitment
(human-escalation floor §6/§7B — hiring a contractor is irreversible).
"""
from __future__ import annotations

import math
from typing import Any

from .substrate import Substrate


class Match:
    """A trust-weighted ranked match between an intent and an offer."""

    def __init__(self, offer_uri: str, provider: str, fit: float, trust: float,
                 score: float):
        self.offer_uri = offer_uri
        self.provider = provider
        self.fit = fit
        self.trust = trust
        self.score = score

    def to_dict(self) -> dict:
        return {
            "offer": self.offer_uri,
            "provider": self.provider,
            "fit": round(self.fit, 3),
            "trust": round(self.trust, 3),
            "score": round(self.score, 3),
        }

    def __repr__(self):
        return f"Match({self.offer_uri}, fit={self.fit:.2f} trust={self.trust:.2f} score={self.score:.2f})"


def _trust_for(trusts: list[dict], provider: str) -> float:
    """Scoped Trust per §3.14: Trust(subject→target=provider, claim, context).
    Best matching scoped score; default = low seed to avoid over-confidence."""
    best = None
    for t in trusts:
        if t.get("target") == provider:
            s = float(t.get("score", 0.0))
            best = s if best is None else max(best, s)
    return best if best is not None else 0.1


def _fit(intent_keys: set, offer_keys: list[str]) -> float:
    """Coverage of needed capabilities by the offer (fit in [0,1])."""
    if not intent_keys:
        return 0.0
    covered = len(intent_keys.intersection(offer_keys))
    return covered / len(intent_keys)


class S2Service:
    def __init__(self, substrate: Substrate):
        self.substrate = substrate

    def infer_intent(self, subject: str, evidence: dict[str, Any]) -> dict:
        """Infer what the subject wants from ambiguous evidence.

        Returns an intent dict (need + capability keys + urgency). The inference is
        recorded as a Decision (§3.12) by the acting agent, on the ledger — it is not
        a new URI noun (URI cap respected).
        """
        text = (evidence.get("request") or "").lower()
        keys: set[str] = set()
        need = "consultation"
        if "roof" in text or "leak" in text or "replac" in text:
            need = "roof replacement/repair"
            keys.update(["roofing", "repair"])
        if "urgent" in text or "emergency" in text or "leak" in text:
            pass  # urgency flagged below
        urgency = "high" if any(w in text for w in ("urgent", "emergency", "leak", "asap")) else "normal"
        budget = evidence.get("budget")
        intent = {
            "subject": subject,
            "need": need,
            "capability_keys": sorted(keys),
            "urgency": urgency,
            "budget": budget,
            "inferred_by": "agent://s2",
        }
        return intent

    def match_offers(self, intent: dict, offers: list[dict], trusts: list[dict],
                     trust_floor: float = 0.5) -> list[Match]:
        """Trust-weighted matching per §5. score = fit(intent∩capability) × scoped Trust
        (§3.14), clamped [0,1]. Offers below the trust floor are excluded."""
        need_keys = set(intent.get("capability_keys") or [])
        matches: list[Match] = []
        for off in offers:
            provider = off.get("provider")
            trust = _trust_for(trusts, provider)
            if trust < trust_floor:
                continue
            fit = _fit(need_keys, off.get("capability_keys") or [])
            score = max(0.0, min(1.0, math.prod([fit, trust])))
            matches.append(Match(off["uri"], provider, fit, trust, score))
        matches.sort(key=lambda m: m.score, reverse=True)
        return matches