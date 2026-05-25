Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v4.0
Cycle: 2026-05-22__release-v4.0
Last Updated: 2026-05-25

Superseded by: v4.0 ship — 2026-05-25
Changelog: docs/product/changelog.md#v40
Verification report: claude/cycles/2026-05-22__release-v4.0/verification_report.md
Cycle: 2026-05-22__release-v4.0

## Release Scope — v4.0 Arc 5 Analytics Foundation + Spec Closure + Gemini Compliance

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Arc 5 analytics metrics — SI-01 pass/fail rate by rule (BLG-FEAT-36), red flag event frequency (BLG-FEAT-37), trade plan adherence rate (BLG-FEAT-39); backend endpoints + frontend display |
| S2-02 | EPIC-01 | E2E Playwright test coverage for SI-01→SI-03 integration path (BLG-QA-25); validates RFJ pipeline end-to-end |
| S2-03 | EPIC-02 | Ticker symbol validation on add (BLG-BE-15) — rejects non-existent or malformed tickers before universe insertion |
| S2-04 | EPIC-02 | Red flag endpoint auth and PII review (BLG-GOV-37) — security governance hygiene post-v3.9 |
| S2-05 | EPIC-03 | AI governance — Gemini audit trail (BLG-GOV-35); Gemini has been in production since v3.8 with no audit log |
| S2-06 | EPIC-03 | AI cost tracking — Gemini token/cost tracking (BLG-OPS-26) + CI/CD automated staging re-deploy on main merge (BLG-OPS-27) |

### Conditional scope

| S2-ID | Epic | Description | Gate |
|-------|------|-------------|------|
| S2-07 | EPIC-04 | PT-04 Setup Quality Score — backend endpoint + frontend display (BLG-FEAT-25) | Product Owner confirms 20+ closed trades before sprint planning seals |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| SI-02 Behavioural Drift Detection | Data-gated: requires PO-03 data, which requires PO-02 (6+ months AI journals — not met until ~Nov 2026) | v5.0 horizon |
| SI-04 Strategy Version Comparison | Data-gated: requires version-tagged trade history | v5.0 horizon |
| SI-05 Weekly Strategy Integrity Digest | Data-gated: depends on SI-02 | v5.0 horizon |
| BLG-SPEC-37 SI-02 data schema pre-def | Gate: SI-02 sprint planning not imminent this cycle | TBD |
| BLG-BE-17 SI-02 query pre-design | Gate: SI-02 sprint planning not imminent this cycle | TBD |
| BLG-BE-18 Arc 5 arch review | Gate: SI-02 sprint planning not imminent this cycle | TBD |
| BLG-GOV-39 SI-02 §13 review | Gate: SI-02 sprint planning not imminent this cycle | TBD |
| BLG-FE-40 RFJ filter state | Gate: 30 days post-v3.9 use — not met (v3.9 shipped 2026-05-22) | v4.1+ |
| BLG-SPEC-33, BLG-SPEC-34 | Already complete (OA-01+OA-02, 2026-05-22, b115b9b4) — backlog archive pending groom | Archive |
| Arc 4 remainder (PO-02/03/04) | Data-gated: 6+ months journal history | TBD |
| All Arc 6 items | Horizon: 100+ trades required | TBD |
| PT-04 (if gate unmet) | Gate not met at sprint planning — deferred_at_planning | v4.1+ |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: —
Changelog: —
Verification report: —
Cycle: 2026-05-22__release-v4.0
