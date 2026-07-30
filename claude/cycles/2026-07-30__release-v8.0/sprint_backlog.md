# Sprint Backlog — 2026-07-30__release-v8.0

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-07-30
**Cycle:** 2026-07-30__release-v8.0
**Release:** v8.0
**Sprint Goal:** Close the platform's outstanding backend error-masking, security-hardening, and FX/data-spec debt while shipping keyboard/focus accessibility fixes to the Trade Plan flow, strengthening QA/CI test infrastructure, hardening operational alerting and disaster-recovery readiness, and fixing the recurring cross-EPIC `execution_state.json` merge-conflict pattern.
**Backlog Slice Source:** original `stage4_backlog_slice.md`

## Merge Order

EPIC merge sequence: **EPIC-01 → EPIC-03 → EPIC-05 → EPIC-02 → EPIC-04 → EPIC-06** (per `sprint_planning_notes.md ## Execution Sequence`).

`execution_state.json` owner EPIC: **EPIC-01**. All later-merging EPICs must check for `execution_state.json` existence and append their section rather than overwrite (per `shared_standards.md §12`).

Shared files across EPICs this sprint: `execution_state.json` (owner: EPIC-01, standard multi-EPIC collision surface); `data_model.md` (owner: EPIC-01, ST-01 — no other EPIC touches it this sprint); `shared_standards.md` (owner: EPIC-06, ST-19 — no other EPIC touches it this sprint). See `sprint_planning_notes.md` for full advisory.

## Sprint Scope

### EPIC-01 — Data Model & Spec Integrity

**Maps to:** S2-01, S2-02, S2-03
**Owner:** Data Model & Domain Schema Owner; Financial Reporting & Records Owner
**Estimated effort:** 4.0 capacity units
**Risk IDs:** None
**Execution sequence:** 1

#### ST-01 — `strategy_version_at_entry` field on trade/trade_plan

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** 2.0
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Notes:** Forward-only migration, no backfill.

**Staging-only ACs:** None — all ACs verifiable via migration + code review / CI.

---

#### ST-02 — FX handling review post-DS-05 US market source change

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** 1.0
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** Documentation/review item; no code change unless a gap is found.

**Staging-only ACs:** None.

---

#### ST-03 — FX conversion audit trail completeness check (§4.1.5 effective-rate logging)

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** 1.0
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** Financial Reporting & Records Owner sign-off required per AC.

**Staging-only ACs:** None.

---

### EPIC-03 — QA & Test Infrastructure Hardening

**Maps to:** S2-10, S2-11, S2-12
**Owner:** Director of Quality; QA Lead; QA & Testing Owner
**Estimated effort:** 5.0 capacity units
**Risk IDs:** None
**Execution sequence:** 2

#### ST-10 — Retroactive Playwright §18 anti-pattern sweep (route.fallback() ordering + networkidle usage) (consolidated)

**Owner:** QA Lead
**Estimated effort:** 1.0
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** One-time grep-and-fix sweep per `shared_standards.md §18`.

**Staging-only ACs:** None — grep/CI-verifiable.

---

#### ST-11 — Test-tagging convention (smoke/regression/critical) for selective CI runs

**Owner:** QA & Testing Owner
**Estimated effort:** 2.0
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-12 — Synthetic trade-history data generator for gated-feature testing

**Owner:** QA & Testing Owner
**Estimated effort:** 2.0
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** Must be clearly scoped/labelled test-only, never usable against production.

**Staging-only ACs:** None.

---

### EPIC-05 — Frontend Technical Debt

**Maps to:** S2-18
**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** 2.0 capacity units
**Risk IDs:** None
**Execution sequence:** 3

#### ST-18 — Reusable Base44 prompt fragment library for common layouts

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** 2.0
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** Authoring-tooling library; no UI shipped by this item itself (per Design Gate classification).

**Staging-only ACs:** None.

---

### EPIC-02 — Security Hardening

