**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v2.5
**Cycle:** 2026-04-05__release-v2.5
**Last Updated:** 2026-04-05

---

# Release Plan — v2.5 Integration Baseline, Quick Wins & Governance Debt

---

## Readiness

**Release:** v2.5
**Date:** 2026-04-05
**Prior cycle:** 2026-03-31__release-v2.4 (status: Closed, post_ship_complete=true, next_cycle_unblocked=true)
**CPS at planning time:** 0.0 (zero active roadmap initiatives)

**Backlog age advisory (1.1):** No spec/documentation debt items aged 2+ cycles without story assignment in the v2.5 candidate pool. No advisory triggered.

**Provisional-Target advisory (1.2):** ℹ 19 items carry `Provisional-Target: v2.5`. 13 selected for scope; 7 deferred to v2.6+. M items without matching Provisional-Target signal: 0 (all in-scope items have v2.5 target).

**Carry-forward:**
- CF-1 (sprint planning governance hygiene) → surfaced to Sprint Planning
- CF-2 (delivery_verification_prompt.md seal gate patch) → scheduled as ST-12 ✅
- CF-3 (trade_history.md DEV-ST14-01) → resolved 2026-04-04 ✅

**Status:** Readiness PASS

---

## Scope

**Theme:** Integration Baseline, Quick Wins & Governance Debt

13 scope items across 4 EPICs. See `docs/product/scope/scope--2026-04-05__release-v2.5-integration-baseline-quick-wins-governance.md` for authoritative scope record.

| S2-ID | EPIC | Item | Priority | Effort |
|-------|------|------|----------|--------|
| S2-01 | EPIC-01 | BLG-OPS-12 Fix auth forwarding POST /test/endpoints | P2 | XS |
| S2-02 | EPIC-01 | BLG-OPS-13 Sync endpoint test list with openapi.yaml | P3 | XS |
| S2-03 | EPIC-01 | BLG-FE-07 Fix System Status endpoint categorisation | P4 | XS |
| S2-04 | EPIC-02 | BLG-BE-08 Reports page backend integration review | P2 | M |
| S2-05 | EPIC-02 | BLG-BE-09 Signals page backend integration review | P2 | M |
| S2-06 | EPIC-02 | BLG-BE-07 Investigate high latency on DB-backed endpoints | P2 | M |
| S2-07 | EPIC-03 | BLG-OPS-11 Add --max-time to GitHub Actions curl | P3 | XS |
| S2-08 | EPIC-03 | BLG-FE-08 Fix Avg Slippage StatsCard gradient | P3 | XS |
| S2-09 | EPIC-03 | BLG-FEAT-15 Fee drag metric on Trade History | P3 | S |
| S2-10 | EPIC-04 | BLG-GOV-10 Fix governance_sync.yml batch push | P2 | XS |
| S2-11 | EPIC-04 | BLG-GOV-12 Formalise backlog entry placement standard | P2 | XS |
| S2-12 | EPIC-04 | v2.4 deferred prompt patches (execution_prompt + delivery_verification) | — | S |
| S2-13 | EPIC-04 | TEST-GAP-EPIC-01-v24 Test scenarios EPIC-01 correctness | P2 | S |

**Deferred:** BLG-TECH-05, BLG-FE-09, BLG-SPEC-D17, BLG-GOV-08, BLG-GOV-11, BLG-GOV-14, BLG-FEAT-13 — all P3, governance-heavy or L effort; deferred to v2.6+ (per Skill-Silo balancing).

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01, S2-02, S2-03 | Head of Engineering | RISK-01 | Sprint 1; S2-01 before S2-02/S2-03 |
| EPIC-02 | S2-04, S2-05, S2-06 | Head of Engineering | RISK-02 | Sprint 2; S2-06 after S2-04/S2-05 (latency investigation benefits from knowing integration state) |
| EPIC-03 | S2-07, S2-08, S2-09 | Frontend + Backend | RISK-03 | Sprint 2; S2-09 requires canonical spec update — coordinate with HoST |
| EPIC-04 | S2-10, S2-11, S2-12, S2-13 | PMO Lead + HoST + QA | RISK-04 | Sprint 1; S2-12 (prompt patches) must precede any sprint execution that applies those fixes |

**EPIC-01 note:** S2-01 (auth forwarding fix) is the dependency for S2-02 and S2-03 to be meaningful — fix auth first, then sync and categorise. Backend-only change in S2-01, frontend-only in S2-03, CI-only in S2-02. No shared file conflicts expected.

**EPIC-02 note:** S2-04 and S2-05 are parallel reviews (independent pages). S2-06 (latency investigation) is most valuable after reviews are complete — may uncover shared infrastructure patterns. No blocking dependency on S2-04/S2-05 but benefits from coordination.

**EPIC-04 note:** S2-12 (prompt patches) should be sealed early in Sprint 1 so that the patched prompts govern any remaining sprint execution work. S2-13 (test scenarios) has no dependency on S2-12 but is best sequenced after EPIC-01 merges to benefit from S2-01 implementation as a test reference.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | auth forwarding fix requires reading API key from incoming request — middleware bypass approach has broader security surface than API key forwarding approach | Medium | Implement API key forwarding (not middleware bypass); add to API key auth AC that internal calls use key forwarding | null |
| RISK-02 | EPIC-02 | Integration reviews (S2-04/S2-05) may surface significant gaps requiring new sprint stories beyond v2.5 scope | Low | Review scope is documentation only; gaps produce backlog items, not in-scope fixes; no sprint overrun risk | null |
| RISK-03 | EPIC-03 | S2-09 (fee drag metric) requires canonical spec updates to 3 specs + openapi.yaml — highest coordination cost in scope | Medium | HoST to co-author spec updates; EPIC-03 branch must be created from up-to-date main after EPIC-01 merges to avoid openapi.yaml conflicts | null |
| RISK-04 | EPIC-04 | S2-12 prompt patches must be applied before any sprint execution that relies on the patched prompts — sequencing risk if patches are delayed | Low | Schedule EPIC-04 in Sprint 1; seal EPIC-04 before Sprint 2 execution begins | null |

