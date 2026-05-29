**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-29
**Cycle:** 2026-05-29__release-v4.3

---

# Sprint Planning Notes — 2026-05-29__release-v4.3

---

## Backlog Slice Source

Original — `claude/cycles/2026-05-29__release-v4.3/stage4_backlog_slice.md`

No amendment file present. `amended_backlog_slice_path` is absent/empty in `.claude_current_state.json`.

---

## Carry-Forward Items

Carry-forward items reviewed: 3 items from cycle `2026-05-27__release-v4.2` (per `lessons_learnt_closure.md ##Carry-Forward`).

| # | Observation | Sprint Backlog Item | Status |
|---|-------------|--------------------|-|
| 1 | `qa_signed_off` stale state: execution_state.json not updated in same commit as QA evidence sign-off | ST-01 (EPIC-01, Sprint 1) | ✅ Addressed |
| 2 | Branch safety gap at sprint close: execution_prompt.md STEP 8 has no branch safety check | ST-02 (EPIC-01, Sprint 1) | ✅ Addressed |
| 3 | QA evidence AC mapping 1:1 advisory needed in qa_evidence_template.md | ST-03 (EPIC-01, Sprint 1) | ✅ Addressed |

All 3 carry-forward items are in Sprint 1 EPIC-01 as sprint-seal prerequisites. No carry-forward items remain unaddressed.

---

## Capacity WARN Acknowledgement

⚠ WARN: Total estimated effort ~20 hrs across 2 sprints is at the upper bound of confirmed solo-dev evening capacity (~20–24 hrs). Sprint 2 (EPIC-02 + EPIC-03, ~12 hrs) is the tighter sprint.

**Product Owner acceptance:** PO issued `plan sprint` with awareness of this WARN from release planning. Risk explicitly acknowledged. Mitigating factors: (1) staging verifications (ST-06/07/08/13/14) are human-delegate tasks with minimal engine effort; (2) Sprint 1 has ~2–6 hrs buffer which can be used if Sprint 2 items slip; (3) all Sprint 2 items are documentation/verification tasks with well-defined ACs.

`capacity_warn_acknowledged = true`

---

## Deferred Items

No items deferred from the backlog slice. All 18 stories are included across 2 sprints.

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| *(none)* | — | — |

---

## Dependency Map

| Item | Depends On | Type | Resolution |
|------|-----------|------|------------|
| ST-06 (Claude thesis staging) | ST-13 (staging parity audit) | Cross-EPIC prerequisite | ST-13 runs first in Sprint 2 before ST-06/07/08 |
| ST-07 (ticker validation staging) | ST-13 (staging parity audit) | Cross-EPIC prerequisite | ST-13 runs first in Sprint 2 before ST-06/07/08 |
| ST-08 (cost threshold staging) | ST-13 (staging parity audit) | Cross-EPIC prerequisite | ST-13 runs first in Sprint 2 before ST-06/07/08 |
| ST-02 (branch safety decision + patch) | HoST gate/advisory decision | Delegated decision prerequisite | HoST decision required before implementation |
| All others | None | — | No dependencies |

Circular dependencies: None detected.

---

## Execution Sequence

### Sprint 1

**EPIC-01 — Governance Patch Resolution** (execution order: 1)
1. ST-01 — autonomous — execution_prompt.md qa_signed_off advisory patch
2. ST-03 — autonomous — qa_evidence_template.md AC mapping advisory
3. ST-04 — autonomous — staging-only AC pre-designation reference table
4. ST-05 — autonomous — AI feature inventory document
5. ST-02 — delegated_decision — sprint close branch safety advisory (HoST must decide gate vs advisory, then implement)

*ST-01/03/04/05 can run in parallel (all autonomous). ST-02 requires HoST decision first; implementation follows once decision is recorded in AC-01.*

**EPIC-04 — Frontend Polish & Arc 5 Feature** (execution order: 2, after EPIC-01 merges)
6. ST-16 — delegated_frontend — pre-entry check entry price bug fix
7. ST-17 — delegated_frontend — Claude thesis generation UI copy audit
8. ST-18 — delegated_frontend — Arc 5 compliance score in monthly P&L report

*ST-16/17/18 are sequential within EPIC-04 (all Base44 frontend delegation).*

### Sprint 2

**EPIC-03 — Operations & Security Hardening** (execution order: 3, Sprint 2 first)
1. ST-13 — delegated_qa — staging environment parity audit (**must run first** — prerequisite for ST-06/07/08)
2. ST-14 — delegated_qa — claude-audit-log performance baseline (after ST-13)
3. ST-15 — autonomous — API key rotation policy and external API key security register (parallel to ST-14)

