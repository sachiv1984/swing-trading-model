Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-06

# Execution Escalations — 2026-10-06__release-v9.10

> EPIC-04 branch copy. `ESC-EXEC-20261006-01`/`-02` (EPIC-01) and `-03`/`-04` (EPIC-03) live on their own branches; union the files at merge (CLAUDE.md §8).

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
