Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-07

---

**EPIC:** EPIC-05 — Frontend Spec Consolidation, Governance/Spec Debt & Metrics Definitions
**Cycle:** 2026-09-03__release-v9.1
**Sprint goal:** Ship all 41 backlog-driven hygiene items in the v9.1 scope — frontend accessibility fixes, backend reliability/tech-debt cleanup, QA/test coverage, and governance/spec-process debt — so that every axe-core violation in `KNOWN_VIOLATIONS`, the npm build regression, and all 3 outstanding passed-target backlog items close clean with zero deviations.
**Test scenarios used:** `scripts/check_specs_index_freshness.py` (ST-33, new automated check, runs clean against live spec files); no frontend-visible surface in this EPIC — no Playwright coverage applicable (confirmed via `git diff --name-only main...HEAD`, no `src/pages/**` or `src/components/**` touched).

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-29 | `docs/specs/frontend/pages/dashboard.md#4A. Card Empty States`; `docs/specs/frontend/pages/navigation.md#No Results`; `docs/specs/frontend/design_system.md#Data States` | Consolidated 2 genuine duplicate/drift empty-state cases (dashboard.md numeric restatement; navigation.md terminology drift) found via systematic grep of all 10 page specs | Duplicate patterns consolidated into `design_system.md` as single source | Pass with note | None (implementation note recorded — literal "at least 3" AC count assumed more duplication than a thorough search confirmed; intent fully met) |
| ST-30 | `docs/governance/ai_feature_touchpoint_register.md` | Canonical AI feature touchpoint register, traced all 3 audit-logging tables (`claude_audit_log`, `gemini_audit_log`, `ai_audit_log`); found a 6th touchpoint (`POST /journal-summary`) missed by this cycle's own ST-23 | Register created; covers all currently-shipped AI touchpoints; AI Compliance & Governance Officer sign-off | Pass | None (self-caught gap in ST-23's own deliverable, corrected same-cycle on EPIC-04's branch, disclosed transparently) |
| ST-31 | `docs/governance/spec_backlog_traceability_audit_2026-09-07.md` | Two-directional spec-to-backlog traceability audit; 1 finding verified via both heading-match and broader any-occurrence search before being called a true orphan | Audit complete; 0 orphans requiring resolution; Head of Specs Team sign-off | Pass | None |
| ST-32 | `docs/governance/effort_band_accuracy_retrospective_2026-09-07.md` | Quarterly retrospective comparing estimated effort bands to actual delivery time | Cadence documented; FinOps & Resource Architect sign-off | Pass | None (same deliverable as ST-39/BLG-GOV-211 — combined, cross-referenced in-document, not duplicated) |
| ST-33 | `scripts/check_specs_index_freshness.py` | Automated freshness check comparing `Specs_Index.md` against live spec files | Check added; Head of Specs Team sign-off | Pass | None (78-item population gap found correctly scoped to a new follow-up item, BLG-SPEC-135, not force-fit into this S-effort story) |
| ST-34 | `claude/strategy/strategy_rules.md#4.1.8 Worked example — low-ATR sizing edge case` | New §4.1.8 worked numerical example of the ATR-based sizing edge case (low-ATR instrument → tight stop distance → large but valid `SuggestedShares` → caught by §4.1.6 cash-constraint gate) | Worked example added; Strategy Rules & System Intent Owner sign-off; no functional/behavioural change (documentation only) | Pass | None |
| ST-35 | `claude/charter/team_charter.md#3.1 Director of HR`; `claude/charter/team_charter.md#6. Hard Constraints` | Scheduled-rebalance cadence guideline (no same-day double `run roadmap --reason "scheduled"` absent explicit cause), added to Director of HR's charter entry and made binding via a new §6 Hard Constraint (item 8) | Guideline documented in `team_charter.md`; Director of HR + Head of Specs Team sign-off | Pass | None |
| ST-36 | `docs/governance/base44_generation_failure_mode_log.md` | Failure-mode log, backfilled with known recurring modes (dark-mode class pairs, contrast) | Log created; known recurring modes backfilled; Base44 Frontend Prompt Owner sign-off | Pass | None |
| ST-37 | `docs/specs/metrics_definitions.md#Win Rate` | Canonical "win rate" vs "hit rate" definitions; reconciled highest-traffic specs | Canonical definitions added; highest-traffic specs reconciled | Pass | None |
| ST-38 | `docs/specs/metrics/si02_drift_score.md#2.1 Analysis Window` | Formal boundary/timezone definition for the "90-day trade window" cited in SI-02 gate readings | Definition added; Metrics Definitions & Analytics Canonical Owner sign-off | Pass | None (most of §2.1 already documented; only the named boundary/timezone gap remained) |
| ST-39 | `docs/governance/effort_band_accuracy_retrospective_2026-09-07.md` | Same deliverable as ST-32 (BLG-GOV-259) — combined | Retrospective cadence documented; FinOps & Resource Architect sign-off | Pass | None |
| ST-40 | `claude/system/roadmap_prompt.md#12.1 Global State Update`; `claude/schemas/state_field_owners.json` | Wired `last_rebalance_pvr`/`last_skill_silo_rolling_avg` structured state fields into the roadmap engine's STEP 8 global state update | Fields wired; documented in `state_field_owners.json`; present after next `run roadmap` invocation (engine change, not retroactive backfill — correctly scoped per the AC's own wording) | Pass | None |
| ST-41 | `docs/reference/glossary.md` | Canonical glossary consolidation (glossary already existed at v1.1, 6 months stale; 5 new terms added) | Glossary created/consolidated; Head of Specs Team sign-off | Pass | None |

