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
| AC-9 | Strategy Rules owner sign-off before merge | **Pass** | Sign-off received 2026-04-18 — see block below |

### Strategy Rules Owner Sign-off

**Status:** SIGNED OFF — 2026-04-18

```
Strategy Rules Owner: Confirmed — 2026-04-18
Confirmed: SRB-v1.7 conditional compliance satisfied.
AI output is structurally isolated from all signal, scoring, compliance,
and recommendation pipelines. Disclaimer is non-dismissible. Section is
opt-in per session (collapsed by default, no auto-generation).
```

**Review findings:**
- Condition 1 (no pipeline path): `aiSummary` state used only in JSX render; not passed to any downstream component; no backend writes. CONFIRMED.
- Condition 2 (disclaimer non-dismissible): First child of expanded block; renders for all sub-states; no dismiss handler. CONFIRMED.
- Condition 3 (collapsed by default, no auto-generation): `useState(false)`, no `useEffect`, generation only on explicit button click. CONFIRMED.

---

## EPIC-04 Consolidation

| Story | Classification | DoQ | Notes |
|-------|---------------|-----|-------|
| ST-07 | Autonomous | Pass — engine sign-off 2026-04-18 | Backend complete |
| ST-08 | Delegated Frontend | Pass — Strategy Rules owner sign-off 2026-04-18 | Frontend complete; merge gate cleared |

**EPIC-04 PR:** #248
**Merge gate:** Cleared — Strategy Rules owner sign-off received 2026-04-18

---

## DoQ EPIC-Level Sign-off — Director of Quality

**Signed off by:** Director of Quality
**Date:** 2026-04-20
**Method:** Evidence review

**Review findings:**

| Item | Status |
|------|--------|
| ST-07 all AC (AC-1 through AC-7) | Pass — engine autonomous sign-off 2026-04-18; all AC code-review-verifiable; no frontend changes |
| ST-08 all AC (AC-1 through AC-9) | Pass — Strategy Rules owner sign-off 2026-04-18; SRB-v1.7 conditions (pipeline isolation, non-dismissible disclaimer, collapsed by default) all confirmed |
| Product Owner acceptance | Pass — 2026-04-19; both stories accepted independently |
| No deviations filed | Confirmed — no spec deviations across EPIC-04 |
| No open escalations | Confirmed |

**EPIC-04 outcome: ACCEPTED.** All stories complete, all sign-off authorities satisfied, PR #248 merged.

---

## Product Owner Acceptance

**Status:** ACCEPTED — 2026-04-19

**Reviewed by:** Product Owner
**Date:** 2026-04-19

**ST-07 verdict:** Accepted. Backend contract, OpenAPI, and implementation all consistent. Graceful failure handling confirmed. Output isolation from pipelines confirmed.

**ST-08 verdict:** Accepted. SRB-v1.7 compliance independently verified in code: collapsed by default, no auto-generation, disclaimer non-dismissible, AI output display-only. Strategy Rules sign-off 2026-04-18 noted.

**EPIC-04 outcome:** Accepted. PR #248 cleared for merge.

---

## Changelog

| Date | Change |
|------|--------|
| 2026-04-18 | Created — ST-07 DoQ passed (engine); ST-08 Strategy Rules owner sign-off received; merge gate cleared |
| 2026-04-19 | Product Owner acceptance recorded — EPIC-04 cleared for merge |
| 2026-04-20 | Director of Quality EPIC-level sign-off added — all story sign-offs and PO acceptance reviewed and confirmed; EPIC-04 accepted |
