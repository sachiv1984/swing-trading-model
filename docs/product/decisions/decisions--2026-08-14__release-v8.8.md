Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v8.8
Cycle: 2026-08-14__release-v8.8
Last Updated: 2026-08-14

## Planning Decisions — v8.8 Live Data-Integrity, Backend Hardening & Debt Closure

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Widen scope beyond the 7 items explicitly `Provisional-Target: v8.8` to draw additional ungated P3 backlog items | The 7-item tight scope totalled only ~5.25 days against a confirmed ~24–28 day/sprint capacity band; widening uses capacity more fully, matching the v8.7 precedent, without a formal roadmap Now-horizon anchor to defer to | Product Owner | 2026-08-14 |
| Lead the Execution Plan with EPIC-01 (live data-integrity / scheduled job coverage) | `BLG-OPS-144`/`BLG-OPS-145` are live P1 data-integrity issues (stale screener data, structurally-stuck regime badge) affecting real trading decisions today | Product Owner | 2026-08-14 |
| Weight remaining scope toward execution-heavy (Backend/Frontend/Ops) items over general governance/process debt | Per `release_planning_prompt.md` §3 Skill-Silo mitigation rotation guidance; the ungated backlog pool is otherwise dominated by governance/process items | Head of Specs Team | 2026-08-14 |
| Promote `BLG-SPEC-118` (api_changelog.md backfill) into scope | Backlog Age Advisory — spec/documentation debt aged ≥5 releases without a story assignment | Head of Specs Team | 2026-08-14 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| No cross-EPIC sequencing dependencies declared | All 7 EPICs are independently scoped this cycle; no EPIC's stories require another EPIC's stories to land first | PMO Lead | 2026-08-14 |

### Accepted risks

None.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-08-14__release-v8.8
