**Owner:** AI Compliance & Governance Officer
**Class:** Canonical Specification (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-04
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# AI Vendor Terms-of-Service & Data-Processing Review

## 1. Purpose

Review the current Terms of Service and Data Processing Addendum (DPA) of every AI vendor **actually integrated** in this codebase against the system's financial-data handling, per ST-12 (EPIC-03, v8.2, BLG-GOV-265).

## 2. Scope Correction (Finding 0 — read this first)

The originating backlog item (BLG-GOV-265) and this sprint's story title name **"Gemini/Claude"** as the two vendors to review. This is based on a stale premise: **Google Gemini is not, and has never been, a live integration in this codebase.**

- `backend/requirements.txt` contains no `google-generativeai` or any Google AI SDK package.
- No `GEMINI_API_KEY` or equivalent environment variable is read anywhere in `backend/`.
- `backend/services/gemini_service.py` — despite its filename — imports and calls only `anthropic.Anthropic` (confirmed at `backend/services/gemini_service.py:90`). The filename is a naming artifact from an earlier design that was never implemented against Google's API, or was fully migrated away from before ship; either way, no Gemini API call exists in the running system today.
- This was already independently discovered and documented in-repo: `backend/database.py:2290-2298` (`get_monthly_claude_cost()` docstring) states outright: *"Claude is the only AI provider integrated in this codebase... no google-generativeai package, no GEMINI_API_KEY, gemini_service.py calls only the Anthropic API."*
- A related finding from a prior cycle (ST-22, EPIC-05 this sprint) independently confirms the frontend AI thesis-generation UI was audited to contain no Gemini references.

**Scope actually reviewed:** Anthropic (Claude API) only — the sole AI vendor with a live integration. This review documents Gemini's non-integration as a **closed, no-action finding** rather than reviewing terms for a vendor with no data flow to assess. If Gemini integration is ever proposed in the future, this review does not cover it and a fresh review (plus a §13 boundary pre-check per `design_gate_prompt.md` STEP 1, ST-16 this same sprint) would be required at that time.

## 3. What Financial Data Reaches Anthropic

Traced via `backend/services/ai_service.py` (`generate_daily_briefing()`, `ai_chat()`, journal-summary/trade-advisor functions) — all three AI-calling code paths send a text prompt built from:

- Open position data: ticker, market, current price, trailing stop price, P&L percentage, alert flags (`ai_service.py:174-197`)
- Portfolio-level aggregates: open position count, cash balance, initial cash (`ai_service.py:168-169`)
- Signal/screener data: ticker, rank (`ai_service.py:207`)
- Red Flag Journal / compliance context text (journal-summary path)
- User-supplied chat questions (`ai_chat()` — free text, validated per `BLG-SEC-01`'s ticker-interpolation sanitisation, `ai_service.py:34-48`)

**Not sent:** no account holder name, email, physical address, government ID, or payment credential. The data sent is portfolio-state financial data (tickers, prices, P&L, cash figures) tied only to the API key's owning account — not independently linkable to a named individual by Anthropic without the caller's own account metadata (which is not sent).

**Classification:** Financial data handling (position/P&L figures), not personal data handling in the GDPR/CCPA "identifiable natural person" sense, per the same distinction `docs/specs/security/trade_plan_data_sensitivity.md` already draws for this codebase's other data classifications.

## 4. Anthropic Commercial API Terms Review (current as of this review date)

Source: Anthropic's published Commercial Terms of Service and DPA (reviewed 2026-08-04). Full sources cited in §6.

| Area | Finding | Assessment |
|------|---------|------------|
| Training on Customer Content | Commercial/API terms contractually prohibit Anthropic from training models on Customer Content by default (distinct from the consumer `claude.ai` chat product, which changed to train-by-default for Free/Pro/Max plans effective 2025-09-28). This system uses the API (`anthropic.Anthropic(api_key=...)`, `backend/services/gemini_service.py:90` and `ai_service.py`), which falls under Commercial Terms, not the consumer chat product. | ✅ No gap — API usage already sits in the non-training tier by contract default. No opt-out action required (there is nothing to opt out of). |
| API log / data retention | API request/response log retention is 7 days (reduced from a prior 30-day retention). | ✅ No gap — consistent with this system's own `claude_audit_log` being the authoritative, permanent cost/audit record (per `ai_service.py`'s existing audit-logging calls); Anthropic-side transient logs are not relied upon as this system's source of truth. |
| Data Processing Addendum (DPA) | An updated DPA effective 2026-01-01 is automatically incorporated into the Commercial Terms of Service — no separate signature/opt-in action required for API customers. | ✅ No gap — DPA coverage is automatic under the account's existing Commercial Terms acceptance. |
| Sub-processor disclosure | Anthropic publishes a sub-processor list as part of its DPA/Trust Center documentation (standard practice for Commercial/Enterprise API terms). | ✅ No gap for this review's purpose — no sub-processor engagement by *this* system beyond the direct Anthropic API call; no re-disclosure obligation triggered for a solo-portfolio tool with no downstream customers of its own. |

## 5. Findings & Remediation

**No remediation items required.** The system's actual AI integration (Anthropic Claude API, Commercial Terms) already sits within a contractually non-training, DPA-covered configuration by default — no user action, opt-out, or contract amendment was needed. The one substantive finding is the **scope correction in §2**: the backlog item's premise (reviewing "Gemini/Claude") named a vendor with no live integration, which this review closes as a non-issue rather than leaving unreviewed.

**Advisory (non-blocking):** If a future story proposes adding a genuine Google Gemini integration, that story must (a) trigger a fresh vendor ToS/DPA review scoped to Gemini specifically — the findings in §4 are Anthropic-specific and do not transfer — and (b) pass the new §13 AI-boundary design-gate pre-check (`design_gate_prompt.md` STEP 1, added this same sprint by ST-16).

## 6. Sources

- Anthropic Commercial Terms of Service and Data Processing Addendum (effective 2026-01-01) — reviewed via web search 2026-08-04.
- [Anthropic — Updates to Consumer Terms and Privacy Policy](https://www.anthropic.com/news/updates-to-our-consumer-terms)
- [Anthropic (Claude) Terms of Service Review 2026 — ToS Watchdog](https://terms.law/ToS-Watchdog/ai-services/anthropic/)
- [Anthropic Claude Data Retention Policy 2026 — Anarlog](https://anarlog.so/blog/anthropic-data-retention-policy/)
- [Anthropic DPA, GDPR & AI Act compliance review — CompanyScope](https://companyscope.io/vendors/anthropic)
- In-repo corroboration: `backend/database.py:2290-2298`, `backend/services/gemini_service.py`, `backend/requirements.txt`

## 7. Sign-off

- **AI Compliance & Governance Officer:** agent-mediated sign-off — 2026-08-04 (ST-12, EPIC-03, v8.2)
