**Owner:** Head of Specs Team
**Status:** Active
**Class:** 3 — Operational Record
**Version:** AUD-2026-07-01
**Last Updated:** 2026-07-01

# Claude Lifecycle Audit — AUD-2026-07-01

Scope: `claude/` | Audit engine version: 6 | Completed cycles at run time: 49 | Cycles since prior audit: 3 (v6.1, v6.2, v6.3)

---

## 1. Resolved Since Last Audit

`PRIOR_AUDIT_OPEN_ITEMS` in `claude/audit.py` = `[]` (comment: "All AUD-2026-06-22 Tier 1 items applied same commit; 0 open items").

Per Phase 0 rule: **First-audit-style output applies — no open items to trace.**

| AUD-ID | Title | Status | Evidence ref |
|---|---|---|---|
| — | — | No prior open items | `claude/audit.py` line 28 |

**Data-integrity note (feeds AUD-2026-07-01-013 below):** `.claude_current_state.json` field `last_audit_open_items` reads `10`, contradicting `audit.py`'s `PRIOR_AUDIT_OPEN_ITEMS = []` (0) for the same `last_audit_id: "AUD-2026-06-22"`. One of the two sources is stale.

**Prompt changes applied since 2026-06-22** (from `claude/system/prompt_change_log.md`, 21 entries dated 2026-06-22 through 2026-06-26): all AUD-2026-06-22 Tier-2 and latent-improvement patches (execution_prompt.md v3.45→v3.47, delivery_verification_prompt.md v3.0→v3.1, post_ship_closure.md v2.14→v2.15) confirmed applied same day. v6.1/v6.2/v6.3 design-gate and ST patches also confirmed applied. No carry-forward gap in the prompt log itself.

**Carry-forward deferred items across the 3 cycles this audit spans:**

| Item | First recorded | Status at this audit |
|---|---|---|
| BLG-GOV-135 / BLG-GOV-136 | v6.1 | RESOLVED — `prompt_change_log.md` line 478, applied v6.2 (execution_prompt.md v3.47→v3.48) |
| FI-P3-01 (Playwright strict-mode) | v6.2 | RESOLVED in practice — v6.3 lessons_learnt_cycle.md line 58 confirms no recurrence |
| FI-P3-02 (staging-only AC protocol ambiguity) | v6.2 | **STALE — 2 cycles, still unresolved** (see AUD-2026-07-01-007) |
| FI-P4-01 / DF-10 (`spec_references=[]` CI/infra convention) | v6.2 | **STALE — 2 cycles, escalation-flagged for v6.4** (see AUD-2026-07-01-004) |
| DF-01–DF-06 (v6.3 atomic-write / sign-off items) | v6.3 | ACTIVE (1 cycle) — not yet due for audit action |

---

## 2. Health Scorecard

SYSTEM HEALTH — 2026-07-01 | Prior: 2026-06-22

| Dimension | Score | Bar (▓=10pts) | Trend | Confidence |
|---|---|---|---|---|
| Token Efficiency | 92 | ▓▓▓▓▓▓▓▓▓░ | ▼ (95→92) | LOW |
| Governance Integrity | 84 | ▓▓▓▓▓▓▓▓░░ | ▲ (78→84) | HIGH |
| Execution Reliability | 48 | ▓▓▓▓▓░░░░░ | ▼ (79→48) | HIGH |
| Friction Load | 64 | ▓▓▓▓▓▓░░░░ | ▲ (0→64, methodology caveat — see appendix) | HIGH |
| Document Hygiene | 80 | ▓▓▓▓▓▓▓▓░░ | ▲ (70→80) | HIGH |
| **Overall** | **74** | ▓▓▓▓▓▓▓░░░ | ▲ (64→74) | — |

Overall ≥ 65 — no Governance Hold triggered. **Execution Reliability (48) is the weakest dimension and the primary audit finding this cycle** — driven by newly-confirmed ASSERTION-only idempotency guards across 7 write operations (full arithmetic in §10 Scorecard Appendix). Note: recomputing the prior audit's per-dimension average (95+78+79+0+70)/5 = 64.4 suggests the *previous* audit cycle may itself have been below the 65 Governance Hold threshold — not something this audit can resolve retroactively, flagged for Head of Specs Team awareness only.

---

## 3. Gap Register

| Stage | File | Status | Impact (5 words) | → Improvement? |
|---|---|---|---|---|
| Phase 2 | `claude/agents/` | OK | 23 files, 1:1 role match | No |
| Phase 2 | `claude/system/lifecycle_schema.json` | OK | Full schema loaded cleanly | No |
| Phase 2 | `claude/ideas/rejected_but_strong.md` | OK | Compliant Class 4 header | No |
| Phase 2 | `claude/scoring/` | OK | 2 files, 1 stale dated snapshot | Yes — AUD-014 |
| Phase 2 | `OPERATIONAL_GUIDE.md` §13 | OK | ~70 rows, broad coverage | No |
| Phase 2 | `CLAUDE.md` | PARTIAL | No document header block itself | No — CLAUDE.md is the anchor file, not a Class 6 prompt; not scored |
| Phase 2 | `.claude_current_state.json` | OK | Status=Closed, consistent | Yes — AUD-013 (separate field) |

No files were unloadable this run. All substantive gaps are version/documentation drift, captured as improvements in §5, not missing files.

---

## 4. Stage Findings

### Stage 1 — Lifecycle Mapping

TABLE 1 — Command path check: **All 13 rows (12 governed prompts + `claude/audit.py`) confirmed present on disk. PASS, no broken paths.**

TABLE 2 — Engine documentation coverage:

| Engine | OPERATIONAL_GUIDE §4? | README §4? | Gap |
|---|---|---|---|
| Roadmap Rebalance | Yes | Yes (§4.1) | none |
| Release Planning, Sprint Planning, Sprint Execution, Delivery Verification, Post-Ship Closure, Amendment Cycle, Design Gate, Idea Intake, Roadmap Mgmt, Backlog Mgmt, Ideas Housekeeping, **Lifecycle Audit** | Yes (OPERATIONAL_GUIDE §4/§14) | **No** | `claude/README.md` §4 documents only 1 of 13 governed routines |

TABLE 3 — §14 version spot check (full 14-row sweep, not just 3 — drift was found, triggering the mandatory full report):

| Engine | §14 version | Actual file version | Match? |
|---|---|---|---|
| Idea Intake / Roadmap Mgmt / Backlog Mgmt / Design Gate / Release / Sprint Planning / Amendment / Execution / Verification / Ideas Housekeeping / Post-Ship / Shared Standards / Lessons Learnt | (13 rows) | (13 rows) | ✓ all match |
| **Roadmap Rebalance Prompt** | **v7.5** | **v7.6** (confirmed `roadmap_prompt.md` line 3) | **✗ MISMATCH — see AUD-003** |

FINDINGS:
- No broken CLAUDE.md command paths; `run audit` **is** present in the §1 table.
- `claude/README.md` §4 coverage gap affects 12 of 13 engines — see AUD-006.
- CLAUDE.md has no "Last Updated" field (not required by its own convention — it is the anchor document, not a Class 6 prompt).
- `claude/README.md`'s own header: `Last Updated: 2026-03-22` — 101 days stale vs. the most recent engine bump (2026-06-24). See AUD-010.

### Stage 2 — Behavioural Audit

`run_manifest.md` and `lessons_learnt*.md` present in 86/86 cycle folders.

B4 (`COMPLETED_CYCLES=46` at audit-config time, ≥3): **NO GATES FIRED — compliant**, based on `open_escalations: {}` in `.claude_current_state.json` and no `Blocked` status found at any checked point. **This is a spot-check, not an exhaustive per-cycle hard-gate history read across all 86 cycles — flagged PARTIAL confidence on completeness, not on the conclusion itself.**

PATTERN TABLE — friction since prior audit (v6.2 + v6.3 only; all-time totals are far larger and not the scoring basis — see §10 appendix methodology note):

