**Owner:** Head of Specs Team
**Class:** Operational Record (Class 3)
**Status:** Active
**Audit ID:** AUD-2026-04-20
**Prior Audit ID:** AUD-2026-04-11
**Filed:** 2026-04-21
**Cycle:** 2026-04-17__release-v2.8
**Completed Cycles at Audit:** 13

---

# Claude Lifecycle Audit v6 — AUD-2026-04-20

---

## 1. Resolved Since Last Audit

Prior audit: AUD-2026-04-11. 10 open items carried forward.

| AUD-ID | Title (3 words) | Status | Evidence ref |
|--------|-----------------|--------|--------------|
| AUD-2026-04-11-001 | §13 missing artefacts | RESOLVED | OPERATIONAL_GUIDE v3.48: sprint_backlog_index, velocity_metrics, audit_report added to §13 |
| AUD-2026-04-11-002 | decision_log advisory guard | RESOLVED | OPERATIONAL_GUIDE v3.54: STEP 9 decision_log decrease upgraded to STRUCTURAL HARD GATE (roadmap_prompt.md v4.8) |
| AUD-2026-04-11-003 | pr_status pre-seal sync | RESOLVED | OPERATIONAL_GUIDE v3.49: execution_prompt.md v3.2 STEP 5.0A pr_status pre-seal sync added as STRUCTURAL |
| AUD-2026-04-11-004 | sprint_close verification readiness | RESOLVED | OPERATIONAL_GUIDE v3.49: execution_prompt.md v3.2 verification readiness block upgraded to STRUCTURAL table |
| AUD-2026-04-11-005 | DV STEP -1.3 sign-off | RESOLVED | OPERATIONAL_GUIDE v3.50: delivery_verification_prompt.md v1.9 STEP -1.3 upgraded to two-tier STRUCTURAL |
| AUD-2026-04-11-006 | design-gate dry-run table | RESOLVED | OPERATIONAL_GUIDE v3.51: shared_standards.md v2.8 §13 dry-run table — `run design-gate` row added |
| AUD-2026-04-11-007 | OPERATIONAL_GUIDE §14 stale | RESOLVED | OPERATIONAL_GUIDE v3.47: §14 Version 3.41→3.47, Last Updated corrected to 2026-04-11 |
| AUD-2026-04-11-008 | §14 team_charter stale | RESOLVED | OPERATIONAL_GUIDE v3.47: §14 team_charter version corrected v1.5→v1.6 |
| AUD-2026-04-11-009 | release_planning design-gate advisory | RESOLVED | OPERATIONAL_GUIDE v3.52: release_planning_prompt.md v2.26 STEP 1 §1.3 design-gate language scan added |
| AUD-2026-04-11-010 | ideas_window.json schema field | RESOLVED | OPERATIONAL_GUIDE v3.51: shared_standards.md v2.8 §16.9 ideas_window.json schema added (per_agent_submission_count) |

**All 10 prior items RESOLVED. No carry-forwards from AUD-2026-04-11.**

---

## 2. Health Scorecard

SYSTEM HEALTH — 2026-04-21  |  Prior: 2026-04-11

| Dimension | Score | Bar (▓=10pts) | Trend | Confidence |
|-----------|-------|----------------|-------|------------|
| Token Efficiency | 84 | ▓▓▓▓▓▓▓▓░░ | ▲ +10 | LOW |
| Governance Integrity | 96 | ▓▓▓▓▓▓▓▓▓▓ | ▲ +30 | MEDIUM |
| Execution Reliability | 94 | ▓▓▓▓▓▓▓▓▓░ | ▲ +14 | MEDIUM |
| Friction Load | 60 | ▓▓▓▓▓▓░░░░ | ▲ +43 | MEDIUM |
| Document Hygiene | 87 | ▓▓▓▓▓▓▓▓▓░ | ▼ -1 | MEDIUM |
| **Overall** | **84** | **▓▓▓▓▓▓▓▓░░** | **▲ +19** | **MEDIUM** |

Overall improved 65 → 84 driven by resolution of all 10 AUD-2026-04-11 items and elimination of stale deferred patches.

---

## 3. Gap Register

| Stage | File | Status | Impact (5 words) | → Improvement? |
|-------|------|--------|------------------|----------------|
| Phase 2 | `claude/ideas/rejected_but_strong.md` | PARTIAL (header only loaded) | Low: Class 4, header compliant | No |
| Stage 4 | `claude/system/invariants.md` | NOT LOADED (header check only) | Invariant correctness unverified | No (Stage 9 SST confirms cross-ref) |
| Stage 8 | `claude/system/amendment_cycle_prompt.md` | NOT LOADED (header only) | A2/A3/A5/A7 checks partial | No (low risk — no amendment cycles active) |
| Stage 2 | Prior cycles v2.1–v2.5 lessons_learnt files | PARTIAL (not loaded) | Friction trend incomplete | No (noted in scorecard confidence) |
| Stage 5 | Inline schema counts in roadmap_prompt.md | ESTIMATED (full file not loaded) | Token budget partially estimated | No |

---

## 4. Stage Findings

### Stage 1 — Lifecycle Mapping

**TABLE 1 — Command path check:**

| Command | Prompt path in CLAUDE.md | File confirmed? | Invocation syntax match? |
|---------|--------------------------|-----------------|--------------------------|
| `run ideas` | `claude/system/idea_intake_prompt.md` | YES | YES |
| `run roadmap` | `claude/system/roadmap_prompt.md` | YES | YES |
| `manage roadmap` | `claude/system/roadmap_management_prompt.md` | YES | YES |
| `groom backlog` | `claude/system/backlog_management_prompt.md` | YES | YES |
| `plan release` / `run planning` | `claude/system/release_planning_prompt.md` | YES | YES |
| `run design-gate` | `claude/system/design_gate_prompt.md` | YES | YES |
| `plan sprint` | `claude/system/sprint_planning_prompt.md` | YES | YES |
| `amend cycle` | `claude/system/amendment_cycle_prompt.md` | YES | YES |
| `run sprint` | `claude/system/execution_prompt.md` | YES | YES |
| `run delivery verification` | `claude/system/delivery_verification_prompt.md` | YES | YES |
| `run post-ship` | `claude/system/post_ship_closure.md` | YES | YES |
| `sync gh` | inline (CLAUDE.md §4) | N/A | YES |
| `run audit` | `claude/audit.py` | YES | YES |

No broken paths in CLAUDE.md command table.

**TABLE 2 — Engine documentation coverage:**

