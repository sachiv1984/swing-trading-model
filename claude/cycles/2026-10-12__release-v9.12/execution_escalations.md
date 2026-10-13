Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-13

# Execution Escalations — 2026-10-12__release-v9.12

## ESC-EXEC-20261013-01

- **Raised at:** 2026-10-13T07:25:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-12__release-v9.12
- **Step:** STEP 3.1.D (EPIC-01 execution loop, raised at sprint start per `sprint_backlog.md` ST-04 Notes)
- **ST/EPIC item:** ST-04 / EPIC-01 (BLG-AI-10)
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-04 adds a post-generation check that catches a daily-briefing or chat response citing a stop without its recalculation time (`stop_calculated_at`, put into both contexts by v9.11 ST-08). BLG-AI-10's scope requires the AI Compliance & Governance Officer to sign off the action taken on a miss before it is built: **(A)** append the time from context to the response, or **(B)** log and count the miss and return the response unchanged.
- **Engine recommendation (non-binding):** none offered; the choice was put to the owner with both options framed.
- **Owning authority:** AI Compliance & Governance Officer
- **Unblock criteria:** A dated ruling (A, B or a combination), recorded in this escalation's resolution and in ST-04's QA evidence. The engine then implements and tests it for briefing and chat, and adds the check to the boundary-sample audit (AC 3).
- **SLA due-by:** 2026-10-14T07:25:00Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-10-13T07:25:55Z):** AI Compliance & Governance Officer ruling, agent-mediated per `execution_prompt.md` §5.3, dated 2026-10-13: **Approved on the first pass — (A) combined with (B).** On a miss the service appends a code-written note, `(<TICKER> <_stop_recalculated_label(p)>)`, after the model's text in the affected field (briefing `summary`, each `actions[].description`, chat `response`), and logs and counts every miss. Neither option alone is approved. Detection: a sentence matching `\bstops?\b` cites a stop. Tickers are open positions from the same context, matched as whole words, plus the action's own `ticker`. The time counts as present if the field contains that position's `stop_calculated_at` date (`YYYY-MM-DD`), or "not recalculated since entry" when it is NULL. A citation with no attributable ticker is logged but nothing is appended. Count: `claude_audit_log.compliance_check_result` = `pass` / `stop_time_missing_appended` / `stop_time_missing_unattributed`, so no schema change is needed. 8 binding conditions: (1) model text is never edited, only appended to, and only from `_stop_recalculated_label()`; (2) the boundary-sample store receives the raw pre-append output; (3) the audit script gains a context-free `scan_stop_time_missing()`, reported as its own `[STOP-TIME-MISSING]` count separate from the §13.2 violations, with a test over the illustrative NVDA rows; (4) the check fails open; (5) tests cover the briefing summary, an action description and chat, asserting the exact note, the unchanged model text, no duplicate note, the warning log and `compliance_check_result`; (6) no response-schema change, or contract and `openapi.yaml` in the same commit; (7) prompt text unchanged, so prompt versions stay v1.2 / v1.1; (8) the append is documented as a deterministic, code-authored addition in the module docstring and the contract. Charter grounds cited: `ai_compliance_governance_officer.md` §1, §3.1, §3.2, §4.1–§4.4, §7; `strategy_rules.md` §13.1–§13.3. ST-04 is reclassified `autonomous` and continues.
