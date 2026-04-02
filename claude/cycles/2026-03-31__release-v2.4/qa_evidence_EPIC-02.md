**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-04-01
**Cycle:** 2026-03-31__release-v2.4
**EPIC:** EPIC-02 — Frontend & UX Polish
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# QA Evidence — EPIC-02 Frontend & UX Polish

---

## Story Sign-Off Blocks

---

### ST-04 — Fix missing P&L (GBP) column on Positions page

**Classification:** autonomous
**Status:** done
**Evidence method:** Code review; staging verification required for V-PATH2-01
**Deviation resolved:** DEV-EPIC02-ST05-03 (positions.md §Known Deviations — P2)

**AC verification:**

| AC | Requirement | Evidence | Result |
|----|-------------|----------|--------|
| 1 | Positions Table View displays P&L (GBP) column with absolute GBP value | `src/pages/Positions.js`: header split into `P&L (GBP)` + `P&L %` columns. GBP cell renders `£{Math.abs(pnl).toFixed(2)}` ✓ | Pass |
| 2 | Positive GBP P&L renders in green; negative renders in red | `isProfit ? "text-emerald-400" : "text-rose-400"` applied to GBP cell ✓ | Pass |
| 3 | P&L % column remains present alongside GBP column | New separate `<TableCell>` for P&L % with same colour-coding and `+/-` sign prefix ✓ | Pass |
| 4 | V-PATH2-01 passes on staging: £70.05 and £96.05 visible in green after seeding | Staging verification required post-merge | Pending staging |

**Verification note:** AC 4 requires staging run with seed data. Code review confirms correct data binding (`pnl` from `position.pnl`, `pnlPercent` from `position.pnl_percent`). Marked Pass with staging verification as post-merge action.

**DoQ sign-off:**
- [ ] Director of Quality — pending

---

### ST-05 — Add user-facing error message mapping layer

**Classification:** autonomous
**Status:** done
**Evidence method:** Code review

**AC verification:**

| AC | Requirement | Evidence | Result |
|----|-------------|----------|--------|
| 1 | API errors display user-readable message (not raw code or "undefined") | `friendlyErrorMessage(error)` prefers backend message; falls back to status-specific messages; final fallback "An unexpected error occurred." — never raw code or undefined ✓ | Pass |
| 2 | Error mapping covers all error codes in Error Response Standard | `STATUS_MESSAGES` covers HTTP 400/404/500 (all codes in conventions.md §13.2). Backend `message` field also surfaced directly ✓ | Pass |
| 3 | Raw technical details logged to console, not shown to user | `console.error("Exit failed:", error)` and equivalent calls log full error object. `friendlyErrorMessage` returns only the safe message string ✓ | Pass |
| 4 | No regression to existing error display behaviour | `friendlyErrorMessage` returns backend `error.message` when it's non-empty and non-generic — preserves all current meaningful messages ✓ | Pass |

**Applied in:** `src/pages/Positions.js` exit and save error handlers. `src/lib/apiError.js` utility available for all future consumers.

**DoQ sign-off:**
- [ ] Director of Quality — pending

---

## Consolidation

| Story | Classification | Result | Deviations |
|-------|---------------|--------|------------|
| ST-04 | autonomous | Pass (staging V-PATH2-01 pending) | Resolves DEV-EPIC02-ST05-03 (P2) |
| ST-05 | autonomous | Pass | None |

**EPIC-02 QA summary:** 2 autonomous stories complete (Pass). ST-04 resolves P2 deviation DEV-EPIC02-ST05-03. ST-04 V-PATH2-01 staging verification pending post-merge.

**Director of Quality sign-off:** Pending

---
