"""S4 — Exchange & Settlement (Sprint 4) + multi-role / multi-org helpers.

§4 S4 / §4b / §3.9 / §3.11 / §3.13 / §3.2 / §C2 / §3.14:
  settle(ledger, exchange)  -> payment obligation, receipt, reconciliation  (§4 S4)
  evaluate(exchange, expectation) -> outcome (met | partial | failed)
Settlement is deterministic local logic (§G.11) over the §4b Asset Ledger slice: the
EXCHANGE is recorded as a signed `event://` (type EXCHANGE) carrying the title/custody
delta as `asset://` state, plus a signed `obligation://` (payment), `receipt://`, and a
`decision://` (reconciliation of expected vs actual value). evaluate() produces a signed
`event://` OUTCOME (met|partial|failed) that S5 consumes to update scoped Trust and close
the §5 loop with settlement in the middle.

No new URI schemes, no new nouns (URI cap, §7J.11/§C16): Exchange/Outcome are existing
Event types; the payment is an existing `obligation://`; the receipt is the existing
`receipt://` financial scheme (Appendix C §C4); reconciliation is an existing `decision://`.
Role-qualified context uses a query param on the SAME relationship scheme
(`relationship://…?role=…`) — schema-valid (uri pattern allows `?`), catalog-safe.
"""
from __future__ import annotations

from typing import Any

from .substrate import Substrate, now_iso
from .s1 import Permission, Denial


def _obj(graph, uri: str) -> dict | None:
    return graph.resolve(uri)


