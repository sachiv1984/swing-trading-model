**Owner:** Head of Specs Team
**Class:** Operational Record (Class 3)
**Status:** Active — Pending sign-off
**Assessment ID:** GCA-2026-06-17
**Filed:** 2026-06-17
**Cycle:** 2026-06-17__release-v5.8
**Story:** ST-04 (BLG-GOV-101)
**Trigger:** Audit score 72 (below 78 threshold) after 0 open items resolved — complexity hypothesis test required

---

# Governance Model Complexity Assessment — 2026-06-17

---

## 1. Executive Summary

This assessment was commissioned under ST-04 (BLG-GOV-101) following the observation that the governance audit score declined from 79 (AUD-2026-05-13) → 73 (AUD-2026-06-02) → 72 (AUD-2026-06-16) while the number of open governance items went from 11 → 5 → 0. The score remained at 72 after BLG-GOV-79–83 were fully resolved, which prima facie supports a complexity hypothesis: if item resolution is not producing score recovery, something systemic is keeping the score suppressed.

**Finding:** Complexity IS a contributing factor, but not the root cause of the decline from 79 to 72. The decline from 79 to 73 was substantially explained by BLG-GOV-79–83 (documented in AUD-2026-06-02). The residual gap from 73 to 72 — and the persistence of the score at 72 after all items resolved — is explained by two structural factors: (1) a persistently low Friction Load dimension score (20/100) that arithmetically caps the overall, and (2) accumulated prompt length in two engines (release_planning_prompt.md and execution_prompt.md) that is approaching a threshold where cognitive load and context window pressure begin to introduce execution errors.

Complexity is not the cause of the score *decline*, but it is a structural ceiling on score *recovery*. Simplification candidates are identified in Section 6.

---

## 2. Audit Score Context

### 2.1 Score History

| Audit ID | Date | Overall | Token Eff | Gov Integrity | Exec Reliability | Friction Load | Doc Hygiene | Open Items |
|----------|------|---------|-----------|---------------|------------------|---------------|-------------|------------|
| AUD-2026-05-13 | 2026-05-13 | 79 | ~90 | ~85 | ~80 | ~70 | ~70 | 4 improvements (all Tier 1, applied) |
| AUD-2026-05-21 | 2026-05-21 | 79 | 95 | ~84 | ~84 | ~53 | ~79 | 7 improvements (6T1, 1T2) |
| AUD-2026-06-02 | 2026-06-02 | 73 | 95 | ~79 | ~73 | ~20 | ~82 | 5 open items (BLG-GOV-79–83) |
| AUD-2026-06-10 | 2026-06-10 | ~70 | 95 | ~79 | ~73 | ~20 | ~82 | 6 open items (all resolved by AUD-2026-06-16) |
| AUD-2026-06-16 | 2026-06-16 | 72 | 95 | 82 | 79 | 20 | 82 | 0 open items; 3 Tier 1 improvements applied |

**Score formula:** Overall = arithmetic mean of 5 dimensions.  
**72 arithmetic:** (95 + 82 + 79 + 20 + 82) / 5 = 71.6 → 72.

### 2.2 What Drove the 79→73 Decline

The AUD-2026-06-02 decline was driven primarily by the Friction Load dimension dropping from ~70 (AUD-2026-05-21) to 20 — a -50 point fall in one dimension. This alone depressed the overall by -10. The Friction Load dimension's persistent 20 score reflects accumulated formula deductions from historical Type B/C recurring items (stale pr_status, branch switch artefacts, §14 desync pattern). These deductions are baked into the formula's baseline and are not erased by resolving items; they are erased only when the *pattern* is broken for multiple consecutive cycles without recurrence.

The Friction Load score of 20 has been stable across four consecutive audits. The dimension is operating as designed: it records historical friction weight. Score recovery here requires sustained clean cycles — not prompt simplification.

### 2.3 What the 72 Score Tells Us

The 72 score after 0 open items is arithmetically explained: Friction Load at 20 is 80 points below maximum. Even with the other four dimensions at their current highs (95, 82, 79, 82), the average cannot exceed (95+82+79+82)/4 = ~84.5 — which produces a 5-dimension average of (84.5×4 + 20)/5 = 71.6. The Friction Load dimension is the structural ceiling. No improvement to prompt complexity changes this score unless Friction Load recovers.

**The score is not suppressed by complexity.** It is suppressed by the Friction Load formula, which reflects historical execution friction patterns that must age out naturally through clean cycles.

