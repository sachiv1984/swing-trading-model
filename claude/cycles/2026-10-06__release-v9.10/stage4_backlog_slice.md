Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-06
Cycle: 2026-10-06__release-v9.10
Release: v9.10

# Backlog Slice — v9.10

<!-- release-plan-marker: RP:v9.10:2026-10-06__release-v9.10 -->

21 stories across 4 EPICs, 27.90 estimated days. The acceptance criteria below are the source of truth for Sprint Planning and Execution. Scope is sized to the top of the confirmed ~24–28 day capacity band, per the explicit user instruction "use full capacity" (2026-10-06). Ready pool: 82 items / 61.80 days. Selection method (`release_planning_prompt.md` §1.4c): the 1 ready P1 item, then all 14 seatable P2 items (`BLG-TECH-21` deferred by its own dedicated-release constraint), then category-balanced round-robin oldest-first over P3/P4. The release is execution-heavy: 8 build-and-ship items carry 19.25d (69%), which answers rebalance `2026-10-06__scheduled`'s §7.1 sustained-failure pull-forward. EPIC-02 and EPIC-03 carry observable UI ACs, so `design_gate_required: true`.

**Where an item's own AC is stale or depends on another story, the AC below restates it.** Any change from the source backlog item is marked *(restated)* with the reason.

---

## EPIC-01 — Stop-Parameter Correctness & ATR Integrity

**Maps to:** S2-01, S2-02, S2-03, S2-04, S2-05
**Owner:** Head of Engineering; Strategy Rules & System Intent Owner (ruling); Backend Engineering Patterns Owner

### ST-01 — One source for §11 stop parameters across the on-load and nightly stop paths
**Source:** BLG-BE-138
**Priority:** P1
**Effort:** M (~3-5d; 4.0d midpoint, includes a ruling sub-step and a production data check)
**Delegation note:** AC 1 needs a read-only look at the **production** `settings` row. The governed environment's `DATABASE_URL` is staging, so this is expected to be Human-Delegation (Infrastructure & Operations Owner). See RISK-01.
**Sequencing:** The parameter-authority ruling (AC 2) is the first sub-step. ST-03, ST-06 and ST-07 depend on it.
**Acceptance Criteria:**
- Production `settings` multiplier and hold-day values recorded in the story's QA evidence, read-only
- Parameter-authority ruling recorded with Strategy Rules & System Intent Owner sign-off: (a) fixed, so Settings shows them read-only; (b) a sanctioned personal override recorded in §12 and honoured by every path; or (c) changeable only through a §12.3 change record. `strategy_rules.md` §12 is updated if (b) or (c) is chosen.
- One source of stop multipliers and grace length used by `analyze_positions`, `run_nightly_trailing_stop_update`, `grace_service`, `compliance_service`, `should_exit_position` and `alerts_service`
- Settings and Trade Entry fallbacks equal §11 (5, 2, 10, 14)
- Parity test: for identical inputs, `analyze_positions` and `run_nightly_trailing_stop_update` produce the same stop, and the test fails if either path is given a different parameter source
- Any open position whose stored stop has already diverged has a recorded Product Owner correction decision (the §7.3 never-loosen rule applies, so no silent rewrite)

### ST-02 — Remove silent ATR fallbacks and record ATR provenance
**Source:** BLG-BE-139
**Priority:** P2
**Effort:** M (~2-3d)
**Sequencing:** After ST-01 (same `position_service.py` paths).
**Acceptance Criteria:**
- New positions record `positions.atr_source` (`fetched` / `user` / `fallback`, nullable for history), and `GET /positions` returns it
- A missing ATR during recompute leaves the stored stop unchanged, flags the position, and does not create a stop-breach signal
- Tests cover both fallbacks (entry-time 2%-of-entry substitution and recompute-time stop-to-entry)
- `data_model.md`, `position_endpoints.md` and `docs/reference/openapi.yaml` document `atr_source` in the same commit (CLAUDE.md §2)

### ST-03 — Contract corrections: losing-stop formula, analyze side effects, settings-change effect
**Source:** BLG-SPEC-187
**Priority:** P2
**Effort:** S (~0.5d)
**Sequencing:** After ST-01's ruling (the settings-change text depends on it).
**Acceptance Criteria:**
- `position_endpoints.md` and the nightly job's docstring give the losing stop as `current price − 5×ATR` (§7.2); a reader can reproduce a displayed stop from the contract
- The `GET /positions/analyze` contract states its persistent side effects (it writes stops and timestamps, and the §7.3 ratchet makes that irreversible). It is no longer described as "safe to refresh".
- `settings_endpoints.md` states the effect of a multiplier change on open positions consistently with ST-01's ruling, and cross-references it
- No new endpoints

