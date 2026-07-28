Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-27

## ESC-EXEC-20260727-02

**Raised by:** QA & Testing Owner (agent-mediated review of PR #1101, EPIC-14)
**Blocks execution:** No
**Blocks merge:** No — this is a tracked follow-up, not a defect in what's shipped in PR #1101.

**Finding:** ST-14's deliverable (`claude/cycles/2026-07-27__release-v7.9/qa_evidence_EPIC-14.md`, § "Displacement Debt Register — Design") is a complete design, handed off for physical placement — per the write-scope hard gate (`execution_prompt.md` §7), this routine cannot create files under `claude/roadmap/` or edit `claude/system/roadmap_prompt.md`. Two separate actions are required to make the register real and self-sustaining:

1. Create `claude/roadmap/displacement_debt_register.md` using the format and seed content in `qa_evidence_EPIC-14.md`.
2. Edit `roadmap_prompt.md` STEP 8's "Displacement candidate flag" instruction so future cycles actually update this register (not just `initiative_register.md`).

Both actions are needed together — if only (1) lands, the register goes stale immediately after creation with no forcing function to keep it current; if only (2) lands, the instruction points at a file that doesn't exist. Recording this as a tracked escalation (rather than only a prose note inside `qa_evidence_EPIC-14.md`) so the dependency between the two isn't lost once this PR merges and this cycle's artefacts stop being actively read.

**Unblock criteria:** Roadmap Rebalance Engine or Head of Specs Team, at the next `run roadmap` or `manage roadmap` invocation, performs both (1) and (2) together and closes this escalation.

**Status:** Open — non-blocking, tracked for next roadmap-engine touch.
