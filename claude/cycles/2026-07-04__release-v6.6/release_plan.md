Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Published
Release: v6.6
Cycle: 2026-07-04__release-v6.6
Last Updated: 2026-07-04

---

# Release Plan — v6.6

## Readiness

**Prior cycle:** `2026-06-26__release-v6.3` (`.claude_current_state.json` `prior_cycle` field). Most recently closed release: `2026-07-02__release-v6.5` (Verified, Closed_with_actions, post_ship_complete=true).

**Roadmap status:** `current_roadmap.md` §3 (Now horizon) reports Arc 1/Arc 2 fully complete. Arc 3–6 remainder (PO-02/PO-04, SI-02/SI-04/SI-05 Phase 2, Arc 6) remain data-density-gated — no Now-horizon feature item is unblocked this cycle. v6.6 formally exists on the roadmap via the documented STEP 8.1 Option (b) deferral from `2026-07-03__scheduled` (see `run_manifest.md` §-1.2). Lifecycle audit AUD-2026-07-01 (17 findings) is now fully remediated as of v6.5 (v6.4 closed 7, v6.5 closed the remaining 10) — no audit remediation debt remains for v6.6 scope; `.claude_current_state.json` still shows `last_audit_open_items: 17` because the next formal `run audit` has not yet executed (due at cycle ≥52, gap≥3 trigger; current count 51).

**Readiness determination: READY.** Scope is drawn from (a) the Skill-Silo pull-forward mandate (per `2026-07-03__scheduled` rebalance: PO advised to commit ≥2 substantive U-items) and (b) small ungated QA/process debt items filed 2026-07-03. Full rationale at `run_manifest.md` STEP 0.

### 1.1 Backlog Age Advisory

No spec/documentation debt item was found flagged with an explicit multi-cycle non-assignment marker (searched for "consecutive cycles" / "cycles without" / carry-forward aging language in `backlog.md` — none matched). No advisory triggered this cycle.

### 1.2 Provisional-Target Advisory

0 items carry `Provisional-Target: v6.6` explicitly (searched `backlog.md` — no matches). All 4 scope candidates (BLG-FE-82, BLG-FE-40, BLG-QA-72, BLG-QA-73) carry `Provisional-Target: TBD` or `Unscheduled` — selected via the Skill-Silo pull-forward mandate and the 2026-07-03 technical-debt review session respectively, not via a pre-set horizon target.

### 1.3 Design-Gate Language Scan

**BLG-FE-82** contains explicit design-gate language: "Head of UX & Design sign-off" required as an acceptance criterion. Flagged — surfaces at the Pre-sprint Required Decisions checklist (STEP 7) and drives `design_gate_required = true` at STEP 4.1. **BLG-FE-40** lists Head of UX & Design as a co-owner but contains no explicit design-decision language beyond standard UX ownership; still classified as UI-facing (observable filter-state rendering) so also drives `design_gate_required = true` independently. BLG-QA-72/73 are backend/process items with no UI acceptance criteria.

### 1.4a Perennial-Return Check

No scope candidate has a documented multi-cycle `returned_to_backlog` / `deferred` history in the prior cycle's `stage4_backlog_slice.md`. All four items are entering release-planning scope for the first time (BLG-FE-82/BLG-QA-72/BLG-QA-73 filed 2026-07-02/03; BLG-FE-40 filed 2026-05-22 but has not previously appeared in a release backlog slice — it was gate-blocked, not returned). No perennial-return disposition required.

### 1.4b Within-Sprint Date Gate Classification

**BLG-FE-40** carries a calendar-based gate: "Red Flag Journal in active use for ≥30 days post-v3.9." v3.9 shipped 2026-05-22; today (2026-07-04) is 43 days later — the gate condition **already cleared before this cycle opened**, not within the planned sprint window. Per §1.4b this rule governs gates clearing *during* the sprint window; a gate that cleared prior to sprint start is not subject to the mandatory-conditional rule. Classified **firm**, subject to Product Owner's explicit gate-clearance confirmation (recorded below) rather than the mandatory-conditional restriction. No other scope candidate carries a calendar-date gate.

