**Owner:** Strategy Rules & System Intent Owner
**Class:** Proof of Gate (Class 8)
**Status:** Active
**Gate ID:** POG-20260304-01
**Issued:** 2026-03-04
**Cycle:** 2026-03-04__item-3.4
**Initiative:** Signal Exposure Enhancement (4.3)
**Gate cleared:** SRB review (v1.7 EPIC-02) confirmed that exposing `top_n` and `lookback_days` as user-facing controls does not violate §13.2 of strategy_rules.md — these parameters are display/query-scope controls, not strategy execution parameters.
**Versioned document referenced:** `claude/strategy/strategy_rules.md` v1.3
**Decision:** Signal Parameter Exposure (4.3) is COMPLIANT with §13.2. Feature may proceed to pre-alignment with the following scope constraint: `top_n` and `lookback_days` are the ONLY parameters cleared. Any future change that allows users to modify signal weights, scoring logic, or ranking methodology requires a new §13 review before that change may enter pre-alignment. This PoG does NOT authorise exposure of any parameters beyond the two named above.
**Confirmed by:** Strategy Rules & System Intent Owner (delegated authority; exercised during v1.7 SRB, EPIC-02 TASK-01 through TASK-05, 2026-03-02)
**Checksum note:** strategy_rules.md v1.3 as of 2026-03-04 — confirmed unchanged since SRB review on 2026-03-02. If strategy_rules.md is incremented after this date, this PoG is automatically stale and must be re-issued.

---

*This document is immutable once issued. Body content may not be edited. Status field only may change to Superseded.*
