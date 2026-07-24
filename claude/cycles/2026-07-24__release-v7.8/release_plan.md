**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-24
**Cycle:** 2026-07-24__release-v7.8
**Release:** v7.8

# Release Plan — v7.8 — Release Visibility & Engineering Hardening

## Readiness

Roadmap release confirmed via STEP 8.1 Option (b) decision from `2026-07-24__scheduled` (see `run_manifest.md` §-1.2 for full citation) — no formal `## v7.8` section exists yet; `current_roadmap.md` §1 `**Next planned release:** [TBD]` is the annotation point (STEP 5). Preflight PASS (see `run_manifest.md`). Prior cycle `2026-07-20__release-v7.6` and the intervening `2026-07-21__release-v7.7` both closed clean (`post_ship_complete=true`, `next_cycle_unblocked=true`), 0 outstanding action-now gaps.

**Design-gate language scan (1.3):** 5 of 12 scoped items carry observable UI acceptance criteria (EPIC-01, EPIC-03, EPIC-04, EPIC-05, EPIC-06) — Design Gate required, see STEP 4.1.

**Gate-condition proximity scan (1.4):** No gate-conditional items in scope this cycle (all 12 items ungated). SI-02 (`BLG-GOV-107`) unchanged from `2026-07-24__scheduled` rebalance reading — NOT MET, 0/11 linked trade plans, `insufficient_data` drift, 9 trades in 90-day window. Not applicable to this release (`BLG-FEAT-73` excluded — see STEP 1.4a in `run_manifest.md`).

**Backlog age advisory (1.1):** None of the 12 selected items are spec/documentation debt type. Not triggered.

**Provisional-Target advisory (1.2):** 0 items carry `Provisional-Target: v7.8` (release unnamed until this cycle); all 34 candidate-pool items carried `Provisional-Target: TBD`. Advisory only — does not block selection.

```yaml
artifacts.stage1_readiness: pass
```

## Scope

**Firm scope — 12 items (S2-01–S2-12):**

| S2 | Item | Priority | Effort | Type |
|----|------|----------|--------|------|
| S2-01 | BLG-FE-128 — In-app "what's new" panel for most recent release | P2 | M (~2d) | Product Feature / Frontend |
| S2-02 | BLG-FEAT-84 — Automated Telegram changelog digest after each release | P2 | S (~1d) | Product Feature / Notifications |
| S2-03 | BLG-FE-127 — Accessibility pass on v7.7 notification UX components | P2 | S (~1d) | Frontend / Accessibility |
| S2-04 | BLG-FE-125 — Dark-mode contrast audit across Base44-generated pages | P2 | M (~2d) | Frontend / Accessibility |
| S2-05 | BLG-FEAT-81 — Monthly realized P&L CSV export | P2 | S (~1d) | Product Feature / Reporting |
| S2-06 | BLG-FEAT-82 — AI usage spend trend dashboard (Gemini/Claude, per release cycle) | P2 | M (~2d) | Product Feature / FinOps |
| S2-07 | BLG-SEC-20 — Scheduled rotation-and-audit cadence for third-party API keys | P2 | S (~1d) | Security / Process |
| S2-08 | BLG-SEC-21 — Rate-limiting review of public-facing endpoints | P2 | M (~2d) | Security |
| S2-09 | BLG-BE-71 — Shared retry/backoff decorator for external data calls | P2 | M (~2d) | Backend Engineering / Technical Debt |
| S2-10 | BLG-QA-117 — Flaky-test quarantine process for the Playwright suite | P2 | M (~2d) | QA / Process |
| S2-11 | BLG-QA-119 — Contract tests for highest-traffic frontend/backend endpoints | P2 | M (~2d) | QA / Backend Engineering |
| S2-12 | BLG-OPS-117 — Automated lint check for API contract `##` heading level | P2 | S (~1d) | Operations / CI Tooling |

**Items explicitly deferred (perennial-return, PO disposition — excluded from firm scope this cycle):**

