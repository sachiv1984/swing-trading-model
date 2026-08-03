Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-03
Cycle: 2026-08-03__release-v8.1
Release: v8.1

# Release Plan — v8.1

## Readiness

Preflight (STEP -1) passed all hard gates. Prior cycle `2026-07-30__release-v8.0` is `Closed` with `post_ship_complete = true` and `next_cycle_unblocked = true`. No `## v8.1` roadmap section exists; this release is scoped via the STEP -1.2 Option (b) equivalence rule, citing the same `2026-07-28__scheduled` rebalance's documented STEP 8.1 Option (b) decision already relied on by `2026-07-30__release-v8.0` (Now horizon fully empty, deferred again; no `run roadmap` invocation has occurred since to supersede it, and its finding is confirmed still accurate this session). See `run_manifest.md` for full STEP -1 detail.

**User instruction this session:** "Use full capacity. Focus on user features where possible." Both applied literally — see `run_manifest.md` §Scope Selection Rationale for the full user-features scan. Headline finding, stated plainly: **exactly one ready, ungated, genuinely user-facing backlog item exists** (`BLG-FE-137`). Every `BLG-FEAT-*`/`BLG-FE-*` candidate beyond it is gate-blocked on inspection of its actual Problem statement (not just its gate label), most tracing back to the SI-02 trade-plan-linkage data-density gate that has now returned `NOT MET`/`insufficient_data` across 9+ consecutive rebalance re-checks. This is consistent with — and further evidence for — the declining Product Value Ratio advisory (0.42 → 0.38 across the last two rebalance windows) already on record.

