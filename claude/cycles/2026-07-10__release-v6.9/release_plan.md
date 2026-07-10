**Owner:** Head of Specs Team
**Status:** Active
**Class:** Planning Document (Class 4)
**Cycle:** 2026-07-10__release-v6.9
**Release:** v6.9
**Last Updated:** 2026-07-10

---

# Release Plan — v6.9

## Readiness

**Trigger:** Roadmap rebalance `2026-07-10__scheduled` — Now horizon left intentionally empty (STEP 8.1 Option (b)), scoping deferred to this `plan release v6.9` invocation (DL-063). 2nd consecutive 🔴 Product Value Alert (ratio=0.18, U=9/G=16/D=24/P=0 of 49, window v6.4–v6.8) named `BLG-FEAT-64` as the mandatory pull-forward anchor candidate, with `BLG-FEAT-65` as secondary.

**Prior cycle:** `2026-07-08__release-v6.8` — Verified, Closed_with_actions, post-ship complete 2026-07-09.

### 1.1 Backlog Age Advisory

No spec/documentation debt item (`BLG-SPEC-*`) is a candidate for this release's scope (scope is limited to the two named Product Value Alert pull-forwards — see §Scope). No advisory triggered.

### 1.2 Provisional-Target Advisory

Both scope candidates carry `Provisional-Target: Unscheduled` (neither was horizon-planned into v6.9 specifically — the Now horizon was empty by Option (b) choice, so no item could have carried a `v6.9` provisional target).

ℹ 0 item(s) carry `Provisional-Target: v6.9`. 2 item(s) (`BLG-FEAT-64`, `BLG-FEAT-65`) carry `Provisional-Target: Unscheduled` — consistent with their status as directly-named mandatory pull-forwards rather than horizon-scheduled items.

### 1.3 Design-Gate Language Scan

Neither `BLG-FEAT-64` nor `BLG-FEAT-65` contains the literal phrases "design decision required" / "pending design" / "requires UX decision." However, both carry observable UI acceptance criteria:
- `BLG-FEAT-64` AC-02: frontend "Recheck compliance" action rendering pass/fail/override-acknowledged states, matching `PreEntryValidationPanel`'s visual pattern.
- `BLG-FEAT-65` AC-01–03: risk flag badge on the Positions page showing historical gap magnitude.

**Design dependency detected** for both items — surfaced to the Pre-sprint Required Decisions checklist / STEP 4.1 design gate classification (see STEP 4.1 below). Non-blocking at this step.

### 1.4a Perennial-Return Check

Neither `BLG-FEAT-64` nor `BLG-FEAT-65` appears in `2026-07-08__release-v6.8/stage4_backlog_slice.md` (both are newly-named candidates from the 2026-07-10 rebalance, not returning items). No perennial-return disposition required.

### 1.4b Within-Sprint Date Gate Classification

No candidate item in this release's scope carries a gate condition with a specific calendar clearing date. `BLG-FEAT-64` AC-04 and `BLG-FEAT-65` AC-04 both require a §13 sign-off, but this is a same-sprint execution deliverable (Strategy Rules & System Intent Owner review during the story itself), not an externally-timed date gate. Both items classified **firm** capacity (see §Scope).

### 1.4 Gate-Condition Proximity Scan (incl. Arc 4 Data Density Sub-Check)

Live production query performed this session (`GET /trades`, `GET /trade-plans`, `GET /analytics/arc5-compliance` via the application `X-API-Key` registered under `BLG-OPS-99`, v6.8):

| Item | Gate condition | Current trajectory | Projected clear date |
|------|----------------|---------------------|----------------------|
| SI-02 (condition 1) | ≥20 closed trades with **linked** trade_plans | **NOT MET** — confirmed live: `total_trades = 20`, `trade_plans = 11`, **`linked (position_id NOT NULL) = 0`**. Identical to the v6.8 closure finding — zero new trade-plan-linked closes have accrued since the `BLG-BE-46` forward-fix shipped (2026-07-09). Gate cannot clear from trade-count accumulation alone; requires new `trade_plans` to be created and closed under the fixed linkage going forward. | Not calculable — no linked closes yet to establish a rate. Re-check at next release planning readiness scan. |
| PO-02 (6+ months AI journal entries) | Journal entry volume/duration threshold | trajectory unknown — no journal-count endpoint resolvable this session | data not available — Product Owner to surface at readiness review |
| PO-04 (50+ trades with plans) | Trade-plan volume threshold | 11 total trade_plans recorded to date (all-time); rate not established | data not available — Product Owner to surface at readiness review |

**Carry-forward applied (v6.8 → v6.9, per `lessons_learnt_closure.md` Carry-Forward item 2):** SI-02 is treated as still NOT MET this cycle, consistent with the prior cycle's explicit warning not to expect the gate to clear from the `BLG-BE-46` fix alone. This live query confirms that warning holds — no drift toward clearance detected.

