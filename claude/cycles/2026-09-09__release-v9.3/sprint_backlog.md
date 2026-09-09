**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-09-09
**Cycle:** 2026-09-09__release-v9.3
**Release:** v9.3
**Sprint Goal:** Clear a full-capacity, cross-category slate of 27 debt items — backend reliability/correctness, QA/test infrastructure, operations/cost monitoring, spec/documentation, and governance-process/security — exhausting the confirmed ~24–28 day capacity band at 27.50 days, with zero P1/P2 debt items deferred on capacity grounds this cycle.
**Backlog Slice Source:** Original — `stage4_backlog_slice.md`

# Sprint Backlog — 2026-09-09__release-v9.3

**Merge order (5 EPICs in scope):** EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04 → EPIC-05. **`execution_state.json` owner: EPIC-01.** No shared frontend/UI spec files across EPICs this cycle (no observable UI acceptance criteria anywhere in scope). Sole cross-EPIC surface note: EPIC-04/ST-17's repo-wide `docs/specs/**` cross-reference scan — see `sprint_planning_notes.md` Multi-EPIC Execution Notes and Dependency Map for the recommended intra-EPIC re-sequencing (ST-17 last within EPIC-04).

---

## Sprint Scope

### EPIC-01 — Backend Reliability & Data Correctness Debt

**Maps to:** S2-01
**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner
**Estimated effort:** 8.00d
**Risk IDs:** RISK-01
**Execution sequence:** 1

#### ST-01 — Screener result history table

**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner
**Estimated effort:** 2.50d
**Delegation class:** autonomous — new table + endpoint, no UX change

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Notes:** Product Owner sign-off on the gate condition (screener live ≥60 days) is required per the item's own AC — confirmed cleared 2026-08-08 at release planning; no outstanding blocker.

**Staging-only ACs:** None — new table + paginated endpoint, CI-testable.

