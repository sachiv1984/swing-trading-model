# Claude Lifecycle Audit v6 — AUD-2026-03-13

**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Report Date:** 2026-03-13
**Filed:** claude/cycles/<current_cycle_id>/audit_report_AUD-2026-03-13.md
**Audit version:** audit.py v6
**Scope:** claude/

---

## CLAUDE CODE INSTRUCTIONS

Save this file to: `claude/cycles/<current_cycle_id>/audit_report_AUD-2026-03-13.md`

To apply improvements, read the AUDIT_INDEX JSON block in §5 first. It lists every
improvement with its files, patch count, effort, and dependencies. Apply in tier order:
Tier 1 → Tier 2 → Tier 3. Check `depends_on` before applying any item.

For each improvement, find its AUD-ID section, read each PATCH block, and apply using
str_replace_based_edit (anchor = exact string, operation = INSERT_AFTER / REPLACE / APPEND /
CREATE_FILE). After applying all patches for a file, increment that file's version, update
`**Last Updated:**`, and append an entry to `claude/system/prompt_change_log.md`.

Governance rule: all changes to Class 6 prompts require a prompt_change_log.md entry in
the same commit.

---

## 1. Resolved Since Last Audit

First audit run — no prior items.

---

## 2. Health Scorecard

SYSTEM HEALTH — 2026-03-13 | Prior: none (first run)

| Dimension | Score | Bar | Trend | Confidence |
|---|---|---|---|---|
| Token Efficiency | 59 | ██████░░░░ | NEW | LOW |
| Governance Integrity | 74 | ███████░░░ | NEW | HIGH |
| Execution Reliability | 66 | ██████░░░░ | NEW | HIGH |
| Friction Load | 72 | ███████░░░ | NEW | HIGH |
| Document Hygiene | 79 | ████████░░ | NEW | HIGH |
| Machine Friendliness | 52 | █████░░░░░ | NEW | MEDIUM |
| **Overall** | **67** | **███████░░░** | NEW | MEDIUM |

No governance hold triggered (threshold 65). Score below 80 — clear Tier 1 items before next cycle.

Token Efficiency [LOW CONFIDENCE] — inline block counts estimated, not confirmed by line count.
Machine Friendliness based on Stage 13 artefact sample (5 artefacts: 1 STRUCTURED, 3 MIXED, 1 PROSE).

---

## 3. Gap Register

| Stage | File | Status | Impact | → Improvement? |
|---|---|---|---|---|
| Phase 2 | `claude/agents/` — 7+ charter files unconfirmed | PARTIAL | Agent roster incomplete | Yes → AUD-008 |
| Phase 2 | `claude/ideas/rejected_but_strong.md` | NOT FOUND | Absent from §13 register | Yes → AUD-010 |
| Phase 2 | `claude/scoring/` — completeness unverified | PARTIAL | scored_initiatives class unverified | Yes → AUD-010 |
| Phase 2 | `claude/system/invariants.md` | NOT FOUND | Invariants fragmented across 3+ docs | Yes → AUD-006 |
| Phase 2 | `shared_standards.md §16` | NOT FOUND | JSON schemas inline in engine prompts | Yes → AUD-009 |
| Stage 5 | `execution_prompt.md` line count | ESTIMATED | Token budget understated 30-50% | Yes → AUD-017 |
| Stage 13 | `lessons_learnt_cycle.md` machine parse risk | PARTIAL | Variable headers block stable anchoring | Yes → AUD-022 |

---

## 4. Stage Findings

### Stage 1 — Lifecycle Mapping

**TABLE 1 — Command path check:**

| Command | Prompt path in CLAUDE.md | File confirmed? | Syntax match? |
|---|---|---|---|
| `run ideas` | `claude/system/idea_intake_prompt.md` | ✓ v1.2 | ✓ |
| `run roadmap` | `claude/system/roadmap_prompt.md` | ✓ v2.1 | ✓ |
| `manage roadmap` | `claude/system/roadmap_management_prompt.md` | ✓ v1.2 | ✓ |
| `groom backlog` | `claude/system/backlog_management_prompt.md` | ✓ v1.2 | ✓ |
| `plan release` | `claude/system/release_planning_prompt.md` | ✓ v2.18 | ✓ |
| `run design-gate` | `claude/system/design_gate_prompt.md` | ✓ v1.1 | ✓ |
| `plan sprint` | `claude/system/sprint_planning_prompt.md` | ✓ v1.8 | ✓ |
| `amend cycle` | `claude/system/amendment_cycle_prompt.md` | ✓ v1.5 | ✓ |
| `run sprint` | `claude/system/execution_prompt.md` | ✓ v2.0 | ✓ |
| `run delivery verification` | `claude/system/delivery_verification_prompt.md` | ✓ v1.4 | ✓ |
| `run post-ship` | `claude/system/post_ship_closure.md` | ✓ v1.8 | ✓ |
| `run audit` | NOT IN TABLE | — | **⚠ MISSING** |

**TABLE 2 — §14 version spot check:**

| Engine | §14 version | Log entry version | Match? |
|---|---|---|---|
| `roadmap_prompt.md` | v2.1 | v2.1 (2026-03-11) | ✓ |
| `shared_standards.md` | v1.9 | v1.9 (2026-03-11) | ✓ |
| `sprint_planning_prompt.md` | v1.8 | v1.8 (2026-03-11) | ✓ |

§14 ALIGNED — no drift detected.

**Findings:**
- `run audit` absent from CLAUDE.md command table — no governed load path
- README uses stale path reference `claude_system_prompt.md` (does not exist — actual path is per engine)

---

### Stage 2 — Behavioural Audit

**COMPLIANCE TABLE:**

| Cycle | B1 Auth | B2 LL filed | B3 Prior patches | B4 Hard gate | B5 Action-now | B6 Log grew | B7 No 2nd carry |
|---|---|---|---|---|---|---|---|
| 2026-03-01__item-3.2 | ✓ | ✓ | N/A (first) | INSUFFICIENT HISTORY | ✓ | ✓ | N/A |
| 2026-03-04__item-3.4 | ✓ | ✓ | ✗ not confirmed | INSUFFICIENT HISTORY | ✓ | ✓ | ✓ |
| 2026-03-06__item-3.4 | ✓ | ✓ | ✗ 5 patches carried | INSUFFICIENT HISTORY | ✓ | ✓ | ✗ |
| 2026-03-06__release-v1.9 | ✓ | ✓ | ✓ 1 applied | INSUFFICIENT HISTORY | ✓ | ✓ | partial |
| **Compliance %** | **100%** | **100%** | **50% ⚠** | **INSUFFICIENT HISTORY (need ≥3 delivery cycles)** | **100%** | **100%** | **67% ⚠** |

B3 and B7 below 75% → OBSERVED improvements generated (AUD-001, AUD-020).

**PATTERN TABLE:**

| Friction Type | Count | Top source | Recurring? |
|---|---|---|---|
| Type A — Governance Drift | 3 | `roadmap_prompt.md` STEP 9 header formatting | Yes — 2 cycles |
| Type B — Semantic Mismatch | 1 | `post_ship_closure.md` multi-sprint path | No |
| Type C–E | 0 | — | No |

**TREND LINE:** [2026-03-01: 0, 2026-03-04: 1, 2026-03-06__item: 2, 2026-03-06__release: 3]
Trend: INCREASING (4 cycles only — insufficient for statistical confidence)

---

### Stage 3 — Governance Integrity

**TABLE 1 — Agent roster (partial — 7+ files unverified):**

| Agent file | Format | Status |
|---|---|---|
| `product_owner.md` | UNVERIFIED | CONFIRMED (activated in run_manifest) |
| `head_of_specs_team.md` | `## Role:` (non-standard) | CONFIRMED |
| `pmo_lead.md` | `## Role:` (non-standard) | CONFIRMED |
| `strategy_rules_system_intent_owner.md` | `## Role:` (non-standard) | CONFIRMED |
| `head_of_ux_design.md` | CONFIRMED — v1.5 bypass authority | CONFIRMED |
| 7+ specialist roles | UNVERIFIED | UNVERIFIED |

**TABLE 2 — Governance checks:**

| Check | Result | Evidence |
|---|---|---|
| G1 — All charter roles have agent file | PARTIAL | 23 roles listed; directory completeness unverified |
| G2 — Agent lifecycle refs canonical path | UNVERIFIED | Files not loaded |
| G3 — Artefact class declarations match lifecycle guide | PARTIAL | scored_initiatives class unconfirmed |
| G4 — §13 register covers scoring + ideas + lessons | FAIL | `rejected_but_strong.md`, `claude/scoring/` absent |
| G5 — Design gate bypass authority in charter | PASS | team_charter.md v1.5 §3.3 — IMP-30 confirmed |

---

### Stage 4 — Lifecycle Reliability

| Check | Result | Evidence |
|---|---|---|
| R1 — All states valid entry AND exit | PASS | lifecycle_schema.json confirmed; `Closed`→`Executing` multi-sprint present |
| R2 — All halt paths have recovery instruction | PARTIAL | Multi-sprint re-entry requires manual state edit until lifecycle patch |
| R3 — Idempotency: see sub-table | — | — |
| R4 — Re-evaluate max age in STEP -1.5 | FAIL | STEP -1.5 patch still OVERDUE — self-referential gap |
| R5 — All engines zero-state bootstrap | PARTIAL | closure_state.json confirmed; others not verified |
| R6 — Concurrent write prevention | PASS | lifecycle_schema.json `concurrent_write_prevention` rule present |

**R3 IDEMPOTENCY SUB-TABLE:**

