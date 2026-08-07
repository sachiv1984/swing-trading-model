**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-07
**Cycle:** 2026-08-07__release-v8.4

# Design Gate Record — 2026-08-07__release-v8.4

## Gate Status: PASSED

Completed: 2026-08-07
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | Add Avg P&L/Trade column to Monthly P&L Report table | Design Required | New data displayed (derived per-row column) on an existing table; genuine decision needed for the zero-trade-count edge case (avoid `£0.00`/`NaN`/`Infinity`) | `docs/design/2026-08-07__release-v8.4/avg-pnl-per-trade-column/decision_record.md` | `docs/specs/frontend/pages/reports.md` v0.14 | ✅ Cleared | Head of UX & Design |
| ST-31 | Trade-tag/trigger-source column on tax-year P&L CSV export | Design Pre-Approved | Backend export column addition; no in-app UI rendering — same basis as `BLG-FEAT-85` (v7.9 Monthly P&L CSV cost-basis reconciliation) | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-02 | Fix openapi.yaml structural defect: ~23 endpoints nested inside `components:` | Design Not Applicable | Structural YAML/documentation fix; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-03 | settings_endpoints.md GET /settings example missing created_at/updated_at | Design Not Applicable | Documentation-only; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-04 | position_endpoints.md GET /positions example missing 5 live fields | Design Not Applicable | Documentation-only; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-05 | health_endpoints.md GET /health example missing external_apis/ai_journal | Design Not Applicable | Documentation-only; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-06 | watchlist_endpoints.md GET /watchlist illustrative example is stale | Design Not Applicable | Documentation-only; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-07 | OpenAPI security-scheme & auth-header documentation completeness check | Design Not Applicable | Documentation audit; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 | Backfill missing data_model.md sections for 4 undocumented tables | Design Not Applicable | Documentation-only; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 | Formal schema-versioning doc for trade_plan/position tables | Design Not Applicable | Documentation-only; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | Add functional index on trade_plans(UPPER(ticker)) | Design Not Applicable | Backend/database index only; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 | Add 429/backoff handling to Alpaca paper-sync close/positions endpoints | Design Not Applicable | Backend resilience only, reuses existing `retry_with_backoff` pattern; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 | Log AI model+version provenance on stored thesis/summary text | Design Not Applicable | Backend metadata field on already-stored AI output; does not introduce or extend an AI-provider call (§13 pre-check not triggered — see Notes); no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 | Mutation/audit-trail log for trade plan edits post-entry | Design Not Applicable | Backend audit-trail extension of existing `BLG-BE-73` pattern; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-14 | Auto-generated data dictionary from live schema | Design Not Applicable | Backend/documentation tooling; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-15 | Audit Dialog/DialogTitle className-override sites for the cn()-has-no-tailwind-merge defect class | Design Pre-Approved | Applies the already-approved `!`-prefix important-modifier fix pattern (shipped v8.3, `ComplianceRecheckModal.js`/`ConfirmationModal.js`) to additional sites found by audit; explicit no-visual-regression AC; no new UX decision — same basis as v8.3 ST-11/ST-15 | N/A | `docs/specs/frontend/design_system.md` v1.7 (unchanged — Dialog styling already governed) | ✅ Cleared | Head of UX & Design |
| ST-16 | Close remaining dark-only-token gaps in inline form-validation error text | Design Pre-Approved | Applies the already-canonical `text-rose-700 dark:text-rose-400` token (established v1.7, v8.3, `BLG-SPEC-108`) to remaining instances; no new UX decision | N/A | `docs/specs/frontend/design_system.md` v1.7 (unchanged — §Interaction States → Error States already governs) | ✅ Cleared | Head of UX & Design |
| ST-17 | WatchlistModal.js fails ESLint (24 problems) | Design Not Applicable | Lint/code-health only; AC explicitly requires no functional or visual behaviour change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 | CSP allows 'unsafe-inline' for script-src and style-src | Design Not Applicable | Security header/config change; AC requires no functional regression, not a new UI decision | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 | Staging verification required for SI-05 weekly digest fix | Design Not Applicable | Ops verification task; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-20 | Endpoint coverage drift: 19 endpoints missing from api_performance_baseline.md | Design Not Applicable | Internal ops documentation; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 | Add POST /digest/si05/send to api_performance_baseline.md | Design Not Applicable | Internal ops documentation; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-22 | CI runner cache warm-up for backend/.venv | Design Not Applicable | CI/CD infrastructure only; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-23 | Database storage growth cost trend tracking (Postgres/Supabase) | Design Not Applicable | Internal ops/FinOps reporting alongside existing cost-tag reporting, no in-app UI — same basis as `BLG-OPS-120` (v7.9) | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-24 | AI API cost model for Arc 4 journal intelligence features | Design Not Applicable | Documentation/analysis deliverable; no UI change; does not itself introduce or extend an AI-provider call | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-25 | Fix wrong patch target in test_get_portfolio_history_returns_ok | Design Not Applicable | Test infrastructure fix; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-26 | Backfill regression baseline with 24 undocumented Playwright spec files | Design Not Applicable | Test documentation/inventory; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-27 | Recurring CSV export content regression check | Design Not Applicable | QA process/test infra; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-28 | Signal correctness fix impact measurement | Design Not Applicable | Data/analytics investigation, informational only; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-29 | Canonical, scripted gate-detection procedure for Release Planning's ungated-candidate scan | Design Not Applicable | Governance prompt amendment; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-30 | Dry-run the cross-EPIC merge conflict runbook | Design Not Applicable | Governance process exercise; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |

