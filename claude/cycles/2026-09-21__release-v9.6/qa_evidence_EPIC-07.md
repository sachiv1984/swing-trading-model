Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active — partial (2 of 6 stories still delegated/blocked)
Last Updated: 2026-09-23

---

# QA Evidence — EPIC-07: Governance Process Debt

**EPIC:** EPIC-07 — Governance Process Debt
**Cycle:** 2026-09-21__release-v9.6
**Sprint goal:** Ship the two build-and-ship product features committed at the 2026-09-19 rebalance — Clone-as-new-plan (`BLG-FEAT-96`) and CSV export for Screener and Watchlist (`BLG-FEAT-97`) — within the full 32-item, 7-EPIC v9.6 scope at the top of confirmed sprint capacity, landing the live-capital trailing-stop formula decision (`BLG-BE-119`) early so the nightly stop-update path can be hardened on a single agreed formula.
**Test scenarios used:** none — all 4 completed stories are governance-prompt/documentation edits; `scan_backlog_gate_conditions.py`'s new date-lapsed logic was exercised live (`python3 scripts/scan_backlog_gate_conditions.py --as-of 2026-09-23`, 12 items correctly flagged) rather than via a pytest file, since this script has no existing test file in `tests/`.

**Delegation class:** ST-27, ST-30, ST-31, ST-32 `autonomous` (all 4 complete, this evidence log covers these). ST-28, ST-29 `delegated_decision` — **not yet resolved**, tracked at `ESC-EXEC-20260921-06` and `ESC-EXEC-20260921-07` respectively (SLA due 2026-09-24T15:51:14Z, not yet breached), delegation log `DEL-20260921-05`/`DEL-20260921-06`. Both require a named human authority (Strategy Rules & System Intent Owner's §13 cadence decision; Product Owner's capacity-band hold/raise decision) the engine does not hold, and are correctly left `Pending`. **This PR does not represent EPIC-07 complete** — it carries the 4 autonomous stories now, on the understanding that ST-28/ST-29 commits land on this same branch once resolved, before merge. No file under `src/pages/**` or `src/components/**` was created or modified by this EPIC — entirely governance-prompt/spec/documentation.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-27 | `release_planning_prompt.md` §1.3a (v2.54); `scripts/scan_backlog_gate_conditions.py`; `backlog.md` | Scan now reports a separate "date-lapsed — verify" list; §1.3a requires it be read and each item cleared or re-gated before the ready pool is fixed | AC-01 (scan reports separately) — done. AC-02 (6 named items verified, cleared or re-gated) — done in full, see notes below. AC-03 (§6 checklist complete) — done | Pass | None |
| ST-30 | `roadmap_management_prompt.md` §5.5 (v1.6) | New mandatory, marker-tracked, every-3rd-invocation governance-prompt version-table audit cadence, wiring the existing `governance-drift` skill into a governed routine | AC-01 (cadence defined, wired in) — done. AC-02 (first mandatory-cadence run completed, results recorded) — done, this file | Pass | None |
| ST-31 | `ai_model_version_pinning_policy.md` §9 (v1.2) | Consolidated deprecation-monitoring procedure — folded into the existing BLG-GOV-63/74 quarterly review rather than a second standalone cadence | AC-01 (procedure defined) — done. AC-02 (integrated with BLG-GOV-74 cadence) — done. AC-03 (gate verified before sprint planning) — done, re-cited | Pass | None |
| ST-32 | `claude/cycles/sprint_velocity_trend_chart.md` | Sprint Velocity Trend Chart — delivered-story-count per cycle (full 81-cycle history) and U/G/D/P split (rolling-window PVR readings, the finest grain actually tracked) | AC-01 (chart shows delivered-story-count, all history) — done. AC-01 continued (U/G/D/P per cycle) — done at the actual data grain available, disclosed | Pass with notes | None (disclosed data-grain limitation) |