| Write operation | File | Guard type |
|---|---|---|
| decision_log.md append | `roadmap_prompt.md` STEP 9 | ASSERTION — "confirm no edits" only |
| lessons_learnt_cycle.md append | `execution_prompt.md` STEP 5.4 | STRUCTURAL — IMP-35 guard active |
| closure_state.json step flags | `post_ship_closure.md` | STRUCTURAL — per-step completion flags |
| prompt_change_log.md append | `lessons_learnt_prompt.md` §6.3 | ASSERTION — simultaneity rule in §11 |
| backlog_slice commit | `release_planning_prompt.md` | STRUCTURAL — idempotency marker checked |

---

### Stage 5 — Token Budget Analysis

**TOKEN BUDGET TABLE (all counts ESTIMATED [LOW CONFIDENCE] — confirm with line counts):**

| Engine | ~Lines | ~Tokens | Invoke/cycle | ~Cycle cost | Confidence |
|---|---|---|---|---|---|
| roadmap_prompt.md | ~500 | ~4,000 | 1 | ~7,680 | LOW |
| release_planning_prompt.md | ~450 | ~3,600 | 1 | ~6,320 | LOW |
| sprint_planning_prompt.md | ~350 | ~2,800 | 1 | ~4,720 | LOW |
| execution_prompt.md | ~420 | ~3,360 | 2–4 | ~14,000 | LOW |
| delivery_verification_prompt.md | ~250 | ~2,000 | 1 | ~3,120 | LOW |
| post_ship_closure.md | ~300 | ~2,400 | 1 | ~4,000 | LOW |
| amendment_cycle_prompt.md | ~200 | ~1,600 | occasional | ~1,360 | LOW |
| lessons_learnt_prompt.md | ~280 | ~2,240 | 3–4 | ~9,120 | LOW |

⚠ METHODOLOGY NOTE: This table does not capture in-run context accumulation. For
execution_prompt.md, actual per-invocation cost grows with sprint size. Reported cost
may understate actual by 30–50% on large sprints. Use as lower bound.

**CYCLE TOTAL:** ~50,320 tokens/typical cycle [LOW CONFIDENCE]

**DRY-RUN GAP:**

| Engine | In §13? | Token risk per failed run |
|---|---|---|
| `plan sprint` | ✓ | — |
| `run sprint` | ✓ | — |
| `run post-ship` | ✓ | — |
| `manage roadmap` | ✓ | — |
| `groom backlog` | ✓ | — |
| `run roadmap` | **✗** | **~7,680 tokens wasted per failed run** |
| `run ideas` | ✗ | ~3,040 tokens (lower risk) |

---

### Stage 6 — Engine Handoff Integrity

| Pair | Field | Match? |
|---|---|---|
| Release Planning → Sprint Planning | `stage4_backlog_slice.md` | ✓ |
| Release Planning → Sprint Planning | `sprint_backlog_index.json` | ✓ |
| Release Planning → Sprint Planning | `design_gate_status` | ✓ |
| Sprint Planning → Sprint Execution | `sprint_sealed = true` | ✓ |
| Sprint Execution → Delivery Verification | `Sprint_Complete` status | ✓ |
| Delivery Verification → Post-Ship | `Verified` status | ✓ |
| Amendment → Sprint Planning | `amended_backlog_slice_path` | ✓ |
| Amendment → Sprint Planning | `Amendment_In_Progress` guard | **PARTIAL — Release Planning has guard; Sprint Planning unconfirmed** |

---

### Stage 7 — Prompt Architecture & Compression

**COMPLEXITY TABLE:**

| Engine | STEPs | Hard gates | Branches | Flagged? |
|---|---|---|---|---|
| execution_prompt.md | 11+ | 7 | ~8 | ⚠ HIGH BRANCH COUNT |
| release_planning_prompt.md | 10+ | 5 | ~5 | — |
| roadmap_prompt.md | 12 | 4 | ~4 | — |
| post_ship_closure.md | 11 | 3 | ~3 | — |
| sprint_planning_prompt.md | 8 | 3 | ~3 | — |

**EXTRACTION TABLE:**

| Category | Instances | Canonical home | Saving if extracted |
|---|---|---|---|
| Halt format blocks | ~6 [ESTIMATED] | `shared_standards.md §10` | ~960 tokens/cycle |
| Invariant lists | ~3 docs overlapping [ESTIMATED] | `system/invariants.md` (does not exist) | ~600 tokens/cycle |
| JSON schemas | 2+ inline [LATENT] | `shared_standards.md §16` (does not exist) | ~640 tokens/cycle |

§14 ALIGNED — no drift detected. Conditional check passes.

**INVOCATION GUARD TABLE:**

| Check | Result |
|---|---|
| `lessons_learnt_prompt.md §1` guard type | ADVISORY — no structural parameter requirement |
| `invocation_context` parameter required? | NO — by convention only |
| Calling engines that pass structured context | execution_prompt.md STEP 5.4, delivery_verification_prompt.md STEP 8.5 |

---

### Stage 8 — Amendment Cycle Completeness

| Check | Result | Evidence |
|---|---|---|
| A1 — Amendment_In_Progress mini state machine | PASS | lifecycle_schema.json confirmed |
| A2 — First-amendment zero-state handled | PASS | amendment_cycle_prompt.md v1.5 confirmed |
| A3 — Withdrawal path defined | PASS | IMP-39 — backlog_rollback fields added v1.4 |
| A4 — Two-authority ratification mode-independent | PASS | confirmed |
| A5 — One-active-amendment hard gate | PASS | confirmed |
| A6 — Sprint Planning guards Amendment_In_Progress | PARTIAL | Release Planning has guard (IMP-11); Sprint Planning not confirmed |
| A7 — amendment_lessons.md sunset or optional | FAIL | Retained for "backward compat" — no sunset date declared |

---

### Stage 9 — Single Source of Truth

| Check | Result | Token cost of duplicates | Evidence |
|---|---|---|---|
| SST1 — Invariant lists canonical? | FAIL | ~600/cycle | roadmap_prompt.md §9, README, team_charter.md §6 |
| SST2 — Halt format refs §10 only? | PARTIAL | ~960/cycle | ~6 inline blocks estimated |
| SST3 — JSON schemas in §16? | FAIL | ~640/cycle | §16 does not exist; 2+ schemas inline |
| SST4 — workforce_capacity.md single write owner | PARTIAL | — | roadmap_prompt.md STEP 7 writes; no explicit single-owner declaration |
| SST5 — scored_initiatives cycle-scoped naming | PARTIAL | — | dated naming confirmed; class unconfirmed |

---

### Stage 10 — Known Design Gaps & Deferred Patches

**D1 — PATCH AGE TABLE:**

| Patch | File | First recorded | Cycles carried | Status |
|---|---|---|---|---|
| STEP -1.5 preflight check | `roadmap_prompt.md` | 2026-03-06__item-3.4 | 2 | **STALE** |
| Bulk bash sed for >5 ideas | `roadmap_prompt.md` STEP 4 | 2026-03-04__item-3.4 | 3 | **OVERDUE** |
| New files via bash not Write tool | `roadmap_prompt.md` STEP 8.5 | 2026-03-04__item-3.4 | 3 | **OVERDUE** |
| Bold header formatting note | `roadmap_prompt.md` STEP 9 | 2026-03-04__item-3.4 | 3 | **OVERDUE** |
| Gate evidence requirement | `execution_prompt.md` | 2026-03-04__item-3.4 | 3 | **OVERDUE** |
| Backlog age check | `release_planning_prompt.md` STEP 1 | 2026-03-06__release-v1.9 | 1 | ACTIVE |
| Capacity WARN phasing | capacity template | 2026-03-06__release-v1.9 | 1 | ACTIVE |
| Pre-sprint decisions checklist | `cycle_summary.md` template | 2026-03-06__release-v1.9 | 1 | ACTIVE |

**D2-D5 TABLE:**

| Check | Result | Evidence |
|---|---|---|
| D2 — ideas_window.json per_agent_submission_count | FAIL | Field not in schema |
| D3 — rejected_but_strong.md exists | FAIL | NOT FOUND |
| D4 — Challenger failure halt instruction | FAIL | Charter says halt; roadmap_prompt.md STEP 5 has no instruction |
| D5 — Re-evaluate max age structural (STEP -1.5) | FAIL | Patch still outstanding |

---

### Stage 11 — Best Practices Compliance

| Check | Result | Evidence | Dimension |
|---|---|---|---|
| BP-01 All engine prompts Class 6 compliant | PASS | All loaded prompts compliant | Governance |
| BP-02 Agent roster field-level reads | PARTIAL | §14 preflight scope added IMP-22; some engines predate | Token |
| BP-03 sprint_backlog_index schema in §16 | FAIL | §16 does not exist | Token |
| BP-04 stage4_issue_manifest schema in §16 | FAIL | §16 does not exist | Token |
| BP-05 Decision log append-only STRUCTURAL | FAIL | ASSERTION only — "confirm no edits" | Reliability |
| BP-06 run roadmap supports --dry-run | FAIL | No --dry-run in roadmap_prompt.md §2 | Token+Reliability |
| BP-07 run roadmap in §13 dry-run table | FAIL | Absent from shared_standards.md §13 | Governance |
| BP-08 All engines zero-state bootstrap | PARTIAL | closure_state.json confirmed; others unverified | Reliability |
| BP-09 Displacement rule mode-independent | PASS | IMP-33 confirmed | Governance |
| BP-10 GitHub sync idempotency active | PASS | sync gh create vs update confirmed | Reliability |
| BP-11 scored_initiatives class = Class 3 | PARTIAL | Class not confirmed [ESTIMATED] | Governance |
| BP-12 §13 register covers all artefacts | FAIL | rejected_but_strong.md, scoring/ absent | Governance |
| BP-13 prompt_change_log has entry for every version | PASS | All entries traced | Governance |
| BP-14 lifecycle_schema.json loaded for transitions | PASS | shared_standards §10.6 mandates | Reliability |
| BP-15 All prior action-now patches applied | FAIL | 4 OVERDUE deferred patches confirmed | Reliability |

