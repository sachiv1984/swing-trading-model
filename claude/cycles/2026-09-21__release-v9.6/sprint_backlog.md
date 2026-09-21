**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-09-21
**Cycle:** 2026-09-21__release-v9.6
**Release:** v9.6
**Sprint Goal:** Ship the two build-and-ship product features committed at the 2026-09-19 rebalance — Clone-as-new-plan (BLG-FEAT-96) and CSV export for Screener and Watchlist (BLG-FEAT-97) — within the full 32-item, 7-EPIC v9.6 scope at the top of confirmed sprint capacity, landing the live-capital trailing-stop formula decision (BLG-BE-119) early so the nightly stop-update path can be hardened on a single agreed formula. See `sprint_goal.md`.
**Backlog Slice Source:** Original — `stage4_backlog_slice.md`, read together with `stage4_backlog_slice_addendum.md` (design-gate corrections to ST-01–ST-06 and ST-08; additive, no scope/priority/effort change).

# Sprint Backlog — 2026-09-21__release-v9.6

## Sprint Scope

**Merge order:** EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04 → EPIC-05 → EPIC-06 → EPIC-07 (rationale: `sprint_planning_notes.md ## Execution Sequence` — release-plan order; EPIC-01 owns the API-contract files and seats the pull-forward features; EPIC-02 lands its `data_model.md` entry before EPIC-06's ST-22 touches the same file; EPIC-07 lands last because it bumps governed prompts and `OPERATIONAL_GUIDE.md` and must rebase onto everything else). **`execution_state.json` owner:** EPIC-01.

**Shared files across EPICs** (canonical owner first; later EPICs rebase onto `main` after the earlier EPIC merges, before finalising their edits): `docs/reference/openapi.yaml`, `docs/reference/api_changelog.md` and `docs/specs/api_contracts/*` — EPIC-01 (ST-04) → EPIC-02 (ST-07/ST-08) → EPIC-03 (ST-10); `backend/routers/test.py` with the `SystemStatus.js` fallback count and `SC-SS-01b` — EPIC-01 → EPIC-02 (only if a new route is added); `data_model.md` — EPIC-02 (ST-08) → EPIC-06 (ST-22); `design_system.md` — EPIC-01 (bumped to v1.21 at the design gate) → EPIC-06 (ST-24); `.github/workflows/*` — EPIC-04 (ST-14/ST-16/ST-17) → EPIC-05 (ST-20); `claude/backlog/backlog.md` — EPIC-06 (ST-23) → EPIC-07 (ST-27) (both flagged in Outstanding Actions). Within-EPIC: `TradePlans.js` (ST-01 → ST-02 → ST-06); the nightly stop-update path (ST-09 → ST-13); governed prompts and `OPERATIONAL_GUIDE.md` (ST-27 → ST-30).

---

### EPIC-01 — Product Features & Frontend Build-and-Ship

**Maps to:** S2-01
**Owner:** Head of Engineering; Head of UX & Design; Product Owner; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 6.75 days
**Risk IDs:** RISK-01, RISK-08 (release-level)
**Execution sequence:** 1

#### ST-01 — 'Clone as new plan' action on the Trade Plans list

**Source:** BLG-FEAT-96
**Owner:** Head of Engineering; Head of UX & Design
**Estimated effort:** S (~0.5–1d)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01` (read with `stage4_backlog_slice_addendum.md#ST-01`)

**Dependencies:** None — first on `TradePlans.js`; must land before ST-02 and ST-06

**Notes:** Read AC 2 as status `draft`, not `planned` (addendum ST-01; `planned` does not exist). Design record `docs/design/2026-09-21__release-v9.6/trade-plan-clone/decision_record.md`; spec `trade_plan.md` v1.15. Playwright coverage of the observable AC required (CLAUDE.md §2).

**Staging-only ACs:** None.

---

#### ST-02 — Flag stale 'planned' trade plans on the Trade Plans list

**Source:** BLG-FE-180
**Owner:** Head of Engineering; Head of UX & Design
**Estimated effort:** S (~0.5–1d)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02` (read with `stage4_backlog_slice_addendum.md#ST-02`)

**Dependencies:** ST-01 (shared file `TradePlans.js`)

**Notes:** Addendum ST-02: marker applies to the four pre-entry statuses (`draft`, `research_pending`, `research_complete`, `entry_conditions_set`); age = whole days since `updated_at`, shown when N > 14; single named constant; display-only. Playwright required.

**Staging-only ACs:** None.

---

#### ST-03 — CSV export for Screener results and Watchlist

**Source:** BLG-FEAT-97
**Owner:** Head of Engineering; Head of UX & Design
**Estimated effort:** S (~0.5–1d)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03` (read with `stage4_backlog_slice_addendum.md#ST-03`)

**Dependencies:** None — land before ST-05 (both touch Screener/Watchlist)

**Notes:** Addendum ST-03: control label "Download CSV"; exports the displayed rows after filters/sort; columns = full desktop column set excluding selection checkbox and Actions; spreadsheet-formula-injection guard on string cells. Specs `screener_results.md` v1.7, `watchlist.md` v0.8. Playwright required.

**Staging-only ACs:** None.

---

#### ST-04 — In-app reminder to complete TradeReflection within 48 hours of a trade closing

**Source:** BLG-FEAT-98
**Owner:** Product Owner; Head of Engineering
**Estimated effort:** M (~1–2d)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04` (read with `stage4_backlog_slice_addendum.md#ST-04`)

**Dependencies:** None

**Notes:** Addendum ST-04: toggle governs email only, in-app feed row always created, new "Reflection Reminder" email toggle defaults Off; re-entry link `/TradeHistory?reflect={trade_id}` opens the existing `TradeReflectionModal`; completing the reflection auto-marks the reminder read. Changes an API response/contract — update `docs/specs/api_contracts/` and `docs/reference/openapi.yaml` (and `backend/routers/test.py` + `SystemStatus.js` fallback count + `SC-SS-01b` if a new route) in the same commit (CLAUDE.md §2). The 48h AC is time-based: verify with an injected clock; Director of Quality to confirm Playwright coverage or a filed backlog item before the PR opens.

**Staging-only ACs:** None.

---

#### ST-05 — Name one primary next action in every empty state

**Source:** BLG-FE-181
**Owner:** Head of UX & Design
**Estimated effort:** S (~1d)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05` (read with `stage4_backlog_slice_addendum.md#ST-05`)

**Dependencies:** ST-01, ST-02, ST-03 (shared call sites — rebase onto them)

**Notes:** Addendum ST-05: re-run `grep -rn emptyHeading src` at build time — the 20-site baseline in the decision record is not a substitute; 2 system-populated sites excluded; fix the trailing-period heading drift in `TradePlanCompletionRateSection.js` in the same touch. Playwright required.

**Staging-only ACs:** None.

---

#### ST-06 — Single number/currency formatting helper — audit and migrate the highest-traffic tables

**Source:** BLG-FE-182
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Estimated effort:** M (~2d)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06` (read with `stage4_backlog_slice_addendum.md#ST-06`)

**Dependencies:** ST-01, ST-02, ST-04 (touches `TradePlans.js` and Trade History) — sequence last in EPIC-01

**Notes:** Convention now defined in `design_system.md` v1.21 §Number and Currency Formatting. The migration visibly changes strings (grouping, `-` → `−`, signed Positions P&L, 1 dp → 2 dp R): update existing Playwright assertions in the same commit and list them in the QA evidence file. Playwright required.

**Staging-only ACs:** None.

---

### EPIC-02 — Financial Reporting & Records Integrity

**Maps to:** S2-02
**Owner:** Financial Reporting & Records Owner; Backend Engineering Patterns Owner; Metrics Definitions & Analytics Owner
**Estimated effort:** 2.75 days
**Risk IDs:** RISK-02
**Execution sequence:** 2

#### ST-07 — Audit whether closed-trade P&L is net of fees_paid; flag closed trades with NULL fees_paid in Monthly P&L

**Source:** BLG-FR-04
**Owner:** Financial Reporting & Records Owner
**Estimated effort:** S (~0.5–1d)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None — must precede ST-08

**Notes:** Net/gross basis must be documented before ST-08 freezes figures computed on it. If a gross-vs-net discrepancy is found, file a fix item — do not change reported figures inside this story (RISK-02). Spec `reports.md` v0.18. Response change: contract + `openapi.yaml` same commit. Playwright or recorded staging run required for the visible NULL-fee count.

**Staging-only ACs:** None.

---

#### ST-08 — Month-end immutable snapshot of Monthly P&L and the tax-year table, with a restatement diff

**Source:** BLG-FR-05
**Owner:** Financial Reporting & Records Owner
**Estimated effort:** M (~2d)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08` (read with `stage4_backlog_slice_addendum.md#ST-08`)

**Dependencies:** ST-07

**Notes:** Addendum ST-08: snapshot store is per closed month only; Tax Year summary bar shows an API-supplied "includes k restated month(s)" notice, not a second snapshot; no acknowledge/re-baseline action; months already closed at ship are baselined once, not retroactively flagged. Likely needs a new table/migration + `data_model.md` entry (and a new route → contract, `openapi.yaml`, `test.py`). The M (~2d) estimate may understate this (RISK-02): if it overruns, deliver persistence with a disclosed partial and file the remainder rather than absorb it.

**Staging-only ACs:** None.

---

### EPIC-03 — Backend & Platform Engineering Debt

**Maps to:** S2-03
**Owner:** Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner; Financial Reporting & Records Owner
**Estimated effort:** 4.55 days
**Risk IDs:** RISK-03
**Execution sequence:** 3

#### ST-09 — calculate_trailing_stop's entry-price floor for profitable positions diverges from strategy_rules.md §7.2/§7.3 and from the backtest tool

**Source:** BLG-BE-119
**Owner:** Strategy Rules & System Intent Owner; Backend Engineering Patterns Owner
**Estimated effort:** S (~0.5–1d)
**Delegation class:** delegated_decision
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None — first in EPIC-03; ST-13 depends on it

**Notes:** Decision-first (RISK-03, High): the Strategy Rules & System Intent Owner ratifies which formula is correct before any change to `calculate_trailing_stop`. Option (b) changes live-capital behaviour and needs explicit sign-off; option (a) edits `claude/strategy/strategy_rules.md` §7.2, a governance file outside the engine's write scope, and must go through that owner's own change route. If no sign-off is obtained this sprint: ship only the golden-output case and the recorded decision, leave the function unchanged, and disclose. Raise the decision request at sprint open, not at story start.

**Staging-only ACs:** None — all ACs verifiable in CI (decision record is a document).

---

#### ST-10 — list_backtest_rule_runs has no negative-limit validation and no offset param

**Source:** BLG-BE-118
**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** Response behaviour change on `GET /backtest-rule-changes/runs` (400 `INVALID_PARAMS`, not 500) — update its contract and `openapi.yaml` in the same commit. `openapi.yaml`/`api_changelog.md` are shared with EPIC-01 and EPIC-02.

**Staging-only ACs:** None.

---

#### ST-11 — JsonLinesFormatter does not truncate `message` to the spec's 500-char max

**Source:** BLG-BE-120
**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-12 — Float-vs-Decimal money-arithmetic audit with rounding-boundary golden tests

**Source:** BLG-BE-121
**Owner:** Backend Engineering Patterns Owner; Financial Reporting & Records Owner
**Estimated effort:** M (~1.5–2d)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** ST-09 if the audit touches `calculate_trailing_stop` or `position_service.py` (advisory)

**Notes:** Financial Reporting & Records Owner is co-owner of the source item. Record the inventory in the QA evidence file. Any discrepancy ≥ £0.01 must be explained, not rounded away.

**Staging-only ACs:** None.

---

#### ST-13 — Shared upstream-call helper: uniform timeout and bounded retry budget for yfinance, Alpaca and Anthropic

**Source:** BLG-BE-122
**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** M (~1.5–2d)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** ST-09 (same nightly stop-update call path)

**Notes:** Touches the live nightly stop-update path. A retry budget on Anthropic calls re-issues paid inference — it must stay within the existing AI cost gating (design gate note). Configure timeout/retry in one place. New tests must cover timeout and retry-exhaustion.

**Staging-only ACs:** None — mocked/fixture-driven tests are sufficient for every AC.

---

### EPIC-04 — Operations & Security Debt

**Maps to:** S2-04
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Estimated effort:** 1.90 days
**Risk IDs:** RISK-04
**Execution sequence:** 4

#### ST-14 — Dead-man's-switch alert when nightly-stop-update has not succeeded within 26 hours

**Source:** BLG-OPS-166
**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~0.5–1d)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** Test against a simulated / non-production run marker; must not disturb live stops (RISK-04). Alert goes to the existing Telegram channel and includes the last-success timestamp. The ACs are explicitly about a *simulated* missed run; live Telegram delivery is not an AC of this story (that is ST-16's concern).

**Staging-only ACs:** None.

---

#### ST-15 — Document GitHub Actions secrets ownership map

**Source:** BLG-OPS-163
**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~0.5d)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** Infrastructure & Operations Owner sign-off is an AC — obtained via the agent-mediated sign-off protocol at execution, recorded in the sign-off block.