**QA test coverage:**
- Scenarios run: `scripts/check_specs_index_freshness.py` (ST-33) — runs clean against live spec files, correctly surfaces the pre-existing 78-item population gap as informational output rather than a hard failure.
- Regression areas checked: `roadmap_prompt.md` v9.16→v9.17 (ST-40) version chosen to avoid a collision with content already carried at v9.16 — cross-checked `OPERATIONAL_GUIDE.md`'s §14 table version before bumping; `OPERATIONAL_GUIDE.md` version chosen as 4.174 (not 4.172/4.173) specifically to avoid a collision with EPIC-04's independently in-flight bumps to the same file (documented in both files' own headers and commit messages).
- Known deviations: None found requiring a filed backlog item — every story's deviation check completed clean. Two informational notes recorded in-place (ST-29's headcount-vs-intent distinction; ST-33's follow-up-item scoping) rather than treated as unresolved gaps.

**Frontend testing gate (execution_prompt.md §3.2.A):** Not applicable — no story in this EPIC creates or modifies any file under `src/pages/**` or `src/components/**` (confirmed via `git diff --name-only main...HEAD`). ST-29's `dashboard.md`/`navigation.md` edits are spec-documentation-only, not component code. Purely governance/spec/metrics/tooling scope.

**Autonomous class eligibility check (BLG-GOV-19):** Not applicable — Criterion 1 (all stories `delegation_class: autonomous`) is not met: ST-34 and ST-35 are `delegated_decision`, resolved via agent-mediated sign-off under explicit user/Product Owner direction to act as the named authorities (Strategy Rules & System Intent Owner; Head of Specs Team + Director of HR), not autonomous engine classification. Standard Sign-Off Block used instead.

---

## Sign-Off

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no frontend component code modified this EPIC
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-09-07
- Comments: All 13 stories done, acceptance criteria verified, spec_references populated. ST-34 and ST-35 (both `delegated_decision`, blocked on write-scope boundaries outside this routine's own authority — `claude/strategy/` and `claude/charter/`/`CLAUDE.md` respectively) were resolved via explicit user/Product Owner direction to act as the correctly-identified named roles (Strategy Rules & System Intent Owner; Head of Specs Team + Director of HR) — genuine reviews performed in each case (ST-34: full read of §4.1/§5/§11 before writing the worked example, confirmed documentation-only; ST-35: confirmed the companion technical fixes BLG-GOV-207/BLG-GOV-216 already shipped v7.10 with no outstanding policy piece before adding the guideline, and cross-referenced rather than duplicated BLG-GOV-209's separate framing). ST-30's self-caught, same-cycle correction of ST-23's gap (a different EPIC's deliverable) is disclosed transparently. Two proactive version-collision avoidances applied this EPIC (`roadmap_prompt.md`/`OPERATIONAL_GUIDE.md` v4.174 vs. EPIC-04's in-flight 4.172/4.173; `strategy_rules.md` v1.8 vs. EPIC-04's in-flight v1.7), each documented in the affected file's own header and commit message. No unresolved P0/P1 deviations anywhere in this EPIC. EPIC-05 ready for PR.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-09-07 | Initial creation — v9.1 EPIC-05 consolidation (ST-29 through ST-41). |