### ST-04 — Unit-test the live exit decision and grace-period behaviour
**Source:** BLG-QA-207
**Priority:** P2
**Effort:** S (~1d)
**Acceptance Criteria:**
- `backend/utils/calculations.py::should_exit_position` is called directly (not stubbed) by CI-run tests covering: grace boundary (day 9 vs day 10), price at/below/above stop, risk-off overriding both grace and stop, and the closed set of exit reasons
- Tests assert the entry write path persists an initial stop, and the grace-period path still stores the calculated stop
- A test asserts manual exit is accepted inside the grace period
- `docs/testing/strategy_rule_test_traceability_matrix.md` rows C6.3-01, C6.3-02, C6.3-03, C8-00, C8.1-01, C8.1-02, C8.2, C8.3, C5-02 and C7.1-02 are updated to reflect the new coverage

### ST-05 — Rule on strategy-version registry coverage and enforce it with a test
**Source:** BLG-BE-137
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Strategy Rules & System Intent Owner ruling recorded: register only behaviour/parameter-changing versions, or all versions
- `backend/strategy_version_registry.py`'s docstring, `data_model.md` DS-11 and `strategy_version_comparison_contract.md` Implementation Note 2 agree with the ruling
- A test fails if a qualifying `strategy_rules.md` Change Log row is added without a matching registry entry. It replaces the hard-coded `len == 5` in `tests/test_strategy_version_registry.py`.
- If ST-01's ruling bumps `strategy_rules.md` with a behavioural change, the registry is updated to match in the same commit

---

## EPIC-02 — Stop & Exit Transparency (build-and-ship)

**Maps to:** S2-06, S2-07, S2-08, S2-09, S2-10
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design; Product Owner

