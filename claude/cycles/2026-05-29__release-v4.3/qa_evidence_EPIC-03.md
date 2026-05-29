**Owner:** QA & Testing Owner; Director of Quality
**Class:** QA Evidence Log (Class 3)
**Status:** In Progress
**Last Updated:** 2026-05-29
**Cycle:** 2026-05-29__release-v4.3
**EPIC:** EPIC-03 — Ops & Security Documentation Hardening
**Branch:** exec/2026-05-29__release-v4.3/EPIC-03

---

# QA Evidence Log — EPIC-03

---

## ST-15 — API Key Rotation Policy and External API Key Security Register

**Classification:** autonomous
**Delegation class:** autonomous (Cybersecurity & Trust Lead sign-off)
**Commit SHA:** 7d75b22b

### Acceptance Criteria Evidence

| AC | Criterion | Evidence | Status |
|----|-----------|----------|--------|
| AC-01 | Policy document `docs/ops/api_key_rotation_policy.md` produced | File created at `docs/ops/api_key_rotation_policy.md` v1.1. Covers all 5 credentials in scope. | Pass |
| AC-02 | Covers Alpaca keys (annual rotation) and ANTHROPIC_API_KEY (annual rotation) | §Scope table: Alpaca Key ID + Secret = annual; Anthropic = annual (first rotation due 2026-08-25). §Rotation Schedule: dedicated schedule table. | Pass |
| AC-03 | Rotation procedure documented (how to rotate without service disruption; env var update, staging + prod) | §Rotation Procedure: 8-step procedure with credential-specific notes. Steps 2–5 enforce staging-first rotation before production. | Pass |
| AC-04 | Responsibility assigned: Infra Owner as executor; Cybersecurity & Trust Lead as policy owner | §Responsibility table: Infra Owner = executor; CTL = policy owner + breach escalation. | Pass |
| AC-05 | External API key security register produced in `docs/security/api_key_security_register.md` | File created at `docs/security/api_key_security_register.md` v1.1. 5 credentials registered. | Pass |
| AC-06 | Register covers all 5 external credentials with metadata fields | Entries: Alpaca Key ID (`APCA_API_KEY_ID`), Alpaca Secret (`APCA_API_SECRET_KEY`), ANTHROPIC_API_KEY, News API Key, Supabase DATABASE_URL. All have: env var, purpose, scope, rotation cadence, storage location, last rotation date, next rotation due, notes. | Pass |
| AC-07 | No credential values stored in register | Security alert block included. All value fields contain metadata only (no keys, secrets, or passwords). | Pass |
| AC-08 | Cross-reference between register and rotation policy established | Register §Purpose references rotation policy; rotation policy §Scope references register. | Pass |

**Note:** env var names corrected in both documents during ST-13 audit (v1.0→v1.1): `ALPACA_API_KEY`→`APCA_API_KEY_ID`, `ALPACA_API_SECRET`→`APCA_API_SECRET_KEY`. Backend confirmed to read `APCA_*` names (`backend/services/alpaca_service.py` line 24–25).

### Cybersecurity & Trust Lead Sign-off

- Accepted by: Cybersecurity & Trust Lead (agent-mediated)
- Date: 2026-05-29
- Finding: All 8 ACs met. Policy complete, rotation procedures are staging-first, responsibility clearly assigned, env var names corrected to match backend code.

---

## ST-13 — Staging Environment Parity Audit

**Classification:** delegated_qa
**Delegation class:** delegated_qa (Infrastructure & Operations Owner)
**Parity report:** `docs/ops/staging_parity_report_v4.3.md`

### Acceptance Criteria Evidence

| AC | Criterion | Evidence | Status |
|----|-----------|----------|--------|
| AC-01 | Staging env vars verified against production (ANTHROPIC_API_KEY, Alpaca keys, DB connection, Telegram keys) | Render dashboard inspection 2026-05-29: `APCA_API_KEY_ID` ✅, `APCA_API_SECRET_KEY` ✅, `DATABASE_URL` ✅, `TELEGRAM_BOT_TOKEN` ✅, `TELEGRAM_CHAT_ID` ✅, `API_KEY` ✅. `ANTHROPIC_API_KEY` absent — intentional (prod-only). See parity report §AC-01. | Pass |
| AC-02 | Database schema parity confirmed (`claude_audit_log`/`gemini_audit_log`, `red_flag_events` tables present in staging) | `GET /ai/claude-audit-log` → HTTP 200 ✅; `GET /portfolio/red-flag-journal` → HTTP 200 ✅. Both tables confirmed present in staging DB. See parity report §AC-02. | Pass |
| AC-03 | Sampled health check: v4.0/v4.1/v4.2 new endpoints respond on staging | `GET /analytics/arc5-compliance` → 200 ✅; `GET /signals` → 200 ✅; `GET /portfolio/red-flag-journal` → 200 ✅; `GET /ai/claude-audit-log` → 200 ✅. See parity report §AC-03. | Pass |
| AC-04 | Parity report produced and filed in `docs/ops/` | `docs/ops/staging_parity_report_v4.3.md` v1.0 filed 2026-05-29. | Pass |
| AC-05 | Infrastructure & Operations Owner sign-off recorded | Signed off below. | Pass |

### Infrastructure & Operations Owner Sign-off

- Signed off by: Infrastructure & Operations Owner
- Date: 2026-05-29
- Method: Direct staging verification (Render dashboard env inspection + curl health checks against `https://trading-assistant-staging.onrender.com`)
- Finding: All 3 ACs pass. Staging environment ready for v4.3 sprint verifications. ST-06/07/08 and ST-14 are now unblocked.

---

## ST-14 — claude-audit-log Performance Baseline

**Classification:** delegated_qa
**Delegation class:** delegated_qa (Infrastructure & Operations Owner)
**Commit SHA (autonomous work):** 7d75b22b

### Acceptance Criteria Evidence

| AC | Criterion | Evidence | Status |
|----|-----------|----------|--------|
| AC-01 | `GET /ai/claude-audit-log` added to `api_performance_baseline.md` with at least estimated p50 latency | Autonomous work complete: §16 added to `docs/ops/api_performance_baseline.md` v1.8 (commit 7d75b22b) with estimated p50 230–270ms. **Actual staging timing run required to finalise.** Timing script provided in §16. | Pending — staging run required |
| AC-02 | Reviewed by Infrastructure & Operations Owner | Pending AC-01 completion. | Pending |

**Unblock criteria:** Infrastructure & Operations Owner to run 7-sample curl timing for `GET /ai/claude-audit-log` against staging. Script is in `docs/ops/api_performance_baseline.md §16`.

---

## DoQ Sign-Off

**Director of Quality:** Pending (ST-14 in progress)

Partial sign-off on completion of ST-15 and ST-13:
- ST-15: All 8 ACs passed. CTL approved. Documents correct env var names confirmed by backend code review.
- ST-13: All 5 ACs passed. Infra Owner staging verification complete 2026-05-29.

Full DoQ sign-off to follow after ST-14 completion.

---

## Consolidation

| Story | AC count | Pass | Fail | Pending | Status |
|-------|----------|------|------|---------|--------|
| ST-15 | 8 | 8 | 0 | 0 | Done |
| ST-13 | 5 | 5 | 0 | 0 | Done |
| ST-14 | 2 | 0 | 0 | 2 | Pending staging run |
| **Total** | **15** | **13** | **0** | **2** | **In Progress** |
