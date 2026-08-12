# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-08-12 (Sprint Execution Engine, acting as Head of Engineering, ST-03/EPIC-02/v8.6 agent-mediated review finding — 1 new item added: BLG-BE-96, staging verification + legacy orphaned-row audit for ST-03's trade-plan-linkage enforcement); prior — 2026-08-11 (Sprint Execution Engine, ST-02/EPIC-01/v8.6 mid-sprint finding — 1 new item added: BLG-BE-95, persist isAiDraft flag on trade_plans for AI-origin display badges); prior — 2026-08-11 (PMO Lead, acting on the `2026-08-11__release-v8.6` design gate's ST-07/BLG-FE-150 recommendation — 1 new item added: BLG-FE-156, convert 4 hardcoded dark-only modals to theme-aware tokens); prior history retained — see prior entries in version control.
**Last rebalance:** 2026-07-12 (cycle 2026-07-12__scheduled — DL-064; 36 new backlog items added (BLG-GOV-203–217, BLG-QA-94–99/101–103, BLG-BE-57/58, BLG-FE-103–105, BLG-SEC-17, BLG-SPEC-78–82, BLG-OPS-106/107) via idea intake IW-20260712-01 (44 submissions, 22 agents) disposition: 36 Promoted-Backlog, 7 Rejected (all resolved by direct action), 1 Promoted-Added (process patch), 2 Parked; 0 active initiatives, CPS=N/A; STEP 2.4 Product Value Ratio 0.21 (U=8 G=9 D=21 P=0, window v6.5–v6.9) — 🔴 3rd consecutive Product Value Alert, improved from prior 0.18 but still below 0.30 floor; mandatory pull-forward named BLG-FE-102 as anchor candidate for next `plan release`, BLG-FE-97 secondary; SI-02 gate live re-checked via production API — NOT MET (0/11 linked trade plans; behavioural-drift endpoint self-reports insufficient_data); STEP 7.1 Skill-Silo rolling-3-cycle avg 76.9% (v6.7/v6.8/v6.9) — Alert persists but improved from 78.2%; STEP 8.1 empty horizon gate: Option (b) — defer, scoping deferred to next `plan release`; Backlog Accessibility Warning RE-TRIGGERED (A=19.9%, down from 38.8%); prior — 2026-07-10 (cycle 2026-07-10__scheduled — DL-063; 39 new backlog items added (BLG-GOV-191–202, BLG-QA-87–93, BLG-OPS-101–105, BLG-SEC-14–16, BLG-BE-53–56, BLG-SPEC-74–77, BLG-FE-99–101, BLG-FEAT-72) via idea intake IW-20260710-01 (44 submissions, 22 agents) disposition: 39 Promoted-Backlog, 3 Parked-cycle-1, 2 Rejected; 0 active initiatives, CPS=N/A; STEP 2.4 Product Value Ratio 0.18 (U=9 G=16 D=24 P=0, window v6.4–v6.8) — 🔴 2nd consecutive Product Value Alert, worse than prior 0.26; mandatory pull-forward named BLG-FEAT-64 as anchor candidate for `plan release v6.9`; STEP 7.1 Skill-Silo rolling-3-cycle avg 78.2% (v6.6/v6.7/v6.8) — Alert persists, single-reading worsening after 2 consecutive improvements; STEP 8.1 empty horizon gate: Option (b) — defer, v6.9 scoping deferred to `plan release v6.9`; prior — 2026-07-02 (cycle 2026-07-02__scheduled — DL-059; 24 new backlog items added (BLG-FEAT-55–60, BLG-FE-81–84, BLG-BE-41/42, BLG-GOV-154/156, BLG-QA-69/70/71, BLG-SEC-09, BLG-SPEC-62/63/65/66, BLG-OPS-84/85) via idea intake IW-20260702-01 (44 submissions) + 19 carried ideas at 3-cycle hard cap; STEP 8.0: 0 fast-track items this cycle; STEP 3.1 Actionable Backlog Assessment: A=35/28%, T=7/6%, D=27/22%, L=55/44% of 124 baseline items — Backlog Accessibility Warning triggered (A% below 30% floor); PVR=0.344 Advisory; Skill-Silo rolling-3-cycle avg=64.8% Alert, worse than prior 53.2% (pull-forward candidate BLG-FE-46)))

> ⚠️ Standing Notice
> This backlog records prioritisation and intent only.
> All formulas, schemas, API contracts, and behavioural rules are indicative until
> confirmed in the relevant canonical specifications.
> No item may proceed to implementation without canonical owner sign-off.

> 📋 Placement Rule
> New items must be appended to the correct existing type section (§1–§8). Do not create new numbered session sections. The backlog is organised by type, not by session date.
> **Ephemeral sections** (Release Slice tables, Test Scenario Gap sections, and "Returned to Backlog" sections appended by governance engines) are temporary. They must be removed during the next `groom backlog` run after the cycle closes. Any still-open items within them must be promoted to the appropriate §1–§8 type section before the ephemeral section is removed.

*Completed and killed items are recorded in `claude/backlog/backlog_archive.md`.*

---

## Priority Definitions

- **P0 — Critical**: Blocks correctness, trust, or release safety
- **P1 — High**: Enables core workflows or governance
- **P2 — Medium**: High leverage but not blocking
- **P3 — Low**: Nice-to-have or future scale

---

## 1. Platform & Validation Governance Backlog

### BLG-GOV-242 — Quarterly model/prompt-drift compliance attestation log
**Priority:** P3 (Low) | **Type:** Governance / AI Compliance | **Owner:** AI Compliance & Governance Officer | **Source:** IDEA-ai-compliance-20260717-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `BLG-GOV-239` tracks the model deprecation calendar, but there is no recurring attestation record confirming the pinned model/prompt behaviour hasn't silently drifted between quarters.
**Scope:** Add a lightweight quarterly attestation log (pinned model version, last prompt-template review date, any observed drift) as a companion to `BLG-GOV-239`'s deprecation calendar.
**Acceptance Criteria:** Attestation log document created; first entry filed.

---

### BLG-GOV-244 — Deprecation header convention for retiring API endpoints
**Priority:** P3 (Low) | **Type:** Governance / API Process | **Owner:** API Contracts & Documentation Owner | **Source:** IDEA-api-contracts-20260717-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The system has never formally retired a shipped API endpoint, so there is no documented convention for how a deprecation should be communicated in `openapi.yaml`/contract docs before removal.
**Scope:** Document a lightweight deprecation-header convention (e.g. `**Deprecated:** vX.Y, removal target vX.Z`) for future use in `docs/specs/api_contracts/`.
**Acceptance Criteria:** Convention documented; referenced from `shared_standards.md` or an equivalent canonical location.

---

### BLG-GOV-245 — Formal expiry review for §13-adjacent initiatives open more than 2 cycles
**Priority:** P3 (Low) | **Type:** Governance Process | **Owner:** Challenger; Strategy Rules & System Intent Owner | **Source:** IDEA-challenger-20260717-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `roadmap_prompt.md` STEP 2.1 requires Score-4/5 initiatives to get heightened Challenger scrutiny at debate time, but there is no recurring check that a Score-4/5 item still open after 2+ cycles gets re-reviewed rather than just re-carried.
**Scope:** Add an advisory check to STEP 2 that flags any Score-4/5 initiative open more than 2 consecutive cycles for explicit Challenger re-review, rather than silent carry-forward.
**Acceptance Criteria:** Check specified; would have fired correctly against at least one historical example if run retroactively (or confirmed no qualifying example exists).

---

### BLG-GOV-247 — Formalise condensed-tier trigger thresholds beyond the "no new FTE required" test
**Priority:** P3 (Low) | **Type:** Governance Process | **Owner:** FinOps & Resource Architect | **Source:** IDEA-finops-20260717-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `roadmap_prompt.md` STEP 0.C's Lightweight-tier workforce economics condensing rule ("Condensed if no new FTE required") has never actually fired in this backlog-driven, solo-developer context (0 active initiatives, no FTE concept in practice) — the criterion may not be a meaningful discriminator here.
**Scope:** Review whether STEP 0.C's condensed-tier language should be reworded for a solo-developer/story-count context, analogous to how `roadmap_prompt.md §7.1` already substitutes story-count for FTE-hours.
**Acceptance Criteria:** Review completed; either a specific prompt change proposed, or an explicit decision recorded that the existing language is fine as-is.

---

### BLG-GOV-287 — stage4_backlog_slice.md post-gate-correction addendum mechanism
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** Found during Sprint Planning, `2026-08-05__release-v8.3` (ST-11 / `BLG-FE-103` stale-slice-text discrepancy — see `claude/cycles/2026-08-05__release-v8.3/sprint_planning_notes.md §Stale Backlog Slice Text (ST-11)`) — 2026-08-05
**Effort:** S (~1 day)
**Provisional-Target:** TBD

**Problem**
When a design-gate escalation changes an item's scope/AC/effort after the cycle's `stage4_backlog_slice.md` is sealed (e.g. `ESC-20260805-01` / `BLG-FE-103` at cycle `2026-08-05__release-v8.3`), the correction lands in `claude/backlog/backlog.md` and `design_gate.md` but `stage4_backlog_slice.md` — the document Sprint Planning is told to treat as source-of-truth for acceptance criteria — has no mechanism to receive it, since it is sealed and Release-Planning-owned. Sprint Planning had to manually reconstruct the correction from `backlog.md` + `design_gate.md` + `escalations.md` and document the discrepancy inline rather than reading a single authoritative source.

**Scope**
- Propose that `design_gate_prompt.md` append a `## Post-Gate Corrections` addendum section to the cycle's `stage4_backlog_slice.md` (additive only, not a mutation of sealed content) whenever a gate-blocking escalation changes an item's AC/effort/scope
- Apply the standard governance file edit checklist (version bump, `OPERATIONAL_GUIDE.md` §14 sync, `prompt_change_log.md` entry) per `CLAUDE.md` §6

**Acceptance Criteria**
- `design_gate_prompt.md` patched with the addendum mechanism
- Head of Specs Team sign-off

---

### BLG-GOV-290 — CLAUDE.md §8 has no rule for a shared JSON field's schema shape drifting mid-sprint between sibling EPIC branches
**Priority:** P2 (Medium) | **Type:** Governance Process | **Owner:** Head of Specs Team | **Source:** ST-30 (EPIC-07), dry-run of the cross-EPIC merge conflict runbook — 2026-08-08 | **Effort:** S | **Provisional-Target:** TBD

**Problem**
The same dry-run (`docs/ops/cross_epic_merge_runbook_dry_run_2026-08-08.md`) found `execution_state.json`'s `open_escalations` field had diverged in *shape*, not just content, between two sibling EPIC branches active in the same sprint — one branch reshaped it from a `list` of strings to a `dict` of `{ESC-ID: status}` mid-session, while the sibling branch (which had already forked from the pre-reshape state) kept the original `list` shape. `git merge` reports this as an ordinary content conflict, but resolving it correctly requires reconciling a schema, not just picking a value — and `CLAUDE.md` §8 has no guidance for this class of conflict at all.

**Scope**
- Add a rule to `CLAUDE.md` §8 (or `shared_standards.md` §16.13's `execution_state.json` schema note) covering one of: (a) require any mid-sprint schema-shape change to a shared JSON field to be applied uniformly across all sibling EPIC branches active that sprint, not just the branch making the change; or (b) prohibit shape changes to already-initialised shared fields mid-sprint entirely, deferring the shape change to the next cycle's STEP 0
- Apply the standard governance file edit checklist (version bump, `OPERATIONAL_GUIDE.md` §14 sync, `prompt_change_log.md` entry) per `CLAUDE.md` §6

**Acceptance Criteria**
- `CLAUDE.md` §8 (or `shared_standards.md` §16.13) covers mid-sprint schema-shape drift on shared JSON fields
- Head of Specs Team sign-off

---

### BLG-GOV-291 — CLAUDE.md §8's own commit message template violates the enforced commit-format hook
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Sprint execution 2026-08-07__release-v8.4, EPIC-06/EPIC-07 real cross-EPIC merge conflict resolution — 2026-08-08
**Effort:** XS (<1 day)
**Provisional-Target:** TBD

**Problem**
`CLAUDE.md` §8 step 4 instructs: `git commit -m "[EPIC-xx] Merge main (<description>) into EPIC-xx — conflict resolution"`. This format was rejected live by the repo's own pre-commit hook when followed exactly during EPIC-06/EPIC-07's real conflict resolution this cycle — the hook requires `[EPIC-xx][ST-xx]` or `[GOVERNANCE]`, and a bare `[EPIC-xx]` with no `ST-xx` fails. Worked around by using `[GOVERNANCE]` instead, which the hook does accept and is arguably the more semantically correct prefix for a conflict-resolution commit anyway (it's not attributable to a single story). `CLAUDE.md` §8's own worked example (`sprint_planning_prompt.md v3.13/v3.14`) predates this discovery, so the mismatch has been silently present in the documented runbook.

**Scope**
- Correct `CLAUDE.md` §8 step 4's commit message template to `[GOVERNANCE] Merge main (<description>) into EPIC-xx — conflict resolution` (or add `[ST-xx]` guidance for cases where the conflict resolution is attributable to a specific story)
- Apply the standard governance file edit checklist per `CLAUDE.md` §6 (n/a for `CLAUDE.md` itself, which has no version field — log in `prompt_change_log.md` per the established no-version-field convention)

**Acceptance Criteria**
- `CLAUDE.md` §8's commit message template matches what the enforced pre-commit hook actually accepts
- Head of Specs Team sign-off

---

### BLG-GOV-292 — Extend scan_backlog_gate_conditions.py to catch bracket-delimited embedded gate language
**Priority:** P3 (Low)
**Type:** Governance / Process Integrity
**Owner:** Head of Specs Team
**Source:** Release planning `2026-08-08__release-v8.5`, STEP 1.3a self-caught finding — 2026-08-08
**Effort:** XS (<1 day)
**Provisional-Target:** ✅ COMPLETE — 2026-08-11 — Head of Specs Team direct action, resolving the 72-hour escalation from post-ship closure `2026-08-08__release-v8.5` §5/§6 (closure_record.md item 1)

**Problem**
`scripts/scan_backlog_gate_conditions.py`'s `EMBEDDED_GATE_SIGNAL_RE` data-quality-warning check (added `BLG-GOV-286`, shipped `v8.4` ST-29) only matches gate-like language inside **parentheses** within a `Provisional-Target` field. `BLG-FEAT-73`'s `Provisional-Target` carries unmet-gate language (`` `[gate status unverified/unmet]` ``) inside **square brackets** — neither a formal `Gate criteria`/`Gate`/`Gate date` field nor the parenthesis-only warning regex catches it, so the script's output alone treats it as ready/ungated. Caught only by a manual full-text read during `v8.5` release planning. This is a 5th distinct failure mode in the same gate-detection problem class `BLG-GOV-286` was filed against (which covered 4 other named modes).

**Scope**
- Extend `EMBEDDED_GATE_SIGNAL_RE` (or add a sibling pattern) to also match bracket-delimited gate language, e.g. `\[.*(gate|gated|no earlier than|conditional|pending|unmet|unverified).*\]`
- Re-run the script against the live `backlog.md` to confirm `BLG-FEAT-73` (and any other bracket-delimited instances) now surface as a data-quality warning
- Apply the standard governance file edit checklist (version bump, `OPERATIONAL_GUIDE.md` §14 sync, `prompt_change_log.md` entry) per `CLAUDE.md` §6 if the change touches `release_planning_prompt.md`'s own documented script behaviour description

**Acceptance Criteria**
- `scan_backlog_gate_conditions.py` flags `BLG-FEAT-73` (or its then-current equivalent) as a data-quality warning
- Existing parenthesis-delimited detection unaffected (no regression against the 5 previously-known warning instances)
- Head of Specs Team sign-off

---

### BLG-GOV-293 — .claude_current_state.json prior_cycle field has no owning engine, found stale
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Release planning `2026-08-08__release-v8.5`, self-caught while syncing root state pointer — 2026-08-08
**Effort:** XS (<1 day)
**Provisional-Target:** TBD

**Problem**
`.claude_current_state.json`'s `prior_cycle` field was found stale at the start of `v8.5` release planning: it read `2026-08-05__release-v8.3` when it should have read `2026-08-07__release-v8.4` (the cycle that closed immediately before `v8.5` opened; `last_post_ship_cycle` correctly showed `2026-08-07__release-v8.4`). No engine's documented write list explicitly owns updating `prior_cycle` after a cycle closes — this mirrors the OA-1 `next_release` ownership gap that `release_planning_prompt.md` STEP 9 was created to close (post-ship closure `2026-07-24__release-v7.8`). Left uncorrected in-place during `v8.5` planning (outside Release Planning's documented write scope for this field) — see `run_manifest.md §STEP -1.5`/`.claude_current_state.json`'s own inline note for this cycle.

**Scope**
- Identify the correct owning engine for `prior_cycle` (candidates: Post-Ship Closure STEP 8/9, or Release Planning STEP 9 alongside its existing `next_release`/`active_cycle` writes)
- Add an explicit, unconditional write of `prior_cycle` at that engine's terminal step, following the `next_release` (OA-1) precedent
- Apply the standard governance file edit checklist per `CLAUDE.md` §6

**Acceptance Criteria**
- `prior_cycle` is written unconditionally by exactly one engine's terminal step, documented as that field's authoritative owner
- Confirmed correct at the next cycle transition (reads the cycle that closed immediately prior, not an older one)
- Head of Specs Team sign-off

---

### BLG-GOV-294 — File retroactive DEV record for the dark-mode/Radix-portal Layout.js fix

**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Agent-mediated PR review (Product Owner role), PR #1327, 2026-08-08__release-v8.5 — 2026-08-10
**Effort:** XS (<1h)
**Provisional-Target:** v8.6

**Problem**
A significant, app-wide production bug (Dialog/Radix-portal components rendering in light-theme CSS scope regardless of the user's actual theme setting, affecting 14+ consumers) was discovered and fixed mid-PR during EPIC-03/ST-06, but no formal `DEV-*` deviation record was ever filed for it — only narrative disclosure in `qa_evidence_EPIC-03.md`. This same PR's own convention elsewhere (`DEV-REPORTS-ST01-02` for ST-08) shows a formal record is the norm for this class of finding, and the accountability trail is currently inconsistent within one cycle.

**Scope**
- File a retroactive `DEV-*` record documenting the dark-mode/Radix-portal fix (root cause, fix applied, verification) per `document_lifecycle_guide.md` §9

**Acceptance Criteria**
- A `DEV-*` record exists for the `src/Layout.js` dark-mode/Radix-portal fix, matching the format already used for `DEV-REPORTS-ST01-02` in the same cycle

---

### BLG-GOV-295 — shared_standards_changelog.md missing v3.27 entry (companion changelog rule violation)

**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Agent-mediated PR review (Director of Quality role), PR #1329, 2026-08-08__release-v8.5 — 2026-08-10
**Effort:** XS (<1h)
**Provisional-Target:** v8.6

**Problem**
`shared_standards.md` was bumped v3.26→v3.27 (new §20, ST-04/EPIC-02) but its companion `claude/system/changelogs/shared_standards_changelog.md` was not updated in the same commit, violating `shared_standards.md` §11's own "Companion per-file changelog rule" — the exact failure mode that rule was written to prevent (per its own v3.17 entry citing an identical `roadmap_prompt_changelog.md` drift as precedent).

**Scope**
- Append the missing v3.27 entry to `claude/system/changelogs/shared_standards_changelog.md`

**Acceptance Criteria**
- `shared_standards_changelog.md`'s top row matches `shared_standards.md`'s current version (v3.27, §20 addition)

---

### BLG-GOV-296 — execution_state.json's deviations_filed field is used as "check performed" not literally "filed"

**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Agent-mediated PR review (Director of Quality role), PR #1330, 2026-08-08__release-v8.5 — 2026-08-10
**Effort:** M (~1-2 days — cross-cutting, touches schema + shared_standards.md + likely multiple prior cycles' records)
**Provisional-Target:** v8.6

**Problem**
Every "done" story in cycle `2026-08-08__release-v8.5`'s `execution_state.json` (and, on inspection, every prior cycle's own file) has `deviations_filed: true` regardless of whether an actual `DEV-*` record exists for that story — the field is being used repo-wide as a "deviation-check-performed" flag rather than literally "a deviation was filed." This directly contradicts `qa_evidence_EPIC-05.md`'s own text ("Known deviations filed: None" for every row in that EPIC) and is systemic across every EPIC this cycle, not an isolated slip.

**Scope**
- Decide: either rename/reinterpret the field's documented meaning in `execution_state_schema.json`/`shared_standards.md` to match actual usage ("deviation check performed"), or split it into two distinct fields (`deviation_check_performed`, `deviation_filed`)
- Update `execution_prompt.md` STEP 3.1.A step 10/10a wording to match whichever resolution is chosen

**Acceptance Criteria**
- `execution_state_schema.json` and `shared_standards.md` document the field's actual, current meaning without contradiction
- No qa_evidence log can simultaneously say "deviations filed: None" while every story's `deviations_filed` reads `true`, going forward
- Head of Specs Team sign-off

---

### BLG-GOV-297 — Annotate BLG-FE-146/BLG-FE-139 with 2026-08-10 trigger-condition re-check

**Priority:** P4 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Agent-mediated PR review (Director of Quality role), PR #1330, 2026-08-08__release-v8.5 — 2026-08-10
**Effort:** XS (<1h)
**Provisional-Target:** v8.6

**Problem**
`BLG-FE-146` (ST-19's source) and `BLG-FE-139` (ST-20's source) were re-checked during `2026-08-08__release-v8.5` and confirmed their trigger condition (a `ChartContainer`/`ui/calendar.js` consumer) is still unmet, but neither backlog item was annotated in `backlog.md` with that re-check date. A future sprint scoping a chart/calendar consumer won't see "re-checked 2026-08-10" without opening this cycle's story doc specifically.

**Scope**
- Add a one-line "re-checked 2026-08-10, still unmet" note to both `BLG-FE-146` and `BLG-FE-139`

**Acceptance Criteria**
- Both items carry the 2026-08-10 re-check confirmation inline

---

### BLG-GOV-298 — Correct BLG-GOV-288's Acceptance Criteria text (says STEP 0, actual fix is STEP 7)

**Priority:** P4 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Agent-mediated PR review (Product Owner role), PR #1331, 2026-08-08__release-v8.5 — 2026-08-10
**Effort:** XS (<1h)
**Provisional-Target:** v8.6

**Problem**
`BLG-GOV-288`'s Acceptance Criteria text says `release_planning_prompt.md` STEP 0 should be patched to reset `sprint_sealed: false`, but STEP 0 never touches the root `.claude_current_state.json` (only cycle-level `state.json`) — the actual, correct fix landed at STEP 7 (matching the existing `design_gate_status` single-write-site pattern), with STEP 0 gaining only a cross-reference note. The backlog item's own problem narrative was factually wrong about where `design_gate_status` resets, so the AC inherited that error. The fix itself is confirmed correct and intent-complete — only the AC's own wording is stale.

**Scope**
- Correct `BLG-GOV-288`'s Acceptance Criteria text to say "STEP 7" (with a one-line note on why)

**Acceptance Criteria**
- `BLG-GOV-288`'s AC text matches the actual, correct implementation site (STEP 7)

---

## 2. Product Feature Backlog (User-Facing)

---

### BLG-FEAT-26 — ATR position-sizing retrospective analysis
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner
**Source:** IDEA-metrics-analytics-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped and live for ≥ 30 days; sufficient attributed closed trades to support retrospective.

**Problem**
There is no retrospective view of whether ATR-based position sizing (risked R per trade) was consistent over time, or whether deviation from the ATR sizing formula correlated with outcome. Understanding sizing discipline and its P&L impact requires a dedicated analytics view built on historical trade data.

**Scope**
- Retrospective dashboard: actual position size vs ATR-recommended size per trade
- Correlation view: sizing deviation vs R-multiple outcome
- Summary metric: sizing discipline score over rolling window

**Acceptance Criteria**
- ATR-sizing deviation visible per trade and in aggregate
- Correlation between sizing deviation and R-multiple summarised
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-30 — Screener-to-trade attribution pipeline & retrospective analytics (consolidated)
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner
**Source:** IDEA-metrics-analytics-20260421-05 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032); consolidates BLG-FEAT-27 (retrospective quality/win-rate analysis) and BLG-FEAT-28 (hit-rate metric) — both are reporting views over the same attribution linkage this item builds; filed together in the same 2026-04-21 idea batch but scoped as if independently buildable, when in practice all three need the same underlying instrumentation — merged 2026-07-27, session duplicate-consolidation cleanup
**Effort:** L (~3–4 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** Screener live ≥ 60 days AND ≥ 60 closed trades with screener attribution (the more demanding of the original gate conditions — the merged retrospective/quality-correlation scope needs both).

**Problem**
The full pipeline from screener hit → watchlist add → research → trade plan → execution → close is not yet instrumented end-to-end. Attribution gaps prevent retrospective analysis of conversion rates at each stage, make it impossible to evaluate whether the screener generates genuinely high-quality candidates vs high-volume noise, and leave no aggregate hit-rate metric available — all needs originally filed as three separate items requiring the same underlying linkage.

**Scope**
- Full attribution model: screener_run_id linkage through to trade close
- Conversion funnel: screener → watchlist → plan → closed
- Aggregate hit-rate metric: screener_candidates_total, advanced_to_watchlist, advanced_to_trade_plan, advanced_to_closed_trade — displayable in governance/operations reporting view
- Retrospective metric: screener hit rate and win rate of attributed trades vs baseline, filterable by screener run date range
- Exportable for offline analysis

**Acceptance Criteria**
- Full attribution pipeline implemented; conversion funnel metrics computable
- Hit-rate metric computed and displayable
- Screener hit rate and attributed-trade win rate reportable, filterable by date range
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-31 — Research-to-trade conversion rate metric
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner
**Source:** IDEA-metrics-analytics-20260421-06 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-02 (Research View) live ≥ 30 days AND ≥ 30 research sessions with attribution.

**Problem**
No metric tracks how often a research session (opening the research view for a ticker) results in a trade plan creation. This conversion rate is an indicator of research quality and operator decision confidence. Requires 30 days of research session history with attribution.

**Scope**
- Metric: research_sessions_total, sessions_leading_to_plan, sessions_leading_to_closed_trade
- Attribution requires `session_id` or equivalent linkage from research view to trade plan

**Acceptance Criteria**
- Research-to-trade conversion rate computable
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-32 — Trade plan completion rate tracking
**Priority:** P2 (Medium) — escalated from P3, 2026-08-11, roadmap rebalance (see note below)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner
**Source:** IDEA-metrics-analytics-20260421-07 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

> ⚠️ **Priority escalation + gate cleared (2026-08-11, roadmap rebalance STEP 7.1, DL-078):** Gate condition ("PT-04 shipped") confirmed met — PT-04 shipped v6.1 (2026-06-23). Named as the lead Skill-Silo mandatory-pull-forward candidate for the next `plan release` — the only ungated, build-and-ship-shaped U-item found in the entire backlog this cycle (see `cycle_record.md` STEP 7.1 for the full candidate search). Priority raised P3→P2 in recognition of this.

**Gate criteria:** ~~PT-04 (Setup Quality Score) shipped.~~ Cleared 2026-08-11 (see note above) — item is now Actionable-now (A-category).

**Problem**
No metric tracks what proportion of created trade plans are completed (i.e., result in a closed trade) vs abandoned. The completion rate is a key indicator of plan quality, operator follow-through, and whether PT-04 quality scores correlate with plan execution. Requires PT-04 to create the quality score baseline for correlation.

**Scope**
- Metric: plans_created, plans_completed (closed trade), plans_abandoned, completion_rate
- Optional: completion rate segmented by setup quality score tier

**Acceptance Criteria**
- Trade plan completion rate computable and displayable
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-33 — Trade plan approval workflow
**Priority:** P3 (Low)
**Type:** Product Feature / Workflow
**Owner:** Product Owner; Head of UX & Design
**Source:** IDEA-trade-plan-20260508-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** L (~3–4 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-05 (Trade Plan feature set) live ≥ 3 months with ≥ 20 plans created; operator confirms approval workflow adds value.

**Problem**
Trade plans are currently created and immediately actionable without a formal review or approval step. As plan complexity grows (multi-day setup, multi-leg risk), an explicit approval checkpoint may improve discipline — but the value of an approval workflow vs friction cost is not yet established. Gate ensures sufficient usage history before committing implementation effort.

**Scope**
- Approval state: Draft → Pending Approval → Approved / Rejected
- Approval action: operator-controlled (self-approval supported for solo use)
- Approved plans visible separately from drafts

**Acceptance Criteria**
- Approval workflow implemented and functional
- Plan state transitions correct and persisted
- Gate condition and usage volume verified by Product Owner before sprint planning

---

### BLG-FEAT-34 — Trade plan P&L attribution
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner; Financial Reporting & Records Owner
**Source:** IDEA-trade-plan-20260508-02 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** `plan_id` linkage live on closed trades (PT-05 shipped and plans actively used).

**Problem**
Closed trade P&L cannot currently be attributed back to the trade plan that governed the entry. Without `plan_id` on position records, it is impossible to compare planned R-risk vs realised R-multiple or evaluate whether adhering to a plan improved outcomes vs discretionary deviation.

**Scope**
- Link `plan_id` from trade plan to position/trade close record
- Attribution report: planned_risk_R vs realised_R per attributed trade
- Aggregate: plan-adhered trades vs plan-deviated trades outcome comparison

**Acceptance Criteria**
- `plan_id` linkage implemented on closed trades
- Attribution report computable
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-35 — Entry zone discipline reporting
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner
**Source:** IDEA-trade-plan-20260508-03 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** ≥ 20 closed trades with linked trade plans AND `entry_delta_pct` field captured on closed trades.

**Problem**
No metric tracks whether entries were executed within the planned entry zone. `entry_delta_pct` (actual entry vs planned entry midpoint) is a candidate field but is not yet captured at trade close. Without this data, it is impossible to assess entry zone discipline or its correlation with trade outcome.

**Scope**
- Capture `entry_delta_pct` on trade close: actual_entry_price vs planned_entry_zone midpoint
- Discipline metric: % of trades entering within planned zone
- Correlation: entry discipline vs R-multiple outcome

**Acceptance Criteria**
- `entry_delta_pct` captured on trade close where plan linkage exists
- Entry discipline metric computable and displayable
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FEAT-44 — Arc 5 compliance score utility advisory at low trade volume
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Product Feature / UX Advisory
**Owner:** Metrics Definitions & Analytics Owner; Head of UX & Design
**Source:** IDEA-metrics-analytics-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Arc5ComplianceSection live 3+ months post-v4.1 ship (~Aug 2026). Minimum usage period needed to assess whether low-volume score values are misinterpreted in practice.

**Problem**
The Arc 5 composite compliance score (shipped v4.1) is computed from fewer than 20 closed trades. At low sample volumes, the score may represent statistical noise rather than actionable signal. Without a "minimum data" advisory in the UI, users may over-interpret early values.

**Scope**
- Assess whether compliance scores at <20 trades are statistically meaningful
- If noise at low volume: add a "Minimum trade history required (< 20 trades)" advisory near the score display
- Gate condition verification by Metrics Definitions & Analytics Owner before sprint planning

**Acceptance Criteria**
- Assessment document produced (advisory or advisory-not-needed conclusion)
- If advisory warranted: UI advisory added to Arc5ComplianceSection for sub-20-trade states
- Gate condition verified before sprint planning

---

### BLG-FEAT-55 — AI chat conversation history persistence across sessions
**Priority:** P3 (Low)
**Type:** Product Feature / AI
**Owner:** Product Owner; Data Model & Domain Schema Owner
**Source:** IDEA-product-owner-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** ≥30 days of AI chat usage (v6.2 shipped 2026-06-25; clears ~2026-07-25) AND a §13 review opened and passed for persistence design (chat is currently stateless per SRB-v1.7).

**Problem**
POST /ai/chat (shipped v6.2) is stateless — no conversation history persists across sessions. Users who want to continue a prior chat thread cannot. Persisting history is a genuine schema and §13 boundary question (stored AI conversation content) that should not be designed ahead of both an established usage pattern and a formal boundary review.

**Scope**
- §13 review: does persisting chat history change SRB-v1.7's stateless-advisory classification?
- Schema design: chat session/message data model (companion to BLG-SPEC-65/66)
- Frontend: session list, resume-conversation UX

**Acceptance Criteria**
- §13 review passed before design begins
- Chat session schema designed and reviewed by Data Model & Domain Schema Owner
- Gate condition (30 days usage) verified by Product Owner before sprint planning

---

### BLG-FEAT-56 — AI-assisted setup thesis digest at order placement
**Priority:** P1 (High) — escalated from P3, 2026-07-27, session product review (see note below)
> ⚠️ **Priority escalation (2026-07-27):** Raised P3→P1 during a session backlog review — flagged as high-value user-facing decision support (surfaces existing AI thesis infra at the order-placement moment). Escalation reflects value judgment only; the gate criteria below are unchanged and still govern when this may enter sprint planning.
**Type:** Product Feature / AI
**Owner:** Product Owner
**Source:** IDEA-product-owner-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** AI adoption window clears ~2026-07-25 AND existing AI touchpoints (daily briefing, chat) show established, validated usage patterns.

**Problem**
The AI thesis generation button (v4.0) populates `setup_thesis` on demand. Adding a further AI touchpoint — an automatic digest surfaced at order placement — before existing AI features are validated risks layering unvalidated AI surface area on top of unvalidated AI surface area.

**Scope**
- Digest content: setup thesis + key risk factors summarised at the order-placement step
- Reuses existing Claude thesis generation infrastructure (v4.0)
- Gated behind confirmed adoption of the existing AI touchpoints

**Acceptance Criteria**
- Digest renders at order placement using existing thesis generation service
- Gate condition (adoption validated) verified by Product Owner before sprint planning

---

### BLG-FEAT-57 — Strategy parameter sensitivity analysis framework
**Priority:** P3 (Low)
**Type:** Product Feature / Strategy Analytics
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** L (~3–4 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** ≥20 closed trades (currently ~15–17) AND Arc 5/6 tooling prerequisite in place.

**Problem**
There is no systematic pre-process to evaluate the effect of a §11 strategy parameter change (e.g. ATR multiplier) against historical trade data before committing to a version bump. Building this ahead of sufficient trade density or the Arc 5/6 analytical foundation would produce statistically unreliable output.

**Scope**
- Sensitivity analysis: apply candidate parameter values against historical trade set, compare outcome deltas
- Feeds into SI-04 (Strategy Version Comparison) as a pre-change evaluation step

**Acceptance Criteria**
- Framework produces before/after outcome comparison for a candidate parameter change
- Gate condition (≥20 closed trades) verified by Strategy Rules & System Intent Owner before sprint planning

---

### BLG-FEAT-58 — Trade annotation model
**Priority:** P3 (Low)
**Type:** Product Feature / Data Model
**Owner:** Data Model & Domain Schema Owner
**Source:** IDEA-data-model-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** Arc 4 PO-02 (Journal Pattern Recognition) data model established (~2026-10-20, 6+ months AI-summarised journal data).

**Problem**
No schema exists for user-authored free-text annotations on individual trades, distinct from the AI-summarised journal entry. Designing this ahead of PO-02's data model risks a schema that conflicts with or duplicates the eventual journal-pattern data structure.

**Scope**
- `trade_annotations` schema: trade_id, annotation_text, created_at, tags (optional, see BLG-FEAT-52)
- Co-designed with PO-02 data model once that gate clears

**Acceptance Criteria**
- Schema co-designed with PO-02 data model, not ahead of it
- Gate condition (PO-02 data model established) verified before sprint planning

---

### BLG-FEAT-59 — AI-assisted monthly P&L narrative
**Priority:** P3 (Low)
**Type:** Product Feature / AI
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** AI adoption window clears ~2026-07-25 (same constraint as BLG-FEAT-55/56 — too early to layer additional AI-generated content onto financial reporting).

**Problem**
Monthly P&L (shipped v2.x) is a fixed-format report. An optional AI-generated narrative commentary could add interpretive value, but adding it before existing AI features (daily briefing, chat) are validated risks compounding unvalidated AI surface area onto a financial-reporting document specifically.

**Scope**
- Optional AI narrative section appended to Monthly P&L using existing Claude infrastructure
- Advisory-only framing consistent with §13 SRB-v1.7

**Acceptance Criteria**
- Narrative section renders as optional/dismissible
- Gate condition (AI adoption window) verified by Financial Reporting & Records Owner before sprint planning

---

### BLG-FEAT-60 — AI chat engagement metric
**Priority:** P3 (Low)
**Type:** Product Feature / Analytics
**Owner:** Metrics Definitions & Analytics Owner
**Source:** IDEA-metrics-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** AI adoption window clears ~2026-07-25 — usage patterns remain unestablished at current usage duration; metric definition would be premature.

**Problem**
No metric tracks AI chat engagement (sessions per week, questions per session, response acceptance rate). Defining the metric before usage patterns stabilise risks needing early revision.

**Scope**
- Define engagement metric set: sessions/week, questions/session, response-acceptance rate
- Document in `metrics_definitions.md`

**Acceptance Criteria**
- Metric set defined and documented
- Gate condition (AI adoption window) verified before sprint planning

---

### BLG-FEAT-73 — SI-02 Behavioural Drift Detection — frontend build
**Priority:** P1 (High)
**Type:** Product Feature / Frontend, gate-conditional
**Owner:** Head of Engineering; Head of UX & Design
**Source:** Feature-gap review (current_roadmap.md Arc 5 status table cross-referenced with BLG-GOV-107, BLG-BE-46, BLG-BE-52) — 2026-07-10
**Effort:** M (~2 days)
**Provisional-Target:** v7.7 — named as v7.7 anchor scope 2026-07-21 (DL-074); `[gate status unverified/unmet]` — BLG-GOV-107 gate conditions last confirmed NOT MET 2026-07-17, not re-verified this session; may not enter sprint planning until independently reconfirmed met
**Depends on:** BLG-FE-56, BLG-FE-57, BLG-FE-58, BLG-FE-59 (UI extension specs); BLG-BE-27, BLG-BE-29 (perf baseline, index review) — all currently gate-conditional on this item entering sprint planning

**Problem**
The behavioural drift detection backend service shipped in v4.6 and computes drift scores from `trade_history`/`trade_plans` window functions, but no frontend was ever built to surface it — there is no UI showing drift scores, trend, or explanation anywhere in the app. This is Arc 5's flagship "tell me when I'm deviating from my own rules" feature, and it is currently invisible to the user despite the backend existing and running.

**Scope**
- Drift score display card(s) in `Arc5ComplianceSection`, per the existing extension-point spec (BLG-FE-59)
- Historical trend view for drift score over time
- Plain-language explanatory copy for what a drift score means and what action it implies

**Acceptance Criteria**
- User can view current drift score(s) in the Arc 5 compliance UI
- User can see a historical trend of drift score over time
- Each score is accompanied by plain-language explanation of contributing factors
- Feature does not enter sprint planning until all 3 BLG-GOV-107 gate conditions are independently reconfirmed met: (1) ≥20 closed trades with **linked** trade_plans (`trade_plans.position_id` populated) — note this gate can only clear via new trade_plans created going forward, since BLG-BE-52 declined to backfill the 11 pre-existing unlinked rows; (2) `GET /analytics/behavioural-drift` p99 < 2s stable over a 7-day window; (3) drift scores show non-trivial variance across trades (not all 0 or 1.0)

---

### BLG-FEAT-74 — PO-05 Lightweight Replay Mode
**Priority:** P1 (High) — escalated from P2, 2026-07-27, session product review (see note below)
> ⚠️ **Priority escalation (2026-07-27):** Raised P2→P1 during a session backlog review — the roadmap itself names this "the highest-value long-term validation feature" in Arc 4. Escalation reflects value judgment only; the §13 pre-clearance and effort-phasing conditions in this item's own scope note still apply before sprint entry.
**Type:** Product Feature / Backend + Frontend, gated
**Owner:** Head of Engineering; Product Owner
**Source:** Feature-gap review (current_roadmap.md §5 Arc 4, PO-05 — flagged as unbacklogged) — 2026-07-10
**Effort:** VH (>2 weeks)
**Provisional-Target:** v7.7 — named as v7.7 anchor scope 2026-07-21 (DL-074); `[gate status unverified/unmet]` — §13 determinism pre-clearance not yet run; effort (VH) exceeds typical single-cycle sizing, Release Planning to confirm phasing
**Depends on:** IT-06 Alpaca Paper Trading Integration (shipped v3.5) — foundational infrastructure this feature reuses

**Problem**
The roadmap names this "the highest-value long-term validation feature" in Arc 4, but no backlog item exists for it at all. There is currently no way for the user to test how a candidate strategy-rule change would have performed historically, or to replay a specific past setup/period against the paper-trading infrastructure that already exists and is otherwise unused for this purpose.

**Scope**
- §13 compliance pre-clearance: confirm the feature is a deterministic replay of the user's own historical data, not a predictive simulation (precedent: PS-03 Monte Carlo's determinism framing; IT-06's four binding conditions as a template for the review)
- Backend: replay a historical window of the user's own trade/candidate history through the existing paper-trading mechanics under the *current* rule set
- Frontend: date range or trade-set selector, and a clearly-labelled retrospective/deterministic output view
- Exact scope (single trade replay vs. full historical window, output format) to be confirmed by canonical spec before implementation, per the roadmap's Standing Notice

**Acceptance Criteria**
- User can select a historical date range or trade set and run it through paper-trading mechanics under current strategy rules
- Output is clearly labelled as retrospective/deterministic, not predictive
- §13 pre-clearance review completed and documented before sprint planning begins

---


### BLG-FEAT-76 — SI-05 Weekly Strategy Integrity Digest — Phase 2 (full digest)
**Priority:** P3 (Low)
**Type:** Product Feature / Backend + Frontend, gate-conditional
**Owner:** Head of Engineering; Head of UX & Design
**Source:** Feature-gap review (current_roadmap.md Arc 5 status table cross-referenced with BLG-FE-69, BLG-FE-71, BLG-GOV-121 — prep-only, no primary Phase 2 item existed) — 2026-07-10
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled (gated)
**Depends on:** BLG-FEAT-73 (SI-02 frontend) and BLG-FEAT-75 (SI-04) — hard-blocked on both shipping first; BLG-FE-69, BLG-FE-71, BLG-GOV-121 are prep items for this build

**Problem**
Only Phase 1 shipped (v5.0/v5.1) — a lightweight Telegram-only digest. The full-scope digest, incorporating SI-02 drift scores and SI-04 version comparison data, has prep items filed but no primary "build Phase 2" item ties them together, so this content will not exist even once its dependencies ship unless the digest itself is scoped and built.

**Scope**
- Extend the existing Telegram digest (or add an in-app channel, pending the Phase 2 channel decision referenced by BLG-FE-69/71) to include SI-02 drift score summaries and SI-04 version comparison highlights
- Sequenced explicitly last of the 5 items in this batch — must not enter sprint planning before SI-02 and SI-04 ship

**Acceptance Criteria**
- Weekly digest includes a drift score summary line
- Weekly digest includes a brief before/after comparison note when a strategy version change occurred in the reporting period
- Phase 2 channel decision (Telegram-only vs. added in-app view) resolved before frontend work begins

---


## 3. Frontend & UX Backlog

---

### BLG-FE-39 — Arc 2 user journey map
**Priority:** P3 (Low)
**Type:** Frontend / UX Design
**Owner:** Head of UX & Design
**Source:** IDEA-ux-design-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped.

**Problem**
No end-to-end user journey map exists covering the full Arc 2 flow: Screener → Watchlist → Research View → Trade Plan → Execution. As Arc 2 ships its final features, a journey map would surface UX gaps, confirm feature sequencing, and establish the baseline for Arc 3 UX planning. Requires PT-04 to be shipped so the full flow is complete before mapping.

**Scope**
- User journey map covering screener discovery → trade plan creation → execution
- Identify friction points and hand-off gaps between views
- Produce design recommendation: maintain current or file targeted UX improvement items

**Acceptance Criteria**
- Journey map document produced
- Friction points enumerated; any actionable items filed as backlog entries
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FE-43 — SI-05 Weekly Digest frontend component spec
**Priority:** P1 (High) — escalated from P2, 2026-07-27, session product review (see note below)
> ⚠️ **Priority escalation (2026-07-27):** Raised P2→P1 during a session backlog review as the highest-priority Frontend/UX item. Note this item is a component spec (pre-work), not a shippable feature — its own gate criteria (SI-05 sprint planning imminent) still govern entry.
**Type:** Frontend / Spec
**Owner:** Frontend Specs & UX Documentation Owner; Base44 Frontend
**Source:** IDEA-base44-frontend-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-05 (Weekly Strategy Integrity Digest) sprint planning imminent.

**Problem**
SI-05 will deliver the Weekly Strategy Integrity Digest via Telegram notification and potentially an in-app view. No frontend component spec or UX spec exists for the digest display. Authoring this spec before sprint planning ensures frontend scope is clearly defined and sized — preventing mid-sprint ambiguity on rendering requirements.

**Scope**
- UX spec: digest layout, content sections (drift signal, red flag summary, compliance score trend), notification vs in-app view decision
- Component requirements document: data inputs, update frequency, display states (no data, loading, populated)
- Review against Telegram notification format constraints (v2.4 weekly digest pattern)

**Acceptance Criteria**
- Frontend component spec and UX spec produced and filed
- Component requirements document covers all SI-05 data inputs
- Spec reviewed by Product Owner and Head of UX & Design before sprint planning
- Gate condition verified before sprint planning

---

### BLG-FE-45 — Arc5ComplianceSection layout expandability review
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Frontend / UX
**Owner:** Base44 Frontend; Head of UX & Design
**Source:** IDEA-base44-frontend-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** v4.1 sprint planning complete — layout expandability review requires knowing which Arc 6 compliance data points will be added to the PerformanceAnalytics page.

**Problem**
Arc5ComplianceSection.js (shipped v4.0) displays 5 compliance metrics. Arc 6 will add performance science metrics to the same analytics surface. Without an expandability review, the component layout may require significant rework when additional data sections are added. A pre-sprint review ensures the component is structurally extensible.

**Scope**
- Review Arc5ComplianceSection layout for extensibility: grid, card count, responsive breakpoints
- Identify layout constraints that would prevent additional section additions
- Produce short design note with recommendations (retain, refactor, or modularise)

**Acceptance Criteria**
- Design note produced and reviewed by Product Owner
- Gate condition verified before sprint planning

---

### BLG-FE-54 — Arc 5 unified pre-entry gateway
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Frontend / UX Exploration
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-frontend-ux-20260522-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035, 3-cycle cap)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** Arc 5 fully complete (SI-02, SI-04, SI-05 all shipped).

**Problem**
SI-01 (pre-entry validation panel) and PT-05 (entry checklist) are separate views requiring multi-view navigation before trade finalisation. A unified pre-entry gateway combining all required checks into a single screen could reduce friction and navigation complexity. Gate ensures design is informed by the complete Arc 5 feature set.

**Scope**
- Explore combining SI-01 and PT-05 into a single pre-entry gateway screen
- Map decision points and information needs for the combined flow
- Propose structural changes; not a committed sprint item until gate clears

**Acceptance Criteria**
- UX exploration document produced
- Combined flow mapped with clear decision points
- Gate condition (Arc 5 fully complete) verified before commencing

---

### BLG-FE-58 — Pre-entry panel: check grouping for Arc 5 expansion
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Frontend / UX Improvement
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Source:** docs/product/ux/pre_entry_panel_ux_assessment.md — candidate P4 — cycle 2026-05-31__release-v4.7 (ST-09)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 or SI-04 sprint planning initiated (Arc 5 expansion imminent).

**Problem**
PreEntryValidationPanel currently displays 5 checks in a flat list. As SI-02 drift detection and SI-04 strategy version comparison add compliance context to the pre-entry flow, check count may grow to 8–10+ items. A flat list at that scale is dense and unscannable.

**Scope**
- Group checks into labelled sections: "Compliance" (Arc 5 checks), "Risk" (cash, sizing), "Technical" (regime, earnings)
- Section headers use small separator labels; no collapsible sub-groups required
- Prepare component structure for Arc 5 check additions before SI-02/SI-04 ship

**Acceptance Criteria**
- Checks grouped into at minimum 2 sections (Compliance and Risk/Technical)
- Grouping does not break existing override acknowledgement behaviour
- Gate condition (SI-02 or SI-04 sprint planning) verified before commencing

---

### BLG-FE-59 — Arc5ComplianceSection extension spec for SI-02/SI-04
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Frontend / Spec
**Owner:** Frontend Specs & UX Documentation Owner; Base44 Frontend
**Source:** IDEA-frontend-ux-20260527-02 — Promoted-Backlog cycle 2026-06-02__scheduled (DL-037; terminal Parked-cycle-2 disposition)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 frontend + SI-04 sprint planning imminent (both Arc 5 features approaching their sprint entry).

**Problem**
Arc5ComplianceSection.js (shipped v4.0) displays 5 compliance metrics. SI-02 drift detection frontend and SI-04 strategy version comparison will each add new display cards to this section. Without extension point specifications defined in advance, each addition will require layout redesign rather than slotting into a prepared contract. Pre-specifying card layout contracts prevents rework.

**Scope**
- Update BLG-FE-48 spec (if exists) or author new: extension point specifications for SI-02 drift score card and SI-04 version comparison card
- Define card layout contract: minimum data fields, display states (loading, populated, gate-not-met), responsive breakpoints
- Ensure additions require no Arc5ComplianceSection.js layout redesign

**Acceptance Criteria**
- Extension spec document produced covering SI-02 and SI-04 card requirements
- Card layout contract defines all required display states
- Gate conditions (both SI-02 frontend + SI-04 sprint planning imminent) verified before commencing

---

### BLG-FE-62 — Pre-entry panel combined component specification (BLG-FE-56/57/58)
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Frontend / Spec
**Owner:** Frontend Specs & UX Documentation Owner; Base44 Frontend Prompt Owner
**Source:** IDEA-base44-frontend-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038; gate cleared: BLG-GOV-87 shipped v5.0)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-FE-56/57/58 sprint planning imminent; SI-02 frontend activation triggered (20+ closed trades confirmed). BLG-GOV-87 re-entry criteria shipped v5.0 — functional activation gate still pending.

**Problem**
BLG-FE-56 (warn/fail override separation), BLG-FE-57 (count badge when collapsed), and BLG-FE-58 (check grouping for Arc 5) are three interdependent PreEntryValidationPanel improvements. Specifying them individually risks fragmented UX implementation. A combined specification aligns all three changes before sprint planning seals.

**Scope**
- Combined component spec covering all three BLG-FE-56/57/58 improvements as a coherent design
- Map interaction dependencies (e.g., grouping in BLG-FE-58 affects badge count in BLG-FE-57)
- Input to sprint planning when gate triggers; replaces need for three separate spec documents

**Acceptance Criteria**
- Combined component spec produced and reviewed by Head of UX & Design
- All three BLG-FE-56/57/58 scopes covered in a single document
- Gate condition verified before sprint planning

---

### BLG-FE-63 — Arc 5 completion visual consistency pre-review
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Frontend / UX Design
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Source:** IDEA-head-of-ux-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038; gate cleared: BLG-GOV-88 shipped v5.0)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-04 sprint planning imminent. BLG-GOV-88 binding conditions shipped v5.0; SI-04 is in Later horizon — gate triggers when SI-04 enters sprint planning.

**Problem**
SI-04 (strategy version comparison) and SI-05 (weekly digest display) will introduce new panels to the Arc 5 UI surface. No review of the existing Arc 5 design vocabulary (Pre-Entry panel, Red Flag Journal, Arc5ComplianceSection) has been done to ensure consistency before these additions begin. A pre-review before SI-04 implementation prevents retroactive consistency fixes.

**Scope**
- Review existing Arc 5 panel design patterns (colour, typography, layout, empty states)
- Identify consistency vocabulary: what patterns to carry forward to SI-04/SI-05 panels
- Produce short design vocabulary note; no implementation required

**Acceptance Criteria**
- Design vocabulary note produced covering existing Arc 5 panels
- Consistency patterns identified; input to SI-04/SI-05 sprint planning
- Gate condition verified before sprint planning

---

### BLG-FE-66 — RFJ date-range filter (date-to field)
**Priority:** P3 (Low)
**Type:** Frontend / UX Refinement
**Owner:** Head of UX & Design; Base44 Frontend Prompt Owner
**Source:** ST-07 RFJ visual design review — filed 2026-06-22 (cycle 2026-06-19__release-v6.0)
**Effort:** XS
**Provisional-Target:** Unscheduled
**Gate criteria:** Event volume makes date-from-only filtering insufficient for review workflows.

**Problem**
The Red Flag Journal filter panel supports a "From date" input only. A growing journal has no upper date bound — a user reviewing "last month's" events cannot scope the view to a period. At current low event volume this is acceptable, but will become limiting as the journal grows.

**Scope**
- Add a "To date" input to the RFJ filter panel
- Update `GET /portfolio/red-flag-journal` to accept an optional `until` parameter
- Convert current date-from-only filter to a date range (from + to)

**Acceptance Criteria**
- "To date" filter input present in filter panel
- Results are scoped to [date-from, date-to] when both are set
- "Clear filters" clears both date inputs
- Existing "From date" behaviour unchanged when "To date" is not set

---

### BLG-FE-68 — Arc 5 compliance score sparkline trend chart (gate-conditional)
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Frontend / Analytics Display
**Owner:** Metrics Definitions & Analytics Owner; Base44 Frontend Prompt Owner
**Source:** IDEA-metrics-analytics-20260607-02 — Promoted-Backlog rebalance 2026-06-09__scheduled (DL-041)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** BLG-FE-45 (Arc5ComplianceSection layout expandability review) complete

**Problem**
The Arc 5 compliance score is displayed as a single value on the compliance section. A sparkline trend chart showing the score's trajectory over recent weeks would help identify improving or degrading compliance at a glance. The gate is BLG-FE-45 — adding widgets to Arc5ComplianceSection before the layout expandability review is premature.

**Scope**
- Add sparkline trend chart to Arc5ComplianceSection (or equivalent compliance view)
- Data source: existing compliance score history endpoint or new rolling-window endpoint
- Chart shows last 8–12 weeks of compliance scores
- BLG-FE-45 must be complete before this enters sprint planning

**Acceptance Criteria**
- Sparkline chart renders in compliance section
- Data sourced from a defined endpoint (not mocked)
- Gate condition (BLG-FE-45) verified before sprint planning
- Playwright: chart renders with data; empty state handled

---

### BLG-FE-69 — SI-05 in-app digest panel — read-only last-sent view (gate-conditional)
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Frontend / Notification Display
**Owner:** Base44 Frontend Prompt Owner; Frontend Specs & UX Documentation Owner
**Source:** IDEA-base44-frontend-20260607-01 — Promoted-Backlog rebalance 2026-06-09__scheduled (DL-041)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** Phase 2 channel decision (BLG-GOV-92 SI-05 Phase 2 activation criteria) — if Telegram remains the sole channel, this item is not required

**Problem**
SI-05 weekly digest is delivered via Telegram (v5.1). Users who miss a Telegram message have no way to retrieve the last digest content from within the app. An in-app read-only panel showing the last-sent digest content would provide a fallback reference point. However, this is premature until the Phase 2 channel decision confirms an in-app component is warranted.

**Scope**
- Read-only digest panel in Settings or a new SI-05 section
- Shows last digest sent: date, content summary, link counts
- No composition or editing — display only
- Phase 2 channel decision must be made before sprint planning

**Acceptance Criteria**
- Panel renders last-sent digest content
- Date and delivery status visible
- Gate condition (BLG-GOV-92 Phase 2 decision) verified before sprint planning

---

### BLG-FE-70 — Compliance score trend widget on dashboard homepage (gate-conditional)
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Frontend / Dashboard
**Owner:** Base44 Frontend Prompt Owner; Head of UX & Design
**Source:** IDEA-base44-frontend-20260607-02 — Promoted-Backlog rebalance 2026-06-09__scheduled (DL-041)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** BLG-FE-45 (Arc5ComplianceSection layout expandability review) complete

**Problem**
Dashboard homepage shows key portfolio metrics but not the Arc 5 compliance score trend. A small trend widget on the homepage would surface compliance trajectory without requiring navigation to the full compliance section. Gate is BLG-FE-45 — homepage widget additions should follow the expandability assessment.

**Scope**
- Small compliance score trend widget on dashboard homepage
- Shows current score + trend arrow (up/down/flat vs prior week)
- Links to full Arc5ComplianceSection
- BLG-FE-45 must be complete before this enters sprint planning

**Acceptance Criteria**
- Widget renders on dashboard with current score and trend indicator
- Links correctly to full compliance section
- Gate condition (BLG-FE-45) verified before sprint planning

---

### BLG-FE-71 — SI-05 in-app digest UX spec — Phase 2 potential (gate-conditional)
**Priority:** P1 (High) — escalated from P3, 2026-07-28, session product review (see note below)
**Type:** Frontend Spec / UX
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-frontend-ux-20260607-02 — Promoted-Backlog rebalance 2026-06-09__scheduled (DL-041)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Phase 2 channel decision (BLG-GOV-92) — if in-app delivery is confirmed for Phase 2, this spec should precede implementation

**Problem**
If SI-05 Phase 2 includes an in-app delivery channel, a UX spec will be required before frontend implementation begins. Authoring the spec before the Phase 2 channel decision is premature — the spec scope depends entirely on which channel(s) Phase 2 targets.

**Scope**
- Interaction pattern for SI-05 digest delivery in-app (read, dismiss, archive)
- Visual design: notification panel, badge indicators, read/unread states
- Produced only if Phase 2 channel decision confirms in-app component
- Must be completed before BLG-FE-69 sprint planning

**Acceptance Criteria**
- UX spec produced covering interaction patterns and visual design
- Reviewed by Head of UX & Design and Frontend Specs & UX Documentation Owner
- Gate condition (BLG-GOV-92) verified before authoring

---

### BLG-FE-83 — Frontend bundle size optimization assessment
**Priority:** P3 (Low)
**Type:** Frontend / Performance
**Owner:** Head of Engineering
**Source:** IDEA-head-of-engineering-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** A user-reported performance issue OR profiling data indicates bundle-size impact.

**Problem**
No formal assessment of current React bundle size or heavy dependencies has been performed. No user-reported issue currently motivates this — the gate exists specifically to avoid speculative optimisation work.

**Scope**
- Bundle analysis (e.g. source-map-explorer or equivalent) to identify heaviest dependencies
- Recommendations report; no implementation required at this stage

**Acceptance Criteria**
- Bundle analysis report produced
- Gate condition (reported issue or profiling signal) verified before commencing

---

### BLG-FE-84 — AI chat UI interaction study protocol
**Priority:** P3 (Low)
**Type:** Frontend / UX Research
**Owner:** Head of UX & Design
**Source:** IDEA-head-of-ux-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** AI adoption window clears ~2026-07-25 — usage patterns must stabilise before a research protocol targeting them is designed.

**Problem**
No structured protocol exists to study how the AI chat advisor is actually used. Designing one before interaction patterns stabilise risks studying patterns that later shift.

**Scope**
- 5-question interaction study protocol targeting chat advisor usage
- Applied once gate clears

**Acceptance Criteria**
- Protocol document produced
- Gate condition (AI adoption window) verified before use

---


### BLG-FE-147 — Register remaining unregistered shadcn design tokens in tailwind.config.js (card, popover, primary, secondary, accent, destructive, border, input, ring)
**Priority:** P2 (Medium)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** ST-06 (EPIC-03, 2026-08-08__release-v8.5), self-caught scope gap discovered mid-story — 2026-08-10
**Effort:** M (~1-2d — token registration + Playwright coverage or staging sign-off per confirmed-affected call site)
**Provisional-Target:** v8.6

**Problem**
`tailwind.config.js`'s `theme.extend.colors` only registers `background`, `foreground`, and (as of ST-06/BLG-FE-145, same release) `muted`. Every other CSS custom property defined in `src/index.css`'s shadcn theme block (`--card`, `--card-foreground`, `--popover`, `--popover-foreground`, `--primary`, `--primary-foreground`, `--secondary`, `--secondary-foreground`, `--accent`, `--accent-foreground`, `--destructive`, `--destructive-foreground`, `--border`, `--input`, `--ring`, `--chart-1..5`) is not registered, so every Tailwind utility class built on them (`bg-card`, `text-card-foreground`, `bg-popover`, `text-primary`, `bg-secondary`, `bg-accent`, `bg-destructive`, `border-border`, `bg-input`, `ring-ring`, etc.) compiles to an empty CSS rule — Tailwind only generates utilities for color tokens it knows about. Confirmed via a real `tailwindcss` build and `grep` across `src/`: `card` (2 distinct classes), `popover` (2), `primary` (5), `secondary` (2), `accent` (2), `destructive` (5), `border` (2), `input` (2), `ring` (1) — all currently dead, same root cause as the `-muted` classes ST-06 just fixed. These are used throughout the shadcn/ui primitive library (`accordion`, `alert-dialog`, `card`, `dialog`, `form`, `select`, `sheet`, `toast`, etc.) consumed across the app.

**Scope**
- Register the remaining tokens in `tailwind.config.js`'s `theme.extend.colors`, following the same `DEFAULT`/`foreground` pattern used for `muted` (ST-06)
- Verify via a real `tailwindcss` build that each affected class now compiles to a non-empty rule
- Identify confirmed-affected call sites per token and add Playwright coverage (or staging sign-off) per CLAUDE.md's frontend-visible-change rule

**Acceptance Criteria**
- `bg-card`, `text-card-foreground`, `bg-popover`, `text-primary`, `bg-secondary`, `bg-accent`, `bg-destructive`, `border-border`, `bg-input`, `ring-ring` (and any other affected `-card`/`-popover`/`-primary`/`-secondary`/`-accent`/`-destructive`/`-border`/`-input`/`-ring` classes found in scope) compile to a non-empty CSS rule, verified via a real `tailwindcss` build
- No visual regression at any confirmed-affected call site — Playwright coverage or staging sign-off per CLAUDE.md's frontend-visible-change rule

---

### BLG-FE-148 — Playwright coverage for the remaining `-muted`/`muted-foreground` call sites left untested by ST-06
**Priority:** P2 (Medium)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** ST-06 (EPIC-03, 2026-08-08__release-v8.5), agent-mediated Director of Quality review — 2026-08-10
**Effort:** S (~0.5d — targeted Playwright coverage, no implementation change)
**Provisional-Target:** v8.6

**Problem**
ST-06 (BLG-FE-145) registered `muted`/`muted-foreground` in `tailwind.config.js`, making every `-muted` utility class app-wide resolve to real CSS for the first time (previously an empty rule). This is a genuine app-wide visible colour change, not scoped to one component — `grep` confirms real, non-`ui/`-internal consumers of `text-muted-foreground`/`bg-muted`/etc. across `Input` (17 files, `placeholder:text-muted-foreground`), `Select` (10 files, `data-[placeholder]:text-muted-foreground`), `Dialog` (14 files, `DialogDescription`'s default `text-muted-foreground` — though every current call site overrides this className, so may not actually resolve; worth confirming as part of this item's own investigation), `Textarea` (4 files), `Tabs` (2 files, `TabsList`), `Sheet`, `Toast`, `Toggle` (1 file each). ST-06 itself added Playwright coverage for 2 of these mechanisms — the `CommandGroup` heading's element `color` (SC-CP-13) and `CommandInput`'s `::placeholder` colour (SC-CP-14), both in `command-palette.spec.js` — verified representative of the `text-muted-foreground` class as consumed by `Input`'s own placeholder styling (identical class), but the remaining families (`Select`, `Tabs`, `Sheet`, `Toast`, `Toggle`, and any `Dialog` call site that does NOT override the className) have zero Playwright coverage of the actual rendered colour post-fix. Filed per CLAUDE.md's frontend-visible-change hard gate (an observable AC deferred to post-merge without Playwright coverage requires a filed backlog item before the PR opens).

**Scope**
- For each of `Select`, `Tabs`, `Sheet`, `Toast`, `Toggle`: identify a real page/component call site and add a Playwright test asserting the post-fix computed colour (following the `SC-CP-13`/`SC-CP-14` pattern — `getComputedStyle`, not just class-name presence)
- Confirm whether any `DialogDescription` call site actually renders the default `text-muted-foreground` (vs. always being overridden by an explicit `className`, as observed in `ExportModal.js`/`WatchlistModal.js`/`WidgetLibrary.js` at filing time) — if none do, document that explicitly rather than leaving it untested and unexplained

**Acceptance Criteria**
- Each of the 5 listed families has at least one Playwright test asserting the real post-ST-06 computed colour at a confirmed-affected call site
- `DialogDescription`'s actual exposure (or non-exposure) of the default `text-muted-foreground` styling is confirmed and documented, with a test added if any live call site does expose it

---

### BLG-FE-149 — Fix 6 drift instances against the v6.7 canonical secondary-text token
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** ST-09 (EPIC-04, 2026-08-08__release-v8.5) — design token audit
**Effort:** XS (~<1h — mechanical class-name corrections, no design decision needed)
**Provisional-Target:** v8.6

**Problem**
ST-09's audit (`claude/cycles/2026-08-08__release-v8.5/st09_secondary_text_token_audit_findings.md`) found 6 instances that drift from the canonical secondary-text token established by the v6.7 remediation (`docs/design/2026-07-06__release-v6.7/secondary-text-contrast/ux_spec.md`: `text-slate-600 dark:text-slate-400`). Two sub-classes: (a) 4 instances use the failing light-theme shade `text-slate-500` (4.34:1 against `bg-slate-100`, below the 4.5:1 requirement) instead of canonical `text-slate-600` — `src/pages/Positions.js:591`, `src/components/positions/PositionCard.js:127`, `src/components/watchlist/WatchlistRow.js:27`, `src/Layout.js:~601-612` (search-affordance button + ⌘K badge — the badge's dark-theme value is also wrong, both branches use the pre-v6.7 failing `text-slate-500`; line numbers approximate and will drift further with subsequent edits — match on the cited class strings, not the line numbers, per the audit doc's 2026-08-10 correction); (b) 2 instances are missing a `dark:` variant entirely — `src/pages/Reports.js:660` (reconciliation sign-off note) and `src/components/dashboard/home/WhatsNewCard.js:56,61` (bullet marker and overflow-count list item, inconsistent with sibling list items in the same file that already use the canonical pair).

**Scope**
- Replace `text-slate-500` with `text-slate-600` (light-theme branch) in the 4 wrong-shade instances
- Add `dark:text-slate-400` to the 2 missing-variant instances (and their bare light value, if not already `text-slate-600`)
- No new design decision required — this is mechanical application of the already-approved v6.7 token

**Acceptance Criteria**
- All 6 instances use exactly `text-slate-600 dark:text-slate-400` (or the equivalent `isDark` ternary form already used elsewhere in `Layout.js`)
- No visual regression — Playwright coverage or staging sign-off per CLAUDE.md's frontend-visible-change rule

---

### BLG-FE-150 — Design decision needed: should modals/dialogs support light theme?
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Head of UX & Design
**Source:** ST-13 (EPIC-04, 2026-08-08__release-v8.5) — dark/light contrast audit follow-up
**Effort:** XS (~<1h to decide; follow-up implementation effort TBD by the decision)
**Provisional-Target:** v8.6

**Problem**
While verifying ST-06's dark-mode-portal fix, ST-13's audit found that 4 of 5 checked `Dialog`-based components (`WatchlistModal.js`, `ExportModal.js`, `PositionEntryModal.js`, `WidgetLibrary.js`) hardcode `DialogContent`'s styling to `bg-slate-900 ... text-white` — always dark, unconditionally, regardless of the app's light/dark theme setting. This is internally high-contrast (not a WCAG failure) but means a user with light theme selected still sees dark-styled modals — a light-theme completeness gap, consistent and long-standing across every consumer checked (not introduced this cycle). The one exception, `CommandDialog` (`src/components/ui/command.js`), correctly relies on the shared theme-aware tokens (`bg-background`, `text-foreground`, `text-muted-foreground`) rather than hardcoding.

**Scope**
- Head of UX & Design to decide: is dark-only modal styling an intentional, permanent design choice for this surface (in which case: document it as such in `design_system.md`, no code change needed), or should modals adopt the same light/dark theme-awareness as the rest of the app (in which case: file a follow-up implementation item to convert the 4 hardcoding consumers to the shared token pattern `CommandDialog` already uses)

**Acceptance Criteria**
- A decision record is produced either confirming dark-only modals as intentional (documented in `design_system.md`) or directing a follow-up implementation item to make modals theme-aware

---

### BLG-FE-151 — SI-02 Gate Status section (Reports.js) hardcodes dark-theme-only structural styling

**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Head of UX & Design
**Source:** ST-18 (EPIC-05, 2026-08-08__release-v8.5) — Reports page information hierarchy review

**Problem**
`SI02GateStatusSection` (`src/pages/Reports.js` lines 429-556, `BLG-FEAT-71`, v6.8) hardcodes its structural styling dark-only — container (`bg-slate-800/50 border-slate-700/50`), toggle hover (`hover:bg-slate-700/20`), heading (`text-white`), condition-badge row backgrounds (`bg-slate-800/50 border-slate-700/50`, ×3), value text (`text-white`, `text-slate-300`), loading skeleton (`bg-slate-800/50`) — with no `dark:` pairing anywhere, unlike the rest of `Reports.js` (44 `dark:` pairs elsewhere in the same file for secondary-text tokens). In a light-themed session this renders as a dark panel with light text inside an otherwise light-themed page. Same recurring defect class as `BLG-FE-87/88/95/125/129` and `BLG-FE-150`.

**Scope**
- Convert the listed classes to explicit light+dark Tailwind pairs, matching the token conventions already used elsewhere on the same page (e.g. `text-slate-600 dark:text-slate-400` for secondary text)

**Acceptance Criteria**
- `SI02GateStatusSection` renders correctly in both light and dark theme with no hardcoded dark-only structural class remaining
- No visual regression to the section's dark-theme appearance

---

### BLG-FE-152 — Unrealised P&L card (Reports.js) hardcodes dark-theme-only structural styling

**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Head of UX & Design
**Source:** ST-18 (EPIC-05, 2026-08-08__release-v8.5) — out-of-scope observation, same root cause as BLG-FE-151, found while reviewing the adjacent SI-02 section

**Problem**
The Unrealised P&L card immediately preceding the SI-02 Gate Status section (`src/pages/Reports.js` lines 401-414) has the identical structural defect — hardcoded `border-slate-600/50 bg-slate-800/30` container and `text-slate-300` heading, no `dark:` pairing — while its own body text correctly uses the `dark:` pair. Predates `BLG-FEAT-71`/SI-02 (unrelated feature), so filed separately from `BLG-FE-151` rather than folded into it.

**Scope**
- Convert the container/heading classes to explicit light+dark Tailwind pairs, consistent with the fix applied for `BLG-FE-151`

**Acceptance Criteria**
- Unrealised P&L card renders correctly in both light and dark theme with no hardcoded dark-only structural class remaining

---

### BLG-FE-153 — Switch Layout.js's dark-class document.documentElement sync to useLayoutEffect

**Priority:** P4 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** Agent-mediated PR review (Director of Quality role), PR #1328, 2026-08-08__release-v8.5 — 2026-08-10 (explicitly assessed as very low risk, non-blocking)
**Effort:** XS (<1h)
**Provisional-Target:** v8.6

**Problem**
`src/Layout.js`'s dark-class-onto-`document.documentElement` sync (the EPIC-03/ST-06 portal-theming fix) runs in a plain `useEffect` (post-paint), not `useLayoutEffect`. Theoretically a portal-rendered dialog opened in the exact same tick as first mount could render one frame in the wrong theme before the sync runs. Reviewer assessed this as very low risk in practice since portals aren't mounted at initial page load.

**Scope**
- Switch the dark-class sync from `useEffect` to `useLayoutEffect`, or explicitly document in a code comment why `useEffect` is intentionally sufficient

**Acceptance Criteria**
- Either the hook is switched to `useLayoutEffect`, or a code comment explains why the current `useEffect` timing is intentionally acceptable

---

### BLG-FE-154 — Correct st15_nav_bar_redesign_exploration.md's nav group/page counts against live NAV_GROUPS

**Priority:** P2 (Medium)
**Type:** Frontend / UX
**Owner:** Head of UX & Design
**Source:** Agent-mediated PR review (Director of Quality + Product Owner roles), PR #1330, 2026-08-08__release-v8.5 — 2026-08-10
**Effort:** S (~0.5d)
**Provisional-Target:** v8.6

**Problem**
`claude/cycles/2026-08-08__release-v8.5/st15_nav_bar_redesign_exploration.md` claims to be "evaluated directly against the live implementation" and states nav group counts (Trading 4, Analytics 3, Tools 1, System 4 = 13 total) that are factually wrong by ~40% — the real `NAV_GROUPS` array in `src/Layout.js` has Trading 5, Analytics 5, Tools 3, System 4 (17 grouped items + `DashboardHome` = 18). The wrong numbers exactly match a stale spec doc (`docs/specs/frontend/pages/navigation.md` §Group Structure v1.4) rather than the code the doc claims to have checked directly. The "page inventory" paragraph also has an internal count mismatch (labels 8 items "the remaining 7") and wrongly claims 5 pages actually in the live sidebar are reached only via contextual links. The qualitative recommendation (maintain current nav pattern) is very likely still correct even with accurate counts, but the document's central evidentiary claim needs correcting before it's cited elsewhere.

**Scope**
- Correct the group-count and page-inventory paragraphs in `st15_nav_bar_redesign_exploration.md` against the actual `NAV_GROUPS` array in `src/Layout.js`
- Flag `docs/specs/frontend/pages/navigation.md` §Group Structure as stale and due for a refresh (it does not reflect the current live sidebar)

**Acceptance Criteria**
- `st15_nav_bar_redesign_exploration.md`'s group/page counts match the live `NAV_GROUPS` array exactly
- `navigation.md`'s staleness is either fixed or explicitly flagged with a follow-up item

---

### BLG-FE-155 — Migrate CohortAnalysis.js from client-side computation to GET /analytics/cohort
**Priority:** P2 (Medium)
**Type:** Frontend / Spec Compliance
**Owner:** Head of Engineering; Base44 Frontend Prompt Owner
**Source:** Head of Specs Team direct action, resolving the 72-hour escalation from post-ship closure `2026-08-08__release-v8.5` §5/§6 (`closure_record.md` item 2) — re-triage of `DEV-EPIC02-ST03-01`, stale since `v1.10` (2026-03-16), never previously filed to backlog despite the deviation's own note committing to do so at "next roadmap rebalance" — 2026-08-11
**Effort:** S (~1 day)
**Provisional-Target:** TBD

**Problem**
`CohortAnalysis.js` (Performance Analytics page, `analytics.md` §15 Cohort Analysis) computes cohort groupings, win rates, avg R-multiple, and net P&L entirely client-side via `buildCohorts()`, despite `analytics.md` §15's canonical hard rule ("All values sourced from backend. No client-side R-multiple computation in this component.") and despite `GET /analytics/cohort?period={month|quarter|year}` already being implemented, tested, and wired in `base44Client.js`. Filed as deviation `DEV-EPIC02-ST03-01` at `v1.9` (2026-03-06); values are currently numerically identical to the backend endpoint (same formula, same null-handling for trades without stop data), so this is not a live correctness bug — but it is an ongoing architectural drift risk: two independent implementations of the same formula exist, and nothing prevents them from silently diverging if the trade data shape changes server-side without a matching frontend update. Sibling section §16 (R-Multiple Distribution) explicitly frames backend computation as authoritative for this exact reason.

**Scope**
- `CohortAnalysis.js` should call `api.analytics.cohort(period)` (already wired in `base44Client.js`) and render the backend response directly, removing the local `buildCohorts()` computation path
- No visual/UX change expected — output values are already identical

**Acceptance Criteria**
- `CohortAnalysis.js` sources all displayed values (`period_label`, `trade_count`, `win_rate`, `avg_r_multiple`, `total_pnl`) from `GET /analytics/cohort`'s response, not local computation
- `buildCohorts()` removed or reduced to a thin response-mapping helper with no independent formula logic
- No visual regression (Playwright coverage or staging sign-off per `CLAUDE.md`'s frontend-visible-change rule — this is a data-source swap not a rendering change, so code review may suffice per FI-P3-02 if genuinely no visual change)
- `analytics.md`'s `DEV-EPIC02-ST03-01` entry marked Resolved referencing this item and the shipping commit
- Head of Specs Team confirms closure

---

### BLG-FE-156 — Convert 4 hardcoded dark-only modals to theme-aware tokens
**Priority:** P2 (Medium)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** ST-07 (EPIC-03, `2026-08-11__release-v8.6` design gate) — follow-up implementation item recommended by `BLG-FE-150`'s design decision, filed by PMO Lead — 2026-08-11
**Effort:** S (~0.5-1d)
**Provisional-Target:** v8.7 or later (see sequencing note below)
**Depends on:** `BLG-FE-147` (this same v8.6 cycle) — see sequencing note

**Problem**
`BLG-FE-150`'s v8.6 design gate decision (`docs/design/2026-08-11__release-v8.6/modal-light-theme-support/decision_record.md`) confirmed that dark-only modal styling is unintentional legacy drift, not an intentional design choice — modals/dialogs should be theme-aware like the rest of the app, matching `CommandDialog`'s already-correct pattern (`src/components/ui/command.js`). 4 components still hardcode `bg-slate-900 ... text-white` unconditionally, regardless of the app's active theme: `WatchlistModal.js`, `ExportModal.js`, `PositionEntryModal.js`, `WidgetLibrary.js` (found at the v8.5 ST-13 dark/light contrast audit). The decision itself does not ship a fix — this item is that fix.

**Scope**
- Convert the 4 named components' `DialogContent` styling from hardcoded `bg-slate-900`/`text-white` to the shared `bg-background`/`text-foreground` (or `bg-popover`/`text-popover-foreground` where a popover-elevation surface is more appropriate) token set, per `design_system.md`'s "Modal / Dialog Theming" subsection (v1.9)

**Acceptance Criteria**
- All 4 named components render correctly in both light and dark theme, using the shared token set instead of hardcoded dark-only classes
- No visual regression to existing dark-theme appearance — Playwright coverage or staging sign-off per `CLAUDE.md`'s frontend-visible-change rule

**Sequencing note:** should not be scheduled before `BLG-FE-147` (this same v8.6 cycle) ships — `bg-popover`/`text-popover-foreground` are among the tokens `BLG-FE-147` registers in `tailwind.config.js`. Building this fix first would silently reproduce the same "empty CSS rule" failure mode `BLG-FE-147` exists to close.

---

## 4. Backend & Data Backlog

---

### BLG-BE-13 — Screener result history table
**Priority:** P3 (Low)
**Type:** Backend Engineering
**Owner:** Head of Backend Engineering
**Source:** IDEA-backend-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** ~~Screener live ≥ 60 days (sufficient history to make a queryable history table valuable).~~ **Gate cleared 2026-08-08** — Screener shipped v3.0 (2026-04-27, 103 days ago); threshold long since passed.

**Problem**
Each screener run overwrites or appends to the current results without a queryable historical table. After 60 days, trend analysis (how screener output has evolved over time) becomes valuable but requires a properly structured history table with per-run metadata (run_timestamp, run_id, ticker count, pass count, regime distribution). Without this, historical comparison is not possible.

**Scope**
- `screener_run_history` table: run_id, run_timestamp, total_tickers, pass_count, regime_distribution JSON
- `GET /screener/history` endpoint returning run history with pagination
- Backfill not required; populate from next run forward

**Acceptance Criteria**
- History table created and populated on each screener run
- `GET /screener/history` returns paginated run history
- Gate condition verified by Product Owner before sprint planning

---

### BLG-BE-14 — Trade plan schema versioning
**Priority:** P3 (Low)
**Type:** Backend Engineering
**Owner:** Head of Backend Engineering; Head of Specs Team
**Source:** IDEA-backend-20260421-02 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** ≥ 3 new fields added to trade plan schema after v3.4 baseline (indicating schema churn warrants versioning overhead).

**Problem**
Trade plan schema has grown incrementally. If the schema continues to change at pace (new fields, deprecated fields), reading old plans stored under prior schema versions becomes an issue. Schema versioning adds a `schema_version` field to each trade plan record, enabling readers to apply the correct transformation for older records. Gate ensures the overhead is warranted before introducing this complexity.

**Scope**
- Add `schema_version` field to trade plan records (default: current version)
- Transformation layer: when reading plans, apply version-appropriate defaults for missing fields
- Migration: backfill existing plans with baseline schema_version

**Acceptance Criteria**
- `schema_version` field present on all trade plan records
- Read path applies correct field defaults for legacy records
- Gate condition (≥3 new fields post v3.4) verified by Product Owner before sprint planning

---

### BLG-BE-21 — Arc 5 analytics endpoint versioning strategy
**Priority:** P3 (Low)
**Type:** Backend / API Design
**Owner:** Head of Backend Engineering; API Contracts Documentation Owner
**Source:** IDEA-backend-engineering-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Arc 6 planning trigger — analytics endpoint versioning strategy needed when Arc 6 analytics endpoints are being designed alongside existing Arc 5 endpoints.

**Problem**
GET /analytics/arc5-compliance (shipped v4.0) and future Arc 6 analytics endpoints will coexist on the same service. Without an explicit versioning and naming convention, Arc 6 additions may collide with or shadow Arc 5 endpoints. A versioning strategy (path prefix, query param, or response envelope version) must be decided before Arc 6 sprint planning.

**Scope**
- Define endpoint versioning convention for analytics namespace
- Assess whether current /analytics/ prefix is extensible or requires refactoring
- Input to Arc 6 analytics endpoint design

**Acceptance Criteria**
- Versioning strategy documented in API design notes or openapi.yaml preamble
- Reviewed by API Contracts Documentation Owner and Head of Specs Team
- Gate condition (Arc 6 planning trigger) verified before commencing

---

### BLG-BE-24 — Red flag events retention policy
**Priority:** P2 (Medium)
**Type:** Backend / Data Lifecycle
**Owner:** Head of Backend Engineering; Infrastructure & Operations Owner
**Source:** IDEA-backend-engineering-20260522-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035, 3-cycle cap)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** red_flag_events table 6+ months old (post 2026-11-22).

**Problem**
The red_flag_events table has no defined data retention policy. As override events accumulate over months, query performance may degrade without indexes and archiving strategy. Defining a retention policy before the table requires unplanned maintenance is standard operational hygiene.

**Scope**
- Define minimum required event fields for retention
- Define archiving cadence (e.g. events older than 12 months archived to cold storage)
- Define query performance thresholds that trigger archiving review
- Document policy in ops notes

**Acceptance Criteria**
- Retention policy document produced
- Archiving cadence defined
- Gate condition (table 6+ months old) verified before commencing

### BLG-BE-27 — SI-02 drift service query performance baseline
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Performance
**Owner:** Backend Engineering Patterns Owner; Head of Engineering
**Source:** IDEA-backend-engineering-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 frontend sprint planning triggered; 20+ closed trades confirmed (BLG-GOV-87 re-entry criteria shipped v5.0 — functional activation still pending trade count gate).

**Problem**
The SI-02 drift service (shipped v4.6) uses window functions over trade_history and trade_plans. With only 6 closed trades, current query volume is too low to surface meaningful index gaps. A performance baseline at activation volume (20+ trades) establishes the query cost before concurrent frontend load is introduced.

**Scope**
- Run drift score queries against staging at 20+ trade volume
- Record p50/p95 query latency per metric (early_entry_rate, momentum_override_rate, losing_streak_sizing, regime_deviation_rate)
- Identify indexes required to maintain sub-200ms response at projected load

**Acceptance Criteria**
- Performance baseline document produced for all 4 drift metric queries
- Indexes identified and filed as implementation items if needed
- Gate condition verified before sprint planning

---

### BLG-BE-28 — Arc 4 PO-03 behavioral pattern storage pre-design
**Priority:** P3 (Low)
**Type:** Backend Engineering / Data Model
**Owner:** Backend Engineering Patterns Owner; Data Model, Domain & Schema Owner
**Source:** IDEA-backend-engineering-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PO-02 gate met (6+ months AI journal entries ~Oct 2026) + Arc 4 sprint planning triggered.

**Problem**
PO-03 (Behavioural Error Taxonomy) requires a new classification table and error_type enum. Pre-designing the schema before Arc 4 sprint planning prevents same-sprint data model debt (pattern observed in v3.3 IT-01/02/03 backend split).

**Scope**
- Define error_type enum values (entry_too_early, sized_incorrectly, ignored_regime, held_too_long, etc.)
- Define behavioral_errors table schema (id, trade_id, journal_entry_id, error_type, notes, detected_at)
- Pre-design migration strategy; no implementation until Arc 4 sprint

**Acceptance Criteria**
- Schema pre-design document produced
- error_type enum values defined and reviewed by Metrics Definitions & Analytics Owner
- Gate condition verified before sprint planning

---

### BLG-BE-29 — Database index review for SI-02 drift queries
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Performance
**Owner:** Head of Engineering; Backend Engineering Patterns Owner
**Source:** IDEA-head-of-engineering-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 frontend sprint planning triggered; 20+ closed trades confirmed. To be completed alongside or immediately after BLG-BE-27.

**Problem**
SI-02 drift service queries trade_plans and trade_history with window functions and date-range filters. Appropriate indexes must be confirmed before frontend activation adds concurrent load. BLG-BE-27 establishes the baseline; this item implements any gaps found.

**Scope**
- Review current indexes on trade_plans (signal_id, entry_date, exit_date) and trade_history (trade_id, close_date)
- Add indexes identified as missing from BLG-BE-27 performance baseline
- Verify drift score queries benefit from new indexes via EXPLAIN ANALYZE

**Acceptance Criteria**
- Index gaps identified and addressed
- EXPLAIN ANALYZE output confirms index usage for all drift metric queries
- Gate condition verified before sprint planning

---

### BLG-BE-30 — SI-04 schema requirements pre-design
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Data Model
**Owner:** Data Model, Domain & Schema Owner; Backend Engineering Patterns Owner
**Source:** IDEA-data-model-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038; gate cleared: BLG-GOV-88 shipped v5.0)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

> ⚠️ **Gate removed (2026-08-11, roadmap rebalance, IDEA-challenger-20260809-01, DL-078):** The prior gate ("SI-04 sprint planning imminent") was self-referential — this item's entire purpose is small (~1 day) pre-design work meant to happen *ahead of* SI-04 entering a sprint, to avoid same-sprint data model debt, which the gate wording prevented by construction. Un-gated by Product Owner decision; now Actionable-now (A-category). No `**Gate criteria:**` field — this item is ready for `plan release` consideration on its own merits.

**Problem**
SI-04 strategy version comparison requires linking trade_plans to historical strategy_rules.md versions. Whether this is a new strategy_versions table, a foreign key, or a snapshot field must be decided before SI-04 sprint to avoid same-sprint data model debt. BLG-SPEC-43 (API contract) exists; data model pre-design is the remaining gap.

**Scope**
- Evaluate three schema options: new table (strategy_versions), FK on trade_plans (strategy_version), snapshot field (strategy_snapshot JSON)
- Recommend approach with rationale (versioning overhead vs query simplicity)
- Define migration path for existing trade_plans (backfill strategy)

**Acceptance Criteria**
- Schema pre-design document produced with recommended approach
- Reviewed by Data Model, Domain & Schema Owner and Strategy Rules & System Intent Owner
- Gate condition verified before sprint planning

---

### BLG-BE-31 — Arc 4 PO-04 reflection-outcome correlation data prerequisites
**Priority:** P3 (Low)
**Type:** Backend Engineering / Data Model
**Owner:** Data Model, Domain & Schema Owner; Backend Engineering Patterns Owner
**Source:** IDEA-data-model-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PO-02 gate met + Arc 4 sprint planning triggered (~Oct-Dec 2026).

**Problem**
PO-04 (Reflection ↔ Outcome Correlation) requires journal entries with quantified reflection depth scores linked to trade outcomes. Neither reflection depth scoring nor the linkage from journal_entries to trade outcomes is currently captured. A data prerequisites assessment determines whether new fields are needed before Arc 4 sprint planning.

**Scope**
- Assess current journal_entries and trade_history data models for PO-04 readiness
- Identify new fields required: reflection_depth_score, journal_entry_id on trade_history, etc.
- Document prerequisites; no implementation until Arc 4 sprint

**Acceptance Criteria**
- Data prerequisites assessment document produced
- New fields required for PO-04 identified and estimated
- Gate condition verified before sprint planning

---

### BLG-QA-21 — Arc 2 end-to-end QA protocol
**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA Lead
**Source:** IDEA-qa-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped — Arc 2 feature set complete.

**Problem**
No consolidated end-to-end QA protocol covers the full Arc 2 feature set (Screener, Research View, Trade Plan, Setup Quality Score). Individual EPICs have per-story DoQ sign-offs, but there is no arc-level protocol that exercises the full workflow from screener discovery to closed trade with a quality score. Such a protocol is most valuable once Arc 2 is complete.

**Scope**
- Arc-level E2E test protocol document covering full Arc 2 flow
- Playwright automation for the core arc-level happy path
- Manual checklist for Arc 2 edge cases not covered by Playwright

**Acceptance Criteria**
- Arc 2 E2E protocol document produced and filed in `docs/qa/`
- Core happy path covered by Playwright
- Gate condition verified by QA Lead and Product Owner before sprint planning

---

### BLG-QA-22 — Arc 2 DoQ standards review
**Priority:** P3 (Low)
**Type:** QA / Governance
**Owner:** QA Lead; Head of Specs Team
**Source:** IDEA-qa-20260421-02 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped — Arc 2 feature set complete.

**Problem**
DoQ standards (shared_standards.md §DoQ) were established in Arc 1 and have evolved incrementally. Arc 2 introduced new feature types (research views, AI-assisted UX, trade plans) that may expose gaps in the existing DoQ rubric. A targeted review of DoQ standards against Arc 2 artefacts will ensure the standards remain fit for Arc 3 and beyond.

**Scope**
- Review DoQ standards against Arc 2 EPIC QA evidence files
- Identify any rubric gaps introduced by Arc 2 feature types
- Propose amendments to `shared_standards.md` DoQ section if warranted

**Acceptance Criteria**
- DoQ standards reviewed; gaps (if any) documented
- If amendments warranted: `shared_standards.md` updated per §6 governance checklist
- Gate condition verified before sprint planning

---

### BLG-QA-23 — Trade plan lifecycle end-to-end test
**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA Lead
**Source:** IDEA-qa-20260421-03 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped.

**Problem**
No Playwright test covers the full trade plan lifecycle: create → edit → link to position → close → view in plan-vs-reality. Individual story tests cover creation and display, but lifecycle continuity (plan survives position link, quality score visible at creation, plan-vs-reality renders post-close) is not tested end-to-end. PT-04 must be shipped to make the quality-score step part of the lifecycle.

**Scope**
- Playwright E2E test: create plan with quality score visible → link to position → close position → verify plan-vs-reality
- Cover: plan state transitions, quality score persistence, plan-vs-reality accuracy

**Acceptance Criteria**
- Full lifecycle Playwright test authored and passing in CI
- Gate condition verified by QA Lead and Product Owner before sprint planning

---

### BLG-QA-26 — Arc 5 QA protocol
**Priority:** P2 (Medium)
**Type:** QA / Test Coverage
**Owner:** Director of Quality; QA Lead
**Source:** IDEA-director-of-quality-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** ~~Arc 5 fully complete per BLG-QA-45 criteria (docs/qa/arc5_qa_completion_criteria.md): SI-01 ✅, SI-02 backend ✅, SI-03 ✅, SI-05 Phase 1 ✅, BLG-QA-49 coverage assessment ✅. SI-02 frontend, SI-04, and SI-05 Phase 2 explicitly excluded from trigger. Updated 2026-06-16 (ST-09 v5.6).~~ **Gate cleared 2026-08-08** — all named trigger sub-conditions (SI-01, SI-02 backend, SI-03, SI-05 Phase 1, BLG-QA-49) already showed ✅ as of the 2026-06-16 update; no remaining condition blocks this item.

**Problem**
SI-01 through SI-03 shipped across v3.8 and v3.9. Each sprint produced per-story DoQ sign-offs but no arc-level QA protocol exists covering the full Arc 5 feature set end-to-end. Once all five features ship, an arc-level protocol analogous to BLG-QA-21 (Arc 2 E2E QA protocol) will ensure the complete Strategy Integrity workflow is tested holistically.

**Scope**
- Arc-level E2E test protocol document covering full Arc 5 flow: validation gate → override event → red flag journal → drift detection review → strategy version comparison → weekly digest
- Playwright automation for the arc-level happy path
- Manual checklist for Arc 5 edge cases not covered by Playwright
- Filed in `docs/qa/arc5_qa_protocol.md`

**Acceptance Criteria**
- Arc 5 E2E protocol document produced and filed
- Core happy path covered by Playwright
- Gate condition verified by QA Lead and Product Owner before sprint planning

---

### BLG-QA-42 — SI-02 E2E Playwright test strategy and scaffold (consolidated)
**Priority:** P2 (Medium)
**Type:** QA / Test Coverage
**Owner:** Director of Quality; QA Lead
**Source:** IDEA-director-of-quality-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038); consolidates BLG-QA-55 — a readiness-assessment follow-up on this item's own scaffold, gated on the same 20+ closed-trades condition — merged 2026-07-28, session duplicate-consolidation cleanup
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 frontend sprint planning triggered; 20+ closed trades confirmed. BLG-QA-37 (Playwright mock strategy for drift features, shipped v4.2) defines the approach — this item implements it.

**Problem**
SI-02 drift service (35 unit tests, shipped v4.6) has no E2E Playwright coverage. When the frontend ships (~2027-Q1), test coverage must be ready immediately. Pre-building the scaffold 1–2 cycles before activation avoids rushed test creation under sprint pressure.

**Scope**
- Define E2E test strategy for GET /analytics/behavioural-drift (per BLG-QA-37 Playwright mock strategy)
- Scaffold Playwright test file with scenarios: drift scores render, gate-not-met state, all 4 metric cards display
- Confirm mock data approach (per BLG-QA-37 mock strategy)
- Once the 20+ closed-trades gate clears and SI-02 frontend enters sprint planning: re-review this scaffold against the final drift service implementation (which may have evolved since authoring) and confirm the mock strategy is still valid before sprint entry

**Acceptance Criteria**
- E2E test strategy document produced
- Playwright test scaffold created and passing against mock data
- All 4 drift metric display scenarios covered
- Gate condition verified before sprint planning
- Pre-sprint-entry readiness confirmation recorded: "proceed with scaffold as-is" or a revision document produced, with Director of Quality sign-off

---

### BLG-QA-44 — SI-04 test planning requirements definition
**Priority:** P2 (Medium)
**Type:** QA / Test Planning
**Owner:** QA Lead; Director of Quality
**Source:** IDEA-qa-lead-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038; gate cleared: BLG-GOV-88 shipped v5.0)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-04 sprint planning imminent. BLG-GOV-88 binding conditions shipped v5.0 — functional activation gate is SI-04 entering sprint planning (Later horizon).

**Problem**
SI-04 (strategy version comparison) requires test coverage across: unit tests (version comparison logic), integration tests (trade_plans version linkage), and Playwright (version diff display). Defining test requirements before sprint planning ensures test scope is clear and prevents test debt analogous to BLG-QA-24 (Yahoo Finance backoff).

**Scope**
- Define unit test requirements: version comparison logic, version not found case
- Define integration test requirements: trade_plans version linkage correctness
- Define Playwright scenario requirements: version diff display, empty state, gate-not-met
- Estimate test effort; input to sprint sizing

**Acceptance Criteria**
- Test requirements document produced covering all three test tiers
- Playwright scenario outlines defined
- Gate condition verified before sprint planning

---

### BLG-BE-42 — Backend request tracing
**Priority:** P3 (Low)
**Type:** Backend Engineering / Observability
**Owner:** Backend Engineering Patterns Owner
**Source:** IDEA-backend-engineering-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** A demonstrated multi-service call failure requiring cross-service tracing to diagnose.

**Problem**
No per-request trace ID propagation exists across routers/services. No incident has yet demonstrated a need for this level of observability — the gate exists to avoid speculative infrastructure investment.

**Scope**
- Trace ID generation at request entry; propagation through service-layer calls
- Surfaced in structured logs

**Acceptance Criteria**
- Trace ID present in logs across a multi-service call path
- Gate condition (demonstrated failure requiring tracing) verified before commencing

---

### BLG-BE-66 — Index review pass for trade_plan queries as row count grows
**Priority:** P3 (Low) | **Type:** Backend / Data Model | **Owner:** Data Model & Domain Schema Owner | **Source:** IDEA-data-model-20260717-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `trade_plans` row count is currently small (11 rows per live check 2026-07-17) so no index pressure exists yet, but several endpoints join or filter on `position_id`/`ticker`/`status` without a confirmed index review.
**Scope:** A lightweight index audit against current query patterns, to be actioned proactively rather than reactively once row count grows materially.
**Acceptance Criteria:** Audit completed; any missing indexes identified (implementation deferred if no current performance impact, per gate below).
**Gate criteria:** Revisit when `trade_plans` row count exceeds ~500 or any query is observed exceeding baseline latency — not urgent at current scale.

---

### BLG-BE-84 — Link price_alerts to the trade they trigger (real alert-to-trade provenance)
**Priority:** P3 (Low)
**Type:** Backend Engineering
**Owner:** Head of Backend Engineering
**Source:** ST-31 (EPIC-01, 2026-08-07__release-v8.4), self-caught scope gap during `ESC-EXEC-20260807-01`
**Effort:** M (~2–3 days, schema + backend + frontend trade-creation wiring — not yet fully scoped, estimate advisory only)
**Provisional-Target:** Unscheduled

**Problem**
`BLG-FEAT-78` originally asked for a tax-year CSV export column distinguishing alert-triggered trades from manually-initiated ones, gated on `price_alerts` (`BLG-FE-116`, shipped v7.5) existing. On implementation (ST-31, v8.4) it was found that `price_alerts` has no schema linkage to any trade/position/trade_plan row at all — `POST /alerts/evaluate` firing an alert only writes a `notifications` row and sets `active=false`/`triggered_at`; it never creates or tags a trade. There is currently no way, anywhere in the data model, to determine "this trade was opened because a price alert fired." ST-31 shipped a *different*, real distinction instead (`trade_plans.signal_id` — the momentum-signals system, relabeled `trade_origin: "Signal"/"Manual"`) — see `docs/specs/api_contracts/reports_endpoints.md`'s Known Deviations section. This item tracks the *original* ask, which remains unbuilt.

**Scope**
- Design and add a linkage from a fired `price_alerts` row to the trade plan/position a user subsequently opens as a result (e.g. a nullable `triggered_by_price_alert_id` on `trade_plans`, populated when the user creates a plan directly from a triggered-alert notification)
- Frontend wiring: some UI path from "alert notification" → "create trade plan" that can pass the alert's id through
- Decide reporting treatment once the linkage exists: could extend `trade_origin` to a third value (e.g. `"Alert"`) or become a separate field — needs its own scoping pass, not assumed here

**Acceptance Criteria**
- A trade plan created via the alert-notification-to-trade-plan path (once that path exists) records which `price_alerts` row triggered it
- A trade plan created any other way leaves the field null
- Reporting treatment (new `trade_origin` value vs. separate field) decided and documented before implementation

---

### BLG-BE-85 — si05_digest_log.telegram_message_id is never populated
**Priority:** P3 (Low)
**Type:** Backend Engineering
**Owner:** Head of Backend Engineering
**Source:** ST-19 (EPIC-05, 2026-08-07__release-v8.4), staging verification of the SI-05 digest delivery fix — 2026-08-08
**Effort:** XS (<1 day)
**Provisional-Target:** TBD

**Problem**
`si05_digest_log`'s `telegram_message_id` column exists specifically to record Telegram's own returned message ID for each delivery attempt (`BLG-BE-33`), but is hardcoded to `None` at both call sites in `si05_digest_service.py::send_si05_digest()`. Root cause: `_send_telegram_request()` calls `urllib.request.urlopen(req, timeout=10)` and returns immediately without reading the response body — Telegram's success response (which contains `result.message_id`) is discarded. Confirmed live at ST-19's staging verification: a genuinely successful send (`status: 'sent'`, message received in Telegram) still logged `telegram_message_id: null`.

**Scope**
- `_send_telegram_request()` reads and returns the response body on success (`json.loads(resp.read())`)
- `send_si05_digest()` extracts `result["message_id"]` from that response and passes it to `_write_delivery_log()` instead of the hardcoded `None`
- No change to failure-path logging (a failed send has no message ID to record)

**Acceptance Criteria**
- A successful SI-05 digest send populates a real, non-null `telegram_message_id` in `si05_digest_log`
- Failure-path logging unchanged (still logs `error_message`, `telegram_message_id` remains null on failure)
- Existing retry/backoff behaviour unaffected

---

### BLG-BE-87 — Add duration logging around POST /digest/si05/send's Telegram send call
**Priority:** P3 (Low)
**Type:** Backend Engineering
**Owner:** Head of Backend Engineering
**Source:** ST-21 (EPIC-05, 2026-08-07__release-v8.4), Render-internal-log-based measurement attempt found no duration data exists — 2026-08-08
**Effort:** XS (<1 day)
**Provisional-Target:** TBD

**Problem**
`POST /digest/si05/send`'s only captured Render log line is the default `uvicorn` access-log format (`"POST /digest/si05/send HTTP/1.1" 200 OK`) — client IP, method+path, status, no duration. Confirmed via direct Render Platform API query against production (30-day window, only one matching log line exists at all). This blocks any future Render-internal-log-based latency measurement for this endpoint (the methodology `ST-21`'s own AC calls for, since firing live test calls would spam the real Telegram channel) — there is currently no way to derive timing from logs for any invocation, past or future, without this fix.

