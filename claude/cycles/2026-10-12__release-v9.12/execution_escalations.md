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

## ESC-EXEC-20261013-02

- **Raised at:** 2026-10-13T08:24:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-12__release-v9.12
- **Step:** STEP 3.2 (EPIC-01 completion, before PR)
- **ST/EPIC item:** ST-06 / EPIC-01 (BLG-OPS-183); `DEL-20261013-02` step 2
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-06 AC 2 asks for the scheduler that calls `POST /ai/check-daily-cost` to be named with its last successful run recorded. The scheduler is named: `.github/workflows/ai-daily-cost-check.yml`, which is new because none existed, and the user confirmed that none runs outside the repo. A scheduled or dispatched workflow can run only from `main`, though, so no run can exist before EPIC-01 merges. Everything else in ST-06 is met (AC 1 pytest, AC 3 cost-estimate correction, AC 2 scheduler naming).
- **Product Owner ruling (2026-10-13, human, in-session):** "accept ST-06 post-merge, open the PR. However ensure this is checked before and not left open." ST-06 is accepted for the EPIC-01 merge gate with the AC 2 run record completed after merge. This escalation stays **Open** until that run is recorded, so that `.github/workflows/escalation-sla-reminder.yml` and `run sprint` STEP -1.2A surface it if it slips. It must be closed before Sprint Close: `DEL-20261013-02` also stays In Progress, and STEP 5.0 hard-gates on it.
- **Owning authority:** Infrastructure & Operations Owner
- **Unblock criteria:** After EPIC-01 merges, one successful `ai-daily-cost-check.yml` run, dispatched or scheduled. Its run ID, date and the endpoint's JSON response are recorded in `ai_endpoints.md` ("Last successful run"), in `qa_evidence_EPIC-01.md` under ST-06, and in `DEL-20261013-02` (→ Unblocked). The engine runs `gh run list --workflow ai-daily-cost-check.yml` at the first `run sprint` after the merge.
- **SLA due-by:** 2026-10-16T08:24:00Z (72h — Human-Delegation)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-10-13T09:15:52Z):** closed post-merge on the evidence recorded in `DEL-20261013-02` (now Unblocked). `ai-daily-cost-check.yml` run 38374258055 succeeded at 09:09 UTC against production deployed at `90099bec`. Production's only `claude_audit_log` row for the day (09:12:10) post-dates that run, so `request_count: 0` was correct. A post-merge staging journal summary wrote a costed `claude_audit_log` row (`POST /ai/journal-summary`, v1.0, $0.001628). `ai_endpoints.md` "Last successful run" is filled in. Closed before Sprint Close, as the Product Owner required.

## ESC-EXEC-20261013-03

