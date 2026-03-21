**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-21

---

# Cycle Record — Roadmap Rebalance 2026-03-21__item-3.5

**Run type:** Completion-triggered
**Completion event:** 3.5 — Alerts & Notifications (shipped v2.1, 2026-03-21)
**Cycle ID:** 2026-03-21__item-3.5
**Date:** 2026-03-21
**Mode:** Standard
**Run tier:** Standard

---

## STEP 1 — Run Manifest

*(See `run_manifest.md` for full preflight records. Summary here.)*

**Run type:** Completion-triggered
**Completion event:**
- ID: 3.5
- Name: Alerts & Notifications
- Date: 2026-03-21
- Release: v2.1

**Canonical inputs:**
- `claude/charter/team_charter.md`
- `claude/charter/document_lifecycle_guide.md`
- `claude/strategy/strategy_rules.md` v1.3
- `claude/roadmap/current_roadmap.md`
- `claude/backlog/backlog.md`

**Decision authorities:** Product Owner, Strategy Rules & System Intent Owner, Head of Specs Team, PMO Lead, FinOps & Resource Architect, Infrastructure & Operations Owner, Director of Quality

**Non-decision roles:** Facilitator, Challenger

### Capacity Release (STEP 1.2)

Item: 3.5 — Alerts & Notifications
- **FTE released:** ~3–4 sprints (backend alert service + watchlist service + notification infrastructure + frontend alert/watchlist pages)
- **Skills released:** Backend engineering (FastAPI services, Telegram delivery), Frontend (React alert/watchlist components), QA (notification test scenarios)
- **Duration freed:** Capacity available for v2.2 scope determination
- **Constraints:** Telegram delivery (BLG-OPS-04) remains a deferred gap — partial capacity release (notification scheduling not yet resolved)

### Prior Cycle Outstanding Actions (STEP -1.5 outcome)

| Patch | Source cycle | Status |
|-------|-------------|--------|
| LL-01-patch-4.3: `roadmap_management_prompt.md` retirement step must update `initiative_register.md` Active→Completed | 2026-03-18__item-4.3 | **Carried forward** — patch not yet applied to prompt file. Head of Specs Team: target before next `manage roadmap` run. `initiative_register.md` will be corrected in STEP 9 of this run (within write scope). Prompt fix deferred. |

---

## STEP 2 — Re-Validation

**Authorities:** Product Owner + Strategy Rules & System Intent Owner

### Active Initiatives Reviewed