| Friction Type | Count (since prior audit) | Top source | Recurring? |
|---|---|---|---|
| Type A | 2 | `lessons_learnt_cycle.md` — sign-off format issue | Yes — root cause persists since delivery_verification_prompt.md v3.0 |
| Type B | 2 | `lessons_learnt_cycle.md` | No |
| Type C | 2 | `lessons_learnt_cycle.md` — sprint-close batch correction, downstream of Type A | No new recurrence flagged this window |
| Type D | 3 | `lessons_learnt_cycle.md` — `spec_references=[]` convention | Yes — 2 cycles (v6.2→v6.3), escalation-flagged |
| Type E | 0 | — | — |

TREND LINE (last 8 release cycles, friction rows per cycle): `v5.8:3, v5.9:2, v6.0:7, v5.1:8, v6.1:3, v6.2:3, v6.3:6`. State: **FLAT** (volatile, no sustained monotonic direction).

### Stage 3 — Governance Integrity

TABLE 1 — Agent roster: 23/23 files use `**Role:**` format (COMPLIANT). Version field present in 6/23 (1 non-bolded — `pmo_lead.md`, see AUD-015). Canonical activation-trigger reference present in only 2/23 (`facilitator.md`, `challenger.md`) — **not a scored deduction** (Class 5 header spec in `document_lifecycle_guide.md` §Class 5 does not require an activation-trigger field), but flagged as a design gap worth considering for a future Class 5 header revision.

TABLE 2 — Governance checks:

| Check | Result | Evidence |
|---|---|---|
| G1 — All charter roles have agent file | **PASS** | 23 charter roles ↔ 23 agent files, 1:1 |
| G2 — Agent lifecycle refs point to canonical path | **FAIL (partial, unscored)** | 21/23 agent files have no activation-trigger reference; not a documented Class 5 requirement, so not deducted |
| G3 — Artefact class declarations match lifecycle guide §3 | **PASS** (sampled) | e.g. `rejected_but_strong.md` Class 4, `roadmap_prompt.md` Class 6 |
| G4 — §13 register covers scoring + ideas + lessons artefacts | **PASS** | `OPERATIONAL_GUIDE.md` §13 rows confirmed for all three families |
| G5 — Design gate bypass authority in charter (not prose-only) | **FAIL** | 0 hits for "bypass" in `claude/charter/*.md`; only defined in `sprint_planning_prompt.md` line 174 — see AUD-005 |

**Self-corrected finding (from evidence-gathering pass):** the evidence agent's Stage 4 sub-table initially classified `decision_log.md` append-only as ASSERTION-only, citing `shared_standards.md` §7 alone. Direct verification of `roadmap_prompt.md` STEP 9 ("**Decision log append-only enforcement (structural)**: Before writing: count existing entries (N). After writing: re-read; confirm count = N + entries added this run... Both checks must pass before STEP 9 commit") shows `decision_log.md` **is** structurally enforced — the enforcement just lives in a different file than the one listing the rule. The real gap is that `shared_standards.md` §7 lists **five** append-only files but only `decision_log.md` has an equivalent structural check; `escalations.md`, `execution_escalations.md`, `verification_escalations.md`, and `delegation_log.md` do not. See AUD-002.

### Stage 4 — Lifecycle Reliability

R1 — All lifecycle_schema.json states have valid entry/exit transitions: **PASS** (10 states, 12 transitions; `Blocked` resolves via `guard_rules.blocked_resolution` back to `prior_status`, documented not gapped).

R2 — Hard-gate recovery instructions: sampled instances (roadmap STEP -1.5, STEP 8.5.E; sprint_planning STEP -1; delivery_verification STEP -1; amendment_cycle STEP -1.3) **all have explicit recovery instructions**. Not exhaustive across all ~64 hard-gate instances system-wide.

R3 — Idempotency guard classification (corrected sub-table — `decision_log.md` removed per Stage 3 self-correction above):

| Write operation | File | Guard type |
|---|---|---|
| `lessons_learnt_cycle.md` Phase 3 append | execution_prompt.md:954 | ASSERTION |
| `lessons_learnt_cycle.md` Phase 4 append | delivery_verification_prompt.md:538 | ASSERTION |
| `lessons_learnt_cycle.md` Amendment append | amendment_cycle_prompt.md:547 | ASSERTION |
| `prompt_change_log.md` append (action-now patches) | amendment_cycle_prompt.md:555 | ASSERTION |
| GitHub issue creation (`sync gh`) | release_planning_prompt.md:1085 | ASSERTION |
| `execution_state.json` pr_status | execution_prompt.md:827 | ASSERTION |
| `.claude_current_state.json` status write | lifecycle_schema.json guard_rules / shared_standards §10.3 | ASSERTION |
| `decision_log.md` append-only | roadmap_prompt.md STEP 9 | **STRUCTURAL** (count-verify + text-unchanged check) |
| `backlog.md` shared write | team_charter.md "Strict Lock" + `claude/backlog/.lock` | **STRUCTURAL** (real lock file) |

7 ASSERTION-type write operations confirmed; 2 STRUCTURAL. No ABSENT (zero idempotency language) operations found.

R4 — Re-evaluate max age rule in STEP -1.5: **PASS** (`roadmap_prompt.md` lines 148–151, 2-cycle OVERDUE + stale-release-target check).

R5/R6 — sampled PASS for the 3 engines checked in depth (roadmap, amendment, idea_intake); not exhaustive for the remaining 10.

### Stage 5 — Token Budget Analysis

| Engine | Lines | ~Tokens (lines×8) | Confidence |
|---|---|---|---|
| roadmap_prompt.md | 812 | ~6,496 | HIGH |
| release_planning_prompt.md | 1,136 | ~9,088 | HIGH |
| sprint_planning_prompt.md | 634 | ~5,072 | HIGH |
| execution_prompt.md | 1,101 | ~8,808 | HIGH |
| delivery_verification_prompt.md | 645 | ~5,160 | HIGH |
| post_ship_closure.md | 735 | ~5,880 | HIGH |
| shared_standards.md | 869 | ~6,952 | HIGH |
| lessons_learnt_prompt.md | 506 | ~4,048 | HIGH |
| **Total** | **6,438** | **~51,504** | — |

⚠ METHODOLOGY FOOTNOTE (mandatory): This table does not capture in-run context accumulation. For `execution_prompt.md`, actual per-invocation cost grows with sprint size (loaded EPIC items add to context). Reported cost may understate actual by 30–50% on large sprints. Use as lower bound.

DRY-RUN GAP: `run audit` is the only CLAUDE.md-listed governed routine absent from the §13 dry-run table (see AUD-008) — low token risk since `claude/audit.py` performs no writes by design (read-only routine), so the gap is documentation-only, not a functional risk.

RANKED SAVINGS: not computed this run — no confirmed inline schema/halt/invariant duplication was found to extract (see Stage 7/9).

### Stage 6 — Engine Handoff Integrity

Sampled handoff pairs (Release Planning → Sprint Planning → Execution → Delivery Verification → Post-Ship; Amendment → Sprint Planning): `design_gate_required`/`design_gate_status` and `amended_backlog_slice_path` fields flow cleanly producer→consumer in every pair checked. **No DEAD OUTPUT or SCHEMA VERSION MISMATCH found** in the fields sampled. Not an exhaustive field-by-field diff of every artefact each engine could theoretically consume.

### Stage 7 — Prompt Architecture & Compression

| Engine | STEPs | Hard gates | Lines | Flagged? |
|---|---|---|---|---|
| roadmap_prompt.md | 20 | 9 | 812 | **FLAGGED — STEPs > 15** |

§14 VERSION DRIFT CHECK (conditional — drift found, full report given per rule):
- 13/14 rows match. **1 mismatch: Roadmap Rebalance Prompt (§14 says v7.5, actual v7.6)** — see AUD-003.
- **Additional, more severe finding: OPERATIONAL_GUIDE.md's own self-metadata is internally inconsistent** — document header (line 5) says Version 4.65; §14's own self-row (line ~1457) says Version 4.63; §14's own Change Log top entry (line ~1497) says 4.64. Cross-referencing `prompt_change_log.md` line 479 confirms the *intended* end-state was 4.65 everywhere (the v6.2 ST-10/11 execution_prompt.md v3.48 bump) — the header was updated correctly, but the §14 self-row and Change Log were not, in violation of CLAUDE.md §6's own Governance File Edit Checklist. This is a recurrence of the pattern PRIOR_SCORES noted as already "5th recurrence; fixed AUD-2026-06-22-003" — it has recurred again since that fix. See AUD-001.