**STEP 1.4a Perennial-Return Check:** `BLG-FEAT-73`/`BLG-FEAT-74` and the Arc 5 UX-prep cluster (`BLG-FEAT-44/56`, `BLG-FE-43/45/54/58/59/62/63/68/69/70/71`) are now excluded for a 2nd consecutive cycle (`v8.0`, `v8.1`). Explicit Product Owner disposition: **(a) Keep as conditional**, with per-item updated gate evidence (not a repeated blanket citation — see `run_manifest.md`). `BLG-GOV-280` (this cycle's own scope, S2-03) exists specifically to replace this ad hoc judgment call with a formal sunset test for future cycles.

**STEP 1.4b Within-sprint date gate check:** `BLG-FEAT-45` (Monthly P&L format review) clears its 3-month usage gate on 2026-08-05 — inside this cycle's likely execution window. Per the mandatory rule, this item may **not** be classified firm regardless of how close the date is; it remains excluded from this cycle's scope (not selected — see Scope below) and is named here only to record that the check was applied.

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

No scope changes to strategy or roadmap boundaries. This section extracts a backlog-driven scope slice (no formal roadmap release section exists yet for v8.1 — see Readiness above). Items are grouped into 7 thematic EPICs. EPIC-01 leads with the sole ready user-facing item per the session instruction; EPICs 02–07 fill the remaining ~25.25 days of confirmed full capacity with the highest-priority ready (ungated) items across Operations, Governance, QA, Spec Debt, and Backend categories.

### Items in scope

| S2-ID | Epic | Item | Description |
|-------|------|------|-------------|
| S2-01 | EPIC-01 | BLG-FE-137 | Trade Plan tag-suggestion buttons use `onMouseDown`, not keyboard-operable |
| S2-02 | EPIC-02 | BLG-OPS-127 | Recurring manual `pg_dump` backup schedule for production Supabase (Free tier — no PITR) |
| S2-03 | EPIC-03 | BLG-GOV-280 | Formal sunset criteria for perennially-returning gated backlog items |
| S2-04 | EPIC-03 | BLG-GOV-268 | Escalation path for Product Value Ratio's persistent Advisory tier |
| S2-05 | EPIC-03 | BLG-GOV-254 | Minimum capacity buffer floor recommendation for sprint planning |
| S2-06 | EPIC-03 | BLG-GOV-273 | Technical debt registry (consolidated cross-cycle view) |
| S2-07 | EPIC-03 | BLG-GOV-246 | Skill-Silo mitigation: rotate execution-heavy story assignment pattern |
| S2-08 | EPIC-03 | BLG-GOV-241 | Automated PII scan gate for new backend endpoints |
| S2-09 | EPIC-03 | BLG-GOV-240 | Governed write path for a non-empty, unversioned Now-horizon carry-forward |
| S2-10 | EPIC-04 | BLG-QA-115 | Staging sign-off: custom price alert live delivery firing (ST-02, EPIC-02, v7.5) |
| S2-11 | EPIC-04 | BLG-QA-113 | Recurring pre-sprint-planning endpoint test coverage audit |
| S2-12 | EPIC-04 | BLG-QA-129 | Cross-EPIC deviation (DEV-*) consolidation review across cycles |
| S2-13 | EPIC-04 | BLG-QA-131 | Post-parallelization Playwright shard balance audit |
| S2-14 | EPIC-05 | BLG-SPEC-72 | Revisit SI-02 Gate Status Condition 2/3 threshold definitions |
| S2-15 | EPIC-05 | BLG-SPEC-82 | Explicit §13 continuity note for v6.9 on-demand recheck |
| S2-16 | EPIC-05 | BLG-SPEC-86 | Formally define SI-02 condition-3 "sufficient data" threshold |
| S2-17 | EPIC-06 | BLG-BE-47 | Standardise pagination pattern across list endpoints (consolidated) |
| S2-18 | EPIC-06 | BLG-BE-55 | `trade_plans.position_id` historical backfill design |
| S2-19 | EPIC-07 | BLG-GOV-284 | Implement per-EPIC `execution_state.json` files (Option 1, per `ESC-EXEC-20260731-01`) |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-73 / BLG-FEAT-74 | SI-02 gate NOT MET / §13 pre-clearance not run; standing perennial-return disposition, Option (a) this cycle with updated evidence | Unscheduled, pending gate clearance |
| Arc 5 UX-prep cluster (BLG-FEAT-44/56, BLG-FE-43/45/54/58/59/62/63/68/69/70/71) | Each item's own Problem statement names a substantive unmet precondition (Arc 6 unscoped, SI-02/SI-04/SI-05 sprint-planning-imminent not true, Phase 2 channel undecided, AI-usage-pattern validation unverifiable in this checkout) — not merely a stale gate label | Unscheduled, pending respective gate clearance |
| BLG-FEAT-45 | Gate clears 2026-08-05 — inside this cycle's likely execution window; STEP 1.4b mandates conditional-only classification for within-sprint date gates, so not promoted to firm this cycle regardless of proximity | Next cycle, once gate owner confirms clearance |
| BLG-OPS-48 | Gate date 2026-11-01, unchanged | ~v4.9 candidate pool |
| BLG-BE-24 | Gate: `red_flag_events` table 6+ months old (post 2026-11-22) | Unscheduled, pending gate |
| Remaining ~140 ungated P2/P3 candidates not selected this cycle | Capacity — full band reached by the 19 items above | v8.2 candidate pool |

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

**Format note:** compact table per IMP-08; full acceptance criteria live in `stage4_backlog_slice.md`.

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 | Base44 Frontend Prompt Owner; Head of UX & Design | RISK-01 | None |
| EPIC-02 | S2-02 | Infrastructure & Operations Owner | — | None |
| EPIC-03 | S2-03, S2-04, S2-05, S2-06, S2-07, S2-08, S2-09 | Product Owner; Challenger; FinOps & Resource Architect; Head of Engineering; Director of HR; AI Compliance & Governance Officer; Head of Specs Team | — | None — 7 independent governance-process items, no cross-dependency |
| EPIC-04 | S2-10, S2-11, S2-12, S2-13 | Director of Quality; QA Lead; QA & Testing Owner | — | None |
| EPIC-05 | S2-14, S2-15, S2-16 | Product Owner; Strategy Rules & System Intent Owner; Head of UX & Design | — | None |
| EPIC-06 | S2-17, S2-18 | Backend Engineering Patterns Owner; Data Model & Domain Schema Owner | — | None |
| EPIC-07 | S2-19 | Head of Engineering | RISK-02 | None — design already signed off at `2026-07-30__release-v8.0` delivery verification (`ESC-EXEC-20260731-01`); this EPIC is implementation-only |

EPIC-01: carries one observable UI acceptance criterion (`BLG-FE-137` — keyboard/focus interaction: tabbing to a tag suggestion and pressing Enter/Space must add it) — classified `design_gate_required = true` at STEP 4.1 below, even though the EPIC is a single small fix.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | `BLG-FE-137` carries an observable UI interaction acceptance criterion (keyboard operability) and requires Design Gate PASS before Sprint Planning may seal | Low | Run `run design-gate --cycle 2026-08-03__release-v8.1` promptly after this plan publishes; Playwright coverage (extending the existing `TradeEntry.js` pattern already used correctly) or a recorded staging sign-off required per CLAUDE.md | null |
| RISK-02 | EPIC-07 | `BLG-GOV-284` is an L-effort (~3-5 day) multi-file governance change (`execution_prompt.md`, `delivery_verification_prompt.md`, `post_ship_closure.md`, `CLAUDE.md` §8, `shared_standards.md` §12) implementing a design already reviewed and signed off; a flawed implementation could introduce a new cross-EPIC state-merge failure mode in the very next multi-EPIC sprint | Medium | Head of Engineering sign-off required before the mechanism is used live; keep the existing reactive-resolution mechanism (`shared_standards.md` §12) as a documented fallback if the new mechanism misbehaves on its first live multi-EPIC sprint | null |
| RISK-03 | Release-level | Scope composition is 18 of 19 items (~25.25 of 25.75 estimated days) governance/process/QA/spec/backend debt, with only 1 item (`BLG-FE-137`, 0.5d) genuinely user-facing — the user's "focus on user features where possible" instruction was honoured by exhausting all ready ungated user-facing scope, but that scope is now confirmed structurally thin, not just this cycle's selection choice | High (product-value, not delivery risk) | `BLG-GOV-280`/`BLG-GOV-268` (this cycle's own scope) are the direct structural remedy; recommend the next `run roadmap` rebalance treat this cycle's Product Value Ratio reading as a strong signal, and that Product Owner consider whether any near-term action could accelerate SI-02 data-density clearance (e.g. prompting trade-plan usage on new trades) | null |
| RISK-04 | Release-level | Scope sized to ~25.75 days midpoint against the confirmed ~24-28 day capacity band (~92-107% utilisation depending on denominator), leaving limited slack — consistent with the top-of-band pattern used at v7.8–v8.0, applied per the user's explicit "full capacity" instruction this session | Medium | STEP 4.5 Capacity Check below confirms no over-allocation against the ceiling; EPIC-03 (7 independent items, most divisible) is the natural trim candidate if early sprint velocity signals overrun | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

All EPIC-ID / S2-ID / RISK-ID cross-references above resolve internally (19 S2-IDs ↔ 7 EPIC-IDs, grouped 1/1/7/4/3/2/1; 2 RISK-IDs reference EPIC-IDs present in the Scope table plus 2 Release-level RISK-IDs). No orphaned references found.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup (ST-14, `shared_standards.md` §16.7):** 0 of the 19 in-scope items have a matching row in `claude/scoring/scored_initiatives.md` (all are backlog-driven items, not roadmap initiatives). Tier 3 applies uniformly: STEP 4 inline estimate used for all 19, no advisory required.

### Capacity Inputs

```
Sprint duration:    ~1-2 calendar days between sprint starts (autonomous execution engine) — per workforce_capacity.md baseline
Available FTE:      1 (solo developer / autonomous execution engine)
Total capacity:     ~24-28 working-day-equivalent units — user instructed "full capacity" this session, so top of band targeted
Skill constraints:  None scarce this cycle — 7 EPICs span 11 distinct owner roles, no concurrent scarce-skill collision identified
```

### Item Effort Mapping

| EPIC | Item | Effort Band | Midpoint (days) |
|------|------|-------------|------------------|
| EPIC-01 | BLG-FE-137 | XS | 0.5 |
| EPIC-02 | BLG-OPS-127 | S | 0.5 |
| EPIC-03 | BLG-GOV-280 | S | 1.0 |
| EPIC-03 | BLG-GOV-268 | S | 1.0 |
| EPIC-03 | BLG-GOV-254 | S | 1.0 |
| EPIC-03 | BLG-GOV-273 | M | 2.5 |
| EPIC-03 | BLG-GOV-246 | M | 2.0 |
| EPIC-03 | BLG-GOV-241 | M | 2.5 |
| EPIC-03 | BLG-GOV-240 | S | 1.0 |
| EPIC-04 | BLG-QA-115 | XS | 0.5 |
| EPIC-04 | BLG-QA-113 | S | 1.0 |
| EPIC-04 | BLG-QA-129 | S | 1.0 |
| EPIC-04 | BLG-QA-131 | S | 1.0 |
| EPIC-05 | BLG-SPEC-72 | S | 0.5 |
| EPIC-05 | BLG-SPEC-82 | S | 1.0 |
| EPIC-05 | BLG-SPEC-86 | S | 1.0 |
| EPIC-06 | BLG-BE-47 | M | 2.5 |
| EPIC-06 | BLG-BE-55 | S | 1.25 |
| EPIC-07 | BLG-GOV-284 | L (~3-5 days) | 4.0 |

All 19 items carry an effort estimate. No `[ESTIMATE REQUIRED]` placeholders.

### Total Effort vs Capacity

```
Total estimated effort:  ~25.75 days midpoint
Confirmed capacity:      ~24-28 working-day-equivalent
Utilisation:             ~92-107% (depending on which end of the band is used as denominator)
Outcome:                 pass (does not exceed the ~28-day ceiling; sits at top of band per "full capacity" instruction)
```

No over-allocation against the confirmed ceiling. Scope includes all 19 items across 7 grouped EPICs — a top-of-band fill by explicit user instruction, not a phasing scenario, so no `### Phasing Recommendation` subsection is required (required only on a `warn` outcome; this is `pass`).

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity

Verified: all 19 S2-IDs map to EPIC-IDs in both `## Scope` and `## Execution Plan` (grouped 1/1/7/4/3/2/1 per EPIC); all 7 EPIC-IDs in `stage4_backlog_slice.md` match the Execution Plan table exactly; both RISK-IDs referenced in the Execution Plan table appear in the Risk Register Summary (plus RISK-03/RISK-04, Release-level); no orphaned S2/EPIC/RISK references found. `stage4_issue_manifest.json` contains exactly 19 entries (ST-01 through ST-19), one per story, labels consistent with `cycle:2026-08-03__release-v8.1`.

**5.7 Decision Record Integrity:** Skipped — `artifacts.escalations` is not `present` (no formal escalations were raised this cycle; capacity outcome was `pass`, not `warn`/`fail`, so the escalation subroutine never triggered).

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```
