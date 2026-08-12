Owner: Head of Specs Team
Class: Governance Record (Class 3)
Status: Active
Last Updated: 2026-08-12
Cycle: 2026-08-11__release-v8.6

# Claude Lifecycle Audit — AUD-2026-08-12

**Scope:** `claude/` | **Audit version:** 6 | **Completed cycles:** 73 (71 at last audit — 2 cycles this window: v8.5, v8.6)

No staleness this run — `claude/audit.py`'s CONFIG constants at session start (`PRIOR_AUDIT_ID = "AUD-2026-08-08"`, `COMPLETED_CYCLES = 71`) matched the most recently filed report (`claude/cycles/2026-08-07__release-v8.4/audit_report_AUD-2026-08-08.md` §11) exactly. The AUD-2026-08-08-001/AUD-2026-08-08-004 self-update fixes held for this run.

---

## 1. Resolved Since Last Audit

| AUD-ID | Title (3 words) | Status | Evidence ref |
|--------|------------------|--------|----------------|
| AUD-2026-08-08-001 | Audit config self-update | **RESOLVED** | Confirmed above — `audit.py` CONFIG matched the true last-filed report exactly at this run's start. |
| AUD-2026-08-08-002 | OPERATIONAL_GUIDE self-header drift | **RESOLVED** | Applied same-session at AUD-2026-08-08; no recurrence — self-header (`4.156`) matches Change Log top row (`4.156`) and §14 rows this run (Stage 1 Table 3, full 19/19 sweep). |
| AUD-2026-08-08-003 | open_escalations state-pointer sync | **RESOLVED** | `post_ship_closure.md` v2.24→v2.25 text confirmed present (line 110, current v2.26). Untested end-to-end this window — no `closure_escalations.md` was raised in either v8.5 or v8.6 (only `execution_escalations.md`, a different pre-existing mechanism, raised 2 items in v8.6, both same-day Resolved) — so the writer exists and is correct by inspection but has not yet fired live. Noted as LATENT-confirmed, not OBSERVED-confirmed. |
| AUD-2026-08-08-004 | audit.py never wrote last_audit_* | **RESOLVED** | `.claude_current_state.json` carried correct AUD-2026-08-08 values (score 71, cycle count 71, 0 open items) into this session — confirmed stale-free at read time, now updated to this run's own values. |

4 of 4 RESOLVED, 0 PARTIAL/OPEN. Clean baseline — first fully-clean carry-forward in the audit history reviewed this session.

---

## 2. Health Scorecard

SYSTEM HEALTH — 2026-08-12  |  Prior: 2026-08-08

| Dimension | Score | Bar (▓=10pts) | Trend | Confidence |
|-----------|-------|----------------|-------|------------|
| Token Efficiency | 100 | ▓▓▓▓▓▓▓▓▓▓ | ─ | HIGH |
| Governance Integrity | 80 | ▓▓▓▓▓▓▓▓░░ | ─ | HIGH |
| Execution Reliability | 53 | ▓▓▓▓▓░░░░░ | ─ | HIGH |
| Friction Load | 37 | ▓▓▓▓░░░░░░ | ▲ (raw score) / ▼ (normalised rate — see Stage 2) | HIGH |
| Document Hygiene | 100 | ▓▓▓▓▓▓▓▓▓▓ | ▲ | HIGH |
| **Overall** | **74** | ▓▓▓▓▓▓▓░░░ | ▲ (71→74) | — |

Overall 74 ≥ 65 — no GOVERNANCE HOLD triggered.

**Read the Friction Load trend carefully (see Improvement AUD-2026-08-12-002):** the raw score rose 25→37, but this window spans only 2 cycles (v8.5, v8.6) against the prior window's 4 (v8.1-v8.4) — normalised per-cycle-record, the friction rate actually rose 4.75→7.5 items/cycle-record. The raw score improving while the underlying rate worsens is a genuine artefact of the window-scoped-not-normalised formula, not a sign things are getting better. Full detail in Stage 2 and Improvement 002.

---

## 3. Gap Register

