Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-31

# QA Evidence — EPIC-02 (Backend Hardening & Frontend Accessibility)

**EPIC:** EPIC-02 — Backend Hardening & Frontend Accessibility
**Cycle:** 2026-07-30__release-v8.0
**Sprint goal:** Close the platform's outstanding backend error-masking, security-hardening, and FX/data-spec debt while shipping keyboard/focus accessibility fixes to the Trade Plan flow, strengthening QA/CI test infrastructure, hardening operational alerting and disaster-recovery readiness, and fixing the recurring cross-EPIC `execution_state.json` merge-conflict pattern.
**Test scenarios used:** `tests/test_st04_implicit_200_error_paths_fixed.py`, `tests/e2e/entry-checklist.spec.js` (SC-CL-08–SC-CL-11), `tests/e2e/epic03-v34-frontend.spec.js` (SC-E03-17–SC-E03-20), `.github/workflows/st08-proxy-ip-verification.yml` (live production run 30611215629), full backend regression suite.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-04 | `docs/specs/api_contracts/conventions.md#13` | Fixed 17 implicit-HTTP-200 error paths in `backend/main.py` (13 more than the ticket's stated count) — canonical `{status,message}` 500 envelope where applicable, `traceback.print_exc()` restored where missing. | All raw-exception-leaking error paths return proper HTTP 500 with no leaked exception text; regression tests added. | Pass | None — scope expanded from 16→17 found paths, all fixed within story |
| ST-05 | `docs/specs/security/ai_endpoint_security_checklist.md` | New mandatory security review checklist for AI-calling endpoints (rate limiting, cost gating, prompt-injection awareness), wired into `design_gate_prompt.md` STEP 2.2. | Checklist created and referenced from the design gate process. | Pass | None |
| ST-06 | `docs/design/2026-07-30__release-v8.0/entry-checklist-keyboard-accessibility/decision_record.md` | `EntryChecklist.js` checklist items converted to WAI-ARIA checkbox pattern (role, aria-checked, tabIndex, Space/Enter key handling). 4 new Playwright tests using real keyboard events. | All checklist items keyboard-reachable and operable (Tab order, Space/Enter toggle, read-only items skipped). | Pass | None — initial test draft used programmatic `.focus()` instead of real keyboard events, corrected during Head of UX & Design review before sign-off |
| ST-07 | `docs/design/2026-07-30__release-v8.0/abandon-modal-focus-trap/decision_record.md` | Hand-rolled Abandon modal replaced with Radix Dialog primitive; fixed a real focus-restoration bug (`onCloseAutoFocus` + explicit trigger ref). 4 new Playwright tests. | Modal traps focus, restores it to the trigger on close (Escape/Cancel), matches existing app modal pattern. | Pass | Decision record's tab-order table corrected to match tested DOM reality (Cancel-then-Submit, not the originally drafted order) — visual layout deliberately unchanged |
| ST-08 | `claude/cycles/2026-07-30__release-v8.0/release_plan.md#RISK-02`; `docs/security/rate_limit_audit_2026-07-29.md` Part 3 | Automated live production verification (`.github/workflows/st08-proxy-ip-verification.yml`, two-job `workflow_dispatch`) of whether `request.client.host` reflects the true client IP behind Render's proxy. | Live verification result recorded — confirmed accurate or fixed + re-verified. | Pass | None — confirmed accurate (no proxy-IP collapse), no uvicorn config change needed |
| ST-09 | `.gitleaks.toml` | Rewrote 4 allowlist blocks using schema-valid `[[rules.allowlists]]`/`[allowlist]` forms (bare `[[allowlists]]` was silently ignored by gitleaks v8.21.2). | CI secret scanning correctly suppresses known false positives without masking real findings. | Pass | None — 3 real false-positive findings confirmed suppressed post-fix, 0 leaks on main-scoped scan |

**ST-08 live-fire test detail:**
- Trigger: `gh workflow run "ST-08 Proxy IP Verification"` (required an early scoped merge to `main` first — PR #1164 — since `workflow_dispatch` only triggers for workflows present on the default branch)
- Run: https://github.com/sachiv1984/swing-trading-model/actions/runs/30611215629
- Job A (runner IP `135.232.227.144`): rate-limited (HTTP 429) on attempt 61, matching `_HEALTH_LIMIT=60` (`backend/main.py:1097`) exactly
- Job B (separate runner, IP `172.182.243.52`): probed ~6s later, got HTTP 200 — not rate-limited
- Conclusion: no proxy-IP collapse; `request.client.host` correctly distinguishes real per-client IPs in production

**QA test coverage:**
- Scenarios run: `tests/test_st04_implicit_200_error_paths_fixed.py` (19 tests), `tests/e2e/entry-checklist.spec.js` (11 tests, 4 new), `tests/e2e/epic03-v34-frontend.spec.js` (20 tests, 4 new) plus `tests/e2e/trade-plan.spec.js` (33 tests, regression), all verified passing against a real browser (system chromium). Full backend suite (925 passed, 2 skipped) confirmed no regressions. Live production diagnostic (ST-08, above) run against the real Render deployment.
- Regression areas checked: all backend error paths touched by ST-04; Trade Plan entry checklist and Abandon modal interaction flows (ST-06/ST-07); secret-scanning CI (ST-09); public `/health` rate limiting (ST-08).
- Known deviations filed: None outstanding — the two noted above (ST-04 scope expansion, ST-07 decision record correction) were resolved within their own stories, not deferred.

**Frontend-visible changes (ST-06, ST-07):** both stories touch `src/components/**`/`src/pages/**`. Per CLAUDE.md's Playwright-or-staging-sign-off requirement, all observable ACs (keyboard reachability, focus trap, focus restoration) are covered by real-browser Playwright tests using genuine keyboard events (not programmatic `.focus()`) — see SC-CL-08–SC-CL-11 and SC-E03-17–SC-E03-20 above. No AC was deferred to staging-only sign-off.

---

## Sign-off

This EPIC is **not** eligible for BLG-GOV-19 autonomous-class sign-off: ST-08 is `delegated_backend` (required live production verification) and ST-06/ST-07 are frontend-visible, so the single-signer autonomous path does not apply. Sign-off is by story-level domain owner, agent-mediated per §5.3, consolidated here:

| Story | Reviewing role | Method | Result | Date |
|-------|-----------------|--------|--------|------|
| ST-04 | Head of Engineering | Agent-mediated | Approved | 2026-07-30 |
| ST-05 | Cybersecurity & Trust Lead | Agent-mediated | Approved | 2026-07-30 |
| ST-06 | Head of UX & Design | Agent-mediated | Approved (retry 1 of 2 — fixed keyboard-event test issue) | 2026-07-30 |
| ST-07 | Head of UX & Design | Agent-mediated | Approved | 2026-07-30 |
| ST-08 | Cybersecurity & Trust Lead | Agent-mediated | Approved — independently re-pulled raw GitHub Actions job logs, verified timing/window-safety math and cross-call-site generalization; also fixed a stale Sign-off block in `rate_limit_audit_2026-07-29.md` during review | 2026-07-31 |
| ST-09 | Cybersecurity & Trust Lead | Agent-mediated | Approved | 2026-07-30 |

- Signed off by: Director of Quality (EPIC-level consolidation, per story-level domain sign-offs above)
- Date: 2026-07-31
- Comments: All 6 stories done and acceptance-verified. 5/6 domain sign-offs are agent-mediated (per §5.3, pending human confirmation); ST-08's live-fire evidence is objective and independently reproducible (GitHub Actions run log linked). No unresolved P0/P1 deviations. EPIC-02 is ready for PR.