**Scope**
- In `si05_digest_service.py::send_si05_digest()`, record a timestamp immediately before the Telegram send call and log elapsed time (e.g. `logger.info("SI-05 digest sent (%d chars, %.0fms)", message_length, elapsed_ms)`) on both the success and failure paths
- No change to retry/backoff behaviour or the `si05_digest_log` table schema — this is additive log output only

**Acceptance Criteria**
- A successful or failed `POST /digest/si05/send` invocation's Render log line includes an elapsed-time value
- Verified against the next real invocation (the following scheduled Sunday 19:00 UTC cron run, or a manual `workflow_dispatch` trigger) — confirm the new field appears in the captured log
- `docs/ops/api_performance_baseline.md` §36 updated with real log-derived timing once available, superseding the interim single-sample proxy measurement

---

### BLG-BE-88 — get_regime_distribution's NULL-exclusion documented behaviour is dead code

**Priority:** P2 (Medium)
**Type:** Backend / Data Correctness
**Owner:** Head of Engineering
**Source:** Agent-mediated PR review (Director of Quality + Product Owner roles), PR #1331, 2026-08-08__release-v8.5 — 2026-08-10
**Effort:** S (~0.5-1d)
**Provisional-Target:** v8.6

**Problem**
`screener_api_contract.md` and `get_regime_distribution()`'s own docstring (`backend/services/screener_batch_service.py`) claim a run where a market's regime failed to resolve (`regime_us`/`regime_uk` NULL) is "excluded from that market's count rather than miscounted as a fabricated regime." Tracing the actual write path (`_fetch_index_regime()` failure handling) shows fetch failures are persisted as a hardcoded `risk_off` value, never NULL — `regime_us`/`regime_uk` are never actually written as NULL via this code path. The NULL-exclusion SQL branch (`COUNT(*) FILTER (...)`) is effectively dead code, and an index-fetch failure is currently silently counted as a real `risk_off` observation — the exact "fabricated regime" the docs claim is avoided.

