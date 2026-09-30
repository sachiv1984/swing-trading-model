**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-30
**Window:** IW-20260930-01

# Idea Intake Summary — IW-20260930-01

## Window Status: Closed

Opened: 2026-09-30T15:08:27Z
Closed: 2026-09-30T15:20:00Z

Invoked directly by the user (`run ideas` equivalent, via a session request to review open-position stop-loss trust/transparency with the Head of UX & Design and Head of Engineering charters). Mode: `standard`.

**Reduced-scope disclosure:** this window deliberately opened for 2 of the ~22 eligible agent roles (Head of UX & Design, Head of Engineering) rather than the full roster — the user's request named these two roles specifically for a joint design review. This is a disclosed scoping choice, not silent under-submission. Precedent: `IW-20260928-01` used the same reduced-roster pattern. The other ~20 roles remain eligible at the next full-roster window.

**Stale-idea horizon check (STEP -0.5):** 0 rows at `Parked-cycle-2` at window open — no advisory.

**Parked queue pre-check (§2.0):** no existing register row has `Submitter` = Head of UX & Design or Head of Engineering — no parked-idea-overlap case this window.

**Backlog scope overlap check (§2.0 step 5, mandatory):** performed as a targeted grep of `claude/backlog/backlog.md` for `stop.loss|ATR|gap.risk|trailing stop|calculated_at`. Existing hits (`BLG-FEAT-26` ATR sizing retrospective analytics, `BLG-BE-133` ATR-fallback timeout migration, orphaned-column drop note at line 3135) are adjacent but address different scope (retrospective analytics, a single call's timeout config, and dead-column removal respectively — none address duplicate live ATR implementations, missing recalculation timestamps, or stop-loss UI transparency). **0 overlaps found** — all 4 submissions are net-new.

**Codebase overlap check (§2.0 step 6, mandatory):** performed via direct code investigation (backend/utils/calculations.py, backend/utils/pricing.py, backend/services/position_service.py, backend/services/strategy_engine.py, backend/services/screener_engine.py, backend/database.py, backend/live_trading_assistant.py, backend/position_manager.py, src/pages/Positions.js, src/components/positions/TrailingStopExplainerIcon.js, docs/specs/api_contracts/position_endpoints.md). Confirmed: no `atr_calculated_at`/`stop_calculated_at` field exists anywhere; the frontend does not display ATR value, multiplier, or a calculation timestamp; 4 live ATR implementations plus 1 dead one exist with no consolidation; the explainer tooltip's "recalculated daily" claim does not match the actual on-load recompute path. **0 already-implemented topics found.**

## Submission Counts

| Agent | New Submissions | Parked Resubmitted | Total |
|-------|------------------|---------------------|-------|
| Head of UX & Design | 2 | 0 | 2 |
| Head of Engineering | 2 | 0 | 2 |
| **Total** | **4** | **0** | **4** |

## Agents Without Minimum Submissions

None — both participating agents met the 2-net-new minimum. (20 other eligible agent roles were not opened this window — see reduced-scope disclosure above; not a §2.3 shortfall, a deliberate scoping choice.)

## Ideas Available for Roadmap STEP 4

| Idea ID | Agent | Title | Recommendation | Status |
|---------|-------|-------|-----------------|--------|
| IDEA-head-of-ux-20260930-01 | Head of UX & Design | Show ATR value, stop multiplier, and recalculation source inline on every open-position stop-loss cell | Now | Submitted |
| IDEA-head-of-ux-20260930-02 | Head of UX & Design | Replace the static "ATR recalculated daily" explainer tooltip with copy sourced from the position's actual last-recalculation event | Now | Submitted |
| IDEA-head-of-engineering-20260930-01 | Head of Engineering | Consolidate the 4 duplicate ATR calculation implementations into one canonical source; remove the dead `position_manager.py` script | Now | Submitted |
| IDEA-head-of-engineering-20260930-02 | Head of Engineering | Persist stop/ATR recalculation timestamp, expose `atr`/multiplier/timestamp on `GET /positions`, and reconcile `strategy_rules.md` §7.1 "recalculated daily" wording against actual on-load recompute cadence | Now | Submitted |

## Parked Ideas Carried Forward (Not Resubmitted)

None.

## Idea Details (full template fields, recorded here per this window's small size rather than duplicated into per-idea files — same convention as `IW-20260928-01`)

### IDEA-head-of-ux-20260930-01 — Show ATR value, stop multiplier, and recalculation source inline on every open-position stop-loss cell

- **Problem Statement:** The user reported loss of confidence in the displayed stop-loss for open positions: they cannot see the ATR value the system used, cannot manually verify the resulting stop, and cannot tell how or why it was calculated. The stop-loss cell (`src/pages/Positions.js`, `PositionCard.js`) shows only the final Init/Trailing prices — no ATR, no multiplier, no source event.
- **Strategic Alignment:** §5 (Initial stop calculation) — stated purpose "to make downside risk visible... to reduce reactive decision-making." A stop the user cannot independently verify does not serve that purpose; it produces the opposite of the intended visibility.
- **Proposed Solution:** Add ATR value, the active multiplier (2× profitable / 5× losing, per §7.2), and a recalculation source line to the stop-loss cell/tooltip, so the displayed stop is checkable against the same formula documented in §5/§7.2 without leaving the page.
- **Expected Value:** Removes the single reported driver of the 2026-09-30 loss-of-confidence report. Verification time for a displayed stop goes from "not possible without backend/DB access" to a single on-screen glance.
- **Effort Estimate:** Medium (1–3 weeks). Constraint: depends on `atr`/multiplier/timestamp being available on `GET /positions` — see `IDEA-head-of-engineering-20260930-02`.
- **Reversibility:** Fully reversible — UI-only, no data model impact.
- **What Would You Stop?** No view — leave to debate.
- **Submitter Recommendation:** Now — directly answers a live user trust issue.

### IDEA-head-of-ux-20260930-02 — Replace the static "ATR recalculated daily" explainer tooltip with copy sourced from the position's actual last-recalculation event

- **Problem Statement:** `TrailingStopExplainerIcon.js`'s tooltip states "ATR is recalculated daily (14-day period)." In the live system, ATR/stop is recalculated on every `GET /positions` page load (`position_service.py::get_positions_with_prices`) as well as by the nightly job — not only daily. The copy is a hardcoded claim, not a reflection of what actually happened for the row it sits next to, and it directly matches the wording in `strategy_rules.md` §7.1 ("ATR is recalculated daily") — see `IDEA-head-of-engineering-20260930-02` for the canonical-spec-vs-implementation reconciliation this implies.
- **Strategic Alignment:** §3 (Human-in-the-loop execution model) — "the system provides decision support only," which depends on the user trusting what's shown. Static copy that contradicts live behaviour undermines that trust independent of whether the underlying number is correct.
- **Proposed Solution:** Source the explainer copy from the row's actual last-recalculation event/timestamp (e.g. "Recalculated when you opened this page at 09:14" / "Recalculated by the nightly job at 22:30 UTC") instead of a hardcoded cadence claim.
- **Expected Value:** Eliminates a currently-false in-product claim; closes a specific, named trust gap distinct from any new feature.
- **Effort Estimate:** Small (days to 1 week) for the copy/behaviour fix itself; full "live event" sourcing depends on the timestamp field in `IDEA-head-of-engineering-20260930-02`. A first increment (removing the false "daily" claim) can ship independently.
- **Reversibility:** Fully reversible.
- **What Would You Stop?** No view — leave to debate.
- **Submitter Recommendation:** Now.

### IDEA-head-of-engineering-20260930-01 — Consolidate the 4 duplicate ATR calculation implementations into one canonical source; remove the dead `position_manager.py` script

- **Problem Statement:** ATR is independently implemented in at least 4 places (`backend/utils/pricing.py::calculate_atr`, `backend/services/strategy_engine.py::compute_atr`, `backend/services/screener_engine.py::compute_atr`, `backend/database.py::compute_atr_simple`), plus a 5th, unwired dead copy in `backend/position_manager.py` that is never imported by `main.py` or any live service. If any of these diverge, exposing a raw ATR value in the UI (per `IDEA-head-of-ux-20260930-01`) would surface that inconsistency directly to the user rather than resolving it.
- **Strategic Alignment:** §12.3 (Parameter governance) — requires strategy parameters "applied consistently across backtests, live logic, and documentation." §12.3's own text already carries one documented, tested exception for `position_manager.py`'s backtest path (the breakeven-floor divergence, v9.5); a second, undocumented divergence source (independent ATR math) in the same file is a materially different risk from that already-accepted exception.
- **Proposed Solution:** Designate one canonical ATR implementation (the live-path function backing `calculate_trailing_stop`'s callers) and have the other live call sites use it. Remove the dead `position_manager.py` copy, or explicitly document why it's exempt if it's intentionally kept as a standalone backtest tool.
- **Expected Value:** Reduces ATR implementation count from 4 (5 including dead code) to 1 canonical source — a concrete, checkable before/after count. Removes the precondition risk blocking `IDEA-head-of-ux-20260930-01`.
- **Effort Estimate:** Medium (1–3 weeks) — touches 4 call sites and their tests.
- **Reversibility:** Mostly reversible — minor rework required if consolidation surfaces a subtle behavioural difference between implementations.
- **What Would You Stop?** No view — leave to debate.
- **Submitter Recommendation:** Now — prerequisite for the UX transparency work above.

### IDEA-head-of-engineering-20260930-02 — Persist stop/ATR recalculation timestamp, expose `atr`/multiplier/timestamp on `GET /positions`, and reconcile `strategy_rules.md` §7.1 wording against actual recompute cadence

- **Problem Statement:** No `atr_calculated_at`/`stop_calculated_at` column or field exists anywhere in the system (confirmed absent from `positions` table and all response contracts). The user expects a refresh on login to refresh the stop, and a nightly process to cover days they don't log in — both already exist in the code (`get_positions_with_prices()` recalculates on every `GET /positions`; `.github/workflows/nightly-stop-update.yml` provides the nightly backstop) but neither is visible or timestamped anywhere the user can see. Separately, `strategy_rules.md` §7.1 states "ATR is recalculated daily," while `position_endpoints.md` line 147 documents the stop as "always present and non-zero after the first nightly update" — both describe a nightly-only cadence that doesn't match the live on-load + nightly behaviour.
- **Strategic Alignment:** §5 purpose ("to make downside risk visible") and §12.3 (documentation must match live logic). The canonical spec and the API contract currently disagree with the implementation on cadence — this is a documentation/implementation consistency gap the Head of Specs Team's canonical-conformance role exists to resolve, not something engineering should silently paper over in the API layer.
- **Proposed Solution:** Add a `stop_calculated_at` (and reuse for `atr`) timestamp column, written alongside `current_stop`/`atr` in both the on-load recompute path and the nightly job. Expose `atr`, the active multiplier, and this timestamp on `GET /positions`. Before finalising, raise a spec query (per Head of Engineering charter §"Mid-Implementation Spec Queries") to the Strategy Rules & System Intent Owner: either §7.1/the API contract's wording is updated to describe the actual on-load + nightly cadence, or the implementation is deliberately constrained to nightly-only recompute to match the documented "daily" cadence — this is a spec decision, not an engineering judgment call.
- **Expected Value:** Closes a documented spec/implementation cadence mismatch; supplies the data fields both UX submissions above depend on.
- **Effort Estimate:** Medium (1–3 weeks) — schema migration + endpoint change + spec query round-trip.
- **Reversibility:** Mostly reversible — additive schema column, easy to drop if abandoned.
- **What Would You Stop?** No view — leave to debate.
- **Submitter Recommendation:** Now.

## Notes

No `[FIELD REQUIRED]` flags — all 4 submissions passed the Submission Quality Check (specific `strategy_rules.md` citation, specific expected-value metric, all required fields non-empty) on first generation.

**Out-of-scope finding surfaced during investigation, not filed as an idea this window:** `strategy_rules.md` §13.3 states "Gap risk monitoring is excluded by design... would increase noise without enabling a decision," yet `backend/services/gap_risk_service.py` (BLG-FEAT-65, v6.9) and its `GapRiskBadge`/`GapRiskCardBadge` UI are live and shipped, and the feature does not appear in the §13.5 in-scope boundary-clearance roster table. This is a live-vs-canonical-spec boundary question for the Strategy Rules & System Intent Owner, unrelated to stop-loss/ATR transparency and outside this window's 2-role scope — flagged directly to the user in-session rather than fabricated into a submission under a role not opened this window.

```yaml
// ARTEFACT_STATUS
{
  "file": "window_summary_IW-20260930-01.md",
  "window_id": "IW-20260930-01",
  "filed_utc": "2026-09-30T15:20:00Z",
  "submission_count": 4,
  "agents_participating": 2,
  "status": "Complete"
}
```