At the start of this run, the active initiatives table in `initiative_register.md` shows: 3.5, 4.2, and CHART-IX. However:
- 3.5 Alerts & Notifications: **Shipped v2.1** (this run's completion event)
- 4.2 Watchlists & Screening: **Shipped v2.1** (retired in post-ship closure 2026-03-21)
- CHART-IX Chart Interactivity Enhancements: **Shipped v2.1** (retired in post-ship closure 2026-03-21)

**Result: Zero active roadmap initiatives to validate.** All previously active items shipped in v2.1.

The register's Active table is stale (LL-01-patch-4.3 root cause — confirmed). STEP 9 will update it.

### Strategy Proximity Scores (SPS)

Zero active initiatives → no SPS computation required.

**Stale register note:** 3.5 SPS was historically 3 (from prior cycle). 4.2 SPS was 2. CHART-IX SPS was 2. These are now archived items.

### Cycle Proximity Score (CPS)

- **CPS this cycle:** N/A — zero active initiatives. Recorded as **0.0**.
- **Prior CPS (2026-03-18__item-4.3):** 2.33
- **Delta:** −2.33 (all items shipped — expected and correct)
- **Trend:** No strategy drift alert. Delta is a decrease (all active items shipped). CPS absolute = 0.0 (below 2.5 threshold). Extended tier not triggered.

### Horizon Review

**Now (committed):** Nothing committed yet. v2.2 scope is TBD — release planning engine will scope.

**Next (planned):** Nothing placed in Next horizon. The release planning engine will use the backlog and freed capacity from v2.1 to plan v2.2.

**Later (Horizon 3):** Items reviewed for potential promotion to Now/Next:
- Position Correlation Analysis: No context change. Still appropriate as Later.
- Backtesting Module: No context change. Very High effort; appropriate as Later.
- Multi-Portfolio Support: No context change. Appropriate as Later.
- Mobile App: No context change. Appropriate as Later.
- Full Compliance Scoring: No context change. Lightweight version shipped in v1.9; full version appropriate as Later.
- BLG-TECH-05 (Prometheus): No context change. P3, no operational need yet.
- Market Correlation Analysis: External data pipeline gate not cleared.
- AI Journal Summarisation: §13 decision gate not cleared.
- New Technical Indicators: Strategy rules review gate not cleared.
- Customisable Dashboard Layout: No context change.

**Gated items reviewed (§6):**
- AI-SUM: Gate not cleared. No §13 boundary decision made.
- TECH-IND: Gate not cleared. No strategy rules review completed.
- MKT-COR: Gate not cleared. No external data pipeline decision.

**Horizon movements:** None recommended. The completion of v2.1 releases significant capacity; v2.2 scope will be set by the release planning engine from the enriched backlog after this run.

---

## STEP 3 — Backlog Health

**Authorities:** Head of Specs Team (process), Product Owner (planning)

### Active Backlog Review

**P0/P1 items:**
- BLG-OPS-04 (P1): Alert evaluation scheduling — HIGH priority gap post-v2.1. Alert system has no scheduler; entirely manual trigger. Design questions still unresolved (frequency, cooldown, trigger mechanism). Needs PO answers before engineering can proceed. Not obsolete. Still strategically aligned.

**P2 items:**
- BLG-QA-01: Playwright E2E for chart interactivity — valid; depends on BLG-OPS-03 (shipped). Dependency cleared. Promotion candidate for v2.2.
- BLG-BE-03 (P2, XS): Latent CSV export import bug — **PROMOTION CANDIDATE.** Latent defect, XS effort, should be in v2.2 as first story. No dependency.
- BLG-UX-01: Sidebar overflow — valid, P2, UX gap post v2.1 growth. Not obsolete.
- TEST-GAP-EPIC-02: Notifications scenarios — not formally executed; P2. Valid gap.
- TEST-GAP-EPIC-03: Watchlist test scenarios — no file exists; P2. Valid gap.
- BLG-GOV-03/04/05/06: Governance improvements — all valid P2 items targeting v2.2.

**P3 items:**
- BLG-BE-02: R-Multiple stop price fix — valid technical gap.
- BLG-FE-01: StatsCard gradient key — cosmetic, P3, XS.
- TEST-GAP-EPIC-05-SLIP: Slippage scenario file — P3, valid gap.
- BLG-TECH-05: Prometheus endpoint — still appropriate as P3.

**Obsolete:** None identified. All items remain relevant.
**Duplicates:** None identified.
**Technical debt accumulation:** BLG-BE-03 (latent bug) should be addressed in v2.2 as the first delivery.
**Quick wins being ignored:** BLG-BE-03 (XS, P2), BLG-FE-01 (XS, P3), BLG-BE-02 (S, P3) — all are small-effort items that should be included in v2.2.

**Overall backlog health:** Good. No obsolete or duplicate items. Clear priority ordering. BLG-OPS-04 P1 gap should drive v2.2 thematic scope. Test coverage gaps (TEST-GAP items) represent ongoing QA debt that should be scheduled in v2.2.

---

## STEP 4 — Ideas

**Authorities:** Facilitator (review), Product Owner (classification)

### Window Summary

Window: IW-20260321-01 (inline intake, triggered by <20 eligible ideas)
Total submissions loaded: 55 (44 new + 11 Parked-cycle-4)
Advancing to STEP 5: 7
Parked: 46
Rejected: 1 (stale — no viable path)
Closed stale ideas: 1 (reject)

*(Full window summary: `claude/ideas/window_summary_IW-20260321-01.md`)*

### Stale Ideas (Parked-cycle-4) — Mandatory PO Active Disposition

| Idea ID | Title | Cycles Parked | Disposition | Rationale |
|---------|-------|---------------|-------------|-----------|
| IDEA-base44-frontend-20260304-01 | Loading State Standardisation | 4 | ✅ Advance | Dependency BLG-TECH-08 (async notification ADR) has shipped in v2.1. Gate cleared. |
| IDEA-base44-frontend-20260304-02 | User-Facing Error Message Mapping Layer | 4 | ✅ Advance | Dependency BLG-SPEC-G2 (Error Response Standard) shipped in v1.9. Gate cleared. |
| IDEA-director-of-quality-20260304-01 | Spec-to-Test Traceability Matrix | 4 | ✅ Advance | Dependency ST-17 (Spec Coverage Inventory) shipped in v2.1. Gate cleared. Duplicate of IDEA-director-of-quality-20260321-01 — merged as single candidate. |
| IDEA-frontend-ux-20260304-02 | Accessibility Baseline for Critical UI Components | 4 | 🅿 Re-park (cycle-5) | Single-user system; accessibility is not blocking core workflows at current scale. Revisit if user base expands or regulatory requirements emerge. |
| IDEA-head-of-engineering-20260304-02 | API Endpoint Performance Baseline | 4 | ✅ Advance | API surface stable post-v2.1. Gate condition met. |
| IDEA-head-of-ux-20260304-02 | Design Token System | 4 | 🅿 Re-park (cycle-5) | Design system document (IDEA-head-of-ux-20260321-02) is a better prerequisite; revisit after design system doc is authored. |
| IDEA-infra-ops-20260304-02 | System Health Check Playbook | 4 | 🅿 Re-park (cycle-5) | Superseded in spirit by IDEA-infra-ops-20260321-01 (health check endpoint) which is more actionable. Will route via health check endpoint backlog item. Re-park this idea. |
| IDEA-metrics-analytics-20260304-02 | Metrics Staleness Indicator | 4 | ✅ Advance | Dependency BLG-FEAT-03 (Slippage Tracking) shipped in v2.1. Gate cleared. |
| IDEA-pmo-lead-20260304-02 | Delivery State Report (CI-Generated) | 4 | 🅿 Re-park (cycle-5) | CI tooling investment; lower priority than alert scheduling, bug fixes, and test coverage gaps for v2.2. Revisit for v2.3. |
| IDEA-qa-lead-20260304-01 | Canonical Test Execution Report Template | 4 | 🅿 Re-park (cycle-5) | Test coverage baseline still being established (TEST-GAP items open). Revisit after TEST-GAP-EPIC-02/03 are completed. |
| IDEA-qa-testing-20260304-02 | Test Automation Readiness Assessment | 4 | ✅ Advance | CI automation exists post-v1.10; readiness assessment now relevant. |

### New Ideas from IW-20260321-01 — Classification

**Advancing (4 from new submissions):**

| Idea ID | Agent | Title | Displacement Named |
|---------|-------|-------|--------------------|
| IDEA-product-owner-20260321-01 | Product Owner | Alert threshold customisation | Capacity freed from 3.5 completion |
| IDEA-strategy-owner-20260321-01 | Strategy Rules & System Intent Owner | Strategy compliance score on dashboard | Capacity freed from 3.5 completion |
| IDEA-backend-engineering-20260321-01 | Backend Engineering Patterns Owner | API key authentication for Render deployment | Lower-priority cosmetic work (BLG-FE-01) |
| IDEA-data-model-owner-20260321-01 | Data Model & Domain Schema Owner | Alert history table | Capacity freed from 3.5 completion |

*(Note: IDEA-cybersecurity-20260321-02 proposes the same API auth idea as IDEA-backend-engineering-20260321-01 — merged as one candidate. IDEA-director-of-quality-20260321-01 merged with stale duplicate above.)*

**Parked (36 from new submissions):**

| Idea ID | Agent | Title | Consecutive Cycles Parked | Reason |
|---------|-------|-------|--------------------------|--------|
| IDEA-head-of-specs-20260321-01 | Head of Specs Team | Spec dependency map | 1 | Valuable governance investment; lower priority than spec-to-test traceability (advancing) and current v2.2 feature priorities. Revisit v2.3. |
| IDEA-head-of-specs-20260321-02 | Head of Specs Team | Machine-readable spec front-matter | 1 | CI automation investment; BLG-GOV-05 (scored_initiatives load) covers similar intent at lower cost. Revisit v2.3. |
| IDEA-pmo-lead-20260321-01 | PMO Lead | Cycle velocity metric | 1 | Process metric; useful but lower priority than product delivery gaps. Revisit v2.3. |
| IDEA-pmo-lead-20260321-02 | PMO Lead | Governance health score | 1 | Operational dashboard; deferred pending v2.2 product delivery. Revisit v2.3. |
| IDEA-director-of-quality-20260321-01 | Director of Quality | Spec-to-test traceability matrix | — | Merged with stale IDEA-director-of-quality-20260304-01 (advancing). |
| IDEA-director-of-quality-20260321-02 | Director of Quality | Test data seed script library | 1 | Operational infrastructure; partially addressed by TEST-GAP items already in backlog. Revisit v2.3. |
| IDEA-strategy-owner-20260321-02 | Strategy Rules & System Intent Owner | §13 boundary review cadence | 1 | Governance process; valid but lower priority than product delivery. Revisit v2.3. |
| IDEA-finops-20260321-01 | FinOps & Resource Architect | Render hosting tier review | 1 | Operational; depends on BLG-OPS-04 (alert scheduling) being specced first to know if cron upgrade is needed. Park until BLG-OPS-04 design is resolved. |
| IDEA-finops-20260321-02 | FinOps & Resource Architect | Database size monitoring | 1 | Operational; valid but lower priority. Revisit if DB growth becomes material. |
| IDEA-infra-ops-20260321-01 | Infrastructure & Operations Owner | Health check endpoint | 1 | Good operational idea; backlog-level not roadmap-level. Will add to backlog as BLG-OPS-05 via this cycle (STEP 9). Parked from ideas register — routed to backlog directly. |
| IDEA-infra-ops-20260321-02 | Infrastructure & Operations Owner | Staging data reset script | 1 | Operational; valid; lower priority than test scenario authoring. Revisit v2.3. |
| IDEA-challenger-20260321-01 | Challenger | SPS≥4 mandatory §13 review gate | 1 | Governance prompt improvement; valid but complex to implement. Revisit v2.3. |
| IDEA-challenger-20260321-02 | Challenger | Complexity budget tracking | 1 | Valuable but premature — system scope is not yet causing uncontrolled complexity growth. Revisit v2.3. |
| IDEA-backend-engineering-20260321-02 | Backend Engineering Patterns Owner | Alert evaluation idempotency | 1 | Design concern; part of BLG-OPS-04 scope. Park — will be addressed as part of BLG-OPS-04 design. |
| IDEA-ai-compliance-20260321-01 | AI Compliance & Governance Officer | Governed decision audit log | 1 | Governance investment; decision_log.md already captures roadmap decisions. Further scope TBD. Revisit v2.3. |
| IDEA-ai-compliance-20260321-02 | AI Compliance & Governance Officer | Model version contract | 1 | Valid AI governance concern; lower priority. Revisit v2.3. |
| IDEA-cybersecurity-20260321-01 | Cybersecurity & Trust Lead | CSP headers | 1 | Good security hardening; XS effort; will add to backlog as BLG-SEC-02. Parked from ideas register. |
| IDEA-cybersecurity-20260321-02 | Cybersecurity & Trust Lead | API auth (X-API-Key) | — | Merged with IDEA-backend-engineering-20260321-01 (advancing). |
| IDEA-metrics-analytics-20260321-01 | Metrics Analytics Owner | Consecutive losing streak metric | 1 | Useful analytics; capacity constrained. Revisit v2.3 alongside BLG-FEAT-09 (Metrics Staleness). |
| IDEA-metrics-analytics-20260321-02 | Metrics Analytics Owner | ATR-normalised sizing retrospective | 1 | Boundary-adjacent (SPS=4, references §13.1 determinism). Needs SPS≥4 careful treatment. Park — requires §13 clarification on whether sizing retrospective is deterministic analytics or inferential. |
| IDEA-head-of-engineering-20260321-01 | Head of Engineering | API response time baseline | 1 | Operational; will add to backlog as BLG-OPS-06. Parked from ideas register. |
| IDEA-head-of-engineering-20260321-02 | Head of Engineering | Background task scheduler | 1 | Directly overlaps BLG-OPS-04 design space. Park — scope should be determined as part of BLG-OPS-04 answer. |
| IDEA-base44-frontend-20260321-01 | Base44 Frontend | Keyboard shortcuts | 1 | UX enhancement; lower priority than functional gaps. Revisit v2.3. |
| IDEA-base44-frontend-20260321-02 | Base44 Frontend | Alert notification badge in nav | 1 | Reasonable UX enhancement; will route to backlog consideration via BLG-UX-01 scope discussion. Park. |
| IDEA-data-model-owner-20260321-02 | Data Model Owner | Position tags normalisation | 1 | Data model change with significant migration complexity; not justified by current single-user scale. Revisit v2.3. |
| IDEA-financial-reporting-20260321-01 | Financial Reporting Owner | Monthly P&L summary report | 1 | Good reporting enhancement; lower priority than alert scheduling and bug fixes. Revisit v2.3. |
| IDEA-financial-reporting-20260321-02 | Financial Reporting Owner | Net-of-costs performance tracking | 1 | Valuable financial insight; medium effort; lower priority than core gaps. Revisit v2.3. |
| IDEA-director-of-hr-20260321-01 | Director of HR | Agent role effectiveness review | 1 | Governance process; valid; lower priority than product delivery. Revisit v2.3. |
| IDEA-director-of-hr-20260321-02 | Director of HR | New agent onboarding checklist | 1 | Governance housekeeping; no new agents anticipated. Revisit when relevant. |
| IDEA-api-contracts-20260321-01 | API Contracts Owner | API version sunset policy | 1 | Governance document; important for future API management; lower priority at current scale. Revisit v2.3. |
| IDEA-api-contracts-20260321-02 | API Contracts Owner | Webhook event catalogue | 1 | Future integration enabler; not needed until integration is planned. Revisit v2.3. |
| IDEA-qa-testing-20260321-01 | QA & Testing Owner | Integration test coverage report | 1 | CI tooling; valuable; lower priority than test scenario authoring (TEST-GAP items). Revisit v2.3. |
| IDEA-qa-testing-20260321-02 | QA & Testing Owner | Critical-path smoke test | 1 | Good testing improvement; scope overlaps BLG-QA-01 (Playwright E2E). Park until BLG-QA-01 scope is confirmed. |
| IDEA-qa-lead-20260321-01 | QA Lead | QA sign-off SLA standard | 1 | Process standard; valuable; lower priority at current delivery velocity. Revisit v2.3. |
| IDEA-qa-lead-20260321-02 | QA Lead | Bug severity classification matrix | 1 | Process standard; currently handled by P0–P3 taxonomy. Revisit if defect reporting gaps emerge. |
| IDEA-frontend-ux-20260321-01 | Frontend Specs Owner | Frontend performance budget | 1 | Spec investment; premature before significant performance issues materialise. Revisit v2.3. |
| IDEA-frontend-ux-20260321-02 | Frontend Specs Owner | React component inventory | 1 | Useful spec work; lower priority. Revisit v2.3. |
| IDEA-head-of-ux-20260321-01 | Head of UX & Design | Responsive layout breakpoints spec | 1 | Good planning even if implementation deferred; lower priority than functional gaps. Revisit v2.3. |
| IDEA-head-of-ux-20260321-02 | Head of UX & Design | Design system document | 1 | Prerequisite to IDEA-head-of-ux-20260304-02 (Design Token System). Good foundation work. Revisit v2.3 as part of a "Design Foundation" theme. |

**Rejected (1):**
None from new submissions. However, IDEA-product-owner-20260321-01 and IDEA-product-owner-20260321-02 (Weekly trading review digest) — the weekly digest is parked, not rejected.

*(Note: IDEA-infra-ops-20260321-01, IDEA-head-of-engineering-20260321-01, IDEA-cybersecurity-20260321-01 are being added directly to the backlog as small, unambiguous improvements rather than advancing to STEP 5 debate — they are clearly backlog-level, not roadmap-level, and have no strategic complexity requiring debate.)*

### Ideas Advancing to STEP 5

| Idea ID | Agent | Title | Displacement Named |
|---------|-------|-------|--------------------|
| IDEA-director-of-quality-20260304-01 | Director of Quality | Spec-to-Test Traceability Matrix | Capacity freed from 3.5 |
| IDEA-base44-frontend-20260304-01 | Base44 Frontend | Loading State Standardisation | Capacity freed from 3.5 |
| IDEA-metrics-analytics-20260304-02 | Metrics Analytics Owner | Metrics Staleness Indicator | Capacity freed from 3.5 |
| IDEA-head-of-engineering-20260304-02 | Head of Engineering | API Endpoint Performance Baseline | Capacity freed from 3.5 |
| IDEA-qa-testing-20260304-02 | QA & Testing Owner | Test Automation Readiness Assessment | Capacity freed from 3.5 |
| IDEA-product-owner-20260321-01 | Product Owner | Alert threshold customisation | Capacity freed from 3.5 |
| IDEA-strategy-owner-20260321-01 | Strategy Rules & System Intent Owner | Strategy compliance score on dashboard | Capacity freed from 3.5 |
| IDEA-backend-engineering-20260321-01 | Backend Engineering Patterns Owner | API key authentication | BLG-FE-01 (cosmetic, lower priority) |
| IDEA-data-model-owner-20260321-01 | Data Model Owner | Alert history table | Capacity freed from 3.5 |

**Innovation Debt Notes:** None — all eligible agents submitted ≥2 ideas. Intake engine run this cycle (IW-20260321-01).

---

## STEP 5 — Debate

**Authorities:** Product Owner (chair) + Challenger (non-decision challenge)

**Context re-read (mandatory per STEP 5 preamble):**
Top 2 constraints most likely to block an "easy yes":
1. §13.2 — system is deterministic; anything that introduces computed judgements or automated scores could be interpreted as blurring the human-in-loop boundary.
2. Zero-sum displacement rule — no roadmap-level additions without confirmed kills. Backlog-only promotions are free of this constraint. The question for each candidate is: is this roadmap-level or backlog-level?

**Pre-debate gate checks (STEP 5.0):**
- PoG validity: No prior PoG documents cover any of these candidates. N/A.
- Score-5 presence: IDEA-strategy-owner-20260321-01 requires SPS assignment → SPS assigned below.

### Candidate Debates

---

**Candidate 1: IDEA-director-of-quality-20260304-01 — Spec-to-Test Traceability Matrix**

Required Case (PO):
- Problem: No formal mapping from spec ACs to test scenarios. DoQ sign-off cannot verify which scenarios cover which ACs.
- Strategic alignment: §4.2 (structured QA planning) — supports the human-in-loop quality gate design.
- If not done: QA sign-offs will continue citing tests without proving AC coverage. Risk of AC gaps remaining invisible until integration failures.
- Displacement: Capacity freed from 3.5 completion. Backlog-level only.

SPS: **1** — pure quality infrastructure, no contact with §13 strategy boundaries.

Challenger (STEP 5.1):
*Clearance Statement — Cleared: This is a QA documentation exercise with no proximity to §13 strategy boundaries (§13.2 non-automation, §13.1 human-in-loop, §13.3 determinism). All §13 sections reviewed; none engaged. Economic constraint: modest effort (M), no FTE conflict given freed capacity.*

PO Response (STEP 5.2): ✅ Advance — to backlog (not roadmap-level initiative). New backlog item: BLG-SPEC-T01.

---

**Candidate 2: IDEA-base44-frontend-20260304-01 — Loading State Standardisation**

Required Case (PO):
- Problem: API-backed interactions (portfolio load, watchlist load, alert evaluation) show inconsistent loading states — some spin, some flash empty, some error silently. UX quality gap.
- Strategic alignment: §2 (human-in-loop UX quality) — reliable loading states support user trust in data freshness.
- If not done: UX quality remains inconsistent; users may misinterpret loading as data absence.
- Displacement: Capacity freed from 3.5 (frontend skills specifically).

SPS: **2** — standard UX improvement, within established frontend patterns.

Challenger (STEP 5.1):
*Clearance Statement — Cleared: §13 sections reviewed. Loading states are pure frontend UX; no contact with strategy execution, automation, or determinism boundaries (§13.1–§13.3). Economic constraint: M effort, frontend skills are available post-v2.1. No economic veto.*

PO Response (STEP 5.2): ✅ Advance — to backlog (not roadmap-level). New backlog item: BLG-FE-02.

---

**Candidate 3: IDEA-metrics-analytics-20260304-02 — Metrics Staleness Indicator**

Required Case (PO):
- Problem: Analytics metrics can be based on stale data (last sync may be hours old). No indicator shows the user when data was last refreshed — they may be trading on stale P&L figures.
- Strategic alignment: §1 (deterministic, accurate decision support) — stale data visibility supports data integrity.
- If not done: User has no visibility into data freshness; may make decisions based on stale portfolio data.
- Displacement: Capacity freed from 3.5 (analytics/backend skills).

SPS: **2** — standard data quality feature, well within established analytics patterns.

Challenger (STEP 5.1):
*Clearance Statement — Cleared: §13.1–§13.3 reviewed. A staleness indicator is a read-only display feature; no contact with automation boundaries or strategy execution rules. Economic constraint: S–M effort, within available capacity.*

PO Response (STEP 5.2): ✅ Advance — to backlog. New backlog item: BLG-FEAT-09.

---

**Candidate 4: IDEA-head-of-engineering-20260304-02 — API Endpoint Performance Baseline**

Required Case (PO):
- Problem: No baseline exists for endpoint response times. As features are added, performance regressions cannot be detected. Particularly relevant for alert evaluation and chart interactivity now shipped.
- Strategic alignment: §1 (reliable decision support) — performance regression directly impacts user experience.
- If not done: Performance regressions will be invisible until they become user-visible problems.
- Displacement: Capacity freed from 3.5 (backend engineering skills).

SPS: **1** — operational infrastructure, no contact with §13.

Challenger (STEP 5.1):
*Clearance Statement — Cleared: Performance baseline is pure engineering infrastructure. §13.1–§13.3 reviewed; none applicable. Economic: S effort; within available capacity.*

PO Response (STEP 5.2): ✅ Advance — to backlog. New backlog item: BLG-OPS-05.

*(Note: Title slightly adjusted from "API Endpoint Performance Baseline" to align with operational framing — same scope.)*

---

**Candidate 5: IDEA-qa-testing-20260304-02 — Test Automation Readiness Assessment**

Required Case (PO):
- Problem: Before investing in broad test automation (Playwright, integration test suite), a readiness assessment should confirm the infrastructure and team capability is in place.
- Strategic alignment: §4.2 (quality gates) — structured QA investment requires scoping.
- If not done: Automation investment may proceed without assessing readiness, leading to partial or wasted effort.
- Displacement: Capacity freed from 3.5.

SPS: **1** — QA process, no contact with §13.

Challenger (STEP 5.1):
*Clearance Statement — Cleared: This is a planning/assessment exercise. §13 sections reviewed; not applicable. Economic: XS–S effort.*

PO Response (STEP 5.2): ✅ Advance — to backlog. New backlog item: BLG-QA-02.

---

**Candidate 6: IDEA-product-owner-20260321-01 — Alert Threshold Customisation**

Required Case (PO):
- Problem: Alert rules use fixed thresholds hardcoded in the system. A user monitoring a low-volatility stock and a high-volatility stock may need different stop_loss_approach percentages. No customisation exists.
- Strategic alignment: §1 (decision support tool) — configurable thresholds improve the quality of alerts as decision support.
- If not done: Alerts may over-fire on volatile assets or under-fire on quiet ones. User configures alerts and then can't tune them to their context.
- Displacement: Capacity freed from 3.5 (alerts domain specifically).

SPS: **3** — standard feature extending the just-shipped alerts system; within established patterns.

Challenger (STEP 5.1):
*Clearance Statement — Cleared: Alert threshold customisation is a user configuration feature for existing alerts. §13.2 reviewed — thresholds are display/query-scope controls (same pattern as DL-004 for top_n/lookback_days), not strategy execution parameters. §13.1 and §13.3 reviewed and not engaged. Economic: M effort, within available capacity.*

PO Response (STEP 5.2): ✅ Advance — to backlog. New backlog item: BLG-FEAT-10.

---

**Candidate 7: IDEA-strategy-owner-20260321-01 — Strategy Compliance Score on Dashboard**

Required Case (PO + Strategy Rules & System Intent Owner):
- Problem: Users have no automated visibility into whether their open positions respect the ATR-based stop discipline rules. A compliance score could surface violations before they compound.
- Strategic alignment: §1 (decision support), §3 (stop-loss discipline), §4 (trailing stop rules) — supports compliance awareness.
- If not done: Users manually review each position for compliance; important signals may be missed.
- Displacement: Capacity freed from 3.5.

SPS assignment (Strategy Rules & System Intent Owner): **4** — boundary-adjacent. A "compliance score" computed automatically approaches the boundary between decision support and automated judgement. §13.1 states the system is "a deterministic decision-support engine." §13.3 states "human-in-the-loop by design." A score that judges user behaviour autonomously (even read-only) is near the edge of this principle.

STEP 5.0 B — Score-4 check: Strategy Rules & System Intent Owner must be active for STEP 5. Confirmed.

Challenger (STEP 5.1) — **Type A counter-argument** (mandatory for Score-4):

- **Challenger position:** Park
- **Evidence:** strategy_rules.md §13.1 ("deterministic decision-support engine"), §13.3 ("human-in-the-loop by design"). Specifically: a "compliance score" that evaluates user behaviour against rules is a form of automated assessment — not a display of raw data, but a computed judgement. The specific §13 boundary being approached: §13.3 "human-in-the-loop by design." A system that tells the user "your compliance is 65%" is performing an evaluative role that should remain with the human.
- **Reason:** The distinction between a data display (✅ human-in-loop) and a computed score (⚠ boundary-adjacent) matters for the system's identity. Once the system computes "compliance" it begins to function as a judge. The next natural request will be "enforce compliance" (notifications for non-compliant positions) which would directly violate §13.2 ("not an automated trading bot" boundary is not far from "not an automated compliance enforcer"). If this idea advances, the scope constraint must be tight enough that it cannot evolve toward enforcement.
- **Consequence:** If we proceed without tight scope constraints, the system will drift from decision-support toward automated supervision, which the Product Owner has consistently declined in §13.

PO Response (STEP 5.2):
- Rebut with scope modification: The compliance score is **display-only, informational, and human-initiated**. It shows: per-position stop distance vs ATR, whether stop was last updated within N days, whether position size matches ATR-derived recommendation. It does NOT: generate alerts, enforce behaviour, block trades, or notify without explicit user action. The score is equivalent to showing raw ATR multiples — it provides the same data in a more digestible format. §13.3 human-in-loop is preserved because no action is taken by the system; the human reads the score and decides.
- Scope constraint: "No automated enforcement, no alerts generated by the score, no blocking behaviour. Display-only panel that surfaces raw stop/ATR data in a compliance-framed summary."
- Displacement: Funded by freed 3.5 capacity, as strategy rules domain.

Strategy Rules & System Intent Owner confirmation (Score-4 item after PO rebut): ✅ Confirmed with scope constraint — the scope modification addresses the §13 concern. "Display-only panel surfacing raw stop/ATR data" is within the deterministic decision-support boundary. Scope constraint must be captured in the backlog item AC.

Outcome: ✅ Advance — to backlog with scope constraint. New backlog item: BLG-FEAT-11.

---

**Candidate 8: IDEA-backend-engineering-20260321-01 — API Key Authentication**

Required Case (PO):
- Problem: The system is deployed on Render with publicly accessible URLs. There is no authentication on the API. Financial data (portfolio, trades, P&L) is readable by anyone who knows the URL.
- Strategic alignment: §1 (trust and data integrity) — financial data must be protected.
- If not done: Personal financial data exposed to anyone with the Render URL. Risk increases as the API surface grows.
- Displacement: BLG-FE-01 (StatsCard gradient cosmetic) is deprioritized to create space in v2.2 schedule.

SPS: **1** — infrastructure/security, no contact with §13 strategy boundaries.

Challenger (STEP 5.1):
- **Challenger position:** Park
- **Evidence:** §2.1 "single-user portfolio tracker." The system is designed for a single user. A shared security threat model applies only if users share the URL — which is by choice. Additionally, Render provides HTTPS by default; the URL is essentially a shared secret in the absence of authentication. Adding API key authentication adds implementation complexity without eliminating the threat (if the key is compromised, data is exposed just as if the URL were).
- **Reason:** For a single-user system where the user controls who knows the Render URL, basic URL obscurity (HTTPS + unguessable path) may be adequate security. Full API key authentication adds ~M effort and ongoing key management overhead for a threat model that may not materialise.
- **Consequence:** If we add auth and then later add multi-user support, the auth mechanism may need to change anyway (moving from API key to OAuth/JWT). Investment now may be wasted.

PO Response (STEP 5.2):
- Rebut: The threat model is not just "someone guesses the URL." Search engines, browser history, referral logs, and sharing of links all represent realistic exposure vectors for a deployed system. "Unguessable URL" is not a security model — it is obscurity. An API key with a single hard-coded value (shared_secret) is an hour of work and provides meaningful protection. The displacement argument (BLG-FE-01) is XS — this is not a capacity concern. Single-user does not mean no security obligation.
- Final outcome: ✅ Advance — to backlog. New backlog item: BLG-SEC-01.

---

**Candidate 9: IDEA-data-model-owner-20260321-01 — Alert History Table**

Required Case (PO):
- Problem: Alert evaluation results are transient — there is no persistence of which rules fired, what values triggered them, or whether a notification was sent. Debugging and auditing the alert system is impossible without history.
- Strategic alignment: §1 (accurate decision support) — history enables users to review alerts that fired while they were away, trust the system's behaviour, and debug misconfigurations.
- If not done: Alert reliability cannot be verified. User cannot see which alerts have fired recently or why.
- Displacement: Capacity freed from 3.5 (data model domain + backend domain).

SPS: **1** — data model addition, no contact with §13.

Challenger (STEP 5.1):
*Clearance Statement — Cleared: Alert history is a standard audit trail feature. §13.1–§13.3 reviewed; none engaged. Economic: M effort (schema migration + endpoint + frontend history view); within available capacity. BLG-OPS-04 (alert scheduling) should probably be designed in parallel as alert history without scheduling may have limited value if alerts still don't fire automatically — but this is not a veto.*

PO Response (STEP 5.2): ✅ Advance — to backlog. New backlog item: BLG-FEAT-12. Note: PO acknowledges Challenger's observation — BLG-OPS-04 (alert scheduling) and BLG-FEAT-12 (alert history) are best sequenced together in v2.2 planning.

---

### STEP 5 Outcome Summary

| Candidate | Outcome | Destination |
|-----------|---------|-------------|
| IDEA-director-of-quality-20260304-01: Spec-to-Test Traceability Matrix | ✅ Advance | Backlog: BLG-SPEC-T01 |
| IDEA-base44-frontend-20260304-01: Loading State Standardisation | ✅ Advance | Backlog: BLG-FE-02 |
| IDEA-metrics-analytics-20260304-02: Metrics Staleness Indicator | ✅ Advance | Backlog: BLG-FEAT-09 |
| IDEA-head-of-engineering-20260304-02: API Endpoint Performance Baseline | ✅ Advance | Backlog: BLG-OPS-05 (note: see also backlog additions in STEP 4 routing) |
| IDEA-qa-testing-20260304-02: Test Automation Readiness Assessment | ✅ Advance | Backlog: BLG-QA-02 |
| IDEA-product-owner-20260321-01: Alert Threshold Customisation | ✅ Advance | Backlog: BLG-FEAT-10 |
| IDEA-strategy-owner-20260321-01: Strategy Compliance Score | ✅ Advance (scope-constrained) | Backlog: BLG-FEAT-11 |
| IDEA-backend-engineering-20260321-01: API Key Authentication | ✅ Advance | Backlog: BLG-SEC-01 |
| IDEA-data-model-owner-20260321-01: Alert History Table | ✅ Advance | Backlog: BLG-FEAT-12 |

All 9 candidates advanced to STEP 6 scoring.

---

## STEP 6 — Scoring Matrix

**Authority:** Facilitator

| ID | Candidate | Strategic Alignment | Financial Impact | Risk Reduction | Workforce Intensity | Time to Value | Reversibility | SPS | Effort Band |
|----|-----------|---------------------|-----------------|----------------|---------------------|---------------|---------------|-----|-------------|
| BLG-SPEC-T01 | Spec-to-Test Traceability Matrix | High — supports QA quality gate | None direct | Medium — reduces AC gap risk | Low | Short | High | 1 | M |
| BLG-FE-02 | Loading State Standardisation | Medium — UX quality | None | Low | Medium | Medium | High | 2 | M |
| BLG-FEAT-09 | Metrics Staleness Indicator | High — data freshness visibility | None | Medium — reduces stale data risk | Low–Medium | Short | High | 2 | S–M |
| BLG-OPS-05 | API Endpoint Performance Baseline | Medium — operational quality | None | Low–Medium | Low | Medium | High | 1 | S |
| BLG-QA-02 | Test Automation Readiness Assessment | Medium — QA infrastructure scoping | None | Low | Very Low | Short | High | 1 | XS |
| BLG-FEAT-10 | Alert Threshold Customisation | High — extends v2.1 alerts, user value | None | Low | Medium | Short–Medium | High | 3 | M |
| BLG-FEAT-11 | Strategy Compliance Score (display-only) | High — decision support, strategy discipline | None | Medium — visibility into stop discipline | Medium | Medium | Medium | 4 | M–L |
| BLG-SEC-01 | API Key Authentication | High — data security | None | High — protects financial data | Medium | Short | High | 1 | M |
| BLG-FEAT-12 | Alert History Table | High — audit trail for alert system | None | Medium — debuggability | Medium | Medium | Medium | 1 | M |

**Scoring notes:**
- All items are backlog-only promotions. No roadmap-level initiative additions.
- BLG-FEAT-11 has SPS=4 (scope-constrained); scope constraint must appear in backlog AC.
- BLG-SEC-01 highest risk reduction — financial data protection.
- BLG-FEAT-10 and BLG-FEAT-12 are natural complements to v2.1 alerts; best sequenced together.

Write: `claude/scoring/scored_initiatives.md` will be updated in STEP 9.

---

## STEP 7 — Workforce Economics Gate

**Authority:** FinOps & Resource Architect

### Capacity Released

| Initiative | FTE freed | Skills freed | Duration |
|-----------|-----------|--------------|----------|
| 3.5 Alerts & Notifications | ~3–4 sprint-equivalents | Backend (alert/watchlist services), Frontend (React components), QA (notification tests) | Available for v2.2 |

### Capacity Required (new backlog additions)

| Item | FTE estimate | Skill type | Duration estimate |
|------|-------------|------------|-------------------|
| BLG-SPEC-T01 | 0.5–1 sprint | Governance (Head of Specs, DoQ) | 1 sprint |
| BLG-FE-02 | 0.5–1 sprint | Frontend | 1 sprint |
| BLG-FEAT-09 | 0.25–0.5 sprint | Backend/Frontend | <1 sprint |
| BLG-OPS-05 | 0.25 sprint | Backend/Ops | <1 sprint |
| BLG-QA-02 | 0.1 sprint | QA/PMO | <1 sprint |
| BLG-FEAT-10 | 0.5–1 sprint | Backend/Frontend | 1 sprint |
| BLG-FEAT-11 | 1–2 sprints | Backend/Frontend/Strategy spec | 1–2 sprints |
| BLG-SEC-01 | 0.5–1 sprint | Backend (API) | 1 sprint |
| BLG-FEAT-12 | 1–1.5 sprints | Backend (data model) + Frontend | 1–2 sprints |

**Total new backlog additions:** ~4.6–8.6 sprint-equivalents

Freed capacity: ~3–4 sprint-equivalents (from 3.5). The new backlog additions exceed freed capacity from a single completion event — but this is expected because:
1. They are backlog items, not immediate sprint commitments
2. Release planning will select which items fit within v2.2 capacity
3. Not all items will enter v2.2

### Skill-Silo Check (STEP 7.1)

**Governance-heavy items:** BLG-SPEC-T01 (spec documentation), BLG-QA-02 (assessment)
**Execution-heavy items:** BLG-FE-02, BLG-FEAT-09, BLG-OPS-05, BLG-FEAT-10, BLG-FEAT-11, BLG-SEC-01, BLG-FEAT-12

Governance load: ~15–20% of total new additions FTE
→ Below 60% ceiling: No Skill-Silo Alert.
→ Below 20% floor: Borderline — but these are backlog additions awaiting release planning capacity check, not immediate sprint allocation. Product Owner sign-off capacity for v2.2 will be confirmed at release planning time.

FinOps conclusion: Freed capacity is adequate for the highest-priority items (BLG-SEC-01, BLG-FEAT-12, BLG-FEAT-10) plus backlog bug fixes. Full capacity allocation will be determined by the release planning engine.

---

## STEP 8 — Final Rebalance Decision

**Authority:** Product Owner (within all constraints)

### STEP 8.5 — Stateless Write Safety Gate

**Context re-anchored:** Debate prose, hypothetical arguments, and exploratory reasoning discarded. STEP 8 decisions are as follows.

### Roadmap-Level Decisions

**Zero active roadmap initiatives.** All v2.1 items shipped and retired.

No roadmap-level initiatives are being added, replaced, deferred, or killed in this run.

**Rationale:** All 9 advancing candidates are backlog-level improvements and features — none represent a major strategic theme that would justify a new roadmap-level initiative. The v2.2 release theme will be determined by the release planning engine, which now has a richer backlog to draw from. No displacement is required (0 roadmap Adds ≤ 0 Kills ✅).

**Decision:** No-change at roadmap level. Record as DL-011 (no-change + backlog additions).

### Backlog-Level Decisions (9 items promoted)

| Item | Decision | Priority | Notes |
|------|----------|----------|-------|
| BLG-SPEC-T01 — Spec-to-Test Traceability Matrix | ✅ Promote to backlog | P2 | Gate cleared (ST-17 complete) |
| BLG-FE-02 — Loading State Standardisation | ✅ Promote to backlog | P3 | Gate cleared (BLG-TECH-08 shipped) |
| BLG-FEAT-09 — Metrics Staleness Indicator | ✅ Promote to backlog | P2 | Gate cleared (slippage tracking shipped) |
| BLG-OPS-05 — API Endpoint Performance Baseline | ✅ Promote to backlog | P3 | Operational quality item |
| BLG-QA-02 — Test Automation Readiness Assessment | ✅ Promote to backlog | P2 | Scoping prerequisite to BLG-QA-01 |
| BLG-FEAT-10 — Alert Threshold Customisation | ✅ Promote to backlog | P2 | Natural v2.1 extension |
| BLG-FEAT-11 — Strategy Compliance Score (display-only) | ✅ Promote to backlog | P2 | Scope-constrained: display-only, no alerts generated |
| BLG-SEC-01 — API Key Authentication | ✅ Promote to backlog | P1 | Security gap; protects financial data |
| BLG-FEAT-12 — Alert History Table | ✅ Promote to backlog | P2 | Audit trail for alert system; best with BLG-OPS-04 |

**Additional backlog items (STEP 4 direct routing — not via STEP 5 debate):**
- BLG-OPS-06 — Health check endpoint (from IDEA-infra-ops-20260321-01; XS, P3)
- BLG-SEC-02 — CSP headers (from IDEA-cybersecurity-20260321-01; XS, P3)

**Displacement candidate flag:** No existing active initiatives to flag. Gated items (AI-SUM, TECH-IND, MKT-COR) remain as-is. For forward-planning, if a v2.2 roadmap item needs to be added later, the natural displacement candidate would be BLG-FEAT-11 (Strategy Compliance Score) — lowest strategic certainty among new promotions.

### STEP 8.5.B — Write Plan

**Cycle:** 2026-03-21__item-3.5

| File | Action | Reason | Traceability |
|------|--------|--------|--------------|
| `claude/cycles/2026-03-21__item-3.5/run_manifest.md` | create | STEP 1.1 requirement | STEP 1 |
| `claude/cycles/2026-03-21__item-3.5/cycle_record.md` | this file | STEP 2–8 working content | STEP 8.5 |
| `claude/roadmap/current_roadmap.md` | modify | Last Updated date; v2.2 note; remove stale Active section if applicable | Lifecycle compliance |
| `claude/roadmap/initiative_register.md` | modify | Move 3.5, 4.2, CHART-IX from Active to Completed (LL-01-patch-4.3 correction); update Last Updated | STEP 9 lifecycle |
| `claude/roadmap/decision_log.md` | append-only | DL-011: No-change roadmap confirm + backlog additions + completion recorded | STEP 8 decision |
| `claude/backlog/backlog.md` | modify | Add 11 new backlog items; update Last rebalance date | STEP 8 decisions (backlog promotions) |
| `claude/ideas/ideas_register.md` | modify | Update statuses: stale ideas → Parked-cycle-5 (4 items); advancing ideas → Promoted-Added (9) or Promoted-Rejected (0); remaining Submitted → Parked-cycle-1 | STEP 4 dispositions; STEP 8.5.B register row verification |
| `claude/scoring/scored_initiatives.md` | create/modify | STEP 6 scoring output | STEP 6 |
| `claude/roadmap/workforce_capacity.md` | modify | Record freed capacity from 3.5; new backlog FTE estimates | STEP 7 |
| `.claude_current_state.json` | modify | Update rebalance keys | STEP 12 |

**Write Plan Integrity Checks:**
- All files within Section 5 write scope: ✅ Yes
- Every write traceable to STEP 8 decision or lifecycle compliance: ✅ Yes
- No formatting-only edits: ✅ Yes
- Decision log append-only and duplicate-checked: ✅ Yes (DL-001 through DL-010 exist; DL-011 is new)
- Backlog edits are reconciliation-only (no grooming): ✅ Yes (adding promoted items only)
- PoG documents: N/A (no hard gates issued this run)
- Hard gate markings: N/A
- Displacement candidate flags: written to initiative_register.md only — N/A (no new flags; BLG-FEAT-11 note recorded in this cycle_record only as informational)
- Effort bands recorded: ✅ Yes (STEP 6 table)
- Action-now prompt patches: N/A (no action-now patches this cycle)
- Deferred prompt patches: ✅ One carried forward (LL-01-patch-4.3) with named owner (Head of Specs Team) and target (before next `manage roadmap` run)
- Meta-review: Checking in STEP 11.

### STEP 8.6 — Run-Level Disagreement Guardrail

Rule: guardrail passes if ANY of the following is true:
1. At least one candidate was parked or rejected during this run. → ✅ YES — multiple stale ideas were re-parked (4 stale re-parks); many new ideas parked (36).
2. Challenger issued a substantive Type A counter-argument for at least one candidate. → ✅ YES — Challenger issued Type A counter-argument for both IDEA-strategy-owner-20260321-01 (SPS=4, §13 boundary) and IDEA-backend-engineering-20260321-01 (single-user threat model).
3. Single-candidate run: No.

**Guardrail: PASSES.** Both conditions 1 and 2 satisfied. No pivot loop required.