**Staging-only ACs:** None.

---

#### ST-16 — Confirm synthetic uptime monitor live-fire and notification delivery (ST-11 follow-up)

**Source:** BLG-OPS-164
**Owner:** Infrastructure & Operations Owner
**Estimated effort:** XS (<1h)
**Delegation class:** delegated_decision
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Notes:** Needs a token/session with Actions-write access and a real Telegram receipt; the prior session's `gh workflow run` returned HTTP 403. If still unavailable, disclose the AC as not closeable (cite `SBX-NO-LIVE-STAGING`/`SBX-NO-LIVE-EXTERNAL-API`) rather than fabricate evidence — precedent `ESC-EXEC-20260910-01`. Raise the access request at sprint open.

**Staging-only ACs:** AC-01 (real live-fire run confirmed, run URL/ID recorded), AC-02 (real Telegram notification confirmed received). AC-03 (doc §7/§8 updated) is verifiable in CI but its content depends on AC-01/AC-02.

---

#### ST-17 — CI minutes and artifact-storage visibility; explicit retention on the 3 uploads that lack it

**Source:** BLG-OPS-165
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Estimated effort:** S (~0.5d)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None — `.github/workflows/*` is shared with EPIC-05 (ST-20); EPIC-05 rebases

**Notes:** Retention (AC-02) is a static, CI-checkable property of the workflow files. The monthly per-workflow figure (AC-01) needs live GitHub Actions usage data; if the available token cannot read it, disclose rather than estimate.