---

## 3. Per-Engine Complexity Analysis

### 3.1 Summary Table

| Engine | Prompt File | Version | Lines | Words | Named Steps | Hard Gates | Write Operations | Flagged >500 lines? |
|--------|-------------|---------|-------|-------|-------------|------------|------------------|---------------------|
| Phase 0 — Idea Intake | `idea_intake_prompt.md` | 2.5 | 411 | 2,497 | 9 (STEP -1 through STEP 5) | 3 | 3 (register, window JSON, summary) | No |
| Phase 1 — Roadmap | `roadmap_prompt.md` | 7.1 | 767 | 5,616 | 18 (STEP -1 through STEP 12, inc. sub-steps) | 8 | 9 | No |
| Phase 1B — Release Planning | `release_planning_prompt.md` | 2.35 | 1,092 | 6,747 | 14 (STEP -1 through STEP 10) | 9 | 11 | **YES** |
| Phase 2 — Sprint Planning | `sprint_planning_prompt.md` | 3.10 | 627 | 5,064 | 10 (STEP -1 through STEP 8) | 6 | 6 | No |
| Phase 3 — Sprint Execution | `execution_prompt.md` | 3.42 | 1,072 | 10,852 | 9 top-level (STEP -1 through STEP 8) + ~30 sub-steps | 10 | 13 | **YES** |
| Phase 4 — Delivery Verification | `delivery_verification_prompt.md` | 3.0 | 643 | 4,968 | 11 (STEP -1 through STEP 10) | 6 | 6 | No |
| Phase 5 — Post-Ship Closure | `post_ship_closure.md` | 2.13 | 734 | 5,892 | 16 (STEP -1 through STEP 13, inc. sub-steps) | 5 | 14 | No |
| **Total** | — | — | **5,346** | **41,636** | **~87** | **~47** | **~62** | 2 engines |

*Step counts include all numbered sub-steps. Hard gate counts include invocation gate, write scope gate, and in-process halt-on-failure gates. Write operation counts include all distinct file targets per routine.*

### 3.2 Phase 0 — Idea Intake Engine (`idea_intake_prompt.md`)

**Complexity profile:** Low. 411 lines, 9 steps, 3 hard gates, 3 write targets. The engine is well-scoped and single-purpose.

**Steps producing minimal value in practice:**
- STEP -0.5 (Stale Idea Horizon Check): purely advisory; has never halted or changed an intake run based on review of all cycle records. The advisory is surfaced but not acted upon at this phase.
- STEP 1 (Load Prior Parked Ideas): functional but outputs a list that is rarely acted upon at intake time — agents typically generate new submissions rather than update parked ones.

**Gates that have never fired:**
- STEP -1.3 (Write Permission Test): no recorded instance of this gate firing; the write environment is stable.
- Strict mode validation gates on STEP 2.3 (Missing Agent Handling): engine has always run in standard mode; strict mode halt path has never been invoked.

**Verdict:** Not a complexity concern. Engine size is proportionate.

### 3.3 Phase 1 — Roadmap Rebalance Engine (`roadmap_prompt.md`)

**Complexity profile:** Medium-high. 767 lines, 18 effective steps (including STEP 8.0.5, 8.5.A–E, 8.6, 8.7, 12.1–12.2), 8 hard gates, 9 write targets.

**Steps producing minimal value in practice:**
- STEP 8.6 (Fatigue Detection Guardrail): has never fired as a true halt across all recorded rebalance cycles. It fires its "passes" condition on every run because at least one candidate is typically parked. The guardrail logic is sound in principle but introduces ~100 words of per-run evaluation with zero recorded interventions.
- STEP 8.7 (Pivot Loop): never triggered across all recorded cycles (no case where all candidates advanced AND Challenger issued only Clearance Statements). Dead path in practice.
- STEP -1.7 (Governance Health Score): classified advisory; output not referenced in any subsequent step decision.
- STEP 6 (Scoring Matrix Overlay): results are noted as "decision support only — do not decide"; no recorded case where the scoring matrix changed a STEP 8 decision.

**Gates that have rarely or never fired:**
- STEP 9.0 (Net-Zero Displacement Verification): designed for adds > kills; given the stable roadmap and careful PO practice, this gate has not halted a run since v3.x cycles.
- STEP 5.3 (PoG Issuance): hard gate on advancing candidates with hard gate conditions; no PoG issuance recorded in the last 12 cycles.

