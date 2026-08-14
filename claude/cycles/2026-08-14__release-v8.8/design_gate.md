**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-14
**Cycle:** 2026-08-14__release-v8.8

# Design Gate Record — 2026-08-14__release-v8.8

## Gate Status: PASSED

Completed: 2026-08-14
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | Add scheduled overnight screener refresh workflow | Design Not Applicable | Pure scheduled-job/CI coverage; run status surfaced only via `GET /health/scheduler` (API, not UI) | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-02 | Add scheduled nightly risk-off-alerts workflow | Design Pre-Approved | `RISK OFF` badge on Positions is already fully specified (colour, label, placement, stacking) — this item only fixes the nightly data refresh feeding `risk_off_exit`; no new UI, existing badge just becomes correctly populated | N/A | `docs/specs/frontend/pages/positions.md` v2.7 (§Alerts Column, locked reference) | ✅ Cleared | Head of UX & Design |
| ST-03 | Investigate nightly backtest import failure | Design Pre-Approved | "Benchmark data as of ..." line is already fully specified — this item only fixes the backend import job populating it; existing line, no new UI | N/A | `docs/specs/frontend/pages/strategy_benchmark.md` v0.5 (locked reference) | ✅ Cleared | Head of UX & Design |
| ST-04 | Add GET /v1beta1/news to api_performance_baseline.md | Design Not Applicable | Documentation-only baseline row; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-05 | Add GET /trade-plans/tags to api_performance_baseline.md | Design Not Applicable | Documentation-only baseline row; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-06 | Live timing measurement for GET /analytics/strategy-version-comparison | Design Not Applicable | Documentation-only baseline row update (measured vs. estimated values); no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-07 | Consolidate two divergent check_market_regime() implementations | Design Not Applicable | Backend refactor/consolidation; no UI change, no behavioural regression permitted by AC | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 | Position lifecycle state-transition history table | Design Not Applicable | Backend append-only table + migration; no UI, no lifecycle-logic behaviour change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 | Link price_alerts to the trade they trigger | Design Not Applicable | Backend data-model/provenance field; no UI acceptance criteria in this story | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | Populate si05_digest_log.telegram_message_id | Design Not Applicable | Backend field population only; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 | Add duration logging around POST /digest/si05/send | Design Not Applicable | Backend logging + baseline doc update; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 | Pre-Trade Research View query-latency budget review | Design Not Applicable | Backend performance review; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 | "What's New" panel surfaces user-facing benefit statements | Design Required | Content/data-source change to an existing card — new `User Impact` column replaces `Description` as the render source, with an empty-cell exclusion filter; no component/layout change | `docs/design/2026-08-14__release-v8.8/whats-new-user-benefit-copy/decision_record.md` | `docs/specs/frontend/pages/dashboard.md` v3.3 (§6A) | ✅ Cleared | Head of UX & Design |
| ST-14 | Research page trade plan status badge: fix raw snake_case | Design Required | Interaction/content-correctness fix touching a rendered badge; single-source-of-truth consolidation decision required (which of 3 divergent maps becomes canonical) | `docs/design/2026-08-14__release-v8.8/research-status-badge-single-source/decision_record.md` | `docs/specs/frontend/pages/research_view.md` v1.3 (§4.7) | ✅ Cleared | Head of UX & Design |
| ST-15 | Ticker Universe page filtering by search, sector, industry | Design Required | New interaction flow (3 new filter controls, a 200ms debounce timing parameter, and a reset control) — new component, new layout on an existing page | `docs/design/2026-08-14__release-v8.8/ticker-universe-search-sector-industry-filters/decision_record.md` | `docs/specs/frontend/pages/ticker_universe.md` v1.2 (§10) | ✅ Cleared | Head of UX & Design |
| ST-16 | Resolve PositionEntryModal.js dead-code status | Design Required | Explicit keep-or-kill UX decision required per the item's own AC; not eligible for Pre-Approved since no prior design covered "remove this component" | `docs/design/2026-08-14__release-v8.8/position-entry-modal-dead-code-removal/decision_record.md` | `docs/specs/frontend/design_system.md` v1.11 (§Modal / Dialog Theming — known-non-compliant list entry removed) | ✅ Cleared | Head of UX & Design |
| ST-17 | Add Playwright coverage for Card/secondary-variant components | Design Required | Observable-colour AC per `CLAUDE.md` §2; classification carried through even though the item's own scope is coverage-only, consistent with EPIC-03's blanket observable-UI framing in `stage4_backlog_slice.md`. First live call site for the `secondary` Badge variant is named by ST-15's decision (`Clear filters` control) — the shadcn `Card` component's own call-site gap (`BLG-FE-160`) remains open, unaffected by this cycle | `docs/design/2026-08-14__release-v8.8/ticker-universe-search-sector-industry-filters/decision_record.md` (§Card component call site) | `docs/specs/frontend/pages/ticker_universe.md` v1.2 (§10, `secondary` Badge call site documented); Card component call site remains open, no spec change | ✅ Cleared | Head of UX & Design |
| ST-18 | Field-population completeness audit for Arc 6 prerequisite fields | Design Not Applicable | Backend/data audit; report + sign-off only, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 | Consolidated backend service-layer test-coverage report | Design Not Applicable | Reporting/QA artefact; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-20 | Test-environment parity check | Design Not Applicable | Infra/config audit; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 | backend/routers/test.py completeness re-audit | Design Not Applicable | Backend test-coverage audit; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-22 | Add system/user role separation to Claude thesis-generation prompts | Design Not Applicable | Backend prompt-construction hardening; no UI. §13 boundary pre-check considered — see note below | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-23 | Dependency license compliance scan | Design Not Applicable | Backend/tooling scan; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-24 | Review baseline npm audit HIGH/CRITICAL findings | Design Not Applicable | Dependency/security audit; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-25 | Add Telegram Bot Token to api_key_rotation_policy.md scope | Design Not Applicable | Governance/security documentation only; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-26 | Backfill api_changelog.md entries for v7.9–v8.4 | Design Not Applicable | Documentation backfill only; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-27 | Correct trade_plan.md §5.1's stale field anchor | Design Not Applicable | Spec-document correction only; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-28 | Correct CLAUDE.md §8's commit message template | Design Not Applicable | Governance documentation correction only; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-29 | Assign an owning engine for prior_cycle field | Design Not Applicable | Governance/state-schema documentation only; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |

