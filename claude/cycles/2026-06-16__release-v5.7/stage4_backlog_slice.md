**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Published
**Cycle:** 2026-06-16__release-v5.7
**Last Updated:** 2026-06-16

<!-- release-plan-marker: RP:v5.7:2026-06-16__release-v5.7 -->

---

# Sprint Backlog Slice — v5.7

**Theme:** Staging Verification Completion, SI-05 Effectiveness Review & Engineering/Governance Patches

---

## EPIC-01 — Staging Verification & QA Coverage

**Maps to:** S2-01, S2-02
**Owner:** Infrastructure & Operations Owner; Director of Quality
**Sprint:** 1

### ST-01 — BLG-OPS-66: Staging verification — concentration-status p95 after FX cache fix

**Source:** BLG-OPS-66 (v5.6 ST-04 EPIC-02 staging-deferred AC)
**Effort:** XS (<1 hour)
**Type:** Operations / Staging Verification

**Acceptance Criteria:**
- AC-01: GET /portfolio/concentration-status p95 latency re-measured on production after v5.6 deployment
- AC-02: p95 ≤1,000ms confirmed (or further investigation item filed if not met)
- AC-03: Infrastructure & Operations Owner sign-off recorded in QA evidence

---

### ST-02 — BLG-OPS-67: Staging verification — red-flag-journal p95 after schema-once fix

**Source:** BLG-OPS-67 (v5.6 ST-05 EPIC-02 staging-deferred AC)
**Effort:** XS (<1 hour)
**Type:** Operations / Staging Verification

**Acceptance Criteria:**
- AC-01: GET /portfolio/red-flag-journal p95 latency re-measured on production after v5.6 deployment
- AC-02: p95 ≤1,000ms confirmed (or further investigation item filed if not met)
- AC-03: Infrastructure & Operations Owner sign-off recorded in QA evidence

---

### ST-03 — BLG-OPS-68: Staging verification — behavioural-drift p95 + cache hit rate

**Source:** BLG-OPS-68 (v5.6 ST-06 EPIC-02 staging-deferred AC)
**Effort:** XS (<1 hour)
**Type:** Operations / Staging Verification

**Acceptance Criteria:**
- AC-01: GET /analytics/behavioural-drift p95 latency re-measured on production after v5.6 deployment
- AC-02: p95 ≤1,000ms for cached calls confirmed
- AC-03: Cache hit rate ≥50% under typical usage confirmed (check logs: `[research_cache] HIT/MISS`)
- AC-04: Infrastructure & Operations Owner sign-off recorded in QA evidence

---

### ST-04 — BLG-OPS-69: Staging verification — research view p95 + cache hit rate

**Source:** BLG-OPS-69 (v5.6 ST-07 EPIC-02 staging-deferred AC)
**Effort:** S (~0.5 day)
**Type:** Operations / Staging Verification

**Acceptance Criteria:**
- AC-01: GET /research/{ticker} p95 latency ≤2,000ms for cached tickers on production
- AC-02: Cache hit rate ≥50% under typical usage (check `[research_cache] HIT/MISS` log output)
- AC-03: Cache invalidation on screener run confirmed (run screener, verify subsequent research request is a MISS)
- AC-04: Infrastructure & Operations Owner sign-off recorded in QA evidence

---

### ST-05 — BLG-FE-75: Staging verification — SI-05 deep links navigate on mobile Telegram

**Source:** BLG-FE-75 (v5.6 ST-01 EPIC-01 AC-02 staging-deferred; Provisional-Target: v5.7)
**Effort:** XS (<1 hour)
**Type:** QA / Staging Verification

**Acceptance Criteria:**
- AC-01: SI-05 weekly Telegram digest opened on a mobile device
- AC-02: Risk Dashboard deep link navigates to `/RiskDashboard` on mobile Telegram — no broken link or navigation error
- AC-03: Red Flag Journal deep link navigates to `/RedFlagJournal` on mobile Telegram — no broken link or navigation error
- AC-04: Staging run date recorded in QA evidence
- AC-05 [staging-only evidence]: Head of UX & Design sign-off confirming mobile navigation test performed

---

### ST-06 — BLG-QA-56: SI-01 all-pass state Playwright scenario

**Source:** BLG-QA-56 (GAP-ARC5-01 — v5.6 Arc 5 coverage assessment ST-10)
**Effort:** XS (<1 hour)
**Type:** QA / Test Coverage