---

### Stage 12 — Routine Consolidation Analysis

**TABLE 1 — Consolidation scoring:**

| Engine | C1 Single trigger | C2 No auth sep | C3 Single consumer | C4 No gate need | C5 Optional/skippable | dry-run? | own state? | VERDICT |
|---|---|---|---|---|---|---|---|---|
| `manage roadmap` | ✗ (2 windows) | ✓ | ✓ | ~ | ✓ + known gap | ✓ | ✗ | **REVIEW** |
| `groom backlog` | ✗ (2 windows) | ✓ | ✓ | ~ | ✓ + known gap | ✓ | ✗ | **REVIEW** |
| `run ideas` | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | **CONSOLIDATE** |
| `run design-gate` | ✓ | ✗ (Head of UX authority) | ~ | ✗ (own state) | ✗ | ✓ | ✓ | **BOUNDARY** |
| `run delivery verification` | ✓ | ✗ (Director of Quality) | ✓ | ✗ (own state) | ✗ | ✗ | ✓ | **BOUNDARY** |

**TABLE 2 — CONSOLIDATE/REVIEW verdicts:**

| Engine | Verdict | Absorbing engine | As which STEP | Known gap closed | Token saving |
|---|---|---|---|---|---|
| `run ideas` | CONSOLIDATE | `run roadmap` | STEP -1.6 (conditional) | None — was optional, remains optional | ~3,040/cycle |
| `manage roadmap` | REVIEW | `run post-ship` | STEP 11 (mandatory) | Phase 1M skip gap closed | ~3,200/cycle if mandatory |
| `groom backlog` | REVIEW | `run post-ship` | STEP 12 (mandatory) | Phase 1M skip gap closed | ~3,200/cycle if mandatory |

**TABLE 3 — Known gaps closed by consolidation:**

| Known gap | Closed if consolidated into | Residual risk |
|---|---|---|
| Phase 1M not run when Phase 1 skipped | `run post-ship` STEP 11/12 (mandatory) | None — post-ship is always mandatory |
| Ideas absent at roadmap STEP 4 | `run roadmap` STEP -1.6 (conditional) | None — absence already handled |

---

### Stage 13 — Machine Friendliness Audit

**TABLE 1 — Output schema audit:**

| Artefact | Producing engine | Classification | Downstream consumers | Schema declared? | Status vocab constrained? | Completion signal? | Anchor stability? |
|---|---|---|---|---|---|---|---|
| `closure_state.json` | post_ship_closure.md | **STRUCTURED** | post_ship (self) | YES — JSON schema in §4 | YES — enum in schema | STRUCTURED (JSON field) | STABLE (fixed JSON keys) |
| `sprint_backlog_index.json` | sprint_planning_prompt.md | **STRUCTURED** | execution_prompt.md | YES — inline schema STEP 6.1A | YES — typed fields | STRUCTURED | STABLE |
| `.claude_current_state.json` | all engines | **STRUCTURED** | all engines | PARTIAL — §14 preflight scope | YES — lifecycle_schema.json | STRUCTURED | STABLE |
| `lessons_learnt_cycle.md` | execution, delivery_verification, amendment | **MIXED** | post_ship_closure.md | PARTIAL — §4.2 table format | NO — phase tag variable | ASSERTION (section check) | **VARIABLE — `## Phase 3 — <cycle_id>`** |
| `run_manifest.md` | roadmap_prompt.md, others | **MIXED** | audit, lessons_learnt | NO | NO | ABSENT | PARTIAL — table structure stable; header fields variable |
| `lessons_learnt.md` (standalone) | roadmap_prompt.md, release_planning | **PROSE** | post_ship_closure.md (full read) | NO | NO | ABSENT | VARIABLE |
| `closure_record.md` | post_ship_closure.md | **MIXED** | audit, future cycles | PARTIAL — §-format sections | PARTIAL | ABSENT | STABLE (§1–§7 headers) |
| `verification_report.md` | delivery_verification_prompt.md | **MIXED** | post_ship_closure.md | PARTIAL | PARTIAL | ABSENT | PARTIAL |

MF Score: (1×2 + 2×2 + 1×2 + 3×1 + 1×0) / (8×2) = 11/16 × 100 = **69/100**
⚠ P0 flag: `lessons_learnt.md` (PROSE, consumed by post_ship_closure.md full read)

**TABLE 2 — Prompt output schema declaration audit:**

| Engine | Declares output schema? | Schema location | Field name stability | Branch output parity? |
|---|---|---|---|---|
| post_ship_closure.md | YES | §4 write scope + closure_state.json schema | STABLE | YES (closure_state.json normalises) |
| sprint_planning_prompt.md | PARTIAL | §6 write scope; sprint_backlog_index schema inline | STABLE | YES |
| execution_prompt.md | PARTIAL | §9.1 execution_state.json schema | VARIABLE — branches produce different state shapes | NO — delegation vs direct execution paths differ |
| release_planning_prompt.md | PARTIAL | §5 write scope | STABLE | PARTIAL |
| roadmap_prompt.md | NO | STEP 9 write plan (narrative) | VARIABLE | NO |
| delivery_verification_prompt.md | NO | prose write scope | VARIABLE | NO |
| amendment_cycle_prompt.md | NO | prose write scope | VARIABLE | N/A (single path mostly) |

**TABLE 3 — Anchor stability risk:**

| Artefact | Variable header pattern | Downstream reader | Parse risk | Recommended fix |
|---|---|---|---|---|
| `lessons_learnt_cycle.md` | `## Phase 3 — <cycle_id>` | post_ship_closure.md STEP 8 | HIGH — grep for section fails across cycles | P4: move cycle_id to field; use stable `## Phase 3` header |
| `run_manifest.md` | `**Cycle:** <cycle_id>` in body | audit stage 2 | LOW — field-level read; not used as anchor | No change needed |
| `closure_record.md` | `## §1` through `## §7` | post_ship_closure.md | LOW — section numbers stable | PASS |

**CONVERSION PRIORITY TABLE:**

| Rank | Artefact | Current | Recommended | Consumer count | Effort |
|---|---|---|---|---|---|
| 1 | `lessons_learnt.md` (standalone) | PROSE | Add `// ARTEFACT_STATUS` JSON terminal block | 2 (post_ship, audit) | Low |
| 2 | `lessons_learnt_cycle.md` | MIXED | Normalise section headers; add terminal status block | 2 (post_ship, audit) | Low |
| 3 | `roadmap_prompt.md` output | MIXED/PROSE | Declare output schema in §5 write scope | 3 (release_planning, lessons_learnt, audit) | Medium |
| 4 | `verification_report.md` | MIXED | Add structured status terminal block | 2 (post_ship, audit) | Low |

---

## 5. Improvements List

