**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-08-04
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Created by:** ST-14 (BLG-GOV-278, EPIC-03, v8.2)

---

# Idea-Intake Backlog-Overlap Check Effectiveness Retrospective

## 1. Purpose

`idea_intake_prompt.md` v2.8 (shipped 2026-07-27) upgraded the §2.0 step 5 backlog-scope-overlap check from advisory prose to a mandatory act: submitting agents must grep-check `backlog.md` for their planned topic before finalising a submission, and a submission restating an existing item with no materially new angle no longer counts toward the agent's minimum. This retrospective assesses whether the change materially reduced downstream STEP 4 (roadmap engine idea classification) rejection rates, per ST-14 (BLG-GOV-278).

## 2. Trigger for v2.8

The check was added reactively, in-cycle, after `2026-07-27__scheduled`'s idea intake window (`IW-20260727-01`) found 23 of 44 submissions (52%) duplicated existing open backlog items at STEP 4 — the check had existed as prose since v2.0 but was confirmed, retroactively, to not actually be performed at submission-generation time across the 20+ windows preceding it (`claude/system/changelogs/idea_intake_changelog.md` v2.8 entry).

## 3. Before / After Data

| Window | Date | Idea Intake Prompt Version | Submissions | STEP 4 Rejected (duplicate/overlap) | Rejection Rate | Pre-submission Reframes |
|--------|------|------------------------------|--------------|--------------------------------------|-----------------|---------------------------|
| `IW-20260727-01` | 2026-07-27 | v2.7 (pre-fix — overlap check advisory-only) | 44 | 23 (22 explicitly identified as duplicates) | **52.3%** | 0 (no mandatory pre-check existed) |
| `IW-20260728-01` | 2026-07-28 | v2.8 (mandatory check active) | 44 | 0 | **0%** | 20 of the initially-planned topic-slots dropped/reframed *before submission*, per `decision_log.md` DL-077 |

Source: `claude/roadmap/decision_log.md` DL-076 (`IW-20260727-01`, pre-fix baseline) and DL-077 (`IW-20260728-01`, first post-fix window).

## 4. Sample Size Caveat

**This retrospective has exactly one post-fix data point.** No idea intake window has run since `IW-20260728-01` (2026-07-28) as of this retrospective's authoring date (2026-08-04) — the ideas register has held 0 open ideas continuously since the 2026-07-30 housekeeping closure per `.claude_current_state.json`'s `last_ideas_housekeeping_outcome`, and the CLAUDE.md auto-invoke condition for idea intake (fewer than 20 open ideas) has not fired again in the interim because no `run roadmap` cycle has reached STEP -1.6 since. A single before/after pair is directionally strong (52.3% → 0%) but is not yet a statistically robust trend — a single unusually light-overlap window could coincidentally produce a 0% reading regardless of the check's effect.

## 5. Assessment

Despite the single-data-point limitation, the result is a **strong positive signal**, not merely a coincidental zero:

- The 0% outcome is explained mechanistically, not just observed as a number: DL-077 explicitly records that 20 of the planned topic-slots were **caught and reframed before submission** — i.e. the check is verifiably doing the work it was designed to do (catching overlap at generation time), not simply correlating with a quieter window.
- The magnitude of the swing (52.3 percentage points) is large relative to plausible window-to-window noise in prior cycles (rejection rates in the surrounding governed rebalances — DL-070: 8/44=18%, DL-075: 9/44=20%, DL-076: 23/44=52% — show the 52% reading itself was already the outlier, and the immediate next window returning to 0% rather than reverting to the ~18-20% pre-outlier baseline is consistent with the fix, not just reversion to mean).

**Correction (caught at PMO Lead review, 2026-08-04):** An earlier draft of this section cited a supposed second data point ("DL-078 onward... confirm the pattern held at the next rebalance too"). No `DL-078` exists — `decision_log.md` ends at DL-077, and `.claude_current_state.json`'s `last_rebalance_cycle` is still `2026-07-28__scheduled` (DL-077 itself). That bullet was double-counting the single `IW-20260728-01`/DL-077 data point as if it were independent confirmation from a later window. Removed — §4's single-data-point caveat stands as the accurate position; no second window has run.

## 6. Recommendation

**Keep** the v2.8 mandatory backlog-overlap check unchanged. Do not adjust or retire it.

**Follow-up (non-blocking):** Re-run this retrospective after 2-3 more idea-intake windows accumulate (once the register next drops below the 20-open-idea threshold and a new window opens) to confirm the single-window result holds under a larger sample, rather than treating this retrospective as final validation. No backlog item filed for this follow-up — it is naturally triggered by the next `run ideas` / `run roadmap` STEP -1.6 invocation; PMO Lead should informally sanity-check the STEP 4 rejection rate at that time against this retrospective's baseline.

## 7. Sign-off

- **PMO Lead:** agent-mediated sign-off — 2026-08-04 (ST-14, EPIC-03, v8.2)
