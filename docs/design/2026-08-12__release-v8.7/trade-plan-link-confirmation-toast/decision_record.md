**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-08-12__release-v8.7
**Story:** ST-02 (EPIC-01, BLG-FE-158)

# Decision Record — Post-Submission Trade-Plan Link Confirmation

## 1. Problem

`POST /portfolio/position` now returns `trade_plan_linked` (boolean) and `trade_plan_id` (UUID | null) in its response (`portfolio_endpoints.md`, `ST-03`/`BLG-BE-91`, v8.6), but `TradeEntry.js` does not yet surface this outcome to the user. The pre-submission "Linked to trade plan" indicator (§10.2) only covers the explicit hand-off/manual-link paths (§10.1–§10.3); it does not cover the best-effort ticker/market auto-link (`BLG-BE-46`), whose outcome is only knowable from the response, not beforehand. `ST-02` closes this gap: the user should learn the actual linkage outcome for every submission, not just the ones where linkage was already visible pre-submit.

## 2. Decision

On a successful `POST /portfolio/position` response, show a `sonner` toast (per `design_system.md`'s existing Toast pattern) reporting the linkage outcome, in addition to (not replacing) any existing position-created confirmation:

- **`trade_plan_linked: true`** — success-styled toast: **"Linked to trade plan for {ticker}."** `{ticker}` is the already-known submitted ticker (client-side, no extra fetch needed) — the response does not return a plan title, and fetching one solely for this toast is out of scope.
- **`trade_plan_linked: false`** — neutral-styled toast (not error/warning — this is an expected, non-failure outcome for a manually-entered position with no matching plan): **"No matching plan found — logged unlinked."**

**Why a toast, not a `StandingAlert`:** per `design_system.md`'s Toast vs `StandingAlert` distinction, this is a one-time, non-actionable, informational outcome of a just-completed action — it does not require sustained user awareness until acknowledged, and there is nothing for the user to act on (the position is already created either way). Default `sonner` duration (no override).

**Sequencing:** the link-outcome toast fires immediately alongside the existing success handling for the position-creation response — both may be visible simultaneously (`sonner`'s stacking behaviour handles this natively, same precedent as any other multi-toast flow in the app).

## 3. §13 Compliance

Display-only surfacing of an already-computed, already-persisted linkage outcome. No new decision logic, no automated action, no gating of position creation (unaffected either way — `trade_plan_linked: false` is not an error state).

## 4. Frontend Spec Impact

New subsection `trade_plan.md` §10.6, immediately following §10.5 (Setup Thesis Digest) — the linkage-outcome confirmation is the last step in the "Start Trade from Plan" / auto-link flow's narrative, after the digest (pre-submit) and before the existing post-submit navigation behaviour.

## 5. Approval

Head of UX & Design: confirmed, 2026-08-12.
Product Owner: confirmed, 2026-08-12.
