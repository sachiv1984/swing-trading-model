Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-06

# QA Evidence — EPIC-01: Stop-Parameter Correctness & ATR Integrity


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

---

## Consolidation Block

**EPIC:** EPIC-01 — Stop-Parameter Correctness & ATR Integrity
**Cycle:** 2026-10-06__release-v9.10
**Sprint goal:** Make every live stop come from one §11 parameter source, and show the ATR, multiplier, recalculation source and already-known exit conditions behind each position (BLG-BE-138, BLG-FE-193, BLG-FE-198), while clearing v9.10's lifecycle/gap-risk rulings and AI-governance, ops and QA hygiene items.
**Test scenarios used:** `tests/test_strategy_parameter_parity.py`, `tests/test_live_exit_decision.py`, `tests/test_atr_provenance.py`, `tests/test_strategy_version_registry.py`, `tests/test_strategy_version_at_entry.py`, `tests/e2e/settings-strategy-parameters-fixed.spec.js`

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | `strategy_rules.md` §11; `backend/utils/strategy_parameters.py`; `settings.md` §Strategy Parameter Presentation; `data_model.md` DS-26 | One fixed §11 source read by every live stop path; Settings read-only; Trade Entry 5×; `stop_calculation_source` (DS-26, live) | 6 ACs: production read recorded (AC 1); ruling (a) by the user as Strategy Rules & System Intent Owner (AC 2); one source (AC 3); Settings/Trade Entry values equal §11 (AC 4); parity test (AC 5); no diverged stops, so no correction owed (AC 6) | Pass | None |
| ST-02 | `data_model.md` DS-25; `position_endpoints.md` GET /positions | `positions.atr_source` (fetched/user/fallback, live); missing ATR on recompute keeps the stop and flags `atr_unavailable` instead of moving it to entry | All 4 ACs met; both fallbacks tested | Pass | None |
| ST-03 | `position_endpoints.md` v2.8.1; `settings_endpoints.md` v1.4.0 | Losing stop documented as current price − 5×ATR; analyze side effects stated; settings multiplier fields documented as having no effect | All 4 ACs met; documentation only | Pass | None |
| ST-04 | `strategy_rules.md` §5–§8; traceability matrix | 67 tests calling `should_exit_position` directly; 9 matrix rows moved to Asserted (51.0% → 69.4%) | All 4 ACs met. C7.1-02 stays Partial for a behaviour reason (on-load path reuses stored ATR), noted in the matrix | Pass with notes | None |
| ST-05 | `data_model.md` DS-11; `strategy_version_comparison_contract.md` Note 2 | Behaviour-only registry rule by the user's ruling; `DOCUMENTATION_ONLY_VERSIONS`; test derived from the Change Log replaces `len == 5` | All 4 ACs met. AC 4 not triggered, because ST-01's ruling added no Change Log row | Pass | None |

**QA test coverage**
- **Scenarios run:** full backend pytest suite, 2160 passed / 14 skipped on the EPIC-01 branch. Playwright `settings-strategy-parameters-fixed.spec.js` SC-SPF-01..05 passed locally (chromium), along with the Settings axe scan and the Trade Entry linkage spec. CI has not yet run on this branch; it runs on PR open.
- **Mutation checks:** a hard-coded nightly multiplier copy fails `test_both_paths_follow_a_changed_source`. An unclassified Change Log row (1.15 probe) fails the registry test.
- **Regression areas:** stop recompute (on-load and nightly), entry stop, exit decision, grace countdown, compliance, alerts grace warning, Settings save payload, Trade Entry suggested stop, `strategy_version_at_entry` stamping.
- **Frontend testing gate (CLAUDE.md §2):**
  - Settings read-only values, caption and save payload: Playwright SC-SPF-01..04.
  - Trade Entry suggested stop: SC-SPF-05.
  - No observable AC is "code review only".
  - EPIC-01 changes `src/pages/Settings.js` and `src/pages/TradeEntry.js`, so the autonomous sign-off class does not apply (Criterion 3).
- **Live environment:** DS-25 and DS-26 applied and verified on staging and production (`data_model.md` Live Confirmation). Production settings and open positions recorded under ST-01 above.
- **Story-level authority sign-offs (BLG-GOV-14):**
  - Strategy Rules & System Intent Owner rulings for ST-01 (a) and ST-05 (behaviour-only): direct user rulings, 2026-10-06.
  - Data Model & Domain Schema Owner: DS-25/DS-26 applied and verified by the user.
- **Known deviations filed:** None.

## Standard Sign-Off Block

- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [ ] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object
- Signed off by: _pending (Director of Quality)_
- Date:
- Comments:
