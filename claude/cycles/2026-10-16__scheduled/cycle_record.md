**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Complete
**Last Updated:** 2026-10-16

---

# Cycle Record — Roadmap Rebalance `2026-10-16__scheduled`

Working content for STEPs 2–8.5 (`roadmap_prompt.md` v9.35, STEP 0.C). Tier: **Standard**.

## STEP 2 — Re-Validation

**Active initiatives:** 0, the 18th consecutive cycle with none (unchanged since 2026-04-03). No 🔥/⚠/❌ classifications are required.

**Strategy Proximity / CPS (2.1–2.2):** CPS = N/A (no active initiatives). The prior cycle's CPS was also N/A, so delta = N/A. No Strategy Drift Alert.

### Horizon Review

- **Now:** empty at run start. The v9.12 section was retired on 2026-10-15 after its one item shipped. STEP 8 adds a `v9.13` section (see STEP 8.1).
- **Next / Later / Gated:** no movement. Every Later/Gated pre-condition was re-checked against current data. **SI-02:** `**Last formally confirmed:**` cited unchanged (NOT MET); no live check was attempted, because no production credential is available in this checkout and the sandbox `DATABASE_URL` is staging and was not queried. **PO-02:** "6+ months of AI-summarised journal entries", projected ~2026-10-20 at the last reading; not yet clear on the run date. **PO-04 / SI-02 trade-plan gates:** unchanged.
- **Operating mode:** backlog-driven delivery with empty Arc horizons (§2.3, v9.20 note). This is expected, not a process failure.

## STEP 2.4 — Product Value Ratio

| Release | U | G | D | P | Total |
|---------|---|---|---|---|-------|
| v9.8 | 2 | 10 | 27 | 0 | 39 |
| v9.9 | 2 | 9 | 24 | 0 | 35 |
| v9.10 | 8 | 3 | 10 | 0 | 21 |
| v9.11 | 10 | 5 | 26 | 2 | 43 |
| v9.12 | 16 | 6 | 26 | 0 | 48 |
| **Total** | **38** | **33** | **113** | **2** | **186** |

Tags were read from `docs/product/changelog.md`; `scripts/compute_rebalance_diagnostics.py` gives the same totals.

**user_value_ratio = 0.204 — 🔴 Product Value Alert, 8th consecutive reading, improving** (from 0.161). The sustained-Advisory clause does not apply, since the ratio is in the Alert tier.

**Effort-weighted reading: 0.361** (U 50.42 effort-days of 139.68), coverage **186/186**, no exclusions. Computed by hand per STEP 2.4: the window v9.8–v9.12 is not in `scripts/compute_effort_weighted_pvr.py`'s `WINDOWS` map, so that script was not run or edited. The same parsing helpers and the Appendix F normalisation table were called from a scratch script. Diagnostic only; no tier.

**Challenger (Product Velocity Concern):** ratio 0.204 < 0.50. Of the window's 38 U-stories, 26 came from v9.11 and v9.12, the two releases that honoured pull-forwards. Proposed pull-forward: the user-facing defects found this window, starting with the broken Monitor exit (`BLG-FE-226`).

**PO written response — Modify:** commit `BLG-FE-226` (STEP 8.0), `BLG-FE-227` and `BLG-BE-182` to v9.13. All three are ungated, build-and-ship and grounded in a direct read of a live surface. Release Planning may seat more U-items through its normal round-robin.

## STEP 3 — Backlog Health Review

Tags: no obsolete or duplicate items among the items touched this run. Quick wins noted for Release Planning: `BLG-GOV-390` (XS, makes 17 items selectable), and this window's XS items (`BLG-FE-228`, `BLG-FE-229`, `BLG-BE-185`, `BLG-GOV-392`, `BLG-GOV-394`).

### 3.1 Actionable Backlog Assessment

**Method:** structural heuristic (231 active items at scan time, ≥ 150), script-assisted (`scan_backlog_gate_conditions.py --as-of 2026-10-16 --json`), the same method as the last 5 rebalances. **Change disclosed:** 17 items whose `**Gate criteria:**` is literally `None` are counted **A** here, although the script still reports them as gated (`BLG-GOV-390`, open). Without that adjustment A would be 107 (46.3%).

| Category | Count (of 231 scanned) |
|----------|-------|
| A (107 ungated + 17 "None" gates) | 124 (53.7%) |
| T | 8 |
| D | 22 |
| L | 77 |

**Date-lapsed (A — verify):** the script reports 0 date-lapsed items as of 2026-10-16. Its separate "gating item shipped — verify" list has 25 items; they stay in their gated category (a shipped gating item is not proof the gate is met) and are left for Release Planning §1.3a, which reads that list.

**D-gated:** the PO-02 cluster (~2026-10-20 projection, not yet clear) and the SI-02 cluster (`**Last formally confirmed:**` NOT MET; no clearance estimate).

**T-gated:** `BLG-FEAT-31`, `BLG-BE-24`, `BLG-OPS-41`, `BLG-OPS-48` (2026-11-01), `BLG-OPS-53` (2026-11-22), `BLG-GOV-144` (2027-06-26), `BLG-OPS-84`, `BLG-GOV-382` (2027-01-03).

**L-gated top 5:** `BLG-FE-43/45/54/58/59` (P1, Arc-5 sprint-entry gates). No condition is more than 12 months away, so there are no archive candidates.

**Backlog Accessibility Warning:** 53.7% ≥ 30%, so not triggered.

## STEP 4 — Ideas

Loaded: 32 `Submitted` rows from the full-roster window `IW-20261016-01`. 0 parked rows.

### Gate-Condition Re-Check

No loaded idea has a Park Rationale, so there is nothing to re-check.

### Per-Idea Classification (PO; Facilitator verified the overlap checks; Challenger challenged each)

