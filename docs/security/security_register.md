**Owner:** Cybersecurity & Trust Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-01
**Cycle:** 2026-06-01__release-v4.8 (ST-05 — BLG-OPS-47)

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
