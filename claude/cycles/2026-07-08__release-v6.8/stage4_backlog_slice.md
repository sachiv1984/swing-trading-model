**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v6.8
**Cycle:** 2026-07-08__release-v6.8
**Last Updated:** 2026-07-08
**Sprint Backlog Source:** This slice is authoritative. Sprint Planning Engine reads this file at Phase 2.

---

# v6.8 Backlog Slice — 2026-07-08__release-v6.8

<!-- release-plan-marker: RP:v6.8:2026-07-08__release-v6.8 -->

---

## EPIC-01 — Production Correctness, Security & Infrastructure

**Purpose:** Resolve the only P1 correctness bug in the backlog (blocking SI-02 gate resolution), a SQL-column-name injection-adjacent security fix, a quick anomaly review, and the 2-cycle-recurring credential gap blocking data-gate verification.

**Sprint assignment:** Sprint 1

**Maps to:** S2-01, S2-02, S2-03, S2-04

---

### ST-01 — Investigate `trade_plans.position_id` never populated in production (BLG-BE-46)

**Type:** Firm
**Effort:** M (~1–2 days)
**Owner:** Backend Engineering Patterns Owner; PMO Lead
**Backlog ref:** BLG-BE-46
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-01

**Context:** `GET /trades` reports 20 closed trades; `GET /trade-plans` reports 11 plans, all with `position_id: null`; `GET /analytics/arc5-compliance` independently confirms `trade_plan_adherence_rate: 0.0`. This has silently distorted the SI-02 gate condition across many cycles.

**Acceptance criteria:**
- AC-01: Root cause documented (bug / workflow gap / other)
- AC-02: If a bug: fix implemented and verified — a newly closed trade with an associated plan shows `position_id` set, confirmed via API
- AC-03: Decision recorded on whether historical backfill was performed or explicitly deferred
- AC-04: `current_roadmap.md`'s SI-02 gate row reflects the corrected linked-plan count once this resolves

---

### ST-02 — Unvalidated dict keys used as SQL column names in `database.update_signal()` (BLG-SEC-08)

**Type:** Firm
**Effort:** S (~0.5 day)
**Owner:** Backend Engineering Patterns Owner; Cybersecurity & Trust Lead
**Backlog ref:** BLG-SEC-08
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-01

**Acceptance criteria:**
- AC-01: Dict keys used as SQL column names in `database.update_signal()` are validated against an allowlist of known columns before use
- AC-02: Regression test added confirming rejection of an unrecognised key

---

### ST-03 — Manual review of existing signals for anomalous ticker/market values (BLG-SEC-07)

**Type:** Firm
**Effort:** XS (<1h)
**Owner:** Cybersecurity & Trust Lead
**Backlog ref:** BLG-SEC-07
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-01

**Acceptance criteria:**
- AC-01: Existing signal records reviewed for anomalous ticker/market values; findings documented; any anomalies filed as follow-up BLG items

---

### ST-04 — Provision application `X-API-Key` for governed routines (BLG-OPS-99)

**Type:** Firm
**Effort:** S (~0.5 day)
**Owner:** Infrastructure & Operations Owner; PMO Lead
**Backlog ref:** BLG-OPS-99
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-01

**Context:** Resolves LP-08 (v6.7 closure carry-forward) — no governed routine currently holds an application-level API key, forcing gate conditions like SI-02's trade-count check to rely on self-report.

**Acceptance criteria:**
- AC-01: Key provisioned and documented (storage location, e.g. `~/.api_keys`)
- AC-02: A governed routine successfully uses it to directly confirm a gate condition without relying on self-report

---

## EPIC-02 — Product Value Pull-Forward (Mandatory)

**Purpose:** Mandatory response to the 2026-07-08 rebalance's Product Value Alert (ratio 0.26, below the 0.30 floor) — both items were named as pull-forward candidates and approved.

**Sprint assignment:** Sprint 1

**Maps to:** S2-05, S2-06

---

### ST-05 — Trade tagging and tag-based performance filtering (BLG-FEAT-52)

**Type:** Firm
**Effort:** S (~2–3 days, descoped from L)
**Owner:** Product Owner; Head of UX & Design; Head of Engineering
**Backlog ref:** BLG-FEAT-52
**Delegation class:** delegated_frontend
**Sprint:** Sprint 1
**EPIC:** EPIC-02

**Context:** Descoped 2026-07-08 to a tags-only scope with no dependency on `trade_annotations`/PO-02. New endpoints — must be registered in `docs/reference/openapi.yaml` and `docs/specs/api_contracts/` in the same commit (CLAUDE.md hard rule), and new routes registered in `backend/routers/test.py` in the same commit.

