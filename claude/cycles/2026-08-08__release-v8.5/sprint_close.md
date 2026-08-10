Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-08-10
Cycle: 2026-08-08__release-v8.5

---

# Sprint Close — 2026-08-08__release-v8.5

## Sprint Goal

> Clear the full ready frontend-correctness, design-consistency, and security-hardening slate across all 25 scoped stories.

**Outcome:** Met in full. All 6 EPICs (25 ST items) reached `merged` status. No items returned to backlog, no open escalations, no unresolved delegations.

---

## Items Done

### EPIC-01 — Production Correctness Fixes (PR #1326, merged)

| ST | Title | Class | Commit | Spec references |
|----|-------|-------|--------|-----------------|
| ST-01 | Fix `GET /analytics/tag-performance` 500 on staging (missing `trade_tags` column ensure) | autonomous | `075e7e238a` | `docs/specs/api_contracts/analytics_endpoints.md#GET /analytics/tag-performance` |
| ST-02 | Confirm `api-key-cross-environment-check.yml` is genuinely running, not silently skipping | autonomous (reclassified from `delegated_backend` at execution time) | `2b6a238ce1` | `docs/security/api_key_security_register.md#6. Application X-API-Key`; `.github/workflows/api-key-cross-environment-check.yml` |

### EPIC-02 — Security Hardening (PR #1329, merged)

| ST | Title | Class | Commit | Spec references |
|----|-------|-------|--------|-----------------|
| ST-03 | Security fix false-positive rate assessment (BLG-SEC-02) | autonomous | `ec528651a7` | `st03_sec02_false_positive_rate_assessment.md` |
| ST-04 | Recurring dependency vulnerability re-scan cadence (consolidated) | autonomous | `ec528651a7` | `.github/workflows/dependency-vuln-rescan.yml`; `scripts/check_dependency_vuln_rescan.py` |
| ST-05 | API key rotation runbook | autonomous | `ec528651a7` | `docs/ops/api_key_rotation_policy.md` |

### EPIC-03 — Frontend Correctness Fixes (PR #1327, merged)

| ST | Title | Class | Commit | Spec references |
|----|-------|-------|--------|-----------------|
| ST-06 | Register `muted`/`muted-foreground` (and other dead `-muted` classes) in `tailwind.config.js` | autonomous | `41619410c7` | `tailwind.config.js`; `tests/e2e/command-palette.spec.js` |
| ST-07 | Frontend wiring to populate `trade_plans.thesis_model_version`/`thesis_prompt_version` on save | autonomous | `1f68d07023` | `docs/specs/api_contracts/trade_plan_endpoints.md` |
| ST-08 | Reconcile Monthly P&L vs Tax Year table's exact-zero P&L colour convention | autonomous | `433009d8c2` | `docs/design/2026-08-08__release-v8.5/exact-zero-pnl-colour-convention/decision_record.md`; `docs/specs/frontend/pages/reports.md` |

### EPIC-04 — Design System & Contrast Consistency Audit (PR #1328, merged)

| ST | Title | Class | Commit | Spec references |
|----|-------|-------|--------|-----------------|
| ST-09 | Design token audit: v6.7 contrast fix consistency | autonomous | `5523c94ca4` | `st09_secondary_text_token_audit_findings.md` |
| ST-10 | Empty-state illustration/microcopy consistency pass | autonomous | `9ace6cddd3` | `docs/design/2026-08-08__release-v8.5/empty-state-microcopy-pattern/decision_record.md`; `docs/specs/frontend/design_system.md` |
| ST-11 | Confirm theme-toggle persistence across sessions | autonomous | `1a3839348f` | `spec_reference_not_applicable: true` — no prior canonical spec governs the theme-persistence mechanism itself; no new artefact created |
| ST-12 | Mobile responsive audit for PerformanceAnalytics page | autonomous | `81fa3186e5` | `docs/specs/frontend/pages/analytics.md` |
| ST-13 | Dark/light theme contrast audit follow-up | autonomous | `895d4517e6` | `st13_dark_light_contrast_audit_followup.md` |
| ST-14 | Ad hoc component inventory: candidates for shared design-system extraction | delegated_decision (Head of UX & Design, agent-mediated, 2 passes) | `19c06db9ff` | `st14_ad_hoc_component_inventory.md` |