- **Raised at:** 2026-10-13T09:21:40Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-12__release-v9.12
- **Step:** STEP 3.1.D (EPIC-06 execution loop, raised at sprint start per `sprint_backlog.md` ST-43 Notes)
- **ST/EPIC item:** ST-43 / EPIC-06 (BLG-GOV-364)
- **Trigger type:** Lifecycle
- **Blocking statement:** `idea_intake_prompt.md` §4 and STEP 0 assume every role in `eligible_agents` is exercised, yet `IW-20260928-01` (3 roles) and `IW-20260930-01` (2 roles) ran with a disclosed reduced roster. v2.10's roster rule (§2.1 step 2a) constrains such a window while a build-and-ship pull-forward is mandatory, but whether reduced-roster windows are permitted at all, and how they interact with `roadmap_prompt.md` STEP -1.6's standalone pre-run exception, has never been ruled on. ST-43's AC needs a recorded ruling first: (A) prohibit reduced-roster windows; (B) permit them under stated conditions with a cap (e.g. no two consecutive reduced windows); or (C) permit them with disclosure only, as today. Any adopted change ships with the full CLAUDE.md §6 checklist.
- **Engine recommendation (non-binding):** none yet; a Head of Specs Team position is being drafted (agent-mediated, §5.3) for the human Product Owner to confirm.
- **Owning authority:** Head of Specs Team; Product Owner
- **Unblock criteria:** A dated Head of Specs Team + Product Owner ruling (A, B or C) recorded in this escalation's resolution. The Product Owner half must be confirmed by the human Product Owner. On (B), the engine applies the cap to `idea_intake_prompt.md` (and STEP -1.6 if needed) with the CLAUDE.md §6 checklist.
- **SLA due-by:** 2026-10-14T09:21:40Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-10-13T09:57:26Z):** ruling **(B): permit reduced-roster windows under conditions, with a no-two-consecutive cap.** The Head of Specs Team position was agent-mediated per `execution_prompt.md` §5.3 (charter §3, §5; first pass). It was **confirmed by the human Product Owner in-session on 2026-10-13** (AskUserQuestion, option "B — permit with cap"). Grounds: option C fails the charter §5 "enforced consistently" bar, since 3 of the last 6 windows ran reduced, each for its own ad hoc reason, and §10 "All agent roles submit" contradicted the §2.1 step 2a roster rule. Option A is too rigid: IW-20260930-01's two-role review produced BLG-BE-135, seated at v9.9. Applied by ST-43: `idea_intake_prompt.md` gains §4.1 (PO authorisation, roster rule, no-two-consecutive cap, disclosure; a hard gate in both modes), and the §2.1 step 2a, §10 and STEP 0 wording follows it. `roadmap_prompt.md` STEP -1.6 bounds the standalone pre-run exception by §4.1. Both carry the CLAUDE.md §6 checklist. The most recent window (IW-20261008-01) was reduced, so the next window must be full roster. ST-43 is reclassified `autonomous`.

## ESC-EXEC-20261013-04

- **Raised at:** 2026-10-13T09:21:40Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-12__release-v9.12
- **Step:** STEP 3.1.D (EPIC-06 execution loop)
- **ST/EPIC item:** ST-44 / EPIC-06 (BLG-GOV-372)
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-44 adds a split-credit secondary tally to `scripts/compute_role_share_history.py` and a split-credit column to `claude/roadmap/role_share_history.md`. The write is authorised by the §7 plan-authorised named-file rule (case a, `sprint_backlog.md` Named-file writes). The story stays `delegated_decision` under the release plan's RISK-06 mitigation (`ESC-CLOSE-20261006-01`), so its owners must approve the method before it lands: equal split of each compound story's credit across its named roles (BLG-GOV-372 Scope), the raw tally remaining primary for roadmap §7.2, and the column's placement in `role_share_history.md`.
- **Engine recommendation (non-binding):** approve the equal-split method as scoped in BLG-GOV-372. The column is additive, history rows are back-filled by the script, and the raw primary tally §7.2 reads is unchanged.
- **Owning authority:** Director of HR; PMO Lead
- **Unblock criteria:** A dated Director of HR + PMO Lead approval (agent-mediated per §5.3 permitted) recorded in this escalation's resolution. The engine then implements ST-44 after ST-45, extending ST-45's test file.
- **SLA due-by:** 2026-10-14T09:21:40Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-10-13T09:30:53Z):** Director of HR and PMO Lead approval, agent-mediated per `execution_prompt.md` §5.3, dated 2026-10-13: **both Approved, with conditions** on the first pass. Charter grounds: `director_of_hr.md` §2, §3.2, §4.1, §4.3; `pmo_lead.md` §5.2, GI-3, GI-5. v9.9 check: all 35 Owner strings compound, Head of Specs Team solo bucket 0; split credit 8.0/35 = 22.9%. 5 binding conditions: (1) split only on `"; "`, strip trailing parenthetical qualifiers, dedupe roles within a string, check tokens against `check_sprint_backlog_owners.py`'s canonical roles and warn on unmatched tokens rather than crediting them silently; (2) the raw tally stays primary and is the only figure §7.2's 40% ceiling reads, with no `roadmap_prompt.md` change; (3) one rightmost History column "Split-Credit Top Role" (`<role> — <credit 2dp> (<share 1dp>%)`, ties "tied with"), plus a separate "Split-credit" sub-table per cycle breakdown; (4) back-fill all 6 recorded cycles as a one-time ST-44 write, with existing raw columns byte-identical; (5) tests for a 2-role split (0.5), a 3-role split (1/3), qualifier stripping and dedupe, and per-cycle conservation (credits sum to the story count). PMO Lead observation (not an ST-44 change): the v9.8–v9.10 rolling line's "19 of v9.10's 21 Owner values are compound" should read 17. That correction is outside ST-44's named-file AC, so it is filed separately. ST-44 is reclassified `autonomous` and continues after ST-45.