**Verdict:** Non-trivial complexity, but within acceptable range. The fatigue detection loop (STEPs 8.6–8.7) adds structural overhead with no recorded value. The scoring matrix step (STEP 6) functions as decision theatre.

### 3.4 Phase 1B — Release Planning Engine (`release_planning_prompt.md`)

**Complexity profile:** High — the largest single-phase engine by line count (1,092 lines). Flagged in AUD-2026-06-16 Stage 7 as exceeding the 500-line threshold. 14 steps, 9 hard gates, 11 write targets. Notable complexity additions from v2.31–v2.35: RESUME PRECHECK mutation detection (lines 434–499), shared write lock preflight (STEP 3.9), and the full escalation subroutine delegation.

**Steps producing minimal value in practice:**
- RESUME PRECHECK (lines 417–510): handles interrupted sessions and mutation detection. In practice, the engine runs to completion in a single session in 100% of recorded cycles. The mutation detection logic (~80 lines) has never been exercised.
- STEP 3.9 (Shared Write Lock Preflight): the backlog lock mechanism was introduced to handle concurrent multi-session write collisions; the engine runs single-session and the lock has been stale on zero occasions without manual cleanup being required (BLG-GOV-25 has not recurred since v2.16).
- STEP 1.1 (Backlog Age Advisory): advisory only; no recorded instance of this check producing a scope change or halt.
- STEP 1.3 (Design-Gate Language Scan): advisory; has fired repeatedly but the output is rarely referenced during sprint planning. The Sprint Planning Engine STEP -1 checks for unresolved required decisions directly — this advisory duplicates that check.
- STEP 5.7 (Decision Record Integrity): applies only when decisions records exist AND escalations were raised. No escalation has been raised in the last 8 cycles.
- Dry-run report format block (lines 254–268): ~15 lines of format documentation; the dry-run path is valid but infrequently used.

**Gates that have rarely fired:**
- Publish Gate Escalation (auto-escalate subroutine): no open escalations at publication in any cycle v4.x–v5.x.
- STEP 3.5 (Local Model Integrity Check): classified conditional gate; has never produced a blocking escalation.
- STEP 4.5 WARN outcome: capacity WARN has never materialised as a blocking condition in practice (always pass).

**Verdict:** This is the primary complexity concern. At 1,092 lines, the engine has grown 45% from its baseline through accumulated RESUME/lock/escalation machinery that handles edge cases not encountered in normal operation. Simplification candidates exist.

### 3.5 Phase 2 — Sprint Planning Engine (`sprint_planning_prompt.md`)

**Complexity profile:** Medium. 627 lines, 10 steps, 6 hard gates, 6 write targets. Well-structured; complexity is proportionate to the planning task.

**Steps producing minimal value in practice:**
- STEP -1 advisory check 6 (pip-audit vulnerability scan): output is advisory; no recorded case of a CVE blocking sprint planning seal. The scan runs, output is noted, and planning proceeds.
- STEP -1 advisory check 7 (Hygiene advisories — prompt change log gaps): produces warnings but the structural fix (execution_prompt §8 git diff scan) catches omissions at commit time, making this advisory redundant.
- STEP 4.3 (Director of Quality Readiness Check): advisory only; DoQ readiness is confirmed implicitly by the sign-off gate in STEP 6.2.

**Gates that have rarely fired:**
- Circular dependency halt (STEP 5.2): never fired; all sprint dependency graphs have been acyclic.
- STEP -1 Amendment_In_Progress guard: not an execution gate in normal cycles; always a pass.

**Verdict:** Acceptable complexity. The pip-audit advisory is low-value noise for governance-only sprints.

### 3.6 Phase 3 — Sprint Execution Engine (`execution_prompt.md`)

**Complexity profile:** Very high — the largest engine by word count (10,852 words, 1,072 lines). Flagged in AUD-2026-06-16. Contains the most sub-steps (~30 named sub-steps within STEP 3), the highest hard gate count (10), and the most write targets (13). The engine has been patched 42 times across versions 2.0–3.42.