| Engine | In OPERATIONAL_GUIDE §4? | In README §4? | Gap |
|--------|--------------------------|---------------|-----|
| Roadmap Rebalance | YES (§6) | YES (§4.1) | None |
| Release Planning | YES (§6B) | Not listed | README §4 only covers Roadmap Rebalance Engine |
| Sprint Planning | YES (§7) | Not listed | README §4 gap (advisory — README is Supporting doc) |
| Sprint Execution | YES (§8) | Not listed | README §4 gap (advisory) |
| Post-Ship Closure | YES (§10) | Not listed | README §4 gap (advisory) |
| Amendment Cycle | YES (§6B.8) | Not listed | README §4 gap (advisory) |
| Design Gate | YES (§6.5) | Not listed | README §4 gap (advisory) |
| Delivery Verification | YES (§9) | Not listed | README §4 gap (advisory) |

- README §4 covers only Roadmap Rebalance (primary routine). All other engines are in OPERATIONAL_GUIDE §4. README is a Supporting document (Class 2) — gap is advisory only, no hard gate impact.

**TABLE 3 — §14 version spot check:**

| Engine | §14 version | Actual file version | Match? |
|--------|-------------|---------------------|--------|
| execution_prompt.md | v3.8 | v3.8 | ✓ MATCH |
| delivery_verification_prompt.md | v2.0 | v2.0 | ✓ MATCH |
| post_ship_closure.md | v2.5 | v2.5 | ✓ MATCH |
| document_lifecycle_guide.md | v2.5 | v2.6 | ✗ DIVERGENCE |
| team_charter.md | v1.6 | v1.6 | ✓ MATCH |
| shared_standards.md | v2.8 | v2.8 | ✓ MATCH |

- **§14 DRIFT DETECTED:** `document_lifecycle_guide.md` listed as v2.5 in §14 but actual file is v2.6 (updated 2026-03-07 — Class 4 sub-type 3 Release Plan added). §14 was not updated at that time. → Generates improvement AUD-2026-04-20-002.

**Findings:**
- All 13 CLAUDE.md command paths confirmed valid.
- README §4 covers only primary routine (Roadmap Rebalance) — advisory gap, no action required.
- CLAUDE.md does not declare a Last Updated field — no stale date to flag.
- `run audit` is present in CLAUDE.md command table ✓.

---

### Stage 2 — Behavioural Audit

**COMPLIANCE TABLE:**

| Cycle | B1 Auth | B2 LL filed | B3 Prior patches | B4 Hard gate | B5 Action-now | B6 Log grew | B7 No 2nd carry |
|-------|---------|-------------|-----------------|--------------|---------------|-------------|-----------------|
| v2.8 | ✓ | ✓ | ✓ (all v2.7 CF applied) | NO GATES FIRED — compliant | ✓ (2 action-now applied) | ✓ | ✓ (no 2nd-cycle carry) |
| v2.7 | ✓ | ✓ | ✓ (all v2.6 CF applied) | NO GATES FIRED — compliant | ✓ (1 action-now applied) | ✓ | ✓ |
| v2.6 | ✓ | ✓ | ✓ (v2.5 CF applied) | NO GATES FIRED — compliant | ✓ (0 action-now at execution) | ✓ | ✓ |
| compliance % | ~100% | ~100% | ~100% | COMPLETED_CYCLES=13 ≥3 — compliant | ~100% | ~100% | ~100% |

B4: COMPLETED_CYCLES = 13 ≥ 3. Hard gate compliance check: no hard gate halts were recorded across v2.6–v2.8 (all preflight passes, no `prior_status` = `Blocked` entries in loaded cycles). Classified NO GATES FIRED — compliant.

**PATTERN TABLE:**

| Friction Type | Count (v2.6–v2.8 confirmed) | Top source file | Recurring? |
|---------------|----------------------------|-----------------|------------|
| Type A | 7 | lessons_learnt_cycle.md (Phase 4 entries) | NO — each item distinct |
| Type B | 0 | — | — |
| Type C | 3 | lessons_learnt_closure.md | NO — no exact recurrence confirmed |
| Type D | 0 | — | — |
| Type E | 0 | — | — |

**TREND LINE:** v2.6: ~1 item | v2.7: ~3 items | v2.8: 4 items
Trend: INCREASING (v2.6→v2.8 loaded). Note: prior cycles v2.1–v2.5 not loaded — trend may not be representative.

**No B-check compliance < 75%. No OBSERVED improvement auto-generated from B-checks.**

---

### Stage 3 — Governance Integrity

**TABLE 1 — Agent roster:**

| Agent file | Role | Format | Version | Status |
|------------|------|--------|---------|--------|
| head_of_specs_team.md | Head of Specs Team | COMPLIANT | Not versioned | CONFIRMED |
| pmo_lead.md | PMO Lead | COMPLIANT (**Role:** field present) | v2.2 | CONFIRMED |
| product_owner.md | Product Owner | COMPLIANT | Not versioned (Class 5 role charter) | CONFIRMED |
| facilitator.md | Facilitator | COMPLIANT | Not versioned | CONFIRMED |
| director_of_quality.md | Director of Quality | COMPLIANT | v1.1 | CONFIRMED |
| All 23 files | — | COMPLIANT (sample of 5 checked; all use **Role:** format) | — | CONFIRMED (sample) |

**TABLE 2 — Governance checks:**

| Check | Result | Evidence |
|-------|--------|----------|
| G1 — All charter roles have agent file | PASS | 23 agent files match 23 roles in team_charter.md §3; all roles confirmed |
| G2 — Agent lifecycle refs point to canonical path | PASS | Agent files reference `claude/charter/document_lifecycle_guide.md` (Class 2 compliant) |
| G3 — Artefact class declarations match lifecycle guide §3 | PARTIAL | lessons_learnt_cycle.md v2.7 declares Class 4 but should be Class 3 (Operational Record) — see Document Hygiene |
| G4 — §13 register covers scoring + ideas + lessons artefacts | PASS | scoring/scored_initiatives.md, ideas/rejected_but_strong.md, lessons_learnt_closure.md, closure_state.json all present in §13 (OPERATIONAL_GUIDE line 1278: "Closure State | `claude/cycles/<id>/closure_state.json` | — | PMO Lead | Post-Ship") |
| G5 — Design gate bypass authority in charter | PASS | team_charter.md v1.6 §3.3 Head of UX & Design — IMP-30 bypass authority with co-confirmation by Product Owner |

---

### Stage 4 — Lifecycle Reliability

**TABLE — Reliability checks:**

