"""S3 — Orchestration & Execution (Sprint 3: commit -> fleet execute + human floor).

§4 S3 / §5 / §6:
  commit(commitment, authority, terms) -> commitment://   (§5: commitment = agree(offer, terms))
  execute(commitment, fleet) -> action set                (split across an agent fleet over the
                                                            §6 routing seam, Trust-weighted)
  orchestrate(plan, capabilities) -> routed agent/human work

Human-escalation floor (§6 LEVEL A normative / §7B): any action with
`irreversible(failure) == true` OR `cost(failure) == unknowable` MUST escalate to a human
before execution. Reversible, cheap actions auto-execute (full autonomy where failure is cheap).

Deterministic local logic only (§G.11: no speculative weights, no frontier-API spend): the
routing seam picks a tier from reversibility + scoped Trust, and the irreversibility floor
overrides the seam by routing to a human `person://qk/approver`. Every step is capability-
gated (authorize, §3.4/§7B), delegated to the owning worker, and recorded as a signed
Ledger event (`decision://` for the split, `event://` ACTION per worker step). No new nouns,
no new URI schemes (frozen ontology, §7J.11/§C16).
"""
from __future__ import annotations

from .substrate import Substrate, now_iso
from .s1 import S1Service, Permission, Denial


# ---------------------------------------------------------------------------
# Routing seam tiers (§6): local / private-cloud / frontier (+ human floor)
# ---------------------------------------------------------------------------
TIERS = ("local", "private-cloud", "frontier")


class Task:
    """A bounded, delegable work item produced by orchestrating a commitment.

    `tier` is the §6 routing-seam tier the task is ROUTED to by capability; an
    irreversible/unknowable-cost task is additionally OVERRIDDEN to a human by the
    escalation floor (its `seam_tier` stays the best-capability tier, its `tier`
    becomes `human`).
    """

    def __init__(self, task_id: str, action: str, worker: str, seam_tier: str,
                 reversible: bool, cost_knowable: bool, delegation: str):
        self.task_id = task_id
        self.action = action
        self.worker = worker
        self.seam_tier = seam_tier
        self.reversible = reversible
        self.cost_knowable = cost_knowable
        self.delegation = delegation
        self.tier = seam_tier            # possibly overridden to "human"
        self.status = "PENDING"

    def escalate_plan(self) -> None:
        """§6 floor: irreversible/unknowable stays not-executed; route to a human."""
        if not self.reversible or not self.cost_knowable:
            self.tier = "human"          # seam_tier keeps the best-capability tier
            self.status = "ESCALATED"

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id, "action": self.action, "worker": self.worker,
            "seam_tier": self.seam_tier, "tier": self.tier,
            "reversible": self.reversible, "cost_knowable": self.cost_knowable,
            "authority": self.delegation, "status": self.status,
        }

    def __repr__(self):
        return f"Task({self.task_id}, {self.action}@{self.tier}, {self.status})"