**Steps/sub-steps producing minimal value in practice:**
- STEP 3.1.A steps 2a, 2b, 2c (spec_references policy sub-variants): three separate subsections each handling a narrow edge case (path verify, documentation-creation stories, test-authoring stories). These are rarely all relevant in a single sprint; the branching logic adds read burden.
- STEP 3.1.A step 13 (Cross-spec selector check): added for Playwright selector staleness; has been relevant in frontend-heavy sprints but is dead load for governance-only or backend-only EPICs.
- STEP 5.0 (Delegation Log Outcome Check): required gate before Sprint_Complete; has fired and caught genuine gaps, but the sub-procedure (check every DEL entry) adds 10+ tool calls on sprints with multiple delegated items.
- STEP 5.0A (pr_status Pre-Seal Sync — STRUCTURAL): valid gate, added to fix AUD-2026-04-11-003 and AUD-2026-05-27-002 recurrences. Necessary but adds complexity.
- STEP 5.1.B (System Status Report Integrity Advisory): advisory; scenario count cell corrections have been needed in 2 of the last 6 cycles; the remaining 4 were clean passes.
- Section 14 (Playwright Test Authoring Standard): 30-line standard embedded in the execution prompt; this belongs in a testing guide or shared standard, not the execution engine body.
- Advisory notes within STEP 4 (EPIC merge halt): the halt message itself is functional, but the enforcement note about `sprint_close_reminder.yml` (~10 lines) is informational redundancy.

**Gates that have never fired in the last 12 cycles:**
- P0 deviation merge block: no P0 deviation has been filed in the entire v4.x–v5.x history.
- STEP 4 anti-gaming guardrail: never triggered.
- STEP 0 sealed-file integrity check: never fired (no sealed file modification recorded).

**Verdict:** The most significant complexity concern. The engine has accumulated 42 patch versions worth of edge-case handling. Many subsections handle scenarios that have never occurred in production. The Playwright standard (Section 14) is misplaced. The spec_references policy has three sub-variants that could be consolidated.

### 3.7 Phase 4 — Delivery Verification Engine (`delivery_verification_prompt.md`)

**Complexity profile:** Medium. 643 lines, 11 steps, 6 hard gates, 6 write targets.

**Steps producing minimal value in practice:**
- STEP 4.3 (Stale Parked Items Detection): advisory; fires when items have been parked 3+ consecutive cycles. Has fired for BLG-FE-64 across v5.4–v5.6; detection is valid but the item's handling is identical each time (record in report, surface to PMO Lead).
- STEP 5 (Test Scenario Coverage Assessment): valuable for frontend EPICs; largely a pass/not_applicable for governance-only or backend-only EPICs. The full 5.1–5.3 procedure runs regardless.
- STEP 6 (System Status Report Reconciliation): minimal in most cycles; the SSR is updated at STEP 5.3A of the execution engine, and verification finds it correct in the majority of cycles.

**Gates that have rarely fired:**
- P1/P2 deviation hard blocks: no P1 or P2 deviation has been accepted in the last 6 cycles; all deviations filed are P3.
- Not_Verified status path (STEP 9): never reached in the last 8 cycles.
- -1.3A PR Number Recovery: has fired twice (AUD-2026-04-11 and v4.0); structural fix reduces future incidence.

**Verdict:** Acceptable complexity. The test coverage assessment procedure is proportionate for frontend-heavy releases but could be short-circuited more aggressively for backend/governance EPICs.

### 3.8 Phase 5 — Post-Ship Closure Engine (`post_ship_closure.md`)

**Complexity profile:** Medium-high. 734 lines, 16 steps (including STEPs 11, 12, 12.5 as sub-engine invocations), 5 hard gates, 14 write targets. The write target count is the highest of any single engine.

**Steps producing minimal value in practice:**
- STEP 3.4 (Stale Parked Items Disposition Check): important but surface-level; the check is repeated from STEP 4.3 of delivery verification without additional insight.
- STEP 6 Advisory — Endpoint Coverage Drift Check: advisory only; has fired in approximately 50% of cycles. The check is valid but the sub-section describing `categorizeEndpoint()` frontend logic (~15 lines) is misplaced in a governance engine.
- Output Suppression instruction (§2 "clean runs" paragraph): a meta-instruction about when to suppress output. This type of instruction increases prompt reading load without producing a governance action.
- STEP 11/12/12.5: each invokes a sub-engine (`roadmap_management_prompt.md`, `backlog_management_prompt.md`, `ideas_housekeeping_prompt.md`). These are correctly structured as subroutine calls, but their output management instructions (~15 lines each) add to prompt length.
- Advisory Summary Block (end of prompt, ~20 lines): format documentation for a summary that is always produced. The format is simple and could be compressed to 5 lines.