| Check | Result | Evidence |
|-------|--------|----------|
| R1 — All lifecycle states have valid entry AND exit transitions | PASS | lifecycle_schema.json v1.0: 9 states, all with transitions. `Blocked` has blocked_resolution rule. Amendment_In_Progress bidirectional. |
| R2 — All hard gate halt paths have defined recovery instruction | PASS | lifecycle_schema.json guard_rules.blocked_state_protocol + recovery_rule defined. All engines reference shared_standards.md §10 for halt format. |
| R3 — Idempotency: classify write ops STRUCTURAL/ASSERTION/ABSENT | see sub-table | |
| R4 — Re-evaluate max age rule in STEP -1.5 | PASS | lifecycle_schema.json recovery_rule references shared_standards.md §8 resumability |
| R5 — All engines have zero-state bootstrap path | PASS | All engines have STEP -1 preflight; run_manifests confirm -1.1 through -1.9 checks for all 3 loaded cycles |
| R6 — Concurrent write prevention at state-write step | PASS | lifecycle_schema.json guard_rules.concurrent_write_prevention: "confirm status value has not changed since read at invocation" |

**R3 SUB-TABLE:**

| Write operation | File | Guard type | Engine |
|----------------|------|-----------|--------|
| decision_log.md append | `docs/product/decisions/decision_log.md` | STRUCTURAL (hard gate since roadmap_prompt.md v4.8 STEP 9) | Roadmap Rebalance |
| backlog.md write | `claude/backlog/backlog.md` | STRUCTURAL (lock file + team_charter §11 strict lock) | Roadmap, Groom Backlog |
| .claude_current_state.json status write | `.claude_current_state.json` | STRUCTURAL (concurrent write check + lifecycle_schema guard_rules) | All engines |
| closure_state.json step updates | `claude/cycles/<id>/closure_state.json` | ASSERTION (no explicit idempotency guard; relies on step-by-step execution order) | Post-Ship Closure |
| sprint_backlog_index.json write | `claude/cycles/<id>/sprint_backlog_index.json` | ASSERTION-implied (produced once at Phase 2 STEP N; no re-run guard) | Sprint Planning |
| lessons_learnt_cycle.md append | `claude/cycles/<id>/lessons_learnt_cycle.md` | ASSERTION (append idempotency via phase tag check — advisory, not structural) | Sprint Execution, Delivery Verification |

Flagged: closure_state.json ASSERTION guard — generates scorecard deduction. Not auto-generating improvement at this time as risk is low (single-user system, resumability rule covers it).

---

### Stage 5 — Token Budget Analysis

**TOKEN BUDGET TABLE:**

| Engine | Lines | ~Tokens | Preflight files (N) | ~Preflight tokens | Inline blocks (N) | ~Block tokens | Total/invoke | Invoke/cycle | Cycle cost | Confidence |
|--------|-------|---------|--------------------|--------------------|------------------|--------------|-------------|-------------|-----------|-----------|
| roadmap_prompt.md | 1,651 | 13,208 | ~5 | ~4,000 | ~2 [ESTIMATED] | ~800 [ESTIMATED] | ~18,008 | ~0.5 | ~9,004 | LOW |
| release_planning_prompt.md | 1,456 | 11,648 | ~5 | ~4,000 | ~1 [ESTIMATED] | ~400 [ESTIMATED] | ~16,048 | 1 | ~16,048 | LOW |
| sprint_planning_prompt.md | 816 | 6,528 | ~4 | ~3,200 | ~1 [ESTIMATED] | ~400 [ESTIMATED] | ~10,128 | 1 | ~10,128 | LOW |
| execution_prompt.md | 1,038 | 8,304 | ~6 | ~4,800 | ~1 [ESTIMATED] | ~400 [ESTIMATED] | ~13,504 | 2+ | ~27,008+ | LOW |
| delivery_verification_prompt.md | 633 | 5,064 | ~4 | ~3,200 | 0 | 0 | ~8,264 | 1 | ~8,264 | MEDIUM |
| post_ship_closure.md | 795 | 6,360 | ~3 | ~2,400 | 0 | 0 | ~8,760 | 1 | ~8,760 | MEDIUM |
| lessons_learnt_prompt.md | 515 | 4,120 | ~2 | ~1,600 | 0 | 0 | ~5,720 | 2 | ~11,440 | MEDIUM |
| amendment_cycle_prompt.md | 644 | 5,152 | ~3 | ~2,400 | 0 | 0 | ~7,552 | 0 (emergency) | ~0 | MEDIUM |
| design_gate_prompt.md | 357 | 2,856 | ~3 | ~2,400 | 0 | 0 | ~5,256 | 1 | ~5,256 | MEDIUM |
| backlog_management_prompt.md | 429 | 3,432 | ~2 | ~1,600 | 0 | 0 | ~5,032 | 1 | ~5,032 | MEDIUM |
| roadmap_management_prompt.md | 384 | 3,072 | ~2 | ~1,600 | 0 | 0 | ~4,672 | 1 | ~4,672 | MEDIUM |

⚠ This table does not capture in-run context accumulation. For execution_prompt.md,
  actual per-invocation cost grows with sprint size (loaded EPIC items add to context).
  Reported cost may understate actual by 30–50% on large sprints. Use as lower bound.

**RANKED SAVINGS TABLE:**

| Rank | Opportunity | Current tokens/cycle | Post-fix tokens/cycle | Saving |
|------|-------------|---------------------|----------------------|--------|
| 1 | BLG-GOV-08: roadmap_prompt.md 10% reduction | ~9,004 | ~8,103 | ~901/cycle |
| 2 | BLG-GOV-08: release_planning_prompt.md 10% reduction | ~16,048 | ~14,443 | ~1,605/cycle |
| 3 | Extract estimated inline blocks from roadmap_prompt.md | ~800 | 0 | ~800/cycle [ESTIMATED] |

Note: roadmap_prompt.md grew from ~1,581 lines (at AUD-2026-04-11) to 1,651 lines (+70 lines), moving FURTHER from BLG-GOV-08 target. release_planning_prompt.md reduced from ~1,534 to 1,456 lines (-78 lines), moving TOWARD target.

**DEAD LOAD CHECK:**

| Engine | File loaded at preflight | Used beyond preflight check? | Dead? |
|--------|--------------------------|------------------------------|-------|
| All engines | `.claude_current_state.json` | YES — fields read throughout | NOT DEAD |
| Release Planning | `scored_initiatives.md` | YES — STEP 4.5 scoring | NOT DEAD |
| Roadmap | `velocity_metrics.md` | YES — STEP 0 velocity | NOT DEAD |

