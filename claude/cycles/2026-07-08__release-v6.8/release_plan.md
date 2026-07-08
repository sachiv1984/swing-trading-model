Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Published
Release: v6.8
Cycle: 2026-07-08__release-v6.8
Last Updated: 2026-07-08

---

# Release Plan — v6.8

## Readiness

**Prior cycle:** `.claude_current_state.json` `prior_cycle` field reads `2026-06-26__release-v6.3` (stale pointer). Most recently closed release: `2026-07-06__release-v6.7` (Verified, Closed_with_actions, post_ship_complete=true).

**Roadmap status:** `current_roadmap.md` §3 (Now horizon) empty by deliberate STEP 8.1 Option (b) choice, 2026-07-08 rebalance — scoping delegated to this engine. v6.8 exists on the roadmap via that documented Option (b) decision (see `run_manifest.md` §-1.2).

**Readiness determination: READY.** Full detail (1.1–1.4 sub-checks, gate proximity table) recorded in `run_manifest.md`. Summary: 4 spec-debt items aged 4+ cycles promoted to firm scope (1.1); 1 item (`BLG-BE-46`) explicitly targets `v6.8` and 3 more carry `Provisional-Target: Next release` (1.2); 2 items are UI-facing, flagging design-gate (1.3); no mechanical perennial-return trigger fired, but an informal 16-item stale-deferral finding from the immediately-prior `groom backlog --dry-run` session drove inclusion of 13 of those 16 this cycle (1.4a); no within-sprint date gates (1.4b); SI-02 gate confirmed NOT MET — 20 closed trades, 0 linked (`BLG-BE-46` root cause) (1.4).

```yaml
# state.json update (STEP 1):
artifacts.stage1_readiness: pass
```

---

## Scope

17 items selected — the largest legitimate pull-through this capacity baseline supports without a WARN outcome. Full rationale for each inclusion/exclusion in `run_manifest.md` and `decisions--2026-07-08__release-v6.8.md`.

### Items in scope

| S2-ID | Backlog item | Description | Priority | Effort |
|-------|--------------|-------------|----------|--------|
| S2-01 | BLG-BE-46 | `trade_plans.position_id` never populated — root cause + fix/backfill decision | P1 (firm) | M (~1–2 days) |
| S2-02 | BLG-SEC-08 | Unvalidated dict keys as SQL column names in `database.update_signal()` | P2 | S (~0.5 day) |
| S2-03 | BLG-SEC-07 | Manual review of signals for anomalous ticker/market values | P3 | XS (<1h) |
| S2-04 | BLG-OPS-99 | Provision application `X-API-Key` for governed routines (resolves LP-08) | P1 | S (~0.5 day) |
| S2-05 | BLG-FEAT-52 | Trade tagging + tag-based performance filtering (descoped, ungated) | P2 | S (~2–3 days) |
| S2-06 | BLG-FEAT-71 | SI-02 gate visibility indicator (Reports page) | P2 | S (~1–2 days) |
| S2-07 | BLG-SPEC-58 | Dashboard homepage visual hierarchy review post-v6.2 | P3 | S (~0.5 day) |
| S2-08 | BLG-SPEC-59 | R-multiple cross-currency normalization specification | P2 | S (~0.5 day) |
| S2-09 | BLG-SPEC-60 | Trailing stop visual indicator frontend specification | P2 | S (~0.5 day) |
| S2-10 | BLG-SPEC-61 | Trailing stop effectiveness metric definition | P2 | S (~0.5 day) |
| S2-11 | BLG-QA-64 | Fix 12 dark spec files surfaced by Playwright glob discovery | P2 | M (~1 day) |
| S2-12 | BLG-GOV-134 | CI inline OpenAPI drift detection for `api_performance_baseline.md` | P2 | S (~0.5 day) |
| S2-13 | BLG-OPS-74 | Log Anthropic API token usage/cost per morning briefing call | P3 | S (<0.5 day) |
| S2-14 | BLG-FE-77 | Refactor `Watchlist.js` to ESLint compliance | P3 | M (~1–2 days) |
| S2-15 | BLG-OPS-61 | `BLG-OPS-13` v5.1–v5.4 endpoint baseline extension | P3 | S (~0.5–1 day) |
| S2-16 | BLG-GOV-123 | Extract Playwright test standard from `execution_prompt.md` to `shared_standards.md` | P2 | XS (~1h) |
| S2-17 | BLG-OPS-71 | System threat model document | P2 | S (~1 day) |

### Items explicitly deferred

See `docs/product/scope/scope--2026-07-08__release-v6.8-correctness-value-pullforward-debt-clearance.md` for the full table (SI-02, PO-02/PO-04, BLG-SPEC-35, BLG-GOV-74/140/141, and all non-selected backlog items).