| Idea ID | Challenger | PO classification | Filed as |
|---------|-----------|-------------------|----------|
| IDEA-ai-compliance-20261016-01 | Is a flag for the same ticker not relevant context anyway? Rebuttal: the prompt presents them as this trade's flags; a later plan's override is not part of this trade. | 📋 Backlog (ungated) | `BLG-BE-186` (consolidated, 2 ideas) |
| IDEA-api-contracts-20261016-01 | Would the existing drift checks not catch this? Rebuttal: they compare routers, contracts and openapi with each other, never with the client. | 📋 Backlog (ungated) | `BLG-QA-228` |
| IDEA-api-contracts-20261016-02 | A rename breaks consumers. Accepted risk: aliases for one release. | 📋 Backlog (ungated) | `BLG-SPEC-204` (consolidated, 2 ideas) |
| IDEA-backend-engineering-20261016-01 | The write is meant to be non-blocking. Rebuttal: logging keeps it non-blocking. | 📋 Backlog (ungated) | `BLG-BE-185` |
| IDEA-base44-frontend-20261016-01 | Cosmetic. Accepted as P3. | 📋 Backlog (ungated) | `BLG-FE-229` |
| IDEA-base44-frontend-20261016-02 | Dead code is harmless. Rebuttal: `Position.update` is dead-looking code that was used, and broke. | 📋 Backlog (ungated) | `BLG-FE-230` (consolidated, 2 ideas) |
| IDEA-challenger-20261016-01 | Consolidated with the Director of Quality guard rather than a one-off sweep, so the check persists. | 📋 Backlog (ungated) | `BLG-QA-227` (consolidated, 2 ideas) |
| IDEA-challenger-20261016-02 | §10 already allows a role to record no further idea; the Alert measures shipped stories. Rejected. | ❌ Reject — not strong | — |
| IDEA-cybersecurity-20261016-01 | Overlaps the Base44 cleanup; consolidated. | 📋 Backlog (ungated) | `BLG-FE-230` (consolidated, 2 ideas) |
| IDEA-cybersecurity-20261016-02 | The API key is already public. Rebuttal: CORS still limits which pages can make credentialed calls; low cost to fix. | 📋 Backlog (ungated) | `BLG-SEC-43` |
| IDEA-data-model-20261016-01 | Ticker matching works for most users. Rebuttal: it mixes trades in the same ticker, which the debrief already shows. | 📋 Backlog (ungated) | `BLG-BE-186` (consolidated, 2 ideas) |
| IDEA-director-of-hr-20261016-01 | Rebalance-time append is enough. Rebuttal: two releases were missing at this run. | 📋 Backlog (ungated) | `BLG-GOV-394` |
| IDEA-director-of-quality-20261016-01 | Allow-listing intentional 404s adds upkeep. Accepted; the list is small. | 📋 Backlog (ungated) | `BLG-QA-227` (consolidated, 2 ideas) |
| IDEA-financial-reporting-20261016-01 | Same code path as the Monitor fix; consolidated. | 📋 Backlog (ungated) | `BLG-FE-226` (consolidated, 4 ideas) |
| IDEA-finops-20261016-01 | Minutes are free on a public repo. Rebuttal: runner queueing delays code PRs; the pass-through job keeps required checks. | 📋 Backlog (ungated) | `BLG-OPS-191` |
| IDEA-frontend-specs-20261016-01 | Off-by-one copy. Accepted as P3; it still contradicts the Positions page on the same day. | 📋 Backlog (ungated) | `BLG-BE-183` |
| IDEA-frontend-specs-20261016-02 | Low impact. Accepted as P3. | 📋 Backlog (ungated) | `BLG-FE-228` |
| IDEA-head-of-engineering-20261016-01 | Why not add a bulk exit route? Rebuttal: exits need a broker fill price and FX per position, which only the exit flow collects. | 📋 Backlog (ungated) | `BLG-FE-226` (consolidated, 4 ideas) |
| IDEA-head-of-engineering-20261016-02 | Overlaps `BLG-SPEC-186`. Kept: that item does not touch frontend consumers. | 📋 Backlog (ungated) | `BLG-FE-227` (consolidated, 2 ideas) |
| IDEA-head-of-specs-20261016-01 | Edge case. Rebuttal: it fired at this run. | 📋 Backlog (ungated) | `BLG-GOV-392` |
| IDEA-head-of-ux-20261016-01 | Cosmetic? Rebuttal: the colour distinguishes rule-driven from discretionary exits, the point of a reflection. | 📋 Backlog (ungated) | `BLG-FE-227` (consolidated, 2 ideas) |
| IDEA-head-of-ux-20261016-02 | Better to build the writers? Both: the checklist writer is in the same item; the prompt types stay labelled until built. | 📋 Backlog (ungated) | `BLG-BE-182` (consolidated, 3 ideas) |
| IDEA-infra-ops-20261016-01 | Screener failures are rare. Rebuttal: at month-end the consequence is an exit recommendation on stale data. | 📋 Backlog (ungated) | `BLG-OPS-190` |
| IDEA-metrics-20261016-01 | Users know what the digest means. Rebuttal: Reports shows a different "compliance" figure. | 📋 Backlog (ungated) | `BLG-SPEC-204` (consolidated, 2 ideas) |
| IDEA-metrics-20261016-02 | Low impact. Accepted as P3. | 📋 Backlog (ungated) | `BLG-SPEC-205` |
| IDEA-pmo-lead-20261016-01 | Overlaps this cycle's lessons. Filed so a sprint can seat it. | 📋 Backlog (ungated) | `BLG-GOV-393` |
| IDEA-product-owner-20261016-01 | Duplicate of Head of Engineering; consolidated. | 📋 Backlog (ungated) | `BLG-FE-226` (consolidated, 4 ideas) |
| IDEA-product-owner-20261016-02 | Risk of narrative creep. Scope restricted to numeric fields. | 📋 Backlog (ungated) | `BLG-BE-184` |
| IDEA-qa-lead-20261016-01 | Belongs in the fix's ACs; consolidated. | 📋 Backlog (ungated) | `BLG-FE-226` (consolidated, 4 ideas) |
| IDEA-qa-testing-20261016-01 | Grep-based tests are brittle. Accepted; dated allow-list. | 📋 Backlog (ungated) | `BLG-BE-182` (consolidated, 3 ideas) |
| IDEA-strategy-owner-20261016-01 | Re-litigates a shipped feature? Rebuttal: the feature shipped without §12.3 change control, so the strategy document is out of date either way. | 📋 Backlog (ungated) | `BLG-GOV-391` |
| IDEA-strategy-owner-20261016-02 | Writing an event for every incomplete plan could flood the journal. Scope: one event per plan save that moves to incomplete. | 📋 Backlog (ungated) | `BLG-BE-182` (consolidated, 3 ideas) |
**Consolidations (v9.0 convention):** 7. `BLG-FE-226` (4 ideas, same code path), `BLG-BE-182` (3, same event type and page), `BLG-FE-227` (2, same maps), `BLG-FE-230` (2, same client file), `BLG-QA-227` (2, same defect class), `BLG-SPEC-204` (2, same fields), `BLG-BE-186` (2, same events). Each consolidated item's `**Source:**` lists every contributing Idea ID, and each register row names its item. Five consolidations have 2 ideas, below the convention's typical 3–10. Each was checked for genuine overlap (same file or same field), not merely adjacency.

**Priorities:** `BLG-FE-226` P1 (a broken exit action, STEP 8.0); `BLG-FE-227`, `BLG-BE-182`, `BLG-QA-227`, `BLG-QA-228`, `BLG-GOV-391` P2; the rest P3.

**Idea Participation Check (4.3):** 10 roles submitted 2 net-new ideas; 12 roles submitted 1 and recorded that no further net-new idea survived the overlap checks (listed in the window summary). Innovation-debt note: those 12 roles are below the §4 minimum this window. Standard mode, so this is informational. 4 of the 12 dropped a topic for overlap.

**Queue verification:** "Advancing to STEP 5" = 0; queue rows = 0. Consistent.

### Submission Details (full template fields — `IW-20261016-01`)