**Acceptance Criteria:**
- AC-01: SC-SI-01d added to `tests/e2e/si01-si03-integration.spec.js`: mock all 5 validation checks as passing; assert success state visible in PreEntryValidationPanel and override checkbox absent
- AC-02: Test passes in CI (green)
- AC-03: QA Lead sign-off

---

### ST-07 — BLG-QA-57: SI-03 Red Flag Journal pagination Playwright scenario

**Source:** BLG-QA-57 (GAP-ARC5-02 — v5.6 Arc 5 coverage assessment ST-10)
**Effort:** XS (<1 hour)
**Type:** QA / Test Coverage

**Acceptance Criteria:**
- AC-01: SC-RFJ-04 added to `tests/e2e/red-flag-journal.spec.js`: mock payload with events > page size; assert load-more trigger renders; assert additional events appear after trigger
- AC-02: Test passes in CI (green)
- AC-03: QA Lead sign-off

---

### ST-08 — BLG-QA-58: Arc 5 compliance score trend Playwright scenario

**Source:** BLG-QA-58 (GAP-ARC5-03 — v5.6 Arc 5 coverage assessment ST-10)
**Effort:** XS (<1 hour)
**Type:** QA / Test Coverage

**Acceptance Criteria:**
- AC-01: SC-ARC5-05 added to `tests/e2e/arc5-compliance-section.spec.js`: mock payload with known compliance score metric values; assert formatted percentage value visible in Arc5ComplianceSection
- AC-02: Test passes in CI (green)
- AC-03: QA Lead sign-off

---

## EPIC-02 — Governance & Engineering Patches

**Maps to:** S2-03
**Owner:** Head of Specs Team; Head of Backend Engineering
**Sprint:** 1

### ST-09 — BLG-FE-64: RFJ design review pre-brief [CONDITIONAL — gate 2026-06-21]

**Source:** BLG-FE-64 (carry-forward LL-v5.6-DV-02; perennial-return item — 3rd consecutive return)
**Effort:** XS (~0.5 day)
**Type:** Frontend / UX Pre-work
**Status at sprint open: conditional — gate 2026-06-21**

**Gate:** SI-03 Red Flag Journal live ≥ 30 days (gate clears 2026-06-21). Sprint planning must confirm gate cleared before this story proceeds. If sprint closes before 2026-06-21: return to backlog (4th deferral; PO re-disposition required at v5.8).

**Acceptance Criteria:**
- AC-01: Design review brief produced for BLG-FE-41 covering: review scope (filter UX, severity visual hierarchy, event type colour coding, timeline vs list layout), evaluation criteria, expected deliverable format
- AC-02: Brief reviewed by Head of UX & Design; sign-off recorded
- AC-03: Brief filed and accessible before BLG-FE-41 sprint planning
- AC-04: Gate 2026-06-21 confirmed cleared before story commences

---

### ST-10 — Lazy-import pattern documentation in backend engineering patterns guide

**Source:** LL-v5.6-EX-03 carry-forward (new item — no prior BLG ID; assigned BLG-BE-36)
**BLG ID:** BLG-BE-36 (new)
**Effort:** S (~1 hour)
**Type:** Backend Engineering / Documentation

**Context:** v5.6 sprint execution (LL-v5.6-EX-03) identified a canonical pattern for cross-router imports: using lazy imports inside functions rather than module-level imports to avoid circular dependency issues. This pattern should be documented as the standard approach.

**Acceptance Criteria:**
- AC-01: Backend engineering patterns guide (`docs/specs/` or `docs/engineering/`) updated with a section documenting the lazy-import pattern for cross-router hooks: when to use it, example code snippet, why module-level imports fail in this context
- AC-02: Document reviewed by Head of Backend Engineering; sign-off recorded
- AC-03: Pattern documentation is findable from the relevant router files (either via link in CLAUDE.md, a comment in an example file, or a README in the relevant directory)

---

### ST-11 — Confirm dual sign-off pattern documented in execution_prompt.md

**Source:** LL-v5.6-DV-03 carry-forward (new item — governance patch verification)
**BLG ID:** BLG-GOV-123 (new)
**Effort:** S (~0.5 hour)
**Type:** Governance / Verification

**Context:** LL-v5.6-DV-03 raised confirming that the dual sign-off pattern (Infrastructure & Operations Owner + Director of Quality co-sign) is documented in execution_prompt.md as a recognised format for infrastructure EPICs. AUD-2026-06-16-002 (execution_prompt.md v3.42) already added this — this story verifies the documentation is clear and accessible, and confirms the carry-forward is closed.