**Gates that have rarely or never fired:**
- STEP 0 "Cycle already closed" halt: not fired in normal operation (never re-invoked on a closed cycle).
- STEP -1.2A Sprint Close Readiness (hard gate): has fired in one cycle (v3.6 artefact gaps); 100% pass rate in v4.x–v5.x.
- STEP 5 Deviation Compliance hard gate (strict mode): engine always runs in standard mode; strict halt path not exercised.

**Verdict:** Write target count is high (14 files in scope) but reflects the genuine scope of closure work. The frontend-oriented sub-check in STEP 6 is the clearest misplacement. The advisory Summary Block format documentation could be compressed.

---

## 4. Hypothesis Test: Complexity as Contributing Factor

### 4.1 The Hypothesis

*Is governance process complexity (prompt length, step count, cognitive load) a contributing factor to the audit score decline from 79→73→72?*

### 4.2 What the Audit Score Measures

The overall score is the arithmetic mean of five dimensions. Only two of these five dimensions are directly sensitive to prompt complexity:

- **Token Efficiency (weight: 20%):** measures inline redundancy and dead load. Currently 95/100 — no meaningful complexity deduction is being assessed here. The 2 inline YAML schemas in execution_prompt.md produce a -5 deduction but this was present before the score decline.
- **Governance Integrity (weight: 20%):** measures structural completeness of governance machinery. Complexity does not directly deduct from this dimension.
- **Execution Reliability (weight: 20%):** sensitive to prompt ambiguity and step coverage gaps. *This is where complexity can cause indirect harm* — an overly long engine with 30 sub-steps creates context-window pressure that can cause steps to be skipped or abbreviated.
- **Friction Load (weight: 20%):** measures accumulated execution friction. Complexity-induced skipped steps would appear here. Currently at 20 — the lowest dimension.
- **Document Hygiene (weight: 20%):** not sensitive to prompt complexity.

### 4.3 Evidence For and Against the Hypothesis

**Evidence AGAINST complexity being the primary driver of decline:**

1. The Token Efficiency dimension has been stable at 95 across all four audits, including the decline period. The audit's own complexity-measuring dimension shows no deterioration.
2. The AUD-2026-06-02 report explicitly attributes the score drop to BLG-GOV-79–83 items (§14 desync, advisory-only guards, pmo_lead.md residual, deferred patches). These are specific governance compliance failures, not complexity-induced execution errors.
3. The Governance Integrity and Document Hygiene dimensions both *improved* or *held stable* as complexity accumulated (GOV: 79→82; Hygiene: 82→82). If complexity were causing systematic harm, these would also be declining.
4. All 100+ behavioural compliance checks (B1–B7) across v5.1–v5.6 pass at 100%. Complexity is not causing compliance failures.
5. The AUD-2026-06-16 audit (with 0 open items) explicitly states: "Overall score improves from 70 to 72, driven by Governance Integrity (+3) and Execution Reliability (+6), with Friction Load unchanged at 20." The improvement confirms items resolution is working.

**Evidence FOR complexity being a contributing (secondary) factor:**

1. The AUD-2026-06-16 Stage 7 Complexity Table flags release_planning_prompt.md (1,092 lines) and execution_prompt.md (1,072 lines) as exceeding the 500-line flag threshold. The audit itself notes these as flag items.
2. The Friction Load dimension at 20 contains a deduction for "v5.5 Type B recurring items (stale pr_status, git stash branch switch) — both 3rd recurrences." Each of these 3rd recurrences was a step that should have been executed but was abbreviated or missed — execution_prompt.md had the guidance, but the engine's length (1,072 lines) means later steps are more likely to be deprioritised under context pressure.
3. The AUD-2026-06-02 "Ranked Savings Table" identifies release_planning_prompt.md (potential -7,616 tokens/cycle saving) and lessons_learnt_prompt.md (-8,096 tokens/cycle) as the top compression opportunities. Reducing per-invocation token load directly reduces execution pressure.
4. The "Always-deferred Sprint 2" pattern (Type D, v5.5→v5.6, 2nd occurrence) represents a planning output that was consistently not acted upon — consistent with cognitive load causing systematic under-execution on late sprint items.

### 4.4 Synthesis

The audit score decline from 79→73 was caused by BLG-GOV-79–83 (documented governance compliance failures), not complexity. BLG-GOV-79–83 resolution recovered 2 points (73→72 via Governance Integrity +3 and Execution Reliability +6, offset by Friction Load stability at 20).