**Scope**
- Decide: either (a) actually persist NULL on fetch failure so the exclusion logic means what it says, or (b) correct the docstring and `screener_api_contract.md` to state the real behaviour (conservative `risk_off` default, not exclusion)
- Apply the chosen fix/correction

**Acceptance Criteria**
- `get_regime_distribution()`'s documented NULL-handling behaviour matches what the code actually does, verified against a real fetch-failure scenario

---

### BLG-BE-95 — Persist isAiDraft flag on trade_plans for AI-origin display badges
**Priority:** P3 (Low) | **Type:** Backend Engineering | **Owner:** Head of Engineering | **Source:** ST-02 (EPIC-01, v8.6, BLG-FEAT-56) — discovered implementing the Setup Thesis Digest panel's "AI draft" badge requirement — 2026-08-11 | **Effort:** S (~0.5-1d) | **Provisional-Target:** TBD

**Problem**
`TradePlan.js`'s `isAiDraft` flag (tracks whether narrative fields were AI-generated via the "Improve with AI" flow, §5b) is ephemeral client-side form state only (`useState`, cleared on manual edit) — it is never persisted to the `trade_plans` table. This blocks any read-time consumer from showing an "AI draft" badge based on the plan's actual origin, since the flag doesn't survive past the creation-form session. The v8.6 Setup Thesis Digest panel (`trade_plan.md` §10.5, `TradeEntry.js`) had to omit its spec'd "AI draft" badge for exactly this reason — no server-side field exists to read it back from.

**Scope**
- Add an `is_ai_draft` boolean column to `trade_plans` (default `false`)
- Set `true` when a narrative field is populated via "Improve with AI" and not yet manually edited, mirroring the existing client-side clearing rule (`isAiDraft` reset on `setNarrativeField`)
- Wire the Setup Thesis Digest panel (and any other future read surface) to consume it

**Acceptance Criteria**
- `trade_plans.is_ai_draft` persists across sessions and reflects the same origin/clearing semantics as the current client-only flag
- Setup Thesis Digest panel shows the "AI draft" badge per `ux_spec.md` §2 when `is_ai_draft` is true

---

### BLG-BE-96 — Staging verification of ST-03's trade-plan-linkage enforcement, and legacy orphaned-row audit against the new CHECK constraint
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Data Integrity
**Owner:** Head of Engineering; Data Model, Domain & Schema Owner
**Source:** Agent-mediated Data Model, Domain & Schema Owner review of ST-03 (BLG-BE-91, EPIC-02, v8.6) — 2026-08-12
**Effort:** S (~0.5-1d)
**Provisional-Target:** TBD

**Problem**
ST-03 (BLG-BE-91)'s delegation explicitly required "staging-verified" confirmation that trade-plan linkage is enforced as the default entry-flow path — what was actually delivered is unit/router-level test coverage only (mocked DB throughout; no live Postgres reachable in this sandbox). The Data Model, Domain & Schema Owner's sign-off review accepted this as a reasonable substitute for code-correctness verification given the sandbox constraint, but was explicit that it does not satisfy the literal "staging-verified" unblock criterion, and flagged it as an open item rather than silently resolved. Separately, the same review flagged that DS-12's new `trade_plans_active_requires_position_check` CHECK constraint (`NOT VALID`, enforced going-forward only) has an unverified interaction with the 11 known legacy pre-`BLG-BE-46` (v6.8) orphaned rows (`position_id IS NULL`): if any of those 11 rows also happen to carry `status = 'active'` (plausible, since the `POST`/`PUT` gap ST-03 closed existed for their entire pre-fix history), any future `UPDATE` touching that specific row will fail against the new constraint until corrected — no live-DB query confirming or ruling this out was possible in this sandbox.

**Scope**
- On staging (or production, read-only), create a position via the "Start Trade from Plan" flow and confirm the trade plan is linked (`trade_plan_linked: true` in the `POST /portfolio/position` response) as the default path
- Run a one-line query against the live `trade_plans` table: `SELECT id, ticker, status, position_id FROM trade_plans WHERE status = 'active' AND position_id IS NULL;` — confirm 0 rows (expected) or identify/fix any that exist before they can block a future legitimate edit
- Confirm the DS-12 CHECK constraint is actually present and `NOT VALID` on the live table (`SELECT conname, convalidated FROM pg_constraint WHERE conrelid = 'trade_plans'::regclass;`)

**Acceptance Criteria**
- Staging run confirms trade-plan linkage is the enforced default path at position entry
- Live query confirms 0 rows (or any found are fixed) matching `status='active' AND position_id IS NULL`
- DS-12 constraint confirmed present and `NOT VALID` on the live table
- Head of Engineering + Data Model, Domain & Schema Owner sign-off

---

## 6. Operations & Infrastructure Backlog

---

### BLG-OPS-13 — Add remaining pre-v4.6 endpoints to api_performance_baseline.md re-run
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** v2.9 post-ship closure 2026-04-24 (3 endpoints); v3.0 post-ship closure 2026-04-28 OA-v30-01 (5 additional endpoints); v3.1 post-ship closure 2026-05-05 (10 additional endpoints); v3.4 post-ship closure 2026-05-14 (2 additional endpoints); v3.5 post-ship closure 2026-05-15 (2 additional endpoints); v3.9 post-ship closure 2026-05-22 (1 additional endpoint: GET /portfolio/red-flag-journal); v4.6 post-ship closure 2026-05-31 (1 additional endpoint: GET /analytics/behavioural-drift). **Reconciled 2026-08-07** (Infrastructure & Operations Owner, lessons-learnt deferred patch from `2026-08-05__release-v8.3` closure, Friction Item 1) — 21 of the 23 originally-named endpoints are now confirmed present in `docs/ops/api_performance_baseline.md`; retained as an open item for the 1 genuine residual gap plus 1 correction, not retired/merged into `BLG-OPS-133` since a real gap remains.
**Effort:** XS (<0.5d — 1 endpoint remaining)
**Provisional-Target:** Before next performance baseline review

**Problem**
Of the 23 originally-listed endpoints, 21 are now present in `docs/ops/api_performance_baseline.md` (resolved across intervening cycles without this item being updated to reflect it — the stale 24-endpoint scope was still being carried forward unedited as of `v8.2` closure). One (`GET /v1beta1/news`) remains genuinely absent from the baseline. One (`GET /trade-plans/by-ticker/{ticker}`) was never shipped under that path — `docs/reference/openapi.yaml` only ever defines `GET /trade-plans/by-position/{position_id}`, no `by-ticker` sibling route exists — so it is dropped from scope as a stale entry, not a residual gap. **Note:** `GET /v1beta1/news` currently sits inside the misplaced block documented in `BLG-SPEC-116` (nested under `components:` instead of `paths:`) — re-confirm this endpoint's existence and exact path after that structural fix lands, since relocation could in principle change how it's named/grouped.

**Scope**
- Run `GET /v1beta1/news` against staging to obtain p50/p95 latencies and add to `docs/ops/api_performance_baseline.md`
- Re-check after `BLG-SPEC-116` lands that the endpoint's canonical path/shape is unchanged

**Acceptance Criteria**
- `GET /v1beta1/news` has p50 and p95 latency entries in the baseline document, consistent with existing measurement methodology

---

### BLG-OPS-17 — Alpaca API cost monitoring
**Priority:** P3 (Low)
**Type:** Operations / Cost Monitoring
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** ~~Screener live ≥ 60 days (sufficient history to establish a meaningful cost baseline).~~ **Gate cleared 2026-08-08** — Screener shipped v3.0 (2026-04-27, 103 days ago); threshold long since passed.

**Problem**
Alpaca API call volume (paper-positions, orders, account data) is not tracked. After 60 days of screener and research operations, a cost-per-run baseline can be established. Without a baseline, it is impossible to detect cost regressions when new features or higher screener frequency are introduced.

**Scope**
- Instrument Alpaca API call count per endpoint per day
- Log to `api_cost_log` or equivalent structured log
- Daily/weekly aggregate report

**Acceptance Criteria**
- Alpaca API call count logged per endpoint per run
- Aggregate report computable
- Gate condition verified by Infrastructure & Operations Owner before sprint planning

---

### BLG-OPS-18 — Data pipeline cost baseline
**Priority:** P3 (Low)
**Type:** Operations / Cost Monitoring
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-02 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-OPS-17 complete (Alpaca cost monitoring instrumented).

**Problem**
No aggregate data pipeline cost baseline exists covering Alpaca, Yahoo Finance, and news API calls together. Once Alpaca is instrumented (BLG-OPS-17), a combined baseline across all external data dependencies can be produced. Without this, cost anomalies across the pipeline are invisible.

**Scope**
- Aggregate cost baseline: Alpaca + YF + news API per week
- Baseline document filed in `docs/ops/`
- Alert threshold definition: >2× baseline triggers advisory

**Acceptance Criteria**
- Combined pipeline cost baseline document produced
- Alert threshold defined
- Gate condition (BLG-OPS-17 complete) verified before sprint planning

---

### BLG-OPS-19 — External API cost attribution per feature
**Priority:** P3 (Low)
**Type:** Operations / Cost Monitoring
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-03 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-OPS-17 complete (Alpaca cost monitoring instrumented).

**Problem**
External API calls are not attributed to the feature or workflow that triggered them. After BLG-OPS-17 instruments Alpaca, the next step is attributing each API call to the triggering feature (screener run, research view load, trade plan creation). This enables per-feature cost analysis and informs future optimisation decisions.

**Scope**
- Call attribution: tag each outbound API call with the triggering endpoint/feature
- Attribution report: cost breakdown by feature
- Identify top 3 cost contributors

**Acceptance Criteria**
- Each external API call tagged with triggering feature
- Attribution report computable
- Gate condition (BLG-OPS-17 complete) verified before sprint planning

---

### BLG-OPS-20 — Research endpoint cost monitoring
**Priority:** P3 (Low)
**Type:** Operations / Cost Monitoring
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-04 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** ~~PT-02 (Research View) live ≥ 30 days.~~ **Gate cleared 2026-08-08** — PT-02 shipped v3.2 (2026-05-08, 92 days ago); threshold long since passed.

**Problem**
Research view loads trigger multiple downstream API calls (Yahoo Finance OHLCV, earnings, news). The per-session API cost of the research endpoint is not tracked. After 30 days of research view usage, a cost-per-session baseline can be established and anomalies detected.

**Scope**
- Instrument research endpoint: log external API calls triggered per request
- Cost-per-session aggregate (weekly baseline)
- Anomaly detection: sessions with >2× baseline API call count

