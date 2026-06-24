**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-24
**Cycle:** 2026-06-24__release-v6.2

---

# Design Gate Record — 2026-06-24__release-v6.2

## Gate Status: PASSED

Completed: 2026-06-24
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

---

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | Nightly trailing stop computation — backend service | Design Not Applicable | Pure backend computation and storage; UI display handled by ST-02 | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-02 | Trailing stop display and breach badge — frontend | Design Required | New UI elements: Trail Stop column, breach badge with distinct colour/icon | `docs/design/2026-06-24__release-v6.2/trailing-stop-display/ux_spec.md` | `docs/specs/frontend/pages/positions.md` v1.8 | ✅ Cleared | Product Owner |
| ST-03 | Month-end rebalance exit signal generation | Design Required | AC-05: `exit_rebalance` signals require visually distinct label/styling in UI | `docs/design/2026-06-24__release-v6.2/rebalance-exit-signal-style/ux_spec.md` | `docs/specs/frontend/pages/signals.md` v0.4 | ✅ Cleared | Product Owner |
| ST-04 | Inverse-volatility position sizing for signal-driven entries | Design Not Applicable | Pure backend computation; inv-vol fields are API response additions only; no UI changes | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-05 | Risk-off exit alerts for existing positions | Design Required | AC-02: `risk_off_exit` alert visible per position, visually distinct from other indicators | `docs/design/2026-06-24__release-v6.2/risk-off-exit-alert/ux_spec.md` | `docs/specs/frontend/pages/positions.md` v1.8 | ✅ Cleared | Product Owner |
| ST-06 | AI daily briefing — backend endpoint | Design Not Applicable | Pure backend/API endpoint; UI display handled by ST-07 | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-07 | AI Daily Briefing card — frontend | Design Required | New full-width card on Dashboard; new UI component with advisory label and action list | `docs/design/2026-06-24__release-v6.2/ai-daily-briefing-card/ux_spec.md` | `docs/specs/frontend/pages/dashboard.md` v2.3 | ✅ Cleared | Product Owner |
| ST-08 | Conversational AI trade advisor — backend endpoint | Design Not Applicable | Pure backend/API endpoint; UI display handled by ST-09 | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 | AI chat widget — frontend | Design Required | New floating chat widget (Positions page primary); advisory-only; §13 compliant | `docs/design/2026-06-24__release-v6.2/ai-chat-widget/ux_spec.md` | `docs/specs/frontend/pages/positions.md` v1.8 | ✅ Cleared | Product Owner |
| ST-10 | execution_prompt autonomous class hard gate (BLG-GOV-135) | Design Not Applicable | Governance document patch; no user-visible UI effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 | execution_prompt test_scenarios path validation (BLG-GOV-136) | Design Not Applicable | Governance document patch; no user-visible UI effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 | api_performance_baseline.md — 2 new v6.1 endpoint measurements (BLG-OPS-75) | Design Not Applicable | Operations documentation update; no UI changes | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 | Playwright spec auto-registration via glob pattern (BLG-QA-62) | Design Not Applicable | CI/CD infrastructure change; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |

---

## Blocked Items

None.

---

## Notes

**ST-03 — `stop_exit` signal type badge (conditional):** The PO review noted that `stop_exit` badge styling was specified alongside the new `exit_rebalance` badge. Implementation team must confirm `stop_exit` is a live API value returned by `GET /signals` before applying the red badge. If `stop_exit` is not yet a live signal type, the red badge is deferred to the sprint that introduces it. This is not a gate blocker — it is an implementation pre-check for ST-03.

**ST-09 — Signals page placement (sprint planning scope):** Product Owner scoped ST-09 implementation to the Positions page as the canonical target. Signals page placement is a capacity-dependent stretch goal. Sprint planning must not treat Signals placement as in-scope unless capacity is explicitly confirmed at sprint planning seal. If deferred, file a follow-on backlog item.

**ST-02 — Table column density:** Implementation team should monitor horizontal scroll behaviour with ~15 Table View columns. If layout testing reveals excessive width, Initial Stop + Trail Stop may be combined into a two-line cell without requiring a spec amendment — this is an implementation-level layout decision within the spec's intent.

**ST-05 — Colour family note:** RISK OFF badge (`#1E40AF`, blue-800) and GRACE lifecycle badge (`#2563EB`, blue-600) share the blue family. They appear in separate columns (Alerts vs Status) with distinct labels. PO accepted Head of UX & Design's justification; no spec change required.

**EPIC-02 §13 pre-condition:** EPIC-02 (ST-06–ST-09) carries a pre-sprint-planning gate requiring Strategy Rules & System Intent Owner §13 review for BLG-FEAT-50 and BLG-FEAT-51. This is a Sprint Planning pre-condition, not a Design Gate condition. Sprint Planning must not seal until this review is recorded in the decisions document.