**Staging-only ACs:** AC-01 (live GitHub Actions usage / artifact-storage data).

---

### EPIC-05 — QA & Test Coverage Debt

**Maps to:** S2-05
**Owner:** QA & Testing Owner; Director of Quality; QA Lead
**Estimated effort:** 3.65 days
**Risk IDs:** RISK-05
**Execution sequence:** 5

#### ST-18 — Quarterly full-suite Playwright re-run against a fresh staging seed

**Source:** BLG-QA-171
**Owner:** Director of Quality
**Estimated effort:** M
**Delegation class:** delegated_qa
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** Needs a live staging environment and a fresh seed; the first-run AC is environment-dependent (RISK-05). Document the cadence and seed procedure separately from the first-run evidence. If staging sign-off is post-merge, file the deferral backlog item before the PR opens (sprint-planning §7 / CLAUDE.md §2).

**Staging-only ACs:** AC-02 (first quarterly run completed against a live staging seed). AC-01 (cadence and procedure documented) is verifiable in CI.

---

#### ST-19 — DoQ checklist addendum for flaky-test disposition

**Source:** BLG-QA-172
**Owner:** Director of Quality
**Estimated effort:** S
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None

**Notes:** Cross-reference must be confirmed against the existing quarantine item, not assumed.

**Staging-only ACs:** None.