class S3Service:
    def __init__(self, substrate: Substrate):
        self.substrate = substrate
        self.s1 = S1Service(substrate)

    # ---------------------------------------------------------------- helpers
    def _ev(self, kind: str, uri: str, actor: str, i: int, detail: str,
            state_update: list[dict] | None = None) -> dict:
        return {
            "uri": uri, "type": kind,
            "event_id": f"ev-s3-{i}", "correlation_id": "corr-qk-s3-1",
            "causation_id": f"ev-s3-{max(0, i-1)}", "idempotency_key": f"idem-s3-{i}",
            "signature": f"signed-by-{actor}", "occurred_at": now_iso(),
            "actor": actor, "detail": detail, "state_update": state_update or [],
        }

    # ------------------------------------------------------- risk classifier
    @staticmethod
    def risk(action: str) -> tuple[bool, bool]:
        """(irreversible, cost_knowable) for an action — the §6 escalation trigger."""
        REVERSIBLE = {
            "prepare_work_order_and_schedule": (False, True),
            "dispatch_dispatcher_and_verify_materials": (False, True),
            "quality_gate_check": (False, True),
        }
        # irreversible once done, and/or cost of failure unknowable
        IRREVERSIBLE = {
            "release_final_payment": (True, False),   # payout can't be retrieved; cost unknowable
        }
        if action in IRREVERSIBLE:
            return IRREVERSIBLE[action]
        return REVERSIBLE.get(action, (False, True))

    # -------------------------------------------------- 3.1 commit (§5)
    def commit(self, offer: dict, terms: dict, by: str, i: int,
               expectation: str = "expectation://qk/e-on-time",
               signer: str = "agent://s3") -> dict:
        """Agree a matched offer into a commitment:// (§5 commitment = agree(offer, terms))."""
        provider = offer["provider"]
        commitment = {
            "uri": f"commitment://qk/c-{provider.split('/')[-1]}",
            "by": by,                       # orchestrator commits on the relationship's behalf
            "to": provider,                 # target of the undertaking
            "obligation": offer["uri"],     # the committed work (uri ref)
            "expectation": expectation,     # what success means (§3.11)
            "status": "AGREED",
            "terms": terms,                 # additive envelope
            "agreed_at": now_iso(),
        }
        obj = {k: v for k, v in commitment.items()}
        self.substrate.record(
            self._ev("STATE_CHANGE", f"event://qk/s3-commit-{provider.split('/')[-1]}",
                     signer, i, f"commit matched offer {offer['uri']} -> "
                     f"commitment://qk/c-{provider.split('/')[-1]} (AGREED)",
                     [obj]),
            signer, [obj],
        )
        return commitment

    # ------------------------------------------------ 3.1 split / orchestrate
    def route_seam(self, task: Task, trust: float) -> None:
        """§6 routing seam, Trust-weighted + reversible: deterministic local tiers.

        A trusted actor's reversible work runs at its planned capability tier (cheap,
        own); lower trust escalates capability to private-cloud/frontier. Irreversible
        or unknowable-cost work is left to the escalation floor (orchestrate -> human).
        """
        if not (task.reversible and task.cost_knowable):
            return                       # floor overrides below (escalate_plan)
        if trust >= 0.7:
            task.tier = task.seam_tier   # deliver at the planned capability tier
        elif trust >= 0.5:
            task.tier = ("private-cloud" if task.seam_tier == "local" else "frontier")
        else:
            task.tier = "frontier"

    def orchestrate(self, commitment: dict, workers: dict, trust_scores: dict,
                    i: int, signer: str = "agent://s3") -> list[Task]:
        """Decompose the committed job into bounded tasks across the worker fleet.

        Emits a signed `decision://` recording the split (§3.12). Each task is then
        routed over the §6 seam and the irreversibility floor is applied BEFORE any
        execution plan is finalised (a sealed plan is never auto-run on irreversible work).
        """
        fleet_plan = [
            # (task_id, action, worker, seam tier by capability, delegation)
            ("t1", "prepare_work_order_and_schedule", workers["w-local"], "local",
             "delegation://qk/w-local"),
            ("t2", "dispatch_dispatcher_and_verify_materials", workers["w-cloud"],
             "private-cloud", "delegation://qk/w-cloud"),
            ("t3", "release_final_payment", workers["w-frontier"], "frontier",
             "delegation://qk/w-frontier"),
        ]
        provider = commitment["to"]
        trust = trust_scores.get(provider, 0.5)
        tasks = []
        details = []
        for tid, action, worker, seam, deleg in fleet_plan:
            rev, ck = self.risk(action)
            t = Task(tid, action, worker, seam, not rev, ck, deleg)
            self.route_seam(t, trust)      # Trust-weighted seam tier
            t.escalate_plan()              # §6 floor override (irreversible -> human)
            tasks.append(t)
            details.append(t.to_dict())

        decision = {
            "uri": f"decision://qk/s3-split-{commitment['uri'].split('/')[-1]}",
            "by": signer,
            "authority": "delegation://qk/s3-execute",
            "alternatives": ["execute serially", "defer job", "renegotiate terms"],
            "confidence": 0.9,
            "expected_outcome": f"{len(tasks)} fleet tasks under the routing seam",
            "actual_outcome": "plan sealed",
            "detail": {"commitment": commitment["uri"], "provider": provider,
                       "trust": round(trust, 3), "tasks": details},
            "made_at": now_iso(),
        }
        self.substrate.record(
            self._ev("DECISION", f"event://qk/s3-split-{commitment['uri'].split('/')[-1]}",
                     signer, i, f"orchestrate {provider}: {len(tasks)} tasks across the "
                     f"routing seam (trust {trust:.3f})",
                     [decision]),
            signer, [decision],
        )
        return tasks

    # ------------------------------------------------ 3.1 / 3.2 execute
    def execute_task(self, task: Task, context: dict, i: int,
                     signer: str | None = None) -> dict | None:
        """Execute ONE bounded, delegable task — capability-gated, then a signed ACTION event.

        Returns the ACTION event, or None if execution is refused (denied capability —
        must never run unbounded).
        """
        worker = task.worker
        signer = signer or worker
        # the worker performs the bounded action under ITS delegation (capability-based §7B)
        authz_ctx = dict(context)
        authz_ctx["delegation"] = task.delegation
        perm = self.s1.authorize(worker, task.action, authz_ctx)
        if isinstance(perm, Denial):
            return None          # refused: not authorized -> no action event
        event = self._ev(
            "ACTION", f"event://qk/s3-step-{task.task_id}", worker, i,
            f"{worker} [{task.action} @ {task.tier}] executed (authorized via "
            f"{task.delegation})",
        )
        # additive objective fields carried on the signed event (additionalProperties)
        event["worker"] = worker
        event["action"] = task.action
        event["task_id"] = task.task_id
        event["tier"] = task.tier
        event["outcome"] = "done"
        self.substrate.record(event, signer)
        task.status = "DONE"
        return event

    # ------------------------------------------------ 3.2 escalation floor
    def escalate_to_human(self, task: Task, approver: str, commitment: dict,
                          i: int, signer: str = "agent://s3") -> dict:
        """Do NOT execute an irreversible/unknowable action: record a signed escalation.

        The decision's detail states the trigger (irreversible / cost-unknowable) and
        lists that auto-execution is NOT permitted; the action proceeds only after a
        signed human acknowledgement. The Ledger records the escalation.
        """
        rev, ck = self.risk(task.action)
        escalation = {
            "uri": f"decision://qk/s3-esc-{task.task_id}",
            "by": signer,
            "authority": task.delegation,
            "alternatives": ["auto-release (NOT permitted: irreversible/unknowable)",
                             "hold pending human acknowledgement"],
            "confidence": 1.0,
            "expected_outcome": f"escalate {task.action} to {approver}",
            "actual_outcome": "ESCALATED, NOT auto-executed",
            "detail": {"task": task.to_dict(), "commitment": commitment["uri"],
                       "trigger": {"irreversible_failure": rev,
                                   "cost_failure_unknowable": (not ck)}},
            "made_at": now_iso(),
        }
        self.substrate.record(
            self._ev("DECISION", f"event://qk/s3-escalate-{task.task_id}",
                     signer, i, f"{task.action} is irreversible/unknowable-cost -> "
                     f"escalated to {approver}; NOT auto-executed",
                     [escalation]),
            signer, [escalation],
        )
        task.tier = "human"
        task.status = "ESCALATED"
        return escalation

    def human_acknowledge(self, task: Task, approver: str, authority: str,
                          commitment: dict, i: int) -> dict:
        """Signed human DECISION that enumerates the alternatives and commits the action.

        Only after this signed acknowledgement may the irreversible action be executed.
        """
        rev, ck = self.risk(task.action)
        decision = {
            "uri": f"decision://qk/s3-human-{task.task_id}",
            "by": approver,
            "authority": authority,
            "alternatives": [
                "release_in_full",
                "hold_pending_inspection",
                "release_partial_and_hold_if_fault",
                "open_dispute",
            ],
            "confidence": 1.0,
            "expected_outcome": task.action,
            "actual_outcome": "release_in_full (human approved)",
            "evidence": ["evidence://qk/e-oidc"],   # evidence_ref (array of uri)
            "detail": {"task": task.task_id, "action": task.action,
                       "commitment": commitment["uri"],
                       "trigger": {"irreversible_failure": rev,
                                   "cost_failure_unknowable": (not ck)}},
            "made_at": now_iso(),
        }
        self.substrate.record(
            self._ev("DECISION", f"event://qk/s3-human-{task.task_id}",
                     approver, i, f"{approver} signed acknowledgement -> enumerates "
                     f"alternatives and commits {task.action}",
                     [decision]),
            approver, [decision],
        )
        task.status = "HUMAN_APPROVED"
        return decision