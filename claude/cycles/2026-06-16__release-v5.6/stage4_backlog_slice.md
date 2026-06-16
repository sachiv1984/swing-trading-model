**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Published
**Cycle:** 2026-06-16__release-v5.6
**Published:** 2026-06-16

---

# Backlog Slice — v5.6

<!-- release-plan-marker: RP:v5.6:2026-06-16__release-v5.6 -->

**Theme:** Research Performance, SI-05 UX Improvements & Backlog Clearance

---

## EPIC-01 — SI-05 UX & Digest Improvements

**Maps to:** S2-01, S2-02, S2-11
**Owner:** Head of Backend Engineering; Head of UX & Design
**Sequencing:** Sprint 1. S2-11 conditional on gate 2026-06-21.

### ST-01 — BLG-FE-73: Add deep links from SI-05 digest to relevant app screens

**Source:** S2-01 | BLG-FE-73
**Priority:** P2
**Effort:** S (~0.5 day)
**Owner:** Head of Backend Engineering; Head of UX & Design
**Delivery class:** autonomous

**Description:**
The SI-05 weekly Telegram digest contains no links to the app. Users reading the digest must manually navigate to relevant screens (minimum 3 steps). Add deep links per digest section to the relevant app screen, using the app's public URL with correct hash/route.

**Acceptance Criteria:**
- AC-01: At least one deep link present in the SI-05 digest pointing to a relevant app screen (e.g. Risk Dashboard, Red Flag Journal)
- AC-02: Link navigates correctly on mobile Telegram (where most users read the digest)
- AC-03: No regression to existing digest delivery or content
- AC-04: Head of UX & Design sign-off on link placement and target screens

---

### ST-02 — BLG-FE-74: Clarify N/A pass rate reason in SI-05 digest message

**Source:** S2-02 | BLG-FE-74
**Priority:** P3
**Effort:** XS (<1 hour)
**Owner:** Head of Backend Engineering
**Delivery class:** autonomous

**Description:**
When pass rate and override rate show "N/A" in the digest, the user cannot determine if this is expected (no trades triggered validation this week) or a system issue. Update `_integrity_summary_line` in `si05_digest_service.py` to include the reason for N/A.

**Acceptance Criteria:**
- AC-01: N/A values in the digest include a parenthetical reason (e.g. "N/A (no validation events this week)")
- AC-02: "No events" and "data unavailable" produce distinct messages
- AC-03: No regression to existing digest delivery

---

### ST-03 — BLG-FE-64: RFJ visual design review pre-brief [CONDITIONAL — gate 2026-06-21]

**Source:** S2-11 | BLG-FE-64
**Priority:** P2
**Effort:** S (~0.5 day)
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Delivery class:** autonomous
**Status at sprint open: conditional — gate 2026-06-21**

**Gate:** SI-03 Red Flag Journal live ≥30 days — clears 2026-06-21. Sprint planning must confirm gate cleared before assigning this story.

**Description:**
Produce a design review brief for BLG-FE-41 (Red Flag Journal visual design review). Brief defines: scope (which aspects of RedFlagJournal.js are in scope for visual review), evaluation criteria, and deliverables. Input to BLG-FE-41 sprint planning when gate clears.

**Acceptance Criteria:**
- AC-01: Design review brief produced covering: scope definition, evaluation criteria, deliverable format
- AC-02: Brief distinguishes visual design review (BLG-FE-64) from UX/interaction review (BLG-FE-66)
- AC-03: Head of UX & Design sign-off on brief scope
- AC-04: Gate condition confirmed cleared (SI-03 live ≥30 days = 2026-06-21) before story proceeds

---

## EPIC-02 — Performance & Latency Hardening

**Maps to:** S2-03, S2-04, S2-05, S2-06
**Owner:** Infrastructure & Operations Owner; Head of Backend Engineering
**Sequencing:** Sprint 1 (investigations S2-04/05/06) + Sprint 2 (S2-03 caching). Investigations should precede caching implementation.

### ST-04 — BLG-OPS-62: Investigate GET /portfolio/concentration-status high latency

**Source:** S2-04 | BLG-OPS-62
**Priority:** P3
**Effort:** S (~0.5 day)
**Owner:** Infrastructure & Operations Owner
**Delivery class:** autonomous

**Description:**
GET /portfolio/concentration-status measured p50=3,985ms, p95=5,917ms on production — highest-latency DB endpoint in the baseline. Profile the SQL query, identify missing indexes or unoptimised joins, and apply fix.

