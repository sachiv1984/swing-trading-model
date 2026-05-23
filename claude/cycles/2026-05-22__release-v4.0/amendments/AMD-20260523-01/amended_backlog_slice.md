**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-23
**Cycle:** 2026-05-22__release-v4.0
**Amendment:** AMD-20260523-01
**Supersedes:** claude/cycles/2026-05-22__release-v4.0/stage4_backlog_slice.md (for sprint planning purposes)
**Ratified:** 2026-05-23 by Product Owner and Director of Quality

> This amended backlog slice supersedes the original stage4_backlog_slice.md for the purposes
> of Sprint Planning. The original sealed artefact is unchanged and remains the historical record
> of the published release plan.

---

# Amended Stage 4 Backlog Slice — v4.0

## Amendment Summary

| Change | Item | Type | Reason |
|--------|------|------|--------|
| Added | ST-12 — Gemini Flash base wiring (BLG-BE-19) | hard-prerequisite | EPIC-03 ST-07/ST-08 undeliverable without Gemini wiring |
| Added | ST-13 — Starlette security upgrade to ≥1.0.1 | emergency-fix | CVE PYSEC-2026-161 medium severity auth bypass |

---

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
| ST-13 [ADDED by AMD-20260523-01] | Starlette security upgrade to ≥1.0.1 | CVE PYSEC-2026-161 | XS | P1 |

**Sprint 1 total:** M+S+S+S+S+XS+XS ≈ 5.5–6.5 days

---

## Sprint 2 Stories

### EPIC-03 — AI Governance & CI/CD

| ST | Title | Source | Effort | Priority | Notes |
|----|-------|--------|--------|----------|-------|
| ST-12 [ADDED by AMD-20260523-01] | Gemini Flash base wiring | BLG-BE-19 | S | P1 | **Must execute first in EPIC-03** — prerequisite for ST-07 and ST-08 |
| ST-07 | Gemini audit trail — log AI thesis generation calls | BLG-GOV-35 | M | P2 | Depends on ST-12 |
| ST-08 | Gemini cost tracking — token usage and cost per call | BLG-OPS-26 | S | P2 | Depends on ST-12 |
| ST-09 | CI/CD automated staging re-deploy on main merge | BLG-OPS-27 | M | P2 | Independent |

### EPIC-04 (Conditional — gate: 20+ closed trades)

| ST | Title | Source | Effort | Priority |
|----|-------|--------|--------|----------|
| ST-10 | PT-04 Setup Quality Score — backend (conditional) | BLG-FEAT-25 | L | P2 |
| ST-11 | PT-04 Setup Quality Score — frontend (conditional) | BLG-FEAT-25 | M | P2 |

**Sprint 2 firm total:** S+M+S+M ≈ 4–5 days
**Sprint 2 conditional total (EPIC-04):** +L+M ≈ 4–6 days additional

---

## Amended Slice Integrity

| Check | Result |
|-------|--------|
| All scope items (S2-01→S2-07) assigned to EPICs | ✅ |
| All original ST-IDs preserved (ST-01→ST-11) | ✅ |
| New ST-IDs continue sequence (ST-12, ST-13) | ✅ |
| Conditional items marked | ✅ ST-10, ST-11 |
| Sprint assignment consistent with release_plan.md | ✅ (ST-12/ST-13 follow EPIC assignments) |
| Amendment marker present | ✅ AMD-20260523-01 |
| Ratification confirmed | ✅ Product Owner + Director of Quality, 2026-05-23 |