### EPIC-05 — Frontend UX Review & Documentation (PR #1330, merged)

| ST | Title | Class | Commit | Spec references |
|----|-------|-------|--------|-----------------|
| ST-15 | Nav bar redesign exploration | delegated_decision (Head of UX & Design, agent-mediated, 1 pass) | `8ec6eb4672` | `st15_nav_bar_redesign_exploration.md` |
| ST-16 | User journey map: SI-05 Telegram digest to app action | delegated_decision (Head of UX & Design, agent-mediated, 2 passes) | `8ec6eb4672` | `docs/ux/si05_user_journey_map.md` |
| ST-17 | Reusable empty-state component spec for Base44 prompts | autonomous | `8ec6eb4672` | `docs/specs/frontend/base44_prompt_template_library.md#12` |
| ST-18 | Reports page information hierarchy review | delegated_decision (Head of UX & Design, agent-mediated, 1 pass) | `8ec6eb4672` | `st18_reports_page_information_hierarchy_review.md` |
| ST-19 | Rework ChartStyle to drop `style-src 'unsafe-inline'` dependency, if/when a consumer adopts `ChartContainer` | delegated_frontend (trigger condition unmet — zero live consumers, confirmed, no action needed) | `8ec6eb4672` | `st19_st20_chart_calendar_consumer_check.md` |
| ST-20 | Playwright/staging visual verification of `calendar.js` when a real consumer is added | autonomous (trigger condition unmet — remains dormant/watching) | `8ec6eb4672` | `st19_st20_chart_calendar_consumer_check.md` |

### EPIC-06 — Analytics & Governance Process Fixes (PR #1331, merged)

| ST | Title | Class | Commit | Spec references |
|----|-------|-------|--------|-----------------|
| ST-21 | Regime distribution metric over screener history | autonomous | `ad102c5074` | `docs/specs/api_contracts/screener_api_contract.md#GET /screener/regime-distribution` |
| ST-22 | Product Value Ratio historical trend chart | autonomous | `ad102c5074` | `claude/roadmap/product_value_ratio_history.md` |
| ST-23 | Release Planning does not reset root `sprint_sealed` to false on new-cycle publish | delegated_decision (Head of Specs Team, agent-mediated, 2 passes) | `ad102c5074` | `claude/system/release_planning_prompt.md#STEP 7` |
| ST-24 | `CLAUDE.md` §8 sibling-vs-sibling union clause for `execution_state.json` array fields | delegated_decision (Head of Specs Team, agent-mediated, 1 pass) | `ad102c5074` | `CLAUDE.md#8. Cross-EPIC Merge Conflict Resolution` |
| ST-25 | Fix unrestored `sys.modules` stubbing in `test_alerts_service.py` (cross-file test pollution) | autonomous | `ad102c5074` | `tests/test_alerts_service.py` |

**Note on EPIC-06 shared commit SHA:** ST-21 through ST-25 all committed to `ad102c5074e074103e15d791eff2c5a34eb4a9a8` as a single batch commit (`[EPIC-06][ST-21][ST-22][ST-23][ST-24][ST-25] Regime distribution metric, PVR history record, sprint_sealed reset fix, merge-conflict union clause, test isolation fix`), followed by 2 real-CI-fix follow-up commits recorded in ST-21's `notes` field (`f59c2cca`, `9170a0e3`).

---

## Items Returned to Backlog

None. All 25 ST items reached `merged` status this sprint.

---

## Items Delegated and Outstanding

None. `execution_state.json`'s `delegated_items` and `blocked_items` arrays are both empty for this cycle — `delegation_log.md` was never created because no item required the STEP 3.1.B park-and-wait delegation flow. The 8 `delegated_decision`/`delegated_frontend`-classified stories (ST-14, ST-15, ST-16, ST-18, ST-19, ST-23, ST-24) were all resolved in-session via agent-mediated sign-off per §5.3 before ever reaching the STEP 3.1.D escalation subroutine, so `execution_escalations.md` was also never created.

---

## QA Evidence Logs Produced