#### IDEA-ai-compliance-20261016-01 — Bound the AI Post-Trade Debrief's red-flag context to the trade's own holding window
*Submitter:* AI Compliance & Governance Officer
- **Problem Statement:** `debrief_service.py::_journal_context_for_trade` (lines 413-421) calls `get_red_flag_events(page=1, page_size=5, ticker=ticker)` with no date bound, and the prompt then says "N recent flag(s) for this ticker". A debrief for an earlier AAPL trade cites the 5 most recent AAPL flags, including overrides logged for later plans that had nothing to do with that trade.
- **Strategic Alignment:** §3 (decision support only) and §13.1 (deterministic decision support). An advisory surface must not attribute behaviour to a trade it did not occur in.
- **Proposed Solution:** Filter the debrief's flags to the trade's own window (plan creation or entry date to exit date), or to its `position_id` once events carry one. When none fall in the window, say "no flags recorded for this trade".
- **Expected Value:** Debrief flag citations dated outside the trade's own window: unbounded today → 0.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks (§2.0 steps 5–6):** Backlog: archived `BLG-BE-108` decided the debrief's sources (notes plus flags), not the date window; no active item (grep `red_flag`, `debrief`). Code: confirmed at `backend/services/debrief_service.py:413-421`.

#### IDEA-api-contracts-20261016-01 — CI check that every frontend API call (method + path) exists in openapi.yaml
*Submitter:* API Contracts & Documentation Owner
- **Problem Statement:** The Dashboard's Daily Position Monitor calls `PATCH /positions/{id}` (`src/api/base44Client.js:223`). No such route exists; only `GET /positions/{position_id}` and three `PATCH` sub-routes do. `check_openapi_drift.py` compares routers, contracts and `openapi.yaml` but never the consumer, and `check_consumer_contract_drift.js` covers only the `api` object's response fields (its own scope note, lines 11-16). A scripted comparison this window found 2 client methods with no route (`PATCH /positions/{id}`, `POST /signals`) and 2 Base44 auth leftovers.
- **Strategic Alignment:** §12.3 (documentation and implementation must match) and §3: a decision-support action that silently fails misleads the user.
- **Proposed Solution:** A script that extracts every `doFetch`/`apiFetch` method and path from `src/` and fails when a pair is missing from `docs/reference/openapi.yaml`, with an allow-list for intentional external calls, run in the existing quality gate.
- **Expected Value:** Live frontend calls to non-existent routes: 2 → 0, and new ones blocked at PR time.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `consumer contract`, `route-existence`). Code: `scripts/check_consumer_contract_drift.js` scope comment confirms response-field-only coverage via the `api` object.

#### IDEA-api-contracts-20261016-02 — `GET /digest/weekly` names journal completion rate `compliance_score_*`
*Submitter:* API Contracts & Documentation Owner
- **Problem Statement:** `digest_endpoints.md` and `routers/digest.py:61-62` define `compliance_score_current` and `compliance_score_7d_ago` as `journal_completion_rate`. Elsewhere "compliance" means the Arc 5 composite (`metrics_definitions.md` "Arc 5 Compliance Composite Score"; v7.7 Strategy Owner decision in `database.py::get_arc5_composite_for_range`). One field name carries two meanings across the API.
- **Strategic Alignment:** §12.3 (documentation must match live logic); role charter rule "same field must mean the same thing everywhere".
- **Proposed Solution:** Add `journal_completion_rate_current`/`_7d_ago` to the contract and response, keep the old names as deprecated aliases for one release, and update `openapi.yaml`.
- **Expected Value:** API fields whose name contradicts their definition: 2 → 0.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item names these fields (grep `compliance_score_current`); 2 archive hits concern a separate red-flag frequency metric. Code: confirmed at `backend/database.py:5255` (`# 4. Compliance score — journal_completion_rate`).

#### IDEA-backend-engineering-20261016-01 — Stop silently discarding failed red-flag override writes
*Submitter:* Backend Engineering Patterns Owner
- **Problem Statement:** `routers/trade_plans.py::_maybe_write_override_event` (lines 174-185) wraps `create_red_flag_event` in `except Exception: pass`. If the insert fails, the override is lost with no log line, so the Red Flag Journal, the Arc 5 composite's override rate and the AI debrief all under-count without anyone knowing.
- **Strategic Alignment:** §4.2.6 (non-blocking pre-entry advisories must still be recorded when overridden) and §12.3.
- **Proposed Solution:** Keep the write non-blocking, but log at WARNING with ticker and event type, and count failures on `GET /health` so a failing writer is visible.
- **Expected Value:** Silent override-event write failures: undetectable today → logged and counted (target 0 unlogged).
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `_maybe_write_override_event`, `override event`). Code: confirmed at `backend/routers/trade_plans.py:174-185`.

#### IDEA-base44-frontend-20261016-01 — Trade Reflections shows "No closed trades yet" when a ticker search simply has no match
*Submitter:* Base44 Frontend Prompt Owner
- **Problem Statement:** `src/pages/TradeReflection.js:61-66` renders the same empty state for an empty list and for a search with no match: "No closed trades yet — close a trade to write your first reflection." A user with 30 closed trades who types a ticker they never traded is told they have no closed trades.
- **Strategic Alignment:** §3 (decision support): the surface must not misstate the user's own record.
- **Proposed Solution:** When `trades.length > 0` and the filtered list is empty, show "No reflections match '<search>'" with a clear-search button; keep the current text for a genuinely empty list.
- **Expected Value:** Misleading empty-state messages on this page: 1 → 0 (Playwright-verifiable).
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon · **Build-and-ship candidate (§2.1 step 2a):** yes
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `TradeReflection`; 4 archive hits are the reminder and format items, not the empty state). Code: confirmed at `TradeReflection.js:61-66`.

#### IDEA-base44-frontend-20261016-02 — Remove dead Base44 scaffold methods from `base44Client.js` that call routes the backend never had
*Submitter:* Base44 Frontend Prompt Owner
- **Problem Statement:** `base44Client.js` keeps `Signal.create` (`POST /signals`, no route), `getPublicSettingsById` (`/apps/public/prod/public-settings/by-id/…`) and `exchangeCodeForToken` (`POST /auth/callback`). None has a caller in `src/`. They make the client look as if those routes exist, and `Position.update` (`PATCH /positions/{id}`, also no route) shows that a dead method can be picked up and used.
- **Strategic Alignment:** §12.3 (implementation should not describe behaviour that does not exist).
- **Proposed Solution:** Delete the three uncalled methods and their helpers. `Position.update` is handled by the Monitor fix.
- **Expected Value:** Client methods targeting non-existent routes: 4 → 1 (→ 0 with the Monitor fix).
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `exchangeCodeForToken`, `public-settings`). Code: grep of `src/` shows no callers besides `Dashboard.js:138` (`Position.update`).

#### IDEA-challenger-20261016-01 — Challenge: the Dashboard's Daily Position Monitor exit action has been broken since January — what is the debt process checking?
*Submitter:* Challenger
- **Problem Statement:** The Monitor's "confirm exits" (`Dashboard.js:136-148`) has called a non-existent `PATCH /positions/{id}` since commit `997ed1b2` (2026-01-24). Every confirm fails with an unhandled 405, and the modal gives no feedback. Thirty-odd releases, most of them debt clearance, did not find a broken primary action on the home page, while the Product Value Ratio has been in Alert for 7 consecutive readings.
- **Strategic Alignment:** §2.5 and §3: the human-in-the-loop exit must actually work when the system recommends one.
- **Proposed Solution:** Make one "dead primary action" sweep the first debt item of the next release: drive every state-changing button through its real route on staging and record the result, instead of a further governance item.
- **Expected Value:** Known broken primary actions: 1 found by chance → systematic coverage of all state-changing actions.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** Defer one governance/process item of equal size from the next release. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `MonitorModal`, `Daily Position Monitor`). Code: confirmed route absence (`grep @app.patch backend/main.py`).

