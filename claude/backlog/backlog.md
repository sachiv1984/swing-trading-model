# Product Backlog — Momentum Trading Assistant

**Owner:** Product Owner
**Status:** Active
**Class:** Planning Document (Class 4)
**Last Updated:** 2026-09-03 (Sprint Execution EPIC-01/ST-02 post-merge resolution, cycle `2026-08-21__release-v9.0` — BLG-BE-107 marked ✅ COMPLETE with resolution note); prior — 2026-08-21 (session — 2 new items added: BLG-BE-110, BLG-TECH-18, backend layering-boundary and npm dependency-upgrade findings from ST-23/ST-27's reviews — synced onto this branch from EPIC-05); prior — 2026-08-21 (session — 1 new item added: BLG-GOV-314, governance_sync.yml auto-close gap on split work/state commits); prior history retained — see prior entries in version control.
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

## Release Slice — v9.0 (ephemeral — remove at next `groom backlog` after cycle closes)

<!-- release-plan-marker: RP:v9.0:2026-08-21__release-v9.0 -->

27 items committed to `2026-08-21__release-v9.0`. Full acceptance criteria: `claude/cycles/2026-08-21__release-v9.0/stage4_backlog_slice.md`.

| ST | Source | Epic | Priority | Effort |
|----|--------|------|----------|--------|
| ST-01 | BLG-BE-109 | EPIC-01 | P1 | S |
| ST-02 | BLG-BE-107 | EPIC-01 | P2 | S |
| ST-03 | BLG-BE-108 | EPIC-01 | P2 | S |
| ST-04 | BLG-TECH-17 | EPIC-01 | P3 | S |
| ST-05 | BLG-TECH-15 | EPIC-01 | P2 | M |
| ST-06 | BLG-BE-105 | EPIC-02 | P1 | S |
| ST-07 | BLG-FEAT-93 | EPIC-02 | P3 | S |
| ST-08 | BLG-BE-106 | EPIC-02 | P3 | S |
| ST-09 | BLG-BE-49 | EPIC-02 | P3 | S |
| ST-10 | BLG-FE-164 | EPIC-02 | P3 | S |
| ST-11 | BLG-QA-153 | EPIC-02 | P3 | S |
| ST-12 | BLG-OPS-103 | EPIC-03 | P2 | S |
| ST-13 | BLG-OPS-25 | EPIC-03 | P2 | M |
| ST-14 | BLG-OPS-90 | EPIC-03 | P2 | M |
| ST-15 | BLG-OPS-147 | EPIC-03 | P3 | XS |
| ST-16 | BLG-OPS-148 | EPIC-03 | P2 | S |
| ST-17 | BLG-QA-26 | EPIC-04 | P2 | M |
| ST-18 | BLG-QA-81 | EPIC-04 | P2 | M |
| ST-19 | BLG-QA-89 | EPIC-04 | P2 | S |
| ST-20 | BLG-QA-144 | EPIC-04 | P3 | S |
| ST-21 | BLG-QA-83 | EPIC-04 | P3 | S |
| ST-22 | BLG-QA-84 | EPIC-04 | P3 | S |
| ST-23 | BLG-BE-56 | EPIC-05 | P3 | S |
| ST-24 | BLG-BE-54 | EPIC-05 | P3 | S |
| ST-25 | BLG-OPS-101 | EPIC-05 | P3 | S |
| ST-26 | BLG-OPS-95 | EPIC-05 | P3 | S |
| ST-27 | BLG-OPS-98 | EPIC-05 | P3 | S |

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

### BLG-GOV-307 — Extract PVR and Skill-Silo metrics from last_rebalance_outcome prose into top-level state fields
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Governance-automation tooling review — 2026-08-13
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`.claude_current_state.json`'s `last_rebalance_outcome` field carries the Product Value Ratio (PVR) and Skill-Silo rolling-average readings that `roadmap_prompt.md` computes each rebalance — including Alert-tier thresholds (PVR < 0.30; a worsening 3-cycle Skill-Silo streak) that trigger mandatory pull-forward behaviour — but only as free text embedded in a long prose outcome summary. There is no direct field to read either number from; any automation wanting to trend-alert on these readings (e.g. a scheduled check that flags a new Alert-tier reading without waiting for the next `run roadmap` session) has to parse prose, which is brittle against wording changes. Raised alongside a governance-automation review that added `claude/schemas/state_field_owners.json`, `claude/schemas/execution_state.schema.json`, and three new hooks/workflows (branch `chore/governance-automation-tooling`) — this item is the one improvement from that review requiring an actual change to governance content (`claude/system/lifecycle_schema.json`, `claude/system/roadmap_prompt.md`), so it is filed here for the roadmap engine's own sanctioned process rather than made ad hoc.

**Scope**
- Add `last_rebalance_pvr` (number) and `last_skill_silo_rolling_avg` (number) top-level fields to `claude/system/lifecycle_schema.json`
- Update `roadmap_prompt.md` to write both fields directly at the same STEP that currently composes `last_rebalance_outcome`'s prose summary, alongside the existing text (not a replacement — the prose stays, for narrative context)
- Add both new fields to `claude/schemas/state_field_owners.json` (owner: `roadmap_prompt.md`, Phase 1) in the same change
- Apply the standard governance file edit checklist per CLAUDE.md §6 (version bump, OPERATIONAL_GUIDE.md §14, prompt_change_log.md)

**Acceptance Criteria**
- `last_rebalance_pvr` and `last_skill_silo_rolling_avg` are present as top-level numeric fields in `.claude_current_state.json` after the next `run roadmap` invocation
- Both fields are documented in `claude/schemas/state_field_owners.json`
- `last_rebalance_outcome`'s existing prose summary is unchanged in content (fields are additive, not a replacement)
- Head of Specs Team sign-off

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

> ⚠️ **Partially pre-met (backlog audit 2026-08-13):** The gate has cleared and most of the core scope already shipped — `backend/services/plan_vs_reality_service.py` (`GET /trades/{id}/plan-vs-reality`) already links trades to their governing plan and computes `r_achieved` vs `r_target` (`r_delta`) per closed trade, contradicting this item's problem statement that the comparison "cannot currently be attributed." Only the aggregate "plan-adhered vs plan-deviated outcome comparison" scope bullet appears unbuilt. Recommend Product Owner narrow this item to that residual aggregate-reporting scope at next `groom backlog`/`plan release`.

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

> ⚠️ **Partially pre-met (backlog audit 2026-08-13):** `entry_delta_pct` is already captured at trade close (`backend/services/plan_vs_reality_service.py::_compute_entry_delta_pct()`), contradicting this item's problem statement that it "is not yet captured." Half the gate condition is therefore met — only the ≥20-linked-trades count remains to verify. The discipline metric and R-multiple correlation reporting layer remain unbuilt. Recommend Product Owner re-check the trade-count gate and narrow this item to the reporting-layer scope if still open.

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
**Provisional-Target:** Unscheduled — do not re-check before 2026-11-09 or 10 new linked trade_plans, whichever first (PO disposition 2026-08-17, see below); `[gate status unverified/unmet]` — BLG-GOV-107 gate conditions last confirmed NOT MET 2026-07-21 (9th consecutive identical reading); not independently reconfirmed since; may not enter sprint planning until independently reconfirmed met
**Depends on:** BLG-FE-56, BLG-FE-57, BLG-FE-58, BLG-FE-59 (UI extension specs); BLG-BE-27, BLG-BE-29 (perf baseline, index review) — all currently gate-conditional on this item entering sprint planning

> ⚠️ **PO disposition — re-check cadence reset (2026-08-17, ad hoc session, acting Product Owner per explicit user direction):** Reviewed without a fresh live query (this session has no production DB/API credentials — dev-only `.env`, consistent with every prior in-session attempt, e.g. `2026-07-24__release-v7.8` run_manifest's 401). Decision: remain excluded from firm scope, **and** stop the every-cycle identical-reading re-check pattern (9 consecutive NOT MET readings 2026-07-12→2026-07-21, zero movement, each one a wasted live-query cycle). Rationale for the reset: gate Condition 1's root cause (0/11 linked `trade_plans`) was structurally fixed by `BLG-BE-91` (enforce trade-plan linkage at position entry — shipped v8.6, 2026-08-11), so the blocker is no longer "nothing is being linked," it's "not enough time/volume has passed since the fix went live" — only 6 days as of this session, nowhere near enough for ≥20 *new* closed, linked trades to accrue. Re-checking every cycle in the meantime cannot produce a different reading and has already cost 9 cycles of live-query overhead. New re-check trigger: **no earlier than 2026-11-09** (90 days post-`BLG-BE-91` ship, a realistic accrual window at this system's trade volume) **or** when a cheap milestone check (10 new `trade_plans` rows created with `position_id` populated post-2026-08-11) is hit, whichever comes first — PMO Lead to action per its existing gate-recheck ownership (`current_roadmap.md` SI-02 entry). This item remains Arc 5's flagship "tell me when I'm deviating from my own rules" feature (backend live since v4.6, zero UI) — once the gate clears this should be a near-immediate sprint-planning candidate, not re-litigated from scratch.

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
**Provisional-Target:** Unscheduled (gated — §13 determinism pre-clearance not yet run)
**Depends on:** IT-06 Alpaca Paper Trading Integration (shipped v3.5) — foundational infrastructure this feature reuses

> PO re-deferral 2026-08-21: `Provisional-Target` corrected from the stale `v7.7` anchor (DL-074, named 2026-07-21, shipped 2026-07-24 without this item ever entering a sprint) to `Unscheduled (gated)`, matching the item's actual state — the real blocker is that nobody has run the §13 determinism pre-clearance review yet, not a scheduling gap per se. Priority remains P1 and the roadmap's "highest-value long-term validation feature" framing stands; this item should be re-targeted to a specific release once the §13 pre-clearance review (Strategy Rules & System Intent Owner) is scheduled and completed, not before.

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

> ⚠️ **Partially pre-met (backlog audit 2026-08-13):** The gate has cleared — `POST /trade-plans/{plan_id}/generate-thesis` (backend/routers/trade_plans.py) already generates AI trade plan summaries via Claude, and already logs to an append-only `claude_audit_log` table (backend/database.py::ensure_claude_audit_log_table) with `endpoint, model_id, prompt_version, input_tokens, output_tokens, cost_usd, generated_at`. This covers the item's intent but uses different field names than the AC's proposed schema (`plan_id, model_version, prompt_version, input_hash, output_hash`) and no explicit 90-day retention policy is confirmed for this specific table. Recommend Product Owner confirm whether the existing `claude_audit_log` schema satisfies this item's governance requirement as-is, or whether the field-level gap needs closing.

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

### BLG-OPS-53 — Application log retention policy expansion (Supabase + claude_audit_log)
**Priority:** P3 (Low)
**Type:** Operations / Data Lifecycle
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Source:** IDEA-infra-ops-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** claude_audit_log table 6+ months old (~Nov 2026, since v4.0 ship 2026-05-22). BLG-OPS-31 (Render log retention policy) shipped v4.7; this extends scope to Supabase query logs and claude_audit_log.

> ⚠️ **Partially pre-met (backlog audit 2026-08-13):** `docs/governance/ai_audit_log_retention_policy.md` already defines a 12-month rolling retention period with an automated purge function — satisfying the `claude_audit_log` half of this item's scope verbatim (the item's own example: "12 months rolling"). The Supabase-query-log retention definition and archiving-trigger scope remain open. Recommend Product Owner narrow this item to the Supabase-log sub-scope at next `groom backlog`/`plan release`.

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
**Provisional-Target:** Gate-conditional — first review due 2026-09-24, not yet due

