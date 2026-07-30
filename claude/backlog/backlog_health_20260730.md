**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-30

# Backlog Health Report — 2026-07-30

## Summary

Items archived: 23 (BLG-BE-68, BLG-BE-75, BLG-BE-76, BLG-BE-41, BLG-SEC-22, BLG-SEC-09, BLG-SEC-18, BLG-SEC-13, BLG-QA-127, BLG-QA-96, BLG-QA-133, BLG-QA-128, BLG-SPEC-102, BLG-SPEC-103, BLG-SPEC-104, BLG-GOV-243, BLG-FE-122, BLG-FE-123, BLG-FE-106, BLG-FE-134, BLG-GOV-256, BLG-GOV-216, BLG-GOV-207)
Ephemeral sections removed: 1 (Release Slice v7.10)
Orphans flagged: 0
Stale blockers flagged: 0
Promotion candidates: 0
New items added: 0

Gate Field Normalisation: 0 occurrences of `**Gate:**` in `backlog.md` — PASS
Effort Day-Range Validation: 1 pre-existing flag (`BLG-QA-115` — unchanged from prior cycles), 0 new
Governance Prompt Duplicate Cross-Check (new §1.3, first run this cycle): 27 open `BLG-GOV-*` items reference a prompt file also touched by `prompt_change_log.md` after their own filing date. Semantic spot-check of each entry's actual change description against the flagged items' stated problems found **0 genuine duplicates** this run — `roadmap_prompt.md`'s high revision cadence (patched almost every cycle) produces many superficial file-level matches with no topical overlap. No items closed or flagged as probable-duplicate candidates.
ID Uniqueness Scan: 367 `### BLG-` headings in `backlog.md`, 367 unique — PASS, 0 duplicates
Deferral Age Validation: no items found with 3+ consecutive deferrals and no PO re-deferral

## Promotion Candidates

None this run.

## Orphans

None.

## Blocked — Stale Blockers

None.

## Archived Items

| Item | Title | Cycle | Story |
|------|-------|-------|-------|
| BLG-BE-68 | Fix errors masked as HTTP 200 in portfolio_risk.py | 2026-07-28__release-v7.10 | ST-01 |
| BLG-BE-75 | Extend Alpaca backoff audit to Yahoo Finance, Gemini, Claude call sites | 2026-07-28__release-v7.10 | ST-02 |
| BLG-BE-76 | Idempotency key pattern for state-mutating POST endpoints | 2026-07-28__release-v7.10 | ST-03 |
| BLG-BE-41 | Deprecated table read-path audit | 2026-07-28__release-v7.10 | ST-04 |
| BLG-SEC-22 | Secrets-scanning pre-commit/CI gate (gitleaks/trufflehog) | 2026-07-28__release-v7.10 | ST-05 |
| BLG-SEC-09 | AI rate-limit bypass test | 2026-07-28__release-v7.10 | ST-06 |
| BLG-SEC-18 | Rate-limit audit on public-facing endpoints ahead of any future auth changes | 2026-07-28__release-v7.10 | ST-07 |
| BLG-SEC-13 | Raw exception text returned in API error responses | 2026-07-28__release-v7.10 | ST-08 |
| BLG-QA-127 | Serve production build for Playwright E2E webServer instead of CRA dev server | 2026-07-28__release-v7.10 | ST-09 |
| BLG-QA-96 | Red Flag Journal auth regression test | 2026-07-28__release-v7.10 | ST-10 |
| BLG-QA-133 | Endpoint test suite coverage audit against all backend/routers/ files | 2026-07-28__release-v7.10 | ST-11 |
| BLG-QA-128 | Consumer-driven contract check: frontend API calls vs documented contracts | 2026-07-28__release-v7.10 | ST-12 |
| BLG-SPEC-102 | position_endpoints.md envelope claim doesn't match live GET /positions behaviour | 2026-07-28__release-v7.10 | ST-13 |
| BLG-SPEC-103 | GET /positions undocumented lifecycle fields | 2026-07-28__release-v7.10 | ST-14 |
| BLG-SPEC-104 | trade_endpoints.md JSON example omits documented fields | 2026-07-28__release-v7.10 | ST-15 |
| BLG-GOV-243 | OpenAPI contract linter in CI for heading-level drift | 2026-07-28__release-v7.10 | ST-16 |
| BLG-FE-122 | Rewrite calendar.js against the react-day-picker v9+ API | 2026-07-28__release-v7.10 | ST-17 |
| BLG-FE-123 | SystemStatus.js categorizeEndpoint() missing branches | 2026-07-28__release-v7.10 | ST-18 |
| BLG-FE-106 | Consolidate StrategyBenchmark.js page header onto shared PageHeader component | 2026-07-28__release-v7.10 | ST-19 |
| BLG-FE-134 | Keyboard navigation & focus-order audit | 2026-07-28__release-v7.10 | ST-20 |
| BLG-GOV-256 | design_gate_prompt.md does not sync .claude_current_state.json root pointer on gate pass | 2026-07-28__release-v7.10 | ST-21 |
| BLG-GOV-216 | Recent-rebalance recency advisory at roadmap STEP -1 | 2026-07-28__release-v7.10 | ST-22 |
| BLG-GOV-207 | Same-day scheduled-rebalance cycle_id collision handling | 2026-07-28__release-v7.10 | ST-23 |

## Write Scope Verification

- All writes within Section 5 scope: Yes
- No content changes beyond status, location, and flags: Yes (item bodies copied verbatim to archive)
- No roadmap modifications: Yes