#### IDEA-challenger-20261016-02 — Challenge: full-roster idea windows require 2 ideas from every role, and 17 of 22 roles have no user-facing remit
*Submitter:* Challenger
- **Problem Statement:** §4's minimum of 2 net-new ideas per role applies to all 22 roles, though §2.1 step 2a names only 5 as user-facing, while STEP 2.4 has read Product Value Alert for 7 consecutive readings. Roles without a user-facing remit are pushed to produce governance and process ideas, which feed the G/D share the Alert is measuring.
- **Strategic Alignment:** §2 (strategy intent: product outcomes) read with roadmap STEP 2.4's purpose.
- **Proposed Solution:** Allow non-user-facing roles to meet the minimum with 1 idea plus a recorded "no further net-new idea" statement during a Product Value Alert, and say so in `idea_intake_prompt.md` §4.
- **Expected Value:** Governance-shaped intake per full window: falls by up to ~17 ideas while the Alert holds.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `minimum submissions`). `BLG-GOV-364` (archived) ruled on reduced rosters, not per-role minimums.

#### IDEA-cybersecurity-20261016-01 — Remove the unused bearer-token path: the client sends any `localStorage` token as `Authorization` to an API that has no auth route
*Submitter:* Cybersecurity & Trust Lead
- **Problem Statement:** `base44Client.js::getToken` reads a token from `localStorage` and `doFetch` attaches it as `Authorization: Bearer …` on every request. `exchangeCodeForToken` posts to `/auth/callback`, which does not exist, and no backend code reads `Authorization`. The dead path widens what a script injected into the page could plant and replay, for no benefit.
- **Strategic Alignment:** §13.1 (a single, explicit system): the trust model is the single API key (`credential_policy.md` v1.1 §1.1), and unused credential plumbing should not imply another.
- **Proposed Solution:** Remove `getToken`/`setToken`, the `Authorization` header and the IdP helpers, and record in `credential_policy.md` that the frontend sends only `X-API-Key`.
- **Expected Value:** Credential-carrying headers with no server consumer: 1 → 0.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `Bearer`, `getToken`). Code: `grep -rn Authorization backend` finds no reader.

#### IDEA-cybersecurity-20261016-02 — Production API's CORS allow-list includes `http://localhost:3000` and the API's own origin
*Submitter:* Cybersecurity & Trust Lead
- **Problem Statement:** `backend/config.py:12-17` has one `ALLOWED_ORIGINS` list for every environment: GitHub Pages, the production API's own origin, the staging frontend and `http://localhost:3000`. With `allow_credentials=True` and `allow_methods=['*']`, production accepts credentialed cross-origin requests from any page served on a developer's localhost:3000.
- **Strategic Alignment:** §13.1 (human-in-the-loop by design): production writes should come only from the user's own frontend.
- **Proposed Solution:** Build the list per environment from an env var: production gets the Pages origin only, staging adds the staging frontend, local dev adds localhost.
- **Expected Value:** Non-production origins accepted by production: 3 → 0.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `CORS`, `ALLOWED_ORIGINS`). Code: confirmed at `backend/config.py:12-17`, `main.py:212-215`.

#### IDEA-data-model-20261016-01 — Link pre-entry override events to the position they led to
*Submitter:* Data Model & Domain Schema Owner
- **Problem Statement:** `trade_plans.py:260` writes `pre_entry_override` with `body.position_id` at plan creation, before any position exists, so the event's `position_id` is null. Nothing back-fills it when the plan becomes a position. Per-trade joins (debrief, plan-vs-reality, the composite's override rate) must fall back to ticker matching, which mixes trades in the same ticker.
- **Strategic Alignment:** §4.2.6 (overridden advisories are part of the trade record) and §12.3.
- **Proposed Solution:** When a plan is linked to a position, set `position_id` on that plan's override events, back-fill existing rows where the plan already carries a `position_id`, and document the column's lifecycle in `data_model.md`.
- **Expected Value:** Override events joinable to their trade by key: ~0% today → 100% of plan-linked trades.
- **Effort Estimate:** Small · **Reversibility:** Mostly reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `red_flag_events.position_id`). Code: confirmed at `backend/routers/trade_plans.py:174-185, 260, 579`.

#### IDEA-director-of-hr-20261016-01 — Append the role-share history row at post-ship closure, not only at a rebalance
*Submitter:* Director of HR
- **Problem Statement:** `claude/roadmap/role_share_history.md` ends at v9.10. v9.11 and v9.12 have shipped, but rows are appended only when a rebalance runs. Two releases shipped between rebalances, so the §7.2 cross-role reading at any moment can lag by two cycles.
- **Strategic Alignment:** §12.3 (recorded figures should match current state); roadmap §7.2.
- **Proposed Solution:** Have post-ship closure run `scripts/compute_role_share_history.py` for the cycle it closes and append the row, mirroring the ready-pool row Release Planning now appends.
- **Expected Value:** Releases missing from the role-share history at any time: up to 2 → 0.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `role_share_history`). File: last History row is v9.10 (`role_share_history.md` line 40).

#### IDEA-director-of-quality-20261016-01 — Fail the Playwright suite on any 404 or 405 API response
*Submitter:* Director of Quality
- **Problem Statement:** SC-DCO-03 (`tests/e2e/dialog-classname-override-fixes.spec.js:98-107`) opens the Daily Position Monitor and checks its layout, but nothing in the suite presses a state-changing button and checks the response. A primary action that has returned 405 since January passed every gate.
- **Strategic Alignment:** §12.3 and §3: the exit a user confirms must reach the backend.
- **Proposed Solution:** Add a shared Playwright fixture that records every API response and fails the test on any 404/405 from the app's own API origin (allow-list for intentional probes). Then add one test per state-changing primary action that is not yet exercised.
- **Expected Value:** State-changing UI actions whose request is verified end-to-end: unknown (Monitor = 0) → all listed actions.
- **Effort Estimate:** Medium · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `404`, `405`, `network guard`). Tests: confirmed SC-DCO-03 asserts layout only.

#### IDEA-financial-reporting-20261016-01 — The Monitor's bulk exit would write a P&L that bypasses fees, broker fill and FX
*Submitter:* Financial Reporting & Records Owner
- **Problem Statement:** `Dashboard.js:136-148` builds the exit payload itself: `pnl = (current_price − entry_price) × shares` from display prices, with no fees, no broker fill price, no exit FX rate and no `trade_history` row. `ExitPositionRequest` (`models/requests.py:107-122`) requires a user exit price and, for US, an exit FX rate. If the route existed, the close would disagree with every other closed trade.
- **Strategic Alignment:** §4.1.5 (currency and FX handling) and §3 (exits recorded from the user's actual execution).
- **Proposed Solution:** Route Monitor exits through `POST /positions/{id}/exit` via the existing ExitModal, so fees, fill and FX are captured the same way as every other exit.
- **Expected Value:** Exit paths that bypass the canonical P&L calculation: 1 → 0.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `handleExitPositions`). Consolidates with the Monitor fix (same code path).