Invocation guard (`lessons_learnt_prompt.md` §1): phrased as a **structural hard gate** ("halts on absent context"), `invocation_context` required (4 fields), 3 calling engines (execution, delivery_verification, amendment_cycle) confirmed passing structured context.

### Stage 8 — Amendment Cycle Completeness

| Check | Result |
|---|---|
| A1 — Amendment_In_Progress state machine | **PASS** |
| A2 — First-amendment zero-state | **PASS** (starts at `01`) |
| A3 — Withdrawal path | **PASS** |
| A4 — Two-authority ratification mode-independent | **PASS** |
| A5 — One-active-amendment hard gate | **PASS** |
| A6 — Sprint Planning guards Amendment_In_Progress | **PASS** (explicit "mode-independent" language, mirrored in release_planning_prompt.md) |
| A7 — amendment_lessons.md sunset/optional status defined | **PASS with latent inconsistency** — §8 (line 545) frames it as deprecated/backward-compat-only from v1.5, but §9 Completion Condition (line 586) still lists it as a **mandatory** completion bullet. Current version 1.8 (<2.0 sunset trigger), so not yet a functional bug, but the framing already contradicts itself. See AUD-017. |

### Stage 9 — Single Source of Truth

| Check | Result | Evidence |
|---|---|---|
| SST1 — Invariant lists unique canonical source | **PASS** | `invariants.md` is the single canonical file; README §3 and roadmap §9 are pointers only, both citing the same source |
| SST2 — Halt format: engines reference §5/§10 only | **PASS** (sampled) | e.g. `release_planning_prompt.md` references `shared_standards.md §5` by pointer |
| SST3 — JSON schemas in shared_standards §16 | **PASS** | §16.1–§16.11 confirmed present |
| SST4 — workforce_capacity.md single write owner | **PASS** | Only `roadmap_prompt.md` claims `Write:`; sprint_planning/execution only read it |
| SST5 — scored_initiatives cycle-scoped naming | **FAIL** | `roadmap_prompt.md` line 503 writes a static `claude/scoring/scored_initiatives.md` — overwritten each cycle, no history retained. See AUD-014. |

### Stage 10 — Known Design Gaps & Deferred Patches

D1 — Patch age table:

| Patch | First recorded | Cycles carried | Status |
|---|---|---|---|
| BLG-GOV-135/136 | v6.1 | 1 | RESOLVED (`prompt_change_log.md` line 478) |
| FI-P3-01 | v6.2 | 1 (did not recur) | RESOLVED in practice |
| FI-P3-02 | v6.2 | **2** | **STALE** — see AUD-007 |
| FI-P4-01 / DF-10 | v6.2 | **2** | **STALE, escalation-flagged** — see AUD-004 |
| DF-01–DF-06 | v6.3 | 0 | ACTIVE (not yet due) |

D2–D5:

| Check | Result |
|---|---|
| D2 — `ideas_window.json` has `per_agent_submission_count` | **PASS** (line 57) |
| D3 — `rejected_but_strong.md` compliant header | **PASS** |
| D4 — Challenger Score-4/5 halt/park instruction | **PASS** (`roadmap_prompt.md` lines 443–446, 489) |
| D5 — Re-evaluate max age structural in STEP -1.5 | **PASS** (same evidence as R4) |

### Stage 11 — Best Practices Compliance

| Check | Result | Dimension |
|---|---|---|
| BP-01 Class 6 compliant headers (14/14 prompts) | **PASS with style note** — 3 files (roadmap, release_planning, sprint_planning) append long prose to `Last Updated` instead of the `[date]`-only format `document_lifecycle_guide.md` Class 6 spec requires | Document Hygiene — see AUD-011 |
| BP-02 Agent roster field-level reads | PASS | Token |
| BP-03 sprint_backlog_index.json in §16 | PASS | Token |
| BP-04 stage4_issue_manifest.json in §16 | PASS | Token |
| BP-05 Decision log append-only STRUCTURAL guard | **PASS** (corrected — see Stage 3 self-correction; enforcement lives in roadmap_prompt.md STEP 9) | Reliability |
| BP-06 `run roadmap --dry-run` | PASS | Token+Reliability |
| BP-07 `run roadmap` in §13 table | PASS | Governance |
| BP-08 zero-state bootstrap | PARTIAL (3/13 confirmed, rest unchecked) | Reliability |
| BP-09 Displacement rule mode-independent | PASS | Governance |
| BP-10 GitHub sync idempotency | PASS (ASSERTION-type, documented check-before-create) | Reliability |
| BP-11 scored_initiatives Class 4 | PASS | Governance |
| BP-12 §13 register coverage | PASS (broad) | Governance |
| BP-13 prompt_change_log entry-per-version | **PARTIAL** — log entry exists for roadmap v7.6, but downstream §14 sync missing (AUD-003) | Governance |
| BP-14 lifecycle_schema.json used for transitions | PASS | Reliability |
| BP-15 prior action-now patches applied | **PARTIAL** — AUD-2026-06-22 items all applied same-day; FI-P4-01/DF-10 (deferred, not "action-now") remains open 2 cycles | Reliability |

### Stage 12 — Routine Consolidation Analysis

All 5 candidate engines (`manage roadmap`, `groom backlog`, `run ideas`, `run design-gate`, `run delivery verification`) trip at least one KEEP-SEPARATE override — every one has its own `--dry-run` support; `run ideas housekeeping` is additionally a confirmed true multi-caller (roadmap STEP 4 + post_ship STEP 12.5); `run design-gate` additionally owns a first-class `lifecycle_schema.json` state (`Design_Gate_Passed`).

| Engine | Verdict | Override |
|---|---|---|
| Roadmap Management | BOUNDARY | Own dry-run |
| Backlog Management | BOUNDARY | Own dry-run |
| Idea Intake | BOUNDARY | Own dry-run |
| Ideas Housekeeping | BOUNDARY | Own dry-run + multi-caller |
| Design Gate | BOUNDARY | Own dry-run + own lifecycle_schema.json state |

No CONSOLIDATE or REVIEW verdicts this run — no consolidation table to report.

---

## 5. Improvements List

### 5a. AUDIT_INDEX (JSON — Claude Code entry point)

