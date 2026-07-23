Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-23

# QA Evidence Log — EPIC-02 (v7.7)

## Consolidation Block

**EPIC:** EPIC-02 — Consolidate notification/digest surfaces
**Cycle:** 2026-07-21__release-v7.7
**Sprint goal:** Ship the four design-gated Strategy Intelligence & Notification UX items and clear seven ready capacity-fill items to fully utilise this sprint's confirmed capacity.
**Test scenarios used:** tests/e2e/nav-notification-digest-consolidation.spec.js (new, 7 scenarios), tests/e2e/alert-nav-badge.spec.js (updated selectors), tests/e2e/sidebar-nav-groups.spec.js (updated selectors), tests/test_api_contracts.py (backend, 2 new tests)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-02 | `navigation.md` v1.4; `notifications.md` v0.5; `weekly_digest.md` v0.2; `alerts_endpoints.md` v0.6 | Removed duplicate "Alerts" nav item (Tools group); "Notifications" (System group) is sole nav path, inherits alert-count badge (propagation moved from Tools→System group header). "Weekly Digest" moved from Analytics to System group, adjacent to Notifications. Weekly Digest's "Alerts Fired (7d)"/"Alerts Dismissed (7d)" values now deep-link to `/notifications?since_days=7[&read=true]`. Added optional `since_days`/`read` query params to `GET /notifications` (backend + contract + openapi.yaml, same commit). Extended "Daily Portfolio Summary" preference row helper text with a cross-link to Weekly Digest. | No two nav entries route to the same page without a visual indicator (AC1); Weekly Digest discoverable from same nav grouping as Alerts/Notifications (AC2); Weekly Digest alert-count values link to filtered notification history (AC3); Daily Portfolio Summary vs Weekly Digest differentiated via copy+cross-link (AC4); `GET /notifications` gets `since_days`/`read` params, same-commit contract update | Pass | None |

**QA test coverage:**
- Scenarios run: `nav-notification-digest-consolidation.spec.js` (SC-NND-01 through SC-NND-07 — no "Alerts" nav entry exists; Weekly Digest + Notifications share System group; both alert-count deep-links present with correct href; clicking a deep-link navigates to the filtered feed; Notification Feed forwards `since_days`/`read` to its API call; Daily Portfolio Summary row links to Weekly Digest); `alert-nav-badge.spec.js` (SC-ANB-01 through SC-ANB-08, rewritten for the System-group badge — item-level when System expanded, group-header propagation when collapsed); `sidebar-nav-groups.spec.js` (SC-SNV-08 updated group membership lists); `tests/test_api_contracts.py::TestAlertsEndpoints` (`test_get_notifications_forwards_since_days_and_read`, `test_get_notifications_rejects_non_positive_since_days` — both passing, verified via `backend/.venv/bin/python3 -m pytest tests/test_api_contracts.py -k notification -v`, 4/4 passed)
- Regression areas checked: full backend suite (`backend/.venv/bin/python3 -m pytest -q` — 747 passed, 2 skipped, no regressions); frontend production build (`CI=false npm run build`) succeeds with no new warnings introduced by this story's files
- Known deviations filed: None

**Environment note:** Playwright browser install is blocked in this local sandbox (`Playwright does not support chromium on ubuntu26.04-x64` — same constraint noted in `qa_evidence_EPIC-01.md`). The new and updated Playwright spec files were reviewed line-by-line by agent-mediated Director of Quality review against the actual `Layout.js`/`WeeklyDigest.js`/`Notifications.js` implementation (selector-by-selector) and will execute under `.github/workflows/quality_gate.yml`'s CI runner (a supported OS).

**Agent-mediated review finding (non-blocking, resolved same-branch):** initial `since_days` SQL used `(%s || ' days')::interval`, valid but inconsistent with this codebase's established `NOW() - (%s * INTERVAL '1 day')` idiom (used elsewhere in the same file and in `database.py`). Corrected in commit `6255f349` for consistency; re-verified via the same 4 passing tests.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, all navigation uses `<Link>`/`createPageUrl()` per existing convention; `GET /notifications` calls continue to use `apiFetch`/`API_BASE_URL` per existing pattern
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-07-23
- Comments: EPIC-02 has frontend-visible changes (Layout.js, WeeklyDigest.js, Notifications.js, NotificationPreferences.js) — BLG-GOV-19 autonomous class does not apply (criterion 3 unmet). All 4 observable ACs are Playwright-covered (see Test scenarios above); local execution blocked by sandbox OS (see Environment note) — CI will execute in `quality_gate.yml`. Human Director of Quality review and PR-level sign-off still required before merge per §5.3 "Always-human gates".

## Frontend Specs & UX Documentation Owner Confirmation (named authority, per sprint_backlog.md ST-02 Verification field)

- Confirmed implementation aligns with all 3 locked frontend specs (`navigation.md` v1.4, `notifications.md` v0.5, `weekly_digest.md` v0.2) — nav group structure, badge propagation logic, deep-link URL formats, and preference-row helper-text copy all match the specs exactly (byte-for-byte on link hrefs and copy text).
- Signed off by: Sprint Execution Engine (agent-mediated, Frontend Specs & UX Documentation Owner role — §5.3)
- Date: 2026-07-23
- Comments: No deviations found; no spec updates required.
