**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Published
**Version:** 1.0
**Release:** v3.8
**Cycle:** 2026-05-19__release-v3.8
**Last Updated:** 2026-05-19
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Scope Document — v3.8

**Theme:** Arc 5 Strategy Integrity Foundation + Trade Plan Form Enhancements + Ticker Universe Management

---

## Items in scope

| S2-ID | Scope Item | EPIC | Effort | Conditional? |
|-------|-----------|------|--------|-------------|
| S2-01 | Arc 5 Foundation — SI-01 Pre-Entry Rule Validation Gate (§13 gate + backend advisory + frontend advisory) | EPIC-01 | M+M+XS | No — §13 review gate story required in Sprint 1 |
| S2-02 | Arc 2 Completion — PT-04 Setup Quality Score (deterministic score from own trade history) | EPIC-02 | M+M | Yes — conditional on 20+ closed trades gate; PO decision due 2026-05-22 |
| S2-03 | Trade Plan Form Enhancements — setup type classification (BLG-FEAT-23) + news context panel (BLG-FE-36) + AI-assisted thesis (BLG-FEAT-24) | EPIC-03 | S+S+M | No |
| S2-04 | Ticker Universe Management Page — full CRUD UI; retire public.tickers startup sync (BLG-FEAT-22) | EPIC-04 | M | No |
| S2-05 | Governance Debt — gh_issue_template.md §14 table entry (BLG-GOV-24) + DoQ sign-off enforcement mechanism | EPIC-04 | XS+XS | No |

---

## Items explicitly deferred

| Item | Rationale | Target |
|------|-----------|--------|
| SI-03 Red Flag Journal | Depends on SI-01 operational first; defer to v3.9 after SI-01 live | v3.9 |
| PO-02 Journal Pattern Recognition | Gate not met: 6+ months of AI-summarised journal entries required | TBD (gate) |
| PO-03 Behavioural Error Taxonomy | Requires PO-01 + PO-02 data | TBD (gate) |
| PO-04 Reflection ↔ Outcome Correlation | Requires PO-01 + PO-02; 50+ trades with plans | TBD (gate) |
| PO-05 Lightweight Replay Mode | Very high effort; requires IT-06 + substantial history | TBD (gate) |
| SI-02 Behavioural Drift Detection | Requires PO-01 + PO-03 data foundation | v4.0+ |
| SI-04 Strategy Version Comparison | Requires version-tagged trade history from Arc 2 | v4.0+ |
| SI-05 Weekly Strategy Integrity Digest | Depends on SI-02 + SI-03 | v4.0+ |
| BLG-FEAT-20 Net-of-costs tracking | Arc 3/4 data model sequencing constraint | Arc 3/4 context |

---

## Supersession note

*(To be completed at Post-Ship Closure — Step 4)*