| Stage | File | Status | Impact (5 words) | → Improvement? |
|-------|------|--------|--------------------|------------------|
| Phase 1 | `claude/agents/` | Loaded (23/23 files, unchanged) | None — full roster confirmed | No |
| Stage 5 | `roadmap_management_prompt.md`, `backlog_management_prompt.md`, `ideas_housekeeping_prompt.md`, `idea_intake_prompt.md`, `design_gate_prompt.md`, `sprint_planning_prompt.md`, `amendment_cycle_prompt.md` | Version-checked only, not full-content re-derived (no `prompt_change_log.md` entry touched any of these this window) | Not deep-audited this run | No — carried, no drift signal |
| Stage 6 | Producer/consumer field contracts | Spot-checked only | Not exhaustively re-derived | No — `sprint_sealed` handoff (the one field this window's changes touched) empirically confirmed working (v8.6 Sprint Planning proceeded correctly from a freshly-reset `sprint_sealed: false`) |
| Stage 8 | `amendment_cycle_prompt.md` | Loaded (version only) | No amendment invoked v8.5-v8.6 | No — unchanged since AUD-2026-08-08 |
| — | `claude/backlog/backlog.md` §5/§7/§8 headers | **Missing** — `## 5.`/`## 7.`/`## 8.` type-section headers not found; only `## 1.`, `## 2.`, `## 3.`, `## 4.`, `## 6.` exist. Recent QA/Spec/Gov/Ops items are landing inside dated "Roadmap Rebalance ... New Items" ephemeral sections instead of their type sections. | Yes | **Yes — AUD-2026-08-12-003** |

No file was entirely unloadable this run.

---

## 4. Stage Findings

### Stage 1 — Lifecycle Mapping

**TABLE 1 — Command path check (13/13 rows):** all resolve, no broken references, unchanged from AUD-2026-08-08 except version bumps below.

**TABLE 3 — §14 version spot check (full 19-row sweep):**

| Engine | §14 version | Actual file `**Version:**` | Match? |
|--------|--------------|-------------------------------|--------|
| Idea Intake | 2.8 | 2.8 | ✅ |
| Roadmap Management | 1.4 | 1.4 | ✅ |
| Backlog Management | 1.13 | 1.13 | ✅ |
| Design Gate | 1.9 | 1.9 | ✅ |
| Roadmap Engine | 9.14 | 9.14 | ✅ |
| Release Engine | 2.49 | 2.49 | ✅ |
| Sprint Planning | 3.16 | 3.16 | ✅ |
| Amendment Cycle | 1.9 | 1.9 | ✅ |
| Execution Engine | 3.67 | 3.67 | ✅ |
| QA Evidence Template | 1.9 | 1.9 | ✅ |
| Verification Engine | 3.8 | 3.8 | ✅ |
| Ideas Housekeeping | 1.2 | 1.2 | ✅ |
| Post-Ship Closure | 2.26 | 2.26 | ✅ |
| Shared Standards | 3.28 | 3.28 | ✅ |
| Governance Invariants | 1.0 | 1.0 | ✅ |
| Lessons Learnt Prompt | 1.10 | 1.10 | ✅ |
| GitHub Issue Template | 1.0 | 1.0 | ✅ |
| Document Lifecycle Guide | 2.7 | 2.7 | ✅ |
| Team Charter | 1.7 | 1.7 | ✅ |

**19/19 match — including OPERATIONAL_GUIDE.md's own self-header this time** (`| Version | 4.156 |` at line 1458 vs. Change Log top row `4.156` at line 1499 — both independently confirmed). This is the first audit in the 3 reviewed this session to find **zero** version-bookkeeping drift anywhere — a direct result of `execution_prompt.md` v3.66→v3.67's new mandatory `governance-drift` skill Step 1b invocation (see Stage 7), which self-caught and fixed the one drift instance that occurred inside this very window (§14 self-row stale at `4.152` on 2026-08-10, corrected to `4.155` on 2026-08-12 before this audit even ran).

**FINDINGS:**
- No broken path in CLAUDE.md command table.
- No engine in OPERATIONAL_GUIDE §4 missing from README (`run audit` present in both).
- 0 version-bookkeeping drift, 0 self-header drift — clean sweep.

### Stage 2 — Behavioural Audit

**COMPLIANCE TABLE (2 cycles: v8.5, v8.6):**

| Cycle | B2 LL filed | B4 Hard gate | B7 No 2nd carry |
|-------|--------------|---------------|-------------------|
| v8.5 | ✅ (`lessons_learnt_cycle.md` + `_closure.md`) | NO GATES FIRED — compliant | Partial — 2 items carried into a 2nd cycle unresolved (see below) |
| v8.6 | ✅ | NO GATES FIRED — compliant | Partial — same 2 items still open at end of window; 1 further item (script fix) hit its 3rd carry and was escalated + resolved by filing (Improvement 001) |

B4 rule: COMPLETED_CYCLES (73) ≥ 3, no `Blocked` transitions found in either cycle's records this window → **NO GATES FIRED — compliant**, both cycles.

**PATTERN TABLE (Type, confirmed via `**Classification:**`/`type` column, `lessons_learnt_cycle.md` + `lessons_learnt_closure.md` Friction Log, both cycles):**

| Friction Type | Count (window) | Recurring? |
|---------------|-------------------|------------|
| Type A (Governance Drift) | 5 | Yes — the §14 self-consistency gap (2 cycles, now RESOLVED) |
| Type B (Semantic Mismatch) | 1 | No |
| Type C (Dependency Stall) | 5 | Yes — the script substring-match fix (3 cycles, ACTIVE/OVERDUE) |
| Type D | 3 | No |
| Type E (Authority Gap) | 1 | Yes — same script-fix item, also classified Type E in v8.6's own closure record (dual-tagged: dependency stall + authority-gap-in-the-carry-mechanism) |
| **Total** | **15** | — |

**Confirmed recurring patterns (2+ cycles):**
1. `OPERATIONAL_GUIDE.md` §14 self-consistency check had no mandatory invocation point — v8.5 (Phase 3, deferred) → v8.6 (Phase 3, action-now recurrence-escalation per §3.7) — **RESOLVED at v8.6**: `execution_prompt.md` §3.2.A now mandatorily invokes the `governance-drift` skill's Step 1b check; applying it live immediately self-caught and fixed a real drift instance. The system's own recurrence-escalation mechanism worked exactly as designed.
2. DoQ sign-off CI-green restatement requirement — v8.5 (Phase 4, deferred) → v8.6 (Phase 4, 2nd carry-forward, deferred again). **Not yet escalated** — below the 3-consecutive auto-escalation threshold, still ACTIVE.
3. `scripts/check_api_performance_baseline_drift.py` substring-match false negatives — v8.4 (closure) → v8.5 (closure, Recurrence Yes) → v8.6 (closure, 3rd consecutive carry). This run additionally found the deferred-patch mechanism's own assumption ("the next Post-Ship Closure can apply this directly") is **false** for script-level fixes — `post_ship_closure.md §5`'s write scope covers only governance/planning documents and templates/prompts, not `scripts/*.py`. **RESOLVED this session via Improvement AUD-2026-08-12-001** — filed `BLG-OPS-142` directly with the closure's own prototyped-heuristic content, rather than allowing a 4th indefinite carry.

**New, non-recurring findings this window worth noting:** a 3-occurrence-in-1-sprint pattern where a story's first-pass completeness/verification claim was factually wrong, caught only by a second independently-requested review pass (v8.6 Phase 3, ST-03/EPIC-02, ST-11+ST-12/EPIC-04, ST-24/EPIC-06 — the ST-12 case is material: an agent-mediated sign-off's own "I re-verified X, it's conservative" claim was itself unsubstantiated, and a real cost-basis-drift bug shipped undetected until the second pass). Flagged by the routine itself as warranting deliberate design work, correctly not rushed into a same-session edit. Tracked in Stage 10 D1, not separately re-derived here.