**Acceptance Criteria:**
- AC-01: SQL query profiled; root cause identified (missing index, full scan, or other)
- AC-02: Fix applied (index, materialised view, or query restructure as appropriate)
- AC-03: p95 latency reduced to ≤1,000ms on production (re-measured after fix)
- AC-04: Infrastructure & Operations Owner sign-off after re-measurement

---

### ST-05 — BLG-OPS-63: Investigate GET /portfolio/red-flag-journal high latency

**Source:** S2-05 | BLG-OPS-63
**Priority:** P3
**Effort:** S (~0.5 day)
**Owner:** Infrastructure & Operations Owner
**Delivery class:** autonomous

**Description:**
GET /portfolio/red-flag-journal measured p50=3,005ms, p95=3,200ms — consistent ~3s indicating a structural query issue. Profile and fix.

**Acceptance Criteria:**
- AC-01: SQL query profiled; root cause identified
- AC-02: Fix applied (index or result caching)
- AC-03: p95 latency reduced to ≤1,000ms on production
- AC-04: Infrastructure & Operations Owner sign-off after re-measurement

---

### ST-06 — BLG-OPS-64: Investigate GET /analytics/behavioural-drift high latency

**Source:** S2-06 | BLG-OPS-64
**Priority:** P3
**Effort:** S (~0.5 day)
**Owner:** Infrastructure & Operations Owner
**Delivery class:** autonomous

**Description:**
GET /analytics/behavioural-drift measured p50=3,293ms, p95=3,798ms. Implement TTL-based result caching (15–30 min) to reduce repeated full-history scans.

**Acceptance Criteria:**
- AC-01: Underlying query profiled; caching approach confirmed appropriate
- AC-02: TTL-based result cache implemented (in-memory or Redis, 15–30 min TTL)
- AC-03: p95 latency reduced to ≤1,000ms for cached calls
- AC-04: Cache hit rate ≥50% under typical usage
- AC-05: Infrastructure & Operations Owner sign-off after re-measurement

---

### ST-07 — BLG-OPS-22: Research data caching layer

**Source:** S2-03 | BLG-OPS-22
**Priority:** P2
**Effort:** M (~2–3 days)
**Owner:** Infrastructure & Operations Owner; Head of Backend Engineering
**Delivery class:** autonomous

**Description:**
Research view loads require multiple sequential external API calls (YF OHLCV, earnings, news). Gate cleared 2026-06-11: p95=4,601ms > 3,000ms threshold confirmed on production. Implement TTL-based cache (Redis or in-memory, 15-minute TTL) per-ticker, with cache invalidation on screener run.

**Acceptance Criteria:**
- AC-01: TTL-based cache implemented (Redis or in-memory): research data per ticker, 15-minute TTL
- AC-02: Cache invalidation triggered on screener run
- AC-03: Cache hit/miss logging added
- AC-04: Research view p95 latency reduced to ≤2,000ms for cached tickers
- AC-05: Cache hit rate ≥50% in typical usage
- AC-06: Gate condition (BLG-OPS-13 + p95 > 3,000ms) verified and documented in QA evidence

---

## EPIC-03 — QA & Gate Governance

**Maps to:** S2-07, S2-08, S2-09, S2-10
**Owner:** PMO Lead; Director of Quality; FinOps & Resource Architect
**Sequencing:** Sprint 1, first. ST-08 (P1 gate check) must run early.

### ST-08 — BLG-GOV-106: PT-04 trade count gate re-verification

**Source:** S2-07 | BLG-GOV-106
**Priority:** P1
**Effort:** S (~0.5 hour)
**Owner:** PMO Lead; Product Owner
**Delivery class:** autonomous

**Description:**
PT-04 gate requires 20+ closed trades (pnl IS NOT NULL in trade_history). Last formal count: 6 trades at v4.6 audit (2026-05-31). Query the current count and update PT-04 gate status in current_roadmap.md and BLG-FEAT-25.

**Acceptance Criteria:**
- AC-01: Query executed: `SELECT COUNT(*) FROM trade_history WHERE pnl IS NOT NULL`
- AC-02: Current count recorded in evidence
- AC-03: PT-04 gate status updated in current_roadmap.md Arc 2 section (PT-04 row) with new count and date
- AC-04: BLG-FEAT-25 Provisional-Target updated if gate cleared (≥20 trades)
- AC-05: PMO Lead and Product Owner sign-off on gate status

---

### ST-09 — BLG-QA-45: Arc 5 QA completion criteria definition

**Source:** S2-08 | BLG-QA-45
**Priority:** P2
**Effort:** S (~0.5–1 day)
**Owner:** Director of Quality; QA Lead
**Delivery class:** autonomous

