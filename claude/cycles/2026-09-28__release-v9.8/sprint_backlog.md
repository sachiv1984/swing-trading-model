# Sprint Backlog — 2026-09-28__release-v9.8

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-09-28
**Cycle:** 2026-09-28__release-v9.8
**Release:** v9.8
**Sprint Goal:** Clear the full v9.8 full-capacity debt slice — 39 stories across 6 EPICs spanning frontend/UX consistency, backend reliability, QA/test coverage, operations/security hardening, spec & API contract debt, and governance/process debt — with no anchor feature, at exactly the top of the confirmed ~24–28 day sprint capacity band.
**Backlog Slice Source:** Original — `claude/cycles/2026-09-28__release-v9.8/stage4_backlog_slice.md`

## Merge Order

- **EPIC merge sequence:** EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04 → EPIC-05 → EPIC-06 (per `release_plan.md ## Execution Plan` table order; EPIC-01 leads per Skill-Silo rotation guideline — see `sprint_planning_notes.md` Execution Sequence).
- **`execution_state.json` owner EPIC:** EPIC-01 (first in execution order). EPIC-02–06 must check for its existence and append their own section rather than overwrite.
- **Shared files across EPICs:** `src/pages/Screener.js` (`SCREENER_COLUMNS`) — EPIC-01 (ST-02) owns the canonical version; EPIC-05 (ST-26) must rebase onto `main` after EPIC-01 merges before finalising its `screener_results.md` cross-check. See `sprint_planning_notes.md` Shared File Ownership Advisory.

## Sprint Scope

### EPIC-01 — Frontend & UX Debt Clearance

**Maps to:** S2-01–S2-06
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Estimated effort:** ~6.5–9.5 days
**Risk IDs:** None
**Execution sequence:** 1

