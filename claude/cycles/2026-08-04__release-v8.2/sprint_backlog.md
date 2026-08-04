# Sprint Backlog — 2026-08-04__release-v8.2

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-08-04
**Cycle:** 2026-08-04__release-v8.2
**Release:** v8.2
**Sprint Goal:** Ship v8.2's curated full-capacity scope — five ready user-facing/UX improvements leading the release, staging/production security hardening, an 11-item governance-process integrity cluster, CI/operations hardening, and QA/spec debt cleanup — advancing the release's explicit "user features first" priority within the confirmed capacity band.
**Backlog Slice Source:** original `stage4_backlog_slice.md`

## Merge Order

**EPIC merge sequence:** EPIC-01 → EPIC-03 → EPIC-04 → EPIC-05 → EPIC-02 (see `sprint_planning_notes.md §Execution Sequence` for full rationale — all-`autonomous` EPICs sequenced first, with EPIC-01 leading per the release's "user features first" instruction and its already-cleared Design Gate; EPIC-02, the sprint's only `delegated_backend` EPIC, sequenced last).

**`execution_state` owner:** EPIC-01 owns `execution_state/_cycle_meta.json` (cycle-level fields, first EPIC to open). Each EPIC branch owns and writes only its own `execution_state/EPIC-xx.json` per the current per-EPIC mechanism (`shared_standards.md` §12.1) — there is no shared file for EPIC branches to conflict on.

**Shared files across EPICs:** `claude/system/design_gate_prompt.md` (EPIC-03/ST-16 and EPIC-05/ST-25 — EPIC-05 must rebase onto `main` after EPIC-03 merges before finalising its edit); `execution_state/_cycle_meta.json` (EPIC-01 only). Full ownership table: `sprint_planning_notes.md §Multi-EPIC Execution Notes`.

---

## Sprint Scope

### EPIC-01 — User-Facing Features & UX

**Maps to:** S2-01
**Owner:** Financial Reporting & Records Owner; Head of UX & Design; Metrics Definitions & Analytics Canonical Owner
**Estimated effort:** 6.0 days (M+S+XS+S+S)
**Risk IDs:** RISK-01
**Execution sequence:** 1