**Acceptance Criteria:**
- AC-01: execution_prompt.md §5.3 (Agent-Mediated Sign-Off section) reviewed and confirmed to contain Infrastructure co-sign class documentation (from v3.42 AUD-2026-06-16-002 patch)
- AC-02: If §5.3 wording is clear and sufficient: Head of Specs Team confirms LL-v5.6-DV-03 closed; record in QA evidence
- AC-03: If §5.3 wording is unclear or missing: minor patch applied (version bump, change log entry per CLAUDE.md §6); Head of Specs Team sign-off
- AC-04: lessons_learnt_closure.md carry-forward LL-v5.6-DV-03 status updated to Resolved in sprint_close.md

---

## EPIC-03 — SI-05 Effectiveness Review & Post-Deploy Metrics [CONDITIONAL SPRINT 2 — gate 2026-07-04]

**Maps to:** S2-04
**Owner:** Product Owner; Infrastructure & Operations Owner; Metrics Definitions & Analytics Owner
**Sprint:** 2 (conditional — gate: SI-05 Phase 1 effectiveness review complete, 2026-07-04)

**Gate condition:** All 3 stories below require the 2026-07-04 SI-05 effectiveness review completion. If gate not confirmed cleared at Sprint 2 planning: entire EPIC-03 deferred to v5.8.

### ST-12 — BLG-GOV-112: SI-05 digest weekly cadence review

**Source:** BLG-GOV-112 (gate date 2026-07-04; returned from v5.5 ST-13)
**Effort:** S (~0.5 day)
**Type:** Governance / Product Review
**Status at sprint open: conditional — gate 2026-07-04**

**Acceptance Criteria:**
- AC-01: After 2026-07-04 effectiveness review: assess weekly cadence appropriateness from si05_digest_log data
- AC-02: Cadence recommendation document produced: maintain weekly / move to bi-weekly / adaptive cadence
- AC-03: Data backing documented (delivery count, any user feedback, observable action rate)
- AC-04: Product Owner sign-off
- AC-05: Gate 2026-07-04 confirmed cleared before story commences

---

### ST-13 — BLG-GOV-115: SI-05 actionability metric definition

**Source:** BLG-GOV-115 (gate date 2026-07-04; returned from v5.5 ST-14)
**Effort:** S (~0.5 day)
**Type:** Governance / Metrics
**Status at sprint open: conditional — gate 2026-07-04**

**Acceptance Criteria:**
- AC-01: 2–4 actionability metrics formally defined for SI-05 digest effectiveness
- AC-02: Each metric has a data source mapping (si05_digest_log, red_flag_events, trade data)
- AC-03: Metrics document produced and reviewed by Metrics Definitions & Analytics Owner
- AC-04: Metrics feed into BLG-GOV-112 cadence review and BLG-GOV-96 effectiveness criteria
- AC-05: Gate 2026-07-04 (BLG-GOV-113 effectiveness review protocol complete) confirmed cleared

---

### ST-14 — BLG-OPS-59: SI-05 service production p99 latency baseline review

**Source:** BLG-OPS-59 (gate: ≥4 weeks production operation ~2026-07-04; returned from v5.5 ST-12)
**Effort:** S (~0.5 day)
**Type:** Operations / Performance
**Status at sprint open: conditional — gate 2026-07-04**

**Acceptance Criteria:**
- AC-01: POST /digest/si05/send p99 latency extracted from Render logs (≥4 weeks post v5.1 ship 2026-06-04)
- AC-02: p99 compared against BLG-OPS-54 pre-launch baseline
- AC-03: If p99 > 2× baseline: performance investigation item filed; otherwise record PASS
- AC-04: Findings documented in a brief performance review note
- AC-05: Infrastructure & Operations Owner sign-off
- AC-06: Gate (≥4 weeks production operation, ≥2026-07-04) confirmed before commencing

---

## Story Count Summary

| Sprint | EPIC | Stories | Firm | Conditional |
|--------|------|---------|------|-------------|
| Sprint 1 | EPIC-01 | ST-01 to ST-08 | 8 | 0 |
| Sprint 1 | EPIC-02 | ST-09 to ST-11 | 2 | 1 (ST-09, gate 2026-06-21) |
| Sprint 2 | EPIC-03 | ST-12 to ST-14 | 0 | 3 (gate 2026-07-04) |
| **Total** | | **14** | **10** | **4** |
