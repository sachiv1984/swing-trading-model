**Owner:** Head of Specs Team
**Class:** Planning Record (Class 3)
**Status:** Published
**Version:** 1.0
**Cycle:** 2026-06-09__release-v5.4
**Last Updated:** 2026-06-09

---

# Stage 4 Backlog Slice — v5.4

<!-- release-plan-marker: RP:v5.4:2026-06-09__release-v5.4 -->

**Release:** v5.4 — Ops Monitoring, UX Debt Clearance & Governance Patches
**Firm stories:** 4 (Sprint 1)
**Conditional stories:** 3 (Sprint 2, gate ≥2026-07-04)
**Total:** 7

---

## EPIC-01 — Ops Monitoring & Performance Baseline

Maps to: S2-01, S2-05

**Description:** Follow-through on v5.3 endpoint coverage drift and SI-05 production performance monitoring. Ensures new endpoints are baselined and SI-05 production p99 latency is validated against pre-launch benchmarks.

---

### ST-01 — Add v5.3 new endpoints to api_performance_baseline.md

**EPIC:** EPIC-01
**Backlog ref:** BLG-OPS-60
**Sprint:** 1
**Effort:** S (~0.5 day)
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Gate:** None

**Problem**
v5.3 shipped 5 new endpoints that appear in openapi.yaml but are absent from api_performance_baseline.md: `GET /ai/journal-summary/history`, `GET /news/{ticker}`, `GET /watchlist`, `POST /watchlist`, `DELETE /watchlist/{entry_id}`. Without baseline entries, performance regressions on these endpoints will go undetected.

**Scope**
- Run performance baseline measurements for all 5 missing endpoints against a live environment
- Add measurement rows to `docs/ops/api_performance_baseline.md`
- Record p50/p95/p99 and any threshold flags per existing baseline format

**Acceptance Criteria**
- [ ] AC-01: All 5 endpoints have baseline rows in `docs/ops/api_performance_baseline.md`
- [ ] AC-02: Measurements made against a live/staging environment (not mocked)
- [ ] AC-03: Row format matches existing api_performance_baseline.md format (p50/p95/p99)
- [ ] AC-04: Infrastructure & Operations Owner sign-off

---

### ST-05 — SI-05 p99 production latency baseline review (conditional)

**EPIC:** EPIC-01
**Backlog ref:** BLG-OPS-59
**Sprint:** 2 (conditional)
**Effort:** S (~0.5 day)
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Gate:** ≥2026-07-04 (SI-05 in production ≥4 weeks)

**Problem**
`POST /digest/si05/send` was baselined pre-launch. Production p99 under real data volume may differ. Confirming production performance validates the service is not degrading under real conditions.

**Scope**
- After 2026-07-04: extract p99 latency from Render logs for `POST /digest/si05/send`
- Compare against BLG-OPS-54 pre-launch baseline
- If p99 > 2× baseline: file a performance investigation item; otherwise record PASS
- Document findings in a brief perf review note (docs/ops/ or equivalent)

**Acceptance Criteria**
- [ ] AC-01: Post-4-week p99 latency extracted from Render logs and documented
- [ ] AC-02: Comparison against BLG-OPS-54 pre-launch baseline made with result recorded
- [ ] AC-03: Performance PASS recorded or investigation item filed (if p99 > 2× baseline)
- [ ] AC-04: Gate condition verified: SI-05 in production ≥4 weeks (≥2026-07-04)
- [ ] AC-05: Infrastructure & Operations Owner sign-off

---

## EPIC-02 — UX Debt Clearance

Maps to: S2-02, S2-03

**Description:** Clears two UX debt items: the pre-entry panel override acknowledgement improvement (from BLG-FE-49 UX assessment candidates), and the Red Flag Journal visual design review pre-brief (enabling BLG-FE-41 sprint planning when gate clears 2026-06-21).

---

### ST-02 — Pre-entry panel: separate warn/fail override acknowledgement flow

