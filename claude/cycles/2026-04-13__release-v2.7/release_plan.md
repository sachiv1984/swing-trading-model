**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v2.7
**Cycle:** 2026-04-13__release-v2.7
**Last Updated:** 2026-04-13

---

# Release Plan — v2.7 Performance, Governance Hardening & Market Intelligence

---

## Readiness

### Readiness Assessment

**Prior cycle:** 2026-04-11__release-v2.6 — Closed (post_ship_complete: true, next_cycle_unblocked: true)
**Governance state:** Clean — no open escalations, no amendment in progress
**Backlog lock:** Not held — clean for new cycle

### 1.1 Backlog Age Advisory

Spec/documentation debt items in candidate pool with 2+ cycles without story assignment:

- **BLG-SPEC-D17** (Spec Dependency Map) — age: 1 cycle (filed v2.5 rebalance 2026-04-05). Below threshold. No advisory.
- **BLG-GOV-08** (Engine prompt compression) — referenced from AUD-2026-03-21 (~3 cycles). Has been explicitly deprioritised at v2.5 and v2.6 planning. ⚠ **Advisory: BLG-GOV-08 has been in the backlog for 3+ cycles without story assignment. Recommend promotion to sprint story if scope permits.**

### 1.2 Provisional-Target Advisory

Items with `Provisional-Target: v2.7`:

| Count | Type |
|-------|------|
| 16 active items | Provisional-Target: v2.7 |
| 0 items | No Provisional-Target signal |

ℹ 16 item(s) carry `Provisional-Target: v2.7` — horizon-planned for this release. 0 items have no matching Provisional-Target signal.

### 1.3 Design-Gate Language Scan

Scanning v2.7 candidates for design-gate language:

- BLG-FEAT-16 (AI Journal Summarisation): "§13 Status: CONDITIONALLY COMPLIANT — SRB-v1.7 — Strategy Rules owner sign-off required before merge" — **design dependency detected**.
- BLG-BE-10 (Supplementary indicator fields): "Strategy Rules owner confirms no scoring logic was modified (sign-off in QA evidence before merge)" — **design dependency detected** (but qualifying criteria already defined; not a gating decision per se).
- BLG-GOV-19 (Autonomous DoQ sign-off class): "Director of Quality sign-off on qualifying criteria" — **design dependency detected**.
- BLG-GOV-14 (Governance Health Score): "Head of Specs Team sign-off on formula definition before implementation" — **design dependency detected**.

Design dependency scan: 4 item(s) flagged — surfaced at Pre-sprint Required Decisions checklist.

**Readiness verdict:** ✅ PASS — prior cycle closed, governance clean, backlog candidates identified with 1 advisory (BLG-GOV-08 age).

---

## Scope

### S2 Scope Items — v2.7

| S2-ID | Category | Item | Priority | Effort |
|-------|----------|------|----------|--------|
| S2-01 | Infrastructure | BLG-OPS-14 — Enable Supabase Supavisor connection pooling | P1 | XS |
| S2-02 | Backend Engineering | BLG-BE-07-FIX — Refactor get_portfolio_summary() single DB connection | P2 | M |
| S2-03 | Governance Process | BLG-GOV-18 — QA evidence sign-off gate before PR | P2 | XS |
| S2-04 | Governance Process | BLG-GOV-19 — Define autonomous DoQ sign-off class | P2 | S |
| S2-05 | Governance / CI | BLG-GOV-16 — Extend governance_sync.yml to trigger on push to main | P2 | XS |
| S2-06 | Test Infrastructure | BLG-QA-11 — Fix Playwright page.route() intercepts | P2 | S |
| S2-07 | Test Automation | BLG-QA-12 — System Status Playwright spec | P3 | M |
| S2-08 | Product Feature | BLG-FEAT-17 — Market Correlation Analysis | P2 | M |
| S2-09 | Backend Engineering | BLG-BE-10 — Supplementary indicator fields (display-only, §13 compliant) | P3 | M |
| S2-10 | Spec Debt | BLG-SPEC-D17 — Spec Dependency Map | P3 | M |
| S2-11 | Governance Process | BLG-GOV-14 — Governance Health Score | P3 | M |

**Total in scope:** 11 items (1 P1, 5 P2, 5 P3)

