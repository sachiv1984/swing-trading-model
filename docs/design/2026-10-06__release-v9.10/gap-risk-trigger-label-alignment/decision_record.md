**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-06__release-v9.10
**Story:** ST-14 (EPIC-03, BLG-BE-136); depends on ST-13 (BLG-GOV-365) ruling

# Decision Record — Gap Risk Reason Labels Match the Ruled Trigger Timing

## 1. Problem

Code, labels and specs disagree on when the GAP RISK flag fires:

- **Earnings trigger.** `gap_risk_service.py` flags `earnings` when `0 <= days_until_earnings <= 1` (calendar days). Viewed on a Friday, Monday earnings are 3 days away and are **not** flagged. The label "Earnings before next session" and `positions.md`/`ux_spec.md` §5 promise exactly that case.
- **Weekend trigger.** `weekend_hold` fires for **every** open position on every Friday, regardless of ticker or event. That conflicts with §13 Binding Condition 6. ST-14 must either remove the trigger or record a signed alternative disposition.
- **Market and day-0 timing.** ST-13 rules which markets the earnings trigger covers and how day-0 is handled.

## 2. Decision

### 2.1 Earnings label

| `reasons` value | Label (both views, `GAP_RISK_REASON_LABELS`) |
|-----------------|---------------------------------------------|
| `earnings` | **"Earnings due by next trading session"** |

- "By next trading session" covers both day-0 (earnings today, reported after the close) and earnings before the next session opens. The Friday-to-Monday case is explicitly included, matching ST-14 AC 2.
- If ST-13 excludes day-0, the label text stays the same: it still describes "the next trading session" accurately. The tooltip and spec must then state the ruled offsets.
- If ST-13 excludes a market (e.g. UK tickers), no label change is needed. The badge simply does not appear for those positions, and the spec states the market scope.

### 2.2 Weekend label: one branch per ST-14 disposition

| ST-14 outcome | UI |
|---------------|----|
| **Trigger removed** (default expectation per Binding Condition 6) | `weekend_hold` is removed from `GAP_RISK_REASON_LABELS` in both `Positions.js` and `PositionCard.js`. The `reasons` enum in `position_endpoints.md` and `openapi.yaml` shrinks in the same commit. No replacement label. |
| **Retained under a signed alternative disposition** | The label becomes **"Held over the weekend (applies to every position on Fridays)"**. The badge must not imply a ticker-specific risk when the trigger is uniform. |

### 2.3 Tooltip and accessibility

The tooltip structure is unchanged: "Gap Risk — {TICKER}", then the reason labels joined with " + ", then the average gap or "insufficient history". The `aria-label` pattern is unchanged; it inherits the new label text.

### 2.4 Unchanged

The badge colour (`#D97706`), the "GAP RISK" text, stacking rules, Grid View placement and clearing behaviour are unchanged.

## 3. §13 Compliance

Display-only. It surfaces a calendar event and a historical statistic, and still predicts neither direction nor magnitude. Binding Conditions 1–8 are re-confirmed by the Strategy Rules & System Intent Owner under ST-14 AC 6, not at this gate.

## 4. Frontend Spec Impact

- `positions.md` v2.11, §Gap Risk Badge: trigger description and reason-label table, with the weekend row marked as conditional on the ST-14 disposition.
- **Outside this gate's write scope:** `docs/design/2026-07-10__release-v6.9/gap-risk-flag/ux_spec.md` §5 (a prior cycle's design artefact) must be brought into agreement in ST-14's own commit, as ST-14 AC 3 already requires.

## 5. Testability (CLAUDE.md §2)

- **Playwright:** a mocked `gap_risk.reasons = ["earnings"]` renders the new label in both views. If the weekend trigger is removed, nothing renders a weekend label.
- **Unit tests:** `tests/test_gap_risk.py` covers a Friday view with Monday earnings, the day-0 case and a UK position (ST-13/ST-14).

## 6. Approval

Head of UX & Design: confirmed, 2026-10-06.
Product Owner: confirmed, 2026-10-06. The design is disposition-conditional; the choice of outcome stays with ST-14 and the Strategy Rules & System Intent Owner.
