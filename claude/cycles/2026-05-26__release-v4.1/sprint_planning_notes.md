**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-27
**Cycle:** 2026-05-26__release-v4.1

---

# Sprint Planning Notes — 2026-05-26__release-v4.1

---

## Backlog Slice Source

Original — `claude/cycles/2026-05-26__release-v4.1/stage4_backlog_slice.md`

No amendment file in use (`amended_backlog_slice_path` is empty in `.claude_current_state.json`).

---

## Carry-Forward Items

Carry-forward items reviewed from `claude/cycles/2026-05-22__release-v4.0/lessons_learnt_closure.md ## Carry-Forward`:

| Item | Owner | Assigned to | Status |
|------|-------|-------------|--------|
| OA-01: execution_prompt.md merge-gate hard gate (2nd recurrence) | Head of Specs Team | ST-01 (EPIC-01) | Assigned as Sprint 1 story |
| OA-02: sprint_planning_prompt.md staging-only AC designation (2nd recurrence) | Head of Specs Team | ST-02 (EPIC-01) | Assigned as Sprint 1 story |
| OA-03: sprint_close_reminder.yml investigation | PMO Lead | ST-01 AC-04 | Assigned as Sprint 1 task |
| OA-04: delivery_verification_prompt.md pr_number null guard | Head of Specs Team | ST-03 (EPIC-01) | Assigned as Sprint 1 story |
| OA-05: Rejected-but-strong register gaps | PMO Lead | Not in v4.1 sprint scope | PMO Lead action before next roadmap run |
| OA-06: Ambiguous ideas register rows | PMO Lead | Not in v4.1 sprint scope | PMO Lead action before next roadmap run |
| BLG-OPS-29: api_performance_baseline.md re-run | Infrastructure & Operations Owner | ST-15 AC-01/02 (EPIC-04) | Assigned as Sprint 2 story |

Carry-forward items reviewed: 7 items from cycle `2026-05-22__release-v4.0`. Items OA-05/06 remain outstanding for PMO Lead.

---

## Pre-Sprint Decisions Resolution

Pre-sprint decisions from `cycle_summary.md ## Pre-Sprint Planning Required Decisions`:

| Decision | Owner | Status | Resolution |
|----------|-------|--------|-----------|
| [RISK-01] OA-01/OA-02 Head of Specs Team availability for Sprint 1 | Head of Specs Team | Resolved | Head of Specs Team confirms availability for Sprint 1 (ST-01, ST-02, ST-03). OA-01/OA-02 are 2nd-recurrence escalations — capacity allocated: ~3 days. Confirmed 2026-05-27. |
| [PT-04] PO written rationale for PT-04 park status | Product Owner | Resolved | PT-04 (Arc 2 performance analytics) gate not met — fewer than 20 closed trades. Rationale: insufficient trade history to produce statistically meaningful performance analytics; implementation would yield misleading metrics. PT-04 remains parked until gate confirmed met by FinOps & Resource Architect. Target: v4.x gate-conditional. Recorded: Product Owner, 2026-05-27. |

Both pre-sprint decisions resolved. No outstanding decision blockers.

---

## Pre-Sprint Backlog Advisory

Item with `Provisional-Target: Before v4.1 sprint planning` found in `claude/backlog/backlog.md` (line ~2803):

- **Staging-only AC reference table** (linked to OA-01 — 2nd recurrence): Advisory asked for a reference table of staging-only AC patterns to be produced before v4.1 sprint planning. This advisory is addressed by ST-02 (EPIC-01) which updates `sprint_planning_prompt.md` with staging-only AC designation guidance. The reference table is subsumed into the sprint_planning_prompt.md §7 update. Advisory resolved via ST-02.

---

## Deferred Items

No items deferred from the authoritative backlog slice. All 15 stories from `stage4_backlog_slice.md` are included in the sealed sprint backlog.

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| — | — | — |

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-07 (EPIC-03) | ST-04 (EPIC-02) — BLG-SPEC-33 closed | Internal — cross-EPIC | Resolved: Sprint ordering (ST-04 Sprint 1, ST-07 Sprint 2) naturally satisfies gate |
| ST-08 AC-05 (EPIC-03) | ST-06 (EPIC-02) — arc5-compliance contract | Internal — cross-EPIC | Advisory: ST-08 P&L integration benefits from ST-06 contract for field verification; not a hard gate |
| ST-13 (EPIC-04) | None | — | Independent |
| ST-14 GOV-56 (EPIC-04) | ST-03 (EPIC-01) | Shared file — delivery_verification_prompt.md | Resolved: EPIC-04 branches off main after EPIC-01 merges; EPIC-04 must rebase before finalising ST-14 GOV-56 changes |
| All Sprint 2 EPICs | Sprint 1 complete | Sequential sprints | Resolved: Sprint 2 begins after Sprint 1 EPICs merge to main |

---

## Execution Sequence

### Sprint 1

1. **EPIC-01** (Governance Prompt Hardening) — first; OA-01/OA-02 are 2nd-recurrence escalations, must not slip
   - ST-01 → ST-02 → ST-03 (sequential within EPIC; each story is a separate governed prompt edit)
2. **EPIC-02** (API Contract Spec Debt Batch 1) — concurrent with EPIC-01; no shared files
   - ST-04 → ST-05 → ST-06 (sequential within EPIC; simple ordering)

### Sprint 2

3. **EPIC-04** (SI-02 Pre-Planning + Security + Ops) — first in Sprint 2; all documentation/review; can be parallelised with EPIC-03 implementation
   - ST-12 → ST-13 → ST-14 → ST-15 (sequential within EPIC)