**Acceptance Criteria**
- Research endpoint API call count logged per session
- Weekly baseline computable
- Gate condition verified by Infrastructure & Operations Owner before sprint planning

---

### BLG-OPS-21 — Arc 2 compute cost review
**Priority:** P3 (Low)
**Type:** Operations / Cost Review
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-05 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped AND 30-day cost baseline exists (BLG-OPS-17 or BLG-OPS-18 complete).

**Problem**
Arc 2 adds screener batch processing, research endpoints, and AI-assisted trade plan features. No compute cost review has been conducted since Arc 1. Once Arc 2 is complete and a 30-day cost baseline is available, a targeted review of Arc 2 compute overhead (CPU, memory, external API cost) should be conducted to inform Arc 3 infrastructure decisions.

**Scope**
- Review compute cost across Arc 2 features against Arc 1 baseline
- Identify top 3 cost drivers
- Produce recommendations for Arc 3 infrastructure planning

**Acceptance Criteria**
- Arc 2 vs Arc 1 compute cost comparison produced
- Recommendations filed
- Gate condition verified before sprint planning

---

### BLG-OPS-23 — Screener performance benchmark
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-07 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-OPS-13 (performance baseline) complete.

**Problem**
Screener batch runs involve 500+ ticker OHLCV fetches. No formal latency benchmark exists for screener run duration (p50/p95 end-to-end). BLG-OPS-13 establishes the API endpoint baseline; this item extends that to the full screener batch run. Without a benchmark, regressions introduced by new screener features (e.g., quality scoring) cannot be detected.

**Scope**
- Benchmark: full screener run duration (p50/p95) against full ticker universe
- Filed in `docs/ops/api_performance_baseline.md`
- Regression alert threshold: >1.5× baseline duration

**Acceptance Criteria**
- Screener run p50/p95 benchmark measured and filed
- Regression threshold defined
- Gate condition (BLG-OPS-13 complete) verified before sprint planning

---

### BLG-OPS-24 — Research endpoint performance benchmark
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-ops-20260421-08 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-OPS-13 (performance baseline) complete AND research endpoint shows regression risk (p95 latency trending up over 30d).

**Problem**
BLG-OPS-13 adds research endpoints to the API performance baseline, but ongoing p95 trending is not monitored. If the research endpoint p95 latency trends upward over 30 days (indicating regression from data volume growth or upstream API changes), a targeted benchmark re-run and root cause investigation is warranted.

**Scope**
- Monthly p95 latency tracking for research endpoint
- Trend report: 30d rolling p95 chart
- Root cause investigation trigger at >1.5× baseline

**Acceptance Criteria**
- Monthly p95 tracking implemented
- Trend report computable
- Gate condition (BLG-OPS-13 + regression trend) verified before sprint planning

---

### BLG-OPS-25 — Automated staging smoke test on deploy/merge (consolidated)
**Priority:** P2 (Medium)
**Type:** Operations / CI/CD
**Owner:** Director of Quality; Infrastructure & Operations Owner
**Source:** IDEA-director-of-quality-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033); consolidates BLG-OPS-100, BLG-OPS-102, BLG-OPS-107, BLG-OPS-119 — the same capability was independently re-proposed across four idea-intake cycles (2026-07-08 through 2026-07-24) without cross-reference to this existing item or each other — merged 2026-07-27, session duplicate-consolidation cleanup
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** None — BLG-OPS-27 (automated staging re-deployment on main merge) shipped v4.0 (2026-05-25); the deploy hook mechanism this item depends on already exists.

**Problem**
Every delivery verification run begins with manual staging health checks, and staging deploys have no automated smoke test — deployment regressions (broken environment, missing env vars, cold-start failures) are caught manually or not until the next deliberate check.

**Scope**
- Smoke test suite: 3–5 critical endpoint health checks (backend health, screener availability, positions endpoint)
- Triggered automatically on both staging deploy and merge to main (the BLG-OPS-27 deploy hook fires on merge, so these are the same trigger in practice)
- Also runs on a scheduled cadence (e.g. weekly), independent of deploy/merge events, to catch environment drift between deploys
- Failure: deploy pipeline reports failure; delivery verification engine advised; alert on scheduled-run failure
- Output: smoke test pass/fail result stored in CI artefacts

**Acceptance Criteria**
- Smoke test suite authored and triggered on staging deploy / merge to main
- Suite covers minimum 3 critical endpoints
- Failure prevents "staging ready" signal from being issued
- Suite also runs on a scheduled cadence and alerts on failure independent of deploy events
- Confirmed to fail correctly on a deliberately-broken staging deploy (dry run)

---

### BLG-OPS-41 — Red flag events table archiving strategy
**Priority:** P2 (Medium)
**Type:** Operations / Data Lifecycle
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260522-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035, 3-cycle cap)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** red_flag_events table 6+ months old (post 2026-11-22).

**Problem**
The red_flag_events table has no defined retention or archiving strategy. As override events accumulate, the table will grow. Without an archiving policy, the table may require unplanned manual intervention. Defining the strategy before the table reaches significant size is operationally prudent.

**Scope**
- Define: retention window (e.g., keep 12 months active; archive older rows to cold storage)
- Define: archiving trigger (size-based vs age-based) and procedure
- Document strategy in ops notes; complement BLG-BE-24 retention policy

**Acceptance Criteria**
- Archiving strategy document produced
- Retention window and trigger defined
- Gate condition (table 6+ months old) verified before commencing

---

### BLG-OPS-48 — ANTHROPIC_API_KEY 6-month scope audit
**Priority:** P2 (Medium)
**Type:** Operations / Security
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Source:** IDEA-cybersecurity-20260601-02 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036)
**Effort:** S (~0.5 day)
**Provisional-Target:** ~v4.9 (date-gated)
**Gate criteria:** No earlier than 2026-11-01 (~6 months after BLG-OPS-36 scope review in v4.2, 2026-05-28)

**Problem**
BLG-OPS-36 (ANTHROPIC_API_KEY scope review) was completed in v4.2 (2026-05-28). Security policy (BLG-OPS-38) requires periodic key scope reviews. 6-month follow-up due ~November 2026 to verify key scope remains minimal and no scope creep has occurred in the API key permissions.

**Scope**
- Review ANTHROPIC_API_KEY permissions against current usage patterns
- Confirm key is not used outside the documented endpoints (generate-thesis, check-daily-cost)
- Verify key rotation has occurred per BLG-OPS-38 policy
- Document review findings

**Acceptance Criteria**
- ANTHROPIC_API_KEY scope confirmed minimal (only documented endpoints)
- Key rotation confirmed per BLG-OPS-38 schedule
- Review findings documented

---

### BLG-SPEC-35 — PO-02 §13 boundary review for AI cross-journal analysis
**Priority:** P1 (High)
**Type:** Governance / §13 Compliance
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PO-02 (Journal Pattern Recognition) sprint planning imminent.

**Problem**
PO-02 (Journal Pattern Recognition) will use AI to analyse cross-journal entries for recurring themes, emotional patterns, and setup types. This is an AI-assisted analysis of trading behaviour — the §13 boundary review must confirm this constitutes display/insight only and does not constitute signal generation or automated advisory. §13 PASS is required before PO-02 sprint planning seals.

**Scope**
- Run §13 checklist against PO-02 story set before sprint planning seals
- Confirm AI analysis output is: display-only, human-reviewed, no automated position recommendations
- Document binding conditions (if any) analogous to IT-06 §13 PASS conditions
- Sign-off recorded in sprint planning artefact

**Acceptance Criteria**
- §13 review completed; PASS or FAIL determination documented
- Binding conditions (if any) recorded
- Gate condition verified before PO-02 sprint planning seals

---

### BLG-SPEC-36 — PO-02 AI output audit schema
**Priority:** P2 (Medium)
**Type:** Spec / Governance
**Owner:** AI Compliance & Governance Officer; Head of Specs Team
**Source:** IDEA-ai-compliance-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** PO-02 (Journal Pattern Recognition) sprint planning imminent.

**Problem**
PO-02 will generate AI output (pattern summaries, theme classifications) using an LLM. Governance policy requires AI-generated content to be traceable to model version, prompt version, and input at time of generation. Designing the audit log schema before sprint planning ensures it is built in from day 1, avoiding retroactive compliance debt.

**Scope**
- Design audit log schema: pattern_id, model_version, prompt_version, journal_ids_included, output_hash, generated_at
- Storage mechanism: append-only table or structured log file
- Retention policy: minimum 90 days
- Schema reviewed by AI Compliance & Governance Officer and Head of Specs Team

**Acceptance Criteria**
- Audit log schema designed and documented
- Storage mechanism defined
- Retention policy specified
- Gate condition verified before sprint planning

---

### BLG-SPEC-44 — SI-02 drift threshold calibration specification
**Priority:** P2 (Medium)
**Type:** Specification / Metrics Definition
**Owner:** Metrics Definitions & Analytics Owner; Head of Specs Team
**Source:** IDEA-metrics-analytics-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038; gate cleared: BLG-GOV-87 shipped v5.0)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 frontend sprint planning triggered; 20+ closed trades confirmed. BLG-GOV-87 re-entry criteria document shipped v5.0 — functional activation gate still pending.

**Problem**
SI-02 backend (shipped v4.6) defines 4 drift metrics (early_entry_rate, momentum_override_rate, losing_streak_sizing, regime_deviation_rate) but does not specify meaningful alert thresholds. Without calibrated thresholds, the frontend display may surface false positives (alert fatigue) or miss genuine drift. Thresholds should be defined before frontend activation.

**Scope**
- Define alert thresholds for each of the 4 drift metrics (e.g., early_entry_rate > 40% = amber, > 60% = red)
- Provide rationale for each threshold (e.g., based on your own historical compliance data, statistical percentiles)
- Define score interpretation guidance for the user-facing display
- Add threshold definitions to metrics_definitions.md (per §12 of that document)

**Acceptance Criteria**
- Threshold calibration specification document produced
- All 4 drift metrics have defined alert levels with rationale
- metrics_definitions.md updated with drift threshold definitions
- Gate condition verified before sprint planning

---

### BLG-SPEC-46 — Arc 4 API contract pre-planning surface area
**Priority:** P3 (Low)
**Type:** Specification / API Contracts
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Source:** IDEA-api-contracts-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-SPEC-35 (PO-02 §13 boundary review) complete. Arc 4 API contract surface area is premature before §13 determines whether PO-02/PO-03 constitute "adaptive logic" or "structured pattern extraction."

**Problem**
PO-02 (journal pattern recognition) and PO-03 (behavioural error taxonomy) will each require new API endpoints. Pre-defining the endpoint surface area (GET /analytics/journal-patterns, classification endpoints) before Arc 4 sprint prevents same-sprint API spec debt analogous to the Arc 5 retroactive contracts filed in v4.1/v4.2.

**Scope**
- Define candidate endpoint names and response shapes for PO-02 and PO-03
- Produce lightweight endpoint surface area document (not full contracts — just paths, methods, response envelopes)
- Input to Arc 4 release planning; pre-authorise contract authoring for named endpoints

**Acceptance Criteria**
- Endpoint surface area document produced for PO-02 and PO-03 APIs
- Reviewed by API Contracts & Documentation Owner and Head of Specs Team
- Gate condition (BLG-SPEC-35 complete) verified before commencing

---

### BLG-SPEC-55 — Arc 4 API contract pre-planning surface area advancement check (gate-conditional)
**Priority:** P3 (Low)
**Type:** Specification / API Contracts
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Source:** IDEA-api-contracts-20260607-02 — Promoted-Backlog rebalance 2026-06-09__scheduled (DL-041)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** PO-02 (Journal Pattern Recognition) sprint planning confirmed imminent — when PO confirms ≥6 months AI-summarised journal entries gate is cleared and PO-02 is entering sprint planning

**Problem**
BLG-SPEC-46 (Arc 4 API surface area) is a gate-conditional spec planning item that was parked until PO-02 sprint planning is imminent (~Oct 2026). When that gate clears, an advancement check should confirm BLG-SPEC-46's scope still reflects the final Arc 4 API surface — the surface may have evolved since BLG-SPEC-46 was authored. This item tracks that confirmation step.

**Scope**
- Review BLG-SPEC-46 against current api_contracts/ documents and openapi.yaml
- Confirm Arc 4 API surface is still accurately captured or produce a revision scope
- Produce brief readiness note: "BLG-SPEC-46 proceed as-is" or list required updates
- Gate: PO-02 sprint planning imminent confirmation by PMO Lead

**Acceptance Criteria**
- BLG-SPEC-46 scope reviewed against current API surface
- Readiness note produced with clear proceed/update decision
- API Contracts & Documentation Owner sign-off
- Gate condition verified

---

### BLG-SPEC-111 — Document GET /test/quick-health and POST /test/rate-limit-scenarios
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** API Contracts & Documentation Owner
**Source:** ST-17 (BLG-QA-94, EPIC-04) quarterly OpenAPI 3-way drift sweep, sprint execution `2026-08-05__release-v8.3` — 2026-08-06
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
`backend/routers/test.py` defines two endpoints, `GET /test/quick-health` and `POST /test/rate-limit-scenarios`, that are undocumented in both `docs/specs/api_contracts/` and `docs/reference/openapi.yaml`. They are internal test-harness routes (not consumed by the frontend or external clients), the same category as the already-documented `POST /test/endpoints` — but these two siblings were never added when that entry was written.

**Scope**
- Document both endpoints in `health_endpoints.md` and `openapi.yaml`, matching the existing `POST /test/endpoints` entry's format
- Or, if documentation is judged unnecessary for internal-only test tooling, explicitly extend the `conventions.md` §11/§13.3 test-endpoint exemption to name both endpoints (currently only `/health`, `/health/detailed`, `/test/endpoints` are named)

**Acceptance Criteria**
- Either both endpoints have a canonical contract + openapi.yaml entry, or both are explicitly named in the conventions.md test-endpoint exemption list
- `scripts/openapi_3way_drift_sweep.py` run clean (0 drift) after the fix

---

### BLG-GOV-26 — Arc velocity tracking dashboard
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** PMO Lead
**Source:** IDEA-governance-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** PT-04 (Setup Quality Score) shipped — Arc 2 velocity history complete.

**Problem**
No arc-level velocity tracking exists. Cycle velocity is tracked per-cycle (cycle_velocity in run_manifest.md), but no aggregate view shows velocity trends across an entire arc. Once Arc 2 is complete (PT-04 shipped), an Arc 2 velocity retrospective would establish baseline expectations for Arc 3 planning.

**Scope**
- Arc velocity report: stories/cycle, epic completion rate, arc-level rolling velocity
- Filed in governance reporting; updated at arc close
- Input to release planning engine for arc-boundary cycles

**Acceptance Criteria**
- Arc 2 velocity report produced at arc close
- Report format reusable for Arc 3+
- Gate condition verified by PMO Lead before sprint planning

---

### BLG-GOV-27 — Cross-arc dependency map
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** PMO Lead; Head of Specs Team
**Source:** IDEA-governance-20260421-02 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** ≥ 3 arcs running concurrently (Arc 3, Arc 4, Arc 5 or later all in active/planned state simultaneously).

**Problem**
Current arcs (Arc 2, Arc 3, Arc 4) have informal dependency tracking (noted in roadmap annotations). If 3 or more arcs are in concurrent active or planned state, cross-arc dependency conflicts become a risk: feature data dependencies, shared backend schema changes, and governance sequencing conflicts all require explicit mapping. Gate ensures effort is only incurred when the complexity warrants it.

**Scope**
- Cross-arc dependency map: for each arc, list upstream arcs (data dependencies) and downstream arcs (consumes output)
- Conflict detection: identify stories across arcs that modify shared resources
- Filed in `claude/strategy/`

**Acceptance Criteria**
- Cross-arc dependency map produced
- Conflicts (if any) documented and escalation plan filed
- Gate condition (≥3 concurrent arcs) verified by PMO Lead before sprint planning

---


### BLG-GOV-29 — Trade plan AI summary audit log
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team; QA Lead
**Source:** IDEA-governance-20260421-04 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** AI trade plan analysis feature scoped and scheduled (i.e., a story exists in the backlog that adds AI-generated trade plan summaries or analysis).

**Problem**
If an AI-assisted trade plan analysis feature is scoped (generating text summaries, recommendations, or signals using an LLM), an audit log is required per governance policy (AI-generated content must be traceable to the model version, prompt version, and input at time of generation). Without a pre-designed audit log schema, retrofitting this after feature delivery creates governance debt.

**Scope**
- Audit log schema: plan_id, model_version, prompt_version, input_hash, output_hash, generated_at
- Storage: append-only table or log file
- Retention policy: minimum 90 days

**Acceptance Criteria**
- Audit log schema designed and documented
- Storage mechanism implemented
- Gate condition (AI trade plan analysis feature scoped) verified by Head of Specs Team before sprint planning

---

### BLG-GOV-68 — Backlog item inter-dependency tracking
**Priority:** P2 (Medium)
**Type:** Governance / Process Enhancement
**Owner:** PMO Lead; Head of Specs Team
**Source:** IDEA-pmo-lead-20260522-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035, 3-cycle cap)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** 20+ concurrent implementation items in a single sprint causing dependency-blocking.

**Problem**
Backlog items have no explicit Blocks/Blocked-by fields. Cross-item dependencies are currently documented via prose in backlog entries (e.g. "Gate: BLG-OPS-36 complete"). As the backlog grows, undiscovered dependencies become sprint-time blockers. A formal inter-dependency field would surface critical path items at sprint planning.

**Scope**
- Add Blocks/Blocked-by field to backlog item format (optional; populated when dependency is known)
- Update sprint planning engine to surface Blocks/Blocked-by chains
- Back-fill critical known dependencies (BLG-OPS-36 → BLG-OPS-37, etc.)

**Acceptance Criteria**
- Field format defined and documented in backlog header conventions
- Sprint planning engine updated to surface dependency chains
- Gate condition (20+ concurrent items with dependency-blocking evidence) verified before commencing

---

### BLG-GOV-71 — Governance engine complexity assessment (gate-conditional)
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Director of HR; PMO Lead
**Source:** IDEA-director-of-hr-20260525-02 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036; terminal 3-cycle disposition)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** Audit overall score drops below 70 OR a step-skip event is formally documented in an audit report.

**Problem**
Governance engine prompts have grown complex over 33 cycles. Without periodic complexity assessment, latent process friction accumulates invisibly. This assessment would identify steps that rarely trigger, candidates for simplification, and produce a governance simplification roadmap for meta-review.

**Scope**
- For each governance engine prompt: count steps, hard gates, and write operations
- Identify steps with documented "never triggered" patterns from lessons_learnt.md history
- Propose candidates for simplification, consolidation, or removal

**Acceptance Criteria**
- Per-engine complexity metrics documented
- Simplification candidates enumerated with rationale
- Gate condition verified before commencing

---

### BLG-GOV-73 — Scheduled rebalance cadence review
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** PMO Lead; Head of Specs Team
**Source:** IDEA-pmo-lead-20260601-02 + IDEA-challenger-20260601-02 (merged) — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Advance at next meta-review cycle (rebalance_cycles_since_meta_review ≥ 3).

**Problem**
10+ scheduled rebalances since 2026-03-24. CPS stable at 1.15. Multiple consecutive scheduled rebalances have had empty Now horizons with no items advancing. The Challenger raised the concern that running full governance process when no strategic decision is pending may produce overhead without proportional value.

**Scope**
- Review scheduled rebalances since last meta-review for value produced (items advanced, horizon movements, CPS changes)
- Assess whether a lightweight mode for no-change-expected cycles could reduce overhead
- Produce recommendation: maintain cadence or propose modification; present at next meta-review

**Acceptance Criteria**
- Value analysis of recent scheduled rebalances documented
- Recommendation produced and presented at next meta-review
- Gate condition (cycles_since_meta_review ≥ 3) verified before commencing

---

### BLG-GOV-74 — AI feature usage quarterly review (BLG-GOV-63 mandate)
**Priority:** P2 (Medium)
**Type:** Governance / Compliance
**Owner:** AI Compliance & Governance Officer; PMO Lead
**Source:** IDEA-ai-compliance-20260601-02 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036; fulfills BLG-GOV-63 mandate)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.10 or first cycle after 2026-08-29
**Gate date:** First review due 2026-08-29 (3 months after v4.0 AI feature ship 2026-05-29)

**Problem**
BLG-GOV-63 (shipped v4.2) requires a quarterly review of the claude_audit_log. First quarterly review due 2026-08-29. Without a backlog item it will be missed.

**Scope**
- Review claude_audit_log for the preceding quarter (v4.0–v4.8 window)
- Assess: total thesis generation requests, model version used, override_rate, cost per use
- Flag anomalies; document findings; file BLG items for any anomalies

**Acceptance Criteria**
- Quarterly audit log review completed; findings documented
- Anomalies (if any) filed as BLG items
- Next review date recorded (2026-11-29)

---

### BLG-OPS-51 — Add GET /analytics/strategy-version-comparison to api_performance_baseline.md (when implemented)
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner; API Contracts & Documentation Owner
**Source:** Post-ship closure 2026-06-01__release-v4.8 — endpoint coverage drift advisory (STEP 6)
**Effort:** S (~0.5 day)
**Provisional-Target:** SI-04 sprint (whenever GET /analytics/strategy-version-comparison is implemented)

**Problem**
v4.8 ST-07 added a placeholder entry for GET /analytics/strategy-version-comparison to openapi.yaml (pre-authored contract; not yet implemented). Once implemented, this endpoint will need p50/p95 latency measurement and an entry in docs/ops/api_performance_baseline.md.

**Scope**
- After SI-04 sprint implements the endpoint: run performance baseline measurement (p50/p95)
- Add measurement to docs/ops/api_performance_baseline.md

**Acceptance Criteria**
- GET /analytics/strategy-version-comparison present in api_performance_baseline.md with p50/p95 values
- Measurement conducted with ≥5 staging samples

---

### BLG-OPS-53 — Application log retention policy expansion (Supabase + claude_audit_log)
**Priority:** P3 (Low)
**Type:** Operations / Data Lifecycle
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Source:** IDEA-infra-ops-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** claude_audit_log table 6+ months old (~Nov 2026, since v4.0 ship 2026-05-22). BLG-OPS-31 (Render log retention policy) shipped v4.7; this extends scope to Supabase query logs and claude_audit_log.

**Problem**
BLG-OPS-31 defined Render log retention. claude_audit_log (shipped v4.0) and Supabase query logs have no defined retention policy. As audit log volume grows, query performance and storage cost may degrade without archiving strategy.

**Scope**
- Define retention period for claude_audit_log (e.g., 12 months rolling)
- Define Supabase query log retention consistent with data privacy obligations
- Define archiving trigger (log volume threshold or time-based)
- Document policy in docs/operations/

**Acceptance Criteria**
- Retention policy document produced covering claude_audit_log and Supabase query logs
- Archiving cadence defined
- Gate condition (6+ months of audit log data) verified before sprint planning

---

### BLG-GOV-84 — Arc 6 gate revision and threshold assessment
**Priority:** P3 (Low)
**Type:** Governance / Product Planning
**Owner:** Product Owner; Challenger; Strategy Rules & System Intent Owner
**Source:** IDEA-product-owner-20260527-02 + IDEA-challenger-20260527-01 — Promoted-Backlog cycle 2026-06-02__scheduled (DL-037; terminal Parked-cycle-2 combined disposition)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** ≥ 50 closed trades (trajectory approaching) — at current ~1–2 trades/month, this is approximately 2026-Q4/2027.

**Problem**
PS-01 (Edge Analysis Dashboard) gate requires 100+ trades with plans and lifecycle data. At current trade frequency (1–2 trades/month), this gate takes 5–8 years to clear. The Challenger has raised (twice) that a meaningful edge analysis may be achievable with 20–30 closed trades with explicit statistical caveats. The Product Owner's Arc 6 minimum viable entry assessment (also raised twice) asks whether the gate calibration is appropriate. Both ideas address the same question: is the 100-trade threshold right? A formal assessment when trade count approaches 50 is the appropriate trigger.

**Scope**
- Formal assessment: at ≥50 closed trades, evaluate whether PS-01 can yield meaningful signal with available history (20–30 qualifying trades as a subset)
- Assess: what statistical confidence is achievable at 30 vs 50 vs 100 trades? Are explicit caveats sufficient to communicate limited confidence?
- Challenge the threshold: if PO decides 30–50 trades is sufficient with caveats, recommend gate revision; document decision in decision_log.md
- §13 check: any gate revision must remain within the "deterministic historical analysis" framework; no predictive claims

**Acceptance Criteria**
- Assessment document produced when ≥50 closed trades confirmed
- Threshold recommendation made (maintain 100-trade gate OR revise with documented caveats)
- PO + Challenger + Strategy Rules Owner sign-off on recommendation
- If gate revised: decision_log.md updated; PS-01 roadmap section updated
- Gate condition (≥50 closed trades approaching) verified before commencing

---

### BLG-GOV-85 — Arc 6 §13 pre-assessment boundary document
**Priority:** P3 (Low)
**Type:** Governance / §13 Compliance Pre-work
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260527-02 — Promoted-Backlog cycle 2026-06-02__scheduled (DL-037; terminal Parked-cycle-2 disposition)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Arc 6 release planning trigger (first sprint planning cycle that includes a PS-01 through PS-05 story).

**Problem**
Arc 6 features (PS-01 through PS-05) are roadmapped with informal §13 compliance notes ("deterministic simulation, §13 COMPLIANT"; "statistical observation, not prediction"). Before Arc 6 sprint planning seals, a formal §13 pre-assessment must consolidate binding conditions for each feature — as was done for SI-01 (8 conditions), IT-06 (4 conditions), SI-04 (6 conditions). PS-03 already has a formal §13 PASS assessment (10 conditions, v4.6). PS-01, PS-02, PS-04, PS-05 need similar pre-assessment documents.

**Scope**
- Formal §13 pre-assessment for PS-01, PS-02, PS-04, PS-05 (PS-03 already complete)
- Each assessment confirms: deterministic calculation only, display-only output, no automated recommendations, no ML/prediction components
- Binding conditions documented per the SI-01/IT-06 pattern
- Strategy Rules & System Intent Owner sign-off required on each assessment

**Acceptance Criteria**
- §13 assessment documents produced for PS-01, PS-02, PS-04, PS-05
- Binding conditions documented for each PASS determination
- Gate condition (Arc 6 release planning trigger) verified before commencing

---

### BLG-GOV-90 — Claude model deprecation monitoring procedure (consolidated)
**Priority:** P3 (Low)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer; Infrastructure & Operations Owner
**Source:** IDEA-ai-compliance-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038); consolidates BLG-GOV-239 — same "track Claude model deprecation on a defined schedule" capability, independently re-proposed as a standalone calendar at the 2026-07-16 idea-intake cycle without cross-reference to this existing item — merged 2026-07-28, session duplicate-consolidation cleanup
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-GOV-74 first quarterly AI feature review completes (due 2026-08-29). Consolidate this procedure definition with the BLG-GOV-74 review action.

**Problem**
BLG-GOV-64 pins the model to claude-3-5-sonnet. Anthropic publishes model deprecation notices. No formal procedure exists for checking deprecation notices on a schedule and triggering a governed sprint story to update the pinned model. BLG-GOV-74 (quarterly AI review, first due 2026-08-29) is the natural integration point for a standard procedure.

**Scope**
- Define quarterly deprecation check procedure: check Anthropic model lifecycle page, compare against pinned model in BLG-GOV-64 policy
- Define trigger: if deprecation notice issued → file P1 sprint story to update pinned model
- Document procedure in docs/governance/ai_model_policy.md or equivalent

**Acceptance Criteria**
- Deprecation monitoring procedure defined and documented
- Procedure integrated with BLG-GOV-74 quarterly review cadence
- Gate condition (BLG-GOV-74 first review complete) verified before sprint planning

---

### BLG-GOV-91 — SI-04 strategy history access security review
**Priority:** P2 (Medium)
**Type:** Governance / Security Review
**Owner:** Cybersecurity & Trust Lead; Strategy Rules & System Intent Owner
**Source:** IDEA-cybersecurity-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038; gate cleared: BLG-GOV-88 shipped v5.0)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-04 sprint planning imminent. BLG-GOV-88 (binding conditions doc) shipped v5.0 — SI-04 remains in Later horizon; gate triggers when SI-04 enters sprint planning.

**Problem**
SI-04 (strategy version comparison) will access historical strategy_rules.md content and link it to trade data. This creates a data access pattern not present in SI-01 through SI-03: querying historical document versions alongside personal trade records. A security pre-assessment confirms whether this pattern introduces any data pattern or access control concerns before sprint planning.

**Scope**
- Assess data access pattern: historical strategy content + trade data linkage
- Determine if any additional access controls or audit logging are required
- Document as security review record per BLG-GOV-31 (security review pattern)
- Cybersecurity & Trust Lead sign-off

**Acceptance Criteria**
- Security review record produced covering SI-04 data access pattern
- PASS or REQUIRES_MITIGATIONS determination with evidence
- Cybersecurity & Trust Lead sign-off recorded
- Gate condition verified before sprint planning

---

### BLG-GOV-95 — strategy_rules.md annual parameter review schedule (consolidated)
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Strategy Rules & System Intent Owner; Product Owner
**Source:** IDEA-strategy-owner-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039); consolidates BLG-GOV-122, BLG-GOV-187 — the same "§11 production parameter review against live trading data" capability was independently re-proposed across two later idea-intake cycles (2026-06-10 and 2026-07-08) without cross-reference to this existing item or each other — merged 2026-07-28, session duplicate-consolidation cleanup
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Displacement:** BLG-GOV-29 (trade plan AI audit log, P3, gate-conditional) deprioritised.

**Gate criteria:** Whichever comes first: ≥ 30 closed trades with ATR-based stop exits in production (sufficient data density to assess parameter appropriateness), OR 12 months elapsed since parameters were last reviewed, OR the annual review cadence date if neither condition has fired sooner.

**Problem**
strategy_rules.md §11 defines production parameters (5× initial ATR, 2× profitable ATR, 10-day grace period, regime gate thresholds). These have never been reviewed against live trading performance data — the system has run on its original parameter settings since inception (last validated at v5.3, BLG-GOV-104, not against realised outcomes). §12.3 requires documented rationale for any parameter change, but there is no scheduled review mechanism to surface whether changes are warranted.

**Scope**
- Define annual parameter review process: PMO Lead adds review to the next roadmap rebalance after the gate clears
- Review actual trading behaviour over the review window against each parameter's assumptions; identify any divergence between documented parameters and actual practice
- Review scope: compare actual trade outcomes against parameter-predicted outcomes for each parameter (does 5× ATR give sufficient breathing room? does 2× ATR lock in enough gain on average?)
- Output: parameter review report; PO + Strategy Rules owner decision: maintain, adjust (with §12.3 rationale), or schedule future review
- If parameters adjusted: follow §12.3 change control (version increment, rationale, consistency across backtests)

**Acceptance Criteria**
- Parameter review process document produced
- Gate condition (≥30 closed trades with stops) verified before review commences
- Product Owner and Strategy Rules & System Intent Owner sign-off on review findings
- If parameters adjusted: strategy_rules.md version increment with §12.3-compliant rationale

---

### BLG-GOV-102 — Arc completion velocity scorecard (gate-conditional)
**Priority:** P3 (Low)
**Type:** Governance / Product Planning Reference
**Owner:** Product Owner; PMO Lead
**Source:** IDEA-product-owner-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Displacement:** BLG-GOV-85 (Arc 6 §13 boundary document, P3, gate-conditional) deprioritised.

**Gate criteria:** Arc 5 fully complete (all five Arc 5 features: SI-01 ✅, SI-03 ✅, SI-05 Phase 1 ✅, SI-02 frontend, SI-04 — all shipped).

**Problem**
With 6 arcs spanning v2.9–v4.0+, there is no single reference document showing arc-level completion status: which arcs are done, which are in progress, which features remain, and what gate conditions are outstanding. As the project moves from Arc 5 toward Arc 6, assembling this picture from multiple sections of current_roadmap.md is time-consuming at each release planning session.

**Scope**
- One-page arc completion scorecard: for each of the 6 arcs, list (a) arc status (Complete/In Progress/Planned), (b) features shipped, (c) features remaining, (d) gate conditions outstanding, (e) earliest realistic activation date
- Filed in docs/product/ or claude/roadmap/
- Updated at each major arc milestone; not a living document requiring cycle-by-cycle updates

**Acceptance Criteria**
- Arc completion scorecard document produced covering all 6 arcs
- Gate condition (Arc 5 fully complete) verified before authoring (ensures Arc 5 data is final)
- Product Owner sign-off

---

### BLG-GOV-103 — Staged verification sprint tracking worksheet (gate-conditional)
**Priority:** P3 (Low)
**Type:** Governance / Process Tool
**Owner:** Director of Quality; PMO Lead
**Source:** IDEA-pmo-lead-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** XS (~1 hour)
**Provisional-Target:** Unscheduled
**Displacement:** BLG-GOV-90 (Claude model deprecation monitoring procedure, P2, gate-conditional) deprioritised.

**Gate criteria:** BLG-GOV-89 (staged verification sprint protocol, shipped v5.1) used 2+ times in practice. First use: v5.1 staged ACs; second use: this staged verification sprint (SI-05 Phase 1 deferred ACs). Gate clears after the v5.1 staged verification sprint is completed.

**Problem**
BLG-GOV-89 (staged verification sprint protocol) defines the pattern. After 2+ uses, a companion tracking worksheet — a simple checklist capturing: which releases have deferred ACs, which ACs per release, their status (pending/verified/signed-off) — would reduce coordination overhead when multiple staged ACs accumulate across releases.

**Scope**
- Produce a single-page tracking worksheet template (Markdown table) for staged verification sprints: columns = Release, AC ID, Description, Status, Evidence, Sign-off Date
- Template filed in docs/operations/ alongside BLG-GOV-89 protocol
- Reviewed by Director of Quality and PMO Lead

**Acceptance Criteria**
- Worksheet template produced and filed
- Gate condition (BLG-GOV-89 used 2+ times) verified before authoring
- Director of Quality and PMO Lead sign-off

---

### BLG-GOV-105 — Arc 6 PS-03 Monte Carlo §13 threshold pre-assessment — ✅ CLOSED (confirmed duplicate, 2026-07-12)
**Priority:** P2 (Medium)
**Type:** Governance / §13 Compliance
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled (before Arc 6 moves from Later to Next)
**Displacement:** BLG-GOV-111 (v5.3 design gate pre-assessment, lower-P) deprioritised.

**Problem**
Arc 6 PS-03 (Monte Carlo simulation) requires a §13 review before sprint planning. The core §13 question — "is Monte Carlo simulation deterministic or predictive?" — can be answered definitively now without knowing implementation details. A pre-assessment scoped to this threshold question de-risks Arc 6 sprint planning entry.

**Scope**
- Assess whether Monte Carlo simulation as described in current_roadmap.md §5 (PS-03 notes) is deterministic (replaying own trade distribution) or predictive (forecasting future outcomes)
- Determine: does PS-03 engage the §13 boundary "Not an ML-based prediction system"?
- Produce a one-page §13 threshold assessment; if PASS (deterministic), note that binding conditions will be defined at full §13 review when Arc 6 moves to Next
- Note: scope is threshold question only — NOT a full §13 review with binding conditions

**Acceptance Criteria**
- §13 threshold assessment produced for PS-03 (deterministic vs predictive question answered)
- PASS/FAIL on the threshold question documented
- Strategy Rules & System Intent Owner sign-off

**Possible duplicate — flagged 2026-07-10 (backlog consistency audit, not yet dispositioned):** This item's threshold question — "is Monte Carlo simulation deterministic or predictive, does PS-03 engage the §13 boundary" — appears to already be answered by `BLG-GOV-45` ("Arc 6 Monte Carlo §13 pre-assessment"), which shipped in v4.6 (2026-05-31, ST-18): PASS, 10 binding conditions, decision doc filed at `docs/product/decisions/arc6_ps03_section13_preassessment.md` (confirmed on disk). This item may have been filed without visibility into that prior work. Not closed here — requires Strategy Rules & System Intent Owner confirmation that BLG-GOV-45 fully supersedes this item before disposition as duplicate/pre-met.

**Confirmed and closed 2026-07-12 (roadmap rebalance 2026-07-12__scheduled, Strategy Rules & System Intent Owner):** Verified `docs/product/decisions/arc6_ps03_section13_preassessment.md` directly — it answers this item's exact threshold question (deterministic vs predictive) for the same feature (PS-03), with a full PASS determination and 10 binding conditions, superseding this item's narrower scope entirely. `BLG-GOV-45` fully supersedes this item. Closed as confirmed duplicate/pre-met — resolves `IDEA-head-of-specs-20260712-01` and `BLG-GOV-202` (see below).

---

### BLG-GOV-119 — Arc 5 delivered value retrospective (gate-conditional)
**Priority:** P3 (Low)
**Type:** Governance / Strategic Review
**Owner:** Product Owner; Strategy Rules & System Intent Owner
**Source:** IDEA-challenger-20260610-01 — Promoted-Backlog rebalance 2026-06-10__scheduled (DL-044)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** SI-04 (strategy version comparison) AND SI-05 Phase 2 both shipped

**Problem**
Arc 5 is functionally near-complete (SI-01/02/03 shipped; SI-04 pre-planned; SI-05 Phase 1 live). Before committing to Arc 6, a retrospective against the original Arc 5 end-state intent would confirm whether the arc is delivering its stated purpose: "making every deviation visible, deliberate, and recorded."

**Scope**
- Review Arc 5 end-state description against delivered features
- Assess whether SI-01/02/03/05 collectively achieve the stated purpose
- Produce a 1-page retrospective document; note gaps or intent drift

**Acceptance Criteria**
- Retrospective document produced and filed
- Gap list (if any) filed as backlog items
- Product Owner + Strategy Rules & System Intent Owner sign-off
- Gate: SI-04 + SI-05 Phase 2 both shipped

---

### BLG-GOV-121 — SI-05 Phase 2 §13 pre-clearance document (gate-conditional)
**Priority:** P2 (Medium)
**Type:** Governance / Strategy Compliance
**Owner:** Strategy Rules & System Intent Owner; Product Owner
**Source:** IDEA-strategy-owner-20260610-02 — Promoted-Backlog rebalance 2026-06-10__scheduled (DL-044)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** 2026-07-04 SI-05 effectiveness review output (BLG-GOV-113) complete AND Phase 2 activation decision made

