# Sprint Backlog — 2026-08-07__release-v8.4

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-08-07
**Cycle:** 2026-08-07__release-v8.4
**Release:** v8.4
**Sprint Goal:** Ship both available user-facing reporting enhancements (Monthly P&L average-per-trade column; tax-year CSV trigger-source column) while clearing a full-capacity slate of API contract & spec debt, backend hardening, frontend code health & security, operational reliability & cost monitoring, QA/test infrastructure, and governance-process integrity work across all 31 scoped stories.
**Backlog Slice Source:** Original `claude/cycles/2026-08-07__release-v8.4/stage4_backlog_slice.md`

## Merge Order

- **EPIC merge sequence:** EPIC-02 → EPIC-03 → EPIC-01 → EPIC-04 → EPIC-05 → EPIC-06 → EPIC-07
- **`execution_state.json` owner:** EPIC-02
- **Shared files:** `data_model.md` (EPIC-02 owns canonical version; EPIC-03 rebases onto `main` after EPIC-02 merges — this is also the assigned exercise case for EPIC-07/ST-30's cross-EPIC merge runbook dry-run, apply `CLAUDE.md §8` including step 2a); `openapi.yaml` (EPIC-02 only, no cross-EPIC conflict expected); `execution_state.json` (all EPICs, standard append handling, EPIC-02 owns).

Full rationale: `sprint_planning_notes.md ## Multi-EPIC Execution Notes`.

---

## Sprint Scope

### EPIC-01 — User-Facing Reporting Enhancement

**Maps to:** S2-01
**Owner:** Financial Reporting & Records Owner
**Estimated effort:** 1.00 days
**Risk IDs:** RISK-05
**Execution sequence:** 3

#### ST-01 — Add Avg P&L/Trade column to Monthly P&L Report table

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** 0.25 days (XS)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Notes:** Observable UI change (new column). Frontend-visible-change rule applies — Playwright coverage or recorded staging sign-off required before merge; CI-verifiable via Playwright, not staging-only.

**Staging-only ACs:** None — all ACs are Playwright-coverable in CI.

---

#### ST-31 — Trade-tag/trigger-source column on tax-year P&L CSV export

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** 0.75 days (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-31`

**Dependencies:** None. Gate condition (`BLG-FE-116` ships) confirmed met at release planning (shipped v7.5, retired 2026-07-20).

**Notes:** Numbered out of sequence (late addition found via self-caught gate correction). CSV content only — not a UI-observable change; no Playwright/staging requirement.

**Staging-only ACs:** None.

---

### EPIC-02 — API Contract & Spec Debt Closure

**Maps to:** S2-02
**Owner:** API Contracts & Documentation Owner; Data Model & Domain Schema Owner
**Estimated effort:** 7.50 days
**Risk IDs:** RISK-01
**Execution sequence:** 1

#### ST-02 — Fix openapi.yaml structural defect: ~23 endpoints nested inside `components:` instead of `paths:`

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 1.75 days (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None — sequenced first within EPIC-02 (foundational for ST-03–ST-09 and cross-EPIC for EPIC-05/ST-20).

**Notes:** RISK-01 (High) — mitigated by objective, automated checks (paths-count cross-check, OpenAPI Drift Detection CI gate). Sequence first in EPIC-02 and across the sprint per `release_plan.md`.

**Staging-only ACs:** None — all ACs are CI-verifiable (yaml parse check, CI gate).

---

#### ST-03 — settings_endpoints.md GET /settings example missing created_at/updated_at

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 0.25 days (XS)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None (may proceed in parallel with ST-02; sequencing note is a recommendation, not a hard block for this item)

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-04 — position_endpoints.md GET /positions example missing 5 live fields

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 0.75 days (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** Cross-check against `position_service.py` live dict required.

**Staging-only ACs:** None — cross-check is a source-code read, CI-verifiable.

---

#### ST-05 — health_endpoints.md GET /health example missing external_apis/ai_journal

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 0.75 days (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-06 — watchlist_endpoints.md GET /watchlist illustrative example is stale

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 0.75 days (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** Field table/version history already correct per the 2026-08-06 correction note — do not re-touch.

**Staging-only ACs:** None.

---

#### ST-07 — OpenAPI security-scheme & auth-header documentation completeness check

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 0.75 days (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None (audits the corrected `openapi.yaml`; benefits from running after ST-02 but not a hard dependency — audit scope is auth-header completeness, not paths structure)

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-08 — Backfill missing data_model.md sections for 4 undocumented tables

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** 0.75 days (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None. Shared-file note: touches `data_model.md` — see Merge Order shared-files table.

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-09 — Formal schema-versioning doc for trade_plan/position tables

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** 1.75 days (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None. Shared-file note: touches `data_model.md` — see Merge Order shared-files table.

**Notes:** None.

**Staging-only ACs:** None.

---

### EPIC-03 — Backend Engineering Hardening

**Maps to:** S2-03
**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner; AI Compliance & Governance Officer
**Estimated effort:** 5.75 days
**Risk IDs:** RISK-03
**Execution sequence:** 2 (runs in parallel with EPIC-02 — see Merge Order / `sprint_planning_notes.md`)

#### ST-10 — Add functional index on trade_plans(UPPER(ticker))

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 0.75 days (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None. Shared-file note: touches `data_model.md` — see Merge Order shared-files table.

**Notes:** None.

**Staging-only ACs:** None — `EXPLAIN` check is CI-verifiable.

---

#### ST-11 — Add 429/backoff handling to Alpaca paper-sync close/positions endpoints

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 0.75 days (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** `BLG-BE-80` — shipped v8.3, no in-cycle dependency.

**Notes:** Regression test confirms retry-before-fallback for both call sites; CI-mockable, not staging-only.

**Staging-only ACs:** None.

---

#### ST-12 — Log AI model+version provenance on stored thesis/summary text

**Owner:** Backend Engineering Patterns Owner (AI Compliance & Governance Officer sign-off)
**Estimated effort:** 0.75 days (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** No local model/prompt-drift integrity issue (confirmed at release planning STEP 3.5) — adds a metadata field on write only.

**Staging-only ACs:** None.

---

#### ST-13 — Mutation/audit-trail log for trade plan edits post-entry

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 1.75 days (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None. Extends the `BLG-BE-73` pattern (already shipped). Shared-file note: touches `data_model.md` — see Merge Order shared-files table.

**Notes:** RISK-03 (Low) — scope-creep risk mitigated by narrow AC (extend existing pattern only).

**Staging-only ACs:** None.

---

#### ST-14 — Auto-generated data dictionary from live schema

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** 1.75 days (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None. Shared-file note: touches `data_model.md` (diff triage target) — see Merge Order shared-files table.

**Notes:** RISK-03 (Low) — narrow AC (generate-and-triage, not generate-and-reconcile).

**Staging-only ACs:** None — script runs against live schema in CI/dev environment, output triage is a code-review step, not a staging-only evidence requirement.

---

### EPIC-04 — Frontend Code Health, Accessibility & Security

**Maps to:** S2-04
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner; Cybersecurity & Trust Lead
**Estimated effort:** 5.00 days
**Risk IDs:** RISK-02
**Execution sequence:** 4

#### ST-15 — Audit Dialog/DialogTitle className-override sites for the cn()-has-no-tailwind-merge defect class

**Owner:** Head of Engineering
**Estimated effort:** 0.75 days (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** Observable-UI rule applies (no visual regression in any fixed component) — Playwright coverage or staging sign-off required; CI-verifiable via Playwright, not staging-only.

**Staging-only ACs:** None.

---

#### ST-16 — Close remaining dark-only-token gaps in inline form-validation error text

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.75 days (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** Design Gate pass — resolved (`design_gate_status = Passed`).

**Notes:** Colour-token change across 6 named components + fresh full-repo grep. Observable-UI rule applies; CI-verifiable via Playwright, not staging-only.

**Staging-only ACs:** None.

---

#### ST-17 — WatchlistModal.js fails ESLint (24 problems) — same patterns fixed in Watchlist.js

**Owner:** Head of Engineering
**Estimated effort:** 1.75 days (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None

**Notes:** No functional or visual behaviour change — lint-only fix, CI-verifiable (`npx eslint` exit code).

**Staging-only ACs:** None.

---

#### ST-18 — CSP allows 'unsafe-inline' for script-src and style-src

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 1.75 days (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** RISK-02 (Medium) — mitigated by full inline-usage audit and functional-regression confirmation required in the AC itself before merge; narrow, documented exception permitted if full removal isn't feasible.

**Staging-only ACs:** None — "app loads and renders correctly" is verifiable via a CI-run Playwright smoke/load check against the tightened CSP; no live external dependency.

---

### EPIC-05 — Operational Reliability & Cost Monitoring

**Maps to:** S2-05
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Estimated effort:** 3.50 days
**Risk IDs:** RISK-06
**Execution sequence:** 5

#### ST-19 — Staging verification required for SI-05 weekly digest fix

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.25 days (XS)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** `BLG-OPS-129` — shipped v8.3, no in-cycle dependency.

**Notes:** Requires a live staging digest send and confirmation via `si05_digest_log` and a real Telegram message — CI cannot reproduce this. Do not begin until EPIC-05 opens in execution sequence.

**Staging-only ACs:** "At least one successful SI-05 digest send observed post-fix, confirmed via `si05_digest_log` and a live Telegram message" — `[staging-only evidence]`.

---

#### ST-20 — Endpoint coverage drift: 19 endpoints missing from api_performance_baseline.md

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.75 days (S)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** EPIC-02/ST-02 (endpoint list must be re-verified against the corrected `openapi.yaml` first). Do not begin until EPIC-02 has merged to `main`.

**Notes:** RISK-06 (Low) — requires live staging access and ≥5 samples per endpoint (19 endpoints); larger execution-time cost than the S-effort band alone suggests, per release plan.

**Staging-only ACs:** "Measurement conducted with ≥5 staging samples per endpoint" — `[staging-only evidence]`.

---

#### ST-21 — Add POST /digest/si05/send to api_performance_baseline.md

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.25 days (XS)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None

**Notes:** Render internal log-based measurement — standard external HTTP timing does not apply; methodology note required in the same PR.

**Staging-only ACs:** "Render internal log-based measurements recorded" — `[staging-only evidence]` (deploy-environment log access, CI cannot reproduce).

---

#### ST-22 — CI runner cache warm-up for backend/.venv to cut pytest job time

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.75 days (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** None

**Notes:** Measured CI job time reduction is observable directly from GitHub Actions run history — CI-verifiable, not staging-only.

**Staging-only ACs:** None.

---

#### ST-23 — Database storage growth cost trend tracking (Postgres/Supabase)

**Owner:** FinOps & Resource Architect
**Estimated effort:** 0.75 days (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-24 — AI API cost model for Arc 4 journal intelligence features

**Owner:** FinOps & Resource Architect
**Estimated effort:** 0.75 days (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`

**Dependencies:** None

**Notes:** Documentation deliverable — no code or staging dependency.

**Staging-only ACs:** None.

---

### EPIC-06 — QA & Test Infrastructure Hardening

**Maps to:** S2-06
**Owner:** QA & Testing Owner; Director of Quality; Financial Reporting & Records Owner; Metrics Definitions & Analytics Owner
**Estimated effort:** 3.50 days
**Risk IDs:** RISK-04
**Execution sequence:** 6

#### ST-25 — Fix wrong patch target in test_get_portfolio_history_returns_ok

**Owner:** QA & Testing Owner
**Estimated effort:** 0.25 days (XS)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None — verified with no DB reachable, CI-runnable.

---

#### ST-26 — Backfill regression baseline with 24 undocumented Playwright spec files (v6.0-v7.3)

**Owner:** QA & Testing Owner (Director of Quality sign-off)
**Estimated effort:** 1.75 days (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-26`

**Dependencies:** None

**Notes:** RISK-04 (Low) — cataloguing effort larger than the M-effort band alone suggests (24 individual files); mitigated by an exact-count-match AC (mechanically verifiable).

**Staging-only ACs:** None.

---

#### ST-27 — Recurring CSV export content regression check

**Owner:** QA & Testing Owner (Financial Reporting & Records Owner input)
**Estimated effort:** 0.75 days (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-27`

**Dependencies:** None

**Notes:** First instance run is CI-executable; "findings filed" path (if triggered) is a standard backlog item, not staging evidence.

**Staging-only ACs:** None.

---

#### ST-28 — Signal correctness fix impact measurement

**Owner:** Metrics Definitions & Analytics Owner (reviewed by Product Owner)
**Estimated effort:** 0.75 days (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-28`

**Dependencies:** None

**Notes:** Informational — historical query against existing data, no remediation implied unless a material discrepancy is found.

**Staging-only ACs:** None — query runs against existing production data export, not a live staging dependency in the CI-cannot-reproduce sense; treat as a data-analysis task.

---

### EPIC-07 — Governance Process Integrity

**Maps to:** S2-07
**Owner:** Head of Specs Team; Head of Engineering
**Estimated effort:** 1.50 days
**Risk IDs:** RISK-07
**Execution sequence:** 7

#### ST-29 — Canonical, scripted gate-detection procedure for Release Planning's ungated-candidate scan

**Owner:** Head of Specs Team
**Estimated effort:** 0.75 days (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-29`

**Dependencies:** None. Standard governance file edit checklist applies (`CLAUDE.md §6`) — version bump, `OPERATIONAL_GUIDE.md §14` sync, `prompt_change_log.md` entry, all in the same commit.

**Notes:** Must cover all 4 known gate-detection failure modes, including the "missing `---` separator" mode self-caught at this cycle's own `BLG-GOV-286` scan.

**Staging-only ACs:** None.

---

#### ST-30 — Dry-run the cross-EPIC merge conflict runbook

**Owner:** Head of Engineering (PMO Lead coordination)
**Estimated effort:** 0.75 days (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-30`

**Dependencies:** Structural — requires the EPIC-02/EPIC-03 parallel-branch merge to have occurred (see Merge Order). Sequence after both branches merge.

**Notes:** RISK-07 (Low) — resolved at planning time by the explicit parallel-branch assignment (EPIC-02/EPIC-03, sharing `data_model.md`). If the assigned pair does not in practice exercise the runbook meaningfully at merge time, this item may need to carry to a sprint where a clearer parallel opportunity exists — record as a deviation, not a silent scope drop.

**Staging-only ACs:** None.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24-28 days (band, Effective 2026-07-17) |
| Total estimated effort (in-scope) | 27.75 days |
| Utilisation | ~99.1% of band ceiling (28d) / ~115.6% of band floor (24d) |
| Over-allocation | No (within band ceiling); buffer-floor advisory (>95%) — PO acknowledged, proceed at full scope (see `sprint_capacity.md §1.5`) |

## Items Deferred This Sprint

None.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Awareness: `execution_prompt.md §7` backlog write-scope escalation remains unresolved (3 consecutive cycles, carried forward from v8.3 closure) | PMO Lead | No |
| Schedule staging evidence gathering for ST-19/ST-20/ST-21 once EPIC-05 opens | Infrastructure & Operations Owner | No |

No outstanding action is marked `Blocker? Yes`.

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed (agent-mediated, delegated authority — see `sprint_goal.md`)
**Scope confirmed:** Confirmed — all 31 items from the authoritative backlog slice classified `include`, none deferred, none flagged
**Capacity confirmed:** Confirmed — within the ~24-28 day band per `sprint_capacity.md`; buffer-floor advisory (>95%) acknowledged, proceed at full scope per the explicit "use full capacity" instruction recorded at release planning
**Deferred execution blockers accepted (if any):** N/A — `deferred_execution_blockers` empty in `state.json`
**Signed off by:** Product Owner (agent-mediated, delegated authority)
**Date:** 2026-08-07