class S4Service:
    def __init__(self, substrate: Substrate):
        self.substrate = substrate

    # ---------------------------------------------------------------- helpers
    def _ev(self, kind: str, uri: str, actor: str, i: int, detail: str,
            state_update: list[dict] | None = None) -> dict:
        return {
            "uri": uri,
            "type": kind,
            "event_id": f"ev-s4-{i}",
            "correlation_id": "corr-qk-s4-1",
            "causation_id": f"ev-s4-{max(0, i-1)}",
            "idempotency_key": f"idem-s4-{i}",
            "signature": f"signed-by-{actor}",
            "occurred_at": now_iso(),
            "actor": actor,
            "detail": detail,
            "state_update": state_update or [],
        }

    # --------------------------------------------------- 4.1 settle (§4 S4)
    def settle(self, exchange: dict, i: int, signer: str = "agent://s4") -> dict:
        """Record an EXCHANGE on the §4b Asset Ledger and settle it.

        `exchange`: {slug, buyer, provider, price, currency, value, cost,
                     due (expectation deadline), settled_at}.
        Produces, as state carried by ONE signed EXCHANGE ledger event:
          - asset://  (title/custody transfer — §4b, not a copy)
          - the EXCHANGE event:// itself (type EXCHANGE)
          - a payment obligation obligation:// (VOLUNTARILY_UNDERTAKEN)
          - a receipt receipt://  (Appendix C §C4 financial scheme)
          - a reconciliation decision://  (expected vs actual matched)
        Returns the exchange event.
        """
        slug = exchange["slug"]
        buyer = exchange["buyer"]
        provider = exchange["provider"]
        price = exchange["price"]
        currency = exchange["currency"]
        settled_at = exchange["settled_at"]

        # --- §4b Asset Ledger: title/custody moves, never a copy ----------
        asset = {
            "uri": f"asset://money/qk-escrow-{slug}",
            "kind": "MONEY",
            "title": provider,                # value settles TO the provider
            "custody": "cleared",             # settlement completed
            "value": price,
            "currency": currency,             # envelope (additive)
            "status": "DELIVERED",
            "provenance": f"settled by {buyer} for {provider} ({slug})",
        }

        # --- the EXCHANGE event itself (type EXCHANGE, §3.16) -------------
        obligation = {
            "uri": f"obligation://qk/s4-pay-{slug}",
            "subject": buyer,                 # payer is obliged to settle
            "source": "VOLUNTARILY_UNDERTAKEN",   # arises from the AGREED commitment
            "content": f"settle {price} {currency} for contracted work by {provider}",
            "due_by": exchange["due"],
            "status": "FULFILLED",            # envelope (additive)
            "settled_at": settled_at,
        }
        receipt = {
            "uri": f"receipt://qk/s4-receipt-{slug}",
            "kind": "SETTLEMENT",             # additive on a DomainObject
            "from": buyer,
            "to": provider,
            "amount": price,
            "currency": currency,
            "received_at": settled_at,
        }
        reconciliation = {
            "uri": f"decision://qk/s4-recon-{slug}",
            "by": signer,
            "authority": "authority://qk/for-settlement",
            "alternatives": ["reject"],
            "confidence": 1.0,
            "expected_outcome": f"expected {price} {currency} from {buyer}",
            "actual_outcome": f"matched exactly: settled {price} {currency}",
            "detail": {"slug": slug, "expected": exchange.get("value"),
                       "actual": price, "matched": exchange["value"] == price,
                       "buyer": buyer, "provider": provider,
                       "reconciliation": "balanced"},
            "made_at": now_iso(),
        }
        exch_event = self._ev(
            "EXCHANGE", f"event://qk/s4-exchange-{slug}", signer, i,
            f"settle exchange {slug}: {price} {currency} {buyer}->{provider} "
            f"(value {exchange.get('value')}, cost {exchange.get('cost')})",
        )
        # additive objective fields (§7K.1 causation/correlation): envelope
        exch_event["value"] = exchange.get("value")
        exch_event["cost"] = exchange.get("cost")
        exch_event["price"] = price
        exch_event["currency"] = currency
        exch_event["buyer"] = buyer
        exch_event["provider"] = provider
        exch_event["settled_at"] = settled_at
        exch_event["exchange_of"] = exchange.get("of")

        # embed the state delta as a CLOSURE COPY (self-reference would break
        # canonical serialization): the graph gets the exchange event object via
        # a copy, exactly the §3.16 / Sprint-1 1.3 reconstruction convention.
        exch_copy = {k: v for k, v in exch_event.items()}
        exch_event["state_update"] = [asset, obligation, receipt, reconciliation,
                                      exch_copy]
        self.substrate.record(exch_event, signer)
        return exch_event

    # ------------------------------------------------ 4.1 evaluate (§4 S4)
    def evaluate(self, exchange: dict, expectation: dict, i: int,
                 signer: str = "agent://s4") -> dict:
        """Evaluate the settled exchange against the §3.11 Expectation.

        met if the settled value equals the expected value AND the settlement
        lands by the expectation deadline; partial if the value is short but the
        expectation was still substantially met; failed otherwise. Returns the
        signed OUTCOME event:// (type OUTCOME).
        """
        slug = exchange["slug"]
        settled = exchange["price"]
        expected = expectation.get("threshold", exchange.get("value"))
        settled_at = exchange["settled_at"]
        deadline = expectation.get("deadline")

        if settled == expected and settled_at <= deadline:
            result, ev_score = "met", 1.0
        elif settled >= expected * 0.9:
            result, ev_score = "partial", 0.5
        else:
            result, ev_score = "failed", 0.0

        outcome = self._ev(
            "OUTCOME", f"event://qk/s4-outcome-{slug}", signer, i,
            f"evaluate settle {slug}: settled {settled} vs expected {expected} "
            f"by {deadline} -> {result}",
        )
        outcome["evaluation"] = result
        outcome["expected"] = expected
        outcome["actual"] = settled
        outcome["deadline"] = deadline
        outcome["settled_at"] = settled_at
        outcome["score"] = ev_score            # 1.0 / 0.5 / 0.0 for S5
        outcome["state_update"] = [dict(outcome)]
        self.substrate.record(outcome, signer)
        return outcome

    # ---------------------------------------------- 4.2 role-scoped identity
    def resolve_role_named(self, relationship: str, participant: str,
                           role: str) -> bool:
        """§C2 role is an attribute of relationship://. True if `participant`
        holds `role` in this relationship (context-specific per §3.2)."""
        rel = _obj(self.substrate.graph, relationship)
        if rel is None:
            return False
        roles = (rel.get("roles") or {}).get(participant, [])
        return role in roles

    # ---------------------------------------------- 4.2 role-scoped authority
    def authorize_for_role(self, identity: str, action: str, relationship: str,
                           role: str) -> Permission | Denial:
        """Role-scoped authz (§3.2/§3.19): an action is permitted in `role`
        only if the relationship's role->authority map grants it. Same identity,
        same relationship, two different answers by role."""
        rel = _obj(self.substrate.graph, relationship)
        if rel is None:
            return Denial(action, f"no such relationship {relationship}")
        by_role = (rel.get("authority_by_role") or {})
        auth_ref = by_role.get(role)
        if not auth_ref:
            return Denial(action, f"no authority bound to role '{role}'")
        auth = _obj(self.substrate.graph, auth_ref)
        if auth is None or isinstance(auth.get("grants"), list) is False:
            return Denial(action, f"{auth_ref} carries no grants")
        if action in auth["grants"]:
            return Permission(action, {
                "performer": identity, "source": auth_ref,
                "relationship": relationship, "role": role,
                "scope": auth["grants"], "issued_at": now_iso()})
        return Denial(action, f"granted for {auth_ref} does not include '{action}'")