**Problem**
SI-05 Phase 2 integrates drift signals (SI-02) with the Telegram digest. Before Phase 2 activates, a targeted §13 review should confirm that incorporating drift signals into an automated notification remains compliant with the "not an automated trading system" and "human-in-the-loop" principles. Phase 1 cleared §13 (notification of compliance scores + red flags). Phase 2 adds drift-signal interpretation — this boundary warrants formal pre-clearance.

**Scope**
- Extend the SI-05 Phase 1 §13 review framework to Phase 2 scope
- Confirm: drift signal summary in digest is informational, not prescriptive; no automated action triggered
- Document binding conditions for Phase 2 operation (analogous to IT-06 §13 conditions)

**Acceptance Criteria**
- §13 pre-clearance document produced and filed
- Strategy Rules & System Intent Owner sign-off
- Gate condition verified before Phase 2 sprint planning

---

### BLG-FE-72 — Arc 4 PO-02 journal pattern UX spec (gate-conditional)
**Priority:** P3 (Low)
**Type:** Frontend & UX / Specification
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-frontend-ux-20260608-02 — Promoted-Backlog rebalance 2026-06-10__scheduled (DL-043)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** PO-02 (Journal Pattern Recognition) sprint planning confirmed imminent — PMO Lead confirmation required before commissioning this work

**Problem**
PO-02 (Journal Pattern Recognition) requires displaying cross-entry AI analysis results: recurring themes, emotional patterns, setup types, conditions present at winning vs losing entries. No UX specification exists for how this data should be presented. Before PO-02 enters sprint planning (gate: 6+ months AI journals, ~Oct 2026), a UX spec should be prepared to enable accurate scope definition at sprint planning.

**Scope**
- Define the display patterns for journal theme analysis (list view? heatmap? timeline?)
- Specify how patterns are surfaced: by entry count, by theme frequency, by outcome correlation
- Define empty state and gate-not-met state (< 6 months of journals)
- Produce a canonical frontend spec for the Journal Pattern Recognition UI component

**Acceptance Criteria**
- Frontend spec document produced: data display patterns, empty states, component architecture
- Spec reviewed and signed off by Head of UX & Design and Frontend Specs & UX Documentation Owner
- Gate: PMO Lead confirms PO-02 sprint planning is imminent before this story begins

---

### BLG-SPEC-56 — Arc 4 API contract pre-authoring (PO-02/03/04)
**Priority:** P3 (Low)
**Type:** Spec / Pre-authoring
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260619-01 — Promoted-Backlog rebalance 2026-06-19__scheduled (DL-049)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled (pre-work before PO-02 gate ~2026-10)

**Problem**
PO-02 (journal pattern recognition), PO-03 (behavioural error taxonomy), and PO-04 (reflection/outcome correlation) are currently gate-blocked (~2026-10). However, the API contract surface for these features can be pre-authored now, reducing execution risk and spec bottlenecks when the gate clears. Pre-authoring allows the Specs team to identify ambiguities, surface §13 questions, and establish endpoint naming conventions before sprint planning pressure exists.

**Scope**
- Draft API contract stub files for PO-02, PO-03, PO-04 feature endpoints in `docs/specs/api_contracts/`
- Flag any §13 boundary questions for BLG-SPEC-35 (§13 pre-assessment, P1, active)
- No implementation; contract stubs only

**Acceptance Criteria**
- Stub contract files exist for PO-02, PO-03, PO-04 endpoint groups in `docs/specs/api_contracts/`
- Each stub includes at minimum: endpoint path, HTTP method, brief description, key request/response fields
- BLG-SPEC-35 §13 pre-assessment reviewed or updated if new boundary questions arise

---

### BLG-SPEC-57 — Data model v3 pre-definition for Arc 4 journal intelligence
**Priority:** P3 (Low)
**Type:** Spec / Pre-authoring
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260619-02 — Promoted-Backlog rebalance 2026-06-19__scheduled (DL-049)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled (pre-work before PO-02 gate ~2026-10)

**Problem**
Arc 4 journal intelligence (PO-02/03/04) will require data model changes. Pre-defining the schema additions now (while the architecture is in working memory post-Arc 3 delivery) reduces execution risk and produces a migration plan that can be reviewed before sprint planning pressure exists.

**Scope**
- Define data model additions for PO-02/03/04 features (new tables or columns for pattern recognition, error taxonomy, outcome correlation)
- Document as a pre-definition document in `docs/specs/` or `docs/data_models/`
- No migration SQL; schema design only

**Acceptance Criteria**
- Data model pre-definition document produced covering Arc 4 schema additions
- BLG-SPEC-56 Arc 4 API contracts reference the pre-defined model where applicable
- Reviewed by Head of Specs Team and Infrastructure & Operations Owner

---

### BLG-QA-59 — Arc 4 E2E test strategy pre-design (PO-02/03/04)
**Priority:** P3 (Low)
**Type:** Quality Assurance / Pre-design
**Owner:** Director of Quality
**Source:** IDEA-director-of-quality-20260619-01 — Promoted-Backlog rebalance 2026-06-19__scheduled (DL-049)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled (pre-work before PO-02 gate ~2026-10)

**Problem**
Arc 4 AI-driven features (PO-02/03/04) introduce Playwright test challenges not present in current arcs: AI response non-determinism, journal pattern recognition latency, cost implications of running AI calls in CI. Pre-designing the test strategy before sprint planning avoids last-minute patching of the CI pipeline during delivery.

**Scope**
- Define Playwright test strategy for Arc 4 features: which ACs require Playwright vs unit tests vs staging-only verification
- Define mocking approach for AI API calls in CI (extend existing mock harness)
- Document in `docs/specs/qa/` or `docs/operations/`

**Acceptance Criteria**
- Arc 4 E2E test strategy document produced
- Mocking approach for PO-02/03/04 AI calls defined and consistent with existing BLG-QA-37 Playwright mock strategy
- Reviewed by Director of Quality

---

### BLG-GOV-137 — API contract version tagging for all api_contracts documents
**Priority:** P3 (Low)
**Type:** Governance Process / Spec Quality
**Owner:** Head of Specs Team; API Contracts & Documentation Owner
**Source:** IDEA-head-of-specs-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Tooling assessment confirming version tagging adds drift detection value not already covered by `quality_gate.yml` OpenAPI validation.

**Problem**
API contract documents in `docs/specs/api_contracts/` do not carry a version field. When a contract is amended (endpoint added, field type changed), there is no audit trail of which version was in force when a sprint was planned. Version tagging creates a lightweight reference that enables contract consumers to identify changes.

**Scope**
- Add `version:` field to each api_contracts document (start at v1.0 for all existing docs)
- Define version bump rules: patch for additive changes, minor for breaking changes
- Update checklist for new endpoint authoring to include version bump step

**Acceptance Criteria**
- All api_contracts documents carry a `version:` field
- Version bump rules documented
- Gate condition verified before sprint planning

---

### BLG-GOV-138 — Sprint velocity trend alert in run_manifest (rolling 3-cycle drop)
**Priority:** P3 (Low)
**Type:** Governance Process / Metrics
**Owner:** PMO Lead; Infrastructure & Operations Owner
**Source:** IDEA-pmo-lead-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** velocity_metrics.md path discrepancy resolved (file currently at `claude/cycles/velocity_metrics.md` instead of `claude/roadmap/velocity_metrics.md` — see DL-057 friction items).

**Problem**
The roadmap_prompt.md reads velocity_metrics.md but does not auto-surface a warning when the rolling 3-cycle velocity falls below 0.90. PMO must manually compare values and raise the concern. An explicit alert rule in the run_manifest generation step ensures degrading velocity is visible without manual tracking.

**Scope**
- Add rule to roadmap_prompt.md STEP 1.1: if rolling 3-cycle average velocity < 0.90, surface "Velocity Trend Advisory" in run_manifest header
- Rule documents the threshold, current value, and whether the advisory is advisory or hard gate

**Acceptance Criteria**
- Rule added to roadmap_prompt.md per §6 governance checklist (version bump, OPERATIONAL_GUIDE update, prompt_change_log entry)
- Gate condition (velocity_metrics.md path resolved) verified before sprint planning

---

### BLG-GOV-139 — Regression impact analysis at sprint planning
**Priority:** P3 (Low)
**Type:** Governance Process / Quality
**Owner:** Director of Quality; QA Lead
**Source:** IDEA-director-of-quality-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Tooling approach identified — cross-reference methodology between changed files and Playwright coverage map assessed (automated script vs manual checklist approach).

**Problem**
When sprint planning seals scope, there is no step to cross-reference the changed files against existing Playwright coverage. A regression could be introduced in a file that has Playwright coverage but whose coverage is not triggered by the specific code path being changed. A lightweight impact analysis would surface this risk at planning time.

**Scope**
- Define methodology: compare sprint story file scope against `tests/e2e/` coverage map
- Produce a "coverage gap report" template: stories × files × test coverage status
- Integrate as an advisory step in sprint_planning_prompt.md STEP 3 or STEP 4

**Acceptance Criteria**
- Methodology document produced; approach decision (automated vs manual) recorded
- Gate condition verified before sprint planning entry
- If integrated into sprint_planning_prompt.md: all §6 governance checklist steps completed

---

### BLG-GOV-140 — AI chat advisory §13 quarterly self-audit checklist
**Priority:** P2 (Medium)
**Type:** Governance Process / §13 Compliance
**Owner:** Strategy Rules & System Intent Owner; AI Compliance & Governance Officer
**Source:** IDEA-strategy-owner-20260626-02 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.3

**Gate criteria:** First review due 2026-09-24 (90 days post-v6.2 ship 2026-06-25). Quarterly cadence thereafter.

**Problem**
v6.2 AI chat advisor and daily briefing are now live. §13 requires AI advisory outputs to remain advisory-only and not cross into automated decision-making. Periodic self-audit confirms this boundary is maintained as prompts and response handling evolve. Without a scheduled review, §13 compliance depends on individual vigilance rather than a governed cadence.

**Scope**
- Author §13 self-audit checklist document covering: output advisory language confirmation, no-automated-action verification, disclaimer visibility check, prompt injection risk review
- Schedule first review 2026-09-24; quarterly cadence thereafter
- Owner: Strategy Rules & System Intent Owner; co-reviewer: AI Compliance & Governance Officer

**Acceptance Criteria**
- Checklist document produced and filed
- First review date scheduled (2026-09-24)
- Product Owner and Strategy Rules owner sign-off

---

### BLG-GOV-141 — AI model output logging completeness audit
**Priority:** P2 (Medium)
**Type:** Governance Process / §13 Compliance
**Owner:** AI Compliance & Governance Officer; Infrastructure & Operations Owner
**Source:** IDEA-ai-compliance-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.3

**Gate criteria:** Schedule within 90 days of v6.2 ship (by 2026-09-24).

**Problem**
v6.2 AI features (briefing, chat) should be logging all AI responses with model ID, prompt hash, and response length per AI governance policy. A completeness audit verifies the logging is in place and complete. Without this audit, log completeness is assumed rather than verified.

**Scope**
- Review claude_audit_log (or equivalent) for completeness: all POST /ai/daily-briefing and POST /ai/chat responses logged
- Verify fields: model_id, prompt_hash, response_length, timestamp
- If gaps found: file remediation items
- Schedule review by 2026-09-24

**Acceptance Criteria**
- Audit completed before 2026-09-24
- Logging completeness confirmed or gaps filed as remediation backlog items
- AI Compliance Officer sign-off

---

### BLG-GOV-142 — AI feature ROI assessment at 3-month post-ship mark
**Priority:** P2 (Medium)
**Type:** Governance Process / Value Assessment
**Owner:** Challenger; FinOps & Resource Architect; Product Owner
**Source:** IDEA-challenger-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** 2026-09-24 (90 days post-v6.2 ship). Assess: adoption rate of AI briefing and chat features, cost per use (Anthropic API cost / sessions), and whether usage data justifies continued investment.

**Problem**
v6.2 AI features have a per-use cost (Anthropic API call for each briefing and chat interaction). Without a formal ROI assessment at 3 months, there is no trigger to reconsider the feature investment if adoption is low or costs are disproportionate. The assessment is a formal governance checkpoint, not a presumption of cancellation.

**Scope**
- Assess: AI briefing usage rate (sessions/week), AI chat usage rate (questions/week), cost-per-session
- Compare against: value hypothesis from v6.2 release planning (trader intelligence value)
- Output: continue / sunset / modify recommendation with rationale
- Product Owner decision authority

**Acceptance Criteria**
- Assessment document produced by 2026-09-24
- Recommendation with rationale produced
- Product Owner decision recorded

---

### BLG-GOV-143 — OpenAPI completeness validation in CI (endpoint count reconciliation)
**Priority:** P3 (Low)
**Type:** Governance Process / CI
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Source:** IDEA-api-contracts-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Coverage methodology assessment confirming this complements (not duplicates) the existing OpenAPI drift detection in `quality_gate.yml`.

**Problem**
The existing `quality_gate.yml` drift detection checks `openapi.yaml` for new endpoints mentioned in contract files. BLG-GOV-134 adds advisory CI annotation. This item proposes a complementary check: validate that `openapi.yaml` covers 100% of routes in `backend/routers/`. These are distinct checks (forward vs backward coverage). Gate: confirm no duplication before implementing.

**Scope**
- Assess current coverage gap between quality_gate.yml (contract → openapi) and a hypothetical route scan (routes → openapi)
- If gap confirmed: author CI step to scan `backend/routers/` for `@router.[get|post|put|delete]` and cross-reference against openapi.yaml paths
- Gate condition assessment first; CI implementation only if gap confirmed

**Acceptance Criteria**
- Coverage gap assessment document produced
- If gap confirmed: CI step implemented as advisory (non-blocking, analogous to BLG-GOV-134)
- Gate condition verified before implementation

---

### BLG-GOV-144 — Agent role charter annual review schedule (consolidated)
**Priority:** P3 (Low)
**Type:** Governance Process / HR
**Owner:** Director of HR
**Source:** IDEA-director-of-hr-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057); consolidates BLG-GOV-182, BLG-GOV-199, BLG-GOV-236 — the same "periodic role-charter freshness review" capability was independently re-proposed across three later idea-intake cycles (2026-07-08 through 2026-07-15) without cross-reference to this existing item or each other — merged 2026-07-28, session duplicate-consolidation cleanup
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Time-gated — first review due 2027-06-26 (annual cadence from first filing). A lighter-weight spot-check may also be run at any 10-cycle interval in the interim (per the absorbed BLG-GOV-236 proposal), without waiting for the full annual date.

**Problem**
Agent role charter files (`claude/agents/*.md`) define role responsibilities and decision authorities. As the governance system evolves, role definitions may become stale — including drift against current tooling and practice (e.g. `gh` CLI usage, current write-scope conventions). Without a scheduled review cadence, charter drift accumulates silently. An annual review, with a lighter interim spot-check, ensures each role definition remains current.

**Scope**
- Author an annual review procedure for all `claude/agents/*.md` charter files
- Schedule first review: 2027-06-26
- Procedure: review each charter for accuracy and continued relevance to current tooling/practice; propose amendments through Head of Specs Team; record in prompt_change_log.md
- Optional lighter interim spot-check every 10 cycles, flagging any staleness found as a follow-up ahead of the next full annual review

**Acceptance Criteria**
- Annual review procedure documented
- First review date: 2027-06-26 recorded
- Director of HR sign-off

---

### BLG-GOV-145 — Database connection pool sizing review for AI endpoints
**Priority:** P3 (Low)
**Type:** Governance Process / Operations Assessment
**Owner:** Head of Engineering; Infrastructure & Operations Owner
**Source:** IDEA-head-of-engineering-20260626-01 — Backlog-gate-conditional; rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** ~~30+ days AI endpoint usage observation post-v6.2 ship (by 2026-07-25). v6.2 AI endpoints make additional DB reads; pool sizing should be reviewed under real load.~~ **Gate cleared 2026-08-08** — v6.2 shipped 2026-06-25; 44 days of AI endpoint usage observation now available, past the 30-day threshold.

**Problem**
v6.2 added POST /ai/daily-briefing and POST /ai/chat, both of which read from the database (portfolio state, trade history for context). Supavisor connection pool configuration was set before AI endpoints existed. Under sustained AI endpoint load, the pool may be undersized. A review at 30 days confirms the pool is sized correctly or identifies adjustment needed.

**Scope**
- Review current Supavisor pool configuration (connection count, timeout settings)
- Cross-reference with AI endpoint DB query volume (from logs or monitoring)
- Identify whether pool size adjustment is warranted
- Document findings; file implementation item if adjustment needed

**Acceptance Criteria**
- Pool configuration review document produced
- Findings: "no change needed" or specific adjustment filed as a separate item
- Gate condition (30+ days usage) verified before review commences

---

