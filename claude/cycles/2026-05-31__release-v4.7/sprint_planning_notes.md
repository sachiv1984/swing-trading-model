**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-31
**Cycle:** 2026-05-31__release-v4.7

---

# Sprint Planning Notes — 2026-05-31__release-v4.7

---

## Backlog Slice Source

Original — `claude/cycles/2026-05-31__release-v4.7/stage4_backlog_slice.md` (no amendment active; `amended_backlog_slice_path` absent in .claude_current_state.json)

---

## Carry-Forward Items

Carry-forward items reviewed: 3 items from cycle `2026-05-30__release-v4.6` (lessons_learnt_closure.md §Carry-Forward).

| # | Observation | Implication | Engine | Actionable in v4.7? |
|---|-------------|-------------|--------|---------------------|
| 1 | SI-02 data density gate NOT MET for 6th time; trajectory clears ~Nov 2026 | Monitor at v4.8 release planning — if gate clears, advance ST-06/07/08 immediately | Release Planning | No — advisory only |
| 2 | SSR metric names error (Phase 4 catch): sprint close may not cross-reference spec when building SSR table | If recurs at v4.8, file sprint close prompt patch for STEP 5.3A | Sprint Execution / PMO Lead | No — monitor at v4.8 |
| 3 | AC-08 sign-off pattern: agent-mediated sign-off should be obtained before PR open, not at merge gate | If recurs at v4.8, update execution prompt STEP 5 | Sprint Execution / Director of Quality | No — monitor at v4.8 |

All 3 carry-forwards are advisory for v4.8. No action required in v4.7 sprint planning.

---

## Preflight Advisory Notes

**A — Design Gate Bypass Fields Empty:**
`design_gate_status = "not_required"` in .claude_current_state.json (set by release planning engine). `design_gate_bypass_authority` and `design_gate_bypass_reason` fields are empty. All sprint items were confirmed Design Not Applicable by the release planning engine (cycle_summary.md: `Design gate required: No`). Sprint items are either document-only assessments or an additive backend change to an existing endpoint (ST-03, no new UX). Standard mode: proceeding. PO sign-off at STEP 6.2 covers this advisory.

**B — Prompt Change Log Gaps (advisory — 4 gaps):**
The following Class 6 prompts have version numbers that exceed the last logged entry in `claude/system/prompt_change_log.md`. These are advisory only and do not block sprint planning or sealing.

| Prompt | Current Version | Last Logged | Gap |
|--------|----------------|-------------|-----|
| `execution_prompt.md` | v3.34 | v3.32→v3.33 | v3.34 not logged |
| `roadmap_prompt.md` | v6.7 | v6.5→v6.6 | v6.7 not logged |
| `post_ship_closure.md` | v2.12 | v2.10→v2.11 | v2.12 not logged |
| `release_planning_prompt.md` | v2.33 | v2.31→v2.32 | v2.33 not logged |

Action: Prepend missing rows to `claude/system/prompt_change_log.md` in the next governance commit per CLAUDE.md §6 and shared_standards.md §11.

**C — Pre-Sprint Vulnerability Scan:**
pip-audit run against `backend/requirements.txt` — No known vulnerabilities found. Clean. All 63 packages scanned; zero CVEs at any severity level.

**D — "Before Sprint Planning" Backlog Items:**
Scan for `Provisional-Target: Before v4.7 sprint planning` — no items found. Clear.

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-03 | GET /analytics/arc5-compliance available on staging | External (RISK-02) | Low risk — shipped v4.0, expected stable |
| ST-04 | RENDER_STAGING_DEPLOY_HOOK secret configured; Render dashboard access | External (RISK-03) | Infrastructure & Operations Owner to confirm before ST-04 |
| ST-05 | DS-07 migration on staging (from v4.6 ST-01) | External | Staging environment required |
| ST-06 | severity column migration on staging (from v4.6 ST-09) | External | Staging environment required |
| ST-02 | SI-01 + SI-03 live ≥30 days | Gate (deferred) | Gate clears 2026-06-21 |

All Sprint 1 firm items are independent of each other. No cross-story code dependencies exist within the firm scope. EPIC-03 stories share the staging environment requirement but are independently executable.

---

## Execution Sequence

### Sprint 1 (Firm)

Execution order reflects merge order:

1. **EPIC-03** — Staging Verifications & Ops Housekeeping (ST-04, ST-05, ST-06, ST-07)
   - Clears v4.6 OA items first (BLG-OPS-44, BLG-OPS-45)
   - All delegated_decision — can proceed in parallel with other EPICs
   - **execution_state.json owner** (first EPIC in merge order)

2. **EPIC-04** — Cost & UX Assessments (ST-08, ST-09)
   - Fully independent of all other EPICs
   - Both delegated_decision — assessment documents only

3. **EPIC-02** — User-Facing Analytics Enhancement (ST-03)
   - Autonomous implementation: backend response schema + frontend integration
   - Depends on GET /analytics/arc5-compliance being stable on staging (RISK-02 — low)