#### IDEA-finops-20261016-01 — Skip the five code-test workflows on governance-only and docs-only pushes
*Submitter:* FinOps & Resource Architect
- **Problem Statement:** 878 of 1,034 commits on `main` since 2026-09-15 touch only `claude/` or `docs/`. CI Pytest, Critical-Path Smoke, Service Layer Coverage, Golden Output and Portfolio Integration still run on every push (no path filter). Together they used ~5,500 run-minutes in 2026-08 (`docs/ops/ci_usage_reports/2026-08.md`). The minutes are free on a public repo, but runner queueing delays real code PRs.
- **Strategic Alignment:** §12 (parameter governance) is not engaged; this is delivery capacity. No strategy section — infrastructure cost.
- **Proposed Solution:** Add `paths-ignore: ['claude/**', 'docs/**']` to those five workflows, with a pass-through job so required checks still report on PRs that touch only governance files (the constraint archived item at `backlog_archive.md:2167` names).
- **Expected Value:** Code-test workflow runs: about −80% of push-triggered runs; run-minutes ~5,500/month → ~1,100.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `paths-ignore`). `BLG-OPS-188` covers the usage report's commit failure, not filtering. Code: confirmed no `paths-ignore` in `.github/workflows/`.

#### IDEA-frontend-specs-20261016-01 — Grace-period warning says "day 8 of 10" while Positions shows Day 9 for the same position
*Submitter:* Frontend Specifications & UX Documentation Owner
- **Problem Statement:** `alerts_service.py:697-713` builds the grace warning from `holding_days` (0-based calendar days) and writes "(day 8 of 10)". Positions numbers the entry day as Day 1 (`Positions.js:146-148`, `min(grace + 1 − grace_days_remaining, grace)`), so the same position on the same day is Day 9 there. The preference text "Notify on days 8–9 of the grace period" (`NotificationPreferences.js:20`) uses the 0-based convention too.
- **Strategic Alignment:** §6.2 (grace period counted in calendar days from entry) and §6.3: the user must see one consistent count of grace left.
- **Proposed Solution:** Use the entry-day-is-Day-1 numbering in the alert message and context, and change the preference copy to "Notify on the last 2 days of the grace period" drawn from `GRACE_PERIOD_DAYS`.
- **Expected Value:** Surfaces disagreeing on the grace day number: 2 (feed/email, preferences) → 0.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon · **Build-and-ship candidate (§2.1 step 2a):** yes
- **Overlap checks (§2.0 steps 5–6):** Backlog: `backlog.md:347` mentions "days 8–9" only inside a test AC about settings rows; no item covers numbering. Code: confirmed at the cited lines.

#### IDEA-frontend-specs-20261016-02 — Alert History's compact values look for keys the backend never writes
*Submitter:* Frontend Specifications & UX Documentation Owner
- **Problem Statement:** `NotificationsHistory.js` shows grace warnings with `[days_remaining, grace_period_days]` and daily summaries with `[positions_count, total_pnl]`. The backend writes `min_hold_days` (`alerts_service.py:697-701`) and `open_positions` (line 763). The "Grace Period" value never appears, and summary rows fall back to raw keys.
- **Strategic Alignment:** §12.3 (displayed values must match live logic).
- **Proposed Solution:** Align the UI key lists and labels to the backend's keys (or rename the backend keys) and add the mapping to the Alert History page spec.
- **Expected Value:** Alert types whose compact cell shows the intended fields: 2 of 4 → 4 of 4.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later · **Build-and-ship candidate (§2.1 step 2a):** yes
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `NotificationsHistory`, `positions_count`). Code: confirmed at the cited lines.

#### IDEA-head-of-engineering-20261016-01 — Make the Daily Position Monitor's "confirm exits" work: open the real exit flow for each selected position
*Submitter:* Head of Engineering
- **Problem Statement:** `MonitorModal` suggests exits (stop hit or market risk-off) and its confirm calls `Dashboard.js::handleExitPositions`, which calls `base44.entities.Position.update` → `PATCH /positions/{id}`. No such route exists (FastAPI returns 405). The handler has no try/catch, so the first failure becomes an unhandled rejection, the modal stays open with the selection cleared, and no position is closed or explained.
- **Strategic Alignment:** §8.1/§8.2 (the system recommends, the user confirms) and §3: a confirmed exit must be recordable.
- **Proposed Solution:** Replace the bulk PATCH with a queue that opens the existing ExitModal for each selected position, with exit reason pre-set ("Stop Loss Hit"/"Risk-Off Signal"), so price, FX and fees are captured. Show an error if any step fails, and delete `Position.update`.
- **Expected Value:** Monitor exit confirmations that close a position: 0% → 100%; silent failures → 0.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now · **Build-and-ship candidate (§2.1 step 2a):** yes
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `MonitorModal`, `handleExitPositions`; 1 archive hit is a dialog layout item). Code: confirmed by route grep and `doFetch` raw-mode throw.

#### IDEA-head-of-engineering-20261016-02 — One shared exit-reason module for the four frontend files that each keep their own map
*Submitter:* Head of Engineering
- **Problem Statement:** `TradeReflection.js:12-22`, `TradeReflectionModal.js:23-26` and `PerformanceAnalytics.js:443-448` map legacy keys (`stop_hit`, `manual`, `target`, `market_regime`) that `ExitModal.js:359-364` never writes. Stored values are "Manual Exit", "Stop Loss Hit" and so on, so every badge colour and label lookup misses and falls back.
- **Strategic Alignment:** §8 (exit conditions shown consistently) and §12.3.
- **Proposed Solution:** `src/constants/exitReasons.js` holding the 6 stored values with label, colour and §8 category, imported by ExitModal, both reflection views, PerformanceAnalytics and TradeHistoryTable; the legacy keys stay as aliases.
- **Expected Value:** Exit-reason maps in the frontend: 5 → 1; lookups that miss stored values: 3 files → 0.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon · **Build-and-ship candidate (§2.1 step 2a):** yes
- **Overlap checks (§2.0 steps 5–6):** Backlog: refines `BLG-SPEC-186` (allowed values and §8 mapping in the specs and a DB constraint), adding the frontend consumers it does not touch.