### BLG-GOV-149 — AI response caching evaluation for morning briefing
**Priority:** P3 (Low)
**Type:** Governance Process / Architecture Assessment
**Owner:** Backend Engineering Patterns Owner; FinOps & Resource Architect
**Source:** IDEA-backend-engineering-20260626-01 — Promoted-Backlog rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Problem**
POST /ai/daily-briefing makes an Anthropic API call on every request. If the same briefing is requested multiple times in the same trading day, each call incurs API cost and latency. A caching evaluation assesses whether same-day caching is technically feasible and whether the staleness risk (briefing should reflect the day's market data) outweighs the cost benefit.

**Scope**
- Evaluate caching feasibility: cache key options (date, user, market open/close state), cache invalidation triggers
- Assess staleness risk: how often does market data change in a way that would materially change the briefing during a trading day?
- Produce evaluation document: recommend cache (with approach) or no-cache (with rationale)
- No implementation commitment; evaluation output only

**Acceptance Criteria**
- Evaluation document produced covering cache key design, staleness risk, and cost-benefit analysis
- Recommendation: cache / no-cache with rationale
- Backend Engineering Owner and FinOps sign-off

---

### BLG-QA-63 — Automated accessibility testing (axe-core) in Playwright CI
**Priority:** P3 (Low)
**Type:** QA / Accessibility
**Owner:** Director of Quality; Head of Frontend Engineering
**Source:** IDEA-director-of-quality-20260619-02 (IW-20260619-01) — Backlog-gate-conditional; rebalance 2026-06-24__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** [TBD — gate-conditional]
**Gate criteria:** Arc 5 fully complete (all SI features shipped) — accessibility testing added after frontend feature set stabilises

**Problem**
The Playwright E2E suite provides functional coverage but no accessibility validation. axe-core (via @axe-core/playwright) can be added to the existing Playwright setup to surface WCAG 2.1 AA violations in CI without blocking test runs.

**Scope**
- Install @axe-core/playwright
- Add a dedicated accessibility spec (tests/e2e/accessibility.spec.js) that visits each major page (Dashboard, Positions, Signals, Screener, Watchlist, Risk, Research, Reports, SystemStatus) and runs axe analysis
- Report violations as CI warnings (non-blocking initially); convert to hard failure after a clean baseline is established

**Acceptance Criteria**
- AC-01: axe-core runs on all major pages in CI (advisory, non-blocking)
- AC-02: Zero critical (level A) violations on any page at time of implementation
- AC-03: Violation report surfaced as CI annotation on PRs

---

### BLG-OPS-76 — Enhanced health check with external dependency verification
**Priority:** P3 (Low)
**Type:** Operations / Observability
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260619-02 (IW-20260619-01) — Backlog-gate-conditional; rebalance 2026-06-24__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** [TBD — gate-conditional]
**Gate criteria:** BLG-OPS-25 (automated staging smoke test) complete AND ≥3 external dependency failures observed in production logs

**Problem**
GET /health returns only internal service health (database connectivity, scheduler status). External dependency status (Alpaca API reachability, Anthropic API reachability, Yahoo Finance fallback) is not surfaced in the health check, making degraded-run detection reactive rather than proactive.

**Scope**
- Add optional `?extended=true` query param to GET /health
- Extended check: attempt lightweight connectivity test for each external dependency (Alpaca: GET /v2/clock; Anthropic: no-op; Yahoo Finance: HEAD check)
- Return dependency status map in health response
- No latency regression on default (non-extended) health check

**Acceptance Criteria**
- AC-01: GET /health?extended=true returns a `dependencies` object with status for each external dependency
- AC-02: GET /health (no param) remains unchanged in response shape and latency
- AC-03: Degraded dependency status visible in `/system-status` page

---

### BLG-OPS-77 — Data provider diversity risk assessment and failover strategy
**Priority:** P3 (Low)
**Type:** Operations / Risk
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Source:** IDEA-challenger-20260619-01 (IW-20260619-01) — Backlog-gate-conditional; rebalance 2026-06-24__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** [TBD — gate-conditional]
**Gate criteria:** BLG-OPS-71 (system threat model) complete — data provider risk will be enumerated in the threat model

**Problem**
All market data (OHLCV, signals, news) is sourced exclusively from Alpaca and Yahoo Finance. No documented failover strategy exists for a scenario where either provider becomes unavailable for an extended period. The risk has been accepted at current scale but has not been formally assessed.

**Scope**
- Produce a data provider risk assessment document (docs/operations/data_provider_risk_assessment.md): enumerate current dependencies, failure modes, estimated impact per provider loss, and mitigation options
- Identify any quick-win failover paths (e.g. Yahoo Finance as sole fallback if Alpaca unavailable)
- Document accepted risk and conditions under which a more robust failover should be re-evaluated

**Acceptance Criteria**
- AC-01: data_provider_risk_assessment.md produced covering all active external data providers
- AC-02: Failure modes and impact documented per provider
- AC-03: Accepted risk statement signed off by Infrastructure & Operations Owner and FinOps & Resource Architect

---


### BLG-GOV-154 — API contract deprecation marker convention
**Priority:** P3 (Low)
**Type:** Governance / API Design
**Owner:** API Contracts & Documentation Owner
**Source:** IDEA-api-contracts-20260702-02 (IW-20260702-01) — Promoted-Backlog; rebalance 2026-07-02__scheduled
**Provisional-Target:** TBD
**Effort:** S (~0.5 day)

**Problem**
No formal process exists for marking an API contract's endpoint as deprecated once its backing implementation is retired. BLG-BE-40 (v6.4) removed a deprecated-table read path but the affected contract sections were updated ad hoc rather than via a defined convention.

**Scope**
- Define a `**Deprecated:**` marker convention for `## METHOD /path` headings in `docs/specs/api_contracts/`
- Document in the API contracts style guide / openapi.yaml preamble

**Acceptance Criteria**
- Deprecation marker convention documented
- Reviewed by Head of Specs Team

---

### BLG-GOV-156 — Base44 prompt template versioning
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Base44 Frontend Prompt Owner
**Source:** IDEA-base44-frontend-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** ≥3 Base44 prompt draft revisions within a single release cycle (current iteration frequency does not warrant versioning overhead).

**Problem**
No versioning exists to track which version of the Base44 generation prompt produced each delivered component. At current low iteration frequency this is not yet a problem, but the gate defines a concrete trigger for when it would become one.

**Scope**
- Lightweight per-revision log (date, summary of change) appended to the Base44 prompt draft file
- No tooling required — a changelog section within the existing prompt file

**Acceptance Criteria**
- Changelog section added once gate condition is met
- Gate condition (≥3 revisions/cycle) verified before commencing

---

### BLG-QA-71 — Playwright fixture isolation tooling
**Priority:** P3 (Low)
**Type:** QA / Test Infrastructure
**Owner:** Director of Quality
**Source:** IDEA-director-of-quality-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** First empirical Playwright fixture-isolation failure observed in CI (no such failure has occurred to date).

**Problem**
No test data fixtures or state-reset mechanism exists between Playwright runs. No empirical fixture-isolation failure has occurred — the gate exists to avoid building tooling for a problem not yet demonstrated.

**Scope**
- Fixture reset mechanism between Playwright test runs
- Applied once a real isolation failure is observed

**Acceptance Criteria**
- Fixture isolation tooling implemented once gate condition met
- Gate condition (demonstrated failure) verified before commencing

---

### BLG-SPEC-62 — Open Positions panel spec backfill
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-frontend-specs-20260702-01 (IW-20260702-01) — Promoted-Backlog; rebalance 2026-07-02__scheduled
**Provisional-Target:** TBD
**Effort:** S (~0.5 day)

**Problem**
BLG-FEAT-54 (Open Positions panel, v6.4) shipped with a UX spec (`docs/design/2026-07-02__release-v6.4/open-positions-panel/ux_spec.md`) but no corresponding entry was backfilled into the canonical `docs/specs/frontend/pages/strategy_benchmark.md` page spec, leaving the page spec incomplete relative to what shipped.

**Scope**
- Backfill Panel 0 (Open Positions) into `docs/specs/frontend/pages/strategy_benchmark.md`
- Cross-reference the existing UX spec and API contract

**Acceptance Criteria**
- `strategy_benchmark.md` page spec includes Panel 0 documentation
- Reviewed by Frontend Specifications & UX Documentation Owner

---

### BLG-SPEC-63 — Spec coverage gap detection script design
**Priority:** P3 (Low)
**Type:** Spec Debt / Tooling
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** Head of Specs Team completes a script-design scoping decision (static route diff vs frontend spec inventory approach).

**Problem**
No automated check compares frontend page specs against deployed routes to detect coverage gaps. The scoping approach (static diff vs inventory-based) has not yet been decided.

**Scope**
- Scope and select an implementation approach
- Build a lightweight script to flag routes with no corresponding spec file (or vice versa)

**Acceptance Criteria**
- Scoping decision recorded
- Script implemented and run at least once with findings documented

---

### BLG-SPEC-65 — AI interaction history data model
**Priority:** P3 (Low)
**Type:** Spec Debt / Data Model
**Owner:** Data Model & Domain Schema Owner
**Source:** IDEA-data-model-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** Same gate as BLG-FEAT-55 — §13 review opened and passed for chat persistence AND AI adoption window clears ~2026-07-25.

**Problem**
Companion spec item to BLG-FEAT-55 (chat persistence). §13-compliant schema design for persisting user chat sessions must not precede the boundary review itself.

**Scope**
- §13-compliant schema design, co-developed with BLG-FEAT-55
- No implementation ahead of the §13 review passing

**Acceptance Criteria**
- Schema spec produced only after §13 review passes
- Gate condition verified before commencing

---

### BLG-SPEC-66 — AI chat conversation persistence spec
**Priority:** P3 (Low)
**Type:** Spec Debt / Frontend Spec
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-frontend-specs-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Same §13 review gate as BLG-FEAT-55/BLG-SPEC-65.

**Problem**
Companion frontend spec item to BLG-FEAT-55/BLG-SPEC-65 — persisting and displaying chat session history. Authoring this spec ahead of the §13 boundary decision risks rework or discard.

**Scope**
- Frontend spec for session list and resume-conversation UX, authored only once the §13 gate clears

**Acceptance Criteria**
- Spec produced only after §13 review passes
- Gate condition verified before commencing

---

### BLG-OPS-84 — Annual data provider cost comparison review
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260626-01 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Annual cadence — first review due ≥2027-06-25.

**Problem**
No scheduled review compares current data provider (Yahoo Finance, Alpaca) costs against alternatives. Annual cadence is appropriate; the gate simply establishes when the first review is due.

**Scope**
- Cost/feature comparison of current vs alternative data providers
- Recommendation: retain or switch

**Acceptance Criteria**
- Review conducted and documented at gate date
- FinOps & Resource Architect sign-off

---

### BLG-OPS-85 — Compute cost trending by feature area
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260626-02 (IW-20260626-01) — Promoted-Backlog, 3-cycle hard cap; rebalance 2026-07-02__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** BLG-OPS-74 (Anthropic API cost logging) ships.

**Problem**
No view partitions Render dyno compute cost by feature area. Meaningful cost trending depends on the per-call cost logging BLG-OPS-74 will provide — building this ahead of that data source would have nothing to trend.

**Scope**
- Partition compute cost by feature area (AI endpoints, screener, core CRUD) once BLG-OPS-74 data is available

**Acceptance Criteria**
- Cost trending view implemented and populated
- Gate condition (BLG-OPS-74 shipped) verified before sprint planning

---

### BLG-FEAT-61 — Screener-to-watchlist promotion friction audit
**Priority:** P3 (Low)
**Type:** Product Feature / UX Research
**Owner:** Product Owner
**Source:** IDEA-product-owner-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** A user-reported friction signal on the DS-07 promotion flow, or an observed drop in promotion-to-watchlist conversion rate.

**Problem**
DS-07 (screener → watchlist promotion) has been unchanged since v3.0 with no reported usage issue. Auditing it now would be speculative.

**Scope**
- Review promotion flow usage once a friction signal exists
- Recommend UX changes if warranted

**Acceptance Criteria**
- Audit conducted and documented only after gate signal observed

---

### BLG-FEAT-62 — Trade plan template presets by setup type
**Priority:** P3 (Low)
**Type:** Product Feature
**Owner:** Product Owner
**Source:** IDEA-product-owner-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** ≥20 closed trades captured post-PT-04 (2026-06-23) with sufficient `setup_type` diversity to justify presets (at least 3 distinct setup types with ≥3 trades each).

**Problem**
PT-04 (Setup Quality Score) is live, but trade volume since its gate clearance is too low to know which setup-type presets would actually be useful.

**Scope**
- Analyse `setup_type` distribution once gate clears
- Design preset templates for the most common setup types

**Acceptance Criteria**
- Preset design only commences after gate condition confirmed

---

### BLG-GOV-171 — Spec staleness scan across owning code paths
**Priority:** P3 (Low)
**Type:** Governance / Spec Debt
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** A staleness-threshold definition (e.g. "spec unedited N releases while its code path changed") is authored first — this item is the scan itself, not the threshold definition.

**Problem**
No demonstrated spec-drift incident motivates this yet, and no threshold exists to define "stale."

**Scope**
- Author a staleness threshold, then run a one-off scan of specs against their owning code paths

**Acceptance Criteria**
- Threshold defined before scan is run
- Scan report produced identifying any specs exceeding the threshold

---

### BLG-GOV-172 — Governance prompt cross-reference integrity check
**Priority:** P3 (Low)
**Type:** Governance
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Opportunistic — run at the next scheduled lifecycle audit (`run audit`, every 3 cycles) or upon discovery of a broken cross-reference, whichever comes first.

**Problem**
No evidence yet of a broken cross-reference between governance prompts, but none has been checked systematically either.

**Scope**
- Scan all `claude/system/*.md` cross-references for validity, bundled into the next scheduled `run audit` pass

**Acceptance Criteria**
- Check performed alongside next lifecycle audit; findings (if any) filed as backlog items

---

### BLG-GOV-173 — Escalation SLA dashboard
**Priority:** P3 (Low)
**Type:** Governance / Tooling
**Owner:** PMO Lead
**Source:** IDEA-pmo-lead-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** Open escalation volume grows to ≥3 concurrent open escalations (current baseline: 0) — below that, existing manual tracking is sufficient.

**Problem**
Escalation volume is currently zero; a dashboard has no data to justify its build cost yet.

**Scope**
- Build a simple SLA-tracking view once escalation volume justifies it

**Acceptance Criteria**
- Dashboard built only after gate condition confirmed

---

### BLG-QA-75 — Playwright flake-rate tracking (consolidated)
**Priority:** P3 (Low)
**Type:** QA / Test Infrastructure
**Owner:** Director of Quality
**Source:** IDEA-director-of-quality-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled; consolidates BLG-QA-80 (flaky Playwright test tracker) and BLG-QA-87 (Playwright flake tracking log) — the same underlying capability was re-proposed across the 2026-07-08 and 2026-07-10 idea-intake cycles without cross-reference to this existing item — merged 2026-07-27, session duplicate-consolidation cleanup
**Effort:** S (~1 day) for the lightweight quarantine list; CI-pipeline-integrated flake-rate tracking (gated, see below) is a larger follow-on effort
**Provisional-Target:** Unscheduled
**Gate criteria:** A lightweight quarantine list/log has no gate and can be built now (per BLG-QA-80/87's original proposal). Full CI-pipeline-integrated flake-rate tracking remains gated on the first demonstrated flaky-test incident (a test that fails intermittently without a code change) — building that fuller tooling ahead of any observed flakiness would be premature.

**Problem**
Occasionally-flaky Playwright tests are re-run ad hoc with no tracking of which tests flake, how often, or why. Intermittent CI failures are currently indistinguishable from confirmed defects in QA evidence logs, and there is no visibility into whether flake rate is worsening.

**Scope**
- Maintain a quarantine list / flake log now: test name, first-flagged date, flake count, whether a re-run passed, re-enable criteria
- Once a first flaky-test incident is confirmed: add flake-rate tracking to the CI pipeline itself (gated follow-on)

**Acceptance Criteria**
- Quarantine list / log created; any currently-known flaky test logged
- CI-pipeline flake-rate tracking built only after the gate condition (first flaky-test incident) is confirmed

---

### BLG-QA-76 — QA evidence cross-link audit
**Priority:** P3 (Low)
**Type:** QA / Governance
**Owner:** Director of Quality
**Source:** IDEA-director-of-quality-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Opportunistic — bundle into the next scheduled lifecycle audit, or run on discovery of a dangling DoQ claim.

**Problem**
No evidence yet of a dangling (unlinked/broken) DoQ sign-off claim, but none has been checked systematically.

**Scope**
- Scan `qa_evidence_*.md` files for DoQ claims lacking a valid evidence link, bundled with the next `run audit` pass

**Acceptance Criteria**
- Check performed alongside next lifecycle audit; findings (if any) filed as backlog items

---

### BLG-OPS-88 — Render dyno right-sizing review
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Bundle with the existing scheduled 90-day AI cost review (due 2026-09-24) — no standalone signal yet indicates the current dyno tier is mismatched.

**Problem**
The 2 AI endpoints are only 8 days live as of this idea's submission; no cost/performance signal yet indicates a right-sizing need.

**Scope**
- Review dyno tier alongside the 2026-09-24 AI cost review

**Acceptance Criteria**
- Review conducted at or after the 2026-09-24 gate date

---

### BLG-OPS-89 — Anthropic API budget alert threshold calibration
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** The existing `POST /ai/check-daily-cost` alert (shipped v4.1) produces a first false positive or false negative.

**Problem**
The existing cost alert has not misfired since shipping; recalibrating its threshold now would be speculative.

**Scope**
- Recalibrate the alert threshold once a false positive/negative is observed

**Acceptance Criteria**
- Recalibration only performed after gate condition confirmed

---

### BLG-OPS-90 — Staging environment drift detector
**Priority:** P2 (Medium) — escalated from P3, 2026-07-28, roadmap rebalance `2026-07-28__scheduled` (gate cleared, see below)
**Type:** Operations / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** TBD
**Gate criteria:** ~~A second occurrence of a staging/production configuration drift incident (first occurrence: BLG-OPS-82, a one-off missing-deploy issue).~~ **Gate cleared 2026-07-28** — commit `e9c73f58` ("[GOVERNANCE] Fix stale What's New panel — trigger staging redeploy on changelog.md changes") is a confirmed second occurrence of the same drift class: a runtime-read file changed in the repo without triggering a staging redeploy (Render dashboard-only build-path filter invisible to repo grep), producing stale served content exactly as BLG-OPS-82 did. Identified via `IDEA-infra-ops-20260728-01` (IW-20260728-01); disposition: idea resolved directly by this gate-status update rather than filed as a separate backlog row (register Status → Promoted-Added).

**Problem**
BLG-OPS-82 was originally treated as a single one-off incident. A second, independently-caused instance of the same underlying pattern (deploy-path filters that are invisible to a repo-level search, so a runtime-read file's change doesn't trigger the redeploy a reviewer would expect) has now occurred, confirming this is a recurring drift class rather than a one-off.

**Scope**
- Build automated drift detection between staging and production config/build-path coverage, informed by both incidents (BLG-OPS-82: missing-deploy; this one: dashboard-only path filter)

**Acceptance Criteria**
- Tooling built and covers both confirmed incident shapes; Infrastructure & Operations Owner sign-off

---

### BLG-OPS-91 — Deploy rollback runbook dry-run
**Priority:** P3 (Low)
**Type:** Operations
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** After the next real production deploy that uses the BLG-OPS-80 rollback runbook.

**Problem**
The rollback runbook (BLG-OPS-80) is authored but has not yet been exercised against a real production deploy.

**Scope**
- Perform a dry-run (or live use) of the runbook at the next production deploy

**Acceptance Criteria**
- Dry-run performed and runbook gaps (if any) documented after the next deploy

---

### BLG-GOV-174 — Skill-Silo Alert historical trend chart
**Priority:** P3 (Low)
**Type:** Governance / Tooling
**Owner:** PMO Lead
**Source:** IDEA-challenger-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Adoption of a second Skill-Silo escalation tier (BLG-GOV-176a / companion idea IDEA-challenger-20260702-01, Advanced this cycle — see `cycle_record.md` STEP 5) — if a second tier is adopted, this chart becomes part of its supporting dashboard; if not adopted, defer indefinitely.

**Problem**
The underlying data already exists across `workforce_capacity.md` and `decision_log.md` cycle entries; a chart is a presentation nice-to-have, not new capability, and its value depends on whether a second escalation tier is adopted.

**Scope**
- Build a historical trend chart of the rolling Skill-Silo percentage, contingent on the companion escalation-tier decision

**Acceptance Criteria**
- Built only if the companion decision (STEP 5, this cycle) adopts a second tier

---

### BLG-SPEC-67 — OpenAPI example-response completeness sweep
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** API Contracts & Documentation Owner
**Source:** IDEA-api-contracts-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** Opportunistic documentation debt — bundle with the next scheduled lifecycle audit.

**Problem**
No evidence gaps in `openapi.yaml` example responses have caused an actual integration problem; this is opportunistic hygiene, not urgent.

**Scope**
- Sweep `docs/reference/openapi.yaml` for endpoints missing example responses, bundled with the next `run audit` pass

**Acceptance Criteria**
- Sweep performed alongside next lifecycle audit; gaps (if any) filed as backlog items

---

### BLG-GOV-175 — Base44 prompt draft changelog
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Base44 Frontend Prompt Owner
**Source:** IDEA-base44-frontend-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Base44 prompt draft revision frequency increases to a point where informal tracking becomes error-prone (e.g. ≥3 revisions to the same prompt draft within a single sprint).

**Problem**
Prompt revision frequency remains low; a formal changelog/versioning process is not yet warranted.

**Scope**
- Introduce a lightweight changelog for Base44 prompt drafts once revision frequency justifies it

**Acceptance Criteria**
- Changelog introduced only after gate condition confirmed

---

### BLG-BE-43 — Trade plan field usage audit
**Priority:** P3 (Low)
**Type:** Backend / Data
**Owner:** Data Model & Domain Schema Owner
**Source:** IDEA-data-model-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Arc 4 PO-02 (Journal Pattern Recognition) design phase begins (gated to ~2026-10-20, 6+ months AI-summarised journal data).

**Problem**
This audit would directly inform Arc 4 PO-02/PO-03 design, but running it ahead of that design phase risks auditing fields that later change.

**Scope**
- Audit actual usage of trade plan fields once PO-02 design phase begins

**Acceptance Criteria**
- Audit conducted only after gate condition (PO-02 design phase start) confirmed

---

### BLG-BE-44 — Signal write-path schema consolidation
**Priority:** P3 (Low)
**Type:** Backend / Refactor
**Owner:** Data Model & Domain Schema Owner
**Source:** IDEA-data-model-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** ~~BLG-SEC-02's 3-path sanitisation fix (shipped v6.4) has run in production for ≥30 days with no incident (clears ~2026-08-01).~~ **Gate cleared 2026-08-08** — 37 days in production since v6.4 (2026-07-02) with no incident on record.

**Problem**
BLG-SEC-02 just shipped a 3-path sanitisation fix to the signal write path; consolidating that code now, before it has stabilised in production, risks compounding an unproven change with a refactor.

**Scope**
- Consolidate the 3 signal write paths into a single validated path once the sanitisation fix has proven stable

**Acceptance Criteria**
- Refactor only commences after gate condition (30-day stability window) confirmed

---

### BLG-GOV-176 — Facilitator workload note
**Priority:** P3 (Low)
**Type:** Governance / HR
**Owner:** Director of HR
**Source:** IDEA-director-of-hr-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Facilitator workload is reported as a bottleneck in any cycle's lessons learnt or escalation record.

**Problem**
No signal currently indicates Facilitator workload is a bottleneck; formal tracking is not yet warranted.

**Scope**
- Produce a workload note/assessment once a bottleneck signal is reported

**Acceptance Criteria**
- Assessment produced only after gate condition confirmed

---

### BLG-FEAT-63 — P&L report AI narrative cost estimate
**Priority:** P3 (Low)
**Type:** Product Feature / FinOps
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Same AI-adoption gate as BLG-FEAT-59 (AI-assisted monthly P&L narrative) — clears ~2026-07-25.

**Problem**
This cost estimate directly feeds BLG-FEAT-59, which is itself gated on the AI-adoption window; estimating cost ahead of that gate is premature.

**Scope**
- Produce a cost estimate for AI-generated P&L narrative once the adoption window clears

**Acceptance Criteria**
- Estimate produced only after gate condition confirmed

---

### BLG-BE-45 — Trade cost field completeness check
**Priority:** P3 (Low)
**Type:** Backend / Data Quality
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** Opportunistic — bundle with the next scheduled lifecycle audit.

**Problem**
No evidence yet of missing `trade_costs` values; this is a data-quality hygiene check, not an urgent fix.

**Scope**
- Check completeness of `trade_costs` fields across closed trades, bundled with the next `run audit` pass

**Acceptance Criteria**
- Check performed alongside next lifecycle audit; gaps (if any) filed as backlog items

---

### BLG-QA-77 — Playwright suite runtime trend
**Priority:** P3 (Low)
**Type:** QA / Test Infrastructure
**Owner:** Head of Engineering
**Source:** IDEA-head-of-engineering-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** CI suite runtime is reported as a bottleneck (e.g. blocking rapid iteration or exceeding a defined CI time budget).

**Problem**
CI suite runtime has not been reported as a bottleneck at the current spec-file count; trend tracking now would be premature.

**Scope**
- Add runtime trend tracking to CI once runtime is reported as a bottleneck

**Acceptance Criteria**
- Tracking added only after gate condition confirmed

---

### BLG-OPS-92 — Dependency update review
**Priority:** P2 (Medium)
**Type:** Operations / Security Hygiene
**Owner:** Head of Engineering
**Source:** IDEA-head-of-engineering-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** A new CVE or deprecation warning surfaces on a project dependency, OR the next quarterly hygiene cadence (~2026-10-06, 3 months post v4.0 starlette remediation).

**Problem**
No known CVE or deprecation warning is currently outstanding since the v4.0 starlette remediation; a full review now would be opportunistic rather than urgent.

**Scope**
- Full dependency update review triggered by either a new CVE/deprecation signal or the quarterly cadence, whichever comes first

**Acceptance Criteria**
- Review conducted at or after the gate condition (signal or cadence date)

---

### BLG-FE-90 — Open Positions panel visual consistency check
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Head of UX & Design
**Source:** IDEA-head-of-ux-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** A visual inconsistency in the Open Positions panel (BLG-FEAT-54, shipped v6.4) is reported.

**Problem**
BLG-FEAT-54 shipped with Head of UX & Design input already incorporated at design-gate time; no visual inconsistency has been reported since.

**Scope**
- Review and correct any reported visual inconsistency once one surfaces

**Acceptance Criteria**
- Review conducted only after a specific inconsistency is reported

---

### BLG-GOV-177 — DoQ sign-off audit spot-check
**Priority:** P3 (Low)
**Type:** Governance / QA
**Owner:** QA Lead
**Source:** IDEA-qa-lead-20260702-02 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** A non-compliant DoQ sign-off is found, OR bundle with the next scheduled lifecycle audit.

**Problem**
Every recent cycle has shipped Verified with zero deviations; no evidence yet of a non-compliant DoQ sign-off.

**Scope**
- Spot-check DoQ sign-off compliance, bundled with the next `run audit` pass

**Acceptance Criteria**
- Spot-check performed alongside next lifecycle audit; findings (if any) filed as backlog items

---

### BLG-QA-78 — Test data fixture staleness check
**Priority:** P3 (Low)
**Type:** QA / Test Infrastructure
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260702-01 (IW-20260702-01) — Backlog (gate-conditional), 3-cycle hard cap; rebalance 2026-07-06__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** A test failure is attributed to a stale test fixture.

**Problem**
No test failures have been attributed to stale fixtures since v6.4's signal/security changes; a staleness check now would be speculative.

**Scope**
- Check test data fixtures for staleness once a failure is attributed to one

**Acceptance Criteria**
- Check conducted only after gate condition confirmed

---

### BLG-BE-48 — Structured logging correlation-ID propagation across FastAPI request lifecycle
**Priority:** P3 (Low)
**Type:** Backend / Observability
**Owner:** Backend Engineering Patterns Owner
**Source:** IDEA-backend-engineering-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Log lines from a single request cannot currently be correlated across service boundaries (e.g. a signal-generation request that also calls the AI service) — debugging multi-step requests requires manual timestamp correlation.

**Scope**
- Add a request-scoped correlation ID (middleware-generated or accepted via header), included in all log lines emitted during that request

**Acceptance Criteria**
- Correlation ID present in logs for at least 2 representative multi-step endpoints
- Documented in `backend_engineering_patterns.md`

---

### BLG-BE-49 — Down-migration rollback verification tests
**Priority:** P3 (Low)
**Type:** Backend / Data Integrity
**Owner:** Data Model & Domain Schema Owner
**Source:** IDEA-data-model-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Schema migrations are tested forward (apply) but not backward (rollback) — a bad migration in production has no verified rollback path.

**Scope**
- Add rollback tests for the 5 most recent schema migrations, confirming `down()` (or equivalent) restores the prior schema state cleanly

**Acceptance Criteria**
- 5 migrations have passing rollback tests
- Pattern documented for future migrations

---

### BLG-GOV-178 — Quarterly AI output sampling audit (consolidated)
**Priority:** P3 (Low)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer
**Source:** IDEA-ai-compliance-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled; consolidates BLG-GOV-197, BLG-GOV-251 — the same "recurring sampled review of AI output against the §13 boundary" capability was independently re-proposed across two later idea-intake cycles (2026-07-10 and 2026-07-24) without cross-reference to this existing item or each other — merged 2026-07-28, session duplicate-consolidation cleanup
**Effort:** S (~0.5 day per quarter)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
AI output (thesis generation, chat, daily briefing) has no recurring compliance sampling — only ad hoc review during feature work. As prompts and models evolve over time, outputs could drift from §13's determinism/no-prediction boundary without a scheduled check to catch it.

**Scope**
- Sample 10 random AI outputs per quarter; check against §13.2 boundary language (no autonomous-sounding directives, advisory framing preserved) and for determinism/no-prediction drift as prompts/models evolve

**Acceptance Criteria**
- First quarterly sample conducted and findings (if any) filed as backlog items

---

### BLG-GOV-179 — Local pre-commit lint for OpenAPI contract completeness
**Priority:** P3 (Low)
**Type:** Governance / Tooling
**Owner:** API Contracts & Documentation Owner
**Source:** IDEA-api-contracts-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The `openapi.yaml` completeness check currently only fires at PR/CI time — a local pre-commit lint would catch omissions before push, reducing CI churn.

**Scope**
- Pre-commit hook scanning `docs/specs/api_contracts/*.md` for new `## METHOD /path` headings without a matching `openapi.yaml` entry, mirroring the existing CI gate's logic

**Acceptance Criteria**
- Hook catches at least the same class of omission as the CI gate, locally, before commit

---

### BLG-SPEC-68 — Deprecation lifecycle policy for removed/renamed endpoints
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** API Contracts & Documentation Owner
**Source:** IDEA-api-contracts-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
No documented policy exists for how an endpoint is deprecated (sunset header, changelog entry, removal timeline) — the current process is ad hoc.

**Scope**
- Author a short policy doc: sunset-header convention, minimum deprecation window, changelog entry format

**Acceptance Criteria**
- Policy doc authored and referenced from `api_contracts` documentation index

---

### BLG-GOV-180 — Base44 prompt versioning changelog
**Priority:** P3 (Low)
**Type:** Governance / Tooling
**Owner:** Base44 Frontend Prompt Owner
**Source:** IDEA-base44-frontend-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Base44 frontend scaffold prompts change over time with no changelog — regressions from a prompt change are hard to trace.

**Scope**
- Create a changelog file tracking Base44 prompt versions and what changed

**Acceptance Criteria**
- Changelog created; first entry backfilled from the most recent known prompt change

---

### BLG-GOV-181 — Base44 component regeneration diff review checklist
**Priority:** P3 (Low)
**Type:** Governance / QA
**Owner:** Base44 Frontend Prompt Owner
**Source:** IDEA-base44-frontend-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
When a Base44-generated component is regenerated, there's no checklist to catch silent regressions (e.g. dropped props, changed class names) before merge.

**Scope**
- Short checklist: diff review points to check when a Base44 component is regenerated

**Acceptance Criteria**
- Checklist authored and referenced from the Base44 frontend prompt owner's charter

---

### BLG-SEC-11 — API key rotation drill
**Priority:** P3 (Low)
**Type:** Security / Operations
**Owner:** Cybersecurity & Trust Lead
**Source:** IDEA-cybersecurity-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The API key rotation runbook has never been exercised end-to-end — its first real use would be during an actual incident, the worst time to discover a gap.

**Scope**
- Exercise the rotation runbook for one non-critical key; document any gaps found

**Acceptance Criteria**
- Drill completed; runbook corrected if any step failed

---

### BLG-OPS-94 — Data retention policy for AI audit log tables
**Priority:** P3 (Low)
**Type:** Operations / Data Management
**Owner:** Data Model & Domain Schema Owner
**Source:** IDEA-data-model-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
`gemini_audit_log` and the Claude audit log table grow without a retention policy — unbounded growth over a multi-year horizon.

**Scope**
- Define a retention window (e.g. 12–24 months) and an archival/deletion procedure

**Acceptance Criteria**
- Policy documented; first cleanup pass (if any rows exceed the window) executed or explicitly deferred with rationale

---

### BLG-GOV-183 — Onboarding template for new agent role charters
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Director of HR
**Source:** IDEA-director-of-hr-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Adding a new agent role charter currently means copying and adapting an existing one with no explicit template — inconsistent header/section coverage risk.

**Scope**
- Author a template charter file with required sections annotated

**Acceptance Criteria**
- Template authored and referenced from `claude/agents/` documentation

---


### BLG-QA-81 — Visual regression baseline snapshots (consolidated: contrast-sensitive + chart-heavy components)
**Priority:** P2 (Medium)
**Type:** QA / Visual Testing
**Owner:** Director of Quality
**Source:** IDEA-director-of-quality-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled; consolidates BLG-QA-118 — same capability (Playwright visual-regression baseline snapshots), independently re-proposed for a second component class at the 2026-07-24__scheduled rebalance without cross-reference to this existing item — merged 2026-07-28, session duplicate-consolidation cleanup; priority raised P3→P2 to match cluster max
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None — Arc 5/contrast remediation work (v6.6/v6.7) now stable; a good time to baseline before further drift accumulates.

**Problem**
No visual regression baseline exists for the components remediated in v6.6/v6.7's contrast work, nor for chart-heavy components (Performance Analytics, Strategy Benchmark) — a future change could silently reintroduce a contrast regression or a chart layout/rendering regression with no automated catch.

**Scope**
- Capture baseline screenshots for the highest-risk contrast-sensitive components; wire into CI visual diff (if tooling supports it) or a manual comparison checklist
- Capture baseline snapshots for the highest-value chart-heavy components (Performance Analytics, Strategy Benchmark) using existing Playwright visual-regression tooling

**Acceptance Criteria**
- Baselines captured for at least the components touched by `BLG-FE-87/88/89`
- Baselines captured for at least one chart-heavy component end-to-end as proof of pattern

---


### BLG-OPS-95 — Render hosting cost trend dashboard
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Render hosting cost is reviewed monthly ad hoc with no trend visualisation — harder to spot a cost trajectory shift early.

**Scope**
- Simple monthly cost-vs-request-volume trend chart, sourced from existing monthly review data

**Acceptance Criteria**
- Trend chart built with at least 3 months of historical data points

---

### BLG-OPS-96 — Anthropic API cost per-feature attribution
**Priority:** P3 (Low)
**Type:** Operations / FinOps
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Anthropic API cost is tracked in aggregate — no breakdown by feature (thesis generation vs. chat vs. daily briefing), making it hard to identify which feature drives cost.

**Scope**
- Tag cost-tracking records by feature/endpoint; produce a per-feature monthly breakdown

**Acceptance Criteria**
- Monthly cost breakdown available by feature for at least 1 reporting cycle

---

### BLG-OPS-97 — CI pipeline build-time reduction via parallelized test jobs
**Priority:** P3 (Low)
**Type:** Operations / CI
**Owner:** Head of Engineering
**Source:** IDEA-head-of-engineering-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Backend and frontend test suites currently run sequentially in CI, extending PR feedback time as the suites grow.

**Scope**
- Parallelize independent CI test jobs (backend/frontend at minimum)

**Acceptance Criteria**
- Measured CI wall-clock time reduced for a representative PR

---

### BLG-OPS-98 — Quarterly dependency minor-version upgrade cadence policy
**Priority:** P3 (Low)
**Type:** Operations / Engineering
**Owner:** Head of Engineering
**Source:** IDEA-head-of-engineering-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~0.5 day per quarter)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Dependency minor-version upgrades happen reactively (security patch, feature need) rather than on a cadence — small upgrades accumulate into larger, riskier jumps.

**Scope**
- Define a quarterly minor-version upgrade window; first pass applies safe minor bumps across `requirements.txt`/`package.json`

**Acceptance Criteria**
- Policy documented; first quarterly pass completed

---

### BLG-SPEC-69 — Spec debt dashboard
**Priority:** P3 (Low)
**Type:** Spec Debt / Tooling
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
All `BLG-SPEC-*` items must currently be found by grepping `backlog.md` — no single view shows spec debt volume or age.

**Scope**
- Generate a single-page summary of all open `BLG-SPEC-*` items with age since filing

**Acceptance Criteria**
- Dashboard produced; refreshable at future `groom backlog` runs

---

### BLG-SPEC-70 — Canonical spec cross-reference linter
**Priority:** P3 (Low)
**Type:** Spec Debt / Tooling
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** M (~2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
A canonical spec document can become orphaned (no backlog item or code references it) with no automated way to detect this.

**Scope**
- Script scanning `docs/specs/**` for files not referenced by any backlog item or codebase comment

**Acceptance Criteria**
- Linter run once; any orphaned specs found are triaged (kept, merged, or archived)

---

### BLG-GOV-184 — Canonical "win rate" definition consistency confirmation
**Priority:** P3 (Low)
**Type:** Governance / Metrics
**Owner:** Metrics Definitions & Analytics Canonical Owner
**Source:** IDEA-metrics-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
"Win rate" is surfaced in at least 4 places (dashboard, P&L report, drift analytics, journal) with no confirmation they all use the same calculation.

**Scope**
- Confirm calculation consistency across all 4 surfaces against `metrics_definitions.md`

**Acceptance Criteria**
- Consistency confirmed, or discrepancy filed as a correctness backlog item

---

### BLG-GOV-185 — Changelog section in metrics_definitions.md
**Priority:** P3 (Low)
**Type:** Governance / Tooling
**Owner:** Metrics Definitions & Analytics Canonical Owner
**Source:** IDEA-metrics-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
`metrics_definitions.md` has no changelog — formula version bumps are not tracked, making it hard to know when a metric's calculation last changed.

**Scope**
- Add a changelog section; backfill known recent formula changes

**Acceptance Criteria**
- Changelog section added with at least the most recent known change recorded

---

### BLG-GOV-186 — §13 boundary illustrative examples appendix
**Priority:** P3 (Low)
**Type:** Governance / Documentation
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Score-4/5 debates require citing specific §13 clauses, but §13 itself has no worked examples — every debate re-derives what "engaging a boundary" looks like in practice.

**Scope**
- Add an appendix to `strategy_rules.md` (or a companion doc) with 1–2 concrete right/wrong examples per §13 sub-clause

**Acceptance Criteria**
- Appendix authored, reviewed by Strategy Rules & System Intent Owner

---

### BLG-GOV-188 — Sprint Velocity Trend Chart
**Priority:** P3 (Low)
**Type:** Governance / Process Visibility
**Owner:** PMO Lead
**Source:** IDEA-pmo-lead-20260708-01 (IW-20260708-01), resubmission of IDEA-pmo-lead-20260619-02 (originally rejected at `2026-06-24__scheduled`, 3-cycle hard cap) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1–2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None — revival condition (velocity_metrics.md populated ≥5 cycles/2 rebalances) confirmed Met 2026-07-08 (49 rows across 8 rebalance-tracked cycles)

**Problem**
Sprint velocity trend (delivered stories per sprint, U/G/D/P breakdown, delivery rate) requires manual changelog/velocity_metrics.md analysis to see at rebalance time — no visualisation exists.

**Scope**
- Chart of velocity trend across the last 10 rebalance-tracked cycles, sourced from `velocity_metrics.md`

**Acceptance Criteria**
- Chart built, showing at least delivered-story-count and U/G/D/P split per cycle over the available history

---

### BLG-QA-82 — Consolidate 3 overlapping SignalCard Playwright specs
**Priority:** P3 (Low)
**Type:** QA / Test Infrastructure
**Owner:** QA Lead
**Source:** IDEA-qa-lead-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
3 Playwright spec files cover overlapping SignalCard scenarios, accumulated incrementally across features (allocation_insufficient, badge colours, etc.) — redundant coverage slows the suite without adding confidence.

**Scope**
- Audit the 3 spec files; consolidate into 1 with no coverage loss

**Acceptance Criteria**
- Consolidated into 1 spec file; full scenario coverage confirmed retained; suite runtime reduced

---

### BLG-QA-83 — Standalone axe-core accessibility CI scan
**Priority:** P3 (Low)
**Type:** QA / Accessibility
**Owner:** QA Lead
**Source:** IDEA-qa-lead-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None — independent of `BLG-QA-63`'s "Arc 5 fully complete" gate; an automated axe-core scan doesn't require the full frontend feature set to stabilise first, unlike the fuller accessibility-testing programme `BLG-QA-63` describes.

**Problem**
No automated accessibility scanning exists in CI at all — `BLG-QA-63` gates a fuller programme behind Arc 5 completion, but a basic axe-core pass could run today at low cost.

**Scope**
- Add axe-core to the existing Playwright CI run for the highest-traffic pages; fail (or warn, initially) on critical violations

**Acceptance Criteria**
- axe-core scan running in CI for at least 3 pages; results visible in CI output

---

### BLG-QA-84 — Publish backend test coverage report to PR comments
**Priority:** P3 (Low)
**Type:** QA / CI
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Backend test coverage is only visible by running pytest locally with coverage flags — no visibility in the PR review flow, so coverage regressions can slip through unnoticed.

**Scope**
- Add a CI step posting a coverage summary (and delta vs. base branch, if feasible) as a PR comment

**Acceptance Criteria**
- Coverage summary posted automatically on the next PR after this ships

---

### BLG-QA-85 — Contract test suite: openapi.yaml vs. actual route behaviour
**Priority:** P3 (Low)
**Type:** QA / API Contracts
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260708-02 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The existing OpenAPI drift gate only checks that a `## METHOD /path` heading has a matching `openapi.yaml` entry (presence check) — it does not verify the entry's schema (request/response shape) actually matches route behaviour.

**Scope**
- Contract tests for a representative sample of endpoints, asserting actual response shape matches the documented `openapi.yaml` schema

**Acceptance Criteria**
- Contract tests passing for at least 5 representative endpoints; documented pattern for extending coverage

---

### BLG-GOV-189 — Governance overhead audit (PMO/spec time per shipped story)
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Challenger; PMO Lead
**Source:** IDEA-challenger-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The Product Value Ratio and Skill-Silo alerts both measure governance overhead indirectly (via story classification) — no direct measurement exists of actual PMO/spec time cost per shipped user story, which would ground future governance-cadence decisions (e.g. `IDEA-pmo-lead-20260708-02`, debated this cycle) in harder evidence.

**Scope**
- Retrospective estimate of PMO/spec/governance effort vs. shipped-story count over the last 10 cycles, using available run_manifest/cycle_record artefacts as a proxy

**Acceptance Criteria**
- Estimate produced; findings inform the next cycle-cadence discussion if one recurs

---

### BLG-GOV-191 — Spec debt aging report
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** Idea intake IW-20260710-01 (IDEA-head-of-specs-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
There is no standing report surfacing which `BLG-SPEC-*` items are approaching the 2-cycle-without-story-assignment advisory threshold defined in `release_planning_prompt.md` STEP 1.1 — it currently only fires reactively when a release plan happens to scan for it.

**Proposed solution**
Add a lightweight scan (reusable at `groom backlog` or release planning time) that lists spec-debt items by cycles-aged, surfaced proactively rather than only at the moment a release plan checks.

---

### BLG-GOV-192 — Governance prompt cross-reference sweep cadence
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** Idea intake IW-20260710-01 (IDEA-head-of-specs-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
§14 OPERATIONAL_GUIDE.md version drift is currently only caught opportunistically (e.g. by the `governance-drift` skill when invoked, or when a friction item happens to surface it) rather than on a fixed cadence.

**Proposed solution**
Schedule a periodic (e.g. every-3-cycle, alongside the meta-review) explicit governance-drift check rather than relying on incidental discovery.

---

### BLG-GOV-193 — Escalation SLA breach dry-run test
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** PMO Lead
**Source:** Idea intake IW-20260710-01 (IDEA-pmo-lead-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The `BLOCKED_SLA_BREACH` 72-hour notice path (`shared_standards.md` §4) has never been exercised end-to-end in this repository's history — it is untested governance machinery.

**Proposed solution**
Construct a deliberate dry-run (e.g. a synthetic escalation with a backdated timestamp) to confirm the breach notice actually fires and halts as designed.

---

### BLG-QA-88 — DoQ sign-off template freshness check
**Priority:** P3 (Low)
**Type:** QA / Process
**Owner:** Director of Quality
**Source:** Idea intake IW-20260710-01 (IDEA-director-of-quality-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The `record-visual-qa` skill's evidence format was defined against a staging practice that may have since evolved; no periodic check confirms the template still matches actual practice.

**Proposed solution**
Periodically (e.g. every few releases) confirm the DoQ sign-off template and the skill that populates it still reflect current staging sign-off practice.

---

### BLG-GOV-194 — §13 boundary language clarity pass — AI journal summarisation
**Priority:** P3 (Low)
**Type:** Governance / Strategy
**Owner:** Strategy Rules & System Intent Owner
**Source:** Idea intake IW-20260710-01 (IDEA-strategy-owner-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
`strategy_rules.md` §13's "deterministic scoring" boundary language pre-dates the AI journal summarisation feature; it has not been explicitly re-read against that feature to confirm the language still functions as an unambiguous boundary.

**Proposed solution**
Strategy Rules & System Intent Owner re-reads §13 against the AI journal summarisation feature specifically and confirms (or clarifies) the boundary language remains unambiguous.

---

### BLG-GOV-195 — Strategic exclusions review cadence
**Priority:** P3 (Low)
**Type:** Governance / Strategy
**Owner:** Strategy Rules & System Intent Owner
**Source:** Idea intake IW-20260710-01 (IDEA-strategy-owner-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The 4 product-scope exclusions in `current_roadmap.md` §2 (broker API integration, real-time streaming, social features, options/futures) have not been explicitly re-confirmed since they were first recorded — they could be stale rather than deliberate.

**Proposed solution**
Add a periodic (e.g. every-N-cycle) explicit re-confirmation that each exclusion remains a deliberate choice, not simply an un-revisited default.

---

### BLG-OPS-101 — Render hosting tier review
**Priority:** P3 (Low)
**Type:** Operations
**Owner:** FinOps & Resource Architect
**Source:** Idea intake IW-20260710-01 (IDEA-finops-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The current Render service tier was set early in the project's life and has not been reviewed against actual usage since v6.8's added traffic (SI-02 indicator, trade tagging).

**Proposed solution**
Compare current Render tier cost/limits against actual measured usage and confirm the tier still fits, or right-size it.

---

### BLG-OPS-103 — Production database backup/restore drill
**Priority:** P2 (Medium)
**Type:** Operations
**Owner:** Infrastructure & Operations Owner
**Source:** Idea intake IW-20260710-01 (IDEA-infra-ops-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
No governed routine has ever exercised a full backup/restore drill against the production database; the recovery procedure's correctness is currently unverified.

**Proposed solution**
Document the current backup mechanism (if any) and perform one full restore drill against a non-production target to confirm the procedure actually works.

---

### BLG-GOV-196 — Sunset review for Priority 3 — Deferred initiatives
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Product Owner
**Source:** Idea intake IW-20260710-01 (IDEA-challenger-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The 7-item `initiative_register.md` Priority 3 — Deferred list (Position Correlation Analysis, Backtesting Module, Multi-Portfolio Support, Mobile App, Full Compliance Scoring, Prometheus, Customisable Dashboard Layout) has not been explicitly re-confirmed since first recorded; some entries may now be stale rather than deliberately deferred.

**Proposed solution**
Product Owner reviews each Priority 3 item and confirms it is still deliberately deferred (not simply forgotten), recording the confirmation date.

---

### BLG-SEC-14 — AI journal generation audit trail
**Priority:** P3 (Low)
**Type:** Security / Compliance
**Owner:** AI Compliance & Governance Officer
**Source:** Idea intake IW-20260710-01 (IDEA-ai-compliance-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Generated AI journal entries do not currently log which model/version produced them, limiting compliance traceability if AI output quality or behaviour is later questioned.

**Proposed solution**
Log model identifier and version alongside each AI-generated journal entry at generation time.

---

### BLG-SPEC-74 — OpenAPI response examples for Arc 5 endpoints
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** API Contracts & Documentation Owner
**Source:** Idea intake IW-20260710-01 (IDEA-api-contracts-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
`docs/reference/openapi.yaml` lacks example response payloads for Arc 5 endpoints, slowing frontend integration since developers must infer shapes from the schema alone.

**Proposed solution**
Add representative example payloads to the Arc 5 endpoint definitions in `openapi.yaml`.

---

### BLG-OPS-104 — Contract drift dashboard
**Priority:** P3 (Low)
**Type:** Operations / Governance
**Owner:** API Contracts & Documentation Owner
**Source:** Idea intake IW-20260710-01 (IDEA-api-contracts-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Routes missing a `docs/specs/api_contracts` entry are currently only caught when the CI OpenAPI Drift Detection gate fires on a PR — there is no proactive, pre-PR way to see the gap.

**Proposed solution**
Add a simple script/report surfacing any `backend/routers/` endpoint lacking a matching contract entry, runnable ahead of opening a PR.

---

### BLG-BE-54 — Database connection pool tuning review
**Priority:** P3 (Low)
**Type:** Backend / Operations
**Owner:** Backend Engineering Patterns Owner
**Source:** Idea intake IW-20260710-01 (IDEA-backend-engineering-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The database connection pool size has not been reviewed against actual concurrent load since v6.8's added traffic; it may be mis-sized in either direction.

**Proposed solution**
Measure current concurrent connection usage and compare against the configured pool size; adjust if warranted.

---

### BLG-GOV-198 — Base44 prompt versioning convention
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Base44 Frontend Prompt Owner
**Source:** Idea intake IW-20260710-01 (IDEA-base44-frontend-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
There is no convention tracking which Base44 prompt draft shipped with which ST-id, making future regression triage ("which prompt produced this component") harder than necessary.

**Proposed solution**
Adopt a lightweight convention (e.g. a comment header or delegation log field) recording the ST-id alongside each Base44 prompt draft.

---

### BLG-SEC-18 — Review baseline npm audit HIGH/CRITICAL findings (react-scripts toolchain)

**Priority:** P3 (Low)
**Type:** Security
**Owner:** Cybersecurity & Trust Lead
**Source:** ST-04 (BLG-SEC-15, EPIC-02, v8.5) — initial baseline capture for `dependency-vuln-rescan.yml`, 2026-08-10

**Problem**
`dependency-vuln-rescan.yml`'s baseline capture run (`docs/security/dependency_vuln_baseline.json`) found 16 npm packages with HIGH/CRITICAL advisories (13 high, 3 critical — `shell-quote`, `tar`, `websocket-driver` critical; `brace-expansion`, `fast-uri`, `form-data`, `js-yaml`, `nanoid`, `postcss`, `react-router`, `svgo`, `ws`, plus 4 no-own-advisory wrapper packages high). All are transitive dependencies pulled in via `react-scripts` (CRA v5's webpack-dev-server/build-toolchain dependency tree) rather than direct runtime dependencies of the shipped app — but none were individually risk-assessed before being added to the baseline; they were captured as a "known, not yet reviewed" snapshot so the new scheduled scan doesn't re-alert on them every month.

**Scope**
- Review each finding: is it build-time-only (dev/CI, never in the shipped production bundle) or does it reach the runtime bundle?
- For any exploitable-in-production finding: fix (upgrade/patch) or file a targeted remediation item.
- For build-time-only findings: record an explicit accept-risk decision (per the `CVE-2026-4539`/pygments precedent in `vulnerability-scan.yml`) rather than leaving them as an unreviewed baseline entry indefinitely.

**Acceptance Criteria**
- Each of the 16 baseline advisory IDs in `docs/security/dependency_vuln_baseline.json` has either been fixed (removed from baseline) or has a recorded accept-risk decision (owner, rationale, review-by date)

---

### BLG-SEC-28 — Telegram Bot Token missing from api_key_rotation_policy.md scope

**Priority:** P3 (Low)
**Type:** Security
**Owner:** Cybersecurity & Trust Lead
**Source:** ST-05 (BLG-SEC-16, EPIC-02, v8.5) — out-of-scope finding surfaced while adding the Application X-API-Key runbook, 2026-08-10

**Problem**
`docs/security/api_key_security_register.md` §7 (Telegram Bot Token / Chat ID) has a rotation procedure, but — same gap this story just fixed for the Application X-API-Key — `docs/ops/api_key_rotation_policy.md`'s own Scope table and Rotation Schedule never reference it, so the canonical rotation policy document is silently incomplete for this credential. Lower priority than the X-API-Key gap this story fixed: the Telegram token's `Last rotation date` is already recorded as "Unknown (pre-register baseline)", so there is no annual-cadence tracking depending on this today.

**Scope**
- Add Telegram Bot Token to `api_key_rotation_policy.md`'s Scope table and Rotation Schedule
- Add a Credential-Specific Notes subsection cross-referencing the register's existing procedure (same pattern as the Application X-API-Key entry added by ST-05)

**Acceptance Criteria**
- `api_key_rotation_policy.md` Scope table and Rotation Schedule include the Telegram Bot Token
- Credential-Specific Notes subsection added, cross-referencing `docs/security/api_key_security_register.md` §7

---

### BLG-SPEC-75 — Migration block consolidation review
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** Data Model & Domain Schema Owner
**Source:** Idea intake IW-20260710-01 (IDEA-data-model-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
`data_model.md`'s migration block history has not been reviewed for consistency since before v6.8's schema changes.

**Proposed solution**
Review all migration blocks in ascending version order for consistency and confirm the footer version matches the highest block.

---

### BLG-SPEC-118 — api_changelog.md not updated since v7.8.0 (v7.9-v8.4 endpoint additions missing)

**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** API Contracts & Documentation Owner
**Source:** ST-21 (EPIC-06, 2026-08-08__release-v8.5) — out-of-scope finding while adding a new endpoint entry

**Problem**
`docs/specs/api_contracts/api_changelog.md`'s most recent entry before this cycle's own addition was `v7.8.0` (2026-07-27) — several releases' worth of endpoint additions in `v7.9` through `v8.4` (e.g. `GET /reports/reconciliation` per `v8.2`, per `SystemStatus.js`'s own endpoint-count comment history) were never logged here, unlike `openapi.yaml` and the individual `docs/specs/api_contracts/*.md` files, which were kept current for each of those additions.

**Scope**
- Backfill `api_changelog.md` entries for each new `## METHOD /path` heading added across `v7.9`–`v8.4` (cross-reference each release's `docs/product/changelog.md` section and/or `git log` on `docs/specs/api_contracts/*.md` for the actual additions)

**Acceptance Criteria**
- `api_changelog.md` contains an entry for every new endpoint shipped in `v7.9` through `v8.4`, in descending version order

---

### BLG-QA-89 — R-multiple calculation regression test
**Priority:** P2 (Medium)
**Type:** QA / Backend
**Owner:** Financial Reporting & Records Owner
**Source:** Idea intake IW-20260710-01 (IDEA-financial-reporting-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The v6.8 R-multiple FX spec has no automated regression test locking its behaviour against known trade fixtures — a future change could silently alter R-multiple calculations.

**Proposed solution**
Add an automated test asserting R-multiple output against a small set of known trade fixtures.

---

### BLG-SPEC-76 — Trade tagging taxonomy documentation
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** Financial Reporting & Records Owner
**Source:** Idea intake IW-20260710-01 (IDEA-financial-reporting-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
BLG-FEAT-52 (trade tagging) shipped without a canonical list of allowed tags, risking inconsistent tag usage that would undermine tag-based reporting.

**Proposed solution**
Document a canonical allowed-tag taxonomy for trade tagging, referenced by both the UI and reporting logic.

---

### BLG-SPEC-77 — Gate-status indicator reusable component pattern documentation
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** Idea intake IW-20260710-01 (IDEA-frontend-specs-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
BLG-FEAT-71's SI-02 gate visibility indicator is a one-off implementation; the pattern is not documented for reuse by future gated features.

**Proposed solution**
Document the SI-02 indicator as a reusable gate-status component pattern in the relevant frontend spec, for future gated-feature reuse.

---

### BLG-OPS-105 — CI pipeline runtime audit
**Priority:** P3 (Low)
**Type:** Operations / QA
**Owner:** Head of Engineering
**Source:** Idea intake IW-20260710-01 (IDEA-head-of-engineering-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Full CI suite runtime has been creeping up without a recent audit identifying which test files are slowest.

**Proposed solution**
Profile CI runtime by file and identify the slowest contributors as candidates for optimisation or parallelisation.

---

### BLG-BE-56 — Backend service-layer boundary review
**Priority:** P3 (Low)
**Type:** Backend
**Owner:** Head of Engineering
**Source:** Idea intake IW-20260710-01 (IDEA-head-of-engineering-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Recent `BLG-BE-*` items have touched router/service/database layers; no recent review confirms the layering boundary still holds cleanly after these changes.

**Proposed solution**
Review recent backend changes for layering-boundary drift (e.g. business logic leaking into routers) and correct any found.

---

### BLG-QA-90 — Watchlist.js post-refactor visual QA
**Priority:** P3 (Low)
**Type:** QA / Frontend
**Owner:** Head of UX & Design
**Source:** Idea intake IW-20260710-01 (IDEA-head-of-ux-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The v6.8 Watchlist.js ESLint refactor (BLG-OPS-61) was a code-quality change; no explicit visual QA pass has confirmed it introduced no visual regressions.

**Proposed solution**
Perform a visual QA pass on the Watchlist page to confirm the ESLint refactor did not change rendered behaviour.

---

### BLG-GOV-200 — Skill-Silo rolling-average automation
**Priority:** P3 (Low)
**Type:** Governance Tooling
**Owner:** Metrics Definitions & Analytics Owner
**Source:** Idea intake IW-20260710-01 (IDEA-metrics-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
The STEP 7.1 Skill-Silo rolling-3-cycle average is currently computed manually each rebalance by reading the prior 2 cycles' recorded percentages from decision-log prose.

**Proposed solution**
Compute the rolling average from a structured source (e.g. a small per-cycle metrics file) instead of manual re-derivation each rebalance.

---

### BLG-QA-91 — Cross-browser Playwright matrix evaluation
**Priority:** P3 (Low)
**Type:** QA
**Owner:** QA Lead
**Source:** Idea intake IW-20260710-01 (IDEA-qa-lead-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Playwright coverage currently runs Chromium-only; critical-path behaviour on Firefox/WebKit is unverified.

**Proposed solution**
Evaluate the cost/benefit of adding Firefox/WebKit to the CI matrix for a small set of critical-path specs.

---

### BLG-GOV-201 — QA evidence log template consolidation
**Priority:** P3 (Low)
**Type:** Governance / QA Process
**Owner:** QA Lead
**Source:** Idea intake IW-20260710-01 (IDEA-qa-lead-20260710-02), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
Per-EPIC `qa_evidence_EPIC-*.md` files currently duplicate a substantial amount of boilerplate header/structure across files.

**Proposed solution**
Consolidate shared boilerplate into a referenced template section, reducing duplication across EPIC evidence files.

---

### BLG-QA-92 — Backend test suite runtime baseline
**Priority:** P3 (Low)
**Type:** QA / Backend
**Owner:** QA & Testing Owner
**Source:** Idea intake IW-20260710-01 (IDEA-qa-testing-20260710-01), roadmap rebalance 2026-07-10__scheduled
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
No current baseline records pytest suite runtime, making future runtime regressions hard to detect early.

**Proposed solution**
Record current `backend/.venv/bin/python3 -m pytest` runtime as a baseline for future comparison.

---

### BLG-QA-93 — conftest.py AST-scan coverage confirmation (consolidated)
**Priority:** P3 (Low)
**Type:** QA / Backend
**Owner:** QA & Testing Owner
**Source:** Idea intake IW-20260710-01 (IDEA-qa-testing-20260710-02), roadmap rebalance 2026-07-10__scheduled; consolidates BLG-QA-99 — the same capability was independently re-proposed at the 2026-07-12__scheduled idea-intake cycle without cross-reference to this existing item — merged 2026-07-28, session duplicate-consolidation cleanup
**Effort:** S (~0.5-2 days)
**Provisional-Target:** Unscheduled
**Gate criteria:** None

**Problem**
BLG-QA-73 replaced the manual `_DB_STUB_FUNCTIONS` list with an AST-scan derivation; no confirmation has been recorded that the scan's glob/traversal logic still covers all `backend/` modules and subpackages added since v6.8.

**Proposed solution**
Re-verify the AST scan's module coverage and glob/traversal logic against the current `backend/` tree; extend if a subpackage was missed; record confirmation.

---

### BLG-OPS-113 — Consolidate window_summary_IW-*.md files older than 90 days into a dated archive folder
**Priority:** P3 (Low) | **Type:** Operations / Housekeeping | **Owner:** Head of Specs Team | **Source:** IDEA-head-of-specs-20260717-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `claude/ideas/` now holds 20+ `window_summary_IW-*.md` files accumulated since 2026-03-21 with no archival pass — a directory-hygiene gap analogous to the pattern `ideas_housekeeping_prompt.md` already solves for register rows.
**Scope:** Move `window_summary_IW-*.md` files older than 90 days into a dated archive subfolder (e.g. `claude/ideas/window_summaries_archive/`), leaving the most recent 90 days in place for easy reference.
**Acceptance Criteria:** Archive folder created; files older than 90 days moved; no content lost (move, not delete).

---

### BLG-GOV-203 — Gemini AI usage audit-trail retention policy
**Priority:** P3 (Low) | **Type:** Governance / AI Compliance | **Owner:** AI Compliance & Governance Officer | **Source:** IDEA-ai-compliance-20260712-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `gemini_audit_log` (v4.0) has no retention/archival policy; unbounded growth complicates compliance review.
**Scope:** Define a retention window and archival job for the audit log table.
**Acceptance Criteria:** Retention policy documented; archival mechanism specified; AI Compliance Officer sign-off.

### BLG-GOV-205 — Standardise `api_changelog.md` entry template
**Priority:** P3 (Low) | **Type:** Governance / Documentation | **Owner:** API Contracts & Documentation Owner | **Source:** IDEA-api-contracts-20260712-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Inconsistent version-footer formatting across releases makes `CLAUDE.md` §8 cross-EPIC merge-conflict resolution harder than necessary.
**Scope:** Define one canonical `api_changelog.md` entry template and apply retroactively where low-cost.
**Acceptance Criteria:** Template documented; existing entries conform or a migration note is filed.

### BLG-BE-58 — Position lifecycle state-transition history table
**Priority:** P3 (Low) | **Type:** Data Model / Pre-work | **Owner:** Data Model & Domain Schema Owner | **Source:** IDEA-data-model-20260712-02 | **Effort:** M | **Provisional-Target:** Unscheduled
**Problem:** `position_lifecycle_service` tracks current state only; no historical transition log exists for post-hoc analysis.
**Scope:** Add an append-only `position_state_history` table, written on each lifecycle transition, to support future PS-04 (Strategy Decay Detection) state-conditional analysis.
**Acceptance Criteria:** Table + migration added; transitions logged; no behavioural change to current lifecycle logic.

### BLG-GOV-208 — Minimum-interval guideline between scheduled rebalances
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Director of HR | **Source:** IDEA-director-of-hr-20260712-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** 55+ completed cycles at high governance intensity, including a same-day double-run this cycle, risk operator fatigue even in a solo-plus-AI-delegation context.
**Scope:** Propose a policy guideline against same-day double scheduled-rebalance runs absent explicit cause (complements `BLG-GOV-207`'s technical fix).
**Acceptance Criteria:** Guideline documented in `claude/charter/team_charter.md` or `CLAUDE.md` §5; Director of HR + Head of Specs Team sign-off.

### BLG-GOV-209 — Frame Skill-Silo Alert as workload-composition, not just product-mix
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Director of HR | **Source:** IDEA-director-of-hr-20260712-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `roadmap_prompt.md` STEP 7.1's >40% governance ceiling is treated purely as a product-value problem; it is equally an HR/workload-composition signal for the one human operator.
**Scope:** Add an HR-perspective note to STEP 7.1's output alongside the existing PO pull-forward mechanism.
**Acceptance Criteria:** `roadmap_prompt.md` STEP 7.1 patched (versioned per `CLAUDE.md` §6); Director of HR sign-off.

### BLG-OPS-106 — AI cost-threshold alert value review
**Priority:** P3 (Low) | **Type:** Operations / FinOps | **Owner:** Financial Reporting & Records Owner | **Source:** IDEA-financial-reporting-20260712-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `POST /ai/check-daily-cost` (v4.0) alerts on a fixed cost threshold; no review has confirmed it's still appropriate given growing SI-04-adjacent AI usage.
**Scope:** Review 90 days of actual AI spend against the current threshold; adjust if warranted.
**Acceptance Criteria:** Review documented; threshold confirmed or adjusted with rationale.

### BLG-GOV-210 — Governance-cycle wall-clock cost logging
**Priority:** P3 (Low) | **Type:** Governance / FinOps | **Owner:** FinOps & Resource Architect | **Source:** IDEA-finops-20260712-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** No estimate exists of session/compute time consumed per scheduled rebalance cycle, relevant given the recent same-day double-run.
**Scope:** Log start/end timestamp and step count per cycle in `run_manifest.md` (partially already present); roll up into `velocity_metrics.md`.
**Acceptance Criteria:** Logging convention documented; applied from the next cycle onward.

### BLG-GOV-211 — Effort-band accuracy retrospective
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** FinOps & Resource Architect | **Source:** IDEA-finops-20260712-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `scored_initiatives.md` assigns S/M/L/XS effort bands at promotion time but nothing checks these against actual sprint-planning delivered effort afterward.
**Scope:** Quarterly retrospective comparing assigned effort band vs actual sprint capacity consumed for shipped initiatives.
**Acceptance Criteria:** First retrospective produced; process documented for repeat.

### BLG-SPEC-81 — Research view `signal_type` filter spec
**Priority:** P3 (Low) | **Type:** Spec Debt | **Owner:** Frontend Specifications & UX Documentation Owner | **Source:** IDEA-frontend-specs-20260712-02 | **Effort:** S | **Provisional-Target:** Unscheduled
**Gate criteria:** ≥5 distinct `signal_type` values observed in practice (currently fewer; re-check at next backlog grooming).
**Problem:** v4.1 added `signal_type` (Setup Type) to the research view with no filter/sort spec as the field accumulates distinct values.
**Scope:** Spec a filter control once the gate condition is met.
**Acceptance Criteria:** Filter spec written; gate condition re-verified before implementation.

### BLG-GOV-215 — Product Value Ratio historical trend row in `velocity_metrics.md`
**Priority:** P3 (Low) | **Type:** Governance / Metrics | **Owner:** Metrics Definitions & Analytics Canonical Owner | **Source:** IDEA-metrics-20260712-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** STEP 2.4's Product Value Ratio is recomputed from scratch each cycle (0.26 → 0.18 → 0.21) with no first-class trend record, making the multi-cycle alert pattern harder to see at a glance.
**Scope:** Add a Product Value Ratio row to `velocity_metrics.md`, appended each time STEP 2.4 runs.
**Acceptance Criteria:** Row added retroactively for the last 3 readings; convention documented for future cycles.

### BLG-GOV-217 — Surface meta-review countdown in every `run_manifest.md`
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** PMO Lead | **Source:** IDEA-pmo-lead-20260712-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** STEP 11.4's meta-review triggers every 3rd cycle but nothing surfaces the countdown until it fires; PMO currently computes it manually each time.
**Scope:** Surface `rebalance_cycles_since_meta_review` in every cycle's run manifest header, regardless of due status.
**Acceptance Criteria:** `roadmap_prompt.md` STEP 1.1 patched (versioned per `CLAUDE.md` §6) to include the field.

### BLG-QA-103 — pip-audit trend log across sprint-planning runs
**Priority:** P3 (Low) | **Type:** QA / Security | **Owner:** QA & Testing Owner | **Source:** IDEA-qa-testing-20260712-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `sprint_planning_notes.md`'s Pre-Sprint Vulnerability Scan runs `pip-audit` each sprint but results aren't tracked over time to see whether the same finding recurs or is repeatedly deferred.
**Scope:** Append a running pip-audit summary log (date, findings count, resolution status) alongside `sprint_planning_notes.md`.
**Acceptance Criteria:** Log convention documented and applied from the next sprint planning onward.


---

### BLG-QA-108 — Spot-check Tier 1/Tier 2 DoQ severity-labeling consistency
**Priority:** P3 (Low) | **Type:** QA / Process | **Owner:** Director of Quality | **Source:** IDEA-director-of-quality-20260713-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** DoQ severity tiering (Tier 1/Tier 2) is applied per verification report without a periodic cross-report consistency check — risk of drift in how similar findings are labelled across cycles.
**Scope:** Sample the last 5 `verification_report.md` files; confirm comparable findings received comparable tier labels; document any drift found.
**Acceptance Criteria:** Spot-check completed and documented; any labelling drift found is either corrected going forward or explicitly justified.

### BLG-SPEC-85 — `trailing_stop_action_rate` spec entry with validation tolerances
**Priority:** P3 (Low) | **Type:** Spec Debt / Metrics | **Owner:** Metrics Definitions & Analytics Canonical Owner | **Source:** IDEA-metrics-20260713-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** v7.0's `trailing_stop_action_rate` metric instrumentation (EPIC-02 ST-07, `BLG-BE-50`) shipped without a formal `metrics_definitions.md` entry defining acceptable validation tolerances (e.g. expected range, what a stale/anomalous reading looks like).
**Scope:** Add a formal spec entry mirroring the format of other Arc 3/5 metrics already documented, including explicit validation tolerance bounds.
**Acceptance Criteria:** Entry added to `metrics_definitions.md`; tolerances stated numerically, not qualitatively.


---

### BLG-GOV-235 — Idea-intake minimum-submission flex condition
**Priority:** P3 (Low) | **Type:** Governance | **Owner:** Head of Specs Team | **Source:** IDEA-director-of-hr-20260715-01 | **Effort:** S | **Provisional-Target:** TBD
**Gate criteria:** Recurs at 3+ consecutive scheduled cycles where the Now horizon is already populated with 3+ ad-hoc (non-governed-cycle) P1 items at window-open — not yet met (this is the 1st such occurrence).
**Problem:** `idea_intake_prompt.md`'s standing 2-net-new-ideas-per-agent minimum does not flex when the Now horizon is already saturated with ad-hoc additions, potentially generating submissions redundant with just-added scope.
**Scope:** If the gate condition recurs, evaluate whether the minimum should reduce or the window should skip agents whose domain is already covered by the ad-hoc additions.
**Acceptance Criteria:** Gate re-checked each scheduled cycle; a written decision follows once met.

### BLG-QA-109 — DoQ sign-off template alignment check (FI-P3-02 wording-only exception)
**Priority:** P3 (Low) | **Type:** QA / Governance | **Owner:** Director of Quality | **Source:** IDEA-director-of-quality-20260715-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** No recent confirmation that the DoQ sign-off block template still correctly reflects CLAUDE.md's FI-P3-02 wording-only exception (code review may substitute for staging sign-off only for non-visual, wording-only ACs).
**Scope:** Compare current DoQ sign-off block template/practice against the CLAUDE.md FI-P3-02 clause; correct if drifted.
**Acceptance Criteria:** Comparison performed; template confirmed current or corrected.

### BLG-GOV-238 — Governed-vs-ad-hoc backlog scope visibility
**Priority:** P3 (Low) | **Type:** Governance / FinOps | **Owner:** PMO Lead; FinOps & Resource Architect | **Source:** IDEA-challenger-20260715-02, IDEA-pmo-lead-20260715-01, IDEA-finops-20260715-02 (3-idea consolidation per STEP 4.2 Idea Consolidation convention) | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Three independent submissions this window flagged the same underlying pattern from different angles: 5 P1 items were added to `backlog.md` outside a governed cycle in the session immediately preceding this rebalance (a 2nd occurrence of ad-hoc additions bypassing governed release scoping, per the Challenger's framing), with no lightweight tracking of governed-cycle-added vs. ad-hoc session-added items per release, nor visibility into whether ad-hoc additions are displacing gated/scored capacity.
**Scope:** Add a lightweight running tally (e.g. a count/tag in each cycle's `run_manifest.md` or `cycle_summary.md`) distinguishing governed-cycle additions from ad-hoc session additions per release, to give FinOps/PMO Lead visibility into the trend.
**Acceptance Criteria:** Tally mechanism scoped; first data point recorded retroactively for v7.1/this cycle where determinable.

### BLG-OPS-112 — AI endpoint (daily-briefing/chat) cost & latency drift monitoring
**Priority:** P3 (Low) | **Type:** Operations / AI Governance | **Owner:** AI Compliance & Governance Officer; Infrastructure & Operations Owner | **Source:** IDEA-ai-compliance-20260716-01 | **Effort:** S (~1 day) | **Provisional-Target:** TBD
**Problem:** `POST /ai/daily-briefing` and `POST /ai/chat` have per-call cost tracking (`gemini_audit_log`/Anthropic usage logging) but no rolling anomaly check — a latency or cost regression would only surface via manual review, not an alert.
**Scope:** Extend existing cost-tracking infrastructure with a rolling anomaly check (e.g. week-over-week cost/latency delta threshold) for the two AI endpoints.
**Acceptance Criteria:** Anomaly check scoped and added; confirmed to fire on a simulated cost/latency spike.

---

### BLG-OPS-135 — Add GET /trade-plans/tags to api_performance_baseline.md
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** Post-ship closure 2026-08-07__release-v8.4 — endpoint coverage drift advisory (STEP 6), re-run after `BLG-OPS-133`/`BLG-SPEC-116` closed this same cycle
**Effort:** XS (<0.5d — 1 endpoint)
**Provisional-Target:** Before next performance baseline review

**Problem**
Re-running the endpoint coverage drift check against the now-corrected `openapi.yaml` (post `BLG-SPEC-116`) and the now-updated `api_performance_baseline.md` (post `BLG-OPS-133`'s §35 registrations) finds 1 remaining genuine gap: `GET /trade-plans/tags` is defined in `openapi.yaml` but has no measurement row in `api_performance_baseline.md`. §27's endpoint-characteristics note references it only in passing ("consistent with `GET /trade-plans/tags` (§ existing pattern)") when documenting its sibling `GET /watchlist/tags` — it was never actually registered with its own row. All 8 other candidate gaps flagged by a naive path-normalised diff were confirmed false positives (already documented under query-string variants, sub-path rows, or explicitly reconciled in `api_performance_baseline.md` §35's own re-derivation note).

**Scope**
- Run `GET /trade-plans/tags` against staging to obtain p50/p95 latencies (single `SELECT DISTINCT unnest(tags)` on `trade_plans`, no path parameters, mirrors `GET /watchlist/tags`'s existing measurement)
- Add a row to `docs/ops/api_performance_baseline.md` §27's endpoint profile table

**Acceptance Criteria**
- `GET /trade-plans/tags` has p50/p95/max latency entries in the baseline document, consistent with existing measurement methodology

---

### BLG-SPEC-117 — Give docs/specs/Specs_Index.md a proper Changelog table instead of a chained Last Updated header
**Priority:** P3 (Low) | **Type:** Spec Debt | **Owner:** Head of Specs Team | **Source:** Found during 2026-08-07 session review of `**Last Updated:**` header bloat (`shared_standards.md` §16.14, broadened to universal scope this session) | **Effort:** S (~0.5d) | **Provisional-Target:** TBD

**Problem**
`docs/specs/Specs_Index.md` is a Class 1 (Authoritative) document, but its `**Last Updated:**` header chains every prior revision inline (`<date> (<reason>); prior — <date> (<reason>); ...`) rather than using a dedicated `## Changelog` table or companion `claude/system/changelogs/*.md` file the way other Class 1/6 canonical documents do. This session found the chain at 5 entries/~2,048 characters and truncated it to the standard 3-entry cap as an immediate stopgap (per §16.14), but the chained pattern will simply re-accumulate on the next few touches since the document has no structural place to put history other than the header field.

**Scope**
- Add a `## Changelog` table (or a companion `claude/system/changelogs/specs_index_changelog.md` file, matching the pattern used by Class 6 prompts) to `docs/specs/Specs_Index.md`
- Migrate the existing truncated header history into the new table/file as its first backfilled rows
- Collapse the header `**Last Updated:**` field to a bare single-line `<date> (<one-line summary>)` — no chaining — going forward

**Acceptance Criteria**
- `docs/specs/Specs_Index.md` has a `## Changelog` table or companion changelog file
- `**Last Updated:**` header field is a single line, no `prior —` chaining
- Head of Specs Team sign-off

---

### BLG-QA-136 — Add endpoint-level regression test for GET /analytics/tag-performance's ensure_trade_plans_table call

**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA & Testing Owner
**Source:** Agent-mediated PR review (Director of Quality role), PR #1326, 2026-08-08__release-v8.5 — 2026-08-10
**Effort:** XS (<1h)
**Provisional-Target:** v8.6

**Problem**
`qa_evidence_EPIC-01.md` cites `tests/test_trade_plan_tags.py` and `TestTradePlanEndpoints` as coverage for the `GET /analytics/tag-performance` 500 fix (ST-01, EPIC-01), but neither test actually exercises the changed code path — `test_trade_plan_tags.py` calls `database.get_tag_performance()` directly (bypassing the router), and `TestTradePlanEndpoints` tests a different router file entirely. The only existing test hitting this endpoint short-circuits before reaching the new `ensure_trade_plans_table()` call. The fix itself is correct (independently reproduced by the reviewing agent), but the evidence record misstates what verifies it.

**Scope**
- Add a direct endpoint-level regression test for `GET /analytics/tag-performance` (patching `ensure_trade_plans_table`/`get_tag_performance`, asserting the ensure-call fires and status is 200)

**Acceptance Criteria**
- A test exists that calls the actual `GET /analytics/tag-performance` router endpoint and asserts `ensure_trade_plans_table()` is invoked before the query

---

### BLG-QA-137 — Add Playwright coverage for setNarrativeField AI-draft-badge clearing on the 3 non-setup_thesis fields

**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA & Testing Owner
**Source:** Agent-mediated PR review (Director of Quality role), PR #1327, 2026-08-08__release-v8.5 — 2026-08-10
**Effort:** S (~0.5d)
**Provisional-Target:** v8.6

**Problem**
`TradePlan.js`'s `setNarrativeField()` helper is applied to all four narrative fields (`setup_thesis`, `entry_rationale`, `confirmation_criteria`, `early_exit_conditions`) to clear the AI-draft badge on manual edit, but `tests/e2e/trade-plan.spec.js` only has dedicated coverage for `setup_thesis`-triggered clearing — the other three fields' clearing behaviour is untested.

**Scope**
- Extend `trade-plan.spec.js` (or the existing SC-TP-24 scenario family) with coverage asserting edits to `entry_rationale`/`confirmation_criteria`/`early_exit_conditions` also clear `isAiDraft`/`isClaudeDraft`

**Acceptance Criteria**
- Playwright coverage exists and passes for all 4 narrative fields' AI-draft-badge-clearing behaviour, not just `setup_thesis`

---

### BLG-QA-138 — Add unit tests for scripts/check_dependency_vuln_rescan.py

**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA & Testing Owner
**Source:** Agent-mediated PR review (Director of Quality role), PR #1329, 2026-08-08__release-v8.5 — 2026-08-10
**Effort:** S (~0.5d)
**Provisional-Target:** v8.6

**Problem**
`scripts/check_dependency_vuln_rescan.py` (171 lines) has real branching logic worth protecting — severity filtering, GHSA-ID extraction from mixed dict/string `via` entries, baseline dedup, no-own-advisory labeling — but has no unit tests. It was verified manually this session against live `npm audit` output, but that verification isn't captured as a repeatable regression test; a future edit to the parsing logic (e.g. npm changing its `via` schema) has nothing to catch a silent regression.

**Scope**
- Add fixture-based unit tests: baseline-hit (known finding, no new alert), new-finding (unknown advisory ID, triggers new-finding path), and malformed/error-shaped input (see `BLG-SEC-29`)

**Acceptance Criteria**
- `tests/` has a test file covering `check_dependency_vuln_rescan.py`'s core parsing/dedup logic with at least the 3 scenarios above

---

### BLG-QA-139 — Document one-directional limitation of test_alerts_service.py's sys.modules restore fixture

**Priority:** P3 (Low)
**Type:** QA / Test Infrastructure
**Owner:** QA & Testing Owner
**Source:** Agent-mediated PR review (Director of Quality role), PR #1331, 2026-08-08__release-v8.5 — 2026-08-10
**Effort:** XS (<1h; M if the broader follow-up is pursued)
**Provisional-Target:** v8.6

**Problem**
`test_alerts_service.py`'s `sys.modules` restore fixture (ST-25, BLG-QA-105) only protects tests collected *after* that file — its stated AC scope, confirmed working (1057 passed, 5 skipped). Independently reproduced that pollution can still flow the *other* direction: an earlier-collected file's own incomplete stub (e.g. `test_price_alerts_service.py`) can overwrite `test_alerts_service.py`'s stub before its tests run, since the fixture's restore only fires at teardown. Confirmed this specific failure mode pre-exists on `main` (not a regression from PR #1331) and doesn't manifest in the actual full-suite run — but the PR's framing ("preventing cross-file test pollution") reads more sweeping than what was actually delivered.

**Scope**
- Add a one-line code comment in the fixture (`tests/test_alerts_service.py`) noting the fix is one-directional
- Consider a broader follow-up (e.g. a session-scoped `conftest.py` fixture) if two-directional protection is later needed — separate, larger item if pursued

**Acceptance Criteria**
- The fixture's code comment or docstring explicitly states the one-directional scope of the protection it provides

---

### BLG-OPS-136 — Align api-key-cross-environment-check.yml's alert-step grep with the skip-guard's ::error:: prefix

**Priority:** P3 (Low)
**Type:** Operations / Bug
**Owner:** Infrastructure & Operations Owner
**Source:** Agent-mediated PR review (Director of Quality role), PR #1326, 2026-08-08__release-v8.5 — 2026-08-10
**Effort:** XS (<1h)
**Provisional-Target:** v8.6

**Problem**
`.github/workflows/api-key-cross-environment-check.yml`'s "check error" alert step greps `cross_env_output.txt` for `^[ERROR]`, but the missing-secrets skip-guard path in the same file emits `::error::` instead — a mismatch means that specific failure path's Telegram alert body loses the underlying detail (nothing is lost from the Actions log itself, but the alert is less useful than it should be).

**Scope**
- Align the grep pattern with the actual emitted prefix, or emit `[ERROR]` from the skip-guard to match the existing grep

**Acceptance Criteria**
- The missing-secrets skip-guard path's Telegram alert includes the specific error detail, verified by triggering the path (or a dry-run/manual test) once fixed

---

### BLG-OPS-137 — Document CVE-2026-4539 ignore rationale in dependency-vuln-rescan.yml

**Priority:** P4 (Low)
**Type:** Operations / Documentation
**Owner:** Cybersecurity & Trust Lead
**Source:** Agent-mediated PR review (Director of Quality role), PR #1329, 2026-08-08__release-v8.5 — 2026-08-10
**Effort:** XS (<1h)
**Provisional-Target:** v8.6

**Problem**
`.github/workflows/dependency-vuln-rescan.yml`'s pip-audit step repeats `--ignore-vuln CVE-2026-4539` from `vulnerability-scan.yml` with no inline rationale comment (the original has a multi-line justification). A reader of the new file alone can't tell why an accepted-risk CVE is still excluded from a scan whose stated purpose is closing gaps other tiers leave, and there are now two places to keep in sync if the risk decision is revisited.

**Scope**
- Add the same rationale comment (or a cross-reference to `vulnerability-scan.yml`'s) to `dependency-vuln-rescan.yml`

**Acceptance Criteria**
- `dependency-vuln-rescan.yml`'s `CVE-2026-4539` ignore has an inline rationale comment or cross-reference

---

### BLG-OPS-138 — Confirm dependency-vuln-rescan.yml runs successfully post-merge (ST-04 deferred verification)

**Priority:** P2 (Medium)
**Type:** Operations / Follow-up
**Owner:** Infrastructure & Operations Owner
**Source:** Agent-mediated PR review (Director of Quality + Product Owner roles), PR #1329, 2026-08-08__release-v8.5 — 2026-08-10
**Effort:** XS (<1h)
**Provisional-Target:** v8.6

**Problem**
ST-04's AC "Scheduled job runs successfully at least once and reports results for both pip-audit and npm audit" could not be verified pre-merge (GitHub returns 404 dispatching a workflow not yet on the default branch) and was deferred to a manual post-merge step with no tracking item — it currently depends on someone remembering to run it.

**Scope**
- Run `gh workflow run dependency-vuln-rescan.yml` once PR #1329 merges to `main`
- Confirm a clean run: job summary populated, correct pip-audit/npm audit counts reported

**Acceptance Criteria**
- A confirmed-successful `dependency-vuln-rescan.yml` run exists post-merge, closing ST-04's originally-deferred AC

---

### BLG-SEC-29 — check_dependency_vuln_rescan.py silently treats a failed audit tool as "zero findings"

**Priority:** P2 (Medium)
**Type:** Security / Bug
**Owner:** Cybersecurity & Trust Lead
**Source:** Agent-mediated PR review (Director of Quality role), PR #1329, 2026-08-08__release-v8.5 — 2026-08-10
**Effort:** S (~0.5d)
**Provisional-Target:** v8.6

**Problem**
`scripts/check_dependency_vuln_rescan.py`'s `pip_audit_findings()`/`npm_audit_findings()` both default to an empty result when the expected JSON key (`dependencies`/`vulnerabilities`) is missing from tool output. Reproduced live: running `npm audit --json` without a lockfile exits 0 and prints an `{"error": ...}` payload with no `vulnerabilities` key — this script reads that as a clean scan. The calling workflow (`dependency-vuln-rescan.yml`) already captures each tool's `exit_code` as a step output but never checks it. Since this job's entire purpose is catching vulnerabilities during windows with no other CI activity, a silent tool failure (bad working directory, registry outage, corrupted lockfile) could go unnoticed indefinitely.

**Scope**
- Check the captured `exit_code` outputs in `dependency-vuln-rescan.yml` and treat a nonzero/error-shaped result as a hard failure or an explicit "scan inconclusive" state, not a clean scan

**Acceptance Criteria**
- A simulated tool failure (missing lockfile, non-JSON output, or nonzero exit) is surfaced as a distinguishable failure/inconclusive state, not silently reported as "0 findings"

---

## Roadmap Rebalance 2026-07-24__scheduled — New Items (IW-20260724-01 disposition)

*34 items added via idea intake IW-20260724-01 STEP 4 disposition (Backlog). Source ideas and full rationale: `claude/ideas/ideas_register.md` (2026-07-24 rows), `claude/ideas/window_summary_IW-20260724-01.md`. DL-075.*

### BLG-GOV-252 — Data-retention policy for closed-trade and journal records
**Priority:** P3 (Low) | **Type:** Governance / Data Model | **Owner:** Data Model & Domain Schema Owner | **Source:** IDEA-data-model-20260724-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** No retention policy exists for closed-trade and journal records; at current trade volume this is low-urgency but undefined.
**Scope:** Define archival-vs-deletion policy ahead of long-term data growth.
**Acceptance Criteria:** Policy documented; no implementation required until data volume warrants action.

---

### BLG-GOV-253 — Onboarding checklist for new governance agent roles
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Director of HR | **Source:** IDEA-director-of-hr-20260724-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Each new governance agent role (`claude/agents/*.md`) is created ad hoc with no standard checklist of required charter fields, write-scope declarations, or review cadence.
**Scope:** Document a standard onboarding checklist for new agent role creation.
**Acceptance Criteria:** Checklist added to `claude/charter/` or `claude/system/`; Head of Specs Team sign-off.

---

### BLG-SPEC-98 — Consolidate duplicate empty-state pattern specs
**Priority:** P3 (Low) | **Type:** Spec Debt / Frontend | **Owner:** Frontend Specifications & UX Documentation Owner | **Source:** IDEA-frontend-specs-20260724-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** Empty-state pattern definitions (the `DataState` pattern formalised in `design_system.md` v1.1, per v7.2) are restated with minor variation across multiple page specs rather than referencing one canonical definition.
**Scope:** Consolidate empty-state pattern definitions into `design_system.md`; update page specs to reference rather than restate.
**Acceptance Criteria:** Duplicate definitions removed from at least 3 page specs; `design_system.md` remains the single source.

---

### BLG-SPEC-99 — Keyboard-navigation requirements section for table-based page specs
**Priority:** P3 (Low) | **Type:** Spec Debt / Accessibility | **Owner:** Frontend Specifications & UX Documentation Owner | **Source:** IDEA-frontend-specs-20260724-02 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** Table-based page specs (Positions, Trades, Red Flag Journal) have no documented keyboard-navigation requirements, leaving the expected behaviour implicit.
**Scope:** Add a keyboard-navigation requirements section to the relevant page specs.
**Acceptance Criteria:** Section added to at least Positions, Trades, and Red Flag Journal specs.

---

### BLG-SPEC-100 — Canonical "win rate" vs "hit rate" definitions doc
**Priority:** P3 (Low) | **Type:** Spec Debt / Metrics | **Owner:** Metrics Definitions & Analytics Canonical Owner | **Source:** IDEA-metrics-20260724-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** "Win rate" and "hit rate" terminology is used inconsistently across specs (`metrics_definitions.md` and page specs) without a single canonical distinction.
**Scope:** Add canonical definitions for both terms to `metrics_definitions.md`; audit existing specs for inconsistent usage.
**Acceptance Criteria:** Canonical definitions added; at least the highest-traffic specs (Performance Analytics, Reports) reconciled to use them consistently.

---

### BLG-FEAT-83 — Cohort-based (setup/signal type) performance metric
**Priority:** P3 (Low) | **Type:** Product Feature / Analytics | **Owner:** Metrics Definitions & Analytics Canonical Owner | **Source:** IDEA-metrics-20260724-02 | **Effort:** M | **Provisional-Target:** TBD
**Gate criteria:** Sufficient `setup_type`/signal-type diversity in closed-trade history to produce a meaningful cohort split (same data-density concern as `BLG-FEAT-62`).
**Problem:** Performance Analytics has no cohort-based (grouped by setup/signal type) performance metric, despite the underlying `signal_type` field being captured since the Research view shipped it (v4.1).
**Scope:** Add a cohort-based performance metric to Performance Analytics, building on the existing Arc 5 compliance analytics layer.
**Acceptance Criteria:** Metric available once gate clears; at least 3 distinct cohorts represented.

---

### BLG-GOV-255 — Periodic §13 boundary review cadence tied to SI-02's gate history
**Priority:** P3 (Low) | **Type:** Governance / Strategy | **Owner:** Strategy Rules & System Intent Owner | **Source:** IDEA-strategy-owner-20260724-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** SI-02's gate has now returned NOT MET across 9+ consecutive re-checks; while this is a data-density issue rather than a §13 issue, no periodic review formally confirms that distinction continues to hold as the system evolves.
**Scope:** Define a periodic (e.g. every 10th consecutive identical gate reading) §13 boundary review checkpoint tied to SI-02's gate history specifically.
**Acceptance Criteria:** Review cadence documented; Strategy Rules & System Intent Owner sign-off.

---

### BLG-SPEC-101 — Worked example of the ATR-based sizing edge case in strategy_rules.md
**Priority:** P3 (Low) | **Type:** Spec Debt / Strategy | **Owner:** Strategy Rules & System Intent Owner | **Source:** IDEA-strategy-owner-20260724-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Several backlog items reference an ATR-based sizing edge case informally without a canonical worked example in `strategy_rules.md` itself.
**Scope:** Add a worked numerical example of the edge case to `strategy_rules.md`.
**Acceptance Criteria:** Worked example added; Strategy Rules & System Intent Owner sign-off; no functional/behavioural change (documentation only).

---

### BLG-QA-122 — Broker statement reconciliation (blocked — no broker import mechanism)
**Priority:** P3 (Low) | **Type:** QA / Financial Reporting, gate-conditional | **Owner:** Financial Reporting & Records Owner | **Source:** IDEA-financial-reporting-20260724-02 | **Effort:** M | **Provisional-Target:** TBD
**Gate criteria:** A broker statement import mechanism exists. Per `current_roadmap.md` §2 Product Scope Exclusions, "Broker API integration (execution)" is currently a deferred (not strategically excluded) exclusion — no import path exists today for this item to reconcile against.
**Problem:** Idea proposed a reconciliation check between journal/trade entries and broker statement data, but no broker statement import mechanism currently exists to reconcile against.
**Scope:** Deferred until broker integration (or a manual statement upload path) exists.
**Acceptance Criteria:** N/A until gate clears.

---

## Delivery Verification 2026-07-24__release-v7.8 — New Items

*Doc-completeness findings surfaced while authoring `tests/test_pilot_contract_schemas.py` (EPIC-11/ST-11), recorded but not fixed in that story per its own scope boundary (adding contract tests, not auditing existing contract docs) — see `qa_evidence_EPIC-11.md`. None are P0/P1; no caller-relied-upon field is missing from any real response.*

## Roadmap Rebalance 2026-07-27__scheduled — New Items (IW-20260727-01 disposition)

*21 items added from `IW-20260727-01`'s 44 submissions (22 agents × 2 ideas). 23 submissions rejected — not strong, the large majority as duplicates of existing open backlog items surfaced by the mandatory STEP 4.0/§2.0.5 backlog-overlap check (this backlog has run 20+ idea-intake cycles and is now heavily saturated for "obvious" governance/process-improvement topics — see `lessons_learnt.md` for the resulting process observation). Full disposition: `claude/ideas/ideas_register.md` (2026-07-27 rows).*

### BLG-GOV-259 — Quarterly retrospective: estimated vs. actual effort bands (§16.7)
**Priority:** P3 (Low) | **Type:** Governance / FinOps | **Owner:** FinOps & Resource Architect | **Source:** IDEA-finops-20260727-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `scored_initiatives.md` Effort Band (§16.7) and `backlog.md` Effort day-ranges (§16.12) are assigned at promotion time but never checked back against actual delivery time — no feedback loop exists to calibrate future estimates.
**Scope:** Add a quarterly (or every-N-cycle) retrospective comparing estimated effort bands to actual sprint-close data.
**Acceptance Criteria:** Retrospective cadence documented; FinOps & Resource Architect sign-off.

---

### BLG-GOV-260 — Retire stale `RA:` roadmap-annotation markers older than 3 releases
**Priority:** P3 (Low) | **Type:** Governance Process | **Owner:** Head of Specs Team | **Source:** IDEA-head-of-specs-20260727-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `current_roadmap.md` §3 accumulates `RA:` retirement markers indefinitely (18+ visible as of this cycle, back to v5.0) with no defined pruning rule — each is a one-line pointer to `roadmap_archive.md`, so retaining very old ones adds document length without adding information not already in the archive.
**Scope:** Define a rule (e.g. `manage roadmap` STEP N) to prune `RA:` markers older than 3 releases, since the archive itself remains the permanent record.
**Acceptance Criteria:** Rule documented in `roadmap_management_prompt.md`; Head of Specs Team sign-off.

---

### BLG-GOV-261 — Lightweight due-date index for outstanding deferred-patch reminders across cycles
**Priority:** P3 (Low) | **Type:** Governance Process | **Owner:** PMO Lead | **Source:** IDEA-pmo-lead-20260727-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Deferred patches are tracked individually within each cycle's `lessons_learnt.md`, requiring STEP -1.5 to re-read the immediately prior cycle's file each time — there is no single cross-cycle index of "what's due when," which is exactly the class of gap that let a v7.6-sourced Recurrence Escalation go unresolved for 2 further cycles (see this cycle's STEP -1.7 finding).
**Scope:** Add a lightweight append-only index file listing every open deferred patch, its target, and owner, updated whenever one is filed or resolved.
**Acceptance Criteria:** Index file created and documented; PMO Lead sign-off.

---

### BLG-GOV-262 — Formalise a data-volume threshold trigger for the §12.2 "elements that may change" review
**Priority:** P3 (Low) | **Type:** Governance / Strategy | **Owner:** Strategy Rules & System Intent Owner | **Source:** IDEA-strategy-owner-20260727-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `strategy_rules.md` §12.2 lists elements that may change as trade-history volume grows, but does not name a specific volume threshold that should trigger a formal review — review timing is currently ad hoc.
**Scope:** Define an explicit trade-count (or time-based) threshold that triggers a §12.2 review.
**Acceptance Criteria:** Threshold documented in §12.2; Strategy Rules & System Intent Owner sign-off.

---

### BLG-GOV-264 — Physically place the Displacement Debt Register and wire it into `roadmap_prompt.md` STEP 8
**Priority:** P3 (Low) | **Type:** Governance | **Owner:** Roadmap Rebalance Engine / Head of Specs Team | **Source:** `ESC-EXEC-20260727-02` (`claude/cycles/2026-07-27__release-v7.9/execution_escalations.md`), raised during EPIC-14/ST-14 (`2026-07-27__release-v7.9`) | **Effort:** XS | **Provisional-Target:** TBD
**Problem:** ST-14 designed the Displacement Debt Register (format + reconstructed seed content) in full, but `claude/roadmap/*` and `claude/system/roadmap_prompt.md` are outside Sprint Execution's write scope, so the design was handed off rather than applied. Two actions are needed together: (1) create `claude/roadmap/displacement_debt_register.md` using the format/seed content in `claude/cycles/2026-07-27__release-v7.9/qa_evidence_EPIC-14.md#Displacement Debt Register — Design`; (2) edit `roadmap_prompt.md` STEP 8's "Displacement candidate flag" instruction to also update this register going forward. Landing only one half leaves either a stale instruction (no file) or an unmaintained file (no forcing function).
**Scope:** Both actions above, in the same session, per CLAUDE.md §6 Governance File Edit Checklist for the `roadmap_prompt.md` edit (version bump, `OPERATIONAL_GUIDE.md` §14 table update, `prompt_change_log.md` entry).
**Acceptance Criteria:** `claude/roadmap/displacement_debt_register.md` created with the seeded content; `roadmap_prompt.md` STEP 8 updated to reference it; `ESC-EXEC-20260727-02` closed.

---

## Roadmap Rebalance 2026-07-28__scheduled — New Items (IW-20260728-01 disposition)

*42 items filed from a 44-submission window (1 idea resolved directly — see BLG-OPS-90 gate-status update above; 2 ideas consolidated into one item — see BLG-GOV-269). All ungated unless a Gate criteria line is present.*

### BLG-GOV-266 — Canonical AI feature touchpoint register with per-feature §13 classification
**Priority:** P3 (Low) | **Type:** Governance / AI Compliance | **Owner:** AI Compliance & Governance Officer | **Source:** IDEA-ai-compliance-20260728-02 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** AI-touching features (thesis generation, daily briefing, chat advisor, cost alerts) have each had individual §13 reviews over time, but no single register lists every AI touchpoint and its current §13 classification in one place.
**Scope:** Build a register listing each AI-calling feature, its §13 classification, and a link to its review record.
**Acceptance Criteria:** Register created and covers all currently-shipped AI touchpoints; AI Compliance & Governance Officer sign-off.

---

### BLG-GOV-267 — Base44 generation failure-mode log (recurring manual-correction patterns)
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Base44 Frontend Prompt Owner | **Source:** IDEA-base44-frontend-20260728-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Base44-generated components occasionally need manual correction (e.g. missed dark-mode class pairs, contrast issues) but no log tracks which failure modes recur, so prompt-template improvements are made ad hoc rather than targeting the most frequent gaps.
**Scope:** Add a lightweight log of Base44 generation failure modes requiring manual correction, reviewed periodically to prioritise prompt-template fixes.
**Acceptance Criteria:** Log created; at least the known recurring modes (dark-mode class pairs, contrast) backfilled; Base44 Frontend Prompt Owner sign-off.

---

### BLG-GOV-271 — Agent onboarding runbook for adding a new governance role
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Director of HR | **Source:** IDEA-director-of-hr-20260728-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Adding a new agent role (most recently done for several roles across the project's history) has no documented runbook — each addition has been done ad hoc (charter file, idea-intake slug mapping, required-roles lists across multiple prompt files).
**Scope:** Document the full checklist of files/lists that must be updated when adding a new governance role.
**Acceptance Criteria:** Runbook created; Director of HR sign-off.

---

### BLG-QA-130 — Quality trend index aggregating DEV-* records over time
**Priority:** P3 (Low) | **Type:** QA / Metrics | **Owner:** Director of Quality | **Source:** IDEA-director-of-quality-20260728-02 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** There is no single trend view of deviation volume/severity over time — each cycle's deviation count is only visible in that cycle's own `sprint_close.md`.
**Scope:** Build a simple trend index (deviation count/severity per cycle, plotted or tabulated over time).
**Acceptance Criteria:** Index created and backfilled from available cycle history; Director of Quality sign-off.

---

### BLG-GOV-272 — Recurring spec-debt backlog review cadence
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Frontend Specifications & UX Documentation Owner | **Source:** IDEA-frontend-specs-20260728-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** BLG-SPEC-* items accumulate over time (105+ so far) with no defined periodic review cadence dedicated specifically to spec debt, distinct from general backlog grooming.
**Scope:** Define a periodic review cadence specifically for BLG-SPEC-* items.
**Acceptance Criteria:** Cadence defined and documented in `backlog_management_prompt.md`; Head of Specs Team confirmation.

---

### BLG-GOV-274 — Automated Specs_Index.md freshness check against live spec files
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Head of Specs Team | **Source:** IDEA-head-of-specs-20260728-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `Specs_Index.md`'s maintenance has previously lapsed silently for 5 consecutive cycles before being caught (per `2026-07-21__release-v7.7` closure Carry-Forward Item 3) — the check for staleness is currently manual.
**Scope:** Add an automated check comparing `Specs_Index.md` entries against the live `docs/specs/` tree for additions/removals it doesn't yet reflect.
**Acceptance Criteria:** Check added; Head of Specs Team sign-off.

---

### BLG-GOV-275 — Searchable index of STEP 11.4 meta-review findings across cycles
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Head of Specs Team | **Source:** IDEA-head-of-specs-20260728-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** STEP 11.4 meta-reviews produce `meta_review.md` files per triggering cycle, but there is no searchable cross-cycle index of what patterns each meta-review found or what it changed.
**Scope:** Add a lightweight index summarising each meta-review's key findings and resulting prompt changes.
**Acceptance Criteria:** Index created and backfilled from existing `meta_review.md` files; Head of Specs Team sign-off.

---

### BLG-GOV-276 — Formalise Product Value Ratio rolling-window boundary-trade handling in metrics_definitions.md
**Priority:** P3 (Low) | **Type:** Governance / Metrics | **Owner:** Metrics Definitions & Analytics Canonical Owner | **Source:** IDEA-metrics-20260728-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** STEP 2.4's Product Value Ratio is computed over "the last 5 completed cycles," but `metrics_definitions.md` does not formally specify how a cycle at the exact window boundary should be handled (e.g. a cycle completing mid-window), leaving this to ad hoc judgment each time the ratio is computed.
**Scope:** Add a formal boundary-handling rule to `metrics_definitions.md`.
**Acceptance Criteria:** Rule documented; Metrics Definitions & Analytics Canonical Owner sign-off.

---

### BLG-GOV-277 — Document exact skill-category taxonomy used for Skill-Silo classification
**Priority:** P3 (Low) | **Type:** Governance / Metrics | **Owner:** Metrics Definitions & Analytics Canonical Owner | **Source:** IDEA-metrics-20260728-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** STEP 7.1's Skill-Silo classification (Governance-heavy vs Execution-heavy) is applied consistently in practice but the exact taxonomy (which roles/story-shapes fall into which bucket) is not written down in one canonical place — it's reconstructed from precedent each cycle.
**Scope:** Document the exact classification taxonomy in `metrics_definitions.md`, consistent with how STEP 2.4's U/G/D/P taxonomy is already documented.
**Acceptance Criteria:** Taxonomy documented; Metrics Definitions & Analytics Canonical Owner sign-off.

---

### BLG-QA-132 — Staging sign-off backlog tracker (FI-P3-02 wording-only AC exceptions)
**Priority:** P3 (Low) | **Type:** QA / Process | **Owner:** QA Lead | **Source:** IDEA-qa-lead-20260728-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The `FI-P3-02` exception (wording-only ACs may substitute code review for staging sign-off) is applied per-story with no consolidated tracker of how often it's invoked, making it hard to spot if the exception is being over-relied upon.
**Scope:** Add a tracker logging each `FI-P3-02` invocation across cycles.
**Acceptance Criteria:** Tracker created and backfilled where findable; QA Lead sign-off.

---

### BLG-QA-134 — Regression suite runtime budget & reporting
**Priority:** P3 (Low) | **Type:** QA / CI | **Owner:** QA & Testing Owner | **Source:** IDEA-qa-testing-20260728-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The regression suite has grown substantially (baseline updates at `BLG-QA-112`, `BLG-QA-114`) with no defined runtime budget or reporting on whether it's trending toward becoming a CI bottleneck.
**Scope:** Define a runtime budget and add simple reporting on regression suite duration over time.
**Acceptance Criteria:** Budget defined; reporting added; QA & Testing Owner sign-off.

---

### BLG-GOV-282 — strategy_rules.md version cross-reference consistency check in dependent docs
**Priority:** P3 (Low) | **Type:** Governance / Spec Debt | **Owner:** Strategy Rules & System Intent Owner | **Source:** IDEA-strategy-owner-20260728-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Several documents cite a specific `strategy_rules.md` version (e.g. §13 review records, compliance score formulas); when `strategy_rules.md` is incremented, nothing checks whether those cross-references have gone stale.
**Scope:** Add a check comparing cited `strategy_rules.md` versions in dependent docs against the current version.
**Acceptance Criteria:** Check added; first run's findings triaged; Strategy Rules & System Intent Owner sign-off.

---


---

## Roadmap Rebalance 2026-08-11__scheduled — New Items (IW-20260809-01 disposition)

### BLG-SEC-30 — Prompt-injection resistance test for the Gemini thesis-generation endpoint
**Priority:** P2 (Medium) | **Type:** Security / AI | **Owner:** Cybersecurity & Trust Lead; AI Compliance & Governance Officer | **Source:** IDEA-ai-compliance-20260809-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** `POST /trade-plans/{plan_id}/generate-thesis` (Gemini-backed) has never had an active adversarial test confirming it resists prompt-injection attempts embedded in user-controlled trade-plan fields.
**Scope:** Design and run a prompt-injection test suite against the endpoint; document findings and any hardening applied.
**Acceptance Criteria:** Test suite run; findings documented; Cybersecurity & Trust Lead sign-off.

---

### BLG-GOV-299 — AI feature cost-vs-value retrospective (6-month actuals vs original estimates)
**Priority:** P3 (Low) | **Type:** Governance / FinOps | **Owner:** FinOps & Resource Architect; AI Compliance & Governance Officer | **Source:** IDEA-ai-compliance-20260809-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** AI features (thesis generation, journal summarisation) were costed at build time but no retrospective has compared 6 months of actual Gemini/Anthropic spend against those original estimates.
**Scope:** Compare actuals vs estimates for each shipped AI feature; note material variances.
**Acceptance Criteria:** Retrospective document filed; FinOps & Resource Architect sign-off.

---

### BLG-SPEC-119 — Deprecated/superseded endpoint sunset tracker
**Priority:** P3 (Low) | **Type:** Spec Debt / API Governance | **Owner:** API Contracts & Documentation Owner | **Source:** IDEA-api-contracts-20260809-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The API endpoint deprecation-window policy (`BLG-SPEC-96`) defines the *process* for deprecating an endpoint but there is no single tracker of which endpoints are currently mid-deprecation-window.
**Scope:** Add a tracker (or a canonical section in `conventions.md`) listing currently-deprecating endpoints and their sunset dates.
**Acceptance Criteria:** Tracker added; API Contracts & Documentation Owner sign-off.

---

### BLG-SPEC-120 — Contract example-payload freshness check against live response shape
**Priority:** P3 (Low) | **Type:** Spec Debt / API Governance | **Owner:** API Contracts & Documentation Owner | **Source:** IDEA-api-contracts-20260809-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Several `docs/specs/api_contracts/*.md` example payloads have previously been found stale against the live response shape (e.g. `BLG-SPEC-112`–`115` at `v8.4`); no recurring check catches this proactively.
**Scope:** Add a recurring spot-check (or automate via the existing OpenAPI drift tooling) comparing example payloads against live responses.
**Acceptance Criteria:** Check added/scheduled; API Contracts & Documentation Owner sign-off.

---

### BLG-BE-89 — Extend the BLG-BE-57 retry/backoff audit pattern to Gemini API call sites
**Priority:** P2 (Medium) | **Type:** Backend Engineering / Reliability | **Owner:** Backend Engineering Patterns Owner | **Source:** IDEA-backend-engineering-20260809-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** `BLG-BE-57` audited Alpaca API rate-limit backoff handling; the same audit has not been extended to Gemini API call sites (thesis generation, cost tracking).
**Scope:** Audit Gemini call sites for retry/backoff handling; apply the same pattern used for Alpaca where gaps are found.
**Acceptance Criteria:** Audit complete; gaps fixed or filed; Backend Engineering Patterns Owner sign-off.

---

### BLG-BE-90 — N+1 query audit across trade/position list endpoints
**Priority:** P2 (Medium) | **Type:** Backend Engineering / Performance | **Owner:** Backend Engineering Patterns Owner | **Source:** IDEA-backend-engineering-20260809-02 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** No systematic audit has confirmed the trade/position list endpoints are free of N+1 query patterns as the schema and join complexity has grown across Arc 4/5 additions.
**Scope:** Audit `GET /trades`, `GET /positions`, and related list endpoints for N+1 patterns; fix or file follow-ups.
**Acceptance Criteria:** Audit complete; findings fixed or filed; Backend Engineering Patterns Owner sign-off.

---

### BLG-SPEC-121 — Base44 prompt-version provenance tag on generated components
**Priority:** P3 (Low) | **Type:** Spec Debt / Frontend Tooling | **Owner:** Base44 Frontend Prompt Owner | **Source:** IDEA-base44-frontend-20260809-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Components generated via a Base44 prompt template carry no record of which template version produced them, making drift audits (like the v6.7 token-drift audit) harder to scope.
**Scope:** Define a lightweight provenance convention (e.g. a comment header) tagging generated components with their source template version.
**Acceptance Criteria:** Convention documented in `base44_prompt_template_library.md`; Base44 Frontend Prompt Owner sign-off.

---

### BLG-SPEC-122 — Base44 regeneration diff checklist — design-token compliance pass
**Priority:** P3 (Low) | **Type:** Spec Debt / Frontend Tooling | **Owner:** Base44 Frontend Prompt Owner | **Source:** IDEA-base44-frontend-20260809-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** When a component is regenerated via Base44, there is no checklist confirming the regenerated output still complies with current design tokens (a recurring source of drift, e.g. `BLG-FE-91`).
**Scope:** Add a regeneration diff checklist to the Base44 prompt template library.
**Acceptance Criteria:** Checklist added; Base44 Frontend Prompt Owner sign-off.

---

### BLG-SEC-31 — Rate-limit audit on unauthenticated/low-auth endpoints
**Priority:** P2 (Medium) | **Type:** Security | **Owner:** Cybersecurity & Trust Lead | **Source:** IDEA-cybersecurity-20260809-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** No audit has confirmed which endpoints lack rate-limiting, and whether the unauthenticated/low-auth ones (e.g. health checks) are appropriately protected against abuse.
**Scope:** Audit endpoint rate-limiting coverage; file fixes for any unprotected unauthenticated endpoint.
**Acceptance Criteria:** Audit complete; gaps fixed or filed; Cybersecurity & Trust Lead sign-off.

---

### BLG-SEC-32 — Dependency license compliance scan
**Priority:** P3 (Low) | **Type:** Security / Compliance | **Owner:** Cybersecurity & Trust Lead | **Source:** IDEA-cybersecurity-20260809-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The recurring dependency-vulnerability re-scan cadence (`BLG-SEC-15`) checks for vulnerabilities but not license compliance; no scan has confirmed all dependencies carry compatible licenses.
**Scope:** Run a license compliance scan across `backend/requirements.txt` and `package.json`; document findings.
**Acceptance Criteria:** Scan run; any incompatible license flagged and resolved; Cybersecurity & Trust Lead sign-off.

---

### BLG-BE-91 — Enforce trade-plan linkage at position entry + DB-level safeguard against orphaned trade_plans rows
**Priority:** P1 (High) — escalated from standard idea-intake priority, 2026-08-11, roadmap rebalance (see rationale below) | **Type:** Backend Engineering / Data Integrity | **Owner:** Data Model, Domain & Schema Owner; Backend Engineering Patterns Owner; Product Owner | **Source:** IDEA-data-model-20260809-01 + IDEA-product-owner-20260809-01 (consolidated, genuine same-root-cause overlap per v9.0 convention) | **Effort:** M | **Provisional-Target:** TBD
> ⚠️ **Priority escalation (2026-08-11, roadmap rebalance STEP 7.1):** Raised to P1 as the Product Owner's named structural response to this cycle's mandatory Skill-Silo pull-forward finding — this item directly targets the root cause (0/11 trade plans currently linked to positions) blocking SI-02's gate condition 1 and, transitively, the entire Arc 5 UX-prep cluster and most of the remaining gated U-item pool. See `cycle_record.md` STEP 7.1.
**Problem:** `BLG-BE-46`'s forward-fix (shipped v6.8) auto-links *new* trade plans to positions going forward, but does not backfill, and — more importantly — nothing *enforces* the linkage at entry time, so it remains possible to create a position without a linked trade plan (or a trade plan without a subsequent linked position). This is the exact fact keeping SI-02's gate condition 1 (≥20 linked trade plans) at 0 despite 20 total closed trades existing. `BLG-FE-109` (shipped v7.3) made linkage the path of least resistance from the UX side but does not enforce it at the data layer.
**Scope:** (1) Product-side: confirm/strengthen the entry flow so a trade plan is linked at position creation as the default path, not an optional one; (2) DB-level: add a safeguard (constraint, trigger, or scheduled integrity check) that flags or prevents a new orphaned `trade_plans` row going forward, so this gap cannot silently recur a second time.
**Acceptance Criteria:** Entry-flow linkage confirmed enforced (staging-verified); DB-level safeguard implemented and tested; Data Model, Domain & Schema Owner + Product Owner sign-off.

---

### BLG-QA-140 — Field-population completeness audit for Arc 6 prerequisite fields
**Priority:** P3 (Low) | **Type:** QA / Data Quality | **Owner:** Data Model, Domain & Schema Owner; QA & Testing Owner | **Source:** IDEA-data-model-20260809-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Arc 6 features (PS-01–05) require `regime_at_entry`, `setup_type`, and similar fields to be populated on every new trade; no audit has confirmed population completeness ahead of the 50/100-trade gates being reached.
**Scope:** Audit population completeness of Arc 6 prerequisite fields across recent trades; fix any gap found.
**Acceptance Criteria:** Audit complete; gaps fixed or filed; QA & Testing Owner sign-off.

---

### BLG-GOV-300 — Formal alert threshold for the cross-role workload-concentration check
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Director of HR; Head of Specs Team | **Source:** IDEA-director-of-hr-20260809-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `roadmap_prompt.md` §7.2's cross-role workload balance check (`BLG-GOV-270`) surfaces an advisory at a 40% ceiling (mirroring §7.1) but has no independently-justified threshold of its own — it borrowed §7.1's number by analogy.
**Scope:** Assess whether 40% is the right threshold for cross-role (as opposed to governance-vs-execution) concentration, or whether a distinct threshold is warranted.
**Acceptance Criteria:** Assessment filed; threshold confirmed or revised in `roadmap_prompt.md` §7.2; Director of HR sign-off.

---

### BLG-GOV-301 — Cross-role escalation response-time tracker
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Director of HR; PMO Lead | **Source:** IDEA-director-of-hr-20260809-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Escalations to named roles (e.g. Head of Specs Team 72-hour SLAs) are tracked individually but there is no aggregate view of response-time trends across roles.
**Scope:** Add a tracker aggregating escalation response times by role across cycles.
**Acceptance Criteria:** Tracker added; PMO Lead sign-off.

---

### BLG-QA-141 — DEV-* deviation recurrence pattern report
**Priority:** P3 (Low) | **Type:** QA / Process | **Owner:** Director of Quality | **Source:** IDEA-director-of-quality-20260809-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The cross-cycle deviation consolidation review (`BLG-QA-129`) checks for concentration by spec file but not by root cause — no report groups `DEV-*` records by whether the same underlying defect class recurs across different stories.
**Scope:** Add a root-cause grouping pass to the deviation consolidation review.
**Acceptance Criteria:** Report produced for the current deviation set; Director of Quality sign-off.

---

### BLG-QA-142 — Definition-of-Done compliance spot-check across the last 5 cycles
**Priority:** P3 (Low) | **Type:** QA / Process | **Owner:** Director of Quality | **Source:** IDEA-director-of-quality-20260809-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** No periodic spot-check confirms DoQ sign-off blocks across recent cycles genuinely meet the Definition-of-Done bar (as opposed to the automated staleness lint at `BLG-QA-98`, which only checks for stale "Pending" rows, not substantive compliance).
**Scope:** Spot-check a sample of DoQ sign-offs from the last 5 cycles against the Definition-of-Done checklist.
**Acceptance Criteria:** Spot-check complete; findings documented; Director of Quality sign-off.

---

### BLG-BE-92 — Multi-currency cost-basis rounding consistency check
**Priority:** P2 (Medium) | **Type:** Backend Engineering / Financial Correctness | **Owner:** Financial Reporting & Records Owner | **Source:** IDEA-financial-reporting-20260809-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** UK (.L) and US market positions use different currency cost-basis calculations; no check confirms rounding behaviour is consistent (and correctly specified) across both.
**Scope:** Audit cost-basis rounding across currencies; document and fix any inconsistency found.
**Acceptance Criteria:** Audit complete; any inconsistency fixed; Financial Reporting & Records Owner sign-off.

---

### BLG-BE-93 — Closed-trade export completeness check against tax-year boundary edge cases
**Priority:** P2 (Medium) | **Type:** Backend Engineering / Financial Correctness | **Owner:** Financial Reporting & Records Owner | **Source:** IDEA-financial-reporting-20260809-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The tax-year P&L CSV export has not been specifically checked for trades that close exactly on a tax-year boundary date — an edge case that could cause a trade to be silently omitted from or double-counted across two exports.
**Scope:** Test the export against boundary-date trades; fix any gap found.
**Acceptance Criteria:** Boundary-case test added and passing; Financial Reporting & Records Owner sign-off.

---

### BLG-OPS-139 — Render Starter-tier headroom reassessment
**Priority:** P2 (Medium) | **Type:** Operations / Infrastructure | **Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner | **Source:** IDEA-finops-20260809-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The last Render tier/headroom assessment predates the Arc 5 analytics endpoints and current trade volume; capacity margin has not been reconfirmed since.
**Scope:** Reassess current Render Starter-tier headroom against current load (trade volume, Arc 5 endpoint traffic).
**Acceptance Criteria:** Reassessment filed; tier confirmed adequate or upgrade recommended; FinOps & Resource Architect sign-off.

---

### BLG-GOV-302 — Idea-intake / roadmap-session compute cost attribution
**Priority:** P3 (Low) | **Type:** Governance / FinOps | **Owner:** FinOps & Resource Architect | **Source:** IDEA-finops-20260809-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Governance overhead (idea intake, roadmap rebalance sessions) consumes compute/session cost that is not separately attributed from delivery spend, making it hard to assess the true cost-of-governance ratio.
**Scope:** Add a lightweight cost-attribution note distinguishing governance-overhead sessions from delivery sessions.
**Acceptance Criteria:** Attribution method documented and applied to at least one cycle retrospectively; FinOps & Resource Architect sign-off.

---

### BLG-SPEC-123 — Component prop-naming convention consistency audit
**Priority:** P3 (Low) | **Type:** Spec Debt / Frontend | **Owner:** Frontend Specifications & UX Documentation Owner | **Source:** IDEA-frontend-specs-20260809-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** No audit has confirmed component prop names follow a consistent convention across the codebase — prior drift audits have focused on design tokens and colour, not prop naming.
**Scope:** Audit prop-naming consistency across shared components; document the convention and fix drift.
**Acceptance Criteria:** Audit complete; convention documented in `design_system.md`; Frontend Specifications & UX Documentation Owner sign-off.

---

### BLG-SPEC-124 — Canonical "gated" DataState variant and visual/interaction spec for not-yet-unlocked feature surfaces
**Priority:** P2 (Medium) | **Type:** Spec Debt / Frontend Design | **Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design | **Source:** IDEA-frontend-specs-20260809-02 + IDEA-head-of-ux-20260809-02 (consolidated, explicit companion-piece overlap per v9.0 convention) | **Effort:** M | **Provisional-Target:** TBD
**Problem:** The `design_system.md` DataState pattern (`BLG-SPEC-98` consolidation) does not yet include a canonical "gated"/"not-yet-unlocked" variant, despite the backlog containing a large and growing cluster of gate-blocked features (Arc 5 UX-prep, Arc 6) that will eventually need a consistent way to say "locked" — visually and interactively, not just in copy.
**Scope:** Define the canonical gated DataState variant (visual treatment) and its interaction spec (what happens on hover/click of a locked surface).
**Acceptance Criteria:** Variant and interaction spec added to `design_system.md`; Head of UX & Design sign-off.

---

### BLG-QA-143 — Consolidated backend service-layer test-coverage report
**Priority:** P3 (Low) | **Type:** QA / Testing | **Owner:** Head of Engineering; QA & Testing Owner | **Source:** IDEA-head-of-engineering-20260809-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** No consolidated report identifies which `backend/services/*.py` files lack a direct unit test, making coverage gaps hard to spot without an ad hoc grep each time.
**Scope:** Generate a consolidated report of service files without direct unit test coverage.
**Acceptance Criteria:** Report generated; gaps triaged; QA & Testing Owner sign-off.

---

### BLG-BE-94 — Pre-Trade Research View query-latency budget review
**Priority:** P3 (Low) | **Type:** Backend Engineering / Performance | **Owner:** Head of Engineering | **Source:** IDEA-head-of-engineering-20260809-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The Pre-Trade Research View (PT-02, shipped v3.2) has not had a latency review since — over a year of data growth and added panels (Alpaca news, drift streak metric) may have shifted its query budget.
**Scope:** Review current query latency for the Research View's data sources; confirm still within an acceptable budget.
**Acceptance Criteria:** Review complete; any regression fixed or filed; Head of Engineering sign-off.

---

### BLG-SPEC-125 — Spec-to-backlog traceability audit
**Priority:** P3 (Low) | **Type:** Spec Debt / Governance | **Owner:** Head of Specs Team | **Source:** IDEA-head-of-specs-20260809-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** No audit confirms every `docs/specs/` file is either linked to an active/shipped backlog item or explicitly marked historical — spec files can silently become orphaned as features evolve.
**Scope:** Audit `docs/specs/` for orphaned files; link or mark historical as appropriate.
**Acceptance Criteria:** Audit complete; orphans resolved; Head of Specs Team sign-off.

---

### BLG-SPEC-126 — Canonical glossary consolidation
**Priority:** P3 (Low) | **Type:** Spec Debt / Governance | **Owner:** Head of Specs Team | **Source:** IDEA-head-of-specs-20260809-02 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** Terms (e.g. "drift score", "compliance score", "grace period") are defined independently and sometimes inconsistently across `strategy_rules.md`, `metrics_definitions.md`, and `data_model.md`.
**Scope:** Consolidate a canonical glossary cross-referencing each term's authoritative definition location.
**Acceptance Criteria:** Glossary created; Head of Specs Team sign-off.

---

### BLG-FEAT-84 — Thesis pre-mortem / invalidation-condition capture at trade-plan entry
**Priority:** P3 (Low) | **Type:** Product Feature | **Owner:** Head of UX & Design; Product Owner | **Source:** IDEA-head-of-ux-20260809-01 | **Effort:** M | **Provisional-Target:** TBD
**Problem:** The trade plan captures entry thesis but not an explicit "what would prove this thesis wrong" (invalidation condition) at the point of entry — a pre-mortem is a well-established discipline technique this system's own structured checklists do not yet capture.
**Scope:** Add an optional invalidation-condition field to the trade plan entry flow.
**Acceptance Criteria:** Field added; captured on new trade plans; Product Owner sign-off.

---

### BLG-OPS-140 — Render dashboard-only build/deploy path filter — canonical documentation + onboarding note
**Priority:** P2 (Medium) | **Type:** Operations / Infrastructure | **Owner:** Infrastructure & Operations Owner | **Source:** IDEA-infra-ops-20260809-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Render's dashboard-only build/deploy path filter setting is invisible to a repo-only search (it lives in the Render dashboard, not version control), and has already caused two silent-drift incidents (`BLG-OPS-82`, `BLG-OPS-90`) where a runtime-read file change was outside the configured filter path.
**Scope:** Document the current filter configuration canonically (e.g. in `docs/ops/`) and add an onboarding note flagging this as a dashboard-only setting to check whenever a new runtime-read file is added outside the existing filtered paths.
**Acceptance Criteria:** Documentation added; Infrastructure & Operations Owner sign-off.

---

### BLG-OPS-141 — Staging environment data-reset cadence review
**Priority:** P3 (Low) | **Type:** Operations / Infrastructure | **Owner:** Infrastructure & Operations Owner | **Source:** IDEA-infra-ops-20260809-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** No defined cadence exists for resetting staging environment data; stale or accumulated staging data can make staging verification runs less representative over time.
**Scope:** Review current staging data state and define an appropriate reset cadence.
**Acceptance Criteria:** Cadence defined and documented; Infrastructure & Operations Owner sign-off.

---

### BLG-SPEC-127 — Formal definition for the "90-day trade window" cited in SI-02 gate reporting
**Priority:** P3 (Low) | **Type:** Spec Debt | **Owner:** Metrics Definitions & Analytics Canonical Owner | **Source:** IDEA-metrics-20260809-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** SI-02 gate reporting cites a "90-day trade window" (`_WINDOW_DAYS = 90` in `behavioural_drift_service.py`, cross-referenced at `si02_drift_score.md` §2) informally in `current_roadmap.md` prose; the window itself (rolling vs fixed, timezone handling) is not formally specified.
**Scope:** Add a formal definition of the 90-day window's exact semantics to `si02_drift_score.md`.
**Acceptance Criteria:** Definition added; Metrics Definitions & Analytics Canonical Owner sign-off.

---

### BLG-SPEC-128 — Gate-metric naming consistency across roadmap, SI-05 digest, and Reports page
**Priority:** P3 (Low) | **Type:** Spec Debt | **Owner:** Metrics Definitions & Analytics Canonical Owner | **Source:** IDEA-metrics-20260809-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The same gate metrics (e.g. SI-02 linked-trade-plan count) are referenced with slightly different naming/phrasing across `current_roadmap.md`, the SI-05 digest content, and the Reports page's SI-02 Gate Status section.
**Scope:** Standardise gate-metric naming across the three surfaces.
**Acceptance Criteria:** Naming standardised; Metrics Definitions & Analytics Canonical Owner sign-off.

---

### BLG-GOV-303 — Roadmap Unlock Tracker — consolidated view of all gated features and their conditions
**Priority:** P2 (Medium) | **Type:** Governance / Roadmap Documentation | **Owner:** PMO Lead; Product Owner | **Source:** IDEA-pmo-lead-20260809-01 + IDEA-product-owner-20260809-02 (consolidated, both propose making the same structural reality visible in one place, per v9.0 convention) | **Effort:** M | **Provisional-Target:** TBD
**Problem:** The roadmap's remaining gated features (SI-02, SI-04, SI-05 Phase 2, PO-02/04/05, PS-01–05, plus the Arc 5 UX-prep cluster) each state their own gate condition individually, but there is no single place showing all gates and their current clearance status together — this cycle's own findings (STEP 2.3, STEP 7.1) had to be manually cross-referenced across `current_roadmap.md` and `backlog.md` to establish that most of the roadmap is currently blocked on a small number of shared root causes.
**Scope:** Build a consolidated "Roadmap Unlock Tracker" section (in `current_roadmap.md` or a companion document) listing every gated feature, its condition, current status, and — where applicable — which other gates share the same underlying blocker. This formally recognises what this cycle informally found: the back half of the roadmap is substantially data-density-blocked on a small number of shared conditions.
**Acceptance Criteria:** Tracker created; cross-referenced from `current_roadmap.md` §6; PMO Lead + Product Owner sign-off.

---

### BLG-GOV-304 — Recurring data-density gate trajectory re-estimate cadence
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** PMO Lead | **Source:** IDEA-pmo-lead-20260809-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `BLG-GOV-34` (v4.6) was a one-time assessment of data-density gate clearance trajectories (e.g. "at current rate, gate X clears in ~N weeks"); it has never been re-run and is now 3+ months stale.
**Scope:** Define a recurring cadence for re-estimating data-density gate trajectories (e.g. every N scheduled rebalances) rather than a one-time assessment.
**Acceptance Criteria:** Cadence defined; first re-estimate run; PMO Lead sign-off.

---

### BLG-QA-144 — Playwright coverage gap audit for Arc5ComplianceSection
**Priority:** P3 (Low) | **Type:** QA / Testing | **Owner:** QA Lead | **Source:** IDEA-qa-lead-20260809-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `Arc5ComplianceSection` (shipped v4.0) has grown several sub-features since (drift streak metric, sparkline candidates) without a corresponding audit confirming Playwright coverage has kept pace.
**Scope:** Audit current Playwright coverage of `Arc5ComplianceSection`; file gaps found.
**Acceptance Criteria:** Audit complete; gaps filed; QA Lead sign-off.

---

### BLG-QA-145 — Test-environment parity check — local vs CI vs staging config drift
**Priority:** P3 (Low) | **Type:** QA / Infrastructure | **Owner:** QA Lead; Infrastructure & Operations Owner | **Source:** IDEA-qa-lead-20260809-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** No check confirms local dev, CI, and staging environments remain configuration-consistent (env vars, dependency versions) — drift here can cause "works locally, fails in CI/staging" defects.
**Scope:** Audit configuration parity across the three environments; document and fix drift found.
**Acceptance Criteria:** Audit complete; drift fixed or documented as intentional; QA Lead sign-off.

---

### BLG-QA-146 — backend/routers/test.py completeness re-audit
**Priority:** P3 (Low) | **Type:** QA / Testing | **Owner:** QA & Testing Owner | **Source:** IDEA-qa-testing-20260809-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** The endpoint-registration test-completeness gate has been in place for several cycles; no recent re-audit confirms zero drift has crept in since introduction.
**Scope:** Re-audit `backend/routers/test.py` against all `@router.*` decorators for completeness.
**Acceptance Criteria:** Re-audit complete; any gap fixed; QA & Testing Owner sign-off.

---

### BLG-QA-147 — Regression suite runtime budget & trend report (last 90 days)
**Priority:** P3 (Low) | **Type:** QA / CI | **Owner:** QA & Testing Owner | **Source:** IDEA-qa-testing-20260809-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `BLG-QA-134` (v7.9 window) defined a runtime budget but no trend report has been produced yet showing whether the suite is tracking within or drifting beyond it over the last 90 days.
**Scope:** Produce the first 90-day trend report against the `BLG-QA-134` budget.
**Acceptance Criteria:** Trend report produced; QA & Testing Owner sign-off.

---

### BLG-GOV-305 — §13 policy question: are confidence-interval-qualified "preview" analytics compatible with the deterministic/non-predictive boundary?
**Priority:** P2 (Medium) | **Type:** Governance / Strategy Policy | **Owner:** Strategy Rules & System Intent Owner | **Source:** IDEA-strategy-owner-20260809-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** Arc 6 items (PS-01/PS-02-style) are gated on trade-count thresholds (50+) before shipping; no policy has considered whether a confidence-interval-qualified "preview" version below the gate (explicitly labelled as statistically provisional) would remain §13-compliant, potentially offering earlier partial value without violating the deterministic/non-predictive boundary.
**Scope:** Strategy Rules & System Intent Owner to formally assess this policy question and record a determination (permitted / not permitted / permitted with conditions).
**Acceptance Criteria:** Determination recorded, citing the relevant `strategy_rules.md §13` clause; Strategy Rules & System Intent Owner sign-off.

---

### BLG-GOV-306 — Strategy rules change-justification template
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Strategy Rules & System Intent Owner | **Source:** IDEA-strategy-owner-20260809-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** When `strategy_rules.md` is version-bumped, there is no required template ensuring the change cites the trade-history evidence (if any) motivating it — SI-04 (Strategy Version Comparison) will eventually need this history to be traceable.
**Scope:** Add a change-justification template section to `strategy_rules.md`'s own change-log convention.
**Acceptance Criteria:** Template added; applied to the next `strategy_rules.md` version bump; Strategy Rules & System Intent Owner sign-off.

---

## Release Slice — v8.6 (ephemeral)

<!-- release-plan-marker: RP:v8.6:2026-08-11__release-v8.6 -->

> This section is written by the Release Planning Engine and is temporary. It records which backlog items are committed to release `v8.6` (cycle `2026-08-11__release-v8.6`). Full acceptance criteria live in `claude/cycles/2026-08-11__release-v8.6/stage4_backlog_slice.md` — that file is the authoritative source. This section must be removed during the next `groom backlog` run after the cycle closes; any still-open items within it must be promoted to the appropriate §1–§8 type section first (per the Placement Rule above).

26 items committed to v8.6, across 6 EPICs:

- **EPIC-01** (User-Facing Product Features): `BLG-FEAT-32`, `BLG-FEAT-56`
- **EPIC-02** (Trade-Plan Data Integrity Foundation): `BLG-BE-91`
- **EPIC-03** (Frontend Design Consistency & Correctness Carryover): `BLG-FE-147`, `BLG-FE-148`, `BLG-FE-149`, `BLG-FE-150`, `BLG-FE-153`, `BLG-FE-154`, `BLG-FE-155`
- **EPIC-04** (Backend & Financial Correctness): `BLG-BE-88`, `BLG-BE-92`, `BLG-BE-93`, `BLG-SEC-29`
- **EPIC-05** (QA Test-Coverage Debt Closure): `BLG-QA-136`, `BLG-QA-137`, `BLG-QA-138`, `BLG-QA-139`
- **EPIC-06** (Operations & Governance Debt Closure): `BLG-OPS-136`, `BLG-OPS-137`, `BLG-OPS-138`, `BLG-GOV-294`, `BLG-GOV-295`, `BLG-GOV-296`, `BLG-GOV-297`, `BLG-GOV-298`

---
