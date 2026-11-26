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
- **Confirmation (2026-11-20T09:46:29Z):** following the pre-commit code review, the AI Compliance & Governance Officer (the user, in session) confirmed two points put to them with an agent-mediated recommendation: **(i)** the negation/declined-suggestion exemption (`_NEGATED_CHANGE_RE`, per-sentence check, briefing and chat only, journal summary unchanged) is approved, on condition that every exempted sentence is logged (`action=negation_exempt`, endpoint and field, no model text) for review at §13.5 re-attestation; **(ii)** the detector misses found in review ("may want to…", "too loose/too tight", halve/double/trail, "don't hesitate to…") are not widened in this sprint, because the detector is shared with the journal summary; they are filed as BLG-AI-34 (P3, provisional v9.19, to be ruled and built with BLG-AI-32, which already lists "You may want to tighten your stops."), which also adds the forms to the boundary sample audit.
- **Implementation note (2026-11-20, PR review):** the agent-mediated Director of Quality and Product Owner reviews found that the first implementation of exemption (i) matched any negation or disclaimer anywhere in the sentence (14 advice sentences passed, e.g. "I cannot advise on trades, but you should consider tightening your stop on NVDA."). It was narrowed to the scope confirmed in (i): only the negated phrase is set aside and the rest of the sentence is checked again; a declined suggestion counts only as "can't/don't … suggest/recommend/advise/say whether/if/that", with the text before it, and after any following contrast ("but/though/however/yet", dash or colon), still checked (round 2 added the "after" check for "I can't say whether X, but [advice]"). This implements the confirmed scope rather than changing it, so no new ruling was sought. Disclosure: the exemption was built in `5e91c0e8` (09:21Z) before its confirmation (09:46Z); the base ruling preceded the code.

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
- **Disposition:** Resolved
- **Resolution summary (2026-11-20T14:14:19Z):** Decision by the AI Compliance & Governance Officer and the Product Owner (both held by the user, given in session, 2026-11-20), on an agent-mediated recommendation: **keep** the debrief focus area at one observational sentence. **Evidence:** 10 production debriefs generated with prompt v1.1 on 2026-11-20 (DEL-20261120-01; production had held only 2 debriefs, both v1.0, and no trade had closed since 2026-10-12). 6 of 10 focus sentences were left out by the numeric cross-check, including all 4 trades that exited on the trailing stop as planned; the 4 shown repeat an R figure computed against the position's starting stop but compared with the plan's target (MU 2026-09-30: 0.59R shown, 2.24R on the plan stop, target 2.2R), and 3 summaries show stops that do not fit the exit. **Rationale:** the one-sentence limit is not what makes the debrief feel empty; the omitted sentences and wrong inputs are. Allowing 2–3 sentences now would widen AI commentary on figures shown to be wrong. **Citations, each answered:** `strategy_rules.md` §13.2 (the AI-text sentence naming the post-trade debrief): unchanged and still enforced; the current limit keeps the debrief within it, and one sampled sentence (STX 2026-07-02, "allowing the position to decline") is close to suggesting a stop change, filed as BLG-AI-36. The §13.5 row for the ST-06 debrief review (`decisions--2026-08-17__release-v8.9--ST-06-section13-review.md`, CONDITIONAL): no amendment, since the limits are kept; Conditions 1, 2, 3 and 9 stand, and the sample shows Condition 9's checks working as fail-safe (no non-compliant sentence shown) but over-rejecting. No `strategy_rules.md` §13.5 change. **Re-review trigger:** once BLG-BE-226 (R basis) and BLG-AI-35 (number check) ship, review a fresh 10-debrief sample and reopen the question. **Filed:** BLG-BE-226 (P2), BLG-AI-35 (P2), BLG-BE-227 (P3), BLG-AI-36 (P3), and BLG-BE-228 (P2, duplicate INTC 2026-09-08 trade_history row, confirmed by the user as looking like a duplicate). ST-40 reclassified `autonomous`.

## ESC-EXEC-20261124-01

