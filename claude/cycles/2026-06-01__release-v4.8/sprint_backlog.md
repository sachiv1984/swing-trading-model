**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-06-01
**Cycle:** 2026-06-01__release-v4.8
**Release:** v4.8
**Sprint Goal:** Resolve all firm v4.8 governance and operations debt items — closing the §13 OPERATIONAL_GUIDE register gap, remediating agent charter header non-compliance, establishing build minutes monitoring policy, completing the post-v4.7 dependency audit, and updating the QA coverage matrix — clearing the decks ahead of the SI-05 Phase 1 gate window (2026-06-21).
**Backlog Slice Source:** original — `claude/cycles/2026-06-01__release-v4.8/stage4_backlog_slice.md`

---

# Sprint Backlog — 2026-06-01__release-v4.8

---

## Merge Order and Multi-EPIC Notes

**EPIC merge sequence:** EPIC-01 → EPIC-02

**execution_state.json owner:** EPIC-01. EPIC-02 must check for `execution_state.json` existence before creating; if found, append EPIC-02's section rather than overwriting.

**Shared files advisory:**
- `claude/backlog/backlog.md`: Both EPICs may append new BLG items (ST-03 and ST-05). Non-conflicting rows — EPIC-02 branch should pull from main after EPIC-01 merges before finalising any backlog.md changes.
- `claude/system/OPERATIONAL_GUIDE.md` and `claude/system/prompt_change_log.md`: EPIC-01 owns; EPIC-02 does not write these files.

---

## Sprint Scope

### EPIC-01 — Governance & Compliance Hardening

**Maps to:** S2-01
**Owner:** Head of Specs Team
**Estimated effort:** ~1.5 dev-days
**Risk IDs:** RISK-03
**Execution sequence:** 1 (execution_state.json owner)

---

#### ST-01 — §13 register completion (BLG-GOV-69)

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Notes:** OPERATIONAL_GUIDE.md version bump and prompt_change_log.md entry mandatory per CLAUDE.md §6. Complements AUD-2026-05-30 Tier 1 patches already applied — verify current OPERATIONAL_GUIDE.md version before bumping.

**Staging-only ACs:** None

---

#### ST-02 — Agent charter header compliance remediation (BLG-GOV-70)

**Owner:** Director of HR; Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** 2 files to fix: `claude/agents/api_contracts_documentation_owner.md` (## Role → **Role:**) and `claude/agents/backend_engineering_patterns_owner.md` (**Owner:** → **Role:**). Verify all other agent files clean post-fix.

**Staging-only ACs:** None

---

#### ST-03 — AUD-2026-05-30-006 gap resolution verification (BLG-GOV-72)

**Owner:** PMO Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** If unresolved patches found, file new BLG-GOV items — do not expand sprint scope inline (RISK-03 disposition). Sprint planning notes carry-forward item 2 (null commit_sha monitor) is relevant context for this review.

**Staging-only ACs:** None

---

### EPIC-02 — Operations, Security & QA Debt

**Maps to:** S2-02
**Owner:** Infrastructure & Operations Owner; Head of Specs Team
**Estimated effort:** ~1.5–2.5 dev-days (firm) + ~1–2 dev-days (conditional)
**Risk IDs:** RISK-02
**Execution sequence:** 2

---

#### ST-04 — Build minutes monitoring policy (BLG-OPS-46)

**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** Document-only story. Establish monthly allocation, v4.6–v4.7 consumption history, 80% threshold, billing reset date, and double-capacity cadence assessment.

**Staging-only ACs:** None

---

#### ST-05 — Dependency audit post-v4.7 (BLG-OPS-47)

**Owner:** Head of Engineering; Cybersecurity & Trust Lead
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** Run both pip-audit (pre-sprint confirmed clean) and npm audit. Check Anthropic SDK version (current: 0.40.0). If HIGH/CRITICAL CVEs found, file P0/P1 BLG-OPS items — sprint scope expansion for CVE fix permitted without amendment (RISK-02 disposition). Document in security_register.md.

**Staging-only ACs:** None

---

#### ST-06 — Coverage matrix update and v4.7 contract verification (BLG-QA-39)

**Owner:** QA Lead; API Contracts & Documentation Owner
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** Verify compliance_summary field (v4.7 ST-03) is captured in QA coverage matrix with regression test reference. Verify GET /reports/monthly-pnl v0.6 contract in docs/specs/api_contracts/. File BLG-SPEC items if contract gaps found.

**Staging-only ACs:** None

---

#### ST-07 — SI-04 strategy version comparison endpoint contract (BLG-SPEC-43)

**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Estimated effort:** S–M (~1–2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** PO confirmed SI-04 is on the medium-term roadmap (2026-06-01). No implementation required — contract pre-authoring only. openapi.yaml placeholder entry required per CLAUDE.md §2.

**Staging-only ACs:** None

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~12–14 dev-days |
| Total estimated effort (7 stories in scope) | ~4–6 dev-days |
| Utilisation | ~30–45% |
| Over-allocation | No |

---

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| ST-08 — SI-05 Phase 1 implementation | EPIC-03 | Gate NOT MET — SI-01 + SI-03 live ≥ 30 days; gate clears 2026-06-21; today 2026-06-01 |

---

## Deferred Execution Blockers Accepted

*(None — deferred_execution_blockers was empty in release plan state.json)*

---

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Append sprint_planning_prompt.md v3.6→v3.8 entries to prompt_change_log.md | Head of Specs Team | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed
**Scope confirmed:** Confirmed — 7 stories (EPIC-01: ST-01/02/03; EPIC-02: ST-04/05/06/07); EPIC-03 ST-08 deferred (gate NOT MET)
**Capacity confirmed:** Confirmed — ~4–6 dev-days estimated; ~12–14 available; no over-allocation
**Deferred execution blockers accepted (if any):** N/A
**Signed off by:** Product Owner
**Date:** 2026-06-01
