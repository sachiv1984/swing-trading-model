**Owner:** Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-23
**Sprint:** 2026-03-21__release-v2.2 — ST-13, ST-14, ST-15

---

# QA Evidence — EPIC-05: Governance Process Enhancements

**EPIC:** EPIC-05 — Governance Process Enhancements
**Cycle:** 2026-03-21__release-v2.2
**Sprint goal:** Apply three governance process improvements that address friction from prior cycles: provisional target signal (BLG-GOV-04), effort sizing handoff (BLG-GOV-05), and structured lessons learnt carry-forward (BLG-GOV-06). All require CLAUDE.md §6 governance edit checklist compliance.

---

## ST-13 — Roadmap Engine: Provisional-Target Field at Backlog Promotion

**Spec references:** `claude/system/roadmap_prompt.md` v4.5; `claude/system/shared_standards.md` v2.5; `claude/system/release_planning_prompt.md` v2.22
**What was built:** `shared_standards.md §16.6` (Provisional-Target field syntax, horizon-to-release mapping, TBD fallback). `roadmap_prompt.md` STEP 9 Write Plan §3 updated (Provisional-Target field required on newly promoted items). `release_planning_prompt.md` STEP 1.2 added (advisory count of horizon-matched candidates before STEP 2; no halt).

**Acceptance criteria:**

| AC | Criterion | Result | Note |
|----|-----------|--------|------|
| 1 | `roadmap_prompt.md` STEP 9 includes Provisional-Target field requirement on new backlog items | Pass | STEP 9 Write Plan §3 updated — field required, TBD fallback documented |
| 2 | `shared_standards.md` documents the Provisional-Target field format and horizon-to-release mapping | Pass | §16.6 added: syntax, mapping table, TBD fallback, advisory-only rule |
| 3 | `release_planning_prompt.md` STEP 1 reads Provisional-Target as a candidate prioritisation input | Pass | STEP 1.2 added — advisory count, no halt, scope selection remains at STEP 2 |
| 4 | All four §6 checklist steps applied to all modified files | Pass | roadmap_prompt.md v4.5, release_planning_prompt.md v2.24, shared_standards.md v2.7, OPERATIONAL_GUIDE.md v3.36, prompt_change_log.md entries |
| 5 | DoQ sign-off | Pass | See sign-off block below |

**§6 Checklist Compliance:**
| File | Version bump | OPERATIONAL_GUIDE §14 | Phase section header | prompt_change_log.md |
|------|-------------|----------------------|---------------------|----------------------|
| `roadmap_prompt.md` | v4.3 → v4.5 ✅ | v4.5 ✅ | §6 v4.5 ✅ | Entry added ✅ |
| `release_planning_prompt.md` | v2.21 → v2.24 ✅ | v2.24 ✅ | §6B v2.24 ✅ | Entry added ✅ |
| `shared_standards.md` | v2.4 → v2.7 ✅ | v2.7 ✅ | N/A (not a phase prompt) ✅ | Entry added ✅ |

**Deviations:** None

---

## ST-14 — Release Planning: Load scored_initiatives.md for Effort Band Handoff

**Spec references:** `claude/system/release_planning_prompt.md` v2.24; `claude/system/shared_standards.md` v2.6
**What was built:** `shared_standards.md §16.7` (scored_initiatives.md effort band column format, three-tier resolution rule, read-only constraint, handoff contract). `release_planning_prompt.md` STEP 0 updated (read-only load of scored_initiatives.md, effort bands extracted, absence noted in run manifest). STEP 4.5 updated (three-tier effort band lookup + advisory for missing entries).

**Acceptance criteria:**

| AC | Criterion | Result | Note |
|----|-----------|--------|------|
| 1 | `release_planning_prompt.md` STEP 0 includes `scored_initiatives.md` in load list | Pass | STEP 0 updated — read-only load, effort bands extracted, absence recorded in run manifest |
| 2 | STEP 4 capacity check references effort bands from `scored_initiatives.md` where available; falls back to STEP 4 estimate if absent | Pass | STEP 4.5 three-tier rule: (1) use scored band; (2) fallback + advisory; (3) fallback silently |
| 3 | `shared_standards.md` documents the handoff contract | Pass | §16.7 added: effort band column, three-tier rule, read-only constraint |
| 4 | All four §6 checklist steps applied | Pass | Covered by ST-13 commit (same files) |
| 5 | DoQ sign-off | Pass | See sign-off block below |

**§6 Checklist Compliance:** Covered by ST-13/15 combined commit — same files (`release_planning_prompt.md`, `shared_standards.md`) bumped in one operation.

