Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-10

# Execution Escalations — 2026-11-06__release-v9.16

## ESC-EXEC-20261110-01

- **Raised at:** 2026-11-10T08:07:27Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-06__release-v9.16
- **Step:** STEP 3.1.D (EPIC-05 execution loop, first sub-step of ST-20 per `sprint_backlog.md` ST-20 Notes)
- **ST/EPIC item:** ST-20 / EPIC-05 (BLG-AI-28)
- **Trigger type:** Strategy
- **Blocking statement:** Three `_NON_TICKER_WORDS` entries are tickers in the scan universe (`backend/tickers_full_list.csv`): **PM** (Philip Morris), **MA** (Mastercard) and **ON** (ON Semiconductor). Checked on this branch; no other entry collides with the universe (AM, IMO, NOTE and BST are listed symbols outside it). A held one is still cited, because `_ticker_in` runs first. A non-held one is never treated as a ticker: the briefing summary check (check 3, ruling `ESC-EXEC-20261027-02` (B)) does not caveat it, and the chat focus rule (ruling `ESC-EXEC-20261030-03`) does not see it as an "other ticker", so with focus `MU` held and PM not held, "PM's stop was hit last week." gets the MU stop note. That is the misattribution `ESC-EXEC-20261030-03` exists to prevent. Neither ruling nor the contract says the collision was decided. Options: **(A) context rule** — each colliding word is a non-ticker only in its non-ticker usage, and otherwise a ticker on both checks (briefing caveat if not held or in context; chat "other ticker" path, so no focus note): PM and AM only directly after a time ("3 PM", "3:30 PM", "3PM"); MA only directly after a number or a period ("200 MA", "50-day MA", "20-week MA"); ON only directly after RISK ("RISK ON"). **(B) universe wins** — PM, MA and ON are treated as tickers everywhere; "Your stop was hit at 3 PM." then loses the MU note and "50-day MA" in a briefing is caveated, so (B) does not meet ST-20 AC 2's second sentence without (A)'s time exception. **(C) non-ticker wins** — keep current behaviour and document it as decided: "PM's stop was hit last week." keeps the MU note. Under every option a held collision ticker is still cited first, the note text, `compliance_check_result` values and fail-open behaviour are unchanged, and model text is never edited.
- **Engine recommendation (non-binding):** (A). It closes the misattribution case while keeping the usual "3 PM", "50-day MA" and "RISK ON" usages silent, and it applies one rule to both checks.
- **Owning authority:** AI Compliance & Governance Officer
- **Unblock criteria:** a dated ruling recorded in this escalation's resolution before the code change (ST-20 AC 1). The engine then implements it for PM, MA and ON (and any token ST-19 finds that collides with the universe), adds the AC 2 sentences as tests with the ruled results, keeps every v9.14 ST-16/ST-17 and v9.15 ST-26 test passing, and states the handling in `ai_endpoints.md` check 3 and the chat focus paragraph.
- **SLA due-by:** 2026-11-13T08:07:27Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-10T08:12:43Z):** AI Compliance & Governance Officer ruling, given in-session by the user acting in that role, dated 2026-11-10: **option (A), context rule.** PM, MA and ON (and AM, for symmetry with PM) count as non-tickers only in their usual non-ticker usage, and otherwise as tickers on both the briefing summary check (check 3, ruling `ESC-EXEC-20261027-02` (B)) and the chat focus rule (ruling `ESC-EXEC-20261030-03`): PM/AM only directly after a time ("3 PM", "3:30 PM", "3PM"); MA only directly after a number or a period ("200 MA", "50-day MA", "20-week MA"); ON only directly after RISK ("RISK ON"). Otherwise a non-held one is caveated in the briefing (unless in the context) and is an "other ticker" in chat, so "PM's stop was hit last week." with focus MU held and PM not held gets no MU note; "Your stop was hit at 3 PM." still gets the MU note. A held collision ticker is still cited first. Note text, `compliance_check_result` values and fail-open behaviour are unchanged; model text is never edited. Applies to any token ST-19 finds that collides with the scan universe. ST-20 reclassified `autonomous`.
- **Clarification (2026-11-10, same officer, in session):** implementing (A) as worded flipped the v9.14 test sentence "Your stop is above the MA and ATR stays OK." (focus NVDA), which ST-20 AC 3 requires to keep passing. Ruled: MA is also a non-ticker directly after a determiner ("the", "its", "a", "an", "their"), the moving-average usage. The rest of (A) is unchanged.

## ESC-EXEC-20261110-02

- **Raised at:** 2026-11-10T09:34:25Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-06__release-v9.16
- **Step:** STEP 3.1.D (EPIC-07 execution loop, first sub-step of ST-30 per `sprint_backlog.md` ST-30 Notes)
- **ST/EPIC item:** ST-30 / EPIC-07 (BLG-GOV-198)
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-30 AC 1 needs a dated decision naming where the ST-id is recorded for each Base44 prompt draft: a comment header, a delegation log field, or both. The engine may not choose the convention. Current practice: all 3 filed prompts in `docs/frontend/prompts/` (v6.3) already carry a `**Story:** ST-xx (BLG-xx, EPIC-xx, vX.Y)` header line, but no rule requires it. `base44_frontend_prompt_owner.md` §12 already makes `ST item` a mandatory delegation record field, but the record does not link to the filed prompt.
- **Engine recommendation (non-binding):** Both. The filed prompt's header carries a `**Story:**` line, and the `delegated_frontend` delegation record names the filed prompt path. Write the convention into the `OPERATIONAL_GUIDE.md` frontend delegation text under the CLAUDE.md §6 checklist (AC 2). Use `strategy-benchmark-v1.md` (ST-11, v6.3) as the AC 3 existing example.
- **Owning authority:** Base44 Frontend Prompt Owner
- **Unblock criteria:** A dated ruling is recorded in this escalation's resolution. The engine then writes the convention to the place the ruling names (AC 2) and records the AC 3 example.
- **SLA due-by:** 2026-11-11T09:34:25Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Open