## ESC-EXEC-20261013-05

- **Raised at:** 2026-10-13T15:33:58Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-12__release-v9.12
- **Step:** STEP 3.1.D (EPIC-05 execution loop)
- **ST/EPIC item:** ST-38 / EPIC-05 (BLG-SPEC-183)
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-38 AC 3 requires the doc-fix vs code-fix decision on `positions.entry_price`'s currency to carry Data Model & Domain Schema Owner sign-off. Code evidence: `create_position()` (`backend/services/position_service.py`) takes `entry_price` in native currency, writes `entry_price = entry_price_native / fx_rate` (GBP; unchanged for UK) and `fill_price = entry_price_native`, and `total_cost = (entry_price_native × shares + fees_native) / fx_rate`. Every native-price reader (`position_service.py` lines ~134, 378, 461, 637, 1179; `portfolio_service.py`) already reads `fill_price` for US. `data_model.md` §2 has said GBP since v2.55. `data_model_positions_dictionary.md` v0.3 still says native, including its US `total_cost` and `pnl` derivations. DS-23's reconstruction note calls the currency "ambiguous (BLG-SPEC-183)". Read-only staging aggregate (user-authorised, 2026-10-13): 0 US positions on staging, so the live sample is empty; per `sprint_backlog.md` ST-38 Notes, the AC is met from code and specs.
- **Engine recommendation (non-binding):** **doc fix.** State GBP for `entry_price` (native in `fill_price`, broker fill in `user_fill_price`) in the dictionary and DS-23; correct the dictionary's US `total_cost` to `fill_price × shares / fx_rate + fees_paid` (equivalently `entry_price × shares + fees_paid`) and its `pnl` derivations to use `fill_price`. Note in `data_model.md` that `backend/test_data/seed_chart_test_data.sql` writes UK prices in pence (test data only). A code fix would change stored values and every reader, and would change displayed values, which needs a design pass (`sprint_backlog.md` ST-38 Notes).
- **Owning authority:** Data Model & Domain Schema Owner
- **Unblock criteria:** A dated Data Model & Domain Schema Owner decision (agent-mediated per §5.3 permitted), recorded in this escalation's resolution and in `data_model.md`.
- **SLA due-by:** 2026-10-14T15:33:58Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-10-13T15:36:45Z):** Data Model & Domain Schema Owner, agent-mediated per `execution_prompt.md` §5.3, dated 2026-10-13: **Approved with conditions — doc fix.** `positions.entry_price` is GBP for every market; `fill_price` is the native entry, `user_fill_price` the broker fill. Code fix rejected (5 readers already use `fill_price`; destructive migration; displayed values would change without a design pass). AC ruling: "matches create_position()'s input" means the value `add_position()` passes to `database.create_position()` (`position_data['entry_price']`, GBP). Evidence cited inline, including the US `total_cost` check: $100 × 10 + $1.50 fee at fx 1.25 gives £801.20 by the code, by `fill_price × shares / fx_rate + fees_paid` and by `entry_price × shares + fees_paid`; the old dictionary formula gives £641.20. Conditions: C1, dictionary rows `entry_price`/`fill_price`/`fx_rate`/`total_cost`/`pnl` plus §5.1/§5.2 in the same change; C2, file the pnl live-FX/no-fee divergence as a backlog item before the PR, not fixed in ST-38 (filed as BLG-SPEC-198; claim re-verified against `portfolio_service.py`); C3, dictionary version bump and 3-entry Last Updated. ST-38 reclassified `autonomous`.

## ESC-EXEC-20261013-06