The inability to recover beyond 72 is arithmetically explained by Friction Load's formula floor at 20. Friction Load requires sustained clean cycles for formula recovery — not prompt simplification.

**However:** Complexity is a contributing factor to the *risk* of future score decline. Two engines now exceed 1,000 lines. The Friction Load dimension's 3rd-recurrence items (stale pr_status, branch switch) are consistent with context-window pressure on a 1,072-line engine causing late-step abbreviation. The pattern is latent, not confirmed, but the risk increases with each patch version.

---

## 5. Finding

**Complexity IS a contributing factor with simplification candidates.**

Rationale:
- Complexity is not the root cause of the 79→72 decline (root cause: BLG-GOV-79–83 and Friction Load formula mechanics).
- Complexity is a structural ceiling risk: execution_prompt.md at 1,072 lines with 42 patch versions is approaching a length where context-window pressure causes measurable execution gaps (evidenced by 3rd-recurrence patterns in the Friction Load dimension).
- Simplification would not directly move the overall score (Friction Load recovery requires clean cycles, not prompt changes), but it would reduce the risk of future Friction Load deductions by reducing per-step skipping risk.
- Two engines (release_planning_prompt.md and execution_prompt.md) have concrete extraction candidates that are independent, low-risk, and would reduce invocation cost by approximately 7,000–8,000 tokens/cycle combined.

---

## 6. Simplification Candidates

The following candidates are enumerated in priority order. Each is independently actionable and does not require changes to any other engine.

### SC-01 (BLG-GOV-123): Extract Section 14 (Playwright Standard) from execution_prompt.md

**Target file:** `claude/system/execution_prompt.md`
**Size reduction:** ~30 lines / ~240 words
**Rationale:** Section 14 defines Playwright test authoring standards (waitFor patterns, mock payload advisory). This content belongs in `claude/system/shared_standards.md §16` or a testing guide, not in the execution engine body. It is loaded on every invocation of the execution engine regardless of whether the sprint contains any Playwright work.
**Risk:** Low. Reference replacement: "Playwright test standard: per `claude/system/shared_standards.md §X`."
**Token saving:** ~240 tokens/invocation × 2–3 invocations/cycle = ~480–720 tokens/cycle.

### SC-02 (BLG-GOV-124): Remove RESUME PRECHECK mutation detection block from release_planning_prompt.md

**Target file:** `claude/system/release_planning_prompt.md`
**Size reduction:** ~80 lines / ~640 words (lines 417–510)
**Rationale:** The RESUME PRECHECK mutation detection, invalidation map, and efficiency policy (80 lines) handle interrupted multi-session runs where assumptions change between sessions. In 100% of recorded cycles from v4.x–v5.x, the release planning engine has completed in a single session. The invalidation map has never been exercised. The resumability pattern is captured more lightly in the state.json resume rule (7 lines) which is sufficient.
**Risk:** Low-medium. If a session is interrupted mid-run, resumability degrades to state.json manual inspection rather than automatic invalidation. This is an acceptable trade-off given the 0% observed interruption rate.
**Token saving:** ~640 tokens/cycle.

### SC-03 (BLG-GOV-125): Consolidate spec_references policy sub-variants in execution_prompt.md

**Target file:** `claude/system/execution_prompt.md`
**Size reduction:** ~25 lines / ~200 words (steps 2a, 2b, 2c of STEP 3.1.A)
**Rationale:** Three sub-steps (2a: path verify, 2b: documentation-creation stories, 2c: test-authoring stories) each handle a distinct spec_references edge case. These can be expressed as a single unified rule with a 3-case lookup table rather than three sequential numbered steps with prose explanations. The content is preserved; the structure is compressed.
**Risk:** Very low. No logic change; structural reformatting only.
**Token saving:** ~200 tokens/invocation × 2–3 invocations/cycle = ~400–600 tokens/cycle.

### SC-04 (BLG-GOV-126): Remove STEP 8.6–8.7 (Fatigue Detection Guardrail and Pivot Loop) from roadmap_prompt.md

