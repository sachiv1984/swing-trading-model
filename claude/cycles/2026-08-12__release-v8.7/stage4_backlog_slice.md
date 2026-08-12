Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-12
Cycle: 2026-08-12__release-v8.7
Release: v8.7

# Backlog Slice — v8.7

<!-- release-plan-marker: RP:v8.7:2026-08-12__release-v8.7 -->

21 stories across 7 grouped EPICs. Full acceptance criteria below (source of truth for Sprint Planning and Execution). Scope led by user-facing features per explicit release-planning directive ("use full capacity, user features to be prioritised").

---

## EPIC-01 — User-Facing Product Features & UX Completion

**Maps to:** S2-01
**Owner:** Product Owner; Head of UX & Design

### ST-01 — Thesis pre-mortem / invalidation-condition capture at trade-plan entry
**Source:** BLG-FEAT-84
**Priority:** P3 (Low)
**Effort:** M
**Acceptance Criteria:**
- Optional invalidation-condition field added to the trade plan entry flow
- Field is captured and persisted on new trade plans
- Product Owner sign-off on field placement/copy

### ST-02 — Consume trade_plan_linked/trade_plan_id in the position-entry flow
**Source:** BLG-FE-158
**Priority:** P3 (Low)
**Effort:** XS
**Acceptance Criteria:**
- `TradeEntry.js` reads `trade_plan_linked`/`trade_plan_id` from the `POST /portfolio/position` response
- User sees a confirmation naming the linked plan when `trade_plan_linked: true`, or an explicit "no matching plan found — logged unlinked" notice when `false`

### ST-03 — Persist isAiDraft flag on trade_plans for AI-origin display badges
**Source:** BLG-BE-95
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- `trade_plans.is_ai_draft` boolean column added (default `false`), persists across sessions
- Set `true` when a narrative field is populated via "Improve with AI" and not yet manually edited; cleared on manual edit (mirrors existing client-side semantics)
- Setup Thesis Digest panel shows the "AI draft" badge per `ux_spec.md` §2 when `is_ai_draft` is true

### ST-04 — SI-02 Gate Status section (Reports.js) light/dark theme fix
**Source:** BLG-FE-151
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- `SI02GateStatusSection` renders correctly in both light and dark theme with no hardcoded dark-only structural class remaining
- No visual regression to the section's dark-theme appearance — Playwright coverage or staging sign-off per CLAUDE.md's frontend-visible-change rule

### ST-05 — Unrealised P&L card (Reports.js) light/dark theme fix
**Source:** BLG-FE-152
**Priority:** P3 (Low)
**Effort:** S
**Acceptance Criteria:**
- Unrealised P&L card renders correctly in both light and dark theme with no hardcoded dark-only structural class remaining
- No visual regression — Playwright coverage or staging sign-off per CLAUDE.md's frontend-visible-change rule

### ST-06 — Convert 4 hardcoded dark-only modals to theme-aware tokens
**Source:** BLG-FE-156
**Priority:** P2 (Medium)
**Effort:** S
**Depends on:** BLG-FE-147 (v8.6, shipped) — tokens already registered
**Acceptance Criteria:**
- `WatchlistModal.js`, `ExportModal.js`, `PositionEntryModal.js`, `WidgetLibrary.js` converted from hardcoded `bg-slate-900`/`text-white` to `bg-background`/`text-foreground` (or `bg-popover`/`text-popover-foreground` where appropriate), per `design_system.md` "Modal / Dialog Theming"
- No visual regression to existing dark-theme appearance — Playwright coverage or staging sign-off per CLAUDE.md's frontend-visible-change rule

---

## EPIC-02 — Trade-Plan Data Integrity Closure

**Maps to:** S2-02
**Owner:** Head of Engineering; Data Model, Domain & Schema Owner

### ST-07 — Staging verification of ST-03's (v8.6) trade-plan-linkage enforcement, and legacy orphaned-row audit
**Source:** BLG-BE-96
**Priority:** P1 (High) — mandatory, PO risk-acceptance condition: do not defer further
**Effort:** S
**Acceptance Criteria:**
- On staging (or production, read-only): confirm `POST /portfolio/position` links a trade plan by default via the "Start Trade from Plan" flow (`trade_plan_linked: true`)
- Live query confirms 0 rows (or any found are fixed) matching `status='active' AND position_id IS NULL` in `trade_plans`
- DS-12 CHECK constraint (`trade_plans_active_requires_position_check`) confirmed present and `NOT VALID` on the live table
- Head of Engineering + Data Model, Domain & Schema Owner sign-off
- **If the legacy-row query finds any of the 11 known rows carry `status='active'`, that finding escalates to its own P0 immediately** — do not fold into this item's timeline

---

## EPIC-03 — Test Coverage for Shipped UI & Financial Correctness

**Maps to:** S2-03
**Owner:** QA & Testing Owner

### ST-08 — Playwright coverage for the remaining shadcn token call-site families left untested by v8.6/ST-04
**Source:** BLG-FE-157
**Priority:** P2 (Medium)
**Effort:** S
**Acceptance Criteria:**
- Each of `card`, `popover`, `secondary`, `accent`, `destructive`, `border`, `ring` has at least one Playwright test asserting the real post-fix computed colour/background at a confirmed-affected live call site
- Tests pass in real CI

### ST-09 — End-to-end integration assertion for tax-year boundary trade rows
**Source:** BLG-QA-148
**Priority:** P3 (Low)
**Effort:** XS
**Acceptance Criteria:**
- A test mocks `get_trade_history_by_tax_year`'s DB cursor to return a fabricated row with `exit_date` on a tax-year boundary day
- Asserts the row appears exactly once in `get_tax_year_report()`'s returned `trades` list for the correct year, and zero times for the adjacent year