---

#### ST-20 — Standing regression check for the OpenAPI Drift Detection gate itself

**Source:** BLG-QA-173
**Owner:** QA Lead
**Estimated effort:** S
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** None — `.github/workflows/*` shared with EPIC-04 (ST-17); EPIC-05 rebases

**Notes:** The deliberate-revert check (proving the fixture actually fails when the gate logic is reverted) is performed and recorded locally as part of the story.

**Staging-only ACs:** None.

---

#### ST-21 — `test_trade_plan_audit_log.py`'s unrestored `sys.modules["database"]` swap is a latent test-isolation hazard

**Source:** BLG-QA-178
**Owner:** Director of Quality
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None

**Notes:** Reordering check is manual and recorded in QA evidence. Any other file with the same unrestored `sys.modules["database"]` pattern is fixed in the same commit.

**Staging-only ACs:** None.

---

### EPIC-06 — Spec & Documentation Debt

**Maps to:** S2-06
**Owner:** Data Model & Domain Schema Owner; Strategy Rules & System Intent Owner; Frontend Specifications & UX Documentation Owner; Head of Engineering; Metrics Definitions & Analytics Owner
**Estimated effort:** 4.15 days
**Risk IDs:** RISK-06
**Execution sequence:** 6

#### ST-22 — DS-17 unique index migration not yet applied to live positions table

