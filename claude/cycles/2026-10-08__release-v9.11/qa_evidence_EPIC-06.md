Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-09

# QA Evidence — EPIC-06

**EPIC:** EPIC-06
**Cycle:** 2026-10-08__release-v9.11
**Sprint goal:** see `sprint_goal.md`.

Per-story entries are added as stories close; the EPIC-level consolidation block and DoQ sign-off block are added at EPIC completion (`execution_prompt.md` §3.2.A).

---

## ST-34 — Give the effort-weighted PVR column its home in product_value_ratio_history.md

- **Spec references:** `claude/roadmap/product_value_ratio_history.md#History`; `docs/specs/metrics_definitions.md` Appendix F (PVR Measurement Package); `claude/system/roadmap_prompt.md#STEP 2.4 — Product Value Ratio Diagnostic (Mandatory)`
- **Acceptance criteria** (`stage4_backlog_slice.md#ST-34`):
  - AC1: `product_value_ratio_history.md`'s `## History` table carries the effort-weighted PVR alongside the story-count PVR, backfilled for the 5 windows computed in Appendix F — **Met**, commit `e8ca73b0` (named-file write, `execution_prompt.md` §7 case (a)). Backfill 0.457 / 0.115 / 0.109 / 0.021 / 0.093, reproduced by `scripts/compute_effort_weighted_pvr.py`.
  - AC2: `roadmap_prompt.md` STEP 2.4 appends both readings at future rebalances once `BLG-GOV-339`'s sign-off is recorded (CLAUDE.md §6 checklist applies) — **Met** in the ST-34 AC2 commit on this branch: STEP 2.4 "Effort-weighted reading" paragraph; `roadmap_prompt.md` v9.32, `OPERATIONAL_GUIDE.md` v4.232 (§6 phase header, §14 rows, Change Log), `prompt_change_log.md` rows, `roadmap_prompt_changelog.md` 9.32 row; history-file column note v1.2.
- **BLG-GOV-339 sign-offs (ESC-EXEC-20261008-03), dated 2026-10-09:**
  - Head of Specs Team — [Agent-mediated review — on behalf of Head of Specs Team, user-directed] 2026-10-09 — Approved (second pass, after a Blocked first pass). `roadmap_prompt.md` v9.32 STEP 2.4 gains an "Effort-weighted reading" paragraph that fills `product_value_ratio_history.md`'s `Effort-weighted Ratio` column at each rebalance, using the `metrics_definitions.md` Appendix F method; unweightable stories are excluded and coverage is recorded in `run_manifest.md`; `scripts/compute_effort_weighted_pvr.py` is used only when its hard-coded window already exists and is never edited during a rebalance (keeps the step inside §4 write scope). Diagnostic only, carries no tier; tier table, Product Value Alert and sustained-Advisory rule unchanged. Evidence: the method reproduces Appendix F's 5 readings exactly (0.457 / 0.115 / 0.109 / 0.021 / 0.093); on v9.6–v9.10 it gives 0.327 effort-weighted vs 0.161 story-count at 155/155 coverage, U/G/D/P 25/36/94/0 matching the recorded row. Any tiering on the effort-weighted figure is a separate threshold decision. CLAUDE.md §6 checklist complete.
  - Product Owner — [Agent-mediated review — on behalf of Product Owner, user-directed] 2026-10-09 — Approved (second pass, after a Blocked first pass). STEP 2.4 records an effort-weighted PVR reading next to the story-count reading at each rebalance; diagnostic only. Tiers, the Product Value Alert, the sustained-Advisory pull-forward and all Product Owner response obligations stay on the story-count `user_value_ratio`, even when the two readings fall in different bands. Worth recording because the readings diverge materially (v9.1–v9.5: 0.046 story-count vs 0.021 effort-weighted; v9.6–v9.10: 0.161 vs 0.327). Scope limit: this sign-off covers the effort-weighted reading only; BLG-GOV-339's D-split re-tagging and leading-indicator wiring still need their own sign-off.
  - First pass (both roles): Blocked on one shared finding — the draft told the roadmap engine to extend the script's hard-coded maps, a write to `scripts/` outside `roadmap_prompt.md` §4 write scope. Fixed with the Head of Specs Team's replacement paragraph, which also spells out the exclusion/coverage rule, three-decimal precision and "carries no tier". Product Owner N2/N3 applied in the `product_value_ratio_history.md` column note (Tier derived from story-count only; 2026-09-30/10-06/10-08 rows stay "—").
- **Follow-ups proposed (not yet filed, pending user confirmation of drafts):** script `--window` argument; Appendix F normalisation-table/script mismatch and stale Appendix F status lines (`metrics_definitions.md` is outside ST-34's authorised files).
- **Deviations:** none. Governance-only story; no runtime test applies.
- **QA findings / disposition:** _(Director of Quality — at EPIC-06 DoQ consolidation)_