**Mandatory §13 boundary pre-check (AI-calling proposals):** two items touch AI-adjacent surface area this cycle — ST-12 (provenance field on already-stored AI-generated text) and ST-24 (AI cost-model documentation). Neither introduces or extends a call to an AI provider: ST-12 adds metadata capture to an existing, already-covered generation path; ST-24 is analysis/documentation of projected costs, not an implementation. No item requires a §13 pre-check flag this run.

## Blocked Items

None. All 31 items cleared on the initial run.

## Notes

- **Only genuinely new item this cycle: ST-01.** All other 30 items are either backend/infrastructure/documentation/governance with no UI change (28 items, Design Not Applicable) or apply an already-approved pattern verbatim with an explicit no-regression AC (ST-15, ST-16, ST-31 — Design Pre-Approved). This mix reflects the release's debt-clearance-weighted scope (see `release_plan.md` §Readiness).
- **ST-01 (Design Required):** the only substantive design decision was the zero-trade-count display treatment (`—` rather than a fabricated `£0.00`/`NaN`), since the column's arithmetic, formatting, and colour rule all follow directly from the existing `Realised P&L` column and the already-established Combined Total Line precedent for client-side derived display arithmetic. `reports.md` bumped 0.13 → 0.14.
- **ST-31 vs. ST-01 CSV interaction:** confirmed the two items don't collide — ST-01's new column is Monthly P&L Report (in-app table) only and explicitly excluded from that report's own CSV export; ST-31's trigger-source column is the separate Tax Year P&L CSV export. No shared surface, no combined design decision needed.
- **ST-15 / ST-16 (Design Pre-Approved):** both close out defect classes whose fix pattern was already established and shipped in `2026-08-05__release-v8.3` (`!`-prefix Dialog override fix; `text-rose-700 dark:text-rose-400` canonical error-text token respectively). Per-site audit-and-apply work with an explicit no-visual-regression AC; no new UX decision. Playwright coverage / staging sign-off for the observable no-regression claim remains a Sprint Planning / execution-phase evidence obligation per CLAUDE.md's frontend-visible-change rule, independent of this gate.
- **Root pointer note (process, not a gate blocker):** `.claude_current_state.json`'s `sprint_sealed` field currently reads `true`, carried over unmodified from `2026-08-05__release-v8.3`'s Sprint Planning seal — Release Planning's STEP 0 does not reset this root-level field when publishing a new cycle, and no other engine writes it except Sprint Planning itself. The authoritative source for this gate's own precondition is the **cycle-level** `claude/cycles/2026-08-07__release-v8.4/state.json`, per `design_gate_prompt.md` STEP -1's explicit wording ("`claude/cycles/<cycle_id>/state.json` with `sprint_sealed = false`") — that file carries no `sprint_sealed` key for this cycle (defaults false; this cycle's Sprint Planning has not run), and its `status` is `Published`, satisfying `lifecycle_schema.json`'s entry condition. This run treated the cycle-level file as authoritative and proceeded. Recommend Sprint Planning Engine STEP -1's bypass audit (or Release Planning's own STEP 0) be checked for whether it should explicitly reset root `sprint_sealed = false` on new-cycle publish, to remove this ambiguity for future cycles — filed as a follow-up (see Backlog reference below).

**Follow-up recommended, not filed here:** Release Planning STEP 0 (or an equivalent early step) should explicitly reset `.claude_current_state.json` `sprint_sealed = false` on publishing a new cycle's release plan, so the root pointer doesn't silently carry a stale `true` from the prior cycle's seal into the next cycle's Design Gate / Sprint Planning preconditions. This engine's §5 write-scope restriction prohibits modifying any backlog document during this routine, so the item is not filed here — flagging for the user/PMO Lead to file via `/backlog-add` (or `run ideas`) outside this run.
