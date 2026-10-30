export const REGIME_RISK_ON = "risk_on";
export const REGIME_RISK_OFF = "risk_off";
export const REGIME_UNKNOWN = "unknown";

const RULING_SENTENCE = "New entries in this market are blocked until it is measured.";

export function regimeStatusOf(index) {
  if (index?.regime_status) return index.regime_status;
  if (index?.is_risk_on === true) return REGIME_RISK_ON;
  if (index?.is_risk_on === false) return REGIME_RISK_OFF;
  return REGIME_UNKNOWN;
}

export function unknownRegimeExplanation(market) {
  return `${market} market regime could not be measured: index data is unavailable. ${RULING_SENTENCE}`;
}