**Gate criteria:** First review due 2026-09-24 (90 days post-v6.2 ship 2026-06-25). Quarterly cadence thereafter.

> **Product Owner note (2026-08-21, post-ship closure `2026-08-17__release-v8.9` STEP 12 review):** This item was flagged by `groom backlog`'s Deferral Age Validation as a stale-target/kill candidate because its `Provisional-Target` field still read the leftover placeholder `v6.3` (long since shipped). That flag was a false positive — the item's own `Gate criteria` field is the actual operative schedule, and 2026-09-24 has not yet arrived. Not neglected, not a kill candidate. `Provisional-Target` corrected above to avoid re-triggering the same false-positive check at the next groom run.

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
**Provisional-Target:** Gate-conditional — schedule within 90 days of v6.2 ship, due 2026-09-24, not yet due

**Gate criteria:** Schedule within 90 days of v6.2 ship (by 2026-09-24).

> **Product Owner note (2026-08-21, post-ship closure `2026-08-17__release-v8.9` STEP 12 review):** This item was flagged by `groom backlog`'s Deferral Age Validation as a stale-target/kill candidate because its `Provisional-Target` field still read the leftover placeholder `v6.3` (long since shipped). That flag was a false positive — the item's own `Gate criteria` field is the actual operative schedule, and 2026-09-24 has not yet arrived. Not neglected, not a kill candidate. `Provisional-Target` corrected above to avoid re-triggering the same false-positive check at the next groom run.

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

> ⚠️ **Partially pre-met (backlog audit 2026-08-13):** `backend/services/health_service.py::get_external_api_health()` already surfaces external dependency status (Alpaca/Yahoo Finance — last successful call, error rate, p95 latency) on `GET /health`, and `src/pages/SystemStatus.js` already renders it (shipped v3.0, ST-08/BLG-OPS-12). The literal AC (`?extended=true` opt-in param, unchanged default response) and Anthropic API coverage remain unbuilt. Recommend Product Owner narrow this item's scope to the residual gap at next `groom backlog`/`plan release`, rather than treating it as a from-scratch build.

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

### BLG-GOV-259 — Quarterly retrospective: estimated vs. actual effort bands (§16.7)
**Priority:** P3 (Low) | **Type:** Governance / FinOps | **Owner:** FinOps & Resource Architect | **Source:** IDEA-finops-20260727-01 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `scored_initiatives.md` Effort Band (§16.7) and `backlog.md` Effort day-ranges (§16.12) are assigned at promotion time but never checked back against actual delivery time — no feedback loop exists to calibrate future estimates.
**Scope:** Add a quarterly (or every-N-cycle) retrospective comparing estimated effort bands to actual sprint-close data.
**Acceptance Criteria:** Retrospective cadence documented; FinOps & Resource Architect sign-off.

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
**Status (2026-08-17__release-v8.9, ST-21/EPIC-06):** Half-achieved — the prompt-wiring action (`roadmap_prompt.md` STEP 8, v9.15→v9.16) is done; the file-creation action remains outstanding, architecturally outside Sprint Execution's write scope. Carried forward via `ESC-EXEC-20260818-02` (`claude/cycles/2026-08-17__release-v8.9/execution_escalations.md`), Open/non-blocking — will close on the next live `run roadmap`/`manage roadmap` invocation per `roadmap_prompt.md` STEP 8's create-if-absent instruction.

---

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

### BLG-QA-147 — Regression suite runtime budget & trend report (last 90 days)
**Priority:** P3 (Low) | **Type:** QA / CI | **Owner:** QA & Testing Owner | **Source:** IDEA-qa-testing-20260809-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** `BLG-QA-134` (v7.9 window) defined a runtime budget but no trend report has been produced yet showing whether the suite is tracking within or drifting beyond it over the last 90 days.
**Scope:** Produce the first 90-day trend report against the `BLG-QA-134` budget.
**Acceptance Criteria:** Trend report produced; QA & Testing Owner sign-off.

---

### BLG-SPEC-131 — trade_plan.md §5.1 form-fields table still lists non-existent "Risk/Reward Notes" field
**Priority:** P3 (Low) | **Type:** Spec Debt | **Owner:** Head of Specs Team | **Source:** ST-27 (BLG-SPEC-129, EPIC-06, `2026-08-14__release-v8.8`), discovered mid-sprint during agent-mediated Head of Specs Team review | **Effort:** XS | **Provisional-Target:** TBD
**Problem:** `docs/specs/frontend/pages/trade_plan.md` §5.1's form-fields table (line ~123) still lists "Risk/Reward Notes | Textarea | No | Free text; used for pre-population of CHK-04" as a live field — but `src/pages/TradePlan.js` has zero `risk_reward_notes` binding (confirmed via grep). ST-27 (this same cycle) fixed the stale Changelog anchor that pointed to this field but deliberately left the table row itself untouched, since the AC's scope was narrowly "correct the anchor," not restructure the table.
**Scope:** Determine what actually happened to this field (renamed? merged into another narrative field? genuinely removed with no replacement?) and either correct the table row to reflect current reality or remove it, updating any other section that still assumes its presence (e.g. §5a.3's pre-population rule, §6.2's CHK-04 rationale note both still reference `risk_reward_notes` by name).
**Acceptance Criteria:** §5.1's field table accurately reflects the live form; any other section referencing `risk_reward_notes` reconciled or explicitly confirmed still accurate; Head of Specs Team sign-off.

---

### BLG-TECH-11 — Scope a future migration off Create React App (react-scripts v5)
**Priority:** P3 (Low) | **Type:** Platform / Technical Debt | **Owner:** Head of Engineering | **Source:** ST-24 (BLG-SEC-18, EPIC-05, `2026-08-14__release-v8.8`) | **Effort:** S (scoping only) | **Provisional-Target:** TBD
**Problem:** The ST-24 npm audit baseline review (`docs/security/npm_audit_baseline_review_2026-08-16.md`) found 14 HIGH/CRITICAL-advisory packages that cannot be fixed without a `react-scripts` major-version bump — all are pinned by CRA v5's own dependency tree (webpack-dev-server, svgo/postcss-loader chain), and Create React App is itself unmaintained upstream with no compatible non-breaking upgrade path. These were accepted as risk (build-toolchain-only exposure, never shipped to the browser — confirmed via repo-wide import grep) with a 6-month review-by date (2027-02-16), but individual accept-risk renewals every cycle only defer the underlying problem; the durable fix is migrating off the toolchain entirely.
**Scope:** Scope (not implement) a migration path off `react-scripts` to an actively-maintained build toolchain (e.g. Vite) — estimate effort, identify breaking-change risk areas (CRA-specific env var handling, `public/` asset conventions, Jest→Vitest if applicable), and produce a migration plan document for a future release to execute against.
**Acceptance Criteria:** Migration scoping document produced (target toolchain recommendation, effort estimate, risk areas identified); Head of Engineering sign-off.
**Reference:** full review at `docs/security/npm_audit_baseline_review_2026-08-16.md` §3.2

---

### BLG-GOV-306 — Strategy rules change-justification template
**Priority:** P3 (Low) | **Type:** Governance / Process | **Owner:** Strategy Rules & System Intent Owner | **Source:** IDEA-strategy-owner-20260809-02 | **Effort:** S | **Provisional-Target:** TBD
**Problem:** When `strategy_rules.md` is version-bumped, there is no required template ensuring the change cites the trade-history evidence (if any) motivating it — SI-04 (Strategy Version Comparison) will eventually need this history to be traceable.
**Scope:** Add a change-justification template section to `strategy_rules.md`'s own change-log convention.
**Acceptance Criteria:** Template added; applied to the next `strategy_rules.md` version bump; Strategy Rules & System Intent Owner sign-off.

---

### BLG-SPEC-132 — Document PositionSizingWidget baseline in trade_plan.md
**Priority:** P3 (Low) | **Type:** Spec Debt | **Owner:** Frontend Specifications & UX Documentation Owner | **Source:** Design gate `2026-08-17__release-v8.9` (ST-04/EPIC-02 review) — filed by PMO Lead per the gate's own follow-up instruction | **Effort:** S (~0.5-1d) | **Provisional-Target:** v8.10
**Problem:** While documenting ST-04's (BLG-BE-104, correlation/sector-concentration-aware sizing) concentration-reason addition to `PositionSizingWidget` (`trade_plan.md` §10.7) during the `2026-08-17__release-v8.9` design gate, it became clear the widget's baseline — fields, debounce behaviour, `POST /portfolio/size` contract — has never had a dedicated frontend spec section of its own, only a passing reference at §10. The design gate's write scope excludes `claude/backlog/backlog.md`, so filing this item was deferred to PMO Lead/Head of Specs Team after `plan sprint` completed (per `design_gate.md`'s own Notes section, `2026-08-17__release-v8.9`).
**Scope:** Add a dedicated `PositionSizingWidget` baseline subsection to `trade_plan.md` covering its fields, debounce parameter, and the `POST /portfolio/size` contract it consumes — as the parent section §10.7's concentration-reason addition now assumes exists.
**Acceptance Criteria:** `trade_plan.md` has a dedicated `PositionSizingWidget` baseline subsection documenting fields, debounce behaviour, and the `POST /portfolio/size` contract; Frontend Specifications & UX Documentation Owner sign-off.

