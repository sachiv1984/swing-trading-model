Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-07

---

## ESC-EXEC-20260907-01

- **Raised at:** 2026-09-07T07:55:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-03__release-v9.1
- **Step:** STEP 3.1.D (delegated_decision)
- **ST/EPIC item:** ST-21 / EPIC-04
- **Trigger type:** Strategy
- **Blocking statement:** ST-21 requires adding a ST-06/BLG-FEAT-90 row to `claude/strategy/strategy_rules.md` §13.5's roster table, referencing the CONDITIONAL §13 clearance review. `claude/strategy/strategy_rules.md` is outside this routine's write scope (execution_prompt.md §7 — "Never modify governance files unless explicitly instructed... `claude/strategy/`" per CLAUDE.md §2). The story's own acceptance criteria explicitly require the edit be made "under Strategy Rules & System Intent Owner authority, in a session/prompt whose write scope explicitly covers `claude/strategy/`" — this routine cannot self-authorise that write.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** Strategy Rules & System Intent Owner (human or a session/prompt with explicit `claude/strategy/` write scope) adds the roster row and confirms CLAUDE.md §6 governance file edit checklist steps 1–4 if `strategy_rules.md`'s version is bumped.
- **SLA due-by:** 2026-09-10T07:55:00Z (72 hours — Strategy boundary)
- **Blocks execution:** No
- **Disposition:** Open
- **Resolution summary:**

## ESC-EXEC-20260907-01 — Resolution (Addendum)

- **Refers to:** ESC-EXEC-20260907-01 above. This file is append-only — recording the resolution as a new entry rather than editing the original.
- **Resolved at:** 2026-09-07T09:02:20Z (well within the 72h SLA due 2026-09-10T07:55:00Z)
- **Disposition:** Resolved
- **Resolution summary:** Acting as Strategy Rules & System Intent Owner (explicit user/Product Owner direction, 2026-09-07): reviewed `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` in full before acting, not a mechanical copy of the pre-drafted backlog text. Added the ST-06/BLG-FEAT-90 row to `strategy_rules.md` §13.5's roster table, explicitly labelled **CONDITIONAL** (9 binding conditions remain in force; the existing roster entries are unlabelled clean PASSes) since this is the highest-condition-count, highest-risk free-text §13 surface reviewed to date — genuinely warranted for the re-attestation cadence, not just a mechanical registration. `strategy_rules.md` v1.6→v1.7 (Class 1 canonical document — versioned via its own header + Change log table; not a Class 6 governance prompt, so no `OPERATIONAL_GUIDE.md`/`prompt_change_log.md` entries required). Commit `5a65aadf` (EPIC-04).

## ESC-EXEC-20260907-02