4. **EPIC-01** — Arc 5 Completion Pre-work (ST-01)
   - delegated_decision: §13 pre-assessment document
   - No code changes — executes independently

### Sprint 2 (Conditional — Gate: 2026-06-21)

5. **EPIC-01 ST-02** — SI-05 Phase 1 Implementation
   - Autonomous; blocked until gate met
   - Activation path: PO confirms gate → `amend cycle` → Sprint 2 planning seal

---

## Multi-EPIC Execution Notes

**Merge order:** EPIC-03 → EPIC-04 → EPIC-02 → EPIC-01

**execution_state.json owner:** EPIC-03 (first in merge order). All other EPIC branches must check for `execution_state.json` existence before creating their own — if found, read and append their EPIC's section rather than overwrite.

**Shared file ownership:**

| File | Owner EPIC | Note |
|------|-----------|------|
| `claude/backlog/backlog.md` | All EPICs (sequential) | Each EPIC marks its BLG items complete; merge order prevents conflicts |
| `docs/reference/openapi.yaml` | EPIC-02 only | EPIC-02 adds `compliance_summary` to monthly-pnl response schema; no other EPIC modifies openapi.yaml |

EPICs 01, 03, 04 make no changes to openapi.yaml. EPIC-02 branch must ensure openapi.yaml update is in the same commit as the implementation.

**Planning-deferred item traceability (AUD-2026-05-21-002):**
ST-02 (EPIC-01) is deferred_at_planning. Execution engine must initialise execution_state.json with:
```yaml
epics.EPIC-01.stories.ST-02:
  status: deferred_at_planning
  gate_condition: "SI-01 + SI-03 live ≥30 days — gate clears 2026-06-21"
```

---

## Risk Flags

| Risk ID | Associated Item | Description | Mitigation Status |
|---------|----------------|-------------|------------------|
| RISK-01 | EPIC-01 ST-02 | SI-05 Phase 1 gate (2026-06-21) may not be confirmed before Sprint 2 planning seals | Valid — ST-02 deferred_at_planning; PO confirms gate before Sprint 2 seals |
| RISK-02 | EPIC-02 ST-03 | GET /analytics/arc5-compliance unavailable on staging | Valid — shipped v4.0, expected stable; Infrastructure & Operations Owner to verify before ST-03 begins |
| RISK-03 | EPIC-03 ST-04 | Staging deploy verification requires Render infrastructure access and RENDER_STAGING_DEPLOY_HOOK secret | Valid — Infrastructure & Operations Owner must confirm Render dashboard access before ST-04 |

---

## Deferred Items

| Item | EPIC | Reason | Next Sprint Candidate? |
|------|------|--------|----------------------|
| ST-02 (SI-05 Phase 1) | EPIC-01 | Gate: SI-01 + SI-03 live ≥30 days — clears 2026-06-21 | Yes — Sprint 2 of this cycle (via amendment cycle if gate met before close) |

---

## Pre-Sprint Backlog Advisory

No items found with `Provisional-Target: Before v4.7 sprint planning` in `claude/backlog/backlog.md`.

---

## Delegation Classification Notes

**ST-03 (EPIC-02):** Classified `autonomous`. Backend additive change (new `compliance_summary` field in existing endpoint) + frontend data display in existing monthly P&L view. No new UX design required — existing data from a stable Arc 5 endpoint. Confirmed against BLG-GOV-72 fast-path: additive backend field with no new design decision → autonomous.

**ST-01 (EPIC-01):** Classified `delegated_decision` (Strategy Rules & System Intent Owner). §13 pre-assessment requires domain authority judgment. No HoST design session artefact needed — the §13 checklist protocol is the governing artefact. Advisory: no design artefact gap.

**ST-04, ST-05, ST-06, ST-07 (EPIC-03):** All `delegated_decision` (Infrastructure & Operations Owner; Data Model & Domain Schema Owner for ST-05/06). Staging environment access required; operational verification tasks not executable by autonomous engine.

**ST-08 (EPIC-04):** `delegated_decision` (FinOps & Resource Architect). Cost analysis and pricing tier decision requires FinOps role judgment.

**ST-09 (EPIC-04):** `delegated_decision` (Head of UX & Design). UX assessment requires design domain authority. Assessment-only — no implementation. Advisory: no design artefact required (this IS the design artefact).

---

## Pre-Sprint Vulnerability Scan

pre-sprint pip-audit: clean — no known vulnerabilities found (63 packages scanned, 2026-05-31).

---

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Prepend 4 missing prompt_change_log.md rows (exec v3.34, roadmap v6.7, post_ship v2.12, release_planning v2.33) | Head of Specs Team | No — advisory only |
| Confirm RENDER_STAGING_DEPLOY_HOOK secret exists before ST-04 execution | Infrastructure & Operations Owner | No — before ST-04 execution |
| Confirm GET /analytics/arc5-compliance available on staging before ST-03 execution | Head of Backend Engineering | No — before ST-03 execution |
| PO to confirm SI-01 + SI-03 gate by 2026-06-21 before Sprint 2 seals | Product Owner | No — before Sprint 2 if applicable |
