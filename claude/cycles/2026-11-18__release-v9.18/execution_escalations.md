Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-20

# Execution Escalations — 2026-11-18__release-v9.18

## ESC-EXEC-20261119-01

- **Raised at:** 2026-11-19T08:07:49Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-18__release-v9.18
- **Step:** STEP 3.1.D (EPIC-01; ST-05 is `delegated_decision` at seal, "raise at sprint start")
- **ST/EPIC item:** ST-05 / EPIC-01 (BLG-SEC-46)
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-05 needs a dated re-review decision by the Cybersecurity & Trust Lead and the Product Owner on the 2026-10-15 open-access accept-risk (`docs/operations/credential_policy.md` §1.1), explicitly covering **read** access to the owner's real positions, cash, P&L and journal. Facts for the review: the front end has no sign-in (`AuthContext.js` hard-codes one user); the site URL is public and named in `package.json`; the repository is public; there is no `robots.txt` or `noindex` under `public/`; `REACT_APP_API_KEY` is in the public bundle and authorises all routes, reads and writes; the public source map (BLG-OPS-221) makes the bundle easier to read. Options: **(1)** keep the acceptance with reasons, and add `noindex` + `robots.txt` (filed as its own item); **(2)** put access control in front of the static site (for example a Cloudflare Access / basic-auth proxy), filed as a v9.20 remedy item; **(3)** narrow the front-end key (the earlier option (a): read-only or allowlisted key), filed as its own item; **(4)** another remedy.
- **Engine recommendation (non-binding):** (2) as the v9.20 remedy, with (1)'s `noindex`/`robots.txt` filed now as a small interim item. Read exposure of real financial data is not reduced by (3), because a read-only key still exposes every read; only access control in front of the site (and the API) closes it.
- **Owning authority:** Cybersecurity & Trust Lead; Product Owner
- **Unblock criteria:** a dated decision from both owners, recorded in `credential_policy.md` §1.1 (with review triggers updated), covering read access; any remedy filed as its own backlog item.
- **SLA due-by:** 2026-11-20T08:07:49Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-19T13:56:00Z):** Decision by the Cybersecurity & Trust Lead and the Product Owner (both held by the user, given in session, 2026-11-19): the 2026-10-15 acceptance no longer covers read access to the owner's data. Remedy: access control in front of the site and the API (BLG-SEC-48, provisional v9.20). Interim: `noindex` and a disallow-all `robots.txt` (BLG-SEC-49, provisional v9.19). Write-scope acceptance stands until BLG-SEC-48 ships. Recorded in `docs/operations/credential_policy.md` §1.1 v1.2 with updated review triggers. ST-05 reclassified `autonomous` and completed.

## ESC-EXEC-20261120-01