---

### BLG-GOV-310 — "Signed off by: PENDING" placeholder reads as unresolved in at-rest Class 3 docs
**Priority:** P3 (Low) | **Type:** Governance Process | **Owner:** Head of Specs Team | **Source:** PR #1426 dual-role Director of Quality review (EPIC-05, `2026-08-14__release-v8.8`) | **Effort:** XS | **Provisional-Target:** TBD
**Problem:** Some Class 3 docs carry a static `Signed off by: PENDING` field even after the actual sign-off has genuinely happened — the sign-off is recorded only in the separate `qa_evidence_EPIC-xx.md` consolidation log, not propagated back to the doc itself. A reader opening the doc directly (not the qa_evidence log) sees an apparently-unresolved sign-off gate.
**Scope:** Document a convention for these fields — either point back to the qa_evidence log explicitly (e.g. "See qa_evidence_EPIC-xx.md"), or remove the field entirely from docs that don't themselves own a sign-off gate.
**Acceptance Criteria:** Convention documented (in `shared_standards.md` or equivalent canonical location); Head of Specs Team sign-off.

---

### BLG-TECH-12 — Unexplained package-lock.json "dev": true churn from the react-router-dom bump
**Priority:** P3 (Low) | **Type:** Platform / Technical Debt | **Owner:** Head of Engineering | **Source:** PR #1426 dual-role Director of Quality review (ST-24, EPIC-05, `2026-08-14__release-v8.8`) | **Effort:** XS | **Provisional-Target:** TBD
**Problem:** ST-24's `react-router-dom` `^7.13.0`→`^7.18.2` bump produced incidental `"dev": true` flag churn on unrelated `package-lock.json` entries — likely benign npm-version lockfile noise, but not verified or explained at the time.
**Scope:** Confirm whether the churn is genuine npm-version behaviour (no dependency-graph change) or reflects a real, unintended shift in which packages are dev-only.
**Acceptance Criteria:** Root cause confirmed and documented as benign, or a real issue found and fixed.

---

### BLG-FEAT-92 — Screener-to-trade conversion funnel view
**Priority:** P2 (Medium)
**Type:** Product Feature / Analytics
**Owner:** Metrics & Analytics Owner; Product Owner
**Source:** Product Owner feature-vision session — 2026-08-17; related to existing `BLG-FEAT-30` (Screener-to-trade attribution pipeline & retrospective analytics, consolidated) — overlap to be reconciled before scheduling
**Effort:** M (~2d)
**Provisional-Target:** Unscheduled
**Depends on:** BLG-FEAT-30 (shares the same underlying attribution linkage; Product Owner/Head of Specs Team to confirm whether this is a sub-scope of BLG-FEAT-30 or a genuinely separate item before either enters sprint planning)

**Problem**
The full pipeline (screener hit → watchlist → research → trade plan → position → close) exists end-to-end, but there is no aggregate view of where candidates drop off at each stage, or what fraction of screener hits ever convert into a trade — let alone a profitable one. Without this, it isn't possible to tell whether the screener's complexity and cost are earning their keep, and every other planned analytics feature building on screener attribution (`BLG-FEAT-30` and its consolidated items) is downstream of having this instrumentation in place.

**Scope**
- Funnel view: screener hit → watchlist add → trade plan created → position opened → position closed, with count and conversion % at each stage
- Filterable by date range and, where available, setup/signal type
- Product Owner/Head of Specs Team to reconcile scope against `BLG-FEAT-30` before this enters sprint planning — may be absorbed as a sub-scope rather than shipped separately

**Acceptance Criteria**
- Funnel view displays counts and conversion % for all 5 pipeline stages over a selectable date range
- Reconciliation with `BLG-FEAT-30` completed and documented (merged, superseded, or confirmed distinct) before either item is scheduled
- Product Owner sign-off

---

### BLG-BE-105 — Audit and backfill open positions against the breakeven-floor stop invariant

**Priority:** P1 (High)
**Type:** Backend Engineering / Risk Management / Data Integrity
**Owner:** Backend Engineering Patterns Owner
**Source:** PR #1452 review (Director of Quality / Product Owner agent-mediated review, 2026-08-18) — ST-01 (`BLG-BE-102`, EPIC-01, v8.9) acceptance criterion "No open profitable position has `current_stop` below its own `entry_price`" was confirmed *not* verified by that story's delivery. ST-01 confirmed the live calculation path is correct going forward (`calculate_trailing_stop()` applies the breakeven floor), but did not query or backfill the existing open-position dataset, since that AC requires a live-DB check that isn't CI-reproducible.
**Effort:** S (~0.5–1d)
**Provisional-Target:** Unscheduled

**Problem**
`BLG-BE-102`'s root cause (stops not floored at `entry_price` for profitable positions) predates the ST-01 fix confirmation — commit `b410cfa3c` (2026-02-12) already made the *live calculation path* correct, but any position that ratcheted its stop before that commit, or via some other now-closed gap, could still be sitting in the database today with `current_stop < entry_price` while profitable. Nothing in the v8.9 EPIC-01 delivery checked or corrected the existing dataset — the AC was explicitly deferred as a post-merge ops action, not closed.

**Scope**
- Query all open positions where `position_state = 'PROFITABLE'` and `current_stop < entry_price`
- For each match found, apply `calculate_trailing_stop()`'s floor logic (`max(current_stop, new_stop, entry_price)`) via the existing nightly recompute path (`run_nightly_trailing_stop_update()` or `analyze_positions()`), not a bespoke one-off script, so the correction goes through the same code path already regression-tested by `tests/test_trailing_stop_breakeven_floor.py`
- Record the count of positions found/corrected for traceability (deviation log or ops note)

**Acceptance Criteria**
- Live-DB query confirms the count of open profitable positions with `current_stop < entry_price`, before and after correction
- Any positions found are corrected via the existing floored calculation path (no new inline stop-adjustment logic)
- Result recorded (count found, count corrected, date) — closes the deferred ST-01 AC from `BLG-BE-102`
- Backend Engineering Patterns Owner sign-off

---

### BLG-QA-153 — Add Playwright coverage for UK-market position on current_trailing_stop_native

**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** Director of Quality
**Source:** PR #1452 review (Director of Quality agent-mediated review, 2026-08-18) — ST-02 (`BLG-BE-103`, EPIC-01, v8.9) added `current_trailing_stop_native` and verified UK-position parity (`current_trailing_stop == current_trailing_stop_native`) at the backend unit level only (`tests/test_position_currency_basis.py::test_native_and_gbp_fields_equal_for_uk_position`). No e2e/Playwright test exercises a UK-market position through the actual rendered Card/Table UI against the new field.
**Effort:** S (~0.5d)
**Provisional-Target:** Unscheduled

**Problem**
`tests/e2e/position-stop-currency-basis.spec.js` (`V-CURR-01`, `V-CURR-02`) only fixtures a US-market position. The "no UK regression" claim for the new native-currency field is verified structurally (backend dict equality) but not through the UI a UK user would actually see. Risk is low — UK native and GBP values are identical by construction — but the gap means a future UI-layer regression specific to UK rendering (e.g. a stray currency-symbol bug) would not be caught by this EPIC's own test suite.

**Scope**
- Add a UK-market position fixture (native == GBP for all stop fields) to `tests/e2e/position-stop-currency-basis.spec.js` or a sibling spec
- Assert Card and Table views render the same, single stop value with the `£` symbol, consistent with `initial_stop`

**Acceptance Criteria**
- New Playwright test(s) cover a UK-market position's Trail Stop tile/cell rendering
- Test passes against current implementation
- Director of Quality sign-off

---

### BLG-QA-154 — Add Playwright coverage for Arc5ComplianceSection's events_per_week value formatting

**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA Lead
**Source:** ST-20 (BLG-QA-144, EPIC-04) Playwright coverage audit refresh, `docs/qa/arc5_coverage_audit.md` §3.3.1 (GAP-ARC5-06), cycle 2026-08-21__release-v9.0 — 2026-08-21
**Effort:** XS (<1h)
**Provisional-Target:** Unscheduled

**Problem**
`src/components/analytics/Arc5ComplianceSection.js`'s `fmtCount` function (1-decimal-place formatting for `events_per_week`, e.g. `3.0`) has no scenario asserting its rendered value in `tests/e2e/arc5-compliance-section.spec.js` — SC-ARC5-05 (BLG-QA-58, v5.7) only covers the two `fmtRate` fields (`override_rate`, `trade_plan_adherence_rate`), leaving this third, distinct formatter function untested.

**Scope**
- Add a scenario to `tests/e2e/arc5-compliance-section.spec.js` asserting the formatted `events_per_week` value renders correctly from mocked data (e.g. `2.3` → `"2.3"`)

**Acceptance Criteria**
- New Playwright scenario asserts the rendered `events_per_week` text matches the expected `fmtCount` output for a known mock value
- Test passes against current implementation

---

### BLG-QA-155 — Add Playwright coverage for Arc5ComplianceSection's top_rule_breach text formatting

**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA Lead
**Source:** ST-20 (BLG-QA-144, EPIC-04) Playwright coverage audit refresh, `docs/qa/arc5_coverage_audit.md` §3.3.1 (GAP-ARC5-07), cycle 2026-08-21__release-v9.0 — 2026-08-21
**Effort:** XS (<1h)
**Provisional-Target:** Unscheduled

**Problem**
`src/components/analytics/Arc5ComplianceSection.js`'s `fmtText` function (underscore-to-space replacement for `top_rule_breach`, e.g. `cash_constraint` → `cash constraint`) has no scenario coverage at all — a regression to this formatting (or to the raw value passed through unformatted) would not be caught.