**EPIC:** EPIC-02
**Backlog ref:** BLG-FE-56
**Sprint:** 1
**Effort:** S (~1 day)
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Gate:** None

**Problem**
PreEntryValidationPanel treats `warn` and `fail` checks with the same override acknowledgement checkbox. `fail` represents a strategy hard stop; `warn` is advisory. Identical acknowledgement paths may encourage reflexive override of hard stops.

**Scope**
- Separate override acknowledgement path for `fail` checks (deliberate confirmation step) vs `warn` checks (existing checkbox flow)
- `fail` acknowledgement should require explicit additional step (e.g., modal with "I understand this violates my strategy" confirmation)
- Document the separated flow in a spec note or update PreEntryValidationPanel component spec
- **Note:** This story produces a specification/design output. Frontend implementation is a separate follow-on story if PO approves.

**Acceptance Criteria**
- [ ] AC-01: Override UX specification differentiates warn (advisory checkbox) from fail (strategy violation — explicit modal or equivalent)
- [ ] AC-02: Fail override acknowledgement requires additional deliberate step beyond existing checkbox
- [ ] AC-03: Existing warn-only acknowledgement flow preserved for warn-only states
- [ ] AC-04: Spec reviewed and signed off by Head of UX & Design and Frontend Specs & UX Documentation Owner
- [ ] AC-05: Output filed in docs/product/ux/ or equivalent spec location

---

### ST-03 — RFJ visual design review pre-brief

**EPIC:** EPIC-02
**Backlog ref:** BLG-FE-64
**Sprint:** 1
**Effort:** S (~0.5 day)
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Gate:** SI-03 live ≥30 days = 2026-06-21 (must not execute before this date)

**Problem**
BLG-FE-41 (Red Flag Journal visual design review) gate clears 2026-06-21. A design review brief prepared ahead of time prevents sprint planning delay. BLG-FE-67 (design review scope definition, ✅ complete v5.3 ST-22) produced `blg_fe_64_scope_definition.md` — this story produces the brief using that scope definition as input.

**Scope**
- Produce design review brief for BLG-FE-41 using `blg_fe_64_scope_definition.md` as input
- Brief defines: review scope (filters UX, severity visual hierarchy, event type colour coding, timeline vs list layout), evaluation criteria, and expected deliverable format
- Brief reviewed by Head of UX & Design

**Acceptance Criteria**
- [ ] AC-01: Design review brief produced and filed (docs/product/ux/ or equivalent)
- [ ] AC-02: Brief references `blg_fe_64_scope_definition.md` as scope input
- [ ] AC-03: Brief covers: scope definition, evaluation criteria, deliverable format
- [ ] AC-04: Head of UX & Design sign-off on brief scope
- [ ] AC-05: Gate condition verified: SI-03 live ≥30 days (≥2026-06-21)
- [ ] AC-06: BLG-FE-64 marked COMPLETE in backlog upon sign-off

---

## EPIC-03 — SI-05 Governance Follow-Through

Maps to: S2-04, S2-06, S2-07

**Description:** SI-05 governance documentation — Phase 2 activation criteria (enabling future Phase 2 decision-making) and post-effectiveness-review monitoring documents (actionability metrics, cadence review). Conditional Sprint 2 items depend on the 2026-07-04 SI-05 effectiveness review completing.

---

### ST-04 — SI-05 Phase 2 activation criteria definition

**EPIC:** EPIC-03
**Backlog ref:** BLG-GOV-92
**Sprint:** 1
**Effort:** S (~0.5 day)
**Owner:** Product Owner; PMO Lead
**Gate:** None (must be complete before SI-02 frontend sprint planning, ~Nov 2026)

**Problem**
SI-05 Phase 2 (integrating SI-02 drift signals) has no documented activation criteria. When SI-02 frontend activates (~Nov 2026), the Phase 2 go/no-go decision will lack empirical reference. Criteria defined now prevent premature or unnecessary delayed activation.

