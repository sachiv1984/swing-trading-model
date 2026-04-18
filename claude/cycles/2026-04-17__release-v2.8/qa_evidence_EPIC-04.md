**Owner:** Director of Quality
**Class:** Governance Artefact (Class 2)
**Status:** Active
**Cycle:** 2026-04-17__release-v2.8
**EPIC:** EPIC-04 — AI Journal Summarisation
**Created:** 2026-04-18

---

# QA Evidence Log — EPIC-04

## ST-07 — AI Journal Summary Backend

**Classification:** Autonomous
**Commit:** 5b67949
**Branch:** exec/2026-04-17__release-v2.8/EPIC-04

### Acceptance Criteria Verification

| AC | Description | Status | Evidence |
|----|-------------|--------|----------|
| AC-1 | `POST /ai/journal-summary` accepts trade_ids or date range | Pass | `backend/routers/ai.py` lines 53–75; raises HTTP 422 if neither provided |
| AC-2 | LLM failure returns HTTP 200 with summary:null and message (no 500) | Pass | `backend/services/ai_service.py` lines 62–76: bare except returns fallback dict; router always returns 200 |
| AC-3 | ANTHROPIC_API_KEY read from env var; no secrets in code | Pass | `ai_service.py` line 29: `os.getenv("ANTHROPIC_API_KEY")` |
| AC-4 | Default model `claude-haiku-4-5-20251001`; override via AI_MODEL env var | Pass | `ai_service.py` lines 16, 30 |
| AC-5 | AI output not stored in database | Pass | Router is read-only; no INSERT/UPDATE anywhere in ai.py or ai_service.py |
| AC-6 | openapi.yaml updated in same commit | Pass | openapi.yaml bumped to v2.7.0 with `/ai/journal-summary` path in commit 5b67949 |
| AC-7 | api_endpoints.md `## POST /ai/journal-summary` at `##` level | Pass | `docs/specs/api_contracts/ai_endpoints.md` line 26: `## POST /ai/journal-summary` |

### DoQ Sign-off (Autonomous)

Autonomous sign-off criteria:
- [x] All AC are autonomous (no human judgement required)
- [x] All AC are code-review-verifiable
- [x] No frontend changes
- [x] Engine signer permitted for autonomous classification

**Signed off by:** Sprint Execution Engine
**Date:** 2026-04-18
**Method:** Code review

---

## ST-08 — AI Journal Summary Frontend

**Classification:** Delegated Frontend
**Commit:** 19acb9c
**Branch:** exec/2026-04-17__release-v2.8/EPIC-04

### Acceptance Criteria Verification

| AC | Description | Status | Evidence |
|----|-------------|--------|----------|
| AC-1 | Section collapsed by default on page load | Pass | `TradeHistory.js` line 24: `useState(false)` for `aiSummaryOpen` |
| AC-2 | No API call until user expands and clicks Generate | Pass | `handleGenerateSummary` only called on button click; no useEffect auto-trigger |
| AC-3 | Disclaimer banner non-dismissible and always visible when expanded | Pass | Disclaimer rendered unconditionally inside `{aiSummaryOpen && ...}` block; no dismiss handler |
| AC-4 | Disclaimer text: "AI-generated summary — for reference only. Not a trading recommendation." | Pass | TradeHistory.js disclaimer span matches spec exactly |
| AC-5 | 4 states: idle placeholder / loading spinner / summary text / error message | Pass | Conditional rendering in summary panel: aiLoading → spinner; aiSummary → text; aiGenerated && !aiSummary → unavailable; default → placeholder |
| AC-6 | Generate/Refresh label toggle on aiSummary state | Pass | Button label: `{aiSummary ? "Refresh Summary" : "Generate Summary"}` |
| AC-7 | POST /ai/journal-summary called with filtered trade IDs | Pass | `filteredTrades.map((t) => t.id)` passed as `trade_ids` |
| AC-8 | AI output not used in any signal/scoring calculation | Pass | Result only sets `aiSummary` state for display; no other usage |
| AC-9 | Strategy Rules owner sign-off before merge | **PENDING** | Hard merge pre-condition — see note below |

### Strategy Rules Owner Sign-off (Required Before Merge)

**Status:** AWAITING SIGN-OFF

This is a hard merge pre-condition per ST-08 AC and SRB-v1.7. The PR must not be merged until the Strategy Rules owner has reviewed and confirmed:

1. AI output is display-only — confirmed no path from summary text into signal, scoring, compliance, or recommendation pipeline.
2. Disclaimer is non-dismissible and always visible when the section is expanded.
3. Section is collapsed by default; no auto-generation on page load.

**Sign-off block:**

```
Strategy Rules Owner: [AWAITING SIGN-OFF]
Date: [AWAITING]
Confirmed: SRB-v1.7 conditional compliance satisfied
```

---

## EPIC-04 Consolidation

| Story | Classification | DoQ | Notes |
|-------|---------------|-----|-------|
| ST-07 | Autonomous | Pass — engine sign-off 2026-04-18 | Backend complete |
| ST-08 | Delegated Frontend | Pending — Strategy Rules owner sign-off required | Frontend complete; merge blocked on sign-off |

**EPIC-04 PR:** Pending creation
**Merge gate:** Blocked on ST-08 Strategy Rules owner sign-off

---

## Changelog

| Date | Change |
|------|--------|
| 2026-04-18 | Created — ST-07 DoQ passed (engine), ST-08 pending Strategy Rules sign-off |
