Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-04
Cycle: 2026-08-04__release-v8.2
Release: v8.2

# Release Plan — v8.2

## Readiness

Preflight (STEP -1) passed all hard gates. Prior cycle `2026-08-03__release-v8.1` is `Closed` with `post_ship_complete = true` and `next_cycle_unblocked = true`. No `## v8.2` roadmap section exists; this release is scoped via the STEP -1.2 Option (b) equivalence rule, citing the same `2026-07-28__scheduled` rebalance's documented STEP 8.1 Option (b) decision already relied on by `2026-07-30__release-v8.0` and `2026-08-03__release-v8.1` (Now horizon fully empty, deferred again; no `run roadmap` invocation has occurred since to supersede it). See `run_manifest.md` for full STEP -1 detail.

**User instruction this session:** "Use full sprint capacity. Focus on user features first." Both applied literally — see `run_manifest.md` §Scope Selection Rationale for the full user-features scan. Headline finding: **5 ready, ungated, genuinely user-facing/user-adjacent backlog items found** (`BLG-FEAT-88`, `BLG-FE-105`, `BLG-FE-67`, `BLG-FE-138`, `BLG-FEAT-86`) — a materially larger pool than the single item found at each of the last two cycles, though still a minority of the full 25-item capacity-fill slice. These lead EPIC-01.

**STEP 1.4a Perennial-Return Check + STEP 1.4a.1 Sunset Criteria:** `BLG-FEAT-73`/`BLG-FEAT-74` and the Arc 5 UX-prep cluster (`BLG-FEAT-44/56`, `BLG-FE-43/45/54/58/59/62/63/68/69/70/71`) are now excluded for a **3rd consecutive cycle** (`v8.0`, `v8.1`, `v8.2`). Explicit Product Owner disposition: **(a) Keep as conditional**, no materially new gate-clearance path since `v8.1`. This is below the 4-consecutive mandatory sunset trigger (§1.4a.1) but is the last cycle before that threshold — see `run_manifest.md`.

**STEP 1.4b Within-sprint date gate check:** `BLG-FEAT-45` (Monthly P&L format review) clears its 3-month usage gate on 2026-08-05 — **tomorrow**, inside this cycle's execution window. Per the mandatory rule, this item may **not** be classified firm regardless of proximity; it remains excluded from this cycle's scope.

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

No scope changes to strategy or roadmap boundaries. This section extracts a backlog-driven scope slice (no formal roadmap release section exists yet for v8.2 — see Readiness above). Items are grouped into 5 thematic EPICs. EPIC-01 leads with the user-facing/user-adjacent items per the session instruction; EPICs 02–05 fill the remaining confirmed full-capacity band with the highest-priority ready (ungated) items across Security/Operations, Governance Process, and QA/Spec/Backend categories.

### Items in scope