### Items Explicitly Deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-GOV-08 — Engine prompt compression | L effort; advisory only — deprioritised in favour of higher-value items | v2.8 |
| BLG-GOV-11 — Cycle artefact inventory | P3; advisory; no user-facing value | v2.8 |
| BLG-GOV-13 — Deduplicate backlog_archive.md | P3; requires Product Owner confirmation (OA outstanding) | v2.8 post-PO confirm |
| BLG-FEAT-13 — Gated feature rollout capability | P3; no current use case; adds complexity | v2.8+ |
| BLG-FEAT-16 — AI Journal Summarisation | P3; complex §13 conditions; Strategy Rules owner pre-alignment required before scoping | v2.8+ |
| BLG-TECH-05 — Prometheus metrics endpoint | P3; single-user system; defer until multi-user | TBD |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-04-13__release-v2.7

---

## Execution Plan

### EPIC Table

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01, S2-02 | Head of Engineering + Infrastructure & Operations Owner | RISK-01 (Supavisor compatibility) | First — baseline for EPIC-04 performance verification |
| EPIC-02 | S2-03, S2-04, S2-05 | Director of Quality + Head of Specs Team | RISK-02 (DoQ sign-off criteria complexity) | Independent — Sprint 1 |
| EPIC-03 | S2-06, S2-07 | QA & Testing Owner | RISK-03 (Playwright intercept root cause) | S2-07 blocked until S2-06 resolved (ST-06 → ST-07) |
| EPIC-04 | S2-08, S2-09 | Head of Engineering + Frontend Specifications & UX Owner | RISK-04 (Yahoo Finance data availability) | S2-09 independent; S2-08 depends on BLG-BE-10 §13 sign-off confirmation |
| EPIC-05 | S2-10, S2-11 | Head of Specs Team + PMO Lead + Director of Quality | RISK-05 (scope of artefact coverage for S2-10) | Independent — Sprint 2 |

**EPIC-03 note:** ST-07 (BLG-QA-12 System Status spec) has a logical dependency on ST-06 (BLG-QA-11 Playwright fix) — the new spec uses page.route() and will fail until the intercept mechanism is working. Recommend sequencing ST-06 and ST-07 as sub-tasks within EPIC-03, with ST-07 implementation gated on ST-06 verification.

**EPIC-04 note:** BLG-BE-10 already has `§13 Status: COMPLIANT (display-only)` — no new §13 decision required. BLG-FEAT-17 requires `openapi.yaml` update in same commit per CLAUDE.md.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Supavisor (pgbouncer=true) may be incompatible with psycopg2 transaction semantics or DDL operations | Medium | Test on staging before production; BLG-BE-07-FIX explicitly sequenced after BLG-OPS-14 verification | null |
| RISK-02 | EPIC-02 | Autonomous DoQ sign-off class criteria (BLG-GOV-19) requires Director of Quality sign-off on qualifying criteria before implementation | Medium | Qualifying criteria draft included in story; Director of Quality to review at sprint start | null |
| RISK-03 | EPIC-03 | Playwright page.route() root cause may require significant investigation time; fix may not generalise to all specs | High | ST-06 scoped to investigate root cause and fix at least one spec end-to-end before writing new spec (ST-07). If fix cannot be generalised, ST-07 is descoped and BLG-QA-12 re-deferred. | null |
| RISK-04 | EPIC-04 | Yahoo Finance rate limiting or data gaps for BLG-FEAT-17 correlation endpoint | Low | Pipeline already uses Yahoo Finance (check_market_regime()); existing pattern validated. Cache TTL (1 trading day) reduces call frequency. | null |
| RISK-05 | EPIC-05 | BLG-SPEC-D17 scope (all canonical specs) may surface more dependencies than estimated, increasing effort | Low | Head of Specs Team signs off on completeness at authoring time; explicit staleness acknowledgement in doc; M effort estimate assumes ~22 specs | null |

---

## Integrity Validation — 3.5 Local Model Integrity

### Local Model Integrity Check

**ID consistency:**
- All S2-IDs (S2-01 through S2-11) present ✅
- All EPIC-IDs (EPIC-01 through EPIC-05) declared with `Maps to` implicit in EPIC table ✅
- All RISK-IDs (RISK-01 through RISK-05) declared in Risk Register Summary ✅
- Each EPIC references only S2-IDs from the scope table ✅

**Dependency validation:**
- EPIC-01 → no blocking dependencies ✅
- EPIC-02 → no blocking dependencies ✅
- EPIC-03 → ST-07 gated on ST-06 (within EPIC-03; intra-EPIC dependency) ✅
- EPIC-04 → §13 sign-off for S2-09 is confirmed pre-existing compliance (no new gate required) ✅
- EPIC-05 → no blocking dependencies ✅