**Product Owner gate-clearance confirmation (BLG-FE-40):** 43 days of Red Flag Journal production use since v3.9 (2026-05-22) is confirmed via shipped-date arithmetic; no contrary evidence of non-use was found in this session. Recorded per the item's own AC: "Gate condition verified by Product Owner before sprint planning."

### 1.4 Gate-Condition Proximity Scan

| Item | Gate condition | Current trajectory | Projected clear date |
|------|-----------------|---------------------|------------------------|
| SI-02 (Behavioural Drift Detection) | ≥20 closed trades with linked trade_plans | Last officially logged trajectory estimate (`2026-07-03__scheduled` rebalance): ~15–17/20. **User separately reported 2026-07-03 that 20 closed trades have now been reached** — not yet formally re-verified via the production query; PMO Lead owns the re-check (see project SI-02 trade gate memory) | Pending PMO Lead re-verification — potentially already cleared, unconfirmed |
| PO-02 (Journal Pattern Recognition) | 6+ months of AI-summarised journal entries (BLG-FEAT-16 live and actively used) | trajectory unknown — journal entry generation rate not queried this session | data not available — Product Owner to surface at readiness review |
| PO-04 (Reflection ↔ Outcome Correlation) | 50+ trades with plans | trajectory unknown; long-horizon at current ~1–2 trades/month pace per prior rebalance estimates | ≈2026-Q4/2027 (indicative only) |

**Note on BLG-FEAT-52:** Named as a Skill-Silo pull-forward candidate by the `2026-07-03__scheduled` rebalance, but its own gate condition ("Arc 4 PO-02 sprint planning imminent") is **not met** — PO-02 remains blocked on the 6-months-AI-journal-entries gate above, which has no confirmed near-term clearance. BLG-FEAT-52 is therefore **excluded from firm v6.6 scope** (see Scope §, Items Explicitly Deferred) notwithstanding the rebalance's advisory naming. BLG-FE-82 is retained as the viable pull-forward candidate; BLG-FE-40 (gate-cleared, see §1.4b) is substituted as the second substantive U-item to meet the PO's "≥2 U-items" advisory.

**Do not halt.** Advisory only — recorded for Product Owner awareness; does not affect v6.6 firm scope beyond the BLG-FEAT-52 exclusion already reasoned above.

```yaml
# state.json update (STEP 1):
artifacts.stage1_readiness: pass
```

---

## Scope

No backlog items were newly filed this session for v6.6 scope — all 4 items (BLG-FE-82, BLG-FE-40, BLG-QA-72, BLG-QA-73) already existed in `backlog.md`. No scope change or reprioritisation was made to the global backlog beyond the release slice itself.

### Items in scope

| S2-ID | Backlog item | Description | Priority | Effort |
|-------|--------------|-------------|----------|--------|
| S2-01 | BLG-FE-82 | Colour contrast audit sweep (secondary/disclaimer text surfaces, app-wide) | P2 | S (~1 day) |
| S2-02 | BLG-FE-40 | Red Flag Journal filter state persistence (localStorage) | P3 | S (~0.5 day) |
| S2-03 | BLG-QA-72 | Audit colliding backlog IDs in `claude/backlog/backlog.md` | P2 | S (~0.5 day) |
| S2-04 | BLG-QA-73 | `database.py` / `_DB_STUB_FUNCTIONS` manual-sync risk — investigate automated derivation | P3 | M (~1–2 days) |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-52 (Trade tagging) | Named as a Skill-Silo pull-forward candidate by the `2026-07-03__scheduled` rebalance, but its own gate ("Arc 4 PO-02 sprint planning imminent") is not met — PO-02 remains blocked on the 6-months-AI-journal-entries data-density gate | Re-review each cycle until PO-02 sprint planning becomes imminent |
| SI-02 (Behavioural Drift Detection) | Data-density gate condition (1) trajectory ~15–17/20 per last official rebalance estimate; user-reported 20-trade count (2026-07-03) not yet formally re-verified by PMO Lead | Re-check at next release planning readiness scan once PMO Lead confirms via production query |
| PO-02/PO-04 (Arc 4 remainder) | Data-density gates not met | Re-check at next release planning readiness scan |
| BLG-FE-66/67/81/83 and remaining ungated backlog items | Not selected this cycle; scope was sized to the two named Skill-Silo U-item candidates (one substituted per gate reasoning above) plus the two 2026-07-03 technical-debt items with the clearest immediate justification, rather than exhausting full capacity | Available for v6.7 scoping |

