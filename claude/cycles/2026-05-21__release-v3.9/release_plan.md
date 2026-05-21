Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v3.9
Cycle: 2026-05-21__release-v3.9
Last Updated: 2026-05-21

---

# Release Plan — v3.9 Screener Quality & Reliability + Arc 5 Red Flag Journal + Governance Patches

---

## Readiness

**Status: Ready**
**Mode:** standard

### Release Eligibility

| Check | Result |
|-------|--------|
| prior cycle closed | ✅ v3.8 Closed_with_actions (completed_cycle_count=24) |
| post_ship_complete | ✅ true |
| next_cycle_unblocked | ✅ true |
| roadmap entry | ✅ "Next planned release: v3.9 — TBD" |
| prior cycle velocity | ✅ 1.00 (v3.8); 6-cycle avg 0.97 |
| open escalations | ✅ none |

### Backlog Age Advisory

No spec/documentation debt items aged 2+ cycles without story assignment in v3.9 candidate scope.

### Provisional-Target Advisory

ℹ 7 item(s) carry `Provisional-Target: v3.9` — horizon-planned for this release. Multiple items with no Provisional-Target signal have gate conditions not yet met and are excluded.

### Design Dependency Scan

Design dependency scan: 0 items flagged.

---

## Scope

### S2 Scope Items

| S2-ID | Description | Source backlog items | Priority |
|-------|-------------|----------------------|----------|
| S2-01 | Screener data quality fixes — YF crumb/401 rate-limiting, sector/industry null bug, invalid ticker removal | BLG-TECH-10, BLG-BE-10, BLG-BE-11 | P1/P2 |
| S2-02 | Screener UX — degraded-run warning banner when OHLCV failure rate >20% | BLG-FE-38 | P2 |
| S2-03 | Ticker Universe enhancements — strip .L suffix from display; add company_name column | BLG-FE-37, BLG-BE-12 | P2/P3 |
| S2-04 | Arc 5 Red Flag Journal (SI-03) — log every override, skipped checklist, dismissed prompt; frontend display | Arc 5 SI-03 | Arc 5 sequence |
| S2-05 | Governance & process carry-forward patches — execution_prompt.md (test_scenarios + createPageUrl), sprint_planning_prompt.md (planning-deferred), BLG-GOV-25 dry-run support, DoQ QA enforcement | CF items 2/4/5, BLG-GOV-25, CF item 3 | P2 |

### Conditional Scope

| S2-ID | Description | Condition |
|-------|-------------|-----------|
| S2-06 | PT-04 Setup Quality Score — backend endpoint + frontend display (BLG-FEAT-25) | Gate: Product Owner confirms 20+ closed trades before sprint planning seals |

### Items Explicitly Deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-26–35 (analytics/tracking items) | Gate conditions not met; screener/PT-04 attribution requires 30–60 days history | TBD |
| BLG-QA-21–23 (Arc 2 E2E QA) | Gate: PT-04 shipped; Arc 2 feature set incomplete until PT-04 confirmed | TBD |
| BLG-OPS-17–24 (cost monitoring suite) | Gate: 30–60 days operational history required | TBD |
| BLG-GOV-26–29 (arc velocity, cross-arc map, PT-04 §13, AI audit log) | Gate conditions not met | TBD |
| BLG-SPEC-32 (external API spec template) | Gate: ≥2 external API integrations | TBD |
| SI-02 Behavioural Drift Detection | Gate: requires PO-01 + PO-03 data foundation | v4.0 horizon |
| SI-04 Strategy Version Comparison | Gate: version-tagged trade history required | v4.0 horizon |
| SI-05 Weekly Strategy Integrity Digest | Gate: requires SI-02 + SI-03 both live | v4.0 horizon |
| PO-02 Journal Pattern Recognition | Gate: 6+ months AI-summarised journal | v4.0+ |
| BLG-FE-27 (nav bar redesign), BLG-FE-39 (Arc 2 UX journey map) | Gate: PT-04 shipped | TBD |

---

## Execution Plan

### EPIC Table

| EPIC-ID | Scope items | Owner | Key risk | Sequencing |
|---------|-------------|-------|----------|------------|
| EPIC-01 | S2-01, S2-02 | Head of Backend Engineering; Head of UX & Design | RISK-01 | Sprint 1; before EPIC-03 |
| EPIC-02 | S2-03 | Head of Backend Engineering; Head of UX & Design | RISK-02 | Sprint 1; parallel-safe with EPIC-01 |
| EPIC-03 | S2-04 | Head of Backend Engineering; Head of UX & Design | RISK-03 | Sprint 2; after EPIC-01 (shares backend infra) |
| EPIC-04 | S2-05 | Head of Specs Team; Director of Quality | RISK-04 | Sprint 2; parallel-safe with EPIC-03 |
| EPIC-05 (conditional) | S2-06 | Head of Backend Engineering; Metrics & Analytics Owner; Head of UX & Design | RISK-05 | Sprint 2 if gate confirmed; else deferred |

