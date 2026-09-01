# 06 — USER MANUAL (the owner's manual)

**Audience:** the owner / decision-maker who reads the cockpit each morning.
**Goal:** read the §7L ten morning questions, understand the operating cycle
exception→case→task→verified-outcome→learning, and exercise human oversight with
**do-nothing treated as a real option**.
**Grounding:** SPEC §7J/§7K/§7L, and the real cockpit report at
`/home/rlg/relational-os/reports/cockpit.md`. I do not need you to
run software every morning — but when you want the day's answer, one command produces it
(`03-run.md §1`). You read the report.

---

## 1. What you are looking at

The **cockpit** is the Monday-morning surface: *business health, what needs attention, and
an AI recommendation.* It answers the ten questions of the **§7L Business Indispensability
Test** — the acceptance test of the whole system — **with evidence** from the ledger/graph,
not opinions (SPEC §7L). "Answer with evidence" means: each answer cites the signed ledger
event or graph object behind it. That is the difference between a dashboard and an operating
system: what the system claims, it can prove from history.

> **Branding (Sprint 7):** in the **sector instances** the cockpit is branded — the lead
> header reads `Company — tagline` (e.g. `Valiant Aero — Subsystems on the line, on the
> date.`) and a `## Brand` appendix (About, Mission/Vision/Values, Products, FAQ, Contact,
> Design language) appears at the foot, so the report always states **for whom** it was
> produced. A separate `branding.md` marketing artifact accompanies each instance. See
> `instances/README.md`.

## 2. The ten morning questions and how to read them (real answers)

These are the exact §7L ten (SPEC §7L), with Quoteko's real cockpit answers (from
`reports/cockpit.md`). Read them top to bottom; #8 is the one that turns into your work.

   1. **WHAT HAPPENED?** On-time contracted completions 6/7 (0.857); solarworks settled on
      time, norcrete late; settled value 24850.0.  [ledger evidence]
   2. **WHAT CHANGED?** Provider re-allocation recommended; rallied solarworks delivery
      verified on time; forward-period on-time = 1.0.  [delta → significance]
   3. **WHAT MATTERS?** Priority-ordered attention: re-balance provider allocation, rallied
      follow-on delivery (solarworks).  [§7J.5]
   4. **WHAT'S GOING WRONG?** On-time delivery 0.857 below target 0.95 (CRITICAL).  [§7J.2]
   5. **WHY?** Provider scheduling failure — norcrete missed its deadline (root SUPPORTED:
      scoped Trust 0.92→0.528).  [§7K.2 epistemic status]
   6. **WHAT IF WE DO NOTHING?** Forecast on-time ~0.83 < 0.95; laggard keeps missing
      deadlines; scoped customer Trust erodes.  [§7K.1 forecast]
   7. **WHAT ARE OUR OPTIONS?** re-balance to solarworks; gate norcrete; do-nothing (all
      costed; trade-off in the recommendation).  [§7K.1]
   8. **WHAT SHOULD WE DO?** → assigned, authorized Task `task://qk/t-provider-rebalance`
      under `authority://qk/for-operations`.  [recommendation]
   9. **WHO DOES IT, AND DO THEY HAVE THE AUTHORITY/CAPACITY?** `agent://w-ops` via
      `delegation://qk/w-ops` (delegation-bounded authority, capacity 1.0), owner
      `person://qk/approver`.  [ownership + authority/capacity]
  10. **DID IT WORK, AND WHAT DID WE LEARN?** Yes — rallied delivery verified on time
      (forward on-time 1.0); Learning entry `decision://qk/s5-learning-on-time`;
      provider-allocation policy v3 updated (change-future-policy).  [verified outcome +
      organisational learning]

**Reading it as an owner:**
- **#1–#6** are your situational awareness — the state, the change, the exceptions, the
  root cause *with its certainty flagged* (#5 says the root is **SUPPORTED**, a claimed
  epistemic status — it is not asserted as absolute fact, §7K.2), and what happens if you do
  nothing (#6).
- **#7** gives your real options, explicitly including **do-nothing**, with the trade-off.
- **#8 is your decision point** — the recommendation carries the **authority it requires**;
  authorizing it turns it into assigned, authorized work.
- **#9** tells you who does it and proves they hold the authority **and** capacity.
- **#10** closes the loop: did it work (verified), and what did we learn (policy updated so
  the next decision is better).