**Mandatory §13 boundary pre-check (AI-calling proposals):** one item touches an AI-adjacent surface this cycle — **ST-22** (adds `system`/`user` role separation to `generate_full_plan()`/`generate_setup_thesis()`, existing Claude API call sites). No `decisions--*--*-section13-review.md` or named pre-assessment was found covering these two functions specifically (searched `docs/product/decisions/`; the closest match, `decisions--2026-05-19__release-v3.8.md`, names "AI thesis" only as an EPIC-03 scope-inclusion rationale, not a §13 review of it). Applying the precedent set at v8.7 (ST-10, retry/backoff wrapper): ST-22 restructures *how* an already-existing, already-cleared prompt is transmitted (message role placement) without changing *what* content is sent or what capability is exercised — no new capability, no new content path, no new provider call. This is judged a non-functional hardening wrapper on an already-cleared call site, not an item that "introduces or extends a call to an AI provider" in the sense the pre-check targets. No covering §13 review required; no `§13 PRE-CHECK REQUIRED` flag raised.

## Blocked Items

None. All 29 items cleared on the initial run.

## Notes

- **Five genuinely new design decisions this cycle: ST-13, ST-14, ST-15, ST-16, ST-17 (all EPIC-03).** `stage4_backlog_slice.md` pre-flagged EPIC-03 as "Design Gate: Required — all 5 items below carry observable UI acceptance criteria," which this run confirms in full. Frontend specs updated same-run: `dashboard.md` 3.2→3.3, `research_view.md` 1.2→1.3, `ticker_universe.md` 1.1→1.2, `design_system.md` 1.10→1.11.
- **ST-15 and ST-17 share one decision record.** ST-15's filter-bar design deliberately gives the shadcn `Badge` `secondary` variant its first live call site (`BLG-FE-160`'s named gap) via its new "Clear filters" control, which is what makes ST-17's Playwright-coverage AC actionable this sprint for that half of its scope. The `Card` component's own call-site gap (`BLG-FE-160`) was considered and deliberately not manufactured here — ST-15's filter bar remains a plain row, consistent with the page's existing filter-bar convention — so that half of ST-17 remains correctly unresolved and open.
- **ST-16 resolved to removal, not restoration.** Repo-check at this gate reconfirmed zero live imports/mounts of `PositionEntryModal.js` (only a stale `Layout.js` comment reference). Product Owner elected Option B (remove) over building a new trigger/interaction flow from scratch, consistent with the item's XS effort budget — see decision record §2 for full rationale. Deletion of the source file and the `Layout.js` comment reference is implementation-time work (outside this gate's write scope, `design_gate_prompt.md` §5) — recorded in the decision record's §3 Scope for Sprint Execution to action.
- **ST-02/ST-03 (Design Pre-Approved):** both are backend data-correctness fixes feeding UI elements that are already fully specified and already shipped (`positions.md` RISK OFF badge, `strategy_benchmark.md` last-imported line) — no new UX decision, consistent with the Design Pre-Approved criterion's "frontend spec already updated in a prior cycle and confirmed unchanged" clause.
- **EPIC-01 (ST-04–ST-06), EPIC-02 (all), EPIC-04 (all), EPIC-06 (all), EPIC-07 (all), and EPIC-05 minus ST-22 classified Design Not Applicable.** 20 items total — backend correctness/hardening, test-coverage audits, dependency/security scans, and documentation-only corrections, none with a live UI change. Consistent with prior cycles' treatment of this item shape (v8.6 ST-11–ST-26, v8.7 ST-07–ST-17).
- **Motion/timing-sensitive clause (`design_gate_prompt.md` §6, `BLG-FE-131`):** ST-15's search-input debounce (200ms) is a new timing parameter on a new interaction flow — this is the reason ST-15 is classified Design Required rather than waved through as pure-code, and the decision record explicitly names the debounce value as an in-scope design decision rather than an incidental implementation detail.
