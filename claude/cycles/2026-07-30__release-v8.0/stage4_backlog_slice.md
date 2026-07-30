Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-30
Cycle: 2026-07-30__release-v8.0
Release: v8.0

# Backlog Slice — v8.0

<!-- release-plan-marker: RP:v8.0:2026-07-30__release-v8.0 -->

19 stories across 6 grouped EPICs. Full acceptance criteria below (source of truth for Sprint Planning and Execution).

---

## EPIC-01 — Data Model & Spec Integrity

**Maps to:** S2-01, S2-02, S2-03
**Owner:** Data Model & Domain Schema Owner; Financial Reporting & Records Owner

### ST-01 — `strategy_version_at_entry` field on trade/trade_plan
**Source:** BLG-SPEC-78
**Effort:** M
**Acceptance Criteria:**
- Migration added
- Field populated on new trade plans at entry (forward-only, no backfill)
- `data_model.md` updated

### ST-02 — FX handling review post-DS-05 US market source change
**Source:** BLG-SPEC-79
**Effort:** S
**Acceptance Criteria:**
- Review documented confirming no silent position-sizing miscalculation for GBP-denominated accounts trading US tickers under the current data pipeline
- `strategy_rules.md` §4.1.5 confirmed accurate, or an amendment filed

### ST-03 — FX conversion audit trail completeness check (§4.1.5 effective-rate logging)
**Source:** BLG-SPEC-107
**Effort:** S
**Acceptance Criteria:**
- Audit of all FX conversion code paths against the `data_model.md` §4.1.5 logging requirement complete
- Any gap found is fixed
- Financial Reporting & Records Owner sign-off

---

## EPIC-02 — Security Hardening

**Maps to:** S2-04, S2-05, S2-06, S2-07, S2-08, S2-09
**Owner:** Cybersecurity & Trust Lead; Head of Engineering; Head of UX & Design

**Staging-only ACs:** ST-06 and ST-07 carry observable UI interaction ACs — see RISK-01; Design Gate PASS or Playwright coverage/staging sign-off required before these ACs may be considered met (per CLAUDE.md §2).

### ST-04 — Raw exception text leaked in 16 implicit-HTTP-200 error paths in backend/main.py
**Source:** BLG-SEC-25
**Effort:** S
**Acceptance Criteria:**
- All 16 call sites return HTTP 500 (not implicit 200) with the canonical `{status, message}` envelope and a generic client-facing message
- Full exception detail logged server-side on every one of the 16 (adding `traceback.print_exc()` wherever currently missing)
- Existing 200-path success shapes unchanged
- Regression test added
- Head of Engineering sign-off

### ST-05 — Mandatory security review checklist for new AI-calling endpoints
**Source:** BLG-SEC-23
**Effort:** S
**Acceptance Criteria:**
- Short mandatory security review checklist for AI-calling endpoints documented (rate limiting, cost gating, prompt-injection awareness)
- Referenced from the design gate process
- Cybersecurity & Trust Lead sign-off

### ST-06 — Trade Plan pre-entry checklist items unreachable by keyboard
**Source:** BLG-FE-135
**Effort:** S
**Acceptance Criteria:**
- `EntryChecklist.js`'s `CheckItem` converted to a real `<button role="checkbox" aria-checked={item.checked}>` (or equivalent `tabIndex`/`role`/`aria-checked`/`onKeyDown` handling)
- Checklist item is reachable via Tab and toggleable via Space/Enter; `aria-checked` reflects state
- **Staging-only AC:** interaction/timing — Playwright coverage or recorded staging sign-off required
- Head of UX & Design sign-off

### ST-07 — Trade Plan "Abandon" modal has no focus trap or restoration
**Source:** BLG-FE-136
**Effort:** S
**Acceptance Criteria:**
- Hand-rolled Abandon Plan modal overlay replaced with the existing Radix-based `src/components/ui/dialog.js` `Dialog` primitive (or equivalent focus-management logic added)
- Tab cannot move focus outside the modal while open; Escape closes it; focus returns to the triggering button on close
- **Staging-only AC:** interaction/timing — Playwright coverage or recorded staging sign-off required
- Head of UX & Design sign-off