| Item | Reason |
|------|--------|
| BLG-FEAT-73 — SI-02 Behavioural Drift Detection frontend build | 2nd consecutive return (v7.7 named-then-excluded; `2026-07-24__scheduled` un-versioned carry-forward). SI-02 gate (`BLG-GOV-107`) remains NOT MET, no live re-check possible this session. PO disposition: Option (b) — remove from horizon. See `run_manifest.md` STEP 1.4a. |
| BLG-FEAT-74 — PO-05 Lightweight Replay Mode | 2nd consecutive return (same pattern as above). §13 determinism pre-clearance never run; VH effort exceeds single-cycle sizing. PO disposition: Option (b) — remove from horizon. See `run_manifest.md` STEP 1.4a. |
| BLG-QA-122 — Broker statement reconciliation | Gate-conditional at the backlog-item level (no broker statement import mechanism exists). Not eligible for scope entry — excluded, not "deferred" in the returning-item sense. |

**Not selected this cycle (remain in backlog, un-scoped — no reprioritisation implied):** the remaining 21 P2/P3 items from the `IW-20260724-01` idea-intake addition not listed above (`BLG-GOV-251`, `BLG-BE-70`, `BLG-SPEC-96`, `BLG-BE-72`, `BLG-SPEC-97`, `BLG-GOV-252`, `BLG-GOV-253`, `BLG-QA-118`, `BLG-GOV-254`, `BLG-SPEC-98`, `BLG-SPEC-99`, `BLG-OPS-116`, `BLG-FE-126`, `BLG-OPS-118`, `BLG-OPS-119`, `BLG-SPEC-100`, `BLG-FEAT-83`, `BLG-QA-120`, `BLG-QA-121`, `BLG-GOV-255`, `BLG-SPEC-101`) — eligible for future release planning.

Scope document: `docs/product/scope/scope--2026-07-24__release-v7.8-release-visibility-engineering-hardening.md`

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 | Product Owner; Base44 Frontend Prompt Owner | RISK-01 | After Design Gate pass |
| EPIC-02 | S2-02 | Product Owner | null | No dependency |
| EPIC-03 | S2-03 | Head of UX & Design | RISK-01 | After Design Gate pass |
| EPIC-04 | S2-04 | Base44 Frontend Prompt Owner | RISK-01 | After Design Gate pass |
| EPIC-05 | S2-05 | Financial Reporting & Records Owner | RISK-01 | After Design Gate pass |
| EPIC-06 | S2-06 | FinOps & Resource Architect | RISK-01 | After Design Gate pass |
| EPIC-07 | S2-07 | Cybersecurity & Trust Lead | null | No dependency |
| EPIC-08 | S2-08 | Cybersecurity & Trust Lead | RISK-04 | No dependency |
| EPIC-09 | S2-09 | Backend Engineering Patterns Owner | RISK-02 | No dependency |
| EPIC-10 | S2-10 | Director of Quality | null | No dependency |
| EPIC-11 | S2-11 | Head of Engineering | RISK-03 | No dependency |
| EPIC-12 | S2-12 | Head of Specs Team | null | No dependency |

EPIC-07/EPIC-08: both owned by Cybersecurity & Trust Lead; no sequencing dependency between them, but EPIC-07 (key rotation cadence) is the lighter item and may run first for scheduling convenience only — not a hard constraint.