**Description:**
BLG-QA-26 (Arc 5 E2E QA protocol) gates on "all five Arc 5 features shipped" but "fully complete" is undefined. Define canonical "Arc 5 fully complete" criteria; confirm with Product Owner and Head of Specs Team whether SI-05 Phase 2 counts separately.

**Acceptance Criteria:**
- AC-01: Arc 5 completion criteria explicitly defined: explicit list of what must be shipped for BLG-QA-26 to trigger
- AC-02: Criteria resolve the ambiguity around SI-05 Phase 2 and SI-02 frontend (separate or included)
- AC-03: BLG-QA-26 gate condition field updated with explicit criteria list
- AC-04: Product Owner and Director of Quality sign-off

---

### ST-10 — BLG-QA-49: Arc 5 test scenario completeness assessment

**Source:** S2-09 | BLG-QA-49
**Priority:** P2
**Effort:** S-M (~0.5–1 day)
**Owner:** QA Lead; Director of Quality
**Delivery class:** autonomous

**Description:**
With SI-01, SI-03, and SI-05 Phase 1 shipped (3 of 5 Arc 5 features), produce an intermediate test scenario completeness assessment: enumerate all Playwright tests covering Arc 5 features, map to ACs, identify top-3 coverage gaps.

**Acceptance Criteria:**
- AC-01: Arc 5 Playwright test coverage map produced: feature × AC × test scenario table
- AC-02: Coverage map covers SI-01 (PreEntryValidationPanel), SI-03 (RedFlagJournal.js), SI-05 (allocation_insufficient badge)
- AC-03: Top-3 coverage gaps identified with proposed remediation paths
- AC-04: Director of Quality sign-off on coverage assessment document

---

### ST-11 — BLG-OPS-65: Anthropic API cost 14-cycle trend analysis

**Source:** S2-10 | BLG-OPS-65
**Priority:** P3
**Effort:** S (~0.5–1 day)
**Owner:** FinOps & Resource Architect
**Delivery class:** autonomous

**Description:**
After 14+ production cycles of Claude API usage (generate-thesis, check-daily-cost), produce a trend analysis: per-cycle Claude API call counts and estimated costs (v4.4–v5.5). Assess trajectory against the $5/month upgrade threshold defined in BLG-OPS-37.

**Acceptance Criteria:**
- AC-01: Trend analysis document produced covering cycles v4.4–v5.5 (14 cycles)
- AC-02: Per-cycle cost estimated from claude_audit_log (call counts × model pricing)
- AC-03: Cost trajectory assessed against BLG-OPS-37 $5/month upgrade threshold
- AC-04: FinOps & Resource Architect sign-off; next review date recorded

---

## Sprint Assignment

| ST | EPIC | Item | Priority | Effort | Sprint |
|----|------|------|----------|--------|--------|
| ST-08 | EPIC-03 | BLG-GOV-106: PT-04 gate re-verification | P1 | S | Sprint 1 |
| ST-09 | EPIC-03 | BLG-QA-45: Arc 5 QA completion criteria | P2 | S | Sprint 1 |
| ST-10 | EPIC-03 | BLG-QA-49: Arc 5 test scenario completeness | P2 | S-M | Sprint 1 |
| ST-11 | EPIC-03 | BLG-OPS-65: Anthropic API cost trend | P3 | S | Sprint 1 |
| ST-01 | EPIC-01 | BLG-FE-73: SI-05 deep links | P2 | S | Sprint 1 |
| ST-02 | EPIC-01 | BLG-FE-74: N/A pass rate clarification | P3 | XS | Sprint 1 |
| ST-03 | EPIC-01 | BLG-FE-64: RFJ design review pre-brief [CONDITIONAL gate 2026-06-21] | P2 | S | Sprint 1 (if gate clears) |
| ST-04 | EPIC-02 | BLG-OPS-62: Concentration-status latency | P3 | S | Sprint 2 |
| ST-05 | EPIC-02 | BLG-OPS-63: Red-flag-journal latency | P3 | S | Sprint 2 |
| ST-06 | EPIC-02 | BLG-OPS-64: Behavioural-drift latency | P3 | S | Sprint 2 |
| ST-07 | EPIC-02 | BLG-OPS-22: Research data caching layer | P2 | M | Sprint 2 |

**Sprint 1: 7 firm stories (ST-01/02/08/09/10/11) + 1 conditional (ST-03)**
**Sprint 2: 4 stories (ST-04/05/06/07) — performance investigations + caching**

Applying LL-P3-03-v55: Sprint 2 EPIC-02 stories are P2/P3 and standalone. If Sprint 2 cannot execute, these items return to backlog without blocking the release.
