**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-11-18
**Window:** IW-20261118-01

# Idea Intake Summary — IW-20261118-01

## Window Status: Closed

Opened: 2026-11-18T08:12:40Z
Closed: 2026-11-18T08:13:09Z

*(Real shell timestamps: open = creation of `ideas_window.json`; close = this file's write. The surface reads and overlap greps behind the submissions ran before the window file was created, between 08:04 and 08:12 UTC.)*

Invoked inline as STEP -1.6 of `run roadmap --reason "scheduled"` (`2026-11-18__scheduled`). The register held 0 rows with `Status: Submitted`/`Parked-cycle-<n>`, below the 20-item threshold. No standalone window ran beforehand, so the standalone pre-run exception does not apply. Mode: `standard`.

**Full roster.** All 22 eligible roles were opened. `idea_intake_prompt.md` §4.1 condition 3 requires this: the preceding window `IW-20261103-01` was reduced-roster. `eligible_agents` was built per STEP 0 (BLG-GOV-407): `_role_charter_template.md`, `facilitator.md` and `README.md` (no `**Role:**` line) were skipped, leaving 22 roles that match §4's list exactly. The §2.1 step 2a build-and-ship requirement applies to the 5 user-facing roles.

**Stale-idea horizon check (STEP -0.5):** 0 rows at `Parked-cycle-2`, so no advisory.

**Parked queue pre-check (§2.0 steps 1–4):** no `Parked-cycle-<n>` rows exist, so there was nothing to resubmit.

**Backlog scope overlap check (§2.0 step 5):** every topic was grepped against `claude/backlog/backlog.md` (340 active items) and `backlog_archive.md` before it was finalised. Dropped for overlap: `robots.txt`/`noindex` (covered by `BLG-SEC-46`), toast-system and `moment` duplication (`BLG-FE-315`, `BLG-TECH-31`), heading entrance fades (`BLG-FE-317`, `BLG-FE-314`), "where your data goes" disclosure for AI panels (`BLG-UX-18`), screener-to-trade funnel (`BLG-FEAT-92`; the loop idea below is kept for its in-week, already-recorded data angle), Vite migration (`BLG-TECH-21`).

**Codebase overlap check (§2.0 step 6):** mechanism-naming topics were checked in `backend/`, `src/`, `.github/workflows/`, `scripts/` and `public/`. Dropped as already implemented: a backup restore drill (`production-db-backup.yml` job `restore_dry_run`), an API uptime alert (`health-check-alert.yml`), a Content-Security-Policy (present). Confirmed absent: any React error boundary (`componentDidCatch`/`getDerivedStateFromError`: 0 hits in `src/`); any stock-split handling (no `splits` use in `backend/`); any `Cache-Control` header (0 hits); any front-end availability poll (`health-check-alert.yml` polls only `${API_URL}/health`); `tabular-nums` on Positions (0 of 14 uses are in `src/pages/Positions.js`); 112 `bg-gradient-to` uses across 54 files (cards are covered by `BLG-FE-304`; buttons are not).

**Inputs this window responds to:** `docs/governance/governance_overhead_audit_2026-11-02.md` (its three questions: ceremony capacity, combined records, batched prompt edits) and `docs/ux/site_structure_rereview_2026-11-17.md` §14–§15 (items it named as unfiled: core-loop measurement, the two §14.2 navigation moves, the §14.5 design direction).

**Method note:** the engine exercised each agent perspective per §2.1, the same convention every prior window used. Submissions are engine-generated under agent perspectives, not independent human input. Full template fields for each idea are recorded in `claude/cycles/2026-11-18__scheduled/cycle_record.md` § "Submission Details".

## Submission Counts

| Agent | New Submissions | Parked Resubmitted | Total |
|-------|-----------------|--------------------|-------|
| AI Compliance & Governance Officer | 1 | 0 | 1 |
| API Contracts & Documentation Owner | 1 | 0 | 1 |
| Backend Engineering Patterns Owner | 1 | 0 | 1 |
| Base44 Frontend Prompt Owner | 1 | 0 | 1 |
| Challenger | 2 | 0 | 2 |
| Cybersecurity & Trust Lead | 1 | 0 | 1 |
| Data Model & Domain Schema Owner | 2 | 0 | 2 |
| Director of HR | 1 | 0 | 1 |
| Director of Quality | 1 | 0 | 1 |
| Financial Reporting & Records Owner | 2 | 0 | 2 |
| FinOps & Resource Architect | 1 | 0 | 1 |
| Frontend Specifications & UX Documentation Owner | 2 | 0 | 2 |
| Head of Engineering | 1 | 0 | 1 |
| Head of Specs Team | 1 | 0 | 1 |
| Head of UX & Design | 1 | 0 | 1 |
| Infrastructure & Operations Owner | 1 | 0 | 1 |
| Metrics Definitions & Analytics Owner | 1 | 0 | 1 |
| PMO Lead | 1 | 0 | 1 |
| Product Owner | 1 | 0 | 1 |
| QA Lead | 2 | 0 | 2 |
| QA & Testing Owner | 1 | 0 | 1 |
| Strategy Rules & System Intent Owner | 1 | 0 | 1 |
| **Total** | **27** | **0** | **27** |

## Agents Without Minimum Submissions

17 roles submitted 1 net-new idea instead of 2; 5 roles (Challenger, Data Model & Domain Schema Owner, Financial Reporting & Records Owner, Frontend Specifications & UX Documentation Owner, QA Lead) met the minimum. Each recorded that no further net-new idea survived the §2.0 overlap checks, as §10 permits in place of a padded submission. Standard mode, so this is noted and not a halt:

- AI Compliance & Governance Officer: 1 — "where your data goes" disclosure dropped for overlap with `BLG-UX-18`.
- API Contracts & Documentation Owner: 1 — a shared error schema dropped (`ApiError` already in `openapi.yaml` components).
- Backend Engineering Patterns Owner: 1 — no further net-new idea.
- Base44 Frontend Prompt Owner: 1 — no further net-new idea.
- Cybersecurity & Trust Lead: 1 — `robots.txt`/`noindex` dropped for overlap with `BLG-SEC-46`; CSP dropped as implemented.
- Director of HR: 1 — no further net-new idea.
- Director of Quality: 1 — no further net-new idea.
- FinOps & Resource Architect: 1 — no further net-new idea.
- Head of Engineering: 1 — duplicate-library removal dropped for overlap with `BLG-FE-315`.
- Head of Specs Team: 1 — "generate routine records by script" merged into the PMO Lead's submission (same records).
- Head of UX & Design: 1 — heading entrance fades dropped for overlap with `BLG-FE-317`/`BLG-FE-314`.
- Infrastructure & Operations Owner: 1 — backup restore drill dropped as implemented (`restore_dry_run`).
- Metrics Definitions & Analytics Owner: 1 — no further net-new idea.
- PMO Lead: 1 — no further net-new idea.
- Product Owner: 1 — product name and purpose dropped for overlap with `BLG-UX-16`.
- QA & Testing Owner: 1 — no further net-new idea.
- Strategy Rules & System Intent Owner: 1 — no further net-new idea.

## Ideas Available for Roadmap STEP 4

All 27 submissions were `Submitted` at window close. Classification happens at roadmap STEP 4 (see `ideas_register.md`).

| Idea ID | Agent | Title | Recommendation | Status |
|---------|-------|-------|----------------|--------|
| IDEA-ai-compliance-20261118-01 | AI Compliance & Governance Officer | Bring the AI feature usage review (BLG-GOV-382) forward to v9.18 | Now | Submitted |
| IDEA-api-contracts-20261118-01 | API Contracts & Documentation Owner | Declare `Cache-Control: no-store` on every API response that carries portfolio data | Soon | Submitted |
| IDEA-backend-engineering-20261118-01 | Backend Engineering Patterns Owner | Detect a stock split on an open position before the split-day price reads as a stop breach | Soon | Submitted |
| IDEA-base44-frontend-20261118-01 | Base44 Frontend Prompt Owner | Replace the decorative gradient buttons with one solid primary button | Soon | Submitted |
| IDEA-challenger-20261118-01 | Challenger | Challenge: measure whether the core loop is used before committing a second UX programme | Now | Submitted |
| IDEA-challenger-20261118-02 | Challenger | Challenge: 12 Arc 5 items have been P1 since 2026-07-28 while gated on data that has not moved | Soon | Submitted |
| IDEA-cybersecurity-20261118-01 | Cybersecurity & Trust Lead | Portfolio and trade responses can be cached by the browser: send no-store | Soon | Submitted |
| IDEA-data-model-20261118-01 | Data Model & Domain Schema Owner | Record a stock split as an adjustment row against the position | Soon | Submitted |
| IDEA-data-model-20261118-02 | Data Model & Domain Schema Owner | Store the core-loop events the existing tables cannot derive | Soon | Submitted |
| IDEA-director-of-hr-20261118-01 | Director of HR | Reserve explicit sprint capacity for per-story ceremony | Soon | Submitted |
| IDEA-director-of-quality-20261118-01 | Director of Quality | Track escaped defects per release as a quality trend | Later | Submitted |
| IDEA-financial-reporting-20261118-01 | Financial Reporting & Records Owner | Record dividends received on held positions | Later | Submitted |
| IDEA-financial-reporting-20261118-02 | Financial Reporting & Records Owner | Download all records in one file | Soon | Submitted |
| IDEA-finops-20261118-01 | FinOps & Resource Architect | Count process-only commits per release alongside velocity | Soon | Submitted |
| IDEA-frontend-specs-20261118-01 | Frontend Specifications & UX Documentation Owner | Use tabular numerals for every price, P&L, R and % figure | Soon | Submitted |
| IDEA-frontend-specs-20261118-02 | Frontend Specifications & UX Documentation Owner | Move Ticker Universe into Settings | Soon | Submitted |
| IDEA-head-of-engineering-20261118-01 | Head of Engineering | Add page-level error boundaries | Soon | Submitted |
| IDEA-head-of-specs-20261118-01 | Head of Specs Team | Apply non-urgent prompt patches in one batch at post-ship closure | Soon | Submitted |
| IDEA-head-of-ux-20261118-01 | Head of UX & Design | Make Strategy Benchmark a "Strategy vs backtest" section of Performance | Soon | Submitted |
| IDEA-infra-ops-20261118-01 | Infrastructure & Operations Owner | Poll the GitHub Pages front end as well as the API | Soon | Submitted |
| IDEA-metrics-20261118-01 | Metrics Definitions & Analytics Owner | Define the core-loop step metrics | Soon | Submitted |
| IDEA-pmo-lead-20261118-01 | PMO Lead | Write each story's routine records in one commit | Soon | Submitted |
| IDEA-product-owner-20261118-01 | Product Owner | Show this week's loop on the Weekly Digest | Now | Submitted |
| IDEA-qa-lead-20261118-01 | QA Lead | Automated 320 px reflow check on every route | Soon | Submitted |
| IDEA-qa-lead-20261118-02 | QA Lead | Run the Telegram-link → Dashboard journey on a mobile profile in CI | Soon | Submitted |
| IDEA-qa-testing-20261118-01 | QA & Testing Owner | Test that a split-day price does not raise a stop breach | Soon | Submitted |
| IDEA-strategy-owner-20261118-01 | Strategy Rules & System Intent Owner | Define how a stock split adjusts entry, stop, ATR and R | Soon | Submitted |

## Parked Ideas Carried Forward (Not Resubmitted)

None — no parked rows existed.

## Notes

Build-and-ship candidates (§2.1 step 2a): 6 — `IDEA-product-owner-20261118-01` (Product Owner; surface `src/pages/WeeklyDigest.js`), `IDEA-head-of-ux-20261118-01` (Head of UX & Design; `src/pages/StrategyBenchmark.js`), `IDEA-head-of-engineering-20261118-01` (Head of Engineering; `src/App.js` route tree), `IDEA-frontend-specs-20261118-01` and `-02` (Frontend Specifications & UX Documentation Owner; `src/pages/Positions.js`, `src/pages/TickerUniverse.js`), `IDEA-base44-frontend-20261118-01` (Base44 Frontend Prompt Owner; `src/pages/TradeEntry.js`). User-facing roles with none: None. Two (the §14.2 moves) depend on `BLG-UX-21`'s `navigation.md` revision, a sibling decision taken at this same rebalance.

Three clusters converge and STEP 4 may consolidate them: stock splits (Backend, Data Model, QA & Testing, Strategy Owner), core-loop measurement (Product Owner, Data Model, Metrics, Challenger), and `Cache-Control` (API Contracts, Cybersecurity).
