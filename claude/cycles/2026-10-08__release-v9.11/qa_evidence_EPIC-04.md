Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-09

# QA Evidence — EPIC-04: AI Reliability, Cost and Usage

**EPIC:** EPIC-04 — AI monthly P&L narrative with its cost estimate, engagement metrics, usage counter and review tracking
**Cycle:** 2026-10-08__release-v9.11
**Sprint goal:** Make the post-trade debrief state R achieved and the stop at exit so it stops misreading correct trades, confirm every AI feature works after the v9.4–v9.10 import defect, and make the Risk Dashboard and Positions page show real prices, GBP entry values, true stop distance and calendar-day grace (BLG-BE-152, BLG-BE-150, BLG-BE-154, BLG-FE-206), while shipping the AI monthly P&L narrative and clearing v9.11's records, spec and governance hygiene items.
**Test scenarios used:** `tests/test_monthly_pnl_narrative.py`, `tests/test_monthly_pnl_narrative_db.py`, `tests/e2e/monthly-pnl-narrative.spec.js`. ST-23, ST-24, ST-27 and ST-28 are documentation and tracking stories, verified by document inspection and, for ST-28, by running `scripts/scan_backlog_gate_conditions.py`.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-23 | `docs/ops/ai_monthly_pnl_narrative_cost_estimate_2026-10-08.md` | Cost estimate for the narrative: about $0.0037 per generation on Haiku 4.5, under $0.10 a month expected (`4dd2f672`) | AC1: a cost estimate is produced before ST-25 is built. Met: committed 2026-10-08, before ST-25's first commit on 2026-10-09. | Pass with notes — the estimate's claim that the daily cost alert would catch runaway spend is wrong: that alert reads Gemini spend only. Corrected in ST-25's security checklist, which enforces a 40-call daily cap, and filed as `BLG-OPS-183` (the estimate gets a correction note there). | None (incidental finding: `BLG-OPS-183`) |
| ST-24 | `metrics_definitions.md` § AI Chat Engagement (v1.27.0) | Chat session (30-minute gap); sessions per week, questions per session, response acceptance rate (`ffa4a311`) | AC1: the metric set is defined and documented. Met. AC2: the gate is satisfied by the Product Owner removal on 2026-10-05; no action. | Pass with notes — the acceptance rate is defined but not yet instrumented; the rating control is filed as `BLG-FE-208`. The AC asked for definition, not instrumentation. | None (`BLG-FE-208` tracks instrumentation) |
| ST-25 | §13 record `decisions--2026-10-08__release-v9.11--ST-25-monthly-pnl-narrative-section13-review.md`; `ai_endpoint_security_checklist.md` and `decision_record.md` (`docs/design/2026-10-08__release-v9.11/monthly-pnl-ai-narrative/`); `reports.md` § AI Summary (v0.21); `reports_endpoints.md` § GET/§ POST /reports/monthly-pnl/narrative (v0.17); `data_model.md` DS-30; `ai_s13_boundary_test_suite.md` B-MPN-01..05 | Addendum steps 1–3 (`4dc83dd4`, `4ff6ebfc`, `8de19d0d`), then the build (`bf1a51f0`): the narrative service with output checks, regenerate-once and the code-written fallback; the fail-closed daily cap of 40; storage per tax year and input hash; `GET`/`POST /reports/monthly-pnl/narrative`; and an optional, dismissible "AI summary" card | AC1: the section renders on Monthly P&L as optional and dismissible (Playwright). Met: SC-MPN-01/02 (no POST until Generate, even when a stored summary is returned), SC-MPN-04/04b (Hide survives a reload, Show restores it, a throwing storage leaves the card visible). AC2: output framed advisory-only, consistent with SRB-v1.7, and the §13 confirmation cites every clause naming AI output or financial reporting. Met: AdvisoryBadge with the Condition 6 caption, `advisory: true`, and the determination citing §13.1–§13.5 (with §13.6 checked) and recording that no clause names financial reporting. | Pass | None |
| ST-26 | `metrics_definitions.md` § AI Monthly P&L Narrative Usage (v1.28.0); `data_model.md` DS-30 (v2.58) | `database.count_monthly_pnl_narrative_generations()`: counts generations, not model calls (one terminal audit row per completed request) (`259d0485`) | AC1: a real, queryable count is documented in `data_model.md`. Met. AC2: the 2027-01-03 review names this count as its evidence source. Met: `BLG-GOV-382` names "the monthly P&L narrative usage count (ST-26)", and the metric section defines that count and points back to `BLG-GOV-382`. | Pass with notes — AC2 is met through the metric definition, not by editing `BLG-GOV-382`. That item already names the count, and the AC does not give its ID, so `execution_prompt.md` §7 rule (b) does not authorise an edit. | None |
| ST-27 | `docs/product/ux/ai_chat_interaction_study_protocol.md` | AI chat interaction study protocol (`b387108c`) | AC1: the protocol has 5 study questions (Q1–Q5, §3), plus method, data and analysis sections. Met. AC2: gate satisfied (Product Owner 2026-10-05); no action. | Pass | None |
| ST-28 | `claude/backlog/backlog.md` `BLG-GOV-382`; `scripts/scan_backlog_gate_conditions.py` | Gated tracking item for the 2027-01-03 AI usage review (`ffa4a311`) | AC1: `scan_backlog_gate_conditions.py --as-of 2027-01-04` reports the item as lapsed, matching STEP 12.6's keyword filter. Met: re-run 2026-10-09, it reports `BLG-GOV-382 … [DATE-LAPSED 2027-01-03 — verify]`. AC2: the sequencing note (ST-24 before ST-25) is in the slice and in `sprint_backlog.md`. Met. | Pass | None |

