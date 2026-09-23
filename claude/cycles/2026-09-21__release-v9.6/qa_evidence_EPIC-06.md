Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active — partial (1 of 5 stories still blocked — ST-22, live-DB write access)
Last Updated: 2026-09-23 (ST-23 completed — see addendum below)

---

# QA Evidence — EPIC-06: Spec & Documentation Debt

**EPIC:** EPIC-06 — Spec & Documentation Debt
**Cycle:** 2026-09-21__release-v9.6
**Sprint goal:** Ship the two build-and-ship product features committed at the 2026-09-19 rebalance — Clone-as-new-plan (`BLG-FEAT-96`) and CSV export for Screener and Watchlist (`BLG-FEAT-97`) — within the full 32-item, 7-EPIC v9.6 scope at the top of confirmed sprint capacity, landing the live-capital trailing-stop formula decision (`BLG-BE-119`) early so the nightly stop-update path can be hardened on a single agreed formula.
**Test scenarios used:** none — all 4 completed stories are documentation-only (Class 1 spec edits / operational records), no runnable test file applies.

**Delegation class:** ST-24, ST-25, ST-26 `autonomous`; ST-23 `delegated_decision`, now resolved agent-mediated (all 4 complete, this evidence log covers these). ST-22 `delegated_decision` — **not yet resolved**, tracked at `ESC-EXEC-20260921-04` (SLA due 2026-09-24T15:51:14Z, not yet breached), delegation log `DEL-20260921-03`. Requires an authority the engine structurally does not and cannot hold — live write access to the *production* database (this sandbox's `DATABASE_URL` is a read-only *staging* credential, confirmed at v9.5's own live-schema check) — and is correctly left `Pending`; no attempt made here to fabricate or simulate completion. **This PR does not represent EPIC-06 complete** — it carries the 4 completed stories now, on the understanding that ST-22's commit lands on this same branch (per the delegation log's own commit-format note) once resolved, before merge. No file under `src/pages/**` or `src/components/**` was created or modified by this EPIC — entirely spec/documentation.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-23 | `docs/product/decisions/po05_section13_preassessment.md` | Full four-criterion §13 pre-assessment for PO-05 (Lightweight Replay Mode) — PASS, with 6 binding conditions carried forward for `BLG-FEAT-74`'s implementation | AC-01 (dated determination) — done. AC-02 (`BLG-FEAT-74`'s gate line reflects the outcome) — **partial**, see notes below | Pass with notes | None (disclosed limitation) |
| ST-24 | `design_system.md` §Canonical Chart Data Palette (v1.22) | New subsection documenting the Okabe-Ito (2008) 8-colour categorical, colour-blind-safe palette, with source/rationale, a usage rule (≤7 series, fall back to a second channel beyond), and a per-theme contrast note tying it to the existing v1.6 chart contrast checklist | AC-01 Palette documented with justification (recognised CVD-safe source) — done. AC-02 Cross-referenced from the design system spec — done, lives in that document itself | Pass | None |
| ST-25 | `docs/adr/decision_log.md`; `backend_engineering_patterns.md` §Architectural Decision Index (v1.7) | New lightweight, append-only Backend Decision Log with a reusable template, seeded with 2 real (not placeholder) decisions already implemented in this codebase: LOG-001 (`BLG-QA-73` test-stub AST-derivation) and LOG-002 (cross-router lazy-import pattern) | AC-01 File exists with template and ≥2 seeded real entries — done. AC-02 Referenced from a relevant onboarding/index document — done, `backend_engineering_patterns.md`'s own Architectural Decision Index now points to it | Pass | None |
| ST-26 | `metrics_definitions.md` §Lookback Window (CANONICAL) (v1.23.0) | New canonical Sharpe-ratio lookback window (trailing 252 trading days) with rationale, plus an explicit discrepancy note against each of the 3 real call sites found in the codebase (`analytics_service.py`, `production_strategy.py`, `PerformanceAnalytics.js`) | AC-01 Canonical window documented with rationale — done. AC-02 Discrepancy noted explicitly for each of the 3 current call sites — done, all 3 named with their specific divergence | Pass | None |

**QA test coverage:**
- Scenarios run: none applicable — all 3 stories are pure spec/documentation edits with no runnable test file and no code path change.
- Regression areas checked: `scripts/openapi_3way_drift_sweep.py` ran automatically on each commit (pre-commit hook) — no drift, 145 router endpoints / 146 contract headings / 146 `openapi.yaml` paths, unchanged by this EPIC (no endpoint touched).
- Known deviations: None found — all 3 completed stories' deviation checks completed with nothing to file.

**Notes for the Director of Quality and Product Owner:**

1. **ST-23 AC-02 is disclosed-partial, same constraint class as EPIC-07's ST-27.** The PASS determination itself is complete and actionable (`po05_section13_preassessment.md`). Applying it to `BLG-FEAT-74`'s own `Provisional-Target` gate line, and adding a new roster row to `strategy_rules.md` §13.5, both require edits `execution_prompt.md` §7 does not permit this engine to make directly (`backlog.md` beyond new-item addition; any `claude/strategy/` file at all). Exact replacement text for both is recorded in `decisions--2026-09-21__release-v9.6.md`'s ST-23 addendum for Head of Specs Team / Product Owner to apply.
2. **ST-25 found a pre-existing, out-of-scope duplication** while surveying decision-record conventions: `docs/decisions/ADR-002-frontend-only-r-multiple.md` and `docs/product/decisions/ADR-002-frontend-only-r-multiple.md` are byte-for-byte duplicates in two different directories. Not fixed here (outside this story's own file-editing scope, and not a "file already open for this story's own work" per the opportunistic in-file fix threshold) — surfacing for Head of Specs Team awareness; a backlog item was considered but not filed, since this is a documentation-hygiene observation rather than a defect with user-facing consequence.
3. **ST-26 surfaced two further Sharpe-formula discrepancies** beyond the lookback-window scope this story was chartered to fix (a missing "trade method" fallback branch in `analytics_service.py` despite the spec describing one at priority 2, and `PerformanceAnalytics.js`'s population-variance/per-trade-return divergence from the sample-variance spec). Both are documented inline in `metrics_definitions.md`'s new subsection as context for the discrepancy, but neither is filed as a separate backlog item in this story — they are pre-existing conditions the story's own read of the code surfaced, not new findings requiring their own AC; Metrics Definitions & Analytics Canonical Owner may want to file follow-on backlog items once ST-26's documentation is reviewed.

**Backlog items filed from this EPIC's findings:** None — see notes 1–2 above for why each candidate finding was disclosed inline instead.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec — for the 4 completed stories (ST-23/24/25/26) only; ST-22 remains outstanding, see Delegation class note above
- [x] No unresolved P0 or P1 deviations — none filed
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no frontend files touched by this EPIC
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-09-23
- Comments: ST-23/24/25/26 acceptance criteria verified against their canonical spec references (see table above); all documentation-only, no test suite applicable. **This sign-off covers the 4 completed stories only — it is not an EPIC-06-complete sign-off.** ST-22 remains genuinely blocked — it requires live *production* database write access, which is structurally unavailable in this environment (the sandbox `DATABASE_URL` is a read-only staging credential) and cannot be substituted by any agent-mediated review, unlike ST-23's determination which was a judgement call within the engine's competence to make. ST-22 must be resolved by someone holding production credentials, committed to this same branch, and added to this evidence log before this EPIC's PR is eligible for the merge gate. Merge remains subject to the always-human QA sign-off and Product Owner acceptance regardless (`execution_prompt.md` §5.3 — this agent-mediated sign-off does not itself substitute for those).