**Acceptance criteria:**
- AC-01: User can add/remove tags on any trade plan
- AC-02: `GET /analytics/tag-performance` returns win rate and average R broken down by tag
- AC-03: PerformanceAnalytics page surfaces tag-based filter controls
- AC-04: Confirmed at sprint planning that `trade_tags` has no foreign-key or service dependency on `trade_annotations`/PO-02 structures
- AC-05: Playwright coverage or recorded staging sign-off for the tag input and filter UI (CLAUDE.md frontend-visible-change rule)

---

### ST-06 — SI-02 gate visibility indicator, Reports page (BLG-FEAT-71)

**Type:** Firm
**Effort:** S (~1–2 days)
**Owner:** Product Owner; Head of UX & Design
**Backlog ref:** BLG-FEAT-71
**Delegation class:** delegated_frontend
**Sprint:** Sprint 1
**EPIC:** EPIC-02

**Context:** No new data model — reads existing `GET /trades`, `GET /trade-plans`, `GET /analytics/arc5-compliance`. Must reflect ST-01's finding (0 linked trades) if `BLG-BE-46` remains unresolved at build time.

**Acceptance criteria:**
- AC-01: Indicator shows total closed trades and total trade-plan-linked closed trades as two distinct numbers
- AC-02: Indicator shows MET/NOT MET for each of the 3 SI-02 gate conditions
- AC-03: Values read live from existing endpoints, not hardcoded
- AC-04: Confirmed at sprint planning that AC-01/02 correctly reflect ST-01's finding if still unresolved
- AC-05: Playwright coverage or recorded staging sign-off for the indicator panel (CLAUDE.md frontend-visible-change rule)

---

## EPIC-03 — Spec & Governance Debt Clearance

**Purpose:** Clear 4 spec-debt items stale 4+ release cycles and resolve 7 further ungated low-effort items, including 3 with 6–12 missed release targets and no PO re-deferral on record.

**Sprint assignment:** Sprint 1

**Maps to:** S2-07, S2-08, S2-09, S2-10, S2-11, S2-12, S2-13, S2-14, S2-15, S2-16, S2-17

---

### ST-07 — Dashboard homepage visual hierarchy review post-v6.2 (BLG-SPEC-58)

**Type:** Firm | **Effort:** S (~0.5 day) | **Owner:** Head of UX & Design | **Backlog ref:** BLG-SPEC-58 | **Delegation class:** autonomous | **Sprint:** Sprint 1 | **EPIC:** EPIC-03

**Acceptance criteria:**
- AC-01: Visual hierarchy review of dashboard homepage completed and documented against post-v6.2 layout changes; any gaps filed as follow-up items

---

### ST-08 — R-multiple cross-currency normalization specification (BLG-SPEC-59)

**Type:** Firm | **Effort:** S (~0.5 day) | **Owner:** Head of Specs Team; Metrics & Analytics Owner | **Backlog ref:** BLG-SPEC-59 | **Delegation class:** autonomous | **Sprint:** Sprint 1 | **EPIC:** EPIC-03

**Acceptance criteria:**
- AC-01: Canonical specification produced defining R-multiple normalization across currencies
- AC-02: Reviewed/signed off by Metrics & Analytics Owner

---

### ST-09 — Trailing stop visual indicator frontend specification (BLG-SPEC-60)

**Type:** Firm | **Effort:** S (~0.5 day) | **Owner:** Head of Specs Team; Head of UX & Design | **Backlog ref:** BLG-SPEC-60 | **Delegation class:** autonomous | **Sprint:** Sprint 1 | **EPIC:** EPIC-03

**Acceptance criteria:**
- AC-01: Frontend specification produced for the trailing-stop visual indicator (states, colours, placement)
- AC-02: Reviewed/signed off by Head of UX & Design

---

### ST-10 — Trailing stop effectiveness metric definition (BLG-SPEC-61)

**Type:** Firm | **Effort:** S (~0.5 day) | **Owner:** Head of Specs Team; Metrics & Analytics Owner | **Backlog ref:** BLG-SPEC-61 | **Delegation class:** autonomous | **Sprint:** Sprint 1 | **EPIC:** EPIC-03

**Acceptance criteria:**
- AC-01: Metric definition produced for trailing-stop effectiveness, consistent with existing R-multiple/analytics conventions
- AC-02: Tooling assessment recorded on whether version tagging adds drift-detection value beyond existing `quality_gate.yml` OpenAPI validation

---

### ST-11 — Fix 12 dark spec files surfaced by Playwright glob discovery (BLG-QA-64)

**Type:** Firm | **Effort:** M (~1 day) | **Owner:** Director of Quality | **Backlog ref:** BLG-QA-64 | **Delegation class:** autonomous | **Sprint:** Sprint 1 | **EPIC:** EPIC-03

