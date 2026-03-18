**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-18
**Cycle:** 2026-03-18__release-v2.1
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Escalations — 2026-03-18__release-v2.1

---

## ESC-DG-20260318-01 — Design Gate Blocked: 6 items require design artefacts

**Raised:** 2026-03-18
**Raised by:** Design Gate Engine (PMO Lead)
**Severity:** Gate Blocker
**Status:** Resolved

**Summary:** The Design Gate run for cycle 2026-03-18__release-v2.1 completed with status BLOCKED. Sprint Planning (`plan sprint`) is blocked until all 6 Design Required items have approved design artefacts and updated frontend specs.

**Blocked Items:**

| Item | Blocker |
|------|---------|
| ST-05 — Notification preferences page | No design artefact; `notifications.md` frontend spec absent |
| ST-06 — In-app notification feed | No design artefact; `notifications.md` frontend spec absent |
| ST-10 — Watchlist UI | No design artefact; `watchlist.md` frontend spec absent |
| ST-11 — Chart interactivity (CHART-IX) | No design artefact; analytics.md v1.4 has no tooltip/zoom/drill-down spec |
| ST-12 — Tax Year P&L PDF Export | No design artefact; reports.md v0.1 has no PDF download control defined |
| ST-14 — Slippage Tracking | No design artefact; no spec covers slippage display location or format |

**Resolution path:**
1. Head of UX & Design produces artefacts for all 6 items (paths defined in design_gate.md)
2. Product Owner approves each artefact
3. Frontend Specs & UX Documentation Owner updates relevant frontend spec files
4. Head of Specs Team confirms compliance
5. PMO Lead re-runs `run design-gate --cycle 2026-03-18__release-v2.1` to clear gate

**Required by:** Before `plan sprint` is issued.

**Resolution:** Resolved — all 6 Design Required items cleared on 2026-03-18. Design gate status updated to Passed. Sprint Planning is now unblocked.
