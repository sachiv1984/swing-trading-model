Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Planning
Release: v6.5
Cycle: 2026-07-02__release-v6.5
Last Updated: 2026-07-02

---

# Release Plan — v6.5

## Readiness

**Prior cycle:** `2026-06-26__release-v6.3` (state.json `prior_cycle` field). Most recently closed release: `2026-07-02__release-v6.4` (Verified, Closed_with_actions, post_ship_complete=true).

**Roadmap status:** `current_roadmap.md` §3 (Now horizon) is empty. All Arc 1–3 features shipped. Arc 2 remainder (PT-04) shipped v6.1. Arc 4 (PO-02/PO-03/PO-04) and Arc 5 remainder (SI-02/SI-04/SI-05 Phase 2) remain data-density-gated — no Now-horizon feature item is unblocked this cycle. v6.5 formally exists on the roadmap via the documented STEP 8.1 Option (b) deferral from `2026-07-02__scheduled` (see run_manifest.md §-1.2).

**Readiness determination: READY.** Scope is drawn from ungated backlog debt (audit remediation, QA/ops debt with explicit v6.5 provisional targets) and two small ungated user-facing items, per the rationale in `run_manifest.md` STEP 0.

### 1.1 Backlog Age Advisory

One spec/QA-debt item confirmed aged 2+ cycles without a story assignment: **BLG-QA-61** (3 consecutive cycles — flagged in `2026-07-02__release-v6.4` lessons_learnt_closure.md Carry-Forward #1). Disposition: promoted to firm v6.5 scope this cycle (see STEP 2/3; XS effort, resolves the recurring flag). No other item surfaced an explicit multi-cycle non-assignment marker during this scan; a full historical cross-check of all 124 active backlog items against every prior cycle's `sprint_backlog.md` was not performed exhaustively — items were identified via each backlog entry's own self-documented aging signals (Carry-Forward entries, "Nth deferral" notes, or gate re-check history).

### 1.2 Provisional-Target Advisory

2 items carry `Provisional-Target: v6.5` (horizon-planned for this release): **BLG-OPS-83**, **TEST-GAP-EPIC-03-v64**. Both are included in scope. The remaining scope items (BLG-QA-61, BLG-FE-46, BLG-FEAT-41, and the AUD-2026-07-01 remediation set) do not carry a `Provisional-Target: v6.5` field — they were selected via the STEP 0 carry-forward disposition, the Skill-Silo pull-forward mandate, and the audit SLA watch-list respectively (see `run_manifest.md` STEP 0).

### 1.3 Design-Gate Language Scan

**BLG-FE-46** contains explicit design-gate language: "UX reviewed by Head of UX & Design before sprint planning." Flagged — surfaced at the Pre-sprint Required Decisions checklist (STEP 7) and drives `design_gate_required = true` at STEP 4.1. No other scope candidate contains design-gate language; BLG-FEAT-41 is a backend metric-definition item with no UI acceptance criterion.

### 1.4a Perennial-Return Check

**BLG-QA-61** is the only scope candidate with a multi-cycle non-resolution history (3 consecutive cycles, per Carry-Forward #1). Per §1.4a, silent re-entry is not permitted at N≥2 — an explicit active PO disposition is recorded here: **neither (a) nor (b)** — Product Owner/Head of Specs Team disposition is to resolve the item outright this cycle (XS effort, <1 hour) rather than re-park or re-condition it, eliminating the recurring flag at source. Recorded per §1.4a intent (active disposition, not silent carry-forward).

### 1.4b Within-Sprint Date Gate Classification

No scope candidate carries a calendar-date gate condition. All five backlog-sourced items (BLG-OPS-83, TEST-GAP-EPIC-03-v64, BLG-QA-61, BLG-FE-46, BLG-FEAT-41) and the AUD-2026-07-01 remediation cluster are ungated. **No items require conditional classification under this rule** — all scope items may be classified firm subject only to the STEP 4.5 capacity check.

### 1.4 Gate-Condition Proximity Scan

| Item | Gate condition | Current trajectory | Projected clear date |
|------|-----------------|---------------------|------------------------|
| SI-02 (Behavioural Drift Detection) | ≥20 closed trades with linked trade_plans | Last recorded checkpoint 2026-06-09: 6/11 closed trades — **stale checkpoint, not re-queried this session** (per `2026-07-02__release-v6.4` run_manifest.md, PMO Lead owns gate re-check) | data not available — PMO Lead / Product Owner to re-verify at readiness review |
| PO-02 (Journal Pattern Recognition) | 6+ months of AI-summarised journal entries (BLG-FEAT-16 live and actively used) | trajectory unknown — journal entry generation rate not queried this session | data not available — Product Owner to surface at readiness review |
| PO-04 (Reflection ↔ Outcome Correlation) | 50+ trades with plans | trajectory unknown; long-horizon at current ~1–2 trades/month pace per `2026-07-02__scheduled` run_manifest.md (≈2026-Q4/2027 estimate for the related 50-trade Performance Science gate) | ≈2026-Q4/2027 (indicative only) |

**Do not halt.** Advisory only — recorded for Product Owner awareness; does not affect v6.5 scope, which does not include any of these gated items.

```yaml
# state.json update (STEP 1):
artifacts.stage1_readiness: pass
```

---

## Scope

Three backlog items (BLG-GOV-157, BLG-GOV-158, BLG-GOV-159) were filed this session via the backlog-add skill to give the remaining AUD-2026-07-01 audit findings a proper backlog record before entering scope — mirroring the precedent set by v6.4's BLG-GOV-150/151/152/153 for the first 7 of 17 findings (see `run_manifest.md` STEP 0). No other scope change or reprioritisation was made to the global backlog.

### Items in scope

| S2-ID | Backlog item | Description | Priority | Effort |
|-------|--------------|-------------|----------|--------|
| S2-01 | BLG-OPS-83 | Add v6.4 endpoint (`GET /strategy/benchmark/open-positions`) to `api_performance_baseline.md` | P3 | XS (<1 hour) |
| S2-02 | TEST-GAP-EPIC-03-v64 | Playwright coverage for Strategy Benchmark Panel 0 (Open Positions) rendering | P3 | XS (<0.5 day) |
| S2-03 | BLG-QA-61 | Review `signals_scenarios.md` against ST-01 signal sizing model changes | P3 | XS (<1 hour) |
| S2-04 | BLG-FE-46 | Claude thesis generation user feedback mechanism | P3 | S (~1 day) |
| S2-05 | BLG-FEAT-41 | Claude thesis adoption rate metric | P3 | S (~0.5 day) |
| S2-06 | BLG-GOV-157 | Lifecycle/prompt/state wording and consistency fixes (AUD-007, -012, -013) | P3 | XS (<1 hour) |
| S2-07 | BLG-GOV-158 | README.md document hygiene sweep (AUD-006, -009, -010, -015) | P3 | S (~0.5 day) |
| S2-08 | BLG-GOV-159 | OPERATIONAL_GUIDE/prompt version-sync drift (AUD-001, -003, -016) | P3 | XS (<1 hour) |

*(Note: BLG-GOV-157/158/159 IDs as filed — see backlog.md; item content is as originally drafted regardless of final ID assignment.)*

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-SPEC-35 (PO-02 §13 boundary review) | Gate condition ("PO-02 sprint planning imminent") not met — PO-02 blocked on Arc 4 6-months-AI-journal-entries data-density gate | Re-review each cycle until PO-02 sprint planning becomes imminent |
| SI-02 (Behavioural Drift Detection) | Data-density gate not met (last checkpoint 6/11 closed trades vs 20 required; stale, PMO Lead to re-verify) | Re-check at next release planning readiness scan |
| PO-02/PO-04 (Arc 4 remainder) | Data-density gates not met | Re-check at next release planning readiness scan |
| Remaining Actionable-now (category A) backlog items not listed above | Not selected this cycle; scope was sized to the ungated audit/debt/feature items with the clearest immediate justification (audit SLA, explicit v6.5 provisional targets, 3-cycle carry-forward, Skill-Silo pull-forward mandate) rather than exhausting full capacity | Available for v6.6 scoping |

```yaml
# state.json update (STEP 2):
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-06, S2-07, S2-08 | Head of Specs Team | RISK-01 | None — independent of EPIC-02/03 |
| EPIC-02 | S2-01, S2-02, S2-03 | Infrastructure & Operations Owner; QA & Testing Owner | RISK-02 | None — independent of EPIC-01/03 |
| EPIC-03 | S2-04, S2-05 | Base44 Frontend; Head of UX & Design; Metrics Definitions & Analytics Owner | RISK-03 | Design gate must pass before sprint planning seals (BLG-FE-46 is UI-facing) |

**EPIC-01** — Audit Remediation Cluster. All three items are governance/documentation hygiene fixes carried directly from AUD-2026-07-01 Tier 1 (Low effort) findings, plus one Tier 2 (Medium effort, BLG-GOV-158/AUD-006) item flagged in the audit's own SLA section as a P0-escalation risk if still open at the next audit. Any prompt version bump made while resolving these findings must follow the CLAUDE.md §6 Governance File Edit Checklist in the same commit (version bump, OPERATIONAL_GUIDE.md §14 sync, phase-section header sync, prompt_change_log.md entry).

**EPIC-02** — Backlog Debt Clearance. S2-01/S2-02 both carry an explicit `Provisional-Target: v6.5`. S2-03 (BLG-QA-61) is the 3-cycle carry-forward item promoted to firm scope this cycle per the STEP 1.4a disposition.

**EPIC-03** — AI Thesis Feedback Loop. Two user-facing items addressing the `2026-07-02__scheduled` rebalance's explicit Skill-Silo pull-forward mandate (see run_manifest.md STEP 0). S2-04 is UI-facing and triggers the design gate (STEP 4.1); S2-05 is a backend metric definition with no UI acceptance criterion.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Prompt/governance-file edits made without completing the full CLAUDE.md §6 checklist (version bump + §14 sync + phase header + change log entry) in the same commit | Medium | Sprint execution must apply the CLAUDE.md §6 checklist explicitly for any Class 6 prompt touched while resolving BLG-GOV-157/158/159; verified at delivery verification | null |
| RISK-02 | EPIC-02 | New Playwright test (S2-02, TEST-GAP-EPIC-03-v64) for the API-error state may be flaky if the mock/error-injection approach is not deterministic | Low | Follow the existing mock strategy documented in BLG-QA-37 (Playwright mock strategy) for the API-error-state scenario | null |
| RISK-03 | EPIC-03 | S2-04 (BLG-FE-46) is UI-facing and has not yet cleared the design gate; sprint planning cannot seal without it | High | Run `run design-gate --cycle 2026-07-02__release-v6.5` immediately after this plan publishes, before invoking `plan sprint` | null |

**Decisions record (required output):**

Created: `docs/product/decisions/decisions--2026-07-02__release-v6.5.md`

```yaml
# state.json update (STEP 3):
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

Verified: all 8 backlog items referenced by S2-01 through S2-08 (BLG-OPS-83, TEST-GAP-EPIC-03-v64, BLG-QA-61, BLG-FE-46, BLG-FEAT-41, BLG-GOV-157, BLG-GOV-158, BLG-GOV-159) exist exactly once each in `claude/backlog/backlog.md`. Every S2-ID maps to exactly one EPIC-ID (EPIC-01: S2-06/07/08; EPIC-02: S2-01/02/03; EPIC-03: S2-04/05) and every EPIC declares its `Maps to` set consistently between the Scope and Execution Plan sections. Every RISK-ID (RISK-01/02/03) declared in the Execution Plan EPIC table appears as a row in the Risk Register Summary with `Relates to` pointing to a valid EPIC-ID. No orphaned references found. PASS.

```yaml
# state.json update (STEP 3.5):
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** No matching row in `scored_initiatives.md` for any of EPIC-01/02/03 (confirmed at STEP 0 — the file scores older roadmap-level initiatives, not these backlog IDs). Per the three-tier resolution rule, this falls to tier 3: use STEP 4 inline estimates; no advisory required.

**Estimated effort (mid-point of each story's stated range):**

| EPIC | Stories | Mid-point effort |
|------|---------|-------------------|
| EPIC-01 | ST-01, ST-02, ST-03 | ~0.1 + 0.5 + 0.1 ≈ 0.7 day |
| EPIC-02 | ST-04, ST-05, ST-06 | ~0.1 + 0.4 + 0.1 ≈ 0.6 day |
| EPIC-03 | ST-07, ST-08 | ~1.0 + 0.5 ≈ 1.5 day |
| **Total** | 8 stories | **≈ 2.8 days** |

**Assumptions:** `--timebox` and `--capacity` were not specified at invocation (both default to empty per `state.json.assumptions`). No explicit capacity figure exists to check against.

**Outcome:** ≈2.8 days of estimated work is materially lighter than every firm-scope sprint delivered since v5.0 (typically 5–15 days of story effort across 5–24 stories). All 8 stories are single-sprint, non-conflicting, and have no cross-EPIC dependency (see Execution Plan). No phasing is required — the full v6.5 scope fits comfortably within a single sprint under any capacity assumption consistent with the cadence of the last 10 releases.

```yaml
# state.json update (STEP 4.5):
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity / 5.7 Decision Record Integrity

**5.5 Cross-Stage Integrity:** All 8 S2 IDs (S2-01 through S2-08) map to exactly one of EPIC-01/02/03; EPIC IDs in `stage4_backlog_slice.md` (EPIC-01, EPIC-02, EPIC-03) match the Execution Plan's EPIC table exactly; all 3 RISK IDs (RISK-01, RISK-02, RISK-03) referenced in the EPIC table appear as rows in the Risk Register Summary; no orphaned references. No Stage 2/3/4 artefact has changed since the STEP 3.5 pass. PASS.

**5.7 Decision Record Integrity:** Skipped — `artifacts.escalations` is not `present` (no escalations were raised this cycle). `not_applicable`.

```yaml
# state.json update (STEP 5.5):
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```