## 3. The operating cycle, end to end

The system's daily heartbeat is an **exception → case → task → verified outcome → learning**
cycle (SPEC §7J.2/§7J.3/§7K.1). On Quoteko this morning it was:

    EXPECTED 0.95 → ACTUAL 0.833 → VARIANCE -0.117 → SIGNIFICANCE CRITICAL
        → EXCEPTION: on-time delivery below target
        → ROOT (SUPPORTED): norcrete missed its deadline; scoped Trust 0.92→0.528
        → RECOMMENDED ACTION (#8): re-balance to solarworks, gate norcrete
        → DECISION: you (the owner) authorize the re-allocation
        → EXECUTION: `agent://w-ops` re-balances the provider mix (bounded by its delegation)
        → VERIFIED OUTCOME: the rallied follow-on delivery settled on time
          (forward-period on-time 1.0; solarworks scoped Trust → 1.0)
        → LEARNING: `decision://qk/s5-learning-on-time` → policy v3

Where each piece appears in the cockpit: the exception (#4/#5), the recommendation (#8), the
assigned task (#8/#9), the verified outcome and learning (#10). That is the product gate in
SPEC §7L/§8: an operating system, not a dashboard.

## 4. A recommendation that "carries the authority it requires"

The AI recommendation is **not a suggestion to be rubber-stamped** — it is scoped to a
specific bounded authority, and it has the audit trail to back it:
- it names the **authority required** (`authority://qk/for-operations`) and the worker who
  would carry it (`agent://w-ops`), acting under a **revocable delegation** (`delegation://qk/w-ops`);
- it states its **confidence** (0.85) and **expected impact**;
- its **options** include contradictory paths and **do-nothing**, with a **trade-off**
  ("re-balancing concentrates work with solarworks [higher short-term concentration risk]
  but restores on-time fulfilment and protects scoped customer Trust").

Your job is to **decide whether to grant that authority**, not to babysit the mechanics —
SPEC §7J.4 turns the human from an AI *babysitter* into an AI *supervisor*.

## 5. Do-nothing is a real option

"Options incl. do-nothing" is a deliberate feature (§7K.1). The cockpit costs the
do-nothing path: see **#6** — "forecast on-time ~0.83 < 0.95; laggard keeps missing
deadlines; scoped customer Trust erodes," and the recommendation's trade-off notes the cost
of inaction. A good recommendation *should* often be "do nothing" when the evidence doesn't
justify action; many decisions legitimately close that way. Do not feel obligated to act on
every recommendation — but decide explicitly, and let the system record why.

## 6. Human-oversight discipline (§6 floor)

The system's center is human authority, not autonomy:
- **Irreversible or unknowable-cost actions are never auto-executed.** They escalate to a
  human first (SPEC §6, §7A). In the S1–S5 chain this is *provable from the signed ledger
  event order* (split < escalate < human < release), not a flag (verified in `checks.escalate_check`).
- Oversight must be **demonstrable** (§7K.1 Acknowledgement): the system only claims "human
  oversight" where the human provably took custody of the decision. When you act, act as a
  signed decision — the record is what makes the system auditable.
- **Authority ≠ responsibility ≠ accountability (§7K.2):** delegating the authority to *act*
  (an agent may re-balance allocation) is not the same as assigning the *work*, and neither
  is the same as *owning the outcome*. Your authorized signature on #8 is the ownership act.

## 7. A short morning routine

1. `cd /home/rlg/relational-os/reference && python3 run_s5_demo.py` (exit 0).
2. Open `reports/cockpit.md`.
3. Read **#1–#6** (situation), **#7** (options incl. do-nothing), then **#8/#9** (the
   decision and who has authority to execute it).
4. Authorize #8 (grants the required authority), or explicitly choose do-nothing — either is
   legitimate, both are recorded.
5. Next morning, **#10** tells you whether it worked and what the system learned.

**Future deployment:** the human-loop UI/SLA/queue (§7D-C) that would put this routine in a
browser is spec'd but not built; today you read the markdown cockpit. The §7E frontends and
the §7F audit findings are also future (see `01-system-manual.md §9`).