**Outstanding Action check (v6.8 closure §6, item 1):** "File a follow-up backlog item tracking `BLG-BE-46`'s deferred historical backfill" — **confirmed already satisfied.** `BLG-BE-55 — trade_plans.position_id historical backfill design` was filed via idea intake `IW-20260710-01` at roadmap rebalance `2026-07-10__scheduled`, before this release planning invocation. No escalation to Head of Specs Team required.

**Do not halt.** All of §1.1–§1.4 are advisory. Proceeding to Scope Extraction.

```yaml
# state.json update (STEP 1):
artifacts.stage1_readiness: pass
```

---

## Scope

**Scope decision (Product Owner, delegated authority):** Release v6.9 scope is the two named mandatory Product Value Alert pull-forwards from rebalance `2026-07-10__scheduled`. No roadmap reprioritisation occurs here — this is a straight translation of the already-named anchor candidates into execution-ready scope, per this engine's Purpose (§1) and the Option (b) deferral that handed scoping authority to this invocation.

| S2-ID | Backlog Item | Epic | Description |
|-------|--------------|------|-------------|
| S2-01 | `BLG-FEAT-64` | EPIC-01 | On-demand pre-entry (SI-01) rule recheck for open positions — primary mandatory pull-forward |
| S2-02 | `BLG-FEAT-65` | EPIC-02 | Overnight/weekend gap risk flag for open positions — secondary mandatory pull-forward |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| PO-02 / PO-04 (Arc 4 remainder) | Data-density gates not met (6+ months AI journals / 50+ trades with plans); confirmed still not queryable/met this session | Re-check at next release planning readiness scan |
| SI-02 (Arc 5, further work) | Gate condition 1 confirmed NOT MET live this session (0/20 linked trade-plans); backfill-design item `BLG-BE-55` now filed and unscheduled | Re-check once forward-linkage accrues or `BLG-BE-55` is scheduled |
| `BLG-SPEC-35` (PO-02 §13 boundary review) | Gate: PO-02 sprint planning imminent — not met (PO-02 not in scope this release) | Re-review when PO-02 sprint planning becomes imminent |
| `BLG-GOV-74` / `BLG-GOV-140` / `BLG-GOV-141` | Genuine calendar gates (quarterly AI-usage review 2026-08-29; quarterly §13 self-audit / AI output logging audit 2026-09-24) — not yet due | First cycle after respective due dates |
| `BLG-GOV-28` (PT-04 §13 compliance review) | Flagged overdue at 2026-07-10 rebalance, not yet dispositioned by Head of Specs Team; outside this release's named scope | Head of Specs Team disposition, outside this routine's authority |
| `BLG-GOV-105` (Arc 6 PS-03 pre-assessment) | Flagged possible duplicate of shipped `BLG-GOV-45` at 2026-07-10 rebalance, not yet dispositioned | Head of Specs Team disposition, outside this routine's authority |
| All other open backlog items (~240) | Not named as mandatory pull-forwards; no `Provisional-Target: v6.9` items exist (Now horizon was empty by Option (b) choice) | Candidate pool for future release planning cycles |

```yaml
# state.json update (STEP 2):
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Head of Engineering; Strategy Rules & System Intent Owner | RISK-01 | None — independent of EPIC-02 |
| EPIC-02 | S2-02 | Head of UX & Design; Head of Engineering | RISK-02 | None — independent of EPIC-01 |

Both EPICs are independent (different backend surfaces, no shared data model change, no shared endpoint) — may execute in either order or in parallel.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | AC-04 requires a §13 sign-off confirming the on-demand SI-01 recheck introduces no new automation/prediction surface. Expected fast pass given SI-01 precedent, but sign-off is not yet recorded. | Low | Strategy Rules & System Intent Owner completes §13 review as part of story execution, before EPIC-01 DoQ sign-off. | null |
| RISK-02 | EPIC-01, EPIC-02 | Both EPICs carry observable UI acceptance criteria (compliance-recheck panel; risk flag badge) — Design Gate is required before Sprint Planning may seal (see STEP 4.1). | Medium | Run `run design-gate --cycle 2026-07-10__release-v6.9` immediately after this plan publishes, before `plan sprint`. | null |
| RISK-03 | EPIC-02 | AC-04 requires the gap-risk flag to remain informational-only (no directional prediction) per §13 boundary — same class of review as RISK-01, lower likelihood of issue given it reuses existing deterministic calendar/OHLCV data. | Low | Strategy Rules & System Intent Owner §13 confirmation during story execution. | null |

```yaml
# state.json update (STEP 3):
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

Checked: every S2-ID maps to exactly one EPIC (S2-01→EPIC-01, S2-02→EPIC-02); every RISK-ID (RISK-01, RISK-02, RISK-03) declares a valid `Relates to` EPIC that exists in the Execution Plan table; no orphaned S2/EPIC/RISK references found. **PASS.**

