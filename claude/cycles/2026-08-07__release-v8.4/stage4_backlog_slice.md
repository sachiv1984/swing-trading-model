Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-07
Cycle: 2026-08-07__release-v8.4
Release: v8.4

# Backlog Slice — v8.4

<!-- release-plan-marker: RP:v8.4:2026-08-07__release-v8.4 -->

31 stories across 7 grouped EPICs. Full acceptance criteria below (source of truth for Sprint Planning and Execution).

---

## EPIC-01 — User-Facing Reporting Enhancement

**Maps to:** S2-01
**Owner:** Financial Reporting & Records Owner

### ST-01 — Add Avg P&L/Trade column to Monthly P&L Report table
**Source:** BLG-FE-141
**Effort:** XS
**Acceptance Criteria:**
- Column renders correctly for every row (including single-trade months and zero-trade edge cases, if any)
- No backend/contract change required or made
- Playwright coverage or staging sign-off for the new visible column, per CLAUDE.md's frontend-visible-change rule

### ST-31 — Trade-tag/trigger-source column on tax-year P&L CSV export
**Source:** BLG-FEAT-78
**Effort:** S
**Note:** Gate condition (`BLG-FE-116` ships) confirmed met — `BLG-FE-116` shipped v7.5, retired 2026-07-20. Self-caught stale-gate-field correction applied to `backlog.md` this cycle (see `run_manifest.md §STEP 2`). Numbered ST-31 (out of sequence) as a late addition found after the initial STEP 2 numbering pass — see `run_manifest.md` for the finding.
**Acceptance Criteria:**
- CSV export includes a trigger-source column
- Column populated correctly for both alert-triggered and manual trades

---

## EPIC-02 — API Contract & Spec Debt Closure

**Maps to:** S2-02
**Owner:** API Contracts & Documentation Owner; Data Model & Domain Schema Owner

### ST-02 — Fix openapi.yaml structural defect: ~23 endpoints nested inside `components:` instead of `paths:`
**Source:** BLG-SPEC-116
**Priority:** P1
**Effort:** M
**Acceptance Criteria:**
- `components:` contains only valid OpenAPI sub-keys (schemas, responses, parameters, examples, requestBodies, headers, securitySchemes, links, callbacks) — 0 path-shaped keys remain nested inside it
- `yaml.safe_load(open('docs/reference/openapi.yaml'))['paths']` returns a path count matching a raw-text scan of top-level `/...:` lines under the `paths:` section
- OpenAPI Drift Detection CI gate passes against the corrected file
- `BLG-OPS-133`'s endpoint list re-verified/corrected against the fixed file in the same PR
- API Contracts & Documentation Owner sign-off

### ST-03 — settings_endpoints.md GET /settings example missing created_at/updated_at
**Source:** BLG-SPEC-112
**Effort:** XS
**Acceptance Criteria:**
- Example includes both fields with representative ISO-8601 values

### ST-04 — position_endpoints.md GET /positions example missing 5 live fields
**Source:** BLG-SPEC-113
**Effort:** S
**Acceptance Criteria:**
- `GET /positions` example lists all 5 fields (`total_cost`, `sector`, `industry`, `exit_reason`, `stop_reason`) with descriptions
- Cross-checked against the actual `positions_list.append({...})` dict in `position_service.py`

### ST-05 — health_endpoints.md GET /health example missing external_apis/ai_journal
**Source:** BLG-SPEC-114
**Effort:** S
**Acceptance Criteria:**
- Example reflects the full live response shape, including both nested objects (`external_apis`, `ai_journal`)

### ST-06 — watchlist_endpoints.md GET /watchlist illustrative example is stale
**Source:** BLG-SPEC-115
**Effort:** S
**Acceptance Criteria:**
- Illustrative JSON example includes `company_name`, `tags`, `updated_at`, `added_at`, `days_on_watchlist`, `is_stale`
- `portfolio_id` (not actually returned) removed from the example
- Field table / version history left unchanged (already correct per the 2026-08-06 correction note on this item)

### ST-07 — OpenAPI security-scheme & auth-header documentation completeness check
**Source:** BLG-SPEC-106
**Effort:** S
**Acceptance Criteria:**
- Audit complete across all authenticated endpoints in `openapi.yaml` against actual backend auth enforcement
- Any documentation gap fixed
- API Contracts & Documentation Owner sign-off

### ST-08 — Backfill missing data_model.md sections for 4 undocumented tables
**Source:** BLG-SPEC-109
**Effort:** S
**Acceptance Criteria:**
- `data_model.md` section added for each of `backtest_trades`, `idempotency_keys`, `ai_journal_entries`, `gemini_audit_log` (columns, types, nullability, purpose, populating function), following the existing per-table format
- Data Model & Domain Schema Owner sign-off