**Source:** BLG-SPEC-148
**Owner:** Data Model & Domain Schema Owner; Infrastructure & Operations Owner
**Estimated effort:** XS (<1h)
**Delegation class:** delegated_decision
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** None — `data_model.md` is shared with EPIC-02 (ST-08 lands first; rebase)

**Notes:** Applying the DS-17 up-migration needs write access to the live database; the staging credential is read-only. Human/delegated step. Re-run the duplicate pre-check (0 groups at 2026-09-18) immediately before applying (RISK-06). If access is unavailable, disclose (`SBX-NO-LIVE-DB`) — the `data_model.md` "confirmed-applied" text must not be written without a real confirmation.

**Staging-only ACs:** AC-01 (index exists on the live `positions` table), AC-02 (`data_model.md` AC-03 disclosure updated to confirmed-applied — depends on AC-01, cannot be closed without it).

---

#### ST-23 — PO-05 (Lightweight Replay Mode) §13 determinism pre-clearance review, standalone

**Source:** BLG-SPEC-160
**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** XS (~0.5 day)
**Delegation class:** delegated_decision
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`

**Dependencies:** None

**Notes:** The §13 determination belongs to the Strategy Rules & System Intent Owner (precedents PS-03 Monte Carlo framing; IT-06's four binding conditions). **Write-scope flag:** AC-02 (`BLG-FEAT-74`'s gate line reflects the outcome) edits an existing `claude/backlog/backlog.md` item, which `execution_prompt.md` §7 does not permit (new-item addition only). See Outstanding Actions — record the determination in a dated decisions document and hand the exact gate-line replacement text to the Head of Specs Team / Product Owner; disclose AC-02 as partial rather than edit the item.

**Staging-only ACs:** None.

---

#### ST-24 — Canonical colour-blind-safe chart palette spec

**Source:** BLG-SPEC-144
**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** S
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`

**Dependencies:** None — `design_system.md` was already bumped to v1.21 at the design gate; this story adds its own bump and rebases onto EPIC-01

**Notes:** Head of UX & Design approves the palette at QA sign-off (design gate: Design Pre-Approved). Not a re-skin — adoption in chart components is a UI change needing its own gate pass.

**Staging-only ACs:** None.

---

#### ST-25 — Lightweight ADR log for cross-cutting backend decisions

**Source:** BLG-SPEC-145
**Owner:** Head of Engineering
**Estimated effort:** M
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`

**Dependencies:** None

**Notes:** Seed at least 2 real decisions (not placeholders). Reference the log from an onboarding/index document.

**Staging-only ACs:** None.

---

#### ST-26 — Canonicalise the Sharpe-ratio lookback window

**Source:** BLG-SPEC-146
**Owner:** Metrics Definitions & Analytics Owner
**Estimated effort:** S
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-26`