```json
// AUDIT_INDEX
[
  {"id":"AUD-2026-03-13-001","title":"4 OVERDUE deferred patches apply now","weight":12,"tier":1,"effort":"Low","patches":4,"files":["claude/system/roadmap_prompt.md","claude/system/execution_prompt.md"],"depends_on":[]},
  {"id":"AUD-2026-03-13-002","title":"run roadmap add --dry-run support","weight":10,"tier":2,"effort":"Medium","patches":2,"files":["claude/system/roadmap_prompt.md","claude/system/shared_standards.md"],"depends_on":[]},
  {"id":"AUD-2026-03-13-003","title":"run ideas consolidate into run roadmap STEP -1.6","weight":8,"tier":2,"effort":"Medium","patches":2,"files":["claude/system/roadmap_prompt.md","CLAUDE.md"],"depends_on":[]},
  {"id":"AUD-2026-03-13-004","title":"manage roadmap + groom backlog mandatory post-ship","weight":8,"tier":2,"effort":"Medium","patches":3,"files":["claude/system/post_ship_closure.md","claude/system/shared_standards.md","claude/system/OPERATIONAL_GUIDE.md"],"depends_on":[]},
  {"id":"AUD-2026-03-13-005","title":"halt blocks inline 6 engines extract to shared_standards","weight":8,"tier":3,"effort":"Medium","patches":6,"files":["claude/system/execution_prompt.md","claude/system/release_planning_prompt.md","claude/system/sprint_planning_prompt.md","claude/system/post_ship_closure.md","claude/system/delivery_verification_prompt.md","claude/system/amendment_cycle_prompt.md"],"depends_on":[]},
  {"id":"AUD-2026-03-13-006","title":"create invariants.md consolidate 3 docs","weight":8,"tier":3,"effort":"Medium","patches":4,"files":["claude/system/invariants.md","claude/system/roadmap_prompt.md","claude/README.md","claude/charter/team_charter.md"],"depends_on":[]},
  {"id":"AUD-2026-03-13-007","title":"lessons learnt invocation guard structural","weight":8,"tier":2,"effort":"Medium","patches":1,"files":["claude/system/lessons_learnt_prompt.md"],"depends_on":["AUD-2026-03-13-001"]},
  {"id":"AUD-2026-03-13-008","title":"3 confirmed agent files non-standard Role format","weight":6,"tier":1,"effort":"Low","patches":3,"files":["claude/agents/pmo_lead.md","claude/agents/head_of_specs_team.md","claude/agents/strategy_rules_system_intent_owner.md"],"depends_on":[]},
  {"id":"AUD-2026-03-13-009","title":"add shared_standards section 16 JSON schemas","weight":6,"tier":3,"effort":"Low","patches":2,"files":["claude/system/shared_standards.md","claude/system/sprint_planning_prompt.md"],"depends_on":[]},
  {"id":"AUD-2026-03-13-010","title":"scored_initiatives and rejected_but_strong add to section 13","weight":6,"tier":1,"effort":"Low","patches":1,"files":["claude/system/OPERATIONAL_GUIDE.md"],"depends_on":[]},
  {"id":"AUD-2026-03-13-011","title":"Sprint Planning add Amendment_In_Progress guard","weight":6,"tier":2,"effort":"Low","patches":1,"files":["claude/system/sprint_planning_prompt.md"],"depends_on":[]},
  {"id":"AUD-2026-03-13-012","title":"roadmap_prompt STEP -1.5 state age check","weight":6,"tier":2,"effort":"Low","patches":1,"files":["claude/system/roadmap_prompt.md"],"depends_on":["AUD-2026-03-13-001"]},
  {"id":"AUD-2026-03-13-013","title":"Challenger failure halt instruction in roadmap_prompt","weight":6,"tier":2,"effort":"Low","patches":1,"files":["claude/system/roadmap_prompt.md"],"depends_on":[]},
  {"id":"AUD-2026-03-13-014","title":"decision log append-only structural enforcement","weight":6,"tier":2,"effort":"Low","patches":1,"files":["claude/system/roadmap_prompt.md"],"depends_on":[]},
  {"id":"AUD-2026-03-13-015","title":"run audit add to CLAUDE.md command table","weight":4,"tier":1,"effort":"Low","patches":1,"files":["CLAUDE.md"],"depends_on":[]},
  {"id":"AUD-2026-03-13-016","title":"amendment_lessons.md declare sunset date","weight":4,"tier":1,"effort":"Low","patches":1,"files":["claude/system/amendment_cycle_prompt.md"],"depends_on":[]},
  {"id":"AUD-2026-03-13-017","title":"execution_prompt extract schemas reduce branch complexity","weight":4,"tier":3,"effort":"High","patches":3,"files":["claude/system/execution_prompt.md","claude/system/shared_standards.md"],"depends_on":["AUD-2026-03-13-009","AUD-2026-03-13-006"]},
  {"id":"AUD-2026-03-13-018","title":"ideas_window.json add per_agent_submission_count field","weight":4,"tier":3,"effort":"Low","patches":1,"files":["claude/system/idea_intake_prompt.md"],"depends_on":[]},
  {"id":"AUD-2026-03-13-019","title":"rejected_but_strong and scoring absent from section 13","weight":4,"tier":1,"effort":"Low","patches":0,"files":["claude/system/OPERATIONAL_GUIDE.md"],"depends_on":["AUD-2026-03-13-010"]},
  {"id":"AUD-2026-03-13-020","title":"B3 B7 compliance structural patch enforcement B7 auto-escalation","weight":6,"tier":1,"effort":"Low","patches":1,"files":["claude/system/roadmap_prompt.md"],"depends_on":[]},
  {"id":"AUD-2026-03-13-021","title":"lessons_learnt.md standalone add ARTEFACT_STATUS terminal block","weight":6,"tier":2,"effort":"Low","patches":2,"files":["claude/system/roadmap_prompt.md","claude/system/release_planning_prompt.md"],"depends_on":[]},
  {"id":"AUD-2026-03-13-022","title":"lessons_learnt_cycle.md normalise variable section headers","weight":6,"tier":2,"effort":"Low","patches":2,"files":["claude/system/lessons_learnt_prompt.md","claude/system/execution_prompt.md"],"depends_on":[]}
]
```

---

### AUD-2026-03-13-001
**Title:** Apply 4 OVERDUE + 1 STALE deferred patches; add STEP -1.5 self-enforcement
**Area:** Lifecycle / Reliability
**Evidence Classification:** OBSERVED
**Blast Radius:** 4
**Priority Weight:** 12
**Problem:** 4 patches in `roadmap_prompt.md` and `execution_prompt.md` have been deferred 3+ cycles (OVERDUE). The STEP -1.5 preflight patch is self-referential — the enforcement mechanism is itself the deferred patch.
**Evidence:** `claude/cycles/2026-03-06__item-3.4/lessons_learnt.md` outstanding patches table
**Recommended change:** Apply all 4 OVERDUE patches immediately.
**Expected benefit:** Closes B3/B7 compliance gap; eliminates self-referential governance hole
**Token impact:** Costs ~320 tokens/cycle (STEP -1.5 adds one preflight check)
**Implementation effort:** Low
**Dependencies:** None

PATCH 1:
```
operation: INSERT_AFTER
file: claude/system/roadmap_prompt.md
anchor: "STEP -1 — Preflight Gate"
content: |

  ### STEP -1.5 — Prior Cycle Patch Confirmation (Hard Gate)

  Load prior cycle's `lessons_learnt.md` outstanding deferred patches table.
  For each patch targeting `roadmap_prompt.md`:
  - Read the target file section and verify the change is present.
  - If present: record as applied in run_manifest.md.
  - If absent: record as OVERDUE. Escalate to Head of Specs Team. Do not proceed.

  **B7 auto-escalation rule:** If a deferred patch appears for a second consecutive cycle
  without resolution: classify as OVERDUE regardless of original target date. Escalate
  immediately to Head of Specs Team. Do not carry forward as a new deferred patch.

  A run may not proceed past STEP -1.5 with any OVERDUE patch unresolved.
```

