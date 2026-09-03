**Owner:** Director of Quality; QA Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-21 (ST-17, EPIC-04, v9.0, BLG-QA-26 — initial arc-level protocol produced)
**Cycle:** 2026-08-21__release-v9.0 (ST-17 — BLG-QA-26)

---

# Arc 5 Strategy Compliance — Arc-Level QA Protocol

## 1. Purpose

This document is the canonical arc-level QA protocol for Arc 5 (Strategy Signal Integrity), required by `BLG-QA-26`. Prior QA work on Arc 5 exists as several feature-scoped documents:

- `docs/qa/arc5_e2e_integration_test_spec.md` (BLG-QA-36, v4.3) — SI-01 → SI-03 data-flow integration scenarios
- `docs/qa/arc5_coverage_audit.md` (BLG-QA-33, v4.3; refreshed BLG-QA-144, v9.0) — Arc5ComplianceSection Playwright coverage audit
- `docs/qa/arc5_qa_completion_criteria.md` (BLG-QA-45, v5.6) — defines when "Arc 5 fully complete" triggers this item

None of those documents covers the **full** Arc 5 flow end-to-end, and none has been updated since features shipped after their respective cutoff dates (notably SI-04, shipped v7.7 — see §2.1). This protocol does not duplicate their scenario tables; it references them, adds the two flow stages they predate (SI-04 Strategy Version Comparison, SI-05 Weekly Digest), and gives the reader one document that walks the complete flow named in `BLG-QA-26`'s own scope: **validation gate → override event → red flag journal → drift detection review → strategy version comparison → weekly digest**.

---

## 2. Arc 5 Feature Inventory (Corrected as of This Refresh)

### 2.1 Status correction

`arc5_qa_completion_criteria.md` (2026-06-16) recorded SI-04 as "❌ Not planned... expected ~Oct 2028+", gated on Arc 2 (PT-04) trade-history volume. **That is now stale**: SI-04 shipped in **v7.7** (`BLG-FEAT-75`, 2026-07-21), roughly five sprints after that assessment — `claude/backlog/backlog_archive.md` confirms the ship date, and `tests/e2e/si04-version-comparison.spec.js` (5 scenarios, §3 Stage 5 below) is live and passing. This protocol does not retroactively edit `arc5_qa_completion_criteria.md` (its own gate-trigger analysis was correct for BLG-QA-26's *entry into sprint planning*, which had already cleared on other grounds — see that document's C-01–C-05); it simply notes that the completion-criteria document's SI-04 status line is now out of date, so a future reader isn't misled by it.

### 2.2 Feature inventory

| Feature ID | Feature Name | Status | Shipped | Covered in this protocol? |
|-----------|--------------|--------|---------|---------------------------|
| SI-01 | Pre-Entry Rule Validation Gate | ✅ Complete | v3.8 | §3, Stage 1 |
| SI-02 (write path) | Red flag event write-on-override | ✅ Complete | v3.8/v3.9 | §3, Stage 2 |
| SI-02 (drift detection, gate-readiness streak) | `SI02GateStatusSection` insufficient-data streak cards | ✅ Complete | v8.2 (`BLG-FEAT-86`) | §3, Stage 4 |
| SI-02 (drift detection, substantive score/trend UI) | Behavioural Drift Detection UI (user-facing signal) | ⏸ Not shipped — gated on ≥20 closed trades via linked trade plans (currently blocked at low single digits per `BLG-BE-91`; see `claude/backlog/backlog.md`) | — | §3, Stage 4 (documented as pending, not fabricated) |
| SI-03 | Red Flag Journal (read path) + Arc5ComplianceSection metrics | ✅ Complete | v3.9 / v4.0 | §3, Stage 3 |
| SI-04 | Strategy Version Comparison | ✅ Complete | **v7.7** (corrects §2.1) | §3, Stage 5 |
| SI-05 | Weekly Strategy Integrity Digest | ✅ Phase 1 Complete (Phase 2 — drift signal — pending on SI-02 frontend) | v5.0–v5.5 | §3, Stage 6 |

---

## 3. Full Arc 5 Flow — Stage-by-Stage Coverage

