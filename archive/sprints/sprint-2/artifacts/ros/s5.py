"""S5 — Accountability & Trust engine (Sprint 2: capture → verify → update → write).

§5 / §3.11 / §3.13 / §3.14 / §3.17:
  capture(outcome, provenance) -> signed evidence://        (anchored completion record)
  verify(evidence, statement)   -> verified result  {claim, degree, procedure}  (§3.17)
  update(Trust, evidence, weight, recency) -> Trust  T_{k+1}=clamp(T_k +
        alpha*(outcome_k - expectation_k)*evidence_k*recency, 0, 1), keyed
        (subject, target, claim, context) per §3.14 — NOT a single global score.

One crisp, objective outcome class: "contracted roofing job completed by its
committed deadline" — verifiable via an anchored completion record comparing
`actual_completed_at` against `committed_deadline`. Captured/reasoned evidence
supports a claim to a *degree* under a *procedure*; no capital-T truth overclaim (F2.1).
"""
from __future__ import annotations

from typing import Any

from .substrate import Substrate, now_iso

# Learning rate budget — same alpha for every update; the run is driven by the
# seeded/verified evidence, not hardcoded speculative weights (§G.11).
ALPHA = 0.5
EXPECTATION = 0.8          # expected success threshold for "on time" (a stated target)
RECENCY = 1.0              # recency multiplier (both updates are current, so 1.0)

EXPUT = 0  # module placeholder (kept for linters); real config lives per-call


class VerifyResult:
    """§3.17: evidence supports claim X to degree Y under procedure Z."""

    def __init__(self, claim: str, degree: float, procedure: str, evidence_uri: str,
                 outcome_uri: str, provider: str, on_time: bool):
        self.claim = claim
        self.degree = degree
        self.procedure = procedure
        self.evidence_uri = evidence_uri
        self.outcome_uri = outcome_uri
        self.provider = provider
        self.on_time = on_time

    def to_dict(self) -> dict:
        return {
            "claim": self.claim,
            "degree": round(self.degree, 3),
            "procedure": self.procedure,
            "evidence": self.evidence_uri,
            "outcome": self.outcome_uri,
            "provider": self.provider,
            "on_time": self.on_time,
        }

    def __repr__(self):
        return (f"VerifyResult({self.provider}, on_time={self.on_time}, "
                f"degree={self.degree:.2f}@{self.procedure})")


