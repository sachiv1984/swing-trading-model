**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Published
**Cycle:** 2026-06-17__release-v5.9
**Published:** 2026-06-17

---

# Release Backlog Slice — v5.9

<!-- release-plan-marker: RP:v5.9:2026-06-17__release-v5.9 -->

**Firm stories:** 5 | **Conditional stories:** 8 | **Total:** 13

---

## EPIC-01 — Governance Simplification (SC-03–SC-07)

**Maps to:** S2-01
**Owner:** Head of Specs Team
**Sprint:** 1
**Classification:** Firm (all items Ready now)

### ST-01 — SC-03: Consolidate spec_references policy sub-variants in execution_prompt.md

**Source:** BLG-GOV-125
**Classification:** Firm
**Effort:** XS (~1 hour)
**Owner:** Head of Specs Team

**Scope:**
STEP 3.1.A steps 2a, 2b, 2c of `execution_prompt.md` each handle a distinct spec_references edge case as separate numbered sub-steps with prose. Consolidate into a single unified rule with a 3-case lookup table (~25 lines → ~10 lines). No logic change.

**Acceptance Criteria:**
- AC-01: Steps 2a, 2b, 2c replaced by a single consolidated rule with a 3-case lookup table
- AC-02: All three edge cases preserved in the table (path verify, documentation-creation, test-authoring)
- AC-03: Version bump on execution_prompt.md; changelog entry appended to prompt_change_log.md
- AC-04: OPERATIONAL_GUIDE.md §14 updated with new version number
- AC-05: Head of Specs Team sign-off

---

### ST-02 — SC-04: Remove STEP 8.6–8.7 fatigue detection guardrail from roadmap_prompt.md

**Source:** BLG-GOV-126
**Classification:** Firm
**Effort:** XS (~1 hour)
**Owner:** Head of Specs Team

**Scope:**
STEP 8.6 (Fatigue Detection Guardrail) and STEP 8.7 (Pivot Loop) in `roadmap_prompt.md` detect convergence bias. This condition has never been triggered. Remove STEPs 8.6–8.7; first verify STEP 5 Challenger failure rule covers convergence bias (add consolidating note to STEP 5 if narrower).

**Acceptance Criteria:**
- AC-01: STEP 5 Challenger failure rule verified to cover convergence bias; if language is narrower, a consolidating note is added to STEP 5 before deletion
- AC-02: STEPs 8.6 and 8.7 removed from roadmap_prompt.md
- AC-03: Version bump; prompt_change_log.md entry appended; OPERATIONAL_GUIDE §14 updated
- AC-04: Head of Specs Team sign-off

---

### ST-03 — SC-05: Remove dead-load advisory steps from release_planning_prompt.md

**Source:** BLG-GOV-127
**Classification:** Firm
**Effort:** XS (~1 hour)
**Owner:** Head of Specs Team

**Scope:**
Two advisory steps run unconditionally but produce no decision-relevant output in the common case: (a) STEP 5.7 (Decision Record Integrity) — no effect when no escalations raised; (b) STEP 1.3 (Design-Gate Language Scan) — duplicates Sprint Planning Engine STEP -1 check. Make STEP 5.7 conditional on escalations existing; remove or reduce STEP 1.3 to a single-line reminder.

**Acceptance Criteria:**
- AC-01: STEP 5.7 made conditional: runs only when escalation records exist in escalations.md (or `artifacts.escalations = present` in state.json)
- AC-02: STEP 1.3 removed or reduced to a single-line note referencing sprint_planning_prompt.md
- AC-03: Version bump; prompt_change_log.md entry; OPERATIONAL_GUIDE §14 updated
- AC-04: Head of Specs Team sign-off

---

### ST-04 — SC-06: Make Playwright selector check conditional on DOM changes in execution_prompt.md

**Source:** BLG-GOV-128
**Classification:** Firm
**Effort:** XS (<1 hour)
**Owner:** Head of Specs Team

**Scope:**
STEP 3.1.A step 13 in `execution_prompt.md` mandates a scan of all Playwright spec files for stale selectors whenever any DOM element is modified. For governance-only or backend-only EPICs (~60% of sprints) this is dead load. Tighten the condition to: "if this story modifies a DOM element that is targeted by existing Playwright selectors." No logic change for frontend EPICs.

**Acceptance Criteria:**
- AC-01: Step 13 condition tightened: selector scan required only for stories that modify DOM elements targeted by existing Playwright selectors
- AC-02: Condition is explicit — governance-only and backend-only stories skip the scan
- AC-03: Existing coverage for frontend EPICs preserved (no regression)
- AC-04: Version bump; prompt_change_log.md entry; OPERATIONAL_GUIDE §14 updated
- AC-05: Head of Specs Team sign-off

---

### ST-05 — SC-07: Compress Advisory Summary Block format docs in post_ship_closure.md

**Source:** BLG-GOV-129
**Classification:** Firm
**Effort:** XS (<30 min)
**Owner:** Head of Specs Team

**Scope:**
The Advisory Summary Block section at the end of `post_ship_closure.md` contains ~20 lines of format documentation for a simple 3-line summary block. Compress to a ≤5-line format block with a single-sentence explanation.

