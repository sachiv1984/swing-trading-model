Owner: PMO Lead
Class: Planning Record (Class 3)
Status: Sealed
Last Updated: 2026-06-10
Cycle: 2026-06-09__release-v5.4

---

# Sprint Backlog — v5.4: Ops Monitoring, UX Debt Clearance & Governance Patches

---

## Sprint Goal

Deliver SI-05 ops monitoring follow-through (v5.3 endpoint baseline), clear the pre-entry panel and Red Flag Journal UX debt, and formally document SI-05 Phase 2 activation criteria — leaving no open ops or governance obligations from v5.3 ship.

**Goal confirmed:** Product Owner ✅ 2026-06-10

---

## Sprint Scope

**Firm stories (Sprint 1):** 4
**Conditional stories (Sprint 2, gate ≥2026-07-04):** 3
**Total:** 7

---

## Merge Order

**Sprint 1:** EPIC-01 → EPIC-02 → EPIC-03

**execution_state.json owner:** EPIC-01 (first in merge order). EPIC-02 and EPIC-03 must check for existing `execution_state.json` before creating their own — append rather than overwrite.

**Shared files:** None. Each EPIC writes to distinct document paths. No rebase required between EPICs.

---

## Sprint 1 — Firm Scope

### EPIC-01 — Ops Monitoring & Performance Baseline

**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Branch:** `exec/2026-06-09__release-v5.4/EPIC-01`

---

#### ST-01 — Add v5.3 new endpoints to api_performance_baseline.md

**Backlog ref:** BLG-OPS-60
**Effort:** S (~0.5 day)
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Delegation class:** `autonomous`
**Gate:** None

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-01`

| Field | Detail |
|-------|--------|
| Technical | All 5 v5.3 endpoints added as baseline rows to `docs/ops/api_performance_baseline.md`; format matches existing rows (p50/p95/p99 + threshold flags) |
| Quality | Measurements taken against live/staging environment (not mocked); all 5 endpoint rows present and correctly formatted |
| Security | N/A — no security surface changed |
| Verification | Director of Quality inspects `docs/ops/api_performance_baseline.md` — confirms 5 new rows present, format-compliant, and Infrastructure & Operations Owner sign-off recorded |

**Staging-only ACs:** AC-02 (live/staging environment measurement — cannot be reproduced in CI)

**Spec references:** `stage4_backlog_slice.md#ST-01`

---

### EPIC-02 — UX Debt Clearance

**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Branch:** `exec/2026-06-09__release-v5.4/EPIC-02`

---

#### ST-02 — Pre-entry panel: separate warn/fail override acknowledgement flow

**Backlog ref:** BLG-FE-56
**Effort:** S (~1 day)
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Delegation class:** `autonomous`
**Gate:** None

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-02`

| Field | Detail |
|-------|--------|
| Technical | Override UX specification differentiates warn (advisory checkbox) from fail (strategy violation — explicit modal or equivalent step); fail override requires additional deliberate step; warn-only flow preserved; spec output filed in `docs/product/ux/` |
| Quality | Spec reviewed by Head of UX & Design and Frontend Specs & UX Documentation Owner and signed off; document present at expected path |
| Security | N/A — specification document only; no security surface |
| Verification | Director of Quality confirms spec document present at `docs/product/ux/`, signed off by both owners, fail/warn distinction clearly documented |

**Staging-only ACs:** None

**Spec references:** `stage4_backlog_slice.md#ST-02`

---

#### ST-03 — RFJ visual design review pre-brief

**Backlog ref:** BLG-FE-64
**Effort:** S (~0.5 day)
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Delegation class:** `autonomous`
**Gate:** SI-03 live ≥30 days = **2026-06-21** — must not execute before this date

**⚠ Within-sprint sequencing constraint:** ST-03 must not be executed before 2026-06-21. Execute ST-02 first. Confirm date ≥ 2026-06-21 before beginning ST-03.

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-03`

| Field | Detail |
|-------|--------|
| Technical | Design review brief produced and filed (`docs/product/ux/` or equivalent); references `blg_fe_64_scope_definition.md`; covers scope definition, evaluation criteria, deliverable format; BLG-FE-64 marked COMPLETE |
| Quality | Brief signed off by Head of UX & Design; gate condition verified (date ≥ 2026-06-21) |
| Security | N/A — design document only |
| Verification | Director of Quality confirms brief present and signed off; BLG-FE-64 marked COMPLETE in `claude/backlog/backlog.md` |

**Staging-only ACs:** None

**Spec references:** `stage4_backlog_slice.md#ST-03`

---

### EPIC-03 — SI-05 Governance Follow-Through

**Owner:** Product Owner; PMO Lead
**Branch:** `exec/2026-06-09__release-v5.4/EPIC-03`

---

#### ST-04 — SI-05 Phase 2 activation criteria definition