**EPIC-02 — QA Debt & Test Coverage** (execution order: 4, after ST-13 confirms staging parity)
4. ST-06 — delegated_qa — staging verification: Claude thesis generation (after ST-13)
5. ST-07 — delegated_qa — staging verification: ticker validation live (after ST-13)
6. ST-08 — delegated_qa — staging verification: Claude API cost threshold alert (after ST-13)
7. ST-09 — autonomous — Playwright E2E for Arc5ComplianceSection
8. ST-10 — autonomous — Arc 5 end-to-end integration test specification
9. ST-11 — autonomous — CI pipeline execution time baseline measurement
10. ST-12 — autonomous — Playwright scenario coverage matrix and Arc 5 coverage audit

*ST-06/07/08 are human-delegate staging tasks, blocked on ST-13 staging parity confirmation. ST-09/10/11/12 are autonomous and can run in parallel once staging confirmation is received.*

---

## Multi-EPIC Execution Notes

**Sprint 1 merge order:** EPIC-01 → EPIC-04

**Sprint 2 merge order:** EPIC-03 → EPIC-02

**execution_state.json owner:** EPIC-01 is the designated owner for the cycle. All other EPIC branches must check for `execution_state.json` existence before creating their own section — read and append their EPIC data rather than overwrite. This prevents execution-state collisions per STEP 5.2 protocol.

**Shared files across EPICs:**
- `execution_state.json` — owned by EPIC-01. All EPICs append; do not overwrite.
- `openapi.yaml` — not modified by any v4.3 EPIC (no new endpoints in scope).
- Source code files — no cross-EPIC overlap identified. EPIC-01/02/03 are documentation/spec only. EPIC-04 modifies: backend monthly-pnl endpoint, frontend P&L component, pre-entry validation component. No other EPIC touches these files.

**Later EPICs rebase advisory:** EPIC-04 must rebase onto `main` after EPIC-01 merges before finalising its changes. EPIC-02 must rebase onto `main` after EPIC-03 merges before finalising its changes.

---

## AC Confirmation and Staging-Only Designations

All 18 stories have defined acceptance criteria in `stage4_backlog_slice.md`. No `[AC REQUIRED]` placeholders issued.

**ST-18 AC-04 Playwright designation (required by cycle_summary.md Sprint Planning Prerequisite):**
Playwright mocking IS feasible for ST-18. `GET /analytics/arc5-compliance` can be mocked with `page.route()` in Playwright test setup. AC-04 ("Strategy Compliance" heading visible, 2+ metric fields present) is NOT staging-only — Playwright CI verification is the evidence path. `**Staging-only ACs:** None` for ST-18.

**Staging-only ACs summary:**
| Story | Staging-only ACs |
|-------|-----------------|
| ST-06 | AC-01, AC-02, AC-03, AC-04 (all — requires live ANTHROPIC_API_KEY) |
| ST-07 | AC-01, AC-02 (requires live internet + staging env) |
| ST-08 | AC-01, AC-02 (requires live TELEGRAM_BOT_TOKEN + claude_audit_log rows) |
| ST-13 | AC-01, AC-02, AC-03 (requires staging access) |
| ST-14 | AC-01 (requires live environment timing run) |
| ST-18 | None (Playwright mocking feasible — designated at sprint planning 2026-05-29) |
| All others | None |

---

## Risk Flags

| Risk ID | Associated Item | Mitigation | Status |
|---------|----------------|------------|--------|
| RISK-01 | EPIC-01 (ST-01/02/03) | All 3 OA items in Sprint 1; ST-01/02/03 are EPIC-01 stories. 2nd-recurrence escalation avoided. | Valid — addressed in Sprint 1 |
| RISK-02 | EPIC-02 (ST-06/07/08) | ST-13 staging parity runs first in Sprint 2; blocks staging verifications until confirmed | Valid — mitigated by Sprint 2 sequence |
| RISK-03 | EPIC-03 (ST-13) | EPIC-03 sequenced first in Sprint 2; ST-13 is first story in EPIC-03 execution | Valid |
| RISK-04 | EPIC-04 (ST-18) | Playwright mocking designated feasible at sprint planning; AC-04 is not staging-only; evidence path: Playwright CI | Valid — resolved at planning |

---

## Pre-Sprint Vulnerability Scan

pre-sprint pip-audit: **CLEAN**

Command: `pip-audit -r backend/requirements.txt --format=json`
Result: 0 vulnerabilities found across 60 dependencies (including anthropic v0.40.0, fastapi v0.135.1, starlette v1.0.1, sqlalchemy v2.0.23, pydantic v2.7.0, yfinance v1.3.0).

No High/Critical CVEs to report. No PO acceptance of vulnerability risk required.

---

## Pre-Sprint Backlog Advisory

No backlog items with `Provisional-Target: Before v4.3 sprint planning` found.

---

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Product Owner sign-off on sprint goal | Product Owner | Yes |
| Product Owner sign-off on sprint backlog | Product Owner | Yes |
| Head of Specs Team — ST-02 gate/advisory decision (AC-01) must be recorded before EPIC-01 sprint execution begins | Head of Specs Team | No (before EPIC-01 start, not before seal) |
