**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-07-06
**Cycle:** 2026-07-06__release-v6.7
**Release:** v6.7
**Sprint Goal:** Eliminate app-wide secondary-text WCAG-AA contrast failures across both dark and light themes and lock the fix into a shared design token, while closing out the full AUD-2026-07-06 governance-hardening backlog (including the 3-cycle-carried `.claude/skills/` write-scope escalation).
**Backlog Slice Source:** Original — `stage4_backlog_slice.md`

# Sprint Backlog — 2026-07-06__release-v6.7

**Merge order:** EPIC-02 → EPIC-01 (EPIC-02 is fully autonomous with no dependency on EPIC-01; EPIC-01 sequences ST-01 → ST-02 → ST-03 internally). **`execution_state.json` owner: EPIC-02** (first in execution order — see `sprint_planning_notes.md` Multi-EPIC Execution Notes). No shared source files identified across EPIC-01/EPIC-02 this sprint (see `sprint_planning_notes.md` Shared File Ownership Advisory).

## Sprint Scope

### EPIC-02 — Governance Process Hardening

**Maps to:** S2-04, S2-05, S2-06, S2-07
**Owner:** Head of Specs Team
**Estimated effort:** ~3.2 days
**Risk IDs:** RISK-03, RISK-04
**Execution sequence:** 1 (runs first — fully autonomous, no dependency on EPIC-01)

#### ST-04 — `.claude/skills/` write-scope authority + commit-check patch (BLG-GOV-167)

**Owner:** Head of Specs Team
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** Resolves the 3-cycle-carried `/commit-check` write-scope escalation (`ESC-CLOSE-20260706-01`) — do not let a 4th cycle pass unresolved. RISK-03: scope narrowly to `.claude/skills/` only, naming Head of Specs Team explicitly.

**Staging-only ACs:** None — all 3 ACs verifiable by direct file read.

---

#### ST-05 — Structural guard for 4 append-only governance logs (BLG-GOV-168)

**Owner:** Head of Specs Team
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** RISK-04: AC-03 requires direct read-verification of all 4 affected engines' actual write steps post-change — not documentation alone. This is the exact failure mode that produced BLG-GOV-168 originally (documentation-only patch, zero adoption).

**Staging-only ACs:** None — all 3 ACs verifiable by direct file read.

---

#### ST-06 — `audit.py` SLA — same-session commit requirement (BLG-GOV-169)

**Owner:** Head of Specs Team
**Estimated effort:** XS (<1 hour)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None — may run in parallel with ST-04/ST-05

**Notes:** Single-line SLA block addition.

**Staging-only ACs:** None.

---

#### ST-07 — Delivery Verification STEP 6 status-line documentation (BLG-GOV-170)

**Owner:** Head of Specs Team
**Estimated effort:** XS (<1 hour)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None — may run in parallel with ST-04/ST-05

**Notes:** Documents existing correct behaviour; no functional change.

**Staging-only ACs:** None.

---

### EPIC-01 — UX & Accessibility Contrast Remediation

**Maps to:** S2-01, S2-02, S2-03
**Owner:** Head of UX & Design; Head of Engineering
**Estimated effort:** ~7.5 days
**Risk IDs:** RISK-01, RISK-02
**Execution sequence:** 2 (runs after EPIC-02; internal order ST-01 → ST-02 → ST-03 is a hard sequencing constraint)

#### ST-01 — Dark-theme secondary-text contrast fix (BLG-FE-87)

**Owner:** Head of UX & Design; Head of Engineering
**Estimated effort:** L (~2–3 days)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (first in EPIC-01 sequence)

**Notes:** Design gate cleared (`design_gate.md` — Design Required, ✅ Cleared). Frontend spec versions locked: `docs/specs/frontend/pages/positions.md` v2.0, `dashboard.md` v2.6, `reflections.md` v0.2. RISK-01: Playwright coverage or recorded staging sign-off required per CLAUDE.md frontend-visible-change rule; per-surface contrast spot-checks recorded.

**Staging-only ACs:** None — AC-03 offers Playwright coverage as a CI-capable evidence path (staging sign-off is an alternative, not exclusive).

---

#### ST-02 — Light-theme secondary-text contrast fix (BLG-FE-88)

**Owner:** Head of UX & Design; Head of Engineering
**Estimated effort:** L (~3–4 days)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** ST-01 (must complete first — sequence after to avoid rework; RISK-02 mitigation)

**Notes:** Design gate cleared (`design_gate.md` — Design Required, ✅ Cleared, same artefact as ST-01). Do not begin branch work on ST-02 until ST-01 has merged to main.

**Staging-only ACs:** None — AC-03 offers Playwright coverage or a recorded manual light-theme QA pass; not CI-incapable.

---

#### ST-03 — Shared secondary-text design token (BLG-FE-89)

**Owner:** Head of UX & Design; Head of Engineering
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** ST-01, ST-02 (recommended sequencing — documents the canonical treatment based on the concrete fixes landed)

**Notes:** Design gate cleared — decision fully locked in `docs/design/2026-07-06__release-v6.7/secondary-text-contrast/ux_spec.md` (§3, §6). Execution's job is verbatim transcription into `design_system.md` §Color Usage / §Accessibility — QA evidence must verify the transcription matches the artefact exactly (per `design_gate.md` Notes).

**Staging-only ACs:** None — documentation-only, both ACs verifiable by direct read.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~12–14 days |
| Total estimated effort (in-scope) | ~10.7 days |
| Utilisation | ~76–89% |
| Over-allocation | No |

## Items Deferred This Sprint

None — all 7 ST items from the authoritative backlog slice are in scope.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| None. | — | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — 2026-07-06 (see `sprint_goal.md`)
**Scope confirmed:** Confirmed — 7 ST items across EPIC-01/EPIC-02, all Firm, no deferrals
**Capacity confirmed:** Confirmed — ~10.7 days within ~12–14 day capacity, no over-allocation, no WARN acknowledgement required
**Deferred execution blockers accepted (if any):** N/A — `deferred_execution_blockers` empty in `state.json`
**Signed off by:** Product Owner
**Date:** 2026-07-06
