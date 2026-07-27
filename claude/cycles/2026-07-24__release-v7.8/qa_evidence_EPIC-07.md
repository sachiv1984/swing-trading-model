Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-26

# QA Evidence — EPIC-07 (v7.8)

**EPIC:** EPIC-07 — Scheduled rotation-and-audit cadence for third-party API keys
**Cycle:** 2026-07-24__release-v7.8
**Sprint goal:** Ship all 12 v7.8 EPICs with every acceptance criterion met and QA sign-off recorded for each EPIC.
**Test scenarios used:** Derived from spec + AC — documentation/process artefact, verified by review (no runnable test applicable).

## ST-07 — Define rotation-and-audit schedule for all external API keys

**Spec reference:** `docs/ops/api_key_rotation_and_audit_schedule.md` (new artefact, Case B)
**Commit:** `78bee997` (implementation `7fee996e`)

**What was built:** A new consolidated document covering all 5 named external key types (Yahoo Finance, Alpaca, Gemini, Claude, Telegram), building on `alpaca_key_rotation_policy.md`'s existing pattern. 3 entries (Alpaca, Claude/Anthropic, Telegram) have real credentials with concrete first-rotation dates. 2 entries (Yahoo Finance, Gemini) were verified — via direct code inspection, not assumption — to have **no actual credential** in this codebase: Yahoo Finance calls public endpoints with only a `User-Agent` header, and "Gemini" is a legacy filename (`gemini_service.py`) that calls only the Anthropic API (consistent with the pre-existing `ESC-EXEC-20260720-01` finding in `database.py`). Adds a new **quarterly audit cadence**, distinct from rotation, for all 5 entries.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-07 | `api_key_rotation_and_audit_schedule.md` | Consolidated 5-key-type rotation-and-audit schedule | Schedule documented for all 5 key types, building on alpaca_key_rotation_policy.md pattern | Pass | None |
| ST-07 | (same) | (same) | First rotation date set per key | Pass — 3 real credentials get concrete dates; 2 no-credential entries correctly marked "not applicable" rather than assigned a fabricated date | None |
| ST-07 | (same) | (same) | Cybersecurity & Trust Lead sign-off | Pass — agent-mediated sign-off obtained (see below) | None |

**QA test coverage:**
- Scenarios run: none applicable — process/documentation artefact, verified by review per the story's own framing ("no code, no Design Gate dependency").
- Regression areas checked: not applicable (no code changed).
- Known deviations filed: None.

## Story-Level Domain-Authority Sign-Off (BLG-GOV-14)

The story's own acceptance criteria named a specific authority (Cybersecurity & Trust Lead), obtained via §5.3 agent-mediated sign-off protocol, distinct from and in addition to the EPIC-level DoQ consolidation block below:

- **Role:** Cybersecurity & Trust Lead
- **Method:** Agent-mediated (§5.3) — subagent invoked with the role's charter (`claude/agents/cybersecurity_trust_lead.md`)
- **Verdict:** Approved
- **Date:** 2026-07-26
- **Notes:** The reviewing agent independently verified both load-bearing "no credential" claims (Yahoo Finance, Gemini) directly against the codebase before approving — did not take the drafted claims on faith. Confirmed the Alpaca/Telegram anchor-date reasoning (scheduling convenience only, not a fabricated rotation event) as sound and properly caveated. No blocking findings.

## Autonomous class eligibility check (BLG-GOV-19)

- Criterion 1 (all stories autonomous): ✓ — ST-07 is the only story, classified `autonomous`.
- Criterion 2 (all AC verifiable by code review alone): ✓ — pure documentation artefact.
- Criterion 3 (no frontend-visible change): ✓ — only `docs/ops/*.md` touched.
- Criterion 4 (engine signer field populated): ✓ — see below.

**All four criteria met — autonomous class applies for the EPIC-level consolidation.** Per BLG-GOV-14, this does not substitute for the story-level domain-authority sign-off above — both are recorded.

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-07-26
- Comments: Autonomous class sign-off for the EPIC-level consolidation — all four qualifying criteria met. Story-level Cybersecurity & Trust Lead sign-off (agent-mediated, §5.3) recorded separately above per BLG-GOV-14 — confirmed cleared.
