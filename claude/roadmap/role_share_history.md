**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-10-05 (created — ST-26, EPIC-04, v9.9, BLG-GOV-353, ESC-EXEC-20261001-04; migrated from interim claude/cycles/2026-09-28__release-v9.8/role_share_history.md, v9.8 row appended)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Created by:** ST-33 (BLG-GOV-341, EPIC-06, v9.8) — interim; migrated to this canonical home by ST-26 (BLG-GOV-353, EPIC-04, v9.9)

---

# Role-Share Tally History

## Provenance

Migrated verbatim from the interim cycle-scoped copy `claude/cycles/2026-09-28__release-v9.8/role_share_history.md` (left in place as a dated historical snapshot), with the v9.8 row added via `scripts/compute_role_share_history.py`. Created under Head of Specs Team write-scope ruling `ESC-EXEC-20261001-04` (agent-mediated, `execution_prompt.md` §5.3, 2026-10-05); appended thereafter by the Roadmap Engine per `roadmap_prompt.md` §4 and §7.2.

## Purpose

`roadmap_prompt.md` §7.2 (Cross-Role Workload Balance Check) tallies each shipped cycle's `sprint_backlog.md` `**Owner:**` field per role, to catch a single role silently carrying a disproportionate share of delivery across the rolling 3-cycle window. Before this file existed, §7.2 re-derived this tally by re-reading and re-parsing the raw `sprint_backlog.md` text at every rebalance — the same class of re-derivation-variance risk `product_value_ratio_history.md` already exists to avoid for the PVR metric. §7.2 now reads this file instead, appending the newest shipped cycle's row before taking its rolling window.