- **Raised at:** 2026-10-13T17:22:34Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-12__release-v9.12
- **Step:** STEP 3.1.D (EPIC-02 execution loop)
- **ST/EPIC item:** ST-10 / EPIC-02 (BLG-BE-159)
- **Trigger type:** Strategy
- **Blocking statement:** ST-10 AC 1 requires a Strategy Rules & System Intent Owner ruling, recorded before the code change, on whether a user may set or raise a stop manually under `strategy_rules.md` §7.3 (RISK-02). The Trail Stop modal calls `PATCH /positions/{id}`, a route that does not exist, so every apply fails. `positions.md` v2.16 §Trail Stop Action carries Branch A (manual raise via `PATCH /positions/{id}/stop`, ratchet-validated: rejected at or below `current_stop` or at or above the current price) and Branch B (read-only modal, button renamed "View Trail"). Under both branches the "Lower stop to {value}" label is removed. Separately, AC 3: `add_position()` (`backend/services/position_service.py`) accepts a `stop_price` argument and never uses it. The design record (`docs/design/2026-10-12__release-v9.12/trail-stop-action/decision_record.md` §2.4) recommends rejecting a supplied entry `stop_price` with a 400.
- **Engine recommendation (non-binding):** none on the branch choice, which is a strategy-boundary call. AC 3: reject with 400, per the design record.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** A dated Strategy Rules & System Intent Owner ruling naming Branch A or Branch B and the AC 3 treatment, recorded in this escalation's resolution. Agent-mediated per §5.3 is permitted on the user's explicit direction (given in-session on 2026-10-13).
- **SLA due-by:** 2026-10-16T17:22:34Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-10-13T17:26:32Z):** Strategy Rules & System Intent Owner ruling, agent-mediated per `execution_prompt.md` §5.3 (user-directed: the user chose agent-mediated rulings for ST-10/ST-14 in-session on 2026-10-13), dated 2026-10-13: **Branch B, Approved with conditions** — no manual stop change; the Trail Stop modal becomes read-only and the button is renamed "View Trail". Grounds: §7.3 forbids only downward moves, but under the ratchet a manual raise becomes a permanent, user-chosen floor that later recomputes build on, which is discretionary input (§13.2 "not a discretionary or adaptive rule system"; §3 makes the human the executor of entries and exits, not the setter of stops). The modal's value uses the stored ATR and a hardcoded 2.0 multiplier with no §7.2 breakeven floor (`backend/main.py` ~1994–1998), while the nightly job uses a freshly fetched ATR (`position_service.py` ~640). Writing from that second formula would break §12.3 consistency between backtest, live and documentation. A manual exit (§6.3, §8.3) remains available. **AC 3: reject a supplied entry `stop_price` with HTTP 400.** Approved message: "stop_price is not accepted. The initial stop is set by the system at entry price − 5 × ATR (strategy_rules.md §5, §11)." The 5 is verified against §11 (strategy_rules.md:444) and `INITIAL_ATR_MULTIPLIER = 5.0` (`backend/strategy_parameters.py:22`). Binding conditions: (1) remove the "Lower stop to …"/"Update stop to …" labels and the `PATCH /positions/{id}` mutation, add no stop-write route, and delete Branch A from `positions.md` §Trail Stop Action in the same commit; (2) keep the "Raise by" row as display only; (3) build the 5 in the AC 3 message from `INITIAL_ATR_MULTIPLIER`, not a literal; (4) reject only a non-null `stop_price`, keeping the field on `AddPositionRequest` so the 400 can fire rather than Pydantic silently dropping it; (5) remove the unused `stop_price` parameter from `add_position()`; (6) leave `portfolio_size.py`'s sizing-input `stop_price` alone; (7) file a backlog item for the modal's hardcoded 2.0 multiplier and missing breakeven floor; (8) any future manual-stop feature needs a versioned §12.3 strategy change. Evidence cited inline by the ruling (file:line): strategy_rules.md:64/307/335/387/444/460/476/487/495; main.py:1941–2010; position_service.py:443/464/530/640/816; calculations.py:400–408; strategy_parameters.py:22; models/requests.py:23; Positions.js:224–249. There is no prior ruling on manual stop changes. ST-10 is reclassified `autonomous`.

## ESC-EXEC-20261013-07