**AI evidence — ST-25 (AI-Touching Story Evidence Addendum):**
1. **Prompt-template version:** `monthly_pnl_narrative_service.py` `PROMPT_VERSION = "v1.0"`. This is a new template; no existing template changed. The debrief template (`debrief_service.py`) is unchanged, and only its `scan_prescriptive` and `numeric_cross_check` are reused.
2. **Boundary-language sample:** this one is illustrative, because there is no live model access in this environment:

   > "In the 2025/26 tax year you closed 9 trades with realised P&L of £259.85 across 3 months. May 2025 was the highest month at £300.25, and June 2025 was the lowest, a loss of £120.40."

   The code-written fallback for the same figures was checked too. `scripts/run_ai_output_boundary_sample_audit.py`'s `scan_prescriptive` and `scan_prediction` were run against both on 2026-10-09: both `False` (clean). The service's own output checks (value, direction, prescriptive, forward-looking, tax and instrument-directive) also pass the sample; `tests/test_monthly_pnl_narrative.py` covers each check failing.

**Story-level authority sign-offs (BLG-GOV-14 consolidation).** All were agent-mediated per `execution_prompt.md` §5.3 at the user's direction, except the Product Owner's:

| Story | Authority | Record | Outcome |
|-------|-----------|--------|---------|
| ST-25 | Strategy Rules & System Intent Owner | §13 determination (ESC-EXEC-20261008-02 resolved) | Cleared 2026-10-09. CONDITIONAL, 12 conditions. First pass Blocked: the numeric check ignores sign, and the output checks had no test-coverage requirement. Second pass Approved. |
| ST-25 | Cybersecurity & Trust Lead | `ai_endpoint_security_checklist.md` | Cleared 2026-10-09. All three items PASS. First pass Blocked: the daily cost alert misses Claude spend, and the cap's failure behaviour was unspecified. Second pass Approved. |
| ST-25 | Head of UX & Design | `decision_record.md` | Cleared 2026-10-09. First pass Blocked: there is no `AdvisoryBadge` file, and the error text failed light-theme contrast. Second pass Approved. |
| ST-25 | Financial Reporting & Records Owner | `decision_record.md` | Cleared 2026-10-09. Approved on both passes. |
| ST-25 | Product Owner (human, in session) | `decision_record.md` §9 | Approved 2026-10-09, with a success measure for the 2027-01-03 review, an effort trade-off (ST-25 and ST-26 move to v9.12 whole if they cannot fit), and a fallback wording change. |
| ST-25 | Head of Specs Team | `reports.md` v0.21 lifecycle | Cleared 2026-10-09. First pass Blocked: the states table differed from the record. Second pass Approved. |

**Note for Head of UX & Design awareness:** the Product Owner changed the fallback note after the UX sign-off. It changed from "did not pass its accuracy checks" to "couldn't be checked against your figures". The wording is recorded in `decision_record.md` §9 and applied identically in `reports.md` and the code.

**QA test coverage:**
- **Scenarios run (locally, 2026-10-09):**
  - `tests/test_monthly_pnl_narrative.py` (78 tests: inputs; each output check passing and failing; regenerate-once; the fallback, including a case where both attempts fail; the daily cap and its fail-closed path; stored-text reuse and invalidation; routes, including the 429/503/404/400 responses and the rate limit; record exclusion; §13 boundary suite B-MPN-01..05; ST-26 usage-count rule).
  - `tests/test_monthly_pnl_narrative_db.py` (4 tests on a throwaway Postgres 18: the DS-30 storage round trip and CHECK constraint, and the ST-26 count and date window).
  - Full backend suite: 2280 passed.
  - Playwright: `tests/e2e/monthly-pnl-narrative.spec.js` (SC-MPN-01..09), plus every affected spec: all Monthly P&L and Reports specs, `accessibility-axe-scan.spec.js` and `system-status.spec.js` (SC-SS-01b updated to 127). 114 passed.
- **Real CI:**
  - Playwright on `bf1a51f0`: run 37945055540, success (ST-25 `ci_pending` cleared).
  - At branch head `12625445`: CI Pytest Suite 37946658710, Critical-Path Smoke Tests (Playwright) 37946658727, Endpoint Coverage Report, Service Layer Coverage Gate, Golden Output Regression Gate and Portfolio Integration Tests all succeeded.
  - The `quality_gate.yml` jobs (OpenAPI drift, API performance baseline, endpoint count) run on the PR. Locally, the OpenAPI drift checks, `check_api_performance_baseline_drift.py` and the endpoint-coverage audit all pass.
