**Owner:** Cybersecurity & Trust Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.2
**Last Updated:** 2026-06-08
**Cycle:** 2026-06-08__release-v5.2 (ST-10/ST-11 — BLG-GOV-98/BLG-GOV-99)

---

# Security Register

This document records dependency vulnerability audits and security findings for the Momentum Trading Assistant.

---

## Audit Log

---

### Audit 001 — Dependency Audit post-v4.7

**Date:** 2026-06-01
**Cycle:** 2026-06-01__release-v4.8 (ST-05)
**Conducted by:** Sprint Execution Engine (Head of Engineering / Cybersecurity & Trust Lead delegation)
**Scope:** Python backend dependencies (`backend/requirements.txt`) + frontend npm dependencies (`package.json`)
**Prior audit:** v4.0 cycle (starlette CVE remediation, 2026-05-25)

---

#### Python Backend — pip-audit

**Command:** `pip-audit -r backend/requirements.txt`
**Result:** ✅ **No known vulnerabilities found**

**Dependencies scanned:** fastapi==0.135.1, starlette==1.0.1, uvicorn[standard]==0.24.0, pandas==2.1.3, numpy==1.26.2, requests==2.33.0, python-dateutil==2.8.2, pydantic==2.7.0, psycopg2-binary==2.9.9, sqlalchemy==2.0.23, httpx==0.28.1, anthropic==0.40.0, pytest==9.0.3, pytest-cov==7.0.0, reportlab==4.2.5, yfinance==1.3.0

**Disposition:** Clean — no action required.

---

#### Frontend — npm audit

**Command:** `npm audit`
**Result:** ⚠️ **45 vulnerabilities found (0 critical, 21 high, 15 moderate, 9 low)**

**Finding summary:**

| Severity | Count | Root cause | Production impact |
|----------|-------|------------|------------------|
| Critical | 0 | — | None |
| High | 21 | react-scripts build toolchain (CRA) | ❌ Build tools only — not in deployed bundle |
| Moderate | 15 | Transitive via build toolchain | Build tools only |
| Low | 9 | Transitive via build toolchain | Build tools only |

**Key HIGH packages:**

| Package | Vulnerability | CVE/Advisory | Production runtime? |
|---------|--------------|-------------|---------------------|
| `react-scripts` (direct dep) | Multiple HIGH via build toolchain | Various | ❌ Dev/build only |
| `@babel/plugin-transform-modules-systemjs` | Arbitrary code generation on malicious input | GHSA-fv7c-fp4j-7gwp | ❌ Build tool only |
| `nth-check` | ReDoS vulnerability | GHSA-rp65-9cf3-cjxr | ❌ Build tool only |
| `lodash` | Prototype pollution | Various | ❌ Transitive build dep |
| `node-forge` | HMAC validation bypass | Various | ❌ Build tool only |

**Production impact assessment:** All 21 HIGH findings are transitive dependencies of `react-scripts` (Create React App build toolchain). The production deployment serves the compiled React bundle and does not include `node_modules/`. Therefore, **these vulnerabilities do not affect the deployed application runtime**.

**Disposition:**
- All HIGH findings filed as BLG-OPS-49 (P1 — devDependency CVEs; react-scripts chain; `npm audit fix` to be applied in a dedicated toolchain upgrade sprint)
- No HIGH/CRITICAL findings in production runtime dependencies
- `npm audit fix` available — deferred to avoid breaking changes mid-sprint

---

#### Anthropic SDK Version Check

**Current version in requirements.txt:** `anthropic==0.40.0`
**Latest available version:** `anthropic==0.105.2` (as of 2026-06-01)
**Gap:** 65 minor versions behind

**Disposition:** A patch upgrade is available. Due to the significant version gap (0.40.0 → 0.105.2), a tested upgrade is required rather than a direct pin bump. Filed as BLG-OPS-50 (P2 — SDK version upgrade; requires integration testing before applying).

---

#### Summary

| Check | Result | Action |
|-------|--------|--------|
| pip-audit (Python backend) | ✅ Clean — no vulnerabilities | None |
| npm audit (frontend) | ⚠️ 45 vulns (0 critical, 21 high — all devDep) | BLG-OPS-49 filed (P1) |
| Anthropic SDK upgrade | ⚠️ 65 versions behind (0.40.0 → 0.105.2) | BLG-OPS-50 filed (P2) |

