**Owner:** Product Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-18
**Cycle:** 2026-03-18__item-4.3

---

# Cycle Record — Roadmap Rebalance

**Completion event:** 4.3 Signal Exposure Enhancement — shipped v2.0 (2026-03-17)
**Run date:** 2026-03-18
**Tier:** Standard

---

## STEP 2 — Re-Validation

### Active Initiatives Reviewed

*Post-v2.0: 4.1b and 4.3 are shipped/retired. Active initiatives are 3.5 Alerts, 4.2 Watchlists, CHART-IX.*

| Initiative | Classification | SPS | Justification |
|-----------|----------------|-----|---------------|
| 3.5 Alerts & Notifications | 🔥 Must continue | 3 | High strategic value — completes the v2.0 reporting & alerts theme. BLG-TECH-08 gate still pending; deferred to v2.1. Auto-advance trigger (DL-003) remains active. Touches async infrastructure patterns — standard feature, no §13 boundary contact. `strategy_rules.md §2` user-value delivery. |
| 4.2 Watchlists & Screening | 🔥 Must continue | 2 | Core product roadmap feature — direct support for trading decision workflow. Monitor tickers for entry signals. Standard product scope, well within established patterns. No §13 contact. `strategy_rules.md §2.` |
| CHART-IX Chart Interactivity | 🔥 Must continue | 2 | UX improvement on existing analytics. Low effort (S), high reversibility. Natural displacement candidate if a future Add requires stops (DL-009, initiative register flag retained). Standard feature, no boundary proximity. |

**No initiative is classified ⚠ Re-evaluate or ❌ Consider stopping.**

### Strategy Proximity Scores

| Initiative | SPS | Strategy ref |
|-----------|-----|-------------|
| 3.5 Alerts & Notifications | 3 | Standard feature — notification delivery and preference model; no §13 boundary contact |
| 4.2 Watchlists | 2 | Standard improvement — display and data model work |
| CHART-IX | 2 | Standard improvement — UX on existing analytics |

**CPS (this cycle):** (3 + 2 + 2) ÷ 3 = **2.33**
**Prior CPS (2026-03-17__item-v1.10):** 2.40
**Delta:** −0.07 (decrease — 4.3 SPS=4 and 4.1b SPS=1 removed from active pool as shipped; remaining 3 initiatives lower-SPS on average)

No delta alert (threshold: +0.5). No absolute alert (2.33 < 2.5 threshold). ✅

### Horizon Review

**Now (v2.1 — committed delivery scope):**
- 3.5 Alerts & Notifications — remains in Now/v2.1 with gate condition (BLG-TECH-08). Auto-advance trigger (DL-003) active. No change warranted.

**Next (v2.1/v2.2 — planned in principle):**
- 4.2 Watchlists & Screening — correctly placed. No urgency signal to promote to Now.
- CHART-IX Chart Interactivity — correctly placed. Displacement candidate flag retained.

**Later (strategic intent):**
- Position Correlation Analysis, Backtesting Module, Multi-Portfolio Support, Mobile App, Full Compliance Scoring, Market Correlation Analysis, AI Journal Summarisation, New Technical Indicators, Customisable Dashboard Layout — no context change since last review. No promotion to Next recommended.

**Recommended horizon movements:** None. All items correctly placed for the v2.1 → v2.2 sequence. No promotion or demotion warranted.

---

## STEP 3 — Backlog Health

### Summary

| Category | Finding |
|----------|---------|
| Obsolete items | None identified. |
| Duplicates | None. BLG-DATA-01 / BLG-NEW-13 scope boundary documented (DL-009 action-now patch). |
| Strategic alignment | All items reviewed; no misaligned items. New BLG-GOV-03/04/05/06 items added 2026-03-18 from architectural review — governance process improvements; correctly placed at v2.2. |
| Quick wins being ignored | BLG-GOV-05 (release planning loads scored_initiatives.md) is a 1-line prompt update — could be treated as an immediate action-now in lessons learnt rather than a v2.2 backlog item. Noted for STEP 11 consideration. |
| Technical debt accumulating | BLG-SPEC-G6 (`total_return_pct` not returned by GET /analytics/metrics) — P3, v2.1 backlog; low urgency but worth addressing before v2.1 ships. BLG-TECH-08 (async notification ADR) is the critical blocker for 3.5 Alerts; should be highest priority for v2.1 pre-work. |
| BLG-TECH-08 status | Not yet in backlog as a formal item — it is referenced as a prerequisite for 3.5 Alerts. Should be confirmed as a backlog item for v2.1 pre-work. Already exists as a reference; note in STEP 8. |

