Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v8.5
Cycle: 2026-08-08__release-v8.5
Last Updated: 2026-08-08

## Planning Decisions — v8.5 Frontend Correctness, Design Consistency & Security Hardening

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Scope sized to ~27.15 days — top of the confirmed ~24-28 day capacity band | Explicit user instruction: "Use fully capacity, focus on user features first." No FTE/capacity change made — band held unchanged since the 2026-07-17 raise (DL-069). | Product Owner (delegated authority) | 2026-08-08 |
| All ready `BLG-FE-*`/`BLG-FEAT-*` (ungated) items led scope selection (17 of 25 items) ahead of P2 non-frontend items | Explicit user instruction to prioritise user features. The ungated backlog pool contains 0 genuinely new user-facing feature-build items this cycle (all `BLG-FEAT-*` roadmap-flagship features remain gate-blocked — see Accepted risks). The largest available honouring of the instruction is to lead with the full ready frontend/UX pool (correctness fixes, design-consistency audits, UX review/documentation) rather than governance or backend-only debt. | Product Owner (delegated authority) | 2026-08-08 |
| 2 P1 production-correctness bugs (`BLG-BE-86`, `BLG-OPS-134`) included ahead of the frontend pool | Both are live, confirmed defects (a real staging 500, and a security check that has silently no-op'd for 5+ months) found during `v8.4` sprint execution. P1 correctness/security bugs take precedence over P2/P3 scope regardless of category. | Product Owner (delegated authority) | 2026-08-08 |
| 2 governance-process items (`BLG-GOV-288`, `BLG-GOV-289`) included despite the Skill-Silo rotation guideline favouring execution-heavy scope | Both are small (XS), self-caught process-integrity gaps found during `v8.4` sprint execution (a state-pointer reset bug and a merge-conflict-rule gap) — cheap to close now rather than let them accumulate; does not materially shift the release's execution-heavy weighting (2 of 25 items, 8%). | Product Owner (delegated authority) | 2026-08-08 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| ST-06 (EPIC-03, dead Tailwind muted-class fix) sequenced before ST-09/ST-13 (EPIC-04 contrast/design-token audits) | Those audits would otherwise assess against a known-broken CSS baseline (muted-text classes currently compile to zero CSS) — see RISK-01. | Head of Specs Team | 2026-08-08 |

### Accepted risks
| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | Product scope | No genuinely new user-facing feature is ready this cycle — the ungated backlog pool's only `Product Feature`-type items (`BLG-FEAT-29`, `BLG-FEAT-72`) are small analytics/governance-tooling additions, not net-new user capability. All roadmap-flagship features (`BLG-FEAT-73`/`74`/`76`) remain gate-blocked (`BLG-FEAT-73`/`74` formally parked at `v8.3`, sunset-triggered). This is the 6th consecutive release (`v8.0`–`v8.5`) where the "prioritise user features" instruction is honoured by leading with the largest available ready frontend/UX pool rather than genuine net-new features. No escalation raised — documented directly per `run_manifest.md §STEP 2`, consistent with every prior release's equivalent finding. | Product Owner (delegated authority) | N/A |

*(No formal escalations raised this cycle — 0 hard/conditional gate blockers encountered.)*

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-08-08__release-v8.5
