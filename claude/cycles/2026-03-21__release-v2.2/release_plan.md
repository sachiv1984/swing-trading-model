**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v2.2
**Cycle:** 2026-03-21__release-v2.2
**Last Updated:** 2026-03-21

---

# Release Plan — v2.2 Security, Alert Maturity & Quality

---

## Readiness

**Release:** v2.2 | **Cycle:** 2026-03-21__release-v2.2 | **Mode:** standard

### Readiness Assessment

| Domain | Status | Notes |
|--------|--------|-------|
| Backlog readiness | ✅ Ready | 24+ items targeting v2.2; 15 selected for this cycle scope |
| Spec readiness | ⚠ Partial | API auth spec (BLG-SEC-01) requires authoring; health endpoint (BLG-OPS-06) requires authoring; all other items build on existing specs. Spec authoring is first story in each EPIC where needed. |
| Dependencies | ✅ Met | BLG-SPEC-G2 (Error Standard) ✅ v2.1; BLG-OPS-03 (preview envs) ✅ v2.1; BLG-OPS-04 is in-release dependency (EPIC-02 sequenced accordingly) |
| Environment | ✅ Ready | Staging environment active (v1.10+); CI/CD active; per-PR preview environments active (v2.1) |
| Governance | ✅ Ready | No open escalations; post-ship closure complete; next_cycle_unblocked=true |

### Backlog Age Advisory

All items targeted for v2.2 scope were added in cycle 2026-03-18__release-v2.1 or 2026-03-21__item-3.5 (0–1 cycles ago). No spec/documentation debt items have aged 2+ cycles without story assignment in the planned scope. Advisory passes cleanly.

**⚠ Advisory (ADV-RP-v22-02):** BLG-BE-02 ID appears in both the closed items table (v2.0, "GET /portfolio/prospective-heat") and the active backlog (v2.1, "R-Multiple Analysis stop price"). Duplicate ID in backlog. This item is deferred to v2.3; post-cycle backlog management should assign a new ID to the active entry.

---

## Scope

### Release Theme: Security, Alert Maturity & Quality

v2.2 consolidates three natural threads following v2.1 (Alerts, Watchlists & Enhancements):
1. **Security hardening** — the alert and watchlist features added in v2.1 created a more complex API surface on a publicly accessible Render deployment with no authentication. BLG-SEC-01 (P1) addresses this gap.
2. **Alert system maturity** — the v2.1 alerts engine delivers rule evaluation but lacks: scheduling autonomy (BLG-OPS-04), threshold customisation (BLG-FEAT-10), and historical observability (BLG-FEAT-12).
3. **Quality coverage** — v2.1 delivery verification flagged QA scenario gaps (TSG-v21-01/02). QA coverage and governance tooling is addressed in EPIC-04 and EPIC-05.

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Security Hardening — API Key Authentication + CSP Headers |
| S2-02 | EPIC-02 | Alert System Maturity — Scheduling design, threshold customisation, history table |
| S2-03 | EPIC-03 | Bug Fixes & Operational Quick Wins — CSV import bug, cosmetic fix, health check endpoint |
| S2-04 | EPIC-04 | QA Coverage — Execute notification scenarios, create watchlist scenarios, automation readiness, traceability matrix |
| S2-05 | EPIC-05 | Governance Process Enhancements — Provisional-Target field, scored_initiatives.md handoff, carry-forward block |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-11 — Strategy Compliance Score | SPS=4, M–L effort; requires Strategy Rules & System Intent Owner full review before scoping. Scope constraint must be formally documented in sprint planning AC before implementation. | v2.3 |
| BLG-UX-01 — Sidebar navigation overflow | Product Owner design decision (grouping/pattern) needed before spec. Not ready for sprint planning. | v2.3 |
| BLG-QA-01 — Playwright E2E automation | Depends on BLG-QA-02 (readiness assessment, in v2.2 EPIC-04); natural sequencing: assess first (v2.2), implement (v2.3). | v2.3 |
| BLG-FE-02 — Loading State Standardisation | P3, M effort; deprioritised in favour of security and alert maturity. | v2.3 |
| BLG-FE-03 — Error Message Mapping Layer | P3, S–M effort; deprioritised. | v2.3 |
| BLG-FEAT-09 — Metrics Staleness Indicator | P2, S–M; deprioritised to keep v2.2 focused. | v2.3 |
| BLG-OPS-05 — API Endpoint Performance Baseline | P3; deprioritised. | v2.3 |
| BLG-GOV-03 — Simplify cycle artefact sealing | P3; governance-internal, no user value. | v2.3 |
| BLG-BE-02 (active) — R-Multiple Analysis stop price | P3; deprioritised. Note: ID conflict with closed item — requires rename before promotion. | v2.3 |
| BLG-TECH-05 — Prometheus metrics | P3, conditional on multi-user or operational need | v3.0+ |
| TEST-GAP-EPIC-05-SLIP — Slippage test scenarios | P3 | v2.3 |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-03-21__release-v2.2

