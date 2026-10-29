Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-10-29
Cycle: 2026-10-16__release-v9.13

---

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: v9.13 — Monitor Exit Fix, Exit Reasons & API Call Integrity
Run: 2026-10-16__release-v9.13
Reviewed by: PMO Lead
Date filed: 2026-10-29
Prior cycle checked: 2026-10-12__release-v9.12 (`lessons_learnt_closure.md`). Its 3 Carry-Forward rows are all closed: the rebalance ran on 2026-10-16 (DL-086), the `Provisional-Target` hygiene rule is standing guidance, and the v9.12 sign-offs were confirmed by the human Product Owner and Director of Quality on 2026-10-15. All 7 of its §6 Outstanding Actions were resolved on 2026-10-15.

---

## What worked well

- **The STEP 7.3 sweep found shipped TSG work.** ST-12 and ST-14 shipped `BLG-QA-204` and `BLG-QA-210`, so TSG-v9.9-01 and TSG-v9.9-02 were resolved in the same run. Marking backlog items COMPLETE at STEP 3, before the STEP 7.3 sweep, keeps that working.
- **The deviation consolidation review's broadened scan (v2.38) mattered.** The two v9.13 deviations against `strategy_rules.md` have no `DEV-*` ID. An ID-only scan would have missed both. A "Known deviation" text diff since the last run found them.
- **The governance-drift skill caught a stale §14 self-row date.** It had read 2026-10-15 since the 2026-10-16 rebalance bumped the guide to 4.241. It was fixed in this run's 4.242 bump.
- **The same-cycle application pattern (v2.32) held.** 4 of 8 source actions were applied this run, including the Phase 4 item that named this closure as its target.

---

## Friction Log

### Friction Item 1

**Classification:** Type E — Authority Gap: A decision was needed and no role was clearly empowered to make it

**Recurrence:** No (first closure-phase occurrence). The same root cause appears from the Sprint Execution side in v9.13 Release Planning Friction Item 3 (`LL-v9.13-Release-03`).

**What happened:**
`verification_report.md` §4 routed `BLG-BE-190`'s missing Known Deviations entry to Post-Ship Closure STEP 5, and the PO + DoQ acceptance made the entry a condition. ST-05's §8.4 entry also lacked Priority, Target, Owner and backlog ID. STEP 5's deviation-compliance carve-out would create or complete both. But `post_ship_closure.md` §5 lists `claude/strategy/strategy_rules.md` as sealed for this routine, and CLAUDE.md §2 forbids edits to `claude/strategy/` unless the prompt instructs them. The edit would also require a `DOCUMENTATION_ONLY_VERSIONS` entry in `backend/strategy_version_registry.py`, which is a code change. The engine stopped and asked the user, who chose to escalate rather than edit.

**Where in the routine:**
STEP 5 — Canonical Spec Deviation Compliance Check (and §5 Write Scope Restriction)

**Root cause:**
authority ambiguity / process gap

**Blast radius analysis:**
- What would have propagated: a P2 strategy-rule divergence in core sizing with no entry in the canonical spec, while an acceptance condition stays unmet.
- When it would have surfaced: the next deviation consolidation review, or never if `BLG-BE-190` shipped first.
- Recovery cost if uncaught: low (single file fix).

**Process patch:**
→ Deferred patch (cannot apply this run):
  - File: `claude/system/post_ship_closure.md` (and `claude/system/execution_prompt.md` §7)
  - Section: §5 Write Scope Restriction / STEP 5
  - Change required: give `strategy_rules.md` a named-file write rule for routed Known Deviations entries, with the version-registry step in the same commit, or route them to the file owner by default
  - Owner: Head of Specs Team, with the Strategy Rules & System Intent Owner
  - Target: decision by 2026-11-01T12:19:42Z (`ESC-CLOSE-20261029-02`). The concrete entries are `ESC-CLOSE-20261029-01` (SLA 2026-11-01T12:12:02Z)

### Friction Item 2

**Classification:** Type A — Governance Drift: A documented rule or header requirement was ignored or missed

**Recurrence:** Yes. The `OPERATIONAL_GUIDE.md` self-row drift has recurred 7+ times (see the governance-drift skill, Step 1b). This instance came from the 2026-10-16 rebalance, not this closure.

**What happened:**
The §14 self-row read `| Version | 4.241 |` / `| Last Updated | 2026-10-15 |`. The 4.241 bump (roadmap rebalance `2026-10-16__scheduled`, STEP -1.5) advanced the version cell but not the date cell. The governance-drift skill reported it while checking this run's 4.242 bump. It was corrected to 4.242 / 2026-10-29.

**Where in the routine:**
STEP 8 — immediate lessons-learnt actions, CLAUDE.md §6 checklist

**Root cause:**
document staleness

**Blast radius analysis:**
- What would have propagated: a wrong self-row date in the guide's governance table.
- When it would have surfaced: the next governance-drift check or audit.
- Recovery cost if uncaught: low (single file fix).

