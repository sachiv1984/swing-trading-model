Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-06

# Execution Escalations — 2026-10-06__release-v9.10

## ESC-EXEC-20261006-01

- **Raised at:** 2026-10-06T15:08:11Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-06__release-v9.10
- **Step:** STEP 3.1.D (EPIC-01 execution loop, raised at sprint start per `sprint_planning_notes.md` Execution Sequence)
- **ST/EPIC item:** ST-01 / EPIC-01 (BLG-BE-138)
- **Trigger type:** Strategy
- **Blocking statement:** ST-01 AC 2 needs a parameter-authority ruling before the single parameter source can be built, because the source differs by outcome. (a) The §11 values are fixed: one backend constants source, and Settings shows them read-only. (b) A sanctioned personal override recorded in `strategy_rules.md` §12: the `settings` row becomes the one source, and every path must read it, including the nightly job, which hard-codes 5×/2× today. (c) Changeable only through a §12.3 change record: same build as (a), with `strategy_rules.md` §12 wording. Today the paths disagree. `analyze_positions` reads the editable `settings` row. `run_nightly_trailing_stop_update` hard-codes `_INITIAL_ATR_MULT = 5.0` / `_PROFIT_ATR_MULT = 2.0`. `should_exit_position` is called with a literal `grace_period_days=10`. `grace_service` hard-codes `10 - holding_days`. `add_position` hard-codes `multiplier=5.0`. The Settings form seeds `5`/`2`/`3` and Trade Entry seeds `atr_multiplier_initial: 2`. Choosing an outcome is a strategy-boundary decision, so the engine does not make it.
- **Engine recommendation (non-binding):** (a). §11 already says the values "must be consistent across production backtests, live system logic, and reported performance metrics", and §12.3 already governs changing them. An editable per-user override (b) would make the live stop path diverge from the backtest by design. (a) and (c) build the same code; (c) only adds §12 wording.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** A dated ruling (a), (b) or (c), recorded in this escalation's resolution and in ST-01's QA evidence. For (b) or (c), the ruling also authorises the `strategy_rules.md` §12 edit and its Change Log row, which ST-05's registry rule then covers. AC 1 (production read, `DEL-20261006-01`) and AC 6 (Product Owner correction decision for any diverged stop) are tracked separately and do not block the ruling.
- **Dependants:** ST-03 (settings-change text), ST-06 (displayed multiplier), ST-07 (Trade Entry fallback multiplier), ST-05 (registry entry if §12 changes).
- **SLA due-by:** 2026-10-09T15:08:11Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolved at:** 2026-10-06T17:30:09Z
- **Resolved by:** Strategy Rules & System Intent Owner (direct user ruling, 2026-10-06: "Go with (a), start building")
- **Resolution summary:** Outcome (a), fixed parameters. The §11 values (10-day grace, 5× / 2× ATR, 14-day ATR) are held in one backend source, `backend/utils/strategy_parameters.py`, read by every live stop path. They are never read from the editable `settings` row. Settings shows them read-only. No `strategy_rules.md` §12 change is needed, so ST-05's registry rule is not triggered. AC 1 (production read, `DEL-20261006-01`) and AC 6 (Product Owner correction decision, only if production drifted) remain open.

## ESC-EXEC-20261006-02

- **Raised at:** 2026-10-06T15:08:11Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-06__release-v9.10
- **Step:** STEP 3.1.D (EPIC-01 execution loop, raised at sprint start)
- **ST/EPIC item:** ST-05 / EPIC-01 (BLG-BE-137)
- **Trigger type:** Strategy
- **Blocking statement:** ST-05 AC 1 needs a ruling on strategy-version registry coverage. `backend/strategy_version_registry.py` ends at 1.4. `strategy_rules.md` has Change Log rows 1.5–1.14, so `get_current_strategy_version()` stamps every new position and trade plan as 1.4. The registry docstring and `data_model.md` DS-11 both say the registry is updated in the same commit as any new Change Log row. Either that obligation has been breached ten times, or there is an unwritten exemption for documentation-only versions. The two options: (1) register only versions that change behaviour or parameters, and tag each Change Log row as behavioural or documentation-only; (2) register every version, adding 1.5–1.14 with effective dates, which changes `strategy_version_at_entry` stamping and SI-04 comparison attribution from now on.
- **Engine recommendation (non-binding):** (1). The registry's purpose is to group trades by the strategy that produced them (SI-04). A wording-only version produces identical trades, so registering it would split comparable trades into separate cohorts.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** A dated ruling (1) or (2), recorded in this escalation's resolution. The engine then aligns the registry docstring, DS-11 and `strategy_version_comparison_contract.md` Implementation Note 2, and replaces the hard-coded `len == 5` test with one derived from the Change Log.
- **SLA due-by:** 2026-10-09T15:08:11Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolved at:** 2026-10-06T17:40:37Z
- **Resolved by:** Strategy Rules & System Intent Owner (direct user ruling, 2026-10-06: "Go with behaviour-only for ST-05, build it")
- **Resolution summary:** Option (1), behaviour/parameter-changing versions only. The registry stays at 1.0–1.4, and 1.5–1.14 are classified documentation-only in `DOCUMENTATION_ONLY_VERSIONS`. 1.1 is grandfathered (zero-width window). The classification sits beside the registry rather than as a tag on `strategy_rules.md`'s Change Log rows, because that file is outside Sprint Execution's write scope. The test enforces the same rule either way. No `strategy_version_at_entry` stamping or SI-04 attribution changes.