**Scope**
- Define SI-05 Phase 2 activation criteria covering:
  - Hard gate: SI-02 frontend shipped and in active use
  - Quality gate: SI-02 drift scores confirmed as meaningful (not noise-dominated)
  - Phase 1 effectiveness gate: PO confirms SI-05 Phase 1 actively used (per BLG-GOV-96 effectiveness criteria)
  - Optional: minimum weeks of SI-02 drift data
- Document criteria in a decisions record or planning note
- PMO Lead to acknowledge responsibility for criteria check at SI-02 frontend release planning

**Acceptance Criteria**
- [ ] AC-01: Phase 2 activation criteria document produced and filed (docs/governance/ or docs/product/decisions/)
- [ ] AC-02: Criteria cover: SI-02 shipping gate, data quality threshold, Phase 1 effectiveness confirmation
- [ ] AC-03: Product Owner reviews and approves criteria document
- [ ] AC-04: PMO Lead acknowledges responsibility for criteria check at SI-02 frontend release planning
- [ ] AC-05: BLG-GOV-92 marked COMPLETE in backlog upon sign-off

---

### ST-06 — SI-05 digest actionability metric definition (conditional)

**EPIC:** EPIC-03
**Backlog ref:** BLG-GOV-115
**Sprint:** 2 (conditional)
**Effort:** S (~0.5–1 day)
**Owner:** Metrics Definitions & Analytics Owner; Infrastructure & Operations Owner
**Gate:** 2026-07-04 effectiveness review (BLG-GOV-113) complete

**Problem**
After the 2026-07-04 effectiveness review, the digest's actionability should be formally assessed. Without metric definitions, the review cannot produce measurable outcomes.

**Scope**
- Define 2–4 actionability metrics for SI-05 digest effectiveness
- Metrics measurable from existing data sources (si05_digest_log, red_flag_events, trade data)
- Produce metrics definition document
- Input to BLG-GOV-96 (effectiveness measurement criteria) and BLG-GOV-112 (cadence review)

**Acceptance Criteria**
- [ ] AC-01: 2–4 actionability metrics formally defined with data source mapping
- [ ] AC-02: Metrics document reviewed by Metrics Definitions & Analytics Owner
- [ ] AC-03: Gate condition verified: 2026-07-04 effectiveness review (BLG-GOV-113) complete
- [ ] AC-04: Metrics document filed and cross-referenced in BLG-GOV-96 and BLG-GOV-112
- [ ] AC-05: BLG-GOV-115 marked COMPLETE in backlog upon sign-off

---

### ST-07 — SI-05 digest weekly cadence review (conditional)

**EPIC:** EPIC-03
**Backlog ref:** BLG-GOV-112
**Sprint:** 2 (conditional)
**Effort:** S (~0.5 day)
**Owner:** Product Owner; Director of Quality
**Gate:** 2026-07-04 effectiveness review (BLG-GOV-113) complete; ST-06 complete (metrics needed as input)

**Problem**
After 4+ weeks of production use, the weekly cadence should be reviewed: is weekly too frequent/infrequent? The first effectiveness review (2026-07-04) provides the data needed for this assessment.

**Scope**
- After 2026-07-04 effectiveness review: assess weekly cadence appropriateness
- Review si05_digest_log delivery count, feedback, and whether digest content is acted upon
- Use ST-06 actionability metrics as evidence input
- Produce cadence recommendation: maintain weekly / move to bi-weekly / adaptive cadence

**Acceptance Criteria**
- [ ] AC-01: Cadence review document produced (docs/governance/ or equivalent)
- [ ] AC-02: Recommendation made with data backing from si05_digest_log and ST-06 metrics
- [ ] AC-03: Gate condition verified: 2026-07-04 effectiveness review complete
- [ ] AC-04: ST-06 (actionability metrics) output available as input
- [ ] AC-05: Product Owner sign-off on recommendation
- [ ] AC-06: BLG-GOV-112 marked COMPLETE in backlog upon sign-off