---

**Cybersecurity & Trust Lead sign-off:** Sprint Execution Engine (autonomous class), 2026-06-01

---

### Remediation 001 — npm HIGH CVE Remediation (v4.9 ST-01)

**Date:** 2026-06-02
**Cycle:** 2026-06-02__release-v4.9 (ST-01 — BLG-OPS-49)
**Conducted by:** Sprint Execution Engine (Head of Engineering / Cybersecurity & Trust Lead)
**Action:** npm devDependency HIGH CVE remediation

---

#### Remediation Steps

1. **Initial state:** 45 vulnerabilities (21 HIGH, 15 moderate, 9 low) — all in react-scripts 5.x devDependency chain
2. **Step 1 — `npm audit fix`:** Applied automatic fixes; reduced to 28 vulnerabilities (13 HIGH, 6 moderate, 9 low)
3. **Step 2 — npm `overrides`:** Added `overrides` block in `package.json` to force-patch three remaining HIGH transitive deps blocked by react-scripts CRA architecture

---

#### npm Overrides Applied

| Package | Vulnerable range | Fixed version | CVE/Advisory |
|---------|-----------------|---------------|--------------|
| `nth-check` | <2.0.1 | >=2.0.1 (3.0.1) | GHSA-rp65-9cf3-cjxr — Inefficient RegExp Complexity |
| `serialize-javascript` | <=7.0.4 | >=7.0.5 (7.0.5) | GHSA-5c6j-r48x-rmvq — RCE via RegExp/Date; GHSA-qj8w-gfj5-8c6v — CPU DoS |
| `underscore` | <=1.13.7 | >=1.13.8 (1.13.8) | GHSA-qpx9-hpmf-5gmw — Unlimited recursion DoS |

---

#### Result

**Final state after remediation:** 15 vulnerabilities (0 HIGH, 6 moderate, 9 low)

| Check | Before | After |
|-------|--------|-------|
| HIGH vulnerabilities | 21 | **0** |
| Moderate vulnerabilities | 15 | 6 |
| Low vulnerabilities | 9 | 9 |
| Production runtime impact | None | None |

`npm audit --audit-level=high` exits 0. Build verified with `npm run build` — no regressions.

**Remaining 6 moderate, 9 low:** All transitive to react-scripts CRA chain; no production runtime impact; deferred per standard CRA maintenance policy.

---

**Cybersecurity & Trust Lead sign-off:** Sprint Execution Engine (autonomous class), 2026-06-02

---

### Upgrade 001 — Anthropic SDK Upgrade 0.40.0 → 0.105.2 (v4.9 ST-02)

**Date:** 2026-06-02
**Cycle:** 2026-06-02__release-v4.9 (ST-02 — BLG-OPS-50)
**Conducted by:** Sprint Execution Engine (Head of Engineering)
**Action:** Anthropic Python SDK version upgrade

---

#### Upgrade Details

| Field | Value |
|-------|-------|
| Previous version | anthropic==0.40.0 |
| New version | anthropic==0.105.2 |
| Gap | 65 minor versions |
| File updated | `backend/requirements.txt` |

---

#### Breaking Change Review (0.40.0 → 0.105.2)

The codebase uses the following SDK API surface:
- `anthropic.Anthropic(api_key=...)` — client creation
- `client.messages.create(model=..., max_tokens=..., messages=[...])` — Messages API
- `response.content[0].text` — response access
- `response.usage.input_tokens` / `response.usage.output_tokens` — usage tracking

**Breaking changes reviewed:**
- v0.47+: TypedBeta parameters — not used in this codebase
- v0.50+: Sync/async streaming refactor — not used (no streaming calls)
- v0.60+: Batch API additions — not used
- v0.80+: Computer use / extended thinking — not used
- v0.95+: Files API — not used
- v0.100+: Managed agents API — not used
- Messages.create() signature, response.content[0].text, response.usage attributes: **stable throughout 0.40.0 → 0.105.2**

**Conclusion:** No breaking changes affecting this codebase.

---

#### Test Verification

`python3 -m pytest tests/` result post-upgrade: 447 passed (13 pre-existing failures, all confirmed present on main before upgrade — none caused by SDK upgrade). Core suite (excluding known pre-existing failures) fully passes.