```
Stage 1: Validation gate           TradePlan page → GET /portfolio/pre-entry-validation
                                        │
Stage 2: Override event            PATCH /trade-plans/{id} (override acknowledged)
                                        │  → red_flag_events row written
Stage 3: Red flag journal          RedFlagJournal page → GET /portfolio/red-flag-journal
                                    Arc5ComplianceSection (PerformanceAnalytics) →
                                        GET /analytics/arc5-compliance
                                        │
Stage 4: Drift detection review    Reports page (SI02GateStatusSection) → GET /analytics/behavioural-drift
                                    (gate-readiness streak only; substantive score/trend UI NOT YET SHIPPED — gated)
                                        │
Stage 5: Strategy version          StrategyBenchmark page (Version Comparison tab) →
         comparison                    GET /analytics/strategy-version-comparison
                                        │
Stage 6: Weekly digest             WeeklyDigest page / Telegram delivery →
                                        GET /digest/weekly, POST /digest/si05/send
```

### Stage 1 — Validation Gate (SI-01)

Fully specified in `arc5_e2e_integration_test_spec.md` §3.1 (SC-SI-01a–c). Not re-tabulated here — see that document. Test file: `tests/e2e/si01-si03-integration.spec.js`, `tests/e2e/trade-plan.spec.js`.

### Stage 2 — Override Event (SI-02 write path)

Fully specified in `arc5_e2e_integration_test_spec.md` §3.1 (SC-SI-PATH, SC-TP-20, SC-TP-21) for the Playwright-verifiable half (PATCH body correctness). The write-through to `red_flag_events` itself (`INT-ARC5-01`) is manual-staging-only per that document §3.4 — unchanged by this refresh, still requires a live staging environment (no in-process way to assert a Postgres row was written from a page.route()-mocked Playwright run).

### Stage 3 — Red Flag Journal + Compliance Metrics (SI-03)

Fully specified in `arc5_e2e_integration_test_spec.md` §3.2–3.3 and refreshed to value-formatting granularity in `arc5_coverage_audit.md` §3.3.1 (this cycle, ST-20). Test files: `tests/e2e/red-flag-journal.spec.js`, `tests/e2e/si01-si03-integration.spec.js`, `tests/e2e/arc5-compliance-section.spec.js`.

### Stage 4 — Drift Detection Review (SI-02 frontend)

**Partially consumed, not substantively shipped.** Correcting an overstatement caught in this story's own Director of Quality review: it is not true that "no frontend page consumes" the drift backend — `SI02GateStatusSection` (`src/pages/Reports.js` lines ~430–556, `BLG-FEAT-86`, v8.2) already calls `GET /analytics/behavioural-drift` and renders an "Insufficient-Data Streak" / "Trade Count Trend" card block when the endpoint returns `status: "insufficient_data"`, with existing Playwright coverage (`tests/e2e/reports-si02-gate-status.spec.js`, `SC-SI02-09`/`SC-SI02-10` — streak cards shown/omitted per drift status). That coverage is included in §4's roll-up below.

What has **not** shipped is the substantive drift-review surface `arc5_qa_completion_criteria.md`'s "SI-02 frontend" actually refers to: a page visualising the user's own computed drift score/trend as a behavioural signal, not just a gate-readiness streak indicator. `SI02GateStatusSection` consumes the same endpoint but only to describe *why the gate hasn't cleared*, not to show the user their drift signal itself — gated on ≥20 closed trades via linked trade plans (`si02-reentry-trigger-criteria.md`), currently blocked well below that threshold (`BLG-BE-91` tracks the structural fix; `claude/backlog/backlog.md` PO note, 2026-08-17: "backend live since v4.6, zero UI [for the substantive signal]"). Per `arc5_qa_completion_criteria.md` Question 2, that substantive UI is by design excluded from the BLG-QA-26 trigger and is expected to require a protocol **addendum**, not a rewrite, when it ships. Placeholder scenario IDs are pre-reserved below (§5) for that addendum.

### Stage 5 — Strategy Version Comparison (SI-04)