**Deviations:** None

---

## ST-15 — Structured Lessons Learnt Carry-Forward Block

**Spec references:** `claude/system/roadmap_prompt.md` v4.5; `claude/system/release_planning_prompt.md` v2.24; `claude/system/sprint_planning_prompt.md` v2.3; `claude/system/post_ship_closure.md` v2.1; `claude/system/lessons_learnt_prompt.md` v1.8; `claude/system/shared_standards.md` v2.7
**What was built:** `shared_standards.md §16.8` (Carry-Forward section schema, 0–5 item rule, Engine enum, absence rules, STEP 0 read protocol). Three engine STEP 0 carry-forward read advisories (roadmap, release planning, sprint planning). `post_ship_closure.md` STEP 8.5 carry-forward write requirement. `lessons_learnt_prompt.md §3.5` output requirement note + §5 record structure updated with §Carry-Forward section.

**Acceptance criteria:**

| AC | Criterion | Result | Note |
|----|-----------|--------|------|
| 1 | `lessons_learnt_closure.md` schema includes `## Carry-Forward` section, documented in `shared_standards.md` | Pass | shared_standards.md §16.8 added; lessons_learnt_prompt.md §5 record structure updated with Carry-Forward section |
| 2 | `roadmap_prompt.md`, `release_planning_prompt.md`, `sprint_planning_prompt.md` STEP 0 each include Carry-Forward read-and-acknowledge | Pass | All three engines updated — advisory, manifest record, no halt on absence |
| 3 | `post_ship_closure.md` writes Carry-Forward section as mandatory STEP output | Pass | STEP 8.5 updated — section required; zero rows valid; absence is not valid |
| 4 | All four §6 checklist steps applied for all modified files | Pass | See §6 checklist table below |
| 5 | DoQ sign-off | Pass | See sign-off block below |

**§6 Checklist Compliance:**
| File | Version bump | OPERATIONAL_GUIDE §14 | Phase section header | prompt_change_log.md |
|------|-------------|----------------------|---------------------|----------------------|
| `roadmap_prompt.md` | v4.3 → v4.5 ✅ | v4.5 ✅ | §6 v4.5 ✅ | Entry added ✅ |
| `release_planning_prompt.md` | v2.21 → v2.24 ✅ | v2.24 ✅ | §6B v2.24 ✅ | Entry added ✅ |
| `sprint_planning_prompt.md` | v2.2 → v2.3 ✅ | v2.3 ✅ | §7 v2.3 ✅ | Entry added ✅ |
| `post_ship_closure.md` | v2.0 → v2.1 ✅ | v2.1 ✅ | §10 v2.1 ✅ | Entry added ✅ |
| `lessons_learnt_prompt.md` | v1.7 → v1.8 ✅ | v1.8 ✅ | N/A (not a phase prompt) ✅ | Entry added ✅ |
| `shared_standards.md` | v2.4 → v2.7 ✅ | v2.7 ✅ | N/A ✅ | Entry added ✅ |

**Deviations:** None

---

## EPIC-Level Consolidation

| ST Item | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|---------------------|---------|----------|
| ST-13 | shared_standards.md §16.6, roadmap_prompt.md STEP 9, release_planning_prompt.md STEP 1.2 | 5 ACs — all met | Pass | None |
| ST-14 | shared_standards.md §16.7, release_planning_prompt.md STEP 0 + STEP 4.5 | 5 ACs — all met | Pass | None |
| ST-15 | shared_standards.md §16.8, 3 engine STEP 0 advisories, post_ship_closure STEP 8.5, lessons_learnt_prompt §3.5 + §5 | 5 ACs — all met | Pass | None |

---

**QA sign-off block:** (Director of Quality)
- [x] ST-13: Provisional-Target field added to roadmap STEP 9, shared_standards §16.6, release planning STEP 1.2 (advisory only — correct scope)
- [x] ST-14: scored_initiatives.md effort band handoff contract documented in §16.7; STEP 0 read-only load and STEP 4.5 three-tier lookup implemented with advisory for missing entries
- [x] ST-15: Carry-Forward schema in §16.8; three STEP 0 advisories; post_ship_closure STEP 8.5 write requirement; lessons_learnt_prompt §5 record structure updated; zero-rows-valid rule prevents false failures on quiet cycles
- [x] §6 checklist: 6 governance files × 4 checklist items verified — all version bumps, OPERATIONAL_GUIDE §14, phase section headers, and prompt_change_log entries present in single commit
- [x] No unresolved P0 deviations
- Signed off by: Director of Quality (agent-mediated)
- Date: 2026-03-23