```json
// AUDIT_INDEX
[
  {"id": "AUD-2026-07-01-001", "title": "Fix OPERATIONAL_GUIDE self-version desync", "weight": 12, "tier": 1, "effort": "Low", "patches": 2, "files": ["claude/system/OPERATIONAL_GUIDE.md"], "depends_on": []},
  {"id": "AUD-2026-07-01-002", "title": "Add structural guard to 4 append-only logs", "weight": 12, "tier": 2, "effort": "Medium", "patches": 1, "files": ["claude/system/shared_standards.md"], "depends_on": []},
  {"id": "AUD-2026-07-01-003", "title": "Fix stale Roadmap Rebalance version in §14", "weight": 9, "tier": 1, "effort": "Low", "patches": 1, "files": ["claude/system/OPERATIONAL_GUIDE.md"], "depends_on": ["AUD-2026-07-01-001"]},
  {"id": "AUD-2026-07-01-004", "title": "Add CI/infra spec_references convention (DF-10)", "weight": 9, "tier": 2, "effort": "Medium", "patches": 1, "files": ["claude/system/execution_prompt.md"], "depends_on": []},
  {"id": "AUD-2026-07-01-005", "title": "Codify design gate bypass authority in charter", "weight": 9, "tier": 1, "effort": "Low", "patches": 1, "files": ["claude/charter/team_charter.md"], "depends_on": []},
  {"id": "AUD-2026-07-01-006", "title": "Document all 13 routines in README §4", "weight": 9, "tier": 2, "effort": "Medium", "patches": 1, "files": ["claude/README.md"], "depends_on": []},
  {"id": "AUD-2026-07-01-007", "title": "Clarify staging-only AC protocol (FI-P3-02)", "weight": 6, "tier": 1, "effort": "Low", "patches": 1, "files": ["CLAUDE.md"], "depends_on": []},
  {"id": "AUD-2026-07-01-008", "title": "Add run audit to §13 dry-run table", "weight": 6, "tier": 1, "effort": "Low", "patches": 1, "files": ["claude/system/shared_standards.md"], "depends_on": []},
  {"id": "AUD-2026-07-01-009", "title": "Fix broken lifecycle guide path in README", "weight": 6, "tier": 1, "effort": "Low", "patches": 1, "files": ["claude/README.md"], "depends_on": []},
  {"id": "AUD-2026-07-01-010", "title": "Refresh README last-updated + routine count", "weight": 6, "tier": 1, "effort": "Low", "patches": 1, "files": ["claude/README.md"], "depends_on": ["AUD-2026-07-01-006", "AUD-2026-07-01-009"]},
  {"id": "AUD-2026-07-01-011", "title": "Fix Last Updated header format in 3 prompts", "weight": 6, "tier": 1, "effort": "Low", "patches": 3, "files": ["claude/system/roadmap_prompt.md", "claude/system/release_planning_prompt.md", "claude/system/sprint_planning_prompt.md"], "depends_on": []},
  {"id": "AUD-2026-07-01-012", "title": "Clarify friction_load formula time window", "weight": 6, "tier": 1, "effort": "Low", "patches": 1, "files": ["claude/audit.py"], "depends_on": []},
  {"id": "AUD-2026-07-01-013", "title": "Reconcile last_audit_open_items state contradiction", "weight": 6, "tier": 1, "effort": "Low", "patches": 1, "files": [".claude_current_state.json"], "depends_on": []},
  {"id": "AUD-2026-07-01-014", "title": "Cycle-scope scored_initiatives filename", "weight": 4, "tier": 2, "effort": "Medium", "patches": 1, "files": ["claude/system/roadmap_prompt.md"], "depends_on": []},
  {"id": "AUD-2026-07-01-015", "title": "Bold pmo_lead.md header fields", "weight": 3, "tier": 1, "effort": "Low", "patches": 1, "files": ["claude/agents/pmo_lead.md"], "depends_on": []},
  {"id": "AUD-2026-07-01-016", "title": "Fix metrics owner role-name drift", "weight": 3, "tier": 1, "effort": "Low", "patches": 1, "files": ["claude/agents/metrics_definitions_analytics_owner.md"], "depends_on": []},
  {"id": "AUD-2026-07-01-017", "title": "Resolve amendment_lessons sunset contradiction", "weight": 2, "tier": 1, "effort": "Low", "patches": 1, "files": ["claude/system/amendment_cycle_prompt.md"], "depends_on": []}
]
```

### 5b. Individual Improvements

---

### AUD-2026-07-01-001
**Title:** OPERATIONAL_GUIDE.md self-version desync across 3 locations
**Area:** Governance
**Evidence Classification:** OBSERVED
**Blast Radius:** 4
**Priority Weight:** 12
**Problem:** `OPERATIONAL_GUIDE.md` header claims Version 4.65, but §14's own self-row still shows 4.63 and §14's own Change Log top entry shows 4.64 — three different numbers in one document. `prompt_change_log.md` line 479 confirms the intended end-state (4.65 everywhere, from the v6.2 ST-10/11 execution_prompt.md v3.48 bump), but the self-row and Change Log were never updated to match.
**Evidence:** `claude/system/OPERATIONAL_GUIDE.md` line 5 (header, 4.65) vs line ~1457 (§14 self-row, 4.63) vs line ~1497 (Change Log top row, 4.64); `claude/system/prompt_change_log.md` line 479.
**Recommended change:** Update §14 self-row to 4.65/2026-06-24; insert the missing v4.65 Change Log entry.
**Expected benefit:** Restores single source of truth for the document's own version — this exact failure mode was already "fixed" once (AUD-2026-06-22-003) and has recurred; closing it cleanly again reduces recurrence risk for the next audit.
**Token impact:** Neutral — 4-line documentation fix.
**Implementation effort:** Low
**Dependencies:** None

PATCH 1:
  operation: REPLACE
  file: claude/system/OPERATIONAL_GUIDE.md
  anchor: "| Version | 4.63 |
| Last Updated | 2026-06-22 |"
  content: |
    | Version | 4.65 |
    | Last Updated | 2026-06-24 |

PATCH 2:
  operation: INSERT_AFTER
  file: claude/system/OPERATIONAL_GUIDE.md
  anchor: "| Version | Date | Change Summary |
|---------|------|----------------|"
  content: |
    | 4.65 | 2026-06-24 | **v6.2 ST-10+ST-11 (BLG-GOV-135/136, EPIC-03) — execution_prompt.md v3.47→v3.48.** §8 source prompt header v3.47→v3.48; §14 Execution Engine Source v3.47→v3.48; §14 Version 4.64→4.65/2026-06-24; document header Version 4.64→4.65. Authority: Head of Specs Team (BLG-GOV-135+136, v6.2 ST-10+ST-11, 2026-06-24). |

---

### AUD-2026-07-01-002
**Title:** 4 of 5 append-only files in §7 lack structural entry-count enforcement
**Area:** Lifecycle
**Evidence Classification:** OBSERVED
**Blast Radius:** 4
**Priority Weight:** 12
**Problem:** `shared_standards.md` §7 lists 5 append-only files, all governed by the same prose instruction ("Never edit a previous entry"). Only `decision_log.md` actually has a structural before/after entry-count + text-unchanged verification (in `roadmap_prompt.md` STEP 9); `escalations.md`, `execution_escalations.md`, `verification_escalations.md`, and `delegation_log.md` have no equivalent check anywhere.
**Evidence:** `claude/system/shared_standards.md` §7 (lines 214–226); `claude/system/roadmap_prompt.md` STEP 9 "Decision log append-only enforcement (structural)" block (no equivalent found for the other 4 files via grep across `claude/system/*.md`).
**Recommended change:** Add a canonical "Append-Only Structural Verification" pattern to §7 (count-before, count-after, text-diff check) and reference it as the required pattern for all 5 files, not just decision_log.md.
**Expected benefit:** Closes a real silent-corruption risk on 4 audit-trail files (escalation and delegation records) that currently rely entirely on prompt discipline.
**Token impact:** Neutral — one shared_standards.md section addition, referenced by pointer from calling engines (no per-engine duplication).
**Implementation effort:** Medium
**Dependencies:** None

PATCH:
  operation: REPLACE
  file: claude/system/shared_standards.md
  anchor: "If a correction is needed to a previous entry, append a correction note referencing the original entry ID. Do not overwrite."
  content: |
    If a correction is needed to a previous entry, append a correction note referencing the original entry ID. Do not overwrite.

    **Structural verification requirement:** `claude/roadmap/decision_log.md` has a confirmed structural guard (`roadmap_prompt.md` STEP 9: count entries before/after write, confirm count only increased, confirm no existing entry text changed — halt if either check fails). The remaining four files above (`escalations.md`, `execution_escalations.md`, `verification_escalations.md`, `delegation_log.md`) currently rely on prose instruction only. Any engine that appends to one of these files should apply the same before/after count-verify pattern at its write step.

---

### AUD-2026-07-01-003
**Title:** §14 table shows Roadmap Rebalance Prompt at stale v7.5
**Area:** Governance
**Evidence Classification:** OBSERVED
**Blast Radius:** 3
**Priority Weight:** 9
**Problem:** `OPERATIONAL_GUIDE.md` §14 lists "Roadmap Engine Source | `claude/system/roadmap_prompt.md` v7.5", but the actual file header is v7.6 (confirmed `roadmap_prompt.md` line 3), and `prompt_change_log.md` line 25 documents the v7.5→v7.6 bump as already applied on 2026-06-22.
**Evidence:** `claude/system/OPERATIONAL_GUIDE.md` §14 row "Roadmap Engine Source"; `claude/system/roadmap_prompt.md` line 3 (`**Version:** 7.6`); `claude/system/prompt_change_log.md` line 25.
**Recommended change:** Bump the §14 row to v7.6.
**Expected benefit:** Removes the one confirmed §14/actual-file version mismatch found in this audit's full 14-row sweep.
**Token impact:** Neutral — 1-line fix.
**Implementation effort:** Low
**Dependencies:** AUD-2026-07-01-001 (same file, apply together to avoid re-reading OPERATIONAL_GUIDE.md twice)

