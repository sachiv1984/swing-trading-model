**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-09-14
**Cycle:** 2026-09-14__release-v9.4
**Release:** v9.4
**Sprint Goal:** Clear the full v9.4 debt-reduction scope — 28 items across 6 EPICs — at the top of confirmed sprint capacity, including standing up the AI-output boundary-language sampling hook (`BLG-AI-06`/ST-23). See `sprint_goal.md`.
**Backlog Slice Source:** Original — `stage4_backlog_slice.md`

## Sprint Scope

**Merge order:** EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04 → EPIC-05 → EPIC-06 (rationale: `sprint_planning_notes.md ## Execution Sequence`). **`execution_state.json` owner:** EPIC-01. **Shared files:** `design_system.md` (EPIC-04 owns, EPIC-05 rebases after); `dashboard.md` (EPIC-05 owns, EPIC-06 rebases after); `reports.md` (EPIC-04 only, no contention). No shared touch to `openapi.yaml` or `data_model.md` this cycle.

---

### EPIC-01 — Backend & Platform Engineering Debt

**Maps to:** S2-01
**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner; API Contracts & Documentation Owner; Head of Engineering
**Estimated effort:** 8.50 days
**Risk IDs:** RISK-01
**Execution sequence:** 1

#### ST-01 — DB-level unique constraint on (ticker, entry_date) for open positions

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** S (~0.5d)
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Notes:** RISK-01 — no live DB access in this environment to pre-check for existing duplicate `(ticker, entry_date)` rows; pre-check must be written into the migration script itself (fail loudly with a clear offending-rows report).

**Staging-only ACs:** AC-03 (live-DB duplicate pre-check against production-shaped data — `DATABASE_URL` unavailable in this environment; if a live pre-check cannot run, the migration is delivered/verified against synthetic/staging-shaped data and the live step is explicitly disclosed as pending per RISK-01, not claimed complete).

---

