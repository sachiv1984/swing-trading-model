**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-06-21__release-v5.1
**Release:** v5.1
**Published:** 2026-06-21

---

# Release Plan — v5.1 SI-05 Phase 1 & Governance Debt

## Readiness

**Source:** `claude/backlog/backlog.md` | Roadmap: `current_roadmap.md` | Prior cycle: `2026-06-03__release-v5.0`

### 1.1 Backlog Age Advisory
No spec/documentation debt items aged 2+ cycles without story assignment in v5.1 scope. BLG-FE-61, LL-RP-v5.0-D-2, BLG-SPEC-45, BLG-QA-43 all filed ≤1 cycle ago and are being assigned this release.

### 1.2 Provisional-Target Advisory
ℹ 1 item carries `Provisional-Target: v5.1` (BLG-FE-61). 3 items are gate-conditional (BLG-GOV-67, BLG-SPEC-45, BLG-QA-43). 1 item is deferred-from-lessons-learnt (LL-RP-v5.0-D-2).

### 1.3 Design Dependency Scan
Design dependency scan: **0 items flagged**. SI-05 Phase 1 format is fully specified per BLG-GOV-86 (shipped v5.0); no new UI components; delivery_verification_prompt.md patch and Playwright story are non-UI.

### 1.4 Gate-Condition Proximity Scan

| Item | Gate condition | Current trajectory | Projected clear date |
|------|---------------|-------------------|---------------------|
| BLG-GOV-67 (SI-05 Phase 1) | SI-01 + SI-03 live ≥ 30 days | SI-03 shipped 2026-05-22 | **2026-06-21 — CLEARS ON RELEASE DATE** |
| BLG-FE-41 (RFJ visual design) | RFJ live ≥ 30 days | SI-03 shipped 2026-05-22 | 2026-06-21 — eligible v5.2+ |
| BLG-FE-40 (RFJ filter persistence) | RFJ in use ≥ 30 days | SI-03 shipped 2026-05-22 | 2026-06-21 — eligible v5.2+ |
| PO-02 (AI journal patterns) | 6+ months AI journals | ~2026-04-20 start | ~2026-10-20 |
| SI-02 frontend (drift detection) | ≥20 closed trades w/plans | 6 trades (v4.6 audit); ~1–2/month | 2027-2028 (gate NOT close) |
| PO-04 (reflection/outcome) | 50+ trades with plans | 6 trades | 2028+ (gate NOT close) |

**Arc 4 data density sub-check:**
- PO-02 (6+ months AI journals): ~2026-04-20 start → projected 2026-10-20
- PO-04 (50+ trades with plans): 6 current at ~1–2/month → data not available — Product Owner to surface at readiness review
- SI-02 (20+ trades with plans): 6 current at ~1–2/month → Product Owner to confirm or update

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

**Scope document:** `docs/product/scope/scope--2026-06-21__release-v5.1-si05-phase1-govdebt.md`

| S2-ID | Item | Source | Priority | Effort |
|-------|------|--------|----------|--------|
| S2-01 | SI-05 Phase 1 — Weekly Strategy Integrity Digest (Telegram) | BLG-GOV-67 | P2 | M |
| S2-02 | delivery_verification_prompt.md §-1.3 Tier 2 fix | LL-RP-v5.0-D-2 | P2 | S |
| S2-03 | BLG-FE-61 SignalCard allocation_insufficient Playwright E2E | BLG-FE-61 (v5.1 firm) | P3 | XS |
| S2-04 | BLG-SPEC-45 SI-05 financial reporting scope verification | BLG-SPEC-45 | P3 | XS |
| S2-05 | BLG-QA-43 compliance_summary field population validation | BLG-QA-43 | P3 | XS |
| S2-06 | BLG-GOV-89 Staged verification sprint protocol document | BLG-GOV-89 | P3 | S |

**Deferred from active backlog:**
- BLG-FE-43 (SI-05 frontend spec): deferred — SI-05 Phase 1 is Telegram-only; in-app spec relevant for Phase 2
- BLG-FE-41, BLG-FE-40: gates clear 2026-06-21; scope for v5.2+
- All SI-02 gated items (BLG-BE-27/29, BLG-SPEC-44, BLG-QA-42): gate NOT MET

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01, S2-04 | Head of Backend Engineering; Head of Specs Team | RISK-01, RISK-02 | After EPIC-02 (scope verification confirms SI-05 format before implementation) |
| EPIC-02 | S2-02 | Head of Specs Team | RISK-03 | Independent; first in merge order |
| EPIC-03 | S2-03, S2-05, S2-06 | QA Lead; Director of Quality; PMO Lead | — | Independent; merge alongside EPIC-02 |

**EPIC-01 note:** Includes authoring the SI-05 API contract and openapi.yaml entry in the same commit per CLAUDE.md §2. Staging verification AC required for Telegram delivery confirmation.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | SI-05 gate clears exactly on 2026-06-21 (release date); gate confirmation must happen at sprint planning | Medium | Gate clears 30 days after SI-03 ship (2026-05-22); PMO Lead confirms at sprint planning with production verification | null |
| RISK-02 | EPIC-01 | No SI-05 API contract exists; must be authored same-sprint per CLAUDE.md §2 | Medium | ST-01 scope includes contract authoring + openapi.yaml + test.py registration; all in same commit | null |
| RISK-03 | EPIC-02 | delivery_verification_prompt.md §-1.3 requires CLAUDE.md §6 checklist (version bump, OPERATIONAL_GUIDE.md update, prompt_change_log.md entry) | Low | Governance checklist applied by Head of Specs Team; well-established pattern from prior cycles | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

**S2 → EPIC mapping:**
- S2-01 → EPIC-01 ✓, S2-04 → EPIC-01 ✓
- S2-02 → EPIC-02 ✓
- S2-03 → EPIC-03 ✓, S2-05 → EPIC-03 ✓, S2-06 → EPIC-03 ✓

**RISK → EPIC mapping:** RISK-01 → EPIC-01 ✓, RISK-02 → EPIC-01 ✓, RISK-03 → EPIC-02 ✓

**Dependency chain:** EPIC-02 completes before EPIC-01; no circular dependencies. EPIC-03 is fully independent.

**Executable:** All S2 items have corresponding EPICs. All EPICs have S2 mappings. All RISKs are in the register.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort estimates (inline — no scored_initiatives.md matches):**

| EPIC | Stories | Effort (mid-point) | Notes |
|------|---------|-------------------|-------|
| EPIC-01 | 2 | ~3 days | ST-01 M (SI-05 backend + Telegram + contract), ST-02 XS (scope verification) |
| EPIC-02 | 1 | ~0.5 day | ST-03 S (governance patch + checklist) |
| EPIC-03 | 3 | ~1 day | ST-04 XS (Playwright), ST-05 XS (spot-check), ST-06 S (protocol doc) |
| **Total** | **6** | **~4.5 days** | Within 1-sprint solo-dev capacity |

**Result:** ✅ PASS — 4.5 days estimated effort is well within a standard 1-sprint timebox.

**Design gate assessment:** NOT required. All scope items are: backend service, governance patch, Playwright test, documentation, spot-check — no new UI or UX components.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```
