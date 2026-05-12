**Owner:** Infrastructure & Operations Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-10
**Story:** ST-16 (EPIC-04, v3.3) — BLG-FEAT-13
**Sign-off:** Infrastructure & Operations Owner: Accepted — 2026-05-10 (agent-mediated, v3.3 sprint execution)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Feature Flag System — Platform Specification

This document defines the feature flag mechanism for the swing trading platform.

---

## 1. Purpose

Feature flags allow individual features to be toggled on or off at runtime without a code change or deploy. They are used to:

- Gate new Arc 3/4 features during phased rollout
- Allow production deployment of incomplete features (disabled by default)
- Support staged testing (enabled in staging, disabled in prod)

---

## 2. Flag Schema

Each feature flag has:

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | Identifier (snake_case; e.g. `arc3_lifecycle_display`) |
| `enabled` | boolean | `true` = feature active; `false` = feature hidden/disabled |

Scope is implicit — flags apply globally (no per-user or per-env scope in v1.0).

---

## 3. Configuration Methods

Flags can be configured via either method. If both are present, `feature_flags.json` takes precedence per flag.

### 3.1 Environment Variable

```
FEATURE_FLAGS=flag1:true,flag2:false
```

Comma-separated `name:value` pairs. `value` must be `true` or `false` (case-insensitive).

### 3.2 Config File

Place `feature_flags.json` in the project root:

```json
{
  "arc3_lifecycle_display": true,
  "arc3_grace_period_alerts": false
}
```

The file is read once at the first flag evaluation after startup.

---

## 4. Evaluation

### 4.1 Python utility

```python
from utils.feature_flags import is_flag_enabled

if is_flag_enabled("arc3_lifecycle_display"):
    # feature-specific code
```

`is_flag_enabled(flag_name: str) -> bool` returns `False` for any unknown flag (fail-safe).

### 4.2 Startup logging

At app startup (`on_startup` hook in `backend/main.py`), all configured flags are logged:

```
INFO:     Feature flags: arc3_lifecycle_display=True
INFO:     Feature flags: arc3_grace_period_alerts=False
```

This makes flag state auditable in deployment logs without exposing sensitive data.

---

## 5. Proof-of-Concept Flag

The `arc3_lifecycle_display` flag gates the position lifecycle state badge added in ST-03 (EPIC-01):

- `arc3_lifecycle_display=true` → lifecycle state badge visible in the positions UI
- `arc3_lifecycle_display=false` (default) → badge hidden; positions render as before (no regression)

This demonstrates the pattern: wrap new frontend-visible state in `is_flag_enabled()` on the relevant API response or React component prop.

---

## 6. Usage Pattern

For new Arc 3/4 features:

1. Add the flag name to this document's §7 flag registry.
2. In backend: wrap new response fields or endpoint behaviour with `if is_flag_enabled(...)`.
3. In frontend: read a flag-gated prop from the API response or from a `/flags` endpoint (future — not in v1.0).
4. Default: all new Arc 3/4 flags default to `false` unless explicitly enabled.
5. No regression: existing features must pass all tests when the flag is disabled.

---

## 7. Flag Registry

| Flag Name | Default | Introduced | Controls |
|-----------|---------|------------|---------|
| `arc3_lifecycle_display` | `false` | v3.3 ST-16 | Position lifecycle state badge (EPIC-01 ST-03) |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-10 | Initial creation — ST-16 (EPIC-04, v3.3). Flag schema, env var + JSON config, is_flag_enabled utility, startup logging, arc3_lifecycle_display POC. |