**Risk coverage:**
- Every EPIC has at least one RISK entry ✅
- All risks mapped to EPIC or Release-level ✅

**Story count sanity:** 11 S2 items → projected 11 stories (1:1 mapping) — within 0.99 velocity range for ~11 sprinting sessions ✅

**Model integrity verdict:** ✅ PASS — no structural inconsistencies found.

---

## Capacity Check

### Effort Estimates by EPIC

| EPIC | S2 Items | Effort Band | Story Points (est.) |
|------|----------|-------------|---------------------|
| EPIC-01 | S2-01 (XS), S2-02 (M) | S+M ≈ ~0.5+2d | ~2.5d |
| EPIC-02 | S2-03 (XS), S2-04 (S), S2-05 (XS) | XS+S+XS ≈ ~0.25+0.5+0.25d | ~1d |
| EPIC-03 | S2-06 (S), S2-07 (M) | S+M ≈ ~0.5+1d | ~1.5d |
| EPIC-04 | S2-08 (M), S2-09 (M) | M+M ≈ ~2+2d | ~4d |
| EPIC-05 | S2-10 (M), S2-11 (M) | M+M ≈ ~1.5+1.5d | ~3d |

**Total estimated effort:** ~12d mid-point across 11 stories

**Capacity note:** No explicit `--timebox` or `--capacity` provided. Using historical baseline: v2.4–v2.6 averaged 13–15 stories shipped at 1.00 velocity, ~2-week sprints. 11 stories is within comfortable capacity.

**scored_initiatives.md:** No matching items — inline estimates used for all EPICs.

**Effort band advisory:** 0 EPICs have effort band from scored_initiatives.md. Inline estimates used. No advisory required (no scored_initiatives rows present for v2.7 items).

**Capacity verdict:** ✅ PASS — 11 stories at ~12d estimated effort fits comfortably within 2-sprint capacity at historical velocity.

### Phasing Recommendation

Sprint 1 (higher priority, governance + infrastructure):
- EPIC-01: Performance & Connection Infrastructure (S2-01, S2-02) — ~2.5d
- EPIC-02: Governance Process Hardening (S2-03, S2-04, S2-05) — ~1d
- EPIC-03: Test Infrastructure (S2-06, S2-07) — ~1.5d

Sprint 2 (features + documentation):
- EPIC-04: Market Intelligence (S2-08, S2-09) — ~4d
- EPIC-05: Spec & Governance Documentation (S2-10, S2-11) — ~3d

Sprint 1 total: ~5d | Sprint 2 total: ~7d — both within single-sprint bounds.

---

## Integrity Validation — 5.5 Cross-Stage Integrity

### Cross-Stage Integrity Check

**Stage 2 → Stage 3 mapping:**

| S2-ID | Description | EPIC assignment |
|-------|-------------|-----------------|
| S2-01 | BLG-OPS-14 | EPIC-01 ✅ |
| S2-02 | BLG-BE-07-FIX | EPIC-01 ✅ |
| S2-03 | BLG-GOV-18 | EPIC-02 ✅ |
| S2-04 | BLG-GOV-19 | EPIC-02 ✅ |
| S2-05 | BLG-GOV-16 | EPIC-02 ✅ |
| S2-06 | BLG-QA-11 | EPIC-03 ✅ |
| S2-07 | BLG-QA-12 | EPIC-03 ✅ |
| S2-08 | BLG-FEAT-17 | EPIC-04 ✅ |
| S2-09 | BLG-BE-10 | EPIC-04 ✅ |
| S2-10 | BLG-SPEC-D17 | EPIC-05 ✅ |
| S2-11 | BLG-GOV-14 | EPIC-05 ✅ |

All 11 S2 items mapped to an EPIC ✅
No S2 item mapped to multiple EPICs ✅
No EPIC references a non-existent S2 item ✅

**Stage 3 → Stage 4 pre-check:**
- 11 S2 items → 11 ST items expected in backlog slice ✅ (confirmed at STEP 4)
- All EPIC-IDs used in Stage 3 are present ✅
- RISK register complete: 5 risks for 5 EPICs ✅

**Cross-stage integrity verdict:** ✅ PASS

---

## Integrity Validation — 5.7 Decision Record Integrity

### Decision Record Integrity Check

**Trigger:** No Accepted Risk escalations were raised in this cycle. Stage 5.7 trigger condition: "only if triggered by an AR or SRB decision record during escalation handling."

**Verdict:** ✅ NOT APPLICABLE — no escalation decision records were created. decisions--2026-04-13__release-v2.7.md contains no AR or SRB rows.
