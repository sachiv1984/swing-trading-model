Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-03 (ESC-CLOSE-20261103-01 and -02 filed)
Cycle: 2026-10-29__release-v9.14

---

# Closure Escalations — 2026-10-29__release-v9.14

Format per `claude/system/shared_standards.md §4`.

---

## ESC-CLOSE-20261103-01

| Field | Value |
|-------|-------|
| Issue | Does a human developer's merge of an EPIC PR, with no separately recorded Director of Quality QA sign-off or Product Owner acceptance, satisfy the always-human merge-gate rows (`execution_prompt.md` STEP 4 and §5.3; CLAUDE.md §2 "Never merge a PR autonomously. QA sign-off and Product Owner acceptance are always required")? At `2026-10-29__release-v9.14` this happened for PR #2137 (EPIC-04) and PR #2139 (EPIC-05), where the only PR review was the agent-mediated one. Raised in `lessons_learnt_cycle.md` Phase 3 Escalations (`LL-v9.14-P3-02`). |
| Type | Decision required — authority ambiguity (`post_ship_closure.md` STEP 8 `decision_required` class) |
| Escalated to | Head of Specs Team, Product Owner |
| Reason | `execution_prompt.md` v3.91 (this closure) now requires a `## Merge Gate Confirmations` section that records the facts, including a bare merge. Whether a bare merge meets the gate is an authority ruling the engine cannot make. |
| Options | (a) A human merge counts as the human Product Owner acceptance and QA sign-off when the merger holds both roles (single-person repository); record it as such in the section. (b) A merge alone never counts; the engine asks for an explicit confirmation before recording the merge, and a merge without one is a process deviation. (c) A merge counts only when the PR carries an explicit human approval or comment from the same person. |
| Tracking | SLA 2026-11-06T08:13:47Z (72h from filing). Related: `closure_record.md` §6 row 1, `execution_prompt.md` v3.91 STEP 4. Non-blocking: v9.14 verification already records the human confirmations for all 7 EPICs (`52242bd3`). |
| Disposition | Open |
| Filed | 2026-11-03T08:13:47Z |

---

## ESC-CLOSE-20261103-02

| Field | Value |
|-------|-------|
| Issue | Release Planning Friction Item 1 (`LL-v9.14-Release-01`) recommends a `release_planning_prompt.md` §1.4c tier, after P1/P2, for backlog items that track a deferred lessons-learnt patch targeted at this release, with the same standing as roadmap-committed items. v9.13's closure deferred `BLG-QA-238`, `BLG-GOV-397` and `BLG-GOV-398` to v9.14; the oldest-first round-robin never reaches new P3 items, and seating them took a Product Owner override. Without them, `roadmap_prompt.md` STEP -1.5 makes them OVERDUE and halts the next rebalance. |
| Type | Decision required — conflicts with a standing Product Owner ruling |
| Escalated to | Head of Specs Team, Product Owner |
| Reason | §1.4c records the `ESC-CLOSE-20260923-01` Product Owner ruling that a same-release `Provisional-Target` tag carries no selection weight. The proposed tier gives one class of such items selection weight, so it narrows that ruling. This routine cannot change a PO ruling as an immediate fix. |
| Options | (a) Add the tier: items whose Source names a deferred lessons-learnt action and whose sprint target is this release are seated after P1/P2, as an explicit exception to `ESC-CLOSE-20260923-01`. (b) Keep the ruling; Post-Ship Closure STEP 8 sets such items to P2 when filing, so the existing P2-first step seats them. (c) Keep the ruling and the per-cycle PO override. |
| Tracking | SLA 2026-11-06T08:13:47Z (72h from filing). Related: `closure_record.md` §6 row 2. Non-blocking for `plan release v9.15`: this closure filed one deferred patch item (`BLG-GOV-404`, P3, v9.15) that the ruling affects. |
| Disposition | Open |
| Filed | 2026-11-03T08:13:47Z |