---

## Execution Plan

### EPIC Table

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Cybersecurity & Trust Lead + Backend Engineering + Base44 Frontend | RISK-01 | None — first priority; can start immediately |
| EPIC-02 | S2-02 | Product Owner + Backend Engineering | RISK-02 | BLG-OPS-04 (ST-03) must complete before ST-04 and ST-05 can begin |
| EPIC-03 | S2-03 | Head of Engineering + Infrastructure & Operations Owner + Base44 Frontend | RISK-03 | None — independent; can run in parallel with EPIC-01 |
| EPIC-04 | S2-04 | Director of Quality + QA & Testing Owner | RISK-04 | ST-11 (BLG-QA-02 readiness assessment) should complete before ST-12 (traceability matrix) — same EPIC, natural ordering |
| EPIC-05 | S2-05 | Head of Specs Team | RISK-05 | None — governance work; can run independently |

**EPIC-01 note:** ST-01 (BLG-SEC-01, API Key Auth) must spec the auth contract before backend implementation. Both frontend and backend changes are required; must ship together in same PR or back-to-back PRs within the EPIC branch. EPIC-01 is the highest priority and should be Sprint 1 priority #1.

**EPIC-02 note:** ST-03 (BLG-OPS-04) is a design + spec task (Product Owner decision + spec authoring). Until ST-03 produces a scheduler decision and spec, ST-04 and ST-05 cannot begin implementation. Sprint planning should sequence ST-03 as Sprint 1 item and ST-04/ST-05 as Sprint 2 items.

**EPIC-03 note:** All three items (ST-06 XS, ST-07 XS, ST-08 XS/S) are trivially small; consider bundling into a single PR.

**EPIC-05 note:** Governance prompt changes require all four steps of CLAUDE.md §6 edit checklist: version bump, OPERATIONAL_GUIDE §14 update, phase section source prompt header update, prompt_change_log.md entry. Head of Specs Team must complete all four for each changed file.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | API key auth requires coordinated frontend + backend change; if frontend doesn't include key on all calls, existing functionality breaks | High | Sprint planning: require ST-01 to cover both backend middleware and frontend env-var integration in single EPIC branch; DoQ sign-off must confirm no regression | null |
| RISK-02 | EPIC-02 | BLG-OPS-04 (alert scheduling design) is a Product Owner decision task — if PO design decision is blocked or scoped too broadly, ST-04 and ST-05 cannot proceed | Medium | ST-03 AC must include a concrete scheduler decision (option selected, documented). Deferred implementation options (if PO defers scheduling to v2.3) must be explicitly stated in ST-03 output. | null |
| RISK-03 | EPIC-03 | BLG-BE-03 (CSV export bug) is latent — may require careful verification to confirm the import path is exercised by a test | Low | ST-06 AC requires regression confirmation (incorrect import name present before fix, correct after). | null |
| RISK-04 | EPIC-04 | TEST-GAP-EPIC-02 (execute notifications scenarios) requires open positions to trigger 3 of 8 alert types — test data setup may block completion | Medium | If test data setup proves infeasible: partial execution is acceptable; document which scenarios were executed and which remain pending due to data dependency. | null |
| RISK-05 | EPIC-05 | Governance prompt changes (BLG-GOV-04/05/06) modify core planning engine prompts; if incorrectly applied, could create process regressions in future cycles | Medium | CLAUDE.md §6 edit checklist enforced; each change requires prompt_change_log.md entry. DoQ (Head of Specs Team) must review all prompt diffs before sign-off. | null |

---

## Integrity Validation — 3.5 Local Model Integrity

### Cross-item dependency check