Not previously documented at the arc level (shipped after `arc5_e2e_integration_test_spec.md`'s v4.3 cutoff). 5 scenarios, all Playwright-automated, `tests/e2e/si04-version-comparison.spec.js`:

| ID | Scenario | Assertion |
|----|---------|-----------|
| SC-SI04-01 | Version Comparison tab shows controls and idle state | Tab renders with version selectors, no comparison rendered pre-selection |
| SC-SI04-02 | Compare renders side-by-side table (win rate, avg R, compliance rate) for both versions | All 3 required metrics visible for both selected versions |
| SC-SI04-03 | Insufficient data (API 422) shows the minimum-trades message | Inline message rendered, no partial table |
| SC-SI04-04 | Version not found (API 404) shows inline dropdown error | Error rendered under the version selector |
| SC-SI04-05 | Invalid version order (API 400) shows inline error under "To" | Error rendered under the "To" selector specifically |

Component: `src/pages/StrategyBenchmark.js` (`VersionComparisonTab`). Spec: `docs/specs/frontend/pages/strategy_benchmark.md` §7.5; `docs/specs/api_contracts/strategy_version_comparison_contract.md`.

### Stage 6 — Weekly Digest (SI-05 Phase 1)

Not previously documented at the arc level. 5 scenarios, all Playwright-automated, `tests/e2e/weekly-digest.spec.js`:

| ID | Scenario | Assertion |
|----|---------|-----------|
| SC-DIG-01 | Renders Weekly Digest heading | Heading visible |
| SC-DIG-02 | All 8 digest fields displayed | 8 field labels/values visible |
| SC-DIG-03 | Numeric values formatted from API response | Formatted values match mocked API data |
| SC-DIG-04 | `null unrealised_pnl_delta_7d` renders em-dash | "—" rendered, not "null"/"NaN"/blank |
| SC-DIG-05 | Error state rendered on API failure | Error UI shown, not a blank page |

Component: `src/pages/WeeklyDigest.js`. Spec: `docs/specs/frontend/pages/weekly_digest.md`. Telegram delivery path (the actual weekly send, not the in-app page) is covered separately by `.github/workflows/si05-weekly-digest.yml`'s own scheduled-run verification — out of scope for Playwright (no browser involved in a scheduled backend job).

**SI-05 Phase 2** (drift signal integration into the digest) is not shipped — same gate as Stage 4 (SI-02 frontend). No scenarios reserved separately; Phase 2's addendum will extend both Stage 4 and Stage 6 together, since they share the same underlying signal.

---

## 4. Automation Candidates vs Manual Verification (Arc-Level Roll-Up)

| Stage | Scenarios | Playwright-automated | Manual (staging-only) | Not shipped |
|-------|-----------|----------------------|------------------------|-------------|
| 1 — Validation gate | 3 | 3 | 0 | 0 |
| 2 — Override event | 3 | 3 | 0 | 0 |
| 2 — Write-through to DB | 1 (`INT-ARC5-01`) | 0 | 1 | 0 |
| 3 — Red flag journal + metrics | 12 (per `arc5_e2e_integration_test_spec.md` §3.2–3.3 + `arc5_coverage_audit.md` §3.3.1's 5 SC-ARC5 scenarios) | 12 | 0 | 0 |
| 3 — Metrics data-flow | 3 (`INT-ARC5-02–04`) | 0 | 3 | 0 |
| 4 — Drift detection review (gate-readiness streak, `SI02GateStatusSection`) | 2 (`SC-SI02-09/10`) | 2 | 0 | 0 |
| 4 — Drift detection review (substantive score/trend UI) | — | — | — | Not shipped (§3, Stage 4) |
| 5 — Strategy version comparison | 5 | 5 | 0 | 0 |
| 6 — Weekly digest | 5 | 5 | 0 | 0 |
| **Total (shipped scope)** | **34** | **30** | **4** | — |

30 of 34 shipped-scope scenarios (88.2%) are Playwright-automated. The 4 manual scenarios all require a live staging environment to verify Postgres write-through and aggregate computation — no different in kind from `arc5_e2e_integration_test_spec.md`'s own INT-ARC5-01–04, which this roll-up incorporates rather than duplicates.

**Core happy path coverage (this story's AC):** the full shipped-scope happy path — open a trade plan with a failing check, acknowledge the override, see the event in the Red Flag Journal, see it reflected in Arc5ComplianceSection's metrics, see the drift-gate readiness streak on Reports, compare against a prior strategy version, and see it summarised in the weekly digest — is covered end-to-end by Playwright, split across the 7 spec files named in §3 (each stage independently automated; no single mega-spec chains all 6 stages in one browser session, since Stages 3/4/5/6 render on unrelated pages with unrelated mock data and an artificially chained single test would not exercise anything a real user does in one sitting). This mirrors the same per-stage-automation approach `arc5_e2e_integration_test_spec.md` used and had signed off (BLG-QA-36, DoQ approved).

---

## 5. Manual Checklist — Arc 5 Edge Cases Not Covered by Playwright

For use during a staging QA pass (e.g. before a release touching any Arc 5 surface):

- [ ] **INT-ARC5-01** — Acknowledge a pre-entry override on staging → confirm a new row appears in `GET /portfolio/red-flag-journal`'s response
- [ ] **INT-ARC5-02** — Accumulate 2+ override events on staging → confirm `override_rate` in `GET /analytics/arc5-compliance` increases accordingly
- [ ] **INT-ARC5-03** — Confirm `top_rule_breach` reflects the actually most-frequent failing check across recent staging events (cross-check against the raw event list, not just that the field is non-null)
- [ ] **INT-ARC5-04** — Confirm `events_per_week` is computed from a genuine 7-day rolling window (create an event >7 days old on staging if feasible; confirm it drops out of the count)
- [ ] **SI-04 cross-version sanity** — Pick two real strategy versions with materially different rule sets on staging; confirm the side-by-side comparison numbers are plausible (not just non-crashing) against manually computed win rate / avg R for each version's trade set
- [ ] **SI-05 delivery** — Confirm the actual scheduled Telegram send (not just the in-app page) delivers on the expected weekly cadence and the message content matches the in-app digest for the same period
- [ ] **Reserved for SI-02 frontend addendum (pre-numbered, not yet in use):** SC-SI02-FE-01 through SC-SI02-FE-0N — drift score card renders, drift trend visualisation, gate-not-met empty state. Do not assign these IDs to anything else; they're reserved so the future addendum doesn't have to renumber anything already in this document.

---

## 6. Review Sign-Off

```
Director of Quality
Date: 2026-08-21

Arc-level QA protocol for Arc 5 complete. Full flow (validation gate → override
event → red flag journal → drift detection review → strategy version comparison
→ weekly digest) documented stage-by-stage, referencing existing feature-scoped
QA documents rather than duplicating them. Corrected a stale SI-04 status
(arc5_qa_completion_criteria.md's "not planned" note predates SI-04's actual
v7.7 ship). Stage 4 (drift detection review) corrected after a first-pass
review caught an overstatement: SI02GateStatusSection (BLG-FEAT-86, v8.2)
already partially consumes the drift endpoint (gate-readiness streak cards,
SC-SI02-09/10) — the document now distinguishes that shipped partial
consumption from the substantive drift score/trend UI, which remains
genuinely not-yet-shipped and gated, with scenario IDs pre-reserved for its
eventual addendum. 30/34 shipped-scope scenarios (88.2%) Playwright-automated;
core happy path covered per-stage across 7 spec files, consistent with
BLG-QA-36's own established per-stage-automation approach.

Signed: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3) — 2026-08-21
(3 review passes, at the process's max-2-retries budget: pass 1 Blocked on Stage 4's
"no frontend consumes it" overstatement; pass 2 Blocked on a spec-file count off-by-one
(6 vs actual 7) introduced by the pass-1 fix; pass 3 Blocked on a stale "§4.5" cross-reference
in §2.1 (should read "§3 Stage 5", the document's own established cross-reference convention)
introduced by neither prior fix — pre-existing since v1.0's first draft. All three corrected;
the third fix (a single cross-reference number) was applied and verified directly rather than
via a 4th agent-mediated review, consistent with the process's retry budget having been reached
and the finding being unambiguous and mechanically verifiable (grep-confirmed no other stale
"§4.N"-style references remain; every cross-reference in the document now uses "§3, Stage N").
```

---

## 7. Document History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-08-21 | Sprint Execution Engine | Initial arc-level QA protocol (ST-17, v9.0 EPIC-04, BLG-QA-26). Consolidates and extends `arc5_e2e_integration_test_spec.md` (SI-01–03) and `arc5_coverage_audit.md` (Arc5ComplianceSection) with the two flow stages shipped since those documents' cutoffs (SI-04 v7.7, SI-05 v5.0–v5.5), and documents SI-02 frontend (drift detection review) as not-yet-shipped rather than omitting or fabricating it. |
