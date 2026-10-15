// Frontend strategy constants: the display mirror of the fixed
// strategy_rules.md §11 parameters. The source is backend/strategy_parameters.py
// (ST-01, BLG-BE-138, v9.10, parameter-authority ruling (a));
// tests/test_strategy_parameter_parity.py fails if these values drift from it.
//
// ST-21 (BLG-GOV-369, v9.12): the one place page text takes strategy numbers
// from (moved here from src/lib/strategyParameters.js, Head of Specs Team
// interpretation 2026-10-13). scripts/check_strategy_copy.py (CI job
// strategy-copy) flags text in src/ that contradicts §5–§11 and literals in
// the pages ST-21 names.

export const GRACE_PERIOD_DAYS = 10;
export const ATR_PERIOD_DAYS = 14;
export const INITIAL_ATR_MULTIPLIER = 5.0;
export const PROFIT_ATR_MULTIPLIER = 2.0;
