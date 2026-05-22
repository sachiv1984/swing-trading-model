**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Published
**Cycle:** 2026-05-22__release-v4.0
**Release:** v4.0
**Published:** 2026-05-22

---

# Release Plan — v4.0

**Theme:** Arc 5 Analytics Foundation + Spec Closure + Gemini Compliance

---

## Readiness

| Check | Result |
|-------|--------|
| Prior cycle closed | ✅ v3.9 Closed_with_actions (completed_cycle_count=25) |
| Prior cycle lessons applied | ✅ OA-03 (execution_prompt v3.27) + OA-04 (sprint_planning v3.6) applied |
| v4.0 on roadmap | ✅ `Next planned release: v4.0` confirmed |
| Backlog populated | ✅ DL-033 added 32 items; v4.0 candidates identified |
| Arc 5 status | SI-01 ✅ v3.8, SI-03 ✅ v3.9; SI-02/04/05 data-gated |
| SPEC-33/SPEC-34 | ✅ Already complete (OA-01+OA-02, b115b9b4 2026-05-22) |
| Locks | ✅ None held |

**STEP 1.2 Provisional-Target Advisory:** 11 items carry `Provisional-Target: v4.0`. Majority are from DL-033 (2026-05-22 rebalance). BLG-SPEC-33 and BLG-SPEC-34 are already complete.

**STEP 1.3 Design Dependency Scan:** 2 items flagged — BLG-FEAT-36 (new metric definition, Metrics owner sign-off) and EPIC-04/PT-04 (score badge UX, Head of UX & Design). Noted in Pre-sprint Required Decisions.

---

## Scope

| ID | Item | Source | Priority | Effort | Notes |
|----|------|--------|----------|--------|-------|
| S2-01 | Arc 5 analytics metrics — SI-01 pass/fail rate by rule, red flag frequency, trade plan adherence rate | BLG-FEAT-36, FEAT-37, FEAT-39 | P2 | M+S+S | No gate; SI-01 and SI-03 shipped; plan_id linkage in use |
| S2-02 | E2E Playwright test SI-01→SI-03 integration path | BLG-QA-25 | P2 | S | No gate; coverage gap for RFJ pipeline |
| S2-03 | Ticker symbol validation on add | BLG-BE-15 | P1 | S | P1; no gate; prevents junk universe entries |
| S2-04 | Red flag endpoint auth/PII review | BLG-GOV-37 | P2 | XS | Security governance; post-v3.9 hygiene |
| S2-05 | AI governance — Gemini audit trail + cost tracking | BLG-GOV-35, BLG-OPS-26 | P2 | M+S | Gemini in production since v3.8; no audit trail exists |
| S2-06 | CI/CD — Automated staging re-deploy on main merge | BLG-OPS-27 | P2 | M | Reduces manual staging sync; free-tier impact noted (RISK-03) |
| S2-07 (cond.) | PT-04 Setup Quality Score — backend + frontend | BLG-FEAT-25 | P2 | L+M | Conditional: gate = 20+ closed trades; PO to confirm before sprint planning |

**Explicitly deferred from v4.0:**

| Item | Reason |
|------|--------|
| SI-02 Behavioural Drift Detection | Data-gated: requires PO-03 data, which requires PO-02 (6+ months AI journals — not met until ~Nov 2026) |
| SI-04 Strategy Version Comparison | Data-gated: requires version-tagged trade history |
| SI-05 Weekly Strategy Integrity Digest | Data-gated: depends on SI-02 |
| BLG-SPEC-37 SI-02 data schema pre-def | Gate: SI-02 sprint planning imminent — not imminent this cycle |
| BLG-BE-17 SI-02 query pre-design | Gate: SI-02 sprint planning imminent |
| BLG-BE-18 Arc 5 arch review | Gate: SI-02 sprint planning imminent |
| BLG-GOV-39 SI-02 §13 review | Gate: SI-02 sprint planning imminent |
| BLG-FE-40 RFJ filter state | Gate: 30 days post-v3.9 use — not met (v3.9 shipped today) |
| BLG-SPEC-33, BLG-SPEC-34 | Already complete (OA-01+OA-02, 2026-05-22) — backlog archive pending groom |
| Arc 4 remainder (PO-02/03/04) | Data-gated: 6+ months journal history |
| All Arc 6 items | Horizon: 100+ trades required |

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01, S2-02 | Metrics & Analytics Owner; QA Lead | RISK-02 (metric endpoint scope) | None; self-contained Arc 5 analytics work |
| EPIC-02 | S2-03, S2-04 | Head of Backend Engineering; Cybersecurity Lead | None | None; independent; ST-04 (GOV-37) is XS review |
| EPIC-03 | S2-05, S2-06 | AI Compliance Officer; FinOps; Infrastructure Owner | RISK-03 (Render free-tier cost) | OPS-27 enables BLG-OPS-25 (smoke test) downstream |
| EPIC-04 (cond.) | S2-07 | Head of Backend Engineering; Head of UX & Design | RISK-01 (PT-04 gate) | Conditional; requires PO gate confirmation before sprint planning seals |

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-04 | PT-04 gate (20+ closed trades) may not be met — PO has not confirmed count at release planning time | High | EPIC-04 deferred to conditional; PO to run BLG-GOV-33 audit before sprint planning seals | null |
| RISK-02 | EPIC-01 | BLG-FEAT-36 (SI-01 validation pass/fail rate) requires new backend endpoint + metric canonical definition; scope may expand beyond S effort if endpoint design is complex | Medium | Metrics & Analytics Owner to confirm metric definition at design gate / pre-sprint; size as M | null |
| RISK-03 | EPIC-03 | OPS-27 (staging auto-deploy) may consume Render free-tier build minutes at a rate that triggers costs; source-file-change filter needed | Medium | Sprint story must include build-minute impact assessment; PO confirmation before implementation | null |