### ST-09 — Formal schema-versioning doc for trade_plan/position tables
**Source:** BLG-SPEC-97
**Effort:** M
**Acceptance Criteria:**
- Schema-versioning doc created covering migration history and field deprecation for `trade_plan`/`position` tables
- Data Model Owner sign-off

---

## EPIC-03 — Backend Engineering Hardening

**Maps to:** S2-03
**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner; AI Compliance & Governance Officer

### ST-10 — Add functional index on trade_plans(UPPER(ticker))
**Source:** BLG-BE-82
**Effort:** S
**Acceptance Criteria:**
- `ensure_trade_plans_table()` creates a functional index on `UPPER(ticker)`
- `data_model.md` canonical `trade_plans` schema block matches the functional index actually created
- `EXPLAIN` on `get_trade_plans(ticker=...)` shows index usage (or equivalent CI-verifiable check)

### ST-11 — Add 429/backoff handling to Alpaca paper-sync close/positions endpoints
**Source:** BLG-BE-83
**Effort:** S
**Depends on:** BLG-BE-80 (`retry_with_backoff` pattern — already shipped v8.3)
**Acceptance Criteria:**
- Both `sync_close_paper_position` and `get_paper_positions` retry on transient/429 failure using the shared `retry_with_backoff` decorator
- Existing best-effort fallback behaviour (log and continue, never raise to caller) unchanged
- Regression test confirms retry attempts occur before fallback for both call sites

### ST-12 — Log AI model+version provenance on stored thesis/summary text
**Source:** BLG-BE-70
**Effort:** S
**Acceptance Criteria:**
- New model/version provenance field present and populated on all newly-created AI-generated records
- Existing records unaffected (no backfill required)

### ST-13 — Mutation/audit-trail log for trade plan edits post-entry
**Source:** BLG-BE-77
**Effort:** M
**Acceptance Criteria:**
- Audit-trail pattern established by `BLG-BE-73` (position edits) extended to trade plan mutations post-entry
- Data Model & Domain Schema Owner sign-off

### ST-14 — Auto-generated data dictionary from live schema
**Source:** BLG-BE-78
**Effort:** M
**Acceptance Criteria:**
- Script added generating a data dictionary directly from the live schema
- First run's diff against `data_model.md` triaged
- Data Model & Domain Schema Owner sign-off

---

## EPIC-04 — Frontend Code Health, Accessibility & Security

**Maps to:** S2-04
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner; Cybersecurity & Trust Lead

