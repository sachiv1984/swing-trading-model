**Owner:** Head of Specs Team
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-04

---

# Stage 2 — Backlog Health Review

**Cycle:** 2026-03-04__item-3.4
**Date:** 2026-03-04
**Authorities:** Head of Specs Team (process), Product Owner (planning ownership)

---

## 1. Completed Items — Confirmed Closed

The following items are complete and correctly marked. No action required.

| Item | Closed |
|------|--------|
| BLG-TECH-01 — Sharpe variance + Capital Efficiency | 2026-02-21 |
| BLG-TECH-02 — Validation severity model | 2026-02-21 |
| BLG-TECH-03 — Service layer consolidation | 2026-02-21 |
| BLG-TECH-04 — CI/CD GitHub Actions | 2026-03-03 |
| BLG-TECH-06 — sharpe_ratio_trade_method canonicalised | 2026-03-03 |
| BLG-TECH-08 — portfolio_endpoints.md alignment | 2026-03-03 |
| BLG-TECH-09 — holding_days in GET /trades | 2026-03-03 |
| BLG-FEAT-01–07 — Quick Wins Bundle (6 features) | 2026-03-01 |
| 4.1a — CSV Export (killed — superseded) | 2026-03-01 |
| v1.7 Release Slice (all 8 items) | 2026-03-03 |

---

## 2. Obsolete Items

**None identified.** All completed items are accurately labelled. No zombie or stale-incomplete items found.

---

## 3. Duplicates

**One near-duplicate identified:**

- **IDEA-financial-reporting-20260304-01 (UK Tax Year Performance Summary Endpoint)** vs **4.1b — Tax-Year P&L Statement** (active roadmap item). These are substantively the same idea. The roadmap item already captures the intent; the idea submission adds no new scope. Handled in STEP 4 as Reject.

**No internal backlog duplicates found.**

---

## 4. Strategic Alignment Review

All active backlog items are strategically aligned.

| Item | Alignment | Concern |
|------|-----------|---------|
| BLG-TECH-05 (Prometheus) | ✅ P3/v2.1 — appropriate | None |
| BLG-FEAT-03 (Slippage Tracking) | ✅ Still relevant | Data model update needed first |
| BLG-FEAT-08 (Compliance Metrics) | ✅ Gate for 5.1 | Metrics owner availability check required at v1.9 |
| BLG-SPEC-D1 (API Contracts README) | ✅ P3 quick win | Trivial — 15 min update |
| BLG-SPEC-D2 (settings method drift) | ⚠️ P1 — **accumulating risk** | PUT vs PATCH mismatch; clients using spec will call wrong path. Decision required. |
| BLG-SPEC-D3 (GET /market/status undocumented) | ⚠️ P2 — live endpoint without spec | Endpoint live and used by frontend; no canonical spec exists |
| BLG-SPEC-D7 (openapi.yaml at v1.8.1) | ⚠️ P2 — reference artefact stale | Three contracts at v1.9.0; openapi.yaml not updated during EPIC-06 |
| BLG-SPEC-G1 (settings_model.md missing) | ⚠️ P2 — open since 2026-02-21 | 12+ days without action; blocked on D2 decision |
| BLG-SPEC-G2 (Error Response Standard) | ⚠️ P2 — open since 2026-02-21 | 12+ days without action; untestable error shapes |

---

## 5. Quick Wins Being Ignored

The following are P3 / low-effort items that have been accumulating without attention:

| Item | Effort | Days Open |
|------|--------|-----------|
| BLG-SPEC-D1 (API README version) | ~15 min | 1 |
| BLG-SPEC-G3 (Specs_Index missing structured logging) | ~15 min | 1 |
| BLG-SPEC-D9 (broken lifecycle guide cross-references) | ~30 min | 1 |
| BLG-SPEC-D8 (System_status_report.md missing header) | ~15 min | 1 |
| TEST-GAP-EPIC-06 (3 QA scenario gaps from v1.7) | ~2 hrs | 1 |

**Recommendation:** Bundle these as a v1.8 pre-work task or early sprint task. Total effort: ~3 hours. All P3 except TEST-GAP which is a QA gap.

---

## 6. Technical Debt Accumulation

**Concerning pattern identified:** The v1.7 release generated 9 new SPEC backlog items (D1–D9, G1–G5 minus pre-existing). This is the first release where spec debt items outnumber closed items in the SPEC category. Two patterns:

1. **Decision-dependent debt:** BLG-SPEC-D2 (settings method) and BLG-SPEC-G1 (settings model) are blocked on each other. The method decision should be forced in v1.8 pre-alignment — it has been open 12+ days.

2. **Reference artefact drift:** openapi.yaml (BLG-SPEC-D7) was explicitly required to be updated per Specs_Index.md §4 during EPIC-06 and was not. This was a missed step in EPIC-06 execution. It has accumulated risk: consumers relying on openapi.yaml for 3 endpoints will see wrong schemas.

**PMO flag:** The spec debt accumulation rate should be monitored. If it continues at this rate, a dedicated spec debt cycle will be required before v2.0.

---

## 7. Summary

| Category | Count | Status |
|----------|-------|--------|
| Correctly closed | 17 | ✅ No action |
| Obsolete | 0 | — |
| Duplicates (handled in STEP 4) | 1 | ❌ Reject in STEP 4 |
| Active backlog — P0/P1 (urgent) | 1 (D2) | ⚠️ Force decision in v1.8 |
| Active backlog — P2 (medium) | 5 (D3, D7, G1, G2, G3) | Schedule in v1.8 |
| Active backlog — P3 (low/quick wins) | 6 (D1, D4, D5, D6, D8, D9, G4, G5) | Bundle as quick wins |
| Test coverage gaps | 1 (TEST-GAP-EPIC-06) | QA to action |
| Deferred / v2.1 | 8 | Hold at current priority |
| Explicitly out of scope | 6 | Permanent |