**Acceptance Criteria:**
- AC-01: Advisory Summary Block format documentation compressed to ≤5 lines (from ~20 lines)
- AC-02: Single-sentence explanation retained; all format elements preserved
- AC-03: Version bump; prompt_change_log.md entry; OPERATIONAL_GUIDE §14 updated
- AC-04: Head of Specs Team sign-off

---

## EPIC-02 — RFJ UX Pre-work, SI-05 Verification & SI-05 Effectiveness Review

**Maps to:** S2-02, S2-03, S2-04
**Owner:** PMO Lead; Infrastructure & Operations Owner; Metrics Definitions & Analytics Owner
**Sprint:** 1 (ST-06–08, near-term conditional) + Sprint 2 (ST-09–13, gate 2026-07-04 conditional)
**Classification:** All conditional — see individual gate conditions

### ST-06 — BLG-FE-64: Red Flag Journal visual design review pre-brief

**Source:** BLG-FE-64
**Classification:** Conditional — gate 2026-06-21 (SI-03 RFJ live ≥ 30 days; 5th sprint attempt)
**Effort:** S (~0.5 day)
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Sprint:** 1 (execute after 2026-06-21 gate confirmed)
**Status at sprint open:** Conditional — gate 2026-06-21

**Promotion:** Gate owner (Frontend Specs & UX Documentation Owner) must explicitly confirm gate cleared before this story enters execution.

**Scope:**
Produce a design review brief for BLG-FE-41: define review scope (filters UX, severity visual hierarchy, event type colour coding, timeline vs list layout), evaluation criteria, and expected deliverable. Input to BLG-FE-41 sprint planning when gate clears 2026-06-21.

**Acceptance Criteria:**
- AC-01: Design review brief produced and filed in docs/product/ux/ or equivalent
- AC-02: Brief covers: scope definition (which aspects of RedFlagJournal.js are in scope), evaluation criteria, and deliverable format
- AC-03: Head of UX & Design sign-off on brief scope
- AC-04: Gate condition confirmed cleared: SI-03 Red Flag Journal live ≥ 30 days (2026-06-21)

---

### ST-07 — BLG-FE-41: Red Flag Journal visual design review

**Source:** BLG-FE-41
**Classification:** Conditional — gate 2026-06-21; depends on ST-06 (BLG-FE-64 brief complete)
**Effort:** M (~1–2 days design + spec)
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Sprint:** 1 (execute after ST-06 complete and gate confirmed)
**Status at sprint open:** Conditional — gate 2026-06-21; depends on ST-06

**Scope:**
Design review for Red Flag Journal: severity visual hierarchy, timeline vs list layout evaluation, event type colour coding. Produce design recommendation with rationale; if redesign recommended, produce UX spec and file implementation backlog item.

**Acceptance Criteria:**
- AC-01: Design recommendation document produced covering: severity visual hierarchy, event type colour coding, timeline vs list layout decision
- AC-02: Rationale documented with reference to existing design system
- AC-03: If redesign recommended: UX spec produced and implementation item filed
- AC-04: Gate condition confirmed: SI-03 live ≥ 30 days (2026-06-21)
- AC-05: ST-06 (BLG-FE-64 pre-brief) completed before this story begins
- AC-06: Frontend Specs & UX Documentation Owner + Head of UX & Design sign-off

---

### ST-08 — BLG-OPS-70: Confirm SI-05 deep links work in production after FRONTEND_URL set

**Source:** BLG-OPS-70
**Classification:** Conditional — gate ~2026-06-23 (next SI-05 digest delivery after FRONTEND_URL set 2026-06-17)
**Effort:** XS (<1 hour)
**Owner:** Infrastructure & Operations Owner
**Sprint:** 1 (execute after next SI-05 digest delivery ~2026-06-23)
**Status at sprint open:** Conditional — gate ~2026-06-23

**Scope:**
Confirm SI-05 Telegram digest deep links resolve to correct frontend pages after FRONTEND_URL env var was set on production backend 2026-06-17. Check next weekly digest delivery.

**Acceptance Criteria:**
- AC-01: SI-05 Telegram digest received after FRONTEND_URL env var applied (next delivery ~2026-06-22/23)
- AC-02: Deep links in digest are present and resolve to correct frontend pages
- AC-03: Infrastructure & Operations Owner confirmation recorded in a brief verification note

---

### ST-09 — BLG-GOV-112: SI-05 digest weekly cadence review

**Source:** BLG-GOV-112
**Classification:** Conditional — gate 2026-07-04 (SI-05 Phase 1 effectiveness review complete; 3rd sprint attempt)
**Effort:** S (~0.5 day)
**Owner:** Product Owner; Director of Quality
**Sprint:** 2 (gate 2026-07-04)
**Status at sprint open:** Conditional — gate 2026-07-04

**Scope:**
After 2026-07-04 effectiveness review: assess weekly cadence appropriateness. Review si05_digest_log delivery count, any feedback from user, and whether digest content is acted upon. Produce cadence recommendation: maintain weekly / move to bi-weekly / introduce adaptive cadence.