```yaml
# state.json update (STEP 2):
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01, S2-02, S2-03, S2-04 | Backend Engineering Patterns Owner / Cybersecurity & Trust Lead / Infrastructure & Operations Owner | RISK-01, RISK-02 | Sequenced first — S2-01's root-cause finding may affect S2-06's display of corrected linkage data; S2-04 has no dependents but is cheap, clear early |
| EPIC-02 | S2-05, S2-06 | Product Owner / Head of UX & Design | RISK-03 | After EPIC-01 begins (not blocking); both are mandatory pull-forwards from the 2026-07-08 Product Value Alert |
| EPIC-03 | S2-07 – S2-17 | Head of Specs Team / PMO Lead | RISK-04, RISK-05 | Independent of EPIC-01/02; all 11 items parallelisable; first candidates to trim if capacity slips (lowest strategic weight of the three EPICs) |

**EPIC-01 (Production Correctness, Security & Infrastructure):** Resolves the only P1 correctness bug in the backlog (`BLG-BE-46`, directly blocking SI-02 gate resolution), a SQL-column-name injection-adjacent security fix, a quick anomaly review, and the credential gap (`BLG-OPS-99`) that has independently stalled data-gate verification twice now (v6.7 rebalance, v6.7 release planning).

**EPIC-02 (Product Value Pull-Forward):** Both items are the mandatory pull-forward response to the first-ever Product Value Alert (ratio 0.26, below the 0.30 floor) at the 2026-07-08 rebalance. `BLG-FEAT-52` introduces 2 new endpoints — `openapi.yaml` + `docs/specs/api_contracts/` + `backend/routers/test.py` registration is required same-commit (CLAUDE.md hard rule).

**EPIC-03 (Spec & Governance Debt Clearance):** Bundles 4 spec-debt items stale 4+ cycles (`BLG-SPEC-58/59/60/61`) with 7 further ungated, low-effort items — 3 of which (`BLG-OPS-61`, `BLG-GOV-123`, `BLG-OPS-71`) had accumulated 6–12 missed release targets with no PO re-deferral note on record, resolved directly this cycle rather than deferred again. `BLG-GOV-123` edits `execution_prompt.md` — subject to CLAUDE.md §6 Governance File Edit Checklist same-commit.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | `BLG-BE-46`'s root-cause investigation may find the linkage bug is deeper than a simple write-path fix (e.g. a service/migration gap), or that historical backfill is infeasible, exceeding the M estimate | High | Item's own AC allows a documented decision (bug fixed / backfill deferred with rationale) as a valid completion path — does not require full backfill to close; time-box investigation to the first half-day before committing to full-fix scope | null |
| RISK-02 | EPIC-01 | `BLG-OPS-99` places a live production API key into a governed-routine-readable location (`~/.api_keys` or equivalent) — a new credential-handling surface | Low | Scope to read-only application key with least-privilege access; do not commit the key value to any tracked file; document storage location only | null |
| RISK-03 | EPIC-02 | `BLG-FEAT-52`/`BLG-FEAT-71` are both UI-facing (design gate required) and `BLG-FEAT-52` introduces new endpoints — two independent compliance surfaces to get right in one EPIC | Medium | Design gate run before `plan sprint`; endpoint registration explicitly called out in Execution Plan and Decisions Record so it isn't missed at execution | null |
| RISK-04 | EPIC-03 | 11 concurrent small items increase context-switching overhead for a solo developer even though each item is individually low-risk; total sprint effort (≈13.9 days) sits near the top of the 12–14 day capacity baseline | Medium | EPIC-03 items are fully independent and parallelisable — if early-sprint velocity signals slippage, trim from EPIC-03 first (lowest strategic weight); no cross-EPIC dependency is broken by deferring any subset of EPIC-03 | null |
| RISK-05 | EPIC-03 | `BLG-GOV-123` touches a governed prompt (`execution_prompt.md`) — governance-file edits have a specific, easy-to-skip checklist (CLAUDE.md §6) | Medium | Item's own AC already requires the version bump + changelog entry; execution must additionally confirm OPERATIONAL_GUIDE §14 sync per CLAUDE.md §6 | null |

```yaml
# state.json update (STEP 3):
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

Verified: all 17 backlog items referenced by S2-01 through S2-17 exist exactly once each in `claude/backlog/backlog.md` (confirmed via direct grep — no duplicates introduced). Every S2-ID maps to exactly one EPIC-ID (EPIC-01: S2-01–04; EPIC-02: S2-05–06; EPIC-03: S2-07–17). Every RISK-ID (RISK-01 through RISK-05) declared in the Execution Plan EPIC table appears as a row in the Risk Register Summary with `Relates to` pointing to a valid EPIC-ID. No orphaned references found. PASS.

