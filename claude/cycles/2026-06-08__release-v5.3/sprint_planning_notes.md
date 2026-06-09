**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-09
**Cycle:** 2026-06-08__release-v5.3

---

# Sprint Planning Notes — 2026-06-08__release-v5.3

## Backlog Slice Source

Original — `claude/cycles/2026-06-08__release-v5.3/stage4_backlog_slice.md`

No amendment sealed; `amended_backlog_slice_path` absent in `.claude_current_state.json`.

## Carry-Forward Items

Carry-forward items reviewed: **2 items** from cycle `2026-06-08__release-v5.2`.

| # | Item | Status |
|---|------|--------|
| CF-1 | LL-v5.2-P4-01 — qa_evidence_template.md signer format note for mixed-class EPICs | Incorporated as ST-11 (EPIC-03, P1) |
| CF-2 | LL-v5.2-P4-02 — execution_prompt.md STEP 5.3A SSR sub-step | Incorporated as ST-12 (EPIC-03, P1) |

Both carry-forward items are firm P1 stories in Sprint 2 EPIC-03. No carry-forward items require new sprint planning action.

## Design Gate Bypass Audit

Entered from `Release_Planning_Complete` (design gate skipped). Bypass audit per IMP-04 / IMP-30:
- `design_gate_bypass_authority`: "Head of UX & Design + Product Owner" ✅ (both roles present)
- `design_gate_bypass_reason`: present — all 22+3 items confirmed as governance/spec/security/QA/planning documents ✅
- Bypass audit: **PASS** — no new UI/UX items in scope

## Capacity WARN Acknowledgement

The release plan capacity check outcome is `warn` (total ~110 hrs across 2 sprints; 2-sprint phasing required; Sprint 2 at upper bound ~71 hrs). Product Owner must acknowledge before scope selection is finalised.

> **Product Owner acknowledgement required:** The v5.3 sprint plan requires 2-sprint phasing. Sprint 2 is at the upper bound (~71 hrs). If execution pace tightens in Sprint 2, ST-21 (BLG-FE-66, P3) and/or ST-17 (BLG-GOV-104, M, data-limited) are deferrable to v5.4 without sprint-goal impact. PO must explicitly acknowledge this WARN before the sprint can seal.

**Status:** ✅ Acknowledged by Product Owner, 2026-06-09

## Pre-Sprint Backlog Advisory

| Item | Status | Note |
|------|--------|------|
| BLG-GOV-106 — PT-04 trade count gate re-verification | ⚠️ OPEN — must resolve before seal | Provisional-Target: Before v5.3 sprint planning seals. DB query `SELECT COUNT(*) FROM trade_history WHERE pnl IS NOT NULL` required. Last known count: 6 trades (v4.6 audit, 2026-05-31). If ≥ 20: PT-04 enters scope via amendment cycle; capacity re-assessed. If < 20: update roadmap + BLG-FEAT-25 with current count. |

## Conditional Stories Gate Check

| Story | Gate | Decision |
|-------|------|----------|
| ST-23 — BLG-GOV-113 (SI-05 effectiveness review protocol) | Before 2026-07-01 | **INCLUDED** — Gate window open at planning date 2026-06-09 |
| ST-24 — BLG-GOV-114 (si05_digest_log schema validation) | Before 2026-07-01 | **INCLUDED** — Gate window open at planning date 2026-06-09 |
| ST-25 — BLG-FE-64 (RFJ visual design review pre-brief) | 2026-06-21 | **DEFERRED** — Gate date not yet reached (2026-06-09 < 2026-06-21) |

## Deferred Items

| Item | EPIC | Reason | Next Sprint Candidate? |
|------|------|--------|----------------------|
| ST-25 — BLG-FE-64 | EPIC-04 (conditional) | Gate: 2026-06-21 — not yet reached at planning time | Yes — via amendment cycle if gate clears during Sprint 2 |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-04 (BLG-SPEC-49) | ST-03 (BLG-QA-51) | Internal (EPIC-01) — QA AC template required first | Resolved by sequencing |
| ST-05 (BLG-SPEC-50) | ST-03 (BLG-QA-51) | Internal (EPIC-01) | Resolved by sequencing |
| ST-06 (BLG-SPEC-51) | ST-03 (BLG-QA-51) | Internal (EPIC-01) | Resolved by sequencing |
| ST-07 (BLG-SPEC-52) | ST-03 (BLG-QA-51) | Internal (EPIC-01) | Resolved by sequencing |
| ST-20 (BLG-QA-54) | EPIC-01 (ST-04–ST-07 merged to main) | Cross-sprint / Cross-EPIC — coverage matrix update requires contract docs to exist | Resolved by sprint sequencing — EPIC-01 Sprint 1; EPIC-04 Sprint 2 |

## Execution Sequence

### Sprint 1

**Execution order: EPIC-02 → EPIC-01**

1. **EPIC-02** (execution_state.json owner — merges first)
   - ST-08 — POST /digest/si05/send API key auth
   - ST-09 — SI-05 Telegram delivery failure alerting
   - ST-10 — CI secret scanning gate
   
2. **EPIC-01** (merges after EPIC-02 push to main)
   - ST-01 — BLG-SPEC-53 resolution plan (first — defines scope for ST-04–07)
   - ST-02 — BLG-SPEC-54 openapi.yaml audit (parallel with ST-01/ST-03)
   - ST-03 — BLG-QA-51 QA AC template (complete before ST-04–07)
   - ST-04 — BLG-SPEC-49 contract (after ST-03)
   - ST-05 — BLG-SPEC-50 contract (after ST-03)
   - ST-06 — BLG-SPEC-51 contract (after ST-03)
   - ST-07 — BLG-SPEC-52 contracts + test.py (after ST-03; updates SystemStatus.js + spec.js)