**TREND LINE:** Friction items per cycle-record: [v8.5: 5, v8.6: 10]. Total 15 across 2 records = **7.5/record**, up sharply from **4.75/record** at AUD-2026-08-08's window (19/4). State as: **INCREASING** (3rd consecutive audit to report this trend increasing: 3.2 → 4.75 → 7.5). See Improvement AUD-2026-08-12-002 for the companion finding that the Friction_Load *score* nonetheless rose this run (25→37) because the window itself was shorter — the two signals point in opposite directions and both need to be read together.

Both B2 and B4 are at 100% compliance. B7 shows partial compliance (2-3 items genuinely carrying 2+ cycles) but 2 of the 3 recurring patterns were resolved via the system's own designed mechanisms (recurrence-escalation, this audit's own direct fix) within this window — the mechanism is working, not silently failing.

### Stage 3 — Governance Integrity

**TABLE 1 — Agent roster:** 23/23 files, unchanged since AUD-2026-08-08. 0 non-compliant.

**TABLE 2 — Governance checks:**

| Check | Result | Evidence |
|-------|--------|-----------|
| G1 — All charter roles have agent file | PASS | Unchanged, 23/23 |
| G2 — Agent lifecycle refs point to canonical path | PASS | No broken references found in sampled files |
| G3 — Artefact class declarations match lifecycle guide §3 | PASS | Unchanged |
| G4 — §13 register covers scoring + ideas + lessons + closure escalation artefacts | PASS | Unchanged since AUD-2026-08-08 |
| G5 — Design gate bypass authority in charter (not prose-only) | PASS | Unchanged |

### Stage 4 — Lifecycle Reliability

| Check | Result | Evidence |
|-------|--------|-----------|
| R1 — All lifecycle states have valid entry AND exit transitions | PASS [carried] | Unchanged |
| R2 — All hard gate halt paths have defined recovery instruction | ~PASS [ESTIMATED, carried] | `shared_standards.md` §10.4 |
| R3 — Idempotency classification | See sub-table | |
| R4 — Re-evaluate max age rule exists in STEP -1.5 | PASS [carried] | Unchanged |
| R5 — All engines have zero-state bootstrap path | ~PASS [ESTIMATED, carried] | |
| R6 — Concurrent write prevention referenced at state-write step | PASS [carried] | Unchanged |

**R3 SUB-TABLE:**

| Write operation | File | Guard type | Engine |
|-------------------|------|------------|--------|
| `.claude_current_state.json.open_escalations` write | global | **STRUCTURAL (confirmed present, unexercised)** — `post_ship_closure.md:110`, the AUD-2026-08-08-003 fix. Readers: `release_planning_prompt.md`, `sprint_planning_prompt.md`, `roadmap_prompt.md`. No `closure_escalations.md` entry was raised in v8.5 or v8.6 to exercise the write path live. | — |
| `execution_state.json.open_escalations` write | per-cycle | STRUCTURAL — unchanged | Sprint Execution |
| `scored_initiatives.md` overwrite | `claude/scoring/` | STRUCTURAL — unchanged | Roadmap Rebalance |

The R3 ABSENT finding carried across AUD-2026-08-03 and AUD-2026-08-08 is now closed — upgraded from ABSENT to STRUCTURAL, though still not live-exercised.

### Stage 5 — Token Budget Analysis

| Engine | Lines | ~Tokens | Confidence | Δ since AUD-2026-08-08 |
|--------|-------|---------|------------|---------------------------|
| roadmap_prompt.md | 891 | ~7,128 | HIGH (`wc -l` this run) | +2 (v9.14) |
| release_planning_prompt.md | 1,141 | ~9,128 | HIGH | +3 (v2.49) |
| sprint_planning_prompt.md | 654 | ~5,232 | HIGH | 0 (unchanged) |
| execution_prompt.md | 1,128 | ~9,024 | HIGH | +2 (v3.67) |
| delivery_verification_prompt.md | 652 | ~5,216 | HIGH | +2 (v3.8) |
| post_ship_closure.md | 784 | ~6,272 | HIGH | +3 (v2.26) |
| shared_standards.md | 1,094 | ~8,752 | HIGH | +30 (v3.26→3.28, 2 bumps — §20 dependency-scan cadence, §16.15 deviations_filed) |
| lessons_learnt_prompt.md | 506 | ~4,048 | HIGH | unchanged |
| amendment_cycle_prompt.md | 630 | ~5,040 | HIGH | unchanged |

