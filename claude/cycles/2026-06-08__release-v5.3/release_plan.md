Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v5.3
Cycle: 2026-06-08__release-v5.3
Last Updated: 2026-06-08

---

# Release Plan — v5.3 Spec Debt, Security Hardening & Ops Governance

## Readiness

| Check | Result |
|-------|--------|
| Roadmap RA:v5.3 section | PASS — present (STEP 8.1 Option(a), DL-040, 2026-06-08__scheduled) |
| Post-ship complete | PASS — v5.2 closed 2026-06-08 |
| Next cycle unblocked | PASS |
| Design gate pre-assessment (BLG-GOV-111) | NOT REQUIRED — 0 new UI/UX components in all 22 firm + 3 conditional candidates |
| Prompt change log integrity | PASS — all 7 Class 6 prompt versions recorded |
| Stale backlog lock | PASS — no lock |
| Carry-forward items | 2 items from v5.2 (CF-1/CF-2) — incorporated as ST-11/ST-12 |

---

## Scope

| S2-ID | Priority | Backlog Item | Effort | EPIC |
|-------|----------|-------------|--------|------|
| S2-01 | P1 | BLG-SPEC-53 — Contract gap resolution plan for SPEC-49–52 | M | EPIC-01 |
| S2-02 | P1 | BLG-SPEC-54 — openapi.yaml completeness audit vs all 50 routes | S | EPIC-01 |
| S2-03 | P2 | BLG-QA-51 — QA acceptance criteria for SPEC-49–52 contract stories | S | EPIC-01 |
| S2-04 | P2 | BLG-SPEC-49 — GET /ai/journal-summary/history contract + openapi.yaml | XS | EPIC-01 |
| S2-05 | P2 | BLG-SPEC-50 — GET /analytics/compliance-metrics contract + openapi.yaml | XS | EPIC-01 |
| S2-06 | P2 | BLG-SPEC-51 — GET /news/{ticker} contract + openapi.yaml | XS | EPIC-01 |
| S2-07 | P2 | BLG-SPEC-52 — Watchlist endpoint contracts + openapi.yaml + test.py | S | EPIC-01 |
| S2-08 | P2 | BLG-BE-35 — POST /digest/si05/send API key authentication | S | EPIC-02 |
| S2-09 | P1 | BLG-OPS-57 — SI-05 Telegram delivery failure alerting | S | EPIC-02 |
| S2-10 | P1 | BLG-OPS-58 — CI secret scanning gate (gitleaks) | S | EPIC-02 |
| S2-11 | P1 | LL-v5.2-P4-01 — qa_evidence_template.md signer format note (CF-1) | S | EPIC-03 |
| S2-12 | P1 | LL-v5.2-P4-02 — execution_prompt.md STEP 5.3A SSR sub-step (CF-2) | S | EPIC-03 |
| S2-13 | P2 | BLG-GOV-107 — SI-02 frontend activation criteria precision | S | EPIC-03 |
| S2-14 | P2 | BLG-GOV-108 — AI model pin update policy | S | EPIC-03 |
| S2-15 | P2 | BLG-GOV-109 — AI audit log retention policy | S | EPIC-03 |
| S2-16 | P2 | BLG-GOV-110 — Arc 4 trade_plan data completeness audit | S | EPIC-03 |
| S2-17 | P2 | BLG-GOV-104 — strategy_rules.md §11 parameter validation | M | EPIC-03 |
| S2-18 | P2 | BLG-QA-52 — Tax year P&L boundary edge case validation | S | EPIC-04 |
| S2-19 | P2 | BLG-QA-53 — SI-05 digest Playwright E2E coverage (≥3 scenarios) | M | EPIC-04 |
| S2-20 | P2 | BLG-QA-54 — Playwright coverage matrix update post-v5.2 | S | EPIC-04 |
| S2-21 | P3 | BLG-FE-66 — Red Flag Journal post-launch UX review document | S | EPIC-04 |
| S2-22 | P2 | BLG-FE-67 — BLG-FE-64 visual design review scope definition | S | EPIC-04 |

**Conditional scope (add if gates clear before sprint planning seals):**

| S2-ID | Gate | Item |
|-------|------|------|
| S2-C1 | Before 2026-07-01 | BLG-GOV-113 — SI-05 effectiveness review protocol |
| S2-C2 | Before 2026-07-01 | BLG-GOV-114 — si05_digest_log schema validation |
| S2-C3 | 2026-06-21 | BLG-FE-64 — RFJ visual design review pre-brief |

**Explicitly deferred:**

