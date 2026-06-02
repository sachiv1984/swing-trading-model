**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Superseded
**Release:** v4.9
**Cycle:** 2026-06-02__release-v4.9
**Last Updated:** 2026-06-02 (post-ship closure)

---

## Release Scope — v4.9 Security/CI Hardening & SI-05 Phase 1

### Items in scope

| S2-ID | Epic | Description | Priority | Notes |
|-------|------|-------------|----------|-------|
| S2-01 | EPIC-01 | Security & Dependency Hardening — npm HIGH CVEs + Anthropic SDK upgrade | P1/P2 | BLG-OPS-49, BLG-OPS-50 |
| S2-02 | EPIC-02 | CI/QA Infrastructure Strengthening — Phase B CI real Postgres + schema smoke test | P2/P3 | BLG-QA-40, BLG-QA-41 |
| S2-03 | EPIC-03 | Governance Debt Clearance — roadmap_prompt.md STEP 8.1 gate strengthening | P3 | BLG-GOV-78 |
| S2-04 | EPIC-04 | Arc 5 SI-05 Phase 1 — weekly Telegram integrity digest | P2 | **Conditional** — gate clears 2026-06-21 (BLG-GOV-67) |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-GOV-74 — AI quarterly review | Gate date 2026-08-29 post v4.9 ship; cannot complete in this cycle | v4.10 or first cycle after 2026-08-29 |
| SI-02 frontend — behavioural drift detection UI | Gate NOT met: 0 closed trades with plans; ~Nov 2026 trajectory | TBD (gate-conditional) |
| BLG-FEAT-25 — PT-04 Setup Quality Score | Gate NOT met: ~6 closed trades; ~Sep 2026 trajectory | TBD (gate-conditional) |
| All Arc 4 (PO-02/03/04/05) | Data density gates unmet | Horizon: v4.0+ |

### Conditional scope note

S2-04 (EPIC-04) is conditional on the SI-05 Phase 1 gate being confirmed cleared at sprint planning. Gate condition: SI-01 + SI-03 live ≥ 30 days (clears 2026-06-21, 30 days after SI-03 shipped v3.9 on 2026-05-22). Sprint planning must verify gate before sealing EPIC-04 stories.

### Supersession note

Superseded by: v4.9 ship — 2026-06-02
Changelog: docs/product/changelog.md#v4.9
Verification report: claude/cycles/2026-06-02__release-v4.9/verification_report.md
Cycle: 2026-06-02__release-v4.9
