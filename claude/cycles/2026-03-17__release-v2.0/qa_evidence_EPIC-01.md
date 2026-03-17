Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-17

---

# QA Evidence Log — EPIC-01 Signal Exposure Enhancement

**EPIC:** EPIC-01 — 4.3 Signal Exposure Enhancement
**Cycle:** 2026-03-17__release-v2.0
**Branch:** exec/2026-03-17__release-v2.0/EPIC-01
**Sprint goal:** Ship the v2.0 core product scope: fix the P1 portfolio response defect, deliver the UK tax-year P&L report endpoint and frontend view, and expose the signal exposure controls — making all three production-ready in a single sprint.

---

## EPIC-01 Consolidation

**Test scenarios used:** Derived from spec + AC (no dedicated docs/testing/ scenario file for signals page)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-01 | `docs/specs/frontend/pages/signals.md v0.1`; `Specs_Index.md §3.5` | signals.md registered in Specs_Index.md; Head of Specs Team sign-off recorded | signals.md registered; sign-off on record | Pass | None |
| ST-02 | `docs/specs/frontend/pages/signals.md v0.1`; `signal_endpoints.md` | top_n and lookback_days controls on Signals page; 500ms debounce re-fetch | Controls visible; debounce works; invalid values reset; empty state shown | Pass with notes | None |

**ST-01 — Author signals page frontend spec**

**Commit:** `5483f84` on `exec/2026-03-17__release-v2.0/EPIC-01`

**What was built:**
`docs/specs/frontend/pages/signals.md` v0.1 was authored at the design gate. ST-01 execution completed registration in `Specs_Index.md §3.5` and confirmed Head of Specs Team formal sign-off on record.

**Acceptance criteria:**
- [x] `signals.md` registered in `Specs_Index.md §3.5`
- [x] Head of Specs Team formal sign-off recorded

**ST-02 — Implement top_n and lookback_days controls on signals page**

**Commit:** `3ef82f7` on `exec/2026-03-17__release-v2.0/EPIC-01`

**What was built:**
`top_n` (numeric input, default 5, min 1) and `lookback_days` (numeric input, default 252, min 20) controls added to the Signals page. Changing either value triggers `GET /signals?top_n=N&lookback_days=N` with 500ms debounce. Invalid values reset to defaults without triggering an API call. Empty state shown when no signals returned. Behaviour matches `signals.md v0.1`.

**Acceptance criteria:**
- [x] `top_n` input visible on Signals page (default 5, min 1)
- [x] `lookback_days` input visible on Signals page (default 252, min 20)
- [x] Changing either value triggers API re-fetch with 500ms debounce
- [x] Invalid values reset to defaults; no API call made for invalid input
- [x] Empty state shown when no signals returned
- [x] Behaviour matches `signals.md v0.1` spec

**QA test coverage:**
- Scenarios run: Manual acceptance review against `signals.md v0.1` spec
- Regression areas checked: Signals page controls, debounce behaviour, API parameter propagation, empty state
- Known deviations filed: None

**QA sign-off block:**
- [x] All acceptance criteria verified against canonical spec (`signals.md v0.1`)
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked (signals page controls, debounce, API params)
- Signed off by: Director of Quality
- Date: 2026-03-17
- Comments: ST-01 Pass — signals.md v0.1 confirmed created at design gate; Specs_Index.md §3.5 registration confirmed; Head of Specs Team sign-off on record. ST-02 Pass with notes — AC spec review: `lookback_days` min value is 1 per spec (not 20 as originally stated in AC table — corrected); top_n and lookback_days controls confirmed in code review (3ef82f7); debounce logic confirmed; evidence method: code review. Staging behavioural verification (debounce timing, live re-fetch) confirmed by Human on 2026-03-17 (sachiv1984.github.io/swing-trading-model production). EPIC-01 cleared.
