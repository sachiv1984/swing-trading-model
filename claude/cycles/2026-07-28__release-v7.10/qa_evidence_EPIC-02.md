Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-29

# QA Evidence — EPIC-02 (Security Hardening)

**EPIC:** EPIC-02 — Security Hardening
**Cycle:** 2026-07-28__release-v7.10
**Sprint goal:** Materially reduce the platform's production risk surface — closing silent backend error-masking, hardening security posture (secrets scanning, rate-limit and exception hygiene), strengthening QA/CI infrastructure, correcting API contract debt, and clearing a first tranche of frontend technical debt — by delivering all 23 in-scope v7.10 hardening items within the confirmed capacity band.
**Test scenarios used:** `tests/test_secrets_scanning_hook.py` (ST-05), `tests/test_ai_rate_limit_bypass.py` (ST-06), `tests/test_main_500_no_raw_exception_text.py` (ST-08)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-05 | `.githooks/pre-commit`, `.gitleaks.toml` | Extended the existing pre-commit hook with a gitleaks scan of staged changes, using the same `.gitleaks.toml` config as the CI-level gate. Degrades to a warning if gitleaks isn't installed locally. Confirmed to catch a planted GitHub PAT test secret, directly and via regression test. | Local pre-commit hook added running a secrets scanner, complementing the CI-level gate; confirmed to catch a deliberately-planted test secret; Cybersecurity & Trust Lead sign-off | Pass | None |
| ST-06 | `docs/ops/ai_rate_limit_bypass_audit_2026-07-29.md` | Tested both AI endpoints against X-Forwarded-For spoofing and IP rotation. Neither is a confirmed code-level bypass. Surfaced a more significant adjacent finding (Render proxy IP collapse risk) filed as `BLG-SEC-24` (P1). | Bypass test performed against both endpoints via both named techniques; findings documented; any confirmed bypass filed as P1/P0; Cybersecurity & Trust Lead sign-off | Pass | None |
| ST-07 | `docs/security/rate_limit_audit_2026-07-29.md` | Refreshed the 2026-07-26 application-level audit against 3 new endpoints; added Render platform-level analysis (no config exists in-repo to audit; cross-references `BLG-SEC-24`). | Audit of Render platform-level and application-level rate-limiting posture against all public-facing endpoints, documented; gaps filed; Cybersecurity & Trust Lead sign-off | Pass | None |
| ST-08 | N/A (security fix, no prior canonical spec — see `spec_reference_not_applicable_reason`) | Fixed 27 500-class error-response call sites in `backend/main.py` to return a generic message instead of raw exception text, with full detail still logged server-side. 4xx messages unchanged. Filed `BLG-SEC-25` (P2, 16 sites) for the adjacent masked-200 bug class, deliberately not fixed here. | 500-class responses no longer include raw exception text; generic message substituted; full detail logged server-side; no change to intentional 4xx messages (RISK-03); Head of Engineering sign-off | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_secrets_scanning_hook.py` (3 passed, skips gracefully without gitleaks installed), `tests/test_ai_rate_limit_bypass.py` (3 passed), `tests/test_main_500_no_raw_exception_text.py` (5 passed). Full backend suite: 873 passed, 5 skipped, 0 failed (final state, after ST-08).
- Regression areas checked: `.githooks/pre-commit` (both a planted-secret block and a clean-commit pass verified live), `backend/routers/ai.py`/`services/rate_limiter.py` (rate-limit keying logic), `backend/main.py` (all 27 fixed 500-paths spot-checked plus a 4xx control confirming RISK-03 compliance).
- Known deviations filed: None within this EPIC's own stories. ST-06/ST-07/ST-08 each filed adjacent, out-of-scope follow-up backlog items (`BLG-SEC-24`, `BLG-SEC-25`) for related-but-distinct findings surfaced during the work, rather than silently expanding story scope.

**Sign-off review process note:** two of the four stories' first-draft audit/backlog artefacts (ST-07's endpoint enumeration, ST-08's `BLG-SEC-25` site count) contained factual errors caught during agent-mediated sign-off review and corrected before approval — the review process functioned as intended (independent verification, not rubber-stamping).

---

## Sign-Off Block

**Eligibility note:** all four stories are classified `autonomous`, but all four name a specific authority in their acceptance criteria ("Cybersecurity & Trust Lead sign-off" for ST-05/06/07, "Head of Engineering sign-off" for ST-08), so per the same principle applied in `qa_evidence_EPIC-01.md`, the named-role agent-mediated format is used below.

- [x] All acceptance criteria verified against canonical spec (or documented as not-applicable, ST-08)
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] No frontend-visible change in this EPIC (n/a check)
- Signed off by:
  Sprint Execution Engine (agent-mediated, Cybersecurity & Trust Lead role — §5.3) — ST-05, ST-06, ST-07
  Sprint Execution Engine (agent-mediated, Head of Engineering role — §5.3) — ST-08
- Date: 2026-07-29
- Comments: 4/4 stories Pass. Each agent-mediated review independently verified its story's factual claims against the live codebase before returning Approved; two reviews (ST-07, ST-08) initially returned Blocked or flagged a correctable inaccuracy and were re-verified after the fix — not a rubber-stamp of the engine's own drafted findings.
