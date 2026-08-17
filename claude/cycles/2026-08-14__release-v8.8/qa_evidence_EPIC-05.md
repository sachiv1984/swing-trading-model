Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-16

# QA Evidence Log — EPIC-05 (Security Hardening)

**EPIC:** EPIC-05 — Security Hardening
**Cycle:** 2026-08-14__release-v8.8
**Sprint goal:** Close the two live P1 data-integrity gaps (stale screener refresh, stuck RISK OFF badge) and ship the full v8.8 debt-closure slice — 29 stories across 7 EPICs — within the confirmed ~24–28 day capacity band.
**Test scenarios used:** tests/test_gemini_prompt_injection_resistance.py (8 scenarios, 2 updated for the ST-22 hardening); npm run build + tests/e2e/smoke-critical-paths.spec.js + tests/e2e/sidebar-nav-groups.spec.js (11 scenarios, ST-24 react-router upgrade regression check)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-22 | `tests/test_gemini_prompt_injection_resistance.py` | `generate_full_plan()`/`generate_setup_thesis()` now pass trusted instructions (persona, rules, output schema — no per-request interpolation) via Claude's `system` parameter; the untrusted trade-parameters block is the sole `user` message. `_call_claude()` gained a `system` kwarg. Resolves the P3 hardening finding filed as `BLG-SEC-33` by the v8.7 prompt-injection resistance suite (that file's own comment previously mislabeled it `BLG-SEC-32` — corrected in the same commit). | `generate_full_plan()`/`generate_setup_thesis()` pass trusted instructions via `system`, not interleaved with untrusted data; `test_no_system_role_separation_used` updated to assert the new hardened behaviour; no regression to existing test coverage | Pass | None |
| ST-23 | `docs/security/dependency_license_compliance_scan_2026-08-16.md` | First-ever dependency license compliance scan: 86 backend (pip-licenses) + 1,463 frontend (license-checker) packages, direct + transitive. Zero genuinely incompatible licenses found; 3 non-obviously-permissive findings individually assessed and resolved as non-issues. **Correction (Cybersecurity & Trust Lead review, first pass Blocked):** original draft overstated both counts (96/~1,919 claimed vs actual 86/1,463) — the per-license breakdown tables were always accurate; only the summary totals were wrong. Corrected. | Scan run across `backend/requirements.txt` and `package.json`; any incompatible license flagged and resolved; Cybersecurity & Trust Lead sign-off | Pass | None |
| ST-24 | `docs/security/npm_audit_baseline_review_2026-08-16.md` | All 16 baseline HIGH/CRITICAL npm advisory-carrying packages individually assessed. 2 fixed directly (`react-router`/`react-router-dom`, the one genuine runtime-dependency pair among the 16 — verified via build + 11 Playwright regression tests). 14 accept-risk (confirmed build-toolchain-only via import grep; owner, rationale, 2027-02-16 review-by date recorded). Baseline JSON updated to reflect both dispositions. `BLG-TECH-11` filed for the durable fix. | Each of the 16 baseline advisory IDs has either been fixed (removed from baseline) or has a recorded accept-risk decision (owner, rationale, review-by date) | Pass | None |
| ST-25 | `docs/ops/api_key_rotation_policy.md` | Scope table and Rotation Schedule gained a Telegram Bot Token/Chat ID row; new Credential-Specific Notes subsection cross-references `api_key_security_register.md` §7, matching the existing Application X-API-Key precedent. v1.2 → v1.3. | `api_key_rotation_policy.md` Scope table and Rotation Schedule include the Telegram Bot Token; Credential-Specific Notes subsection added, cross-referencing `api_key_security_register.md` §7 | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_gemini_prompt_injection_resistance.py` full suite (8 tests, incl. the 2 updated for hardening) — all pass; full backend suite (`backend/.venv/bin/python3 -m pytest`) 1158 passed / 5 skipped, 0 regressions. `npm run build` succeeds post-react-router upgrade; `tests/e2e/smoke-critical-paths.spec.js` (3 scenarios) + `tests/e2e/sidebar-nav-groups.spec.js` (8 scenarios) — 11/11 pass against the upgraded dependency.
- Regression areas checked: Claude thesis-generation call sites (ST-22), client-side routing/navigation (ST-24's react-router bump), no other production code touched by ST-23/ST-25 (documentation/policy only).
- Known deviations: None found — all 4 stories' deviation checks completed with nothing to file.

**No frontend-visible UI changes in this EPIC** (ST-24's react-router version bump has no observable UI/behavioural change — same major version, verified via the existing Playwright suite rather than new coverage) — the `execution_prompt.md` §3.2.A frontend testing gate does not require new Playwright authorship here; existing coverage sufficed as regression evidence.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no story in this EPIC constructs URLs directly

> **Delegated-QA sign-off pattern (BLG-GOV-69/74) — Format (i), individual sign-off:**

- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-08-17
- Comments: Story-level sign-off provided by Cybersecurity & Trust Lead (ST-23, ST-24), agent-mediated per §5.3 — see below. ST-24 was confirmed clean on the first pass. ST-23's first pass found real, material inaccuracies in the scan's own summary package-scan-scope counts (96/~1,919/~2,015 claimed vs actual 86/1,463/1,549) — corrected and confirmed on retry 1. Reviewed and acknowledged in aggregate — all 4 stories' acceptance criteria met, no unresolved P0/P1 gaps.

### Story-level authority sign-off (BLG-GOV-14 — required in addition to, not instead of, the EPIC-level block above)

**Cybersecurity & Trust Lead** (ST-23, ST-24):
- Signed off by: Sprint Execution Engine (agent-mediated, Cybersecurity & Trust Lead role — §5.3)
- Date: 2026-08-17
- Comments: ST-24 approved clean on the first pass — independently re-verified `npm audit` shows react-router/react-router-dom fully resolved, the remaining 14 accept-risk packages confirmed absent from any `src/` import, `dependency_vuln_baseline.json` correctly updated (16→14, 41→29), and `BLG-TECH-11` correctly filed. ST-23 first pass Blocked — the scan's summary totals (96 backend / ~1,919 frontend / ~2,015 combined) did not match an independent re-scan (86 / 1,463 / 1,549); the per-license breakdown tables were already accurate, only the top-line totals were wrong. Retry 1 Approved: independently re-ran both scans, confirmed 86 and 1,463 are the genuinely correct counts, and confirmed the correction commit (311b0027) touched only the count references with no other content altered.
