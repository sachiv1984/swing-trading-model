Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-03 (ESC-CLOSE-20261103-01 and -02 dispositions set to Resolved — option (a) each; execution_prompt.md v3.92, release_planning_prompt.md v2.67); prior — 2026-11-03 (both filed)
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
| Disposition | Resolved — 2026-11-03T08:48:01Z |
| Resolved by | Head of Specs Team with the Product Owner (agent-mediated per `execution_prompt.md` §5.3, on explicit user direction 2026-11-03: "have relevant agent deal with esculations"; role ownership checked per the CLAUDE.md §2 rule — both escalations name the Head of Specs Team and Product Owner) |
| Resolution | **Option (a), narrowed.** A PR merge by the human who holds the Director of Quality and Product Owner roles counts as that person's QA sign-off and PO acceptance for the always-human rows, and is recorded in `## Merge Gate Confirmations` as "confirmed by merge" with who, when and merge commit. An agent-mediated review never counts, and a merge by anyone not holding both roles is recorded as no confirmation (a process deviation). Rationale: in this single-owner repository the merger and the accepting authority are the same person, and the act of merging is their acceptance; option (b) would add a ceremony with no new evidence, while the narrowing keeps the CLAUDE.md §2 rule that agents never stand in for these rows. Applied as `execution_prompt.md` v3.92 STEP 4 (`OPERATIONAL_GUIDE.md` v4.247). PR #2137 and #2139 were merged by the repository owner and their human confirmations are also recorded (`52242bd3`), so no retroactive deviation arises. |
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
| Disposition | Resolved — 2026-11-03T08:48:01Z |
| Resolved by | Head of Specs Team with the Product Owner (agent-mediated per `execution_prompt.md` §5.3, on explicit user direction 2026-11-03: "have relevant agent deal with esculations"; role ownership checked per the CLAUDE.md §2 rule — both escalations name the Head of Specs Team and Product Owner) |
| Resolution | **Option (a).** `release_planning_prompt.md` §1.4c gains step 1a: after P1 and P2, seat every ready item whose Source names a Post-Ship Closure STEP 8 deferred lessons-learnt action and whose Provisional-Target is this release, in ascending ID order, while capacity remains. The `ESC-CLOSE-20260923-01` ruling stands for every other same-release tag and now notes this one exception. Rationale: those targets are set by Post-Ship Closure under a governed rule (`LL-v9.12-Release-01`), not filed optimistically, which is what the 2026-09-23 ruling addressed; option (b) would distort priority meaning, and option (c) needs a fresh PO override every cycle. Applied as `release_planning_prompt.md` v2.67 (`OPERATIONAL_GUIDE.md` v4.247). First applies to `BLG-GOV-404` and `BLG-QA-240` at `plan release v9.15`. |
| Filed | 2026-11-03T08:13:47Z |
