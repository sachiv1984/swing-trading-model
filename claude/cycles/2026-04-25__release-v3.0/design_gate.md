**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-25
**Cycle:** 2026-04-25__release-v3.0

---

# Design Gate Record — 2026-04-25__release-v3.0

## Gate Status: PASSED

Completed: 2026-04-25
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed (ST-11 keyboard shortcuts design artefact approved)

---

## Item Classification Summary

| Item ID | Title | Classification | Design Artefact | Frontend Spec | Gate Status |
|---------|-------|----------------|-----------------|---------------|-------------|
| ST-01 | Ticker Universe Data Model + Endpoints | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-02 | OHLCV Data Pipeline Service | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-03 | ATR + Regime Detection + Signal Scoring Engine | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-04 | Screener Batch Engine + API Endpoints | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-05 | Screener Results Page | Design Pre-Approved | `docs/specs/frontend/pages/screener_results.md` v1.0 | `screener_results.md` v1.0 §4–§10 | ✅ Cleared |
| ST-06 | Watchlist Promotion Flow | Design Pre-Approved | `docs/specs/frontend/pages/screener_results.md` v1.0 §8 | `screener_results.md` v1.0 §8 | ✅ Cleared |
| ST-07 | Screener News Panel Attachment | Design Pre-Approved | `docs/specs/frontend/pages/screener_results.md` v1.0 §9 | `screener_results.md` v1.0 §9; DEV-01 notes v3.0 as target | ✅ Cleared |
| ST-08 | External API Health Check Extension | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-09 | AI Journal Monitoring Metrics | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-10 | AI Audit Service Unit Tests | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-11 | Keyboard Shortcuts | Design Required | `docs/design/2026-04-25__release-v3.0/keyboard-shortcuts/ux_spec.md` v1.0 | `navigation.md` v1.1 §Keyboard Shortcuts | ✅ Cleared |
| ST-12 | execution_prompt.md §2 Deferred Patch | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-13 | execution_prompt.md §3.1.A Deferred Patch | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-14 | prompt_change_log.md Retrospective Entries | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-15 | Consecutive Losing Streak Metric | Design Pre-Approved | `docs/specs/frontend/pages/analytics.md` v1.7 §3 (`loss_streak` field already specced) | `analytics.md` v1.7 §3 | ✅ Cleared |
| ST-16 | Model Version Contract for AI Journal | Design Not Applicable | N/A | N/A | ✅ Cleared |

---

## Blocked Items

None.

---

## Design Artefacts Produced This Cycle

| Item | Artefact | Location | Approved by |
|------|----------|----------|-------------|
| ST-11 | Keyboard shortcuts UX decision record | `docs/design/2026-04-25__release-v3.0/keyboard-shortcuts/ux_spec.md` | Product Owner — 2026-04-25 |

---

## Frontend Spec Versions Locked for Sprint Planning

| Item | Spec | Version |
|------|------|---------|
| ST-05 | `docs/specs/frontend/pages/screener_results.md` | v1.0 |
| ST-06 | `docs/specs/frontend/pages/screener_results.md` | v1.0 |
| ST-07 | `docs/specs/frontend/pages/screener_results.md` | v1.0 |
| ST-11 | `docs/specs/frontend/pages/navigation.md` | v1.1 |
| ST-15 | `docs/specs/frontend/pages/analytics.md` | v1.7 |

---

## Classification Rationale Notes

**ST-05–ST-07 (Design Pre-Approved):** `screener_results.md` v1.0 was produced in v2.9 (BLG-FE-17) as the UX prerequisite for DS-02. It covers all DS-02 interaction patterns per §11 AC Coverage Summary: column layout (§4), sort/filter (§5), freshness indicator (§6), empty states (§7), watchlist promotion flow (§8), news panel (§9), skeleton loading (§10). DEV-01 in screener_results.md explicitly designates v3.0 as the news panel implementation target (ST-07).

**ST-11 (Design Required → Cleared):** ST-11 introduces a new user-facing UI element (keyboard shortcut reference in the sidebar footer). No prior spec existed. Head of UX & Design produced `ux_spec.md` v1.0; Product Owner approved; Frontend Specs owner updated `navigation.md` to v1.1; Head of Specs Team confirmed compliant.

**ST-15 (Design Pre-Approved):** `analytics.md` v1.7 §3 Advanced Metrics Grid already specifies `advanced_metrics.loss_streak` as a displayed field alongside Win Streak. ST-15 implements the backend computation that supplies this value and extends the metrics definitions spec. No new UI elements required; the display slot is already specced.

---

## Notes

- Design gate bypass authority was pre-recorded in `.claude_current_state.json` for v2.9 (no frontend UI in v2.9). This gate is the first active design gate for v3.0 as EPIC-02 contains frontend implementation.
- All 16 sprint stories classified; 1 Design Required item (ST-11) cleared with artefact produced; 0 blocked.
- Sprint Planning (`plan sprint --cycle 2026-04-25__release-v3.0`) may now proceed.
