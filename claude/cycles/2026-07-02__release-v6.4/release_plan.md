**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v6.4
**Cycle:** 2026-07-02__release-v6.4
**Last Updated:** 2026-07-02

---

# Release Plan — v6.4 Audit Remediation, Security Hardening & Strategy Benchmark Enhancement

---

## Readiness

**Roadmap authority:** §-1.2 cleared via STEP 8.1 Option(b) decision from rebalance 2026-07-01__scheduled. `run_manifest.md` (2026-07-01__scheduled) records: "PO decision (STEP 8.1): Option (b) — defer... Release planning for v6.4 is the appropriate next step via `plan release v6.4`." `**Next planned release:** v6.4` confirmed in roadmap §1 header.

**Context:** v6.3 (Strategy Benchmark, AI Security & Quality Infrastructure) shipped 2026-06-30 (Verified, Closed_with_actions). v6.4 opens with one mandatory production correctness fix (BLG-BE-40, STEP 8.0 fast-track — signal generation reads a deprecated table), a P1 security-adjacent cluster from the AI injection risk assessment (BLG-SEC-01/02), the full lifecycle-audit remediation set from AUD-2026-07-01 (BLG-GOV-150/151/152/153), the Skill-Silo pull-forward feature candidate (BLG-FEAT-54 — Open Positions panel), two accessibility contrast fixes (BLG-UX-01/02), one ops baseline registration (BLG-OPS-82), and two Playwright test-gap closures carried from v6.3 delivery verification (TEST-GAP-EPIC-01/03).

**Advisories from STEP 1:**
- ℹ No perennial-return items; no within-sprint date gates (§1.4a/b) — all 13 candidates are new to backlog tracking this cycle.
- ℹ Advisory (§1.2): all 13 candidates already carry `Provisional-Target: v6.4` — no stale-target correction needed.
- ⚠ Advisory (§1.3): Design dependencies on BLG-FEAT-54 (new Open Positions panel), BLG-UX-01/02 (contrast changes to existing components). Design Gate required — 3 items classified as UI-facing (see STEP 4.1).
- ℹ Re-targeting: FI-P4-01 and FI-P3-02 (both carried as "action during sprint execution" since v6.3 planning, both missed) are resolved by inclusion in `BLG-GOV-152`'s scope this cycle. FI-P3-01 (Playwright strict-mode Base44 §6 advisory) has no existing backlog item — folded into `BLG-GOV-152` scope by Head of Specs Team delegated decision (see `decisions--2026-07-02__release-v6.4.md`). All three now carry a concrete cycle_id target instead of a shipped release label.
- ℹ Arc 4 data density: AI journals started v6.2 (2026-06-25); PO-02 gate → projected 2026-12-25. PO-04 (50+ trades with plans) trajectory unknown — not re-queried this session. SI-02 (20+ trades with plans) last checkpoint 2026-06-09 (6/11 trades, gate NOT MET) — stale, PMO Lead owns re-check. None of these gate-conditional initiatives are in this release's scope.

---

## Scope

| S2-ID | Backlog Item | Description | Priority | Effort | Type | Class |
|-------|-------------|-------------|----------|--------|------|-------|
| S2-01 | BLG-BE-40 | Signal generation reads deprecated `tickers` table instead of `ticker_universe` | P1 | XS | Bug/Data Model | Firm |
| S2-02 | BLG-SEC-01 | Sanitise `context_opts.ticker` before system prompt injection (POST /ai/chat) | P2 | XS | Security | Firm |
| S2-03 | BLG-SEC-02 | Validate ticker/market strings at signal write time (screener pipeline) | P3 | S | Security | Conditional |
| S2-04 | BLG-GOV-150 | Fix governance version-sync drift (OPERATIONAL_GUIDE self-desync, §14 roadmap version, metrics owner role-name drift) | P2 | S | Governance | Firm |
| S2-05 | BLG-GOV-151 | Document hygiene cleanup (README coverage/staleness/broken path, Class 6 header format, agent header bolding) | P3 | S | Governance/Docs | Conditional |
| S2-06 | BLG-GOV-152 | Close structural reliability gaps (append-only guard parity, DF-10 `spec_references` convention, staging AC protocol, `amendment_lessons` sunset contradiction, FI-P3-01 Base44 §6 fold-in) | P2 | M | Governance | Firm |
| S2-07 | BLG-GOV-153 | Audit & governance process fixes (design gate bypass authority, `run audit` dry-run entry, `FRICTION_LOAD` formula wording, `scored_initiatives` naming) | P2 | S | Governance | Firm |
| S2-08 | BLG-FEAT-54 | Add Open Positions panel to Strategy Benchmark page | P2 | M | Product Feature | Firm |
| S2-09 | BLG-UX-01 | Improve AI daily briefing disclaimer text contrast | P3 | XS | UX/Accessibility | Conditional |
| S2-10 | BLG-UX-02 | Improve AI chat widget footer disclaimer contrast and add test coverage | P2 | XS | UX/Accessibility | Firm |
| S2-11 | BLG-OPS-82 | Add v6.3 endpoints to `api_performance_baseline.md` | P3 | XS | Operations | Conditional |
| S2-12 | TEST-GAP-EPIC-01 | Playwright coverage for ST-01 observable UI ACs (AI journal summary error states) | P3 | XS | QA/Test Coverage | Conditional |
| S2-13 | TEST-GAP-EPIC-03 | Playwright scenario coverage for Strategy Benchmark page | P2 | S | QA/Test Coverage | Firm |

