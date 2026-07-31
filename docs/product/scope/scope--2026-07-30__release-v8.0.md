Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v8.0
Cycle: 2026-07-30__release-v8.0
Last Updated: 2026-07-31

Superseded by: v8.0 ship — 2026-07-31
Changelog: docs/product/changelog.md#v8.0
Verification report: claude/cycles/2026-07-30__release-v8.0/verification_report.md
Cycle: 2026-07-30__release-v8.0

## Release Scope — v8.0 Data Integrity, Security Follow-Through & Operational Hardening

### Items in scope
| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | `strategy_version_at_entry` field on trade/trade_plan |
| S2-02 | EPIC-01 | FX handling review post-DS-05 US market source change |
| S2-03 | EPIC-01 | FX conversion audit trail completeness check (§4.1.5 effective-rate logging) |
| S2-04 | EPIC-02 | Raw exception text leaked in 16 implicit-HTTP-200 error paths in backend/main.py |
| S2-05 | EPIC-02 | Mandatory security review checklist for new AI-calling endpoints |
| S2-06 | EPIC-02 | Trade Plan pre-entry checklist items unreachable by keyboard |
| S2-07 | EPIC-02 | Trade Plan "Abandon" modal has no focus trap or restoration |
| S2-08 | EPIC-02 | Verify `request.client.host` reflects true client IP behind Render's proxy |
| S2-09 | EPIC-02 | `.gitleaks.toml` global `[[allowlists]]` blocks use an invalid schema |
| S2-10 | EPIC-03 | Retroactive Playwright §18 anti-pattern sweep (consolidated) |
| S2-11 | EPIC-03 | Test-tagging convention (smoke/regression/critical) for selective CI runs |
| S2-12 | EPIC-03 | Synthetic trade-history data generator for gated-feature testing |
| S2-13 | EPIC-04 | Render service health-check alerting to Telegram on 5xx spike |
| S2-14 | EPIC-04 | Configure TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID as GitHub Actions repo secrets |
| S2-15 | EPIC-04 | Confirm Render rollback runbook has real execution history |
| S2-16 | EPIC-04 | Render dashboard-only build/deploy path filter audit (invisible to repo grep) |
| S2-17 | EPIC-04 | Backup & disaster recovery runbook for production database |
| S2-18 | EPIC-05 | Reusable Base44 prompt fragment library for common layouts |
| S2-19 | EPIC-06 | Structural fix for recurring cross-EPIC `execution_state.json` merge-conflict pattern |

### Items explicitly deferred
| Item | Reason | Target |
|------|--------|--------|
| BLG-OPS-48 | Real future-dated gate (`Gate date: 2026-11-01`); self-caught scope correction, see `run_manifest.md` | ~v4.9 candidate pool, no earlier than 2026-11-01 |
| BLG-FEAT-73 / BLG-FEAT-74 | SI-02 gate NOT MET / §13 determinism pre-clearance not run; standing PO perennial-return disposition | Unscheduled, pending gate clearance |
| Arc 5 pre-entry/compliance-gateway UX cluster (12 items) + BLG-SPEC-35 | Escalated to P1 as a value-judgment priority override on 2026-07-27/28, but each item's own gate criteria remain unmet | Unscheduled, pending respective gate clearance |
| Remaining ungated P2/P3 candidates not selected this cycle | Capacity — full band reached by the 19 items above | v8.1 candidate pool |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-07-30__release-v8.0