- **Raised at:** 2026-11-20T08:49:02Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-18__release-v9.18
- **Step:** STEP 3.1.D (EPIC-07; ST-39 is `delegated_decision` at seal, "AI Compliance & Governance Officer ruling recorded before the code")
- **ST/EPIC item:** ST-39 / EPIC-07 (BLG-AI-29)
- **Trigger type:** Lifecycle
- **Blocking statement:** `strategy_rules.md` §13.2 (v1.25) says AI-written text describing the user's data, naming the daily briefing and chat, must not suggest changing stops, position sizing, setups or any other strategy parameter. `POST /ai/daily-briefing` and `POST /ai/chat` check only stop times (ST-04, v9.12) and tickers (ST-17, v9.13); nothing checks that sentence. The BLG-FEAT-50/51 §13 review (`docs/product/decisions/decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md`, §13.5 row "BLG-FEAT-50/51 (AI Advisory Layer — daily briefing + chat)") cleared both features with Criterion 3 ("no prompt design that asks the LLM to improve or revise strategy parameters") and Binding Condition 5, but required no output-side check. The ruling must settle two things. **(1) Which check form applies:** **(a)** the `trading_change` category only (`_TRADING_CHANGE_RE` plus the advisory forms from the journal-summary check: wording that suggests changing stops, sizing or setups), so briefing actions written as recommendations ("EXIT AAPL: the stop was breached") still pass; or **(b)** both journal-summary categories (`scan_prescriptive` and `trading_change`), which would also catch "you should exit", the wording a deterministic EXIT/HOLD recommendation often takes. In either case the EXIT/ENTER/MONITOR/HOLD `type` and `ticker` fields are never checked, only text. **(2) How a failure is handled:** **(A)** regenerate once, then a code-written fallback (briefing: a failing summary is replaced by a code-written line and a failing action keeps its deterministic `type`/`ticker` with a code-written description; chat: a fixed withheld message); **(B)** a code-written note appended after the model's text, the stop-time and ticker check pattern (model text still shown); **(C)** log only. Each call's result goes in `claude_audit_log.compliance_check_result`, combined with the existing stop-time and ticker results.
- **Engine recommendation (non-binding):** (1)(a) and (2)(A). (a) matches §13.2's wording exactly: the briefing is designed to recommend deterministic actions, and `scan_prescriptive` would flag that. (A) matches the journal summary, debrief and monthly narrative, so wording that suggests a parameter change never reaches the user, and the deterministic EXIT/HOLD actions survive a fallback.
- **Owning authority:** AI Compliance & Governance Officer
- **Unblock criteria:** a dated choice of (1) and (2) recorded in this escalation's resolution, citing §13.2 and the §13.5 BLG-FEAT-50/51 row.
- **SLA due-by:** 2026-11-21T08:49:02Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-20T09:02:57Z):** AI Compliance & Governance Officer ruling, given by the user in session (holds the role), 2026-11-20: **(1)(a)** the `trading_change` category only, so recommendations under the existing rules pass and action `type`/`ticker` are never checked; **(2)(A)** regenerate once, then a code-written fallback. Binding conditions: (1) the check is the journal summary's `_trading_change_found`, applied to the raw briefing `summary`, each `actions[].description` (after the context-ticker filter) and the raw chat `response`; `scan_prescriptive` is not applied; (2) one regeneration per request covers every failing field; on a second failure a failing summary becomes "The AI summary was withheld because it suggested changing a stop, position size or setup.", a failing action keeps `type` and `ticker` with the description "Description withheld because it suggested changing a stop, position size or setup.", and chat returns "The answer was withheld because it suggested changing a stop, position size or setup. Please ask again or rephrase your question." with no `answer_id`; the stop-time and ticker checks run only on kept model text; (3) one `claude_audit_log` row per model call: `fail_regenerate:trading_change`, then the stop-time/ticker value, `pass_on_regenerate[+<value>]` or `fail_fallback:trading_change[+<value>]`; logs carry field names and categories only; the sampling hook gets each attempt's raw output; (4) both prompts add a sentence not to suggest changing stops, sizing, setups or any other strategy setting (`BRIEFING_PROMPT_VERSION` v1.4, `CHAT_PROMPT_VERSION` v1.3); (5) `ai_endpoints.md` and `ai_s13_boundary_test_suite.md` (B-DB-06, B-CH-07) updated. **Citations, each answered:** `strategy_rules.md` §13.2 (the AI-text sentence naming the daily briefing and chat): enforced on output by this check. The §13.5 row for BLG-FEAT-50/51 (`decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md`): its clearance stands; the check adds an output-side control to Criterion 3 and Binding Condition 5, and the regeneration is a further call to the same model in the same request, so Binding Conditions 2, 4 and 9 are unaffected; the next §13.5 re-attestation should record this control. The ruling's sentence classification is re-verified by the ST-39 tests, not relied on alone (LL-v8.6-P3-01). ST-39 reclassified `autonomous`.

## ESC-EXEC-20261120-02

- **Raised at:** 2026-11-20T08:49:02Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-18__release-v9.18
- **Step:** STEP 3.1.D (EPIC-07; ST-40 is `delegated_decision` at seal)
- **ST/EPIC item:** ST-40 / EPIC-07 (BLG-GOV-378)
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-40 needs a recorded decision, with rationale, from the AI Compliance & Governance Officer and the Product Owner: keep the debrief focus area at one observational sentence about how execution differed from plan (`debrief_service.py` `_FOCUS_AREA_SYSTEM`, prompt v1.1), or allow 2–3 observational sentences (still non-prescriptive and number-checked) covering what went well as well as what differed. The decision must cite `strategy_rules.md` §13.2 (the AI-text sentence naming the post-trade debrief) and the §13.5 row for the ST-06 debrief review (`docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md`, CONDITIONAL), and answer each. The relevant review conditions are 1 (pattern-surfacing, not prescriptive), 2 (numbers sourced verbatim), 3 (retrospective framing) and 9 (output-side checks: `scan_prescriptive`, `numeric_cross_check`, regenerate once then fallback). None of them fixes the sentence count, so allowing more sentences is a change to the prompt and output contract under the same conditions, not a new §13 review (Condition 7's trigger, a suggested follow-up trade, is not met). A `strategy_rules.md` §13.5 change is not authorised by this plan; any implementation is filed as its own item. The scope asks for the decision to be made against a sample of real production debriefs (BLG-BE-152 shipped v9.11, so the precondition is met). The execution environment has only the staging database, so the sample is a Human-Delegation (DEL-20261120-01). If the sample is not available in-sprint, AC 1 is `post-merge` and BLG-GOV-378 stays open (sealed `sprint_backlog.md` ST-40 Staging-only ACs).
- **Engine recommendation (non-binding):** decide against the sample. Without it, the engine has no basis to recommend keep or amend.
- **Owning authority:** AI Compliance & Governance Officer; Product Owner
- **Unblock criteria:** a dated keep-or-amend decision with rationale from both owners, citing §13.2 and the §13.5 ST-06 row; if amend, the §13 review amendment recorded and the implementation item filed.
- **SLA due-by:** 2026-11-21T08:49:02Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Open
