**Owner:** Cybersecurity & Trust Lead
**Class:** Security Review (Class 3)
**Status:** Complete
**Review Date:** 2026-07-09
**Reviewed By:** Sprint Execution Engine (ST-03, EPIC-01, v6.8)
**Backlog ref:** BLG-SEC-07

# Security Review — Existing Signal Records: Anomalous Ticker/Market Values

## Scope

ST-03 (BLG-SEC-07, v6.8 EPIC-01): manual review of existing `signals` table records for anomalous `ticker`/`market` values, in the same risk area as BLG-SEC-02 (signal write-path sanitisation — see `docs/specs/security/ai_injection_risk_assessment.md` "Input 5") and BLG-SEC-08 (`update_signal()` column allowlist, this sprint's ST-02). The concern: any signal record written before the ST-03/ST-08-era sanitisation fixes landed could carry a `ticker`/`market` value with unexpected characters, excessive length, or a market code outside `{US, UK}` — any of which could indicate a prior injection attempt or a downstream AI-prompt risk (ticker/market values are interpolated into daily-briefing and chat prompts).

## Method

Queried the live production API (`GET /signals`, no status filter — returns all records regardless of lifecycle status) via the application `X-API-Key` (provisioned this sprint, ST-04/BLG-OPS-99), retrieving all 300 signal records currently in the production `signals` table. Each record's `ticker` and `market` field was checked against:

1. Allowed character set for `ticker`: `[A-Za-z0-9.\-/:]` only (matches the sanitisation allowlist in `database._sanitize_signal_string`, see `tests/test_signal_write_sanitization.py`).
2. Maximum `ticker` length: 12 characters (same sanitisation cap).
3. `market` value must be exactly `US` or `UK`.
4. `market`/`ticker` suffix consistency: `UK` records must end in `.L`; `US` records must not.
5. No empty/null `ticker` or `market`.

## Findings

**Result: PASS — no anomalies found.**

| Check | Result |
|---|---|
| Records reviewed | 300 |
| Disallowed characters in `ticker` | 0 |
| `ticker` length > 12 | 0 |
| `market` outside `{US, UK}` | 0 (299 `US`, 1 `UK`) |
| `market`/`ticker` suffix mismatch | 0 |
| Empty/null `ticker` or `market` | 0 |
| Unique tickers | 11 — `ALB`, `DELL`, `FCIT.L`, `INTC`, `MRNA`, `MU`, `SNDK`, `STX`, `TER`, `WBD`, `WDC` — all recognised, legitimate equity tickers |

All 300 records carry clean, well-formed ticker/market values consistent with legitimate signal generation. No record shows evidence of an injection attempt, encoding anomaly, or malformed market code.

**No follow-up BLG items filed** — the review found no anomalies to action. This satisfies AC-01's "any anomalies filed as follow-up BLG items" as a vacuous condition (zero anomalies → zero follow-up items).

## Note on scope boundary

This review covers the `ticker`/`market` fields only, per AC-01. Other signal fields (e.g. `momentum_percent`, `reason`) were observed in passing but are out of scope for this story — `momentum_percent` values in the dataset reach up to ~999%, which is a data-quality/business-logic question (screener output magnitude), not a security anomaly, and is not actioned here.