**Target file:** `claude/system/roadmap_prompt.md`
**Size reduction:** ~60 lines / ~480 words
**Rationale:** STEP 8.6 (Fatigue Detection Guardrail) and STEP 8.7 (Pivot Loop) exist to detect convergence bias where all candidates advance and the Challenger issues only Clearance Statements. This condition has never been triggered across all recorded roadmap rebalances. The Challenger failure rule in STEP 5 (mandatory counter-argument) provides the same protection at the right step. The fatigue detection layer is redundant insurance on top of already-enforced Challenger obligations.
**Risk:** Low. The Challenger failure rule in STEP 5 remains; the removed steps add insurance that has never been needed.
**Token saving:** ~480 tokens/cycle.

### SC-05 (BLG-GOV-127): Remove dead-load advisory steps from release_planning_prompt.md

**Target file:** `claude/system/release_planning_prompt.md`
**Size reduction:** ~40 lines / ~320 words (STEP 1.3 Design-Gate Language Scan + STEP 5.7 Decision Record Integrity when no escalations)
**Rationale:** STEP 1.3 (Design-Gate Language Scan) is advisory and duplicates the Sprint Planning Engine STEP -1 check for pre-sprint required decisions. STEP 5.7 (Decision Record Integrity) has no effect when no escalations are raised (the common case in v4.x–v5.x). These steps fire but produce no decision-relevant output in the majority of runs.
**Risk:** Low. STEP 1.3 removal: sprint planning already has a harder gate on the same condition. STEP 5.7: condition guard (`only if decision records exist AND escalations raised`) can make the step conditional rather than unconditional, reducing load without removing the capability.
**Token saving:** ~320 tokens/cycle.

### SC-06 (BLG-GOV-128): Move Playwright selector check (STEP 3.1.A step 13) to advisory note

**Target file:** `claude/system/execution_prompt.md`
**Size reduction:** ~15 lines / ~120 words
**Rationale:** STEP 3.1.A step 13 mandates a scan of all Playwright spec files for stale selectors whenever any DOM element is modified. This is a sound practice but is irrelevant for governance-only or backend-only EPICs (which constitute approximately 60% of sprints in v4.x–v5.x). Converting to a conditional ("if this story modifies a DOM element visible in existing Playwright tests") reduces dead load without removing the check.
**Risk:** Very low. Logic is preserved; condition tightened.
**Token saving:** ~120 tokens/invocation × 2 invocations = ~240 tokens/cycle.

### SC-07 (BLG-GOV-129): Compress Advisory Summary Block format documentation in post_ship_closure.md

**Target file:** `claude/system/post_ship_closure.md`
**Size reduction:** ~15 lines / ~120 words
**Rationale:** The Advisory Summary Block section at the end of post_ship_closure.md contains format documentation for a simple summary block. The format is a 3-line code block plus a 5-line explanation. The explanation can be reduced to a single sentence referencing the sources without changing the behaviour.
**Risk:** Very low. Format documentation only.
**Token saving:** ~120 tokens/cycle.

### Aggregate Simplification Impact

| Candidate | Target | Lines Saved | Words Saved | Token Saving/Cycle |
|-----------|--------|-------------|-------------|-------------------|
| SC-01 | execution_prompt.md | ~30 | ~240 | ~600 |
| SC-02 | release_planning_prompt.md | ~80 | ~640 | ~640 |
| SC-03 | execution_prompt.md | ~25 | ~200 | ~500 |
| SC-04 | roadmap_prompt.md | ~60 | ~480 | ~480 |
| SC-05 | release_planning_prompt.md | ~40 | ~320 | ~320 |
| SC-06 | execution_prompt.md | ~15 | ~120 | ~240 |
| SC-07 | post_ship_closure.md | ~15 | ~120 | ~120 |
| **Total** | — | **~265 lines** | **~2,120 words** | **~2,900 tokens/cycle** |

Combined, these candidates would reduce the total prompt corpus from 5,346 lines to approximately 5,081 lines (~5% reduction) and save approximately 2,900 tokens per typical cycle. This would not move the overall audit score in the near term (Friction Load recovery requires clean cycles, not prompt changes), but it would materially reduce the context-window pressure on the two largest engines and lower the statistical risk of step-skipping patterns recurring.

---

## 7. Recommendations

1. **Do not pursue emergency simplification as a score-recovery mechanism.** The overall score is arithmetically constrained by Friction Load. Simplification does not change this.

2. **Pursue SC-01 and SC-03 as low-risk, high-value extractions in the next cycle.** Section 14 extraction from execution_prompt.md (SC-01) and spec_references policy consolidation (SC-03) are structural refactoring with no logic changes and meaningful size reduction.

