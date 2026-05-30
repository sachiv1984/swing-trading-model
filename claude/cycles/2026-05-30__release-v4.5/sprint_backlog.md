**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-05-30
**Cycle:** 2026-05-30__release-v4.5
**Release:** v4.5
**Sprint Goal:** Deliver all four v4.4 deferred execution_prompt.md governance patches and standardize agent role headers, resolving outstanding audit debt and hardening the governance infrastructure before SI-02 sprint planning begins.
**Backlog Slice Source:** original `claude/cycles/2026-05-30__release-v4.5/stage4_backlog_slice.md`

---

# Sprint Backlog — 2026-05-30__release-v4.5

---

## Sprint Scope

### Merge Order (Sprint 1)

Execution sequence: **EPIC-02 → EPIC-01**

| Order | EPIC | Rationale |
|-------|------|-----------|
| 1st | EPIC-02 | No governance file edits; no version bumps; fast autonomous delivery; `execution_state.json` owner |
| 2nd | EPIC-01 | All §6 checklist steps (version bumps, OPERATIONAL_GUIDE §14, prompt_change_log.md); EPIC-01 must rebase onto main after EPIC-02 merges |

**execution_state.json owner:** EPIC-02 (first EPIC to merge)

**Shared files advisory:** No file overlap between EPIC-01 and EPIC-02. EPIC-01 modifies `claude/system/execution_prompt.md`, `OPERATIONAL_GUIDE.md`, `claude/system/prompt_change_log.md`. EPIC-02 modifies 5 agent files in `claude/agents/`. EPIC-01 branch must rebase onto `main` after EPIC-02 merges before finalising its PR.

---

### EPIC-02 — Agent Header Standardization (S2-02)

**Maps to:** S2-02
**Owner:** Head of Specs Team
**Estimated effort:** ~1 hr (S)
**Risk IDs:** RISK-02
**Execution sequence:** 1 (first — no version bumps; execution_state.json owner)

#### ST-05 — Standardize 5 agent file role headers