#### IDEA-head-of-specs-20261016-01 — Reconcile shared_standards §2's "write Blocked state before halting" with the roadmap engine's state-write limits
*Submitter:* Head of Specs Team
- **Problem Statement:** `shared_standards.md` §2 step 3 says every hard-gate halt updates state to `Blocked`. `roadmap_prompt.md` §4 allows `.claude_current_state.json` only at STEP 12, and STEP 12.1 forbids overwriting `status`, because the field belongs to the release cycle. At this run's STEP -1.5 OVERDUE halt the two rules could not both be followed. State was not written, and the halt report disclosed the conflict.
- **Strategic Alignment:** §12.3 (one rule per behaviour). Governance precedence: `shared_standards.md` vs an engine's own write scope.
- **Proposed Solution:** State the exception in §2: rebalance and other non-cycle engines record the halt in their own artefact (`run_manifest.md`), or in a dedicated `last_halt` key, rather than the cycle `status`.
- **Expected Value:** Contradictory halt instructions between the shared standard and an engine: 1 → 0.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `Blocked` with `rebalance`). Evidence: this cycle's run manifest, STEP -1.5.

#### IDEA-head-of-ux-20261016-01 — Trade Reflections cards show grey raw-uppercase exit badges because their colour map never matches
*Submitter:* Head of UX & Design
- **Problem Statement:** Every Trade Reflections card badge (`TradeReflection.js:12-22`) and the modal's Exit Reason (`TradeReflectionModal.js:23-26`) look up `stop_hit`/`manual`/`target`/`market_regime`. Stored reasons are "Stop Loss Hit", "Manual Exit" and so on, so every card falls back to grey with text such as "STOP LOSS HIT" or "RISK-OFF SIGNAL", and the red/violet/green/amber coding that distinguishes stop exits from discretionary ones never renders.
- **Strategic Alignment:** §8 (three exit conditions; stop exits are the strategy's core outcome) and §2.5. Reviewing which exits were rule-driven is the point of a reflection.
- **Proposed Solution:** Map the 6 stored values to labels and colours (stop and trailing stop red, risk-off amber, manual violet, target and partial green) in both views, with Playwright coverage of each colour.
- **Expected Value:** Reflection cards with a meaningful exit-reason colour: 0% → 100%.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon · **Build-and-ship candidate (§2.1 step 2a):** yes
- **Overlap checks (§2.0 steps 5–6):** Backlog: refines `BLG-SPEC-186` (spec/DB values), adding the user-visible badge fix. 4 archive hits (reminder, format) do not cover badges. Code: confirmed at the cited lines.

#### IDEA-head-of-ux-20261016-02 — Red Flag Journal offers three event-type filters that can never return a row
*Submitter:* Head of UX & Design
- **Problem Statement:** The Red Flag Journal's type filter (`RedFlagJournal.js:43-49`) offers Checklist Skipped, Stop Prompt Dismissed and Drawdown Prompt Dismissed. Nothing in `backend/` or `src/` ever writes those three types; the only writer is `pre_entry_override` (`trade_plans.py:174-185`). A user who filters for skipped checklists sees an empty journal and concludes they never skipped one.
- **Strategic Alignment:** §4.2.6 (overrides of advisories must be visible) and §3.
- **Proposed Solution:** Until each type has a writer, show the filter options greyed with "not yet recorded" (or hide them), and say in the empty state which types are recorded today.
- **Expected Value:** Filter options that can only return empty results without saying so: 3 → 0.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon · **Build-and-ship candidate (§2.1 step 2a):** yes
- **Overlap checks (§2.0 steps 5–6):** Backlog: archived colour item (`backlog_archive.md:15752`) only; no active item (grep `checklist_skipped`). Code: writer grep confirmed.

#### IDEA-infra-ops-20261016-01 — Nightly job chain is ordered by clock time only; rebalance-exit can run on a stale top-5
*Submitter:* Infrastructure & Operations Owner
- **Problem Statement:** `screener-refresh.yml` (22:00 UTC), `nightly-stop-update.yml` (22:30) and `rebalance-exit.yml` (22:45) rely on start times for ordering (`rebalance-exit.yml` header). Nothing checks that the screener finished or succeeded. `generate_rebalance_exit_signals` reads "the most recent signal_date" top-5, so on a month-end where the screener fails, exit recommendations use the previous day's ranking with no warning.
- **Strategic Alignment:** §8 and §3: an exit recommendation must rest on current data.
- **Proposed Solution:** Before generating, have the rebalance-exit endpoint (or workflow) check that a screener run completed today. If none did, skip and alert, the way `nightly-stop-update-staleness-check.yml` does for stops.
- **Expected Value:** Month-end exit recommendations generated on stale rankings without warning: possible today → 0.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `rebalance-exit`); `BLG-SPEC-188` covers stop freshness only. Code: `signal_service.py:411-440`.

#### IDEA-metrics-20261016-01 — Weekly Digest labels journal completion rate as "Compliance Score"
*Submitter:* Metrics Definitions & Analytics Owner
- **Problem Statement:** `WeeklyDigest.js` shows "Compliance Score (current)" and "(7d ago)", which `database.py:5255` computes as journal completion rate. `metrics_definitions.md` defines the compliance score as the Arc 5 composite, and the v7.7 Strategy Owner decision (cited at `database.py::get_arc5_composite_for_range`) says the same field must mean the same thing everywhere. A user comparing the digest with Reports sees two different "compliance" figures.
- **Strategic Alignment:** §12.3 and the metrics charter's single-meaning rule.
- **Proposed Solution:** Relabel the digest rows "Journal Completion Rate". Alternatively, source the rows from the Arc 5 composite. Record the choice in `metrics_definitions.md`.
- **Expected Value:** UI metrics named "compliance" with a non-compliance definition: 2 → 0.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon · **Build-and-ship candidate (§2.1 step 2a):** yes
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `Compliance Score`, `compliance_score_current`). Code: confirmed at the cited lines.

#### IDEA-metrics-20261016-02 — "Alerts Dismissed (7d)" counts alerts created in the window that are now read, not alerts read in the window
*Submitter:* Metrics Definitions & Analytics Owner
- **Problem Statement:** `routers/digest.py:59` documents `alerts_dismissed_7d` as "count of notifications marked read in the last 7 days". The SQL (`database.py`, digest step 3) counts notifications *created* in the last 7 days that are read. An alert from 10 days ago dismissed yesterday is not counted, and the figure cannot exceed Alerts Fired.
- **Strategic Alignment:** §12.3 (documented definitions must match the computation).
- **Proposed Solution:** Either add a `read_at` timestamp and count by it, or change the definition and label to "Alerts fired in 7d and since read". Record the result in `metrics_definitions.md`.
- **Expected Value:** Digest fields whose computation differs from its definition: 1 → 0.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `alerts_dismissed`). Code: confirmed at `backend/database.py` digest step 3.

#### IDEA-pmo-lead-20261016-01 — Deferred roadmap patches go OVERDUE by carry count before their own target date
*Submitter:* PMO Lead
- **Problem Statement:** Three patches deferred on 2026-10-06 with target 2026-10-20 were OVERDUE at this rebalance (second carry), 4 days before their target date. That halted STEP -1.5 until the Head of Specs Team applied them in-session. Two sprints (v9.11, v9.12) ran in between without seating them, because no step turns a deferred prompt patch into backlog work.
- **Strategic Alignment:** §12.3 (change control); roadmap STEP -1.5.
- **Proposed Solution:** When a rebalance files a deferred prompt patch, also file a backlog item (owner and target as in the patch) so Release Planning can seat it, and have STEP -1.5 treat a patch whose backlog item is seated in the current release as carried, not OVERDUE.
- **Expected Value:** Rebalance halts from un-seated deferred patches: 1 this cycle → 0.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `deferred patch`). Evidence: this cycle's STEP -1.5.

