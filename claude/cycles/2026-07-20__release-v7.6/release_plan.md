Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v7.6
Cycle: 2026-07-20__release-v7.6
Last Updated: 2026-07-20

# Release Plan — v7.6

## PO-Directed Post-Publish Scope Expansion (2026-07-20)

This cycle reached `state.json.status = Published` earlier in the same session with a 2-EPIC scope (EPIC-01/EPIC-02). The user then asked to push more work into the sprint. Neither the Amendment Cycle Engine (restricted to `emergency-fix`/`hard-blocker`; "more capacity" does not qualify, and the lifecycle state didn't match anyway — `sprint_sealed` was still `true` from v7.5, `status` was `Published` not `Sprint_Planning_Complete`) nor re-invoking Release Planning (blocked by the Published terminal-state guard) offered a compliant path, and Sprint Planning has no mechanism to pull items beyond the confirmed slice. With zero downstream consumption of the published plan (no Design Gate run, no Sprint Planning run), the Product Owner explicitly directed a same-session bypass reopening this cycle's artefacts. Full rationale: `claude/roadmap/decision_log.md` DL-073. EPIC-03 through EPIC-08 below were added by this reopen.

## Readiness

Roadmap confirmed: v7.6 formally anchored in `current_roadmap.md` §1/§3 this session (out-of-band direct-write, DL-072 — see run_manifest.md for full preflight -1.2 narrative). Anchor scope: `BLG-FE-119` (PDF / print-friendly export).

**1.1 Backlog age advisory:** N/A — anchor item is a frontend feature, not spec/documentation debt.

**1.2 Provisional-Target advisory:** 1 item carries `Provisional-Target: v7.6` (`BLG-FE-119`, set at this session's roadmap formalization). 0 items with a mismatched or absent signal in this release's scope.

**1.3 Design-gate language scan:** `BLG-FE-119`'s acceptance criteria are observable-UI ("Print / Export PDF" action availability; output legibility/formatting) — design dependency flagged. Surfaced at STEP 4.1 below: `design_gate_required = true`.

**1.4a Perennial-Return check:** `BLG-FE-119` was never named in any prior cycle's `stage4_backlog_slice.md` (only carried a stale `Provisional-Target` twice, v7.3/v7.4, without being scoped) — this is not a `returned_to_backlog` pattern, so the perennial-return counter does not apply. No PO disposition required under this check.

**1.4b Within-sprint date gate:** N/A — `BLG-FE-119` carries no gate condition of any kind (no date-based or trade-volume-based gate).

**1.4 Gate-Condition Proximity Scan + Arc 4 data density sub-check (mandatory):** No gate-conditional items in this release's scope. Arc 4 gate metrics re-checked live this session (production API, 2026-07-20T12:43Z) for standing advisory value:

| Item | Gate condition | Current trajectory | Projected clear date |
|------|-----------------|---------------------|------------------------|
| PO-04 | 50+ trades with plans | `GET /trades` → 20 closed trades total (unchanged since 2026-07-06) | data insufficient to project a rate — trajectory flat |
| SI-02 cond. (1) | 20+ trades with linked plans | `GET /trade-plans` → 11 total, 0 with non-null `position_id` (unchanged since 2026-07-06) | trajectory unknown — `BLG-FE-109` ("Start Trade from Plan") shipped v7.3 but not yet exercised by any closed trade |
| SI-02 cond. (3) | Non-trivial drift variance | `GET /analytics/behavioural-drift` → `insufficient_data`, 9 trades in 90-day window (unchanged since 2026-07-12) | trajectory unknown |

**Bottom line:** SI-02 gate remains NOT MET — 8th consecutive unchanged reading across all three conditions since 2026-07-12 (spanning 2026-07-12/13/14/15/16/17/20; no re-check recorded 07-18/19). Not relevant to this release's scope (no Arc 5 items in v7.6). PO-02/PO-04 gated Arc 4 items likewise out of scope.

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

Scope document: `docs/product/scope/scope--2026-07-20__release-v7.6-pdf-print-friendly-export.md`

| S2-ID | Description | Maps to |
|-------|-------------|---------|
| S2-01 | PDF / print-friendly export for `WeeklyDigest.js` and `TradePlan.js` | EPIC-01 |
| S2-02 | Regression suite baseline update for `BLG-FE-115`-`119` interaction surfaces (`BLG-QA-112`, gate-conditional item, gate fired by S2-01 entering scope) | EPIC-02 |
| S2-03 | P&L export audit trail reconciliation (`BLG-FEAT-79`) | EPIC-03 |
| S2-04 | Backend error-response envelope standardisation (`BLG-BE-65`) | EPIC-04 |
| S2-05 | OpenAPI-derived Playwright fixture library (`BLG-QA-114`) | EPIC-05 |
| S2-06 | Nightly batch-job idempotency audit (`BLG-BE-62`) | EPIC-06 |
| S2-07 | Consolidated monthly AI cost view (`BLG-FEAT-77`) | EPIC-07 |
| S2-08 | Ticker/market input sanitisation regression suite (`BLG-QA-69`) | EPIC-08 |

### Items explicitly deferred
None.

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

Decisions record: `docs/product/decisions/decisions--2026-07-20__release-v7.6.md`

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 | Head of UX & Design; Frontend Specs & UX Documentation Owner | RISK-01 | None — standalone, no dependencies |
| EPIC-02 | S2-02 | QA Lead | RISK-02 | Gate-triggered companion to EPIC-01; documentation-only, no Design Gate dependency |
| EPIC-03 | S2-03 | Financial Reporting & Records Owner | RISK-03 | None — standalone, no dependencies |
| EPIC-04 | S2-04 | Backend Engineering Patterns Owner | RISK-04 | None — standalone, no dependencies |
| EPIC-05 | S2-05 | QA & Testing Owner | RISK-05 | None — standalone, no dependencies |
| EPIC-06 | S2-06 | Backend Engineering Patterns Owner | RISK-06 | None — standalone, no dependencies |
| EPIC-07 | S2-07 | FinOps & Resource Architect | RISK-01 | None — standalone, no dependencies |
| EPIC-08 | S2-08 | Director of Quality; Backend Engineering Patterns Owner | RISK-08 | None — standalone, no dependencies |

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01, EPIC-07 | Observable UI acceptance criteria (EPIC-01: action presence, print/PDF output legibility and layout without app chrome; EPIC-07: new consolidated cost summary view) require Design Gate pass per CLAUDE.md's frontend-visible-change rule before sprint planning may seal. | Medium | Run `run design-gate --cycle 2026-07-20__release-v7.6` before `plan sprint`; Playwright coverage or human staging sign-off required per AC at sprint execution. | null |
| RISK-02 | EPIC-02 | None — documentation-only change (regression baseline doc), no code or UI surface, no gate dependency. | Low | N/A | null |
| RISK-03 | EPIC-03 | None — backend audit/reconciliation, no UI surface, no gate dependency. | Low | N/A | null |
| RISK-04 | EPIC-04 | None — backend audit/documentation, no UI surface, no gate dependency. | Low | N/A | null |
| RISK-05 | EPIC-05 | None — test infrastructure, no UI surface, no gate dependency. | Low | N/A | null |
| RISK-06 | EPIC-06 | None — backend audit, no UI surface, no gate dependency. | Low | N/A | null |
| RISK-08 | EPIC-08 | None — backend test suite, no UI surface, no gate dependency. | Low | N/A | null |

**Effort Day-Range Advisory:** 5 of the 6 EPIC-03–08 items (all except `BLG-QA-69`, which states "M (~1–2 days)") carry `Effort: M` with no explicit day-range parenthetical, per `shared_standards.md §16.12`. Not backfilled here — owner judgment required at next `groom backlog`. Capacity check below uses a conservative M midpoint of 2.0 days for these 5.

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

All S2/EPIC/RISK IDs are self-consistent: S2-01↔EPIC-01↔RISK-01, S2-02↔EPIC-02↔RISK-02, S2-03↔EPIC-03↔RISK-03, S2-04↔EPIC-04↔RISK-04, S2-05↔EPIC-05↔RISK-05, S2-06↔EPIC-06↔RISK-06, S2-07↔EPIC-07↔RISK-01 (shared), S2-08↔EPIC-08↔RISK-08 — eight EPIC chains, no orphans.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` has no matching row for any of the 8 items (all backlog-driven, not initiative-register scope) — falls back to each item's own inline estimate.

| EPIC | Backlog item | Effort | Midpoint (days) |
|------|--------------|--------|------------------|
| EPIC-01 | `BLG-FE-119` | M (~1–2 days) | 1.5 |
| EPIC-02 | `BLG-QA-112` | S (~1 day) | 1.0 |
| EPIC-03 | `BLG-FEAT-79` | M (no range) | 2.0 |
| EPIC-04 | `BLG-BE-65` | M (no range) | 2.0 |
| EPIC-05 | `BLG-QA-114` | M (no range) | 2.0 |
| EPIC-06 | `BLG-BE-62` | M (no range) | 2.0 |
| EPIC-07 | `BLG-FEAT-77` | M (no range) | 2.0 |
| EPIC-08 | `BLG-QA-69` | M (~1–2 days) | 1.5 |

**Total estimated effort:** ~14.0 days midpoint (range ~11–17 days depending on where each unlabelled "M" falls within a typical 1.5–3 day band).
**Confirmed capacity:** ~24–28 working-day-equivalent per sprint (`workforce_capacity.md`, effective 2026-07-17 — same baseline `release_plan.md` and `sprint_capacity.md` used at v7.5).

~14 days of ~24–28 days is ~50–58% of ceiling — well within capacity, consistent with the v7.5 baseline (11–14 days, also ~50–58%). No phasing recommendation required; no over-allocation.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Cross-Stage Integrity — 5.5 / 5.7

**5.5 Cross-Stage Integrity:** All 8 S2-IDs map to their respective EPICs (S2-01↔EPIC-01 ... S2-08↔EPIC-08); all 8 EPICs in `stage4_backlog_slice.md` match this document; all RISK-IDs (RISK-01 through RISK-06, RISK-08) appear in the Risk Register above and are referenced by their respective EPICs. No orphaned references.

**5.7 Decision Record Integrity:** Not applicable — no escalations were raised this cycle (`artifacts.escalations` not present).

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```
