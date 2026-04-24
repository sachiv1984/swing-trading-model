**Owner:** QA & Testing Owner
**Class:** Class 3 Operational Record
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-04-24
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Canonical specs:** docs/specs/api_contracts/ai_endpoints.md v1.0; docs/specs/data_model.md (trade_history table)

---

# AI Journal Summary — Test Scenario Coverage

**Purpose:** Defines test scenarios for the AI journal summary feature (`POST /api/ai/journal-summary` and frontend AI summary section). Covers happy path, failure handling, and frontend behaviour requirements.

---

## Scenario Registry

| ID | Name | Type | Component | Expected Outcome |
|----|------|------|-----------|-----------------|
| AI-S-01 | Happy path — valid trade IDs | Backend | `POST /api/ai/journal-summary` | 200 with non-null summary |
| AI-S-02 | Graceful LLM failure | Backend | `POST /api/ai/journal-summary` | 200 with `summary: null`, informational message |
| AI-S-03 | Frontend collapse on load | Frontend | AI summary section | Section collapsed by default; no LLM call made on page load |
| AI-S-04 | Disclaimer visible when expanded | Frontend | AI summary section | Disclaimer text always visible in all expanded states |

---

## Scenario Definitions

### AI-S-01 — Happy Path: Valid Trade IDs

**Canonical spec:** `docs/specs/api_contracts/ai_endpoints.md §POST /ai/journal-summary`

**Preconditions:**
- At least 2 closed trades exist in `trade_history` with non-empty `entry_note` or `exit_note`
- `ANTHROPIC_API_KEY` environment variable is set and valid

**Request:**
```json
POST /api/ai/journal-summary
{
  "trade_ids": [<id1>, <id2>]
}
```

**Expected response (HTTP 200):**
```json
{
  "summary": "<non-empty string — LLM-generated text>",
  "trade_count": 2,
  "model": "<model identifier string>",
  "cached": false,
  "message": null
}
```

**Verification:**
- `summary` is a non-null, non-empty string
- `trade_count` equals number of trades with matching IDs that have an `exit_date`
- `model` matches the configured model (default `claude-haiku-4-5-20251001` or `AI_MODEL` env var)
- `cached` is `false` (caching not implemented)
- One audit record created in `ai_audit_log`: `summary_produced = true`, `output_hash` non-null

---

### AI-S-02 — Graceful LLM Failure

**Canonical spec:** `docs/specs/api_contracts/ai_endpoints.md §POST /ai/journal-summary — LLM unavailability`

**Preconditions:**
- `ANTHROPIC_API_KEY` is unset or invalid (simulate LLM unavailability)
- At least 1 closed trade with journal notes exists

**Request:**
```json
POST /api/ai/journal-summary
{
  "trade_ids": [<id1>]
}
```

**Expected response (HTTP 200):**
```json
{
  "summary": null,
  "trade_count": 1,
  "model": null,
  "cached": false,
  "message": "AI summarisation is currently unavailable. Please try again later."
}
```

**Verification:**
- HTTP status is 200 (not 500)
- `summary` is null
- `message` is a user-facing informational string (not a stack trace)
- `model` is null
- One audit record created in `ai_audit_log`: `summary_produced = false`, `output_hash = null`
- No exception propagated to the client

---

### AI-S-03 — Frontend: AI Summary Section Collapsed by Default on Page Load

**Canonical spec:** `docs/specs/api_contracts/ai_endpoints.md` (display-only constraint); implied by SRB-v1.7 (no automated advisory)

**Preconditions:**
- User navigates to the Trade History or Journal page containing the AI summary section
- No user interaction performed after page load

**Expected behaviour:**
- AI summary section is in collapsed state immediately after page load
- No call to `POST /api/ai/journal-summary` is made on page load
- A control to expand the section (button or chevron) is visible

**Verification method:** Code review of component initial state (default collapsed state in component state or CSS); network request inspection confirms no LLM call on mount.

---

### AI-S-04 — Frontend: Disclaimer Always Visible When Section Expanded

**Canonical spec:** `docs/specs/api_contracts/ai_endpoints.md` (display-only constraint; AI output not for decision-making)

**Preconditions:**
- User expands the AI summary section (triggers `POST /api/ai/journal-summary`)
- Summary loads (both success and failure states)

**Expected behaviour (all expanded states):**
- Disclaimer text is visible whenever the AI summary section is expanded
- Disclaimer must be visible in: (a) loading state, (b) summary returned, (c) summary null / error state
- Disclaimer is not hidden, collapsed, or behind a scroll

**Disclaimer text must include:** indication that AI output is informational only and not a recommendation to buy or sell.

**Verification method:** Code review confirms disclaimer is rendered unconditionally within the expanded section (not conditional on `summary !== null`).

---

## DoQ Sign-Off

- [x] Minimum 4 scenarios defined covering: happy path, LLM failure, frontend collapse, disclaimer visibility
- [x] All scenarios reference `docs/specs/api_contracts/ai_endpoints.md` and `trade_history` as canonical spec
- [x] Backend scenarios include expected HTTP status, response shape, and audit log assertions
- [x] Frontend scenarios specify verification method (code review)
- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-04-24
- Comments: Autonomous class sign-off — all four qualifying criteria met. No frontend implementation in this story; scenarios reference code-review-verifiable AC.
