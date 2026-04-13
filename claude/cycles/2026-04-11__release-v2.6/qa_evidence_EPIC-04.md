**Owner:** Director of Quality
**Class:** Quality Artefact (Class 3)
**Status:** Active
**Last Updated:** 2026-04-11
**Cycle:** 2026-04-11__release-v2.6
**EPIC:** EPIC-04 — Governance & Spec Debt
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# QA Evidence — EPIC-04 (v2.6)

---

## Stories in Scope

| Story | Title | Status |
|-------|-------|--------|
| ST-12 | execution_prompt.md STEP 5.1 Unpushed-Commit Check | ✅ Done |
| ST-13 | Prompt Log Hygiene: §6 Edit Reminders for 3 Engines | ✅ Done |
| ST-14 | Upgrade decision_log.md Hard Gate in roadmap_prompt.md | ✅ Done |
| ST-15 | Frontend Performance Budget Spec | ✅ Done |

---

## ST-12 — execution_prompt.md STEP 5.1 Unpushed-Commit Check

**Acceptance Criteria verification (code review):**

| AC | Description | Evidence | Result |
|----|-------------|----------|--------|
| AC-1 | `execution_prompt.md` STEP 5.1 contains unpushed-commit check using `git log --not origin/<branch> --oneline` | `claude/system/execution_prompt.md` — STEP 5.1 block added after QA Evidence Persistence Check: instructs engine to run `git log --not origin/<branch> --oneline` before sprint close; if any unpushed commits exist, output SHAs/subjects. | ✅ Pass |
| AC-2 | Soft gate if unpushed commits include a `qa_evidence_EPIC-xx.md` file | Check via `git show <sha> --name-only` specified; soft gate (push required before sprint close proceeds). | ✅ Pass |
| AC-3 | Version bumped `v3.2 → v3.3` | Header: `**Version:** 3.3`; `**Last Updated:** 2026-04-11` | ✅ Pass |
| AC-4 | OPERATIONAL_GUIDE §14 updated to v3.3 | Line: `Execution Engine Source | claude/system/execution_prompt.md v3.3` | ✅ Pass |
| AC-5 | OPERATIONAL_GUIDE §8 source prompt header updated to v3.3 | Line: `**Source prompt:** claude/system/execution_prompt.md (v3.3)` | ✅ Pass |
| AC-6 | `prompt_change_log.md` entry appended | Entry: `2026-04-11 | execution_prompt.md | v3.2→v3.3 | ST-12/CF-1: STEP 5.1 Unpushed-Commit Check added...` | ✅ Pass |

**Verification method:** Code review — governance file patch (no observable UI behaviour).

---

## ST-13 — Prompt Log Hygiene: §6 Edit Reminders for 3 Engines

**Acceptance Criteria verification (code review):**

| AC | Description | Evidence | Result |
|----|-------------|----------|--------|
| AC-1 | `design_gate_prompt.md` STEP 7 contains §6 edit reminder | STEP 7 "Governance file edit check (ST-13 / CF-2):" paragraph added after git operations paragraph. | ✅ Pass |
| AC-2 | `design_gate_prompt.md` version bumped `v1.1 → v1.2` | Header: `**Version:** 1.2`; `**Last Updated:** 2026-04-11` | ✅ Pass |
| AC-3 | `amendment_cycle_prompt.md` STEP 9 contains §6 edit reminder | STEP 9 "Governance file edit check (ST-13 / CF-2):" paragraph added. | ✅ Pass |
| AC-4 | `amendment_cycle_prompt.md` version bumped `v1.6 → v1.7` | Header: `**Version:** 1.7`; `**Last Updated:** 2026-04-11` | ✅ Pass |
| AC-5 | `roadmap_prompt.md` STEP 12 contains §6 edit reminder | STEP 12 "Governance file edit check (ST-13 / CF-2):" paragraph added. | ✅ Pass |
| AC-6 | `roadmap_prompt.md` version bumped `v4.7 → v4.8` (combined with ST-14) | Header: `**Version:** 4.8`; combined bump covers both ST-13 and ST-14 changes. | ✅ Pass |
| AC-7 | OPERATIONAL_GUIDE §14 and phase section headers updated for all 3 prompts | §6.5 → v1.2; §6B.8 → v1.7; §6 → v4.8; §14 table rows updated correspondingly. | ✅ Pass |
| AC-8 | `prompt_change_log.md` entries prepended for all 3 files | Three entries dated 2026-04-11 for design_gate, amendment_cycle, roadmap prompts. | ✅ Pass |

**Verification method:** Code review — governance file patch (no observable UI behaviour).

---

## ST-14 — Upgrade decision_log.md Hard Gate in roadmap_prompt.md

**Acceptance Criteria verification (code review):**