- **Raised at:** 2026-11-24T14:36:01Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-18__release-v9.18
- **Step:** STEP 3.1.D (EPIC-02; ST-07 is `delegated_decision` at seal)
- **ST/EPIC item:** ST-07 / EPIC-02 (BLG-UX-21)
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-07's remaining AC needs dated Head of UX & Design approval that `navigation.md` (v2.5, the two §14.2 moves, written at the design gate) and `design_system.md` (the §14.5 design direction) reflect DL-089's adoption of the 2026-11-17 re-review §14. The engine wrote `design_system.md` v1.28 §Design Direction from §14.5, with each gap naming its backlog item (BLG-UX-11, BLG-FE-288, BLG-FE-311, BLG-FE-313, BLG-FE-314, BLG-FE-315, BLG-FE-317).
- **Engine recommendation (non-binding):** approve both files.
- **Owning authority:** Head of UX & Design
- **Unblock criteria:** a dated Head of UX & Design approval of both files, recorded in `design_system.md` and the ST-07 QA evidence.
- **SLA due-by:** 2026-11-25T14:36:01Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-24T14:36:34Z):** Head of UX & Design approval, given by the user in session (holds the role), 2026-11-24: `design_system.md` v1.28 §Design Direction and `navigation.md` v2.5 both approved. Recorded in `design_system.md` §Design Direction. ST-07 reclassified `autonomous` and completed.

## ESC-EXEC-20261124-02

- **Raised at:** 2026-11-24T14:36:01Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-18__release-v9.18
- **Step:** STEP 3.1.D (EPIC-02; ST-12 is `delegated_decision` at seal, "Strategy Rules & System Intent Owner confirmation (dated) of the `trade_plan.md` v1.30 §6 §13-note amendment, before the build")
- **ST/EPIC item:** ST-12 / EPIC-02 (BLG-UX-19)
- **Trigger type:** Lifecycle
- **Blocking statement:** `trade_plan.md` v1.30 §6 amends the PT-05 §13 note (`docs/specs/compliance/pt05_entry_checklist_s13_review.md`, "no automated condition evaluation") so that "Position size checks" (worst of the §4.2.2 sector-concentration, §4.2.4 cash and §4.2.5 sizing-validity pre-entry checks) and "Stop level defined" (Stop Level holds a positive number) show a deterministic status instead of a tick. Both are advisory under `strategy_rules.md` §4.2.6, gate nothing and make no recommendation, so the spec states no new §13 review is needed. The build cannot start until the owner confirms.
- **Engine recommendation (non-binding):** confirm.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** a dated confirmation of the `trade_plan.md` v1.30 §6 §13-note amendment.
- **SLA due-by:** 2026-11-25T14:36:01Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-24T14:36:34Z):** Strategy Rules & System Intent Owner confirmation, given by the user in session (holds the role), 2026-11-24: the `trade_plan.md` v1.30 §6 §13-note amendment is confirmed; the two items stay advisory under §4.2.6, gate nothing and make no recommendation; no new §13 review. Recorded in `trade_plan.md` §6. ST-12 reclassified `autonomous`.

## ESC-EXEC-20261124-03

- **Raised at:** 2026-11-24T14:36:01Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-18__release-v9.18
- **Step:** STEP 3.1.D (EPIC-02; ST-13 is `delegated_decision` at seal, "Metrics Definitions & Analytics Owner definition in `metrics_definitions.md`, before the build")
- **ST/EPIC item:** ST-13 / EPIC-02 (BLG-FE-320)
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-13 needs the "rules followed" definition per closed trade before `GET /trades` can return `rules_followed`/`rules_broken`. Data facts: `red_flag_events` (`pre_entry_override`, `checklist_skipped`, `stop_prompt_dismissed`, `drawdown_prompt_dismissed`) carries a nullable `position_id`; a plan-time `pre_entry_override` is written before the position exists, so its `position_id` is usually null, but the plan stores `pre_entry_override_acknowledged` and is later linked by `trade_plans.position_id`; `pre_entry_validation_log` has no position link; the checks run on every Trade Entry route from 2026-11-04 (v9.15, `e0a78667`); `strategy_rules.md` §8.3 allows a manual exit at any time. Draft put to the owner: Not known with no `position_id`; Broken on any `red_flag_events` row with the position's id, or a linked plan with `pre_entry_override_acknowledged = true`; Followed when nothing is broken and the checks provably ran (a linked plan with a `pre_entry_validation_snapshot`, or `entry_date` on or after 2026-11-04); otherwise Not known; the exit reason never counts.
- **Engine recommendation (non-binding):** approve the draft.
- **Owning authority:** Metrics Definitions & Analytics Owner
- **Unblock criteria:** a dated definition approved by the owner and recorded in `metrics_definitions.md`.
- **SLA due-by:** 2026-11-25T14:36:01Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-24T14:36:34Z):** Metrics Definitions & Analytics Owner approval, given by the user in session (holds the role), 2026-11-24: the draft is approved as written (all four red-flag event types count). The engine records it in `metrics_definitions.md` §Rules Followed with worked examples. ST-13 reclassified `autonomous`.

