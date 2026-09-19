**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-19
**Window:** IW-20260919-01

# Idea Intake Summary — IW-20260919-01

## Window Status: Closed

Opened: 2026-09-19T09:03:01Z
Closed: 2026-09-19T09:11:36Z

*(Timestamps are the real filesystem times of the run manifest's creation — intake invoked immediately after — and of the window artefacts' write; an earlier draft carried estimated times that post-dated the real clock and were corrected.)*

Invoked inline as STEP -1.6 of `run roadmap --reason "scheduled"` (`2026-09-19__scheduled`) — the register held 0 rows with `Status: Submitted`/`Parked-cycle-<n>` (below the 20-item threshold; only 1 `Rejected` row present, not eligible for resubmission). Mode: `standard`.

**Stale-idea horizon check (STEP -0.5):** 0 rows at `Parked-cycle-2` — no advisory.

**Backlog scope overlap check (§2.0 step 5, mandatory):** performed as a scripted keyword scan of `claude/backlog/backlog.md` (172 active items) and `claude/backlog/backlog_archive.md` for every candidate topic, across three passes (~65 candidate topics). **Candidates dropped for genuine overlap (11):** per-AI-endpoint kill switch (BLG-GOV-221/234), error-code catalog (BLG-BE-69), soft/hard delete policy (BLG-GOV-252), role-charter staleness (BLG-GOV-144/182/199), broker P&L reconciliation (BLG-QA-122, BLG-FR-02), UK tax-year handling (BLG-FR-03 and 26 more), monthly budget alert (BLG-OPS-89), Render cold-start monitor, Render log retention (BLG-OPS-31/53), sustainable-pace/capacity-band (BLG-GOV-328), Arc 5 gate-progress indicator (BLG-SPEC-73 — already exists). **Candidates dropped because the UI already has the feature:** days-held column, earnings-days column, sector heat map. **Candidates kept with a stated refinement of an existing item (7):** IDEA-ai-compliance-20260919-01, IDEA-cybersecurity-20260919-01, IDEA-head-of-specs-20260919-02, IDEA-infra-ops-20260919-01, IDEA-strategy-owner-20260919-02, IDEA-api-contracts-20260919-02, IDEA-director-of-hr-20260919-01 — each notes the related BLG-ID and the new angle. Estimated undetected-overlap rate is therefore expected to be well below the 52% observed at `2026-07-27__scheduled`.

**Method note:** each agent perspective was exercised by the engine per §2.1 (the same convention every prior window used); submissions are engine-generated under agent perspectives, not independent human input. Full template fields (problem / strategy § / expected value / effort / reversibility / stop / recommendation / overlap result) are recorded per idea in `cycle_record.md` `## STEP 4 — Ideas`, following the precedent that the register carries titles and the cycle record carries the field detail.

## Submission Counts

| Agent | New Submissions | Parked Resubmitted | Total |
|-------|-----------------|--------------------|-------|
| AI Compliance & Governance Officer | 2 | 0 | 2 |
| API Contracts & Documentation Owner | 2 | 0 | 2 |
| Backend Engineering Patterns Owner | 2 | 0 | 2 |
| Base44 Frontend Prompt Owner | 2 | 0 | 2 |
| Challenger | 2 | 0 | 2 |
| Cybersecurity & Trust Lead | 2 | 0 | 2 |
| Data Model & Domain Schema Owner | 2 | 0 | 2 |
| Director of HR | 2 | 0 | 2 |
| Director of Quality | 2 | 0 | 2 |
| Financial Reporting & Records Owner | 2 | 0 | 2 |
| FinOps & Resource Architect | 2 | 0 | 2 |
| Frontend Specifications & UX Documentation Owner | 2 | 0 | 2 |
| Head of Engineering | 2 | 0 | 2 |
| Head of Specs Team | 2 | 0 | 2 |
| Head of UX & Design | 2 | 0 | 2 |
| Infrastructure & Operations Owner | 2 | 0 | 2 |
| Metrics Definitions & Analytics Canonical Owner | 2 | 0 | 2 |
| PMO Lead | 2 | 0 | 2 |
| Product Owner | 2 | 0 | 2 |
| QA Lead | 2 | 0 | 2 |
| QA & Testing Owner | 2 | 0 | 2 |
| Strategy Rules & System Intent Owner | 2 | 0 | 2 |
| **Total** | **44** | **0** | **44** |

## Agents Without Minimum Submissions

None — all 22 eligible agents met the 2-net-new minimum. (Facilitator excluded by design.)

## Ideas Available for Roadmap STEP 4

All 44 submissions below are `Submitted` and available to the roadmap engine's STEP 4. Classification (Advance / Park / Backlog / Reject) is performed there, not here — see `claude/ideas/ideas_register.md` (window `IW-20260919-01`). The Recommendation column is the submitter's own view.

