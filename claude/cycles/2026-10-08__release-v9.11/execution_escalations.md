Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-08

# Execution Escalations — 2026-10-08__release-v9.11

## ESC-EXEC-20261008-01

- **Raised at:** 2026-10-08T11:01:30Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-08__release-v9.11
- **Step:** STEP 3.1.D (EPIC-03 execution loop, raised at sprint start per `sprint_backlog.md` ST-16 Notes)
- **ST/EPIC item:** ST-16 / EPIC-03 (BLG-BE-143)
- **Trigger type:** Strategy
- **Blocking statement:** `strategy_rules.md` §6.3 says that during grace "the stop price is calculated and stored", but the two live paths disagree. The on-load path (`position_service.analyze_positions`, the `if grace_period:` branch) carries the stored stop over unchanged, with no recalculation. The nightly job (`position_service.run_nightly_trailing_stop_update`) never checks grace: it recalculates with `calculate_trailing_stop` and ratchets the stored stop up from day 0. The outcomes: (a) **recalculate and ratchet during grace** (the nightly behaviour): the on-load path also recalculates and stores, but nothing is enforced until day 10. The first enforced stop can then be tighter than a day-10 recalculation would give, because a mid-grace price spike is locked in by the ratchet. (b) **freeze the stop at the §5 initial stop during grace** (the on-load behaviour): the nightly job skips in-grace positions, "calculated and stored" is read as "calculated at entry and stored", and trailing starts from the initial stop on day 10. (c) **recalculate and store for display, without ratcheting, during grace**: both paths compute the stop, but the stored stop on day 10 is the initial stop, and the ratchet starts then.
- **Engine recommendation (non-binding):** (b). §6.4 gives the grace period's purpose as avoiding exits caused by normal post-entry volatility. Under (a), that same volatility still sets the level of the first enforced stop through the ratchet. (b) matches the on-load path that every user-facing screen already shows, and it reads §6.3's "calculated and stored" as the entry-time calculation already asserted by `TestEntryPersistsInitialStop`. If the Owner prefers (a) or (c), §6.3 needs no wording change for (a), and a clarifying sentence for (c).
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** A dated ruling (a), (b) or (c), recorded in this escalation's resolution and in ST-16's QA evidence. Any `strategy_rules.md` §6.3 wording edit is made only under the Owner's explicit authority, with its Change Log row. The engine then aligns the diverging path, adds the in-grace parity test, and moves traceability row C6.3-02 to Asserted.
- **Dependants:** ST-17 (the grace ruling may affect the recorded parameter source).
- **SLA due-by:** 2026-10-11T11:01:30Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Open

## ESC-EXEC-20261008-02

- **Raised at:** 2026-10-08T11:01:30Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-08__release-v9.11
- **Step:** STEP 3.1.D (EPIC-04 execution loop, raised at sprint start per `stage4_backlog_slice_addendum.md` step 1)
- **ST/EPIC item:** ST-25 / EPIC-04 (BLG-FEAT-59)
- **Trigger type:** Strategy
- **Blocking statement:** ST-25 adds a new call to an AI provider whose output sits inside a financial report (Monthly P&L). No existing §13 review covers AI text inside a financial report (design gate §13 pre-check, `design_gate.md`). Per the RISK-06 confirmation route ruled at planning, the Strategy Rules & System Intent Owner must record a PASS / CONDITIONAL / FAIL §13 determination for the monthly P&L narrative. It must cite every §13 clause that names AI output or financial reporting (ST-25 AC 2; ST-35's citation rule, if it has landed by then). At minimum, §13.1 and §13.2 ("a machine-learning or AI-driven prediction system"), and the §13.5 roster (each AI feature joins it at its first clearance). Prior AI-output precedents for the conditions: `decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md` (briefing and chat) and `decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` (debrief, Conditions 1, 2 and 9).
- **Engine recommendation (non-binding):** CONDITIONAL, with conditions mirroring the debrief review: the narrative is backward-looking and covers the user's own month only; every number is sourced verbatim from the deterministic Monthly P&L figures, enforced by a server-side numeric cross-check; prescriptive-language scan with a deterministic fallback; advisory framing (AdvisoryBadge); optional and dismissible; no persistence as a recommendation; and a §13.5 roster row added in the same commit as the determination.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** A dated PASS / CONDITIONAL / FAIL determination recorded under `docs/product/decisions/`, citing each §13 clause that names AI output or financial reporting. On PASS or CONDITIONAL, ST-25 continues with addendum steps 2–3 (AI endpoint security checklist with ST-23's cost input; design decision record with Product Owner approval; `reports.md` update) before any implementation commit. On FAIL, or a ruling that a full §13 review is needed, ST-25 and ST-26 stop and go to `amend cycle`.
- **Dependants:** ST-26 (usage counter).
- **SLA due-by:** 2026-10-11T11:01:30Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Open

## ESC-EXEC-20261008-03

- **Raised at:** 2026-10-08T11:01:30Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-08__release-v9.11
- **Step:** STEP 3.1.D (EPIC-06 execution loop, raised at sprint start per `sprint_backlog.md` ST-34 Notes)
- **ST/EPIC item:** ST-34 / EPIC-06 (BLG-GOV-355)
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-34 AC 2 changes `roadmap_prompt.md` STEP 2.4 so each rebalance appends both PVR readings (story-count and effort-weighted). `BLG-GOV-339`'s scope requires Head of Specs Team **and** Product Owner sign-off before any STEP 2.4 behaviour change. AC 1, the `product_value_ratio_history.md` `## History` backfill, is authorised by the §7 named-file rule (case a) and does not wait on this sign-off.
- **Engine recommendation (non-binding):** Approve. The change adds one column to an existing append step. It does not change the PVR thresholds, the Advisory pull-forward rule or the Alert-tier actions, and the effort-weighted figure is already defined and cross-validated in `metrics_definitions.md` Appendix F.
- **Owning authority:** Head of Specs Team; Product Owner
- **Unblock criteria:** Both sign-offs recorded with a date in this escalation's resolution and in ST-34's QA evidence. The engine then applies the STEP 2.4 edit under the CLAUDE.md §6 checklist.
- **SLA due-by:** 2026-10-09T11:01:30Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Open