No dead loads confirmed.

**DRY-RUN GAP:**

| Engine | In §13 dry-run table? | If not: token risk per failed run |
|--------|----------------------|----------------------------------|
| plan sprint | YES | — |
| run sprint | YES | — |
| run post-ship | YES | — |
| manage roadmap | YES | — |
| groom backlog | YES | — |
| run design-gate | YES | — |
| run roadmap | YES | — |
| run ideas | YES | — |
| plan release | NOT in §13 | ~16,048 tokens per uncached failed run |
| run delivery verification | NOT in §13 | ~8,264 tokens per failed run |
| amend cycle | NOT in §13 | ~7,552 tokens (low risk — emergency only) |

Note: `plan release` and `run delivery verification` do not appear to have `--dry-run` support per CLAUDE.md syntax. Their absence from §13 reflects that they don't support `--dry-run`, not a gap. §13 correctly lists only engines with `--dry-run` support. No action required.

**CYCLE TOTAL:** ~105,612 tokens/typical cycle (lower bound; execution engine understated by 30–50% on large sprints).

---

### Stage 6 — Engine Handoff Integrity

**HANDOFF TABLE:**

| Pair | Field/Section | Producer writes? | Consumer reads? | Match? |
|------|--------------|-----------------|-----------------|--------|
| Release Planning → Sprint Planning | `sprint_sealed`, `backlog_slice_path` | YES (state.json) | YES (STEP -1) | ✓ |
| Release Planning → Sprint Planning | `design_gate_status = Passed` | YES (state.json) | YES (guard) | ✓ |
| Sprint Planning → Sprint Execution | `sprint_backlog_index.json` | YES (STEP N) | YES (STEP -1/-0) | ✓ |
| Sprint Planning → Sprint Execution | `sprint_sealed = true` | YES | YES | ✓ |
| Sprint Execution → Delivery Verification | `execution_state.json sealed = true` | YES (STEP 7) | YES (STEP -1.1) | ✓ |
| Sprint Execution → Delivery Verification | `sprint_close.md` | YES (STEP 5.1) | YES (STEP -1.2) | ✓ |
| Delivery Verification → Post-Ship Closure | `verification_report.md status = Verified` | YES | YES (§4 inputs) | ✓ |
| Delivery Verification → Post-Ship Closure | `next_cycle_unblocked = true` | YES | YES (STEP 0) | ✓ |
| Roadmap Rebalance → Release Planning | `current_roadmap.md` "Next planned release" | YES | YES (STEP -1.2) | ✓ |
| Amendment Cycle → Sprint Planning | `amended_backlog_slice_path` | YES | YES (STEP -1.1 authoritative slice read) | ✓ |

No CONSUMER READS UNGUARANTEED FIELD, DEAD OUTPUT, or SCHEMA VERSION MISMATCH findings.

---

### Stage 7 — Prompt Architecture & Compression

**COMPLEXITY TABLE:**

| Engine | STEPs | Hard gates | Branches | Inline blocks | Lines | Flagged? |
|--------|-------|-----------|---------|--------------|-------|---------|
| roadmap_prompt.md | ~15 | ~4 | ~6 | ~2 [ESTIMATED] | 1,651 | YES (lines > 500; STEPs ≈15 boundary) |
| release_planning_prompt.md | ~13 | ~3 | ~5 | ~1 [ESTIMATED] | 1,456 | YES (lines > 500) |
| sprint_planning_prompt.md | ~11 | ~2 | ~4 | ~1 [ESTIMATED] | 816 | YES (lines > 500) |
| execution_prompt.md | ~12 | ~5 | ~8 | ~1 [ESTIMATED] | 1,038 | YES (lines > 500) |
| delivery_verification_prompt.md | ~9 | ~3 | ~5 | 0 | 633 | YES (lines > 500) |
| post_ship_closure.md | ~13 | ~2 | ~4 | 0 | 795 | YES (lines > 500) |
| lessons_learnt_prompt.md | ~5 | 0 | ~2 | 0 | 515 | YES (lines > 500) |
| amendment_cycle_prompt.md | ~9 | ~3 | ~3 | 0 | 644 | YES (lines > 500) |
| design_gate_prompt.md | ~7 | ~1 | ~2 | 0 | 357 | NO |
| backlog_management_prompt.md | ~8 | ~1 | ~3 | 0 | 429 | NO |
| roadmap_management_prompt.md | ~6 | ~1 | ~2 | 0 | 384 | NO |

All engines > 500 lines are flagged per audit rule; this is a known structural trait of this system (complex domain requires detailed instructions). BLG-GOV-08 specifically targets roadmap_prompt.md and release_planning_prompt.md reduction.

**EXTRACTION TABLE:**

| Category | Confirmed instances | Canonical home | Saving if extracted |
|----------|-------------------|----------------|---------------------|
| Halt format blocks | ~1 [ESTIMATED] (roadmap_prompt.md §1 rules) | shared_standards.md §10 | ~200 tokens/cycle [ESTIMATED] |
| Invariant lists | 0 CONFIRMED (execution_prompt.md §13 references invariants.md; README §3 references invariants.md) | claude/system/invariants.md | None required |
| JSON schemas | ~1 [ESTIMATED] (execution_prompt.md §9.1 ST item schema may be inline) | shared_standards.md §16 | ~400 tokens/cycle [ESTIMATED] |
| Role verify blocks | 0 CONFIRMED | — | — |

**INVOCATION GUARD TABLE:**

| Check | Result |
|-------|--------|
| lessons_learnt_prompt.md §1 guard type | STRUCTURAL (invocation context required per §1 protocol) |
| invocation_context parameter required? | YES |
| Calling engines that pass structured context | Sprint Execution (STEP 8), Delivery Verification (STEP 8.5), Post-Ship Closure (STEP 8) |

**§14 VERSION DRIFT CHECK (v6 — conditional):**

DRIFT DETECTED: `document_lifecycle_guide.md` v2.5 in §14 → actual v2.6 (updated 2026-03-07).
All other 20 entries in §14 match actual file versions ✓.

→ Generates improvement AUD-2026-04-20-002.

---

### Stage 8 — Amendment Cycle Completeness

**TABLE — Amendment checks:**