**METHODOLOGY FOOTNOTE (mandatory):**
⚠ This table does not capture in-run context accumulation. For `execution_prompt.md`, actual per-invocation cost grows with sprint size. Reported cost may understate actual by 30–50% on large sprints. Use as lower bound.

**RANKED SAVINGS TABLE:** No new confirmed inline-schema/invariant/halt-format extraction opportunities this run.

**DEAD LOAD CHECK:** No new dead-load findings this run.

**DRY-RUN GAP:** Not exhaustively re-verified; no `prompt_change_log.md` entry this window removed or added a `--dry-run` flag.

**CYCLE TOTAL:** ~59,840 tokens/typical cycle for the 9 core engine prompts (+336 since AUD-2026-08-08, driven almost entirely by `shared_standards.md`).

### Stage 6 — Engine Handoff Integrity

| Pair | Field/Section | Match? |
|------|----------------|--------|
| Release Planning → Sprint Planning | `backlog_slice_path`, `next_release`, `sprint_sealed` | ✅ — `sprint_sealed` reset-on-publish fix (v2.49) empirically confirmed working: v8.6 opened with `sprint_sealed: false` and reached a clean seal without the stale-carryover symptom observed at v8.4's design gate |
| Sprint Execution → Delivery Verification | `execution_state.json sealed` | ✅ (carried) |
| Delivery Verification → Post-Ship Closure | `verification_report.md` DoQ + PO sign-off | ✅ (carried) |
| Roadmap Rebalance → Release Planning | `next_release` | ✅ (carried) |
| Amendment Cycle → Sprint Planning | `amendment_status`, `sprint_sealed` | ✅ (no amendment invoked this window either) |

No CONSUMER READS UNGUARANTEED FIELD / DEAD OUTPUT / SCHEMA VERSION MISMATCH newly confirmed. New field semantics documented this window (`execution_state.json.deviations_filed` — `shared_standards.md` §16.15, ST-24) close a prior ambiguity rather than create a new gap.

### Stage 7 — Prompt Architecture & Compression

**COMPLEXITY TABLE:** Unchanged flags — `roadmap_prompt.md`, `release_planning_prompt.md`, `execution_prompt.md` (>500 lines, pre-existing), `shared_standards.md` (reference document, expected).

**EXTRACTION TABLE:** No new inline schema/invariant/halt-format blocks confirmed this run.

**INVOCATION GUARD TABLE:** Unchanged — `lessons_learnt_prompt.md` §1 guard remains STRUCTURAL.

**§14 VERSION DRIFT CHECK (conditional):** **ALIGNED — no drift detected. Conditional check passes**, including the self-header row this time (Stage 1). This is the direct, immediate payoff of `execution_prompt.md` v3.67's new mandatory Step 1b invocation — worth noting since the check caught a real drift instance (the same session it was added) before this audit ever ran, rather than this audit being the one to catch it.

### Stage 8 — Amendment Cycle Completeness

Unchanged since AUD-2026-08-08 — `amendment_cycle_prompt.md` remains v1.9; `active_amendment` empty throughout v8.5-v8.6. A1-A7: PASS (carried).

### Stage 9 — Single Source of Truth

| Check | Result | Evidence |
|-------|--------|-----------|
| SST1 — Invariant lists: unique canonical source? | PASS | Unchanged |
| SST2 — Halt format: all engines reference §10 only? | PASS [not re-derived exhaustively] | |
| SST3 — JSON schemas in shared_standards §16? | PASS | New §16.15 added this window (`deviations_filed` semantics) — correctly placed in the canonical location, not duplicated inline elsewhere |
| SST4 — workforce_capacity.md single write owner | PASS | Unchanged |
| SST5 — scored_initiatives cycle-scoped naming | **FAIL (by design, compensating control)** | Unchanged — not a fresh finding |

### Stage 10 — Known Design Gaps & Deferred Patches

**D1 — PATCH AGE TABLE:**

