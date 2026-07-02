**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-07-02__release-v6.4
**Last Updated:** 2026-07-02
**Design Gate Required:** true

---

# Cycle Summary — Release Planning v6.4

## Release Identity

**v6.4 — Audit Remediation, Security Hardening & Strategy Benchmark Enhancement**

**Context:** v6.3 (Strategy Benchmark, AI Security & Quality Infrastructure) shipped 2026-06-30 (Verified, Closed_with_actions). v6.4 opens with one mandatory P1 correctness fix (BLG-BE-40 per rebalance STEP 8.0 fast-track mandate), a P2 security-hardening cluster from the ST-04 AI injection risk assessment, the full lifecycle-audit remediation set (AUD-2026-07-01, 4 items), the Skill-Silo pull-forward feature candidate (Open Positions panel), two accessibility contrast fixes, one ops baseline registration, and both outstanding v6.3 Playwright test gaps.

---

## Plan Overview

| Attribute | Value |
|-----------|-------|
| Cycle ID | 2026-07-02__release-v6.4 |
| Release | v6.4 |
| Date | 2026-07-02 |
| Mode | standard |
| Sprints planned | 1 |
| Capacity assessment | PASS (total ~7.8d; single-sprint plan) |
| EPICs | 3 (EPIC-01, EPIC-02, EPIC-03) |
| Total stories | 13 (8 firm, 5 conditional) |
| Design Gate Required | true — 3 UI-facing stories (ST-08, ST-09, ST-10) |

---

## Scope Summary

### EPIC-01 — Backend Correctness & Security Hardening (Sprint 1)

| ST-ID | Description | BLG-ID | Class |
|-------|-------------|--------|-------|
| ST-01 | Signal generation reads deprecated `tickers` table | BLG-BE-40 | Firm |
| ST-02 | Sanitise context_opts.ticker before system prompt injection | BLG-SEC-01 | Firm |
| ST-03 | Validate ticker/market strings at signal write time | BLG-SEC-02 | Conditional |

### EPIC-02 — Governance & Audit Remediation (Sprint 1)

| ST-ID | Description | BLG-ID | Class |
|-------|-------------|--------|-------|
| ST-04 | Fix governance version-sync drift | BLG-GOV-150 | Firm |
| ST-05 | Document hygiene cleanup | BLG-GOV-151 | Conditional |
| ST-06 | Close structural reliability gaps (+ FI-P3-01/FI-P3-02/FI-P4-01 re-target) | BLG-GOV-152 | Firm |
| ST-07 | Audit & governance process fixes | BLG-GOV-153 | Firm |

### EPIC-03 — Strategy Benchmark Enhancement & UX/QA Polish (Sprint 1)

| ST-ID | Description | BLG-ID | Class |
|-------|-------------|--------|-------|
| ST-08 | Add Open Positions panel to Strategy Benchmark page | BLG-FEAT-54 | Firm |
| ST-09 | Improve AI daily briefing disclaimer text contrast | BLG-UX-01 | Conditional |
| ST-10 | Improve AI chat widget footer disclaimer contrast + test | BLG-UX-02 | Firm |
| ST-11 | Add v6.3 endpoints to api_performance_baseline.md | BLG-OPS-82 | Conditional |
| ST-12 | Playwright coverage — AI journal summary error states | TEST-GAP-EPIC-01 | Conditional |
| ST-13 | Playwright scenario coverage — Strategy Benchmark page | TEST-GAP-EPIC-03 | Firm |

---

## Key Risks

| RISK-ID | Description | Priority | Mitigation |
|---------|-------------|----------|------------|
| RISK-06 | 3 UI-facing items require Design Gate clearance before sprint planning seals | High | `run design-gate --cycle 2026-07-02__release-v6.4` must Pass (or receive documented bypass) before `plan sprint` |
| RISK-01 | Ticker source switch (BLG-BE-40) could change live signal output if active lists diverge | Medium | Verify parity via Ticker Universe Management before merge |
| RISK-04 | 4 governance-file-editing stories in EPIC-02 risk missing the CLAUDE.md §6 checklist | Medium | Run `/governance-drift` before each governance commit |
| RISK-05 | BLG-FEAT-54 new endpoint (if any) must ship contract + test.py registration same commit | Medium | Sequence backend/contract/test before frontend; use `/commit-check` |
| RISK-02 | Ticker/market validation regex could reject legitimate international formats | Low | Test regex against full current ticker_universe before deploy |
| RISK-03 | BLG-GOV-152 folds in FI-P3-01 without a dedicated backlog ID | Low | Documented explicitly in decisions record and ST-06 ACs |

---

## Pre-sprint Planning Required Decisions

The following High-priority decisions must be resolved before sprint planning seals (i.e., before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-06] Design Gate clearance for ST-08/ST-09/ST-10 (UI-facing items) — Run `run design-gate --cycle 2026-07-02__release-v6.4` and confirm Pass (or documented bypass) — Owner: Head of UX & Design

---

## Design Gate

**Design Gate Required: true**

⚠ DESIGN GATE REQUIRED before plan sprint.

3 stories classified as UI-facing with observable rendering ACs:
- ST-08 (BLG-FEAT-54): New Open Positions panel — summary line + per-position table on Strategy Benchmark page
- ST-09 (BLG-UX-01): Daily briefing disclaimer text contrast change
- ST-10 (BLG-UX-02): Chat widget footer disclaimer contrast change + new `data-testid`

**Required next step:** `run design-gate --cycle 2026-07-02__release-v6.4`

---

## Re-targeted Friction Items (resolved this cycle)

| ID | Description | Owner | Disposition |
|----|-------------|-------|--------------|
| FI-P4-01 | CI/infra `spec_references` convention to `execution_prompt.md` §3.1.A | Head of Specs Team | Folded into ST-06 (BLG-GOV-152) — concrete v6.4 target, no longer open-ended |
| FI-P3-02 | Frontend testing gate clarification (code review vs staging, wording-only ACs) | Head of Specs Team | Folded into ST-06 (BLG-GOV-152) — concrete v6.4 target |
| FI-P3-01 | Playwright strict-mode advisory to Base44 prompt draft §6 | Director of Quality / Head of Specs Team | Folded into ST-06 (BLG-GOV-152) via delegated Head of Specs Team decision — concrete v6.4 target |

---

## Outstanding Actions Before Sprint Planning

| Action | Owner | Blocking? |
|--------|-------|-----------|
| Run design gate | Head of UX & Design | YES — hard gate at sprint planning STEP -1.3 |
| Re-check SI-02 gate (stale 2026-06-09 checkpoint: 6/11 trades) | PMO Lead | No — advisory, out of this release's scope |
| Evaluate standing AI safety checklist proposal (DF-09 carry-forward) | PMO Lead | No — advisory, not actioned this cycle |

---

## Recommended Next Action

Run: `run design-gate --cycle 2026-07-02__release-v6.4`

Then: `plan sprint --cycle 2026-07-02__release-v6.4`
