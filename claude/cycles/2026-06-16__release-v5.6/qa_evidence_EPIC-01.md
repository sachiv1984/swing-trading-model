Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-06-16

---

## EPIC-01 — SI-05 UX & Digest Improvements

**EPIC:** EPIC-01 — SI-05 UX & Digest Improvements
**Cycle:** 2026-06-16__release-v5.6
**Sprint goal:** Ship the PT-04 governance gate re-verification, Arc 5 QA completion criteria, and SI-05 UX improvements in Sprint 1; deliver research and portfolio performance optimisations in Sprint 2.
**Test scenarios used:** tests/test_si05_digest_service.py (33 tests; 13 new for ST-01/ST-02)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 (BLG-FE-73) | backend/services/si05_digest_service.py | Added `_format_deep_links()` and `FRONTEND_URL` env var support; Risk Dashboard and Red Flag Journal deep links appended to digest when env var configured; gracefully omitted if not set | AC-01: At least one deep link present pointing to relevant app screen ✓ (code review) | AC-02: Link navigates on mobile Telegram — staging-deferred (BLG-FE-75) | AC-03: No regression to digest delivery ✓ (33 tests pass) | AC-04: HoUX sign-off — see below | Pass with notes (AC-02 staging-deferred) | None |
| ST-02 (BLG-FE-74) | backend/services/si05_digest_service.py | Added `validation_na_reason` and `override_na_reason` fields to `fetch_arc5_data_for_digest()`; `_format_pass_rate()`, `_format_override_rate()`, `_integrity_summary_line()` updated with optional `na_reason` param; backward-compatible default None | AC-01: N/A includes parenthetical reason ✓ | AC-02: "no events" and "data unavailable" produce distinct messages ✓ | AC-03: No regression ✓ (33 tests pass) | Pass | None |

**QA test coverage:**
- Scenarios run: tests/test_si05_digest_service.py (33 tests — 20 existing + 13 new)
- New test classes: TestNaReasonClarification (5 tests, ST-02 AC-01/AC-02), TestDeepLinks (4 tests, ST-01 AC-01/AC-03)
- Regression areas checked: format_si05_section, _integrity_summary_line, send_si05_digest, message truncation, retry logic
- Known deviations filed: None
- Staging-deferred AC: ST-01 AC-02 (mobile Telegram navigation) — BLG-FE-75 filed 2026-06-16

---

## Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓
- [ ] Criterion 2: All AC verifiable by code review alone — ✗ (ST-01 AC-02 is staging-only; mobile Telegram navigation cannot be verified in CI)
- [x] Criterion 3: No frontend-visible change — ✓ (no React page or UI component modified; changes are in backend Python service and test file)
- [ ] Criterion 4: N/A — autonomous class does not apply (Criterion 2 fails)

Autonomous class does NOT apply. Standard sign-off required.

**AC-02 staging gate note (CLAUDE.md §2 frontend testing gate):**
ST-01 AC-02 (link navigates correctly on mobile Telegram) is staging-only. A Playwright test cannot reproduce mobile Telegram navigation behaviour. Backlog item BLG-FE-75 ("Staging verification: SI-05 digest deep links navigate on mobile Telegram") filed 2026-06-16 as required. This backlog item reference is recorded here to satisfy the hard gate requirement.

**Head of UX & Design sign-off (ST-01 AC-04):**
Deep link placement: Risk Dashboard and Red Flag Journal links appended after the summary line, preceded by 🔗 emoji and separator. Link text is human-readable (no escaped chars in display text). Link targets are the two most relevant screens for SI-05 weekly context: Risk Dashboard (overall health snapshot) and Red Flag Journal (event detail). Sign-off: Head of UX & Design (agent-mediated, 2026-06-16) — link placement and targets confirmed appropriate per SI-05 digest spec (BLG-GOV-86 §4). No visual layout issues (Telegram renders inline links natively).

---

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked (33 tests pass; existing test suite unmodified)
- [x] For any frontend component making direct URL construction (not via api.* wrapper): N/A — no frontend changes
- Signed off by: Director of Quality (agent-mediated — §5.3)
- Date: 2026-06-16
- Comments: ST-01 AC-02 staging-deferred with BLG-FE-75 filed (hard gate satisfied). All other ACs verified by code review and unit tests. 13 new tests cover ST-01 AC-01/AC-03 and ST-02 AC-01/AC-02 with distinct message assertions. ST-02 backward-compatible (na_reason defaults to None; existing test `test_null_pass_rate_triggers_no_data_summary` still passes). No deviations.
