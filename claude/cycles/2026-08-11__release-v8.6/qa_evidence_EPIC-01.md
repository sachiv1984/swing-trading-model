Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-11

# QA Evidence — EPIC-01 (User-Facing Product Features)

**EPIC:** EPIC-01 — User-Facing Product Features
**Cycle:** 2026-08-11__release-v8.6
**Sprint goal:** Ship all 26 scoped v8.6 stories — trade-plan completion-rate tracking and an AI-assisted order-placement thesis digest, trade-plan-to-position linkage enforced with a DB-level integrity safeguard, the remaining shadcn design-token and secondary-text drift debt closed, and the financial-correctness, QA-coverage, and governance-debt carryover from v8.5 fully resolved.
**Test scenarios used:** `tests/test_trade_plan_completion_rate.py`, `tests/e2e/trade-plan-completion-rate.spec.js`, `tests/e2e/setup-thesis-digest.spec.js`

## Per-Story Evidence

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-01 | `docs/specs/frontend/pages/analytics.md#21` | `GET /analytics/trade-plan-completion-rate` (new `database.get_trade_plan_completion_rate()` + router endpoint) and a new `TradePlanCompletionRateSection` on Performance Analytics — 3 summary cards (Plans Created, Completion Rate with green≥60%/amber40-59%/red<40% threshold, Plans Abandoned + %) and a "{completed} of {created} plans completed" summary line. Empty state ("No trade plans created yet.") when `plans_created === 0`, not a misleading 0%. | AC-01: completion rate (plans_created/plans_completed/plans_abandoned/completion_rate) computable and displayable. AC-02 (optional): segmented by setup quality score tier. | Pass (AC-02 intentionally not implemented — optional per AC and per decision_record.md §2's own "omitted entirely when [tier data] doesn't [exist]" rule; backend does not return tier-segmented data, so the frontend correctly omits the table rather than rendering an empty stub) | None |
| ST-02 | `docs/specs/frontend/pages/trade_plan.md#10.5` | `SetupThesisDigestPanel` in `TradeEntry.js` — collapsible panel rendered below the "Linked to trade plan" indicator, showing the linked plan's `setup_thesis` (truncated to 3 sentences) and up to 4 "Key Risk Factors" bullets (2 from `early_exit_conditions`, 2 from `confirmation_criteria`), plus a "View full plan →" link. No new AI call — fetches the already-generated plan record via the existing `GET /trade-plans/{id}` endpoint (new `api.tradePlans.getById()` client method). Panel renders only when `trade_plan_id` is present and the plan has non-empty `setup_thesis` and/or `early_exit_conditions`. | AC-01: digest (setup thesis + key risk factors) renders at order-placement using the existing Claude thesis generation service (v4.0 infra) — i.e. surfaces already-generated content, no fresh inference call. | Pass with notes — "AI draft" badge (ux_spec.md §2) omitted; see Deviations column. | DEV-v8.6-ST02-01 (P3) — `isAiDraft` is ephemeral client-only state in `TradePlan.js`, never persisted to `trade_plans`; no server field exists to read it back from at order-placement time. Filed in `trade_plan.md` Known Deviations. Follow-up: `BLG-BE-95` (persist `is_ai_draft` column). |

**QA test coverage:**
- Scenarios run: 5 backend unit tests (`tests/test_trade_plan_completion_rate.py`) executed and passing against a mocked `get_db()` connection — confirmed via `backend/.venv/bin/python3 -m pytest`. Playwright scenarios SC-TPCR-01–07 (`tests/e2e/trade-plan-completion-rate.spec.js`) and SC-TSD-01–06 (`tests/e2e/setup-thesis-digest.spec.js`) authored against this codebase's established mocking patterns (`arc5-compliance-section.spec.js`, `v7.2-dashboard-tradeplan-ux-hardening.spec.js`) — **not locally executed**: this sandbox's OS (`ubuntu26.04-x64`) is unsupported by the installed Playwright version and Chromium could not be installed (`npx playwright install` fails with "Playwright does not support chromium on ubuntu26.04-x64"). Real GitHub Actions CI (`quality_gate.yml`) will run these on the PR — per the environment-parity sub-clause (LL-v8.3-P3-02), this is disclosed rather than treated as "coverage exists" for any interaction-timing-class AC (none of ST-01/ST-02's ACs fall in that sub-class — all are static rendering/content assertions, not focus/keyboard-trap/timing).
- Regression areas checked: `PerformanceAnalytics.js` (existing §13–§19 sections unaffected — new §21 section appended after the last existing rendered section, Arc5ComplianceSection); `TradeEntry.js` (existing form validity, cost preview, manual-link selector §10.3, and submit flow — `trade_plan_id` capture — unaffected; new `useQuery` for the linked plan is additive and only fires when `linkedPlanId` is set).
- Known deviations filed: DEV-v8.6-ST02-01 (P3, `trade_plan.md` Known Deviations, backlog ref `BLG-BE-95`)

**Frontend testing gate (LL-v3.1-EX-01) — per observable AC:**
- ST-01: card values/colours (Playwright, SC-TPCR-02/07), loading skeleton (SC-TPCR-03), empty state (SC-TPCR-04), error state (SC-TPCR-05), summary line (SC-TPCR-06) — all covered by `tests/e2e/trade-plan-completion-rate.spec.js`.
- ST-02: panel heading/thesis/risk-factor rendering (SC-TSD-01–03), hidden-when-absent (SC-TSD-04), view-full-plan link (SC-TSD-05), collapse/expand (SC-TSD-06) — all covered by `tests/e2e/setup-thesis-digest.spec.js`.
- No AC in this EPIC is left as "code review only" — every observable AC has an authored Playwright scenario. (Local execution not possible in this sandbox per the note above; CI will confirm on the PR.)

**Autonomous DoQ sign-off class (BLG-GOV-19) — NOT applicable:**
- Criterion 1 (all stories `autonomous`): ✓ met.
- Criterion 2 (all AC code-review-verifiable, no observable UI): ✗ **unmet** — both stories introduce observable UI (cards, colours, panel, collapse behaviour).
- Criterion 3 (no frontend-visible change): ✗ **unmet** — `src/components/analytics/TradePlanCompletionRateSection.js`, `src/components/trades/SetupThesisDigestPanel.js`, and modifications to `src/pages/PerformanceAnalytics.js`/`src/pages/TradeEntry.js` all fall under `src/components/**`/`src/pages/**` (BLG-GOV-135 detection rule).
- The autonomous class path is unavailable. Standard sign-off block used below.

---

## Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations (DEV-v8.6-ST02-01 is P3)
- [x] Regression areas checked
- [x] No frontend component in this EPIC constructs URLs directly outside the `api.*` wrapper (`api.analytics.tradePlanCompletionRate()`, `api.tradePlans.getById()` both added to `base44Client.js`; the "View full plan →" link uses the existing `react-router-dom` `Link`/`createPageUrl` convention, not a raw API URL)
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-08-11
- Comments: Agent-mediated review per user direction (2026-08-11). Findings: (1) no router-level integration test for `GET /analytics/trade-plan-completion-rate` — DB-layer coverage (5 tests) is solid but the endpoint's own 404/`ensure_trade_plans_table()` call path is untested at that layer; consistent with existing precedent (`test_trade_plan_tags.py` doesn't router-test `/tag-performance` either) so not a blocker, noted for future tightening. (2) `abandonedPct` is computed client-side from two already-fetched integers (`plans_abandoned`/`plans_created`) — a simple derived percentage, not a re-derivation of a value the backend is supposed to own (distinct from the analytics.md §15/§16 "no client-side R-multiple" rule); acceptable. (3) Playwright suites (13 scenarios total) could not be executed in this sandbox (no installable Chromium) — authored against proven patterns, disclosed as pending real-CI confirmation rather than claimed as verified. No P0/P1 issues found. **This is an agent-mediated sign-off, not a human Director of Quality's — see PR comment for full findings; final human QA sign-off and Product Owner acceptance are still required before merge (CLAUDE.md §2, execution_prompt.md §5.3 "Always-human gates").**

---

## Real CI Confirmation (post-PR)

The sandbox-unexecuted-Playwright disclosure above proved warranted: real GitHub Actions CI (`quality_gate.yml`, PR #1358) found 3 failing scenarios on first run — `SC-TPCR-02`, `SC-TPCR-04`, `SC-TSD-06`. All three were **test-locator bugs, not product bugs**: `page.getByText('Completion Rate')`/`'Setup Thesis'`/`'Plans Created'` used non-exact (substring) matching, which collided with pre-existing page text ("Journal Completion Rate", "Setup Thesis Digest" heading) or, for the empty-state negative assertion, with the empty-state copy itself ("No trade plans created yet." contains "plans created" as a case-insensitive substring). Fixed by adding `{ exact: true }` to the 6 affected locators — no component code changed. Re-pushed; awaiting CI re-run confirmation.

---

## Product Owner Disposition — DEV-v8.6-ST02-01

**Requested by:** user, in-session, 2026-08-11 — "act as `product_owner.md` and decide on the P3."
**Rendered by:** Sprint Execution Engine (agent-mediated, Product Owner role — §5.3). Per CLAUDE.md §2, this is recorded as agent-mediated, not a literal `Product Owner:` sign-off, regardless of the direct instruction to decide — that label is reserved for genuine human sign-off.

**Decision: Accept — ship ST-02 as-is.**

**Reasoning (per `product_owner.md` §6/§8.2/§8.3):**
- ST-02's actual backlog AC — "digest renders at order placement using the existing Claude thesis generation service" — is fully met. The "AI draft" badge is a design-spec (`ux_spec.md` §2) visual cue, one level below the committed AC, not an AC failure.
- Root cause (`isAiDraft` never persisted anywhere in the system) pre-dates this story; a proper fix is a schema change correctly scoped out to `BLG-BE-95`, not this order-placement UI story.
- Shipping impact of the gap: cosmetic only — the digest's actual content (thesis, risk factors, link) is identical with or without the badge. No misleading, blocked, or incorrect financial information results.
- Trade-off made explicit: holding EPIC-01 for a `trade_plans` schema migration to add one visual badge is a worse outcome than shipping the working feature now with the gap tracked (P3, `DEV-v8.6-ST02-01`, `BLG-BE-95`).

This disposition does not itself satisfy the STEP 4 merge gate's "Product Owner acceptance" row (always-human, CLAUDE.md §2) — final human confirmation is still the trigger to merge.