---

## Integrity Validation — 3.5 Local Model Integrity

**Check 1 — S2-ID completeness:** All 13 scope items have S2-IDs (S2-01 to S2-13). ✅

**Check 2 — EPIC completeness:** All 4 EPICs have EPIC-IDs (EPIC-01 to EPIC-04). Each declares `Maps to: S2-xx` in the backlog slice. ✅

**Check 3 — Risk register completeness:** All 4 EPICs have at least 1 risk in the register. All RISK-IDs (RISK-01 to RISK-04) appear in the EPIC table. ✅

**Check 4 — No scope changes:** This section extracts from the roadmap — no new items were added that weren't on the v2.5 roadmap target list. ✅

**Check 5 — Strategy boundary check:** No scope item contacts strategy_rules.md §13 boundaries. BLG-FEAT-15 (fee drag metric) is a display-only analytics metric — it does not affect signal ranking, scoring, or trading decisions. SPS=1 confirmed. ✅

**Check 6 — S2-09 canonical spec update flag (IMP pre-check):** BLG-FEAT-15 requires updates to `metrics_definitions.md`, `docs/specs/frontend/pages/trade_history.md`, `docs/specs/api_contracts/trade_endpoints.md`, and `docs/reference/openapi.yaml`. This is expected scope for S2-09 / ST-09. The EPIC-03 branch must not merge until all four canonical specs and openapi.yaml are updated in the same commit. Pre-condition recorded here for sprint planning. ✅

**Integrity result:** PASS — plan is structured and executable.

---

## Capacity Check

**Mode:** Standard (WARN allowed)

**Effort estimates by EPIC:**

| EPIC | Stories | Estimated effort | Skills | Source |
|------|---------|-----------------|--------|--------|
| EPIC-01 | ST-01, ST-02, ST-03 | ~2–3h total (3×XS) | Backend (ST-01), CI (ST-02), Frontend (ST-03) | Inline |
| EPIC-02 | ST-04, ST-05, ST-06 | ~4–6 days (3×M) | Backend Engineering + Head of Engineering | Inline |
| EPIC-03 | ST-07, ST-08, ST-09 | ~1–2 days (2×XS + 1×S) | Operations CI, Frontend, Backend + HoST | scored_initiatives.md (BLG-FEAT-15: S) |
| EPIC-04 | ST-10, ST-11, ST-12, ST-13 | ~1.5–2.5 days (2×XS + 2×S) | DevOps, HoST, PMO, QA | Inline |

**Total estimated:** ~6.5–10.5 days (mid-point: ~8.5 days)

**Capacity:** Not explicitly constrained — solo-dev, evening cadence, 3-day sprints. Prior releases (v2.4: ~8–12 days across 6 EPICs / 3 sprints) confirm this is within normal throughput.

**Skill-Silo check:**
- Governance/documentation load: S2-10, S2-11, S2-12 = 3 of 13 items = 23% — within 20–60% bounds ✅
- Execution items: 10 of 13 items (77%) — well-balanced with prior Skill-Silo Alert addressed

**Capacity result:** PASS

### Phasing Recommendation (Sprint Planning Input)

| Sprint | EPICs | Rationale |
|--------|-------|-----------|
| Sprint 1 | EPIC-04 (governance patches), EPIC-01 (System Status reliability) | Governance fixes first (prompts, backlog rule, batch push); System Status fix is the highest-priority P2 |
| Sprint 2 | EPIC-02 (backend integration reviews + latency), EPIC-03 (quick wins + fee drag) | Investigation stories; feature work after governance baseline established |

Two sprints expected. If EPIC-02 investigation work surfaces large scope, sprint planner may split into Sprint 2 (EPIC-02) + Sprint 3 (EPIC-03).

---

## Integrity Validation — 5.5 Cross-Stage Integrity

**Check 1 — S2-ID ↔ EPIC mapping:** All 13 S2-IDs are mapped to exactly one EPIC. No unmapped S2 items. No EPIC with 0 S2 items. ✅

**Check 2 — EPIC ↔ Story traceability:** All EPICs will have Stories (ST-xx) in stage4_backlog_slice.md. Each story maps to a backlog item ID (or has a named source for S2-12 deferred patches). ✅

**Check 3 — Risk ↔ EPIC linkage:** RISK-01 → EPIC-01, RISK-02 → EPIC-02, RISK-03 → EPIC-03, RISK-04 → EPIC-04. All risks are linked. ✅

**Check 4 — Deferred items:** All 7 deferred items appear in both the scope document and the stage4_backlog_slice.md deferred section. ✅

**Check 5 — Backlog lock marker:** `<!-- release-plan-marker: RP:v2.5:2026-04-05__release-v2.5 -->` present in backlog. ✅ (written at STEP 4)

**Cross-stage integrity result:** PASS

---

## Integrity Validation — 5.7 Decision Record Integrity

No Accepted Risk (AR) escalations raised in this cycle. No AR decision records required.

**Decisions record** at `docs/product/decisions/decisions--2026-04-05__release-v2.5.md` — present. ✅

**Decision record integrity result:** PASS (not_applicable for AR records; decisions.md present)