**Scope**
- Add a scenario to `tests/e2e/arc5-compliance-section.spec.js` asserting the formatted `top_rule_breach` value renders with spaces, not underscores, for a known mock value

**Acceptance Criteria**
- New Playwright scenario asserts the rendered `top_rule_breach` text matches the expected `fmtText` output (underscores replaced with spaces) for a known mock value
- Test passes against current implementation

---

### BLG-QA-156 — Add Playwright coverage for Arc5ComplianceSection's null-value handling

**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA Lead
**Source:** ST-20 (BLG-QA-144, EPIC-04) Playwright coverage audit refresh, `docs/qa/arc5_coverage_audit.md` §3.3.1 (GAP-ARC5-08), cycle 2026-08-21__release-v9.0 — 2026-08-21
**Effort:** XS (<1h)
**Provisional-Target:** Unscheduled

**Problem**
None of `src/components/analytics/Arc5ComplianceSection.js`'s three formatter functions (`fmtRate`/`fmtCount`/`fmtText`) have a scenario covering the case where an individual metric field is `null` (each renders `"—"` for `null`) — e.g. `top_rule_breach: null` while the other three fields are populated. This is a real, distinct code path (the `val != null` guard in each formatter) that has never been exercised.

**Scope**
- Add a scenario to `tests/e2e/arc5-compliance-section.spec.js` with at least one metric field set to `null` per formatter type, asserting the corresponding card renders `"—"`

**Acceptance Criteria**
- New Playwright scenario asserts `"—"` renders for at least one `null` field covering each of `fmtRate`/`fmtCount`/`fmtText`
- Test passes against current implementation

---

### BLG-SPEC-133 — position_endpoints.md example JSON: current_trailing_stop_native doesn't reconcile with current_trailing_stop × live_fx_rate

**Priority:** P4 (Trivial)
**Type:** Specification / Documentation Accuracy
**Owner:** API Contracts & Documentation Owner
**Source:** PR #1452 review (Director of Quality agent-mediated review, 2026-08-18) — `docs/specs/api_contracts/position_endpoints.md`'s `GET /positions` example response block shows `current_trailing_stop: 560.50`, `live_fx_rate: 1.3650`, and `current_trailing_stop_native: 764.00` in the same object; `560.50 × 1.3650 = 765.08`, not `764.00` (off by ~£1.08 / 0.14%), so the example doesn't reconcile with the documented conversion formula for the two fields.
**Effort:** XS (~15min)
**Provisional-Target:** Unscheduled

**Problem**
Purely an illustrative-example inconsistency (not test-enforced, no functional impact — the live conversion in `backend/services/position_service.py` is correct and covered by `tests/test_position_currency_basis.py`), but a reader manually verifying the field notes against the example would hit an arithmetic mismatch.

**Scope**
- Correct the example JSON's `current_trailing_stop_native` value (or its `current_trailing_stop`/`live_fx_rate` counterparts) so all three reconcile exactly

**Acceptance Criteria**
- Example JSON block in `docs/specs/api_contracts/position_endpoints.md` is internally consistent (`current_trailing_stop × live_fx_rate == current_trailing_stop_native`, within rounding)
- API Contracts & Documentation Owner sign-off (or Head of Specs Team, per standard doc-fix delegation)

---

### BLG-BE-106 — ensure_trade_plans_table() memoization flag has no lock — thread-safety by idempotent-SQL luck, not by construction

**Priority:** P3 (Low)
**Type:** Backend Engineering
**Owner:** Backend Engineering Patterns Owner
**Source:** PR #1454 (EPIC-03) agent-mediated Director of Quality review — 2026-08-19
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
ST-08's `_trade_plans_table_ensured` module-global flag in `backend/database.py` is checked-then-set with no lock. All routes calling `ensure_trade_plans_table()` (`backend/routers/trade_plans.py`, `backend/routers/analytics.py`) are sync `def` handlers, which FastAPI dispatches via a thread pool — so two concurrent requests hitting a cold-start process could both pass the flag check before either sets it, both running the DDL block concurrently. Currently harmless only because every statement in the guarded block is idempotent (`CREATE TABLE IF NOT EXISTS`/`CREATE INDEX IF NOT EXISTS`), so correctness holds today by luck, not by construction — a future edit to that block that isn't naturally idempotent would silently reintroduce a real race.

**Scope**
- Add a `threading.Lock` (or equivalent) around the check-then-set in `ensure_trade_plans_table()`, matching whatever pattern is idiomatic for this codebase's other memoized lazy-init functions if one exists

**Acceptance Criteria**
- The flag check-and-set is guarded by a lock
- A regression test demonstrates two concurrent calls only execute the DDL block once (or confirms serialization)
- No behaviour change to callers

---

### BLG-FEAT-93 — trade_plans.setup_type="Other" default conflates user-chosen-Other with never-classified

**Priority:** P3 (Low)
**Type:** Product Feature
**Owner:** Product Owner
**Source:** PR #1455 (EPIC-04) agent-mediated Product Owner review — 2026-08-19 (reviewer explicitly recommended filing this as a follow-up rather than blocking the PR)
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
ST-13 (BLG-QA-150) fixed `trade_plans.setup_type` having no server-side default by normalizing null/absent/empty to the existing canonical value `"Other"` in `create_plan()`. This closed the immediate data-quality gap but means a trade plan where the user explicitly selected "Other" from the dropdown is now indistinguishable, in the stored data, from one where `setup_type` was never classified at all — permanently degrading the precision of the future `win_rate_by_setup_type` analytics (SI-02) this fix was meant to protect, since both cases collapse into the same bucket. Also noted: the default is applied only on `POST /trade-plans` (create), not on `PUT /trade-plans/{id}` (update) — a plan created before this fix, with `setup_type` still null, is never backfilled or corrected on a later edit.

**Scope**
- Decide and implement a way to distinguish "explicitly Other" from "never classified" (e.g. a `setup_type_source` field, a distinct enum value, or a `null`-preserving default used only in reporting) OR make an explicit, documented decision to accept the conflation with rationale (matching the "accept-as-is with documented rationale" option ST-13's own original AC offered)
- If a fix is chosen, also decide whether to extend the default to `PUT`

**Acceptance Criteria**
- Decision recorded
- If implemented, `win_rate_by_setup_type`'s future query logic (or its predesign doc) is updated to reflect the distinction
- Product Owner sign-off

---

### BLG-OPS-147 — Confirm production PUBLIC_URL is actually set in the Render dashboard (BLG-OPS-146 remainder)

**Priority:** P3 (Low)
**Type:** Operations / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** PR #1456 (EPIC-05) agent-mediated Product Owner review — 2026-08-19; remainder of BLG-OPS-146 (ST-16)
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
ST-16 fixed the local-venv Python-pin documentation and added `PUBLIC_URL=/` to `.env.production`'s repo template for parity with `.env.staging`, but could not confirm whether production's real Render dashboard env vars actually already have `PUBLIC_URL` set — no dashboard access was available in that session. The production site is known to serve correctly today, which is consistent with (but doesn't prove) this already being set. Once BLG-OPS-146 is archived as shipped (since ST-16's achievable scope did ship), this specific unconfirmed sub-item has no other tracking mechanism.

**Scope**
- Someone with Render dashboard access checks the production Static Site's environment variables for `PUBLIC_URL`
- If absent, add it (value `/`, matching staging); if present, just confirm and close

**Acceptance Criteria**
- Production `PUBLIC_URL` dashboard value confirmed one way or the other, documented in this item's resolution

---

### BLG-OPS-148 — Add CI safeguard to catch future PUBLIC_URL/asset-path regressions on GitHub Pages deploy

**Priority:** P2 (Medium)
**Type:** Operations / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** 2026-08-21 GitHub Pages white-page incident, fixed via PR #1461; related: BLG-OPS-146, BLG-OPS-147
**Effort:** S (~0.5d)
**Provisional-Target:** v8.10

**Problem**
On 2026-08-21 the GitHub Pages site went blank because `.env.production`'s `PUBLIC_URL=/` (added in `5f80e301`, `[EPIC-05][ST-16]`, merged to `main` 2026-08-20) was picked up automatically by `deploy.yml`'s `npm run build`, overriding `package.json`'s `homepage`-derived subpath and producing root-relative asset paths that 404 on GitHub Pages (served from `/swing-trading-model`). PR #1461 fixed it by pinning `PUBLIC_URL: /swing-trading-model` as an explicit build-step env var, but that's a point fix — nothing stops a future edit to `.env.production` (or any new CRA-auto-loaded env file) from silently reintroducing root-relative paths, since Render (root-served) and GitHub Pages (subpath-served) share that file with no automated check that the GitHub Pages build output is actually subpath-correct. BLG-OPS-146/147 track confirming `PUBLIC_URL` values are correct per-environment but neither adds a check that would have caught this regression.

**Scope**
- Add a CI step (in `deploy.yml`, after `npm run build`) that fails the job if `build/index.html`'s script/link asset paths don't start with `/swing-trading-model/`
- Document the check's rationale inline (why GitHub Pages needs a subpath and Render doesn't) so a future edit understands the constraint instead of just seeing a red CI check

**Acceptance Criteria**
- `deploy.yml` fails fast if a future build produces root-relative (or otherwise wrong-subpath) asset paths in `build/index.html`
- A deliberate local test (temporarily unsetting the `PUBLIC_URL` override) confirms the new step actually catches the regression
- Infrastructure & Operations Owner sign-off

---

### BLG-TECH-16 — Sector-concentration adjustment's fail-open exception handler logs nothing on failure

**Priority:** P3 (Low)
**Type:** Platform / Technical Debt
**Owner:** Head of Engineering
**Source:** PR #1453 (EPIC-02) agent-mediated Director of Quality review — 2026-08-19
**Effort:** XS (<1h)
**Provisional-Target:** TBD

