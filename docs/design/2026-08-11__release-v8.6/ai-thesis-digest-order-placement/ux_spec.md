**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 4)
**Status:** Approved
**Last Updated:** 2026-08-11
**Cycle:** 2026-08-11__release-v8.6
**Story:** ST-02 (BLG-FEAT-56, EPIC-01)

# UX Spec — AI-Assisted Setup Thesis Digest at Order Placement (TradeEntry)

## 1. Problem

At the order-placement step (`TradeEntry.js`), an operator executing a "Start Trade from Plan" flow (`trade_plan.md` §10, `BLG-FE-109`, v7.3) sees the plan's linked context block (thesis first 120 chars, entry zone, stop, R-target — `positions.md` line 254) only *after* the position is created, on the resulting position card. Nothing at the order-placement moment itself re-surfaces the plan's reasoning or its risk factors as a pre-commit check. Classified Design Required per `design_gate_prompt.md` §6 ("new UI element", "changed interaction flow").

**§13 pre-check (per STEP 1, mandatory for AI-calling proposals):** this reuses the existing, already-cleared Claude thesis generation surface — `docs/specs/api_contracts/ai_thesis_generation.md` §13 compliance note (successor to `gemini_thesis_generation.md`, itself already on the `strategy_rules.md` §13.5 re-attestation roster). Covered; no fresh §13 review required for this item.

## 2. Decision

**No new AI call at order placement.** The digest surfaces the plan's **already-generated** content — the same Setup Thesis and Early Exit Conditions fields captured via the existing "Improve with AI" flow at plan-creation time (`trade_plan.md` §5b) — rather than triggering a second live inference call at the order-placement moment. This is a deliberate design choice, not a scope-reduction:

- Avoids a duplicate paid Claude Haiku 4.5 call for content that, in the common case, hasn't materially changed between plan creation and order placement (minutes-to-days later, same plan).
- Keeps the feature within §13's existing "advisory text only, operator-reviewed, no automated trade decision" boundary with no new inference surface to re-clear.
- Matches the AC's literal wording — "using the existing Claude thesis generation service" is satisfied by displaying that service's already-produced output, not by re-invoking it.

**Placement:** A new collapsible **"Setup Thesis Digest"** panel in `TradeEntry.js`, rendered directly below the existing "Linked to trade plan" indicator (`trade_plan.md` §10, non-editable badge shown when `trade_plan_prefill`/`trade_plan_id` is present) and above the order form fields (ticker/shares/entry price). Placement follows the "context before commitment" precedent already set by the Signal Context panel (§5a, `trade_plan.md`) and the Regime History panel (v8.5, `screener_results.md` — page-level context shown before the user acts).

**Visibility rule (mirrors §10's existing "hidden entirely when absent" convention):** the panel renders only when `trade_plan_id` is present **and** the linked plan has non-empty `setup_thesis` and/or `early_exit_conditions` content. No plan linked, or a linked plan with no thesis content yet (never ran "Improve with AI" or manual template fill) → panel does not render at all. This matches the existing optional-link-selector precedent exactly (§10.2 of `trade_plan.md`).

**Contents:**
- Panel header: **"Setup Thesis Digest"** with a collapse/expand chevron (default: expanded), plus the existing violet **"AI draft"** badge (`Sparkles` icon, `trade_plan.md` §5b convention) shown only when the source plan's `isAiDraft` flag was `true` at generation time — carrying the same "AI-originated content" signal forward from the plan into this new surface, not inventing a new one.
- **Setup Thesis** — the plan's `setup_thesis` field, truncated to 2–3 sentences if longer (same length convention as `positions.md`'s existing 120-char thesis excerpt, loosened slightly to sentence boundaries rather than a hard character cut, since this is the primary read here rather than a secondary card detail).
- **Key Risk Factors** — a short bulleted list, synthesised from the plan's `early_exit_conditions` and `confirmation_criteria` fields (the two structured, risk-relevant fields already captured on every plan — no new backend field). Each condition/criterion renders as one bullet, verbatim, capped at 4 bullets total (2 from each field, prioritising non-empty ones) to keep the panel compact at a moment the operator is trying to complete an order, not read a document.
- No edit affordance — this is a read-only pre-commit check, distinct from the editable plan-creation form (§5b). A **"View full plan →"** text link (reusing the existing `positions.md` link-styling convention) navigates to the plan's detail view for anyone who wants the complete thesis/rationale.

**States:**
- **Rendered** (plan linked, thesis content present): panel as described above, default-expanded.
- **Collapsed** (user-toggled): header + chevron only, persisted per-session only (not `localStorage` — this is a single order-placement visit, not a standing preference like the Behavioural Drift panel's collapse state).
- **Not rendered**: no plan linked, or plan linked but no thesis content — no placeholder, no empty-state card (mirrors §10.2's existing convention for the optional link selector).

## 3. Rationale

- Reusing already-generated content instead of a fresh call keeps this squarely inside the existing, already-cleared §13 boundary and avoids a second cost-tracked inference call per order for content unlikely to have changed.
- Deriving "Key Risk Factors" from `early_exit_conditions`/`confirmation_criteria` (already-structured plan fields) rather than inventing a new stored field or a new free-text AI output keeps the data model unchanged — no backend schema change needed for this story.
- Collapse-not-persisted (vs. Behavioural Drift's `localStorage`-persisted collapse) reflects that this panel is seen once per order, not a standing dashboard fixture revisited across sessions.
- Read-only, with a link out to the full plan, keeps the editable surface singular (the plan-creation form) — no risk of two divergent copies of the thesis being edited independently.

## 4. Data source and edge cases

- Sourced entirely from the already-fetched trade plan record (same `GET /trade-plans/{plan_id}` call §10 already makes for the prefill) — no new endpoint.
- Plan has `setup_thesis` but empty `early_exit_conditions`/`confirmation_criteria`: Key Risk Factors section is omitted (heading not shown), thesis paragraph still renders.
- Plan has thesis content that was hand-written (not AI-generated, `isAiDraft` was never `true` or was cleared by a later manual edit per §5b's existing rule): panel still renders, simply without the "AI draft" badge — the digest is not exclusively an AI feature, it is a pre-commit reasoning check regardless of origin.

## 5. Scope boundary

`TradeEntry.js` "Start Trade from Plan" flow only. Does not change the plan-creation form (§5b, unchanged), the plan detail/list views (`trade_plan.md` §1–§10, unchanged beyond this new panel), or the manual-entry "Link to trade plan (optional)" path's existing behaviour (§10.2) beyond making this panel available once a plan becomes linked via either path. No new AI endpoint, no new stored field.

## §13 check

Advisory text only, sourced from an already-cleared generation path (`ai_thesis_generation.md` §13 compliance note); operator-reviewed, no automated trade decision; does not gate, block, or modify order submission. Consistent with §13.1/§13.2.