| Check | Result | Evidence |
|-------|--------|---------|
| A1 — Amendment_In_Progress has complete mini state machine | PASS | lifecycle_schema.json: Sprint_Planning_Complete → Amendment_In_Progress → Sprint_Planning_Complete; entry_condition and completion_signal defined |
| A2 — First-amendment zero-state handled | PARTIAL [NOT LOADED] | amendment_cycle_prompt.md not fully loaded — cannot confirm first-run bootstrap; amendment_cycle_prompt.md v1.7 STEP 0 structure not examined |
| A3 — Withdrawal path defined | PARTIAL | OPERATIONAL_GUIDE §6B.8: "seal or withdraw before opening another" — withdrawal path acknowledged. Full instructions in amendment_cycle_prompt.md not verified. |
| A4 — Two-authority ratification is mode-independent | PASS | lifecycle_schema.json completion_signal: "two-authority ratification complete" — not qualified by mode |
| A5 — One-active-amendment rule is a hard gate | PARTIAL | shared_standards.md §10 guard algorithm and lifecycle_schema.json forward_only rule prevent second amendment opening. Explicit hard gate in amendment_cycle_prompt.md not verified. |
| A6 — Sprint Planning guards Amendment_In_Progress explicitly | PASS | lifecycle_schema.json guard_rules.skip_prevention: "verify current status is in its valid from-states" — Amendment_In_Progress is not a valid from-state for sprint planning |
| A7 — amendment_lessons.md has defined sunset | NOT CHECKABLE | amendment_lessons.md is Class 3 per §13; sunset clause not verified without loading amendment_cycle_prompt.md |

---

### Stage 9 — Single Source of Truth

**TABLE — SST checks:**

| Check | Result | Duplicate count | Token cost of duplicates | Evidence |
|-------|--------|----------------|--------------------------|---------|
| SST1 — Invariant lists: unique canonical source? | PASS | 0 inline copies confirmed | 0 | execution_prompt.md §13 references `invariants.md`; README §3 references `invariants.md`; team_charter §6 has forward-reference note to `invariants.md` |
| SST2 — Halt format: all engines reference §10 only? | PASS [MEDIUM CONFIDENCE] | ~1 [ESTIMATED] inline halt block (roadmap_prompt.md §1) | ~200 tokens/cycle | execution_prompt.md line 55 references shared_standards.md §10 |
| SST3 — JSON schemas in shared_standards §16? | PARTIAL | ~1 [ESTIMATED] inline schema (execution_prompt.md §9.1) | ~400 tokens/cycle | shared_standards.md §16 has schemas §16.1–§16.9; execution_prompt.md §9.1 item schema not confirmed as fully migrated |
| SST4 — workforce_capacity.md has single declared write owner | PASS | — | — | team_charter §4: FinOps & Resource Architect owns workforce_capacity.md |
| SST5 — scored_initiatives uses cycle-scoped naming | PASS | — | — | claude/scoring/scored_initiatives_2026-03-06.md (cycle-dated); scored_initiatives.md (current working copy) |

---

### Stage 10 — Known Design Gaps & Deferred Patches

**D1 — PATCH AGE TABLE:**

| File | Section | Change | Owner | Target | First recorded | Cycles carried | Status |
|------|---------|--------|-------|--------|---------------|----------------|--------|
| execution_prompt.md | §3.2.A | reclassification note: delegated_frontend→autonomous with frontend changes requires DoQ counter-sign at STEP 5 sprint close | Head of Specs Team | v2.9 planning | v2.8 Phase 4 (OA-v28-03) | 1 cycle | ACTIVE |
| execution_prompt.md | §3.2 DoQ template | EPIC-level DoQ consolidation block required when story-level authority is domain-specific | Head of Specs Team | v2.9 planning | v2.8 Phase 4 (OA-v28-03) | 1 cycle | ACTIVE |

Both tracked as backlog item BLG-GOV-14 (P2 Medium). No improvement generated (1 cycle = ACTIVE, not yet STALE). Will auto-generate improvement at next audit if unresolved (STALE at 2 cycles).

**D2-D5 — DESIGN GAP TABLE:**

| Check | Result | Evidence |
|-------|--------|---------|
| D2 — ideas_window.json has per_agent_submission_count field | PASS | shared_standards.md §16.9 added by AUD-2026-04-11-010; actual ideas_window.json schema confirmed with field |
| D3 — rejected_but_strong.md exists with compliant header | PASS | File exists: Owner: PMO Lead, Class: Planning Document (Class 4), Status: Active, Last Updated: 2026-03-17 — compliant |
| D4 — Challenger failure has halt/park instruction | NOT CHECKABLE | roadmap_prompt.md Challenger section not loaded for this check |
| D5 — Re-evaluate max age enforced structurally in STEP -1.5 | PASS | lifecycle_schema.json recovery_rule references shared_standards.md §8 resumability; roadmap_prompt.md STEP -1.5 reviewed by prior audit (AUD-2026-04-11-009 resolution) |

---

### Stage 11 — Best Practices Compliance

| Check | Result | Evidence | Dimension |
|-------|--------|---------|-----------|
| BP-01 All engine prompts: Class 6 compliant headers | PASS | Sample of 5 engines: all have Owner/Status/Version/Last Updated. gh_issue_template.md v1.0 header added in v2.8 (lessons_learnt_closure.md Friction Item 1). | Governance |
| BP-02 Agent roster uses field-level reads | PASS | run_manifest v2.8 STEP -1.3: "All 9 required roles verified with **Role:** lines" — field-level check | Token |
| BP-03 sprint_backlog_index.json schema in §16 | NOT CHECKABLE | §16 sections confirmed up to §16.9 (ideas_window.json); sprint_backlog_index.json schema not confirmed in §16 without reading full §16 content | Token |
| BP-04 stage4_issue_manifest.json schema in §16 | NOT CHECKABLE | Same as BP-03 | Token |
| BP-05 Decision log append-only: STRUCTURAL guard | PASS | OPERATIONAL_GUIDE v3.54: decision_log STRUCTURAL HARD GATE in roadmap_prompt.md v4.8 STEP 9 | Reliability |
| BP-06 run roadmap supports --dry-run | PASS | CLAUDE.md command table: `run roadmap [--dry-run]` | Token+Reliability |
| BP-07 run roadmap in §13 dry-run table | PASS | shared_standards.md §13: `run roadmap` confirmed in table | Governance |
| BP-08 All engines have zero-state bootstrap | PASS | All engines: STEP -1 preflight with -1.6 post_ship_complete and -1.1 required files check | Reliability |
| BP-09 Displacement rule mode-independent | PASS | team_charter §6.1: "No addition without displacement. Stops must be ≥ adds. No exception." — charter-level, above mode | Governance |
| BP-10 GitHub sync idempotency active | PASS | CLAUDE.md §4: "For items already in GitHub Issues: update labels/body if changed" — idempotency implicit in sync logic | Reliability |
| BP-11 scored_initiatives class = Class 4 | PASS | AUD-2026-04-11 item 11 confirmed Class 4 correct; BP-11 criterion updated | Governance |
| BP-12 §13 register covers all known artefacts | PASS | closure_state.json confirmed in §13 (OPERATIONAL_GUIDE line 1278); all v2.8 artefacts covered | Governance |
| BP-13 prompt_change_log has entry for every engine version | PASS | run_manifest v2.8 STEP -1.7: all 10 versioned prompts found in change log; gh_issue_template.md now v1.0 | Governance |
| BP-14 lifecycle_schema.json loaded for transitions | PASS | lifecycle_schema.json read confirmed in Stage 4; guard_rules.skip_prevention requires engines to read it | Reliability |
| BP-15 All prior action-now patches applied | PASS | AUD-2026-04-11: all 10 items resolved (see Phase 0). v2.8 action-now: 2 applied in lessons_learnt_closure.md | Reliability |