**Pre-sprint planning required decisions (RISK-01):** Product Owner must confirm closed trade count (≥ or < 20) before sprint planning seals. See cycle_summary.md Pre-sprint Required Decisions.

---

## Integrity Validation — 3.5 Local Model Integrity

| Check | Result |
|-------|--------|
| All S2-IDs declared | ✅ S2-01 through S2-07 (conditional) |
| All EPICs declare Maps-to | ✅ EPIC-01→S2-01,S2-02; EPIC-02→S2-03,S2-04; EPIC-03→S2-05,S2-06; EPIC-04→S2-07 |
| All RISK-IDs in register | ✅ RISK-01, RISK-02, RISK-03 declared |
| No orphaned S2 items | ✅ All scope items assigned to EPICs |
| Design gate requirement | ✅ Required (FEAT-36 metric definition, PT-04 UX score badge) |

**STEP 3.5 Result:** PASS — model is locally consistent and executable.

---

## Capacity Check

| EPIC | Sprint | Effort estimate | Stories |
|------|--------|-----------------|---------|
| EPIC-01 | Sprint 1 | M+S+S+S = ~4-5 days | ST-01 (FEAT-36 M), ST-02 (FEAT-37 S), ST-03 (QA-25 S), ST-04 (FEAT-39 S) |
| EPIC-02 | Sprint 1 | S+XS = ~1 day | ST-05 (BE-15 S), ST-06 (GOV-37 XS) |
| EPIC-03 | Sprint 2 | M+S+M = ~3-4 days | ST-07 (GOV-35 M), ST-08 (OPS-26 S), ST-09 (OPS-27 M) |
| EPIC-04 (cond.) | Sprint 2 | L+M = ~4-6 days | ST-10 (PT-04 backend L), ST-11 (PT-04 frontend M) |

**Firm total (EPICs 1–3):** ~8-10 days  
**Conditional total (EPIC-04):** ~4-6 days additional  
**Available capacity (solo-dev, standard mode):** 2 sprints × ~5 days = ~10 days

**Outcome:** WARN — firm scope (8-10 days) is at the edge of 2-sprint solo capacity. EPIC-04 conditional adds risk if gate is confirmed.

### Phasing Recommendation

| Phase | EPICs | Estimated effort | Notes |
|-------|-------|-----------------|-------|
| Sprint 1 | EPIC-01, EPIC-02 | ~5-6 days | Arc 5 analytics + ticker validation; self-contained deliverables |
| Sprint 2 | EPIC-03 + EPIC-04 if gate met | ~7-10 days | AI governance + CI/CD + conditional PT-04; confirm gate before sealing Sprint 2 |

Note: EPIC-04 conditional in Sprint 2 creates capacity risk. If PT-04 gate IS confirmed (≥20 trades), Sprint 2 becomes heavy (7-10 days). PMO Lead should flag this at sprint planning and consider whether EPIC-04 defers to v4.1 as a fallback.

---

## Cross-Stage Integrity (STEP 5.5)

| Check | Result |
|-------|--------|
| All S2-IDs in scope map to EPICs | ✅ |
| All EPIC-IDs in backlog slice match stage3 | ✅ |
| All RISK-IDs referenced in EPIC table appear in Risk Register | ✅ |
| No orphaned references | ✅ |
| Stage 2 scope document exists | ✅ `docs/product/scope/scope--2026-05-22__release-v4.0-arc5-analytics-spec-closure-gemini-compliance.md` |
| Decisions record exists | ✅ `docs/product/decisions/decisions--2026-05-22__release-v4.0.md` |

**STEP 5.5 Result:** PASS
