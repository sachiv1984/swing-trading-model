"""
Allowed exit_reason values and the strategy_rules.md §8 exit condition each
maps to (v9.13 ST-02, BLG-SPEC-186; data_model.md §3 Exit Reason Values, DS-34).

Every stored trade_history / positions exit_reason is one of EXIT_REASONS or
NULL. DS-34's CHECK constraints enforce the same list in the database, and
POST /positions/{id}/exit rejects anything else with a 400. LEGACY_ALIASES are
the old snake-case spellings DS-34 backfills; they are not accepted on write.
src/constants/exitReasons.js holds the frontend copy of the same table.
"""

SECTION_8_STOP_LOSS = "§8.1 Stop-loss trigger"
SECTION_8_RISK_OFF = "§8.2 Market risk-off override"
SECTION_8_MANUAL = "§8.3 Manual exit"

EXIT_REASONS = {
    "Stop Loss Hit": SECTION_8_STOP_LOSS,
    "Trailing Stop": SECTION_8_STOP_LOSS,
    "Risk-Off Signal": SECTION_8_RISK_OFF,
    "Manual Exit": SECTION_8_MANUAL,
    "Target Reached": SECTION_8_MANUAL,
    "Partial Profit Taking": SECTION_8_MANUAL,
}

DEFAULT_EXIT_REASON = "Manual Exit"

LEGACY_ALIASES = {
    "stop_hit": "Stop Loss Hit",
    "manual": "Manual Exit",
    "manual_exit": "Manual Exit",
    "target": "Target Reached",
    "target_reached": "Target Reached",
    "market_regime": "Risk-Off Signal",
    "risk_off": "Risk-Off Signal",
    "risk_off_signal": "Risk-Off Signal",
    "trailing_stop": "Trailing Stop",
    "partial": "Partial Profit Taking",
    "partial_profit_taking": "Partial Profit Taking",
}

INVALID_EXIT_REASON = (
    "exit_reason must be one of: " + ", ".join(EXIT_REASONS) + "."
)