#### IDEA-product-owner-20261016-01 — The Daily Position Monitor cannot exit a position: fix it before the next stop or risk-off event
*Submitter:* Product Owner
- **Problem Statement:** On the Dashboard, Quick Actions → Run Monitor lists positions with a stop hit or a risk-off market and lets the user select and confirm exits. Every confirm calls a route that does not exist, so nothing closes and nothing is said. This is the home page's only exit shortcut, and it fails exactly when §8.1/§8.2 say to exit.
- **Strategic Alignment:** §8.1/§8.2 (exit is recommended and requires manual confirmation; the confirmation must work) and §3.
- **Proposed Solution:** Same scope as the Head of Engineering submission: each confirmed exit opens the real exit flow, with a visible error on failure and Playwright coverage of the confirm path.
- **Expected Value:** Working exit confirmations from the Monitor: 0 → all.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** Defer one P3 governance item from the next release. · **Submitter Recommendation:** Now · **Build-and-ship candidate (§2.1 step 2a):** yes
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `MonitorModal`). Consolidates with `IDEA-head-of-engineering-20261016-01`.

#### IDEA-product-owner-20261016-02 — The Daily Portfolio Summary notification says only how many positions are open
*Submitter:* Product Owner
- **Problem Statement:** Notification Preferences describes Daily Portfolio Summary as "a daily digest of portfolio status" (`NotificationPreferences.js:31-45`). The message the backend sends is "Daily summary: N open position(s) as of today." (`alerts_service.py:763-766`): no P&L, no stops near the price, no grace endings.
- **Strategic Alignment:** §5/§7 purpose (make downside risk visible) and §3 (decision support).
- **Proposed Solution:** Include total unrealised P&L (GBP), the day's change, positions within the stop-approach threshold and grace periods ending in ≤2 days, all from existing computations; keep it numeric, with no narrative.
- **Expected Value:** Decision-relevant fields in the daily summary: 1 (count) → 5.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon · **Build-and-ship candidate (§2.1 step 2a):** yes
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `daily_portfolio_summary`; 4 archive hits are the original feature and email wiring). Code: confirmed at the cited lines.

#### IDEA-qa-lead-20261016-01 — Regression test for the Daily Position Monitor confirm path
*Submitter:* QA Lead
- **Problem Statement:** The only Monitor test (SC-DCO-03) checks dialog width. No unit or e2e test calls `handleExitPositions`, which is why a 405 on every confirm has gone unseen since January.
- **Strategic Alignment:** §8.1/§8.2 and §3.
- **Proposed Solution:** As part of the Monitor fix: a Playwright test that selects a suggested exit, confirms, completes the exit flow and asserts the position leaves the open list (staging seed), plus a test that a failed request shows an error.
- **Expected Value:** Tests covering the Monitor's state-changing path: 0 → 2.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item. Consolidates with the Monitor fix.

#### IDEA-qa-testing-20261016-01 — Test that every red-flag event type the API accepts has at least one writer
*Submitter:* QA & Testing Owner
- **Problem Statement:** `database.py::_VALID_EVENT_TYPES` and the API contracts list 4 event types, but only `pre_entry_override` is written anywhere. No test notices when a declared type has no producer, so the gap has persisted since v3.9.
- **Strategic Alignment:** §4.2.6 and §12.3.
- **Proposed Solution:** A pytest that greps `backend/` and `src/` for a write of each declared type and fails for any without one (with an explicit, dated allow-list while the writers are built).
- **Expected Value:** Declared event types without a producer, detected automatically: 3 undetected → 0 undetected.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `checklist_skipped`). Consolidates with the Strategy Owner's writer idea.

#### IDEA-strategy-owner-20261016-01 — Month-end rebalance exits are live but not in `strategy_rules.md`
*Submitter:* Strategy Rules & System Intent Owner
- **Problem Statement:** Since v6.2 (`BLG-FEAT-47`), `generate_rebalance_exit_signals` recommends exiting every open position not in the current top-5 momentum ranking on the last trading day of each month, and `rebalance-exit.yml` runs it nightly. `strategy_rules.md` has no mention of rebalancing. §8 says a position may exit under "exactly three conditions" and §1 says any behaviour that can affect outcomes "must be specified here". The feature came from a `production_strategy.py` gap analysis, not a §12.3 change.
- **Strategic Alignment:** §1 (behavioural contract), §8 (exactly three exit conditions), §2.2-§2.3 (avoid premature exits; give losing trades time).
- **Proposed Solution:** Strategy Rules & System Intent Owner determination: either add rebalance exit to §8 through §12.3 change control (with its §2 rationale), or withdraw the signal. Until then, label the signal "outside §8 — informational".
- **Expected Value:** Live exit recommendations not defined in the strategy: 1 → 0.
- **Effort Estimate:** Small · **Reversibility:** Mostly reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: no active item (grep `exit_rebalance`, `rebalance exit`); `BLG-FEAT-47` (archived) shipped the feature without a strategy amendment. `BLG-SPEC-186` maps stored exit reasons to §8 but does not cover generated signals.