**Acceptance criteria:**
- AC-01: Each of the 12 dark spec files investigated; each either fixed (registered/wired up) or deleted with rationale
- AC-02: No remaining dark spec files after this story per the same glob-discovery method

---

### ST-12 — CI inline OpenAPI drift detection for `api_performance_baseline.md` (BLG-GOV-134)

**Type:** Firm | **Effort:** S (~0.5 day) | **Owner:** Infrastructure & Operations Owner | **Backlog ref:** BLG-GOV-134 | **Delegation class:** autonomous | **Sprint:** Sprint 1 | **EPIC:** EPIC-03

**Acceptance criteria:**
- AC-01: CI check added that flags new/removed endpoints in `openapi.yaml` not yet reflected in `api_performance_baseline.md`
- AC-02: Check runs in the existing quality-gate workflow

---

### ST-13 — Log Anthropic API token usage and cost per morning briefing call (BLG-OPS-74)

**Type:** Firm | **Effort:** S (<0.5 day) | **Owner:** FinOps & Resource Architect | **Backlog ref:** BLG-OPS-74 | **Delegation class:** autonomous | **Sprint:** Sprint 1 | **EPIC:** EPIC-03

**Acceptance criteria:**
- AC-01: Each morning briefing call logs token usage and estimated cost
- AC-02: Logged data queryable/reviewable for cost-trend analysis

---

### ST-14 — Refactor `Watchlist.js` to ESLint compliance (BLG-FE-77)

**Type:** Firm | **Effort:** M (~1–2 days) | **Owner:** Head of Engineering | **Backlog ref:** BLG-FE-77 | **Delegation class:** autonomous | **Sprint:** Sprint 1 | **EPIC:** EPIC-03

**Context:** Pure refactor, no behaviour change — no observable UI ACs, so no Playwright/staging requirement triggered.

**Acceptance criteria:**
- AC-01: `Watchlist.js` passes ESLint with zero warnings/errors under the project's existing configuration
- AC-02: No functional or visual behaviour change (confirmed by existing test suite passing unmodified)

---

### ST-15 — `BLG-OPS-13` v5.1–v5.4 endpoint baseline extension (BLG-OPS-61)

**Type:** Firm | **Effort:** S (~0.5–1 day) | **Owner:** Infrastructure & Operations Owner | **Backlog ref:** BLG-OPS-61 | **Delegation class:** autonomous | **Sprint:** Sprint 1 | **EPIC:** EPIC-03

**Acceptance criteria:**
- AC-01: All v5.1/v5.2 new endpoints have latency entries in `api_performance_baseline.md`
- AC-02: Consistent with existing measurement methodology
- AC-03: Infrastructure & Operations Owner sign-off

---

### ST-16 — Extract Playwright test standard from `execution_prompt.md` to `shared_standards.md` (BLG-GOV-123)

**Type:** Firm | **Effort:** XS (~1 hour) | **Owner:** Head of Specs Team | **Backlog ref:** BLG-GOV-123 | **Delegation class:** autonomous | **Sprint:** Sprint 1 | **EPIC:** EPIC-03

**Context:** Governance-file edit — CLAUDE.md §6 checklist applies same-commit (version bump both files, OPERATIONAL_GUIDE §14 sync, `prompt_change_log.md` entry).

**Acceptance criteria:**
- AC-01: Section 14 content moved to `shared_standards.md` under a new heading
- AC-02: `execution_prompt.md` Section 14 replaced with a reference line
- AC-03: Version bump on both files; changelog entries appended; OPERATIONAL_GUIDE §14 synced
- AC-04: Head of Specs Team sign-off

---

### ST-17 — System threat model document (BLG-OPS-71)

**Type:** Firm | **Effort:** S (~1 day) | **Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner | **Backlog ref:** BLG-OPS-71 | **Delegation class:** autonomous | **Sprint:** Sprint 1 | **EPIC:** EPIC-03

**Acceptance criteria:**
- AC-01: `docs/security/threat_model.md` produced covering attack surfaces, data classifications, threat actors, current mitigations, and identified gaps
- AC-02: Any gaps produce separate BLG items before sign-off
- AC-03: Reviewed and signed off by Cybersecurity & Trust Lead and Infrastructure & Operations Owner

---

## Summary

| EPIC | Stories | Firm | Conditional | Total effort estimate |
|------|---------|------|-------------|------------------------|
| EPIC-01 | ST-01, ST-02, ST-03, ST-04 | 4 | 0 | ~2.6 days |
| EPIC-02 | ST-05, ST-06 | 2 | 0 | ~4.0 days |
| EPIC-03 | ST-07–ST-17 | 11 | 0 | ~7.3 days |
| **Total** | **17** | **17** | **0** | **~13.9 days** |