- **Shared-badge regression:** `tests/e2e/epic02-v62-ai-briefing-chat.spec.js` (the Dashboard briefing badge and the chat widget) passed 21 with 1 flaky. The flaky test, SC-AC-03 (chat submit), fails intermittently because the first-visit "Press ⌘K" hint toast covers the submit button.
  - Flaky-test disposition, step 2: it also fails 1 of 3 on EPIC-04 at `dde0501c`, before any ST-25 change, and neither branch touches `src/Layout.js`, so it is unrelated to this EPIC's diff.
  - CI passed it on every EPIC-04 run.
  - Not quarantined: it is not blocking, and the fix belongs in the spec. Tracked as `BLG-QA-219`.
- **Regression areas checked:**
  - the Monthly P&L view, including the table, CSV, restatement marker, fees notice and Unrealised card;
  - the Dashboard briefing's badge (`AiDisclaimer`'s default caption is unchanged);
  - the System Status endpoint count;
  - UI copy lint (one allow-list entry, with its justification);
  - the strategy version registry (`strategy_rules.md` v1.16, documentation-only).
- **Known deviations:** None found. All six stories' deviation checks completed with nothing to file.

**Frontend testing gate:** EPIC-04's observable ACs are all ST-25's, and each one has Playwright coverage that passed in real CI (run 37945055540 on `bf1a51f0`). No observable AC relies on code review alone.
- Card rendering, badge and caption: SC-MPN-01.
- Optional (no POST before Generate; a stored summary is shown without a POST): SC-MPN-01/02.
- Generate: SC-MPN-03.
- Dismissible: SC-MPN-04/04b.
- Year-change discard: SC-MPN-05.
- Fallback note: SC-MPN-06.
- Error and 429 messages: SC-MPN-07.
- Empty state: SC-MPN-08.
- Contrast, populated and in error, in both themes: SC-MPN-09 (axe).

There are no focus or interaction-timing ACs (the LL-v8.3-P3-02 sub-class). The same-EPIC testing-gap check found nothing: no story filed a testing-gap backlog item.

**Merge-gate preconditions specific to this EPIC:**
1. **AI Compliance & Governance Officer sign-off** before merge, for the new AI endpoint (`ai_s13_boundary_test_suite.md` "Requirements before shipping any new AI endpoint"). See the block below. D2 (no automatic action) is recorded in that block.
2. **EPIC-01 merges first.** The ST-25 security checklist's sequencing gate requires ST-06's `prompt_hash`/`response_length` columns to be on `main`. The code takes those fields automatically once `create_claude_audit_entry` accepts them. The merge order (EPIC-01 first, EPIC-04 fifth) already satisfies this.
3. **Re-derive at merge (CLAUDE.md §8):**
   - the SystemStatus fallback (127 here; EPIC-03 adds 1 more);
   - the `strategy_rules.md` (v1.16, after EPIC-03's v1.15), `reports.md` (v0.21, before EPIC-05's v0.22) and `data_model.md` (v2.58) header conflicts.

---

## AI Compliance & Governance Officer Sign-Off — New AI Endpoint

**Endpoint:** `POST /reports/monthly-pnl/narrative` (and its read-only `GET` sibling)
**Required by:** `docs/specs/qa/ai_s13_boundary_test_suite.md` (v1.1) — all 5 B-MPN scenarios documented; D1 and D3 CI-automated; D2 audit recorded in the QA evidence; AI Compliance Officer sign-off in the same cycle, before PR merge.

- D1 (advisory language in the system prompt): B-MPN-01, CI-automated — [AIC-D1]
- D2 (no automatic action): B-MPN-03, an AST check of the service's `database` imports. It finds only `get_portfolio`, `get_monthly_pnl_narrative`, `upsert_monthly_pnl_narrative`, `count_claude_audit_entries_today` and `create_claude_audit_entry`: no trade, position, plan, snapshot or settings write. Exports and snapshots are checked separately in `TestKeptOutOfTheRecord`. — [AIC-D2]
- D3 (`advisory: true`; the badge is rendered): B-MPN-02 and B-MPN-05, CI-automated; the badge is checked by Playwright SC-MPN-01 — [AIC-D3]
- D4 (no instrument directive): B-MPN-04, the `instrument_directive` output-scan category, CI-automated — [AIC-D4]
- Signed off by: [AIC-SIGNER]
- Date: [AIC-DATE]
- Comments: [AIC-COMMENTS]

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — `MonthlyNarrativeCard.js` builds its URLs from `base44.baseUrl` and `apiFetch`, the same import pattern as `Reports.js`'s `MonthlyPnlTable`.
- [x] **Strategy values checked (conditional — ST-36, BLG-GOV-370, v9.11):** N/A — no stop/grace/ATR/exit/sizing logic touched. ST-25's `strategy_rules.md` edit is a §13.5 roster row only (v1.16, documentation-only, registered in `DOCUMENTATION_ONLY_VERSIONS`).
- Signed off by: [DOQ-SIGNER]
- Date: [DOQ-DATE]
- Comments: [DOQ-COMMENTS]