**Dependencies:** None

**Notes:** Metrics-spec documentation only; note each of the 3 call-site discrepancies explicitly — the code fix is a separate follow-on item.

**Staging-only ACs:** None.

---

### EPIC-07 — Governance Process Debt

**Maps to:** S2-07
**Owner:** Head of Specs Team; Product Owner; PMO Lead; FinOps & Resource Architect; AI Compliance & Governance Officer; Strategy Rules & System Intent Owner
**Estimated effort:** 4.25 days
**Risk IDs:** RISK-07
**Execution sequence:** 7

#### ST-27 — Release-planning gate scan treats lapsed date gates as permanently gated

**Source:** BLG-GOV-345
**Owner:** Head of Specs Team; Product Owner
**Estimated effort:** S (~0.5–1d)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-27`

**Dependencies:** None — first prompt/`OPERATIONAL_GUIDE.md` bump in EPIC-07; must precede ST-30

**Notes:** Edits `scripts/scan_backlog_gate_conditions.py` and `release_planning_prompt.md` §1.3a — CLAUDE.md §6 checklist applies (version bump, `OPERATIONAL_GUIDE.md` §14 and source-prompt header, `prompt_change_log.md`); apply the §8 step 2a collision check per file. `BLG-GOV-90`/`BLG-GOV-188` were already cleared at Release Planning (ST-31/ST-32). The four uncleared items (`BLG-FEAT-59`/`60`/`63`, `BLG-FE-84`) are re-gated by this story with a new dated condition — it does not wait on the 2026-09-24 review. **Write-scope flag:** clearing/re-gating edits existing `backlog.md` items — see Outstanding Actions.

**Staging-only ACs:** None.

---

#### ST-28 — Re-confirm §13 boundary review cadence

**Source:** BLG-GOV-329
**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** S
**Delegation class:** delegated_decision
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-28`

**Dependencies:** None

**Notes:** Decision belongs to the Strategy Rules & System Intent Owner (STEP 8.1.5 finding). If deferred again, the new trigger must be more concrete than the prior one — the engine may draft options but must not choose for the owner.

**Staging-only ACs:** None.

---

#### ST-29 — Revisit sprint capacity band given sustained ≥90% utilisation

**Source:** BLG-GOV-328
**Owner:** Product Owner
**Estimated effort:** S
**Delegation class:** delegated_decision
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-29`

**Dependencies:** None

**Notes:** **Names `claude/roadmap/workforce_capacity.md` for the `execution_prompt.md` §7 plan-authorised exception (BLG-GOV-337):** the review and the hold/raise decision are documented into that file under this story; the commit message must cite this `sprint_backlog.md` ST-29 entry. The file may be documented into, never used to decide — the hold/raise call is the Product Owner's (file owner = story owner = Product Owner). FinOps & Resource Architect reviews the utilisation history. Any change applies from the next planning run, not to this sealed sprint.

**Staging-only ACs:** None.

---

#### ST-30 — Fixed-cadence audit of every governance prompt's §14 version-table entry

**Source:** BLG-GOV-325
**Owner:** Head of Specs Team
**Estimated effort:** S
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-30`

**Dependencies:** ST-27 (prompt-version and `OPERATIONAL_GUIDE.md` bumps must not collide)

**Notes:** Edits a governed prompt (`roadmap_prompt.md` or the manage-roadmap prompt) — CLAUDE.md §6 checklist applies; separate commit per bump; §8 step 2a collision check per file. The first mandatory-cadence run must be a real run with results recorded.

**Staging-only ACs:** None.

---

#### ST-31 — Claude model deprecation monitoring procedure (consolidated)