---

**Head of Engineering sign-off:** Sprint Execution Engine (autonomous class), 2026-06-02

---

### Review 002 — Telegram Bot Token Minimal-Permission Review (v5.2 ST-10)

**Date:** 2026-06-08
**Cycle:** 2026-06-08__release-v5.2 (ST-10 — BLG-GOV-98)
**Conducted by:** Sprint Execution Engine (Cybersecurity & Trust Lead delegation)
**Scope:** SI-05 Telegram bot token permission scope — verify send-only to designated digest chat

---

#### Review Findings

**Token location in code:** `TELEGRAM_BOT_TOKEN` environment variable (set in Render deployment environment)
**Chat scope:** `TELEGRAM_CHAT_ID` environment variable — fixed single chat ID per deployment

**Code-level verification:**

| Permission aspect | Observed | Evidence |
|---|---|---|
| API method used | `sendMessage` only | `backend/services/si05_digest_service.py:268` — `sendMessage` endpoint called |
| Read capability (getUpdates, getMessage) | ❌ Not used | No read API calls in codebase |
| Cross-chat send capability | ❌ Not used | Only sends to `TELEGRAM_CHAT_ID` — no dynamic chat_id logic |
| Bot admin operations | ❌ Not used | No admin API calls |

**BotFather configuration verification:** Cannot be verified programmatically from code alone. BotFather permission settings are configured in the Telegram platform and are not queryable via code inspection. Manual verification via BotFather is recommended to confirm:
- Bot is not added to unintended group chats
- Bot does not have admin privileges in any chat

**Finding:**

| Check | Status | Notes |
|---|---|---|
| Code-level send-only usage | ✅ PASS | sendMessage API only; no read calls |
| Single fixed chat target | ✅ PASS | TELEGRAM_CHAT_ID env var is fixed per deployment |
| BotFather permission settings | ⚠️ UNVERIFIED | Cannot verify from code; manual BotFather check recommended |

**Overall finding:** PASS with recommendation — code confirms send-only usage to a fixed chat. BotFather settings should be manually verified by Infrastructure & Operations Owner to confirm no unintended chat memberships or admin privileges.

---

**Cybersecurity & Trust Lead sign-off:** Sprint Execution Engine (autonomous class), 2026-06-08

---

### Review 003 — SI-05 Digest Endpoint Authentication Review (v5.2 ST-11)

**Date:** 2026-06-08
**Cycle:** 2026-06-08__release-v5.2 (ST-11 — BLG-GOV-99)
**Conducted by:** Sprint Execution Engine (Cybersecurity & Trust Lead delegation)
**Scope:** POST /digest/si05/send authentication status

---

#### Review Findings

**Endpoint:** `POST /digest/si05/send`
**Router file:** `backend/routers/digest.py:227`

**Authentication status check:**

```python
# backend/routers/digest.py lines 227-228
@router.post("/si05/send")
def send_si05_digest_endpoint():
```

The endpoint uses a bare `@router.post` decorator with no authentication dependency injected. The router import block (`from fastapi import APIRouter`) does not include `Depends` or any HTTPBearer/APIKey security scheme.

**Finding: AUTHENTICATION GAP FOUND**

| Check | Result |
|---|---|
| API key authentication enforced | ❌ ABSENT — endpoint callable without authentication |
| Authentication pattern per BLG-SEC-01/v2.2 | ❌ NOT APPLIED — other endpoints use API key auth; this endpoint does not |
| Risk | Unauthenticated caller can trigger Telegram API calls and digest sends |

**Impact assessment:**
- An unauthenticated caller can POST to `/digest/si05/send` and trigger a Telegram message to the designated digest chat
- Risk: abuse of Telegram quota, spam to digest chat, incurring Anthropic API cost (if any AI path is triggered)
- The endpoint is currently intended for internal cron/scheduled invocation only; no documented auth requirement means it is an unintended open endpoint

**Disposition:** Fix is out of scope for EPIC-03 (review phase only). P2 backlog item filed: **BLG-BE-35** — Add API key authentication to POST /digest/si05/send.

---

**Cybersecurity & Trust Lead sign-off:** Sprint Execution Engine (autonomous class), 2026-06-08
