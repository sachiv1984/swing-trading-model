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
- **Disposition:** Open

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