**Maps to:** S2-04, S2-05, S2-06, S2-07, S2-08, S2-09
**Owner:** Cybersecurity & Trust Lead; Head of Engineering; Head of UX & Design
**Estimated effort:** 6.0 capacity units
**Risk IDs:** RISK-01, RISK-02, RISK-03
**Execution sequence:** 4

#### ST-04 — Raw exception text leaked in 16 implicit-HTTP-200 error paths in backend/main.py

**Owner:** Head of Engineering
**Estimated effort:** 1.0
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** Head of Engineering sign-off required per AC.

**Staging-only ACs:** None — regression test + code review verifiable in CI.

---

#### ST-05 — Mandatory security review checklist for new AI-calling endpoints

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 1.0
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** Reference from design gate process; Cybersecurity & Trust Lead sign-off required.

**Staging-only ACs:** None.

---

#### ST-06 — Trade Plan pre-entry checklist items unreachable by keyboard

**Owner:** Head of UX & Design
**Estimated effort:** 1.0
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** RISK-01. Design Gate PASSED with decision record (`docs/design/2026-07-30__release-v8.0/entry-checklist-keyboard-accessibility/decision_record.md`) and `trade_plan.md` v1.3. Classified `autonomous` per BLG-GOV-72 fast-path (c) — modification against an already-locked frontend spec with Playwright feasibility implied by the staging-only AC framing.

**Staging-only ACs:** AC-2 (Tab/Space/Enter interaction, `aria-checked` state reflection — timing/interaction) — Playwright coverage or recorded staging sign-off required per CLAUDE.md §2 before this AC is considered met.

---

#### ST-07 — Trade Plan "Abandon" modal has no focus trap or restoration

**Owner:** Head of UX & Design
**Estimated effort:** 1.0
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** RISK-01. Design Gate PASSED with decision record (`docs/design/2026-07-30__release-v8.0/abandon-modal-focus-trap/decision_record.md`) and `trade_plan.md` v1.3. Classified `autonomous` per BLG-GOV-72 fast-path (c).

**Staging-only ACs:** AC-2 (Tab focus containment, Escape close, focus restoration on close — interaction/timing) — Playwright coverage or recorded staging sign-off required per CLAUDE.md §2 before this AC is considered met.

---

#### ST-08 — Verify request.client.host reflects true client IP behind Render's proxy; configure trusted-proxy headers if not

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 1.0
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** RISK-02. Requires live verification against the production Render deployment and a possible uvicorn `--forwarded-allow-ips` config change, scoped narrowly per RISK-02 mitigation. Cybersecurity & Trust Lead sign-off required.

**Staging-only ACs:** AC-1 (live `request.client.host` behaviour verification), AC-3 (live re-verification of independent rate-limit buckets per client) — both require live production behaviour that CI cannot reproduce; Playwright coverage is not applicable — evidence must be a recorded live-verification note in the QA evidence log.

---

#### ST-09 — `.gitleaks.toml`'s global `[[allowlists]]` blocks use an invalid schema

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 1.0
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** RISK-03. Each rewritten block's suppression must be verified by an actual local `gitleaks detect` run against its target file, not just TOML syntax validity. Cybersecurity & Trust Lead sign-off required.

**Staging-only ACs:** None — local `gitleaks detect` run and CI `secret-scanning.yml` pass are both CI/local-verifiable, not staging-only.

---

### EPIC-04 — Operations & Reliability

**Maps to:** S2-13, S2-14, S2-15, S2-16, S2-17
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Estimated effort:** 5.25 capacity units
**Risk IDs:** None
**Execution sequence:** 5

#### ST-13 — Render service health-check alerting to Telegram on 5xx spike

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 2.0
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** ST-14 (should land before/alongside — both depend on the same Telegram credential pair)

**Notes:** Render webhook/dashboard configuration may require Infrastructure & Operations Owner action beyond repo-level changes, depending on current plan tier.

**Staging-only ACs:** AC-2 (alert confirmed to fire on a simulated 5xx spike) — staging or documented dry-run test required; CI cannot reproduce a live Telegram delivery.