| Dependency | From | To | Verified |
|------------|------|----|---------|
| BLG-OPS-04 design must precede BLG-FEAT-10, BLG-FEAT-12 impl | ST-03 | ST-04, ST-05 | ✅ — enforced by sequencing note in EPIC-02 row and ST ordering in Stage 4 |
| BLG-QA-02 should precede BLG-SPEC-T01 (readiness informs traceability scope) | ST-11 | ST-12 | ✅ — both in EPIC-04; natural story ordering enforces this |
| BLG-SPEC-G2 (Error Standard) as dependency of BLG-FE-03 | Shipped v2.1 | N/A (deferred) | ✅ — BLG-FE-03 is deferred; gate met for v2.3 |
| BLG-OPS-03 (preview envs) as dependency of BLG-QA-01 | Shipped v2.1 | N/A (deferred) | ✅ — BLG-QA-01 deferred; gate met for v2.3 |
| ST-17 (Spec Coverage Inventory) as dependency of BLG-SPEC-T01 | Shipped v2.1 | ST-12 | ✅ — gate cleared |

### S2 → EPIC ID mapping check

| S2-ID | EPIC-ID | Verified |
|-------|---------|---------|
| S2-01 | EPIC-01 | ✅ |
| S2-02 | EPIC-02 | ✅ |
| S2-03 | EPIC-03 | ✅ |
| S2-04 | EPIC-04 | ✅ |
| S2-05 | EPIC-05 | ✅ |

### RISK ID coverage

All 5 EPICs have a RISK-ID assigned. All RISK rows have `Relates to` and `escalation_ref` fields. ✅

### Scope boundary check

- No item in scope is listed under §4 (Explicitly Out of Scope) of backlog.md. ✅
- No item in scope violates strategic exclusions in strategy_rules.md §13.
  - BLG-FEAT-11 (Compliance Score) was a SPS=4 boundary-adjacent item — correctly deferred. ✅
  - BLG-GOV-04/05/06 are governance process items, not product features — within scope. ✅
- No item changes the strategy spec (strategy_rules.md write scope is excluded). ✅

**Local Model Integrity: PASS**

---

## Capacity Check

### Effort Estimates

| EPIC | Stories | Effort (mid-point) | Notes |
|------|---------|-------------------|-------|
| EPIC-01 | ST-01 (M, ~1d), ST-02 (XS, <1h) | ~1–1.5 days | Frontend + backend coordination required |
| EPIC-02 | ST-03 (S–M, ~0.5–1d), ST-04 (M, ~2–3d), ST-05 (M, ~2–3d) | ~5–7 days | ST-03 gates ST-04/ST-05 |
| EPIC-03 | ST-06 (XS, <15min), ST-07 (XS, <30min), ST-08 (XS, <1h) | ~0.5–1 day | Bundle into single PR |
| EPIC-04 | ST-09 (S, ~0.5d QA), ST-10 (S–M, ~1d), ST-11 (XS–S, ~0.5d), ST-12 (M, ~1.5d) | ~3.5–4 days | QA-heavy; not blocked by dev work |
| EPIC-05 | ST-13 (M, ~1–2d), ST-14 (M, ~1–2d), ST-15 (M, ~1–2d) | ~3–6 days | Governance work; spec changes require §6 checklist |
| **Total** | **15 stories** | **~13–20 days (mid: ~16 days)** | |

### Capacity Baseline

Solo developer, evenings/part-time. Estimated velocity: ~3–4 days of work per week. Estimated available capacity over a 3-sprint cycle: ~9–12 days.

### Outcome: WARN

Total estimated effort (~16 days mid-point) exceeds estimated available capacity (~12 days). The release is not infeasible but requires phasing to 2–3 sprints.

### Phasing Recommendation

**Phase 1 (Sprint 1) — Security + Quick Wins (~4–5 days):**
- EPIC-01: ST-01 (API Key Auth), ST-02 (CSP Headers)
- EPIC-03: ST-06 (CSV bug), ST-07 (cosmetic), ST-08 (health check) — bundle as single PR
- EPIC-02: ST-03 (Alert scheduling design — Product Owner decision task, low dev effort)
- Estimated dev effort: ~3–4 days. Security hardening ships first.