## ESC-EXEC-20261006-05

- **Raised at:** 2026-10-06T16:00:46Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-06__release-v9.10
- **Step:** STEP 3.1.D (EPIC-04 execution loop)
- **ST/EPIC item:** ST-20 / EPIC-04 (BLG-SPEC-171)
- **Trigger type:** Strategy
- **Blocking statement:** ST-20 AC 1 requires the Strategy Rules & System Intent Owner to acknowledge findings F1, F2 and F4 (`docs/product/decisions/po05_replay_scope_confirmation.md` §1) and to decide the replay results-view caption wording. The corrections in AC 2 and AC 3 then edit an SRSIO-owned §13 decision record, so they follow the acknowledgement rather than precede it. F1: replay does not reuse IT-06's Alpaca mechanics; it runs on `strategy_engine.py` and makes no Alpaca call. F2: "byte-identical" determinism does not hold for a float pipeline fed by `yfinance`; the guarantee is fingerprint-checkable. F4: the engine differs from §7.2 in several ways: no breakeven floor, close-only ATR, stop evaluated before risk-off, entry-fee treatment. Text still to correct: `po05_section13_preassessment.md` lines 21, 73, 88, 124, 140–144; `claude/roadmap/current_roadmap.md` line 399 (PO-05 row: "Requires Alpaca paper trading foundation (IT-06)") and line 534 (IT-06 row: "foundational for PO-05 replay mode"). These are written in-sprint under the named-file ruling (`ESC-CLOSE-20261006-01`, `sprint_planning_notes.md`). `replay_mode.md` §13 item 5 was already corrected in v0.2 (ST-01c, v9.7); only its determinism and divergence wording remains to align.
- **Engine recommendation (non-binding):** acknowledge F1, F2 and F4 as stated in the scope note. Caption: **"Simulated with the strategy backtest engine's exit rules, which differ from live stop handling in a few places."** This is wording-only inside the existing `replay-fx-basis-caption` area (FI-P3-02 exception, design gate: Design Pre-Approved).
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** A dated acknowledgement of F1, F2 and F4 and the chosen caption text, recorded here and in ST-20's QA evidence. The engine then applies AC 2 and AC 3 and cites `ESC-CLOSE-20261006-01` in the commit that edits `current_roadmap.md`.
- **SLA due-by:** 2026-10-09T16:00:46Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Open

## ESC-EXEC-20261006-06

- **Raised at:** 2026-10-06T16:04:53Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-06__release-v9.10
- **Step:** STEP 3.1.A step 11 (sign-off gate), EPIC-04
- **ST/EPIC item:** ST-15 / EPIC-04 (BLG-GOV-140)
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-15 AC 3 requires sign-off from the Product Owner and from the Strategy Rules & System Intent Owner on `docs/ops/ai_chat_section13_quarterly_self_audit_checklist.md`. The SRSIO half was attempted agent-mediated (§5.3); see `execution_state.json` ST-15 `sign_off_record`. The Product Owner half cannot be agent-mediated and needs the human Product Owner.
- **Owning authority:** Product Owner
- **Unblock criteria:** The Product Owner confirms the checklist (including the first review on 2026-11-03 and the BLG-AI-09 baseline exception), recorded in the checklist's §5 Sign-off and in ST-15's QA evidence.
- **SLA due-by:** 2026-10-07T16:04:53Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Open