**Source:** BLG-GOV-90
**Owner:** AI Compliance & Governance Officer; Infrastructure & Operations Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-31`

**Dependencies:** None

**Notes:** Build on `docs/governance/ai_model_version_pinning_policy.md` (§6–§7) and `ai_model_deprecation_check_v52.md` — do not duplicate. AC-03 gate (`BLG-GOV-74` first review) was verified met at Release Planning: `docs/governance/ai_feature_usage_quarterly_review_2026-09-07.md`; re-cite it.

**Staging-only ACs:** None.

---

#### ST-32 — Sprint Velocity Trend Chart

**Source:** BLG-GOV-188
**Owner:** PMO Lead
**Estimated effort:** S (~1–2 days)
**Delegation class:** autonomous
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-32`

**Dependencies:** None

**Notes:** Governance artefact generated from `velocity_metrics.md`, not product UI (if built as an app page it would need its own design-gate pass).

**Staging-only ACs:** None.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | 28.00 days (ceiling of the ~24–28 day band, `workforce_capacity.md` effective 2026-07-17) |
| Total estimated effort (in-scope) | 28.00 days (27.90 days under a band-letter-only reading) |
| Utilisation | 100.0% of the 28-day ceiling — exceeds the §1.5 95% buffer floor (acknowledged; see `sprint_capacity.md`) |
| Over-allocation | No (28.00 is not > 28; the WARN threshold is not crossed) |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| None | — | All 32 items in the authoritative backlog slice enter the sprint; no `deferred_at_planning` entries are required in `execution_state.json`. Items excluded at Release Planning are listed in `sprint_planning_notes.md ## Deferred Items` and are not re-litigated here. |

## Deferred Execution Blockers Accepted

Omitted — `deferred_execution_blockers` is empty in `state.json`.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Buffer-floor-exceeded acknowledgement (100.0% of ceiling) | Product Owner | No |
| ST-09: schedule the live trailing-stop formula decision at sprint open; without explicit sign-off ship only the golden-output case + recorded decision and disclose | Strategy Rules & System Intent Owner | No |
| ST-16 / ST-22 / ST-18: raise the Actions-write token, live-DB write access and live-staging requests at sprint open; disclose rather than fabricate if unavailable; file the deferral backlog item before the PR opens if staging sign-off is post-merge | Infrastructure & Operations Owner / Director of Quality | No |
| ST-23 (AC-02) and ST-27 (clear/re-gate legs): `execution_prompt.md` §7 does not permit editing existing `backlog.md` items — rule on a plan-authorised exception (as BLG-GOV-337 did for `workforce_capacity.md`) or accept the disclosed-partial fallback | Head of Specs Team + Product Owner | No |
| ST-29: hold/raise decision must be supplied by the Product Owner — the engine documents it, never decides it | Product Owner | No |
| Confirm Playwright coverage for the observable ACs of ST-01–ST-08 (incl. ST-04's 48h AC); file a backlog item before any PR opens if an AC is deferred to staging | Director of Quality | No |
| 12 `Provisional-Target: v9.6` items not seated (`BLG-SPEC-149`–`155`, `BLG-FE-178`/`179`, `BLG-QA-179`/`180`/`181`, 4.80 days) — Product Owner call for v9.7; not re-decided here | Product Owner | No |
| STEP -1 Hard Gates 1–2 status-vocabulary wording — already filed as `BLG-GOV-333`; applied the Lifecycle Guard reading again this cycle | Head of Specs Team | No |

No outstanding action is marked `Blocker? Yes`.

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed (agent-mediated — see `sprint_goal.md`)
**Scope confirmed:** Confirmed — full 32-item / 7-EPIC scope per Release Planning and the Design Gate, no items deferred at Sprint Planning
**Capacity confirmed:** Confirmed — 28.00d within the ~24–28d band; buffer-floor overage (100.0% of ceiling) acknowledged as the direct consequence of the standing "use full capacity" instruction
**Deferred execution blockers accepted (if any):** N/A — `deferred_execution_blockers` empty in `state.json`
**Signed off by:** Product Owner (agent-mediated, same method as the `2026-09-15__release-v9.5` sprint planning seal and this cycle's design gate)
**Date:** 2026-09-21

---

## Change Log

| Date | Change |
|------|--------|
| 2026-09-21 | Initial publication and seal — 32 items / 7 EPICs, 28.00d, for 2026-09-21__release-v9.6. |
