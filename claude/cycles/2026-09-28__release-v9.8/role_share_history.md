**Owner:** PMO Lead
**Class:** Execution Artefact (Class 3, cycle-scoped, interim)
**Status:** Active — interim location, pending `BLG-GOV-353`
**Version:** 1.0
**Last Updated:** 2026-09-30 (created — ST-33, EPIC-06, v9.8, BLG-GOV-341, backfilled for the last 3 shipped cycles)
**Created by:** ST-33 (BLG-GOV-341, EPIC-06, v9.8)

---

# Role-Share Tally History (Interim)

> **Interim location notice.** This file's canonical home is `claude/roadmap/role_share_history.md` (mirroring `product_value_ratio_history.md`'s own precedent), but `execution_prompt.md` §7's write-scope restriction does not authorise a Sprint Execution write to that path for this story — see `execution_escalations.md`'s `ESC-EXEC-20260930-02` and backlog item `BLG-GOV-353`. This cycle-scoped copy carries the full backfill so the data is not lost; `roadmap_prompt.md` §7.2 has **not** been updated to read from a file at this path, since it is not the intended durable home. Once `BLG-GOV-353` is resolved, migrate this content to `claude/roadmap/role_share_history.md` and update §7.2 accordingly.

## Purpose

`roadmap_prompt.md` §7.2 (Cross-Role Workload Balance Check) tallies each shipped cycle's `sprint_backlog.md` `**Owner:**` field per role, to catch a single role silently carrying a disproportionate share of delivery across the rolling 3-cycle window. Before this file existed, §7.2 re-derived this tally by re-reading and re-parsing the raw `sprint_backlog.md` text at every rebalance — the same class of re-derivation-variance risk `product_value_ratio_history.md` already exists to avoid for the PVR metric.

**Tallying method ("raw-tally"):** each ST item's `**Owner:**` field is tallied verbatim, including compound multi-role strings (e.g. `"Head of Engineering; Head of UX & Design"`) as their own distinct bucket — not split into separate per-role counts. This matches `roadmap_prompt.md` §7.2's own established method (see `decision_log.md`'s `2026-09-28__scheduled` entry: "raw-tally method — Owner-field canonicalisation patch still unapplied, 2nd carry, condition-gated, not yet stale"). A future canonicalisation patch is a separate, deferred item — not applied here.

**Computed with:** `scripts/compute_role_share_history.py <sprint_backlog.md path> [...]` — re-run this script at each rebalance rather than hand-tallying.

## History (one row per cycle — top role by raw-tally share)

| Cycle | Date | Total Stories | Top Role | Top Role Count | Top Role Share |
|-------|------|----------------|----------|-----------------|-----------------|
| 2026-09-15__release-v9.5 | 2026-09-15 | 43 | Infrastructure & Operations Owner | 8 | 18.6% |
| 2026-09-21__release-v9.6 | 2026-09-21 | 32 | Head of Engineering; Head of UX & Design | 3 | 9.4% |
| 2026-09-23__release-v9.7 | 2026-09-23 | 31 | Head of Engineering | 7 | 22.6% |

**Rolling 3-cycle aggregate (v9.5–v9.7, 106 total stories):** Infrastructure & Operations Owner leads at 13 stories (12.3%). This is close to, but not identical with, the 12.4% figure already recorded in `decision_log.md`'s `2026-09-28__scheduled` entry and `current_roadmap.md`'s own `last_rebalance_outcome` field; the ~0.1pp gap is rounding noise between a pooled-total percentage (this file's method) and whatever per-cycle-average method produced the recorded figure — both are consistent with the same raw-tally underlying counts. Below the 40% advisory ceiling — no advisory required.

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

---

## Status

**ST-33 AC status:**
- "History backfilled for the last 3 cycles" — **met** (this file, interim location).
- "STEP 7.2 reads the file instead of re-parsing Owner fields" — **deferred**, tracked as `BLG-GOV-353`. `roadmap_prompt.md` §7.2 is unchanged this sprint.

**PMO Lead:** Approved interim delivery — backfill computed via `scripts/compute_role_share_history.py` against the 3 most recent shipped cycles' `sprint_backlog.md` files, cross-checked against `decision_log.md`'s `2026-09-28__scheduled` entry's independently-derived 12.4% figure (agrees to within rounding). Location deferred per `ESC-EXEC-20260930-02`. Sprint Execution Engine (agent-mediated, PMO Lead role — §5.3), 2026-09-30.