- `claude/cycles/2026-08-08__release-v8.5/qa_evidence_EPIC-01.md`
- `claude/cycles/2026-08-08__release-v8.5/qa_evidence_EPIC-02.md`
- `claude/cycles/2026-08-08__release-v8.5/qa_evidence_EPIC-03.md`
- `claude/cycles/2026-08-08__release-v8.5/qa_evidence_EPIC-04.md`
- `claude/cycles/2026-08-08__release-v8.5/qa_evidence_EPIC-05.md`
- `claude/cycles/2026-08-08__release-v8.5/qa_evidence_EPIC-06.md`

All six sign-off blocks carry a non-blank `Date: 2026-08-10` and `qa_signed_off: true` is set in `execution_state.json` for every EPIC.

---

## Process Notes

Rolled up from `execution_state.json.process_notes`:

1. **EPIC-01:** PR #1326 opened with all engine-side work + evidence complete, awaiting human QA sign-off + Product Owner acceptance per §5.3's always-human merge gate — not a blocker for other EPICs; engine proceeded to EPIC-03 (next in merge order) per STEP 4's "record unmet condition, don't halt" guidance.
2. **EPIC-03:** Agent-mediated DoQ review (independent subagent, 2 passes) caught 2 real blocking findings before PR open — ST-06's AC-02 claimed Pass with only 1 of ~9 real call-site families covered and no backlog item filed for the rest (hard-gate violation); ST-08's implementation silently carried the colour fix into a column (P&L %) the Design Gate decision explicitly excluded. Both remediated in-session before the PR opened.
3. **EPIC-04:** PR #1328's first real CI run found 2 genuine bugs in `tests/e2e/analytics-mobile-responsive.spec.js` itself (not in ST-12's actual fixes) — fixed across 2 follow-up commits; all 34 checks green on the 3rd CI run. User-directed agent-mediated DoQ+PO review also ran on all 3 open PRs at user request during the session (see PR comments on #1326/#1327/#1328).
4. **EPIC-04:** PR #1327 (EPIC-03) merging to main put PR #1328 into `CONFLICTING`/`DIRTY` — resolved per `CLAUDE.md` §8 by taking the branch's `execution_state.json` wholesale after confirming main's copy held no data absent from the branch.
5. **STEP 4 resume-sync (this session, 2026-08-10):** Session started with EPIC-06 (PR #1331) already `MERGED` on GitHub (confirmed via `gh pr view`) but `execution_state.json` still showed `status: done` / `pr_status: open` and `merge_gate.epics_pending: [EPIC-06]` — the pre-halt-persist step from EPIC-06's own merge had not yet run in a prior session. Synced to `status: merged` / `pr_status: merged`, `merge_gate.epics_merged += EPIC-06`, `epics_pending: []`, `all_merged: true`. Orphaned post-merge commit check (LL-v6.8-P3-01) run for all 6 EPIC branches vs `origin/main`: 0 orphaned commits found on any branch.

---

## Deviations Filed This Sprint

None. All six EPICs' QA evidence logs record `Known deviations filed: None`. (ST-08 resolves a deviation opened in a prior cycle, `DEV-REPORTS-ST01-02` — not a new filing this sprint.)

---

## Backlog Items Filed This Sprint (out-of-scope findings, §7 exception)

`BLG-SEC-18`, `BLG-SEC-28`, `BLG-FE-147`, `BLG-FE-148`, `BLG-FE-149`, `BLG-FE-150`, `BLG-FE-151`, `BLG-FE-152`, `BLG-SPEC-118` — all confirmed present in `claude/backlog/backlog.md`.

---

## Open Escalations

None.

---

## Net Outcome vs Sprint Goal

Sprint goal fully met: all 25 scoped stories across 6 EPICs reached `merged`. Two systemic, previously-unnoticed production bugs were found and fixed beyond the originally scoped ACs — a dark-mode CSS class never applied to `document.documentElement` (EPIC-03/ST-06, meant every Radix Dialog-based component app-wide was always in light-theme CSS scope) and a theme-toggle flash-on-load defect (EPIC-04/ST-11). No scope was added or removed; no items deferred.

---

## Verification Readiness Statement

| Field | Status |
|-------|--------|
| All spec references populated in execution_state.json | Yes |
| All P1–P3 deviations filed and backlog references updated | Yes |
| QA evidence logs complete and DoQ sign-off non-blank for all EPICs | Yes |
