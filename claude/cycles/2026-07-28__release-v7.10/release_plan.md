Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-28
Cycle: 2026-07-28__release-v7.10
Release: v7.10

# Release Plan — v7.10

## Readiness

Preflight (STEP -1) passed all hard gates. Prior cycle `2026-07-27__release-v7.9` is `Closed` with `post_ship_complete = true` and `next_cycle_unblocked = true`. No `## v7.10` roadmap section exists; this release is scoped via the STEP -1.2 Option (b) equivalence rule, citing the `2026-07-28__scheduled` rebalance's documented STEP 8.1 Option (b) decision (Now horizon fully empty, deferred again, no newly-ready anchor content that cycle). See `run_manifest.md` for full STEP -1 detail and the STEP 1.1/1.2/1.3/1.4/1.4a/1.4b advisory outputs.

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

No scope changes to strategy or roadmap boundaries. This section extracts a backlog-driven scope slice (no formal roadmap release section exists yet for v7.10 — see Readiness above). Per explicit user instruction, items are grouped into a small set of thematic EPICs rather than one EPIC per story.

### Items in scope

| S2-ID | Epic | Item | Description |
|-------|------|------|-------------|
| S2-01 | EPIC-01 | BLG-BE-68 | Fix errors masked as HTTP 200 in portfolio_risk.py |
| S2-02 | EPIC-01 | BLG-BE-75 | Extend Alpaca backoff audit (BLG-BE-57) to Yahoo Finance, Gemini, and Claude call sites |
| S2-03 | EPIC-01 | BLG-BE-76 | Idempotency key pattern for state-mutating POST endpoints |
| S2-04 | EPIC-01 | BLG-BE-41 | Deprecated table read-path audit |
| S2-05 | EPIC-02 | BLG-SEC-22 | Secrets-scanning pre-commit/CI gate (gitleaks/trufflehog) |
| S2-06 | EPIC-02 | BLG-SEC-09 | AI rate-limit bypass test |
| S2-07 | EPIC-02 | BLG-SEC-18 | Rate-limit audit on public-facing endpoints ahead of any future auth changes |
| S2-08 | EPIC-02 | BLG-SEC-13 | Raw exception text returned in API error responses |
| S2-09 | EPIC-03 | BLG-QA-127 | Serve production build for Playwright E2E webServer instead of CRA dev server |
| S2-10 | EPIC-03 | BLG-QA-96 | Red Flag Journal auth regression test |
| S2-11 | EPIC-03 | BLG-QA-133 | Endpoint test suite coverage audit against all backend/routers/ files |
| S2-12 | EPIC-03 | BLG-QA-128 | Consumer-driven contract check: frontend API calls vs documented contracts |
| S2-13 | EPIC-04 | BLG-SPEC-102 | `position_endpoints.md` envelope claim doesn't match live `GET /positions` behaviour |
| S2-14 | EPIC-04 | BLG-SPEC-103 | `GET /positions` undocumented lifecycle fields |
| S2-15 | EPIC-04 | BLG-SPEC-104 | `trade_endpoints.md` JSON example omits documented fields |
| S2-16 | EPIC-04 | BLG-GOV-243 | OpenAPI contract linter in CI for heading-level drift |
| S2-17 | EPIC-05 | BLG-FE-122 | Rewrite calendar.js against the react-day-picker v9+ API |
| S2-18 | EPIC-05 | BLG-FE-123 | `SystemStatus.js` `categorizeEndpoint()` missing branches |
| S2-19 | EPIC-05 | BLG-FE-106 | Consolidate StrategyBenchmark.js page header onto shared PageHeader component |
| S2-20 | EPIC-05 | BLG-FE-134 | Keyboard navigation & focus-order audit |
| S2-21 | EPIC-06 | BLG-GOV-256 | design_gate_prompt.md does not sync .claude_current_state.json root pointer on gate pass |
| S2-22 | EPIC-06 | BLG-GOV-216 | Recent-rebalance recency advisory at roadmap STEP -1 |
| S2-23 | EPIC-06 | BLG-GOV-207 | Same-day scheduled-rebalance cycle_id collision handling |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-73 / BLG-FEAT-74 | SI-02 gate NOT MET / §13 determinism pre-clearance not run; standing PO perennial-return disposition (Option (b), unchanged since `manage roadmap` 2026-07-27) | Unscheduled, pending gate clearance |
| Arc 5 pre-entry/compliance-gateway UX cluster (BLG-FEAT-44/56, BLG-FE-43/45/54/58/59/62/63/68/69/70/71) + BLG-SPEC-35 | All 14 escalated to P1 as a value-judgment priority override on 2026-07-27/28, but every item's own gate criteria (e.g. "Arc 5 fully complete", "SI-02/SI-04 sprint planning imminent", "BLG-FE-45 complete") remain unmet — escalation is not a gate-clearance | Unscheduled, pending respective gate clearance |
| Remaining ~157 ungated P3 candidates not selected this cycle (e.g. BLG-FEAT-88, BLG-GOV-* process-analysis items, remaining BLG-SPEC-*/BLG-OPS-* items) | Capacity — full band reached by the 23 items above | v7.11 candidate pool |

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