```yaml
# state.json update (STEP 3.5):
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## STEP 4 — Backlog Slice (Committed)

`stage4_backlog_slice.md` written (17 stories, ST-01 through ST-17, across EPIC-01/02/03, all Firm). Backlog lock `RP:v6.8:2026-07-08__release-v6.8` acquired, transaction `BLTX-20260708-01` prepared → committed, release-slice section written to `claude/backlog/backlog.md` with the required marker, lock released. `stage4_issue_manifest.json` written (17 entries; `--issues` defaults to `none` so no GitHub/import artefact generated at this stage).

### STEP 4.1 — Design Gate Classification

⚠ **DESIGN GATE REQUIRED before plan sprint — 2 items classified as UI-facing** (ST-05 `BLG-FEAT-52`, ST-06 `BLG-FEAT-71` — both `delegated_frontend`/autonomous-with-observable-AC: tag input/filter UI, gate-status panel). Run: `run design-gate --cycle 2026-07-08__release-v6.8`

```yaml
# state.json update (STEP 4 outcome):
artifacts.stage4_backlog_slice: pass
artifacts.stage4_issue_manifest: pass
attributes.backlog_committed: true
attributes.design_gate_required: true
status: Committed
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** 2 EPIC-02 items have a `scored_initiatives.md` row (`BLG-FEAT-52`, `BLG-FEAT-71`, both Effort Band S — matches inline estimate). All other 15 items: no matching row — tier 3, inline STEP 4 estimate used, no advisory required.

| EPIC | Stories | Estimated effort (mid-point) |
|------|---------|-------------------|
| EPIC-01 | S2-01–04 | 1.5 + 0.5 + 0.1 + 0.5 ≈ 2.6 days |
| EPIC-02 | S2-05–06 | 2.5 + 1.5 ≈ 4.0 days |
| EPIC-03 | S2-07–17 | 0.5+0.5+0.5+0.5+1.0+0.5+0.4+1.5+0.75+0.15+1.0 ≈ 7.3 days |
| **Total** | 17 stories | **≈ 13.9 days** |

**Assumptions:** `--timebox`/`--capacity` not specified; baseline is `workforce_capacity.md`'s solo-developer ~12–14 days/sprint (warn threshold >14 days).

**Outcome: PASS.** ≈13.9 days sits within the 12–14 day capacity baseline — no WARN, no phasing recommendation required. This is the largest single-sprint firm scope by story count since v6.3 (15 stories) / v6.4 (13 stories), achieved without exceeding capacity, in direct response to the instruction to maximise legitimate scope pull-through this cycle.

```yaml
# state.json update (STEP 4.5):
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Roadmap Annotation

No formal `## v6.8` roadmap section exists (Option (b)-deferred release). Per §5 fallback rule, annotated the `**Next planned release:**` line in `current_roadmap.md` §1 instead. Lock `RA:v6.8:2026-07-08__release-v6.8` acquired, `roadmap_txn.json` prepared → committed, annotation written with marker, lock released.

```yaml
# state.json update (STEP 5):
artifacts.roadmap_txn: committed
locks.roadmap_lock.status: released
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity / 5.7 Decision Record Integrity

**5.5 Cross-Stage Integrity:** All 17 S2 IDs map to exactly one of EPIC-01/02/03; EPIC IDs in `stage4_backlog_slice.md` match the Execution Plan's EPIC table exactly; all 5 RISK IDs referenced in the EPIC table appear as rows in the Risk Register Summary; no orphaned references. No Stage 2/3/4 artefact has changed since the STEP 3.5 pass. PASS.

**5.7 Decision Record Integrity:** Skipped — `artifacts.escalations` is not `present` (no escalations raised this cycle). `not_applicable`.

```yaml
# state.json update (STEP 5.5):
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```

---

## Publish Gate

All engine-specific conditions verified: `open_escalations` empty; `deferred_execution_blockers` empty; `stage4_5_capacity_check = pass`; `stage5_5_cross_stage_integrity = pass`; `stage5_7_decision_record_integrity = not_applicable`; `stage1_readiness`/`stage3_5_model_integrity = pass`; `plan_structured`/`plan_executable`/`backlog_committed = true`. Gate PASSES. Scope and Decisions documents exist; both locks released. Completion conditions met.

```yaml
# state.json terminal update:
status: Validated → Published (on STEP 9 global sync)
publish_eligible: true
sealed.sealed_utc: 2026-07-08T19:30:00Z
```

---

**Design Gate:** REQUIRED — 2 UI-facing stories (ST-05, ST-06). Run `run design-gate --cycle 2026-07-08__release-v6.8` before invoking `plan sprint`.