| Idea ID | Agent | Title | Recommendation | Status |
|---------|-------|-------|----------------|--------|
| IDEA-ai-compliance-20260919-01 | AI Compliance & Governance Officer | Golden-fixture CI regression for AI prompt templates: replay fixed prompts and assert no advisory-to-predictive phrase drift at te… | Advance | Submitted |
| IDEA-ai-compliance-20260919-02 | AI Compliance & Governance Officer | Stamp model ID and prompt-template version onto every claude_audit_log row so a boundary-language finding traces to the exact temp… | Advance | Submitted |
| IDEA-api-contracts-20260919-01 | API Contracts & Documentation Owner | Document idempotency and double-submit behaviour for each mutating endpoint (POST /trades, /trade-plans, position entry) as a cont… | Advance | Submitted |
| IDEA-api-contracts-20260919-02 | API Contracts & Documentation Owner | Add 4xx/5xx error-payload examples to the contracts of the 10 most-called endpoints and extend the example-freshness checker to co… | Advance | Submitted |
| IDEA-backend-engineering-20260919-01 | Backend Engineering Patterns Owner | Audit float-vs-Decimal money arithmetic in sizing, FX conversion and P&L paths and pin rounding boundaries with golden tests | Advance | Submitted |
| IDEA-backend-engineering-20260919-02 | Backend Engineering Patterns Owner | One shared upstream-call helper enforcing a uniform timeout and bounded retry budget for yfinance, Alpaca and Anthropic clients | Advance | Submitted |
| IDEA-base44-frontend-20260919-01 | Base44 Frontend Prompt Owner | Lint rendered UI copy strings in CI for forbidden predictive or advice-crossing phrases, independent of the AI-endpoint audit | Advance | Submitted |
| IDEA-base44-frontend-20260919-02 | Base44 Frontend Prompt Owner | Bake accessible-name and heading-order rules into the Base44 prompt template so regenerated pages stop reintroducing the BLG-FE-17… | Advance | Submitted |
| IDEA-challenger-20260919-01 | Challenger | Challenge: PVR's 'D' bucket is 110 of 174 stories — split debt into user-protective (bug/security/data-integrity) vs pure hygiene,… | Advance | Submitted |
| IDEA-challenger-20260919-02 | Challenger | Challenge: after 3 Alert readings the Skill-Silo/PVR pull-forward clauses cannot be satisfied — replace the lagging shipped-ratio … | Advance | Submitted |
| IDEA-cybersecurity-20260919-01 | Cybersecurity & Trust Lead | Read-only production credential scoped to aggregate gate-check views for governed routines — env-injected, never committed | Advance | Submitted |
| IDEA-cybersecurity-20260919-02 | Cybersecurity & Trust Lead | CI guard rejecting non-registry dependency specifiers (git+ssh, git+https, file:) in package.json and requirements | Advance | Submitted |
| IDEA-data-model-20260919-01 | Data Model & Domain Schema Owner | Read-only live-schema vs data_model.md drift detector that lists undocumented and missing columns, indexes and constraints | Advance | Submitted |
| IDEA-data-model-20260919-02 | Data Model & Domain Schema Owner | Column provenance annotations in data_model.md (user-entered / derived / system-stamped) so analytics know which fields are safe t… | Advance | Submitted |
| IDEA-director-of-hr-20260919-01 | Director of HR | Persist STEP 7.2 role-share tallies as a structured history file so ceiling checks read a table instead of re-parsing sprint_backl… | Advance | Submitted |
| IDEA-director-of-hr-20260919-02 | Director of HR | Sign-off single-point-of-failure matrix: per governance gate, which roles can sign, flagging gates where one agent-mediated role i… | Advance | Submitted |
| IDEA-director-of-quality-20260919-01 | Director of Quality | Escaped-defect tracker: defects first observed after merge, per cycle, linked to the originating story | Advance | Submitted |
| IDEA-director-of-quality-20260919-02 | Director of Quality | DoQ checklist addendum for AI-touching stories: record prompt-template version and a boundary-language sample in the evidence file | Advance | Submitted |
| IDEA-financial-reporting-20260919-01 | Financial Reporting & Records Owner | Surface closed trades with NULL fees_paid in Monthly P&L as a 'fees not recorded' count | Advance | Submitted |
| IDEA-financial-reporting-20260919-02 | Financial Reporting & Records Owner | Month-end immutable snapshot of Monthly P&L and the tax-year table, with a restatement diff when later edits change a reviewed mon… | Advance | Submitted |
| IDEA-finops-20260919-01 | FinOps & Resource Architect | Track CI minutes and artifact-storage consumption per workflow (Playwright shards were raised 4→8 in v9.3) | Advance | Submitted |
| IDEA-finops-20260919-02 | FinOps & Resource Architect | Review GitHub Actions cache and artifact retention-days settings across workflows and set explicit limits | Advance | Submitted |
| IDEA-frontend-specs-20260919-01 | Frontend Specifications & UX Documentation Owner | Responsive-table spec: how Positions, TradeHistory and TradePlans degrade below 768px (column priority, scroll vs card) | Advance | Submitted |
| IDEA-frontend-specs-20260919-02 | Frontend Specifications & UX Documentation Owner | Canonical keyboard-shortcut inventory spec covering every shortcut, conflicts and discoverability | Advance | Submitted |
| IDEA-head-of-engineering-20260919-01 | Head of Engineering | 'Clone as new plan' action on the Trade Plans list | Advance | Submitted |
| IDEA-head-of-engineering-20260919-02 | Head of Engineering | CSV export for Screener results and Watchlist | Advance | Submitted |
| IDEA-head-of-specs-20260919-01 | Head of Specs Team | JSON Schema for .claude_current_state.json and add the last_updated_utc field the roadmap engine reads | Advance | Submitted |
| IDEA-head-of-specs-20260919-02 | Head of Specs Team | Split roadmap_prompt.md into core plus appendix — it is now 957 lines (~34k tokens) and exceeds a single read | Advance | Submitted |
| IDEA-head-of-ux-20260919-01 | Head of UX & Design | Every empty state names one primary next action (for example 'Run the screener') with a link | Advance | Submitted |
| IDEA-head-of-ux-20260919-02 | Head of UX & Design | Single number/currency formatting helper and audit across tables (symbol, decimals, negative style) | Advance | Submitted |
| IDEA-infra-ops-20260919-01 | Infrastructure & Operations Owner | Dead-man's-switch alert when nightly-stop-update has not succeeded within 26 hours | Advance | Submitted |
| IDEA-infra-ops-20260919-02 | Infrastructure & Operations Owner | External-dependency failure-mode matrix (yfinance, Alpaca, Anthropic, Supabase, Render) with degradation and manual fallback | Advance | Submitted |
| IDEA-metrics-20260919-01 | Metrics Definitions & Analytics Canonical Owner | Report an effort-weighted PVR (U days over total days) alongside the story-count PVR | Advance | Submitted |
| IDEA-metrics-20260919-02 | Metrics Definitions & Analytics Canonical Owner | Lead-time metric: backlog item filed to shipped, by priority band | Advance | Submitted |
| IDEA-pmo-lead-20260919-01 | PMO Lead | Ready-pool runway forecast: cycles until empty given intake and capacity | Advance | Submitted |
| IDEA-pmo-lead-20260919-02 | PMO Lead | Follow-on ratio: items filed during execution per shipped story, tracked per cycle | Advance | Submitted |
| IDEA-product-owner-20260919-01 | Product Owner | Nudge the operator to complete TradeReflection within 48 hours of a trade closing | Advance | Submitted |
| IDEA-product-owner-20260919-02 | Product Owner | Flag trade plans in 'planned' status older than a configurable number of days as stale on the Trade Plans list | Advance | Submitted |
| IDEA-qa-lead-20260919-01 | QA Lead | Mutation-testing pilot on the sizing calculator and stop ratchet | Advance | Submitted |
| IDEA-qa-lead-20260919-02 | QA Lead | Strategy-rule to test traceability matrix mapping each §4–§8 normative clause to its asserting test | Advance | Submitted |
| IDEA-qa-testing-20260919-01 | QA & Testing Owner | Property-based tests (hypothesis) for 'stop never decreases' and sizing validity rules | Advance | Submitted |
| IDEA-qa-testing-20260919-02 | QA & Testing Owner | Retain Playwright traces and screenshots on CI failure for 14 days with a triage note | Advance | Submitted |
| IDEA-strategy-owner-20260919-01 | Strategy Rules & System Intent Owner | Run the §13 determinism pre-clearance for PO-05 Replay Mode as a standalone review, decoupled from the very-high-effort build | Advance | Submitted |
| IDEA-strategy-owner-20260919-02 | Strategy Rules & System Intent Owner | Parameter-change ledger for §11 production parameters (date, justification, link per change) | Advance | Submitted |

## Parked Ideas Carried Forward (Not Resubmitted)

None — register held no `Parked-cycle-<n>` rows.

## Notes

- Effort mix: 36 Small, 8 Medium, 0 Large — small-grained by design. Rough sizing (Small ≈ 0.5d, Medium ≈ 1.5–2d): the 44 ideas total ~30–34 estimated days if all were promoted, on top of a current ready pool of ~20–28 days (against a 24–28 day release band) — i.e. promoting all 44 would take the pool to ~50–62 days, so promotion volume is a STEP 7.3 input, not a foregone conclusion.
- Two ideas (`IDEA-head-of-engineering-20260919-01`, `-02`) are ungated, user-facing build-and-ship candidates; `IDEA-product-owner-20260919-01`/`-02` and `IDEA-head-of-ux-20260919-01`/`-02` are also user-visible. Together with `IDEA-strategy-owner-20260919-01` (which could unblock the P1 `BLG-FEAT-74`), these are the window's contribution to the Skill-Silo/PVR pull-forward problem — see `cycle_record.md` STEP 7.1.
- Two submissions are explicitly challenges (`IDEA-challenger-20260919-01`/`-02`) on the PVR and Skill-Silo mechanisms themselves.
