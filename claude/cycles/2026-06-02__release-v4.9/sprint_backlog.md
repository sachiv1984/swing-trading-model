**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-06-02
**Cycle:** 2026-06-02__release-v4.9
**Release:** v4.9
**Sprint Goal:** Ship v4.9 security and CI hardening: remediate 21 npm HIGH CVEs, upgrade the Anthropic SDK to latest, wire real Postgres CI service to close the schema-invisible-column class of bug, add schema lifecycle smoke tests, and strengthen the roadmap empty-horizon gate.
**Backlog Slice Source:** original — `claude/cycles/2026-06-02__release-v4.9/stage4_backlog_slice.md`

---

# Sprint Backlog — 2026-06-02__release-v4.9

## Sprint Scope

**Active EPICs:** EPIC-01, EPIC-02, EPIC-03 (firm) | **Deferred:** EPIC-04 (gate 2026-06-21)

---

### Merge Order

**Merge sequence:** EPIC-01 → EPIC-02 → EPIC-03

**execution_state.json owner:** EPIC-01 (first in merge order). EPIC-02 and EPIC-03 branches must check for `execution_state.json` existence before creating; if found, append their EPIC section rather than overwrite.

**Shared files:** No cross-EPIC shared files identified. Each EPIC writes to distinct file domains (security_register for EPIC-01; ci-tests.yml + test files for EPIC-02; governance prompts for EPIC-03).

---

### Sprint 1

---

#### EPIC-01 — Security & Dependency Hardening

**Maps to:** S2-01
**Owner:** Head of Engineering; Cybersecurity & Trust Lead
**Estimated effort:** ~1–1.5 days
**Risk IDs:** RISK-01
**Execution sequence:** 1 (parallel with EPIC-02 and EPIC-03)

---

##### ST-01 — npm devDependency HIGH CVE remediation

**Owner:** Head of Engineering; Cybersecurity & Trust Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

*(The Execution Engine reads AC from `stage4_backlog_slice.md` directly via `spec_references`. Do not duplicate the full AC table here.)*

**Dependencies:** None

**Staging-only ACs:** None

**Notes:** 21 HIGH severity CVEs in react-scripts devDependency chain (2026-06-01 audit). All build-toolchain CVEs, not production runtime. Remediate via `npm audit fix`.

---

##### ST-02 — Anthropic SDK upgrade 0.40.0 → latest

**Owner:** Head of Engineering
**Estimated effort:** S–M (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Staging-only ACs:** AC-04 ([staging-only] POST /trade-plans/{plan_id}/generate-thesis and POST /ai/check-daily-cost functional on staging post-upgrade)

**Notes:** RISK-01 applies — 65 minor versions of changelog to review. Full backend test suite required post-upgrade. Staging validation (AC-04) required; if staging sign-off deferred to post-merge, a backlog item must be filed before the PR opens per CLAUDE.md §2.

---

#### EPIC-02 — CI/QA Infrastructure Strengthening

**Maps to:** S2-02
**Owner:** QA Lead; Head of Engineering
**Estimated effort:** ~1.5–2.5 days
**Risk IDs:** RISK-02
**Execution sequence:** 2 (parallel with EPIC-01 and EPIC-03)

---

##### ST-03 — Wire Phase B CI with real Postgres service

**Owner:** QA Lead; Head of Engineering
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Staging-only ACs:** None

**Notes:** RISK-02 — Phase B real Postgres CI may surface existing masked test failures; accept and fix any surfaced failures. ST-04 cannot start until ST-03 is complete (Phase B CI must be wired first).

---

##### ST-04 — Schema smoke test: lifecycle columns on positions table

**Owner:** QA Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** ST-03 (Phase B CI must be wired — hard internal dependency within EPIC-02)

**Staging-only ACs:** None

**Notes:** Test must be skipped/excluded when DATABASE_URL points to stub (Phase A). Test must pass in Phase B CI environment.

---

#### EPIC-03 — Governance Debt Clearance

**Maps to:** S2-03
**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** ~0.5 day
**Risk IDs:** None
**Execution sequence:** 3 (parallel with EPIC-01 and EPIC-02)

---

##### ST-05 — roadmap_prompt.md STEP 8.1 Empty Now Horizon gate strengthening

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Staging-only ACs:** None

**Notes:** Governance-file edit requiring CLAUDE.md §6 checklist: version bump + OPERATIONAL_GUIDE.md §6 + §14 update + prompt_change_log.md entry. AC-07 requires Head of Specs Team + PMO Lead sign-off confirmation in the commit/PR.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~12–14 days |
| Total estimated effort (in-scope, firm) | ~3–4.5 days |
| Utilisation | ~25–35% |
| Over-allocation | No |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| ST-06 — SI-05 Phase 1 backend service + Telegram delivery | EPIC-04 | Gate not met: SI-01 + SI-03 live ≥ 30 days — gate clears 2026-06-21 |
| ST-07 — SI-05 Phase 1 Playwright coverage | EPIC-04 | Same gate condition; depends on ST-06 |

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| BLG-GOV-74 Provisional-Target update (v4.9 → v4.10+) | PMO Lead | No |
| ST-02 AC-04: staging sign-off post-SDK-upgrade | Infrastructure & Operations Owner | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** confirmed
**Scope confirmed:** confirmed — 5 firm stories (ST-01–ST-05) across EPIC-01/02/03; EPIC-04 deferred (gate 2026-06-21)
**Capacity confirmed:** confirmed — firm effort ~3–4.5 days; within 12–14 day sprint capacity
**Deferred execution blockers accepted (if any):** N/A — no deferred execution blockers in this cycle
**Signed off by:** Product Owner
**Date:** 2026-06-02
