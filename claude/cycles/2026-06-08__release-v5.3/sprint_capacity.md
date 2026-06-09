Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-06-09
Cycle: 2026-06-08__release-v5.3

---

# Sprint Capacity — v5.3 Spec Debt, Security Hardening & Ops Governance

## Capacity Baseline

| Field | Value |
|-------|-------|
| Sprint duration | ~12–14 working days per sprint (solo developer, evenings/weekends) |
| Available FTE | 1 (solo developer) |
| Total capacity per sprint | ~50–60 hrs |
| Warn threshold | Effort > 14 days (~70 hrs) per sprint |
| Source | workforce_capacity.md (revised baseline 2026-05-27) |

## Item Effort Mapping

### Sprint 1

| EPIC | Story | Backlog Item | Effort | Type |
|------|-------|-------------|--------|------|
| EPIC-02 | ST-08 | BLG-BE-35 — POST /digest/si05/send API key auth | S (~0.5 day / ~4 hrs) | autonomous |
| EPIC-02 | ST-09 | BLG-OPS-57 — SI-05 Telegram delivery failure alerting | S (~0.5–1 day / ~6 hrs) | autonomous |
| EPIC-02 | ST-10 | BLG-OPS-58 — CI secret scanning gate | S (~0.5–1 day / ~6 hrs) | autonomous |
| EPIC-01 | ST-01 | BLG-SPEC-53 — Contract gap resolution plan | M (~1–2 days / ~10 hrs) | autonomous |
| EPIC-01 | ST-02 | BLG-SPEC-54 — openapi.yaml completeness audit | S (~0.5–1 day / ~6 hrs) | autonomous |
| EPIC-01 | ST-03 | BLG-QA-51 — QA AC for SPEC-49–52 | S (~0.5 day / ~4 hrs) | autonomous |
| EPIC-01 | ST-04 | BLG-SPEC-49 — GET /ai/journal-summary/history contract | XS (~1–2 hrs) | autonomous |
| EPIC-01 | ST-05 | BLG-SPEC-50 — GET /analytics/compliance-metrics contract | XS (~1–2 hrs) | autonomous |
| EPIC-01 | ST-06 | BLG-SPEC-51 — GET /news/{ticker} contract | XS (~1–2 hrs) | autonomous |
| EPIC-01 | ST-07 | BLG-SPEC-52 — Watchlist endpoint contracts + test.py | S (~0.5 day / ~4 hrs) | autonomous |

**Sprint 1 total: ~39 hrs** (within Sprint 1 capacity)

### Sprint 2 (Firm)

| EPIC | Story | Backlog Item | Effort | Type |
|------|-------|-------------|--------|------|
| EPIC-03 | ST-11 | LL-v5.2-P4-01 — qa_evidence_template.md signer note | S (~1–2 hrs) | autonomous |
| EPIC-03 | ST-12 | LL-v5.2-P4-02 — execution_prompt.md STEP 5.3A | S (~1–2 hrs) | autonomous |
| EPIC-03 | ST-13 | BLG-GOV-107 — SI-02 frontend activation criteria | S (~0.5–1 day / ~5 hrs) | autonomous |
| EPIC-03 | ST-14 | BLG-GOV-108 — AI model pin update policy | S (~0.5–1 day / ~5 hrs) | autonomous |
| EPIC-03 | ST-15 | BLG-GOV-109 — AI audit log retention policy | S (~0.5 day / ~4 hrs) | autonomous |
| EPIC-03 | ST-16 | BLG-GOV-110 — Arc 4 trade_plan data completeness audit | S (~0.5–1 day / ~5 hrs) | autonomous |
| EPIC-03 | ST-17 | BLG-GOV-104 — strategy_rules.md §11 parameter validation | M (~1–2 days / ~10 hrs) | autonomous |
| EPIC-03 | ST-23 | BLG-GOV-113 — SI-05 effectiveness review protocol | S (~0.5–1 day / ~5 hrs) | autonomous |
| EPIC-03 | ST-24 | BLG-GOV-114 — si05_digest_log schema validation | S (~0.5 day / ~4 hrs) | autonomous |
| EPIC-04 | ST-18 | BLG-QA-52 — Tax year P&L boundary edge case validation | S (~0.5–1 day / ~5 hrs) | autonomous |
| EPIC-04 | ST-19 | BLG-QA-53 — SI-05 digest Playwright E2E coverage | M (~1–2 days / ~10 hrs) | autonomous |
| EPIC-04 | ST-20 | BLG-QA-54 — Playwright coverage matrix update post-v5.2 | S (~0.5 day / ~4 hrs) | autonomous |
| EPIC-04 | ST-21 | BLG-FE-66 — Red Flag Journal post-launch UX review | S (~0.5–1 day / ~5 hrs) | autonomous |
| EPIC-04 | ST-22 | BLG-FE-67 — BLG-FE-64 visual design scope definition | S (~0.5 day / ~4 hrs) | autonomous |

**Sprint 2 total: ~71 hrs** (at upper bound — within extended WARN acceptance range; P3 item ST-21 deferrable if capacity tightens)

### Sprint 2 Conditionals Included

| ST-ID | Item | Gate confirmed |
|-------|------|----------------|
| ST-23 | BLG-GOV-113 — SI-05 effectiveness review protocol | Gate "Before 2026-07-01" — window open at planning date 2026-06-09 |
| ST-24 | BLG-GOV-114 — si05_digest_log schema validation | Gate "Before 2026-07-01" — window open at planning date 2026-06-09 |

## Capacity vs Effort Summary

| Sprint | Estimated Effort | Available Capacity | Status |
|--------|-----------------|-------------------|--------|
| Sprint 1 (EPIC-02 + EPIC-01) | ~39 hrs | ~50–60 hrs | ✅ PASS |
| Sprint 2 (EPIC-03 + EPIC-04) | ~71 hrs | ~50–60 hrs | ⚠️ WARN — upper bound; defer ST-21 (P3) or ST-17 (data-limited M) if capacity tightens |
| **Overall** | **~110 hrs** | **~100–120 hrs** | **⚠️ WARN — 2-sprint phasing required; consistent with release plan capacity assessment** |

## Conditional (Deferred)

| EPIC | Story | Effort | Gate Condition |
|------|-------|--------|----------------|
| EPIC-04 | ST-25 (BLG-FE-64) | S | Gate: 2026-06-21 — not yet reached at planning time (2026-06-09); defer to post-gate assessment |

> **Gate re-invocation:** If the ST-25 gate condition above is met during the sprint, do not add the item informally. Invoke the amendment cycle (`amend cycle --cycle 2026-06-08__release-v5.3 --reason "BLG-FE-64 gate cleared 2026-06-21"`) to add it to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.

## Sprint 2 Capacity Advisory

Sprint 2 at ~71 hrs is at the upper bound of available capacity. If execution pace tightens:
- **First to defer:** ST-21 (BLG-FE-66 — P3, UX review document)
- **Second to defer:** ST-17 (BLG-GOV-104 — M effort, data-limited: <20 trades may yield "insufficient data" finding regardless)
- Both items can move to v5.4 without sprint-goal impact