**QA test coverage:**
- Scenarios run: `scripts/scan_backlog_gate_conditions.py --as-of 2026-09-23` run directly (12 date-lapsed items found, matches expected — 6 named in `BLG-GOV-345` plus 6 more the extended scan newly surfaces); `scripts/openapi_3way_drift_sweep.py` ran automatically on each commit (pre-commit hook) — no drift, 145/146/146 unchanged.
- Regression areas checked: `governance-drift`-equivalent self-consistency check performed directly (ST-30's own first run) across all 23 §14-tracked files plus OPERATIONAL_GUIDE.md's own 3-way header/self-row/Change-Log-top-row consistency — 0 file-version mismatches, 1 self-row drift found and fixed in the same session.
- Known deviations: None found — all 4 completed stories' deviation checks completed with nothing to file.

**Notes for the Director of Quality and Product Owner:**

1. **ST-27 AC-02 was initially disclosed-partial, then completed same-session after an explicit write-scope ruling.** `sprint_backlog.md`'s own Outstanding Actions table pre-flagged the conflict: `execution_prompt.md` §7 does not permit the engine to edit existing `claude/backlog/backlog.md` items (new-item addition only). `ESC-EXEC-20260921-08` (Head of Specs Team + Product Owner ruling, agent-mediated §5.3, per explicit user direction to act as the relevant agents and complete the actions) granted a narrow, plan-authorised write exception — same class as `BLG-GOV-337`'s `workforce_capacity.md` precedent — scoped only to applying this determination's own already-published replacement text. The 4 items (`BLG-FEAT-59`/`60`/`63`/`BLG-FE-84` — `BLG-GOV-90`/`BLG-GOV-188` were already handled via ST-31/ST-32) now carry the re-gated text, anchored to the already-scheduled 2026-09-24 AI review, applied directly to `backlog.md`.
2. **ST-30's first audit run caught and fixed a real drift from the immediately-preceding ST-27 commit** — worth surfacing as a concrete demonstration the new cadence works, not just a theoretical addition. `OPERATIONAL_GUIDE.md`'s §14 self-row was left at the stale `4.201`/`2026-09-22` after the ST-27 commit despite that commit's own message claiming it was updated; found and corrected within the same session by ST-30's own first run, with a same-session correction note added to `prompt_change_log.md`'s ST-27 row rather than silently rewriting history.
3. **ST-30 also disclosed, but did not act on, 2 untracked Class-6-shaped template files** (`decisions_record_template.md`, `scope_document_template.md`) — both carry the same versioned header shape as `qa_evidence_template.md`, which *is* tracked in §14. Whether to add them is a scope judgement for Head of Specs Team, not a version-mismatch this audit auto-corrects.
4. **ST-32's chart cannot show a true per-single-cycle U/G/D/P split, because no source in this repo tracks one.** `product_value_ratio_history.md` records rolling-window readings (e.g. `v9.1-v9.5`) tied to roadmap rebalances, not individual release cycles. The chart reports these real rolling-window figures, clearly labelled, rather than fabricating a per-cycle number — flagged here in case Product Owner/PMO Lead want a true per-cycle breakdown built as a future story (would require retroactively tagging each shipped story by U/G/D/P, a materially larger undertaking than this story's own `S` effort estimate).

**Backlog items filed from this EPIC's findings:** None — all 4 completed stories' own scope was completed or transparently disclosed within their own AC; no out-of-scope finding surfaced beyond what's already noted above (the untracked-templates finding, note 3, is disclosed rather than filed since it is itself a byproduct of this EPIC's own governance-audit work, not an unrelated out-of-scope discovery).

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec — for the 4 completed stories (ST-27/30/31/32) only; ST-28/ST-29 remain outstanding, see Delegation class note above
- [x] No unresolved P0 or P1 deviations — none filed
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no frontend files touched by this EPIC
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-09-23
- Comments: ST-27/30/31/32 acceptance criteria verified against their canonical spec references (see table above); all governance-prompt/documentation edits, no test suite applicable beyond the scripts exercised directly. **This sign-off covers the 4 completed stories only — it is not an EPIC-07-complete sign-off.** ST-28 and ST-29 remain genuinely blocked on human/authority action (a Strategy Rules & System Intent Owner cadence decision; a Product Owner capacity-band decision) and must be resolved, committed to this same branch, and added to this evidence log before this EPIC's PR is eligible for the merge gate. Merge remains subject to the always-human QA sign-off and Product Owner acceptance regardless (`execution_prompt.md` §5.3 — this agent-mediated sign-off does not itself substitute for those).