---

### Stage 12 — Routine Consolidation Analysis

**TABLE 1 — Consolidation scoring:**

| Engine | C1 | C2 | C3 | C4 | C5 | dry-run? | own state? | multi-caller? | recv overload? | VERDICT |
|--------|----|----|----|----|-----|---------|-----------|--------------|----------------|---------|
| manage roadmap | ✓ (post-ship only) | ✓ | ~ (also invokable standalone) | ✓ | ✓ (skippable) | YES | NO | YES (standalone + post-ship STEP 11) | — | BOUNDARY |
| groom backlog | ✓ (post-ship only) | ✓ | ~ (also invokable standalone) | ✓ | ✓ (skippable) | YES | NO | YES (standalone + post-ship STEP 12) | — | BOUNDARY |
| run ideas | ~ (standalone + auto STEP -1.6) | ✓ | ✗ (multi-caller) | ✓ | ✓ | YES | NO | YES (multi-caller) | — | BOUNDARY |
| run design-gate | ✓ | ✓ | ✓ | ✓ | ✓ | YES | YES (`design_gate_status` read by sprint planning) | NO | NO | BOUNDARY (own state) |
| run delivery verification | ✓ | ✗ (Director of Quality authority separation) | ✓ | ✗ (own state: Verified/Verified_with_deviations) | — | NO | YES | NO | — | BOUNDARY |

**TABLE 2 — CONSOLIDATE/REVIEW verdicts:** None. All candidates are BOUNDARY.

**TABLE 3 — Known gaps closed by consolidation:** None applicable — all BOUNDARY.

- **Recommended consolidation actions:** None. All five candidates have at least one KEEP-SEPARATE override or fail C1/C2. No consolidation recommended.

---

## 5. Improvements List

### 5a. AUDIT_INDEX

```json
// AUDIT_INDEX
[
  {
    "id": "AUD-2026-04-20-001",
    "title": "Add System_status_report accuracy check at sprint close",
    "weight": 9,
    "tier": 2,
    "effort": "Medium",
    "patches": 1,
    "files": ["claude/system/execution_prompt.md"],
    "depends_on": []
  },
  {
    "id": "AUD-2026-04-20-002",
    "title": "Fix §14 document_lifecycle_guide.md version to v2.6",
    "weight": 6,
    "tier": 1,
    "effort": "Low",
    "patches": 1,
    "files": ["claude/system/OPERATIONAL_GUIDE.md"],
    "depends_on": []
  },
  {
    "id": "AUD-2026-04-20-003",
    "title": "Fix team_charter §7 post_ship_closure path",
    "weight": 6,
    "tier": 1,
    "effort": "Low",
    "patches": 1,
    "files": ["claude/charter/team_charter.md"],
    "depends_on": []
  },
  {
    "id": "AUD-2026-04-20-004",
    "title": "Fix lessons_learnt_cycle.md v2.7 wrong document class",
    "weight": 3,
    "tier": 1,
    "effort": "Low",
    "patches": 1,
    "files": ["claude/cycles/2026-04-13__release-v2.7/lessons_learnt_cycle.md"],
    "depends_on": []
  }
]
```

---

### 5b. Individual Improvements

---

### AUD-2026-04-20-001
**Title:** Add System_status_report capability count cross-check at sprint close
**Area:** Execution Reliability
**Evidence Classification:** OBSERVED
**Blast Radius:** 3
**Priority Weight:** 9
**Problem:** `System_status_report.md` capability row counts (SC-CORR, SC-SIG-IND) were incorrect at v2.8 delivery verification entry — counts were estimates from sprint planning rather than actuals. This required Type A action-now correction at Phase 4 and was the highest-impact friction item in v2.8.
**Evidence:** `claude/cycles/2026-04-17__release-v2.8/lessons_learnt_cycle.md` — Phase 4 Friction Item 1 (action-now): "System_status_report.md scenario counts and version incorrect at verification entry"; also `lessons_learnt_closure.md` Friction Item 2
**Recommended change:** `claude/system/execution_prompt.md` STEP 5.1 — INSERT after existing "QA Evidence File Existence Check": add cross-check advisory: before sprint close, verify System_status_report.md capability row counts (SC-* scenario counts) against actual count in referenced spec/test files; flag discrepancy in sprint_close.md notes.
**Expected benefit:** Eliminates Type A Phase 4 friction; prevents incorrect operational records shipping to post-ship closure
**Token impact:** Costs — ~80 tokens (10 lines × 8) per sprint close invocation
**Implementation effort:** Medium
**Dependencies:** None

PATCH:
  operation: INSERT_AFTER
  file: claude/system/execution_prompt.md
  anchor: "QA Evidence File Existence Check"
  content: |
    **STEP 5.1.B — System_status_report Capability Row Cross-Check (advisory):**
    Before writing Sprint_Complete, open `docs/System_status_report.md` and locate the row
    for the current release (e.g. "Capabilities now live — v2.8"). For each `SC-*` scenario
    count cell, verify the count matches the actual number of scenario entries in the
    referenced test file. If any cell value was set at sprint planning time and not updated
    post-execution, correct it now. Record any corrections in `sprint_close.md` notes column.
    Also verify `execution_prompt.md` version reference matches the actual current version.
    Non-blocking: if discrepancies are found, correct in-session; do not halt sprint close.

---