**No backlog items deleted or rewritten at this stage.**

---

## STEP 4 — Ideas

Window: IW-20260317-01 (for the 2 submitted ideas)
Total submissions loaded: 21 (2 Submitted + 19 Parked-cycle-3)
Advancing to STEP 5: 2
Parked (re-park): 11
Rejected: 8
Stale ideas (≥3 cycles parked) surfaced: 19
Stale ideas disposed this cycle: 19

### Stale Idea Dispositions (19 ideas at Parked-cycle-3 — mandatory active PO disposition per §4.5)

| Idea ID | Title | Disposition | Written Rationale |
|---------|-------|-------------|------------------|
| IDEA-ai-compliance-20260304-02 | AI-Generated Artefact Traceability Standard | ❌ Reject | AI governance infrastructure not aligned with current delivery focus; YAGNI at 2-person scale; no AI traceability framework is planned |
| IDEA-base44-frontend-20260304-01 | Loading State Standardisation | 🅿 Re-park (cycle-4) | Still capacity-constrained for v2.1; revisit for v2.2 after async notification infrastructure (BLG-TECH-08) lands |
| IDEA-base44-frontend-20260304-02 | User-Facing Error Message Mapping Layer | 🅿 Re-park (cycle-4) | BLG-SPEC-G2 Error Response Standard still undefined; revisit once error response standard is specified |
| IDEA-data-model-owner-20260304-02 | Data Retention and Archiving Policy | ❌ Reject | Single-user system; data retention policy is YAGNI at current scale; reject unless operational or legal need arises |
| IDEA-director-of-hr-20260304-01 | Agent Role Onboarding Guide | ❌ Reject | Team charter adequately covers role definitions for a 2-person operation; onboarding guide would be redundant overhead |
| IDEA-director-of-quality-20260304-01 | Spec-to-Test Traceability Matrix | 🅿 Re-park (cycle-4) | ST-17 Spec Coverage Inventory still incomplete (items_blocked in v2.0 sprint); revisit after ST-17 ships in v2.1 |
| IDEA-finops-20260304-01 | Cloud Resource Tagging Standard | ❌ Reject | Premature at current scale; cloud costs not material for single-user system |
| IDEA-finops-20260304-02 | Infrastructure Cost Budget Alert | ❌ Reject | Same rationale as Cloud Resource Tagging; premature |
| IDEA-frontend-ux-20260304-01 | UI Component Interaction Specification | ❌ Reject | Requires design system foundation not planned; YAGNI at 2-person scale without a design system |
| IDEA-frontend-ux-20260304-02 | Accessibility Baseline | 🅿 Re-park (cycle-4) | v2.0 shipped; accessibility improvements valid for v2.2+ consideration; revisit when user base grows |
| IDEA-head-of-engineering-20260304-02 | API Endpoint Performance Baseline | 🅿 Re-park (cycle-4) | API surface now stable post-v2.0; performance baseline technically feasible; revisit for v2.2 |
| IDEA-head-of-ux-20260304-01 | Daily Trading Workflow Journey Map | ❌ Reject | UX research artefact not warranted for single-user system where user and developer are the same person |
| IDEA-head-of-ux-20260304-02 | Design Token System | 🅿 Re-park (cycle-4) | v2.0 shipped; design tokens meaningful for v2.2+ as UI matures; revisit for v2.2 planning |
| IDEA-infra-ops-20260304-02 | System Health Check Playbook | 🅿 Re-park (cycle-4) | Staging environment now live (BLG-OPS-01 v1.10); health check playbook now relevant; revisit for v2.2 |
| IDEA-metrics-analytics-20260304-02 | Metrics Staleness Indicator | 🅿 Re-park (cycle-4) | Valid UX enhancement; revisit for v2.2 alongside BLG-FEAT-03 (Slippage Tracking) |
| IDEA-pmo-lead-20260304-02 | Delivery State Report (CI-Generated) | 🅿 Re-park (cycle-4) | CI pipeline stable post-v1.10; technically feasible; revisit for v2.2 |
| IDEA-qa-lead-20260304-01 | Canonical Test Execution Report Template | 🅿 Re-park (cycle-4) | Test infrastructure developing; revisit for v2.2 after test coverage baseline established |
| IDEA-qa-lead-20260304-02 | Defect Age Reporting | ❌ Reject | Premature when test coverage gaps exist; focus on coverage first |
| IDEA-qa-testing-20260304-02 | Test Automation Readiness Assessment | 🅿 Re-park (cycle-4) | CI automation now exists (v1.10); readiness assessment now more relevant; revisit for v2.2 |