| Item | Reason | Target |
|------|--------|--------|
| BLG-GOV-106 | OA-RP-01: gate check required before sprint planning seals (PT-04 trade count); not a sprint story | Before sprint planning seals |
| BLG-GOV-111 | Resolved inline: design gate pre-assessment complete (NOT REQUIRED) | Done |
| BLG-GOV-105 | Provisional-Target: Unscheduled; Arc 6 not yet on Next horizon | Future release |
| BLG-GOV-112 | Gate: 2026-07-04 effectiveness review (too late for v5.3 sprint) | v5.4 |
| BLG-OPS-59 | Gate: 4 weeks production operation (~2026-07-04) | v5.4 |

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01–S2-07 | Head of Specs Team | RISK-01 | Sprint 1; merge before EPIC-04 |
| EPIC-02 | S2-08–S2-10 | Head of Engineering | RISK-04 | Sprint 1; parallel with EPIC-01 |
| EPIC-03 | S2-11–S2-17 | Head of Specs Team | RISK-02 | Sprint 2; merge before EPIC-04 |
| EPIC-04 | S2-18–S2-22 | Director of Quality | RISK-03 | Sprint 2; after EPIC-01 contracts committed |

EPIC-01 note: BLG-SPEC-49–52 contract authoring depends on BLG-SPEC-53 (resolution plan) completing first within EPIC-01. BLG-QA-51 (QA AC definition) should complete alongside BLG-SPEC-53/54 to inform acceptance criteria for the contract stories.

EPIC-04 note: BLG-QA-54 (coverage matrix update) must occur after EPIC-01 contracts are committed (counts new contract docs toward coverage).

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|-----------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Spec contract authoring may surface additional openapi.yaml + test.py gaps beyond the 6 known; CLAUDE.md §2 compliance requires all three (contract + openapi.yaml + test.py) in same sprint | Medium | BLG-SPEC-53 resolution plan + BLG-SPEC-54 audit scoped to identify scope before authoring begins | null |
| RISK-02 | EPIC-03 | BLG-GOV-104 strategy_rules.md parameter validation requires real trade data; current closed trade count (~6) may limit validation depth | Medium | Accept "insufficient data" for items requiring >20 trades; document as advisory finding | null |
| RISK-03 | EPIC-04 | PT-04 gate (20+ closed trades) may clear before sprint planning seals (OA-RP-01), requiring PT-04 (M effort) to enter scope late | Medium | OA-RP-01 mandatory before sprint planning seals; if gate cleared: EPIC-04 scope expands and capacity re-assessed | null |
| RISK-04 | EPIC-02 | BLG-OPS-58 (CI secret scanning) may flag existing false positives in test fixtures requiring allowlist calibration | Low | Scope includes allowlist configuration step; false positive handling documented in AC | null |

---

## Integrity Validation — 3.5 Local Model Integrity

- All S2-01–S2-22 scope items have S2-IDs assigned ✅
- All EPICs declared Maps to S2 IDs ✅
- All RISK-IDs referenced in EPIC table appear in Risk Register ✅
- No orphaned S2 IDs (every S2 maps to exactly one EPIC) ✅
- No orphaned EPIC IDs (every EPIC references valid S2 items) ✅
- Conditional items (S2-C1/C2/C3) documented separately ✅

**Result: PASS**

---

## Capacity Check

**Effort estimates:**

| EPIC | Stories | Types | Estimate (hrs) |
|------|---------|-------|----------------|
| EPIC-01 | 7 | 3×XS + 4×S | 20–28 hrs |
| EPIC-02 | 3 | 3×S | 12–18 hrs |
| EPIC-03 | 7 | 6×S + 1×M | 36–50 hrs |
| EPIC-04 | 5 | 1×M + 4×S | 22–30 hrs |
| **Total** | **22** | | **90–126 hrs** |

Available capacity (solo-dev evenings, 2-sprint plan): ~80–100 hrs.

**Result: WARN** — total estimate at mid-point (~108 hrs) exceeds single-sprint available capacity. 2-sprint phasing required.

### Phasing Recommendation

**Sprint 1 — API Contract Debt + Security Hardening (EPIC-01 + EPIC-02):**
- EPIC-01: 7 stories — S2-01 through S2-07 (~24 hrs)
- EPIC-02: 3 stories — S2-08 through S2-10 (~15 hrs)
- Sprint 1 total: 10 stories, ~39 hrs (within capacity)
- Merge order: EPIC-02 → EPIC-01

**Sprint 2 — Governance Patches + QA/Testing (EPIC-03 + EPIC-04):**
- EPIC-03: 7 stories — S2-11 through S2-17 (~43 hrs)
- EPIC-04: 5 stories — S2-18 through S2-22 (~26 hrs) + conditionals S2-C1/C2/C3
- Sprint 2 total: 12 firm stories, ~69 hrs (at upper bound — may require phasing within Sprint 2)
- Merge order: EPIC-03 → EPIC-04
- Sprint 2 gate: EPIC-04 BLG-QA-54 requires EPIC-01 contract authoring merged to main first

Ordering rationale: P1 spec debt and security hardening in Sprint 1 addresses highest-risk items first. Governance patches (CF-1/CF-2) in Sprint 2 EPIC-03 because they are smaller operational improvements. QA testing (EPIC-04) last to capture post-EPIC-01 contract additions in coverage matrix.

**Sprint 2 advisory:** If Sprint 2 effort exceeds available capacity, defer BLG-FE-66 (P3) and/or BLG-GOV-104 (M, data-limited) to v5.4 — both have lowest execution risk.