**Items explicitly deferred:** None — all 13 `Provisional-Target: v6.4` candidates are in scope.

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01, S2-02, S2-03 | Backend Engineering Patterns Owner; Cybersecurity & Trust Lead | RISK-01 | None |
| EPIC-02 | S2-04, S2-05, S2-06, S2-07 | Head of Specs Team | RISK-03 | None |
| EPIC-03 | S2-08, S2-09, S2-10, S2-11, S2-12, S2-13 | Head of UX & Design; Backend Engineering Patterns Owner; QA & Testing Owner | RISK-05 | Design Gate required before sprint planning seals (BLG-FEAT-54, BLG-UX-01, BLG-UX-02 are UI-facing) |

**EPIC-01 — Backend Correctness & Security Hardening.** Fixes the P1 ticker-source correctness bug (mandatory STEP 8.0 fast-track) alongside the two AI-injection input-validation gaps identified in the ST-04 risk assessment. All backend-only; no frontend or contract surface.

**EPIC-02 — Governance & Audit Remediation.** Closes all four remediation clusters from lifecycle audit AUD-2026-07-01, and resolves the two-cycle-overdue FI-P4-01/FI-P3-02 friction items plus the Base44 §6 FI-P3-01 advisory (folded into BLG-GOV-152's scope — see Decisions Record). Multiple governance-file edits across 4 stories in the same EPIC — see RISK-04.

**EPIC-03 — Strategy Benchmark Enhancement & UX/QA Polish.** Delivers the Skill-Silo pull-forward feature (Open Positions panel), two accessibility contrast fixes, one ops baseline registration, and closes both outstanding v6.3 Playwright test gaps (TSG-v63-01, TSG-v63-02).

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Switching `signal_service.py`'s ticker source from `tickers` to `ticker_universe` could change live signal generation output if the active lists diverge materially | Medium | Verify parity by adding/deactivating a test ticker in Ticker Universe Management and confirming it appears/disappears in generated signals before merge, per BLG-BE-40 AC | null |
| RISK-02 | EPIC-01 | Ticker/market validation regex (BLG-SEC-01/02) could reject legitimate international ticker formats | Low | Test validation regex against full current `ticker_universe` active list before deploy; regex explicitly allows `.`, `-`, `/`, `:` | null |
| RISK-03 | EPIC-02 | BLG-GOV-152 folds in FI-P3-01 (Base44 prompt draft §6 fix) without a dedicated backlog ID, risking scope ambiguity at sprint planning | Low | Documented explicitly in `decisions--2026-07-02__release-v6.4.md` Scope Decisions; `stage4_backlog_slice.md` ST-06 acceptance criteria will list the FI-P3-01 fix as an explicit AC | null |
| RISK-04 | EPIC-02 | 4 governance-file-editing stories in one EPIC risk missing the CLAUDE.md §6 Governance File Edit Checklist (version bump, OPERATIONAL_GUIDE §14 sync, prompt_change_log.md entry) on one or more touched files | Medium | Run `/governance-drift` before each governance commit in this EPIC; PMO Lead to verify checklist completion at delivery verification | null |
| RISK-05 | EPIC-03 | BLG-FEAT-54's new backend read path, if implemented as a new endpoint, must ship `openapi.yaml` + contract doc + `backend/routers/test.py` registration in the same commit (CLAUDE.md hard gate) | Medium | Sequence backend endpoint + contract + test registration before frontend panel work within the story; use `/commit-check` before each commit | null |
| RISK-06 | EPIC-03 | 3 UI-facing items (BLG-FEAT-54, BLG-UX-01, BLG-UX-02) require Design Gate clearance before sprint planning can seal | High | `run design-gate --cycle 2026-07-02__release-v6.4` must be run and must Pass (or receive a documented bypass) before `plan sprint` is invoked — flagged in `cycle_summary.md` Pre-sprint Planning Required Decisions | null |

---

## Integrity Validation — 3.5 Local Model Integrity

All 13 scope items (S2-01–S2-13) map to exactly one EPIC each; all 3 EPICs reference at least one RISK-ID; all 6 RISK-IDs referenced in the EPIC table appear in the Risk Register Summary with no orphaned references. No S2 item is unmapped. No EPIC lacks an Owner. Plan is internally consistent and executable.

**Result: PASS**

---

## Capacity Check

**Effort Band Lookup (ST-14):** No matching rows in `scored_initiatives.md` for any of the 13 items in scope (see `run_manifest.md`) — all estimates below use the STEP 4 inline estimate derived from each backlog item's stated Effort band.

| EPIC | ST-ID | Story | Effort (days) | Class |
|------|-------|-------|----------------|-------|
| EPIC-01 | ST-01 | Signal generation ticker source fix (BLG-BE-40) | 0.15 | Firm |
| EPIC-01 | ST-02 | Sanitise context_opts.ticker (BLG-SEC-01) | 0.25 | Firm |
| EPIC-01 | ST-03 | Validate ticker/market at signal write (BLG-SEC-02) | 0.5 | Conditional |
| EPIC-02 | ST-04 | Fix governance version-sync drift (BLG-GOV-150) | 0.5 | Firm |
| EPIC-02 | ST-05 | Document hygiene cleanup (BLG-GOV-151) | 0.5 | Conditional |
| EPIC-02 | ST-06 | Structural reliability gaps + FI re-target (BLG-GOV-152) | 1.75 | Firm |
| EPIC-02 | ST-07 | Audit & governance process fixes (BLG-GOV-153) | 0.5 | Firm |
| EPIC-03 | ST-08 | Open Positions panel (BLG-FEAT-54) | 1.5 | Firm |
| EPIC-03 | ST-09 | Daily briefing disclaimer contrast (BLG-UX-01) | 0.25 | Conditional |
| EPIC-03 | ST-10 | Chat widget footer contrast + test (BLG-UX-02) | 0.25 | Firm |
| EPIC-03 | ST-11 | API performance baseline registration (BLG-OPS-82) | 0.15 | Conditional |
| EPIC-03 | ST-12 | Playwright coverage — AI journal summary errors (TEST-GAP-EPIC-01) | 0.5 | Conditional |
| EPIC-03 | ST-13 | Playwright coverage — Strategy Benchmark page (TEST-GAP-EPIC-03) | 1.0 | Firm |
| **Total** | | | **7.8** | 8 Firm / 5 Conditional |

**Capacity baseline:** ~12–14 working days per sprint (solo developer, `workforce_capacity.md` effective 2026-05-27). Warn threshold: >14 days.

**Outcome: PASS.** Estimated total effort (7.8 days) is well within the single-sprint capacity baseline — no phasing recommendation required. A single-sprint plan is feasible.

**Skill constraints:** None. Solo operator model — all roles fulfilled by a single developer. Governance load (EPIC-02, 4 items) ≈38% of estimated effort — within the 20–60% healthy band, resolving the Skill-Silo Alert raised at the 2026-07-01__scheduled rebalance via inclusion of `BLG-FEAT-54` (execution/product item).

---

## Integrity Validation — 5.5 Cross-Stage Integrity

- All 13 S2-IDs (S2-01–S2-13) map to exactly one EPIC each in both §Scope and §Execution Plan.
- All 3 EPIC IDs in `stage4_backlog_slice.md` (EPIC-01, EPIC-02, EPIC-03) match the EPIC table in §Execution Plan.
- All 6 RISK-IDs (RISK-01–RISK-06) referenced in the §Execution Plan EPIC table appear in the Risk Register Summary. No orphaned references.
- All 13 ST-IDs (ST-01–ST-13) in `stage4_backlog_slice.md` reference a valid `Backlog ref` and `EPIC` matching §Scope/§Execution Plan.

**Result: PASS**

## Integrity Validation — 5.7 Decision Record Integrity

Not applicable — `artifacts.escalations` is absent (no escalations raised this cycle). Skipped per STEP 5.5 rule.

**Result: not_applicable**

---