---

## EPIC-04 — Backend Reliability & Performance Hardening

**Maps to:** S2-04
**Owner:** Backend Engineering Patterns Owner

### ST-10 — Extend the BLG-BE-57 retry/backoff audit pattern to Gemini API call sites
**Source:** BLG-BE-89
**Priority:** P2 (Medium)
**Effort:** M
**Acceptance Criteria:**
- All Gemini API call sites apply the same retry/backoff pattern established for other external API calls (`BLG-BE-57`)
- Failure modes (timeout, rate-limit, transient 5xx) covered by tests

### ST-11 — N+1 query audit across trade/position list endpoints
**Source:** BLG-BE-90
**Priority:** P2 (Medium)
**Effort:** M
**Acceptance Criteria:**
- Trade/position list endpoints audited for N+1 query patterns
- Clearly-attributable N+1 cases fixed; any requiring broader refactor filed as follow-up backlog items rather than expanded in-cycle

### ST-12 — SI-04 schema requirements pre-design
**Source:** BLG-BE-30
**Priority:** P2 (Medium)
**Effort:** S
**Acceptance Criteria:**
- SI-04 data model requirements documented ahead of SI-04 sprint entry (schema-only pre-work, no SI-04 feature implementation)

---

## EPIC-05 — Security Hardening

**Maps to:** S2-05
**Owner:** Cybersecurity & Trust Lead

### ST-13 — Prompt-injection resistance test for the Gemini thesis-generation endpoint
**Source:** BLG-SEC-30
**Priority:** P2 (Medium)
**Effort:** M
**Acceptance Criteria:**
- Test suite exercises known prompt-injection patterns against the Gemini thesis-generation endpoint (staging/test environment only)
- Results documented; any confirmed vulnerability filed as a P1/P0 security item

### ST-14 — Rate-limit audit on unauthenticated/low-auth endpoints
**Source:** BLG-SEC-31
**Priority:** P2 (Medium)
**Effort:** M
**Acceptance Criteria:**
- All unauthenticated/low-auth endpoints inventoried and checked against expected rate-limit configuration
- Gaps documented; any missing rate limits filed as follow-up items or fixed in-cycle if trivial

---

## EPIC-06 — Operations & Infrastructure Debt

**Maps to:** S2-06
**Owner:** Infrastructure & Operations Owner

### ST-15 — Render Starter-tier headroom reassessment
**Source:** BLG-OPS-139
**Priority:** P2 (Medium)
**Effort:** S
**Acceptance Criteria:**
- Current Render Starter-tier resource headroom (CPU/memory/dyno hours) reassessed against current traffic/build patterns
- Recommendation recorded (upgrade / hold / downgrade) with supporting data

### ST-16 — Render dashboard-only build/deploy path filter — canonical documentation + onboarding note
**Source:** BLG-OPS-140
**Priority:** P2 (Medium)
**Effort:** S
**Acceptance Criteria:**
- Canonical documentation added explaining Render's dashboard-only build-path filter (invisible to repo grep) — the root cause behind `BLG-OPS-82`/`BLG-OPS-90`
- Onboarding note added so a future runtime-read file change is checked against this filter before assuming a deploy will pick it up

### ST-17 — Fix substring-match false negatives in check_api_performance_baseline_drift.py's find_missing_endpoints()
**Source:** BLG-OPS-142
**Priority:** P2 (Medium)
**Effort:** S
**Acceptance Criteria:**
- `find_missing_endpoints()` no longer produces false negatives from substring matching
- Regression test added covering the previously-missed case class
- Closes the fix carried across 3 consecutive Post-Ship Closures (v8.4→v8.5→v8.6)

---

## EPIC-07 — Governance & Spec Debt

**Maps to:** S2-07
**Owner:** Head of Specs Team

### ST-18 — CLAUDE.md §8 rule for shared JSON schema drift mid-sprint between sibling EPIC branches
**Source:** BLG-GOV-290
**Priority:** P2 (Medium)
**Effort:** S
**Acceptance Criteria:**
- CLAUDE.md §8 (or a linked shared-standards section) gains an explicit rule covering a shared JSON field's schema shape drifting mid-sprint between sibling EPIC branches (git merge sees no conflict on schema-shape drift the way it does on version-number collisions)

### ST-19 — Roadmap Unlock Tracker — consolidated view of all gated features and their conditions
**Source:** BLG-GOV-303
**Priority:** P2 (Medium)
**Effort:** M
**Acceptance Criteria:**
- A single consolidated document/table lists all gated backlog items, their gate conditions, and current gate status
- Sourced from (or cross-checked against) `scripts/scan_backlog_gate_conditions.py` output to avoid drift from the authoritative scan

### ST-20 — §13 policy question: are confidence-interval-qualified "preview" analytics compatible with the deterministic/non-predictive boundary?
**Source:** BLG-GOV-305
**Priority:** P2 (Medium)
**Effort:** S
**Acceptance Criteria:**
- Strategy Rules & System Intent Owner produces a written policy determination answering the question
- Determination recorded in `strategy_rules.md` §13 or a linked policy note

### ST-21 — Canonical "gated" DataState variant and visual/interaction spec for not-yet-unlocked feature surfaces
**Source:** BLG-SPEC-124
**Priority:** P2 (Medium)
**Effort:** M
**Acceptance Criteria:**
- A canonical `DataState` variant ("gated") is specified with visual treatment and interaction behaviour for feature surfaces that exist but are not yet unlocked
- Spec published to the appropriate `docs/specs/` location and cross-referenced from `design_system.md`