#### ST-02 — Nullable trade_plan_id FK migration path

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** M (~2–3 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** Formalises/cross-references `BLG-BE-52`'s existing no-backfill decision; does not reopen it.

**Staging-only ACs:** None.

---

#### ST-03 — CI check for the inverse OpenAPI drift case

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** M (~1–3 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** Any pre-existing inverse-drift gap found must be filed as its own `BLG-SPEC-*` item, not fixed inline.

**Staging-only ACs:** None.

---

#### ST-04 — Deprecated-endpoint removal-follow-through scan

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** Manual grep acceptable at current scale.

**Staging-only ACs:** None.

---

#### ST-05 — Investigate consolidating the 3 scheduled-job runners into one orchestrator

**Owner:** Head of Engineering
**Estimated effort:** M (~1–3 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** Spec-only this cycle — no migration performed.

**Staging-only ACs:** None.

---

### EPIC-02 — QA & Test Coverage Debt

**Maps to:** S2-02
**Owner:** QA Testing Owner; Director of Quality
**Estimated effort:** 0.45 days
**Risk IDs:** RISK-02
**Execution sequence:** 2

#### ST-06 — Add boundary-condition Playwright coverage for Arc5ComplianceSection low-trade-volume advisory

**Owner:** QA Testing Owner
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-07 — Add backend pytest coverage for GET /analytics/arc5-compliance total_closed_trades field

**Owner:** QA Testing Owner
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** RISK-02 — confirm current `get_arc5_trade_plan_adherence_rate` signature in `backend/services/` before writing tests; update AC text if renamed rather than testing a stale name.

**Staging-only ACs:** None.

---

#### ST-08 — Pinned regression assertion for Settings heading-order fix and TradePlan/Settings aria-labelledby swap

**Owner:** QA Testing Owner
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

### EPIC-03 — Operations & Security Debt

**Maps to:** S2-03
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect; Cybersecurity & Trust Lead
**Estimated effort:** 1.65 days
**Risk IDs:** RISK-03
**Execution sequence:** 3

#### ST-09 — Wire the AI endpoint cost/latency anomaly check into a scheduled job and alert channel

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~0.5d)
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** RISK-03 — `DATABASE_URL` unavailable in this environment (re-confirmed this session); wiring must be delivered and verified against a mocked/simulated feed if live data access is unavailable, with the real-data sub-criterion explicitly disclosed as pending.

**Staging-only ACs:** AC-01/AC-04 (scheduled job running against real production data, and the "runs against real data" sub-criterion — `DATABASE_URL` unavailable; disclose, do not fabricate, per RISK-03).

---

#### ST-10 — Run real Q3 2026 AI cost-trend query against production data

**Owner:** FinOps & Resource Architect
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** RISK-03 — same production-DB-access constraint as ST-09; if unavailable, disclose and leave the existing carried-forward estimate in place with the disclosure dated.

**Staging-only ACs:** AC-01 (actual Q3 2026 production query result — `DATABASE_URL` unavailable; disclose per RISK-03 rather than fabricate).

---

#### ST-11 — Rotate and scope-narrow the CI service account token

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** Credential rotation requires repo-admin-level execution access.

**Staging-only ACs:** None.

---

#### ST-12 — Automated secret-scanning pre-commit hook

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

### EPIC-04 — Spec, Documentation & Financial Reporting Debt

**Maps to:** S2-04
**Owner:** Frontend Specifications & UX Documentation Owner; Metrics Definitions & Analytics Canonical Owner; Financial Reporting & Records Owner
**Estimated effort:** 5.45 days
**Risk IDs:** RISK-04
**Execution sequence:** 4

#### ST-13 — Framer Motion stagger-delay entrance animations can exceed the 500ms motion-vs-contrast guideline ceiling

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** Design Gate Required (motion/timing special rule, §6/BLG-FE-131) — **cleared**; target release (v9.5) and per-component remediation fixed in `design_gate.md`; `design_system.md` v1.15 already bumped. Follow-up backlog item `BLG-FE-175` filed post-gate for the actual v9.5 implementation.

**Staging-only ACs:** None.

---

#### ST-14 — Name the GBP-basis FX-conversion display pattern in design_system.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** XS (<1h)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** Design Pre-Approved — pure spec debt documenting an already-live pattern.

**Staging-only ACs:** None.

---

#### ST-15 — Review placement of Appendix D governance metrics in metrics_definitions.md

**Owner:** Metrics Definitions & Analytics Canonical Owner
**Estimated effort:** XS (<1h)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** Requires an explicit placement decision from Product Owner + Metrics Definitions & Analytics Canonical Owner. LL-v2.2-SP-01 check: this is a content-placement/governance decision, not a UI design decision — no HoST/design artefact applies (`design_gate.md` confirms Design Not Applicable).

**Staging-only ACs:** None.

---

#### ST-16 — Reconciliation check: journal-derived P&L vs broker-statement import totals

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** M (~1–2 days, spec/dependency-mapping only this cycle)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** `BLG-QA-122` (blocked — no broker-import mechanism exists) — external, not blocking (ST-16's own AC scopes this cycle to spec/dependency-mapping only)

**Notes:** RISK-04 — no mitigation action needed beyond following the scoping as written.

**Staging-only ACs:** None.

---

#### ST-17 — Carried-forward-loss field on the tax-year P&L statement

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None

**Notes:** Design Required (new-data-displayed criterion) — **cleared**; `reports.md` v0.17 already bumped, ships as "Design Only — Implementation Pending" (existing document convention).

**Staging-only ACs:** None.

---

### EPIC-05 — Governance Process & AI Compliance Debt

**Maps to:** S2-05
**Owner:** PMO Lead; AI Compliance & Governance Officer; FinOps & Resource Architect; Director of HR
**Estimated effort:** 7.00 days
**Risk IDs:** RISK-05
**Execution sequence:** 5

#### ST-18 — Cross-role escalation response-time tracker

**Owner:** PMO Lead
**Estimated effort:** S (~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-19 — Idea-intake / roadmap-session compute cost attribution

**Owner:** FinOps & Resource Architect
**Estimated effort:** S (~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-20 — Recurring data-density gate trajectory re-estimate cadence

**Owner:** PMO Lead
**Estimated effort:** S (~0.5d)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

#### ST-21 — Quarterly automated re-scan of AI-generated copy for boundary-language drift

**Owner:** AI Compliance & Governance Officer
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None

**Notes:** §13 pre-check: does not introduce/extend an AI-provider call — pre-check does not apply (confirmed in `design_gate.md`).

**Staging-only ACs:** None.

---

#### ST-22 — In-app disclosure block: advisory-only AI outputs vs deterministic outputs

**Owner:** AI Compliance & Governance Officer
**Estimated effort:** M (~1–3 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** ST-23 (`BLG-AI-06`) — soft sequencing per RISK-05, not a hard blocker (sequence after if both touch the same AI-response wrapper)

**Notes:** Design Required (observable UI element) — **cleared**; `design_system.md` v1.15 and `dashboard.md` v3.5 bumped, decision record produced. Classified `autonomous` per BLG-GOV-72 fast-path (c) — new component against a now-locked frontend spec, Playwright feasibility confirmed by the AC itself. Its own AC already requires Playwright coverage of the badge's presence on the daily-briefing surface, or a recorded staging sign-off, per the CLAUDE.md frontend-visible-change standard — "documented in a canonical frontend spec" alone does not satisfy it (carried verbatim from `stage4_backlog_slice.md`'s own design-gate note).

**Staging-only ACs:** None (Playwright coverage is the primary, CI-verifiable path; staging sign-off is the AC's named fallback only).

---

#### ST-23 — Implement generation-time opt-in sampling hook for AI-output boundary-language audits

**Owner:** AI Compliance & Governance Officer
**Estimated effort:** M (~1–2 days)
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`

**Dependencies:** None

**Notes:** RISK-05 — scope to the shared AI-response helper/wrapper if one exists (touch one chokepoint, not 5 call sites individually); if none exists, deliver a phased implementation and file follow-on `BLG-AI-*` items for remaining call sites. On completion of a genuine ≥10-output sample, `ESC-EXEC-20260910-01` should be re-acknowledged toward `Resolved` (superseding its interim `Deferred` disposition) per its own `deferred_trigger`.

**Staging-only ACs:** AC-04 (a genuine, non-illustrative sample of ≥10 AI outputs drawn and scanned — requires production credentials/`ANTHROPIC_API_KEY` per `ESC-EXEC-20260910-01`'s own disclosed environment constraint; disclose rather than fabricate if still unavailable).

---

### EPIC-06 — Frontend, UX & Product Debt

**Maps to:** S2-06
**Owner:** Base44 Frontend Prompt Owner; Head of UX & Design; Product Owner
**Estimated effort:** 4.50 days
**Risk IDs:** RISK-06
**Execution sequence:** 6

#### ST-24 — Audit Base44 components for orphaned props

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`

**Dependencies:** None

**Notes:** Design Pre-Approved — cleanup only, existing Playwright coverage must pass with no regression.

**Staging-only ACs:** None.

---

#### ST-25 — Standardise the loading-skeleton pattern across screens

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** M (~1–3 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`

**Dependencies:** None

**Notes:** Design Required — **cleared**; `screener_results.md` v1.5, `red_flag_journal.md` v1.2, `dashboard.md` v3.5 (confirmed conformant) all bumped/confirmed. Classified `autonomous` per BLG-GOV-72 fast-path (c) — locked frontend spec now exists across all 3 target screens.

**Staging-only ACs:** None (Playwright visual check is the primary, CI-verifiable path; staging sign-off is the AC's named fallback only).

---

#### ST-26 — Usability pass on the Arc 5 compliance advisory banner

**Owner:** Head of UX & Design
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-26`

**Dependencies:** None

**Notes:** Review-only; any recommended change filed as its own item, not fixed inline.

**Staging-only ACs:** None.

---

#### ST-27 — Standard interaction-timing rule for toast notifications

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-27`

**Dependencies:** None

**Notes:** Design Required (motion/timing special rule, reclassified from an initial Pre-Approved read) — **cleared**; `design_system.md` v1.15 already bumped. List of non-conforming screens is documentation-only this cycle.

**Staging-only ACs:** None.

---

#### ST-28 — Minimal "trade plan required before entry" UI soft-nudge

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-28`

**Dependencies:** None

**Notes:** Design Required — **cleared**; `position_form.md` v1.4 bumped, decision record produced. Classified `autonomous` per BLG-GOV-72 fast-path (c). Priority corrected P3→P2 at Release Planning (Skill-Silo mandatory pull-forward, BLG-FEAT-95). Does not conflict with §13 (no automation of the entry decision itself).

**Staging-only ACs:** None (Playwright coverage confirming non-blocking behaviour is the AC's own required, CI-verifiable path).

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24–28 days |
| Total estimated effort (in-scope) | 27.55 days |
| Utilisation | 98.4% of the 28-day ceiling |
| Over-allocation | No — within band; buffer-floor-exceeded advisory recorded and acknowledged (`sprint_capacity.md §1.5`) |

## Items Deferred This Sprint

None — all 28 items in the authoritative backlog slice are in scope. See `sprint_planning_notes.md ## Deferred Items` for items excluded from v9.4 scope at Release Planning (out of this engine's remit to re-litigate).

## Deferred Execution Blockers Accepted

*(section omitted — `deferred_execution_blockers` was empty in `state.json`)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|----------|
| Buffer-floor-exceeded acknowledgement (98.4% of capacity ceiling) | Product Owner | No |
| Soft-sequence ST-23 before ST-22 at execution if a shared AI-response chokepoint exists | PMO Lead | No |

No outstanding action is marked `Blocker? Yes`.

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — 2026-09-14 (see `sprint_goal.md`)
**Scope confirmed:** Confirmed — 28/28 items in, full capacity per explicit Release Planning instruction, no over-allocation
**Capacity confirmed:** Confirmed — 27.55d vs ~24–28d band, pass/no-WARN; buffer-floor-exceeded (98.4%) acknowledged per `sprint_capacity.md §1.5`
**Deferred execution blockers accepted (if any):** N/A — none present
**Signed off by:** Product Owner (agent-mediated, per `shared_standards.md §16.13`)
**Date:** 2026-09-14
