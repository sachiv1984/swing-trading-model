Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-06-16

---

# QA Evidence — EPIC-01: Staging Verification & QA Coverage

**Cycle:** 2026-06-16__release-v5.7
**Sprint:** Sprint 1

---

## ST-05 — BLG-FE-75: Staging verification — SI-05 deep links mobile Telegram

**ST ID:** ST-05
**Delegation Class:** delegated_qa
**Assigned To:** Head of UX & Design
**Spec Reference:** `claude/cycles/2026-06-16__release-v5.7/stage4_backlog_slice.md#ST-05`
**Delegation Record:** DEL-20260616-05

**Acceptance Criteria:**
- AC-01: SI-05 weekly Telegram digest opened on a mobile device
- AC-02: Risk Dashboard deep link navigates to `/RiskDashboard` on mobile Telegram — no broken link or navigation error
- AC-03: Red Flag Journal deep link navigates to `/RedFlagJournal` on mobile Telegram — no broken link or navigation error
- AC-04: Staging run date recorded in QA evidence
- AC-05 [staging-only evidence]: Head of UX & Design sign-off confirming mobile navigation test performed

**What was built (prior cycle):** SI-05 Telegram digest with deep links shipped in v5.1 (2026-06-04). Deep links constructed via frontend `createDeepLink()` utility. v5.6 ST-01 EPIC-01 AC-02 was deferred to this sprint for mobile Telegram environment verification.

**Test scenarios to execute:**
- Open production SI-05 weekly digest on a physical mobile device in Telegram
- Tap Risk Dashboard deep link → confirm navigation to `/RiskDashboard`
- Tap Red Flag Journal deep link → confirm navigation to `/RedFlagJournal`
- Record staging run date

**QA Findings (Head of UX & Design to complete):**

| AC | Description | Result | Notes |
|----|-------------|--------|-------|
| AC-01 | Digest opened on mobile | Pending | Requires physical mobile + Telegram |
| AC-02 | Risk Dashboard deep link navigates | Pending | |
| AC-03 | Red Flag Journal deep link navigates | Pending | |
| AC-04 | Staging run date recorded | Pending | |
| AC-05 | Head of UX & Design sign-off | Pending | |

**Disposition:** Pending — awaiting Head of UX & Design mobile staging run

---

## ST-06 — BLG-QA-56: SI-01 all-pass state Playwright scenario

*Entered at EPIC completion — pending ST-01 through ST-05 completion*

---

## ST-07 — BLG-QA-57: SI-03 Red Flag Journal pagination Playwright scenario

*Entered at EPIC completion — pending ST-01 through ST-05 completion*

---

## ST-08 — BLG-QA-58: Arc 5 compliance score trend Playwright scenario

*Entered at EPIC completion — pending ST-01 through ST-05 completion*

---

## ST-01 — BLG-OPS-66: Staging verification — concentration-status p95

*Entered at EPIC completion — pending Infrastructure & Operations Owner production measurement*

---

## ST-02 — BLG-OPS-67: Staging verification — red-flag-journal p95

*Entered at EPIC completion — pending Infrastructure & Operations Owner production measurement*

---

## ST-03 — BLG-OPS-68: Staging verification — behavioural-drift p95 + cache

*Entered at EPIC completion — pending Infrastructure & Operations Owner production measurement*

---

## ST-04 — BLG-OPS-69: Staging verification — research view p95 + cache

*Entered at EPIC completion — pending Infrastructure & Operations Owner production measurement*

---

## EPIC-Level Consolidation (to be completed at EPIC close)

*All 8 stories must reach `done` before the consolidation block and sign-off are completed.*