### ST-06 — Show ATR, active multiplier and recalculation source in the stop-loss cell
**Source:** BLG-FE-193
**Priority:** P2
**Effort:** M (~4-6d; 5.0d midpoint)
**Gate:** Met. `BLG-BE-135` shipped v9.9, and `atr`, active multiplier and `stop_calculated_at` are on `GET /positions`. *(restated: the source item's "do not begin until BLG-BE-135 ships" AC is satisfied and dropped.)*
**Sequencing:** After ST-01's ruling, so the displayed multiplier matches the single parameter source. May use ST-02's `atr_source` if it has landed. Not required.
**Acceptance Criteria:**
- The stop-loss cell or its tooltip (`src/pages/Positions.js`, `PositionCard.js`) shows the ATR value, the active multiplier (2× profitable / 5× losing, §7.2) and the calculation source, checkable against the §5/§7.2 formula without leaving the page (Playwright)
- `TrailingStopExplainerIcon.js` tooltip copy reflects the row's actual last-recalculation event (on-load timestamp or nightly-job timestamp) instead of the hard-coded "ATR is recalculated daily" claim (Playwright)
- `docs/specs/frontend/pages/positions.md` updated to describe the new cell content

### ST-07 — Trade Entry shows the stop and risk the system will actually store
**Source:** BLG-FE-197
**Priority:** P2
**Effort:** M (~2-3d)
**Sequencing:** After ST-01 (the fallback multiplier must come from ST-01's single source).
**Acceptance Criteria:**
- The risk shown at entry equals the risk implied by the stored initial stop (Playwright or recorded staging run)
- No input suggests it sets the stop unless it does (the Stop Price input is removed or relabelled as a note)
- The ATR field is no longer labelled "(Optional)" in a way that contradicts §4 (the backend fetches ATR when it is empty)
- `add_position` stop handling is pinned by a backend test

### ST-08 — Exit dialog pre-selects the exit reason the system already knows
**Source:** BLG-FE-198
**Priority:** P2
**Effort:** S (~1d)
**Acceptance Criteria:**
- A position with `risk_off_exit` true opens `ExitModal.js` with "Risk-Off Signal" selected; a position whose post-grace price is at or below its stop opens with "Stop Loss Hit" selected. A one-line reason for the pre-selection is shown, and the user can change it (Playwright).
- All other positions still default to "Manual Exit" (Playwright)

### ST-09 — Morning briefing card for §8 exit recommendations
**Source:** BLG-FE-199
**Priority:** P2
**Effort:** S (~1-1.5d; 1.25d midpoint)
**Sequencing:** After ST-08. Both detect "post-grace stop breach or risk-off", so they should share one predicate.
**Acceptance Criteria:**
- A morning-briefing card (`src/components/dashboard/home/morning/`) lists positions with a post-grace stop breach or `risk_off_exit`, each linking to the exit dialog. It renders for qualifying positions and is absent otherwise (Playwright).
- §13: display-only, no automated action. The card's wording passes the existing UI-copy boundary lint.

### ST-10 — Recent Trades badge shows a neutral glyph for a break-even trade
**Source:** BLG-FE-194
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- A zero-P&L (or missing-P&L) trade in `RecentTradesWidget.js` renders a neutral glyph (e.g. lucide `Minus`); winners and losers keep their `TrendingUp`/`TrendingDown` arrows, matching the neutral badge colour shipped in v9.9 `BLG-FE-192`
- `tests/e2e/recent-trades-zero-pnl-badge.spec.js` extended to assert the glyph, passing in CI

---

## EPIC-03 — Lifecycle & Gap-Risk Strategy Boundary

**Maps to:** S2-11, S2-12, S2-13, S2-14
**Owner:** Strategy Rules & System Intent Owner; Head of Specs Team; Head of Engineering; Head of UX & Design

### ST-11 — Reconcile the lifecycle-state registry with strategy_rules.md §9
**Source:** BLG-SPEC-185
**Priority:** P2
**Effort:** S (~1d)
**Acceptance Criteria:**
- Ruling recorded with Strategy Rules & System Intent Owner sign-off: is the lifecycle badge a §9 state machine, or a display overlay that defers to §9?
- `docs/specs/position_lifecycle_states_registry.md` and §9 no longer conflict. If the overlay becomes canonical, §9 is amended under §16's change-justification template.

### ST-12 — Positions lifecycle badge agrees with the §6 grace window, in calendar days
**Source:** BLG-FE-196
**Priority:** P2
**Effort:** S (~1-2d; 1.5d midpoint)
**Sequencing:** In-grace behaviour does not depend on ST-11. Post-grace badge semantics follow ST-11's ruling if it lands first.
**Acceptance Criteria:**
- An in-grace position outside ±0.5 ATR shows GRACE, not LOSING/PROFITABLE, with calendar days remaining (Playwright)
- No "trading days" wording for the grace period remains (GRACE tooltip, Grace Period Alert)
- The UNKNOWN tooltip distinguishes "missing ATR/plan" from "flat after grace", using the reason the backend returns

### ST-13 — Gap Risk Flag §13.3 ruling on UK-ticker earnings flags and day-0 timing
**Source:** BLG-GOV-365
**Priority:** P2
**Effort:** S (~0.5d ruling)
**Sequencing:** Before ST-14, which absorbs any resulting code change.
**Acceptance Criteria:**
- A dated Strategy Rules & System Intent Owner ruling on UK tickers and on day-0 timing is recorded as an addendum to `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md`
- The code, `strategy_rules.md` §13.3/§4.2.3 and the decision record agree on which markets and which day offsets the earnings trigger covers. Any `strategy_rules.md` wording change carries its Change Log row and the §15 grep.
- Tests in `tests/test_gap_risk.py` pin the ruled behaviour, covering a UK position and the day-0 case (may land in ST-14's commit)

### ST-14 — Gap risk flag: disposition the standalone weekend-hold trigger and align trigger-timing label/spec with code
**Source:** BLG-BE-136
**Priority:** P2
**Effort:** S (~1-2d; 1.5d midpoint)
**Acceptance Criteria:**
- No flag trigger in `gap_risk_service.py` fires identically for all open positions regardless of ticker or event (Binding Condition 6), or a signed alternative disposition is recorded in the §13 review record
- A position viewed on a Friday with earnings on the following Monday is flagged with reason `earnings`
- The reason label (`Positions.js`, `PositionCard.js`), `ux_spec.md` §5, `positions.md` §Gap Risk Badge and the code agree on trigger timing (Playwright for the label)
- `gap_risk_service.py`'s module docstring cites the §13 review record (Binding Condition 8)
- Unit and Playwright tests updated and passing. Contract and OpenAPI updated in the same commit if the `reasons` enum changes.
- Strategy Rules & System Intent Owner sign-off confirms Binding Conditions 1–8 still hold after the change

---

## EPIC-04 — AI Governance, Ops & QA Hygiene

**Maps to:** S2-15, S2-16, S2-17, S2-18, S2-19, S2-20, S2-21
**Owner:** AI Compliance & Governance Officer; Infrastructure & Operations Owner; QA & Testing Owner; Head of Specs Team

### ST-15 — AI chat advisory §13 quarterly self-audit checklist
**Source:** BLG-GOV-140
**Priority:** P2
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Checklist document produced and filed, covering advisory language, no-automated-action verification, disclaimer visibility and prompt-injection risk
- *(restated: the source AC's "first review 2026-09-24" date has passed.)* The first quarterly review is scheduled for a dated slot after this sprint closes. The checklist states the quarterly cadence.
- Product Owner and Strategy Rules & System Intent Owner sign-off

### ST-16 — AI model output logging completeness audit
**Source:** BLG-GOV-141
**Priority:** P2
**Effort:** S (~0.5d)
**Delegation note:** If confirming completeness needs a live `claude_audit_log` read, it is Human-Delegation (the governed environment has no production credential). A code-path audit is in scope regardless.
**Acceptance Criteria:**
- *(restated: the source AC's "before 2026-09-24" deadline has passed.)* The audit is completed in this sprint. Every `POST /ai/daily-briefing` and `POST /ai/chat` path is checked for logging of model_id, prompt_hash, response_length and timestamp.
- The silent-failure path found by the v9.9 usage review (`database.create_claude_audit_entry()` swallowing insert errors) is covered: fixed in this story or filed as a remediation item
- Logging completeness confirmed, or gaps filed as remediation backlog items
- AI Compliance & Governance Officer sign-off

### ST-17 — Quarterly dependency update review
**Source:** BLG-OPS-92
**Priority:** P2
**Effort:** S (~1d)
**Gate:** Met 2026-10-06. The quarterly cadence date has been reached and a new advisory signal surfaced (issue #1885 rescan).
**Acceptance Criteria:**
- Review covers all 17 `backend/requirements.txt` entries and all 38 direct `package.json` dependencies (25 runtime, 13 dev): current vs latest version, known CVEs/deprecations, recommended action
- The npm half reuses `docs/security/npm_audit_rescan_triage_2026-10-06.md` as input instead of repeating it. `react-scripts`-pinned findings are referred to `BLG-TECH-21`, not re-triaged.
- Review filed under `docs/security/`; any upgrade worth doing is either applied in this story (with CI green) or filed as its own backlog item

### ST-18 — Confirm the stale-staging-deploy alert fires on a real stale-staging condition
**Source:** BLG-OPS-171
**Priority:** P3
**Effort:** S (~0.5d; calibrated up one tier from XS for live-environment verification, ST-35 rule)
**Delegation note:** Needs live Render/GitHub Actions control. Expected Human-Delegation (Infrastructure & Operations Owner). See RISK-04.
**Acceptance Criteria:**
- A recorded failing CI run (run URL) showing the `STALE STAGING DEPLOY` message for a real, deliberately introduced staging/main divergence
- A recorded passing run (run URL) after staging is restored to the current `main` commit

### ST-19 — Add the Reports and Notifications pages to the axe accessibility scan
**Source:** BLG-QA-195
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- `tests/e2e/accessibility-axe-scan.spec.js` covers the Reports page (Monthly tab with a restated month expanded, Tax Year tab with the restated-months notice) and the Notifications preferences/history pages, in dark and light themes
- Any serious/critical finding is fixed or has its own filed item

### ST-20 — Correct the PO-05 pre-assessment and replay page spec wording
**Source:** BLG-SPEC-171
**Priority:** P3
**Effort:** S (~0.5d)
**Write-scope note:** The source AC routes the `current_roadmap.md` correction through the Roadmap Rebalance Engine. That is the `claude/roadmap/*` boundary under `ESC-CLOSE-20261006-01`. See RISK-03 and the Pre-sprint Planning Required Decisions.
**Acceptance Criteria:**
- The Strategy Rules & System Intent Owner acknowledges findings F1, F2 and F4 and decides the replay results-view caption wording
- No governed document other than sealed artefacts still says PO-05 reuses IT-06's Alpaca paper-trading mechanics. The `current_roadmap.md` correction is routed through the Roadmap Rebalance Engine (or as `ESC-CLOSE-20261006-01`'s ruling directs).
- The determinism guarantee and the engine-versus-live rule divergences are stated consistently across `po05_section13_preassessment.md`, the roadmap and `replay_mode.md`

### ST-21 — Sign-off single-point-of-failure matrix
**Source:** BLG-GOV-357
**Priority:** P3
**Effort:** S (~1-2d; 1.5d midpoint)
**Acceptance Criteria:**
- A published matrix (governance gate × authorised signer role(s)) covering roadmap, release planning, sprint planning, sprint execution, delivery verification and post-ship closure, filed under `docs/ops/` *(restated: the source AC also allows `claude/roadmap/`. `docs/ops/` keeps it clear of the `ESC-CLOSE-20261006-01` boundary.)*
- Gates with a sole authorised signer are explicitly flagged

---