#### ST-02 — Signal write-path schema consolidation

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 2.50d
**Delegation class:** autonomous — backend refactor, no UX change

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None (precondition — `BLG-SEC-02` v6.4 sanitisation fix's 30-day production stability window — already confirmed cleared 2026-08-08, no incidents on record)

**Notes:** RISK-01 — QA sign-off requires regression coverage on all 3 consolidated write paths.

**Staging-only ACs:** None — regression coverage is CI-verifiable.

#### ST-03 — Structured logging correlation-ID propagation across FastAPI request lifecycle

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 2.50d
**Delegation class:** autonomous — middleware addition, no UX change

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** Documented in `backend_engineering_patterns.md` per AC.

**Staging-only ACs:** None — log-line assertions are CI-testable against 2 representative multi-step endpoints.

#### ST-04 — Arc5 compliance total_closed_trades conflates DB schema error with genuine zero-trades state

**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner
**Estimated effort:** 0.50d
**Delegation class:** autonomous — backend correctness fix + spec update; frontend touch (if any) matches existing rendering, no new UX decision (BLG-GOV-72 fast-path (a) equivalent)

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** Updates `docs/specs/api_contracts/arc5_compliance_analytics.md`; if the v9.2 ST-01 Arc5ComplianceSection low-trade-volume advisory rendering depends on this field, update it to match.

**Staging-only ACs:** None — null-vs-zero distinction is unit-testable.

---

### EPIC-02 — QA & Test Infrastructure Debt

**Maps to:** S2-02
**Owner:** QA Testing Owner; Director of Quality
**Estimated effort:** 5.00d
**Risk IDs:** RISK-02
**Execution sequence:** 2

#### ST-05 — Consolidate 3 overlapping SignalCard Playwright specs

**Owner:** QA Testing Owner
**Estimated effort:** 0.50d
**Delegation class:** autonomous — test consolidation, no product code change

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** Full scenario coverage must be confirmed retained before the 2 redundant spec files are removed.

**Staging-only ACs:** None — suite runtime and coverage are CI-measurable.

#### ST-06 — Contract test suite: openapi.yaml vs. actual route behaviour

**Owner:** QA Testing Owner; Director of Quality
**Estimated effort:** 2.50d
**Delegation class:** autonomous — test authoring, no product code change

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** RISK-02 — any drift found beyond the 5-endpoint sample is filed as a new `BLG-SPEC-*` item, not resolved inline.

**Staging-only ACs:** None — contract tests run in CI against the documented schema.

#### ST-07 — DoQ sign-off template freshness check

**Owner:** Director of Quality
**Estimated effort:** 0.50d
**Delegation class:** autonomous — documentation/process review

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** Any drift found is documented and, if actionable, filed as a follow-on item.

**Staging-only ACs:** None — a documentation/process review, not a runtime-behaviour AC.

#### ST-08 — Watchlist.js post-refactor visual QA

**Owner:** QA Testing Owner
**Estimated effort:** 0.50d
**Delegation class:** delegated_qa — the deliverable is the human/staging visual verification itself

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** Verifies the v6.8 ESLint refactor (`BLG-OPS-61`) introduced no rendered-behaviour regression. Record via the `record-visual-qa` skill.

**Staging-only ACs:** Visual QA pass on Watchlist.js — this story's entire deliverable is the staging run itself; not deferred post-merge, so no separate backlog filing is triggered.

#### ST-09 — Cross-browser Playwright matrix evaluation

**Owner:** QA Testing Owner
**Estimated effort:** 0.50d
**Delegation class:** autonomous — produces a recommendation document; adoption decision is for a future cycle, not a gate on this story's completion

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** Recommendation (adopt/defer, with rationale) documented for a small set of critical-path specs.

**Staging-only ACs:** None — a cost/benefit evaluation deliverable, not a runtime-behaviour AC.

#### ST-10 — Backend test suite runtime baseline

**Owner:** QA Testing Owner
**Estimated effort:** 0.50d
**Delegation class:** autonomous — runs the existing suite and records timing

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** Per CLAUDE.md §9, run via `backend/.venv/bin/python3 -m pytest`, not system Python.

**Staging-only ACs:** None — the baseline is captured from a CI or local venv pytest run, either is acceptable evidence.

---

### EPIC-03 — Operations & Cost Monitoring Debt

**Maps to:** S2-03
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Estimated effort:** 6.50d
**Risk IDs:** RISK-03
**Execution sequence:** 3

#### ST-11 — Alpaca API cost monitoring

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.50d
**Delegation class:** autonomous — backend instrumentation

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None — sequence first within EPIC-03 (RISK-03 reference instrumentation pattern for ST-12/ST-14)

**Notes:** Infrastructure & Operations Owner sign-off required per AC.

**Staging-only ACs:** None — call-count logging is CI-testable via mocked API interactions.

#### ST-12 — Research endpoint cost monitoring

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.50d
**Delegation class:** autonomous — backend instrumentation

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** ST-11 (reuses its logging approach, RISK-03) — sequence after ST-11

**Notes:** Infrastructure & Operations Owner sign-off required per AC. Anomaly threshold (>2× baseline) is a configurable constant — document its location.

**Staging-only ACs:** None — anomaly-flagging logic is CI-testable with seeded session data.

#### ST-13 — Data retention policy for AI audit log tables

**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Estimated effort:** 0.50d
**Delegation class:** autonomous — policy definition + implementation

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** Policy definition (retention window + archival/deletion procedure) is CI-verifiable via a documented policy file; the first cleanup pass itself is not.

**Staging-only ACs:** "First cleanup pass executed (if any rows exceed the window) or explicitly deferred with rationale" — requires inspecting actual row counts in the live `gemini_audit_log`/Claude audit log tables; not reproducible from a CI fixture.

#### ST-14 — Anthropic API cost per-feature attribution

**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Estimated effort:** 2.50d
**Delegation class:** autonomous — backend instrumentation

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** ST-11 (reuses its logging approach where applicable, RISK-03) — sequence after ST-11

**Notes:** Per-feature tagging (thesis generation, chat, daily briefing) — document the tag taxonomy used.

**Staging-only ACs:** None — cost-tracking tagging and the monthly breakdown are CI-testable with seeded records.

#### ST-15 — CI pipeline build-time reduction via parallelized test jobs

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 2.50d
**Delegation class:** autonomous — CI configuration change

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** Before/after wall-clock evidence must be recorded from an actual representative PR run — a CI-observable outcome, not staging-only (the evidence is the CI run itself).

**Staging-only ACs:** None — before/after timing evidence comes directly from CI run logs.

---

### EPIC-04 — Spec & Documentation Debt

**Maps to:** S2-04
**Owner:** Head of Specs Team; API Contracts & Documentation Owner
**Estimated effort:** 4.50d
**Risk IDs:** RISK-04
**Execution sequence:** 4

#### ST-16 — Spec debt dashboard

**Owner:** Head of Specs Team
**Estimated effort:** 0.50d
**Delegation class:** autonomous — documentation/tooling

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Notes:** Must be refreshable at future `groom backlog` runs per AC.

**Staging-only ACs:** None — a generated summary document, CI-reproducible.

#### ST-18 — OpenAPI response examples for Arc 5 endpoints

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** 0.50d
**Delegation class:** autonomous — documentation-only change to `openapi.yaml`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** Examples-only change — no new `## METHOD /path` heading, so CLAUDE.md's same-commit OpenAPI Drift Detection rule does not apply (no new contract introduced).

**Staging-only ACs:** None — a static documentation change.

#### ST-19 — Migration block consolidation review

**Owner:** Data Model & Domain Schema Owner; Head of Specs Team
**Estimated effort:** 0.50d
**Delegation class:** autonomous — documentation review

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None

**Notes:** Footer version must match the highest migration block after any correction.

**Staging-only ACs:** None — `data_model.md`'s own migration blocks are the CI-verifiable source of truth.

#### ST-20 — Trade tagging taxonomy documentation

**Owner:** Head of Specs Team; API Contracts & Documentation Owner
**Estimated effort:** 0.50d
**Delegation class:** autonomous — documentation

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** None

**Notes:** Taxonomy for `BLG-FEAT-52` (trade tagging) must be referenced by both UI and reporting logic — a documentation cross-reference, not new UI (no observable AC).

**Staging-only ACs:** None — a documentation deliverable.

#### ST-17 — Canonical spec cross-reference linter

**Owner:** Head of Specs Team
**Estimated effort:** 2.50d
**Delegation class:** delegated_decision — orphaned-spec triage (keep / merge / archive) requires Head of Specs Team judgment, not mechanical resolution

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** Recommended last within EPIC-04's execution order (re-sequenced from listed order — see `sprint_planning_notes.md` Dependency Map) to avoid false-orphan findings from sibling EPICs' concurrent spec changes.

**Notes:** RISK-04 — unresolved individual specs are filed as follow-on `BLG-SPEC-*` items rather than blocking this story's closure.

**Staging-only ACs:** None — the linter itself runs in CI/locally against the repo tree; only the triage decision requires a human, already captured via `delegated_decision`.

---

### EPIC-05 — Governance Process Debt & Security

**Maps to:** S2-05
**Owner:** Head of Specs Team; Cybersecurity & Trust Lead
**Estimated effort:** 3.50d
**Risk IDs:** RISK-05
**Execution sequence:** 5

#### ST-21 — Database connection pool sizing review for AI endpoints

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.50d
**Delegation class:** autonomous — technical review with documented findings

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None (gate condition — 30+ days AI endpoint usage — confirmed cleared 2026-08-08 at release planning)

**Notes:** Findings documented as "no change needed" or a specific adjustment filed as a separate item.

**Staging-only ACs:** "Current Supavisor pool configuration... reviewed against AI endpoint DB query volume" — requires reviewing live production connection-pool configuration and real query volume; not CI-testable.

#### ST-22 — Quarterly AI output sampling audit (consolidated)

**Owner:** AI Compliance & Governance Officer
**Estimated effort:** 0.50d
**Delegation class:** delegated_decision — §13.2 boundary-language compliance judgment, not mechanically verifiable

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** None

**Notes:** Any findings are filed as backlog items.

**Staging-only ACs:** None — the sampling review itself is the delegated_decision deliverable; no separate CI-unverifiable runtime AC beyond the judgment already captured by the delegation class.

#### ST-23 — Local pre-commit lint for OpenAPI contract completeness

**Owner:** Head of Specs Team; API Contracts & Documentation Owner
**Estimated effort:** 0.50d
**Delegation class:** autonomous — tooling addition mirroring the existing CI gate's logic

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`

**Dependencies:** None

**Notes:** Must catch at least the same class of omission as the CI gate (`## METHOD /path` heading without a matching `openapi.yaml` entry).

**Staging-only ACs:** None — a local git-hook script, testable by triggering it against a deliberate fixture omission.

#### ST-24 — Base44 prompt versioning changelog

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** 0.50d
**Delegation class:** autonomous — documentation

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`

**Dependencies:** None

**Notes:** First entry backfilled from the most recent known prompt change.

**Staging-only ACs:** None — a documentation deliverable.

#### ST-25 — Base44 component regeneration diff review checklist

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** 0.50d
**Delegation class:** autonomous — documentation

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`

**Dependencies:** Sequence before ST-26 (both touch `claude/agents/` documentation — see `sprint_planning_notes.md` Dependency Map advisory)

**Notes:** Checklist referenced from the Base44 Frontend Prompt Owner's charter.

**Staging-only ACs:** None — a documentation deliverable.

#### ST-26 — Onboarding template for new agent role charters

**Owner:** Director of HR
**Estimated effort:** 0.50d
**Delegation class:** autonomous — documentation/template authoring

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-26`

**Dependencies:** Sequenced after ST-25 (see `sprint_planning_notes.md` Dependency Map advisory)

**Notes:** Template referenced from `claude/agents/` documentation.

**Staging-only ACs:** None — a documentation deliverable.

#### ST-27 — API key rotation drill

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 0.50d
**Delegation class:** delegated_backend — touches live credentials and an external provider; requires human-supervised execution

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-27`

**Dependencies:** None

**Notes:** Runbook corrected if any step failed; findings documented.

**Staging-only ACs:** "Rotation runbook exercised end-to-end for one non-critical key" — requires a real rotation against a live external provider; cannot be simulated in CI.

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Yes — confirmed as written, 2026-09-09.
**Capacity buffer-floor (98.2%) acknowledged:** Yes — proceed at full scope, 2026-09-09 (see `sprint_capacity.md §1.5`).
**Sprint backlog sealed:** Yes — all 27 items across 5 EPICs, as drafted.

Product Owner: Confirmed
Date: 2026-09-09
