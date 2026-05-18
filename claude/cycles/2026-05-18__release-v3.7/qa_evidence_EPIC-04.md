Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-05-18

---

## Consolidation Block

**EPIC:** EPIC-04 — Governance hardening patches (BLG-QA-20, BLG-OPS-16, BLG-FE-35, BLG-GOV-23)
**Cycle:** 2026-05-18__release-v3.7
**Sprint goal:** Deliver four governance hardening patches deferred from v3.6
**Test scenarios used:**
- `docs/testing/watchlist_scenarios.md` v1.1 (SC-WATCH-01 through SC-WATCH-06 — pre-existing)
- Playwright: `tests/e2e/research-typography.spec.js` (SC-RV-TYP-01, new — covers BLG-FE-35 AC-02)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-09 | `tests/conftest.py` (BLG-QA-20) | Session-scoped database stub conftest.py; four per-file stubs removed | All database stub tests pass; no ImportError; CLAUDE.md §2 reference updated | Pass | None |
| ST-10 | `docs/frontend/design_system.md` typography scale (BLG-FE-35) | Research page typography verified conformant; Playwright SC-RV-TYP-01 authored for regression coverage | Research page font/typography matches design_system.md; staging sign-off recorded | Pass | None |
| ST-11 | `claude/scoring/scored_initiatives.md` (BLG-GOV-23) | Arc 3 (IT-01–IT-06), Arc 4 (PO-01–05), Arc 5 (SI-01–05), Arc 6 (PS-01–05) scored rows added; header updated | All Arc 3–6 initiatives scored; existing rows preserved; Last Updated updated | Pass | None |

**QA test coverage:**
- ST-09: autonomous, no frontend — code review sufficient
- ST-10: human staging run performed 2026-05-18 (Head of UX & Design); Playwright test `tests/e2e/research-typography.spec.js` authored for permanent regression coverage
- ST-11: governance doc update — code review sufficient; no observable AC
- Regression areas checked: Research page typography (design_system.md), database stub fixture, scored_initiatives.md integrity
- Known deviations filed: None

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): ST-10 is a typography conformance check only — no new frontend code introduced
- Signed off by: Director of Quality
- Date: 2026-05-18
- Comments: ST-10 BLG-FE-35 — human staging run performed and confirmed conformant by Head of UX & Design (sachiv.patel@hotmail.co.uk) on 2026-05-18. Research page typography matches design_system.md at all checked levels. Playwright test `tests/e2e/research-typography.spec.js` (SC-RV-TYP-01, 5 assertions) added for permanent CI regression coverage. BLG-FE-35 archived to backlog_archive.md. BLG-FE-26 already archived 2026-05-17.
