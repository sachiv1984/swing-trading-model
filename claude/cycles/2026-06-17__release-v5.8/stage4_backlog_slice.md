**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Published
**Cycle:** 2026-06-17__release-v5.8
**Release:** v5.8
**Published:** 2026-06-17

---

# Stage 4 Backlog Slice — v5.8

**Theme:** RFJ UX Design Completion, SI-05 Effectiveness Review & Production Hardening

---

## EPIC-01 — RFJ UX Design, Production Ops & Governance Assessment

**Maps to:** S2-01, S2-02, S2-03, S2-04
**Owner:** Head of UX & Design; PMO Lead; Infrastructure & Operations Owner
**Sprint:** 1

---

### ST-01 — BLG-FE-64: RFJ design review pre-brief

**Source backlog item:** BLG-FE-64
**Priority:** P2
**Effort:** XS (~0.5 day)
**Sprint:** 1
**Conditional:** No (gate 2026-06-21 — time-certain by sprint start)

**Context:** BLG-FE-64 has been returned 4 consecutive cycles due to the gate date (SI-03 live ≥30 days from 2026-05-22 = 2026-06-21) not being reached at sprint close. Gate is now time-certain and clears within the sprint planning window. PO has provided active re-disposition: advance as firm story.

**Scope:**
- Produce a design review brief for BLG-FE-41 (the actual Red Flag Journal visual design review)
- Brief defines: review scope (which aspects of RedFlagJournal.js are in scope), evaluation criteria, and expected deliverable
- Brief reviewed and signed off by Head of UX & Design before BLG-FE-41 begins

**Acceptance Criteria:**
- AC-01: Design review brief document produced (Markdown, filed in docs/product/ux/ or equivalent)
- AC-02: Brief covers: scope definition (filters UX, severity visual hierarchy, event type colour coding, timeline vs list layout), evaluation criteria, and deliverable format
- AC-03: Head of UX & Design sign-off on brief scope recorded
- AC-04: Brief completed ≥ gate date 2026-06-21 (SI-03 live 30 days)

**DoQ evidence:** Head of UX & Design sign-off on brief. No staging or Playwright required (documentation deliverable).

---

### ST-02 — BLG-FE-41: Red Flag Journal visual design review

**Source backlog item:** BLG-FE-41
**Priority:** P3
**Effort:** M (~1–2 days design + spec)
**Sprint:** 1
**Conditional:** No (gate 2026-06-21 — same as ST-01)
**Depends on:** ST-01 (pre-brief scopes this review)

**Context:** SI-03 Red Flag Journal shipped v3.9 (2026-05-22). After 30 days (gate 2026-06-21), the design review assesses visual hierarchy, timeline layout, and colour coding for severity and rule breach types. ST-01 pre-brief defines the scope for this review.

**Scope:**
- Review existing RedFlagJournal.js design patterns: severity visual hierarchy, event type colour coding, timeline vs list layout evaluation
- Evaluate against current application design system
- Produce design recommendation document with rationale
- If redesign recommended: produce UX spec and file implementation backlog item
- Review against existing application design language

**Acceptance Criteria:**
- AC-01: Design recommendation document produced (one of: maintain current, redesign to pattern X)
- AC-02: Rationale covers: severity hierarchy, event type colour coding, timeline vs list layout options
- AC-03: If redesign recommended: UX spec produced and implementation backlog item filed
- AC-04: Head of UX & Design sign-off recorded
- AC-05: Completed after gate date 2026-06-21

**DoQ evidence:** Head of UX & Design sign-off on recommendation. No staging or Playwright required (design review deliverable).

---

### ST-03 — FRONTEND_URL production env var configuration

**Source backlog item:** v5.7 post-ship OA (Infrastructure & Operations Owner; Deadline: v5.8 sprint 1)
**Priority:** P1 (OA from prior cycle)
**Effort:** XS (~1–2 hours)
**Sprint:** 1
**Conditional:** No

**Context:** v5.7 delivery verification found that deep links in SI-05 Telegram digests were absent in production because FRONTEND_URL is not set on the production backend (trading-assistant-api-c0f9.onrender.com). ST-05 (BLG-FE-75) confirmed mobile Telegram deep links work when FRONTEND_URL is set correctly (staging verification passed). Production needs the same env var.

**Scope:**
- Set FRONTEND_URL environment variable on production backend (Render dashboard: trading-assistant-api-c0f9.onrender.com)
- Value: production frontend URL
- Confirm SI-05 digest deep links work in next scheduled digest delivery
- Document env var addition in deployment runbook (or equivalent ops notes)

**Acceptance Criteria:**
- AC-01: FRONTEND_URL set on production backend service in Render dashboard
- AC-02: Deployment runbook or ops notes updated to include FRONTEND_URL as a required env var
- AC-03: Infrastructure & Operations Owner sign-off recorded
- AC-04: (Staging-only) Deep links confirmed working in next SI-05 digest delivery post-deploy

**DoQ evidence:** Infrastructure & Operations Owner sign-off. Env var confirmation screenshot or Render log confirmation.

---

### ST-04 — BLG-GOV-101: Governance model complexity assessment

**Source backlog item:** BLG-GOV-101
**Priority:** P2
**Effort:** M (~2 days)
**Sprint:** 1
**Conditional:** No (gate met: 0 open audit items post-AUD-2026-06-16; score 72 provides evidence trigger)

**Context:** BLG-GOV-101 was filed after AUD-2026-06-02 scored 73 (decline from 79) with 5 open items (BLG-GOV-79–83). AUD-2026-06-16 scored 72 with 0 open items. The trigger condition is met: open items resolved, score still below 78. The hypothesis test phase can now proceed: is complexity a contributing factor to the score decline, or were BLG-GOV-79–83 the full explanation?

