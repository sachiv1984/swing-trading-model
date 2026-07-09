**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-07-09
**Cycle:** 2026-07-08__release-v6.8
**Release:** v6.8
**Sprint Goal:** Fix the SI-02-blocking trade-plan linkage bug and close the two accompanying security gaps, ship both mandatory Product Value Alert pull-forwards (trade tagging and the SI-02 gate visibility indicator), and clear the accumulated spec, QA, and governance debt cluster — the largest single-sprint firm scope by story count since v6.3/v6.4.
**Backlog Slice Source:** Original — `stage4_backlog_slice.md`

# Sprint Backlog — 2026-07-08__release-v6.8

**Merge order:** EPIC-01 → EPIC-02 → EPIC-03 (EPIC-01 sequenced first per `release_plan.md`'s explicit sequencing constraint; EPIC-02 begins once EPIC-01 is underway, not blocking on its completion; EPIC-03 is fully independent). **`execution_state.json` owner: EPIC-01** (first in execution order — see `sprint_planning_notes.md` Multi-EPIC Execution Notes). **Shared file:** `docs/operations/api_performance_baseline.md` is touched by both EPIC-02 (ST-05, new-endpoint entries) and EPIC-03 (ST-15, historical backfill) — EPIC-03's ST-15 branch should rebase onto `main` after EPIC-02 merges (see `sprint_planning_notes.md` Shared File Ownership Advisory).

## Sprint Scope

### EPIC-01 — Production Correctness, Security & Infrastructure

**Maps to:** S2-01, S2-02, S2-03, S2-04
**Owner:** Backend Engineering Patterns Owner / Cybersecurity & Trust Lead / Infrastructure & Operations Owner
**Estimated effort:** ~2.6 days
**Risk IDs:** RISK-01, RISK-02
**Execution sequence:** 1 (runs first — release plan's explicit sequencing constraint)

#### ST-01 — Investigate `trade_plans.position_id` never populated in production (BLG-BE-46)

**Owner:** Backend Engineering Patterns Owner; PMO Lead
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (first in EPIC-01 sequence)

**Notes:** Design gate: Pre-Approved (backend correctness fix, no UI change). RISK-01: investigation time-boxed to the first half-day before committing to full-fix scope; a documented decision (bug fixed / backfill deferred with rationale) is a valid completion path — full historical backfill is not required to close. Root-cause finding informs ST-06's display of corrected linkage data (soft dependency, not blocking — see `sprint_planning_notes.md` Dependency Map).

**Staging-only ACs:** None — AC-02 verified via direct API read (own backend, testable in CI with a test-DB fixture).

---

#### ST-02 — Unvalidated dict keys used as SQL column names in `database.update_signal()` (BLG-SEC-08)

**Owner:** Backend Engineering Patterns Owner; Cybersecurity & Trust Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** Design gate: Pre-Approved (backend security fix, no UI change).

**Staging-only ACs:** None — regression test verifiable in CI.

---

#### ST-03 — Manual review of existing signals for anomalous ticker/market values (BLG-SEC-07)

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** Design gate: Not Applicable (manual review/audit, no code or UI shipped).

**Staging-only ACs:** None — findings document verified by direct read.

---

#### ST-04 — Provision application `X-API-Key` for governed routines (BLG-OPS-99)

**Owner:** Infrastructure & Operations Owner; PMO Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** Design gate: Not Applicable (infrastructure/credential provisioning, no user-visible effect). Resolves `LP-08` (v6.7 closure carry-forward, 2-cycle-recurring credential gap). RISK-02: scope to read-only application key with least-privilege access; do not commit the key value to any tracked file; document storage location only (e.g. `~/.api_keys`).

**Staging-only ACs:** AC-02 — requires the live production key confirming a real gate condition against live production data; CI cannot reproduce this. If evidence is deferred to a post-merge live run, a backlog item must be filed before the PR opens (CLAUDE.md §2 / LL-v3.9-P3-2).

---

### EPIC-02 — Product Value Pull-Forward (Mandatory)

**Maps to:** S2-05, S2-06
**Owner:** Product Owner / Head of UX & Design
**Estimated effort:** ~4.0 days
**Risk IDs:** RISK-03
**Execution sequence:** 2 (begins once EPIC-01 is underway, not blocking on its completion)

#### ST-05 — Trade tagging and tag-based performance filtering (BLG-FEAT-52)

**Owner:** Product Owner; Head of UX & Design; Head of Engineering
**Estimated effort:** S (~2–3 days, descoped from L)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None (may run in parallel with ST-06)

**Notes:** Design gate: Required, ✅ Cleared (`ux_spec.md` v1.0; `trade_plan.md` v0.9, `analytics.md` v2.0 locked). Mandatory pull-forward from the 2026-07-08 Product Value Alert (ratio 0.26). New endpoints — `openapi.yaml` + `docs/specs/api_contracts/` + `backend/routers/test.py` registration required same-commit (CLAUDE.md hard rule). AC-04 (no dependency on `trade_annotations`/PO-02) confirmed at this sprint planning — see `sprint_planning_notes.md` AC Confirmation table. LL-v2.0-P4-2: new user-facing controls — EPIC `test_scenarios` must be set `pending` in `execution_state.json` at Execution STEP 0.

**Staging-only ACs:** None — AC-05 offers Playwright coverage as a CI-capable evidence path, with staging sign-off as an alternative, not exclusive.

---

#### ST-06 — SI-02 gate visibility indicator, Reports page (BLG-FEAT-71)

**Owner:** Product Owner; Head of UX & Design
**Estimated effort:** S (~1–2 days)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None — soft data-coherence relationship with ST-01 only, not a build-time blocker (see `sprint_planning_notes.md` Dependency Map)

**Notes:** Design gate: Required, ✅ Cleared (`ux_spec.md` v1.0; `reports.md` v0.6 locked, additive to the existing Dashboard "Gate Progress" strip). Mandatory pull-forward from the 2026-07-08 Product Value Alert. AC-04 confirmed at this sprint planning: `BLG-BE-46` (ST-01) is unresolved as of planning (0 linked trades); since AC-03 requires live reads, the indicator will correctly show NOT MET at build time and self-correct once ST-01 merges. LL-v2.0-P4-2: new user-facing section — same EPIC `test_scenarios = pending` flag as ST-05.

**Staging-only ACs:** None — AC-05 offers Playwright coverage as a CI-capable evidence path, with staging sign-off as an alternative, not exclusive.

---

### EPIC-03 — Spec & Governance Debt Clearance

**Maps to:** S2-07, S2-08, S2-09, S2-10, S2-11, S2-12, S2-13, S2-14, S2-15, S2-16, S2-17
**Owner:** Head of Specs Team / PMO Lead
**Estimated effort:** ~7.3 days
**Risk IDs:** RISK-04, RISK-05
**Execution sequence:** 3 (independent of EPIC-01/EPIC-02; all 11 items parallelisable; first candidates to trim if capacity slips)

#### ST-07 — Dashboard homepage visual hierarchy review post-v6.2 (BLG-SPEC-58)

**Owner:** Head of UX & Design
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** Design gate: Not Applicable (review/documentation activity; any resulting UI change is design-gated separately in a future cycle).

**Staging-only ACs:** None — review document verified by direct read.

---

#### ST-08 — R-multiple cross-currency normalization specification (BLG-SPEC-59)

**Owner:** Head of Specs Team; Metrics & Analytics Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** Design gate: Not Applicable (spec-authoring only; no UI ships this sprint). Stale 4+ cycles per `release_plan.md` Scope.

**Staging-only ACs:** None.

---

#### ST-09 — Trailing stop visual indicator frontend specification (BLG-SPEC-60)

**Owner:** Head of Specs Team; Head of UX & Design
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** Design gate: Not Applicable (deliverable is the spec document itself; implementation not in this sprint's scope). Stale 4+ cycles.

**Staging-only ACs:** None.

---

#### ST-10 — Trailing stop effectiveness metric definition (BLG-SPEC-61)

**Owner:** Head of Specs Team; Metrics & Analytics Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** Design gate: Not Applicable (metric definition documentation only). Stale 4+ cycles.

**Staging-only ACs:** None.

---

#### ST-11 — Fix 12 dark spec files surfaced by Playwright glob discovery (BLG-QA-64)

**Owner:** Director of Quality
**Estimated effort:** M (~1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** Design gate: Not Applicable (test/spec wiring remediation; no UI change).

**Staging-only ACs:** None — glob-discovery re-run is the verification step, CI-capable.

---

#### ST-12 — CI inline OpenAPI drift detection for `api_performance_baseline.md` (BLG-GOV-134)

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** Design gate: Not Applicable (CI/CD tooling; no user-visible effect).

**Staging-only ACs:** None — CI workflow run confirms the check executes.

---

#### ST-13 — Log Anthropic API token usage and cost per morning briefing call (BLG-OPS-74)

**Owner:** FinOps & Resource Architect
**Estimated effort:** S (<0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** Design gate: Not Applicable (backend logging/observability; no UI).

**Staging-only ACs:** None — logging wrapper unit-testable in CI (mocks the API call).

---

#### ST-14 — Refactor `Watchlist.js` to ESLint compliance (BLG-FE-77)

**Owner:** Head of Engineering
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** Design gate: Not Applicable (pure refactor; AC-02 explicitly requires no functional or visual behaviour change). No frontend-visible change triggered — no Playwright/staging requirement per CLAUDE.md.

**Staging-only ACs:** None.

---

#### ST-15 — `BLG-OPS-13` v5.1–v5.4 endpoint baseline extension (BLG-OPS-61)

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None (recommended: rebase onto `main` after EPIC-02 merges — see Shared File Ownership Advisory, `api_performance_baseline.md` also touched by ST-05)

**Notes:** Design gate: Not Applicable (documentation of API latency baselines; no UI). 6–12 missed release targets, resolved directly this cycle rather than deferred again.

**Staging-only ACs:** None.

---

#### ST-16 — Extract Playwright test standard from `execution_prompt.md` to `shared_standards.md` (BLG-GOV-123)

**Owner:** Head of Specs Team
**Estimated effort:** XS (~1 hour)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Notes:** Design gate: Not Applicable (governance document reorganisation; no UI). RISK-05: Governance File Edit Checklist (CLAUDE.md §6) applies same-commit — version bump both files, `prompt_change_log.md` entry, OPERATIONAL_GUIDE §14 sync. 6–12 missed release targets, resolved directly this cycle.

**Staging-only ACs:** None.

---

#### ST-17 — System threat model document (BLG-OPS-71)

**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None

**Notes:** Design gate: Not Applicable (security documentation; no UI). 6–12 missed release targets, resolved directly this cycle.

**Staging-only ACs:** None.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~12–14 days |
| Total estimated effort (in-scope) | ~13.9 days |
| Utilisation | ~99–116% (near top of range) |
| Over-allocation | No — within the 12–14 day baseline, matches `release_plan.md` Capacity Check (PASS, not WARN) |

## Items Deferred This Sprint

None — all 17 ST items from the authoritative backlog slice are in scope.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Prompt change log gaps (5 files, see `sprint_planning_notes.md` Hygiene Advisories) | Head of Specs Team | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — 2026-07-09 (see `sprint_goal.md`)
**Scope confirmed:** Confirmed — 17 ST items across EPIC-01/EPIC-02/EPIC-03, all Firm, no deferrals
**Capacity confirmed:** Confirmed — ~13.9 days within ~12–14 day capacity, no over-allocation, no WARN acknowledgement required
**Deferred execution blockers accepted (if any):** N/A — `deferred_execution_blockers` empty in `state.json`
**Signed off by:** Product Owner
**Date:** 2026-07-09
