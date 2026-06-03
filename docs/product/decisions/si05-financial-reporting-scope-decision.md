**Owner:** Head of Specs Team
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-06-21
**Cycle:** 2026-06-21__release-v5.1
**Story:** ST-02 (EPIC-01, v5.1)
**Backlog ref:** BLG-SPEC-45
**Depends on:** BLG-GOV-86 — SI-05 Telegram message format spec (shipped v5.0)

---

# SI-05 Phase 1 — Financial Reporting Scope Decision

## Question

Does BLG-GOV-86 (SI-05 Phase 1 Telegram Message Format Specification, `docs/product/decisions/si05-telegram-message-format-spec.md`) address financial performance reporting scope? If not, is weekly financial summary (P&L, portfolio returns) in or out of scope for Phase 1?

## Review Summary

BLG-GOV-86 was reviewed in full for this decision. The specification defines the SI-05 weekly digest as a **Strategy Integrity** digest, not a financial performance digest. It specifies four data fields:

| Field | Source | Nature |
|-------|--------|--------|
| `pass_rate` | `GET /analytics/arc5-compliance` → `validation_pass_rate_by_rule` | Pre-entry validation compliance |
| `red_flag_count` | `events_per_week × 7` | Red flag event frequency |
| `override_rate` | `override_rate × 100` | Override discipline metric |
| `top_rule_breach` | `top_rule_breach` | Most frequently failing rule |

None of these are financial performance metrics (P&L, realised/unrealised returns, drawdown, win rate). BLG-GOV-86 does not address financial performance reporting.

## Scope Decision

**Financial performance reporting (P&L, portfolio returns, drawdown, win rate) is OUT OF SCOPE for SI-05 Phase 1.**

Rationale:
1. SI-05 is the "Strategy Integrity" arc — it covers behavioural discipline and pre-entry rule compliance, not financial outcomes.
2. Financial performance is already surfaced in the v2.4 weekly digest (`GET /digest/weekly`) which includes `realised_pnl_7d`, `unrealised_pnl_delta_7d`, and `compliance_score_*`.
3. SI-05 Phase 1 extends the v2.4 digest with a **new strategy integrity section** — it does not replace or expand the financial metrics section.
4. Including financial performance in SI-05 would duplicate v2.4 content and is not consistent with the SI-05 arc intent (strategy rule compliance, not financial reporting).

## Supplementary Spec

No supplementary spec required. The financial reporting scope exclusion is documented here. Phase 2 or later SI-05 phases may revisit this decision if there is a product requirement to add financial metrics to the strategy integrity digest.

## BLG-SPEC-45 Disposition

**COMPLETE** — Financial reporting scope question answered: OUT OF SCOPE for Phase 1. No supplementary spec required.

## Sign-Off

**Financial Reporting & Records Owner:** Financial Reporting & Records Owner — 2026-06-21  
Confirmed: SI-05 Phase 1 scope correctly excludes financial performance reporting. The v2.4 weekly digest already covers financial metrics; SI-05 supplements with strategy discipline data. Decision is consistent with the SI-05 arc intent and does not create a gap in financial reporting.