### ST-15 — Audit Dialog/DialogTitle className-override sites for the cn()-has-no-tailwind-merge defect class
**Source:** BLG-FE-142
**Priority:** P2
**Effort:** S
**Acceptance Criteria:**
- Every `Dialog*` consumer audited; genuine same-property override collisions listed
- Each genuine collision fixed (or, if the broader `tailwind-merge` fix is chosen instead, all affected sites verified correct under it)
- No visual regression in any fixed component (Playwright coverage or staging sign-off per CLAUDE.md's frontend-visible-change rule)

### ST-16 — Close remaining dark-only-token gaps in inline form-validation error text
**Source:** BLG-FE-140
**Effort:** S
**Acceptance Criteria:**
- All genuine form-validation-error instances of the bare `text-rose-400` token (across `StrategyBenchmark.js`, `AlertThresholdsSection.js`, `PreferenceRow.js`, `CustomPriceAlertsSection.js`, `ProspectiveHeatPanel.js`, `SavedFiltersControl.js`, and any other fresh full-repo grep hits) are closed to the canonical `text-rose-700 dark:text-rose-400` token
- No visual regression in dark mode (the existing `dark:text-rose-400` value is unchanged, only the light-mode pair is added)

### ST-17 — WatchlistModal.js fails ESLint (24 problems) — same patterns fixed in Watchlist.js
**Source:** BLG-FE-98
**Effort:** M
**Acceptance Criteria:**
- `npx eslint src/components/watchlist/WatchlistModal.js` exits 0 with zero warnings/errors
- No functional or visual behaviour change

### ST-18 — CSP allows 'unsafe-inline' for script-src and style-src
**Source:** BLG-SEC-12
**Effort:** M
**Acceptance Criteria:**
- CSP no longer includes a blanket `'unsafe-inline'` for `script-src`; `style-src` narrowed or justified explicitly if any exception remains
- No functional regression (app loads and renders correctly under the tightened CSP)

---

## EPIC-05 — Operational Reliability & Cost Monitoring

**Maps to:** S2-05
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect

### ST-19 — Staging verification required for SI-05 weekly digest fix
**Source:** BLG-OPS-132
**Priority:** P2
**Effort:** XS
**Depends on:** BLG-OPS-129 (shipped v8.3)
**Acceptance Criteria:**
- At least one successful SI-05 digest send observed post-fix, confirmed via `si05_digest_log` and a live Telegram message
- Outcome recorded against this item (and referenced from `docs/ops/si05_digest_delivery_root_cause_2026-08-05.md`)

### ST-20 — Endpoint coverage drift: 19 endpoints missing from api_performance_baseline.md
**Source:** BLG-OPS-133
**Effort:** S
**Depends on:** ST-02 (endpoint list must be re-verified against the corrected openapi.yaml first)
**Acceptance Criteria:**
- All 19 listed endpoints present in `api_performance_baseline.md` with p50/p95/max values
- Measurement conducted with ≥5 staging samples per endpoint

### ST-21 — Add POST /digest/si05/send to api_performance_baseline.md
**Source:** BLG-OPS-54
**Effort:** XS
**Acceptance Criteria:**
- `POST /digest/si05/send` present in `api_performance_baseline.md` with Render internal log-based measurements recorded
- Measurement methodology note added explaining why standard external HTTP timing does not apply

### ST-22 — CI runner cache warm-up for backend/.venv to cut pytest job time
**Source:** BLG-OPS-122
**Effort:** S
**Acceptance Criteria:**
- Cache step added (keyed on `requirements.txt` hash) for `backend/.venv` in the relevant GitHub Actions workflows
- Measured CI job time reduction
- Infrastructure & Operations Owner sign-off

### ST-23 — Database storage growth cost trend tracking (Postgres/Supabase)
**Source:** BLG-OPS-123
**Effort:** S
**Acceptance Criteria:**
- Simple storage-growth trend view (size over time) added alongside the existing cost-tag reporting
- FinOps & Resource Architect sign-off

### ST-24 — AI API cost model for Arc 4 journal intelligence features
**Source:** BLG-OPS-72
**Effort:** S
**Acceptance Criteria:**
- Cost model document (`docs/operations/arc4_ai_cost_model.md`) produced with estimated monthly AI API cost for Arc 4 features
- Cost controls identified and quantified
- Reviewed by FinOps & Resource Architect

---

## EPIC-06 — QA & Test Infrastructure Hardening

**Maps to:** S2-06
**Owner:** QA & Testing Owner; Director of Quality; Financial Reporting & Records Owner; Metrics Definitions & Analytics Owner

### ST-25 — Fix wrong patch target in test_get_portfolio_history_returns_ok
**Source:** BLG-QA-135
**Priority:** P2
**Effort:** XS
**Acceptance Criteria:**
- Test passes with no outbound network/DB connection attempt (verified by running with no DB reachable)
- Fix follows the file's own documented "Patch target rule" convention

### ST-26 — Backfill regression baseline with 24 undocumented Playwright spec files (v6.0-v7.3)
**Source:** BLG-QA-116
**Effort:** M
**Acceptance Criteria:**
- Part 2 table of `regression_test_suite_baseline.md` lists all spec files present in `tests/e2e/` at time of this item's execution
- Total spec files / Total scenarios counts match the table exactly
- Part 3 Arc coverage table references every newly-added file
- Director of Quality sign-off recorded

### ST-27 — Recurring CSV export content regression check
**Source:** BLG-QA-110
**Effort:** S
**Acceptance Criteria:**
- Lightweight recurring (e.g. quarterly) regression check added confirming CSV export content stays correct
- First instance run clean or findings filed

### ST-28 — Signal correctness fix impact measurement
**Source:** BLG-QA-70
**Effort:** S
**Acceptance Criteria:**
- Impact measurement query run against historical signals generated before the `BLG-BE-40` fix; count and magnitude of affected `suggested_shares` values identified
- Findings documented — informational, no remediation implied unless a material discrepancy is found
- Reviewed by Metrics Definitions & Analytics Owner and Product Owner

---

## EPIC-07 — Governance Process Integrity

**Maps to:** S2-07
**Owner:** Head of Specs Team; Head of Engineering

### ST-29 — Canonical, scripted gate-detection procedure for Release Planning's ungated-candidate scan
**Source:** BLG-GOV-286
**Priority:** P1
**Effort:** S
**Acceptance Criteria:**
- `release_planning_prompt.md` documents a specific, repeatable scan procedure (not prose guidance) for gate detection
- Procedure explicitly covers the `Provisional-Target`-embedded-gate-condition case that caused 2 of 3 recorded misses at v8.0/v8.1/v8.2
- Also covers the "missing `---` separator between adjacent backlog entries causes body-text bleed into the next item's gate scan" failure mode self-caught at `BLG-GOV-286`'s own scan this cycle (v8.4) — a 4th distinct failure mode, worth folding into the same fix
- Standard governance file edit checklist applied (version bump, `OPERATIONAL_GUIDE.md` §14 sync, `prompt_change_log.md` entry) per `CLAUDE.md` §6
- Head of Specs Team sign-off

### ST-30 — Dry-run the cross-EPIC merge conflict runbook
**Source:** BLG-GOV-212
**Effort:** S
**Acceptance Criteria:**
- One sprint executed with genuinely parallel EPIC branches
- Runbook (`CLAUDE.md` §8) followed
- Gaps found are filed as follow-ups