**Problem**
`backend/services/sizing_service.py`'s `_apply_concentration_adjustment()` wraps its body in `try/except Exception: return default` (fail-open, so a concentration-service error never blocks position sizing) — but the except block has no logging, so if `get_sector_exposure()` or any other call inside starts silently failing in production (e.g. a schema drift, a bad ticker-to-sector mapping), there's no signal anywhere that the concentration feature has gone dark; it just always returns the unadjusted default with no visible symptom.

**Scope**
- Add a log line (matching this codebase's existing fail-open logging convention, e.g. the pattern already used by `_calculate_heat_impact`'s sibling fail-open handler, which does log a warning) inside the except block before returning default

**Acceptance Criteria**
- Exception is logged (level appropriate to a fail-open path, e.g. warning) with enough context to diagnose (ticker/sector where available)
- No change to the fail-open return behaviour itself
- Existing tests still pass

---

### BLG-GOV-311 — Add ST-06 §13 CONDITIONAL clearance to strategy_rules.md §13.5 semi-annual re-attestation roster

**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Strategy Rules & System Intent Owner
**Source:** ST-23/EPIC-02, 2026-08-17__release-v8.9 — 2026-08-18
**Effort:** XS (~15min)
**Provisional-Target:** v8.9 (or next cycle touching `strategy_rules.md` under Strategy Rules & System Intent Owner authority)

**Problem**
`strategy_rules.md` §13.5's Maintenance rule requires: "New features entering the roster do so by adding a row to the table above in the same commit that records their own initial §13 clearance." ST-23 (this cycle) produced `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` (Determination: CONDITIONAL) for ST-06 (Automated AI Post-Trade Debrief, BLG-FEAT-90), but `execution_prompt.md`'s write scope does not permit the Sprint Execution Engine to edit `claude/strategy/strategy_rules.md` — CLAUDE.md §2 restricts governance-file edits to cases "explicitly instructed by the relevant prompt," and `execution_prompt.md` §7 does not list `claude/strategy/` in its write scope. The roster update is therefore deferred to this backlog item rather than performed out-of-scope by this routine.

**Scope**
- Add a row for ST-06 / BLG-FEAT-90 to the §13.5 roster table (`Feature` | `§13 Review Record` | `Cleared` columns), citing `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` and `v8.9` as the Cleared version
- Perform under Strategy Rules & System Intent Owner authority — the same role that signed off the review this row documents
- Follow `strategy_rules.md`'s own governance-file edit checklist (CLAUDE.md §6) if the edit bumps the document's version

**Acceptance Criteria**
- `strategy_rules.md` §13.5's roster table includes a ST-06/BLG-FEAT-90 row pointing at the CONDITIONAL review document
- Edit committed under Strategy Rules & System Intent Owner authority, in a session/prompt whose write scope explicitly covers `claude/strategy/`
- If `strategy_rules.md`'s version is bumped: CLAUDE.md §6 governance file edit checklist steps 1–4 completed in the same commit

---

### BLG-GOV-312 — Recurrence-check false positive: named target file not read directly before concluding "not applied"

**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Post-ship closure `2026-08-17__release-v8.9`, `ESC-CLOSE-20260821-01` resolution — 2026-08-21
**Effort:** S (~0.5 day)
**Provisional-Target:** TBD

**Problem**
`ESC-CLOSE-20260821-01` (a §6.4 2-cycle recurrence escalation for the "CI-green per-fix restatement clarification") turned out to be a false positive: the fix had actually been applied at `2026-08-12__release-v8.7` post-ship closure STEP 8 (`LL-v8.7-P4-01`, `qa_evidence_template.md` v1.10→v1.11), but both `2026-08-14__release-v8.8` and `2026-08-17__release-v8.9`'s Phase 4 recurrence checks (`lessons_learnt_prompt.md §3.7`) reported "no ... language change found in either target file" — searching `execution_prompt.md §5.3` and `prompt_change_log.md` — without ever actually reading `qa_evidence_template.md` itself, the file the original friction item's own Process Patch entry named as the fix target. This is a distinct failure mode from the one `lessons_learnt_prompt.md` v1.10→v1.11's "Patch-ID matching requirement" (`LL-v8.6-P4-01b`) already closed (that one was about searching `prompt_change_log.md` by date/filename instead of patch-ID; this one is about not reading the named target file at all) — the existing fix did not cover this case.

**Scope**
- `lessons_learnt_prompt.md §3.7`: when checking whether a deferred patch was subsequently applied, and the patch's own Process Patch entry names a specific target file (as most `→ Deferred patch` entries do, per §5's record structure), that file must be opened and read directly — not just grepped by an assumed keyword, and not silently substituted for a same-topic sibling file (e.g. `execution_prompt.md` when the named target was `qa_evidence_template.md`) — before concluding "not applied" and letting the recurrence/escalation clock advance.

**Acceptance Criteria**
- `lessons_learnt_prompt.md §3.7` gains an explicit "read the named target file directly" step
- Standard CLAUDE.md §6 governance file edit checklist applied (version bump, `OPERATIONAL_GUIDE.md` §14, `prompt_change_log.md` entry)
- Head of Specs Team sign-off

---

### BLG-GOV-313 — Canonical "Sandbox Access Constraint" disclosure block for shared_standards.md
**Priority:** P3 (Low) | **Type:** Governance Process | **Owner:** Head of Specs Team | **Source:** `2026-08-12__release-v8.7` Phase 4 lessons learnt (friction item 2), carried 2 cycles, escalated as `ESC-CLOSE-20260821-02` — resolved directly 2026-08-21 | **Effort:** S | **Provisional-Target:** ✅ COMPLETE — 2026-08-21 — direct Head of Specs Team action, post-ship closure `2026-08-17__release-v8.9`
**Problem:** Three independent stories at v8.7 (ST-07, ST-13, ST-15) each disclosed the same "no live staging/production access in this sandbox" constraint with slightly different re-derived prose, with no canonical statement to point to instead.
**Scope:** New `shared_standards.md` §16.16 — canonical constraint statement, stable disclosure IDs (`SBX-NO-LIVE-DB`/`SBX-NO-LIVE-STAGING`/`SBX-NO-LIVE-EXTERNAL-API`), usage note.
**Acceptance Criteria:** Section added; `shared_standards.md` version bumped; `OPERATIONAL_GUIDE.md` §14 and `prompt_change_log.md` updated in the same commit.

---

### BLG-GOV-314 — governance_sync.yml's auto-close never fires when a story's completion-state commit is split from its work commit
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Engineering
**Source:** `2026-08-21__release-v9.0` Sprint Execution session — 2026-08-21
**Effort:** S (~0.5-1d)
**Provisional-Target:** Unscheduled

**Problem**
`execution_prompt.md`'s own guidance (adopted mid-session this cycle as a self-identified process improvement, after an earlier mistake of setting `commit_sha: null`/omitted before the real SHA was known) is: commit the actual work → push → `git rev-parse HEAD` → *then* update `execution_state.json`'s status/commit_sha in a separate follow-up commit. This is procedurally sound for capturing the real commit SHA, but it silently defeats `governance_sync.yml`'s auto-close mechanism for every story handled this way — in **both** directions, confirmed at `2026-08-21__release-v9.0`:

- **Under-closing (16 confirmed cases, ST-08 through ST-27 across EPIC-02–05):** the work commit (tagged `[EPIC-xx][ST-xx]`) triggers the workflow, which correctly finds the `[ST-xx]` tag but checks `execution_state.json`'s status *as of that commit* — still not `done` (the follow-up commit hasn't landed yet) — so it correctly skips closing per its anti-premature-closure guard (`BLG-GOV-285`). The follow-up commit that actually sets `status: done` is conventionally tagged `[GOVERNANCE] Record ST-xx completion...` — a bare `[GOVERNANCE]` tag with no `[ST-xx]` in it — so the workflow's `grep -oE '\[(ST-[0-9]+)\]'` parse finds nothing and the close-issue step never even runs. Net effect: the story is genuinely `done`, correctly verified — but its issue never auto-closes (issues #1469-1488 range; manually closed same-session with an audit-trail comment once discovered).
- **Over-closing (1 confirmed case, ST-02/#1463, more serious — misrepresents an *incomplete* story as done):** when the work commit is pushed on its own *before* any `execution_state.json` entry exists for that story yet (e.g. the very first story of a fresh EPIC branch, pushed before the tracking-commit that follows it), the workflow's `is_story_done()` jq lookup finds no status at all and falls back to its documented `"unknown" = close unconditionally` behaviour (preserved for pre-per-EPIC-mechanism cycles). If that story's real eventual disposition is `blocked_backend`/`blocked_decision` rather than `done` — set 2 minutes later in the follow-up commit — the issue is now wrongly closed for a story that isn't actually finished, and nothing subsequently reopens it. Manually reopened same-session (`#1463`, ST-02) once discovered, with the real outstanding ACs and delegation record noted in the reopen comment.

**Scope**
- Either (a) change the follow-up commit-message convention to include the `[ST-xx]` tag alongside `[GOVERNANCE]` (e.g. `[GOVERNANCE][ST-xx] Record ST-xx completion...`) so the existing parser catches it on the completion commit too, or (b) change `governance_sync.yml`'s status-check logic to look at the *current* `execution_state.json` on the branch tip at workflow-run time rather than only the commit range's own diff, so a later completion-commit still triggers correctly for an earlier work-commit's `[ST-xx]` tag
- Separately, reconsider the `"unknown" = close unconditionally` fallback: it was added to preserve pre-per-EPIC-mechanism behaviour, but on the mechanism this cycle actually uses, "unknown" more often means "the tracking commit for this story hasn't landed yet" than "this is a non-sprint-execution reference" — closing in that case is a false positive with real-world consequence (an actually-blocked story reads as done). Consider flipping the default to "skip" (matching the `"no"` branch) unless a story is unambiguously not part of any tracked cycle at all.
- Whichever fix(es) are chosen, add a regression test/dry-run confirming both failure modes are closed: a split work-commit + governance-commit pair correctly auto-closes an eventually-`done` story, and does *not* auto-close a story that ends up `blocked_*`

**Acceptance Criteria**
- A story completed via the commit→push→get-SHA→separate-governance-commit pattern has its GitHub issue auto-closed by `governance_sync.yml` without manual intervention
- A story that ends up `blocked_backend`/`blocked_decision` (rather than `done`) after its work commit is pushed does NOT have its issue auto-closed, even if no `execution_state.json` entry exists yet at the moment the work commit's own push triggers the workflow
- Existing anti-premature-closure protection (`BLG-GOV-285` — a delegation-record-only commit must not close the issue) remains intact

---

### BLG-TECH-13 — Consolidate 4 independent sector-lookup implementations

**Priority:** P3 (Low)
**Type:** Platform / Technical Debt
**Owner:** Backend Engineering Patterns Owner
**Source:** ST-04/EPIC-02, 2026-08-17__release-v8.9 — 2026-08-18
**Effort:** S (~0.5d)
**Provisional-Target:** Unscheduled

**Problem**
The codebase now carries four independent implementations of "look up a ticker's sector, DB-first, falling back to open positions": `routers/pre_entry_validation.py::_get_ticker_sector`, `services/compliance_recheck_service.py::_get_ticker_sector`, `routers/portfolio_risk.py::_lookup_sector`/`_get_ticker_sector_map`, and the new `services/concentration_service.py::get_ticker_sector` added by ST-04 (BLG-BE-104). ST-04 deliberately did not refactor the first three — they are working, independently tested code (`test_pre_entry_validation.py`, `test_compliance_recheck.py`, `test_portfolio_risk_sector.py`) outside ST-04's scope, and touching them risked regressions unrelated to this story's own acceptance criteria. This mirrors the precedent of `check_market_regime()`'s two divergent implementations (BLG-BE-? consolidated as its own story rather than folded into the story that found it).

**Scope**
- Consolidate all sector-lookup logic into one shared function (candidate home: `services/concentration_service.py::get_ticker_sector`, already DB-first/no-live-call)
- Update `pre_entry_validation.py`, `compliance_recheck_service.py`, and `portfolio_risk.py` to import and use the shared function
- Preserve existing test-patch targets where possible (e.g. `patch("routers.pre_entry_validation._get_ticker_sector", ...)` continues to work if the name is imported into that module's namespace rather than removed outright), or update the affected tests in the same commit if patch targets must change

**Acceptance Criteria**
- Exactly one sector-lookup implementation exists in the codebase; the other three call sites delegate to it
- All 4 existing test suites (`test_pre_entry_validation.py`, `test_compliance_recheck.py`, `test_portfolio_risk_sector.py`, `test_sizing_concentration.py`) pass unchanged in behaviour (same assertions, potentially updated patch targets)
- Backend Engineering Patterns Owner sign-off

---

### BLG-TECH-14 — Consolidate PositionSizingWidget.js / WhatIfSizingPreview.js debounced-fetch boilerplate

**Priority:** P3 (Low)
**Type:** Platform / Technical Debt
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** ST-05/EPIC-02 Head of Engineering sign-off review, 2026-08-17__release-v8.9 — 2026-08-18
**Effort:** S (~0.5d)
**Provisional-Target:** Unscheduled

**Problem**
`PositionSizingWidget.js` (§10.7) and `WhatIfSizingPreview.js` (§5d, added ST-05/BLG-FEAT-91) share only the two `AMBER_MESSAGES`/`SYSTEM_MESSAGES` constant objects (exported from `PositionSizingWidget.js` for reuse). The debounce/sessionStorage/fetch-effect boilerplate — ~30-40 lines each — is duplicated near-verbatim between the two components. Consistent with this codebase's already-acknowledged pattern of deferring widget-consolidation debt (§10.7's own baseline-documentation gap, BLG-SPEC-132), but worth tracking rather than left silently duplicated a second time.

**Scope**
- Extract a shared `useDebouncedSizing` hook (or equivalent) covering: debounced 300ms fetch to `POST /portfolio/size`, loading state, sessionStorage-backed risk-percent state (parameterised by storage key, since the two components deliberately use distinct keys)
- Both components consume the shared hook, each keeping their own presentation/layout

**Acceptance Criteria**
- `PositionSizingWidget.js` and `WhatIfSizingPreview.js` share the debounce/fetch/session-storage logic via one hook
- Existing Playwright coverage for both components (`position-sizing-concentration.spec.js`, `what-if-sizing-preview.spec.js`, `smoke-critical-paths.spec.js`) passes unchanged
- Frontend Specifications & UX Documentation Owner sign-off

---

### BLG-FE-164 — What-If Sizing Preview never sends an fx_rate override — AC-02 reproducibility claim doesn't fully hold for US-market plans

**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** ST-05/EPIC-02 Head of Engineering sign-off review, 2026-08-17__release-v8.9 — 2026-08-18
**Effort:** S (~0.5d)
**Provisional-Target:** Unscheduled

**Problem**
`trade_plan.md` §5d.3 claims the What-If Sizing Preview panel "reproduces an identical suggested size" to what `TradeEntry.js` computes at order time, because both call `POST /portfolio/size`. This holds for UK-market plans, but not reliably for US-market plans: the Trade Plan form has no `fx_rate` field (confirmed against §5.1 and the ux_spec's own payload, which omits `fx_rate`), so the What-If panel always prices against the *live* FX rate, while `TradeEntry.js`'s `PositionSizingWidget` uses a manually-entered field defaulting to a static `1.27`. If the live rate has moved since the plan was drafted, the two suggested sizes can diverge. This does not violate the formally-stated AC-02 ("no DB write occurs from interacting with the preview alone" holds regardless), and is rooted in the design spec's own payload/reasoning rather than an implementation deviation — but the §5d.3 "reproduces an identical suggested size" claim is stronger than the implementation actually guarantees for US-market plans.

**Scope**
- Either (a) add an optional FX-rate override field to the What-If panel (or the Trade Plan form generally) mirroring `TradeEntry.js`'s field, or (b) soften §5d.3's wording to note the live-rate caveat for US-market plans explicitly

**Acceptance Criteria**
- `trade_plan.md` §5d.3's reproducibility claim is either made accurate (FX override added) or explicitly scoped to note the US-market live-rate caveat
- Frontend Specifications & UX Documentation Owner sign-off

---

### BLG-FE-165 — DashboardHome "AI Advisory" badge fails colour-contrast

**Priority:** P3 (Low)
**Type:** Frontend / UX / Accessibility
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** ST-21 (BLG-QA-83, EPIC-04) axe-core accessibility scan, cycle 2026-08-21__release-v9.0 — 2026-08-21
**Effort:** XS (<1h)
**Provisional-Target:** Unscheduled

**Problem**
The new standalone axe-core CI scan (`tests/e2e/accessibility-axe-scan.spec.js`, ST-21) found a `serious`-impact `color-contrast` violation on DashboardHome: the amber "AI Advisory" badge (`.bg-amber-600` background, white text) does not meet the minimum WCAG contrast ratio. Currently grandfathered in the scan's `KNOWN_VIOLATIONS` baseline (pre-existing, not a regression introduced by ST-21) so the new CI gate does not fail on introduction — should be removed from that baseline once fixed.

**Scope**
- Darken the amber background, lighten the badge text, or otherwise adjust the colour pairing to meet WCAG AA contrast (4.5:1 for normal text)

**Acceptance Criteria**
- axe-core no longer reports a `color-contrast` violation for this badge
- `KNOWN_VIOLATIONS["DashboardHome"]`'s `color-contrast` entry removed in `tests/e2e/accessibility-axe-scan.spec.js`

---

### BLG-FE-166 — TradePlan select elements lack accessible names

**Priority:** P3 (Low)
**Type:** Frontend / UX / Accessibility
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** ST-21 (BLG-QA-83, EPIC-04) axe-core accessibility scan, cycle 2026-08-21__release-v9.0 — 2026-08-21
**Effort:** S (~0.5d)
**Provisional-Target:** Unscheduled

**Problem**
The new standalone axe-core CI scan found a `critical`-impact `select-name` violation on the TradePlan form: 3 `<select>` elements have no accessible name (no associated `<label>`, `aria-label`, or `aria-labelledby`) — a real barrier for screen-reader users completing the form. Currently grandfathered in the scan's `KNOWN_VIOLATIONS` baseline.

**Scope**
- Add a proper `<label>` (or `aria-label`) association to each of the 3 affected `<select>` elements

**Acceptance Criteria**
- axe-core no longer reports a `select-name` violation on TradePlan
- `KNOWN_VIOLATIONS["TradePlan"]`'s `select-name` entry removed in `tests/e2e/accessibility-axe-scan.spec.js`

---

### BLG-FE-167 — Settings page combobox buttons lack discernible text

**Priority:** P3 (Low)
**Type:** Frontend / UX / Accessibility
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** ST-21 (BLG-QA-83, EPIC-04) axe-core accessibility scan, cycle 2026-08-21__release-v9.0 — 2026-08-21
**Effort:** S (~0.5d)
**Provisional-Target:** Unscheduled

**Problem**
The new standalone axe-core CI scan found a `critical`-impact `button-name` violation on the Settings page: 2 buttons with `role="combobox"` (Radix UI Select trigger) have no discernible text for assistive technology. Currently grandfathered in the scan's `KNOWN_VIOLATIONS` baseline.

**Scope**
- Add `aria-label` (or visible, associated text) to the affected Radix Select trigger buttons

**Acceptance Criteria**
- axe-core no longer reports a `button-name` violation on Settings
- `KNOWN_VIOLATIONS["Settings"]`'s `button-name` entry removed in `tests/e2e/accessibility-axe-scan.spec.js`

---

### BLG-FE-168 — Settings page form inputs lack labels

**Priority:** P3 (Low)
**Type:** Frontend / UX / Accessibility
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** ST-21 (BLG-QA-83, EPIC-04) axe-core accessibility scan, cycle 2026-08-21__release-v9.0 — 2026-08-21
**Effort:** S (~0.5d)
**Provisional-Target:** Unscheduled

**Problem**
The new standalone axe-core CI scan found a `critical`-impact `label` violation on the Settings page: 12 numeric strategy-parameter input fields have no associated `<label>` element — a real barrier for screen-reader users. Currently grandfathered in the scan's `KNOWN_VIOLATIONS` baseline. This is also the largest single node count of any finding from the initial scan, worth prioritising above the other three accessibility items filed alongside it despite the shared P3 rating.

**Scope**
- Add a proper `<label>` (or `aria-label`) association to each of the 12 affected inputs

**Acceptance Criteria**
- axe-core no longer reports a `label` violation on Settings
- `KNOWN_VIOLATIONS["Settings"]`'s `label` entry removed in `tests/e2e/accessibility-axe-scan.spec.js`

---

### BLG-FE-169 — Settings page subtitle text fails colour-contrast

**Priority:** P3 (Low)
**Type:** Frontend / UX / Accessibility
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** ST-21 (BLG-QA-83, EPIC-04) axe-core accessibility scan, cycle 2026-08-21__release-v9.0 — 2026-08-21
**Effort:** XS (<1h)
**Provisional-Target:** Unscheduled

**Problem**
The new standalone axe-core CI scan found a `serious`-impact `color-contrast` violation on the Settings page: the page subtitle ("Configure your strategy parameters and preferences", `.mt-1` / `text-slate-600 dark:text-slate-400`) does not meet the minimum WCAG contrast ratio against its background. Currently grandfathered in the scan's `KNOWN_VIOLATIONS` baseline. **Note:** this finding was observed once during initial exploration but did not reproduce across repeated re-runs of the same spec afterward — possibly a near-threshold or rendering-timing-dependent result. Worth a manual contrast-checker verification before spending implementation effort, since it may already be borderline-passing.

**Scope**
- Adjust the subtitle's text colour (or background) to meet WCAG AA contrast (4.5:1 for normal text) — likely affects other pages sharing the same `text-slate-600 dark:text-slate-400` subtitle convention; worth a quick grep-and-check across pages while fixing this one, though only Settings was in this scan's scope

**Acceptance Criteria**
- axe-core no longer reports a `color-contrast` violation for the Settings subtitle
- `KNOWN_VIOLATIONS["Settings"]`'s `color-contrast` entry removed in `tests/e2e/accessibility-axe-scan.spec.js`

---

### BLG-TECH-15 — backtest_rule_service.py's ported algorithm functions can silently drift from production_strategy.py

**Priority:** P2 (Medium)
**Type:** Platform / Technical Debt
**Owner:** Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner
**Source:** ST-07/EPIC-02, 2026-08-17__release-v8.9 — 2026-08-18
**Effort:** M (~1-2d)
**Provisional-Target:** Unscheduled

**Problem**
ST-07 (BLG-FEAT-89, In-app backtesting engine) added `backend/services/backtest_rule_service.py`, which ports (copies, does not import) `production_strategy.py`'s `compute_signals`/`compute_atr`/`compute_risk_on`/`transaction_fee`/`backtest` functions. This was a deliberate choice, not an oversight: `production_strategy.py` is a standalone script (never used as a library, has import-time side effects) whose `backtest()` reads regime state from module-level globals (`spy_risk_on`/`ftse_risk_on`) — unsafe to import and mutate from a concurrent web-server process, where two simultaneous requests would race on the same globals. The port is behaviourally identical except regime state is threaded through as an explicit parameter instead of module globals. However, this means the two copies of the core momentum-strategy algorithm can now silently drift apart if `production_strategy.py`'s logic changes (e.g. a future tuning of the stop-loss/rebalance/sizing logic) without the port being updated to match — financially significant, since both feed comparative decision-support output.

**Scope**
- Extract the pure, parameter-only algorithm logic (`compute_signals`, `compute_atr`, `compute_risk_on`, `transaction_fee`, and a globals-free `backtest`) into a genuinely shared module both `production_strategy.py` and `backend/services/backtest_rule_service.py` import — e.g. a new root-level `strategy_engine/` package, or `backend/services/` if `production_strategy.py` can safely import from `backend/`
- `production_strategy.py`'s own `is_risk_on`/module-global usage would need updating to call the shared `backtest()` with explicit regime parameters, matching the port's existing signature
- Add a CI check (or a simple hash/diff comparison) that fails if the two implementations diverge, until the consolidation above ships

**Acceptance Criteria**
- Exactly one implementation of `compute_signals`/`compute_atr`/`compute_risk_on`/`transaction_fee`/`backtest` exists; both `production_strategy.py` and `backend/services/backtest_rule_service.py` use it
- Nightly backtest (`.github/workflows/backtest.yml`) and the in-app Backtest Rule Change endpoint both continue to produce the same historical results as before the consolidation (regression-verified against a fixed historical run)
- Backend Engineering Patterns Owner and Strategy Rules & System Intent Owner sign-off

---

### BLG-BE-107 — Configure root/app logging so logger.info() calls in application code actually reach Render's captured logs
**Priority:** P2 (Medium)
**Type:** Backend Engineering
**Owner:** Backend Engineering Patterns Owner
**Source:** ST-09 (EPIC-03, v8.9, BLG-BE-99) evidence-gathering session — 2026-08-20
**Effort:** S (~0.5d)
**Provisional-Target:** ✅ COMPLETE — 2026-09-03 — ST-02/EPIC-01, cycle `2026-08-21__release-v9.0`

**Problem**
Production runs `uvicorn main:app --host 0.0.0.0 --port $PORT` (per `render.yaml`'s `startCommand`) with no `--log-config`/`--log-level` flag, and `backend/main.py` never calls `logging.basicConfig()` or otherwise configures the root logger (confirmed via repo-wide grep — no `basicConfig`/`addHandler`/`dictConfig` anywhere in `backend/`). Uvicorn's own default logging setup only wires up its own named loggers (`uvicorn`, `uvicorn.error`, `uvicorn.access`) — it never touches the root logger or any `logging.getLogger(__name__)` logger used throughout the app's service modules. With the root logger left at its default level (WARNING) and no handler attached, every `logger.info(...)` call anywhere in application code is filtered out before it ever reaches a handler, and is silently dropped rather than erroring or warning anyone. This was empirically confirmed: a real, successful `POST /digest/si05/send` invocation on 2026-08-20 (Render deploy log, `07:11:51Z`, 200 OK) produced no corresponding `"SI-05 digest sent (%d chars) in %.2fs"` line anywhere in the surrounding log window, even though that `logger.info()` call sits directly in the code path that ran.

**Scope**
- Add a root logging configuration (e.g. `logging.basicConfig(level=logging.INFO)` early in `backend/main.py`, or an explicit `--log-config` passed to uvicorn) so that INFO-level (and above) records from application-module loggers propagate to a handler that writes to stdout/stderr, where Render's log pipeline captures them
- Confirm the fix doesn't create duplicate/conflicting handlers with uvicorn's own access/error logging
- Verify via one real invocation post-deploy that `services/si05_digest_service.py`'s `"SI-05 digest sent..."` line (and ideally at least one other existing `logger.info()` call elsewhere in the app) now actually appears in Render's captured logs

**Acceptance Criteria**
- Root logging is configured such that `logger.info()` calls from any `backend/` module reach stdout/stderr in the running process
- A real post-deploy production invocation confirms at least the `si05_digest_service.py` duration line is now captured in Render logs (this also closes the outstanding evidence gap referenced by `ST-09`/`BLG-BE-99`'s original AC)
- No regression to uvicorn's own existing access/error log formatting or duplicate log lines
- `docs/ops/api_performance_baseline.md` §36 updated with the real log-derived timing once available, superseding the interim GitHub-Actions-proxy measurements recorded there (§36.3 and §36.5)

**Returned to backlog (2026-08-21, cycle `2026-08-21__release-v9.0`, ST-02/EPIC-01):** Same structural blocker recurred — the code fix (`backend/main.py`'s `logging.basicConfig()`) is complete and merge-ready, but the remaining ACs (real post-deploy log confirmation, baseline doc update) require the fix to already be live in production, not obtainable pre-merge; see `execution_state.json` ST-02 and delegation record `DEL-20260821-01` for this cycle's disposition.

**Resolved (2026-09-03, cycle `2026-08-21__release-v9.0`, ST-02/EPIC-01):** PR #1492 merged and deployed to production; a real post-deploy invocation confirmed the digest-timing line now reaches Render's captured logs (`"SI-05 digest sent (498 chars) in 0.37s"`, confirmed directly in the Render dashboard log viewer). All ACs met — see `docs/ops/api_performance_baseline.md` §36.7, `execution_state.json` ST-02 (`done`), and delegation record `DEL-20260821-01`'s final resolution addendum.

---

### BLG-TECH-17 — Debrief-generation prompt encourages cross-trade pattern language with no data to back it
**Priority:** P3 (Low)
**Type:** Backend Engineering / AI Governance
**Owner:** Backend Engineering Patterns Owner; AI Compliance & Governance Officer
**Source:** Agent-mediated Director of Quality review, PR #1460 (ST-06, EPIC-02, v8.9) — 2026-08-20
**Effort:** S (~0.5–1d)
**Provisional-Target:** v9.0

**Problem**
`backend/services/debrief_service.py`'s `_FOCUS_AREA_SYSTEM` prompt instructs the model toward pattern-surfacing phrasing like "this is the Nth trade where X occurred," but no cross-trade frequency/count data is ever computed or passed into `source_values` for `numeric_cross_check()` to verify such a number against. Any count the model states will either fail the §13 review's Condition 9 numeric cross-check and trigger the no-focus-area fallback (a frequent, silent loss of the feature's main value), or — worse — coincidentally match one of the trade's own unrelated numeric fields (entry price, P&L, etc.) by chance and pass despite being an ungrounded guess. Found during PR #1460's agent-mediated Director of Quality review.

**Scope**
- Decide one of two directions: (a) remove the cross-trade pattern-language framing from `_FOCUS_AREA_SYSTEM` until real aggregates exist, or (b) compute a small set of genuine historical counts (e.g. `trades_this_setup_type_count`, `consecutive_early_exit_count`) in `debrief_service.py` and add them to `source_values` so such claims become genuinely verifiable
- If (b): add the new counts to the prompt's user template and to `numeric_cross_check`'s allowed-number set
- Add a test case covering a model-generated cross-trade count claim against the chosen fix

**Acceptance Criteria**
- The prompt's encouraged phrasing style matches what the numeric cross-check can actually verify — no encouraged claim type is systematically un-verifiable
- `tests/test_debrief_service.py` covers the chosen fix (either an added-source-value verification case, or a removed-phrasing regression test)
- Backend Engineering Patterns Owner sign-off

---

### BLG-BE-108 — Decide "linked journal entries" data source for the AI Post-Trade Debrief (red_flag_events vs. trade_history entry/exit notes)
**Priority:** P2 (Medium)
**Type:** Backend Engineering
**Owner:** Product Owner; Backend Engineering Patterns Owner
**Source:** Agent-mediated Product Owner review, PR #1460 (ST-06, EPIC-02, v8.9) — 2026-08-20
**Effort:** S (~0.5d, once decided)
**Provisional-Target:** v9.0

**Problem**
ST-06's acceptance criterion "Debrief references plan-vs-reality data and any linked journal entries where present" was implemented (`backend/services/debrief_service.py::_journal_context_for_trade`) by sourcing "journal entries" from `red_flag_events` — the separate, system-generated Red Flag Journal feature — rather than `trade_history.entry_note`/`exit_note`, the fields this same codebase already labels "Trade Journal" one section above the new Debrief panel in the identical Trade History expandable row (`TradeHistoryTable.js`). This is a plausible but debatable reading of the AC, flagged by an agent-mediated Product Owner review as needing an explicit decision rather than an implicit one.

**Scope**
- Product Owner decides: should the debrief prompt draw on `entry_note`/`exit_note` instead of (or in addition to) `red_flag_events`?
- If entry/exit notes are added: extend `_journal_context_for_trade` (or a renamed equivalent) to include them in the prompt context, subject to the same §13 Condition 2 sourcing discipline already applied to numeric values (free-text notes aren't numbers, so this only affects prompt context, not `numeric_cross_check`)
- Update `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` or `trade_endpoints.md` with the confirmed interpretation, if it changes behaviour

**Acceptance Criteria**
- Product Owner decision recorded (keep `red_flag_events`-only, add entry/exit notes, or both)
- If implementation changes: `tests/test_debrief_service.py` covers the new data source; full backend suite re-verified passing
- Spec updated to reflect the confirmed interpretation of "linked journal entries"

---

### BLG-BE-109 — Nightly backtest rebalance-date computation treats the current in-progress month's latest bar as month-end
**Priority:** P1 (High)
**Type:** Backend Engineering
**Owner:** Backend Engineering Patterns Owner
**Source:** User review session — 2026-08-21 (found while investigating unexpected INTC/WDC trade behaviour in the nightly backtest output)
**Effort:** S (~0.5–1d)
**Provisional-Target:** v9.0

**Problem**
`production_strategy.py` and its in-app port `backend/services/backtest_rule_service.py` both compute monthly rotation checkpoints as `prices.groupby(prices.index.to_period(period_freq)).tail(1).index`. This is correct for every completed past month, but for the current, still-in-progress month it silently resolves to "whichever trading day happens to be the most recent row currently in the data" — not the genuine last trading day of the month. Verified with a direct pandas repro: a business-day index for 2026-08-01 → 2026-08-20 (August not yet complete) returns `2026-08-20` as the sole rebalance date. Because `.github/workflows/backtest.yml` reruns `production_strategy.py` from scratch every night (`0 1 * * *`) and `import_backtest.py` does a full DELETE+INSERT of results, this means the monthly "No longer qualifies" rotation-exit logic fires on the latest bar **every single night** throughout the current month, not once at true month-end — generating spurious rotation-exit trades (wrong `exit_reason`, wrong `holding_days`) and same-day rebuys via the unconditional daily slot-fill-in for any ticker still in the qualifying set. Observed live: INTC exited "No longer qualifies" and WDC exited-then-rebought in the same nightly run on 2026-08-20, three weeks before August's real last trading day (2026-08-31).
**Impact:** Corrupts the nightly backtest trade history every night mid-month until the real month-end arrives and the group tail catches up. Not caught by `import_backtest.py`'s existing `BACKTEST_DRIFT_ALERT` check, which only detects P&L drift with zero new closed trades — a different anomaly class from this (which produces genuine, but wrongly-dated, new trades).

**Scope**
- Fix `rebalance_dates` in both `production_strategy.py` and `backend/services/backtest_rule_service.py` to exclude the in-progress month — e.g. drop the final group if its period equals the current calendar period, or only take `tail(1)` of month-groups whose max date is before today
- Add a regression test with a mid-month date index confirming no rebalance date is returned for the current, incomplete month
- Note in the story whether nightly-imported trade history already corrupted by this bug (any `exit_reason = "No longer qualifies"` trade dated before a true month-end) needs a one-off cleanup on next import, given the full DELETE+INSERT self-heals it automatically at the next true month-end

**Acceptance Criteria**
- `rebalance_dates` never includes a date from the current, incomplete calendar month in either file
- Regression test added and passing for the mid-month case
- `tests/backtest_data_integrity_smoke_test.py`-class checks re-verified passing (no new invariant broken)
- Backend Engineering Patterns Owner sign-off

---

### BLG-BE-110 — Move raw SQL execution out of backend/routers/analytics.py and digest.py into the service/database layers
**Priority:** P3 (Low)
**Type:** Backend Engineering
**Owner:** Backend Engineering Patterns Owner
**Source:** ST-23 (BLG-BE-56, EPIC-05, v9.0) backend service-layer boundary review — 2026-08-21
**Effort:** L (~3-5 days)
**Provisional-Target:** Unscheduled

**Problem**
ST-23's layering-boundary review (per `claude/agents/backend_engineering_patterns_owner.md`'s router→service→database pattern, "Routers must be thin. No business logic, no SQL, no calculations in a router") found that `backend/routers/analytics.py` contains ~25 direct `cursor.execute()` calls (including several f-string-interpolated queries) and `backend/routers/digest.py` contains 7, both bypassing the service/database layers entirely — SQL is built and executed directly inside router handler functions. `backend/routers/ai.py` had the same pattern (2 call sites) and was fixed directly within ST-23's own scope (moved to `database.fetch_journal_notes()`) since it was small and bounded; `analytics.py` and `digest.py` are too large (32 combined call sites across ~1200+ lines) to safely refactor within a single S-effort review story without disproportionate regression risk to production analytics/digest code paths.

**Scope**
- Extract each `cursor.execute()` call in `analytics.py` and `digest.py` into an appropriately-named function in `backend/database.py` (SQL only, no business logic, matching the existing `get_trade_history()`-style convention)
- Update each router handler to call the new database-layer function instead of building/executing SQL directly
- Preserve exact query behaviour (parameterization, filters, joins) — this is a structural move, not a query rewrite
- Full backend test suite must pass with zero behavioural change

**Acceptance Criteria**
- Zero `cursor.execute()`/`conn.execute()` calls remain in `backend/routers/analytics.py` and `backend/routers/digest.py`
- All existing tests for these routers' endpoints continue to pass unchanged
- No new raw SQL introduced in the service layer either — `database.py` remains the sole SQL layer per the established pattern

---

### BLG-TECH-18 — npm dependency tree produces a reproducible production-build regression after a routine `npm update`
**Priority:** P2 (Medium)
**Type:** Platform / Technical Debt
**Owner:** Head of Engineering
**Source:** ST-27 (BLG-OPS-98, EPIC-05, v9.0) quarterly dependency upgrade cadence policy, first pass — 2026-08-21
**Effort:** M (~1-2 days)
**Provisional-Target:** Unscheduled

**Problem**
Running `npm update` (bumping ~20 packages, all within their existing `package.json` semver ranges — nothing outside declared compatibility bounds) produces a reproducible `CI=false npm run build` failure: `[eslint] Failed to load config "react-app" to extend from`. `eslint-config-react-app@7.0.1` (a transitive dependency of `react-scripts`) is present in `npm ls`'s reported tree but is not actually installed under `node_modules/eslint-config-react-app` after the update — confirmed reproducible across 3 independent installs (`npm install` after `npm update`, and two full `rm -rf node_modules && npm install` clean reinstalls from the bumped `package-lock.json`). A related but distinct issue also surfaced during the same investigation: bumping `recharts` specifically (3.7.0 → 3.10.1, also within its declared range) introduces a new `react-is` peer-dependency requirement that isn't satisfied by anything already in the tree (`Module not found: Can't resolve 'react-is'`) — adding `react-is@19.2.8` as an explicit direct dependency fixed that half, but did not fix the `eslint-config-react-app` resolution failure. The dual-eslint-version tree (this repo runs ESLint 9 flat config at the top level; `react-scripts` internally still requires ESLint 8.x, per `playwright.config.js`'s own documented `DISABLE_ESLINT_PLUGIN` workaround for a related but distinct symptom) is the likely root cause area, but was not conclusively isolated within ST-27's own effort budget — the clean, pre-bump `package-lock.json` builds successfully with the same dual-eslint-version structure present, so the trigger is something in the specific version deltas, not the mere existence of two eslint majors in the tree.

**Scope**
- Bisect which specific package version bump(s) among the ~20 in the `npm update` batch actually break `eslint-config-react-app`'s installation/hoisting (candidates: `eslint` 9.39.4→9.39.5, `eslint-plugin-playwright` 2.10.4→2.11.0, or an indirect effect from another bump reshuffling the dependency tree's hoisting decisions)
- Once isolated, either fix forward (e.g. an explicit `overrides`/`resolutions` entry pinning the conflicting sub-dependency) or file the specific incompatibility upstream if it's a genuine bug in one of the packages
- Re-attempt the full `npm update` batch (see `docs/ops/quarterly_dependency_upgrade_cadence_policy.md` §3.1 for the exact list) once the root cause is fixed, verifying `CI=false npm run build` succeeds
- Also apply the already-diagnosed `react-is` fix (add `react-is@19.2.8` as an explicit dependency) as part of this same story, since it's a confirmed, isolated, real fix for the `recharts` half of this investigation

**Acceptance Criteria**
- `npm update`'s full candidate list from `quarterly_dependency_upgrade_cadence_policy.md` §3.1 applied and `CI=false npm run build` succeeds
- Root cause of the `eslint-config-react-app` resolution failure documented (not just worked around)
- Full Playwright E2E suite re-verified passing against the updated dependency tree

---