| File | Section | Change | Owner | First recorded | Cycles carried | Status |
|------|---------|--------|-------|--------------------|-------------------|--------|
| `claude/roadmap/current_roadmap.md` §2a-§2c | Six-Arc model vs. backlog-driven reconciliation | Head of Specs Team assessment | Head of Specs Team | 2026-07-28__scheduled | 1st re-check performed 2026-08-11__scheduled, confirmed **not OVERDUE** | **ACTIVE**, tracked correctly — no longer aging unchecked |
| `scripts/check_api_performance_baseline_drift.py` `find_missing_endpoints()` | substring-match false negative | Infrastructure & Operations Owner | v8.4 closure | 3 (v8.4→v8.5→v8.6) | **RESOLVED this session** — `BLG-OPS-142` filed (Improvement AUD-2026-08-12-001), closing the indefinite-carry loop `BLG-OPS-135` alone could not close (that item tracks the 1 known symptom endpoint, not the script fix itself, and remains separately open) |
| `execution_prompt.md §5.3` / `qa_evidence_template.md` | DoQ sign-off CI-green restatement | Head of Specs Team | v8.5 closure | 2 (v8.5→v8.6) | **ACTIVE** |
| `lessons_learnt_prompt.md §3.7` | recurrence-check should match by patch-ID tag, not date/filename | Head of Specs Team | v8.6 closure | 0 (**NEW**) | **NEW** — root-caused a real false-positive recurrence claim this window (v8.5's closure incorrectly claimed `LL-v8.4-P4-01` was "still unapplied" when it had genuinely shipped 2 days earlier) |
| `execution_prompt.md §3.2.A` | `test_scenarios` roll-up backstop should re-trigger on post-seal `spec_references` edits | Head of Specs Team | v8.6 closure | 0 (**NEW**) | **NEW** |
| `execution_prompt.md §5.3` | mandatory 2nd review pass for quantitative "already verified" claims | Head of Specs Team | v8.6 closure | 0 (**NEW**) | **NEW** — see Stage 2 |
| `claude/backlog/backlog.md` §5/§7/§8 | ephemeral "New Items" sections never promoted to type sections | Head of Specs Team / PMO Lead | 2026-07-24__scheduled (oldest) | 4+ groom backlog runs since (v8.3-v8.6 closures) without promotion | **NEW — AUD-2026-08-12-003** |

Frontend-testing-gate environment-parity sub-clause (carried ACTIVE since v8.3, "unexercised" at AUD-2026-08-08) — **RESOLVED/CONFIRMED WORKING**: EPIC-01's v8.6 QA evidence log explicitly applied it correctly (Playwright scenarios disclosed as not-locally-executed per the sub-clause, real CI deferred to, no interaction-timing AC affected).

**D2-D5 — DESIGN GAP TABLE:** All PASS, unchanged since AUD-2026-08-08.

### Stage 11 — Best Practices Compliance

| Check | Result | Dimension |
|-------|--------|-----------|
| BP-01 Class 6 compliant headers | PASS | Governance |
| BP-02 Agent roster field-level reads | PASS | Token |
| BP-03/04 schema §16 checks | PASS [carried] | Token |
| BP-05 Decision log append-only STRUCTURAL guard | PASS [carried] | Reliability |
| BP-06/07 `run roadmap --dry-run`, §13 table | PASS [carried] | Token+Reliability |
| BP-08 All engines have zero-state bootstrap | ~PASS [ESTIMATED, carried] | Reliability |
| BP-09 Displacement rule mode-independent | PASS [carried] | Governance |
| BP-10 GitHub sync idempotency active | PASS [carried] | Reliability |
| BP-11 scored_initiatives class = Class 4 | PASS [carried] | Governance |
| BP-12 §13 register covers all known artefacts | PASS [carried] | Governance |
| BP-13 prompt_change_log has entry for every engine version | PASS | Governance — full window sweep, 0 gaps, 0 self-drift |
| BP-14 lifecycle_schema.json loaded for transitions | PASS [carried] | Reliability |
| BP-15 All prior action-now patches applied | **4/4** — see §1, clean sweep | Reliability |

### Stage 12 — Routine Consolidation Analysis

Unchanged since AUD-2026-08-08 — no new governed routine added this window, no `--dry-run`/own-state/multi-caller property changed for any of the 6 evaluated engines.

| Engine | VERDICT (carried) |
|--------|---------|
| manage roadmap | ALREADY CONSOLIDATED |
| groom backlog | ALREADY CONSOLIDATED |
| run ideas housekeeping | ALREADY CONSOLIDATED |
| run ideas | ALREADY CONSOLIDATED |
| run design-gate | BOUNDARY |
| run delivery verification | BOUNDARY |

No recommended consolidation actions this run.

---

## 5. Improvements List

### 5a. AUDIT_INDEX

```json
// AUDIT_INDEX
[
  {
    "id": "AUD-2026-08-12-001",
    "title": "Script fix carried 3 cycles, closure write-scope cannot resolve it",
    "weight": 15,
    "tier": 1,
    "effort": "Low",
    "patches": 1,
    "files": ["claude/backlog/backlog.md"],
    "depends_on": [],
    "status": "APPLIED — this session (BLG-OPS-142 filed)"
  },
  {
    "id": "AUD-2026-08-12-002",
    "title": "Friction_Load raw score can rise while per-cycle rate worsens",
    "weight": 6,
    "tier": 1,
    "effort": "Low",
    "patches": 1,
    "files": ["claude/audit.py"],
    "depends_on": [],
    "status": "APPLIED — this session"
  },
  {
    "id": "AUD-2026-08-12-003",
    "title": "4 ephemeral backlog sections never promoted despite groom backlog runs",
    "weight": 8,
    "tier": 2,
    "effort": "Medium",
    "patches": 1,
    "files": ["claude/system/backlog_management_prompt.md"],
    "depends_on": [],
    "status": "OPEN — deferred, recommend applying at next backlog_management_prompt.md revision"
  }
]
```

### 5b. Individual improvements

### AUD-2026-08-12-001 — APPLIED THIS SESSION
**Title:** `scripts/check_api_performance_baseline_drift.py` substring-match fix carried 3 consecutive closures with no venue able to apply it
**Area:** Automation | Governance
**Evidence Classification:** OBSERVED
**Blast Radius:** 3
**Priority Weight:** 15
**Problem:** The script's `find_missing_endpoints()` false-negative fix was carried forward at `v8.4`, `v8.5`, and `v8.6` closures on the assumption that "the next Post-Ship Closure" was the correct venue to apply it directly. `v8.6`'s own closure checked that assumption against `post_ship_closure.md §5`'s write scope and found it false — a bare `scripts/*.py` file is neither a governance/planning document nor a template/prompt file. The closure's own Outstanding Action #1 directed the PMO Lead to file a `BLG-OPS-*` story "before next groom backlog or run roadmap session" — but `groom backlog` ran later in that same session (2026-08-12T14:30Z, after the closure's 14:15Z) without the item being filed, so the deadline was already missed by the time this audit started.
**Evidence:** `claude/cycles/2026-08-11__release-v8.6/lessons_learnt_closure.md` Friction Item 2; `claude/cycles/2026-08-11__release-v8.6/closure_record.md` §6 Outstanding Action #1; `.claude_current_state.json.last_groom_backlog_utc: "2026-08-12T14:30:00Z"` vs. `last_post_ship_utc: "2026-08-12T14:15:00Z"`; grep of `claude/backlog/backlog.md` for "substring"/"find_missing_endpoints" returned 0 hits pre-fix.
**Recommended change:** File the backlog item directly with the closure's own already-prototyped acceptance criteria, rather than let a governance-process deadline miss compound into a 4th indefinite carry.
**Expected benefit:** Closes a 3-cycle recurring reliability gap and the process-mechanism gap it exposed (the deferred-patch carry-forward mechanism cannot resolve fixes outside its own write scope, and had no fallback when that happened).
**Token impact:** Neutral.
**Implementation effort:** Low (single backlog entry, standard `backlog-add` skill flow).
**Dependencies:** None
**Status:** Applied this session — `BLG-OPS-142` filed in `claude/backlog/backlog.md` §6 Operations & Infrastructure Backlog, with the closure's own acceptance-criteria content (table-row/heading-context requirement, `KNOWN_GAPS` grandfathering). Header `**Last Updated:**` field updated per §16.14 retention rule (oldest of the existing 3 chained entries dropped to keep the cap at 3).

PATCH: (applied — shown for the record)
  operation: INSERT_AFTER
  file: claude/backlog/backlog.md
  anchor: "### BLG-OPS-141 — Staging environment data-reset cadence review"
  content: |
    (New item BLG-OPS-142 inserted after this item's closing `---` — see backlog.md for full text. Full acceptance criteria and Source line as filed.)

---

### AUD-2026-08-12-002 — APPLIED THIS SESSION
**Title:** Friction_Load's window-scoped-not-normalised formula lets the raw score improve while the underlying per-cycle rate worsens
**Area:** Token Efficiency | Governance | Automation
**Evidence Classification:** OBSERVED
**Blast Radius:** 2
**Priority Weight:** 6
**Problem:** `audit.py`'s FRICTION_LOAD formula computes a raw window-scoped total (not normalised by the number of cycle-records in the window). This run's window (2 cycles) scored 37 vs. the prior window's (4 cycles) 25 — an apparent improvement — while the Stage 2 per-cycle-record rate actually *worsened*, 4.75→7.5 items/cycle-record, because this window simply had fewer cycles to accumulate deductions across. A reader trusting the raw score trend alone would draw the wrong conclusion.
**Evidence:** This run's own Stage 2/Scorecard Appendix arithmetic — Friction_Load raw 25→37 (▲) vs. items/cycle-record 4.75→7.5 (▲, i.e. worse) computed from the same underlying friction counts.
**Recommended change:** Document that the raw score and the per-cycle-record rate must both be reported and compared to their own prior values, since they can disagree.
**Expected benefit:** Prevents a future audit (or reader) from reading "Friction Load improved" as good news when the underlying trend is worsening, purely because of window-length variance.
**Token impact:** Neutral (+9 lines to `audit.py`'s own prompt text, amortised across every future `run audit` invocation only — not a per-cycle engine cost).
**Implementation effort:** Low
**Dependencies:** None
**Status:** Applied this session — `claude/audit.py`'s FRICTION_LOAD formula block gains a "NORMALISED RATE NOTE."

PATCH: (applied — shown for the record)
  operation: INSERT_AFTER
  file: claude/audit.py
  anchor: "  -5 per deferred patch confirmed unresolved since PRIOR_AUDIT_ID (cite patch)\n"
  content: |
    NORMALISED RATE NOTE (added AUD-2026-08-12-002): report items-per-cycle-record alongside the raw
    score every run, and compare it to the prior audit's own reported rate.

---

### AUD-2026-08-12-003 — OPEN, not applied this session
**Title:** 4 ephemeral "New Items" backlog sections never promoted to their type sections despite multiple `groom backlog` runs since
**Area:** Document Hygiene | Automation
**Evidence Classification:** OBSERVED
**Blast Radius:** 3
**Priority Weight:** 8
**Problem:** `claude/backlog/backlog.md`'s own Placement Rule states ephemeral "New Items" sections (added by roadmap-rebalance idea-intake disposition) "must be removed during the next `groom backlog` run after the cycle closes," with open items promoted to their §1-§8 type section first. Four such sections exist, dated `2026-07-24__scheduled`, `2026-07-27__scheduled`, `2026-07-28__scheduled`, and `2026-08-11__scheduled` — the first three predate at least 4 subsequent `groom backlog` runs (v8.3, v8.4, v8.5, v8.6 closures), none of which promoted or removed them. A structural symptom of the same gap: `## 5.`, `## 7.`, and `## 8.` top-level type-section headers (QA, Spec Debt, Governance) do not exist in the file at all — recent items of those types (e.g. `BLG-QA-147`, `BLG-SPEC-128`, `BLG-GOV-299`) are landing inside the dated ephemeral sections instead, not under a proper type heading.
**Evidence:** `grep -n "^## " claude/backlog/backlog.md` — only `## 1.`-`## 4.` and `## 6.` present; ephemeral sections at lines 4772, 4850, 4854, 4898, 5001 (this run's line numbers); Placement Rule text at file top; `.claude_current_state.json.last_groom_backlog_utc` history shows grooms at v8.3 through v8.6 with no mention of ephemeral-section promotion in any recorded outcome string.
**Recommended change:** `backlog_management_prompt.md` (groom backlog engine) should gain an explicit check: any "New Items" ephemeral section older than the current cycle must have its still-open items promoted into the correct `## 1.`-`## 8.` type section (creating `## 5.`/`## 7.`/`## 8.` headers if genuinely absent) before the section itself is removed, rather than leaving it to accumulate indefinitely.
**Expected benefit:** Restores the backlog's own documented type-based organisation; prevents indefinite accumulation of undated-lookup-cost ephemeral sections; closes a real gap between the file's own stated Placement Rule and its actual structure.
**Token impact:** Neutral to slightly positive (a flat type-organised file is cheaper to grep/scan than nested dated sections).
**Implementation effort:** Medium — requires a full-file section audit and safe mass-promotion of potentially dozens of items across 4 sections, plus the standard `backlog_management_prompt.md` edit-checklist (version bump, OPERATIONAL_GUIDE §14, changelog, `prompt_change_log.md`). Out of scope for `audit.py` to apply directly — this is a `groom backlog` (Head of Specs Team) task, not an audit-tooling task.
**Dependencies:** None
**Status:** Not applied this session — flagged for the next `groom backlog` or `backlog_management_prompt.md` revision. Carries forward as this run's one open item (see §11 Config Update).

PATCH: (not applied — recommendation only)
  operation: INSERT_AFTER
  file: claude/system/backlog_management_prompt.md
  anchor: "(insert after the step that currently removes ephemeral Release Slice / Test Scenario Gap sections — exact anchor to be located by the implementing session)"
  content: |
    Ephemeral "New Items" sections (added by roadmap-rebalance idea-intake disposition) older than the
    current cycle: promote every still-open item to its correct `## 1.`-`## 8.` type section (creating
    the section heading if genuinely absent) before removing the ephemeral section itself. Do not leave
    a dated ephemeral section in place past the `groom backlog` run that immediately follows the cycle
    in which it was created.

---

## 6. Cross-Improvement Map

No dependencies between the 3 improvements. 001 and 002 are both APPLIED (independent files, independent fixes). 003 is OPEN and independent of both — it targets `backlog_management_prompt.md`, not touched by 001's `backlog.md` content edit or 002's `audit.py` edit. No conflicts.

## 7. Implementation Tiers

**Tier 1 (Low effort, no dependencies):** 001 (APPLIED), 002 (APPLIED).
**Tier 2 (Medium effort, no dependencies):** 003 (OPEN — recommend for next `groom backlog`/`backlog_management_prompt.md` session).
**Tier 3:** None this run.

## 8. Audit Summary

All 4 of AUD-2026-08-08's own improvements held clean into this session — the first fully-clean carry-forward across the 3 audits reviewed. This window's own 2 new improvements (the missed-deadline `BLG-OPS-142` filing and a Friction_Load methodology clarification) were both applied same-session; 1 further finding (4 ephemeral backlog sections never promoted) is genuinely out of `audit.py`'s own scope and carries forward as this run's sole open item. Overall health is **74/100** (up from 71), driven by Document Hygiene fully restoring to 100 (0 version-bookkeeping drift anywhere this run — a direct, immediate payoff of `execution_prompt.md` v3.67's new mandatory `governance-drift` skill invocation, which self-caught and fixed the one drift instance that occurred inside this very window before this audit ever ran) and Friction Load's raw score improving to 37 — though that improvement is an artefact of a shorter window, not genuine progress: the underlying per-cycle friction rate continued climbing for a 3rd consecutive audit (3.2→4.75→7.5 items/cycle-record), and 2 of this window's 3 confirmed 2+-cycle recurring patterns needed active intervention (1 resolved by the system's own recurrence-escalation design, 1 resolved directly by this audit) to avoid becoming a 4th consecutive carry-forward. The next audit's baseline should start from a genuinely clean governance-bookkeeping state (0 open drift items) but should watch the DoQ CI-green restatement item (now 2 cycles carried) for a 3rd-cycle auto-escalation, and should confirm `BLG-OPS-142` was picked up by a sprint rather than itself beginning a new multi-cycle carry pattern.

## 9. SLA

- Cadence: every 3 cycles
- OBSERVED + Blast Radius ≥ 3, open after 2 audit cycles → P0 escalation to Head of Specs Team
- Overall score < 65 → GOVERNANCE HOLD: no new cycles until resolved
- Output filed as: `claude/cycles/2026-08-11__release-v8.6/audit_report_AUD-2026-08-12.md` (Class 3)
- Committed in this same session per BLG-GOV-169.
- `claude/audit.py` CONFIG constants and `.claude_current_state.json.last_audit_*` fields both updated in this same session/commit per the standing AUD-2026-08-08-001/004 rules — no staleness carried forward.

**Watch item for next audit:** AUD-2026-08-12-003 (ephemeral backlog sections) — OBSERVED, Blast Radius 3 — if still open at the next audit (2 audit cycles from first flagging), escalates to P0 per the SLA rule above.

---

## 10. Scorecard Appendix

**TOKEN_EFFICIENCY: 100** (prior 100, no change)
- 0 confirmed inline schema/invariant/halt-format blocks, 0 engines missing field-level preflight, 0 absent from §13 dry-run table.
- Confidence: HIGH

**GOVERNANCE_INTEGRITY: 80** (prior 80, no change)
- 0 newly confirmed advisory-only guards needing to become hard gates this window (the one prior candidate, `open_escalations`, was already fixed at AUD-2026-08-08 and is not re-scored here without a clearer historical linkage to the exact deduction — see note below).
- 0 authority roles with no confirmed charter file (23/23).
- 0 artefacts newly absent from §13 register.
- 0 §14 version entries diverging from actual file version (19/19 match, including self-header).
- **Note (transparency, not a deduction):** the `open_escalations` writer fix (Stage 4) plausibly warrants a restoration credit here per the prior audit's own forward guidance ("expect ... the advisory-only-guard deduction class to no longer apply to open_escalations"), but this run could not confirm the exact historical deduction amount tied to that specific check with enough precision to apply a numeric restoration without guessing — left flat and flagged rather than estimated.
- Confidence: HIGH

**EXECUTION_RELIABILITY: 53** (prior 53, no net change)
- Deferred patch carried 2+ cycles unresolved: 1 NEWLY CONFIRMED at higher severity (script substring-match fix, now 3 cycles + confirmed structurally unresolvable by the existing mechanism) × −5 = −5
- **Restoration:** Frontend-testing-gate environment-parity sub-clause (−5, baked into the 53 baseline since AUD-2026-08-08) is now RESOLVED — confirmed correctly exercised at v8.6 (EPIC-01 QA evidence) → +5
- 0 newly confirmed halt paths with no recovery instruction, 0 newly confirmed ASSERTION-only writes, 0 newly confirmed missing zero-state bootstrap.
- Confidence: HIGH for the two window deltas; R2/R5 baseline carried forward without full re-derivation

**FRICTION_LOAD: 37** (100 − 20 − 15 − 18 − 10; window-scoped fresh computation per methodology, not incremental from baseline)
(Window: 2 cycle-records since PRIOR_AUDIT_ID — v8.5, v8.6.)
- Type A × 5 (v8.5 Phase3 §14-invocation-gap item; v8.6 Phase3 action-now item; v8.6 closure Friction Item 1 TSG-stale-entries; v8.6 closure Friction Item 3 recurrence-check-accuracy item) × −4 = −20
- Type C × 5 (v8.5 Phase3 session-boundary item; v8.5 Phase4 test_scenarios-recurrence item; v8.5 closure script-substring item; v8.6 Phase3 workflow-dispatch item; v8.6 Phase4 DEV-Resolved-carve-out item) × −3 = −15
- Friction item confirmed recurring across 2+ cycles: 3 (§14 self-consistency gap, v8.5→v8.6, resolved v8.6; DoQ CI-green restatement, v8.5→v8.6, still active; script substring-match fix, v8.4→v8.5→v8.6, resolved this session) × −6 = −18
- Deferred patch confirmed unresolved since PRIOR_AUDIT_ID: 2 (Six-Arc roadmap-model reconciliation, still ACTIVE though re-checked; script substring-match fix, ACTIVE at session start though resolved by this audit's own Improvement 001 — scored as found, per standard methodology of scoring the state found not the state after same-session remediation) × −5 = −10
- Confidence: HIGH — all counted rows individually cited above (Stage 2). See Improvement AUD-2026-08-12-002 for the companion normalised-rate reading, which is worse (▼) even though this raw score is better (▲).

**DOCUMENT_HYGIENE: 100** (prior 96, +4 — restoration)
- 0 confirmed non-compliant headers this window (0 self-header drift, 0 §14 mismatches — full clean sweep, Stage 1).
- **Restoration:** the AUD-2026-08-08 `OPERATIONAL_GUIDE.md` self-header drift (−4, scored pre-fix per standard methodology at that audit) was fixed same-session there and independently reconfirmed still-consistent by this run's own fresh 19-row sweep → +4.
- 0 wrong document class declarations, 0 confirmed broken path references, 0 non-standard agent role headers.
- Confidence: HIGH

**Overall = (100 + 80 + 53 + 37 + 100) / 5 = 370 / 5 = 74.0 → 74**

---

## 11. Config Update

```python
# === PASTE INTO audit.py CONFIG AFTER THIS RUN ===
PRIOR_AUDIT_ID = "AUD-2026-08-12"
PRIOR_AUDIT_OPEN_ITEMS = ["AUD-2026-08-12-003"]
  # 001 and 002 applied within this session. 003 (4 ephemeral backlog sections never promoted) is a
  # groom-backlog-scoped fix, deferred — not applied by audit.py itself. 1 item open at session end.
PRIOR_SCORES = {
    "token_efficiency":      100,
    "governance_integrity":  80,
    "execution_reliability": 53,
    "friction_load":         37,
    "document_hygiene":      100,
}

# Completed cycle count — increment after each post-ship closure
# Used to determine B4 history sufficiency (need ≥3 cycles for hard gate compliance)
COMPLETED_CYCLES = 73  # current completed_cycle_count at AUD-2026-08-12
# === END PASTE ===
```

*(Already applied to `claude/audit.py` and `.claude_current_state.json` in this same session — shown here per the mandatory §11 output format.)*
