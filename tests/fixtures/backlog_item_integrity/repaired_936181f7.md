<!-- ST-39 fixture: BLG-SPEC-190 and BLG-BE-157 exactly as they read in claude/backlog/backlog.md at 936181f7 -->

## 9. Fixture

### BLG-SPEC-190 — Positions data dictionary states `entry_price` is native currency; the code stores GBP
**Priority:** P3 (Low)
**Type:** Spec Debt
**Owner:** Data Model & Domain Schema Owner
**Source:** ST-30 (BLG-SPEC-173), EPIC-05, cycle `2026-10-08__release-v9.11` — 2026-10-08
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`add_position()` stores `positions.entry_price` as the entry price **in GBP** (native ÷ `fx_rate` for US positions), and stores the native entry price in `fill_price`; the user's broker fill goes in `user_fill_price`. `data_model.md` §2 was corrected at v2.55 (ST-30). `docs/specs/data_model_positions_dictionary.md` (the canonical field dictionary) still says `entry_price` is native and `fill_price` is the actual execution fill, and its §derivation formulas (`total_cost`, `pnl`) use `entry_price` as if it were native.

**Scope**
- Correct the dictionary's `entry_price`, `fill_price` and `user_fill_price` rows and the derivation formulas to match the code
- Check other specs that describe `positions.entry_price` as native

**Acceptance Criteria**
- The dictionary and `data_model.md` §2 agree with `add_position()` for every price field
- No spec describes `positions.entry_price` as native currency for US positions

---
### BLG-BE-157 — Batch signal sizing gives a zero-ATR signal a 5% allocation
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Correctness
**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Source:** ST-39 (BLG-QA-199), EPIC-06, cycle `2026-10-08__release-v9.11` — found while writing mutation-testing cases for `size_batch_inv_vol` — 2026-10-08
**Effort:** S (~0.5d)
**Provisional-Target:** TBD

**Problem**
`sizing_service.size_batch_inv_vol()` (used by `signal_service.py` for every new signal's suggested shares) gives a signal with `atr_value` 0 or missing an inverse-ATR weight of 0, then clamps every weight to the 5% minimum, so that signal still receives 5% of available cash (before renormalisation) and a non-zero share count. Its own docstring says "Signals with atr_value == 0 get 0 shares". Reproduced 2026-10-08: signals with ATR 1, 0 and 2 and £10,000 cash gave the zero-ATR signal a weight of 0.111 and 22 shares. `tests/test_signal_sizing.py::test_zero_atr_produces_zero_shares` passes only because it uses a batch where every ATR is 0, which takes the early-exit branch; the mixed case is untested.

**Scope**
- Exclude zero/missing-ATR signals from the clamp and renormalisation, and give them 0 shares with a reason
- Add a mixed-batch test (some zero-ATR, some valid)

**Acceptance Criteria**
- In a mixed batch, a zero-ATR signal gets `suggested_shares` 0, `inv_vol_weight` 0 and a reason, and the other signals' weights sum to 1.0
- The existing all-zero and capping tests still pass

---