#### IDEA-strategy-owner-20261016-02 — Record `checklist_skipped` when a trade plan is saved with its checklist incomplete
*Submitter:* Strategy Rules & System Intent Owner
- **Problem Statement:** TradePlan lets a plan be saved with `checklist_completed: false` (`TradePlan.js:442, 674`). The Red Flag Journal contract defines `checklist_skipped` for exactly this (`red_flag_journal.md:39, 68`), but nothing writes it. The journal and the Arc 5 composite's events-per-week term therefore never see skipped checklists.
- **Strategic Alignment:** §4.2.6 (non-blocking, but overrides recorded) and §2 (discipline is part of the strategy's intent).
- **Proposed Solution:** On plan create or update where `checklist_completed` moves to false with a non-empty checklist, write a `checklist_skipped` event (ticker, plan id, unchecked item count), non-blocking.
- **Expected Value:** Skipped-checklist plans recorded in the journal: 0% → 100%.
- **Effort Estimate:** Small · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Soon · **Build-and-ship candidate (§2.1 step 2a):** yes
- **Overlap checks (§2.0 steps 5–6):** Backlog: no active item (grep `checklist_skipped`; archived hit is a colour change). Code: writer grep confirmed only `pre_entry_override` is written.

## STEP 5 — Debate

Queue empty — no debates required. No idea was classified ✅ Advance.

## STEP 6 — Scoring

No surviving STEP 5 candidates, so there is nothing to score. `claude/scoring/scored_initiatives.md` is not rewritten this run.

## STEP 7 — Workforce Economics

No in-scope initiatives, so there is no FTE load to assess.

- **§7.1 Skill-Silo:** 69.6% pooled (78/112, v9.10–v9.12). Improved from 87.4%, but still above the 40% ceiling. Under the v9.35 definition (`ESC-RB-20261008-01`), every above-ceiling reading is "unresolved", and the run of such readings is well over 3. **Sustained-failure clause applies:** ≥2 build-and-ship U-items, met by `BLG-FE-226`, `BLG-FE-227` and `BLG-BE-182`. **Candidate gate verification:** none of the three has a `**Gate criteria:**` line. **Live-status cross-check:** all three are active, filed this run, with no completion marker. **Cross-role pairing note:** `workforce_capacity.md` read; no conflict. The unrecorded v9.9–v9.11 pooled reading was 79.8% (`--silo-history`).
- **§7.2:** max 8.0% raw (Infrastructure & Operations Owner, v9.10–v9.12), so no advisory. Source: `role_share_history.md`, with the v9.11 and v9.12 rows appended via script this run.
- **§7.3:** source `claude/roadmap/ready_pool_history.md` (first use; created this run under `BLG-GOV-374`). Newest row v9.12: 54.70-day pool against a 28-day ceiling, gap 26.70 days. Gap series v9.10 33.80 → v9.11 33.67 → v9.12 26.70: shrinking for 2 releases, so advisory only. Runway: N/A — pool growing (rolling Δ leftover +6.13).
- **< 20% floor:** not applicable (69.6%).

## STEP 8 — Final Rebalance Decision

**Initiatives:** no change (0 active). This is a valid "no change" outcome for initiatives. `Last Updated` is refreshed and DL-086 is logged.

**Displacement candidate flag:** none, since there are no initiatives. `displacement_debt_register.md` is unchanged.

### STEP 8.0 — Production Correctness Fast-Track

Scanned 13 pre-existing P0/P1 items (`BLG-FEAT-73`, `BLG-FE-43/45/54/58/59/62/63/68/69/70/71`, `BLG-SPEC-35`): none is a correctness or security item. **`BLG-FE-226` (P1, filed this run) qualifies.** The Monitor's exit confirmation silently fails, so a user acting on a §8.1/§8.2 recommendation from the home page closes nothing and is told nothing. **Promoted to the v9.13 Now horizon** ("Correctness Fast-Track Promotion", DL-086). No PO override: an exit action that fails silently can affect a trading decision.

### STEP 8.0.5 / 8.2 — Candidate verification

For each of `BLG-FE-226`, `BLG-FE-227` and `BLG-BE-182`: active in `backlog.md`, with no `✅ COMPLETE` and no `RA:` marker. **STEP 8.2 verification complete — 3 items verified active, 0 items excluded.**

### STEP 8.1 — Empty Now Horizon Gate

Conditions 1a (Now empty) and 2 (no next-release section) were true at run start.

**PO decision (STEP 8.1): Option (a) — next-release section added to current_roadmap.md. Section: v9.13 — Committed items. Rationale:** the Product Owner wants v9.13 planned next. A version-labelled section with 3 committed items lets Release Planning pass §-1.2 directly.

### STEP 8.1.5 — §13-Adjacent Initiative Expiry Review

⚠ **§13-adjacent expiry:** `BLG-FEAT-55` / `BLG-SPEC-65` / `BLG-SPEC-66` have been gated on an unopened §13 chat-persistence review since 2026-07-25, which is more than 2 rebalance cycles. Surfaced to the Strategy Rules & System Intent Owner again. Their recorded response this cycle (agent-mediated): **"still not ready, re-check next cycle"**. Chat remains stateless per SRB-v1.7, and no persistence design exists to review. That response clears this cycle's surfacing. New this cycle and related but not §13-gated: `BLG-GOV-391` asks the same owner for a §8 determination on rebalance exits.

## STEP 8.5 — Stateless Write Safety Gate

### 8.5.A — Re-anchored decisions

1. Add a `v9.13` Now section (STEP 8.1 Option (a)) with `BLG-FE-226`, `BLG-FE-227` and `BLG-BE-182`; §1 Next planned release → v9.13.
2. File 21 backlog items from STEP 4.
3. Set 31 register rows to `Promoted-Backlog` and 1 to `Rejected`.
4. Append DL-086.
5. Append history rows (PVR; role share v9.11 + v9.12) and a workforce section.
6. Make no initiative changes.

### 8.5.B — Write plan

| File | Change | Traceable to |
|------|--------|--------------|
| `claude/roadmap/current_roadmap.md` | §1 Next planned release → v9.13; §3 v9.13 section; Last Updated / Last rebalance | (A) STEP 8.1, 8.0, §7.1, STEP 2.4 |
| `claude/backlog/backlog.md` | Append 21 items; Last Updated | (A) STEP 4 |
| `claude/roadmap/decision_log.md` | Append DL-086 (count 48 → 49, verified; prior text byte-identical) | (A) STEP 8 |
| `claude/roadmap/product_value_ratio_history.md` | Append row, refresh sparkline, reading note | (A) STEP 2.4 |
| `claude/roadmap/role_share_history.md` | Append v9.11 and v9.12 rows and breakdowns; rolling line | (A) §7.2 |
| `claude/roadmap/workforce_capacity.md` | Append "Rebalance 2026-10-16__scheduled" section | (A) STEP 7 |
| `claude/ideas/ideas_register.md` | 32 rows → terminal status | (A) STEP 4.2 |
| `claude/ideas/ideas_window.json`, `window_summary_IW-20261016-01.md` | Intake window (committed separately, intake STEP 5, `e20ac8a3`) | STEP -1.6 |
| `claude/cycles/2026-10-16__scheduled/*` | run_manifest, cycle_record, cycle_summary, lessons_learnt, escalations, meta_review | Process |
| `.claude_current_state.json` | Rebalance keys (STEP 12) | Process |

Written before this plan, in its own commit (`d424ea68`), at STEP -1.5: `roadmap_prompt.md`, `roadmap_prompt_appendix.md`, `release_planning_prompt.md`, `OPERATIONAL_GUIDE.md`, `prompt_change_log.md`, two per-file changelogs, `claude/roadmap/ready_pool_history.md`. These are the OVERDUE patch applications (Head of Specs Team, user-directed, `ESC-RB-20261016-01`), within §4's `claude/system/*` and `claude/roadmap/ready_pool_history.md` scope.

**Register row status verification:** no `Advancing` rows, so nothing needs a terminal status.

**BLG-ID collision advisory:** highest IDs across `backlog.md` + `backlog_archive.md` before this run: `BLG-FE-225`, `BLG-BE-181`, `BLG-QA-226`, `BLG-SPEC-203`, `BLG-SEC-42`, `BLG-OPS-189`, `BLG-GOV-390`. New IDs start at highest+1. No collision.

### 8.5.C / D — Verification

Every file in the plan is within §4 write scope. The decision log is append-only (count verified 48 → 49, no prior text changed). No formatting-only edits. Every write traces to (A). **PASS.**

### 9.0 — Net-Zero Displacement

Additions (✅ Advance) 0; confirmed kills 0. 0 ≤ 0, **passes**.

**Post-write checks:** `scripts/check_backlog_item_integrity.py` passes on `backlog.md`. No park counts exist this cycle, so the park-count grep is not applicable.