| AC | Description | Evidence | Result |
|----|-------------|----------|--------|
| AC-1 | `roadmap_prompt.md` STEP 9 decision_log check upgraded to hard gate with callout block | `> **⚠ HARD GATE (ST-14 / BLG-GOV-15):**` callout block added after existing `(structural)` enforcement comment. States: decrease in entry count = violation; do not commit; do not proceed to STEP 10; surface violation with pre/post counts; halt. | ✅ Pass |
| AC-2 | Callout states gate is not bypassed by time pressure or delivery context | Text: "This gate is structural — it is not bypassed by time pressure or delivery context." | ✅ Pass |
| AC-3 | OPERATIONAL_GUIDE §1 Hard Rules table updated to reflect structural enforcement | Decision log row updated from "governance convention, not a hard gate" to "structural hard gate enforced by Roadmap Engine STEP 9; a decrease in entry count halts the engine and blocks commit" | ✅ Pass |
| AC-4 | `roadmap_prompt.md` version bump captured (combined with ST-13 as v4.7→v4.8) | Confirmed — single version bump covers both patches, per ST-13 evidence. | ✅ Pass |
| AC-5 | `prompt_change_log.md` entry captures ST-14 content | Entry for `roadmap_prompt.md v4.7→v4.8` explicitly documents both ST-13 and ST-14 changes. | ✅ Pass |

**Verification method:** Code review — governance file patch (no observable UI behaviour).

---

## ST-15 — Frontend Performance Budget Spec

**Acceptance Criteria verification (code review):**

| AC | Description | Evidence | Result |
|----|-------------|----------|--------|
| AC-1 | `docs/specs/frontend/performance_budget.md` exists | File created at `docs/specs/frontend/performance_budget.md`. | ✅ Pass |
| AC-2 | Defines page load time targets (FCP, LCP, TTI) | §3.1: FCP ≤ 1,500ms; LCP ≤ 2,500ms; TTI ≤ 3,000ms (frontend rendering overhead only, on local prod build). | ✅ Pass |
| AC-3 | Defines JS bundle size targets (main bundle, code-split chunks, total) | §3.3: main ≤ 200KB gzip; per chunk ≤ 80KB gzip; total ≤ 500KB gzip. | ✅ Pass |
| AC-4 | Targets aligned to BLG-OPS-05 API latency floor | §2 explicitly documents observed p95 ranges from `docs/ops/api_performance_baseline.md` (1,300–6,200ms) and states targets are rendering overhead budgets separate from backend latency. | ✅ Pass |
| AC-5 | Measurement methodology documented | §4: bundle size via `gzip -c`, Lighthouse via CLI or DevTools for load performance. | ✅ Pass |
| AC-6 | Scope limitation stated (no code instrumentation in this version) | §5 explicitly states no automated CI enforcement in scope. | ✅ Pass |
| AC-7 | Correct Class 2 (Frontend Specification) header with Owner field | Header: `Class: Frontend Specification (Class 2)`, `Owner: Frontend Specifications & UX Documentation Owner`. | ✅ Pass |

**Verification method:** Code review — documentation spec (no observable UI behaviour or code change).

---

## DoQ Sign-Off

**Director of Quality:** Sprint Execution Engine (autonomous EPIC-04 — governance/spec items only; code review verification method applies to all 4 stories; no interactive UI behaviour)

**Date:** 2026-04-11

**Notes:** All 4 stories in EPIC-04 are governance documentation patches or specification documents. Verification by code review is the appropriate and sufficient method for this class of work. No AC in this EPIC requires observable UI behaviour, interactive testing, or staging run. Post-merge action: none required.

---

## Director of Quality Counter-Sign (Delivery Verification Gate)

**Reviewed by:** Director of Quality
**Date:** 2026-04-12
**Context:** Counter-sign issued at delivery verification preflight (Tier 2 — prior signer was Sprint Execution Engine acting as autonomous DoQ; this note confirms independent DoQ review and acceptance).

**Review finding:** All 4 stories are governance documentation patches or specification documents. Code review is the appropriate and sole sufficient verification method for this work class — there is no observable UI behaviour, no staging required. All AC items verified against the modified files. Version bumps, OPERATIONAL_GUIDE updates, and prompt_change_log entries confirmed present. No P0/P1 deviations.

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked (prompt engine invocation paths for 3 modified governance prompts)
- [x] No direct URL construction outside api.* wrapper (N/A — governance document items)

**Signed off by:** Director of Quality
**Date:** 2026-04-12
**Comments:** QA evidence accepted. CF-1 and CF-2 carry-forward items from v2.5 confirmed closed. Performance budget spec (ST-15) confirmed complete and correctly classified as Class 2 Frontend Specification.