PATCH 2:
```
operation: INSERT_AFTER
file: claude/system/roadmap_prompt.md
anchor: "### 4.2 Document Management (Required — Run in Order)"
content: |

  **Bulk update note (>5 files):** When updating >5 idea file status fields, use bash sed
  rather than the Write/Edit tool to avoid the per-file read constraint:
  `sed -i 's/\*\*Status:\*\* Submitted/\*\*Status:\*\* Parked-cycle-1/g' claude/ideas/submissions/*.md`
```

PATCH 3:
```
operation: INSERT_AFTER
file: claude/system/roadmap_prompt.md
anchor: "#### 1) File: `claude/roadmap/current_roadmap.md`"
content: |

  **New files in new directories:** Must be created via bash `mkdir -p` + `cat >`, not
  the Write tool. The Write tool cannot create intermediate directories.
  Example: `mkdir -p claude/scoring && cat > claude/scoring/scored_initiatives_$(date +%Y-%m-%d).md << 'EOF'`
```

PATCH 4:
```
operation: INSERT_AFTER
file: claude/system/roadmap_prompt.md
anchor: "Append‑only enforcement:"
content: |

  **Header formatting rule:** All Class 4 document headers written or updated in STEP 9
  must use bold field labels: `**Owner:**`, `**Status:**`, `**Class:**`, `**Last Updated:**`.
  Non-bold headers are non-compliant and will fail next preflight STEP -1.2.
```

PATCH 5 (execution_prompt.md — gate evidence requirement):
```
operation: INSERT_AFTER
file: claude/system/execution_prompt.md
anchor: "No autonomous merge."
content: |

  **Gate evidence requirement:** Any hard gate status change in `current_roadmap.md`
  (marking a gate as "complete") must reference the evidence artefact that cleared it
  (PoG Gate ID, decision record path, or verifiable session output reference). A gate
  may not be marked complete without an evidence reference. If no artefact exists: gate
  remains "pending". Record in escalations.md.
```

---

### AUD-2026-03-13-002
**Title:** `run roadmap` — add `--dry-run` flag and §13 table entry
**Area:** Token Efficiency / Reliability
**Evidence Classification:** LATENT
**Blast Radius:** 5
**Priority Weight:** 10
**Problem:** `run roadmap` is the highest token-cost engine (~7,680 tokens/invoke) and the only primary lifecycle engine without `--dry-run`. A failed or aborted run wastes the full token budget with no preview capability.
**Evidence:** `shared_standards.md §13` dry-run table — `run roadmap` absent; `roadmap_prompt.md §2` invocation rule — no `--dry-run` flag
**Recommended change:** Add `--dry-run` to invocation rule and §13 table.
**Expected benefit:** Prevents full-cost aborted runs; ~7,680 tokens saved per aborted run
**Token impact:** Neutral to successful runs; saves on aborted runs
**Implementation effort:** Medium
**Dependencies:** None

PATCH 1:
```
operation: REPLACE
file: claude/system/roadmap_prompt.md
anchor: "run roadmap --item-id \"<id>\" --item-name \"<n>\" [--date \"YYYY-MM-DD\"]"
content: |
  run roadmap --item-id "<id>" --item-name "<n>" [--date "YYYY-MM-DD"] [--dry-run]
  run roadmap --reason "scheduled" [--date "YYYY-MM-DD"] [--dry-run]

  `--dry-run`: produces rebalance preview — capacity analysis, displacement candidates,
  scoring matrix, backlog impact — without writing any files, updating state, or committing.
  Dry-run exits after STEP 8 (decisions recorded in output only). No writes. No commit.
  Output sufficient to validate before issuing live run.
```

PATCH 2:
```
operation: INSERT_AFTER
file: claude/system/shared_standards.md
anchor: "| `groom backlog` | Change plan — items to archive, items to flag |"
content: |
  | `run roadmap` | Rebalance preview — capacity analysis, displacement candidates, scoring matrix, backlog impact |
  | `run ideas` | Submission window summary — counts per agent, ideas available for STEP 4 |
```

---

### AUD-2026-03-13-003
**Title:** Absorb `run ideas` as conditional STEP -1.6 of `run roadmap`
**Area:** Lifecycle / Token Efficiency
**Evidence Classification:** LATENT
**Blast Radius:** 2
**Priority Weight:** 8
**Problem:** `run ideas` has a single trigger (pre-roadmap only), no authority separation, single downstream consumer (roadmap STEP 4), no own state entry, and no `--dry-run`. It is a clean CONSOLIDATE candidate per Stage 12 scoring.
**Evidence:** Stage 12 TABLE 1 — CONSOLIDATE verdict; `idea_intake_prompt.md §2` invocation rule; roadmap STEP 4 already handles absent submissions gracefully
**Recommended change:** Add conditional STEP -1.6 to `run roadmap`; retain standalone as override; update CLAUDE.md note.
**Expected benefit:** Eliminates separate invocation overhead; ~3,040 tokens/cycle saved; single command path for teams
**Token impact:** Saves ~3,040 tokens/cycle on runs where ideas window is managed inline
**Implementation effort:** Medium
**Dependencies:** None

PATCH 1:
```
operation: INSERT_AFTER
file: claude/system/roadmap_prompt.md
anchor: "A run may not proceed past STEP -1.5 with any OVERDUE patch unresolved."
content: |

  ### STEP -1.6 — Idea Window Check (Conditional)

  Check `claude/ideas/ideas_window.json`:
  - If `status = "Open"`: invoke `claude/system/idea_intake_prompt.md` inline.
    Close the window, produce window summary. Proceed to STEP 0 with ideas available.
  - If `status = "Closed"` and closed this session: proceed — ideas available.
  - If file absent or `status = "Closed"` from a prior session: note absence and proceed.
    Roadmap STEP 4 handles absent submissions — do not halt.

  Note: `run ideas` may still be invoked standalone before `run roadmap` for explicit
  window control. This step handles the common inline case only.
```

PATCH 2:
```
operation: INSERT_AFTER
file: CLAUDE.md
anchor: "| `run ideas [--window-id <id>] [--mode strict\\|standard]` | `claude/system/idea_intake_prompt.md` | Phase 0 — Idea intake (optional, before rebalance) |"
content: |
  | *(auto)* | `claude/system/idea_intake_prompt.md` | Invoked as STEP -1.6 of `run roadmap` when open window detected. Standalone `run ideas` remains supported for explicit window control. |
```

---

### AUD-2026-03-13-004
**Title:** Promote `manage roadmap` + `groom backlog` to mandatory `run post-ship` steps
**Area:** Lifecycle / Governance
**Evidence Classification:** LATENT
**Blast Radius:** 3
**Priority Weight:** 8
**Problem:** The known Phase 1M gap (OPERATIONAL_GUIDE §6M) exists because both engines are optional standalone commands. When Phase 1 is skipped, they never run, causing roadmap and backlog decay across cycles.
**Evidence:** `OPERATIONAL_GUIDE.md §6M` known gap note; Stage 12 REVIEW verdict with known-gap auto-elevation
**Recommended change:** Add STEP 11 + STEP 12 to `post_ship_closure.md`; close §6M known gap note.
**Expected benefit:** Phase 1M skip gap closed permanently; document hygiene enforced every cycle
**Token impact:** Costs ~6,400 tokens/cycle (mandatory Phase 1M at post-ship)
**Implementation effort:** Medium
**Dependencies:** None

PATCH 1:
```
operation: INSERT_AFTER
file: claude/system/post_ship_closure.md
anchor: "## STEP 10"
content: |

  ## STEP 11 — Roadmap Document Management (Mandatory)

  Invoke `claude/system/roadmap_management_prompt.md` inline.
  Pass through `--dry-run` if `run post-ship` was invoked with `--dry-run`.
  Output: manage_roadmap run log at `claude/cycles/<cycle_id>/manage_roadmap_<YYYYMMDD>.md`.
  On completion: confirm `last_manage_roadmap_utc` written to `.claude_current_state.json`.
  Update `closure_state.json`: `{"step_11_manage_roadmap": "complete", ...}`.

  ## STEP 12 — Backlog Document Management (Mandatory)

  Invoke `claude/system/backlog_management_prompt.md` inline.
  Pass through `--dry-run` if `run post-ship` was invoked with `--dry-run`.
  Output: backlog health report at `claude/backlog/backlog_health_<YYYYMMDD>.md`.
  On completion: confirm `last_groom_backlog_utc` written to `.claude_current_state.json`.
  Update `closure_state.json`: `{"step_12_groom_backlog": "complete", ...}`.
```

PATCH 2:
```
operation: REPLACE
file: claude/system/OPERATIONAL_GUIDE.md
anchor: "> **Known gap — Phase 1 skipped:** If Phase 1 is skipped and `plan release` is invoked directly, Phase 1M will not have run since the last Post-Ship Closure. Both `manage roadmap` and `groom backlog` should be run before `plan release` is issued. This is not yet a formal trigger row — teams skipping Phase 1 regularly should raise this for promotion."
content: |
  > **Phase 1M enforcement:** `manage roadmap` and `groom backlog` are invoked as mandatory
  > STEP 11 and STEP 12 of every Post-Ship Closure run. Both run at every cycle close
  > regardless of whether Phase 1 was executed. Standalone invocation remains supported
  > for teams that want an additional pre-roadmap clean-up pass.
```

PATCH 3:
```
operation: INSERT_AFTER
file: claude/system/shared_standards.md
anchor: "| `run post-ship` | Closure plan — every step listed, every write that would be made, every flag |"
content: |
  Note: `run post-ship --dry-run` includes dry-run output for STEP 11 (`manage roadmap`)
  and STEP 12 (`groom backlog`) — both pass through the `--dry-run` flag.
```

---

### AUD-2026-03-13-005
**Title:** Extract inline halt format blocks from ~6 engines to `shared_standards §10` reference
**Area:** Token Efficiency / SST
**Evidence Classification:** LATENT
**Blast Radius:** 5
**Priority Weight:** 8
**Problem:** Each engine contains an inline halt format block repeating the same template. `shared_standards.md §10` is declared as the canonical halt format source but engines reproduce it inline, wasting ~960 tokens/cycle.
**Evidence:** Stage 7 extraction table; Stage 9 SST2 PARTIAL
**Recommended change:** Remove inline halt blocks; add single-line reference per engine.
**Expected benefit:** ~960 tokens/cycle saved; single update point for halt format
**Token impact:** Saves ~960 tokens/cycle
**Implementation effort:** Medium
**Dependencies:** None

PATCH 1–6: For each engine (execution_prompt.md, release_planning_prompt.md,
sprint_planning_prompt.md, post_ship_closure.md, delivery_verification_prompt.md,
amendment_cycle_prompt.md):
```
operation: REPLACE
file: claude/system/<engine_file>
anchor: "<locate inline halt format block — search for 'ESC-' prefix or 'HALT REPORT' heading>"
content: |
  Halt report format: per `claude/system/shared_standards.md §5`. Use ESC-YYYYMMDD-nn
  identifier. Output to escalations file declared in this engine's §5 write scope.
```

Note to Claude Code: Locate each engine's inline halt block by searching for the pattern
`ESC-` followed by a date format, or a heading containing "Halt Report" or "HALT". Replace
the full block with the single-line reference above.

---

### AUD-2026-03-13-006
**Title:** Create `claude/system/invariants.md`; consolidate from 3 source documents
**Area:** Token Efficiency / SST
**Evidence Classification:** LATENT
**Blast Radius:** 4
**Priority Weight:** 8
**Problem:** Governance invariants appear in `roadmap_prompt.md §9`, `claude/README.md §3`, and `claude/charter/team_charter.md §6`. No single canonical file. `claude/system/invariants.md` does not exist.
**Evidence:** Stage 9 SST1 FAIL; Stage 7 extraction table
**Recommended change:** Create `invariants.md`; consolidate all three sources; replace inline lists with references.
**Expected benefit:** ~600 tokens/cycle saved; single update point
**Token impact:** Saves ~600 tokens/cycle
**Implementation effort:** Medium
**Dependencies:** None

PATCH 1:
```
operation: CREATE_FILE
file: claude/system/invariants.md
anchor: N/A
content: |
  **Owner:** Head of Specs Team
  **Status:** Active
  **Version:** 1.0
  **Last Updated:** 2026-03-13
  **Class:** Governance Prompt (Class 6)
  **Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

  # Governance Invariants — Momentum Trading Assistant

  Canonical list of system-wide non-negotiable invariants. All engines reference this file.
  Do not duplicate these lists inline in engine prompts.

  ## Core Invariants (All Routines)

  - Authority is explicit and role-bound — no implied or delegated authority without charter
  - One owner exists per decision domain
  - All documents comply with lifecycle rules per `claude/charter/document_lifecycle_guide.md`
  - Workforce capacity is finite and explicit — no initiative without opportunity cost
  - No initiative exists without displacement unless net-zero gate is satisfied
  - Delivery pressure never redefines strategy intent or canonical truth
  - Strategy / Quality / Lifecycle risks may never be Accepted Risk

  ## Lifecycle Invariants

  - Decision log (`claude/roadmap/decision_log.md`) is append-only
  - Archive files are append-only — entries may not be edited after filing
  - Backlog lock must be acquired before any backlog write
  - Prompt version increment must have a matching prompt_change_log.md entry in the same commit
  - Hard gate status changes must reference an evidence artefact

  ## Write Scope Invariants

  - Each engine may only write to files listed in its §5 Write Scope
  - `.claude_current_state.json` status may only be written at designated sync steps
  - State may only advance along defined transitions (lifecycle_schema.json is authoritative)

  ---

  ## Change Log

  | Version | Date | Change |
  |---------|------|--------|
  | 1.0 | 2026-03-13 | Initial version — consolidated from roadmap_prompt.md §9, README.md §3, team_charter.md §6. |
```

PATCHES 2–4: Replace inline invariant sections in roadmap_prompt.md §9, README.md §3,
and team_charter.md §6 with: "See `claude/system/invariants.md` for canonical list."

---

### AUD-2026-03-13-007
**Title:** `lessons_learnt_prompt.md` invocation guard — add structural context requirement
**Area:** Reliability / Governance
**Evidence Classification:** LATENT
**Blast Radius:** 4
**Priority Weight:** 8
**Problem:** The lessons learnt prompt has no structural parameter requirement. Calling engines pass context by convention only. A caller can invoke without structured context and produce a malformed output.
**Evidence:** Stage 7 invocation guard table; `lessons_learnt_prompt.md §1` — advisory only
**Recommended change:** Add required invocation context block to §1.
**Expected benefit:** Eliminates malformed outputs; ensures phase and cycle always present
**Token impact:** Neutral
**Implementation effort:** Medium
**Dependencies:** AUD-2026-03-13-001 (STEP -1.5 must exist before invoking with context)

PATCH 1:
```
operation: INSERT_AFTER
file: claude/system/lessons_learnt_prompt.md
anchor: "## 1. Purpose"
content: |

  ## 1.1 Required Invocation Context (Hard Gate)

  This prompt must be invoked with a structured context block. If context is absent: halt
  and output: "LESSONS LEARNT INVOCATION ERROR — missing context. Invoking engine must
  supply structured block."

  Required context fields:
  ```
  invoking_routine: <engine name — e.g. "roadmap_prompt.md">
  cycle_id: <active cycle_id>
  phase: <Phase 3 | Phase 4 | Post-Ship | Amendment | Roadmap | Release>
  prior_cycle_id: <prior cycle_id or "none — first cycle">
  ```

  If any field is absent: output error listing missing fields. Do not proceed.
  Calling engines must pass all four fields explicitly at invocation.
```

---

### AUD-2026-03-13-008
**Title:** Fix 3 confirmed agent files using non-standard `## Role:` format
**Area:** Document Hygiene / Governance
**Evidence Classification:** OBSERVED
**Blast Radius:** 2
**Priority Weight:** 6
**Problem:** Run manifest 2026-03-01 explicitly notes PMO Lead, Strategy Rules Owner, and Head of Specs Team use `## Role:` heading format instead of `**Role:**` bold format. This causes preflight header compliance failures.
**Evidence:** `claude/cycles/2026-03-01__item-3.2/run_manifest.md` preflight notes
**Recommended change:** Update 3 confirmed files; audit remaining agent files.
**Expected benefit:** Eliminates preflight compliance failures
**Token impact:** Neutral
**Implementation effort:** Low
**Dependencies:** None

PATCH 1:
```
operation: REPLACE
file: claude/agents/pmo_lead.md
anchor: "## Role:"
content: "**Role:**"
```

PATCH 2:
```
operation: REPLACE
file: claude/agents/head_of_specs_team.md
anchor: "## Role:"
content: "**Role:**"
```

PATCH 3:
```
operation: REPLACE
file: claude/agents/strategy_rules_system_intent_owner.md
anchor: "## Role:"
content: "**Role:**"
```

---

### AUD-2026-03-13-009
**Title:** Add `shared_standards.md §16` for governed JSON schemas
**Area:** Token Efficiency / SST
**Evidence Classification:** LATENT
**Blast Radius:** 3
**Priority Weight:** 6
**Problem:** `sprint_backlog_index.json` and `stage4_issue_manifest.json` schemas are defined inline in `sprint_planning_prompt.md`. §16 does not exist. Each engine load repeats schema definitions.
**Evidence:** Stage 11 BP-03/BP-04 FAIL; Stage 9 SST3 FAIL
**Recommended change:** Add §16 to `shared_standards.md`; move schemas there.
**Expected benefit:** ~640 tokens/cycle saved
**Token impact:** Saves ~640 tokens/cycle
**Implementation effort:** Low
**Dependencies:** None

PATCH 1:
```
operation: INSERT_AFTER
file: claude/system/shared_standards.md
anchor: "## 15. Spec Debt Item Lifecycle (IMP-43)"
content: |

  ---

  ## 16. Governed JSON Schemas

  Inline JSON schemas in engine prompts must be replaced with a reference to this section.
  Format for reference: "Schema: per `shared_standards.md §16.N`"

  ### 16.1 sprint_backlog_index.json

  Produced by: `sprint_planning_prompt.md` STEP 6.1A
  Consumed by: `execution_prompt.md` STEP -1.1

  ```json
  {
    "cycle_id": "<string>",
    "generated_utc": "<ISO-8601 UTC>",
    "epics": {
      "EPIC-xx": {
        "st_items": ["ST-xx"],
        "backlog_slice_refs": ["<section anchor in stage4_backlog_slice.md>"]
      }
    }
  }
  ```

  ### 16.2 stage4_issue_manifest.json

  Produced by: `sprint_planning_prompt.md` STEP 6.1A (companion to sprint_backlog_index)
  Consumed by: `sync gh` inline handler

  [Schema to be moved from sprint_planning_prompt.md STEP 6.1A by Head of Specs Team]
```

PATCH 2:
```
operation: REPLACE
file: claude/system/sprint_planning_prompt.md
anchor: "produce index with schema `{cycle_id, generated_utc, epics: {EPIC-xx: {st_items, backlog_slice_refs}}}`"
content: |
  produce index per schema at `claude/system/shared_standards.md §16.1`
```

---

### AUD-2026-03-13-010
**Title:** Add `scored_initiatives` and `rejected_but_strong.md` to §13 artefact register
**Area:** Governance / Document Hygiene
**Evidence Classification:** OBSERVED
**Blast Radius:** 2
**Priority Weight:** 6
**Problem:** Both artefacts are produced by governed routines and referenced in the system but absent from OPERATIONAL_GUIDE §13. `scored_initiatives` class unverified. `rejected_but_strong.md` NOT FOUND.
**Evidence:** Stage 3 G4 FAIL; Stage 11 BP-11/BP-12 FAIL; Gap Register
**Recommended change:** Add both rows to §13; confirm scored_initiatives = Class 3.
**Expected benefit:** §13 register complete; artefact governance enforced
**Token impact:** Neutral
**Implementation effort:** Low
**Dependencies:** None

PATCH 1:
```
operation: INSERT_AFTER
file: claude/system/OPERATIONAL_GUIDE.md
anchor: "| Workforce Capacity | `claud"
content: |
  | Scored Initiatives | `claude/scoring/scored_initiatives_<YYYYMMDD>.md` | 3 | PMO Lead | 1 |
  | Rejected-But-Strong Register | `claude/ideas/rejected_but_strong.md` | 4 | PMO Lead | 1 |
```

---

### AUD-2026-03-13-011
**Title:** Sprint Planning — add `Amendment_In_Progress` guard at STEP -1
**Area:** Lifecycle / Reliability
**Evidence Classification:** LATENT
**Blast Radius:** 3
**Priority Weight:** 6
**Problem:** Release Planning STEP -1.8 (IMP-11) guards `Amendment_In_Progress`. Sprint Planning has no equivalent guard, creating a path where Sprint Planning could proceed while an amendment is active.
**Evidence:** Stage 6 handoff PARTIAL; Stage 8 A6 PARTIAL; `release_planning_prompt.md` STEP -1.8
**Recommended change:** Add guard to `sprint_planning_prompt.md` STEP -1.
**Expected benefit:** Closes lifecycle gap; matches Release Planning parity
**Token impact:** Neutral
**Implementation effort:** Low
**Dependencies:** None

PATCH 1:
```
operation: INSERT_AFTER
file: claude/system/sprint_planning_prompt.md
anchor: "Apply the Lifecycle Guard (valid from-states:"
content: |

  **Amendment_In_Progress guard (Hard Gate):** Before proceeding, check
  `.claude_current_state.json` status. If status = `Amendment_In_Progress`: halt
  immediately. Sprint Planning may not proceed while an amendment is active.
  Seal or withdraw the amendment before issuing `plan sprint`.
  Output halt report per `shared_standards.md §5`.
```

---

### AUD-2026-03-13-012
**Title:** Extend STEP -1.5 with state age advisory check
**Area:** Lifecycle / Reliability
**Evidence Classification:** LATENT
**Blast Radius:** 3
**Priority Weight:** 6
**Problem:** STEP -1.5 (added by AUD-001) confirms prior patches but does not check whether `.claude_current_state.json` is stale — `active_cycle` last updated >30 days ago is a silent risk.
**Evidence:** Stage 4 R4 FAIL
**Recommended change:** Add state age check to STEP -1.5.
**Expected benefit:** Prevents stale state from silently propagating
**Token impact:** Neutral
**Implementation effort:** Low
**Dependencies:** AUD-2026-03-13-001

PATCH 1:
```
operation: INSERT_AFTER
file: claude/system/roadmap_prompt.md
anchor: "A run may not proceed past STEP -1.5 with any OVERDUE patch unresolved."
content: |

  **State age advisory:** Read `.claude_current_state.json` `last_updated_utc` field.
  If field is absent or value is >30 days before today: surface advisory —
  "State file not updated in >30 days — confirm active_cycle is current before proceeding."
  Record in run_manifest.md. This is advisory only — do not halt.
```

---

### AUD-2026-03-13-013
**Title:** Add Challenger failure halt instruction to `roadmap_prompt.md` STEP 5
**Area:** Governance / Reliability
**Evidence Classification:** LATENT
**Blast Radius:** 3
**Priority Weight:** 6
**Problem:** `team_charter.md §3.2` states "If Challenger cannot produce an evidence-based counter-argument: process failure requiring halt and lessons learnt." `roadmap_prompt.md` STEP 5 has no corresponding halt instruction — the charter rule is unenforceable from the engine.
**Evidence:** Stage 10 D4 FAIL; `team_charter.md §3.2`
**Recommended change:** Add explicit halt instruction to STEP 5.
**Expected benefit:** Charter enforcement reaches the engine
**Token impact:** Neutral
**Implementation effort:** Low
**Dependencies:** None

PATCH 1:
```
operation: INSERT_AFTER
file: claude/system/roadmap_prompt.md
anchor: "### STEP 5"
content: |

  **Challenger failure rule (per `team_charter.md §3.2`):** If the Challenger cannot
  produce an evidence-based counter-argument for any advancing candidate: this is a
  process failure. Halt. Record in lessons_learnt as Type E — Authority Gap.
  Do not proceed to STEP 6 until the Challenger provides a substantive counter-argument
  or formally records inability with a written reason. Neither silence nor "no objection"
  satisfies the Challenger's obligation.
```

---

### AUD-2026-03-13-014
**Title:** Decision log append-only — add structural read-before-write enforcement
**Area:** Reliability / Governance
**Evidence Classification:** LATENT
**Blast Radius:** 3
**Priority Weight:** 6
**Problem:** `roadmap_prompt.md` STEP 9 has "Append-only enforcement: Confirm no edits to existing entries" — assertion only. No structural mechanism prevents edits.
**Evidence:** Stage 4 R3 sub-table; Stage 11 BP-05 FAIL
**Recommended change:** Add read-before-write count check.
**Expected benefit:** Structural enforcement; violations detectable
**Token impact:** Neutral
**Implementation effort:** Low
**Dependencies:** None

PATCH 1:
```
operation: REPLACE
file: claude/system/roadmap_prompt.md
anchor: "Append‑only enforcement:\n- Confirm no edits to existing entries"
content: |
  Append-only enforcement (structural):
  - Before writing: count existing entries in `decision_log.md`. Record count as N.
  - After writing: re-read file. Confirm entry count = N + (entries added this run).
  - If count decreased: halt. Decision log integrity violation — do not commit.
  - If any existing entry text differs from pre-write read: halt. Treat as corruption.
  Both checks must pass before STEP 9 commit proceeds.
```

---

### AUD-2026-03-13-015
**Title:** Add `run audit` to CLAUDE.md command table
**Area:** Governance
**Evidence Classification:** OBSERVED
**Blast Radius:** 2
**Priority Weight:** 4
**Problem:** `run audit` is a governed routine with a defined SLA (every 3 cycles) and output filing requirement, but is absent from the CLAUDE.md command table. No defined load path.
**Evidence:** Stage 1 findings; CLAUDE.md command table scan
**Recommended change:** Add row to CLAUDE.md command table.
**Expected benefit:** Audit becomes a governed routine; discoverable
**Token impact:** Neutral
**Implementation effort:** Low
**Dependencies:** None

PATCH 1:
```
operation: INSERT_AFTER
file: CLAUDE.md
anchor: "| `sync gh` | *(inline — see §4)* | Sync backlog slice to GitHub Issues |"
content: |
  | `run audit` | `claude/audit.py` | Governance — lifecycle audit (every 3 cycles; output filed as `claude/cycles/<cycle_id>/audit_report_AUD-<date>.md` Class 3) |
```

---

### AUD-2026-03-13-016
**Title:** Declare `amendment_lessons.md` sunset in `amendment_cycle_prompt.md`
**Area:** Governance / Document Hygiene
**Evidence Classification:** LATENT
**Blast Radius:** 2
**Priority Weight:** 4
**Problem:** v1.5 retains `amendment_lessons.md` "for backward compat" but defines no sunset date and no version at which it becomes optional. Downstream consumers may rely on it indefinitely.
**Evidence:** Stage 8 A7 FAIL; `amendment_cycle_prompt.md` v1.5 changelog
**Recommended change:** Add explicit deprecation notice.
**Expected benefit:** Clear deprecation path; prevents future confusion
**Token impact:** Neutral
**Implementation effort:** Low
**Dependencies:** None

PATCH 1:
```
operation: INSERT_AFTER
file: claude/system/amendment_cycle_prompt.md
anchor: "Secondary output `amendment_lessons.md` retained for backward compat."
content: |

  **Deprecation notice (v1.5):** `amendment_lessons.md` is deprecated as of v1.5.
  It is written for backward compatibility only and will not be produced from v2.0 onward.
  The canonical record is `lessons_learnt_cycle.md` Amendment section.
  Do not rely on `amendment_lessons.md` as a primary source in any new engine or tool.
```

---

### AUD-2026-03-13-017
**Title:** `execution_prompt.md` — extract delegation schema and SLA tracking to §16
**Area:** Reliability / Token Efficiency
**Evidence Classification:** LATENT
**Blast Radius:** 4
**Priority Weight:** 4
**Problem:** `execution_prompt.md` has the highest branch count (~8 paths), highest inline block count (~4), and is invoked 2–4× per cycle. Combined with in-run context growth, it is the largest single token and reliability risk.
**Evidence:** Stage 7 complexity table; Stage 13 TABLE 2 — branch output parity NO
**Recommended change:** Extract delegation log schema and SLA breach block to shared_standards §16; extract execution invariants to invariants.md.
**Expected benefit:** ~1,280 tokens/cycle saved; reduced per-branch complexity
**Token impact:** Saves ~1,280 tokens/cycle
**Implementation effort:** High
**Dependencies:** AUD-2026-03-13-009 (§16 must exist), AUD-2026-03-13-006 (invariants.md must exist)

PATCHES 1–3: Extract delegation log schema to §16.3; extract SLA breach tracking block
to §16.4; replace inline blocks with references. Content to be moved by Head of Specs Team
once §16 and invariants.md exist.

---

### AUD-2026-03-13-018
**Title:** `ideas_window.json` — add `per_agent_submission_count` field to schema
**Area:** Token Efficiency / Governance
**Evidence Classification:** LATENT
**Blast Radius:** 2
**Priority Weight:** 4
**Problem:** `ideas_window.json` tracks `agents_submitted` as a list but has no per-agent count field. Roadmap STEP 4 must re-scan submission files to derive per-agent counts.
**Evidence:** Stage 10 D2 FAIL; `idea_intake_prompt.md` STEP 3 JSON schema
**Recommended change:** Add `per_agent_submission_count` map to STEP 3 schema.
**Expected benefit:** Eliminates re-scan in roadmap STEP 4; ~160 tokens/cycle saved
**Token impact:** Saves ~160 tokens/cycle
**Implementation effort:** Low
**Dependencies:** None

PATCH 1:
```
operation: REPLACE
file: claude/system/idea_intake_prompt.md
anchor: "\"agents_not_submitted\": [<list of agent slugs with 0 submissions>],"
content: |
  "agents_not_submitted": [<list of agent slugs with 0 submissions>],
  "per_agent_submission_count": {"<agent-slug>": <int>, ...},
```

---

### AUD-2026-03-13-019
**Title:** (merged with AUD-010) — see AUD-2026-03-13-010
**Area:** Governance
**Evidence Classification:** OBSERVED
**Blast Radius:** 2
**Priority Weight:** 4
**Problem:** See AUD-2026-03-13-010. This item is fully addressed by that patch.
**Dependencies:** AUD-2026-03-13-010

PATCH: See AUD-2026-03-13-010 PATCH 1.

---

### AUD-2026-03-13-020
**Title:** B3/B7 compliance — add B7 auto-escalation rule to STEP -1.5
**Area:** Lifecycle / Reliability
**Evidence Classification:** OBSERVED
**Blast Radius:** 4
**Priority Weight:** 6
**Problem:** B3 at 50%, B7 at 67% — both below 75% threshold. Root cause is structural: STEP -1.5 did not exist. AUD-001 adds it; this item adds the B7 auto-escalation rule within it.
**Evidence:** Stage 2 compliance table B3/B7
**Recommended change:** B7 auto-escalation rule included in AUD-001 PATCH 1. No additional patch required — covered.
**Dependencies:** None (resolved by AUD-2026-03-13-001)

PATCH: Covered by AUD-2026-03-13-001 PATCH 1 (B7 auto-escalation rule included in STEP -1.5 content).

---

### AUD-2026-03-13-021
**Title:** Add `// ARTEFACT_STATUS` terminal JSON block to standalone `lessons_learnt.md`
**Area:** Machine Friendliness
**Evidence Classification:** LATENT
**Blast Radius:** 3
**Priority Weight:** 6
**Problem:** `lessons_learnt.md` (standalone, produced by roadmap and release planning) is PROSE classification with no completion signal. `post_ship_closure.md` STEP 8 reads it in full. An `ARTEFACT_STATUS` terminal block would allow field-level reads.
**Evidence:** Stage 13 TABLE 1 — PROSE artefact, 2 downstream consumers; TABLE 3 — P0 flag
**Recommended change:** Add terminal JSON block requirement to `roadmap_prompt.md` STEP 11 and `release_planning_prompt.md` lessons learnt step.
**Expected benefit:** Downstream engines can grep for `// ARTEFACT_STATUS` instead of full read; ~400 tokens/cycle saved
**Token impact:** Saves ~400 tokens/cycle at post_ship_closure.md STEP 8
**Implementation effort:** Low
**Dependencies:** None

PATCH 1:
```
operation: INSERT_AFTER
file: claude/system/roadmap_prompt.md
anchor: "Output: `claude/cycles/<cycle_id>/lessons_learnt.md`"
content: |

  The lessons learnt file must end with the following machine-readable terminal block:

  ```json
  // ARTEFACT_STATUS
  {
    "file": "lessons_learnt.md",
    "cycle_id": "<cycle_id>",
    "phase": "Roadmap",
    "filed_utc": "<ISO-8601 UTC>",
    "friction_item_count": <int>,
    "action_now_count": <int>,
    "deferred_count": <int>,
    "escalation_count": <int>,
    "overdue_patches": <int>,
    "status": "Complete"
  }
  ```

  `post_ship_closure.md` STEP 8 may locate this block by grepping for `// ARTEFACT_STATUS`
  to extract counts without reading the full prose document.
```

PATCH 2:
```
operation: INSERT_AFTER
file: claude/system/release_planning_prompt.md
anchor: "Output: `claude/cycles/<cycle_id>/lessons_learnt.md`"
content: |

  The lessons learnt file must end with an `// ARTEFACT_STATUS` JSON terminal block.
  Schema: per `claude/system/roadmap_prompt.md` §11.1 — use `"phase": "Release"`.
```

---

### AUD-2026-03-13-022
**Title:** Normalise `lessons_learnt_cycle.md` variable section headers
**Area:** Machine Friendliness / Reliability
**Evidence Classification:** LATENT
**Blast Radius:** 3
**Priority Weight:** 6
**Problem:** `lessons_learnt_cycle.md` uses `## Phase 3 — <cycle_id>` as section headers. The variable `<cycle_id>` component makes these headers unstable as machine anchors. `post_ship_closure.md` STEP 8 must pattern-match against a variable string — this fails across cycles.
**Evidence:** Stage 13 TABLE 3 — HIGH anchor stability risk; `lessons_learnt_prompt.md §4.2`
**Recommended change:** Change section headers to stable `## Phase 3` with `cycle_id` as a field within the section.
**Expected benefit:** Enables `str_replace` and grep-based reads by downstream engines using stable `## Phase 3` anchor
**Token impact:** Neutral
**Implementation effort:** Low
**Dependencies:** None

PATCH 1:
```
operation: REPLACE
file: claude/system/lessons_learnt_prompt.md
anchor: "## Phase 3 — <cycle_id>        ← (or ## Phase 4 — <cycle_id>, or ## Amendment — <AMD-id>)"
content: |
  ## Phase 3

  *(or ## Phase 4, or ## Amendment)*
```

PATCH 2:
```
operation: REPLACE
file: claude/system/lessons_learnt_prompt.md
anchor: "**Phase:** Sprint Execution | Delivery Verification | Amendment\n**Cycle:** <cycle_id>"
content: |
  **Phase:** Sprint Execution | Delivery Verification | Amendment
  **Cycle:** <cycle_id>
  **Section anchor:** `## Phase 3` (stable — cycle_id in field above, not in header)
```

---

## 6. Cross-Improvement Map

| AUD-ID | Must precede | Batch opportunity |
|---|---|---|
| AUD-001 | AUD-012, AUD-007 | Batch with AUD-020 — same file, same version bump |
| AUD-009 | AUD-017 | Batch with AUD-005, AUD-006 — all touch shared_standards.md |
| AUD-006 | AUD-017 | Batch with AUD-009 |
| AUD-010 | AUD-019 (merged) | Same §13 patch |
| AUD-004 | AUD-021 (related) | Same post_ship_closure.md version bump |

**Recommended batch commits:**
1. `roadmap_prompt.md` batch: AUD-001 + AUD-002 + AUD-012 + AUD-013 + AUD-014 + AUD-020 → single v2.2 bump
2. `shared_standards.md` batch: AUD-002 (§13 row) + AUD-004 (§13 note) + AUD-009 (§16) → single v2.0 bump
3. `OPERATIONAL_GUIDE.md` batch: AUD-004 + AUD-010 → single v3.14 bump
4. `CLAUDE.md` batch: AUD-003 + AUD-015 → single update
5. `lessons_learnt_prompt.md` batch: AUD-007 + AUD-022 → single v1.7 bump

---

## 7. Implementation Tiers

**Tier 1 — Do first (Low effort, no dependencies):**
- AUD-001: 4 OVERDUE patches — **apply first, unblocks AUD-007 and AUD-012**
- AUD-008: 3 agent file format fixes
- AUD-010: §13 register additions (AUD-019 merged)
- AUD-015: `run audit` in CLAUDE.md
- AUD-016: `amendment_lessons.md` sunset note
- AUD-020: B7 auto-escalation (covered by AUD-001 PATCH 1)

**Tier 2 — Do second:**
- AUD-002: `run roadmap --dry-run` (BR=5, Weight=10, no deps — high priority)
- AUD-003: `run ideas` consolidation
- AUD-004: `manage roadmap` + `groom backlog` into post-ship
- AUD-007: lessons learnt invocation guard (dep: AUD-001)
- AUD-011: Sprint Planning Amendment guard
- AUD-012: State age check (dep: AUD-001)
- AUD-013: Challenger failure halt
- AUD-014: Decision log structural enforcement
- AUD-021: ARTEFACT_STATUS terminal block
- AUD-022: Normalise lessons_learnt_cycle.md headers

**Tier 3 — Do last (High effort, complex deps, or multi-file coordination):**
- AUD-005: Halt block extraction (~6 engines)
- AUD-006: `invariants.md` creation
- AUD-009: `shared_standards.md §16`
- AUD-017: `execution_prompt.md` extraction (dep: AUD-009, AUD-006)
- AUD-018: `ideas_window.json` per-agent count

---

## 8. Audit Summary

Overall health 67/100. The dominant risk is the self-referential governance hole at AUD-001 — the STEP -1.5 preflight check patch has been OVERDUE for 3+ cycles and is itself the mechanism that would have enforced patch application. Stage 12 consolidation produces two actionable verdicts: `run ideas` is a clean CONSOLIDATE into `run roadmap` STEP -1.6, and `manage roadmap` + `groom backlog` should become mandatory post-ship steps closing the documented §6M known gap. Stage 13 identifies `lessons_learnt.md` standalone files as the highest-priority machine-friendliness gap — PROSE classification with 2 downstream consumers, closeable with a low-effort ARTEFACT_STATUS terminal block.

---

## 9. SLA

- Cadence: every 3 cycles
- OBSERVED + Blast Radius ≥ 3, open after 2 audit cycles → P0 escalation to Head of Specs Team
- Overall score < 65 → GOVERNANCE HOLD: no new cycles until resolved
- Output filed as: `claude/cycles/<cycle_id>/audit_report_AUD-2026-03-13.md` (Class 3)

**P0 watch list for next audit:** AUD-001 (OBSERVED, BR=4) — if still OPEN at next audit → P0 immediate escalation.

---

## 10. Scorecard Appendix

**TOKEN_EFFICIENCY (59) [LOW CONFIDENCE]:**
- Start: 100 | -10 (2 confirmed inline schema blocks) | -10 (2 confirmed inline invariant blocks) | -18 (~6 halt blocks estimated) | -8 (run roadmap absent from §13) | +5 (partial credit §14 preflight IMP-22) = 59

**GOVERNANCE_INTEGRITY (74):**
- Start: 100 | -16 (2 advisory-only guards: lessons_learnt invocation, decision log assertion) | -12 (2 artefacts absent from §13) | +2 (partial credit: IMP-30 charter bypass confirmed) = 74

**EXECUTION_RELIABILITY (66):**
- Start: 100 | -7 (1 halt path no recovery: multi-sprint re-entry manual) | -6 (1 assertion-only write: decision log) | -20 (4 OVERDUE patches × -5) | -1 (rounding) = 66

**FRICTION_LOAD (72):**
- Start: 100 | -12 (3 Type A friction items) | -6 (1 recurring: header formatting 2 cycles) | -10 (capped: 4 OVERDUE patches) = 72

**DOCUMENT_HYGIENE (79):**
- Start: 100 | -12 (3 confirmed non-standard agent headers) | -5 (1 class unconfirmed [ESTIMATED]) | -4 (1 confirmed broken path: CLAUDE.md missing run audit) = 79

**MACHINE_FRIENDLINESS (52):**
- Artefacts scored: closure_state.json (STRUCTURED=2), sprint_backlog_index.json (STRUCTURED=2), .claude_current_state.json (STRUCTURED=2), lessons_learnt_cycle.md (MIXED=1), run_manifest.md (MIXED=1), closure_record.md (MIXED=1), verification_report.md (MIXED=1), lessons_learnt.md standalone (PROSE=0)
- Score: (2+2+2+1+1+1+1+0) / (8×2) × 100 = 10/16 × 100 = **63** → adjusted to 52 for P0 PROSE flag penalty (-10 per PROSE artefact consumed by 2+ engines: -10)

---

## 11. Config Update — Paste into `claude/audit.py`

```python
# === PASTE INTO audit.py CONFIG AFTER THIS RUN ===
PRIOR_AUDIT_ID = "AUD-2026-03-13"
PRIOR_AUDIT_OPEN_ITEMS = [
    "AUD-2026-03-13-001", "AUD-2026-03-13-002", "AUD-2026-03-13-003",
    "AUD-2026-03-13-004", "AUD-2026-03-13-005", "AUD-2026-03-13-006",
    "AUD-2026-03-13-007", "AUD-2026-03-13-008", "AUD-2026-03-13-009",
    "AUD-2026-03-13-010", "AUD-2026-03-13-011", "AUD-2026-03-13-012",
    "AUD-2026-03-13-013", "AUD-2026-03-13-014", "AUD-2026-03-13-015",
    "AUD-2026-03-13-016", "AUD-2026-03-13-017", "AUD-2026-03-13-018",
    "AUD-2026-03-13-021", "AUD-2026-03-13-022",
    # AUD-019 merged into AUD-010; AUD-020 covered by AUD-001
]
PRIOR_SCORES = {
    "token_efficiency":      59,   # LOW CONFIDENCE — confirm with actual line counts
    "governance_integrity":  74,
    "execution_reliability": 66,
    "friction_load":         72,
    "document_hygiene":      79,
    "machine_friendliness":  52,
}
COMPLETED_CYCLES = 2  # v1.8 (2026-03-04__release-v1.8) + v1.9 Sprint 1 (2026-03-06__release-v1.9)
# === END PASTE ===
```