**Acceptance Criteria:**
- AC-01: Cadence review document produced after 2026-07-04 effectiveness review completes
- AC-02: Recommendation made with data backing from si05_digest_log and observable signals
- AC-03: Product Owner sign-off on recommendation
- AC-04: Gate confirmed: SI-05 Phase 1 effectiveness review (BLG-GOV-96) complete

---

### ST-10 — BLG-GOV-113: SI-05 effectiveness review protocol execution

**Source:** BLG-GOV-113
**Classification:** Conditional — gate 2026-07-04
**Effort:** S (~0.5 day)
**Owner:** Director of Quality; PMO Lead
**Sprint:** 2 (gate 2026-07-04)
**Status at sprint open:** Conditional — gate 2026-07-04

**Scope:**
Execute the SI-05 Phase 1 effectiveness review protocol (BLG-GOV-96 protocol document). Assess whether SI-05 Phase 1 is producing actionable outputs. Produce effectiveness review output document. Input to ST-09 (cadence review), ST-11 (actionability metric definition), and ST-13 (Phase 2 activation decision).

**Acceptance Criteria:**
- AC-01: Effectiveness review conducted per BLG-GOV-96 protocol on or after 2026-07-04
- AC-02: Review output document produced covering: delivery count, content quality assessment, observed user behaviour signals
- AC-03: Director of Quality + PMO Lead sign-off on review output
- AC-04: Gate confirmed: 2026-07-04 reached and ≥ 4 weeks of production operation confirmed

---

### ST-11 — BLG-GOV-115: SI-05 digest actionability metric definition

**Source:** BLG-GOV-115
**Classification:** Conditional — gate 2026-07-04 (BLG-GOV-113 complete; 3rd sprint attempt)
**Effort:** S (~0.5–1 day)
**Owner:** Metrics Definitions & Analytics Owner; Infrastructure & Operations Owner
**Sprint:** 2 (gate 2026-07-04)
**Status at sprint open:** Conditional — gate 2026-07-04

**Scope:**
Define 2–4 actionability metrics for SI-05 digest effectiveness. Metrics must be measurable from existing data sources (si05_digest_log, red_flag_events, trade data). Produce metrics definition document.

**Acceptance Criteria:**
- AC-01: 2–4 actionability metrics formally defined with data source mapping
- AC-02: Metrics cover at minimum: digest delivery count, indication of user engagement signal, compliance score trend observation
- AC-03: Metrics definition document reviewed by Metrics Definitions & Analytics Owner
- AC-04: Gate confirmed: BLG-GOV-113 (effectiveness review execution) complete
- AC-05: Metrics feed BLG-GOV-112 cadence review and BLG-GOV-96 effectiveness criteria

---

### ST-12 — BLG-OPS-59: SI-05 service production p99 latency baseline review

**Source:** BLG-OPS-59
**Classification:** Conditional — gate 2026-07-04 (≥4 weeks POST /digest/si05/send production operation; 3rd sprint attempt)
**Effort:** S (~0.5 day)
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Sprint:** 2 (gate 2026-07-04)
**Status at sprint open:** Conditional — gate 2026-07-04

**Scope:**
After 4 weeks of production operation (≥ 2026-07-04): extract p99 latency from Render logs for POST /digest/si05/send. Compare against BLG-OPS-54 pre-launch baseline. If p99 > 2× baseline: file a performance investigation item; otherwise record PASS.

**Acceptance Criteria:**
- AC-01: Post-4-week p99 latency extracted from Render logs for POST /digest/si05/send
- AC-02: Comparison against BLG-OPS-54 baseline documented
- AC-03: Performance PASS recorded; or performance investigation item filed if p99 > 2× baseline
- AC-04: Brief performance review note filed
- AC-05: Infrastructure & Operations Owner sign-off
- AC-06: Gate confirmed: ≥ 4 weeks POST /digest/si05/send production operation (2026-07-04)

---

### ST-13 — BLG-GOV-130: SI-05 Phase 2 activation decision scope

**Source:** BLG-GOV-130
**Classification:** Conditional — gate 2026-07-04 (SI-05 effectiveness review complete)
**Effort:** S (~0.5 day)
**Owner:** Product Owner; PMO Lead
**Sprint:** 2 (gate 2026-07-04)
**Status at sprint open:** Conditional — gate 2026-07-04

**Scope:**
After 2026-07-04 effectiveness review: PO reviews review outputs (ST-10) and makes a formal Phase 2 activation decision. Produce decision document: SI-05 Phase 2 activation criteria met/not met, activation timeline (if met), deferral rationale (if not met). File in docs/product/decisions/ as Class 3 Operational Record.

**Acceptance Criteria:**
- AC-01: 2026-07-04 effectiveness review outputs (ST-10) reviewed by Product Owner
- AC-02: Formal Phase 2 activation decision document produced and filed in docs/product/decisions/
- AC-03: If activation criteria met: Phase 2 sprint planning timeline confirmed; SI-02 gate status re-checked
- AC-04: If not met: deferral rationale documented with revised review date
- AC-05: Product Owner sign-off
- AC-06: Gate confirmed: 2026-07-04 effectiveness review complete
