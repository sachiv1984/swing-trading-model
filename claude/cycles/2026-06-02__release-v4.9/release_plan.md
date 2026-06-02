**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v4.9
**Cycle:** 2026-06-02__release-v4.9
**Published:** 2026-06-02

---

# Release Plan — v4.9

## Readiness

**Source cycle:** 2026-06-01__release-v4.8 (Closed — post_ship_complete, next_cycle_unblocked)
**Preflight:** PASS with 3 advisories (documented in run_manifest.md)

**Backlog readiness:**
- BLG-OPS-49 (P1): npm HIGH CVEs — tagged v4.9, ready
- BLG-OPS-50 (P2): Anthropic SDK upgrade — tagged v4.9, ready
- BLG-QA-40 (P2): Phase B CI with real Postgres — tagged v4.9, ready
- BLG-QA-41 (P3): Schema smoke test — tagged v4.9, depends on BLG-QA-40
- BLG-GOV-78 (P3): roadmap_prompt STEP 8.1 strengthening — Unscheduled, natural v4.9 fit; Head of Specs Team + PMO Lead
- BLG-GOV-67 (P2): SI-05 Phase 1 — gate clears 2026-06-21 (conditional)
- BLG-GOV-74 (P2): AI quarterly review — **excluded** (gate: 2026-08-29, post v4.9 ship)

**Gate proximity (STEP 1.4 summary):**
- SI-05 Phase 1 gate: clears 2026-06-21 ← primary conditional; include in v4.9 as EPIC-04
- PT-04 gate: ~Sep 2026 — not in scope
- SI-02 gate: ~Nov 2026 — not in scope

**Design gate required:** No — no UI design decisions required in v4.9 scope.

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

| ID | Item | Source | Priority | Notes |
|----|------|--------|----------|-------|
| S2-01 | Security & Dependency Hardening | BLG-OPS-49, BLG-OPS-50 | P1/P2 | npm HIGH CVEs (21); Anthropic SDK 0.40→0.105.2 |
| S2-02 | CI/QA Infrastructure Strengthening | BLG-QA-40, BLG-QA-41 | P2/P3 | Phase B real Postgres + schema smoke test |
| S2-03 | Governance Debt Clearance | BLG-GOV-78 | P3 | roadmap_prompt.md STEP 8.1 gate strengthening |
| S2-04 | Arc 5 SI-05 Phase 1 | BLG-GOV-67 | P2 | **Conditional** — gate clears 2026-06-21 |

**Explicitly deferred:**
- BLG-GOV-74 — AI quarterly review (gate: 2026-08-29; Provisional-Target updated to v4.10+)
- SI-02 frontend (gate: ~Nov 2026 for 20+ closed trades with plans)
- All Arc 4 features (data density gates unmet)

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Head of Engineering; Cybersecurity & Trust Lead | RISK-01 | No dependency — execute first |
| EPIC-02 | S2-02 | QA Lead; Head of Engineering | RISK-02 | ST-04 depends on ST-03 within EPIC |
| EPIC-03 | S2-03 | Head of Specs Team; PMO Lead | None | No dependency |
| EPIC-04 | S2-04 | Head of Backend Engineering | RISK-03 | **Conditional** — sprint planning gate confirmation required; execute last |

EPIC-04 is conditional. Sprint planning must confirm gate cleared (SI-01 + SI-03 live ≥ 30 days, verifiable on/after 2026-06-21) before sealing EPIC-04 stories.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Anthropic SDK 0.40→0.105.2 (65 minor versions) — potential breaking changes to /ai/generate-thesis and /ai/check-daily-cost | Medium | Review SDK changelog; full backend test suite post-upgrade; staging AI endpoint validation | null |
| RISK-02 | EPIC-02 | Phase B CI (real Postgres) may surface existing test failures masked by stub | Low | Accept and fix any surfaced failures — quality improvement; adjust test counts if needed | null |
| RISK-03 | EPIC-04 | SI-05 Phase 1 gate (2026-06-21) may slip or gate data may be insufficient | Low | Gate date deterministic (2026-05-22 + 30d); trajectory confirmed at STEP 1.4; probability of slip very low | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

**Scope → EPIC mapping check:**
- S2-01 → EPIC-01 ✓
- S2-02 → EPIC-02 ✓
- S2-03 → EPIC-03 ✓
- S2-04 → EPIC-04 ✓

**RISK mapping check:**
- RISK-01 → EPIC-01 ✓ (appears in Risk Register)
- RISK-02 → EPIC-02 ✓
- RISK-03 → EPIC-04 ✓

**Role coverage:** All EPICs have named owners from required roles list. ✓

**Conditional item guard:** EPIC-04 marked conditional with explicit gate condition (2026-06-21) and sprint planning gate confirmation requirement. ✓

**Result:** PASS — plan is logically consistent and executable.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort estimates (from backlog + inline sizing):**

| EPIC | Stories | Effort (each) | Total estimate |
|------|---------|---------------|----------------|
| EPIC-01 | ST-01 (BLG-OPS-49 S), ST-02 (BLG-OPS-50 S–M) | S = ~0.5d; S–M = ~0.5–1d | ~1–1.5 days |
| EPIC-02 | ST-03 (BLG-QA-40 M), ST-04 (BLG-QA-41 S) | M = ~1–2d; S = ~0.5d | ~1.5–2.5 days |
| EPIC-03 | ST-05 (BLG-GOV-78 S) | S = ~0.5d | ~0.5 day |
| EPIC-04 (conditional) | ST-06, ST-07 (BLG-GOV-67 M total) | M = ~2–3d total | ~2–3 days |

**Firm scope total:** ~3–4.5 days
**With conditional EPIC-04:** ~5–7.5 days

**scored_initiatives.md effort bands:** No matching rows — using inline estimates.

**Assessment:** Firm scope fits comfortably in 1 sprint. With EPIC-04 conditional, total is at the upper end of standard sprint capacity but feasible. Sprint planning should sequence EPIC-01→02→03 (firm) and EPIC-04 (conditional) to allow gate confirmation.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity

**Cross-stage checks:**

| Check | Result |
|-------|--------|
| All S2-IDs map to EPICs | PASS — S2-01→EPIC-01, S2-02→EPIC-02, S2-03→EPIC-03, S2-04→EPIC-04 |
| All EPIC-IDs in backlog slice match EPIC table | PASS — verified against stage4_backlog_slice.md |
| All RISK-IDs in EPIC table appear in Risk Register | PASS — RISK-01/02/03 all present |
| No orphaned EPIC references in backlog slice | PASS |
| Conditional EPIC-04 marked correctly | PASS — conditional gate stated in both execution plan and backlog slice |

**Decision Record Integrity (STEP 5.7):**
- decisions--2026-06-02__release-v4.9.md: present ✓
- No escalations raised → no AR/SRB records to verify
- All mandatory template fields populated ✓

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: pass
attributes.cross_stage_integrity: pass
attributes.decisions_validated: pass
```

---

*Plan published: 2026-06-02 | Cycle: 2026-06-02__release-v4.9*
