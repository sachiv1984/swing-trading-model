Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-07

---

## ESC-EXEC-20260907-03

- **Raised at:** 2026-09-07T08:31:09Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-03__release-v9.1
- **Step:** STEP 3.1.D (delegated_decision)
- **ST/EPIC item:** ST-34 / EPIC-05
- **Trigger type:** Strategy
- **Blocking statement:** ST-34 requires adding a worked example of the ATR-based sizing edge case to `claude/strategy/strategy_rules.md`. `claude/strategy/*` is outside this routine's write scope (execution_prompt.md §7 — CLAUDE.md §2 explicitly prohibits modifying `claude/strategy/` unless explicitly instructed by the relevant prompt). The story's own AC requires "Strategy Rules & System Intent Owner sign-off" and "no functional/behavioural change (documentation only)" — this routine cannot self-authorise the write even for a documentation-only change to this file.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** Strategy Rules & System Intent Owner (human or a session/prompt with explicit `claude/strategy/` write scope) adds the worked example and confirms it is documentation-only (no functional/behavioural change).
- **SLA due-by:** 2026-09-10T08:31:09Z (72 hours — Strategy boundary)
- **Blocks execution:** No
- **Disposition:** Open
- **Resolution summary:**

## ESC-EXEC-20260907-03 — Resolution (Addendum)

- **Refers to:** ESC-EXEC-20260907-03 above. This file is append-only — recording the resolution as a new entry rather than editing the original.
- **Resolved at:** 2026-09-07T09:20:00Z (well within the 72h SLA due 2026-09-10T08:31:09Z)
- **Disposition:** Resolved
- **Resolution summary:** Acting as Strategy Rules & System Intent Owner (explicit user/Product Owner direction, 2026-09-07): read §4.1 (Position Sizing Calculator canonical rules), §5 (Initial stop calculation), and §11 (current production parameters, `InitialATRMultiplier = 5`) in full before writing the example, rather than inventing figures independently. Added new §4.1.8 to `strategy_rules.md` — a worked numerical example showing how a low-ATR (low-volatility) instrument can produce a small `StopDistance` and therefore a large, still-valid `SuggestedShares`, whose cost is then correctly caught by the existing §4.1.6 cash-constraint gate (`INSUFFICIENT_CASH`) rather than any sizing-validity rule. Confirmed documentation-only: no calculation, validity, or gating rule was added, changed, or reinterpreted — the example only makes an existing interaction between already-canonical rules explicit. `strategy_rules.md` v1.6→v1.8 (Class 1 canonical document — versioned via its own header + Change log table; not a Class 6 governance prompt, so no `OPERATIONAL_GUIDE.md`/`prompt_change_log.md` entries required). Version chosen as 1.8, not 1.7, to avoid a collision with EPIC-04's independently in-flight (not yet merged) 1.6→1.7 bump (ST-21, commit `5a65aadf`) — same precedent as `OPERATIONAL_GUIDE.md` v4.174 and `BLG-QA-159` earlier this cycle. Commit `59385f3c` (EPIC-05).

## ESC-EXEC-20260907-04

- **Raised at:** 2026-09-07T08:31:09Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-03__release-v9.1
- **Step:** STEP 3.1.D (delegated_decision)
- **ST/EPIC item:** ST-35 / EPIC-05
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-35 requires documenting a minimum-interval guideline between scheduled rebalances in `claude/charter/team_charter.md` or `CLAUDE.md` §5, with "Director of HR + Head of Specs Team sign-off." Both target files are outside this routine's write scope: `claude/charter/*` is explicitly prohibited by CLAUDE.md §2 unless explicitly instructed by the relevant prompt; `CLAUDE.md` itself carries a standing write-authority grant to Head of Specs Team specifically (`shared_standards.md` §17), not to Sprint Execution's general write scope.
- **Owning authority:** Head of Specs Team (with Director of HR co-sign per the story's own AC)
- **Unblock criteria:** Head of Specs Team (human, or a session/prompt with explicit `claude/charter/`/`CLAUDE.md` write authority) adds the guideline and obtains Director of HR co-sign.
- **SLA due-by:** 2026-09-08T08:31:09Z (24 hours — Lifecycle/Process Integrity)
- **Blocks execution:** No
- **Disposition:** Open
- **Resolution summary:**

## ESC-EXEC-20260907-04 — Resolution (Addendum)

- **Refers to:** ESC-EXEC-20260907-04 above. This file is append-only — recording the resolution as a new entry rather than editing the original.
- **Resolved at:** 2026-09-07T09:22:00Z (well within the 24h SLA due 2026-09-08T08:31:09Z)
- **Disposition:** Resolved
- **Resolution summary:** Acting as Head of Specs Team + Director of HR (explicit user/Product Owner direction, 2026-09-07): read the full Director of HR §3.1 entry, §5.5/§5.6 conflict rules, and §6 Hard Constraints list in `team_charter.md` before editing, and confirmed `BLG-GOV-207`/`BLG-GOV-216` (the companion technical fixes referenced by this story) had already shipped v7.10 with no outstanding policy piece. Added the scheduled-rebalance cadence guideline to Director of HR's §3.1 entry (no same-day double `run roadmap --reason "scheduled"` invocation absent explicit cause, with the cause-recording path specified) and a corresponding §6 Hard Constraint (item 8) cross-referencing it, making the guideline binding rather than advisory-only prose. Distinguished explicitly from `BLG-GOV-209`'s Skill-Silo Alert workload-composition framing (cross-referenced, not duplicated) per the story's own scope note. `team_charter.md` v1.7→v1.8 (own header + Change Log table; Class 1 canonical charter document per CLAUDE.md §7 Governance Source Hierarchy — confirmed via `git log --all` that no other in-flight branch this cycle touches this file, so no version-collision risk to avoid). Commit `78d69e40` (EPIC-05).