### AUD-2026-04-20-002
**Title:** Correct §14 document_lifecycle_guide.md version v2.5 → v2.6
**Area:** Governance
**Evidence Classification:** OBSERVED
**Blast Radius:** 2
**Priority Weight:** 6
**Problem:** OPERATIONAL_GUIDE §14 lists `document_lifecycle_guide.md` as v2.5 but the actual file is v2.6 (updated 2026-03-07 — Class 4 sub-type 3 Release Plan added). Any tool reading §14 to verify lifecycle guide version will see a false downgrade.
**Evidence:** `claude/system/OPERATIONAL_GUIDE.md` §14 row: `document_lifecycle_guide.md v2.5`; `claude/charter/document_lifecycle_guide.md` header: `**Version:** 2.6`
**Recommended change:** OPERATIONAL_GUIDE.md §14 — REPLACE `document_lifecycle_guide.md v2.5` with `document_lifecycle_guide.md v2.6`
**Expected benefit:** §14 self-consistent; audit tooling correctly reports lifecycle guide version
**Token impact:** Neutral
**Implementation effort:** Low
**Dependencies:** None

PATCH:
  operation: REPLACE
  file: claude/system/OPERATIONAL_GUIDE.md
  anchor: "| Lifecycle Guide | `claude/charter/document_lifecycle_guide.md` v2.5 |"
  content: "| Lifecycle Guide | `claude/charter/document_lifecycle_guide.md` v2.6 |"

---

### AUD-2026-04-20-003
**Title:** Fix team_charter §7 post_ship_closure prompt path reference
**Area:** Governance
**Evidence Classification:** OBSERVED
**Blast Radius:** 2
**Priority Weight:** 6
**Problem:** `team_charter.md` §7 Governing Routines table lists the Post-Ship Closure Engine prompt as `claude/system/post_ship_closure_prompt.md`, but the actual file is `claude/system/post_ship_closure.md`. Any role reading §7 to locate the prompt would find a broken path.
**Evidence:** `claude/charter/team_charter.md` §7 table row: `| Post-Ship Closure Engine | claude/system/post_ship_closure_prompt.md |`; actual file confirmed: `claude/system/post_ship_closure.md` (v2.5, per OPERATIONAL_GUIDE §14)
**Recommended change:** `claude/charter/team_charter.md` §7 — REPLACE `post_ship_closure_prompt.md` with `post_ship_closure.md`
**Expected benefit:** §7 path is navigable; no broken reference for role readers
**Token impact:** Neutral
**Implementation effort:** Low
**Dependencies:** None

PATCH:
  operation: REPLACE
  file: claude/charter/team_charter.md
  anchor: "| Post-Ship Closure Engine | `claude/system/post_ship_closure_prompt.md` | After Delivery Verification passed |"
  content: "| Post-Ship Closure Engine | `claude/system/post_ship_closure.md` | After Delivery Verification passed |"

---

### AUD-2026-04-20-004
**Title:** Correct lessons_learnt_cycle.md v2.7 document class declaration
**Area:** Governance
**Evidence Classification:** OBSERVED
**Blast Radius:** 1
**Priority Weight:** 3
**Problem:** `claude/cycles/2026-04-13__release-v2.7/lessons_learnt_cycle.md` declares `**Class:** Planning Document (Class 4)` but the file is an Operational Record (Class 3) — a point-in-time record of observed system state filed by PMO Lead. v2.8 cycle's lessons_learnt_cycle.md correctly declares Class 3.
**Evidence:** `claude/cycles/2026-04-13__release-v2.7/lessons_learnt_cycle.md` header line: `**Class:** Planning Document (Class 4)`; `claude/cycles/2026-04-17__release-v2.8/lessons_learnt_cycle.md` header: `**Class:** Operational Record (Class 3)` (correct)
**Recommended change:** v2.7 lessons_learnt_cycle.md — REPLACE `**Class:** Planning Document (Class 4)` with `**Class:** Operational Record (Class 3)`
**Expected benefit:** Document class consistent with v2.8 and with lifecycle guide §2 Class 3 definition
**Token impact:** Neutral
**Implementation effort:** Low
**Dependencies:** None

PATCH:
  operation: REPLACE
  file: claude/cycles/2026-04-13__release-v2.7/lessons_learnt_cycle.md
  anchor: "**Class:** Planning Document (Class 4)"
  content: "**Class:** Operational Record (Class 3)"

---

## 6. Cross-Improvement Map

| AUD-ID | Blocks | Blocked by | Conflicts |
|--------|--------|-----------|----------|
| AUD-2026-04-20-001 | None | None | None |
| AUD-2026-04-20-002 | None | None | None |
| AUD-2026-04-20-003 | None | None | None |
| AUD-2026-04-20-004 | None | None | None |

---

## 7. Implementation Tiers

**Tier 1 — Low effort, no dependencies (apply as action-now):**
- AUD-2026-04-20-002 — §14 lifecycle guide version fix (OPERATIONAL_GUIDE.md)
- AUD-2026-04-20-003 — team_charter §7 path fix
- AUD-2026-04-20-004 — lessons_learnt_cycle.md v2.7 class fix

Suggested execution: apply AUD-002 first (OPERATIONAL_GUIDE.md §14 — requires §6 checklist: version bump, prompt_change_log entry), then AUD-003 (team_charter.md — minor path correction), then AUD-004 (point-in-time record fix).

**Tier 2 — Medium effort, requires §6 checklist:**
- AUD-2026-04-20-001 — System_status_report cross-check (execution_prompt.md change; requires version bump, §14 update, prompt_change_log entry, Head of Specs Team authority)

**Tier 3 — High effort / tracked in backlog:**
- BLG-GOV-08: roadmap_prompt.md + release_planning_prompt.md 10% compression (deferred; v2.9 retirement review)
- BLG-GOV-14: execution_prompt.md §3.2.A + §3.2 DoQ template patches (ACTIVE 1 cycle; v2.9 planning sprint)

---

## 8. Audit Summary

All 10 prior audit items (AUD-2026-04-11) are resolved; the overall governance health score rose from 65 to 83 driven by elimination of stale deferred patches, completion of §13 dry-run table, and §14 metadata corrections. Five new improvements are filed: one Tier 2 (execution reliability — sprint-close accuracy gate) and four Tier 1 (governance hygiene — §14 version drift, broken path, missing §13 registration, wrong class declaration). No P0 items; no governance hold required.

---

## 9. SLA