**EPIC-01 note:** Sprint 1 priority — screener is the front-of-funnel system; P1 bugs silently degrade results for every user. BLG-TECH-10 (YF rate-limiting) is the highest-impact fix.

**EPIC-03 note:** SI-01 shipped v3.8 provides the override acknowledgement infrastructure; SI-03 extends it to the Red Flag Journal. §13 compliance confirmed — Red Flag Journal is a display-only audit log, no automated decisions.

**EPIC-04 note:** Contains 2-cycle escalation (CF item 3 — DoQ QA enforcement). Director of Quality must confirm PR template checklist item is active before v3.9 execution begins.

**EPIC-05 note:** Conditional on Product Owner confirming 20+ closed trades gate at sprint planning. If gate not confirmed, ST-13/ST-14 remain in backlog as `deferred_at_planning`.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | YF rate-limiting fix may be incomplete if YF changes auth mechanism between delivery and release | Medium | Scope crumb refresh + backoff; log failures for observability; degraded-run warning (S2-02) provides user-visible signal | null |
| RISK-02 | EPIC-02 | company_name backfill migration could fail silently if tickers_full_list.csv has encoding or missing rows | Low | Validate CSV row count vs backfill result; log rows with null company_name post-migration | null |
| RISK-03 | EPIC-03 | SI-03 Red Flag Journal requires SI-01 override acknowledgement events to be persisted in DB; if SI-01 override events are not stored, SI-03 backend has no source data | Medium | Verify SI-01 override event persistence model in v3.8 code before sprint planning; if not stored, include DB migration in ST-07 scope | null |
| RISK-04 | EPIC-04 | governance patches require prompt version bumps and OPERATIONAL_GUIDE §14 table updates across multiple files; missed update = non-compliant state | Medium | Apply CLAUDE.md §6 governance checklist; prompt-sync skill post-commit | null |
| RISK-05 | EPIC-05 | PT-04 gate (20+ closed trades) may still not be met at sprint planning | High (blocks EPIC-05) | Product Owner confirms gate status at sprint planning seal; if unmet, EPIC-05 excluded; deferred_at_planning recorded in execution_state.json | null |

---

## Capacity Check

**Effort estimates (inline — no Effort Band in scored_initiatives.md for v3.9 items):**

| EPIC | Stories | Effort estimate | Sprint |
|------|---------|----------------|--------|
| EPIC-01 | 4 | M + XS + XS + S = ~2–3 days | Sprint 1 |
| EPIC-02 | 2 | XS + S = ~0.5–1 day | Sprint 1 |
| EPIC-03 | 2 | M = ~2–3 days total | Sprint 2 |
| EPIC-04 | 4 | XS + S + M + S = ~2–3 days | Sprint 2 |
| EPIC-05 (conditional) | 2 | L = ~2–4 days | Sprint 2 (if gate met) |

**Total firm:** ~7–10 days
**Total with EPIC-05:** ~9–14 days

**Available capacity (solo dev, standard pace):** ~10–12 days across 2 sprints

**Result: WARN** — Total with EPIC-05 may approach upper bound of capacity. Firm scope is within capacity.

### Phasing Recommendation

Estimated firm scope mid-point: ~8.5 days available capacity: ~11 days — WARN when EPIC-05 conditional is included.

- **Sprint 1 (EPIC-01, EPIC-02):** ~2.5–4 days — screener bug fixes and ticker universe enhancements. Well within single-sprint capacity.
- **Sprint 2 (EPIC-03, EPIC-04, conditional EPIC-05):** ~4–6 days firm + ~2–4 days conditional. If EPIC-05 gate confirmed, Product Owner to assess phasing at sprint planning.

Ordering rationale: P1/P2 bug fixes first (screener correctness directly impacts daily workflow); new Arc 5 feature + governance patches in Sprint 2 (lower urgency, higher planning depth required).

---

## Integrity Validation — 3.5 Local Model Integrity

All S2 IDs have corresponding EPICs:
- S2-01 → EPIC-01 ✓
- S2-02 → EPIC-01 ✓
- S2-03 → EPIC-02 ✓
- S2-04 → EPIC-03 ✓
- S2-05 → EPIC-04 ✓
- S2-06 (conditional) → EPIC-05 (conditional) ✓

All RISK IDs declared in EPIC table appear in Risk Register: RISK-01 through RISK-05 ✓

No orphaned scope items or undeclared risks.

**Result: Pass**