### Sprint 2

**Execution order: EPIC-03 → EPIC-04**

3. **EPIC-03** (execution_state.json owner — merges first in Sprint 2)
   - ST-11 — qa_evidence_template.md signer note (CF-1, P1 — early)
   - ST-12 — execution_prompt.md STEP 5.3A (CF-2, P1 — early)
   - ST-13 — SI-02 frontend activation criteria
   - ST-14 — AI model pin update policy
   - ST-15 — AI audit log retention policy
   - ST-16 — Arc 4 trade_plan data completeness audit
   - ST-17 — strategy_rules.md §11 parameter validation
   - ST-23 — SI-05 effectiveness review protocol
   - ST-24 — si05_digest_log schema validation
   
4. **EPIC-04** (merges after EPIC-03 is committed to main; ST-20 requires EPIC-01 contracts on main)
   - ST-18 — Tax year P&L boundary edge case validation
   - ST-19 — SI-05 digest Playwright E2E coverage
   - ST-20 — Playwright coverage matrix update (after EPIC-01 and EPIC-03 merged)
   - ST-21 — Red Flag Journal post-launch UX review (P3 — deferrable)
   - ST-22 — BLG-FE-64 visual design scope definition

## Multi-EPIC Execution Notes

**execution_state.json ownership (STEP 5.2 invariant):**

| Sprint | EPIC (Owner) | EPIC (Consumer) |
|--------|-------------|-----------------|
| Sprint 1 | EPIC-02 (creates execution_state.json) | EPIC-01 (reads and appends) |
| Sprint 2 | EPIC-03 (reads Sprint 1 state, appends Sprint 2 EPIC-03 section) | EPIC-04 (reads and appends) |

**Rule:** EPIC-01, EPIC-03, EPIC-04 must check for execution_state.json existence before creating. If found: read and append own EPIC section. Do not overwrite.

**Shared files across EPICs:**

| File | Modifying EPICs | Owner | Advisory |
|------|----------------|-------|---------|
| docs/reference/openapi.yaml | EPIC-01 (ST-02/04/05/06/07) | EPIC-01 | EPIC-04 must rebase onto main after EPIC-01 merges before finalising any openapi.yaml changes |
| backend/routers/test.py | EPIC-01 (ST-07) | EPIC-01 | EPIC-04 rebase advisory applies |
| src/pages/SystemStatus.js | EPIC-01 (ST-07) | EPIC-01 | EPIC-04 rebase advisory applies |
| tests/e2e/system-status.spec.js | EPIC-01 (ST-07) | EPIC-01 | EPIC-04 rebase advisory applies |
| claude/system/execution_prompt.md | EPIC-03 (ST-12) | EPIC-03 | Governance file — CLAUDE.md §6 compliance required (version bump + OPERATIONAL_GUIDE §14 + prompt_change_log.md entry) |
| claude/system/templates/qa_evidence_template.md | EPIC-03 (ST-11) | EPIC-03 | Governance file — CLAUDE.md §6 compliance required |
| claude/roadmap/current_roadmap.md | EPIC-03 (ST-13) | EPIC-03 | ST-13 updates SI-02 gate conditions |

## Risk Flags

| RISK-ID | Associated Item | Mitigation Status | Assessment |
|---------|----------------|------------------|------------|
| RISK-01 | EPIC-01 | Valid | ST-02 audit scoped to identify additional openapi.yaml gaps; ST-01 resolution plan scoped first; CLAUDE.md §2 compliance enforced at story level |
| RISK-02 | EPIC-03 (ST-17) | Valid | AC accepts "insufficient data" outcome for <20 trades; last known count 6 (v4.6); most likely insufficient — document as such |
| RISK-03 | EPIC-04 | Partially Resolved | PT-04 gate check (OA-RP-01) pending (see Outstanding Actions below); conditional stories ST-23/24 confirmed in scope |
| RISK-04 | EPIC-02 (ST-10) | Valid | Allowlist config step included in AC; false positive handling documented |

## Pre-Sprint Vulnerability Scan

**pip-audit scan (2026-06-09):** Clean — no known vulnerabilities found across all 60 dependencies.

## Planning-Deferred Item Traceability

Per AUD-2026-05-21-002 (STEP 5.2): Items in backlog slice NOT in sealed sprint backlog must be recorded in execution_state.json at initialisation with `status: deferred_at_planning`.

| Item | EPIC | Gate Condition |
|------|------|---------------|
| ST-25 (BLG-FE-64) | EPIC-04 (conditional) | BLG-FE-64 gate date 2026-06-21 not yet reached at planning time 2026-06-09; add via amendment cycle if gate clears |

## Outstanding Actions

| Action | Owner | Blocker? |
|--------|-------|---------|
| OA-RP-01: PT-04 trade count gate re-verification — 6 closed trades / 11 total (2026-06-09); gate NOT MET; current_roadmap.md + BLG-FEAT-25 updated | PMO Lead; Product Owner | ✅ Resolved |
| Capacity WARN acknowledgement — Sprint 2 upper bound accepted; ST-21/ST-17 deferrable to v5.4 if capacity tightens | Product Owner | ✅ Resolved |
| Sprint goal sign-off — confirmed by Product Owner 2026-06-09 | Product Owner | ✅ Resolved |