**Process patch:**
→ Immediate patch applied this run:
  - File: `claude/system/OPERATIONAL_GUIDE.md`
  - Section: §14 self-row
  - Change: self-row set to the header and Change Log values (4.242 / 2026-10-29)
  - Version: 4.241 → 4.242 (same bump as this run's prompt changes)
  - Confirmed by: Head of Specs Team (post-ship closure STEP 8 authority)
  - Prompt change log entry: Yes. The 4.242 row is appended to `claude/system/prompt_change_log.md`. No prompt change is needed: the skill's Step 1b already detects this, and it worked.

---

## Recurrence Escalations

None. No v9.12 deferred patch is still open. Friction Item 2's pattern is caught mechanically by the governance-drift skill, so no new outstanding action is raised.

---

## Process improvements actioned this run

Consolidated STEP 8 action summary. Sources: Release Planning `lessons_learnt.md` (3 items), `lessons_learnt_cycle.md` Phase 3 (4 items) and Phase 4 (1 item), and 2 closure-phase findings.

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/delivery_verification_prompt.md` | STEP 2.1 | The found-defect severity rule applies to any grade, including `Pass with notes` (`LL-v9.13-P4-01`). Seal-marked `post-merge` ACs are a planned remainder, checked under §5 (`LL-v9.13-P3-03`) | 3.15 → 3.16 | Yes |
| `claude/system/execution_prompt.md` | STEP 5.3; `Pass_with_deviation` self-check | The deviation table lists found P1/P2 defects under any grade (`LL-v9.13-P4-01`). Seal-marked `post-merge` ACs are recorded as planned, not graded as deviations (`LL-v9.13-P3-03`) | 3.87 → 3.88 | Yes |
| `claude/system/sprint_planning_prompt.md` | STEP 6.2 | Post-merge AC seal check: mark `post-merge` and name the tracking item, or the seal is blocked (`LL-v9.13-P3-03`) | 3.22 → 3.23 | Yes |
| `.claude/skills/lessons_learnt.md` | 2026-04-28 `commit-check` row | "Always create a PR immediately" replaced with "open the PR at EPIC completion, once the DoQ sign-off `Date:` is set" (`LL-v9.13-P3-02`) | Not versioned | Not applicable (skill log, not a Class 6 prompt) |
| `claude/system/OPERATIONAL_GUIDE.md` | Header, §7/§8/§9 source-prompt lines, §14 rows and self-row, Change Log | CLAUDE.md §6 checklist for the three prompts, plus the Friction Item 2 self-row fix | 4.241 → 4.242 | Yes |

**Totals: 4 immediate** (P4-01, P3-02, P3-03, and closure Friction Item 2), **4 deferred** (Release-01, Release-02, P3-01, P3-04), **2 escalated** (Release-03 and closure Friction Item 1, filed as `ESC-CLOSE-20261029-02` and `ESC-CLOSE-20261029-01`).

---

## New files created this run

- `docs/governance/deviation_consolidation_review_2026-10-29.md`: the eighth consolidation review (STEP 5.1, cadence-due).
- `claude/cycles/2026-10-16__release-v9.13/closure_escalations.md`: `ESC-CLOSE-20261029-01` and `-02`.

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `scripts/check_local_openapi_contract_completeness.py` (via `.githooks/pre-commit`) | File reading | Read contract files and `openapi.yaml` from the index when run from the hook (`LL-v9.13-P3-01`) | API Contracts & Documentation Owner | v9.14 sprint — `BLG-QA-238` |
| `scripts/check_execution_state_consistency.py`; `claude/system/execution_prompt.md` §9.2 | Mechanical checks | Check `deviations_filed` on `done` stories and the `ESC-EXEC-*` → `open_escalations` mapping (`LL-v9.13-P3-04`) | Head of Specs Team; Head of Engineering | v9.14 sprint — `BLG-GOV-397` |
| `claude/system/release_planning_prompt.md` §1.3a or `claude/system/backlog_management_prompt.md` | Gate-field carve-out / standing step | Give the "gating item shipped — verify" list a write-back path (`LL-v9.13-Release-01`) | Head of Specs Team; PMO Lead | v9.14 sprint — `BLG-GOV-398` |
| — (observation, no prompt change) | `release_planning_prompt.md` §1.4c | P2-first ordering lowered the U share from 42% to 31% while Skill-Silo is above ceiling. Watch the next rebalance's §7.1 reading before considering a §1.4c U-first step (`LL-v9.13-Release-02`) | Head of Specs Team | Next roadmap rebalance |

---

## Escalations

| Issue | Type | Escalated to | Reason |
|-------|------|-------------|--------|
| `strategy_rules.md` Known Deviations entries for `BLG-BE-190` (missing) and ST-05 §8.4 (fields incomplete): `ESC-CLOSE-20261029-01` | Authority ambiguity | Strategy Rules & System Intent Owner | The routine's §5 seals the file, and an edit requires a code change to the version registry |
| Standing write rule for `strategy_rules.md` (Sprint Execution and Post-Ship Closure STEP 5): `ESC-CLOSE-20261029-02` | Authority ambiguity | Head of Specs Team, with the Strategy Rules & System Intent Owner | Granting write access to a §7 governance-hierarchy document is an authority decision |

---

## Carry-Forward

Items: 4

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `next_release` still reads `v9.13`, the release just shipped, and roadmap §1 "Next planned release" is `[TBD]` | Run `run roadmap --reason scheduled`, or make a scoping decision, before `plan release v9.14` | Roadmap |
| 2 | Verification sign-off was agent-mediated at the user's direction for the 6th consecutive cycle (v9.8–v9.13), and is marked "Pending human confirmation" | Confirm or amend the v9.13 DoQ and PO sign-offs, including the `BLG-BE-190` P2 acceptance, before `plan release v9.14` | Release Planning |
| 3 | `BLG-BE-190` (P2, v9.14) fixes a `strategy_rules.md` §4.1.5 divergence. Its Known Deviations entry is not yet written (`ESC-CLOSE-20261029-01`) | If seated, plan the `strategy_rules.md` write route at Release Planning (cf. v9.13 RISK-02), unless `ESC-CLOSE-20261029-02` has set a standing rule | Release Planning |
| 4 | The new STEP 6.2 post-merge AC check applies from the next Sprint Planning | Mark ACs that only a run on `main` or production data can meet as `post-merge`, with a named tracking item, before seal | Sprint Planning |