**Owner:** Head of Specs Team
**Estimated effort:** ~1 hr (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

*(The Execution Engine reads AC from `stage4_backlog_slice.md` directly via `spec_references`. Do not duplicate the full AC table here — the sprint backlog is a sequencing and ownership document.)*

**Dependencies:** None

**Notes:** 5 files to edit in single commit: `api_contracts_documentation_owner.md`, `backend_engineering_patterns_owner.md`, `data_model_domain_schema_owner.md`, `frontend_specs_ux_documentation_owner.md`, `metrics_definitions_analytics_owner.md`. Agent files are role documents (not Class 6 governance prompts) — no version bumps required. Verified against `shared/preflight_common.md §2` role check after edit.

**Staging-only ACs:** None — all ACs verifiable by document inspection; no network/staging dependencies.

---

### EPIC-01 — Execution Prompt Hardening (S2-01)

**Maps to:** S2-01
**Owner:** Head of Specs Team
**Estimated effort:** ~2 hrs (4 × XS)
**Risk IDs:** RISK-01
**Execution sequence:** 2 (second — all §6 governance file edit checklist steps; rebase onto main after EPIC-02 merges)

**EPIC-01 packaging note:** All 4 stories modify `execution_prompt.md`. Apply in a single EPIC commit to minimize version bump overhead. CLAUDE.md §6 checklist is satisfied once in the final commit (version bump, OPERATIONAL_GUIDE §14 update, prompt_change_log.md entry).

#### ST-01 — execution_prompt.md: split DEL terminal-status write into sign-off and push steps

**Owner:** Head of Specs Team
**Estimated effort:** ~0.5 hr (XS)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (packaged with ST-02, ST-03, ST-04 in single EPIC-01 commit)

**Notes:** v4.4 OA-01 resolution. Splits DEL record status write into (a) `status = "sign_off_cleared"` at sign-off time and (b) `commit_sha` at push step.

**Staging-only ACs:** None — document inspection verification only.

---

#### ST-02 — execution_prompt.md STEP 3.2.B: explicit pr_status sync after PR open

**Owner:** Head of Specs Team
**Estimated effort:** ~0.5 hr (XS)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None (packaged with ST-01, ST-03, ST-04 in single EPIC-01 commit)

**Notes:** v4.4 OA-02 resolution. Adds explicit `gh pr view` step after PR open to sync `pr_status`. Also adds EPIC.status `"done"` → `"merged"` update rule at QA evidence commit time.

**Staging-only ACs:** None — document inspection verification only.

---

#### ST-03 — execution_prompt.md: verification-class sub-criterion for pre-planning sprints

**Owner:** Head of Specs Team
**Estimated effort:** ~0.5 hr (XS)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None (packaged with ST-01, ST-02, ST-04 in single EPIC-01 commit)

**Notes:** v4.4 OA-03 resolution (carry-forward item 2 from v4.4). Adds verification-class sub-criterion to §3.2.A autonomous class sign-off block. Prevents spurious Tier 2 advisories for pre-planning sprints where all VERIFICATION is document inspection.

**Staging-only ACs:** None — document inspection verification only.

---

#### ST-04 — execution_prompt.md: spec_references policy for documentation-creation stories

**Owner:** Head of Specs Team
**Estimated effort:** ~0.5 hr (XS)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None (packaged with ST-01, ST-02, ST-03 in single EPIC-01 commit)

**Notes:** v4.4 OA-04 resolution; AUD-003 mandate (BLG-GOV-70 stale — 3rd+ recurrence); carry-forward item 1 from v4.4. Adds policy note for doc-creation stories where primary deliverable IS the spec file. Includes archiving BLG-GOV-70 from backlog (AC-05).

**Staging-only ACs:** None — document inspection verification only.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity (Sprint 1) | ~12–14 days |
| Total estimated effort (Sprint 1 in-scope) | ~4.5 hrs (~0.6 days) |
| Utilisation (Sprint 1) | ~5% |
| Over-allocation | No |
| Capacity verdict | WARN (inherited from release plan — Sprint 2 conditional uncertainty; Sprint 1 within capacity) |
| WARN acknowledged by PO | Yes (2026-05-30) |

---

## Items Deferred This Sprint

~~ST-06, ST-07, ST-08 were deferred at Sprint 1 seal~~ — **Gate confirmed 2026-05-30**: EPIC-03 activated. See Sprint 2 section below.

---

## Deferred Execution Blockers Accepted

*(Section omitted — `deferred_execution_blockers` was empty in release plan state.json)*

---

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Confirm SI-02 20-closed-trades gate status; provide explicit PO go/no-go for EPIC-03 before Sprint 2 planning seals | Product Owner | **RESOLVED** — gate confirmed 2026-05-30; EPIC-03 activated as Sprint 2 |

No outstanding actions block Sprint 2 seal.

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed (2026-05-30)
**Scope confirmed:** Confirmed — EPIC-01 (ST-01–04, autonomous, governance patches) + EPIC-02 (ST-05, autonomous, agent headers); EPIC-03 deferred conditional on SI-02 gate
**Capacity confirmed:** Confirmed — Sprint 1 ~4.5 hrs well within capacity; WARN acknowledged (Sprint 2 conditional uncertainty)
**Deferred execution blockers accepted (if any):** N/A — none
**Signed off by:** Product Owner
**Date:** 2026-05-30

---

## Sprint 2 — EPIC-03 (SI-02 Gate Confirmed 2026-05-30)

> **Gate confirmed:** Product Owner confirmed SI-02 sprint planning is imminent (2026-05-30). EPIC-03 activated via direct `plan sprint` invocation with explicit PO authority. Sprint 2 proceeds as the planned conditional second sprint within v4.5. Amendment cycle path not used — EPIC-03 is a pre-planned conditional sprint, not an emergency scope change.

### Merge Order (Sprint 2)

Execution sequence: **EPIC-03** (single EPIC — no merge ordering required)

**execution_state.json ownership:** EPIC-03 appends to the existing `execution_state.json` created by EPIC-02 in Sprint 1. Phase 3 (Sprint 2) must read the existing file and append the EPIC-03 section — do not overwrite.

**Shared files advisory:** No file overlap with Sprint 1 EPICs. EPIC-03 produces new spec documents in `docs/specs/metrics/` and `docs/specs/data_model/`.

---

### EPIC-03 — SI-02 Spec Pre-Sprint Completion (S2-03)

**Maps to:** S2-03
**Owner:** Head of Specs Team + Metrics Definitions & Analytics Canonical Owner + Data Model & Domain Schema Owner
**Estimated effort:** ~20–28 hrs (~2.5–3.5 days)
**Risk IDs:** RISK-03
**Execution sequence:** Sprint 2 (sole EPIC; gate confirmed 2026-05-30)

**EPIC-03 packaging note:** Three sequenced `delegated_decision` stories: ST-06 (§13 boundary review) → ST-07 (drift score metric) → ST-08 (data schema). Execution engine generates delegation records; human domain owners execute each. ST-07 depends on ST-06 PASS; ST-08 is informed by (not hard-blocked on) ST-07.

#### ST-06 — SI-02 §13 formal boundary review

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** S (~0.5 day / ~4 hrs)
**Delegation class:** delegated_decision (Strategy Rules & System Intent Owner)

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

*(The Execution Engine reads AC from `stage4_backlog_slice.md` directly via `spec_references`. Do not duplicate the full AC table here.)*

**Dependencies:** None (first in sequence; gate confirmation is the entry condition)

**Notes:** Must produce PASS/FAIL determination on whether drift detection output is deterministic, display-only, and non-automated. Binding conditions documented. ST-07 depends on ST-06 PASS.

**Staging-only ACs:** None — document inspection verification only.

---

#### ST-07 — SI-02 drift detection score metric definition

**Owner:** Metrics Definitions & Analytics Canonical Owner; Head of Specs Team
**Estimated effort:** S (~1 day / ~8 hrs)
**Delegation class:** delegated_decision (Metrics Definitions & Analytics Canonical Owner)

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

*(The Execution Engine reads AC from `stage4_backlog_slice.md` directly via `spec_references`.)*

**Dependencies:** ST-06 §13 PASS required before ST-07 begins

**Notes:** Metric definition document covering user-facing format, rolling window, threshold bands (green/amber/red), warning state triggers, SI-05 weekly digest integration points. Filed at `docs/specs/metrics/si02_drift_score.md`.

**Staging-only ACs:** None — document inspection verification only.

---

#### ST-08 — SI-02 data schema pre-definition

**Owner:** Data Model & Domain Schema Owner; Head of Specs Team
**Estimated effort:** M (~1–2 days / ~8–16 hrs)
**Delegation class:** delegated_decision (Data Model & Domain Schema Owner)

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

*(The Execution Engine reads AC from `stage4_backlog_slice.md` directly via `spec_references`.)*

**Dependencies:** Informed by ST-07 metric definition (can proceed in parallel after ST-06 PASS; benefits from ST-07 context but not hard-blocked)

**Notes:** Gap analysis of current trade/position/trade plan schemas; missing fields enumerated with data types, tables affected, and migration complexity estimate. Filed at `docs/specs/data_model/si02_data_schema.md`.

**Staging-only ACs:** None — document inspection verification only.

---

## Sprint 2 Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity (Sprint 2) | ~12–14 days |
| Total estimated effort (Sprint 2 in-scope) | ~20–28 hrs (~2.5–3.5 days) |
| Utilisation (Sprint 2) | ~20–25% |
| Over-allocation | No |
| Capacity verdict | Within capacity |

---

## Product Owner Sign-Off (Sprint 2)

**Sprint 2 goal confirmed:** Complete SI-02 spec pre-sprint work — §13 boundary review, drift score metric definition, and data schema pre-definition — to enable SI-02 sprint planning to proceed
**Scope confirmed:** EPIC-03 (ST-06, ST-07, ST-08 — all delegated_decision)
**Gate confirmed:** SI-02 sprint planning imminent — confirmed by Product Owner 2026-05-30
**Capacity confirmed:** Sprint 2 ~20–28 hrs well within confirmed capacity (~12–14 days)
**Signed off by:** Product Owner
**Date:** 2026-05-30
