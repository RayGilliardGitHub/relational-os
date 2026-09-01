# Protocol — RelationalOS sprint lifecycle

**Applies to every sprint and sub-sprint.** A fresh Hermes `/new` session has NO
memory; it must rely only on these files. Follow this sequence in every sprint.

## The loop
1. **Read the spec.** Open `/home/rlg/relational-os/SPEC.md` and read it in full
   before touching anything. Read this `PROTOCOL.md`. Read the prior sprint's
   `summary.md` (if any) for hand-off context.
2. **Plan first.** Write `<sprint>/plan.md`: objectives, a numbered sub-sprint
   breakdown, a Definition of Done, and explicit exit criteria. Each sub-sprint
   ALSO gets a plan at `<sprint>/work/<n>-plan.md` written before that sub-sprint
   executes. Planning always precedes execution — never the reverse.
3. **Execute** the sub-sprints in order. Ground every claim in real tool output;
   produce real artifacts (schemas, validators, reports) and RUN them. Never
   fabricate results, file contents, or citations.
4. **Capture findings as you go.** Append every discovery (assumptions that broke,
   decisions taken, spec gaps, corrections) to `<sprint>/notes/findings.md` with a
   date. Findings are what drive spec updates.
5. **Update the spec from findings (mandatory).** Apply changes to `SPEC.md`
   following the `system-specification` skill conventions: targeted `patch` edits,
   re-number sections if anything moves, bump the minor version, append a dated
   entry to the Version/Review Log. Rules:
   - Do NOT restructure at whim.
   - Do NOT add new ontology concepts or URI schemes beyond the documented cap
     (§7J.11 / Appendix C §C16). The ontology is frozen.
   - Preserve every requirement's meaning; fix real problems found during the build.
6. **Verify the Definition of Done** against the plan. Write `<sprint>/summary.md`
   (what was built, verified output, open issues, what the spec gained).
7. **Hand off.** In your final message AND as a file, write the next sprint's
   self-contained prompt at `<next>/PROMPT.md`. It must reference only absolute
   paths and the current `SPEC.md` — a fresh session depends on nothing else.
8. **Terminate when there is nothing new to do (mandatory check).** Before writing
   the next prompt, ask: *would the next sprint add new capability, a new proof, or
   a genuinely new audit surface — or would it only re-verify ground already proven
   from the same recorded data?* If the next sprint would add nothing new — every
   derivable seam is closed and what remains is the honest residual (a boundary the
   project refuses to invent, or a §6-human choice no machine can make) plus ritual
   re-audit over byte-identical inputs — then DO NOT write a next `PROMPT.md`.
   Instead:
   - Write `<current>/COMPLETE.md` stating that the chain is done, naming the
     residual boundary, and noting the decisive prior sprint.
   - Write NO `<next>/PROMPT.md`; do not manufacture a successor.
   - State plainly in your final message: "nothing new left for a sprint; series
     ends here."
   This is not optional decoration: a fresh session asked to write Sprint N+1 must
   first decide whether any real sprint would pay for itself, and must refuse to emit
   one purely because the previous prompt said "write a next prompt." The prompt
   chain is a means to the work, not an obligation to run forever.

## Non-negotiables
- Read before write, plan before build.
- Real tool output only.
- **Single-threaded execution. Do all work yourself, in ONE sequential process. Do
  NOT use `delegate_task`/subagents and do NOT hand off work to child agents** — they
  consistently fail at this task. Sub-sprints are sequential phases *you* execute
  directly (plan → build → verify in order), not parallel tasks to farm out.
- Keep the URI cap and the frozen ontology.
- Respect the user's ~$10/mo token cap: prefer local computation, batch where
  possible, keep prompts lean.
- User is Raymond: clean English output, report status at each long step, use
  `file://` absolute paths, no fabrication, no flattery.

## Sprint-0 scope (current)
Deliver the implementation contract: a machine-validatable schema (from Appendix F),
a conformance validator, executable fixtures (Appendix E + §7L loop + Case
lifecycle), and the four committed surveys (§7D-E). Full detail is in
`SPEC.md §8` and `sprints/sprint-0/PROMPT.md`.