#### ST-01 — P&L / tax record reconciliation report (system totals vs individual trade export)

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** 2.5 (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

*(The Execution Engine reads AC from `stage4_backlog_slice.md` directly via `spec_references`. Do not duplicate the full AC table here — the sprint backlog is a sequencing and ownership document.)*

**Dependencies:** None

**Notes:** Design Gate PASSED (Design Required — `pnl-reconciliation-report/decision_record.md`; `reports.md` bumped 0.12→0.13).

**Staging-only ACs:** None — observable UI (new view rendering) is Playwright-verifiable in CI per CLAUDE.md §2's general observable-AC rule, not the staging-only-evidence exception.

**Status at sprint open: ready**

---

#### ST-02 — Compliance Recheck Modal all-pass empty-state design

**Owner:** Head of UX & Design
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** Design Gate PASSED (Design Required — `compliance-recheck-all-pass-state/decision_record.md`; `positions.md` bumped 2.6→2.7).

**Staging-only ACs:** None — Playwright-verifiable in CI.

**Status at sprint open: ready**

---

#### ST-03 — RFJ event type colour palette refinement

**Owner:** Head of UX & Design
**Estimated effort:** 0.5 (XS)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** Design Gate PASSED (Design Pre-Approved — fix already fully specified in the v6.0 RFJ design review; live code checked against that review's pre-fix colours to confirm no drift).

**Staging-only ACs:** None — Playwright-verifiable in CI (colour-token assertions).

**Status at sprint open: ready**

---

#### ST-04 — Trade Plan native form fields use a weaker focus indicator than the rest of the codebase

**Owner:** Head of UX & Design
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** Design Gate PASSED (Design Pre-Approved — implementation bug against `design_system.md` v1.4's already-mandated pattern).

**Staging-only ACs:** None — Playwright-verifiable in CI (focus-ring assertions).

**Status at sprint open: ready**

---

#### ST-05 — Drift-detection metric for the behavioural-drift endpoint's `insufficient_data` streak

**Owner:** Metrics Definitions & Analytics Canonical Owner
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** Design Gate PASSED (Design Pre-Approved — reuses the existing `SI02GateStatusSection` stat-grid pattern verbatim).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-03 — Governance Process Integrity Cluster

**Maps to:** S2-03
**Owner:** Product Owner; Infrastructure & Operations Owner; Metrics Definitions & Analytics Canonical Owner; Head of Specs Team; AI Compliance & Governance Officer; PMO Lead; Strategy Rules & System Intent Owner; Head of Engineering
**Estimated effort:** 10.85 days (XS+S+S+S+S+M+S+S+S+S+S)
**Risk IDs:** None
**Execution sequence:** 2

#### ST-08 — File SI-05 Phase 1 30-day effectiveness review record

**Owner:** Product Owner
**Estimated effort:** 0.1 (XS)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** Phase 2 activation decision (PROCEED/ITERATE/PAUSE) recorded as part of the record itself.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-09 — `velocity_metrics.md` row-count audit against cycle folder count

**Owner:** PMO Lead
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** None

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-10 — Confirm Arc 5 composite formula accounts for v6.9 recheck events

**Owner:** Metrics Definitions & Analytics Canonical Owner
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** None

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-11 — Rebalance-skip advisory should verify next release is actually scoped

**Owner:** Head of Specs Team
**Estimated effort:** 0.5 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** Governance file edit checklist applies (`post_ship_closure.md` version bump, `OPERATIONAL_GUIDE.md` §14 sync, `prompt_change_log.md` entry).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-12 — AI vendor Terms-of-Service & data-processing review (Gemini/Claude, financial data handling)

**Owner:** AI Compliance & Governance Officer
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** None

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-13 — Direct-write / governance-bypass pattern tracker (roadmap & amendment gate bypasses)

**Owner:** PMO Lead
**Estimated effort:** 2.5 (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** Backfill with known historical instances (v7.4 AMD, v7.5, v7.6 DL-073, v7.7 DL-074, and others).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-14 — Idea-intake backlog-overlap check effectiveness retrospective (v2.8, post-N-windows)

**Owner:** PMO Lead
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** None

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-15 — SI-02 production credential provisioning decision (formalise fallback vs acquire)

**Owner:** Product Owner
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** Two alternative remediation paths named in the item's own AC — resolve the choice at execution kickoff (see `sprint_planning_notes.md §Risk Flags`, LP-14 check). If option (a) is chosen, the actual credential provisioning sub-step requires `delegated_backend` handling.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-16 — Mandatory §13 boundary pre-check at design gate for new AI-calling feature proposals

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Notes:** Governance file edit checklist applies to `design_gate_prompt.md`. Shared-file — see Merge Order (EPIC-05/ST-25 also touches this file; EPIC-03 merges first).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-17 — Codify a `Last Updated` header-history retention convention

**Owner:** Head of Specs Team
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None

**Notes:** Governance file edit checklist applies to `shared_standards.md`, `roadmap_prompt.md`, `idea_intake_prompt.md`.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-18 — governance_sync.yml auto-close regex cannot distinguish delegation commits

**Owner:** Head of Engineering
**Estimated effort:** 0.75 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** Convention documented in `shared_standards.md` §8.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-04 — Operations & CI Hardening

**Maps to:** S2-04
**Owner:** Head of Engineering; Infrastructure & Operations Owner
**Estimated effort:** 3.0 days (S+S+S)
**Risk IDs:** None
**Execution sequence:** 3

#### ST-19 — Quarterly dependency-upgrade cadence for backend/requirements.txt

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None

**Notes:** None

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-20 — CI cache tuning to reduce Playwright suite runtime

**Owner:** Head of Engineering
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** None

**Notes:** None

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-21 — Automated commit-message format lint (pre-commit hook)

**Owner:** Head of Engineering
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None

**Notes:** None

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-05 — QA & Spec Debt Cleanup

**Maps to:** S2-05
**Owner:** QA & Testing Owner; Head of Specs Team; Head of Engineering; Head of UX & Design
**Estimated effort:** 3.6 days (S+M+XS+S)
**Risk IDs:** None
**Execution sequence:** 4

#### ST-22 — Snapshot test for `SystemStatus.js` hardcoded fallback counts

**Owner:** QA & Testing Owner
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** None

**Notes:** None

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-23 — Reconstruct 13 undocumented versions in sprint_planning_changelog.md (v3.1–v3.13)

**Owner:** Head of Specs Team
**Estimated effort:** 1.5 (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`

**Dependencies:** None

**Notes:** Use `git log -p` as the reconstruction source.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-24 — Remove dead-code duplicate POST /test/endpoints handler in backend/main.py

**Owner:** Head of Engineering
**Estimated effort:** 0.1 (XS)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`

**Dependencies:** None

**Notes:** None

**Staging-only ACs:** None

**Status at sprint open: ready**

---

#### ST-25 — Design-gate checklist addendum for motion/timing-sensitive chart interactions

**Owner:** Head of UX & Design
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`

**Dependencies:** None

**Notes:** Governance file edit checklist applies to `design_gate_prompt.md`. Shared-file — see Merge Order (EPIC-03/ST-16 also touches this file; rebase onto `main` after EPIC-03 merges before finalising).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-02 — Staging/Production Security Hardening

**Maps to:** S2-02
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Estimated effort:** 1.25 days (S+S)
**Risk IDs:** RISK-02
**Execution sequence:** 5

#### ST-06 — Provision a distinct API key for the staging environment

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 0.5 (S)
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None (sequencing precedence: precedes ST-07 per RISK-02)

**Notes:** Requires live production credential provisioning/rotation — not implementable by the execution engine alone.

**Staging-only ACs:** "Confirmed live: the old shared key no longer works against production after rotation" — `[staging-only evidence]`, no CI-reproducible equivalent. The delegated implementer produces this evidence as part of the story's own delivery; no additional pre-PR backlog item required per CLAUDE.md §2 (the story itself is the live-verification deliverable).

**Status at sprint open: ready**

---

#### ST-07 — Detect silent staging deploy staleness (GitHub↔Render auto-deploy webhook can fail silently)

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.75 (S)
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None (sequencing precedence: sequenced after/alongside ST-06 per RISK-02; note the rotation window in this PR)

**Notes:** Render build/deploy path filters are dashboard-only and not visible via repo search — root-cause diagnosis may require the Render dashboard directly.

**Staging-only ACs:** None — "confirmed firing correctly on a deliberately-stale test" is achievable via a simulated stale-SHA test harness, not a live-production-only check.

**Status at sprint open: ready**

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24-28 days |
| Total estimated effort (in-scope) | ~24.7 days |
| Utilisation | ~88-103% |
| Over-allocation | No |

## Items Deferred This Sprint

None — all 25 items in the authoritative backlog slice entered the sprint.

## Deferred Execution Blockers Accepted

*(omitted — `deferred_execution_blockers` was empty in `state.json`)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Provision live production credential rotation and post-rotation confirmation as part of ST-06's own delivery evidence | Cybersecurity & Trust Lead | No |
| Coordinate the ST-06/ST-07 staging-config rotation window and note it in the ST-07 PR (RISK-02) | Infrastructure & Operations Owner | No |
| Resolve ST-15's two-vehicle remediation choice at execution kickoff (LP-14) | Product Owner | No |
| Rebase EPIC-05's `design_gate_prompt.md` edit onto `main` after EPIC-03 merges, before finalising ST-25 | Head of UX & Design / Head of Engineering | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — Product Owner, 2026-08-04
**Scope confirmed:** Confirmed — all 25 items across 5 EPICs accepted within capacity; no items deferred — Product Owner, 2026-08-04
**Capacity confirmed:** Confirmed — ~24.7 days against ~24-28 day band, `pass` outcome; Minimum Capacity Buffer Floor advisory (§1.5) reviewed and acknowledged (proceed at full curated scope) — Product Owner, 2026-08-04
**Deferred execution blockers accepted (if any):** N/A — none present
**Signed off by:** Product Owner
**Date:** 2026-08-04