---

#### ST-14 — Configure TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID as GitHub Actions repo secrets for nightly backtest job alerting

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.25
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None (ST-13 depends on this)

**Notes:** Requires repo admin action to input the actual secret values (same values as existing Render env vars) via GitHub Settings → Secrets and variables → Actions — the execution engine does not hold these values and cannot supply them; human action required to complete this item.

**Staging-only ACs:** AC-2 (manual `workflow_dispatch` re-run confirms a Telegram message is actually received) — staging-only, requires a live GitHub Actions run against a deliberately-broken endpoint.

---

#### ST-15 — Confirm Render rollback runbook has real execution history

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 1.0
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** Requires checking Render dashboard/deployment history or running a deliberate rollback drill against a non-production/staging deploy — dashboard-level access needed.

**Staging-only ACs:** AC-1/AC-2 (historical execution evidence or a live rollback drill) — staging-only, not CI-verifiable.

---

#### ST-16 — Render dashboard-only build/deploy path filter audit (invisible to repo grep)

**Owner:** FinOps & Resource Architect
**Estimated effort:** 1.0
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Notes:** Render's build/deploy path-filter configuration lives in the dashboard only and is invisible to repo search — must be read directly from the Render dashboard and then documented in-repo. FinOps & Resource Architect sign-off required.

**Staging-only ACs:** AC-1 (dashboard config audit) — staging-only in the sense that it requires direct dashboard access, not a CI-reproducible check.

---

#### ST-17 — Backup & disaster recovery runbook for production database

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 1.0
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None

**Notes:** Requires confirming actual hosting-provider backup/retention configuration and recovery capability. Infrastructure & Operations Owner sign-off required.

**Staging-only ACs:** AC-2 (recovery runbook confirmed against actual hosting provider capability) — staging-only, requires provider-side verification not reproducible in CI.

---

### EPIC-06 — Governance & Engineering Process Hardening

**Maps to:** S2-19
**Owner:** Head of Engineering
**Estimated effort:** 4.0 capacity units
**Risk IDs:** RISK-04
**Execution sequence:** 6

#### ST-19 — Structural fix for recurring cross-EPIC execution_state.json merge-conflict pattern

**Owner:** Head of Engineering
**Estimated effort:** 4.0
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None

**Notes:** RISK-04. No HoST design/technical-approach artefact exists yet for this item (advisory per LL-v2.2-SP-01 — see `sprint_planning_notes.md`); a design/technical-approach session should be scheduled before execution begins. Head of Engineering sign-off required before the new mechanism is used live. Existing reactive `shared_standards.md §12` mechanism kept as documented fallback. Must update `shared_standards.md §12` to reference the new mechanism in the same change.

**Staging-only ACs:** AC-2 (next multi-EPIC sprint shows a measured reduction in per-branch conflicts) — this AC can only be confirmed retrospectively at the *next* multi-EPIC sprint, not within this sprint; record as a follow-up verification item at that sprint's delivery verification.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24-28 units |
| Total estimated effort (in-scope) | ~26.25 units |
| Utilisation | ~94-109% |
| Over-allocation | No |

## Items Deferred This Sprint

None — all 19 ST items from the authoritative backlog slice are in scope.

## Deferred Execution Blockers Accepted

None — `deferred_execution_blockers` was empty in `state.json` at STEP -1.2.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Schedule a HoST design/technical-approach session for ST-19 before execution begins | Head of Specs Team | No |
| `sprint_planning_prompt.md` prompt-change-log gap (current v3.13, last logged v3.11→v3.12) | Head of Specs Team | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — see `sprint_goal.md`
**Scope confirmed:** Confirmed — 19 ST items across 6 EPICs, no deferrals
**Capacity confirmed:** Confirmed — ~94-109% utilisation, `pass` outcome, no WARN acknowledgement required
**Deferred execution blockers accepted (if any):** N/A — none present
**Signed off by:** Product Owner
**Date:** 2026-07-30
