Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v4.2
Cycle: 2026-05-27__release-v4.2
Last Updated: 2026-05-29

## Release Scope — v4.2 Claude API Governance, SI-02 Pre-Work Readiness & Spec Debt

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Claude API Compliance & Security — model version pinning policy, API key security review, accountability assignment, log hygiene policy |
| S2-02 | EPIC-02 | Operational Monitoring & Baselines — api_performance_baseline update (OA-3), Claude API first monthly cost review, Claude API latency baseline |
| S2-03 | EPIC-03 | Claude API Implementation & Spec Debt — Claude API audit trail (backend), AI thesis contract update for Claude, Playwright mock strategy, prompt caching assessment |
| S2-04 | EPIC-04 | Governance Preparation & Pre-Planning — SI-02 prerequisites checklist, SI-04 pre-planning scope doc, v4.1 staging sign-off review, backlog namespace audit |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-SPEC-41 (SI-02 drift score metric) | Gate-conditional on SI-02 sprint planning imminent; gate not met (< 20 closed trades) | Before SI-02 sprint planning seals |
| BLG-GOV-62 (SI-04 §13 pre-assessment) | Gate-conditional on SI-04 sprint planning imminent; not yet scheduled | Before SI-04 sprint planning seals |
| BLG-GOV-67 (SI-05 Phase 1) | Gate: SI-01 + SI-03 live ≥ 30 days; gate clears 2026-06-21 | v4.3+ |
| BLG-OPS-37 (Anthropic tier cost assessment) | Gate: BLG-OPS-36 complete first | Post-v4.2 |
| BLG-GOV-68 (backlog inter-dependency tracking) | Gate: 20+ concurrent implementation items | Unscheduled |
| BLG-QA-36, BLG-QA-38 | Lower priority; capacity constraint | v4.3+ |
| BLG-BE-22 (optional) | Sprint 2 capacity relief valve — defer if Sprint 2 overloads | v4.3 if deferred |
| BLG-GOV-58 | COMPLETE — resolved by AUD-2026-05-27-003 (execution_prompt.md v3.29) before this planning run | — |

### Supersession note

Superseded by: v4.2 ship — 2026-05-29
Changelog: docs/product/changelog.md#v42
Verification report: claude/cycles/2026-05-27__release-v4.2/verification_report.md
Cycle: 2026-05-27__release-v4.2
