**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-06-21
**Cycle:** 2026-06-21__release-v5.1
**Release:** v5.1
**Sprint Goal:** Deliver the SI-05 Phase 1 weekly Telegram digest (combining SI-01 compliance data and SI-03 red flag trends) and clear outstanding governance and QA debt — delivery verification prompt patch, SignalCard Playwright coverage, compliance_summary validation, and staged verification sprint protocol.
**Backlog Slice Source:** claude/cycles/2026-06-21__release-v5.1/stage4_backlog_slice.md (original)

---

# Sprint Backlog — 2026-06-21__release-v5.1

## Merge Order

**EPIC-02 → EPIC-03 → EPIC-01**

- `execution_state.json` owner: **EPIC-02** (first in merge order)
- EPIC-03 and EPIC-01 must check for `execution_state.json` before creating; if found, append their EPIC section
- **Shared files:** `openapi.yaml` owned by EPIC-01 (ST-01); EPIC-01 branch must rebase onto main after EPIC-02 and EPIC-03 merge before finalising changes to `openapi.yaml`

---

## Sprint Scope

### EPIC-02 — Governance Patch: Delivery Verification §-1.3 Tier 2 Fix

**Maps to:** S2-02
**Owner:** Head of Specs Team
**Estimated effort:** ~0.5 day
**Risk IDs:** RISK-03
**Execution sequence:** 1 (first — independent, lowest risk)

#### ST-03 — delivery_verification_prompt.md §-1.3 Tier 2: agent-mediated signer format acceptance

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** Must apply CLAUDE.md §6 governance file edit checklist in full (version bump, OPERATIONAL_GUIDE.md update, prompt_change_log.md entry). Well-established pattern. Carry-forward item from 2026-06-03__release-v5.0 (LL-RP-v5.0-D-2).

**Staging-only ACs:** None

---

### EPIC-03 — QA & Documentation Debt Clearance

**Maps to:** S2-03, S2-05, S2-06
**Owner:** QA Lead; Director of Quality; PMO Lead
**Estimated effort:** ~1 day
**Risk IDs:** None
**Execution sequence:** 2 (parallel with EPIC-02 — fully independent)

#### ST-04 — BLG-FE-61: SignalCard allocation_insufficient badge Playwright E2E coverage

**Owner:** QA Lead
**Estimated effort:** XS (<1 hour)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** 3rd consecutive carry-forward (v4.3, v4.6, v5.0). Now firm. BLG-GOV-72(c) default-autonomous applies — new test component against locked spec with Playwright feasibility confirmed. Source: BLG-FE-61 (carry-forward LL-RP-v5.0-CF-1).

**Staging-only ACs:** None

---

#### ST-05 — BLG-QA-43: compliance_summary field population validation

**Owner:** Director of Quality
**Estimated effort:** XS (~1–2 hours)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** Spot-check verification only — no implementation. Mismatch must be filed as P2 bug immediately if found.

**Staging-only ACs:** AC-01 (staging/production environment required for compliance_summary verification — Infrastructure & Operations Owner sign-off)

---

#### ST-06 — BLG-GOV-89: Staged verification sprint protocol document

**Owner:** PMO Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** Documentation only. Validated pattern from v4.7 (first use) and v5.0 (confirmed). File at `docs/operations/staged_verification_sprint_protocol.md`. Requires DoQ + PMO Lead sign-off.

**Staging-only ACs:** None

---

### EPIC-01 — SI-05 Phase 1: Weekly Strategy Integrity Digest

**Maps to:** S2-01, S2-04
**Owner:** Head of Backend Engineering; Head of Specs Team
**Estimated effort:** ~3 days
**Risk IDs:** RISK-01, RISK-02
**Execution sequence:** 3 (last — after EPIC-02; ST-02 before ST-01 within EPIC)

#### ST-02 — BLG-SPEC-45: SI-05 financial reporting scope verification

**Owner:** Head of Specs Team
**Estimated effort:** XS (~1 hour)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None (but must complete before ST-01 seals)

**Notes:** Review BLG-GOV-86 for financial reporting scope. Gate cleared (BLG-GOV-86 shipped v5.0). FR&R Owner sign-off required. Complete before ST-01 implementation seals.

**Staging-only ACs:** None

---

#### ST-01 — SI-05 Phase 1: Backend service + Telegram weekly digest implementation

**Owner:** Head of Backend Engineering
**Estimated effort:** M (~2–3 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** ST-02 (must complete first — scope verification before implementation seals); EPIC-02 merged (governance patch before SI-05 impl)

**Notes:** RISK-01 gate confirmed cleared at sprint planning (SI-01 + SI-03 live ≥ 30 days; 2026-06-21 = 30 days post SI-03 ship ✓). RISK-02: API contract + openapi.yaml + test.py registration all in same commit per CLAUDE.md §2. Uses BLG-GOV-86 Telegram format spec and v2.4 weekly digest pattern. No SI-02 dependency in Phase 1.

**Staging-only ACs:** AC-07 (Telegram message received and formatted correctly on staging — Infrastructure & Operations Owner sign-off required)

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~12–14 working days |
| Total estimated effort (in-scope) | ~4.5 days |
| Utilisation | ~32–38% |
| Over-allocation | No |

## Items Deferred This Sprint

None. All 6 backlog slice items included.

## Deferred Execution Blockers Accepted

None — `deferred_execution_blockers` was empty at release planning.

## Outstanding Actions at Planning Seal

None.

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed
**Scope confirmed:** Confirmed — 6 stories, 3 EPICs, ~4.5 days estimated effort, within 12–14 day capacity
**Capacity confirmed:** Confirmed — PASS (no WARN)
**Deferred execution blockers accepted (if any):** N/A
**Signed off by:** Product Owner
**Date:** 2026-06-21