**Format note:** compact table per IMP-08; full acceptance criteria live in `stage4_backlog_slice.md`.

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01, S2-02, S2-03, S2-04 | Backend Engineering Patterns Owner; Head of Backend Engineering | RISK-02 | None |
| EPIC-02 | S2-05, S2-06, S2-07, S2-08 | Cybersecurity & Trust Lead; Head of Engineering | RISK-03 | None |
| EPIC-03 | S2-09, S2-10, S2-11, S2-12 | QA Lead; QA & Testing Owner; API Contracts & Documentation Owner | RISK-04 | None |
| EPIC-04 | S2-13, S2-14, S2-15, S2-16 | API Contracts & Documentation Owner | — | None |
| EPIC-05 | S2-17, S2-18, S2-19, S2-20 | Frontend Specifications & UX Documentation Owner; Head of UX & Design; Head of Engineering | RISK-01 | None |
| EPIC-06 | S2-21, S2-22, S2-23 | Head of Specs Team; PMO Lead | — | None |

EPIC-05: carries at least two observable UI acceptance criteria (BLG-FE-106 "renders via the shared PageHeader component... no visual regression"; BLG-FE-122 "renders correctly, spot-checked") — classified `design_gate_required = true` at STEP 4.1 below.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-05 | Two items (BLG-FE-106, BLG-FE-122) carry observable UI acceptance criteria and require Design Gate PASS before Sprint Planning may seal | Medium | Run `run design-gate --cycle 2026-07-28__release-v7.10` promptly after this plan publishes; per CLAUDE.md, Playwright coverage or recorded staging sign-off required for each observable AC | null |
| RISK-02 | EPIC-01 | BLG-BE-76's idempotency-key pattern touches state-mutating trade-entry/trade-plan-creation endpoints — a live trading-critical path; an overly broad dedup-check implementation risks unintended request rejection | Low | Scope the story explicitly to an additive, opt-in dedup check (client-supplied key only); no change to existing request-handling behaviour when the key is absent | null |
| RISK-03 | EPIC-02 | BLG-SEC-13 touches ~44 call sites in `backend/main.py` — a wide surface area where an over-broad find/replace could inadvertently generalise a legitimate, safe 4xx validation message rather than only the 500-class raw-exception cases in scope | Medium | Story AC explicitly requires no change to intentional, safe 4xx error messages; QA sign-off should spot-check a sample of 4xx paths post-change | null |
| RISK-04 | EPIC-03 | BLG-QA-127 changes the CI E2E `webServer` invocation (adds a build step + new static-serve dependency) — a CI pipeline change with a plausible failure mode of breaking the existing `playwright-e2e` job if the production-build env-var injection is misconfigured | Medium | Land on a feature branch first; confirm the full 677-test suite passes against the production-served build in CI before merging; keep `npm start` as the local dev fallback per the story's own AC | null |
| RISK-05 | Release-level | Scope is deliberately sized to the top of the confirmed ~24-28 day capacity band (~26.15 days midpoint, ~93-109% utilisation) per explicit user "use the full capacity" instruction, leaving limited slack for in-sprint surprises | Medium | Accepted per explicit user instruction (see `decisions--2026-07-28__release-v7.10.md`); STEP 4.5 Capacity Check below confirms no over-allocation against the ceiling | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