**Phase 2 (Sprint 2) — Alert Maturity + QA Coverage (~7–9 days):**
- EPIC-02: ST-04 (Alert Threshold Customisation), ST-05 (Alert History Table) — gated on ST-03 complete
- EPIC-04: ST-09 (Execute notifications scenarios), ST-10 (Create watchlist scenarios), ST-11 (Test Automation Readiness)
- Estimated dev+QA effort: ~6–8 days.

**Phase 3 (Sprint 3) — Governance + QA Traceability (~5–7 days):**
- EPIC-04: ST-12 (Spec-to-Test Traceability Matrix)
- EPIC-05: ST-13 (GOV-04), ST-14 (GOV-05), ST-15 (GOV-06)
- Estimated effort: ~5–7 days. Governance-heavy; can be interleaved with Phase 2.

**Ordering rationale:** Security first (P1, risk reduction), alert maturity in Sprint 2 (gated on design decision), governance in Sprint 3 (no external dependency, can slip without blocking delivery).

**Note:** If Phase 3 proves over-capacity, EPIC-05 governance items (BLG-GOV-04/05/06) are the lowest-risk deferral as they affect future cycles only, not current delivery.

---

## Integrity Validation — 5.5 Cross-Stage Integrity

### S2 → EPIC → ST mapping audit

| S2-ID | EPIC-ID | ST items | Count | Status |
|-------|---------|----------|-------|--------|
| S2-01 | EPIC-01 | ST-01, ST-02 | 2 | ✅ |
| S2-02 | EPIC-02 | ST-03, ST-04, ST-05 | 3 | ✅ |
| S2-03 | EPIC-03 | ST-06, ST-07, ST-08 | 3 | ✅ |
| S2-04 | EPIC-04 | ST-09, ST-10, ST-11, ST-12 | 4 | ✅ |
| S2-05 | EPIC-05 | ST-13, ST-14, ST-15 | 3 | ✅ |
| **Total** | 5 EPICs | 15 stories | 15 | ✅ |

### RISK coverage audit

All 5 EPIC-IDs in EPIC table have an associated RISK-ID (RISK-01 through RISK-05). All RISK rows in the Risk Register have: RISK-ID, Relates to (EPIC-ID), Description, Priority, Mitigation, escalation_ref. ✅

### Scope document ↔ release_plan.md consistency

- Scope doc: `scope--2026-03-21__release-v2.2-security-alert-maturity-quality.md` — 5 S2 items, same IDs. ✅
- Decisions doc: `decisions--2026-03-21__release-v2.2.md` — references same items and deferred items. ✅
- Backlog slice: `stage4_backlog_slice.md` — 15 stories, all EPIC-IDs match, release-plan-marker present. ✅
- Backlog.md: marker `<!-- release-plan-marker: RP:v2.2:2026-03-21__release-v2.2 -->` confirmed inserted. ✅
- Roadmap: marker `<!-- roadmap-annotation-marker: RA:v2.2:2026-03-21__release-v2.2 -->` confirmed inserted. ✅

### Deferred item consistency

All items in the "Items explicitly deferred" table in the scope document have: item ID, reason, and target release. ✅

### Sequencing consistency

- ST-04, ST-05 marked as gated on ST-03 in both the EPIC table and the stage4_backlog_slice.md. ✅
- ST-12 marked as after ST-11 in both documents. ✅
- No circular dependencies detected. ✅

### Open escalations

No escalations raised. open_escalations = []. ✅

**Cross-Stage Integrity: PASS**

---

## Integrity Validation — 5.7 Decision Record Integrity

**Trigger check:** Were any escalations raised that resulted in Accepted Risk (AR) or Strategic Review Board (SRB) decision records? No — no escalations were raised in this cycle (open_escalations = []). Accepted risks table in decisions record is empty ("None").

**Decision record file:** `docs/product/decisions/decisions--2026-03-21__release-v2.2.md`
- Owner present: ✅
- Class: Planning Document (Class 4): ✅
- Status: Active: ✅
- Release: v2.2: ✅
- Cycle: 2026-03-21__release-v2.2: ✅
- §Scope decisions: populated (6 decisions): ✅
- §Sequencing decisions: populated (4 decisions): ✅
- §Accepted risks: "None" (no AR escalations): ✅
- Supersession note present (TBD): ✅

**Decision Record Integrity: PASS (no AR/SRB records required; decisions record is well-formed)**