```yaml
# state.json update (STEP 2):
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01, S2-02 | Base44 Frontend Prompt Owner / Head of UX & Design | RISK-01, RISK-04 | Design gate must pass before sprint planning seals (both stories are UI-facing) |
| EPIC-02 | S2-03, S2-04 | Director of Quality / QA & Testing Owner | RISK-02, RISK-03 | None — independent of EPIC-01 |

**EPIC-01 (UX & Accessibility Debt):** Contrast sweep (S2-01) and RFJ filter persistence (S2-02) both touch frontend-visible surfaces; both require Playwright coverage per CLAUDE.md's frontend-visible-change rule. No dependency between the two stories.

**EPIC-02 (QA & Test Infrastructure Debt):** Backlog ID collision audit (S2-03) is a documentation/process task with no code change. `database.py` stub-sync investigation (S2-04) may or may not result in an implementation change depending on feasibility findings (see BLG-QA-73 AC) — scoped as an investigation-with-conditional-implementation story.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Contrast/colour changes could introduce a new WCAG regression if reviewed only by code inspection | Medium | Head of UX & Design sign-off required as AC (already specified in BLG-FE-82); Playwright visual assertions for BLG-FE-40 | null |
| RISK-02 | EPIC-02 | Backlog ID renumbering (BLG-QA-72) could break existing cross-references in run manifests, cycle summaries, or the ideas register if not searched exhaustively | Medium | Grep all `claude/cycles/*/` and `claude/roadmap/` for any renumbered ID before finalising; document the resolution list per the item's own AC | null |
| RISK-03 | EPIC-02 | Automated `_DB_STUB_FUNCTIONS` derivation (BLG-QA-73), if adopted, could silently under- or over-stub and mask a real `ImportError` in CI rather than surfacing it | Low | AC requires a verifying CI run before merge; if infeasible, item resolves as a documented decision with no code change (zero regression risk) | null |
| RISK-04 | EPIC-01 | ST-01 (BLG-FE-82) and ST-02 (BLG-FE-40) are both UI-facing and have not yet cleared the design gate; sprint planning cannot seal without it | High | Run `run design-gate --cycle 2026-07-04__release-v6.6` immediately after this plan publishes, before invoking `plan sprint` | null |

```yaml
# state.json update (STEP 3):
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

Verified: all 4 backlog items referenced by S2-01 through S2-04 (BLG-FE-82, BLG-FE-40, BLG-QA-72, BLG-QA-73) exist exactly once each in `claude/backlog/backlog.md` (confirmed via direct grep — no collision, notably including BLG-QA-72 itself, the item auditing backlog ID collisions). Every S2-ID maps to exactly one EPIC-ID (EPIC-01: S2-01/S2-02; EPIC-02: S2-03/S2-04) and every EPIC declares its scope-item set consistently between the Scope and Execution Plan sections. Every RISK-ID (RISK-01/02/03/04) declared in the Execution Plan EPIC table appears as a row in the Risk Register Summary with `Relates to` pointing to a valid EPIC-ID. No orphaned references found. PASS.

```yaml
# state.json update (STEP 3.5):
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## STEP 4 — Backlog Slice (Committed)

`stage4_backlog_slice.md` written (4 stories, ST-01 through ST-04, across EPIC-01/EPIC-02, all Firm). Backlog lock `RP:v6.6:2026-07-04__release-v6.6` acquired, transaction `BLTX-20260704-01` prepared → committed, release-slice section written to `claude/backlog/backlog.md` with the required marker, lock released. `stage4_issue_manifest.json` written (4 entries, `--issues` defaults to `none` so no GitHub/import artefact generated at this stage — deferred to STEP 10).

### STEP 4.1 — Design Gate Classification

⚠ **DESIGN GATE REQUIRED before plan sprint — 2 items classified as UI-facing** (ST-01 BLG-FE-82, ST-02 BLG-FE-40 — both `delegated_frontend` with observable UI acceptance criteria: contrast rendering and filter-state rendering/persistence respectively). Run: `run design-gate --cycle 2026-07-04__release-v6.6`

```yaml
# state.json update (STEP 4 outcome):
artifacts.stage4_backlog_slice: pass
artifacts.stage4_issue_manifest: pass
attributes.backlog_committed: true
attributes.design_gate_required: true
status: Committed

# .claude_current_state.json:
design_gate_required: true
design_gate_status: "not_started"
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** No matching row in `scored_initiatives.md` for any of EPIC-01/02 (confirmed at STEP 0 — the file scores older roadmap-level initiatives and pre-2026-06-07 backlog IDs, not BLG-FE-82/BLG-FE-40/BLG-QA-72/BLG-QA-73). Per the three-tier resolution rule, this falls to tier 3: use STEP 4 inline estimates; no advisory required.

| EPIC | Stories | Estimated effort |
|------|---------|-------------------|
| EPIC-01 | ST-01, ST-02 | ~1 + 0.5 ≈ 1.5 days |
| EPIC-02 | ST-03, ST-04 | ~0.5 + 1.5 ≈ 2.0 days |
| **Total** | 4 stories | **≈ 3.5 days** |

**Assumptions:** `--timebox` and `--capacity` were not specified at invocation (both default to empty per `state.json.assumptions`). No explicit capacity figure exists to check against.

**Outcome:** ≈3.5 days of estimated work is materially lighter than every firm-scope sprint delivered since v5.0 (typically 5–15 days of story effort). All 4 stories are single-sprint, non-conflicting, and have no cross-EPIC dependency (see Execution Plan). No phasing is required.

```yaml
# state.json update (STEP 4.5):
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Roadmap Annotation

No formal `## v6.6` roadmap section exists (Option (b)-deferred release). Per §5 fallback rule, annotated the `**Next planned release:**` line in `current_roadmap.md` §1 instead. Lock `RA:v6.6:2026-07-04__release-v6.6` acquired, `roadmap_txn.json` prepared → committed, annotation written with marker, lock released.

```yaml
# state.json update (STEP 5):
artifacts.roadmap_txn: committed
locks.roadmap_lock.status: released
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity / 5.7 Decision Record Integrity

**5.5 Cross-Stage Integrity:** All 4 S2 IDs (S2-01 through S2-04) map to exactly one of EPIC-01/02; EPIC IDs in `stage4_backlog_slice.md` (EPIC-01, EPIC-02) match the Execution Plan's EPIC table exactly; all 4 RISK IDs (RISK-01, RISK-02, RISK-03, RISK-04) referenced in the EPIC table appear as rows in the Risk Register Summary; no orphaned references. No Stage 2/3/4 artefact has changed since the STEP 3.5 pass. PASS.

**5.7 Decision Record Integrity:** Skipped — `artifacts.escalations` is not `present` (no escalations were raised this cycle). `not_applicable`.

```yaml
# state.json update (STEP 5.5):
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```

---

## Publish Gate

All engine-specific conditions verified: `open_escalations` empty; `deferred_execution_blockers` empty; `stage4_5_capacity_check = pass`; `stage5_5_cross_stage_integrity = pass`; `stage5_7_decision_record_integrity = not_applicable`; `stage1_readiness`/`stage3_5_model_integrity = pass`; `plan_structured`/`plan_executable`/`backlog_committed = true`. Gate PASSES. `docs/product/scope/scope--2026-07-04__release-v6.6-ux-debt-clearance.md` and `docs/product/decisions/decisions--2026-07-04__release-v6.6.md` exist; both locks released. Completion conditions met.

```yaml
# state.json terminal update:
status: Validated → Published (on STEP 9 global sync)
publish_eligible: true
sealed.sealed_utc: 2026-07-04T08:40:00Z
```

---

**Design Gate:** REQUIRED — 2 UI-facing stories (ST-01, ST-02). Run `run design-gate --cycle 2026-07-04__release-v6.6` before invoking `plan sprint`.
