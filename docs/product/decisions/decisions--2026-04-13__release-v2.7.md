Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v2.7
Cycle: 2026-04-13__release-v2.7
Last Updated: 2026-04-13

## Planning Decisions — v2.7 Performance, Governance Hardening & Market Intelligence

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include BLG-OPS-14 (Supavisor pooling) as P1 in EPIC-01 | P1 item; XS effort; immediate p50 latency improvement (1–4s projected) with no code changes | Product Owner | 2026-04-13 |
| Include BLG-BE-07-FIX sequenced after BLG-OPS-14 | M effort; pooling improvement should be isolated and measured before refactor adds second variable | Head of Engineering | 2026-04-13 |
| Include BLG-GOV-18, BLG-GOV-19, BLG-GOV-16 as EPIC-02 | All P2; XS–S effort; address recurring process friction (blank DoQ sign-off, Tier 2 advisory fire, manual issue closure); governance hardening priority post-audit (score 65) | Director of Quality + Head of Specs Team | 2026-04-13 |
| Include BLG-QA-11 as ST-06 (EPIC-03) | P2; S effort; unblocks four existing structurally-correct Playwright specs from v2.5–v2.6; growing test coverage debt | QA & Testing Owner | 2026-04-13 |
| Include BLG-QA-12 as ST-07 gated on ST-06 | P3; M effort; safe to include if BLG-QA-11 is resolved; descope path exists if intercept fix cannot be generalised | QA & Testing Owner | 2026-04-13 |
| Include BLG-FEAT-17 (Market Correlation) in EPIC-04 | P2; existing Yahoo Finance pipeline confirmed sufficient; M effort; addresses user need for portfolio vs. benchmark context | Product Owner + Head of Engineering | 2026-04-13 |
| Include BLG-BE-10 (supplementary indicator fields) in EPIC-04 | P3; M effort; §13 COMPLIANT (display-only); enriches signal decision context without altering ranking | Product Owner | 2026-04-13 |
| Include BLG-SPEC-D17 and BLG-GOV-14 in EPIC-05 | P3; M effort each; governance documentation debt; audit-recommended (score 65 — at hold threshold) | Head of Specs Team + PMO Lead | 2026-04-13 |
| Defer BLG-GOV-08 (engine prompt compression) | L effort; advisory governance item; 3+ cycles in backlog — Advisory recorded in run manifest; will escalate to scope decision if deferred again at v2.8 | Product Owner | 2026-04-13 |
| Defer BLG-FEAT-16 (AI Journal Summarisation) | §13 conditions require Strategy Rules owner pre-alignment; scoping premature without that gate | Product Owner + Strategy Rules & System Intent Owner | 2026-04-13 |
| Defer BLG-GOV-13 (deduplicate archive) | Product Owner confirmation required per outstanding action (OA); not resolved in time for v2.7 planning | PMO Lead | 2026-04-13 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Sprint 1: EPIC-01, EPIC-02, EPIC-03 | Infrastructure + governance improvements first; unblocks test coverage; lower risk items | PMO Lead | 2026-04-13 |
| Sprint 2: EPIC-04, EPIC-05 | Feature and documentation work sequenced after infrastructure stable; EPIC-04 depends on confirmed §13 compliance review pattern from EPIC-02 | PMO Lead | 2026-04-13 |
| ST-07 (BLG-QA-12) gated on ST-06 (BLG-QA-11) | BLG-QA-12 uses page.route() — new spec will fail until intercept fix from BLG-QA-11 is in place | QA & Testing Owner | 2026-04-13 |
| BLG-BE-07-FIX (ST-02) sequenced after BLG-OPS-14 (ST-01) | Supavisor improvement must be measured independently before DB connection refactor is applied | Head of Engineering | 2026-04-13 |

### Accepted risks

| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | — | No Accepted Risk escalations raised in this cycle | — | — |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-04-13__release-v2.7
