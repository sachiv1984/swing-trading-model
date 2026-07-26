**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-26
**Cycle:** 2026-07-24__release-v7.8 (ST-07 — BLG-SEC-20)

---

# API Key Rotation-and-Audit Schedule

## Purpose

This document consolidates a **rotation-and-audit schedule** — with a concrete first-rotation date per key — for the 5 external key types named in this cycle's scope (ST-07, EPIC-07): Yahoo Finance, Alpaca, Gemini, Claude, Telegram. It builds on the existing rotation pattern established in `docs/ops/alpaca_key_rotation_policy.md` (step-by-step procedure, trigger conditions) and `docs/ops/api_key_rotation_policy.md` (general procedure, all-credential scope table), and adds the **audit** half that neither prior document covers: a recurring, non-emergency review confirming each credential is still required, still minimally scoped, still stored correctly, and — for the two key types with no actual credential — still absent.

This document does not replace `docs/ops/alpaca_key_rotation_policy.md` or `docs/ops/api_key_rotation_policy.md` (the step-by-step rotation procedures remain there, unchanged) or `docs/security/api_key_security_register.md` (the authoritative per-credential metadata record). It adds the audit cadence and gives all 5 named key types — including the 2 with no credential — a single place to be enumerated together with a concrete schedule.

---

## Rotation-and-Audit Schedule (5 Key Types)

| # | Key Type | Credential Exists? | Rotation Cadence | First Rotation Due | Audit Cadence | First Audit Due |
|---|----------|--------------------|--------------------|--------------------|--------------|-------|
| 1 | Alpaca (`APCA_API_KEY_ID` + `APCA_API_SECRET_KEY`) | Yes | Annual (12 months) — per `alpaca_key_rotation_policy.md` | 2027-07-26 (anchored today; prior rotation date was unknown/pre-register — see Note A) | Quarterly (90 days) | 2026-10-24 |
| 2 | Claude / Anthropic (`ANTHROPIC_API_KEY`) | Yes | Annual (12 months) — per `api_key_rotation_policy.md §Anthropic API Key` | 2026-08-25 (existing register date, unchanged) | Quarterly (90 days) | 2026-10-24 |
| 3 | Telegram (`TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`) | Yes | Annual (12 months) — per `api_key_security_register.md` entry #7 | 2027-07-26 (anchored today; prior rotation date was unknown/pre-register — see Note A) | Quarterly (90 days) | 2026-10-24 |
| 4 | Yahoo Finance | **No** — see Note B | Not applicable (no credential to rotate) | Not applicable | Quarterly (90 days) — confirms Note B still holds | 2026-10-24 |
| 5 | Gemini | **No** — see Note C | Not applicable (no credential to rotate) | Not applicable | Quarterly (90 days) — confirms Note C still holds | 2026-10-24 |

**Note A (Alpaca, Telegram — anchor date):** Both `docs/security/api_key_security_register.md` entries record `Last rotation date: Unknown (pre-register baseline)`, so "12 months from last rotation" has no concrete anchor. This schedule fixes that gap by anchoring both to today's date (2026-07-26) as the effective baseline, giving a first concrete due date of 2027-07-26. This is a scheduling anchor only — it does not itself constitute a rotation and does not change the "Last rotation date" field in the register (still accurately "Unknown"); the register's `Last rotation date` field updates only when an actual rotation is performed.

**Note B (Yahoo Finance — no credential):** Yahoo Finance data fetching (`utils/pricing.py`, `services/screener_data_service.py`, `services/screener_batch_service.py`) uses unauthenticated public chart-API endpoints (`query1.finance.yahoo.com`) with only a browser `User-Agent` header — no API key, token, or credential of any kind is sent. There is nothing to rotate. The quarterly audit for this entry confirms this remains true (no credential has since been introduced, e.g. via a paid Yahoo Finance tier) and that the unauthenticated endpoint continues to function within the existing crumb/cooldown handling (`screener_data_service.py` `_YAHOO_COOLDOWN_SECS`).

**Note C (Gemini — no credential):** "Gemini" has no separate credentialed integration in this codebase. Per the finding already recorded in `database.py` (`get_monthly_claude_cost()` docstring, ST-07/EPIC-07/v7.6, `ESC-EXEC-20260720-01`): Claude (Anthropic) is the only AI provider integrated; there is no `google-generativeai` package and no `GEMINI_API_KEY` anywhere in this codebase. `backend/services/gemini_service.py` is a legacy filename retained for backward compatibility that calls only the Anthropic API (`ANTHROPIC_API_KEY`, entry #2 above). There is nothing to rotate under a distinct "Gemini" credential. The quarterly audit for this entry confirms this remains true (no separate Gemini/Google credential has since been introduced).

---

## Audit Procedure (New — Applies to All 5 Entries)

Distinct from rotation (which replaces a credential value), the audit is a lightweight quarterly review that does **not** require generating a new credential:

1. **Confirm still in use:** for entries 1–3, confirm the credential is still actively called by the codebase (grep the relevant env var name across `backend/`). For entries 4–5, confirm no new credential has been introduced for that provider (grep for a newly-added env var, e.g. `YAHOO_API_KEY` or `GEMINI_API_KEY`).
2. **Confirm scope still minimal:** re-check the "Scope" field in `docs/security/api_key_security_register.md` for entries 1–3 against actual usage — flag if a credential now has broader access than the codebase requires.
3. **Confirm storage location still compliant:** verify the credential is only in Render environment variables (staging + production), never committed to the repository (per the Storage Rules section in `api_key_rotation_policy.md`).
4. **Record the audit:** append a row to the Audit Log table below — no register update is needed unless the audit surfaces a finding requiring rotation or a scope correction, in which case follow the relevant rotation procedure and file a backlog item for any scope correction.

### Audit Log

| Date | Key Type | Finding | Action Taken |
|------|----------|---------|--------------|
| _(none yet — first audit due 2026-10-24)_ | | | |

---

## Cross-References

- Rotation procedures: `docs/ops/alpaca_key_rotation_policy.md` (Alpaca step-by-step), `docs/ops/api_key_rotation_policy.md` (general procedure, all credentials)
- Credential metadata: `docs/security/api_key_security_register.md`
- Rotation date cross-check: `docs/ops/external_api_credential_inventory.md`

---

## Acceptance

- Accepted by: Cybersecurity & Trust Lead
- Date: 2026-07-26
