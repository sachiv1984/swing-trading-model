**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-06-29
**Story:** ST-06 (BLG-GOV-148, EPIC-01, v6.3)

---

# AI Advisory Endpoint — Contract Review Checklist

## Purpose

This checklist must be completed for every AI advisory endpoint before the endpoint is considered contract-complete. It enforces §13 (SRB-v1.7) boundary requirements alongside standard contract documentation standards. Checklist results are appended as a sign-off block to the relevant endpoint section in the contract document.

---

## Checklist Template

For each AI advisory endpoint, confirm all items below. Mark: **PASS** / **FAIL** / **N/A**.

### §13 Boundary Checks

| # | Check | Requirement | Evidence |
|---|-------|-------------|----------|
| §13-01 | Response schema contains `advisory: true` | Every response includes `advisory` field with value `true` at the root level; client must verify | Schema definition in contract |
| §13-02 | No automated action fields in response | Response must not contain fields that directly initiate trades, modify positions, or trigger any automated system action | Schema review: no `order_id`, `position_id_to_close`, `execute`, `action_required: true`, or equivalent fields |
| §13-03 | Response is display-only | API contract explicitly states AI output is read-only display output — it must NOT feed into signals, scoring, compliance, or trade plan calculations | Contract contains "display-only" statement; SRB-v1.7 reference present |
| §13-04 | §13 Status documented | Contract section includes an explicit `**§13 Status:**` line with classification (PASS / CONDITIONALLY COMPLIANT) and date of review | Check for `§13 Status:` heading |
| §13-05 | Disclaimer requirement stated | Contract notes that the corresponding frontend surface must display an advisory disclaimer (non-dismissible) | Contract or linked spec references disclaimer requirement |

### Contract Completeness Checks

| # | Check | Requirement | Evidence |
|---|-------|-------------|----------|
| CC-01 | Rate limiting documented | Contract includes rate limit (requests/min/IP), HTTP 429 response schema, and Retry-After header description | Rate limiting section with 429 response block |
| CC-02 | Audit logging documented | Contract states token usage is logged to `claude_audit_log` via `create_claude_audit_entry` | Implementation constraints section |
| CC-03 | Model identifier documented | Contract names the specific Claude model used (e.g., `claude-sonnet-4-6`) | Response schema or implementation constraints |
| CC-04 | Error response for LLM unavailability documented | Contract specifies what happens when the external LLM API is unreachable (HTTP 200 with null summary / error string, not HTTP 500) | Error responses section |
| CC-05 | openapi.yaml entry exists | Endpoint has a corresponding path entry in `docs/reference/openapi.yaml` including 429 response | grep-verifiable |
| CC-06 | Contract version bumped on any endpoint change | Any modification to endpoint behaviour is accompanied by a contract version bump and changelog entry | Changelog section |

---

## Retroactive Application — v6.2 AI Advisory Endpoints

Applied to contracts in `docs/specs/api_contracts/ai_endpoints.md` as of v1.5 (2026-06-29).

### POST /ai/daily-briefing

| # | Check | Result | Notes |
|---|-------|--------|-------|
| §13-01 | `advisory: true` in response | **PASS** | `"advisory": true` present in response schema (v1.4+) |
| §13-02 | No automated action fields | **PASS** | `actions[]` contains `type`, `ticker`, `description` — display-only; no execution trigger fields |
| §13-03 | Display-only statement | **PASS** | Contract states: "Advisory-only — display-only, not integrated with trade execution" |
| §13-04 | §13 Status documented | **PASS** | `§13 Status: PASS — SRB-v1.7` present since v1.4 |
| §13-05 | Disclaimer requirement stated | **PASS** | Frontend surface `AiDailyBriefing.js` displays non-dismissible "AI Advisory" badge; confirmed in ST-05 assessment |
| CC-01 | Rate limiting documented | **PASS** | Added v1.5 (ST-03): 10 req/min/IP, 429+Retry-After schema |
| CC-02 | Audit logging documented | **PASS** | "Token usage logged to `claude_audit_log` via `create_claude_audit_entry`" in implementation constraints |
| CC-03 | Model identifier documented | **PASS** | `claude-sonnet-4-6` named in response schema and constraints |
| CC-04 | LLM unavailability documented | **PASS** | "Always returns 200. LLM errors return `summary: null` with `error` message" in error responses |
| CC-05 | openapi.yaml entry | **PASS** | `/ai/daily-briefing` path present in `docs/reference/openapi.yaml` v3.5.0; 429 response added v3.5.0 |
| CC-06 | Contract versioned on change | **PASS** | v1.0→1.1→1.2→1.3→1.4→1.5 changelog entries present |