- **Raised at:** 2026-10-13T17:22:34Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-12__release-v9.12
- **Step:** STEP 3.1.D (EPIC-02 execution loop)
- **ST/EPIC item:** ST-14 / EPIC-02 (BLG-BE-148)
- **Trigger type:** Strategy
- **Blocking statement:** ST-14 replaces the weekday calendar in `backend/services/gap_risk_service.py` with the US exchange calendar for "next trading session", and uses the US market date (so a 02:00 UTC view uses the US date). The v9.10 addendum's Ruling 3, in `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md`, says: "Exchange holidays are not modelled; the deterministic weekday calendar is the rule." ST-14 therefore changes Ruling 3, which applies §13.3's "falls before that position's next trading session" limb. Per the slice AC, the Strategy Rules & System Intent Owner records a dated addendum that answers §13.3 and §13.5 (the roster row and the 2027-02-06 re-attestation). The calendar must be deterministic, with no network call at request time.
- **Engine recommendation (non-binding):** a rule-based NYSE full-closure holiday calendar computed in code (pandas `AbstractHolidayCalendar`, already a dependency; no network), with the "today" date taken in `America/New_York`. Early-close days count as trading sessions.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** A dated Strategy Rules & System Intent Owner ruling on the revised Ruling 3 (calendar, market date), with the §13.3/§13.5 addendum text, recorded in this escalation's resolution and appended to the decision record by ST-14. Agent-mediated per §5.3 is permitted on the user's explicit direction (given in-session on 2026-10-13).
- **SLA due-by:** 2026-10-16T17:22:34Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-10-13T17:26:56Z):** Strategy Rules & System Intent Owner ruling, agent-mediated per `execution_prompt.md` §5.3 (user-directed: the user chose agent-mediated rulings for ST-10/ST-14 in-session on 2026-10-13), dated 2026-10-13: **Revised Ruling 3 Approved.** `T` is the current America/New_York date. A US position is flagged when `1 ≤ days_until ≤ d`, where `days_until` is the earnings date minus `T` and `d` is the calendar days from `T` to the first NYSE session after `T`. Weekends, NYSE full-closure holidays (NYSE observance: Saturday holidays move to Friday, except that New Year's Day on a Saturday is not observed; Sunday holidays move to Monday; Juneteenth from 2022) and an in-code list of one-off closures are not sessions. Early closes are sessions. Rulings 1 and 2 are unchanged. The change stays within §13.3's carve-out (a closer reading of the "next trading session" limb), so no new §13 review is needed. Binding Conditions 1–8 hold. No `strategy_rules.md` change. Binding conditions: (1) deterministic, in-code calendar with no network, file, database or OHLCV inference; (2) one market date on both sides: compute `days_until` from `next_earnings_date − T` in `gap_risk_service`, not `earnings_service`'s server-local `days_until_earnings` (`earnings_service.py:60-61` uses `date.today()`; verified by the engine); (3) rule-based with no year limit; (4) one-off closures kept as a dated in-code constant, with docstring and contract stating that unannounced closures are not anticipated, the last-checked date, and the under-flag-only error direction; (5) tests: the two ACs, Thursday before Good Friday, New Year's Day on a Saturday not observed (2021-12-31 is a session), Juneteenth before 2022, early close counts as a session (Wednesday before Thanksgiving gives d=2), a view on a holiday, a published 2026–2027 NYSE holiday fixture, a no-network test, and all existing tests kept; (6) docstring cites the v9.12 addendum, the weekday text is replaced, and the docstring test is extended; (7) `position_endpoints.md` and `positions.md` weekday wording updated in the same commit, with a contract changelog row; (8) scope lock: no change to the `reasons` enum, Rulings 1/2, the statistic definition, GET behaviour or consumers. Non-binding: file the weekend-statistic selection (`today.weekday() >= 4`, which does not follow the calendar) and the existing `_compute_gap_stats` `> 3`-day weekend classification defect (a Friday-to-Monday gap is exactly 3 days, so ordinary weekends land in the overnight set; verified by the engine), and `earnings_service.py:39`'s `utcfromtimestamp` date roll, as backlog items. The addendum text is appended to the decision record by ST-14. ST-14 is reclassified `autonomous`.