### ST-08 — Verify request.client.host reflects true client IP behind Render's proxy; configure trusted-proxy headers if not
**Source:** BLG-SEC-24
**Effort:** S
**Acceptance Criteria:**
- Live verification documented (whether `request.client.host` reflects the real client IP or Render's proxy IP)
- If proxy-IP collapse confirmed: uvicorn configured to trust the correct forwarded-IP header from Render's known edge, scoped narrowly (not a blanket wildcard) — see RISK-02
- Re-verified live that distinct real clients get independent rate-limit buckets
- Cybersecurity & Trust Lead sign-off

### ST-09 — `.gitleaks.toml`'s global `[[allowlists]]` blocks use an invalid schema
**Source:** BLG-SEC-26
**Effort:** S
**Acceptance Criteria:**
- All 4 allowlist blocks rewritten using the schema-valid `[[rules]] / [[rules.allowlists]]` nested form, with `condition = "AND"` and `regexTarget = "match"` set explicitly — see RISK-03
- Each rewritten block's suppression verified by an actual local `gitleaks detect` run against its target file
- CI `secret-scanning.yml` still passes on a clean branch
- Cybersecurity & Trust Lead sign-off

---

## EPIC-03 — QA & Test Infrastructure Hardening

**Maps to:** S2-10, S2-11, S2-12
**Owner:** Director of Quality; QA Lead; QA & Testing Owner

### ST-10 — Retroactive Playwright §18 anti-pattern sweep (route.fallback() ordering + networkidle usage) (consolidated)
**Source:** BLG-QA-97
**Effort:** S
**Acceptance Criteria:**
- One-time grep-and-fix sweep complete for both patterns: (a) generic catch-all `route.continue()` handlers registered ahead of a more specific handler, and (b) any remaining `waitForLoadState('networkidle')` usage
- Any found instances fixed (replaced with element-specific waits where applicable)
- Zero remaining instances of either confirmed via grep in CI or a one-time report

### ST-11 — Test-tagging convention (smoke/regression/critical) for selective CI runs
**Source:** BLG-QA-120
**Effort:** M
**Acceptance Criteria:**
- Tagging convention (smoke/regression/critical) documented
- Applied to at least the smoke-tier subset of the existing Playwright suite
- Selective-run capability wired into CI where useful

### ST-12 — Synthetic trade-history data generator for gated-feature testing
**Source:** BLG-QA-121
**Effort:** M
**Acceptance Criteria:**
- Generator produces realistic (non-production) data satisfying at least the SI-02 and Setup Quality Score gate thresholds
- Clearly scoped/labelled as test-only, never usable against production

---

## EPIC-04 — Operations & Reliability

**Maps to:** S2-13, S2-14, S2-15, S2-16, S2-17
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect

### ST-13 — Render service health-check alerting to Telegram on 5xx spike
**Source:** BLG-OPS-114
**Effort:** M
**Acceptance Criteria:**
- Lightweight health-check poll (or Render webhook, if available on current plan tier) posts a Telegram alert on a sustained 5xx spike
- Alert confirmed to fire on a simulated 5xx spike (staging) or a documented dry-run test
- Depends on ST-14's GitHub Actions secrets being configured for full end-to-end confirmation

### ST-14 — Configure TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID as GitHub Actions repo secrets for nightly backtest job alerting
**Source:** BLG-OPS-115
**Effort:** XS
**Acceptance Criteria:**
- `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` present in repo Settings → Secrets and variables → Actions (same values as existing Render env vars)
- A manual `workflow_dispatch` re-run against a deliberately-broken endpoint confirms a Telegram message is actually received (not just the `::warning::` fallback)

### ST-15 — Confirm Render rollback runbook has real execution history
**Source:** BLG-OPS-109
**Effort:** S
**Acceptance Criteria:**
- Either historical execution evidence of a real prior rollback is found and documented, or a deliberate rollback drill is run against a non-production/staging deploy
- Outcome documented either way

### ST-16 — Render dashboard-only build/deploy path filter audit (invisible to repo grep)
**Source:** BLG-OPS-124
**Effort:** S
**Acceptance Criteria:**
- Full current Render dashboard build/deploy path-filter configuration audited against the set of files the running app actually reads at runtime
- Any other file outside the watched paths documented
- Configuration documented in-repo (source of truth remains the dashboard) so future searches can find it
- FinOps & Resource Architect sign-off

### ST-17 — Backup & disaster recovery runbook for production database
**Source:** BLG-OPS-126
**Effort:** S
**Acceptance Criteria:**
- Backup frequency/retention (as currently configured on the hosting provider) documented
- Step-by-step recovery runbook documented and confirmed against actual hosting provider capability
- Infrastructure & Operations Owner sign-off

---

## EPIC-05 — Frontend Technical Debt

**Maps to:** S2-18
**Owner:** Base44 Frontend Prompt Owner

### ST-18 — Reusable Base44 prompt fragment library for common layouts
**Source:** BLG-FE-124
**Effort:** M
**Acceptance Criteria:**
- Most-repeated card/empty-state/loading-skeleton layout prompt fragments extracted into `base44_prompt_template_library.md`
- Library extended with at least 3 new reusable fragments
- Referenced by at least one new story going forward

---

## EPIC-06 — Governance & Engineering Process Hardening

**Maps to:** S2-19
**Owner:** Head of Engineering

### ST-19 — Structural fix for recurring cross-EPIC `execution_state.json` merge-conflict pattern
**Source:** BLG-GOV-263
**Effort:** L (~3-5 days)
**Acceptance Criteria:**
- Structural fix designed and implemented that removes the recurring merge-conflict surface itself (e.g. per-EPIC append-only manifest files aggregated at build/CI time instead of every branch writing to the same shared state file independently) — see RISK-04
- Next multi-EPIC sprint shows a measured reduction in per-branch `execution_state.json` conflicts
- Head of Engineering sign-off
- `shared_standards.md` §12 updated to reference the new mechanism

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24-28 working-day-equivalent units |
| Total estimated effort (in-scope) | ~26.25 days midpoint |
| Utilisation | ~94-109% |
| Over-allocation | No — within the confirmed ceiling |

```yaml
artifacts.stage4_backlog_slice: pass
artifacts.stage4_issue_manifest: pass
attributes.backlog_committed: true
attributes.design_gate_required: true
status: Committed
```
