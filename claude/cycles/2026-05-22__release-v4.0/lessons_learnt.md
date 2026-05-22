Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v4.0
Cycle: 2026-05-22__release-v4.0
Last Updated: 2026-05-22

---

# Lessons Learnt — v4.0 Release Planning

*This file captures lessons from the release planning phase only. Sprint execution lessons are appended during post-ship closure.*

---

## Planning Phase Observations

### LP-01 — v3.9 post-ship artefacts stranded on unmerged branch

**What happened:** The v3.9 post-ship closure artefacts (`closure_record.md`, `verification_report.md`, `lessons_learnt_closure.md`, prompt patches for OA-03/OA-04) were committed to `hotfix/research-atr-signal-fields` but not merged to main before v4.0 planning was initiated. The global state file reflected `post_ship_complete=false`, triggering a hard gate failure at STEP -1.6.

**Root cause:** Post-ship closure session ended without pushing the merge to main; branch remained unmerged.

**Resolution:** Located artefacts via `git show origin/hotfix/...:path` archaeology; resolved 3-way merge conflicts (OPERATIONAL_GUIDE.md, sprint_planning_prompt.md, prompt_change_log.md) per CLAUDE.md §8; cherry-picked one unpushed commit (DL-033 rebalance); pushed to main.

**Carry-forward:** None — the fix is complete. Advisory: at post-ship closure, always verify `git log --oneline origin/main | head -3` confirms the closure commit landed before ending the session.

---

### LP-02 — Both branches independently claimed OPERATIONAL_GUIDE v4.00

**What happened:** The hotfix branch and the main branch (from OA-01+OA-02 commit b115b9b4) both independently incremented OPERATIONAL_GUIDE.md to v4.00 with different content.

**Root cause:** Two parallel governance patch streams (OA-03/04 on hotfix, OA-01/02 on main) both applied version bumps without awareness of each other.

**Resolution:** Applied union rule from CLAUDE.md §8: combined all changelog entries, bumped header to v4.01, maintained all changes from both sides under distinct version numbers.

**Carry-forward:** None — version collision is handled by the §8 union rule. This case validates that the policy works as designed.

---

## Carry-Forward Actions (Mandatory for v4.1 planning)

| ID | Action | Owner |
|----|--------|-------|
| — | None at release planning time | — |

*Sprint execution carry-forward actions to be appended at post-ship closure.*

---

## Appendix — Prompt Version State at v4.0 Planning

| Prompt | Version | Last Changed |
|--------|---------|--------------|
| execution_prompt.md | v3.27 | OA-03 2026-05-22 |
| sprint_planning_prompt.md | v3.6 | OA-04 (BLG-GOV-30+31) 2026-05-22 |
| release_planning_prompt.md | v2.31 | 2026-05-21 |
| shared_standards.md | v3.3 | BLG-GOV-30 2026-05-22 |
| OPERATIONAL_GUIDE.md | v4.01 | Conflict resolution 2026-05-22 |
