**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-10-17 (ST-40, EPIC-06, v9.13, BLG-GOV-387 — v9.8–v9.10 rolling line's compound count corrected 19 → 17 of 21, matching `scripts/compute_role_share_history.py`); prior — 2026-10-16 (roadmap rebalance `2026-10-16__scheduled` §7.2 — v9.11 and v9.12 rows and breakdowns appended via `scripts/compute_role_share_history.py`; rolling aggregate v9.10–v9.12); prior — 2026-10-13 (ST-44, EPIC-06, v9.12, BLG-GOV-372 — split-credit secondary tally: History column "Split-Credit Top Role" and per-cycle "Split-credit" sub-tables, back-filled for v9.5–v9.10; raw tally unchanged); prior history retained — see prior entries in version control
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Created by:** ST-33 (BLG-GOV-341, EPIC-06, v9.8) — interim; migrated to this canonical home by ST-26 (BLG-GOV-353, EPIC-04, v9.9)

---

# Role-Share Tally History

## Provenance

Migrated verbatim from the interim cycle-scoped copy `claude/cycles/2026-09-28__release-v9.8/role_share_history.md` (left in place as a dated historical snapshot), with the v9.8 row added via `scripts/compute_role_share_history.py`. Created under Head of Specs Team write-scope ruling `ESC-EXEC-20261001-04` (agent-mediated, `execution_prompt.md` §5.3, 2026-10-05); appended thereafter by the Roadmap Engine per `roadmap_prompt.md` §4 and §7.2.

## Purpose

`roadmap_prompt.md` §7.2 (Cross-Role Workload Balance Check) tallies each shipped cycle's `sprint_backlog.md` `**Owner:**` field per role, to catch a single role silently carrying a disproportionate share of delivery across the rolling 3-cycle window. Before this file existed, §7.2 re-derived this tally by re-reading and re-parsing the raw `sprint_backlog.md` text at every rebalance — the same class of re-derivation-variance risk `product_value_ratio_history.md` already exists to avoid for the PVR metric. §7.2 now reads this file instead, appending the newest shipped cycle's row before taking its rolling window.

**Tallying method ("raw-tally"):** each ST item's `**Owner:**` field is tallied verbatim, including compound multi-role strings (e.g. `"Head of Engineering; Head of UX & Design"`) as their own distinct bucket — not split into separate per-role counts. This matches `roadmap_prompt.md` §7.2's own established method (see `decision_log.md`'s `2026-09-28__scheduled` entry: "raw-tally method — Owner-field canonicalisation patch still unapplied, 2nd carry, condition-gated, not yet stale"). A future canonicalisation patch is a separate, deferred item — not applied here.

**Split-credit secondary tally (ST-44, BLG-GOV-372, v9.12; Director of HR + PMO Lead approval, `ESC-EXEC-20261013-04`):** the script also emits a split-credit tally. Each story's credit of 1 is shared equally across the roles in its Owner string, split on `"; "`, with trailing qualifiers stripped and repeated names counted once. It is recorded in the History table's rightmost column and in a "Split-credit" sub-table under each cycle's breakdown. It is **secondary and advisory**: §7.2's 40% ceiling reads the raw tally only. Back-filled for all recorded cycles by ST-44.

**Computed with:** `scripts/compute_role_share_history.py <sprint_backlog.md path> [...]` — re-run this script at each rebalance rather than hand-tallying.

## History (one row per cycle — top role by raw-tally share)

| Cycle | Date | Total Stories | Top Role | Top Role Count | Top Role Share | Split-Credit Top Role |
|-------|------|----------------|----------|-----------------|-----------------|-----------------------|
| 2026-09-15__release-v9.5 | 2026-09-15 | 43 | Infrastructure & Operations Owner | 8 | 18.6% | Infrastructure & Operations Owner — 8.00 (18.6%) |
| 2026-09-21__release-v9.6 | 2026-09-21 | 32 | Head of Engineering; Head of UX & Design | 3 | 9.4% | Infrastructure & Operations Owner — 4.50 (14.1%) |
| 2026-09-23__release-v9.7 | 2026-09-23 | 31 | Head of Engineering | 7 | 22.6% | Head of Engineering — 7.00 (22.6%) |
| 2026-09-28__release-v9.8 | 2026-09-28 | 39 | Head of Specs Team | 12 | 30.8% | Head of Specs Team — 13.00 (33.3%) |
| 2026-09-30__release-v9.9 | 2026-09-30 | 35 | Director of Quality; QA & Testing Owner — tied with Head of Specs Team; PMO Lead | 9 | 25.7% | Head of Specs Team — 8.00 (22.9%) |
| 2026-10-06__release-v9.10 | 2026-10-06 | 21 | Frontend Specifications & UX Documentation Owner; Head of UX & Design | 3 | 14.3% | Head of Engineering — 3.67 (17.5%) |
| 2026-10-08__release-v9.11 | 2026-10-08 | 43 | QA & Testing Owner | 6 | 14.0% | QA & Testing Owner — 6.50 (15.1%) |
| 2026-10-12__release-v9.12 | 2026-10-12 | 48 | Head of Engineering; Strategy Rules & System Intent Owner | 5 | 10.4% | Head of Engineering — 6.83 (14.2%) |

**Rolling 3-cycle aggregate (v9.7–v9.9, 105 total stories — appended by roadmap rebalance `2026-10-06__scheduled`):** Head of Specs Team (solo bucket) leads at 17 stories (16.2%) — 5 (v9.7) + 12 (v9.8) + 0 (v9.9). Next: Director of Quality 13 (12.4%), Frontend Specifications & UX Documentation Owner 11 (10.5%), Head of Specs Team; PMO Lead 10 (9.5%), Director of Quality; QA & Testing Owner 9 (8.6%). Raw-tally method. Below the 40% advisory ceiling — no advisory required. **Method note:** every one of v9.9's 35 Owner values is a compound string, so v9.9 contributes nothing to any solo bucket; the raw tally under-reports single-role load for that cycle. A split-credit secondary tally is tracked as `BLG-GOV-372`.

**Rolling 3-cycle aggregate (v9.8–v9.10, 95 total stories — appended by roadmap rebalance `2026-10-08__scheduled`):** Head of Specs Team (solo bucket) leads at 12 stories (12.6%) — 12 (v9.8) + 0 (v9.9) + 0 (v9.10). Next: Head of Specs Team; PMO Lead 11 (11.6%), Director of Quality; QA & Testing Owner 9 (9.5%), Director of Quality 8 (8.4%), Frontend Specifications & UX Documentation Owner 6 (6.3%). Raw-tally method. Below the 40% advisory ceiling — no advisory required. 17 of v9.10's 21 Owner values are compound strings (`BLG-GOV-372` tracks a split-credit tally). *(Corrected from 19 on 2026-10-17, ST-40, EPIC-06, v9.13, BLG-GOV-387: re-derived with `scripts/compute_role_share_history.py`; 4 of the 21 have no `"; "` separator.)*

**Rolling 3-cycle aggregate (v9.10–v9.12, 112 total stories — appended by roadmap rebalance `2026-10-16__scheduled`, which also appended the v9.11 and v9.12 rows; neither had been added because no rebalance ran between them):** Infrastructure & Operations Owner (solo bucket) leads at 9 stories (8.0%) — 1 (v9.10) + 4 (v9.11) + 4 (v9.12). Next: QA & Testing Owner 8 (7.1%), Frontend Specifications & UX Documentation Owner; Head of UX & Design 6 (5.4%), Head of Engineering; Strategy Rules & System Intent Owner 5 (4.5%), API Contracts & Documentation Owner 4 (3.6%). Raw-tally method. Below the 40% advisory ceiling — no advisory required. Split-credit (secondary): Head of Engineering 14.00 (12.5%), Infrastructure & Operations Owner 12.33 (11.0%), QA & Testing Owner 11.00 (9.8%).

*Prior window, kept for reference:* v9.6–v9.8 (102 total stories): Head of Specs Team leads at 18 stories (17.6%), as used by the `2026-09-30__scheduled` rebalance. Below the 40% advisory ceiling.

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

Split-credit (secondary; each story's credit shared equally across its named roles):

| Role | Split Credit | Share |
|------|--------------|-------|
| Infrastructure & Operations Owner | 8.00 | 18.6% |
| QA & Testing Owner | 7.00 | 16.3% |
| API Contracts & Documentation Owner | 5.00 | 11.6% |
| Backend Engineering Patterns Owner | 4.00 | 9.3% |
| Base44 Frontend Prompt Owner | 4.00 | 9.3% |
| Data Model & Domain Schema Owner | 3.00 | 7.0% |
| FinOps & Resource Architect | 3.00 | 7.0% |
| Head of Specs Team | 3.00 | 7.0% |
| Director of HR | 2.00 | 4.7% |
| Director of Quality | 1.00 | 2.3% |
| Frontend Specifications & UX Documentation Owner | 1.00 | 2.3% |
| PMO Lead | 1.00 | 2.3% |
| Product Owner | 1.00 | 2.3% |

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

Split-credit (secondary; each story's credit shared equally across its named roles):

| Role | Split Credit | Share |
|------|--------------|-------|
| Infrastructure & Operations Owner | 4.50 | 14.1% |
| Backend Engineering Patterns Owner | 4.00 | 12.5% |
| Director of Quality | 3.00 | 9.4% |
| Head of Engineering | 3.00 | 9.4% |
| Head of UX & Design | 3.00 | 9.4% |
| Financial Reporting & Records Owner | 2.50 | 7.8% |
| Strategy Rules & System Intent Owner | 2.50 | 7.8% |
| Product Owner | 2.00 | 6.2% |
| Frontend Specifications & UX Documentation Owner | 1.50 | 4.7% |
| Head of Specs Team | 1.50 | 4.7% |
| Metrics Definitions & Analytics Owner | 1.00 | 3.1% |
| PMO Lead | 1.00 | 3.1% |
| QA Lead | 1.00 | 3.1% |
| AI Compliance & Governance Officer | 0.50 | 1.6% |
| Data Model & Domain Schema Owner | 0.50 | 1.6% |
| FinOps & Resource Architect | 0.50 | 1.6% |

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

Split-credit (secondary; each story's credit shared equally across its named roles):

| Role | Split Credit | Share |
|------|--------------|-------|
| Head of Engineering | 7.00 | 22.6% |
| Frontend Specifications & UX Documentation Owner | 6.00 | 19.4% |
| Director of Quality | 5.00 | 16.1% |
| Head of Specs Team | 5.00 | 16.1% |
| Data Model & Domain Schema Owner | 3.00 | 9.7% |
| Infrastructure & Operations Owner | 2.00 | 6.5% |
| Cybersecurity & Trust Lead | 1.00 | 3.2% |
| Financial Reporting & Records Owner | 1.00 | 3.2% |
| PMO Lead | 1.00 | 3.2% |

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

Split-credit (secondary; each story's credit shared equally across its named roles):

| Role | Split Credit | Share |
|------|--------------|-------|
| Head of Specs Team | 13.00 | 33.3% |
| Director of Quality | 8.00 | 20.5% |
| Frontend Specifications & UX Documentation Owner | 5.00 | 12.8% |
| PMO Lead | 3.50 | 9.0% |
| Infrastructure & Operations Owner | 3.00 | 7.7% |
| Head of UX & Design | 2.00 | 5.1% |
| Cybersecurity & Trust Lead | 1.00 | 2.6% |
| Data Model & Domain Schema Owner | 1.00 | 2.6% |
| Financial Reporting & Records Owner | 1.00 | 2.6% |
| Head of Engineering | 1.00 | 2.6% |
| Strategy Rules & System Intent Owner | 0.50 | 1.3% |

### 2026-09-30__release-v9.9 (35 stories)

| Role | Count | Share |
|------|-------|-------|
| Director of Quality; QA & Testing Owner | 9 | 25.7% |
| Head of Specs Team; PMO Lead | 9 | 25.7% |
| Data Model & Domain Schema Owner; Head of Specs Team | 7 | 20.0% |
| Head of Engineering; Backend Engineering Patterns Owner | 5 | 14.3% |
| Infrastructure & Operations Owner; Cybersecurity & Trust Lead | 4 | 11.4% |
| Head of UX & Design; Frontend Specifications & UX Documentation Owner | 1 | 2.9% |

Split-credit (secondary; each story's credit shared equally across its named roles):

| Role | Split Credit | Share |
|------|--------------|-------|
| Head of Specs Team | 8.00 | 22.9% |
| Director of Quality | 4.50 | 12.9% |
| PMO Lead | 4.50 | 12.9% |
| QA & Testing Owner | 4.50 | 12.9% |
| Data Model & Domain Schema Owner | 3.50 | 10.0% |
| Backend Engineering Patterns Owner | 2.50 | 7.1% |
| Head of Engineering | 2.50 | 7.1% |
| Cybersecurity & Trust Lead | 2.00 | 5.7% |
| Infrastructure & Operations Owner | 2.00 | 5.7% |
| Frontend Specifications & UX Documentation Owner | 0.50 | 1.4% |
| Head of UX & Design | 0.50 | 1.4% |

### 2026-10-06__release-v9.10 (21 stories)

| Role | Count | Share |
|------|-------|-------|
| Frontend Specifications & UX Documentation Owner; Head of UX & Design | 3 | 14.3% |
| Head of Engineering; Strategy Rules & System Intent Owner (ruling); Infrastructure & Operations Owner (production read) | 1 | 4.8% |
| Head of Engineering; Backend Engineering Patterns Owner | 1 | 4.8% |
| API Contracts & Documentation Owner; Head of Engineering | 1 | 4.8% |
| QA & Testing Owner; Head of Engineering | 1 | 4.8% |
| Strategy Rules & System Intent Owner (ruling); Backend Engineering Patterns Owner | 1 | 4.8% |
| Strategy Rules & System Intent Owner (ruling); Head of Specs Team | 1 | 4.8% |
| Head of UX & Design; Head of Engineering | 1 | 4.8% |
| Strategy Rules & System Intent Owner (ruling) | 1 | 4.8% |
| Head of Engineering; Head of UX & Design; Strategy Rules & System Intent Owner (sign-off) | 1 | 4.8% |
| AI Compliance & Governance Officer; Product Owner and Strategy Rules & System Intent Owner (sign-off) | 1 | 4.8% |
| AI Compliance & Governance Officer (sign-off); Head of Engineering | 1 | 4.8% |
| Infrastructure & Operations Owner; Cybersecurity & Trust Lead | 1 | 4.8% |
| Infrastructure & Operations Owner | 1 | 4.8% |
| QA & Testing Owner | 1 | 4.8% |
| Head of Specs Team; Strategy Rules & System Intent Owner (acknowledgement) | 1 | 4.8% |
| Head of Specs Team; PMO Lead | 1 | 4.8% |
| Frontend Specifications & UX Documentation Owner; Head of Engineering | 1 | 4.8% |
| Frontend Specifications & UX Documentation Owner | 1 | 4.8% |

Split-credit (secondary; each story's credit shared equally across its named roles):

| Role | Split Credit | Share |
|------|--------------|-------|
| Head of Engineering | 3.67 | 17.5% |
| Strategy Rules & System Intent Owner | 3.17 | 15.1% |
| Frontend Specifications & UX Documentation Owner | 3.00 | 14.3% |
| Head of UX & Design | 2.33 | 11.1% |
| Infrastructure & Operations Owner | 1.83 | 8.7% |
| Head of Specs Team | 1.50 | 7.1% |
| QA & Testing Owner | 1.50 | 7.1% |
| AI Compliance & Governance Officer | 1.00 | 4.8% |
| Backend Engineering Patterns Owner | 1.00 | 4.8% |
| API Contracts & Documentation Owner | 0.50 | 2.4% |
| Cybersecurity & Trust Lead | 0.50 | 2.4% |
| PMO Lead | 0.50 | 2.4% |
| Product Owner and Strategy Rules & System Intent Owner | 0.50 | 2.4% |

### 2026-10-08__release-v9.11 (43 stories)

| Role | Count | Share |
|------|-------|-------|
| QA & Testing Owner | 6 | 14.0% |
| Infrastructure & Operations Owner | 4 | 9.3% |
| Backend Engineering Patterns Owner | 3 | 7.0% |
| Head of Engineering; API Contracts & Documentation Owner | 3 | 7.0% |
| API Contracts & Documentation Owner | 3 | 7.0% |
| Frontend Specifications & UX Documentation Owner; Head of UX & Design | 2 | 4.7% |
| Metrics Definitions & Analytics Owner | 2 | 4.7% |
| Backend Engineering Patterns Owner; AI Compliance & Governance Officer | 1 | 2.3% |
| AI Compliance & Governance Officer; Infrastructure & Operations Owner | 1 | 2.3% |
| AI Compliance & Governance Officer; Data Model & Domain Schema Owner | 1 | 2.3% |
| AI Compliance & Governance Officer | 1 | 2.3% |
| Head of Engineering | 1 | 2.3% |
| Head of Engineering; Frontend Specifications & UX Documentation Owner | 1 | 2.3% |
| Frontend Specifications & UX Documentation Owner | 1 | 2.3% |
| Strategy Rules & System Intent Owner; Head of Engineering | 1 | 2.3% |
| Financial Reporting & Records Owner; Data Model & Domain Schema Owner | 1 | 2.3% |
| Data Model & Domain Schema Owner; Infrastructure & Operations Owner | 1 | 2.3% |
| Head of Specs Team | 1 | 2.3% |
| Head of Specs Team; Metrics Definitions & Analytics Owner | 1 | 2.3% |
| Head of Specs Team; Strategy Rules & System Intent Owner | 1 | 2.3% |
| Director of Quality; QA & Testing Owner | 1 | 2.3% |
| Financial Reporting & Records Owner | 1 | 2.3% |
| Financial Reporting & Records Owner; Strategy Rules & System Intent Owner; Head of UX & Design | 1 | 2.3% |
| Metrics Definitions & Analytics Owner; Data Model & Domain Schema Owner | 1 | 2.3% |
| Head of UX & Design | 1 | 2.3% |
| Frontend Specifications & UX Documentation Owner; API Contracts & Documentation Owner | 1 | 2.3% |
| Data Model & Domain Schema Owner | 1 | 2.3% |

Split-credit (secondary; each story's credit shared equally across its named roles):

| Role | Split Credit | Share |
|------|--------------|-------|
| QA & Testing Owner | 6.50 | 15.1% |
| API Contracts & Documentation Owner | 5.00 | 11.6% |
| Infrastructure & Operations Owner | 5.00 | 11.6% |
| Backend Engineering Patterns Owner | 3.50 | 8.1% |
| Head of Engineering | 3.50 | 8.1% |
| Data Model & Domain Schema Owner | 3.00 | 7.0% |
| Frontend Specifications & UX Documentation Owner | 3.00 | 7.0% |
| Metrics Definitions & Analytics Owner | 3.00 | 7.0% |
| AI Compliance & Governance Officer | 2.50 | 5.8% |
| Head of UX & Design | 2.33 | 5.4% |
| Head of Specs Team | 2.00 | 4.7% |
| Financial Reporting & Records Owner | 1.83 | 4.3% |
| Strategy Rules & System Intent Owner | 1.33 | 3.1% |
| Director of Quality | 0.50 | 1.2% |

### 2026-10-12__release-v9.12 (48 stories)

| Role | Count | Share |
|------|-------|-------|
| Head of Engineering; Strategy Rules & System Intent Owner | 5 | 10.4% |
| AI Compliance & Governance Officer; Backend Engineering Patterns Owner | 4 | 8.3% |
| Infrastructure & Operations Owner | 4 | 8.3% |
| Director of Quality; QA & Testing Owner | 3 | 6.2% |
| Data Model & Domain Schema Owner | 2 | 4.2% |
| Frontend Specifications & UX Documentation Owner; Head of Engineering | 2 | 4.2% |
| Backend Engineering Patterns Owner; AI Compliance & Governance Officer | 1 | 2.1% |
| PMO Lead; Head of Specs Team | 1 | 2.1% |
| Head of Specs Team; Head of Engineering | 1 | 2.1% |
| Head of Engineering; Head of Specs Team | 1 | 2.1% |
| Metrics Definitions & Analytics Owner; Head of Specs Team | 1 | 2.1% |
| Head of Specs Team; Product Owner | 1 | 2.1% |
| Director of HR; PMO Lead | 1 | 2.1% |
| QA & Testing Owner; PMO Lead | 1 | 2.1% |
| QA & Testing Owner | 1 | 2.1% |
| QA Lead | 1 | 2.1% |
| API Contracts & Documentation Owner | 1 | 2.1% |
| Head of Specs Team; Frontend Specifications & UX Documentation Owner | 1 | 2.1% |
| Metrics Definitions & Analytics Owner; Data Model & Domain Schema Owner | 1 | 2.1% |
| Strategy Rules & System Intent Owner; Head of Specs Team | 1 | 2.1% |
| Head of Engineering; Financial Reporting & Records Owner | 1 | 2.1% |
| Head of Engineering | 1 | 2.1% |
| Backend Engineering Patterns Owner; Data Model & Domain Schema Owner | 1 | 2.1% |
| Head of Engineering; Frontend Specifications & UX Documentation Owner; API Contracts & Documentation Owner | 1 | 2.1% |
| Frontend Specifications & UX Documentation Owner; Head of UX & Design | 1 | 2.1% |
| Head of Specs Team; Frontend Specifications & UX Documentation Owner; Director of HR | 1 | 2.1% |
| Head of UX & Design; Product Owner | 1 | 2.1% |
| Head of UX & Design; Frontend Specifications & UX Documentation Owner | 1 | 2.1% |
| Frontend Specifications & UX Documentation Owner | 1 | 2.1% |
| Infrastructure & Operations Owner; Backend Engineering Patterns Owner | 1 | 2.1% |
| Cybersecurity & Trust Lead | 1 | 2.1% |
| Cybersecurity & Trust Lead; Product Owner | 1 | 2.1% |
| Infrastructure & Operations Owner; Head of Engineering | 1 | 2.1% |
| Infrastructure & Operations Owner; FinOps & Resource Architect | 1 | 2.1% |

Split-credit (secondary; each story's credit shared equally across its named roles):

| Role | Split Credit | Share |
|------|--------------|-------|
| Head of Engineering | 6.83 | 14.2% |
| Infrastructure & Operations Owner | 5.50 | 11.5% |
| Frontend Specifications & UX Documentation Owner | 4.17 | 8.7% |
| Head of Specs Team | 3.83 | 8.0% |
| Backend Engineering Patterns Owner | 3.50 | 7.3% |
| Data Model & Domain Schema Owner | 3.00 | 6.2% |
| QA & Testing Owner | 3.00 | 6.2% |
| Strategy Rules & System Intent Owner | 3.00 | 6.2% |
| AI Compliance & Governance Officer | 2.50 | 5.2% |
| Cybersecurity & Trust Lead | 1.50 | 3.1% |
| Director of Quality | 1.50 | 3.1% |
| Head of UX & Design | 1.50 | 3.1% |
| PMO Lead | 1.50 | 3.1% |
| Product Owner | 1.50 | 3.1% |
| API Contracts & Documentation Owner | 1.33 | 2.8% |
| Metrics Definitions & Analytics Owner | 1.00 | 2.1% |
| QA Lead | 1.00 | 2.1% |
| Director of HR | 0.83 | 1.7% |
| FinOps & Resource Architect | 0.50 | 1.0% |
| Financial Reporting & Records Owner | 0.50 | 1.0% |