## ESC-EXEC-20261126-01

- **Raised at:** 2026-11-26T16:26:09Z (first raised in session on 2026-11-24; that question went unanswered when the session ended, and was asked again on 2026-11-26)
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-18__release-v9.18
- **Step:** STEP 3.1.A, ST-12 first-time-right pass A, check 17 (readers of a new state)
- **ST/EPIC item:** ST-12 / EPIC-02 (BLG-UX-19)
- **Trigger type:** Lifecycle
- **Blocking statement:** `trade_plan.md` v1.30 §6.5 and design record `trade-plan-checklist-status` §4 save the two system items as `heat_limit_checked.checked` = (Position size checks is pass) and `stop_defined.checked` = (stop set). `backend/routers/trade_plans.py` `_maybe_write_checklist_skipped_event` writes a `checklist_skipped` red flag when a saved checklist has any unchecked item, and the `metrics_definitions.md` rules-followed definition approved for ST-13 (`ESC-EXEC-20261124-03`) counts `checklist_skipped` as broken. A plan saved before shares are entered ("Not checked yet") or with an acknowledged size warning would log "Checklist Skipped" and mark the trade "rules broken" although the trader ticked every item they can tick.
- **Engine recommendation (non-binding):** count only judgement items: ignore items saved with `"auto": true` when counting unchecked items.
- **Owning authority:** Product Owner; Head of UX & Design
- **Unblock criteria:** a dated choice of how `checklist_skipped` counts the system items.
- **SLA due-by:** 2026-11-27T16:26:09Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-26T16:26:09Z):** Decision by the user in session (holds the Product Owner and Head of UX & Design roles), 2026-11-26: **judgement items only**. `checklist_skipped` counts unchecked items among entries without `"auto": true`, so it fires only when "Strategy signal confirmed" or "Pre-trade research reviewed" is unticked ("{n} of 2 checklist items unchecked"). Size warnings and fails stay recorded as `pre_entry_override`. Built in ST-12 with tests and notes in `trade_plan.md` §6.5 and `red_flag_journal.md`. Legacy plans (no `auto` flag) are counted as before.

## ESC-EXEC-20261126-02

- **Raised at:** 2026-11-26T17:11:43Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-18__release-v9.18
- **Step:** STEP 3.1.A, ST-13 pre-commit code review (commit-check Check 11)
- **ST/EPIC item:** ST-13 / EPIC-02 (BLG-FE-320)
- **Trigger type:** Lifecycle
- **Blocking statement:** the review of the staged ST-13 build found two gaps in the definition approved under `ESC-EXEC-20261124-03`. (1) A `checklist_skipped` event written when a plan is saved has no `position_id` (the position does not exist yet), so it never joins, and a trade whose plan skipped checklist items shows as "Followed"; the event names its plan in `context.plan_id`, and the plan later links to the position. (2) The "checks provably ran" fallback used the user-entered `entry_date`, which can be back- or forward-dated; `positions.created_at` records when the position was entered in the app.
- **Engine recommendation (non-binding):** join plan-time events through `context.plan_id` → `trade_plans.position_id`; use `positions.created_at` for the 2026-11-04 test.
- **Owning authority:** Metrics Definitions & Analytics Owner
- **Unblock criteria:** a dated choice for each gap.
- **SLA due-by:** 2026-11-27T17:11:43Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-26T17:11:43Z):** Metrics Definitions & Analytics Owner decision, given by the user in session (holds the role), 2026-11-26: (1) **yes** — plan-time events join through the plan; (2) **`positions.created_at`**. Recorded in `metrics_definitions.md` v1.36.0 §Rules Followed (rows C2 and F2 added) and `trade_endpoints.md` v2.7.0; built in ST-13 with tests `tests/test_rules_followed.py` and `tests/test_rules_followed_db.py`.