class S5Service:
    def __init__(self, substrate: Substrate):
        self.substrate = substrate

    # ------------------------------------------------------------------ utils
    def _ev(self, kind: str, uri: str, actor: str, i: int, detail: str,
            state_update: list[dict] | None = None) -> dict:
        return {
            "uri": uri,
            "type": kind,
            "event_id": f"ev-s2-{i}",
            "correlation_id": "corr-qk-trust-1",
            "causation_id": f"ev-s2-{max(0, i-1)}",
            "idempotency_key": f"idem-s2-{i}",
            "signature": f"signed-by-{actor}",
            "occurred_at": now_iso(),
            "actor": actor,
            "detail": detail,
            "state_update": state_update or [],
        }

    # ---------------------------------------------------------- 2.1 capture
    def capture(self, outcome: dict, provenance: dict, signer: str, i: int
                ) -> tuple[dict, bool]:
        """Capture a raw outcome as signed, anchored evidence.

        `outcome`: {uri: outcome:///event://, provider, committed_deadline,
                    actual_completed_at, note}.
        `provenance`: {source, procedure, confidence}.
        Returns (evidence:// object, on_time Bool). The outcome is objective:
        completed by the committed deadline => on time.
        """
        g = self.substrate.graph
        on_time = outcome["actual_completed_at"] <= outcome["committed_deadline"]
        provider = outcome["provider"]

        # the anchored completion record itself is an OUTCOME Event (§3.16)
        completion = self._ev(
            "OUTCOME", outcome["uri"], provider, i,
            f"job {outcome['job']} by {provider}: actual "
            f"{outcome['actual_completed_at']} vs committed "
            f"{outcome['committed_deadline']} -> {'on time' if on_time else 'LATE'}",
        )
        # additive objective fields (Event envelope allows additionalProperties)
        completion["job"] = outcome["job"]
        completion["provider"] = provider
        completion["committed_deadline"] = outcome["committed_deadline"]
        completion["actual_completed_at"] = outcome["actual_completed_at"]
        completion["on_time"] = on_time
        evidence = {
            "uri": f"evidence://qk/{outcome['job']}",
            "kind": "ANCHORED",
            "source": provenance["source"],
            "verity": {"procedure": provenance["procedure"],
                       "confidence": provenance["confidence"]},
            "captured_at": now_iso(),
        }
        # embed the state delta in the ledger entry so the round-trip
        # reconstructs it (§3.16 / sprint-1 1.3 convention); the closure copy
        # avoids a self-referential list in the canonical serialization.
        obj_for_update = {k: v for k, v in completion.items()}
        completion["state_update"] = [obj_for_update, evidence]
        self.substrate.record(completion, signer)
        return evidence, on_time

    # --------------------------------------------------------- 2.1 expectation
    def make_expectation(self, uri: str, subject: str, condition: str,
                         deadline: str) -> dict:
        """§3.11 expectation:// — what success means for the outcome class."""
        exp = {
            "uri": uri,
            "actor": "org://quoteko",
            "subject": subject,
            "condition": condition,
            "metric": "on_time",
            "threshold": EXPECTATION,
            "deadline": deadline,
            "evidence_required": "CLEAR",
        }
        self.substrate.graph.put(exp)
        return exp

    # ------------------------------------------------------------- 2.1 verify
    def verify(self, evidence: dict, statement: str, outcome: dict,
               i: int, signer: str = "agent://s5") -> VerifyResult:
        """§3.17 claim-verification: evidence supports claim X to degree Y under
        procedure Z. Bounded result — never a capital-T 'truth' declaration."""
        on_time = outcome["actual_completed_at"] <= outcome["committed_deadline"]
        verity = evidence.get("verity", {})
        result = VerifyResult(
            claim=statement,
            degree=float(verity.get("confidence", 1.0)),
            procedure=verity.get("procedure", "asserted"),
            evidence_uri=evidence["uri"],
            outcome_uri=outcome["uri"],
            provider=outcome["provider"],
            on_time=on_time,
        )
        claim_obj = {
            "uri": f"claim://qk/{outcome['job']}",
            "proposer": signer,
            "statement": statement,
        }
        self.substrate.record(
            self._ev("DECISION", f"event://qk/verify-{outcome['job']}", signer, i,
                     f"verify '{statement}' -> degree {result.degree:.2f} "
                     f"under procedure '{result.procedure}'",
                     [claim_obj, evidence]),
            signer,
        )
        return result

    def outcome_score(self, on_time: bool) -> float:
        """The objective scalar the trust update consumes (0 or 1)."""
        return 1.0 if on_time else 0.0

    # ---------------------------------------------------------- 2.2 update
    def update_trust(self, subject: str, target: str, claim: str, context: str,
                     verify: VerifyResult, evidence_score: float, i: int,
                     alpha: float = ALPHA, expectation: float = EXPECTATION,
                     recency: float = RECENCY, signer: str = "agent://s5") -> dict:
        """§5: T_{k+1} = clamp(T_k + alpha*(outcome_k - expectation_k)
        * evidence_k * recency, 0, 1). Keyed (subject, target, claim, context).

        Writes the updated trust:// to the Graph + a signed STATE_CHANGE ledger
        event, and returns the new trust object.
        """
        g = self.substrate.graph
        outcome = self.outcome_score(verify.on_time)
        delta = alpha * (outcome - expectation) * evidence_score * recency

        # find the existing trust:// object keyed on (subject,target,claim,context)
        current = None
        for obj in g.objects.values():
            if not obj.get("uri", "").startswith("trust://"):
                continue
            if (obj.get("subject") == subject and obj.get("target") == target
                    and obj.get("claim") == claim
                    and obj.get("context") == context):
                current = obj
                break
        cold_start = 0.5  # conservative seed if none present (new (subj,tgt,claim,ctx) key)
        t_old = float(current.get("score")) if current else cold_start
        t_new = max(0.0, min(1.0, t_old + delta))

        trust = dict(current) if current else {
            "uri": f"trust://qk/t-{target.split('/')[-1]}",
            "subject": subject, "target": target, "claim": claim,
            "context": context, "score": 0.0,
        }
        trust["score"] = round(t_new, 3)
        trust["updated_at"] = now_iso()
        # additive envelope fields (additionalProperties:true) — auditable update
        trust["expected"] = expectation
        trust["outcome"] = outcome
        trust["evidence"] = [verify.evidence_uri]
        trust["alpha"] = alpha
        trust["recency"] = recency

        self.substrate.record(
            self._ev("STATE_CHANGE",
                     f"event://qk/trust-update-{target.split('/')[-1]}", signer, i,
                     f"trust for {target} [{claim}] {t_old:.3f} -> {t_new:.3f} "
                     f"(outcome={outcome:.0f}, exp={expectation:.1f}, "
                     f"ev={evidence_score:.2f}, alpha={alpha})",
                     [trust]),
            signer, [trust],
        )
        return trust


def config_defaults() -> dict:
    """Expose the run's update configuration (alpha/expectation/recency)."""
    return {"alpha": ALPHA, "expectation": EXPECTATION, "recency": RECENCY}