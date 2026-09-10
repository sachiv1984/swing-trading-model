**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-09-09
**Source:** ST-07 (BLG-QA-88, EPIC-02, v9.3 sprint execution)

---

# DoQ Sign-Off Template Freshness Check

## Purpose

ST-07's acceptance criteria: confirm `claude/system/templates/qa_evidence_template.md` (the DoQ sign-off template) and the `record-visual-qa` skill (`.claude/skills/record-visual-qa/SKILL.md`) still reflect current staging sign-off practice; document any drift found and file a follow-on item if actionable.

## Method

1. Read the DoQ sign-off template and the `record-visual-qa` skill in full.
2. Sampled actual `qa_evidence_EPIC-*.md` staging sign-off entries across the cycle history (`claude/cycles/*/qa_evidence_EPIC-*.md`) to compare documented format against what is actually being written.
3. Checked git history for actual invocations of the `record-visual-qa` skill (its distinctive commit message format: `[EPIC-xx][ST-xx] Record staging visual QA results — N pass, M fail/fixed, K blocked`).

## Finding: `qa_evidence_template.md` — no drift found

The template's "Standard Sign-Off Block" section is generic — a free-text `Comments:` field, no mandated table structure for staging evidence. This matches actual current practice (see below). No action needed; template is current (v1.13, last bumped 2026-09-09 for an unrelated reason — `Pass_with_deviation` result value, LL-v9.2-P4-01).

## Finding: `record-visual-qa` skill — drift confirmed

The skill's Step 4 mandates a specific structured output format in the QA evidence file:

```
**Visual AC — Staging results ({YYYY-MM-DD}):**
| Check | Result | Notes |
...
**Visual sign-off status:** ✅ Granted / ⏳ Provisional / ❌ Deferred — ...
```

**This format has not been used in any real `qa_evidence_EPIC-*.md` entry since `2026-04-11__release-v2.6`** (`claude/cycles/2026-04-11__release-v2.6/qa_evidence_EPIC-03.md` and `claude/cycles/2026-03-24__release-v2.3/qa_evidence_EPIC-02.md` are the only 2 matches across the entire cycle history for the `"Visual sign-off status"` string). Git history confirms only 3 actual invocations of the skill ever, the most recent on **2026-04-12** (`2307c91d`) — roughly 5 months / ~80 cycles before this review.

Every staging sign-off recorded since then (sampled: `2026-05-18__release-v3.7` ST-10, `2026-07-17__release-v7.5`→`2026-08-03__release-v8.1` ST-10/BLG-QA-115, `2026-07-21__release-v7.7` EPIC-03, and others) instead uses **free-form prose directly in the DoQ sign-off block's `Comments:` field or an ad hoc `Staging sign-off:`/`Staging confirmation:` line** — e.g. `"human staging run performed 2026-08-03 by Director of Quality against the staging deployment... Confirmed: (1)...(2)...(3)..."`. This is a real, functional format — it satisfies CLAUDE.md's frontend testing gate (date recorded, evidence described) — but it is not the format the skill documents itself as producing, and the skill has evidently not been the mechanism used to produce it for ~5 months.

**Root cause (not confirmed, noted for the follow-on item):** possibly the freeform format proved simpler for one-off staging confirmations that don't map cleanly onto the skill's "many named checks in a pre-existing visual test script file" model (the skill assumes a `docs/testing/staging_visual_test_script_ST-xx.md` file with pre-defined check IDs like `V-CHART-01a` — several of the sampled recent staging sign-offs were single ad hoc confirmations with no such pre-authored script).

## Disposition

Drift is real but not urgent (no incorrect sign-offs resulted — the freeform format is a valid substitute that already satisfies the governance gate). Actionable, so filed as a follow-on backlog item (**BLG-GOV-319**) rather than fixed inline here — ST-07's scope is the freshness *check*, not a skill rewrite, and reconciling the skill to match ~5 months of accumulated freeform practice (or conversely, confirming the freeform practice as the intended path and deprecating/narrowing the skill's structured-table requirement) is a real design decision for whoever owns the skill, not a mechanical sync fix.

## Acceptance

- Reviewed by: Sprint Execution Engine (autonomous class, per BLG-GOV-19 — this is a documentation/process review with no observable UI behaviour)
- Date: 2026-09-09
