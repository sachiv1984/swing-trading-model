Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-06

# QA Evidence — EPIC-01: Stop-Parameter Correctness & ATR Integrity

> Per-story evidence is recorded here as it arrives. The EPIC-level consolidation block and the DoQ sign-off block are added at EPIC completion (STEP 3.2.A).

## ST-01 — Production stop-parameter and open-position evidence (AC 1, AC 6)

**Source:** two read-only queries against **production**, run by the user (human, with production access, acting for the Infrastructure & Operations Owner) and pasted into the execution session on 2026-10-06. `DEL-20261006-01`, unblocked in-session.

### AC 1 — Production `settings` row

```sql
SELECT id, min_hold_days, atr_period, atr_multiplier_initial,
       atr_multiplier_trailing, updated_at
FROM settings;
```

| id | min_hold_days | atr_period | atr_multiplier_initial | atr_multiplier_trailing | updated_at |
|----|---------------|------------|------------------------|-------------------------|------------|
| `2b4d41b3-71aa-4738-80a9-a64e085f586c` | 10 | 14 | 5.00 | 2.00 | 2026-06-03 16:03:20 |

**Finding:** the row equals the `strategy_rules.md` §11 values exactly and was last written 2026-06-03. That is before any currently open position was entered (earliest 2026-09-14). For every open position's whole life, the on-load path (which read this row) and the nightly path (hard-coded 5×/2×) therefore used identical parameters. The divergence ST-01 fixes was latent in production, never live. The Settings form's wrong fallbacks (5/2/3) were never saved.

### AC 6 — Open positions and diverged stops

```sql
SELECT id, ticker, market, entry_date, entry_price, fill_price, atr,
       current_stop, initial_stop, active_atr_multiplier, stop_calculated_at
FROM positions WHERE status = 'open';
```

| Ticker | Entry date | Fill (USD) | ATR | Initial stop | Current stop | Active mult. | Stop calculated at (UTC) |
|--------|-----------|-----------|-----|--------------|--------------|--------------|--------------------------|
| MU | 2026-09-14 | 926.80 | 41.8593 | 702.85 | 1010.73 | 2.00 | 2026-10-06 02:21:33 |
| SNDK | 2026-09-15 | 1571.00 | 92.6404 | 1046.47 | 1684.33 | 2.00 | 2026-10-06 02:21:30 |
| WDC | 2026-09-18 | 438.18 | 26.6907 | 312.97 | 438.18 | 2.00 | 2026-10-06 02:21:28 |
| DELL | 2026-09-14 | 548.50 | 25.7579 | 367.47 | 548.50 | 2.00 | 2026-10-06 02:21:35 |

(IDs: MU `f9da6743-…`, SNDK `5720d511-…`, WDC `36f36920-…`, DELL `5fbfb3ab-…`, recorded in full in the session paste.)

**Finding: no open position's stored stop has diverged from §11.**
- All four are past grace and profitable (every stop is at or above the fill price), so their stops come from the profitable 2× rule. A stop set while losing would sit below entry and has since been superseded by the ratchet.
- WDC and DELL sit exactly on the §7.2 breakeven floor (stop = fill price).
- The initial stops are consistent with 5× ATR at entry.
- `active_atr_multiplier = 2.00` on every row, and the settings row has been 2.00 since June.

No AC 6 correction decision is owed, because AC 6 applies only to positions "whose stored stop has already diverged". No stop is changed.

**Note:** the `stop_calculated_at` stamps (02:21 UTC, about 2s apart) do not match the nightly job's 22:30 UTC schedule. They are most likely an on-load recompute (`GET /positions/analyze`). Either path gives the same result here, because both used 5×/2×.

**AC result:** AC 1 met (production values recorded, read-only). AC 6 met: no diverged stops, so no correction needed.
