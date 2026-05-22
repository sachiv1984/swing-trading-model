**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Published
**Cycle:** 2026-05-22__release-v4.0
**Release:** v4.0
**Generated:** 2026-05-22

---

# Stage 4 Backlog Slice — v4.0

## Sprint 1 Stories

### EPIC-01 — Arc 5 Analytics Metrics

| ST | Title | Source | Effort | Priority |
|----|-------|--------|--------|----------|
| ST-01 | SI-01 pass/fail rate by rule — backend metric endpoint | BLG-FEAT-36 | M | P2 |
| ST-02 | Red flag event frequency metric — backend + frontend | BLG-FEAT-37 | S | P2 |
| ST-03 | E2E Playwright test — SI-01→SI-03 integration path | BLG-QA-25 | S | P2 |
| ST-04 | Trade plan adherence rate metric — backend + frontend | BLG-FEAT-39 | S | P2 |

### EPIC-02 — Ticker Quality & Security

| ST | Title | Source | Effort | Priority |
|----|-------|--------|--------|----------|
| ST-05 | Validate ticker symbol on add | BLG-BE-15 | S | P1 |
| ST-06 | Red flag endpoint auth and PII review | BLG-GOV-37 | XS | P2 |

**Sprint 1 total:** M+S+S+S+S+XS ≈ 5–6 days

---

## Sprint 2 Stories

### EPIC-03 — AI Governance & CI/CD

| ST | Title | Source | Effort | Priority |
|----|-------|--------|--------|----------|
| ST-07 | Gemini audit trail — log AI thesis generation calls | BLG-GOV-35 | M | P2 |
| ST-08 | Gemini cost tracking — token usage and cost per call | BLG-OPS-26 | S | P2 |
| ST-09 | CI/CD automated staging re-deploy on main merge | BLG-OPS-27 | M | P2 |

### EPIC-04 (Conditional — gate: 20+ closed trades)

| ST | Title | Source | Effort | Priority |
|----|-------|--------|--------|----------|
| ST-10 | PT-04 Setup Quality Score — backend (conditional) | BLG-FEAT-25 | L | P2 |
| ST-11 | PT-04 Setup Quality Score — frontend (conditional) | BLG-FEAT-25 | M | P2 |

**Sprint 2 firm total:** M+S+M ≈ 3–4 days  
**Sprint 2 conditional total (EPIC-04):** +L+M ≈ 4–6 days additional

---

## Slice Integrity

| Check | Result |
|-------|--------|
| All scope items (S2-01→S2-07) assigned to EPICs | ✅ |
| All ST-IDs sequential (ST-01→ST-11) | ✅ |
| Conditional items marked | ✅ ST-10, ST-11 |
| Sprint assignment consistent with release_plan.md | ✅ |
| Backlog lock protocol followed | ✅ acquired → committed → released |
| Idempotency marker written to backlog.md | ✅ `<!-- release-plan-marker: RP:v4.0:2026-05-22__release-v4.0 -->` |