### Ideas Advancing to STEP 5

| Idea ID | Agent | Title | Displacement Named |
|---------|-------|-------|--------------------|
| IDEA-financial-reporting-20260317-01 | Financial Reporting Owner | Tax Year P&L Report — PDF Export | CHART-IX (if roadmap-level; backlog-only promotion — displacement not required per DL-005 precedent) |
| IDEA-financial-reporting-20260317-02 | Financial Reporting Owner | Tax Year P&L Report — CSV Table Export | None required (backlog-only promotion) |

### Innovation Debt Notes

Idea intake engine was not run before this roadmap run (no standalone `run ideas` this cycle). Ideas were available from the prior intake window IW-20260317-01 (2 submitted items from v2.0 staging feedback). Intake threshold (≥20 open ideas) was met so STEP -1.6 inline intake was also skipped. No new agent submissions this cycle.

---

## STEP 5 — Debate

**Strategy constraints re-stated (top 2 most likely to block):**
1. **§13 system boundaries** — the system is deterministic and non-configurable at the strategy level. Any feature touching execution parameters, automation, or ML-based outputs hits a hard gate.
2. **Single-user scope** — complexity-to-value ratio must justify itself for a solo trader-developer; features with heavy infrastructure overhead for marginal gain are candidates for deferral.

### Pre-Debate Gate Checks (5.0)

**PoG validity:** Active PoG is POG-20260304-01 (item 4.3). Item 4.3 has now shipped — PoG is moot; no active item carries an open PoG gate. No stale PoG check required for advancing candidates (neither PDF Export nor CSV Export has a prior PoG or §13 gate).

**Score-5 presence:** Neither candidate has a Score-5 proximity. No SRO veto authority required.

---

### Candidate 1: IDEA-financial-reporting-20260317-01 — Tax Year P&L Report PDF Export

**5.0 Required Case (Product Owner):**
1. **Problem:** The tax year P&L report shipped in v2.0 is browser-only. The trader needs to share this report with an accountant or file supporting documentation with HMRC. Browser-print produces inconsistent formatting — table layouts, page breaks, and number formatting vary across browsers. For a statutory financial record, formatting reliability matters.
2. **Strategic alignment:** `strategy_rules.md §2` — user value delivery. Annual tax filing is a real, recurring obligation for an active trader. A PDF export with consistent formatting removes friction in the compliance workflow.
3. **If not done:** User relies on browser-print; formatting inconsistencies possible; limited sharing workflow; manual workarounds required.
4. **Displacement:** Backlog-level promotion only — no roadmap-level Add. No roadmap displacement required (DL-005 precedent). If treated as a roadmap-level Add: CHART-IX is the standing displacement candidate.

**5.1 Challenger Counter-Argument (Type A):**
- **Challenger position:** Park
- **Evidence:** `decision_log.md DL-008` — 4.1c Server-Side PDF Report was explicitly killed because "browser-print remains functional." The prior kill decision specifically weighed PDF formatting inconsistency against development cost and concluded browser-print sufficed. This idea re-proposes the same feature category. Submitting the same class of feature as staging feedback after one use cycle does not constitute a material change in the cost-benefit calculus.
- **Reason:** The DL-008 rationale did not distinguish by report type — it assessed PDF generation as a category and found browser-print adequate. A tax year P&L report has the same browser-print options as any other report. The statutory filing use case is not new — it was foreseeable when 4.1b was scoped. If it was important enough to require a server-side PDF, it should have been scoped into 4.1b.
- **Consequence:** If we proceed, we open a PDF infrastructure track that we deliberately deferred in DL-008. If we park, the user has functional browser-print until demand is confirmed beyond staging observation.
- **Outcome implied:** 🅿 Park — revisit if browser-print proves materially inadequate in practice.

**5.2 Product Owner Response:**
The Challenger's DL-008 reference is well-taken but the distinction is meaningful. DL-008 killed 4.1c (server-side PDF of a portfolio view) as a *displaced* item — it was killed specifically to make room for BLG-OPS-01 (infrastructure), not because PDF value was low. The kill decision was capacity-driven, not value-driven. The tax year P&L report is categorically different: it is a compliance document with statutory filing implications, not a display convenience. Browser-print of a styled multi-table financial report with page-break requirements and number precision requirements is unreliable in a way that a portfolio analytics view is not.

