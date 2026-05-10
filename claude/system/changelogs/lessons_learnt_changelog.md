**Owner:** Head of Specs Team
**Status:** Active

# Change Log — Lessons Learnt Prompt

This file contains the historical change log for `claude/system/lessons_learnt_prompt.md`.
The prompt itself contains only the current version — full history is here.

---

| Version | Date | Change |
|---------|------|--------|
| 1.7 | 2026-03-14 | AUD-2026-03-13-007: §1.1 Required Invocation Context added — hard gate requiring 4 structured fields (invoking_routine, cycle_id, phase, prior_cycle_id); halts on absent context. AUD-2026-03-13-022: lessons_learnt_cycle.md section headers normalised — Phase 3/4 headers changed from `## Phase 3 — <cycle_id>` to stable `## Phase 3` with cycle_id as metadata field; idempotency guards updated to two-part check (header + Cycle field); §4.2 template, 4.1 output table, and 3.7 recurrence table all updated for consistency. |
| 1.6 | 2026-03-10 | **§3.2 Release Planning inputs alignment.** Old stage file list replaced with `release_plan.md` (consolidated intermediate, aligned with `release_planning_prompt.md` v2.11+ artefact consolidation). `stage4_backlog_slice.md`, `escalations.md`, `cycle_summary.md`, and `run_manifest.md` retained. |
| 1.5 | 2026-03-10 | **IMP-28 lessons learnt consolidation + IMP-37 amendment append.** §3.3 (Sprint Execution) and §3.4 (Delivery Verification) restructured as append-only phase-tagging sections: output target changed to `lessons_learnt_cycle.md` phase sections; idempotency guards added. §3.5 (Post-Ship Closure) updated. §3.6 added (IMP-37 Amendment). Old §3.6 Cross-Cycle Recurrence Check renumbered §3.7. §4.1 output path table updated. §4.2 Structured Table Block Format added. **IMP-35 (gap 2):** idempotency guard built into §3.3 append logic. |
| 1.4 | 2026-03-06 | **Continuous improvement additions.** Prompt change classification requirement added. Prompt change log as required output (§4.3). §3.6 cross-cycle recurrence check updated. §5 record structure updated. §6.2/6.3/6.4 action rules enforced. §8 completion condition updated. |
| 1.3 | 2026-03-04 | Added §3.6 Cross-Cycle Recurrence Check. Added Friction Classification system (Type A–E). Added Blast Radius Analysis. Added Process Patch requirement. Added Type E — Authority Gap. Rewrote §5 record structure. Added Recurrence Escalations section. Added Outstanding Deferred Patches table. Rewrote §6 action rules. Updated completion condition (§8). |
| 1.2 | 2026-03-03 | Added §3.4 (Delivery Verification inputs) and §3.5 (Post-Ship Closure inputs). Added output path entries for Delivery Verification and Post-Ship Closure to §4.1. |
| 1.1 | 2026-03-02 | Added §3.3 (Execution routine inputs) and §4.1 (Output path override) to support Sprint Execution Engine. |
| 1.0 | 2026-03-02 | Initial version. Roadmap Rebalance and Release Planning routines. |
