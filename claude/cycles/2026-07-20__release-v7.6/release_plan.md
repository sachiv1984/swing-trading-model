Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v7.6
Cycle: 2026-07-20__release-v7.6
Last Updated: 2026-07-20

# Release Plan — v7.6

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

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Observable UI acceptance criteria (action presence, print/PDF output legibility and layout without app chrome) require Design Gate pass per CLAUDE.md's frontend-visible-change rule before sprint planning may seal. | Medium | Run `run design-gate --cycle 2026-07-20__release-v7.6` before `plan sprint`; Playwright coverage or human staging sign-off required per AC at sprint execution. | null |
| RISK-02 | EPIC-02 | None — documentation-only change (regression baseline doc), no code or UI surface, no gate dependency. | Low | N/A | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

All S2/EPIC/RISK IDs are self-consistent (S2-01 ↔ EPIC-01 ↔ RISK-01; S2-02 ↔ EPIC-02 ↔ RISK-02; two independent chains, no orphans). No local model integrity issues.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` has no matching row for either item (both backlog-driven, not initiative-register scope) — falls back to each item's own inline estimate: `BLG-FE-119` Effort M (~1–2 days); `BLG-QA-112` Effort S (~1 day). Combined: ~2–3 days across 2 EPICs.

This is well within any single-sprint capacity baseline used across recent cycles (v7.5 shipped 4 EPICs; v7.4/v7.3 shipped 4 and 7 items respectively). No phasing recommendation required.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Cross-Stage Integrity — 5.5 / 5.7

**5.5 Cross-Stage Integrity:** S2-01 maps to EPIC-01, S2-02 maps to EPIC-02; both EPICs in `stage4_backlog_slice.md` match this document; RISK-01/RISK-02 appear in the Risk Register above and are referenced by their respective EPICs. No orphaned references.

**5.7 Decision Record Integrity:** Not applicable — no escalations were raised this cycle (`artifacts.escalations` not present).

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```