| S2-ID | Epic | Item | Description |
|-------|------|------|-------------|
| S2-01 | EPIC-01 | BLG-FEAT-88 | P&L / tax record reconciliation report |
| S2-01 | EPIC-01 | BLG-FE-105 | Compliance Recheck Modal all-pass empty-state design |
| S2-01 | EPIC-01 | BLG-FE-67 | RFJ event type colour palette refinement |
| S2-01 | EPIC-01 | BLG-FE-138 | Trade Plan native form fields weak focus indicator |
| S2-01 | EPIC-01 | BLG-FEAT-86 | Drift-detection metric for the `insufficient_data` streak |
| S2-02 | EPIC-02 | BLG-SEC-27 | Provision a distinct API key for staging (shares production's key today) |
| S2-02 | EPIC-02 | BLG-OPS-128 | Detect silent staging deploy staleness (GitHub↔Render webhook) |
| S2-03 | EPIC-03 | BLG-GOV-160 | File SI-05 Phase 1 30-day effectiveness review record |
| S2-03 | EPIC-03 | BLG-GOV-213 | `velocity_metrics.md` row-count audit against cycle folder count |
| S2-03 | EPIC-03 | BLG-GOV-214 | Confirm Arc 5 composite formula accounts for v6.9 recheck events |
| S2-03 | EPIC-03 | BLG-GOV-218 | Rebalance-skip advisory should verify next release is actually scoped |
| S2-03 | EPIC-03 | BLG-GOV-265 | AI vendor Terms-of-Service & data-processing review |
| S2-03 | EPIC-03 | BLG-GOV-269 | Direct-write / governance-bypass pattern tracker |
| S2-03 | EPIC-03 | BLG-GOV-278 | Idea-intake backlog-overlap check effectiveness retrospective |
| S2-03 | EPIC-03 | BLG-GOV-279 | SI-02 production credential provisioning decision |
| S2-03 | EPIC-03 | BLG-GOV-281 | Mandatory §13 boundary pre-check at design gate for new AI-calling features |
| S2-03 | EPIC-03 | BLG-GOV-283 | Codify a `Last Updated` header-history retention convention |
| S2-03 | EPIC-03 | BLG-GOV-285 | governance_sync.yml auto-close regex cannot distinguish delegation commits |
| S2-04 | EPIC-04 | BLG-OPS-116 | Quarterly dependency-upgrade cadence for backend/requirements.txt |
| S2-04 | EPIC-04 | BLG-OPS-118 | CI cache tuning to reduce Playwright suite runtime |
| S2-04 | EPIC-04 | BLG-OPS-125 | Automated commit-message format lint (pre-commit hook) |
| S2-05 | EPIC-05 | BLG-QA-126 | Snapshot test for `SystemStatus.js` hardcoded fallback counts |
| S2-05 | EPIC-05 | BLG-SPEC-110 | Reconstruct 13 undocumented versions in `sprint_planning_changelog.md` |
| S2-05 | EPIC-05 | BLG-BE-81 | Remove dead-code duplicate `POST /test/endpoints` handler |
| S2-05 | EPIC-05 | BLG-FE-131 | Design-gate checklist addendum for motion/timing-sensitive chart interactions |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-73 / BLG-FEAT-74 | SI-02 gate unmet / §13 pre-clearance not run; perennial-return disposition, Option (a), 3rd consecutive cycle — one cycle short of the mandatory sunset trigger (§1.4a.1) | Unscheduled, pending gate clearance or forced disposition at `v8.3` |
| Arc 5 UX-prep cluster (BLG-FEAT-44/56, BLG-FE-43/45/54/58/59/62/63/68/69/70/71) | Each item's own Problem statement names a substantive unmet precondition | Unscheduled, pending respective gate clearance |
| BLG-FEAT-45 | Gate clears 2026-08-05 (tomorrow) — inside this cycle's execution window; STEP 1.4b mandates conditional-only classification for within-sprint date gates | Next cycle, once gate owner confirms clearance |
| BLG-BE-24 | Gate: `red_flag_events` table 6+ months old (post 2026-11-22) | Unscheduled, pending gate |
| BLG-OPS-48 | Self-caught during scope write-up: carries a date gate (2026-11-01, ~6 months after BLG-OPS-36 in v4.2) expressed only inside its `**Provisional-Target:**` field text ("Gate date: 2026-11-01"), not as a standalone `**Gate criteria:**` field — missed by the initial ungated-candidate scan, caught before commit on a second full-text read. See `lessons_learnt.md` Friction Item 1. | ~v4.9, no earlier than 2026-11-01 |
| Remaining ungated P2/P3 candidates not selected this cycle | Capacity — curated highest-value selection made rather than exhaustive fill; see Capacity Check for rationale | v8.3 candidate pool |

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

**Format note:** compact table per IMP-08; full acceptance criteria live in `stage4_backlog_slice.md`.

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 (5 items) | Financial Reporting & Records Owner; Head of UX & Design; Metrics Definitions & Analytics Canonical Owner | RISK-01 | None |
| EPIC-02 | S2-02 (2 items) | Cybersecurity & Trust Lead; Infrastructure & Operations Owner | RISK-02 | BLG-SEC-27 should land before/alongside BLG-OPS-128 (both touch staging environment config) |
| EPIC-03 | S2-03 (11 items) | Product Owner; Infrastructure & Operations Owner; Metrics Definitions & Analytics Canonical Owner; Head of Specs Team; AI Compliance & Governance Officer; PMO Lead; Strategy Rules & System Intent Owner; Head of Engineering | — | None — 11 independent governance-process items, no cross-dependency |
| EPIC-04 | S2-04 (3 items) | Head of Engineering; Infrastructure & Operations Owner | — | None |
| EPIC-05 | S2-05 (4 items) | QA & Testing Owner; Head of Specs Team; Head of Engineering; Head of UX & Design | — | None |

EPIC-01: carries three observable UI acceptance criteria (`BLG-FE-105` empty-state design, `BLG-FE-67` colour-palette change, `BLG-FE-138` focus-indicator change) plus `BLG-FEAT-88`'s reconciliation view rendering — classified `design_gate_required = true` at STEP 4.1 below.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Multiple observable UI acceptance criteria (empty-state design, colour palette, focus indicator, reconciliation report rendering) require Design Gate PASS before Sprint Planning may seal | Low | Run `run design-gate --cycle 2026-08-04__release-v8.2` promptly after this plan publishes; Playwright coverage or a recorded staging sign-off required per CLAUDE.md for each observable AC | null |
| RISK-02 | EPIC-02 | `BLG-SEC-27` (distinct staging API key) and `BLG-OPS-128` (deploy-staleness detection) both touch staging environment configuration; sequencing them without coordination risks a staging config conflict or a staleness-check false-positive during the key rotation window | Low | Sequence `BLG-SEC-27` first (or explicitly coordinate if run in parallel); note the rotation window in the `BLG-OPS-128` PR so a transient drift reading during rotation isn't mistaken for a fresh webhook failure | null |
| RISK-03 | Release-level | EPIC-03 (governance process cluster) is the largest single EPIC at 11 of 25 items (~44% by count, ~44% by effort) — consistent with the backlog's persistently governance/debt-heavy composition noted at the last several rebalances, but worth naming plainly rather than letting EPIC count alone obscure the skew | Medium (product-value, not delivery risk) | EPIC-01's 5 user-facing items (~23% of effort) already exceed the "≥2 build-and-ship U-items" mandatory pull-forward clause that fires on sustained Skill-Silo worsening, should that clause be checked at the next rebalance; EPIC-03's 11 items are individually small and independently divisible, making this EPIC the natural trim candidate if sprint velocity signals overrun | null |
| RISK-04 | Release-level | Scope sized to ~24.7 days midpoint against the confirmed ~24-28 day capacity band (~88-103% utilisation depending on denominator) — near top of band per the user's explicit "full sprint capacity" instruction, deliberately not padded further with low-value filler once the curated highest-value pool was exhausted (see Capacity Check) | Low | STEP 4.5 Capacity Check below confirms no over-allocation against the ceiling | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

All EPIC-ID / S2-ID / RISK-ID cross-references above resolve internally (25 items ↔ 5 S2-IDs ↔ 5 EPIC-IDs, grouped 5/2/11/3/4; 4 RISK-IDs reference EPIC-01/EPIC-02 plus 2 Release-level RISK-IDs). No orphaned references found.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup (ST-14, `shared_standards.md` §16.7):** 0 of the 25 in-scope items have a matching row in `claude/scoring/scored_initiatives.md` (all are backlog-driven items, not roadmap initiatives). Tier 3 applies uniformly: STEP 4 inline estimate used for all 25, no advisory required.

### Capacity Inputs

```
Sprint duration:    ~1-2 calendar days between sprint starts (autonomous execution engine) — per workforce_capacity.md baseline
Available FTE:      1 (solo developer / autonomous execution engine)
Total capacity:     ~24-28 working-day-equivalent units — user instructed "full sprint capacity" this session, so top of band targeted
Skill constraints:  None scarce this cycle — 5 EPICs span 12 distinct owner roles, no concurrent scarce-skill collision identified
```

### Item Effort Mapping

| EPIC | Item | Effort Band | Midpoint (days) |
|------|------|-------------|------------------|
| EPIC-01 | BLG-FEAT-88 | M | 2.5 |
| EPIC-01 | BLG-FE-105 | S | 1.0 |
| EPIC-01 | BLG-FE-67 | XS | 0.5 |
| EPIC-01 | BLG-FE-138 | S | 1.0 |
| EPIC-01 | BLG-FEAT-86 | S | 1.0 |
| EPIC-02 | BLG-SEC-27 | S | 0.5 |
| EPIC-02 | BLG-OPS-128 | S | 0.75 |
| EPIC-03 | BLG-GOV-160 | XS | 0.1 |
| EPIC-03 | BLG-GOV-213 | S | 1.0 |
| EPIC-03 | BLG-GOV-214 | S | 1.0 |
| EPIC-03 | BLG-GOV-218 | S | 0.5 |
| EPIC-03 | BLG-GOV-265 | S | 1.0 |
| EPIC-03 | BLG-GOV-269 | M | 2.5 |
| EPIC-03 | BLG-GOV-278 | S | 1.0 |
| EPIC-03 | BLG-GOV-279 | S | 1.0 |
| EPIC-03 | BLG-GOV-281 | S | 1.0 |
| EPIC-03 | BLG-GOV-283 | S | 1.0 |
| EPIC-03 | BLG-GOV-285 | S | 0.75 |
| EPIC-04 | BLG-OPS-116 | S | 1.0 |
| EPIC-04 | BLG-OPS-118 | S | 1.0 |
| EPIC-04 | BLG-OPS-125 | S | 1.0 |
| EPIC-05 | BLG-QA-126 | S | 1.0 |
| EPIC-05 | BLG-SPEC-110 | M | 1.5 |
| EPIC-05 | BLG-BE-81 | XS | 0.1 |
| EPIC-05 | BLG-FE-131 | S | 1.0 |

All 25 items carry an effort estimate. No `[ESTIMATE REQUIRED]` placeholders.

### Total Effort vs Capacity

```
Total estimated effort:  ~24.7 days midpoint
Confirmed capacity:      ~24-28 working-day-equivalent
Utilisation:             ~88-103% (depending on which end of the band is used as denominator)
Outcome:                 pass (does not exceed the ~28-day ceiling; sits at top of band per "full sprint capacity" instruction)
```

No over-allocation against the confirmed ceiling. Scope was deliberately **curated**, not exhaustively filled to the exact ceiling: the genuinely-ready P1/P2 ungated pool (16 items, all included — of the 19 nominal P1/P2 candidates found by the initial scan, 2 were excluded as the standing perennial-return disposition (`BLG-FEAT-73`/`BLG-FEAT-74`) and 1 — `BLG-OPS-48` — was self-caught as actually date-gated to 2026-11-01 despite an initial scan miss, see `lessons_learnt.md` Friction Item 1) plus the 5 user-facing items and a small set of the highest-value P3 QA/Spec/Backend debt items (4 items) reaches ~24.7 days without reaching for lower-value filler from the ~100+ remaining ungated P3 candidates — consistent with backlog-quality principles over mechanical ceiling-maximisation. No `### Phasing Recommendation` subsection is required (only on a `warn` outcome; this is `pass`).

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity

Verified: all 25 items map to their S2-ID/EPIC-ID in both `## Scope` and `## Execution Plan` (grouped 5/2/11/3/4 per EPIC); all 5 EPIC-IDs in `stage4_backlog_slice.md` match the Execution Plan table exactly; all 4 RISK-IDs referenced in the Execution Plan table appear in the Risk Register Summary; no orphaned S2/EPIC/RISK references found. `stage4_issue_manifest.json` contains exactly 25 entries (ST-01 through ST-25), one per story, labels consistent with `cycle:2026-08-04__release-v8.2`.

**5.7 Decision Record Integrity:** Skipped — `artifacts.escalations` is not `present` (no formal escalations were raised this cycle; capacity outcome was `pass`, not `warn`/`fail`, so the escalation subroutine never triggered).

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```