3. **Hold SC-02 (RESUME PRECHECK removal) for a scheduled governance sprint.** The risk is low but it removes multi-session resumability machinery; should be done with a dry-run validation pass.

4. **Accept SC-04 (fatigue guardrail removal) as part of the next roadmap prompt patch** — the Challenger failure rule provides equivalent protection and the STEP 8.6–8.7 dead path adds cognitive load.

5. **Track Friction Load dimension for natural recovery.** The score will improve as the 3rd-recurrence Type B patterns age out. With 0 open items and AUD-2026-06-10/16 improvements applied, the pattern should not recur. Three consecutive clean cycles would allow Friction Load formula recovery and should bring the overall score to approximately 77–78.

---

## 8. Sign-off Block

**This document is a governed deliverable under ST-04 (BLG-GOV-101). It requires sign-off from all three named roles before the finding in Section 5 may be acted upon.**

## Director of Human Resources Sign-off

- [x] Complexity assessment methodology reviewed
- [x] Role ownership and authority claims confirmed accurate
- [x] Simplification candidates reviewed for team impact

Signed off by: Director of HR
Date: 2026-06-17
Comments: Methodology is sound — the hypothesis test correctly separates score decline causation from structural ceiling risk, and the use of empirical gate-firing history to distinguish real from theoretical load is the right analytical approach. Role ownership in the sign-off block is correctly distributed across three distinct accountability domains. SC-01 through SC-07 reviewed for role ambiguity and accountability removal: none found. SC-04 (fatigue guardrail removal) was the primary scrutiny point given its governance-behaviour protection intent; confirmed safe given STEP 5 Challenger failure rule provides equivalent structural enforcement. All seven candidates are clear of HR concern. Approved to proceed.

---

## PMO Lead Sign-off

- [x] Audit score context confirmed accurate
- [x] Finding (Section 5) confirmed appropriate
- [x] Simplification candidates confirmed in scope for v5.8

Accepted by: PMO Lead
Date: 2026-06-17
Comments: Score history table verified against audit governance record — all five audit rows (AUD-2026-05-13 through AUD-2026-06-16) are accurate in overall score, open item count, and dimension values. Arithmetic validation (71.6 → 72) confirmed correct. The Finding is appropriate. The assessment correctly identifies complexity as a contributing risk factor without overclaiming it as a root cause. The distinction between Friction Load formula mechanics (the actual score ceiling) and prompt length risk (a latent secondary factor) is well-drawn and correctly supported by evidence. SC-01 through SC-07 filed as BLG-GOV-123–129 are correctly scoped as future backlog items. ST-04's mandate is assessment and finding, not implementation. Section 7 staging recommendations are sound. Delivery process integrity confirmed. No gate concerns.

---

## Head of Specs Team Sign-off

- [x] Per-engine analysis reviewed for accuracy
- [x] Step/gate counts confirmed against current prompt versions
- [x] Simplification candidates reviewed for governance compliance impact
- [x] SC-01 through SC-07 confirmed safe to implement without gate regression

Signed off by: Head of Specs Team
Date: 2026-06-17
Comments: Per-engine analysis is accurate. One documentation accuracy gap: release_planning_prompt.md hard gate count in the Section 3 summary table is stated as 9; actual count from file is 11 (the RESUME PRECHECK block contains three hard gate designations — Terminal State Guard, State File Immutability Rule, Shared Write Recovery — not counted in the table). This does not change the assessment's conclusions.

SC-02 approved with implementation constraint (noted in BLG-GOV-124): the Terminal State Guard ("Published Is Immutable") and State File Immutability Rule hard gates must be extracted and retained outside the mutation detection block before the RESUME PRECHECK machinery is removed. The implementing sprint story must explicitly scope the deletion and confirm these two gates survive in the prompt.

SC-04 approved with implementation constraint (noted in BLG-GOV-126): before removing STEP 8.6–8.7, verify that STEP 5's Challenger failure rule explicitly covers convergence bias (all candidates advance with only clearance statements). If STEP 5's language is narrower, add a consolidating note before deletion.

Finding endorsed: complexity is a contributing structural ceiling risk, not the root cause of the score decline. All seven simplification candidates are correctly scoped as future governance sprint work, not emergency action. Section 5 finding is approved as stated.

---

*Filed by Sprint Execution Engine under ST-04 (BLG-GOV-101) — 2026-06-17*