4. **EPIC-03** (Feature Integration + Quality) — after EPIC-04 initiates; ST-07 gates on ST-04 completion (satisfied by sprint ordering)
   - ST-07 → ST-08 → ST-09 → ST-10 → ST-11 (sequential within EPIC; ST-11 is verification, can slip to v4.2 if needed)

---

## Multi-EPIC Execution Notes

**execution_state.json owner: EPIC-01**

EPIC-01 creates `execution_state.json` at Sprint 1 STEP 0. All subsequent EPICs (EPIC-02, EPIC-04, EPIC-03) must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section. Do not overwrite.

**Shared file ownership advisory:**

| Shared File | First (Owner) EPIC | Subsequent EPICs | Advisory |
|-------------|-------------------|-----------------|---------|
| `docs/reference/openapi.yaml` | EPIC-02 (ST-04/05/06) | EPIC-03 (ST-07) | EPIC-03 must rebase onto `origin/main` after EPIC-02 merges before finalising openapi.yaml changes |
| `claude/system/delivery_verification_prompt.md` | EPIC-01 (ST-03) | EPIC-04 (ST-14 GOV-56) | EPIC-04 must rebase onto `origin/main` after EPIC-01 merges before modifying delivery_verification_prompt.md |
| `claude/system/OPERATIONAL_GUIDE.md` | EPIC-01 (ST-01/02/03) | EPIC-04 (ST-14 GOV-56) | EPIC-04 must rebase after EPIC-01 merges to avoid OPERATIONAL_GUIDE.md version conflict |
| `claude/system/prompt_change_log.md` | EPIC-01 (ST-01/02/03) | EPIC-04 (ST-14) | EPIC-04 must rebase after EPIC-01 merges; append to log, do not conflict |

All shared file conflicts are resolved by the merge order: EPIC-01 → EPIC-02 → EPIC-04 → EPIC-03.

---

## Risk Flags

| Risk ID | Associated Item | Mitigation | Status |
|---------|----------------|------------|--------|
| RISK-01 | EPIC-01 (ST-01/02/03) | Head of Specs Team confirmed available for Sprint 1; 2nd-recurrence escalation treated as hard gate at seal | Valid — mitigated |
| RISK-02 | EPIC-02 (ST-04/05/06) | Included as Sprint 1 stories; EPIC-03 ST-07 gate naturally satisfied | Valid — mitigated |
| RISK-03 | EPIC-03 (ST-07 through ST-11) | Sprint 2 EPIC-04 parallelisation; ST-09/ST-11 are lowest-risk deferrals; staging bundle (ST-11) verification-only | Valid — monitored |
| RISK-04 | EPIC-04 (ST-12 through ST-15) | All documentation/review outputs; low deployment risk; EPIC-04 sequenced first in Sprint 2 | Valid — low risk |

---

## Pre-Sprint Vulnerability Scan

pip-audit: **clean** — no known vulnerabilities found across all 63 backend dependencies (run 2026-05-27).

---

## Staging-Only AC Designations

The following ACs cannot be verified by unit or integration test in CI — designated `[staging-only evidence]` per sprint_planning_prompt.md §7 (LL-v3.9-P3-2):

| Story | AC | Reason |
|-------|-----|--------|
| ST-09 | AC-05 | Telegram threshold alert firing requires staging environment with real Telegram credentials |
| ST-11 | AC-02 | POST /trade-plans/{plan_id}/generate-thesis requires live GEMINI_API_KEY on staging |
| ST-11 | AC-03 | Yahoo Finance live rejection path requires live external API (not available in CI) |
| ST-11 | AC-04 | RENDER_STAGING_DEPLOY_HOOK validation requires live Render staging infrastructure |

**Filing note:** ST-11 itself is the backlog item for the staging verifications (it exists to close BLG-QA-28, BLG-QA-29, BLG-QA-30, BLG-OPS-28). No additional backlog items required for ST-11 staging ACs.

For ST-09 AC-05: staging verification is an explicit AC in the story. Human QA Lead must perform the staging check before the PR is merged. If deferred post-merge, a backlog item (BLG-QA-xx) must be filed before the PR opens per CLAUDE.md §2.

---

## Outstanding Actions

| Action | Owner | Blocker? | Status |
|--------|-------|---------|--------|
| OA-05: Rejected-but-strong register gaps (3 ideas) | PMO Lead | No | Carry-forward from v4.0; before next roadmap run |
| OA-06: Ambiguous ideas register rows (2 rows) | PMO Lead | No | Carry-forward from v4.0; before next roadmap run |
| ST-09 AC-05 staging verification: if deferred post-merge, file BLG-QA-xx backlog item before PR opens | QA Lead | No (conditional) | Action-at-execution |

No outstanding actions are marked Blocker? Yes. All pre-sprint decisions resolved. Sprint is ready to seal.

---

## Capacity WARN Acknowledgement

> **Capacity WARN acknowledged.** Sprint 2 estimated effort (~17 days) exceeds solo-developer sprint capacity (~8–10 days). Product Owner has explicitly acknowledged the over-allocation risk and accepts all 15 stories in scope, noting:
> 1. EPIC-04 (reviews/docs, ~6.5 days) can run in parallel with EPIC-03 implementation, reducing effective sequenced load.
> 2. If Sprint 2 capacity is constrained, ST-11 (staging bundle) and ST-09 (Gemini cost alerting) are discretionary deferrals to v4.2 with no functional regression.
> 3. No formal amendment is required for these discretionary deferrals — the Product Owner may direct deferral during Sprint 2 execution.
>
> `capacity_warn_acknowledged = true` set in `.claude_current_state.json`. Recorded: Product Owner, 2026-05-27.