PATCH:
  operation: REPLACE
  file: claude/system/OPERATIONAL_GUIDE.md
  anchor: "| Roadmap Engine Source | `claude/system/roadmap_prompt.md` v7.5 |"
  content: |
    | Roadmap Engine Source | `claude/system/roadmap_prompt.md` v7.6 |

---

### AUD-2026-07-01-004
**Title:** CI/infrastructure spec_references convention unresolved 2 cycles (DF-10)
**Area:** Handoff
**Evidence Classification:** OBSERVED
**Blast Radius:** 3
**Priority Weight:** 9
**Problem:** `FI-P4-01` (filed v6.2) asked for guidance so CI/infrastructure stories with no prior canonical spec reference the primary file changed rather than leaving `spec_references=[]`. It is still unapplied at v6.3 close, now filed as `DF-10` with explicit "ESCALATION RISK (2-cycle if missed)" language for v6.4.
**Evidence:** `claude/cycles/2026-06-26__release-v6.3/lessons_learnt_closure.md` line 47, 67; `claude/system/execution_prompt.md` lines 534–542 (current 3-case table has no CI/infra case; final sentence still says "Leave `[]` only for purely infrastructural items with no governing spec" — the opposite of the requested convention).
**Recommended change:** Add Case D to the `spec_references` policy table and correct the trailing sentence.
**Expected benefit:** Closes a 2-cycle-carried deferred patch before it becomes a 3rd-cycle recurrence (the SLA's own P0-escalation threshold).
**Token impact:** Neutral — table row + one sentence.
**Implementation effort:** Medium
**Dependencies:** None

PATCH:
  operation: REPLACE
  file: claude/system/execution_prompt.md
  anchor: "   If none of the above cases apply and a governing spec exists: set `spec_references` to that spec path. Leave `[]` only for purely infrastructural items with no governing spec."
  content: |
       | D — CI/infrastructure | Sole deliverable is a CI/pipeline/tooling config change (e.g. `playwright.config.js`, workflow YAML) with no prior canonical spec | Set `spec_references` to the primary file changed — it is the de facto spec reference. (FI-P4-01 / DF-10) |

       If none of the above cases apply and a governing spec exists: set `spec_references` to that spec path. `spec_references = []` should not occur for any story type covered by Cases A–D above.

---

### AUD-2026-07-01-005
**Title:** Design gate bypass authority not codified in team charter
**Area:** Governance
**Evidence Classification:** OBSERVED
**Blast Radius:** 3
**Priority Weight:** 9
**Problem:** `sprint_planning_prompt.md` line 174 requires `design_gate_bypass_authority` to name both "Head of UX & Design + Product Owner" (IMP-30) before a skipped design gate can be accepted, but this dual-authority rule exists only in a Class 6 governance prompt — it is absent from `team_charter.md`, the Class 1 canonical authority document.
**Evidence:** `claude/system/sprint_planning_prompt.md` lines 172–174; zero hits for "bypass" in `claude/charter/team_charter.md` or `document_lifecycle_guide.md`.
**Recommended change:** Add a new §5.7 "Design gate bypass disputes" subsection to team_charter.md, mirroring the existing §5.6 pattern, naming the dual-authority requirement at the charter level.
**Expected benefit:** Fixes G5 FAIL — a prompt-only authority rule is not binding on future prompt edits the way a charter rule is; this closes that gap structurally.
**Token impact:** Neutral — one new charter subsection, referenced by pointer from sprint_planning_prompt.md going forward.
**Implementation effort:** Low
**Dependencies:** None

PATCH:
  operation: INSERT_AFTER
  file: claude/charter/team_charter.md
  anchor: "### 5.6 Process halt disputes

If Facilitator halts a governed routine:
- No decision authority may override the halt
- Resolution requires the specific gate violation to be remediated
- Product Owner + Head of Specs Team must jointly agree that the gate is satisfied before the routine resumes"
  content: |


    ### 5.7 Design gate bypass disputes

    If a cycle enters `Sprint_Planning_Complete` from `Release_Planning_Complete` without passing through `Design_Gate_Passed` (design gate skipped):
    - `design_gate_bypass_authority` must name both **Head of UX & Design and Product Owner** — a single role is non-compliant (IMP-30, enforced at `sprint_planning_prompt.md` STEP -1 Bypass Audit).
    - A bypass without both authorities recorded may not be treated as valid; the sprint may not seal.

---

### AUD-2026-07-01-006
**Title:** README §4 documents 1 of 13 governed routines
**Area:** Document Hygiene
**Evidence Classification:** OBSERVED
**Blast Radius:** 3
**Priority Weight:** 9
**Problem:** `claude/README.md` §4 "Organisational Routines" documents only Roadmap Rebalance (§4.1). The other 12 governed routines (Release Planning, Sprint Planning, Sprint Execution, Delivery Verification, Post-Ship Closure, Amendment Cycle, Design Gate, Idea Intake, Roadmap/Backlog Management, Ideas Housekeeping, Lifecycle Audit) are documented in `OPERATIONAL_GUIDE.md` §4/§14 but absent from README.
**Evidence:** `claude/README.md` lines 45–75 (§4, one subsection only); `claude/system/OPERATIONAL_GUIDE.md` §4 phase table (13 rows).
**Recommended change:** Add a summary table to README §4 pointing to OPERATIONAL_GUIDE for each routine, rather than duplicating full routine descriptions.
**Expected benefit:** README is the first file a new agent or reader loads; a 1-of-13 coverage rate misrepresents the system's actual scope.
**Token impact:** Costs — ~15 lines added to README.md, loaded once per README read (not part of any engine's per-invocation preflight).
**Implementation effort:** Medium
**Dependencies:** None

PATCH:
  operation: INSERT_AFTER
  file: claude/README.md
  anchor: "Execution logic is defined in:
- `claude/system/roadmap_prompt.md`

---"
  content: |


    ### 4.2 Other Governed Routines (Summary)

    | Routine | Command | Prompt |
    |---|---|---|
    | Release Planning | `plan release` | `claude/system/release_planning_prompt.md` |
    | Sprint Planning | `plan sprint` | `claude/system/sprint_planning_prompt.md` |
    | Sprint Execution | `run sprint` | `claude/system/execution_prompt.md` |
    | Delivery Verification | `run delivery verification` | `claude/system/delivery_verification_prompt.md` |
    | Post-Ship Closure | `run post-ship` | `claude/system/post_ship_closure.md` |
    | Amendment Cycle | `amend cycle` | `claude/system/amendment_cycle_prompt.md` |
    | Design Gate | `run design-gate` | `claude/system/design_gate_prompt.md` |
    | Idea Intake | `run ideas` | `claude/system/idea_intake_prompt.md` |
    | Roadmap Management | `manage roadmap` | `claude/system/roadmap_management_prompt.md` |
    | Backlog Management | `groom backlog` | `claude/system/backlog_management_prompt.md` |
    | Ideas Housekeeping | `run ideas housekeeping` | `claude/system/ideas_housekeeping_prompt.md` |
    | Lifecycle Audit | `run audit` | `claude/audit.py` |

    Full trigger conditions and phase sequencing: see `claude/system/OPERATIONAL_GUIDE.md` §4.

    ---

---

### AUD-2026-07-01-007
**Title:** Staging-only AC protocol ambiguity unresolved 2 cycles
**Area:** Lifecycle
**Evidence Classification:** OBSERVED
**Blast Radius:** 2
**Priority Weight:** 6
**Problem:** `FI-P3-02` (v6.2) asked for CLAUDE.md's frontend testing gate rule to clarify when code review of static JSX is an acceptable substitute for staging sign-off (wording-only ACs) versus when it is not (visual rendering/colour ACs). It remains unresolved at v6.3 close — the v6.3 lessons_learnt_cycle.md explicitly notes "Protocol ambiguity from v6.2 remains unresolved... not closed this sprint."
**Evidence:** `claude/cycles/2026-06-24__release-v6.2/lessons_learnt_closure.md` line 50, 74; `claude/cycles/2026-06-26__release-v6.3/lessons_learnt_cycle.md` line 37; `CLAUDE.md` §2 Playwright/staging bullet (current wording does not distinguish wording-only vs visual ACs).
**Recommended change:** Add an explicit clause to the existing CLAUDE.md §2 bullet distinguishing the two AC types.
**Expected benefit:** Closes a 2-cycle-carried friction item before the next cycle escalates it further.
**Token impact:** Neutral — one clause added to an existing bullet.
**Implementation effort:** Low
**Dependencies:** None

PATCH:
  operation: REPLACE
  file: CLAUDE.md
  anchor: "Code review alone is not a valid evidence method for observable UI behaviour."
  content: |
    Code review alone is not a valid evidence method for observable UI behaviour. **Exception (FI-P3-02):** for ACs that are wording-only (text content, no visual rendering/colour/layout claim), code review of the static JSX/text may substitute for staging sign-off. Any AC involving visual rendering, colour, layout, or interaction timing requires Playwright coverage or a recorded staging run regardless of how simple the change appears.

---

### AUD-2026-07-01-008
**Title:** `run audit` absent from §13 dry-run table
**Area:** Token Efficiency
**Evidence Classification:** OBSERVED
**Blast Radius:** 2
**Priority Weight:** 6
**Problem:** `shared_standards.md` §13 lists 12 dry-run-capable engines. `run audit` is a governed routine listed in CLAUDE.md §1 but is absent from this table.
**Evidence:** `claude/system/shared_standards.md` §13 table (12 rows, no `run audit` row); `CLAUDE.md` §1 command table row for `run audit`.
**Recommended change:** Add a `run audit` row noting it is inherently read-only (no dry-run mode needed).
**Expected benefit:** Removes the only confirmed engine documentation gap in the dry-run standard; low functional risk since audit.py performs no writes by design.
**Token impact:** Neutral.
**Implementation effort:** Low
**Dependencies:** None

PATCH:
  operation: REPLACE
  file: claude/system/shared_standards.md
  anchor: "| `amend cycle --dry-run` | Amendment preview — proposed backlog slice delta, scope changes, authority ratification requirements; no state.json writes, no slice artefact created |"
  content: |
    | `amend cycle --dry-run` | Amendment preview — proposed backlog slice delta, scope changes, authority ratification requirements; no state.json writes, no slice artefact created |
    | `run audit` | N/A — `claude/audit.py` is read-only by design (produces a report + a PATCH manifest for Claude Code to apply separately); no `--dry-run` flag needed, no writes occur during the audit run itself |

---

### AUD-2026-07-01-009
**Title:** README §2 references a non-existent file path
**Area:** Document Hygiene
**Evidence Classification:** OBSERVED
**Blast Radius:** 2
**Priority Weight:** 6
**Problem:** `claude/README.md` §2 "Governing Authorities" lists `/charter/documentation_lifecycle_guide.md`. The actual file is `claude/charter/document_lifecycle_guide.md` (no "ation").
**Evidence:** `claude/README.md` §2; `ls claude/charter/` confirms only `document_lifecycle_guide.md` exists.
**Recommended change:** Fix the filename typo.
**Expected benefit:** Removes a confirmed broken canonical-authority path from the first file most readers load.
**Token impact:** Neutral — 1-word fix.
**Implementation effort:** Low
**Dependencies:** None

PATCH:
  operation: REPLACE
  file: claude/README.md
  anchor: "- `/charter/documentation_lifecycle_guide.md`"
  content: |
    - `/charter/document_lifecycle_guide.md`

---

### AUD-2026-07-01-010
**Title:** README.md is 101 days stale
**Area:** Document Hygiene
**Evidence Classification:** OBSERVED
**Blast Radius:** 2
**Priority Weight:** 6
**Problem:** `claude/README.md`'s own header declares `Last Updated: 2026-03-22`, 101 days before the most recent engine version bump in the repo (`execution_prompt.md` v3.48, 2026-06-24).
**Evidence:** `claude/README.md` line 4; `claude/system/prompt_change_log.md` line 478.
**Recommended change:** Bump the Last Updated date once AUD-006 and AUD-009 are applied in the same commit.
**Expected benefit:** Keeps the header honest about how current the file actually is.
**Token impact:** Neutral.
**Implementation effort:** Low
**Dependencies:** AUD-2026-07-01-006, AUD-2026-07-01-009 (apply in the same commit as those two README edits)

PATCH:
  operation: REPLACE
  file: claude/README.md
  anchor: "Last Updated: 2026-03-22  "
  content: |
    Last Updated: 2026-07-01  

---

### AUD-2026-07-01-011
**Title:** 3 governance prompts violate Class 6 "Last Updated: [date]" header spec
**Area:** Document Hygiene
**Evidence Classification:** OBSERVED
**Blast Radius:** 2
**Priority Weight:** 6
**Problem:** `document_lifecycle_guide.md` Class 6 requires `Last Updated: [date]` — a date, not prose. `roadmap_prompt.md`, `release_planning_prompt.md`, and `sprint_planning_prompt.md` all append a full change-description paragraph after the date in that field.
**Evidence:** `claude/charter/document_lifecycle_guide.md` Class 6 required header fields; `claude/system/roadmap_prompt.md` line 4, `release_planning_prompt.md` line 4, `sprint_planning_prompt.md` line 4 (each: date followed by a parenthetical paragraph).
**Recommended change:** Move the change description out of the header field into a comment or leave the header date-only; the detail already lives in `prompt_change_log.md`.
**Expected benefit:** Restores Class 6 header compliance across the 3 highest-traffic governance prompts. Low risk — purely cosmetic, no information is lost since the same detail is duplicated in `prompt_change_log.md`.
**Token impact:** Saves — removes ~150 words of duplicated changelog prose from 3 files that are read at every relevant engine's preflight (header + version check happens on nearly every invocation).
**Implementation effort:** Low
**Dependencies:** None

PATCH 1:
  operation: REPLACE
  file: claude/system/roadmap_prompt.md
  anchor: "**Last Updated:** 2026-06-22 (v7.5→v7.6: STEP 8.2 — Now Horizon Item Verification added (mandatory); checks every proposed Now horizon item against active backlog.md before scope inclusion; catches prose-referenced archived items that bypass STEP 3 candidate list. Root cause: 2026-06-19__scheduled included BLG-GOV-113 (archived v5.3) via run_manifest prose reference, caught at STEP 9. Authority: Head of Specs Team (LL-RP-01 deferred patch, rebalance 2026-06-22__scheduled).)"
  content: |
    **Last Updated:** 2026-06-22

PATCH 2:
  operation: REPLACE
  file: claude/system/release_planning_prompt.md
  anchor: "**Last Updated:** 2026-06-22 (v2.37→v2.38: ST-01/BLG-GOV-132 — STEP 4.1 Design Gate Classification added: STEP 4 now scans backlog slice for UI-facing scope and sets design_gate_required in state.json and .claude_current_state.json; STEP 7 updated to include design_gate_required status line in cycle_summary.md header)"
  content: |
    **Last Updated:** 2026-06-22

PATCH 3:
  operation: REPLACE
  file: claude/system/sprint_planning_prompt.md
  anchor: "**Last Updated:** 2026-06-22 (v3.10→v3.11: ST-02/BLG-GOV-133 — STEP -1 check 3 updated: design gate hard gate now conditional on design_gate_required = true; when design_gate_required = false gate check is skipped with explicit log note; source reads from state.json attributes.design_gate_required)"
  content: |
    **Last Updated:** 2026-06-22

---

### AUD-2026-07-01-012
**Title:** FRICTION_LOAD formula wording ambiguous about time window
**Area:** Prompt
**Evidence Classification:** LATENT
**Blast Radius:** 3
**Priority Weight:** 6
**Problem:** `audit.py`'s FRICTION_LOAD formula says "per confirmed Type A friction item **across all cycles**", and the Phase 1 load instruction says to load friction counts from "ALL cycles". Taken literally, this would mean cumulative all-time totals (Type A=61, Type C=33 confirmed this run) — but `PRIOR_SCORES`'s own baseline note ("Type A×1 + Type C×3") is far too small to be an all-time count, implying the real intended window is "since last audit." If a future run (or a different agent) takes the literal wording at face value, the score will differ wildly and non-reproducibly from this run's interpretation.
**Evidence:** `claude/audit.py` FRICTION_LOAD formula block and the `PRIOR_SCORES` comment for `friction_load` (both quoted in this audit's config).
**Recommended change:** Clarify the formula wording to explicitly say "since PRIOR_AUDIT_ID" rather than "across all cycles."
**Expected benefit:** Removes a scoring-methodology ambiguity that could otherwise produce a non-reproducible Friction Load score on the next audit run.
**Token impact:** Neutral — one wording clarification in a comment/docstring.
**Implementation effort:** Low
**Dependencies:** None

PATCH:
  operation: REPLACE
  file: claude/audit.py
  anchor: "FRICTION_LOAD:
  -4 per confirmed Type A friction item across all cycles (cite cycle)
  -3 per confirmed Type C friction item across all cycles (cite cycle)
  -6 per friction item confirmed recurring across 2+ cycles (cite cycles)
  -5 per deferred patch confirmed unresolved across all cycles (cite patch)"
  content: |
    FRICTION_LOAD:
      (Window: cycles since PRIOR_AUDIT_ID only — not all-time cumulative. Confirmed at AUD-2026-07-01: literal "all cycles" wording is ambiguous and was resolved as "since last audit" to match PRIOR_SCORES baseline methodology.)
      -4 per confirmed Type A friction item since PRIOR_AUDIT_ID (cite cycle)
      -3 per confirmed Type C friction item since PRIOR_AUDIT_ID (cite cycle)
      -6 per friction item confirmed recurring across 2+ cycles (cite cycles)
      -5 per deferred patch confirmed unresolved since PRIOR_AUDIT_ID (cite patch)

---

### AUD-2026-07-01-013
**Title:** State file contradicts audit config on prior open-item count
**Area:** State
**Evidence Classification:** OBSERVED
**Blast Radius:** 2
**Priority Weight:** 6
**Problem:** `.claude_current_state.json` field `last_audit_open_items` reads `10`, but `claude/audit.py`'s `PRIOR_AUDIT_OPEN_ITEMS = []` (0 items) for the same `last_audit_id: "AUD-2026-06-22"`. All AUD-2026-06-22 items are confirmed applied same-day per `prompt_change_log.md`, consistent with 0, not 10.
**Evidence:** `.claude_current_state.json` field `last_audit_open_items`; `claude/audit.py` line 28 comment "All AUD-2026-06-22 Tier 1 items applied same commit; 0 open items."
**Recommended change:** Correct the state field to 0 to match the resolved reality.
**Expected benefit:** Removes a confusing discrepancy between the two files a future audit or engine would read for this figure.
**Token impact:** Neutral.
**Implementation effort:** Low
**Dependencies:** None

PATCH:
  operation: REPLACE
  file: .claude_current_state.json
  anchor: "  "last_audit_open_items": 10,"
  content: |
      "last_audit_open_items": 0,

---

### AUD-2026-07-01-014
**Title:** scored_initiatives.md uses a static, non-cycle-scoped filename
**Area:** State
**Evidence Classification:** LATENT
**Blast Radius:** 2
**Priority Weight:** 4
**Problem:** `roadmap_prompt.md` writes `claude/scoring/scored_initiatives.md` with a static filename, overwritten every cycle. A stray historical file (`scored_initiatives_2026-03-06.md`) shows a cycle-scoped naming convention was used at least once, but is not the current pattern — per-cycle scoring history is not retained.
**Evidence:** `claude/system/roadmap_prompt.md` line 503 ("Write: `claude/scoring/scored_initiatives.md`"); `claude/scoring/` directory listing (2 files, 1 stale-dated).
**Recommended change:** Adopt cycle-scoped naming consistently, or explicitly document that the file is intentionally cycle-current-only (and remove the stray dated file to avoid implying a convention that isn't followed).
**Expected benefit:** Either restores per-cycle scoring history (useful for the roadmap trend analysis other stages reference) or removes a confusing half-adopted convention.
**Token impact:** Neutral if documentation-only; costs one extra write per cycle if the naming convention is adopted.
**Implementation effort:** Medium
**Dependencies:** None

PATCH:
  operation: REPLACE
  file: claude/system/roadmap_prompt.md
  anchor: "Write: `claude/scoring/scored_initiatives.md` (create if needed — use bash heredoc if directory does not exist)"
  content: |
    Write: `claude/scoring/scored_initiatives.md` (create if needed — use bash heredoc if directory does not exist). This file reflects only the current cycle's scoring — it is overwritten each run and does not retain history. If per-cycle history is needed, also write a copy to `claude/scoring/scored_initiatives_<cycle_id>.md`.

---

### AUD-2026-07-01-015
**Title:** pmo_lead.md header fields not bolded
**Area:** Document Hygiene
**Evidence Classification:** OBSERVED
**Blast Radius:** 1
**Priority Weight:** 3
**Problem:** All other agent files with a Version field use `**Version:**` (bold-label) formatting; `pmo_lead.md` uses plain `Owner:`, `Status:`, `Version:`, `Last Updated:`.
**Evidence:** `claude/agents/pmo_lead.md` lines 3–6, vs. `claude/agents/head_of_engineering.md` lines 6–7 (`**Status:**`, `**Version:**`).
**Recommended change:** Bold the 4 header field labels to match convention.
**Expected benefit:** Consistency across the 6 agent files that declare a version.
**Token impact:** Neutral.
**Implementation effort:** Low
**Dependencies:** None

PATCH:
  operation: REPLACE
  file: claude/agents/pmo_lead.md
  anchor: "Owner: Head of Specs Team
Status: Canonical
Version: 2.2
Last Updated: 2026-03-01"
  content: |
    **Owner:** Head of Specs Team
    **Status:** Canonical
    **Version:** 2.2
    **Last Updated:** 2026-03-01

---

### AUD-2026-07-01-016
**Title:** Metrics owner role-name drift vs team charter
**Area:** Governance
**Evidence Classification:** OBSERVED
**Blast Radius:** 1
**Priority Weight:** 3
**Problem:** `metrics_definitions_analytics_owner.md` self-declares as "Metrics Definitions & Analytics **Canonical** Owner"; `team_charter.md` names the role "Metrics Definitions & Analytics Owner" (no "Canonical").
**Evidence:** `claude/agents/metrics_definitions_analytics_owner.md` lines 1–2; `claude/charter/team_charter.md` line 298 (`#### Metrics Definitions & Analytics Owner`), line 409.
**Recommended change:** Align the agent file to the charter's role name (charter is the authoritative source per team_charter.md §6 rule 3 "Canonical truth overrides planning").
**Expected benefit:** Removes a role-name mismatch that could cause a cross-reference or automated role lookup to fail.
**Token impact:** Neutral.
**Implementation effort:** Low
**Dependencies:** None

PATCH:
  operation: REPLACE
  file: claude/agents/metrics_definitions_analytics_owner.md
  anchor: "# Metrics Definitions & Analytics Canonical Owner
**Role:** Metrics Definitions & Analytics Canonical Owner"
  content: |
    # Metrics Definitions & Analytics Owner
    **Role:** Metrics Definitions & Analytics Owner

---

### AUD-2026-07-01-017
**Title:** amendment_lessons.md sunset framing contradicts its own completion condition
**Area:** Lifecycle
**Evidence Classification:** LATENT
**Blast Radius:** 1
**Priority Weight:** 2
**Problem:** `amendment_cycle_prompt.md` §8 (line 545) declares `amendment_lessons.md` "deprecated as of v1.5... will not be produced from v2.0 onward," but §9's Completion Condition (line 586) still lists it as a mandatory bullet with no conditional language. Current file version is 1.8 (below the v2.0 sunset trigger), so this is not yet a functional bug, but the two sections already disagree on how to treat the file.
**Evidence:** `claude/system/amendment_cycle_prompt.md` line 545 (§8), line 586 (§9).
**Recommended change:** Make the §9 bullet conditional on file version, matching §8's framing.
**Expected benefit:** Removes a latent inconsistency before the file crosses v2.0 and the contradiction becomes a real completion-condition bug.
**Token impact:** Neutral.
**Implementation effort:** Low
**Dependencies:** None

PATCH:
  operation: REPLACE
  file: claude/system/amendment_cycle_prompt.md
  anchor: "- `amendment_lessons.md` filed (standalone, in amendment sub-folder)"
  content: |
    - `amendment_lessons.md` filed (standalone, in amendment sub-folder) — **required only while this prompt is <v2.0**; per §8 deprecation notice, this output is dropped entirely from v2.0 onward and this bullet becomes void at that point

---

## 6. Cross-Improvement Map

| Pair | Relationship |
|---|---|
| AUD-001 ↔ AUD-003 | Same file (`OPERATIONAL_GUIDE.md`) — apply in the same commit to avoid a second read/write pass |
| AUD-006 ↔ AUD-009 ↔ AUD-010 | Same file (`README.md`) — apply together; AUD-010's date bump should be the last of the three |
| AUD-004 ↔ AUD-012 | No file overlap, but both concern the audit/lessons-learnt formula precision that produced the friction-load carry-forward count for DF-10 — apply independently, no ordering constraint |

No conflicting patches found — all anchors are file-unique and non-overlapping.

---

## 7. Implementation Tiers

**Tier 1 (Low effort, no dependencies — apply first):**
AUD-001, AUD-003, AUD-005, AUD-007, AUD-008, AUD-009, AUD-010, AUD-011, AUD-012, AUD-013, AUD-015, AUD-016, AUD-017

**Tier 2 (Medium effort, no dependencies, or BR≥4+Medium override):**
AUD-002 (BR4 override), AUD-004, AUD-006, AUD-014

**Tier 3 (High effort / complex dependency chain):**
None this cycle.

---

## 8. Audit Summary

Overall system health is 74/100 (▲ from an estimated prior-cycle 64), with Execution Reliability the clear outlier at 48 — driven by 7 confirmed ASSERTION-only write operations and 2 deferred patches (FI-P3-02, DF-10) now carried 2 cycles. Governance Integrity improved to 84 once a mis-scoped decision-log finding was corrected during synthesis (the real gap is the other 4 append-only files, not decision_log.md itself), but the OPERATIONAL_GUIDE.md self-version desync is a confirmed 6th recurrence of a pattern already "fixed" once. 17 improvements are filed, all Tier 1–2, none blocked on new files or multi-engine coordination — the full set is safe to apply in a single governance commit per CLAUDE.md §6's checklist.

---

## 9. SLA

- Cadence: every 3 cycles
- OBSERVED + Blast Radius ≥ 3, open after 2 audit cycles → P0 escalation to Head of Specs Team
- Overall score < 65 → GOVERNANCE HOLD: no new cycles until resolved
- Output filed as: `claude/cycles/2026-06-26__release-v6.3/audit_report_AUD-2026-07-01.md` (Class 3)

**Items to watch for P0 escalation next audit if still open:** AUD-2026-07-01-002 (BR4), AUD-2026-07-01-004 (BR3, already 2-cycle friction-side), AUD-2026-07-01-006 (BR3).

---

## 10. Scorecard Appendix

**TOKEN_EFFICIENCY = 100 − 8 = 92**
- `run audit` absent from §13 dry-run table: −8 (CONFIRMED, `shared_standards.md` §13, 12 rows, no `run audit` row)
- Inline schema/invariant/halt blocks: not confirmed present anywhere this run → 0 deduction, but 2 sub-checks (inline JSON schema count, inline halt-format count) were not exhaustively grepped file-by-file → **[LOW CONFIDENCE]** tag applied per the 2+ ESTIMATED-input rule, even though no numeric estimate was substituted.

**GOVERNANCE_INTEGRITY = 100 − 8 − 4 − 4 = 84**
- 4 of 5 §7 append-only files lack structural guard (escalations.md, execution_escalations.md, verification_escalations.md, delegation_log.md): −8 (CONFIRMED)
- §14 Roadmap Rebalance Prompt version diverges from actual file (v7.5 vs v7.6): −4 (CONFIRMED)
- OPERATIONAL_GUIDE.md self-version desync (header 4.65 / §14 self-row 4.63 / Change Log top 4.64): −4 (CONFIRMED)
- Confidence: HIGH — all three deductions have exact file+line citations.
- Correction note: `decision_log.md` was initially miscited by the evidence-gathering pass as an ASSERTION-only guard (based on `shared_standards.md` §7 prose alone). Direct verification of `roadmap_prompt.md` STEP 9 found a genuine structural count-verify check, so no deduction was taken for `decision_log.md` specifically — the −8 above is for the *other four* files only.

**EXECUTION_RELIABILITY = 100 − 42 − 10 = 48**
- 7 confirmed ASSERTION-only write operations × −6 = −42 (lessons_learnt_cycle.md × 3 append sites, prompt_change_log.md append, GitHub issue creation, execution_state.json pr_status, .claude_current_state.json status write)
- 2 deferred patches carried 2+ cycles unresolved (FI-P3-02, FI-P4-01/DF-10) × −5 = −10
- Confidence: HIGH — all 9 line items have file+operation citations (Stage 4 R3 sub-table).
- This is the largest score movement this audit (79→48) and reflects a materially deeper sweep than the prior run recorded, not a new regression — see Audit Summary.

**FRICTION_LOAD = 100 − 8 − 6 − 12 − 10 = 64, not floored**
- Type A × 2 (since PRIOR_AUDIT_ID) × −4 = −8
- Type C × 2 (since PRIOR_AUDIT_ID) × −3 = −6
- 2 friction items confirmed recurring across 2+ cycles (Type A sign-off format; Type D spec_references convention) × −6 = −12
- 2 deferred patches confirmed unresolved (FI-P3-02, FI-P4-01/DF-10) × −5 = −10
- Confidence: HIGH, but **methodology flag**: the formula's literal wording ("across all cycles") is ambiguous — this audit interpreted it as "since PRIOR_AUDIT_ID" to match the `PRIOR_SCORES` baseline note, not literal all-time (all-time Type A=61, Type C=33 — using those would floor this dimension at 0 every single audit forever). See AUD-2026-07-01-012.

**DOCUMENT_HYGIENE = 100 − 4 − 12 − 4 = 80**
- pmo_lead.md non-bolded header fields: −4 (CONFIRMED)
- 3 governance prompts violate Class 6 `Last Updated: [date]` spec (roadmap, release_planning, sprint_planning — prose appended instead of clean date): −4 × 3 = −12 (CONFIRMED against `document_lifecycle_guide.md` Class 6 spec)
- README.md broken path reference (`documentation_lifecycle_guide.md`): −4 (CONFIRMED)
- Confidence: HIGH.

**Overall = (92 + 84 + 48 + 64 + 80) / 5 = 368 / 5 = 73.6 → 74**

---

## 11. Config Update

```python
# === PASTE INTO audit.py CONFIG AFTER THIS RUN ===
PRIOR_AUDIT_ID = "AUD-2026-07-01"
PRIOR_AUDIT_OPEN_ITEMS = [
    "AUD-2026-07-01-001", "AUD-2026-07-01-002", "AUD-2026-07-01-003", "AUD-2026-07-01-004",
    "AUD-2026-07-01-005", "AUD-2026-07-01-006", "AUD-2026-07-01-007", "AUD-2026-07-01-008",
    "AUD-2026-07-01-009", "AUD-2026-07-01-010", "AUD-2026-07-01-011", "AUD-2026-07-01-012",
    "AUD-2026-07-01-013", "AUD-2026-07-01-014", "AUD-2026-07-01-015", "AUD-2026-07-01-016",
    "AUD-2026-07-01-017"
]  # all currently OPEN — re-classify at next audit once patches are applied
PRIOR_SCORES = {
    "token_efficiency":      92,
    "governance_integrity":  84,
    "execution_reliability": 48,
    "friction_load":         64,
    "document_hygiene":      80,
}
COMPLETED_CYCLES = 49  # updated from 46 to current completed_cycle_count at this audit
# === END PASTE ===
```
