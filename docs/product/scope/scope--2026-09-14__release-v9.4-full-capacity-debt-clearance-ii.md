Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v9.4
Cycle: 2026-09-14__release-v9.4
Last Updated: 2026-09-15

Superseded by: v9.4 ship — 2026-09-15
Changelog: docs/product/changelog.md#v9.4
Verification report: claude/cycles/2026-09-14__release-v9.4/verification_report.md
Cycle: 2026-09-14__release-v9.4

## Release Scope — v9.4 Full-Capacity Debt Clearance II

### Items in scope
| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Backend & Platform Engineering Debt — DB-level uniqueness constraint, trade_plan_id FK migration path, inverse OpenAPI drift check, deprecated-endpoint scan, scheduled-job-runner consolidation investigation |
| S2-02 | EPIC-02 | QA & Test Coverage Debt — 3 carried-forward test-coverage gaps from v9.2 PR reviews (Arc5 boundary Playwright coverage, backend pytest coverage, Settings a11y regression pinning) |
| S2-03 | EPIC-03 | Operations & Security Debt — AI cost/latency anomaly check wired to a live scheduled job/alert channel, real Q3 2026 AI cost-trend query, CI service-account token rotation, secret-scanning pre-commit hook |
| S2-04 | EPIC-04 | Spec, Documentation & Financial Reporting Debt — motion-vs-contrast guideline fix, GBP-basis FX-conversion pattern documentation, Appendix D placement review, P&L reconciliation-check spec, carried-forward-loss statement field |
| S2-05 | EPIC-05 | Governance Process & AI Compliance Debt — cross-role escalation response-time tracker, governance compute-cost attribution, data-density gate re-estimate cadence, quarterly AI-copy re-scan cadence, AI-output advisory disclosure badge, generation-time opt-in AI-output sampling hook |
| S2-06 | EPIC-06 | Frontend, UX & Product Debt — Base44 orphaned-prop audit, loading-skeleton pattern standardisation, Arc 5 compliance banner usability pass, toast-notification timing standard, trade-plan-required UI soft-nudge |

### Items explicitly deferred
| Item | Reason | Target |
|------|--------|--------|
| `BLG-GOV-178` | Literal AC already shipped at ST-22/v9.3; retained un-archived only for escalation-tracking (`ESC-EXEC-20260910-01`, now `Deferred`) | N/A — tracked via escalation, not a future release target |
| `BLG-FEAT-73`, `BLG-FEAT-74`, `BLG-FEAT-76`, `BLG-SPEC-56`, `BLG-SPEC-57`, `BLG-QA-59` | Data-quality-flagged gate-like free text (no formal `Gate` field); treated as not-ready | Re-assess once each item's named condition clears or a formal `Gate` field is added |
| 130 formally gated/conditional backlog items | No clearance evidence this cycle | Re-assess at next rebalance/release planning |
| 46 further ungated P3/P4 items (~37.50 days) | Left unselected on capacity grounds only | Available for the next release cycle |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-09-14__release-v9.4