**Scope:**
- Review audit score context: are the resolved items (BLG-GOV-79–83) the full explanation or is there residual structural complexity?
- Per-engine step count analysis: count steps, hard gates, write operations for each governance prompt
- Identify: steps that consistently produce no output, gates that have never fired in 10+ cycles, longest prompts vs usage frequency
- Hypothesis test: given 0 open items but score still at 72, determine if complexity is a contributing factor
- Output: complexity assessment report with finding: "complexity NOT root cause" or "complexity IS a contributing factor with simplification candidates"

**Acceptance Criteria:**
- AC-01: Complexity assessment report produced covering all 6 governance phase engines
- AC-02: Per-engine step count and complexity indicators documented
- AC-03: Hypothesis test outcome stated: complexity is/is not a root cause
- AC-04: If complexity IS a factor: simplification candidates enumerated with rationale and filed as backlog items
- AC-05: Director of HR, PMO Lead, and Head of Specs Team sign-off

**DoQ evidence:** Sign-off from Director of HR, PMO Lead, and Head of Specs Team. Assessment document filed in claude/ or docs/governance/.

---

## EPIC-02 — SI-05 Effectiveness Review

**Maps to:** S2-05, S2-06, S2-07
**Owner:** Product Owner; Infrastructure & Operations Owner; Metrics Definitions & Analytics Owner
**Sprint:** 2
**Conditional:** Yes — entire EPIC gated on SI-05 Phase 1 first effectiveness review (BLG-GOV-113) completing by 2026-07-04

**Gate check required at Sprint 2 planning:** SI-05 Phase 1 effectiveness review (BLG-GOV-113) must be complete by 2026-07-04. If not cleared: defer all 3 stories to backlog and close Sprint 2 as gate-deferred.

---

### ST-05 — BLG-GOV-112: SI-05 digest weekly cadence review

**Source backlog item:** BLG-GOV-112
**Priority:** P2
**Effort:** S (~0.5 day)
**Sprint:** 2
**Conditional:** Yes — gate 2026-07-04 (SI-05 Phase 1 effectiveness review complete)

**Sprint history:** Returned from v5.5 (gate 2026-07-04 not met), v5.7 (same gate). Not eligible before 2026-07-04.

**Scope:**
- After 2026-07-04 effectiveness review: assess weekly cadence appropriateness for SI-05 digest
- Review si05_digest_log delivery count, user engagement signals, whether digest content is acted upon
- Produce cadence recommendation: maintain weekly / move to bi-weekly / introduce adaptive cadence
- Product Owner sign-off

**Acceptance Criteria:**
- AC-01: Cadence review document produced after 2026-07-04 effectiveness review
- AC-02: Review covers: delivery count, action signals (indirect: red_flag_journal views post-delivery), user feedback
- AC-03: Recommendation made (maintain / change cadence) with data backing
- AC-04: Product Owner sign-off
- AC-05: Gate condition verified: BLG-GOV-113 complete

**DoQ evidence:** Product Owner sign-off. Cadence recommendation document filed.

---

### ST-06 — BLG-GOV-115: SI-05 digest actionability metric definition

**Source backlog item:** BLG-GOV-115
**Priority:** P2
**Effort:** S (~0.5–1 day)
**Sprint:** 2
**Conditional:** Yes — gate 2026-07-04

**Sprint history:** Returned from v5.5 (gate not met), v5.7 (gate not met). Not eligible before 2026-07-04.

**Scope:**
- After 2026-07-04 effectiveness review: define 2–4 actionability metrics for SI-05 digest
- Metrics must be measurable from existing data sources (si05_digest_log, red_flag_events, trade data)
- Produce metrics definition document for Metrics Definitions & Analytics Owner review
- Metrics feed BLG-GOV-112 cadence review and BLG-GOV-96 effectiveness criteria

**Acceptance Criteria:**
- AC-01: 2–4 actionability metrics formally defined with data source mapping
- AC-02: Metrics document reviewed and signed off by Metrics Definitions & Analytics Owner
- AC-03: Each metric specifies: name, definition, data source query, expected range
- AC-04: Gate condition verified: BLG-GOV-113 complete (2026-07-04)
- AC-05: Metrics added to relevant section of metrics_definitions.md

**DoQ evidence:** Metrics Definitions & Analytics Owner sign-off. Metrics document filed.

---

### ST-07 — BLG-OPS-59: SI-05 service production p99 latency baseline review

**Source backlog item:** BLG-OPS-59
**Priority:** P2
**Effort:** S (~0.5 day)
**Sprint:** 2
**Conditional:** Yes — gate 2026-07-04 (≥4 weeks of POST /digest/si05/send production operation)

**Sprint history:** Returned from v5.5 (gate 2026-07-04 not met), v5.7 (same gate). Not eligible before 2026-07-04.

**Scope:**
- After 4 weeks of production operation (≥2026-07-04): extract p99 latency from Render logs for POST /digest/si05/send
- Compare against BLG-OPS-54 pre-launch baseline
- If p99 > 2× baseline: file a performance investigation item; otherwise record PASS
- Document findings in brief perf review note

**Acceptance Criteria:**
- AC-01: Post-4-week p99 latency extracted from Render logs and documented
- AC-02: Comparison against BLG-OPS-54 pre-launch baseline made
- AC-03: Performance PASS determination recorded OR investigation item filed
- AC-04: Infrastructure & Operations Owner sign-off recorded
- AC-05: Gate condition verified: ≥2026-07-04

**DoQ evidence:** Infrastructure & Operations Owner sign-off. Performance review note filed.