**Tallying method ("raw-tally"):** each ST item's `**Owner:**` field is tallied verbatim, including compound multi-role strings (e.g. `"Head of Engineering; Head of UX & Design"`) as their own distinct bucket — not split into separate per-role counts. This matches `roadmap_prompt.md` §7.2's own established method (see `decision_log.md`'s `2026-09-28__scheduled` entry: "raw-tally method — Owner-field canonicalisation patch still unapplied, 2nd carry, condition-gated, not yet stale"). A future canonicalisation patch is a separate, deferred item — not applied here.

**Computed with:** `scripts/compute_role_share_history.py <sprint_backlog.md path> [...]` — re-run this script at each rebalance rather than hand-tallying.

## History (one row per cycle — top role by raw-tally share)

| Cycle | Date | Total Stories | Top Role | Top Role Count | Top Role Share |
|-------|------|----------------|----------|-----------------|-----------------|
| 2026-09-15__release-v9.5 | 2026-09-15 | 43 | Infrastructure & Operations Owner | 8 | 18.6% |
| 2026-09-21__release-v9.6 | 2026-09-21 | 32 | Head of Engineering; Head of UX & Design | 3 | 9.4% |
| 2026-09-23__release-v9.7 | 2026-09-23 | 31 | Head of Engineering | 7 | 22.6% |
| 2026-09-28__release-v9.8 | 2026-09-28 | 39 | Head of Specs Team | 12 | 30.8% |

**Rolling 3-cycle aggregate (v9.6–v9.8, 102 total stories):** Head of Specs Team leads at 18 stories (17.6%) — 1 (v9.6) + 5 (v9.7) + 12 (v9.8), raw-tally method (compound Owner strings that include Head of Specs Team are counted in their own buckets, not here). This matches the figure used by the `2026-09-30__scheduled` rebalance's §7.2 check (`claude/cycles/2026-09-30__scheduled/cycle_record.md`). Below the 40% advisory ceiling — no advisory required.

*Prior window, kept for reference:* v9.5–v9.7 (106 total stories): Infrastructure & Operations Owner leads at 13 stories (12.3%). This is close to, but not identical with, the 12.4% figure already recorded in `decision_log.md`'s `2026-09-28__scheduled` entry and `current_roadmap.md`'s own `last_rebalance_outcome` field; the ~0.1pp gap is rounding noise between a pooled-total percentage (this file's method) and whatever per-cycle-average method produced the recorded figure — both are consistent with the same raw-tally underlying counts. Below the 40% advisory ceiling — no advisory required.

## Full Per-Role Breakdown (backing data for the rolling-window computation)

### 2026-09-15__release-v9.5 (43 stories)

| Role | Count | Share |
|------|-------|-------|
| Infrastructure & Operations Owner | 8 | 18.6% |
| QA & Testing Owner | 7 | 16.3% |
| API Contracts & Documentation Owner | 5 | 11.6% |
| Backend Engineering Patterns Owner | 4 | 9.3% |
| Base44 Frontend Prompt Owner | 4 | 9.3% |
| FinOps & Resource Architect | 3 | 7.0% |
| Data Model & Domain Schema Owner | 3 | 7.0% |
| Head of Specs Team | 3 | 7.0% |
| Director of HR | 2 | 4.7% |
| Frontend Specifications & UX Documentation Owner | 1 | 2.3% |
| PMO Lead | 1 | 2.3% |
| Director of Quality | 1 | 2.3% |
| Product Owner | 1 | 2.3% |

### 2026-09-21__release-v9.6 (32 stories)

| Role | Count | Share |
|------|-------|-------|
| Head of Engineering; Head of UX & Design | 3 | 9.4% |
| Backend Engineering Patterns Owner | 3 | 9.4% |
| Infrastructure & Operations Owner | 3 | 9.4% |
| Director of Quality | 3 | 9.4% |
| Financial Reporting & Records Owner | 2 | 6.2% |
| Strategy Rules & System Intent Owner | 2 | 6.2% |
| Product Owner; Head of Engineering | 1 | 3.1% |
| Head of UX & Design | 1 | 3.1% |
| Head of UX & Design; Frontend Specifications & UX Documentation Owner | 1 | 3.1% |
| Strategy Rules & System Intent Owner; Backend Engineering Patterns Owner | 1 | 3.1% |
| Backend Engineering Patterns Owner; Financial Reporting & Records Owner | 1 | 3.1% |
| FinOps & Resource Architect; Infrastructure & Operations Owner | 1 | 3.1% |
| QA Lead | 1 | 3.1% |
| Data Model & Domain Schema Owner; Infrastructure & Operations Owner | 1 | 3.1% |
| Frontend Specifications & UX Documentation Owner | 1 | 3.1% |
| Head of Engineering | 1 | 3.1% |
| Metrics Definitions & Analytics Owner | 1 | 3.1% |
| Head of Specs Team; Product Owner | 1 | 3.1% |
| Product Owner | 1 | 3.1% |
| Head of Specs Team | 1 | 3.1% |
| AI Compliance & Governance Officer; Infrastructure & Operations Owner | 1 | 3.1% |
| PMO Lead | 1 | 3.1% |

### 2026-09-23__release-v9.7 (31 stories)

| Role | Count | Share |
|------|-------|-------|
| Head of Engineering | 7 | 22.6% |
| Frontend Specifications & UX Documentation Owner | 6 | 19.4% |
| Head of Specs Team | 5 | 16.1% |
| Director of Quality | 5 | 16.1% |
| Data Model & Domain Schema Owner | 3 | 9.7% |
| Infrastructure & Operations Owner | 2 | 6.5% |
| Financial Reporting & Records Owner | 1 | 3.2% |
| PMO Lead | 1 | 3.2% |
| Cybersecurity & Trust Lead | 1 | 3.2% |

### 2026-09-28__release-v9.8 (39 stories)

| Role | Count | Share |
|------|-------|-------|
| Head of Specs Team | 12 | 30.8% |
| Director of Quality | 8 | 20.5% |
| Frontend Specifications & UX Documentation Owner | 5 | 12.8% |
| Infrastructure & Operations Owner | 3 | 7.7% |
| PMO Lead | 3 | 7.7% |
| Head of UX & Design | 2 | 5.1% |
| Head of Engineering | 1 | 2.6% |
| Financial Reporting & Records Owner | 1 | 2.6% |
| Cybersecurity & Trust Lead | 1 | 2.6% |
| Data Model & Domain Schema Owner | 1 | 2.6% |
| Strategy Rules & System Intent Owner (disposition); Head of Specs Team (documentation) | 1 | 2.6% |
| Head of Specs Team; PMO Lead | 1 | 2.6% |
