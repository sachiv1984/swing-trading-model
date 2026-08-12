Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v8.7
Cycle: 2026-08-12__release-v8.7
Last Updated: 2026-08-12

# Release Plan — v8.7

## Readiness

Preflight PASS (see `run_manifest.md` STEP -1). Release cleared for planning via STEP -1.2 Option (b) equivalence — no formal `## v8.7` roadmap section exists; `2026-08-11__scheduled` rebalance recorded a documented Option (b) defer decision (4th consecutive firing), which this routine treats as authorization to draw scope directly from the ungated backlog pool for `plan release`.

**Capacity assumption (user-directed):** "Use full capacity, user features to be prioritised." Confirmed capacity band: ~24–28 working-day-equivalent units (`workforce_capacity.md`, unchanged since 2026-07-17). Scope selection targets this band with user-facing product/UX items sequenced first in the Execution Plan.

Advisories (full detail in `run_manifest.md`):
- Backlog Age Advisory: no spec/documentation debt items in scope aged ≥2 cycles without story assignment.
- Provisional-Target Advisory: 4 items carry `Provisional-Target: v8.7 or later` (`BLG-FE-156`, `BLG-FE-157`, `BLG-QA-148`, `BLG-BE-96`); 17 items are `TBD`/unassigned, drawn from the ungated pool.
- Design-Gate Language Scan: no explicit design-pending language found; `BLG-FEAT-84`'s exact field placement/wording is a routine UX design call, not a blocking dependency.
- Gate-Detection Procedure (`scripts/scan_backlog_gate_conditions.py`): 292 items scanned, 175 gated. All 21 selected items confirmed ungated.
- Perennial-Return Check / Within-Sprint Date Gate: not applicable — no gate-conditional items in scope.

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

Scope document: `docs/product/scope/scope--2026-08-12__release-v8.7.md`

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | User-facing product features & UX completion (thesis pre-mortem field, trade-plan-link outcome banner, AI-draft badge, 3 theme-consistency fixes) |
| S2-02 | EPIC-02 | Trade-plan data integrity closure — staging verification + legacy orphaned-row audit (mandatory carryover, v8.6 PO risk-acceptance condition) |
| S2-03 | EPIC-03 | Test coverage for shipped UI & financial correctness (Playwright shadcn-token coverage, tax-year boundary assertion) |
| S2-04 | EPIC-04 | Backend reliability & performance hardening (Gemini retry/backoff extension, N+1 query audit, SI-04 schema pre-design) |
| S2-05 | EPIC-05 | Security hardening (Gemini prompt-injection resistance test, rate-limit audit) |
| S2-06 | EPIC-06 | Operations & infrastructure debt (Render headroom reassessment, build/deploy path filter doc, perf-baseline-drift script fix — closes a 3-cycle carry-forward) |
| S2-07 | EPIC-07 | Governance & spec debt (cross-EPIC schema-drift rule, Roadmap Unlock Tracker, §13 preview-analytics policy question, canonical "gated" DataState spec) |

### Items explicitly deferred

None. This cycle draws directly from the ungated backlog pool (no formal roadmap Now-horizon scope exists to defer from — see Readiness). Remaining ungated P1/P2 items not selected (e.g. further BLG-GOV/QA/OPS process items) remain available in `backlog.md` for the next release cycle; none were displaced from a committed scope.

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

**Format note:** full acceptance criteria live in `stage4_backlog_slice.md`. This table is sequencing/ownership/risk only.

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 | Product Owner; Head of UX & Design | RISK-01 | None — leads capacity allocation per user directive |
| EPIC-02 | S2-02 | Head of Engineering; Data Model, Domain & Schema Owner | RISK-02 | None — mandatory, no dependency on other EPICs this cycle |
| EPIC-03 | S2-03 | QA & Testing Owner | RISK-03 | ST-08 depends on EPIC-01/ST-06's shipped token usage remaining stable |
| EPIC-04 | S2-04 | Backend Engineering Patterns Owner | RISK-04 | None |
| EPIC-05 | S2-05 | Cybersecurity & Trust Lead | RISK-05 | None |
| EPIC-06 | S2-06 | Infrastructure & Operations Owner | RISK-06 | None |
| EPIC-07 | S2-07 | Head of Specs Team | RISK-07 | None |

**EPIC-01:** Leads the table per the user's explicit "user features to be prioritised" instruction. All 6 items are ungated, several directly complete or extend v8.6 work that shipped with a known gap (`BLG-FE-158` surfaces `BLG-BE-91`'s linkage outcome; `BLG-BE-95` unblocks the Setup Thesis Digest panel's AI-draft badge, omitted in v8.6 for lack of this field).

