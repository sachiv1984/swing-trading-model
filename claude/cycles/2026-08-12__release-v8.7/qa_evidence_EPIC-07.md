Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-13

---

## Consolidation Block

**EPIC:** EPIC-07 — Governance & Spec Debt
**Cycle:** 2026-08-12__release-v8.7
**Sprint goal:** Deliver v8.7's user-facing feature and theme-consistency completion work while closing the mandatory trade-plan data-integrity carryover from v8.6, backed by expanded test, security, reliability, and governance coverage across the release's remaining six EPICs.
**Test scenarios used:** N/A — governance/documentation-only EPIC, no code changes, no observable UI behaviour

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-18 | `CLAUDE.md` §8 step 2b | New mandatory pre-resolution check for shared-JSON-field schema-shape drift between sibling EPIC branches, added to `CLAUDE.md` §8 (no version field, per established convention). `OPERATIONAL_GUIDE.md` v4.159→v4.160 (header + §14 self-row + Change Log top row, self-consistency confirmed via `governance-drift` skill — 1 self-drift found and fixed in the same pass, see notes). `prompt_change_log.md` appended per the established no-version-field `CLAUDE.md` convention. | See `stage4_backlog_slice.md#ST-18` | Pass | None found |
| ST-19 | `docs/product/roadmap_unlock_tracker.md` | Consolidated Roadmap Unlock Tracker covering all 9 named roadmap-level Arc feature gates (SI-02, SI-05 Phase 2, PO-02/04/05, PS-01–05), cross-checked against `scan_backlog_gate_conditions.py`'s broader item-level scan (294 items, 175 gated) to confirm scope. Found and corrected the source backlog item's stale premise (SI-04 listed as still-gated; it shipped v7.7) and 2 further tracking gaps (PO-02, PO-05) — disclosed, not silently resolved. **Write-scope limitation:** `current_roadmap.md` §6 cross-reference could not be added directly — `claude/roadmap/*` is outside Sprint Execution's write scope (`execution_prompt.md` §7); flagged for the next `run roadmap`/`manage roadmap` pass. | See `stage4_backlog_slice.md#ST-19` | Pass with notes | None — write-scope boundary correctly respected and disclosed rather than worked around |
| ST-20 | `docs/product/decisions/decisions--2026-08-12__release-v8.7--confidence-interval-preview-analytics-section13-policy.md` | Formal §13 policy determination: confidence-interval-qualified "preview" analytics (PS-01/PS-02 class) are **Permitted, with 4 conditions** — reasoning distinguishes computational determinism (unchanged by sample size) from statistical reliability; explicitly scopes the ruling away from genuinely forward-looking analytics (PS-03), which would need its own separate assessment. **Write-scope limitation:** `strategy_rules.md` §13 itself could not be edited directly (`claude/strategy/strategy_rules.md` is outside Sprint Execution's write scope) — recorded as the AC's own permitted alternative ("or a linked policy note"), with the cross-reference addition flagged for a future authorized routine. | See `stage4_backlog_slice.md#ST-20` | Pass | None — write-scope boundary correctly respected |
| ST-21 | `docs/specs/frontend/design_system.md#Shared UI Components` | **Pre-met.** The canonical `gated` `DataState` variant was already fully specified and approved during this cycle's own Design Gate phase (2026-08-12, commit `31590f41`, `design_system.md` v1.9→v1.10) — before Sprint Execution began. Verified by direct inspection: variant present, cross-referenced, visual/interaction behaviour (evaluation order, `Lock` icon, copy pattern, no default CTA, optional `gatedProgress`) fully specified per the AC. | See `stage4_backlog_slice.md#ST-21` | Pass | None — pre-met, verified not re-implemented |

**Requirement (OA-3/ST-03) AC coverage check:** ST-18's 1 AC — covered (rule added, logged per convention). ST-19's 2 ACs — AC-1 (consolidated tracker) covered; AC-2 (cross-referenced from `current_roadmap.md` §6) not directly actionable by this routine, disclosed as a write-scope limitation with a concrete follow-up action named, not silently dropped. ST-20's 2 ACs — AC-1 (determination recorded) covered via the linked-policy-note alternative the AC itself permits; AC-2 (Strategy Rules & System Intent Owner sign-off) covered via agent-mediated sign-off. ST-21's 2 ACs — both covered, pre-met.

**QA test coverage:**
- Scenarios run: N/A (no code changes this EPIC)
- Regression areas checked: full local pytest suite re-run after `CLAUDE.md`/`OPERATIONAL_GUIDE.md` edits (1100 passing, 5 skipped, no regressions — governance-doc-only changes, expected no test impact)
- Known deviations: None found — all stories' deviation checks completed with nothing to file

---

## Governance self-consistency check (mandatory per execution_prompt.md §3.2.A, since OPERATIONAL_GUIDE.md's version was bumped this EPIC)

Ran the `governance-drift` skill's Step 1b 3-way self-consistency check (document header / §14 self-row / Change Log top row) before this EPIC's DoQ sign-off, per the mandatory rule. **Found 1 SELF-DRIFT:** the §14 self-row (`| Version | 4.159 |` / `| Last Updated | 2026-08-12 |`) had not been updated in the same edit as the document header and Change Log top row (both correctly bumped to `4.160`/`2026-08-13`). Fixed in the same session, before this qa_evidence entry was written — all three now read `4.160`/`2026-08-13`. This is exactly the class of gap the mandatory check (added at lifecycle audit AUD-2026-08-12, itself referenced in the very `4.157` Change Log entry two rows below this EPIC's own new row) exists to catch — confirming the check's own value in the same session it was most recently hardened.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] No frontend component modified by this EPIC (governance/documentation-only) — URL-base-variable check not applicable
- Signed off by: Sprint Execution Engine (agent-mediated, Head of Specs Team role — §5.3)
  Sprint Execution Engine (agent-mediated, PMO Lead role — §5.3)
  Sprint Execution Engine (agent-mediated, Strategy Rules & System Intent Owner role — §5.3)
- Date: 2026-08-13
- Comments: ST-19 and ST-20 both hit the same class of write-scope boundary (`claude/roadmap/*` and `claude/strategy/strategy_rules.md` respectively, both explicitly excluded from Sprint Execution's write scope per `execution_prompt.md` §7) — both correctly produced their substantive deliverable as a standalone document (the AC's own named alternative in ST-20's case; the only viable option in ST-19's) rather than attempting an out-of-scope write or silently skipping the story. Both flag a concrete, named follow-up action for a routine that does hold the relevant write access. ST-21 confirmed pre-met by direct inspection, not assumed from the design-gate changelog reference alone. Governance self-consistency check (above) caught and fixed a real 1-field self-drift in this EPIC's own `OPERATIONAL_GUIDE.md` edit before sign-off.