**Result: ALL PASS.** No gaps found. No remediation items required.

---

### POST /ai/chat

| # | Check | Result | Notes |
|---|-------|--------|-------|
| §13-01 | `advisory: true` in response | **PASS** | `"advisory": true` present in response schema (v1.4+) |
| §13-02 | No automated action fields | **PASS** | Response contains `response` (string), `advisory` (bool), `model` (string) — display-only; no execution trigger fields |
| §13-03 | Display-only statement | **PASS** | Contract states: "Advisory-only — display-only, not integrated with trade execution" |
| §13-04 | §13 Status documented | **PASS** | `§13 Status: PASS — SRB-v1.7` present since v1.4 |
| §13-05 | Disclaimer requirement stated | **PASS** | Frontend surface `AiChatWidget.js` displays non-dismissible "Advisory" header badge and footer text; confirmed in ST-05 assessment |
| CC-01 | Rate limiting documented | **PASS** | Added v1.5 (ST-03): 30 req/min/IP, 429+Retry-After schema |
| CC-02 | Audit logging documented | **PASS** | "Token usage logged to `claude_audit_log` via `create_claude_audit_entry`" in implementation constraints |
| CC-03 | Model identifier documented | **PASS** | `claude-sonnet-4-6` named in constraints |
| CC-04 | LLM unavailability documented | **PASS** | "Always returns 200. LLM errors return a `response` error string" in error responses |
| CC-05 | openapi.yaml entry | **PASS** | `/ai/chat` path present in `docs/reference/openapi.yaml` v3.5.0; 429 response added v3.5.0 |
| CC-06 | Contract versioned on change | **PASS** | v1.0→…→1.5 changelog entries present |

**Result: ALL PASS.** No gaps found. No remediation items required.

---

## Open Item — BLG-SEC-01 (cross-reference)

ST-04 injection risk assessment identified `context_opts.ticker` (POST /ai/chat) as an open risk (user-controlled string interpolated into system prompt without sanitization). This is a security gap, not a contract documentation gap. The contract currently does not document input validation requirements for `context_opts.ticker`. When BLG-SEC-01 is resolved (v6.4), the contract should be updated to document ticker validation rules in the request parameter table.

---

## Usage Guide for Future AI Endpoints

When a new AI advisory endpoint is added:

1. Add it to `docs/specs/api_contracts/` (or the relevant contract document)
2. Complete this checklist for the new endpoint section
3. Attach the completed checklist as a sign-off block at the end of the endpoint section
4. Checklist sign-off counts as the §13 gate clearance for the new endpoint
5. openapi.yaml must be updated in the same commit (CLAUDE.md §2)

---

## Sign-Off

| Role | Decision | Date |
|------|----------|------|
| API Contracts & Documentation Owner | Approved — checklist complete; retroactive application to POST /ai/daily-briefing and POST /ai/chat — both ALL PASS; no gaps found at v1.5 | 2026-06-29 |
| Head of Specs Team | Approved — checklist template adopted as mandatory step for all future AI advisory endpoint contracts | 2026-06-29 |

*Sign-off completed by Sprint Execution Engine under agent-mediated governance protocol — ST-06 AC-04.*
