// Display mirror of the fixed strategy_rules.md §11 stop parameters (ST-01,
// BLG-BE-138, v9.10, parameter-authority ruling (a)). The source is
// backend/utils/strategy_parameters.py. tests/test_strategy_parameter_parity.py
// fails if these values drift from it.

export const GRACE_PERIOD_DAYS = 10;
export const ATR_PERIOD_DAYS = 14;
export const INITIAL_ATR_MULTIPLIER = 5.0;
export const PROFIT_ATR_MULTIPLIER = 2.0;