All EPIC-ID / S2-ID / RISK-ID cross-references above resolve internally (23 S2-IDs ↔ 6 EPIC-IDs, grouped; 5 RISK-IDs reference EPIC-IDs present in the Scope table or "Release-level"). No orphaned references found.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** 0 of the 23 in-scope items have a matching row in `claude/scoring/scored_initiatives.md` (all are backlog-driven items, not roadmap initiatives). Tier 3 applies uniformly: STEP 4 inline estimate used for all 23, no advisory required.

### Capacity Inputs

```
Sprint duration:    ~1-2 calendar days between sprint starts (autonomous execution engine) — per workforce_capacity.md baseline
Available FTE:      1 (solo developer / autonomous execution engine)
Total capacity:     ~24-28 working-day-equivalent units
Skill constraints:  None scarce this cycle — 6 EPICs span 9 distinct owner roles, no concurrent scarce-skill collision identified
```

### Item Effort Mapping

| EPIC | Item | Effort Band | Midpoint (days) |
|------|------|-------------|------------------|
| EPIC-01 | BLG-BE-68 | S (~0.5d) | 0.5 |
| EPIC-01 | BLG-BE-75 | M | 2.0 |
| EPIC-01 | BLG-BE-76 | M | 2.0 |
| EPIC-01 | BLG-BE-41 | S (~1 day) | 1.0 |
| EPIC-02 | BLG-SEC-22 | S | 1.0 |
| EPIC-02 | BLG-SEC-09 | S (~1 day) | 1.0 |
| EPIC-02 | BLG-SEC-18 | M | 2.0 |
| EPIC-02 | BLG-SEC-13 | M (~1-2 days) | 1.5 |
| EPIC-03 | BLG-QA-127 | M (~1-2 days) | 1.5 |
| EPIC-03 | BLG-QA-96 | S | 1.0 |
| EPIC-03 | BLG-QA-133 | M | 2.0 |
| EPIC-03 | BLG-QA-128 | M | 2.0 |
| EPIC-04 | BLG-SPEC-102 | XS | 0.25 |
| EPIC-04 | BLG-SPEC-103 | XS | 0.25 |
| EPIC-04 | BLG-SPEC-104 | XS | 0.25 |
| EPIC-04 | BLG-GOV-243 | M | 2.0 |
| EPIC-05 | BLG-FE-122 | S | 1.0 |
| EPIC-05 | BLG-FE-123 | XS | 0.25 |
| EPIC-05 | BLG-FE-106 | XS (<1h) | 0.15 |
| EPIC-05 | BLG-FE-134 | M | 2.0 |
| EPIC-06 | BLG-GOV-256 | S (~0.5-1 day) | 0.75 |
| EPIC-06 | BLG-GOV-216 | S | 0.75 |
| EPIC-06 | BLG-GOV-207 | S | 0.75 |

All 23 items carry an effort estimate. No `[ESTIMATE REQUIRED]` placeholders.

### Total Effort vs Capacity

```
Total estimated effort:  ~26.15 days midpoint
Confirmed capacity:      ~24-28 working-day-equivalent
Utilisation:             ~93-109% (depending on which end of the band is used as denominator)
Outcome:                 pass (does not exceed the ~28-day ceiling; intentionally at the top of the band per explicit user "use the full capacity" instruction)
```

No over-allocation against the confirmed ceiling. STEP 3/STEP 4 scope selection includes all 23 items across 6 grouped EPICs — this is a deliberate full-capacity fill, not a phasing scenario, so no `### Phasing Recommendation` subsection is required (that subsection is required only on a `warn` outcome; this is `pass`).

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity

Verified: all 23 S2-IDs map to EPIC-IDs in both `## Scope` and `## Execution Plan` (grouped, 4/4/4/4/4/3 per EPIC); all 6 EPIC-IDs in `stage4_backlog_slice.md` match the Execution Plan table exactly; all 5 RISK-IDs referenced in the Execution Plan table appear in the Risk Register Summary; no orphaned S2/EPIC/RISK references found. `stage4_issue_manifest.json` contains exactly 23 entries (ST-01 through ST-23), one per story, labels consistent with `cycle:2026-07-28__release-v7.10`.

**5.7 Decision Record Integrity:** Skipped — `artifacts.escalations` is not `present` (no escalations were raised this cycle; capacity outcome was `pass`, not `warn`/`fail`, so the escalation subroutine never triggered).

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```