That said, the PO accepts the Challenger's point that this should remain a **backlog-level** item rather than a roadmap-level initiative — the effort is S and it competes within v2.1 release planning capacity, not at the roadmap level.

**Outcome: ✅ Advance — backlog-level only.** `strategy_rules.md §2` user value; statutory filing use case distinguishes from DL-008. No roadmap displacement required.

---

### Candidate 2: IDEA-financial-reporting-20260317-02 — Tax Year P&L Report CSV Export

**5.0 Required Case (Product Owner):**
1. **Problem:** The tax year P&L report has no machine-readable export. An accountant or tax software may require structured data rather than a rendered document.
2. **Strategic alignment:** `strategy_rules.md §2` user value. CSV is the simplest possible output format extension — minimal infrastructure, immediate value.
3. **If not done:** User must manually extract data; no integration path with tax software.
4. **Displacement:** Backlog-level only. No displacement required.

**5.1 Challenger Clearance:**
Cleared — Assessed against `strategy_rules.md §13` system boundaries: §13.1 (no automated trading), §13.2 (fixed strategy), §13.3 (deterministic outputs) — none are engaged by a CSV export of computed P&L data. The export is a deterministic serialisation of an existing endpoint response. Strategic scope boundaries are fully intact. High reversibility (format-only change; no schema migration). Single-user scale is appropriate. No §13 boundary is approached.

**5.2 Product Owner:** ✅ Advance — backlog-level only. Simple, high-value, low-risk output format extension.

---

### STEP 5 Summary

| Candidate | Challenger Output | PO Decision | Disposition |
|-----------|------------------|-------------|-------------|
| Tax Year P&L PDF Export | Type A counter-argument (Park — DL-008 consistency) | Rebutted (distinction: capacity-kill vs value-kill; statutory filing use case) | ✅ Advance (backlog) |
| Tax Year P&L CSV Export | Clearance Statement | Confirmed Advance | ✅ Advance (backlog) |

**No PoG required** — neither candidate has a hard gate condition.

---

## STEP 8 — Final Rebalance Decision

### Roadmap-Level Decisions

| Initiative | Decision | Rationale |
|-----------|----------|-----------|
| 3.5 Alerts & Notifications | ⏸ Defer (unchanged, DL-003) | BLG-TECH-08 gate still pending. Auto-advance trigger active. No change. |
| 4.2 Watchlists & Screening | 🔥 Continue | Correct v2.1 placement. No change. |
| CHART-IX | 🔥 Continue | Correct v2.1 placement. Displacement candidate flag retained. No change. |

**Net-zero check (STEP 9.0):** 0 roadmap Adds, 0 roadmap Kills. 0 ≤ 0. ✅

### Backlog-Level Decisions

Two new items promoted to backlog (backlog-level only — per DL-005 precedent, no roadmap displacement required):

| ID | Item | Priority | Effort | Target |
|----|------|----------|--------|--------|
| BLG-FR-01 | Tax Year P&L Report — PDF Export | P2 | S | v2.1 |
| BLG-FR-02 | Tax Year P&L Report — CSV Table Export | P2 | S | v2.1 |

### Skill-Silo Check

Active roadmap execution scope (v2.1):
- 3.5 Alerts (blocked, L effort when unblocked) — execution-heavy
- 4.2 Watchlists (M) — execution-heavy
- CHART-IX (S) — execution-heavy
- BLG-TECH-08 ADR (S) — governance-heavy (architecture decision record)

Governance load ≈ 10–15%. Below 20% floor.

**Sign-Off Capacity Floor check (20%):** PO confirms adequate review capacity for v2.1 execution volume. In the 2-person team model (user = PO + developer), sign-off is inherent in the delivery workflow. Governance capacity risk: low. Noted but does not halt.

**No Skill-Silo Alert issued** (governance load below ceiling; floor advisory acknowledged).

### BLG-TECH-08 Note

BLG-TECH-08 (async notification architecture ADR) is the sole gate for 3.5 Alerts v2.1. It is referenced in the current roadmap but is not a formal backlog item with acceptance criteria. Recommend ensuring it is formalised as a backlog item in v2.1 planning to guarantee it gets scheduled.

### Displacement Candidate

CHART-IX remains the natural displacement candidate per initiative register flag (DL-009). No change. No new displacement candidate flag required.
