Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-16

# Execution Escalations — 2026-11-11__release-v9.17

## ESC-EXEC-20261116-01

- **Raised at:** 2026-11-16T13:00:31Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-11__release-v9.17
- **Step:** STEP 3.1.D (EPIC-02 execution loop; in-story sequencing gate per `stage4_backlog_slice_addendum.md` ST-06 and `performance-page-brief/decision_record.md` §1)
- **ST/EPIC item:** ST-06 / EPIC-02 (BLG-FE-259)
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-06's build may not start until `docs/specs/frontend/pages/performance.md` exists, meets the brief §2 and carries a dated Head of UX & Design approval; AC 2 also needs a dated Metrics Definitions & Analytics Canonical Owner confirmation that every KPI keeps its canonical definition. The draft v1.0 is written. Two points need a ruling inside those approvals: (1) the §5 scope rule — one home per period-level KPI, with narrower-scope figures (tax year, month, market, exit reason, tag, cohort) kept with their breakdowns; (2) §5.2 — the Analytics page's browser-computed Sharpe, drawdown and other §1/§3 metrics are replaced by the server's canonical `GET /analytics/metrics` values, which can change some displayed values (brief §2.4 "the canonical one is kept" versus §2.8 "no recalculation").
- **Engine recommendation (non-binding):** approve the draft as written: the scope rule keeps every scoped breakdown intact, and §5.2 is the case brief §2.4 names; `metrics_definitions.md` §Sharpe Ratio already records the browser figure as non-canonical.
- **Owning authority:** Head of UX & Design (spec approval); Metrics Definitions & Analytics Canonical Owner (KPI confirmation)
- **Unblock criteria:** both dated confirmations recorded in `performance.md` §11 Change Log (and the KPI confirmation in `qa_evidence_EPIC-02.md` at sign-off), with any requested changes applied to the draft.
- **SLA due-by:** 2026-11-17T13:00:31Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Open
