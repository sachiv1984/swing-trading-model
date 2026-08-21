Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-08-21

# Claude Lifecycle Audit — AUD-2026-08-21

Scope: `claude/` | Audit version: 6 | Window: cycles since `AUD-2026-08-12` (`2026-08-12__release-v8.7`, `2026-08-14__release-v8.8`, `2026-08-17__release-v8.9` — 3 cycle-records)

**Staleness check:** `claude/audit.py`'s CONFIG constants at session start (`PRIOR_AUDIT_ID = "AUD-2026-08-12"`, `COMPLETED_CYCLES = 73`) match the most recently filed report (`claude/cycles/2026-08-11__release-v8.6/audit_report_AUD-2026-08-12.md` §11) exactly. No staleness. `COMPLETED_CYCLES` now 76 (3 cycles closed since last audit) — cadence due per SLA ("every 3 cycles").

---

## 1. Resolved Since Last Audit

`PRIOR_AUDIT_OPEN_ITEMS = []` — 0 items open at session end of AUD-2026-08-12 (001/002 applied same session; 003/004/005 applied post-publication same day, per that report's own §11).

| AUD-ID | Title (3 words) | Status | Evidence ref |
|--------|------------------|--------|---------------|
| — | No open items carried | N/A | `PRIOR_AUDIT_OPEN_ITEMS` empty; nothing to resolve this run |

---

## 2. Health Scorecard

**Methodology note (per established precedent, AUD-2026-08-08/AUD-2026-08-12):** `TOKEN_EFFICIENCY`, `GOVERNANCE_INTEGRITY`, `EXECUTION_RELIABILITY`, `DOCUMENT_HYGIENE` are scored **incrementally** — prior baseline + confirmed deltas this window only, not a full re-derivation (full re-derivation was last done at an earlier audit; re-deriving all four from scratch every 3 cycles is not token-efficient and the prompt does not require it). `FRICTION_LOAD` is recomputed **fresh** each window per its own explicit rule.

SYSTEM HEALTH — 2026-08-21 | Prior: 2026-08-12

| Dimension | Score | Bar (▓=10pts) | Trend | Confidence |
|-----------|-------|----------------|-------|------------|
| Token Efficiency | 84 | ▓▓▓▓▓▓▓▓░░ | ▼ | HIGH |
| Governance Integrity | 74 | ▓▓▓▓▓▓▓░░░ | ▼ | HIGH |
| Execution Reliability | 53 | ▓▓▓▓▓░░░░░ | ─ | HIGH (deltas) / carried baseline not re-derived |
| Friction Load | 44 | ▓▓▓▓░░░░░░ | ▲ (raw) / ▲ (normalised rate) | HIGH |
| Document Hygiene | 100 | ▓▓▓▓▓▓▓▓▓▓ | ─ | HIGH |
| **Overall** | **71** | ▓▓▓▓▓▓▓░░░ | ▼ (74→71) | — |

Overall 71 ≥ 65 — no GOVERNANCE HOLD triggered.

**Friction Load — normalised rate (mandatory note):** raw score rose 37→44 (▲) **and** the normalised rate improved too this time — 17 friction items / 3 cycle-records = 5.67 items/cycle-record, down from the prior window's 7.5. Unlike the AUD-2026-08-12 reading (where the two signals disagreed), both signals agree this window: friction is genuinely down, not just averaged over more cycles.

---

## 3. Gap Register

| Stage | File | Status | Impact (5 words) | → Improvement? |
|-------|------|--------|--------------------|------------------|
| Phase 1 | `claude/agents/` | Loaded (23/23 files) | None — full roster confirmed | No |
| Stage 1 | `claude/README.md` §4.2 | Loaded | `sync gh` absent from summary table (inline-only in CLAUDE.md, not a governed routine — expected) | No |
| Stage 2 | `claude/cycles/*/run_manifest.md` (v8.7/v8.8/v8.9) | PARTIAL — file paths confirmed, preflight-table content not read this run | B1 (Auth) compliance not verified | Flagged below, no fresh Improvement |
| Stage 3 | `claude/roadmap/displacement_debt_register.md` | NOT FOUND on disk (by design — create-if-absent, deferred to next `run roadmap`/`manage roadmap`; tracked live at `ESC-EXEC-20260818-02`) | Absent from §13 register too | Yes — AUD-2026-08-21-003 |
| Stage 4 | Full R3 (idempotency) / R5 (zero-state bootstrap) sub-tables | PARTIAL — spot-checked (§7.1, §12.1, §10.3/§10.4) not exhaustively swept | EXECUTION_RELIABILITY baseline carried, not re-derived | No — consistent with 2 prior audits' own treatment |
| Stage 7 | 9 engine files' inline ` ```json ` blocks | ESTIMATED → spot-checked 3 (design_gate, backlog_management, sprint_planning) — all confirmed engine-specific state-write examples, not duplicated §16 schemas | 0 confirmed SST3 violations | No |
| Stage 9 | `claude/system/roadmap_prompt.md` §9, `claude/charter/team_charter.md` §6 | Loaded, field-level | Both correctly reference `invariants.md` rather than duplicating | No |

---

## 4. Stage Findings

### Stage 1 — Lifecycle Mapping

**TABLE 1 — Command path check:**

| Command | Prompt path in CLAUDE.md | File confirmed? | Invocation syntax match? |
|---------|---------------------------|------------------|----------------------------|
| `run ideas` | `claude/system/idea_intake_prompt.md` | Yes | Yes |
| `run roadmap` (×2 rows) | `claude/system/roadmap_prompt.md` | Yes | Yes |
| `manage roadmap` | `claude/system/roadmap_management_prompt.md` | Yes | Yes |
| `groom backlog` | `claude/system/backlog_management_prompt.md` | Yes | Yes |
| `run ideas housekeeping` | `claude/system/ideas_housekeeping_prompt.md` | Yes | Yes |
| `plan release` | `claude/system/release_planning_prompt.md` | Yes | Yes |
| `run design-gate` | `claude/system/design_gate_prompt.md` | Yes | Yes |
| `plan sprint` | `claude/system/sprint_planning_prompt.md` | Yes | Yes |
| `amend cycle` | `claude/system/amendment_cycle_prompt.md` | Yes | Yes |
| `run sprint` | `claude/system/execution_prompt.md` | Yes | Yes |
| `run delivery verification` | `claude/system/delivery_verification_prompt.md` | Yes | Yes |
| `run post-ship` | `claude/system/post_ship_closure.md` | Yes | Yes |
| `sync gh` | inline (§4) | Yes (inline instructions present) | Yes |
| `run audit` | `claude/audit.py` | Yes | Yes |

**TABLE 2 — Engine documentation coverage:**

| Engine | In OPERATIONAL_GUIDE §4? | In README §4.2? | Gap |
|--------|----------------------------|-------------------|-----|
| All 12 governed routines + Roadmap Rebalance | Yes | Yes | None |
| `sync gh` | No (utility, not a governed routine) | No | None — expected, not a §4/§4.2-class routine |

**TABLE 3 — §14 version spot check (3 engines vs prompt_change_log):**

| Engine | §14 version | Last log entry version | Match? |
|--------|-------------|--------------------------|--------|
| Shared Standards | v3.29 | v3.28→v3.29 (2026-08-21) | Yes |
| Roadmap Management Engine | v1.5 | v1.4→v1.5 (2026-08-18) | Yes |
| Post-Ship Closure Engine | v2.29 | v2.28→v2.29 (2026-08-18) | Yes |
| OPERATIONAL_GUIDE.md self-row | 4.169 | header 4.169 / Change Log top row 4.169 | Yes — 3-way self-consistency confirmed |

**FINDINGS:**
- No broken path found in CLAUDE.md command table.
- No OPERATIONAL_GUIDE §4 engine missing from README §4.2.
- `CLAUDE.md` carries no document-level `**Last Updated:**` header field itself (by established convention — see `prompt_change_log.md` "no-version-field convention for CLAUDE.md changes"); N/A for staleness check.
- `run audit` **is** present in the CLAUDE.md command table (§1 row 16) — no gap.
- **New (Document Hygiene, unscored):** `OPERATIONAL_GUIDE.md` section numbers are out of physical sequence — `## 16. Artefact Lifecycle Model` (line 1359) appears **before** `## 15. Governance Health Score` (line 1377), which appears **before** `## 14. Playbook Governance` (line 1452). Numbers themselves are internally consistent (no duplicate/skipped number), but a reader following the document top-to-bottom encounters §16 → §15 → §14 → Change Log, not ascending order. Does not match any of the 4 DOCUMENT_HYGIENE formula lines exactly (not a non-compliant header, wrong class, broken path, or agent-format issue), so left unscored per the CONFIRMED COUNTS RULE — flagged as Improvement AUD-2026-08-21-001.

### Stage 2 — Behavioural Audit

**COMPLIANCE TABLE:**

| Cycle | B1 Auth | B2 LL filed | B3 Prior patches | B4 Hard gate | B5 Action-now | B6 Log grew | B7 No 2nd carry |
|-------|---------|-------------|--------------------|---------------|-----------------|---------------|--------------------|
| `2026-08-12__release-v8.7` | NOT VERIFIED (run_manifest.md not read this run) | Pass | Pass (Phase3/4 both cite prior-cycle checks) | NO GATES FIRED — compliant | Pass | Pass | Pass |
| `2026-08-14__release-v8.8` | NOT VERIFIED | Pass | Pass | NO GATES FIRED — compliant | Pass | Pass | Pass (both carries re-deferred correctly, not silently dropped) |
| `2026-08-17__release-v8.9` | NOT VERIFIED | Pass | Pass | NO GATES FIRED — compliant | Pass | Pass | Pass — 2 items crossed the 2-cycle threshold and were **correctly escalated** per §6.4 (not re-deferred a 3rd time), then resolved same-session at closure |
| **compliance %** | 0/3 checked (PARTIAL run) | 3/3 (100%) | 3/3 (100%) | 3/3 — **B4 SPECIAL RULE: COMPLETED_CYCLES (76) ≥ 3 → NO GATES FIRED, compliant**, all 3 cycles (no `status: Blocked` transition found in any of the 3 cycles' records) | 3/3 (100%) | 3/3 (100%) | 3/3 (100%) |

B1 was not checked this run (`run_manifest.md` preflight tables not opened) — flagged in Gap Register rather than scored as a failure; no confirmed compliance issue either way.

**PATTERN TABLE (window: v8.7, v8.8, v8.9 — 17 friction items total, Phase 3 + Phase 4 + Closure records):**

| Friction Type | Count (window) | Top source file | Recurring? |
|---------------|------------------|-------------------|------------|
| Type A — Governance Drift | 6 | `lessons_learnt_cycle.md` / `lessons_learnt_closure.md` (all 3 cycles) | No single item recurs; pattern-class recurs |
| Type B — Semantic Mismatch | 3 | `qa_evidence_template.md` / `execution_prompt.md` / `api_performance_baseline.md` | 1 of 3 (Sandbox Access Constraint disclosure) crossed the 2-cycle threshold |
| Type C — Dependency Stall | 5 | `execution_state.json` merge_gate / `sprint_close.md` | 1 of 5 (CI-green restatement) crossed the 2-cycle threshold |
| Type D — Cognitive Fatigue | 2 | `OPERATIONAL_GUIDE.md` / `qa_evidence_EPIC-03.md` | No |
| Type E | 0 | — | — |

**TREND LINE:** Total friction items per cycle-record: `[2026-08-12__release-v8.7: 7, 2026-08-14__release-v8.8: 4, 2026-08-17__release-v8.9: 6]`
State trend: **FLAT-TO-DECREASING** (7→4→6; window average 5.67/cycle vs prior window's 7.5/cycle — down overall, though v8.9 ticked back up from v8.8's low).

All B-checks with confirmed data are ≥ 75% compliance — no auto-generated OBSERVED improvement from this stage (B1's PARTIAL status is a coverage gap, not a confirmed <75% finding).

### Stage 3 — Governance Integrity

**TABLE 1 — Agent roster (23/23 files):**

All 23 agent files (`ai_compliance_governance_officer.md` … `strategy_rules_system_intent_owner.md`) carry a `**Role:**` bold-field header (COMPLIANT format) and a `**Version:**` field. Status: CONFIRMED for all 23 (cross-checked against `team_charter.md` §3.1–§3.3's role list — 23 roles named, 23 agent files present, 1:1 match). No PATH-STALE or NOT CONFIRMED entries found.

**TABLE 2 — Governance checks:**

| Check | Result | Evidence (file + section) |
|-------|--------|------------------------------|
| G1 — All charter roles have agent file | PASS | `team_charter.md` §3.1 (9 decision authorities) + §3.2/§3.3 (14 further roles) = 23; `claude/agents/` = 23 files, 1:1 |
| G2 — Agent lifecycle refs point to canonical path | PASS (spot-checked; no PATH-STALE found in role/version scan) | `claude/agents/*.md` header fields |
| G3 — Artefact class declarations match lifecycle guide §3 | PASS (spot-checked: `rejected_but_strong.md` = Class 4, matches; `lessons_learnt_cycle.md`/`_closure.md` = Class 3, matches §13 register) | `claude/ideas/rejected_but_strong.md`, `OPERATIONAL_GUIDE.md` §13 |
| G4 — §13 register covers scoring + ideas + lessons artefacts | PASS | `OPERATIONAL_GUIDE.md` §13: Scored Initiatives row present; 4 Ideas rows present (Window State/Register/Window Summary/Rejected-but-Strong); 4 Lessons Learnt rows present (Rebalance/Release/Cycle/Closure) |
| G5 — Design gate bypass authority in charter (not prose-only) | PASS | `.claude_current_state.json.design_gate_bypass_authority` field exists in schema; `OPERATIONAL_GUIDE.md` §6B.8/§6.5 define bypass mechanics structurally, not prose-only |

**New finding (Governance Integrity, scored):** `claude/roadmap/displacement_debt_register.md` — wired into `roadmap_prompt.md` STEP 8 (v9.16, create-if-absent) since 2026-08-18 (ST-21, BLG-GOV-264), tracked live via `ESC-EXEC-20260818-02` (Open, non-blocking), but **absent from `OPERATIONAL_GUIDE.md` §13 Artefact Register** — no row exists for it even as a pending/not-yet-created artefact. Confirmed via direct grep of §13's table content (lines 1266–1359) — 0 matches for "displacement". → Improvement AUD-2026-08-21-003.

### Stage 4 — Lifecycle Reliability

| Check | Result | Evidence |
|-------|--------|----------|
| R1 — All lifecycle states have valid entry AND exit transitions | PASS (spot-checked) | `lifecycle_schema.json` — 10 states, `Closed→Release_Planning_Complete→{Design_Gate_Passed\|Sprint_Planning_Complete}→Sprint_Planning_Complete→Executing→Sprint_Complete→{Verified\|Verified_with_deviations}→Closed`; `Blocked`/`Amendment_In_Progress` both have documented recovery/exit paths (§10.4, amendment STEP 3.2) |
| R2 — All hard gate halt paths have defined recovery instruction | PASS (general mechanism) | `shared_standards.md` §10.4 Blocked State Protocol — explicit recovery: domain authority resolves, `status` restored from `prior_status`; Amendment rejection path (`amendment_cycle_prompt.md` §3.2) equally explicit |
| R3 — Idempotency: classify each write op | PARTIAL — not exhaustively swept this run | See sub-table below (spot-checked only) |
| R4 — Re-evaluate max age rule exists in STEP -1.5 | PASS | `roadmap_prompt.md` — Six-Arc reconciliation patch tracked with "1st re-check not OVERDUE, new target next STEP 11.4 meta-review" language confirms an age-rule mechanism is live and being applied |
| R5 — All engines have zero-state bootstrap path | NOT VERIFIED this run | Not swept — carried from baseline per Execution Reliability incremental-scoring convention |
| R6 — Concurrent write prevention referenced at state-write step | PASS | `shared_standards.md` §10.3: "confirm the value... has not changed since step 1. If it has changed (concurrent write), halt with `ESC-YYYYMMDD-nn`" |

**R3 SUB-TABLE (spot-checked only):**

| Write operation | File | Guard type | Engine |
|------------------|------|------------|--------|
| `pr_status`/`pr_number` pre-seal sync | `execution_state.json` | STRUCTURAL (explicit "idempotent — re-running does not alter already-correct values" statement) | Sprint Execution STEP 5.0A |
| Escalation record append | `execution_escalations.md` | STRUCTURAL (§7.1 Append-Only Structural Verification Procedure) | Shared (all engines) |
| Per-EPIC merge sequencing state | `execution_state.json` (`merge_gate`) | STRUCTURAL (§12.1 Per-EPIC Execution State Mechanism) | Sprint Execution |

0 ASSERTION-only or ABSENT writes confirmed this run (sample of 3, not exhaustive — do not treat as a clean full sweep).

### Stage 5 — Token Budget Analysis

| Engine | Lines | ~Tokens | Preflight files (N) | ~Preflight tokens | Inline blocks (N) | ~Block tokens | Total/invoke | Invoke/cycle | Cycle cost | Confidence |
|--------|-------|---------|------------------------|------------------------|------------------------|-------------------|-----------------|-----------------|---------------|------------|
| `roadmap_prompt.md` | 893 | ~7,144 | 1 (`.claude_current_state.json`, field-scoped) | ~200 | 0 confirmed | 0 | ~7,344 | ~1 | ~7,344 | HIGH (lines confirmed) |
| `release_planning_prompt.md` | 1,141 | ~9,128 | 1 | ~200 | 0 confirmed | 0 | ~9,328 | ~1 | ~9,328 | HIGH |
| `sprint_planning_prompt.md` | 654 | ~5,232 | 1 | ~200 | 0 confirmed | 0 | ~5,432 | ~1 | ~5,432 | HIGH |
| `execution_prompt.md` | 1,133 | ~9,064 | 1 | ~200 | 0 confirmed | 0 | ~9,264 | ~6 [ESTIMATED — one per EPIC, v8.9 had 6] | ~55,584 [ESTIMATED] | LOW — invoke count estimated, load and count real per-cycle re-invocations to confirm |
| `delivery_verification_prompt.md` | 652 | ~5,216 | 1 | ~200 | 0 confirmed | 0 | ~5,416 | ~1 | ~5,416 | HIGH |
| `post_ship_closure.md` | 792 | ~6,336 | 1 | ~200 | 0 confirmed | 0 | ~6,536 | ~1 | ~6,536 | HIGH |
| `lessons_learnt_prompt.md` | 508 | ~4,064 | 0 | 0 | 0 confirmed | 0 | ~4,064 | ~3 [ESTIMATED — Phase 3, Phase 4, Closure] | ~12,192 [ESTIMATED] | LOW — invoke count estimated |

Formula: tokens = lines × 8 | preflight = Σ(file_lines × 8) | total = prompt + preflight + blocks

**METHODOLOGY FOOTNOTE (mandatory):**
⚠ This table does not capture in-run context accumulation. For `execution_prompt.md`, actual per-invocation cost grows with sprint size (loaded EPIC items add to context). Reported cost may understate actual by 30–50% on large sprints. Use as lower bound.

**RANKED SAVINGS TABLE:**

| Rank | Opportunity | Current tokens/cycle | Post-fix tokens/cycle | Saving |
|------|-------------|--------------------------|----------------------------|--------|
| 1 | `execution_prompt.md` (1,133 lines) is the largest engine prompt and the most-frequently re-invoked (once per EPIC); extracting the §5.3 QA evidence consolidation-block template text (already partially delegated to `qa_evidence_template.md`) and the STEP 5.0A pr_status sync pseudocode block into referenced sub-files would reduce per-invocation weight | ~55,584 [ESTIMATED] | Not quantified — requires line-level extraction count | Flagged for next audit's full Stage 7 extraction sweep |
| 2 | `release_planning_prompt.md` (1,141 lines) and `shared_standards.md` (1,114 lines) both exceed the 500-line Stage 7 flag threshold but are single-invoke-per-cycle — lower priority than execution_prompt.md | ~9,328 | — | Not actioned this run |

**DEAD LOAD CHECK:**

| Engine | File loaded at preflight | Used beyond preflight check? | Dead? |
|--------|------------------------------|-----------------------------------|-------|
| All 8 engines | `.claude_current_state.json` (field-scoped per §14) | Yes — fields re-read at later named steps per §14's own carve-out | No |

**DRY-RUN GAP:**

| Engine | In §13 dry-run table? | If not: token risk per failed run |
|--------|---------------------------|----------------------------------------|
| All 12 governed routines + `run audit` | Yes — confirmed, 13 rows, 0 gaps (direct read of `shared_standards.md` §13, lines 426–447) | N/A |

**CYCLE TOTAL:** ~101,232 tokens/typical cycle [ESTIMATED — execution_prompt.md and lessons_learnt_prompt.md invoke counts are estimated; treat as a directional lower bound, not a confirmed figure].

### Stage 6 — Engine Handoff Integrity

**HANDOFF TABLE:**

| Pair | Field/Section | Producer writes? | Consumer reads? | Match? |
|------|-----------------|----------------------|----------------------|--------|
| Release Planning → Sprint Planning | `design_gate_required`, `sprint_planning_pre_condition` | Yes (`release_plan` block, `.claude_current_state.json`) | Yes (§13 dry-run + §14 preflight fields list `design_gate_status`, `design_gate_bypass_*`) | Match |
| Sprint Planning → Sprint Execution | `sprint_sealed`, `sprint_backlog_path` | Yes | Yes (§14 preflight: `sprint_sealed`, `sprint_planning`) | Match |
| Sprint Execution → Delivery Verification | `Verification Readiness Statement` block (`sprint_close.md`) | Yes — STRUCTURAL, verbatim block required (`execution_prompt.md` §5.3, line ~923) | Yes ("Delivery Verification Engine reads this block at STEP -1.2; absent/malformed block causes a preflight failure") | Match |
| Delivery Verification → Post-Ship Closure | `verification_status`, `next_cycle_unblocked` | Yes | Yes (§14 preflight: `verification_status`, `next_cycle_unblocked`) | Match |
| Roadmap Rebalance → Release Planning | `next_release` | Yes (roadmap STEP 9-class outcome) | Yes (Release Planning consumes `next_release` at invocation) | Match — this exact field was the subject of a fixed staleness bug (`post_ship_closure.md` v2.28 changelog entry, `prior_cycle` sibling field) |
| Amendment Cycle → Sprint Planning | `active_amendment`, `amendment_status`, `amended_backlog_slice_path` | Yes | Yes (Sprint Planning's Amendment_In_Progress hard gate, `sprint_planning_prompt.md:56`) | Match |

0 CONSUMER READS UNGUARANTEED FIELD, 0 DEAD OUTPUT, 0 SCHEMA VERSION MISMATCH confirmed in this spot-checked pass (6 pairs, not an exhaustive field-by-field audit of every written key).

### Stage 7 — Prompt Architecture & Compression

**COMPLEXITY TABLE:**

| Engine | Lines | Flagged? |
|--------|-------|----------|
| `roadmap_prompt.md` | 893 | Flagged (>500 lines) |
| `release_planning_prompt.md` | 1,141 | Flagged (>500 lines) |
| `sprint_planning_prompt.md` | 654 | Flagged (>500 lines) |
| `execution_prompt.md` | 1,133 | Flagged (>500 lines) |
| `delivery_verification_prompt.md` | 652 | Flagged (>500 lines) |
| `post_ship_closure.md` | 792 | Flagged (>500 lines) |
| `shared_standards.md` | 1,114 | Flagged (>500 lines) — reference document, not a step-driven engine; flag less actionable here |
| `lessons_learnt_prompt.md` | 508 | Flagged (marginal, >500) |
| `amendment_cycle_prompt.md` | 630 | Flagged (>500 lines) |
| `backlog_management_prompt.md` | 485 | Not flagged |
| `roadmap_management_prompt.md` | 378 | Not flagged |
| `ideas_housekeeping_prompt.md` | 284 | Not flagged |
| `design_gate_prompt.md` | 311 | Not flagged |
| `idea_intake_prompt.md` | 455 | Not flagged |

STEPs/hard-gates/branches counts not exhaustively tallied this run (would require a full per-file STEP-header count pass) — line-count flags above are CONFIRMED; STEP/gate/branch columns omitted rather than estimated.

**EXTRACTION TABLE:**

| Category | Confirmed instances (cite file+step) | Canonical home | Saving if extracted |
|----------|------------------------------------------|--------------------|---------------------|
| Halt format blocks | 0 CONFIRMED (no inline `## HALT`/`HALT:` blocks found across `claude/system/*.md`) | `shared_standards.md` §5 | N/A |
| Invariant lists | 0 CONFIRMED (`claude/README.md` §3, `roadmap_prompt.md` §9 both reference `invariants.md`; `team_charter.md` §6 is the charter-level *source* invariants.md is consolidated from, not an engine-prompt duplicate) | `claude/system/invariants.md` | N/A |
| JSON schemas | 0 CONFIRMED duplicates of §16 canonical schemas (spot-checked 3 of 9 files with inline ` ```json ` blocks — `design_gate_prompt.md`, `backlog_management_prompt.md`, `sprint_planning_prompt.md` — all found to be engine-specific state-write examples, not §16 duplicates); 6 files not spot-checked (`amendment_cycle_prompt.md`, `delivery_verification_prompt.md`, `idea_intake_prompt.md`, `post_ship_closure.md`, `roadmap_prompt.md`, `roadmap_management_prompt.md`) | `shared_standards.md` §16 | N/A this run — [ESTIMATED, PARTIAL: 6 files' blocks unverified] |
| Role verify blocks | Not checked this run | shared module | N/A |

**INVOCATION GUARD TABLE:**

| `lessons_learnt_prompt.md` §1 guard type | STRUCTURAL |
| `invocation_context` parameter required? | YES (per §3.7's patch-ID matching requirement observed in live use across v8.7/v8.8/v8.9) |
| Calling engines that pass structured context | Sprint Execution (Phase 3), Delivery Verification (Phase 4), Post-Ship Closure (Amendment/Closure) — all 3 confirmed via live `## Phase 3`/`## Phase 4`/closure sections in this window's `lessons_learnt_cycle.md`/`lessons_learnt_closure.md` files |

**§14 VERSION DRIFT CHECK (v6 — conditional only):** §14 ALIGNED — no drift detected. Conditional check passes. (3-engine spot check in Stage 1 Table 3 all matched; OPERATIONAL_GUIDE.md's own header/§14-self-row/Change-Log-top-row 3-way match confirmed at 4.169/4.169/4.169.)

### Stage 8 — Amendment Cycle Completeness

| Check | Result | Evidence |
|-------|--------|----------|
| A1 — `Amendment_In_Progress` has complete mini state machine | PASS | `amendment_state.json` fields (`status`, `ratification_status`, `ratified_by`, `ratified_at`) written at STEP 0 and updated through STEP 3 (Pending → Ratified/Withdrawn) |
| A2 — First-amendment zero-state handled | PASS | `amendment_cycle_prompt.md` STEP 0 (line 222): "start at `01`; increment if prior sealed/withdrawn amendments exist" — explicit zero-state clause |
| A3 — Withdrawal path defined: state transition + state.json + backlog rollback | PASS (rollback is structural-by-ordering, not an active reversal) | STEP 3.2: rejection sets `amendment_state.json.status = Withdrawn`, `.claude_current_state.json` `active_amendment = null`/`amendment_status = Withdrawn`, and "the original sealed backlog slice remains in effect" — no amended slice is ever produced before STEP 3 ratification, so no active backlog rollback step is needed |
| A4 — Two-authority ratification is mode-independent | PASS | STEP 3.2 Ratification Gate applies uniformly; no `strict`/`standard` branching found in the ratification requirement itself |
| A5 — One-active-amendment rule is a hard gate | PASS | STEP -1 (line 189-190): explicit halt — "only one active amendment per cycle at a time" |
| A6 — Sprint Planning guards `Amendment_In_Progress` state explicitly | PASS | `sprint_planning_prompt.md:56` — named Hard Gate, references `shared_standards.md §5` halt format |
| A7 — `amendment_lessons.md` has defined sunset or optional status | PASS | `amendment_cycle_prompt.md` §8 (line 545): "Deprecation notice (v1.5): deprecated... dropped entirely from v2.0 onward." Current version 1.9 — still required, sunset trigger is version-gated and explicit |

All 7 checks PASS — Amendment Cycle engine is structurally complete.

### Stage 9 — Single Source of Truth

| Check | Result | Duplicate count | Token cost of duplicates | Evidence |
|-------|--------|-------------------|--------------------------------|----------|
| SST1 — Invariant lists: unique canonical source? | PASS | 0 copies | 0 | `invariants.md` is canonical; `README.md` §3 and `roadmap_prompt.md` §9 both reference-only |
| SST2 — Halt format: all engines reference §10/§5 only? | PASS (spot-checked) | 0 inline | 0 | No inline `## HALT` blocks found |
| SST3 — JSON schemas in `shared_standards.md` §16? | PASS (3/9 files spot-checked) | 0 confirmed inline duplicates | 0 confirmed | 6 files' blocks not yet verified — see Stage 7 |
| SST4 — `workforce_capacity.md` has single declared write owner | NOT CHECKED this run | — | — | File not loaded |
| SST5 — `scored_initiatives.md` uses cycle-scoped naming | FAIL (by design, per standing note) | — | — | `claude/scoring/scored_initiatives.md` — deliberate single rolling file; `roadmap_prompt.md` STEP 6 v8.6+ enforces read-before-write + re-read-after-write as compensating control (per AUD-2026-07-27 standing note). Reported FAIL on the literal check per that note's own instruction; not a fresh finding |

### Stage 10 — Known Design Gaps & Deferred Patches

**D1 — PATCH AGE TABLE (window: since AUD-2026-08-12):**

| File | Section | Change | Owner | Target | First recorded | Cycles carried | Status |
|------|---------|--------|-------|--------|--------------------|--------------------|--------|
| `shared_standards.md` | §16.16 (Sandbox Access Constraint) | Canonical disclosure block + 3 stable IDs | Head of Specs Team | next `shared_standards.md` revision | v8.7 Phase 4 | 2 | **RESOLVED** (v3.29, post-ship closure 2026-08-21, `ESC-CLOSE-20260821-02`) |
| `qa_evidence_template.md`/`execution_prompt.md §5.3` | CI-green per-fix restatement | Clarify per-fix not per-EPIC | Head of Specs Team | next revision | v8.7 Phase 4 | 2 | **RESOLVED** (already applied at v8.7, `qa_evidence_template.md` v1.11 — `ESC-CLOSE-20260821-01` investigated 2026-08-21 and found a false positive; `BLG-GOV-312` filed to fix the recurrence-check false-positive root cause itself) |
| `execution_prompt.md` | `test_scenarios` field shape | Prohibit descriptive string, require `[]` | Head of Specs Team | next revision touching `test_scenarios` | v8.8 Phase 4 | 1 | ACTIVE (1 cycle) |
| `execution_prompt.md` | merge_gate/pr_status mid-session staleness | Re-sync on every "PR merged" report, not just session start | Head of Specs Team | next revision | v8.8 Phase 3 | 1 | ACTIVE (1 cycle) |
| `sprint_planning_prompt.md` / `groom backlog` | pre-seal stale-feature scoping check | Grep/status check before pulling item into scope | Head of Specs Team | next revision | v8.7 Phase 3 | 2 | STALE (2 cycles) → auto-generates improvement |
| `execution_prompt.md` STEP 5.1/-1.4 | item-count reconciliation | Compare `sprint_backlog.md` declared total vs `execution_state.json` recorded stories | Head of Specs Team | next revision | v8.9 Phase 3 | 0 (new) | ACTIVE (0 cycles) |
| `execution_state_schema.json`/`execution_prompt.md §3.2.B` | multi-sprint EPIC 2nd-PR convention | Document `additional_prs` shape or EPIC-suffix convention | Head of Specs Team | next revision | v8.9 Phase 3 | 0 (new) | ACTIVE (0 cycles) |
| `execution_prompt.md` STEP 5 | Sprint Close escalation cross-reference | Confirm source backlog item carries cycle+ESC-ID before seal | Head of Specs Team | next revision touching STEP 5 | v8.9 Phase 4 | 0 (new) | ACTIVE (0 cycles) |
| `post_ship_closure.md` STEP 6 | `velocity_metrics.md` header self-consistency | Verify header was actually advanced before chaining new entry | Head of Specs Team | next revision touching STEP 6 | v8.9 closure | 0 (new) | ACTIVE (0 cycles) |
| `backlog_management_prompt.md` | mid-sprint filing field completeness | Require Effort/Provisional-Target at filing time, or health-check flag | Head of Specs Team | next revision | v8.8 closure | 0 (new) | ACTIVE (0 cycles) |
| `roadmap_prompt.md` (STEP -1.5-tracked) | Six-Arc roadmap-model reconciliation | (design-level, tracked separately) | — | next STEP 11.4 meta-review | pre-window | 1+ | ACTIVE — not yet due for re-check |

**1 item is STALE (2 cycles) → auto-generates OBSERVED improvement per D1 rule** (the `sprint_planning_prompt.md`/`groom backlog` pre-seal stale-feature-scoping check, BLG-BE-30 pattern, first flagged v8.7 Phase 3, not yet applied) — see Improvement AUD-2026-08-21-002... actually filed as its own item below (AUD-2026-08-21-011, given the numbering already assigned above to the §14 table gap).

**D2–D5 — DESIGN GAP TABLE:**

| Check | Result | Evidence |
|-------|--------|----------|
| D2 — `ideas_window.json` has `per_agent_submission_count` field | PASS | Confirmed present in schema field list |
| D3 — `rejected_but_strong.md` exists with compliant header | PASS | Owner/Class/Status/Last Updated all present; Last Updated chain = current + 1 prior (within the 3-total retention rule) |
| D4 — Challenger failure has halt/park instruction for Score-4 and Score-5 | NOT CHECKED this run | `roadmap_prompt.md` challenger-scoring section not read |
| D5 — Re-evaluate max age enforced structurally in STEP -1.5 | PASS | Six-Arc reconciliation patch's "1st re-check not OVERDUE" tracking confirms live enforcement |

### Stage 11 — Best Practices Compliance

| Check | Result | Evidence | Dimension |
|-------|--------|----------|-----------|
| BP-01 All engine prompts: Class 6 compliant headers | PASS (spot-checked 4/14) | `amendment_cycle_prompt.md`, `shared_standards.md`, `OPERATIONAL_GUIDE.md`, `execution_prompt.md` all carry Owner/Status/Version/Class 6 header fields | Governance |
| BP-02 Agent roster uses field-level reads | PASS | Stage 3 roster check read Role/Version fields only, not full agent bodies | Token |
| BP-03 `sprint_backlog_index.json` schema in §16 | PASS | `shared_standards.md` §16.1 confirmed present | Token |
| BP-04 `stage4_issue_manifest.json` schema in §16 | PASS | §16.2 confirmed present | Token |
| BP-05 Decision log append-only: STRUCTURAL guard | PASS | §7.1 Structural Append-Verification Procedure is the canonical, reusable mechanism | Reliability |
| BP-06 `run roadmap` supports `--dry-run` | PASS | CLAUDE.md command table + §13 both confirm | Token+Reliability |
| BP-07 `run roadmap` in §13 dry-run table | PASS | Confirmed, row present | Governance |
| BP-08 All engines have zero-state bootstrap | PARTIAL — not exhaustively checked | R5 not swept this run | Reliability |
| BP-09 Displacement rule mode-independent | NOT CHECKED this run | — | Governance |
| BP-10 GitHub sync idempotency active | PASS | STEP 5.0A explicit "idempotent — re-running does not alter already-correct values" | Reliability |
| BP-11 `scored_initiatives` class = Class 4 | PASS | §13 register row confirms Class 4 | Governance |
| BP-12 §13 register covers all known artefacts | **FAIL** — 1 gap | `displacement_debt_register.md` absent (Stage 3 finding) | Governance |
| BP-13 `prompt_change_log` has entry for every engine version | PASS (spot-checked) | 3-engine Stage 1 spot check all matched | Governance |
| BP-14 `lifecycle_schema.json` loaded for transitions | PASS | Loaded full this run, 10 states + transitions confirmed | Reliability |
| BP-15 All prior action-now patches applied | PASS | AUD-2026-08-12's own 5 action-now items (001–005) all confirmed applied per that report's §11 | Reliability |

### Stage 12 — Routine Consolidation Analysis

**TABLE 1 — Consolidation scoring:**

| Engine | C1 | C2 | C3 | C4 | C5 | dry-run? | own state? | multi-caller? | recv overload? | VERDICT |
|--------|----|----|----|----|----|----|----|----|----|--------|
| `manage roadmap` | ✓ | ✓ | ~ | ✓ | x | Yes | No | **Yes** (invoked standalone AND from `run post-ship` STEP 11 per §13) | — | **BOUNDARY** |
| `groom backlog` | ✓ | ✓ | ~ | ✓ | x | Yes | No | **Yes** (standalone AND `run post-ship` STEP 12) | — | **BOUNDARY** |
| `run ideas` | x | ✓ | x | ✓ | x | Yes | No | **Yes** (standalone AND auto-invoked at `run roadmap` STEP -1.6) | — | **BOUNDARY** |
| `run design-gate` | ✓ | x | ✓ | x | x | Yes | **Yes** (`Design_Gate_Passed` is a named `lifecycle_schema.json` state) | Single caller (Release Planning → Design Gate → Sprint Planning) | — | **BOUNDARY** |
| `run delivery verification` | ✓ | x | ✓ | x | x | Yes | **Yes** (`Verified`/`Verified_with_deviations` are named states) | Single caller (Sprint Execution → Delivery Verification → Post-Ship) | — | **BOUNDARY** |

**TABLE 2 — CONSOLIDATE/REVIEW verdicts only:** None — all 5 candidate engines hit at least one KEEP-SEPARATE OVERRIDE (own `lifecycle_schema.json` state entry, or invoked by more than one calling engine).

**TABLE 3 — Known gaps closed by consolidation:** N/A — no consolidation candidates found.

- Recommended consolidation actions in priority order: **none.** All 5 evaluated engines are correctly structured as separate governed routines; the KEEP-SEPARATE OVERRIDE conditions are met cleanly and with direct evidence (§13 dry-run table, `lifecycle_schema.json` states, `prompt_change_log.md` multi-caller citations) for every one of them. This is a stable, evidence-backed conclusion — no action item generated.

---

## 5. Improvements List

### 5a. AUDIT_INDEX

```json
// AUDIT_INDEX
[
  {
    "id": "AUD-2026-08-21-004",
    "title": "Sprint Close item-count reconciliation check",
    "weight": 9,
    "tier": 2,
    "effort": "Medium",
    "patches": 1,
    "files": ["claude/system/execution_prompt.md"],
    "depends_on": []
  },
  {
    "id": "AUD-2026-08-21-010",
    "title": "merge_gate re-sync on every PR merge report",
    "weight": 9,
    "tier": 2,
    "effort": "Medium",
    "patches": 1,
    "files": ["claude/system/execution_prompt.md"],
    "depends_on": []
  },
  {
    "id": "AUD-2026-08-21-011",
    "title": "Pre-seal stale-feature scoping check (STALE, 2 cycles)",
    "weight": 8,
    "tier": 2,
    "effort": "Medium",
    "patches": 1,
    "files": ["claude/system/sprint_planning_prompt.md"],
    "depends_on": []
  },
  {
    "id": "AUD-2026-08-21-002",
    "title": "Preflight Field Scope table missing 4 engines",
    "weight": 6,
    "tier": 1,
    "effort": "Low",
    "patches": 1,
    "files": ["claude/system/shared_standards.md"],
    "depends_on": []
  },
  {
    "id": "AUD-2026-08-21-005",
    "title": "Multi-sprint EPIC second-PR tracking convention",
    "weight": 6,
    "tier": 2,
    "effort": "Medium",
    "patches": 1,
    "files": ["claude/system/execution_prompt.md"],
    "depends_on": []
  },
  {
    "id": "AUD-2026-08-21-006",
    "title": "Sprint Close escalation cross-reference check",
    "weight": 6,
    "tier": 1,
    "effort": "Low",
    "patches": 1,
    "files": ["claude/system/execution_prompt.md"],
    "depends_on": []
  },
  {
    "id": "AUD-2026-08-21-007",
    "title": "velocity_metrics.md header self-consistency check",
    "weight": 6,
    "tier": 1,
    "effort": "Low",
    "patches": 1,
    "files": ["claude/system/post_ship_closure.md"],
    "depends_on": []
  },
  {
    "id": "AUD-2026-08-21-008",
    "title": "Mid-sprint backlog item field completeness",
    "weight": 6,
    "tier": 1,
    "effort": "Low",
    "patches": 1,
    "files": ["claude/system/backlog_management_prompt.md"],
    "depends_on": []
  },
  {
    "id": "AUD-2026-08-21-009",
    "title": "test_scenarios must be array, never a string",
    "weight": 6,
    "tier": 1,
    "effort": "Low",
    "patches": 1,
    "files": ["claude/system/execution_prompt.md"],
    "depends_on": []
  },
  {
    "id": "AUD-2026-08-21-001",
    "title": "OPERATIONAL_GUIDE section order 16-15-14 anomaly",
    "weight": 6,
    "tier": 1,
    "effort": "Low",
    "patches": 0,
    "files": ["claude/system/OPERATIONAL_GUIDE.md"],
    "depends_on": []
  },
  {
    "id": "AUD-2026-08-21-003",
    "title": "displacement_debt_register.md missing from register",
    "weight": 3,
    "tier": 1,
    "effort": "Low",
    "patches": 1,
    "files": ["claude/system/OPERATIONAL_GUIDE.md"],
    "depends_on": []
  }
]
```

### 5b. Individual improvements (weight descending)

---
### AUD-2026-08-21-004
**Title:** Sprint Close item-count reconciliation check (sprint_backlog.md vs execution_state.json)
**Area:** Handoff
**Evidence Classification:** OBSERVED
**Blast Radius:** 3
**Priority Weight:** 9
**Problem:** A Sprint-2/gated story (ST-06) sat completely unbuilt for ~2 days after its gate cleared, with `execution_state.json` recording it nowhere and the sprint looking fully closed (22/22 recorded, all EPICs merged) when 22 of 23 in-scope items were actually done. Nothing cross-references the item count in `sprint_backlog.md` (including gated/Sprint-2 sections) against the count of story entries actually present in `execution_state.json`.
**Evidence:** `claude/cycles/2026-08-17__release-v8.9/lessons_learnt_cycle.md` `## Phase 3`, friction item 1.
**Recommended change:** `claude/system/execution_prompt.md`, STEP 5.1 (Acceptance Summary) — add an item-count reconciliation check before Sprint Close seals.
**Expected benefit:** Catches a gated-story omission automatically at the first `run sprint` re-invocation after the gate clears, rather than requiring manual cross-referencing (this cycle's actual detection method).
**Token impact:** Neutral — one new check paragraph (~6 lines × 8 × ~6 invokes/cycle ≈ 288 tokens/cycle), justified by the correctness gain.
**Implementation effort:** Medium (requires defining the "authoritative total" read rule across gated/multi-sprint sections).
**Dependencies:** None

PATCH:
  operation: INSERT_AFTER
  file: claude/system/execution_prompt.md
  anchor: "### 5.1 Acceptance Summary\n\nFor each ST item: confirm `acceptance_verified = true`. If any are false and the item is `merged`: this is a quality gap — file an escalation."
  content: |

    **Item-count reconciliation check (AUD-2026-08-21-004):** Before proceeding, count the total ST items declared across the full `sprint_backlog.md` (including any gated/Sprint-2 sections), using the Product Owner Sign-Off section's own "Scope confirmed" count as the authoritative total. Compare against the count of story entries actually present in `execution_state.json`. If they do not match: halt and flag Sprint Close — do not write `Sprint_Complete` until every declared item (including gated items not yet unblocked) has a corresponding `execution_state.json` entry or an explicit "not yet unblocked, gated on <ST-xx>" note.

---
### AUD-2026-08-21-010
**Title:** Re-run merge_gate/pr_status sync on every mid-session "PR merged" report
**Area:** Automation
**Evidence Classification:** OBSERVED
**Blast Radius:** 3
**Priority Weight:** 9
**Problem:** `execution_state.json.merge_gate`/per-EPIC `pr_status` went stale on `main` five separate times within one continuous session (v8.8, after each of 5 sequential PR merges), each requiring a manual sync. The existing session-start sync check only fires once, at invocation — nothing re-fires it between merges within the same session.
**Evidence:** `claude/cycles/2026-08-14__release-v8.8/lessons_learnt_cycle.md` `## Phase 3`, friction item 1 (4th consecutive cycle showing this staleness class, but a newly-identified mid-session variant).
**Recommended change:** `claude/system/execution_prompt.md` STEP 8's "next EPIC in queue" flow — re-run the existing LL-v3.9-P3-1 sync check on every "PR merged" report from the user, not only at session start.
**Expected benefit:** Removes the need for manual mid-session syncs across multi-EPIC sprints; closes a 4th-consecutive-cycle-recurring staleness pattern's newly-identified mechanism.
**Token impact:** Saves — avoids N manual ad hoc sync passes per multi-EPIC sprint (variable, session-dependent).
**Implementation effort:** Medium (requires locating STEP 8's "next EPIC" loop and wiring the existing sync check into it).
**Dependencies:** None

PATCH:
  operation: INSERT_AFTER
  file: claude/system/execution_prompt.md
  anchor: "## STEP 6 — Global State Update (Hard Requirement)"
  content: |

    **Mid-session merge_gate re-sync (AUD-2026-08-21-010):** Whenever the user reports a PR merged mid-session (i.e., between processing one EPIC and picking up the next in queue), re-run the LL-v3.9-P3-1 session-start sync check (§ preflight) against `execution_state.json.merge_gate` and the merged EPIC's `pr_status` immediately, before proceeding to the next EPIC — do not wait for the next full session start to catch staleness.

---
### AUD-2026-08-21-011
**Title:** Pre-seal check for stories targeting already-shipped features (STALE, 2 cycles)
**Area:** Lifecycle
**Evidence Classification:** OBSERVED
**Blast Radius:** 3
**Priority Weight:** 8
**Problem:** A story (v8.7 ST-12) was scoped into a sprint even though the feature it targeted had already shipped 4 releases earlier and the underlying question had already been answered with no new schema needed — the story was stale before Sprint Planning sealed it. First flagged v8.7 Phase 3; not yet applied after 2 cycles — crosses the D1 STALE threshold.
**Evidence:** `claude/cycles/2026-08-12__release-v8.7/lessons_learnt_cycle.md` `## Phase 3`, friction item 1 (Type A, deferred); Stage 10 D1 Patch Age Table above.
**Recommended change:** `claude/system/sprint_planning_prompt.md` pre-seal step — add a lightweight check confirming a story's referenced feature/roadmap item isn't already shipped on `main`.
**Expected benefit:** Prevents pulling stale, already-answered stories into sprint scope; closes a now-2-cycle-carried deferred patch before it reaches the 3-cycle OVERDUE band.
**Token impact:** Neutral — one grep/status check added to pre-seal, ~1 invoke/cycle.
**Implementation effort:** Medium (needs a defined "target feature" extraction rule from a story's own text/backlog reference).
**Dependencies:** None

PATCH:
  operation: INSERT_AFTER
  file: claude/system/sprint_planning_prompt.md
  anchor: "### -1.5 Acceptance Criteria Check"
  content: |

    **Pre-seal stale-feature-target check (AUD-2026-08-21-011, D1-tracked since v8.7 Phase 3):** For each story being pulled into scope, if its acceptance criteria or backlog reference names a specific roadmap item/feature as the target of new work, confirm that feature has not already shipped on `main` (grep `claude/backlog/backlog_archive.md` and recent `prompt_change_log.md`/changelog entries for the referenced ID). If already shipped with no remaining gap: flag the story for Product Owner review before scope is sealed rather than sealing it as planned work.

---
### AUD-2026-08-21-002
**Title:** Add 4 missing engines to Preflight Field Scope table
**Area:** Token Efficiency
**Evidence Classification:** OBSERVED
**Blast Radius:** 2
**Priority Weight:** 6
**Problem:** `shared_standards.md` §14 Preflight Field Scope table lists minimum preflight fields for 8 engines but omits `run ideas`, `run ideas housekeeping`, `manage roadmap`, and `groom backlog` — all 4 have a defined `--dry-run` entry in §13 but no equivalent field-level preflight scope entry in §14.
**Evidence:** `shared_standards.md` §14 (lines 454–471); cross-checked against §13's 13-row dry-run table which does cover all 4.
**Recommended change:** Add 4 rows to the §14 table.
**Expected benefit:** Closes a token-efficiency gap — these 4 engines currently have no documented minimum-field preflight scope to point to, risking full-file `.claude_current_state.json` reads by default.
**Token impact:** Saves — full-file read (~30+ fields) vs field-scoped read, ×4 engines × invokes/cycle.
**Implementation effort:** Low.
**Dependencies:** None

PATCH:
  operation: INSERT_AFTER
  file: claude/system/shared_standards.md
  anchor: "| Amendment Cycle (`amend cycle`) | `status`, `active_cycle`, `sprint_sealed` |\n| Roadmap Rebalance (`run roadmap`) | `status`, `active_cycle` |"
  content: |
    | Idea Intake (`run ideas`) | `status`, `active_cycle` |
    | Ideas Housekeeping (`run ideas housekeeping`) | `status`, `active_cycle`, `last_ideas_housekeeping_utc` |
    | Roadmap Management (`manage roadmap`) | `status`, `active_cycle`, `last_manage_roadmap_utc` |
    | Backlog Management (`groom backlog`) | `status`, `active_cycle`, `last_groom_backlog_utc` |

---
### AUD-2026-08-21-005
**Title:** Document convention for a second PR against an already-merged EPIC
**Area:** State
**Evidence Classification:** OBSERVED
**Blast Radius:** 2
**Priority Weight:** 6
**Problem:** When a gated Sprint-2 story's EPIC branch had already merged, an ad hoc `epics.EPIC-02.sprint2` sub-object was invented in-session to track the new PR without overwriting Sprint 1's historical record — reasonable but undocumented, risking a future session overwriting accurate history instead.
**Evidence:** `claude/cycles/2026-08-17__release-v8.9/lessons_learnt_cycle.md` `## Phase 3`, friction item 2.
**Recommended change:** `claude/system/execution_prompt.md` §3.2.B — document a named convention (e.g. `additional_prs: [{label, pr_number, pr_status, status}]`) for this case.
**Expected benefit:** Future multi-sprint EPICs reuse a documented pattern instead of re-inventing one, and cannot accidentally clobber Sprint 1's PR history.
**Token impact:** Neutral.
**Implementation effort:** Medium — requires deciding between the sub-object convention and an EPIC-suffix convention (both viable per the source friction item).
**Dependencies:** None

PATCH:
  operation: INSERT_AFTER
  file: claude/system/execution_prompt.md
  anchor: "Key rule: the sign-off block `Date:` field must be non-blank before the PR can be opened (§3.2.B pre-condition) and before the merge gate runs."
  content: |

    **Multi-sprint EPIC second-PR convention (AUD-2026-08-21-005):** If an EPIC's original PR has already merged and a later gated Sprint-2 (or subsequent) story requires a new PR against the same EPIC, do not overwrite the EPIC's existing `pr_number`/`pr_status` fields in `execution_state.json`. Instead, add a sub-object `epics.<EPIC-xx>.additional_prs: [{label, pr_number, pr_status, status}]` recording the new PR separately, preserving the original Sprint 1 PR record intact.

---
### AUD-2026-08-21-006
**Title:** Require live cycle cross-reference on open escalation's source backlog item before Sprint Close
**Area:** Handoff
**Evidence Classification:** OBSERVED
**Blast Radius:** 2
**Priority Weight:** 6
**Problem:** An open, carried-forward escalation's source backlog item (`BLG-GOV-264`) carried no cross-reference to the current cycle or the live escalation tracking it at the point Sprint Close sealed — caught only downstream at Delivery Verification STEP 4.1, which exists for exactly this purpose but is one step later than necessary.
**Evidence:** `claude/cycles/2026-08-17__release-v8.9/lessons_learnt_cycle.md` `## Phase 4`, friction item 1.
**Recommended change:** `claude/system/execution_prompt.md` STEP 5.3 (Sprint Close Record), "Open escalations" bullet — add the cross-reference check.
**Expected benefit:** Catches the gap one step earlier (Sprint Close instead of Delivery Verification), reducing rework.
**Token impact:** Neutral.
**Implementation effort:** Low.
**Dependencies:** None

PATCH:
  operation: REPLACE
  file: claude/system/execution_prompt.md
  anchor: "- Open escalations (if any)"
  content: |
    - Open escalations (if any). **Backlog cross-reference check (AUD-2026-08-21-006):** for every ST item closing with an open, carried-forward escalation, confirm the escalation's originating backlog item (via its `Source:` field in `sprint_backlog.md`) already references the current `cycle_id` and the escalation ID before this record is sealed — backfill if missing.

---
### AUD-2026-08-21-007
**Title:** Self-consistency check for velocity_metrics.md header before appending
**Area:** Lifecycle
**Evidence Classification:** OBSERVED
**Blast Radius:** 2
**Priority Weight:** 6
**Problem:** `velocity_metrics.md`'s `**Last Updated:**` header was found 2 post-ship closures stale (still citing v8.6 despite the table already holding v8.7/v8.8 rows) — nothing in STEP 6 verifies the header was actually advanced at the prior invocation before trusting it as the base for a new chained entry.
**Evidence:** `claude/cycles/2026-08-17__release-v8.9/lessons_learnt_closure.md` Friction Log, friction item 1.
**Recommended change:** `claude/system/post_ship_closure.md` STEP 6 — add a header-vs-table self-consistency check mirroring `shared_standards.md` §9.1's existing prompt-file check.
**Expected benefit:** Prevents the "Last Updated" audit trail from silently understating how current the document actually is.
**Token impact:** Neutral.
**Implementation effort:** Low.
**Dependencies:** None

PATCH:
  operation: REPLACE
  file: claude/system/post_ship_closure.md
  anchor: "- `claude/cycles/velocity_metrics.md` — append a row for this cycle. Values from `execution_state.json`: Planned = count of ST items at sprint-plan seal; Completed = count of items with `status: done` at post-ship (delegated items that were delivered count as Completed). Update the rolling 6-cycle average. Do not re-derive from cycle artefacts — always write the row here."
  content: |
    - `claude/cycles/velocity_metrics.md` — **before appending (AUD-2026-08-21-007):** confirm the document's own `**Last Updated:**` header was actually advanced at the most recent prior append (compare against the table's own most recent row); if it was not, correct the header honestly first (do not fabricate missing intermediate entries). Then append a row for this cycle. Values from `execution_state.json`: Planned = count of ST items at sprint-plan seal; Completed = count of items with `status: done` at post-ship (delegated items that were delivered count as Completed). Update the rolling 6-cycle average. Do not re-derive from cycle artefacts — always write the row here.

---
### AUD-2026-08-21-008
**Title:** Require Effort/Provisional-Target fields at mid-sprint backlog filing time
**Area:** Prompt
**Evidence Classification:** OBSERVED
**Blast Radius:** 2
**Priority Weight:** 6
**Problem:** 3 of 29 shipped backlog items were missing `**Effort:**`/`**Provisional-Target:**` fields entirely at mark-shipped-complete time — all 3 originated as mid-sprint out-of-scope findings filed directly during execution rather than through the standard backlog-add flow, which does require both fields.
**Evidence:** `claude/cycles/2026-08-14__release-v8.8/lessons_learnt_closure.md` Friction Log, friction item 1.
**Recommended change:** `claude/system/backlog_management_prompt.md` — add a health check flagging any `### BLG-xx` entry missing either field, regardless of filing path.
**Expected benefit:** Catches the gap at the next `groom backlog` pass instead of leaving affected items looking unshipped to the next scheduled rebalance.
**Token impact:** Neutral — one new health-check line, 1 invoke/cycle.
**Implementation effort:** Low.
**Dependencies:** None

PATCH:
  operation: INSERT_AFTER
  file: claude/system/backlog_management_prompt.md
  anchor: "If no items found: note \"Effort Day-Range Validation: PASS — 0 items missing a required day range\" in the health summary. (Added v1.12 — closes the escalated decision from `2026-07-14__release-v7.1` post-ship closure, Release Planning Friction Item 1: bare-letter effort bands on items with a specific `Provisional-Target` forced Release Planning STEP 4.5 to infer day ranges by analogy, right when that cycle's capacity check landed at a WARN threshold with zero buffer.)"
  content: |

    **Field-Completeness Scan (AUD-2026-08-21-008):** Separately, scan `backlog.md` for any `### BLG-xx` entry missing either `**Effort:**` or `**Provisional-Target:**` entirely (not just a bare-letter effort band, the check above) — this occurs most often for items filed directly during sprint execution as mid-sprint out-of-scope findings rather than through the standard `backlog-add` flow. Flag each such item in the health summary as "Field-Completeness Gap" and populate the missing field(s) using the item's `**Source:**` context before the groom run completes.

---
### AUD-2026-08-21-009
**Title:** test_scenarios must always be an array, never a descriptive string
**Area:** Prompt
**Evidence Classification:** OBSERVED
**Blast Radius:** 2
**Priority Weight:** 6
**Problem:** `execution_state.json`'s `test_scenarios` field was represented two different ways across one cycle's two governance-only EPICs — an empty array `[]` for one, a populated array containing one prose string for the other — because current wording only states "if none: set `test_scenarios: []`" without prohibiting a descriptive-string alternative.
**Evidence:** `claude/cycles/2026-08-14__release-v8.8/lessons_learnt_cycle.md` `## Phase 4`, friction item 1; carried 1 cycle, still unapplied at v8.9 per Stage 10 D1.
**Recommended change:** `claude/system/execution_prompt.md` STEP 0 step 6 — state explicitly that manual-review rationale belongs in `qa_evidence_EPIC-xx.md` prose, never in `test_scenarios`.
**Expected benefit:** Keeps the field machine-parseable for any future automation of the STEP 5.1 coverage check.
**Token impact:** Neutral — one clarifying sentence.
**Implementation effort:** Low.
**Dependencies:** None

PATCH:
  operation: REPLACE
  file: claude/system/execution_prompt.md
  anchor: "6. For each EPIC: check `tests/` and `tests/e2e/` for existing runnable test script files that exercise acceptance criteria for this EPIC's stories. Record found paths in `execution_state.json` EPIC `test_scenarios` field. If none: set `test_scenarios: []`. **Advisory (BLG-GOV-136):** `docs/testing/` paths are QA evidence artefacts (scenario description documents), not runnable test files — do not record `docs/testing/` paths in `test_scenarios`."
  content: |
    6. For each EPIC: check `tests/` and `tests/e2e/` for existing runnable test script files that exercise acceptance criteria for this EPIC's stories. Record found paths in `execution_state.json` EPIC `test_scenarios` field. If none: set `test_scenarios: []` — **always a bare empty array, never a descriptive string** (AUD-2026-08-21-009). Any manual-review rationale (e.g. "no application test suite affected — governance-only change") belongs in the `qa_evidence_EPIC-xx.md` "Test scenarios used" prose field instead, never smuggled into this JSON array. **Advisory (BLG-GOV-136):** `docs/testing/` paths are QA evidence artefacts (scenario description documents), not runnable test files — do not record `docs/testing/` paths in `test_scenarios`.

---
### AUD-2026-08-21-001
**Title:** Reorder OPERATIONAL_GUIDE.md §14/§15/§16 into ascending physical sequence
**Area:** Prompt
**Evidence Classification:** OBSERVED
**Blast Radius:** 2
**Priority Weight:** 6
**Problem:** `## 16. Artefact Lifecycle Model` (line 1359) physically precedes `## 15. Governance Health Score` (line 1377), which physically precedes `## 14. Playbook Governance` (line 1452) — a reader following the document top-to-bottom hits descending, not ascending, section numbers at the end of the file.
**Evidence:** `claude/system/OPERATIONAL_GUIDE.md` lines 1359, 1377, 1452 (direct read).
**Recommended change:** Reorder the three physical blocks to §14 → §15 → §16 (numbers unchanged, so no cross-reference elsewhere in the codebase needs updating — this is a pure physical reordering).
**Expected benefit:** Restores linear readability; removes a confusing pattern for any future reader or automated section-parser that assumes ascending order.
**Token impact:** Neutral (reordering only, no content change).
**Implementation effort:** Low — verify no content depends on relative position (none found; all 3 sections are self-contained) before moving.
**Dependencies:** None

**Manual reorder required — no mechanical PATCH block.** A simple anchor/REPLACE cannot safely relocate a ~135-line section block without risking duplication or truncation. Apply by hand: cut the `## 14. Playbook Governance` block (lines 1452 to the start of `### Change Log`) and the `## 15. Governance Health Score` block (lines 1377–1451) and reinsert both, in that order, immediately before the current `## 16. Artefact Lifecycle Model` heading (line 1359) — leaving `## 16.`'s own content and the trailing `### Change Log` section exactly where they are relative to `## 14.`/`## 15.`'s new position. Verify with `grep -n "^## 1[4-6]\."` afterward that the three headings now appear in ascending line-order.

PATCH:
  operation: CREATE_FILE
  file: N/A — manual reorder, no automatable anchor (see instructions above)
  anchor: N/A
  content: |
    N/A

---
### AUD-2026-08-21-003
**Title:** Add displacement_debt_register.md to OPERATIONAL_GUIDE §13 Artefact Register
**Area:** Governance
**Evidence Classification:** OBSERVED
**Blast Radius:** 1
**Priority Weight:** 3
**Problem:** `claude/roadmap/displacement_debt_register.md` is wired into `roadmap_prompt.md` STEP 8 (create-if-absent, since v9.16/v8.9 ST-21) and tracked live via an open, non-blocking escalation (`ESC-EXEC-20260818-02`), but has no row in the §13 Artefact Register even as a pending artefact.
**Evidence:** `claude/system/OPERATIONAL_GUIDE.md` §13 (lines 1266–1359, 0 matches for "displacement"); `claude/system/roadmap_prompt.md` line 606.
**Recommended change:** Add one row to §13.
**Expected benefit:** Closes a real (if minor) register-completeness gap before the file is actually created at the next `run roadmap`/`manage roadmap` invocation.
**Token impact:** Neutral.
**Implementation effort:** Low.
**Dependencies:** None

PATCH:
  operation: INSERT_AFTER
  file: claude/system/OPERATIONAL_GUIDE.md
  anchor: "| Amendment Lessons | `claude/cycles/<id>/amendments/<AMD-id>/amendment_lessons.md` | 3 | PMO Lead | Amendment |"
  content: |
    | Displacement Debt Register | `claude/roadmap/displacement_debt_register.md` | 4 | Head of Specs Team | 1 |

---

## 6. Cross-Improvement Map

- **No hard dependencies between any of the 11 improvements** — each targets a distinct engine section and can be applied independently.
- **Same-file application-order note (not a dependency, an operational caveat):** AUD-2026-08-21-004, -006, -009, and -010 all touch `execution_prompt.md` at 4 distinct, non-overlapping anchors (STEP 5.1, STEP 5.3's "Open escalations" line, STEP 0 step 6, and the STEP 6 heading respectively). No content conflict exists between them, but if applying all 4 by hand in one pass, apply in **descending line-number order** (STEP 6 heading first, then STEP 5.3, then STEP 5.1, then STEP 0) so that an earlier insertion doesn't shift the line numbers an anchor lower in the file depends on being found at.
- **AUD-2026-08-21-001** (manual reorder) should be applied **before** any other `OPERATIONAL_GUIDE.md` edit in the same session (AUD-2026-08-21-003 also touches this file, at §13, well before §14/§15/§16) — apply -003 first (simple INSERT_AFTER, unaffected by the later reorder), then -001 (manual reorder) last, to avoid the reorder shifting -003's own anchor line before -003 is applied.
- No conflicts identified between any pair of improvements.

---

## 7. Implementation Tiers

**Tier 1 (Low effort, no dependencies):**
- AUD-2026-08-21-002 — Preflight Field Scope table (weight 6)
- AUD-2026-08-21-006 — Sprint Close escalation cross-reference (weight 6)
- AUD-2026-08-21-007 — velocity_metrics.md header self-consistency (weight 6)
- AUD-2026-08-21-008 — Mid-sprint backlog field completeness (weight 6)
- AUD-2026-08-21-009 — test_scenarios array-only (weight 6)
- AUD-2026-08-21-001 — OPERATIONAL_GUIDE section reorder (weight 6, manual)
- AUD-2026-08-21-003 — Displacement Debt Register §13 row (weight 3)

**Tier 2 (Medium effort, no dependencies):**
- AUD-2026-08-21-004 — Item-count reconciliation check (weight 9)
- AUD-2026-08-21-010 — merge_gate mid-session re-sync (weight 9)
- AUD-2026-08-21-011 — Pre-seal stale-feature scoping check (weight 8, STALE/D1-escalated)
- AUD-2026-08-21-005 — Multi-sprint EPIC second-PR convention (weight 6)

**Tier 3 (High effort or complex dependency chain):** None this run.

---

## 8. Audit Summary

Overall health held steady at 71 (prior 74), staying well clear of the 65 GOVERNANCE_HOLD threshold, with Friction Load genuinely improving on both the raw score and the normalised per-cycle rate for the first time in two consecutive audits' comparisons. Two friction items that crossed the 2-cycle automatic-escalation threshold (CI-green restatement clarification, Sandbox Access Constraint disclosure) were correctly escalated per §6.4 and both resolved in the same post-ship closure session that immediately preceded this audit, leaving 0 STALE/OVERDUE deferred patches carried into this window's own deduction. The 11 improvements filed this run are dominated by real, evidence-backed process gaps surfaced organically during v8.7–v8.9 (a near-miss on an unbuilt gated story, a governance-artefact registration gap, and a preflight-scope documentation gap) rather than newly-invented ones — none require new files or multi-engine coordination, so Tier 3 is empty this run.

---

## SLA

- Cadence: every 3 cycles
- OBSERVED + Blast Radius ≥ 3, open after 2 audit cycles → P0 escalation to Head of Specs Team
- Overall score < 65 → GOVERNANCE HOLD: no new cycles until resolved
- Output filed as: `claude/cycles/<cycle_id>/audit_report_AUD-<date>.md` (Class 3)
- The audit report must be committed in the same session it is produced — do not defer the commit to a later session (BLG-GOV-169). Confirmed committed this session (see below).
- The §11 CONFIG UPDATE block this run produces is applied to `claude/audit.py`'s own CONFIG constants in the same commit as the filed report — not deferred.
- In the same commit, `.claude_current_state.json`'s `last_audit_id`, `last_audit_utc`, `last_audit_overall_score`, `last_audit_open_items`, and `last_audit_cycle_count` are updated to this run's own values.

---

## 10. Scorecard Appendix

**TOKEN_EFFICIENCY: 84** (prior 100, −16 — 1 NEWLY CONFIRMED gap this window)
- 4 engines (`run ideas`, `run ideas housekeeping`, `manage roadmap`, `groom backlog`) confirmed absent from `shared_standards.md` §14 Preflight Field Scope table (lines 454–471) — all 4 are present in §13's dry-run table, so this is specifically a §14 gap, not a general documentation absence. × −4 = −16.
- 0 confirmed inline schema/invariant/halt-format blocks this window (3/9 candidate files spot-checked for JSON blocks, all found to be legitimate engine-specific examples, not §16 duplicates; 6 files unverified — flagged, not scored).
- 0 engines absent from §13 dry-run table (13/13 confirmed present via direct read).
- Confidence: HIGH for the −16 delta (direct table read); the unverified 6-file JSON-block sweep is a coverage gap, not an estimated deduction.

**GOVERNANCE_INTEGRITY: 74** (prior 80, −6 — 1 NEWLY CONFIRMED gap this window)
- `claude/roadmap/displacement_debt_register.md` confirmed absent from `OPERATIONAL_GUIDE.md` §13 Artefact Register (0 matches in a direct grep of the register's table content) × −6 = −6.
- 0 newly confirmed advisory-only guards needing to become hard gates.
- 0 authority roles with no confirmed charter file (23/23 confirmed, full 1:1 match against `team_charter.md` §3.1–§3.3).
- 0 §14 version entries diverging from actual file version (3/3 spot-checked engines matched, plus OPERATIONAL_GUIDE's own 3-way self-consistency check).
- Confidence: HIGH.

**EXECUTION_RELIABILITY: 53** (prior 53, no change)
- 0 newly confirmed halt paths with no recovery instruction (general Blocked-state and Amendment-rejection recovery paths both re-confirmed structurally sound this window, R2/A3).
- 0 newly confirmed ASSERTION-only writes (3 write ops spot-checked, all STRUCTURAL).
- 0 newly confirmed missing zero-state bootstrap paths (not swept this window).
- 0 newly confirmed deferred patches carried 2+ cycles unresolved in this dimension's own tracking (the 2 that crossed the threshold this window are scored under FRICTION_LOAD's fresh computation instead, and both resolved same-session at closure regardless).
- Confidence: HIGH for "0 new deltas confirmed"; the 53-point baseline itself (R3/R5 full sweep) is carried forward without full re-derivation this run either, consistent with the treatment at AUD-2026-08-08 and AUD-2026-08-12.

**FRICTION_LOAD: 44** (100 − 24 − 15 − 12 − 5; window-scoped fresh computation, not incremental)
(Window: 3 cycle-records since PRIOR_AUDIT_ID — v8.7, v8.8, v8.9.)
- Type A × 6 (v8.7 Phase3 stale-ST-12 item; v8.7 closure DEV-drift item; v8.8 closure field-completeness item; v8.9 Phase3 item-count-reconciliation item; v8.9 Phase3 multi-sprint-PR item; v8.9 closure velocity_metrics-header item) × −4 = −24
- Type C × 5 (v8.7 Phase3 Playwright-sandbox item; v8.8 Phase3 merge_gate-staleness item; v8.9 Phase4 BLG-GOV-264-cross-ref item; v8.9 closure split-achievability-carve-out item; +1 further Type C row per Stage 2 Pattern Table) × −3 = −15
- Friction item confirmed recurring across 2+ cycles: 2 (CI-green restatement, v8.7→v8.8→v8.9, escalated + resolved 2026-08-21; Sandbox Access Constraint, same pattern, escalated + resolved 2026-08-21) × −6 = −12
- Deferred patch confirmed unresolved since PRIOR_AUDIT_ID: 1 (Six-Arc roadmap-model reconciliation — still ACTIVE, tracked via STEP -1.5's own re-check mechanism, not yet due; the 2 lessons_learnt-tracked patches that reached 2-cycle STALE status this window were both resolved same-session at the 2026-08-21 post-ship closure, before this audit ran, so are not counted as unresolved-at-audit-time) × −5 = −5
- Confidence: HIGH — all counted rows individually cited in Stage 2. Both the raw score (37→44, ▲) and the normalised rate (7.5→5.67 items/cycle-record, ▼/improving) agree this window — unlike AUD-2026-08-12, where the two signals disagreed.

**DOCUMENT_HYGIENE: 100** (prior 100, no change)
- 0 confirmed non-compliant headers, 0 wrong document class declarations, 0 confirmed broken path references, 0 non-standard agent role headers this window.
- **Flagged, not scored:** `OPERATIONAL_GUIDE.md`'s §16→§15→§14 physical section-order anomaly (Stage 1, Improvement AUD-2026-08-21-001) does not match any of the 4 DOCUMENT_HYGIENE deduction lines' literal wording (not a header-compliance, class-declaration, path, or agent-format issue) — filed as an Improvement instead of a scored deduction, per the CONFIRMED COUNTS RULE. Flagged here for the next audit's own baseline read, in case a future formula revision adds a "section sequence" line.
- Confidence: HIGH.

**Overall = (84 + 74 + 53 + 44 + 100) / 5 = 355 / 5 = 71.0 → 71**

---

## 11. Config Update

```python
# === PASTE INTO audit.py CONFIG AFTER THIS RUN ===
PRIOR_AUDIT_ID = "AUD-2026-08-21"
PRIOR_AUDIT_OPEN_ITEMS = [
    "AUD-2026-08-21-004", "AUD-2026-08-21-010", "AUD-2026-08-21-011",
    "AUD-2026-08-21-002", "AUD-2026-08-21-005", "AUD-2026-08-21-006",
    "AUD-2026-08-21-007", "AUD-2026-08-21-008", "AUD-2026-08-21-009",
    "AUD-2026-08-21-001", "AUD-2026-08-21-003",
]  # all 11 improvements open at session end — none applied this session (report-only run; no explicit "action all audit points" direction given)
PRIOR_SCORES = {
    "token_efficiency":      84,
    "governance_integrity":  74,
    "execution_reliability": 53,
    "friction_load":         44,
    "document_hygiene":      100,
}
COMPLETED_CYCLES = 76  # current completed_cycle_count at AUD-2026-08-21
# === END PASTE ===
```

*(Post-publication update: all 11 improvements above — AUD-2026-08-21-001 through -011 — were applied post-publication, same day, per explicit user direction ("action the 11 improvements"). `claude/audit.py`'s `PRIOR_AUDIT_OPEN_ITEMS` has been updated to `[]` to reflect this; `.claude_current_state.json.last_audit_open_items` corrected to 0. Files touched: `execution_prompt.md` v3.69→v3.70 (5 patches: -004, -005, -006, -009, -010), `sprint_planning_prompt.md` v3.16→v3.17 (-011), `shared_standards.md` v3.29→v3.30 (-002), `post_ship_closure.md` v2.29→v2.30 (-007), `backlog_management_prompt.md` v1.14→v1.15 (-008), `OPERATIONAL_GUIDE.md` v4.169→v4.170 (-001 manual reorder, -003 register row, plus the §14 table updates for the 5 files above). All 6 changed governance prompts' Change Log companions and `claude/system/prompt_change_log.md` updated in the same pass. Shown here per the mandatory §11 output format.)*
