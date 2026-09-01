"""RelationalOS Sprint-1 substrate: shared Relationship Graph (state) + append-only Ledger.

Implements the §3.16 contract: Ledger = history (append-only, content-addressed,
signed), Graph = current state. Both read/write schema-conformant objects.
Round-trip: unknown fields are preserved on rewrite (§2, Appendix C).
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _canonical(obj: dict) -> str:
    """Canonical JSON matching conformance.py C3 (sort_keys, compact separators)."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def sign(payload: dict, service: str) -> str:
    """Deterministic signature by the responsible service over the canonical payload."""
    h = hashlib.sha256(_canonical(payload).encode()).hexdigest()
    return f"sig:{service}:{h}"


class Ledger:
    """Append-only, content-addressed (SHA-256 over prev-hash + payload), signed history."""

    def __init__(self, uri: str):
        self.uri = uri
        self.entries: list[dict] = []
        self.head_hash = ""

    def append(self, event: dict, signer: str) -> dict:
        """Append a copy of `event` (minus any existing 'hash'), chained + signed.

        Returns the stored ledger entry.
        """
        payload = {k: v for k, v in event.items() if k != "hash"}
        if "signature" not in payload:
            payload["signature"] = sign(payload, signer)
        content = _canonical(payload)
        h = hashlib.sha256((self.head_hash + content).encode()).hexdigest()
        entry = dict(payload)
        entry["hash"] = h
        self.entries.append(entry)
        self.head_hash = h
        return entry

    def to_dict(self) -> dict:
        return {"uri": self.uri, "head_hash": self.head_hash, "entries": self.entries}

    def verify(self) -> tuple[bool, str]:
        prev = ""
        for e in self.entries:
            content = _canonical({k: v for k, v in e.items() if k != "hash"})
            expect = hashlib.sha256((prev + content).encode()).hexdigest()
            if e.get("hash") != expect:
                return False, f"chain break @ {e.get('event_id')}"
            if not e.get("signature"):
                return False, f"unsigned @ {e.get('event_id')}"
            prev = expect
        if self.head_hash != prev:
            return False, "head_hash mismatch"
        return True, "ok"


class Graph:
    """Current relational state projection (§3.16 Graph = state, distinct from ledger)."""

    def __init__(self):
        self.objects: dict[str, dict] = {}

    def put(self, obj: dict) -> None:
        """Put/upsert a current-state object keyed by its URI. Preserve-unknown."""
        self.objects[obj["uri"]] = obj

    def get(self, uri: str) -> dict | None:
        return self.objects.get(uri)

    def resolve(self, uri: str) -> dict | None:
        return self.get(uri)

    def to_dict(self) -> dict:
        return {"kind": "GRAPH", "objects": list(self.objects.values())}


class Substrate:
    """Binds the shared Graph + Ledger; the integration point (§5, §7C)."""

    def __init__(self, ledger_uri: str = "db://ledger/quoteko-2026"):
        self.ledger = Ledger(ledger_uri)
        self.graph = Graph()

    def record(self, event: dict, signer: str, graph_updates: list[dict] | None = None) -> dict:
        """Append an event to the Ledger, then apply resulting graph updates (state).

        `graph_updates` is taken from the event's embedded `state_update` when not
        given explicitly, so every state change is carried by its producing event
        (which is what makes Graph→Ledger reconstruction possible in 1.3).
        """
        entry = self.ledger.append(event, signer)
        updates = graph_updates if graph_updates is not None else event.get("state_update")
        if updates:
            for obj in updates:
                self.graph.put(obj)
        return entry

    def clone_graph(self):
        from copy import deepcopy
        g = Graph()
        g.objects = {u: deepcopy(o) for u, o in self.graph.objects.items()}
        return g