EPIC-02/07/08/09/10/11/12 have no UI surface and no cross-EPIC dependency on EPIC-01/03/04/05/06; may execute fully in parallel to the design-gated cluster.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | Release-level (EPIC-01/03/04/05/06) | 5 of 12 items carry observable UI acceptance criteria — Design Gate is a hard prerequisite before Sprint Planning seals | Medium | `run design-gate --cycle 2026-07-24__release-v7.8` must run and PASS (or record a bypass with authority+reason) before `plan sprint` is invoked | null |
| RISK-02 | EPIC-09 | `BLG-BE-71`'s shared retry/backoff decorator touches external call sites (Yahoo Finance, Alpaca); migrating a call site could regress existing error-handling behaviour | Low | AC is explicitly scoped to the highest-traffic call site only as proof-of-pattern, not a full retrofit — bounds the regression surface | null |
| RISK-03 | EPIC-11 | `BLG-QA-119`'s "3 highest-traffic endpoints" selection has no telemetry-backed ranking on record | Low | Head of Engineering to confirm the 3 pilot endpoints (positions, trades, dashboard per the backlog item's own problem statement) before implementation begins | null |
| RISK-04 | EPIC-08 | `BLG-SEC-21` rate-limiting review could surface more findings than fit this cycle's remaining capacity | Low | AC only requires each undocumented-limit endpoint be either remediated or explicitly accepted-risk categorised — no open-ended scope creep | null |

Decisions record: `docs/product/decisions/decisions--2026-07-24__release-v7.8.md`

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

## Integrity Validation — 3.5 Local Model Integrity

All EPIC IDs (EPIC-01–EPIC-12) map 1:1 to declared S2 IDs (S2-01–S2-12). All RISK IDs (RISK-01–04) referenced in the Execution Plan table appear in the Risk Register. No orphaned references. PASS.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

## Capacity Check

**Capacity Inputs** (per `workforce_capacity.md` / DL-069 convention, consistent with v7.6/v7.7's own capacity docs):
```
Available FTE:   1 (solo developer / autonomous execution engine)
Total capacity:  ~24–28 working-day-equivalent per sprint
```

**Effort Band Lookup (ST-14):** `claude/scoring/scored_initiatives.md` present but explicitly states 0 active roadmap initiatives this cycle and no separate initiative-row lookup applicable to standalone backlog items with `Provisional-Target: TBD` — STEP 4 inline estimates used for all 12 EPICs, no advisory required (see `run_manifest.md`).

| EPIC | Item | Effort | Midpoint (days) |
|------|------|--------|------------------|
| EPIC-01 | BLG-FE-128 | M | 2.0 |
| EPIC-02 | BLG-FEAT-84 | S | 1.0 |
| EPIC-03 | BLG-FE-127 | S | 1.0 |
| EPIC-04 | BLG-FE-125 | M | 2.0 |
| EPIC-05 | BLG-FEAT-81 | S | 1.0 |
| EPIC-06 | BLG-FEAT-82 | M | 2.0 |
| EPIC-07 | BLG-SEC-20 | S | 1.0 |
| EPIC-08 | BLG-SEC-21 | M | 2.0 |
| EPIC-09 | BLG-BE-71 | M | 2.0 |
| EPIC-10 | BLG-QA-117 | M | 2.0 |
| EPIC-11 | BLG-QA-119 | M | 2.0 |
| EPIC-12 | BLG-OPS-117 | S | 1.0 |

**Total estimated effort:** ~19.0 days midpoint.
**Confirmed capacity:** ~24–28 working-day-equivalent.
**Utilisation:** ~68–79% of ceiling.

**No over-allocation. No capacity WARN.** Consistent with the `2026-07-21__release-v7.7` full-capacity-fill precedent while retaining ~20–30% buffer against estimate variance. No Phasing Recommendation needed (outcome is `pass`, not `warn`).

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

## Roadmap Annotation

See `current_roadmap.md` §1 `**Next planned release:**` line — execution notes appended at STEP 5 (below). No formal `## v7.8` roadmap section is created by this routine (Release Planning may not alter roadmap scope); annotation only.

## Cross-Stage Integrity (5.5) / Decision Record Integrity (5.7)

**5.5:** All S2 IDs (S2-01–S2-12) map to EPICs (EPIC-01–EPIC-12, 1:1). All EPIC IDs in `stage4_backlog_slice.md` match this Execution Plan. All RISK IDs (RISK-01–04) appear in the Risk Register above. No orphaned references. PASS.

**5.7:** No escalations were raised this cycle (`artifacts.escalations` not present) — this check is `not_applicable`.

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```
