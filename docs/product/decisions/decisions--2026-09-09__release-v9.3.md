Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v9.3
Cycle: 2026-09-09__release-v9.3
Last Updated: 2026-09-09

## Planning Decisions — v9.3 Full-Capacity Debt Clearance

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Scope entirely backlog-driven (no formal roadmap `## v9.3` section) | 8th consecutive cycle relying on the STEP -1.2 Option(b)-equivalence rule against the `2026-08-11__scheduled` rebalance's "defer again" decision; no Now-horizon anchor exists | Product Owner (via Release Planning Engine) | 2026-09-09 |
| Select 27 of 61 ungated ready-pool items, sized to 27.50 days (top of the ~24–28 day band) | Explicit user "use full capacity" instruction; round-robin selection across all 6 represented categories (Backend, QA, Operations, Spec, Governance, Security), oldest-first within each, to spread debt clearance evenly rather than exhausting one category | Product Owner (via Release Planning Engine) | 2026-09-09 |
| `BLG-FEAT-92` remains excluded from scope | Standing reconciled-sub-scope-of-`BLG-FEAT-30` decision from `2026-09-03__release-v9.1`, unchanged; inherited gate (screener live ≥60 days AND ≥60 closed trades with attribution) remains unmet | Product Owner | 2026-09-09 (reaffirmed) |
| 34 ungated P3 items left unselected purely on capacity grounds | No gate blocks them — simply exceeds this cycle's ~24–28 day band once the 27.50d subset is scoped; carried forward as available candidates for `plan release v9.4` | Product Owner (via Release Planning Engine) | 2026-09-09 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| All 5 EPICs sequenced independently (no cross-EPIC dependency) | No item in scope depends on another EPIC's output; each EPIC owns a distinct debt category | PMO Lead (via Release Planning Engine) | 2026-09-09 |
| EPIC-05 (Governance Process Debt & Security) items sequenced serially within the sprint, not as parallel branches | 7 items span 4 owners with governance-tooling overlap (3 Base44-prompt-adjacent items); serial execution avoids cross-item collisions, matching the v9.2 EPIC-04 precedent | Head of Specs Team | 2026-09-09 |
| EPIC-03's `BLG-OPS-17` sequenced first within its EPIC as the reference cost-instrumentation pattern | `BLG-OPS-20`/`BLG-OPS-96` depend on a shared logging approach; building it once avoids duplicated instrumentation | Infrastructure & Operations Owner | 2026-09-09 |

### Accepted risks

None — no escalations raised this cycle; all preflight and hard gates passed cleanly.

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-09-09__release-v9.3