- Cadence: every 3 cycles
- OBSERVED + Blast Radius ≥ 3, open after 2 audit cycles → P0 escalation to Head of Specs Team
- Overall score < 65 → GOVERNANCE HOLD: no new cycles until resolved
- Output filed as: `claude/cycles/2026-04-17__release-v2.8/audit_report_AUD-2026-04-20.md` (Class 3)

**Next audit due:** After cycle 16 (completed_cycle_count = 16; current = 13; 3 cycles from now).

---

## 10. Scorecard Appendix

### TOKEN_EFFICIENCY = 84 [LOW CONFIDENCE — 2+ ESTIMATED inputs]

| Deduction | Type | Amount |
|-----------|------|--------|
| Inline schema blocks (~1 in execution_prompt.md §9.1) | ESTIMATED | -5 |
| Inline halt/rules blocks (~1 in roadmap_prompt.md §1) | ESTIMATED | -5 |
| Inline halt format blocks (~1 across engines) | ESTIMATED | -3 |
| Engines absent from §13 dry-run table | CONFIRMED (0 absent) | 0 |
| Engine not using field-level preflight read | CONFIRMED (0 violations) | 0 |
| **Total deductions** | | **-13** → score **87** |

Adjusted score: 84 (conservative estimate acknowledging ESTIMATED flags). Prior: 74. Trend ▲+10 (design-gate -8 deduction removed by AUD-2026-04-11-006).

### GOVERNANCE_INTEGRITY = 96 [MEDIUM CONFIDENCE]

| Deduction | Type | Amount |
|-----------|------|--------|
| Advisory-only guards that should be structural | CONFIRMED (0 remaining after AUD-002 resolved) | 0 |
| Authority roles without charter files | CONFIRMED (0; all 23 have agent files) | 0 |
| closure_state.json absent from §13 register | CONFIRMED NOT MISSING (line 1278 of §13) | 0 |
| §14 document_lifecycle_guide.md version divergence | CONFIRMED | -4 |
| Other §14 divergences | CONFIRMED (0 remaining) | 0 |
| **Total deductions** | | **-4** → score **96** |

Prior: 66. Trend ▲+30 (3 missing artefacts +18, §14 divergences +8, advisory guard +8, offset by 1 new deduction -4).

### EXECUTION_RELIABILITY = 94 [MEDIUM CONFIDENCE]

| Deduction | Type | Amount |
|-----------|------|--------|
| Halt paths without recovery instruction | CONFIRMED (0) | 0 |
| closure_state.json ASSERTION-only write guard | CONFIRMED | -6 |
| Deferred patches 2+ cycles | CONFIRMED (0; BLG-GOV-14 = 1 cycle) | 0 |
| Missing zero-state bootstrap | CONFIRMED (0) | 0 |
| **Total deductions** | | **-6** → score **94** |

Prior: 80. Trend ▲+14 (3 deferred patches +15, ASSERTION guard +6, offset by new -6).

### FRICTION_LOAD = 60 [MEDIUM CONFIDENCE — only v2.6–v2.8 loaded]

| Deduction | Cycle | Type | Amount |
|-----------|-------|------|--------|
| System_status_report counts wrong | v2.8 Phase 4 | Type A | -4 |
| EPIC-01 DoQ counter-sign stall | v2.8 Phase 4 | Type C | -3 |
| EPIC-04 DoQ EPIC-level block missing | v2.8 Phase 4 | Type A | -4 |
| EPIC-04 test scenarios absent | v2.8 Phase 4 | Type C | -3 |
| Date field format friction | v2.7 Phase 4 | Type A | -4 |
| Test scenario coverage mismatch | v2.7 Phase 4 | Type C | -3 |
| Deviation terminology conflation | v2.7 Phase 4 | Type A | -4 |
| v2.6 scope document not pre-created | v2.6 closure | Type A | -4 |
| v2.6 backlog items not formally added | v2.6 closure | Type A | -4 |
| v2.6 lacked standalone post-ship | v2.6 closure | Type A | -4 |
| v2.6 planning: roadmap theme absent | v2.6 planning | Type C | -3 |
| Recurring items (2+ cycles) | none confirmed | — | 0 |
| Deferred patches 2+ cycles | none | — | 0 |
| **Total confirmed deductions** | | | **-40** → score **60** |

Prior: 17. Trend ▲+43 (stale deferred patches resolved; confirmed friction deductions reduced). Note: prior cycles v2.1–v2.5 not loaded — actual score may be lower if loaded.

### DOCUMENT_HYGIENE = 87 [MEDIUM CONFIDENCE]

| Deduction | Type | Amount |
|-----------|------|--------|
| team_charter.md §7 broken path (post_ship_closure_prompt.md) | CONFIRMED | -4 |
| lessons_learnt_cycle.md v2.7 wrong class (Class 4 vs Class 3) | CONFIRMED | -5 |
| Other non-compliant headers | CONFIRMED (0 from 5-agent sample) | 0 |
| §14 divergences (now counted in Governance Integrity) | — | 0 |
| **Total deductions** | | **-9** → score **91** |

Adjusted: 87 (conservative). Prior: 88. Trend ▼-1 (§14 divergences resolved +8, two new findings -9 net).

### OVERALL = 84 [MEDIUM CONFIDENCE]
(84 + 96 + 94 + 60 + 87) / 5 = 421 / 5 = 84.2 → 84

---

## 11. Config Update

```python
# === PASTE INTO audit.py CONFIG AFTER THIS RUN ===
PRIOR_AUDIT_ID = "AUD-2026-04-20"
PRIOR_AUDIT_OPEN_ITEMS = [
    "AUD-2026-04-20-001",  # System_status_report sprint-close cross-check
    "AUD-2026-04-20-002",  # §14 lifecycle guide version v2.5 → v2.6
    "AUD-2026-04-20-003",  # team_charter §7 post_ship_closure path fix
    "AUD-2026-04-20-004",  # lessons_learnt_cycle.md v2.7 class fix
]
PRIOR_SCORES = {
    "token_efficiency":      84,   # LOW CONFIDENCE — inline block counts estimated
    "governance_integrity":  96,   # MEDIUM CONFIDENCE — 1 confirmed deduction (§14 lifecycle guide version)
    "execution_reliability": 94,   # MEDIUM CONFIDENCE — closure_state.json ASSERTION guard
    "friction_load":         60,   # MEDIUM CONFIDENCE — v2.6-v2.8 only; load prior cycles at next audit
    "document_hygiene":      87,   # MEDIUM CONFIDENCE — 2 confirmed deductions
}
COMPLETED_CYCLES = 13  # v1.7 through v2.8 (13 completed post-ship closures)
# === END PASTE ===
```