**EPIC-02:** `BLG-BE-96` carries an explicit Product Owner risk-acceptance condition from v8.6 ("do not defer further" — see `qa_evidence_EPIC-02.md`). Treated as a hard scope commitment, not subject to the "user features first" ordering (data-integrity foundation work, non-negotiable carryover).

**EPIC-06:** `BLG-OPS-142` closes the `check_api_performance_baseline_drift.py` fix carried across 3 consecutive Post-Ship Closures (v8.4→v8.5→v8.6) — see `run_manifest.md` Carry-Forward Advisory.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | `BLG-FEAT-84`'s exact invalidation-condition field placement/wording is not yet specified beyond "optional field" | Medium | Head of UX & Design confirms placement/copy at sprint planning or via a lightweight design note before implementation | null |
| RISK-02 | EPIC-02 | `BLG-BE-96` requires live staging/Postgres access; the v8.6 attempt at the same verification could only run mocked-DB tests (no live environment reachable in-sandbox) | High | Confirm staging DB access before/at sprint planning; if still unavailable, execute the two live-DB checks (linkage confirmation, orphaned-row query, constraint validation) via the best available proxy and record the residual gap explicitly rather than silently substituting mocks again | null |
| RISK-03 | EPIC-03 | `BLG-FE-157`'s Playwright coverage depends on the shadcn tokens registered in v8.6 remaining stable; any EPIC-01 theme change (`BLG-FE-156`) landing first could shift selectors | Low | Land `BLG-FE-156` and `BLG-FE-157` in the same sprint window; sequence coverage authoring after the modal conversion lands | null |
| RISK-04 | EPIC-04 | `BLG-BE-90`'s N+1 query audit may surface additional remediation scope beyond a single-cycle fix | Low | Scope this cycle to audit + fix of clearly-attributable cases only; file follow-up backlog items for anything requiring broader refactor | null |
| RISK-05 | EPIC-05 | Security testing (`BLG-SEC-30`/`31`) must not exercise production endpoints or real rate limits against live infrastructure | Medium | Run all prompt-injection and rate-limit tests against staging/test environment only; no production traffic generation | null |
| RISK-06 | EPIC-06 | None material — all 3 items are documentation/reassessment/script-fix scoped, low blast radius | Low | Standard review | null |
| RISK-07 | EPIC-07 | None material — all 4 items are governance/spec documents, no code or runtime behaviour change | Low | Standard review | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

All 21 in-scope items map to a data model or existing schema with no unresolved model ambiguity: `BLG-BE-95`/`BLG-BE-96` operate on the existing `trade_plans` table (no new entities); `BLG-BE-90`'s N+1 audit and `BLG-BE-89`'s retry/backoff extension touch existing endpoints/patterns only; frontend items (EPIC-01/EPIC-03) consume existing API response fields or Tailwind tokens already registered in v8.6. No new database migrations required by this scope. Plan is executable as scoped.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` empty (0 active initiatives) — no pre-assigned effort bands; all EPICs sized via inline STEP 4 estimate (see `stage4_backlog_slice.md` / `sprint_capacity.md`).

Confirmed capacity band: **~24–28 working-day-equivalent units** (`workforce_capacity.md`, unchanged since 2026-07-17).

| EPIC | Subtotal (days) |
|------|------------------|
| EPIC-01 | 6.25 |
| EPIC-02 | 1.00 |
| EPIC-03 | 1.50 |
| EPIC-04 | 4.50 |
| EPIC-05 | 3.50 |
| EPIC-06 | 3.00 |
| EPIC-07 | 5.50 |
| **Total** | **25.25** |

Total estimated effort (25.25 days) sits within the confirmed 24–28 day band (≈90–105% depending on the reading used), consistent with the user's "use full capacity" instruction without requiring scope trim or triggering a WARN outcome.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity / 5.7 Decision Record Integrity

**5.5 Cross-Stage Integrity:** All S2-01..S2-07 map to EPIC-01..EPIC-07 (1:1). All EPIC IDs in `stage4_backlog_slice.md` match this document's Execution Plan table. All RISK-01..RISK-07 appear in the Risk Register above with no orphaned references. Pass.

**5.7 Decision Record Integrity:** Skipped — `artifacts.escalations` not present this cycle (no escalations raised; 0 open, 0 deferred, 0 accepted-risk). Not applicable.

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```