- **Raised at:** 2026-09-07T07:55:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-03__release-v9.1
- **Step:** STEP 3.1.D (delegated_decision)
- **ST/EPIC item:** ST-26 / EPIC-04
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-26 requires physically creating `claude/roadmap/displacement_debt_register.md` (seeded content per `roadmap_prompt.md` STEP 8) and closing `ESC-EXEC-20260727-02` / `ESC-EXEC-20260818-02`. `claude/roadmap/*` is outside this routine's write scope (execution_prompt.md §7 explicitly excludes `claude/roadmap/*`; the story's own note in `stage4_backlog_slice.md` confirms this: "deferred to this story because `execution_prompt.md`'s write scope does not permit Sprint Execution to write `claude/roadmap/*`"). Carried forward from `ESC-EXEC-20260818-02` (`claude/cycles/2026-08-17__release-v8.9/execution_escalations.md`), still Open/non-blocking as of this cycle.
- **Owning authority:** PMO Lead
- **Unblock criteria:** PMO Lead (or Head of Specs Team, per the story's note) creates the register file with the seeded content from `roadmap_prompt.md` STEP 8, then closes both `ESC-EXEC-20260727-02` and `ESC-EXEC-20260818-02`.
- **SLA due-by:** 2026-09-08T07:55:00Z (24 hours — Lifecycle/Process Integrity)
- **Blocks execution:** No
- **Disposition:** Open
- **Resolution summary:**

## ESC-EXEC-20260907-02 — Resolution (Addendum)

- **Refers to:** ESC-EXEC-20260907-02 above. This file is append-only — recording the resolution as a new entry rather than editing the original.
- **Resolved at:** 2026-09-07T09:04:10Z (well within the 24h SLA due 2026-09-08T07:55:00Z)
- **Disposition:** Resolved
- **Resolution summary:** Acting as PMO Lead / Head of Specs Team (explicit user/Product Owner direction, 2026-09-07): created `claude/roadmap/displacement_debt_register.md` using the exact format and seed content designed at `claude/cycles/2026-07-27__release-v7.9/qa_evidence_EPIC-14.md` (ST-14, EPIC-14, BLG-GOV-258) — verbatim, not re-derived. Confirmed currency before creating: no roadmap-level STEP 8 displacement candidate has been flagged since that design was written (2026-07-27) through today — the seed content (4.1c, CHART-IX) is still the complete, current history. `roadmap_prompt.md` STEP 8's write instruction was already wired at `2026-08-17__release-v8.9` (ST-21, EPIC-06, BLG-GOV-264) — this completes the remaining half of that two-part handoff. Created directly per explicit user direction rather than via a full `run roadmap` invocation — a targeted action using already-designed, already-reviewed content, not a substitute for that routine's own STEP 8 write path going forward, which remains the authoritative future maintainer of this file. This resolution also supersedes, without touching, the sealed `ESC-EXEC-20260727-02` (`claude/cycles/2026-07-27__release-v7.9/execution_escalations.md`) and `ESC-EXEC-20260818-02` (`claude/cycles/2026-08-17__release-v8.9/execution_escalations.md`) — both cycles are closed/sealed and cannot be edited (CLAUDE.md "never modify sealed artefacts"); this is now the live, terminal resolution for the whole chain. Commit `c2db66df` (EPIC-04).

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
- **Resolution summary:** Acting as Strategy Rules & System Intent Owner (explicit user/Product Owner direction, 2026-09-07): read §4.1 (Position Sizing Calculator canonical rules), §5 (Initial stop calculation), and §11 (current production parameters, `InitialATRMultiplier = 5`) in full before writing the example, rather than inventing figures independently. Added new §4.1.8 to `strategy_rules.md` — a worked numerical example showing how a low-ATR (low-volatility) instrument can produce a small `StopDistance` and therefore a large, still-valid `SuggestedShares`, whose cost is then correctly caught by the existing §4.1.6 cash-constraint gate (`INSUFFICIENT_CASH`) rather than any sizing-validity rule. Confirmed documentation-only: no calculation, validity, or gating rule was added, changed, or reinterpreted — the example only makes an existing interaction between already-canonical rules explicit. `strategy_rules.md` v1.6→v1.8 (Class 1 canonical document — versioned via its own header + Change log table; not a Class 6 governance prompt, so no `OPERATIONAL_GUIDE.md`/`prompt_change_log.md` entries required). Version chosen as 1.8, not 1.7, to avoid a collision with EPIC-04's independently in-flight (not yet merged) 1.6→1.7 bump (ST-21, commit `5a65aadf`) — same precedent as `OPERATIONAL_GUIDE.md` v4.174 and `BLG-QA-159` earlier this cycle. Commit `59385f3c` (EPIC-05). **Cross-branch collision confirmed clear at merge (CLAUDE.md §8 step 2a):** EPIC-04's own bump to this file landed at v1.7 (ESC-EXEC-20260907-01 above) — the two changes do not share a version number; both changelog rows retained in `strategy_rules.md`'s Change log table (v1.8 on top, v1.7 beneath) at this merge.

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