```yaml
# state.json update (STEP 3.5):
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## STEP 4 — Backlog Slice (Commitment)

`stage4_backlog_slice.md` written (ST-01/EPIC-01, ST-02/EPIC-02). Backlog lock acquired (`RP:v6.9:2026-07-10__release-v6.9`), release slice section appended to `claude/backlog/backlog.md` with marker (idempotency confirmed — marker not previously present), transaction prepared → committed (`BLTX-20260710-01`), lock released. `stage4_issue_manifest.json` produced (2 entries, one per ST item).

### STEP 4.1 — Design Gate Classification

Both ST-01 (`delegated_frontend`, observable UI ACs: recheck-panel pass/fail/override rendering) and ST-02 (`delegated_frontend`, observable UI ACs: risk flag badge rendering + Friday-close timing) carry at least one observable UI acceptance criterion.

**⚠ DESIGN GATE REQUIRED before plan sprint — 2 items classified as UI-facing. Run: `run design-gate --cycle 2026-07-10__release-v6.9`**

```yaml
# state.json update (STEP 4 outcome):
artifacts.stage4_backlog_slice: pass
artifacts.stage4_issue_manifest: pass
attributes.backlog_committed: true
attributes.design_gate_required: true
status: Committed
locks.backlog_lock.status: released
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` (rebalance `2026-07-10__scheduled`) carries 0 active initiative rows (CPS=N/A) — no matching row for either EPIC. Tier 3 resolution applies: use STEP 4 inline estimates; no advisory required.

**Estimate:** EPIC-01 (ST-01) ~2–3 days (M); EPIC-02 (ST-02) ~2–3 days (M). Combined estimate: ~4–6 days.

**Historical baseline (`claude/cycles/velocity_metrics.md`):** rolling 6-cycle average (v6.3–v6.8) = 1.00 planned/completed ratio. Sprint sizes on record range 2–24 stories, with the large majority of single-sprint releases comfortably absorbing 2–17 stories at 100% completion. A 2-story, 2-EPIC release is well within this project's demonstrated single-sprint capacity.

**No explicit `--timebox` / `--capacity` was supplied at invocation** — assumption recorded: standard single-sprint timebox, capacity consistent with the v6.3–v6.8 historical baseline (no explicit capacity constraint flagged by Product Owner).

**Outcome: PASS.** No phasing recommendation required — scope fits comfortably within a single sprint.

```yaml
# state.json update (STEP 4.5):
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## STEP 5 — Roadmap Annotation

No formal `## v6.9` roadmap section exists (Option (b)-deferred release). Annotated the `**Next planned release:**` line in `current_roadmap.md` §1 instead, per this engine's fallback rule. Roadmap lock (`RA:v6.9:2026-07-10__release-v6.9`) acquired, annotation written (idempotency confirmed — marker not previously present), transaction committed (`RATX-20260710-01`), lock released.

```yaml
# state.json update (STEP 5):
artifacts.roadmap_txn: committed
locks.roadmap_lock.status: released
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity / 5.7 Decision Record Integrity

**5.5 Cross-Stage Integrity:**
- S2-01 → EPIC-01: confirmed (Scope §, Execution Plan §). S2-02 → EPIC-02: confirmed.
- EPIC IDs in `stage4_backlog_slice.md` (EPIC-01, EPIC-02) match `release_plan.md §Execution Plan` (EPIC-01, EPIC-02): confirmed, no drift.
- RISK-01, RISK-02, RISK-03 (referenced in the Execution Plan EPIC table) all appear in the Risk Register Summary with valid `Relates to` targets that exist in the EPIC table: confirmed.
- No orphaned S2/EPIC/RISK/ST references found. **PASS.**

**5.7 Decision Record Integrity:** `artifacts.escalations` was never set to `present` this cycle (no escalations raised — `open_escalations` is empty throughout). Per this step's precondition ("run only when `artifacts.escalations = present`"), this check is **not_applicable** — skipped.

```yaml
# state.json update (STEP 5.5):
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```

---

## Publish Gate Evaluation

| Condition | Result |
|-----------|--------|
| `open_escalations` empty | ✅ (0 escalations raised this cycle) |
| Deferred escalations all `Blocks execution: No`; `deferred_execution_blockers` empty | ✅ (no deferred escalations) |
| `stage4_5_capacity_check` = pass or warn | ✅ pass |
| `stage5_5_cross_stage_integrity` = pass | ✅ pass |
| `stage5_7_decision_record_integrity` = pass or not_applicable | ✅ not_applicable |
| `stage1_readiness`, `stage3_5_model_integrity` = pass | ✅ pass, pass |
| `plan_structured`, `plan_executable`, `backlog_committed` = true | ✅ true, true, true |

**Engine-specific completion condition:**
- `docs/product/scope/scope--2026-07-10__release-v6.9-si01-recheck-gap-risk-flag.md` exists ✅
- `docs/product/decisions/decisions--2026-07-10__release-v6.9.md` exists ✅
- `locks.backlog_lock.status = released` ✅
- `locks.roadmap_lock.status = released` ✅

**Gate PASSES.** `status = Validated`, `publish_eligible = true`.
