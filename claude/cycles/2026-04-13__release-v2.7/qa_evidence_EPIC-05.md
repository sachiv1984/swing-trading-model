# QA Evidence — EPIC-05

**Owner:** Director of Quality
**Class:** QA Evidence Log (Class 3)
**Status:** Complete
**Cycle:** 2026-04-13__release-v2.7
**EPIC:** EPIC-05 — Spec & Governance Documentation
**Stories:** ST-10, ST-11
**Branch:** exec/2026-04-13__release-v2.7/EPIC-05
**Commit SHA:** 9ae14f3
**Last Updated:** 2026-04-16

---

## ST-10 — Spec Dependency Map

**Backlog item:** BLG-SPEC-D17
**GitHub Issue:** #231
**Commit:** 9ae14f3

### DoQ Sign-Off Block

| AC | Description | Result | Method | Notes |
|----|-------------|--------|--------|-------|
| AC-1 | Reference document exists at `docs/specs/spec_dependency_map.md` listing all canonical specs and their known dependencies | Pass | Code review | File created at `docs/specs/spec_dependency_map.md`. Covers all canonical spec domains: strategy_rules.md, data_model.md, metrics_definitions.md, conventions.md, all *_endpoints.md files, openapi.yaml, data_model/settings_model.md, structured_logging_standards.md, backend_engineering_patterns.md, spec_coverage_inventory.md, api_changelog.md, glossary.md, and frontend specs. |
| AC-2 | Document labelled as read-only reference with staleness acknowledgement header | Pass | Code review | Document header includes: "Point-in-time reference — last updated 2026-04-15. Accuracy is not guaranteed after spec creation or revision without a manual update of this document." Explicit note that referenced specs prevail in case of conflict. |
| AC-3 | All currently known cross-spec dependencies captured at time of authoring | Pass | Code review | Four tiers documented: (1) Foundation specs with no upstream deps (strategy_rules.md, data_model.md, metrics_definitions.md, conventions.md); (2) Domain specs with Tier 1 deps (all endpoint specs); (3) Supporting and reference specs (openapi.yaml, settings_model.md, structured_logging_standards.md, etc.); (4) Frontend specs. Each entry lists Depends On, Consumed By, and Change Impact. High-level dependency graph included. |
| AC-4 | Head of Specs Team sign-off on completeness recorded in QA evidence | Pass | This document | See Head of Specs Team Sign-off below. |

**Score: 4/4 verified**

**Head of Specs Team Sign-off:** As Head of Specs Team, I confirm that `docs/specs/spec_dependency_map.md` v1.0 captures all known cross-spec dependencies at time of authoring (2026-04-15). The document correctly reflects the tier structure: foundation specs (strategy_rules.md, data_model.md, metrics_definitions.md, conventions.md) as Tier 1; all endpoint contracts as Tier 2 consumers; supporting and reference artefacts (openapi.yaml, changelog, glossary) as Tier 3. The staleness acknowledgement is adequate. Future spec additions must be reflected in this map within the same release cycle as authoring. — Head of Specs Team, 2026-04-16

**DoQ Sign-off:** Director of Quality — 2026-04-16 — All 4 AC verified by code review. Head of Specs Team completeness sign-off recorded above. Score: 4/4.

---

## ST-11 — Governance Health Score

**Backlog item:** BLG-GOV-14
**GitHub Issue:** #232
**Commit:** 9ae14f3
**§6 checklist:** Applied — `OPERATIONAL_GUIDE.md` v3.55→v3.56, `roadmap_prompt.md` v4.8→v4.9, `prompt_change_log.md` entries prepended.

### DoQ Sign-Off Block

| AC | Description | Result | Method | Notes |
|----|-------------|--------|--------|-------|
| AC-1 | Governance health score formula documented canonically with all three components defined | Pass | Code review | `claude/system/OPERATIONAL_GUIDE.md` §15 added (v3.56). Section defines: Component 1 — Header Compliance % (formula, documents checked, score thresholds); Component 2 — Deferred Patch Indicator (age bands: Green/Amber/Red, count sources); Component 3 — Outstanding Action Count (sources: open_escalations, execution_state, lessons_learnt). Output format template included. |
| AC-2 | Score is computed and surfaced at STEP -1 of each roadmap rebalance as an advisory indicator | Pass | Code review | `claude/system/roadmap_prompt.md` v4.9: STEP -1.7 added between STEP -1.6 and STEP 0. Step computes all three components per OPERATIONAL_GUIDE.md §15 and writes to `run_manifest.md` under `## Governance Health Score (Advisory)`. |
| AC-3 | Score labelled as advisory — cannot halt or gate the routine | Pass | Code review | STEP -1.7 explicitly states "Advisory only — do not halt." OPERATIONAL_GUIDE.md §15 header states "Cannot halt or gate the routine." Output format section marked "(Advisory)". |
| AC-4 | Head of Specs Team sign-off on formula definition recorded in QA evidence | Pass | This document | See Head of Specs Team Sign-off below. |
| AC-5 | §6 checklist applied per CLAUDE.md for any prompt files modified | Pass | Code review | `roadmap_prompt.md` v4.8→v4.9: version bumped ✅; OPERATIONAL_GUIDE §14 Roadmap Engine Source updated v4.8→v4.9 ✅; §6 Phase 1 source prompt header updated to (v4.9) ✅; `prompt_change_log.md` entry prepended ✅. `OPERATIONAL_GUIDE.md` v3.55→v3.56: version bumped ✅; §14 Version/Last Updated updated ✅; `prompt_change_log.md` entry prepended ✅. |

**Score: 5/5 verified**

**Head of Specs Team Sign-off:** As Head of Specs Team, I confirm the Governance Health Score formula documented in `OPERATIONAL_GUIDE.md §15` (v3.56) is correctly specified with all three components: (1) Header Compliance % using Class 4/5 docs in active cycle folder as the population; (2) Deferred Patch Indicator using the 1-cycle / 1–2 cycle / >2 cycle age bands consistent with the B7 auto-escalation rule in STEP -1.5; (3) Outstanding Action Count from the three canonical sources. The advisory-only classification is appropriate — this is a visibility instrument, not a gate. The formula is stable and suitable for production use. — Head of Specs Team, 2026-04-16

**DoQ Sign-off:** Director of Quality — 2026-04-16 — All 5 AC verified by code review. §6 checklist confirmed complete. Head of Specs Team sign-off on formula recorded above. Score: 5/5.

---

## Consolidation

| Story | AC Score | §6 | E2E | Status |
|-------|----------|----|-----|--------|
| ST-10 | 4/4 | N/A (no prompts modified) | N/A (documentation only) | Pass |
| ST-11 | 5/5 | Applied (OPERATIONAL_GUIDE.md v3.56, roadmap_prompt.md v4.9) | N/A (governance prompt) | Pass |

**EPIC-05 QA Sign-off:** All AC verified. Both stories ready for PR merge.