#### ST-01 — Migrate the remaining toFixed / toLocaleString call sites to the shared formatting helper

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** L (~3–5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Notes:** Frontend-visible change — CLAUDE.md §2 Playwright coverage requirement is already built into this item's own AC (3rd bullet).

**Staging-only ACs:** None — all ACs verifiable in CI via Playwright.

---

#### ST-02 — Drive Screener and Watchlist table body cells from the shared column definitions

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** M (~1–2d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None (but see Notes — EPIC-05/ST-26 depends on this item's outcome; sequence ST-02 before ST-26)

**Notes:** Owns the canonical `SCREENER_COLUMNS` definition this sprint — EPIC-05's ST-26 must be sequenced after this EPIC merges to `main` (Merge Order / Shared File Ownership Advisory above).

**Staging-only ACs:** None — all ACs verifiable in CI via Playwright.

---

#### ST-03 — Make the Tax Year restated-months notice link to months the Monthly tab actually shows

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** S (~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None — all ACs verifiable in CI via Playwright.

---

#### ST-04 — SystemStatus.js categorizeEndpoint() has no case for the new /replay prefix

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** Carried forward from `2026-09-23__release-v9.7` closure Friction Log (filed as `BLG-FE-191`, P4, outside that routine's write scope).

**Staging-only ACs:** None — all ACs verifiable in CI via Playwright.

---

#### ST-05 — Responsive-table behaviour spec for Positions, TradeHistory and TradePlans

**Owner:** Head of UX & Design
**Estimated effort:** S (~0.5–1d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** Spec-authoring task documenting existing/well-scoped behaviour — no new UX design decision required (BLG-GOV-72 default-autonomous fast-path).

**Staging-only ACs:** None — spec-authoring item, no observable UI AC requiring Playwright or staging.

---

#### ST-06 — Canonical keyboard-shortcut inventory spec

**Owner:** Head of UX & Design
**Estimated effort:** S (~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** If genuine shortcut conflicts are found during authoring that cannot be resolved unilaterally, file a follow-on backlog item rather than resolving unilaterally.

**Staging-only ACs:** None — spec-authoring item.

---

### EPIC-02 — Backend Reliability & Financial Correctness

**Maps to:** S2-07–S2-08
**Owner:** Head of Engineering; Financial Reporting & Records Owner
**Estimated effort:** ~2 days
**Risk IDs:** None
**Execution sequence:** 2

#### ST-07 — Remaining ad hoc timeout=/retry call sites not yet on the shared upstream-call helper

**Owner:** Head of Engineering
**Estimated effort:** S (~1d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** Must not change behaviour of already-working Stooq/Twelve Data cooldown/rate-limit logic (explicit AC).

**Staging-only ACs:** None — verifiable via unit/integration test.

---

#### ST-08 — Extend the v9.7 float→Decimal fee-rounding audit to tax-year statement calculations

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** S (~1d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** If a gap is found, file it with the same rigor as `BLG-BE-127` (per AC).

**Staging-only ACs:** None — verifiable via unit test at rounding boundaries.

---

### EPIC-03 — QA & Test Coverage

**Maps to:** S2-09–S2-16
**Owner:** Director of Quality
**Estimated effort:** ~6.5 days
**Risk IDs:** None
**Execution sequence:** 3

#### ST-09 — Golden-fixture CI regression for AI prompt templates — boundary-language drift caught at template-change time

**Owner:** Director of Quality
**Estimated effort:** S (~0.5–1d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** Must run without `ANTHROPIC_API_KEY` (explicit AC) — golden-fixture comparison only, no live model call.

**Staging-only ACs:** None — CI-only by design.

---

#### ST-10 — No end-to-end test confirms backend/main.py's wired root logger actually emits JSON in situ

**Owner:** Director of Quality
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None — verifiable via test asserting current implementation and failing on regression.

---

#### ST-11 — Add Playwright duration-assertion coverage for the 9 toast call sites fixed in ST-42 (Toast Notification Timing standard)

**Owner:** Director of Quality
**Estimated effort:** S (~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** Frontend-visible timing AC — CLAUDE.md §2 requires Playwright coverage for interaction-timing ACs; this item is exactly that coverage.

**Staging-only ACs:** None — timing assertions are CI-Playwright-verifiable.

---

#### ST-12 — Add regression coverage for the motion-timing values fixed in ST-41 (500ms ceiling components)

**Owner:** Director of Quality
**Estimated effort:** S (~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None — CI-verifiable.

---

#### ST-13 — Escaped-defect and follow-on-ratio tracking per cycle

**Owner:** Director of Quality
**Estimated effort:** S (~0.5–1d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** Baseline computed for v9.5; per-cycle row added at each post-ship closure going forward (process change, not one-off).

**Staging-only ACs:** None — data/process tracking, no runtime behaviour to verify.

---

#### ST-14 — DoQ checklist addendum for AI-touching stories

**Owner:** Director of Quality
**Estimated effort:** S (~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None — document addition.

---

#### ST-15 — Mutation-testing pilot on the sizing calculator and stop ratchet

**Owner:** Director of Quality
**Estimated effort:** M (~2d)
**Delegation class:** delegated_qa

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** Survivor triage requires Director of Quality judgment on genuine test gaps vs. acceptable equivalent mutants — not engine-determinable.

**Staging-only ACs:** None — mutation testing runs in CI/local test environment.

---

#### ST-16 — Enable Playwright trace and screenshot retain-on-failure

**Owner:** Director of Quality
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Notes:** Playwright config change.

**Staging-only ACs:** None — CI config verifiable by forcing a failing run.

---

### EPIC-04 — Operations & Security Hardening

**Maps to:** S2-17–S2-19
**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead
**Estimated effort:** ~1.5 days
**Risk IDs:** RISK-01 (ST-17)
**Execution sequence:** 4

#### ST-17 — No check that the staging backend actually redeployed after a merge that changes startup-applied schema (DS-19 sat unapplied on staging)

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~0.5d)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None (internal sequencing only — see Notes)

**Notes:** **RISK-01.** Scope explicitly names 3 alternative implementation vehicles (existing `staging-smoke-test.yml`, a new post-merge workflow, or a cycle-close verification step) with the choice deferred to implementation. Execution must resolve this design decision (Infrastructure & Operations Owner) as a first sub-step before beginning the build sub-step — do not begin implementation before the decision is recorded. No HoST design-session artefact exists yet (LL-v2.2-SP-01 advisory) — recommend a brief decision session at kickoff.

**Staging-only ACs:** AC-01 ("A merge to main that should have redeployed staging but did not produces a visible failure or alert") — `[staging-only evidence]`: confirming the alert actually fires on a real stale-staging condition cannot be reproduced in CI. If staging sign-off is deferred to post-merge, a backlog item must be filed before the PR opens (CLAUDE.md §2).

---

#### ST-18 — No documented allow-list of pre-approved read-only staging-DB query patterns for governed-session gate re-checks

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~0.5d)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** Establishing which query patterns are safe against a production-adjacent staging role without further confirmation is a security-sensitive policy call — requires Infrastructure & Operations Owner / Cybersecurity & Trust Lead sign-off, not engine-determinable. No HoST design-session artefact exists yet (LL-v2.2-SP-01 advisory).

**Staging-only ACs:** None — output is a documentation change; no runtime behaviour to verify in CI or staging.

---

#### ST-19 — Harden the non-registry dependency guard (missed specifier forms, trailing-comment false positive, no exit-code test)

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** S (~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None — script + exit-code behaviour fully testable in CI.

---

### EPIC-05 — Spec & API Contract Debt

**Maps to:** S2-20–S2-29
**Owner:** Head of Specs Team; Data Model & Domain Schema Owner
**Estimated effort:** ~5–7.5 days
**Risk IDs:** None
**Execution sequence:** 5

#### ST-20 — Document idempotency and double-submit behaviour for every mutating endpoint

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5–1d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** None

**Notes:** Endpoint headings must remain `## METHOD /path` (OpenAPI Drift Detection gate, CLAUDE.md §2) — explicit AC already covers this.

**Staging-only ACs:** None — documentation-only, no runtime behaviour change.

---

#### ST-21 — Error-payload (4xx/5xx) examples for the 10 most-called endpoints, covered by the example-freshness checker

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5–1d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None — `scripts/check_contract_example_freshness.py` runs in CI.

---

#### ST-22 — Full field-level openapi.yaml authoring pass for 20 generic/thin data payload schemas

**Owner:** Head of Specs Team
**Estimated effort:** M (~1–2d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** None

**Notes:** Largest EPIC-05 item — 20 endpoint dispositions required per its own triage doc §5.

**Staging-only ACs:** None — schema authoring verified by the existing freshness checker in CI.

---

#### ST-23 — POST /trade-plans and DELETE /trade-plans/{id} declare no response schema in openapi.yaml

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None — CI-verifiable via freshness checker.

---

#### ST-24 — trade_plans CREATE TABLE / DS-04 CHECK constraint undocumented since ensure_trade_plans_extended_status() shipped

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`

**Dependencies:** None

**Notes:** New DS-xx entry must match `data_model.md`'s established format (explicit AC).

**Staging-only ACs:** None — documentation-only.

---

#### ST-25 — openapi.yaml's OperationalHealthResponse.ai_journal doesn't model its either/or shape with oneOf

**Owner:** Head of Specs Team
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None — schema-shape change, CI-verifiable.

---

#### ST-26 — screener_results.md column list omits the Earnings column that the shipped table has

**Owner:** Head of Specs Team
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-26`

**Dependencies:** EPIC-01/ST-02 (must complete and merge first — see Merge Order / Shared File Ownership Advisory)

**Notes:** Rebase onto `main` after EPIC-01 merges before finalising the §5.3 column list, so it reflects the post-ST-02 `SCREENER_COLUMNS` state rather than a stale snapshot.

**Staging-only ACs:** None — documentation cross-check against source code.

---

#### ST-27 — trade_reflection.md §4 specifies an en dash for a missing R-multiple; the convention is an em dash

**Owner:** Head of Specs Team
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-27`

**Dependencies:** None

**Notes:** Modal fields must format via the shared helper (2nd AC bullet) — touches the same formatting helper as EPIC-01/ST-01; no file-level collision expected (different components) but worth a final grep check at PR time.

**Staging-only ACs:** None — glyph/formatting fix, CI-verifiable.

---

#### ST-28 — sprint_velocity_trend_chart.md trend sentence splices non-adjacent PVR readings

**Owner:** Head of Specs Team
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-28`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None — documentation-only.

---

#### ST-29 — Reconcile the IT-06 §13 review (Alpaca sync recorded as GET-only, no orders placed) with a sync that POSTs orders and DELETEs positions

**Owner:** Strategy Rules & System Intent Owner (disposition); Head of Specs Team (documentation)
**Estimated effort:** S (~0.5d)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-29`

**Dependencies:** None

**Notes:** AC explicitly requires the disposition to be recorded by the Strategy Rules & System Intent Owner — named-authority decision, not engine-determinable.

**Staging-only ACs:** None — reconciliation is a documentation/decision output, not a runtime behaviour change.

---

### EPIC-06 — Governance & Process Debt

**Maps to:** S2-30–S2-39
**Owner:** PMO Lead; Head of Specs Team
**Estimated effort:** ~7–8.5 days
**Risk IDs:** RISK-02 (ST-38)
**Execution sequence:** 6

#### ST-30 — Bake accessible-name and heading-order rules into the Base44 prompt template

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** S (~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-30`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None — template text change; a regenerated-page test run is the verification method, not live staging.

---

#### ST-31 — PVR / Skill-Silo measurement package — split debt into user-protective vs hygiene, add effort-weighted PVR, add a leading ungated-U-pool indicator

**Owner:** PMO Lead

**Estimated effort:** M (~1.5–2d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-31`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None — metrics/documentation.

---

#### ST-32 — Delivery-flow metrics — lead time by priority band and ready-pool runway forecast

**Owner:** PMO Lead
**Estimated effort:** S (~1d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-32`

**Dependencies:** None

**Notes:** Runway figure must be cited in the next rebalance's STEP 7.3 (forward-looking AC, not verifiable this sprint).

**Staging-only ACs:** None.

---

#### ST-33 — Persist STEP 7.2 role-share tallies as a structured history file

**Owner:** PMO Lead
**Estimated effort:** S (~0.5–1d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-33`

**Dependencies:** None

**Notes:** History backfilled for the last 3 cycles (explicit AC).

**Staging-only ACs:** None.

---

#### ST-34 — JSON Schema for .claude_current_state.json, including the last_updated_utc field the roadmap engine reads

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5–1d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-34`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None — schema validation is a local/CI check.

---

#### ST-35 — Size "grep-and-fix-everywhere" and "verify against live environment" story classes a notch higher by default

**Owner:** Head of Specs Team
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-35`

**Dependencies:** None

**Notes:** Governance prompt edit (`sprint_planning_prompt.md` or `release_planning_prompt.md`) — CLAUDE.md §6 Governance File Edit Checklist applies in the same commit (version bump, `OPERATIONAL_GUIDE.md` §14 sync, `prompt_change_log.md` entry).

**Staging-only ACs:** None.

---

#### ST-36 — strategy_rules.md §13.5 roster missing PO-05 row after 2026-09-23 clearance

**Owner:** Head of Specs Team
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-36`

**Dependencies:** None

**Notes:** `claude/strategy/` is a governance file — CLAUDE.md §2 restriction applies; this story is the explicit instruction authorising the edit.

**Staging-only ACs:** None.

---

#### ST-37 — governance_sync.yml does not auto-close a phased story's GitHub issue (ST-XXa/b/c vs. the commit tag's bare ST-XX)

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-37`

**Dependencies:** None

**Notes:** Must not regress the ST-19/BLG-GOV-314 fix for partially-done phased stories (explicit AC) — regression test required.

**Staging-only ACs:** None — CI workflow logic, unit-testable.

---

#### ST-38 — No scheduled trigger/owner fires the 90-day post-ship AI feature usage review (BLG-GOV-74/140/141/142 cluster)

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** S (~1d)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-38`

**Dependencies:** None (internal sequencing only — see Notes)

**Notes:** **RISK-02.** Scope defers "which governed routine owns firing the review" to a decision at build time (post-ship closure's own cadence checks are the most natural fit per the item's own Problem statement, but not pre-decided here). Execution must resolve this design decision (Head of Specs Team / PMO Lead) as a first sub-step before beginning the build sub-step. No HoST design-session artefact exists yet (LL-v2.2-SP-01 advisory).

**Staging-only ACs:** None — the trigger mechanism itself is CI/schedule-testable; actually conducting the review is explicitly out of scope for this item.

---

#### ST-39 — PO-04 (Reflection ↔ Outcome Correlation) needs its own §13 boundary review, not just a stub-file note

**Owner:** Head of Specs Team
**Estimated effort:** XS (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-39`

**Dependencies:** None

**Notes:** This story itself is the trackable item required by its own AC.

**Staging-only ACs:** None.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24–28 days |
| Total estimated effort (in-scope) | 28.00 days |
| Utilisation | 100.0% (top of band) |
| Over-allocation | No (within band, at ceiling) |

## Items Deferred This Sprint

None — all 39 backlog-slice items entered the sprint at full capacity.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Schedule a brief design-decision session ahead of ST-17 kickoff (RISK-01 — where does the post-deploy check live) | Infrastructure & Operations Owner | No |
| Schedule a brief design-decision session ahead of ST-18 kickoff (staging-DB query allow-list scope) | Infrastructure & Operations Owner / Cybersecurity & Trust Lead | No |
| Schedule the §13 disposition review ahead of ST-29 kickoff (Alpaca sync GET-only vs. actual order-placing behaviour) | Strategy Rules & System Intent Owner | No |
| Schedule a brief design-decision session ahead of ST-38 kickoff (RISK-02 — which routine owns firing the 90-day review) | Head of Specs Team / PMO Lead | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed 2026-09-28 — see `sprint_goal.md`.
**Scope confirmed:** Confirmed 2026-09-28 — all 39 items from `stage4_backlog_slice.md`, full capacity (28.00/28.00 days), no deferrals.
**Capacity confirmed:** Confirmed 2026-09-28 — 100% utilisation acknowledged (buffer-floor advisory noted and accepted, see `sprint_capacity.md` §1.5); not a `warn` outcome.
**Deferred execution blockers accepted (if any):** N/A — `deferred_execution_blockers` empty in `state.json`.
**Signed off by:** Product Owner
**Date:** 2026-09-28
