"""S1 — Identity, Authentication, Authorization (substrate service).

§4 S1 / §3.19: IDENTITY (who) -> AUTHENTICATION (prove it) -> AUTHORIZATION (may you)
-> ACTION. Role is an attribute of relationship:// (§C2), never a separate identity.
Authorization is capability-based per §7B: bounded, revocable, expiry-bound; a revoked
delegation immediately voids the derived capability.
"""
from __future__ import annotations

import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any

from .substrate import Ledger, Substrate, now_iso


class Permission:
    def __init__(self, target: str, capability: dict):
        self.target = target
        self.capability = capability

    def to_dict(self) -> dict:
        return {"action": self.target, "capability": self.capability}

    def __repr__(self):
        return f"Permission({self.target}, scoped@{self.capability.get('scope')})"


class Denial:
    def __init__(self, target: str, reason: str):
        self.target = target
        self.reason = reason

    def to_dict(self) -> dict:
        return {"action": self.target, "denial": self.reason}

    def __repr__(self):
        return f"Denial({self.target}, {self.reason})"


def _obj(graph, uri: str) -> dict | None:
    return graph.resolve(uri)


class S1Service:
    """S1 substrate calls operate over the shared Graph + Ledger."""

    def __init__(self, substrate: Substrate):
        self.substrate = substrate

    # ---- IDENTITY (who) ---------------------------------------------------
    def resolve_identity(self, subject: str, evidence: list[str]) -> str | None:
        """Map a subject + evidence to a canonical identity URI.

        Delegates to an `entity://` canonical-resolution record if present
        (§7K.1: IBM ≡ International Business Machines); otherwise returns the
        subject verbatim if it is already an identity Actor on the graph.
        """
        g = self.substrate.graph
        for obj in g.objects.values():
            if obj.get("uri", "").startswith("entity://"):
                if subject in (obj.get("aliases") or []) or subject == obj["canonical"]:
                    return obj["canonical"]
        return subject  # already a typed identity URI (person://x, org://x, agent://x)

    # ---- AUTHENTICATION (prove it) ----------------------------------------
    def authenticate(self, identity: str, credentials: dict[str, Any]) -> float:
        """Prove identity from evidence/attestations; return verification score [0,1]."""
        actor = _obj(self.substrate.graph, identity)
        attests = (actor or {}).get("identity", {}).get("attestations", [])
        score = 0.0
        if "oide-verified" in (credentials.get("attestations") or []):
            score += 0.8
        if attests:
            score += 0.2 * min(1.0, len(attests))
        return round(min(1.0, score), 3)

    # ---- AUTHORIZATION (may you) — capability-based (§7B) -----------------
    def authorize(self, identity: str, action: str, context: dict[str, Any]) -> Permission | Denial:
        """Return a bounded capability if the actor may perform `action` in this
        relationship/context, else a Denial. Capability is derived from the
        relationship's authority + any ACTIVE delegation; a revoked/expired
        delegation voids it immediately (§7B). Authority and delegation scope are
        URIs (per schema): an authority:// carries `grants`; a delegation://
        references rule:// scope entries that carry `grants`."""
        rel_uri = context.get("relationship")
        rel = _obj(self.substrate.graph, rel_uri)
        if rel is None:
            return Denial(action, f"no such relationship {rel_uri}")
        refs: list[str] = list(rel.get("authority") or [])
        if context.get("delegation"):
            refs.insert(0, context["delegation"])
        for ref in refs:
            if not ref:
                continue
            src = _obj(self.substrate.graph, ref)
            if src is None:
                continue
            if src.get("status") not in (None, "ACTIVE"):
                return Denial(action, f"{ref} not active ({src.get('status')})")
            if isinstance(src.get("grants"), list) and action in src["grants"]:
                return Permission(
                    action,
                    {"performer": identity, "source": ref, "relationship": rel_uri,
                     "scope": src["grants"],
                     "issued_at": now_iso(),
                     "expires_at": (datetime.now(timezone.utc)
                                    + timedelta(hours=1)).isoformat().replace("+00:00", "Z")},
                )
            # delegation: scope = list of rule:// URIs; follow to their grants
            if isinstance(src.get("scope"), list):
                for sref in src["scope"]:
                    s = _obj(self.substrate.graph, sref)
                    if s and isinstance(s.get("grants"), list) and action in s["grants"]:
                        return Permission(
                            action,
                            {"performer": identity, "source": ref, "scope": s["grants"],
                             "relationship": rel_uri, "issued_at": now_iso(),
                             "expires_at": (datetime.now(timezone.utc)
                                            + timedelta(hours=1)).isoformat().replace("+00:00", "Z")},
                        )
        return Denial(action, "no active authority/delegation grants this action")

    # ---- ROLE (attribute of relationship, per §C2) ------------------------
    def resolve_role(self, relationship: str, participant: str, context: dict[str, Any]) -> str | None:
        rel = _obj(self.substrate.graph, relationship)
        if rel is None:
            return None
        roles = (rel.get("roles") or {}).get(participant, [])
        return roles[0] if roles else None


def authorize_via(mod, **kw):
    """Small helper wrapper to keep authorize() callable from other services."""
    return mod.authorize(**kw)