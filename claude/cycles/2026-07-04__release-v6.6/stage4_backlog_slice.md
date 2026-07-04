**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v6.6
**Cycle:** 2026-07-04__release-v6.6
**Last Updated:** 2026-07-04
**Sprint Backlog Source:** This slice is authoritative. Sprint Planning Engine reads this file at Phase 2.

---

# v6.6 Backlog Slice — 2026-07-04__release-v6.6

<!-- release-plan-marker: RP:v6.6:2026-07-04__release-v6.6 -->

---

## EPIC-01 — UX & Accessibility Debt

**Purpose:** Close two Skill-Silo pull-forward U-items: a systematic WCAG-AA contrast sweep across secondary/disclaimer text surfaces, and Red Flag Journal filter-state persistence (gate cleared 2026-06-21, 43 days prior to this cycle).

**Sprint assignment:** Sprint 1

**Maps to:** S2-01, S2-02

---

### ST-01 — Colour contrast audit sweep (BLG-FE-82)

**Type:** Firm
**Effort:** S (~1 day)
**Owner:** Head of UX & Design
**Backlog ref:** BLG-FE-82
**Delegation class:** delegated_frontend
**Sprint:** Sprint 1
**EPIC:** EPIC-01

**Context:** BLG-UX-01/02 (v6.4) fixed WCAG-AA contrast failures on the two AI disclaimer surfaces specifically, found via ad hoc review. No systematic sweep has checked other secondary/disclaimer-style text surfaces app-wide for the same class of issue.

**Acceptance criteria:**
- AC-01: Contrast audit completed across all identified secondary-text surfaces app-wide
- AC-02: Findings documented; any failures filed as follow-up backlog items
- AC-03: Head of UX & Design sign-off recorded

---

### ST-02 — Red Flag Journal filter state persistence (BLG-FE-40)

**Type:** Firm
**Effort:** S (~0.5 day)
**Owner:** Base44 Frontend; Head of UX & Design
**Backlog ref:** BLG-FE-40
**Delegation class:** delegated_frontend
**Sprint:** Sprint 1
**EPIC:** EPIC-01

**Context:** Red Flag Journal filter state (date range, severity, rule type) resets on page reload. Gate condition ("RFJ in active use ≥30 days post-v3.9") cleared 2026-06-21 (v3.9 shipped 2026-05-22); PO gate-clearance confirmation recorded in `release_plan.md` §1.4b.

**Acceptance criteria:**
- AC-01: Filter state persists across page reloads (localStorage)
- AC-02: Stale state (version mismatch) cleared gracefully without error
- AC-03: Playwright test: set filter → reload page → verify filter state restored

---

## EPIC-02 — QA & Test Infrastructure Debt

**Purpose:** Close two 2026-07-03 technical-debt review findings: backlog ID collision audit, and investigation of automated derivation for the `database.py` stub-sync list.

**Sprint assignment:** Sprint 1

**Maps to:** S2-03, S2-04

---

### ST-03 — Audit colliding backlog IDs (BLG-QA-72)

**Type:** Firm
**Effort:** S (~0.5 day)
**Owner:** Director of Quality; Product Owner
**Backlog ref:** BLG-QA-72
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-02

**Context:** `groom backlog`'s last run flagged "pre-existing duplicate IDs" as known-but-unresolved without naming them. A direct scan confirms real collisions: `BLG-OPS-13` and `BLG-FE-45` each appear 9 times, `BLG-OPS-17`/`BLG-GOV-88`/`BLG-FEAT-55` appear 8 times, `BLG-SPEC-46`/`BLG-QA-42` appear 7 times, plus a dozen more IDs appearing 4–6 times.

**Acceptance criteria:**
- AC-01: All IDs appearing ≥4 times classified as prose-citation vs. true collision
- AC-02: Any true collisions renumbered with no ID reused across backlog.md/backlog_archive.md
- AC-03: Next `groom backlog` health report shows 0 unresolved duplicate IDs

---

### ST-04 — database.py / _DB_STUB_FUNCTIONS manual-sync risk (BLG-QA-73)

**Type:** Firm
**Effort:** M (~1–2 days)
**Owner:** QA & Testing Owner; Backend Engineering Patterns Owner
**Backlog ref:** BLG-QA-73
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-02

**Context:** `tests/conftest.py` maintains a hand-written parallel list (`_DB_STUB_FUNCTIONS`, currently 37 entries) that must list every `database` function imported by `backend/services/position_service.py`, or CI fails with an opaque `ImportError` (BLG-QA-20 convention, codified in CLAUDE.md). Nothing enforces the two lists stay in sync beyond manual discipline.

**Acceptance criteria:**
- AC-01: Decision recorded — automated derivation adopted, or documented as infeasible with reasoning
- AC-02: If adopted: adding a new `database` import to `position_service.py` no longer requires a manual `conftest.py` edit, verified by a CI run
- AC-03: CLAUDE.md rule updated or retired to match the outcome

---

## Summary

| EPIC | Stories | Firm | Conditional | Total effort estimate |
|------|---------|------|-------------|------------------------|
| EPIC-01 | ST-01, ST-02 | 2 | 0 | ~1.5 days |
| EPIC-02 | ST-03, ST-04 | 2 | 0 | ~1.5–2.5 days |
| **Total** | **4** | **4** | **0** | **~3–4 days** |