**Backlog ref:** BLG-GOV-92
**Effort:** S (~0.5 day)
**Owner:** Product Owner; PMO Lead
**Delegation class:** `autonomous`
**Gate:** None

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-04`

| Field | Detail |
|-------|--------|
| Technical | Phase 2 activation criteria document filed (`docs/governance/` or `docs/product/decisions/`); covers SI-02 shipping gate, data quality threshold, Phase 1 effectiveness confirmation; PMO Lead accountability recorded; BLG-GOV-92 marked COMPLETE |
| Quality | Product Owner reviews and approves criteria document; PMO Lead explicitly acknowledges criteria check responsibility at SI-02 frontend release planning |
| Security | N/A — governance document only |
| Verification | Director of Quality confirms document filed, Product Owner approval recorded, PMO Lead acknowledgement present, BLG-GOV-92 marked COMPLETE |

**Staging-only ACs:** None

**Spec references:** `stage4_backlog_slice.md#ST-04`

---

## Sprint 2 — Conditional Scope (Gate ≥2026-07-04)

Sprint 2 may not begin until the Product Owner confirms all Sprint 2 gate conditions are met. The amendment cycle must be invoked to unseal Sprint 2 stories.

---

### EPIC-01 — Ops Monitoring (Sprint 2)

#### ST-05 — SI-05 p99 production latency baseline review

**Backlog ref:** BLG-OPS-59
**Effort:** S (~0.5 day)
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Delegation class:** `autonomous`
**Gate:** ≥2026-07-04 (SI-05 in production ≥4 weeks)
**Status at planning:** `deferred_at_planning`

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-05`

| Field | Detail |
|-------|--------|
| Technical | Post-4-week p99 latency for `POST /digest/si05/send` extracted from Render logs; compared against BLG-OPS-54 pre-launch baseline; PASS recorded or investigation item filed if p99 > 2× baseline |
| Quality | Findings documented; gate condition verified; comparison result clearly stated |
| Security | N/A |
| Verification | Director of Quality confirms findings documented, comparison against baseline made, gate condition verified (SI-05 ≥4 weeks production) |

**Staging-only ACs:** AC-01 (p99 extraction from Render logs — requires live environment), AC-04 (gate condition verification — production-state dependent)

**Spec references:** `stage4_backlog_slice.md#ST-05`

---

### EPIC-03 — SI-05 Governance (Sprint 2)

#### ST-06 — SI-05 digest actionability metric definition

**Backlog ref:** BLG-GOV-115
**Effort:** S (~0.5–1 day)
**Owner:** Metrics Definitions & Analytics Owner; Infrastructure & Operations Owner
**Delegation class:** `autonomous`
**Gate:** 2026-07-04 effectiveness review (BLG-GOV-113) complete
**Status at planning:** `deferred_at_planning`

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-06`

| Field | Detail |
|-------|--------|
| Technical | 2–4 actionability metrics defined with data source mapping; metrics document filed and cross-referenced in BLG-GOV-96 and BLG-GOV-112; BLG-GOV-115 marked COMPLETE |
| Quality | Metrics reviewed by Metrics Definitions & Analytics Owner; gate condition verified |
| Security | N/A |
| Verification | Director of Quality confirms metrics document present, gate condition verified, cross-references in place |

**Staging-only ACs:** None

**Spec references:** `stage4_backlog_slice.md#ST-06`

---

#### ST-07 — SI-05 digest weekly cadence review

**Backlog ref:** BLG-GOV-112
**Effort:** S (~0.5 day)
**Owner:** Product Owner; Director of Quality
**Delegation class:** `autonomous`
**Gate:** 2026-07-04 effectiveness review complete; ST-06 complete
**Status at planning:** `deferred_at_planning`
**Story dependency:** ST-06 must complete before ST-07 begins

**Acceptance Criteria:** See `stage4_backlog_slice.md#ST-07`

| Field | Detail |
|-------|--------|
| Technical | Cadence review document produced; recommendation made (maintain weekly / bi-weekly / adaptive) with data backing from si05_digest_log and ST-06 metrics; BLG-GOV-112 marked COMPLETE |
| Quality | Product Owner sign-off on recommendation; gate conditions verified; ST-06 output available as input |
| Security | N/A |
| Verification | Director of Quality confirms document present, recommendation data-backed, Product Owner sign-off recorded |

**Staging-only ACs:** None

**Spec references:** `stage4_backlog_slice.md#ST-07`

---

## Product Owner Sign-Off

Product Owner: ✅ Confirmed
Date: 2026-06-10

**Sign-off scope:**
- Sprint goal confirmed ✅
- Sprint 1 firm scope (ST-01 through ST-04) confirmed ✅
- Sprint 2 conditional scope (ST-05 through ST-07, gate ≥2026-07-04) acknowledged ✅
- All acceptance criteria reviewed and confirmed ✅
- Staging-only AC designations reviewed (ST-01 AC-02 staging-only) ✅
- Capacity PASS acknowledged ✅
- No outstanding actions marked Blocker? Yes ✅

---

## Director of Quality Sign-Off

Director of Quality: ✅ Confirmed — QA criteria sufficient for `qa_evidence_EPIC-*.md` production at sprint close. No coverage gaps identified.
Date: 2026-06-10
