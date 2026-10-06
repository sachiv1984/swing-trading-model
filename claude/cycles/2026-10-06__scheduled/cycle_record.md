**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Complete
**Last Updated:** 2026-10-06

---

# Cycle Record — Roadmap Rebalance `2026-10-06__scheduled`

## STEP 1 — Run Manifest & Capacity Release Registration

See `run_manifest.md` (this cycle folder). Scheduled run — no Capacity Release Registration (STEP 1.2 is completion-triggered only).

---

## STEP 2 — Roadmap Re-Validation

**Active initiatives: 0** (unchanged since 2026-04-03 — 16th consecutive cycle with 0 active initiatives). No initiative to classify 🔥/⚠/❌.

### 2.1–2.2 Strategy Proximity Score / CPS

No active initiatives → **CPS = N/A**. No delta, no absolute alert.

### Horizon Review

**Now horizon:** empty at run start (since 2026-07-27). This run adds a `v9.10` section holding backlog items committed to the next release (STEP 8.0 fast-track and the §7.1 pull-forward — see STEP 8). These are not Arc initiatives and no Arc moves horizon.

**Next horizon (Arcs 1 & 2):** both complete — no promotion candidates.

**Later horizon (Arcs 3–6), re-checked gate by gate:**
- **SI-02 (Behavioural Drift Detection):** `**Last formally confirmed:**` re-read — **20 total closed trades / 0 linked trade plans — gate NOT MET.** No live re-check attempted: no production API credential is present in this checkout, and the sandbox `DATABASE_URL` targets staging (context only, never a production confirmation per §2.3) and was not queried. Cited unchanged.
- **PO-02 (Journal Pattern Recognition), data-density gate:** estimated clearance ~2026-10-20 (14 days out) — not reached; not re-verified live (no production access). Carried forward.
- **SI-04 / PO-03 / PO-04 / Arc 6 (PS-01–05):** gated on trade-count/history thresholds far above current data — no change.

**Standing operating-mode note (§2.3, v9.20) applies:** "no movements warranted" for a re-checked data-gate reason. 10 consecutive releases (v8.9–v9.9) shipped backlog-driven.

---

## STEP 2.4 — Product Value Ratio Diagnostic

**Window:** last 5 completed cycles, v9.5–v9.9. Tags read directly from `docs/product/changelog.md` `[U|G|D|P]` inline tags; cross-checked with `scripts/compute_rebalance_diagnostics.py` (same totals).

| Release | U | G | D | P | Total |
|---------|---|---|---|---|-------|
| v9.5 | 0 | 10 | 30 | 3 | 43 |
| v9.6 | 8 | 6 | 18 | 0 | 32 |
| v9.7 | 5 | 8 | 15 | 0 | 28 |
| v9.8 | 2 | 10 | 27 | 0 | 39 |
| v9.9 | 2 | 9 | 24 | 0 | 35 |
| **Total** | **17** | **43** | **114** | **3** | **177** |

**user_value_ratio = 17 ÷ 177 = 0.096 — 🔴 Product Value Alert (< 0.30), 6th consecutive Alert-tier reading** (0.110, 0.092, 0.046, 0.089, 0.094, now 0.096). Flat. v9.9's 2 U-stories were ST-01 (`BLG-BE-135`) and ST-35 (`BLG-FE-192`).

**Challenger Product Velocity Concern:** raised. Ratio 0.096, window as above; the last 5 releases averaged 3.4 U-stories each. Proposed pull-forward: `BLG-FE-193` (gate met this cycle) and this cycle's ExitModal item (`BLG-FE-198`).

**PO written response (mandatory): Modify.** Unlike the prior two readings, the response is a commitment: `BLG-FE-193` and `BLG-FE-198` are placed in a new `v9.10` Now-horizon section (STEP 8). Both passed the LP-05 gate check and the live-status cross-check (STEP 8.2). Further ungated build-and-ship candidates from this cycle's intake (`BLG-FE-196`, `BLG-FE-197`, `BLG-FE-199`; `BLG-FE-195` once `BLG-BE-138`'s ruling lands) are left to Release Planning's ready-pool process.

**Structured history:** row appended to `claude/roadmap/product_value_ratio_history.md` (`DL-083`).

---

## STEP 3 — Backlog Health Review

185 active backlog items at run start (after `groom backlog` 2026-10-06 and one session-added item, `BLG-TECH-21`). 211 after this run's writes (+25 intake items, +`BLG-GOV-375`). No obsolete/duplicate tagging beyond STEP 3.1.

### STEP 3.1 — Actionable Backlog Assessment

**Method:** structural heuristic (185 ≥ 150 items, v9.1), script-assisted: `scripts/scan_backlog_gate_conditions.py --as-of 2026-10-06` for the gate list and date-lapse flags; T/D/L split by the v9.1 keyword rule over each `**Gate criteria:**` line.

1. **A vs gated:** 61 items without a `**Gate criteria:**` field → **A**; 124 with one → gated. (The scan script reports 123 gated / 62 ungated — it treats one gate field reading as resolved; the 1-item difference does not change any threshold.)
2. **T/D/L of gated items:** T = 13, D = 22, L = 89.
3. **Date-lapse re-check (v9.25):** the scan flagged 7 items. **2 excluded as known false positives** (3rd consecutive rebalance): `BLG-OPS-53` (matched the 2026-05-22 ship date; real target ~Nov 2026 → stays T) and `BLG-FEAT-92` (matched a provenance note; gate inherited from `BLG-FEAT-30` → stays D). Allow-list filed as `BLG-GOV-373`.

   **5 genuinely date-lapsed** → reclassified **A (date-lapsed — verify)**:

| BLG-ID | Title | Latest gate date | Remaining non-date condition |
|--------|-------|-------------------|-------------------------------|
| `BLG-FEAT-55` | AI chat history persistence | 2026-07-25 | §13 review for chat persistence not opened |
| `BLG-SPEC-65` | AI interaction history data model | 2026-07-25 | Same §13 review |
| `BLG-GOV-121` | SI-05 Phase 2 §13 pre-clearance document | 2026-07-04 | Phase 2 activation decision not found |
| `BLG-FEAT-62` | `setup_type` preset justification | 2026-06-23 | ≥20 closed trades with ≥3 setup types × ≥3 trades — not confirmed |
| `BLG-OPS-92` | Dependency update review | 2026-10-06 | None — quarterly cadence date reached today; ready to schedule |

   The 8-item AI-review cluster flagged at the last two rebalances is gone from the lapsed list: v9.9 ST-19 conducted the review (`docs/ops/ai_feature_usage_review_2026-09-24.md`) and cleared or re-gated each item.

**Revised counts:** **A = 66** (35.7% of 185), **T = 9**, **D = 21**, **L = 89**. **Backlog Accessibility Warning:** 35.7% ≥ 30% → not triggered.

**D-gated example:** PO-02 cluster (`BLG-BE-28/31/43`, `BLG-FEAT-58`, `BLG-SPEC-35/36/55`, `BLG-FE-72`) — estimated clearance ~2026-10-20, unchanged.

**L-gated top 5 by priority:** the Arc-5 P1 frontend-spec cluster (`BLG-FE-43/45/54/58/59`), all gated on SI-02/SI-04/SI-05 sprint entry. No new archive candidates (none has a stated condition > 12 months away).

**STEP 8.0.5 pre-clean (call site 1):** this run compiled no STEP 3 horizon-candidate list from the existing backlog; the v9.10 items were chosen at STEP 8 and verified at STEP 8.2.

---

## STEP 4 — Ideas

**Pre-clean:** `run ideas housekeeping` already ran at `2026-09-30__release-v9.9` post-ship closure STEP 12.5 (register header confirms 5 rows archived 2026-10-06) — skipped.

**Loaded rows:** 0 parked; 44 `Submitted` from this run's inline window `IW-20261006-01` (full 22-role roster — see `run_manifest.md` STEP -1.6 and `claude/ideas/window_summary_IW-20261006-01.md`).

### Gate-Condition Re-Check

No parked ideas → no idea-level re-check. **Backlog-level re-check carried from the v9.9 closure (Carry-Forward #2):** `BLG-FE-193`'s gate names `BLG-BE-135`; `BLG-BE-135` is absent from `backlog.md` and present in `backlog_archive.md` (shipped v9.9, ST-01) → **gate met.** Recorded on the item; `BLG-FE-193` committed to v9.10 (STEP 8). `BLG-FEAT-59`'s gate was removed by Product Owner decision on 2026-10-05 (item text) — available to Release Planning.

### 4.1–4.2 Classification and Document Management

PO classification of all 44 submissions. No idea was classified ✅ Advance: each sound idea is backlog-sized work with no Arc-initiative shape, so each is filed directly as 📋 Backlog, matching the multi-cycle pattern. 11 consolidations under the v9.0 convention (genuine shared scope: same mechanism, same file, or same target item). No park was used, so the Facilitator park-rationale gate did not engage.

| Idea ID | Classification | Backlog item |
|---------|----------------|--------------|
| `IDEA-ai-compliance-20261006-01` | 📋 Backlog (ungated) | `BLG-BE-142` |
| `IDEA-ai-compliance-20261006-02` | 📋 Backlog (ungated) | `BLG-BE-141` |
| `IDEA-api-contracts-20261006-01` | 📋 Backlog (ungated) | `BLG-SPEC-187` (consolidated, 2 ideas) |
| `IDEA-api-contracts-20261006-02` | 📋 Backlog (ungated) | `BLG-SPEC-187` (consolidated, 2 ideas) |
| `IDEA-backend-engineering-20261006-01` | 📋 Backlog (ungated) | `BLG-BE-139` (consolidated, 2 ideas) |
| `IDEA-backend-engineering-20261006-02` | 📋 Backlog (ungated) | `BLG-BE-138` (consolidated, 5 ideas) |
| `IDEA-base44-frontend-20261006-01` | 📋 Backlog (gate-conditional) | `BLG-FE-195` (consolidated, 4 ideas) |
| `IDEA-base44-frontend-20261006-02` | 📋 Backlog (ungated) | `BLG-GOV-369` (consolidated, 3 ideas) |
| `IDEA-challenger-20261006-01` | ❌ Reject — not strong | — |
| `IDEA-challenger-20261006-02` | ❌ Reject — not strong | — |
| `IDEA-cybersecurity-20261006-01` | 📋 Backlog (ungated) | `BLG-SEC-41` |
| `IDEA-cybersecurity-20261006-02` | 📋 Backlog (ungated) | `BLG-SEC-42` |
| `IDEA-data-model-20261006-01` | 📋 Backlog (ungated) | `BLG-BE-139` (consolidated, 2 ideas) |
| `IDEA-data-model-20261006-02` | 📋 Backlog (ungated) | `BLG-SPEC-186` (consolidated, 2 ideas) |
| `IDEA-director-of-hr-20261006-01` | 📋 Backlog (ungated) | `BLG-GOV-372` |
| `IDEA-director-of-hr-20261006-02` | 📋 Backlog (ungated) | `BLG-GOV-369` (consolidated, 3 ideas) |
| `IDEA-director-of-quality-20261006-01` | 📋 Backlog (ungated) | `BLG-GOV-370` |
| `IDEA-director-of-quality-20261006-02` | 📋 Backlog (gate-conditional) | `BLG-OPS-179` |
| `IDEA-financial-reporting-20261006-01` | 📋 Backlog (gate-conditional) | `BLG-FEAT-99` |
| `IDEA-financial-reporting-20261006-02` | 📋 Backlog (ungated) | `BLG-FR-06` |
| `IDEA-finops-20261006-01` | 📋 Backlog (ungated) | `BLG-BE-140` (consolidated, 2 ideas) |
| `IDEA-finops-20261006-02` | 📋 Backlog (ungated) | `BLG-GOV-371` (consolidated, 2 ideas) |
| `IDEA-frontend-specs-20261006-01` | 📋 Backlog (ungated) | `BLG-FE-197` (consolidated, 2 ideas) |
| `IDEA-frontend-specs-20261006-02` | 📋 Backlog (ungated) | `BLG-FE-196` (consolidated, 2 ideas) |
| `IDEA-head-of-engineering-20261006-01` | 📋 Backlog (ungated) | `BLG-BE-138` (consolidated, 5 ideas) |
| `IDEA-head-of-engineering-20261006-02` | 📋 Backlog (ungated) | `BLG-BE-140` (consolidated, 2 ideas) |
| `IDEA-head-of-specs-20261006-01` | 📋 Backlog (ungated) | `BLG-SPEC-185` (consolidated, 2 ideas) |
| `IDEA-head-of-specs-20261006-02` | 📋 Backlog (ungated) | `BLG-GOV-369` (consolidated, 3 ideas) |
| `IDEA-head-of-ux-20261006-01` | 📋 Backlog (ungated) | `BLG-FE-196` (consolidated, 2 ideas) |
| `IDEA-head-of-ux-20261006-02` | 📋 Backlog (gate-conditional) | `BLG-FE-195` (consolidated, 4 ideas) |
| `IDEA-infra-ops-20261006-01` | 📋 Backlog (ungated) | `BLG-BE-138` (consolidated, 5 ideas) |
| `IDEA-infra-ops-20261006-02` | 📋 Backlog (ungated) | `BLG-GOV-371` (consolidated, 2 ideas) |
| `IDEA-metrics-20261006-01` | 📋 Backlog (ungated) | `BLG-SPEC-186` (consolidated, 2 ideas) |
| `IDEA-metrics-20261006-02` | 📋 Backlog (ungated) | `BLG-SPEC-188` |
| `IDEA-pmo-lead-20261006-01` | 📋 Backlog (ungated) | `BLG-GOV-373` |
| `IDEA-pmo-lead-20261006-02` | 📋 Backlog (ungated) | `BLG-GOV-374` |
| `IDEA-product-owner-20261006-01` | 📋 Backlog (ungated) | `BLG-FE-198` |
| `IDEA-product-owner-20261006-02` | 📋 Backlog (ungated) | `BLG-FE-199` |
| `IDEA-qa-lead-20261006-01` | 📋 Backlog (gate-conditional) | `BLG-FE-195` (consolidated, 4 ideas) |
| `IDEA-qa-lead-20261006-02` | 📋 Backlog (gate-conditional) | `BLG-FE-195` (consolidated, 4 ideas) |
| `IDEA-qa-testing-20261006-01` | 📋 Backlog (ungated) | `BLG-BE-138` (consolidated, 5 ideas) |
| `IDEA-qa-testing-20261006-02` | 📋 Backlog (ungated) | `BLG-FE-197` (consolidated, 2 ideas) |
| `IDEA-strategy-owner-20261006-01` | 📋 Backlog (ungated) | `BLG-BE-138` (consolidated, 5 ideas) |
| `IDEA-strategy-owner-20261006-02` | 📋 Backlog (ungated) | `BLG-SPEC-185` (consolidated, 2 ideas) |

**Rejections (Facilitator check — rationale specific, not vague):**
- `IDEA-challenger-20261006-01` (STEP 8.1 soft gate always resolved by Option (b)): not strong — this run's STEP 8.0 promotion adds a v9.10 section, so STEP 8.1 resolves differently once evidence changes; the earlier streak is explained by the v9.20 operating-mode note.
- `IDEA-challenger-20261006-02` (prioritise strategy-behaviour conformance in debt slices): not strong — absorbed; this run commits that work directly (`BLG-BE-138` fast-tracked, `BLG-FE-196/197/198` filed).

**Consolidations:** `BLG-BE-138` (5 ideas), `BLG-FE-195` (4), `BLG-GOV-369` (3), `BLG-BE-139`, `BLG-BE-140`, `BLG-FE-196`, `BLG-FE-197`, `BLG-SPEC-185`, `BLG-SPEC-186`, `BLG-SPEC-187`, `BLG-GOV-371` (2 each). Each item's `**Source:**` lists every contributing idea; each register row's Step 4 column names the item.

**Gate-conditional filings:** `BLG-FE-195` (on `BLG-BE-138`'s ruling), `BLG-OPS-179` (on `BLG-BE-138`), `BLG-FEAT-99` (on `BLG-SPEC-186`) — each a named sibling dependency, not a date or data-density gate.

**Priority:** `BLG-BE-138` filed **P1** (correctness — see STEP 8.0). P2: `BLG-BE-139`, `BLG-FE-195/196/197/198/199`, `BLG-SPEC-185`, `BLG-SPEC-187`. P3: the rest.

### 4.3 Idea Participation Check

22 of 22 eligible roles submitted 2 each (Facilitator excluded by design). No innovation-debt note.

### 4.4 Write Summary

Window summary: `claude/ideas/window_summary_IW-20261006-01.md`. **STEP 5 Debate Queue:** empty. Queue row count (0) equals "Advancing to STEP 5" count (0) — consistent.

### 4.5 Parked Idea Expiry

No parked ideas exist before or after this run.

### Submission Details (full template fields — `IW-20261006-01`)

#### IDEA-ai-compliance-20261006-01 — Pin every Claude model ID in one backend module; two call sites use the floating `claude-haiku-4-5` alias while `ai_service.py` pins `claude-haiku-4-5-20251001`
*Submitter:* AI Compliance & Governance Officer
- **Problem Statement:** Model IDs are literal strings in 4 backend files. `ai_service.py` pins `claude-haiku-4-5-20251001`, but `debrief_service.py` and `gemini_service.py` call the unpinned alias `claude-haiku-4-5`, so those two features can change model version without any code change, and the BLG-GOV-90 deprecation procedure has no single place to check.
- **Strategic Alignment:** §13.1/§13.2 — advisory-only AI behaviour must stay stable and reviewable; an unpinned alias lets the model behind an advisory surface change silently.
- **Proposed Solution:** Create one module (e.g. `backend/services/ai_models.py`) holding every model ID as a pinned constant; import it at all 4 call sites; add a unit test that fails on any `claude-` literal outside that module.
- **Expected Value:** Model literals outside one module: 4 files → 0. Unpinned aliases in production code: 2 → 0.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: refines archived `BLG-GOV-90` (deprecation monitoring procedure, shipped v9.6), which inventories models but did not pin or centralise them. Code: confirmed 4 literal sites (`routers/ai.py:175`, `ai_service.py:48-49,144`, `debrief_service.py:53`, `gemini_service.py:45`); no central module exists.

#### IDEA-ai-compliance-20261006-02 — AI daily briefing and chat should state when the stop they quote was last recalculated, using v9.9's `stop_calculated_at`
*Submitter:* AI Compliance & Governance Officer
- **Problem Statement:** `ai_service.py` builds briefing/chat context from `current_stop` and emits `STOP BREACH` alerts (lines 205-222) with no indication of how fresh that stop is. v9.9 (BLG-BE-135) added `stop_calculated_at`, but the AI context does not read it, so advisory output can present a days-old stop as current.
- **Strategic Alignment:** §3 (decision support only) and §5 purpose (make downside risk visible) — an AI advisory that quotes a stop must not overstate its currency.
- **Proposed Solution:** Include `stop_calculated_at` in the per-position AI context line and instruct the model to name the recalculation time whenever it cites a stop or a breach; omit the breach alert when the stop is older than the last nightly run.
- **Expected Value:** AI stop citations carrying a recalculation time: 0% → 100% of briefing/chat responses that mention a stop.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item covers AI context freshness (grep `stop_calculated_at`, `briefing.*stop`). Code: `ai_service.py` reads `current_stop` only; `stop_calculated_at` exists on `GET /positions` since v9.9.

#### IDEA-api-contracts-20261006-01 — Correct the documented losing-position stop formula: `position_endpoints.md` and the nightly job docstring say `entry − 5×ATR`, the code and §7.2 use `current price − 5×ATR`
*Submitter:* API Contracts & Documentation Owner
- **Problem Statement:** `position_endpoints.md` line 150 documents `current_trailing_stop` as `profit → price − 2×ATR, else entry − 5×ATR`, and `run_nightly_trailing_stop_update`'s docstring says the same. The code (`utils/calculations.py::calculate_trailing_stop`) computes `current_price − mult×ATR` in both branches, which is what `strategy_rules.md` §7.2 specifies. A reader of the contract cannot reproduce a displayed stop.
- **Strategic Alignment:** §7.2 (profit-aware stop logic) and §12.3 (documentation must match live logic).
- **Proposed Solution:** Change both texts to the §7.2 formulas (including the breakeven floor), and add a contract example row that reproduces one stop from its inputs.
- **Expected Value:** Contract/code stop-formula mismatches: 2 → 0.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item names this formula text (grep `entry − 5×ATR`). Code: confirmed at `docs/specs/api_contracts/position_endpoints.md:150` and `backend/services/position_service.py:568-571`.

#### IDEA-api-contracts-20261006-02 — `GET /positions/analyze` contract says 'safe to refresh' and settings changes 'do not affect open positions'; the endpoint actually rewrites stops for every open position using the current settings
*Submitter:* API Contracts & Documentation Owner
- **Problem Statement:** `position_endpoints.md` §GET /positions/analyze states 'Idempotency: Safe to refresh. Deterministic recomputation on every call.' `settings_endpoints.md` states multiplier changes 'take effect on the next call to GET /positions/analyze. Open positions are not retroactively affected.' In code, `analyze_positions()` recomputes and persists `current_stop` for all open positions with the current settings multipliers, and the 7.3 ratchet makes any tightening permanent — so a settings change does retroactively affect open positions, irreversibly.
- **Strategic Alignment:** §7.3 (stops never move down — a ratcheted write is irreversible) and §12.3 (documentation must match live logic).
- **Proposed Solution:** Rewrite both contract sections to state the side effects (persisted stop, timestamps, ratchet) and that the nightly job ignores settings; cross-reference whatever single-source ruling BLG-BE-138 reaches.
- **Expected Value:** Undocumented state-changing behaviour on a GET endpoint: 1 → 0.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: `BLG-API-04` (archived, idempotency sweep v9.8) covered mutating POSTs, not this GET. Code: confirmed writes in `position_service.py::analyze_positions` (stop and `stop_calculated_at`).

#### IDEA-backend-engineering-20261006-01 — Remove the silent ATR fallbacks: `add_position` invents ATR as 2% of entry, and `analyze_positions` sets a losing position's stop to its entry price when ATR is missing
*Submitter:* Backend Engineering Patterns Owner
- **Problem Statement:** When ATR cannot be fetched, `add_position` uses `entry_price × 0.02` and stores the resulting §5 stop with no flag. Separately, `analyze_positions` falls back to `stop = max(current_stop, entry)` when ATR is missing, which for a losing position places the stop above the current price and produces a stop-breach signal that §7.2's wide-stop rule would never produce.
- **Strategic Alignment:** §5 (initial stop from a real ATR) and §7.2 (losing positions keep a wide stop).
- **Proposed Solution:** Record how each position's ATR was obtained; when ATR is missing, keep the last stored stop instead of jumping to entry, and surface 'ATR unavailable' on the position rather than a breach.
- **Expected Value:** Positions whose stop can jump to entry because of a data outage: all → 0.
- **Effort Estimate:** Medium (1–3 weeks) · **Reversibility:** Mostly reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item names either fallback (grep `2% of entry`, `stop at entry`, `atr_source`). Code: `position_service.py` add_position ATR block and `analyze_positions` 'No ATR - stop at entry' branch.

#### IDEA-backend-engineering-20261006-02 — Consolidate the grace-period length: it is hardcoded as 10 in four places and also read from the user-editable `settings.min_hold_days` (form default 5) by the alerts service
*Submitter:* Backend Engineering Patterns Owner
- **Problem Statement:** §6.2 fixes the grace period at 10 calendar days. The value is a literal in `compliance_service.py` (`GRACE_PERIOD_DAYS = 10`), `grace_service.py`, `should_exit_position(grace_period_days=10)`, and the lifecycle service (10 *trading* days), while `alerts_service.py` reads `settings.min_hold_days`, which the Settings form defaults to 5 and labels 'Days before stop can trail'.
- **Strategic Alignment:** §6.2 (grace period: 10 calendar days) and §11 (parameters consistent across live logic).
- **Proposed Solution:** One `GRACE_PERIOD_DAYS` constant imported everywhere; decide (with BLG-BE-138's ruling) whether `min_hold_days` is retired or bound to it.
- **Expected Value:** Independent grace-length sources: 5 → 1.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `GRACE_PERIOD_DAYS`, `min_hold_days`). Code: confirmed at the five sites named.

#### IDEA-base44-frontend-20261006-01 — Settings › Strategy Parameters shows wrong defaults (2×/3× ATR, 5 hold days) and helper text that contradicts §7.2
*Submitter:* Base44 Frontend Prompt Owner · **build-and-ship candidate (§2.1 step 2a)**
- **Problem Statement:** Surface: `src/pages/Settings.js`. When no settings row exists the form pre-fills `atr_multiplier_initial: 2`, `atr_multiplier_trailing: 3`, `min_hold_days: 5` (§11: 5, 2, 10), and saving writes them. Helper text says 'Entry − 5×ATR' for the losing stop and 'High − 2×ATR' for the profitable one; §7.2 and the code use the current price, with a breakeven floor. The page contradicts what the system does.
- **Strategic Alignment:** §7.2 (formulas), §11 (production parameters) and §12.3 (change control) — a parameter page must not advertise or seed non-production values.
- **Proposed Solution:** Set the fallback defaults to §11 values, rewrite the helper text to the §7.2 formulas, and mark the section as governed by §12 (read-only or with a divergence warning, per BLG-BE-138's ruling).
- **Expected Value:** Settings defaults matching §11: 0 of 3 → 3 of 3. Helper-text formula errors: 2 → 0.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `Settings.js` hits only BLG-FE-171 aria-labels). Code: confirmed at `Settings.js:42-46`, `:231`, `:243`.

#### IDEA-base44-frontend-20261006-02 — Put strategy numbers the UI displays in one frontend constants module instead of literals in each page
*Submitter:* Base44 Frontend Prompt Owner
- **Problem Statement:** Strategy values are hard-coded per file: `TradeEntry.js` (fallback 2×), `Settings.js` (2×/3×/5), `Positions.js` ('ATR × 2.0', '10 trading days'), `SignalContextPanel.js` ('entry − 5×ATR'). Each Base44 prompt revision has to restate them, and they have already drifted apart.
- **Strategic Alignment:** §11 — parameters must be consistent across live logic and what the user is shown.
- **Proposed Solution:** Add `src/constants/strategy.js` mirroring §11; replace the literals; reference the module in Base44 prompt drafts.
- **Expected Value:** Strategy-number literals across `src/`: ≥7 → 0 outside the module.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `constants`, `strategy constants`). Code: no `src/constants` directory exists.

#### IDEA-challenger-20261006-01 — Challenge: STEP 8.1's empty-Now-horizon soft gate has been cleared with Option (b) 'defer' 8 times running — is it still forcing a decision, or recording a default?
*Submitter:* Challenger
- **Problem Statement:** From `2026-08-11__scheduled` to `2026-09-30__scheduled`, every rebalance recorded Option (b) with near-identical rationale. A gate that always resolves the same way may no longer be doing work.
- **Strategic Alignment:** §3 (human decision support) applies by analogy to governance — a gate that never changes the outcome adds cost without decision value.
- **Proposed Solution:** Either retire STEP 8.1 while the v9.20 backlog-driven operating-mode note applies, or require Option (b) to name the specific evidence that would flip it to (a).
- **Expected Value:** Rebalance minutes spent on a non-discriminating gate: ~2-3 per run → 0.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item on STEP 8.1's discrimination (grep `Option (b)` hits only roadmap headers). Not a code topic.

#### IDEA-challenger-20261006-02 — Challenge: nine debt-clearance releases did not catch that the Settings page can seed 2×/3× ATR into live stops — debt slices should prioritise strategy-behaviour conformance over governance paperwork
*Submitter:* Challenger
- **Problem Statement:** v8.9–v9.9 were all debt-heavy (Skill-Silo 83–99%), yet a one-file read of `Settings.js` this window found defaults contradicting §11 that the on-load stop path consumes. The debt being cleared is mostly governance and documentation, not behaviour.
- **Strategic Alignment:** §1 — where code or UI conflicts with this document, this document prevails; conformance is the highest-value debt.
- **Proposed Solution:** The next release's debt slice should rank strategy-behaviour conformance items (stop math, grace, exit conditions) ahead of governance-process items.
- **Expected Value:** Conformance defects found per release: currently 0 by design (none sought) → measurable.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item states this prioritisation rule. Not a code topic.

#### IDEA-cybersecurity-20261006-01 — Audit trail for strategy-parameter changes in Settings — who changed a multiplier, when, from what, to what
*Submitter:* Cybersecurity & Trust Lead
- **Problem Statement:** `POST/PATCH /settings` overwrites ATR multipliers and hold days in place. Those values drive the on-load stop recompute, and the §7.3 ratchet makes the effect permanent, but no record of the change exists. A tightened stop cannot be traced back to a settings edit.
- **Strategic Alignment:** §12.3 (change control: explicit, versioned) and §7.3 (irreversible ratchet).
- **Proposed Solution:** Append a `settings_change_log` row (field, old, new, timestamp, request source) on every settings write; show the last change on the Settings page.
- **Expected Value:** Untraceable strategy-parameter changes: all → 0.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Mostly reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog/archive: no item (grep `settings change`, `settings audit`). Code: `database.py::create_settings`/update write in place with no history.

#### IDEA-cybersecurity-20261006-02 — Re-assess the 'low-sensitivity' classification of the bundled `REACT_APP_API_KEY` now that it authorises writes that move live stops
*Submitter:* Cybersecurity & Trust Lead
- **Problem Statement:** `credential_policy.md` line 34 classes the frontend key as 'a low-sensitivity authentication token'. The same key authorises `POST /settings`, position entry/exit and `GET /positions/analyze` (which writes stops). Anyone who reads the bundle can change the parameters that set the user's stops.
- **Strategic Alignment:** §3 (system provides decision support; the user executes) — integrity of the displayed stop is part of that support.
- **Proposed Solution:** Re-rate the key against its actual write scope; either scope a read-mostly frontend key or record an explicit accept-risk with the Product Owner.
- **Expected Value:** Credential classifications that understate write scope: 1 → 0.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item re-rates the frontend key (grep `REACT_APP_API_KEY`). Docs: `credential_policy.md:34`, `api_key_security_register.md` (rotation only).

#### IDEA-data-model-20261006-01 — Record how each position's ATR was obtained (`atr_source`: fetched / user-entered / fallback) so invented ATRs are visible
*Submitter:* Data Model & Domain Schema Owner
- **Problem Statement:** `positions.atr_value` stores fetched, user-typed and invented (2% of entry) values identically. Analytics, stop audits and BLG-FE-193's ATR display cannot tell them apart.
- **Strategic Alignment:** §4 (ATR required at entry) and §5 (stop derived from ATR).
- **Proposed Solution:** Add `positions.atr_source` (enum, nullable for history), written by `add_position` and the recompute paths; expose it on `GET /positions`.
- **Expected Value:** Positions with unknown ATR provenance: all → 0 for new positions.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Mostly reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `atr_source`, `provenance` hits BLG-SPEC-173, which annotates columns in docs, not this field). Code: no such column in `database.py`.

#### IDEA-data-model-20261006-02 — Constrain `exit_reason` to a defined set mapped to §8's three exit conditions
*Submitter:* Data Model & Domain Schema Owner
- **Problem Statement:** `exit_reason` is free text. The UI offers 6 values (`ExitModal.js`), legacy rows hold snake-case variants, and `TradeHistoryTable.js` keeps an alias map to cope. §8 says a position exits under exactly three conditions; 'Target Reached', 'Trailing Stop' and 'Partial Profit Taking' have no stated mapping.
- **Strategic Alignment:** §8 (exactly three exit conditions).
- **Proposed Solution:** Define the allowed values and their §8 category in `data_model.md`; backfill legacy variants; add a CHECK constraint.
- **Expected Value:** Distinct stored exit_reason spellings: ≥10 → the defined set.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Mostly reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `exit_reason enum`, `exit reason taxonomy`: 0). Code: confirmed in `ExitModal.js:356-361`, `TradeHistoryTable.js:86-98`.

#### IDEA-director-of-hr-20261006-01 — Add a split-credit secondary tally to `compute_role_share_history.py` — at v9.9 every one of 35 stories had a compound Owner string, so the raw tally names no single role
*Submitter:* Director of HR
- **Problem Statement:** The raw-tally method counts each compound Owner string as its own bucket. At v9.9 all 35 stories were compound (top bucket 'Director of Quality; QA & Testing Owner', 25.7%), so §7.2 can no longer see whether one person-role is carrying the load.
- **Strategic Alignment:** §12.3 by analogy — a metric must measure what it claims; workforce balance is the stated purpose of §7.2.
- **Proposed Solution:** Keep the raw tally as primary; add a secondary column splitting each compound story's credit equally across its named roles.
- **Expected Value:** Cycles where §7.2 can identify a top single role: 0 of 1 (v9.9) → every cycle.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: refines the deferred Owner-field canonicalisation patch (`shared_standards.md §16.11`, condition-gated) and `BLG-GOV-353` (shipped v9.9) — neither adds a split tally. Code: script has no split mode.

#### IDEA-director-of-hr-20261006-02 — Name an owner for checking that UI copy restating strategy rules matches `strategy_rules.md`
*Submitter:* Director of HR
- **Problem Statement:** No role charter assigns responsibility for UI text that restates §5–§11 (helper text, tooltips, alerts). This window found four such texts that contradict the canonical rules, none caught by any role's normal review.
- **Strategic Alignment:** §1 — the strategy document prevails over the UI; someone has to check.
- **Proposed Solution:** Add the duty to one charter (Frontend Specifications & UX Documentation Owner proposed) and link it to the lint in BLG-GOV-369.
- **Expected Value:** Roles accountable for strategy-copy conformance: 0 → 1.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `conformance`, `strategy copy`). Not a code topic.

#### IDEA-director-of-quality-20261006-01 — Add a DoQ sign-off line for stories that touch stop math or strategy parameters: values checked against §5–§11
*Submitter:* Director of Quality
- **Problem Statement:** The DoQ sign-off block has no item requiring a check of stop, grace or parameter values against `strategy_rules.md`. v9.9 ST-01 (ATR consolidation) passed without anyone noticing the on-load path reads user-editable multipliers.
- **Strategic Alignment:** §11 (parameters consistent across live logic, backtests and reporting).
- **Proposed Solution:** Add one conditional DoQ line: 'If this story touches stop, grace, ATR or exit logic: values and formulas checked against §5–§11 (cite sections).'
- **Expected Value:** Stop-touching stories with an explicit strategy-conformance check: 0% → 100%.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `DoQ.*strategy`). Not a code topic.

#### IDEA-director-of-quality-20261006-02 — Post-deploy synthetic check: every post-grace open position reports a non-null stop and an `active_atr_multiplier` in the §11 set
*Submitter:* Director of Quality
- **Problem Statement:** v9.9 exposed `active_atr_multiplier` and `stop_calculated_at` on `GET /positions`. Nothing checks them after deploy, so a regression to a non-§11 multiplier or a missing stop would only be noticed by the user.
- **Strategic Alignment:** §11 (production parameters) and §5 (stop exists from day one).
- **Proposed Solution:** Extend the existing synthetic monitor to assert the two conditions and alert via the current Telegram path.
- **Expected Value:** Detection time for a non-§11 live multiplier: unbounded → ≤1 day.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `active_atr_multiplier` hits only BLG-QA-204, a unit-test mock gap). Code: synthetic monitor does not read these fields.

#### IDEA-financial-reporting-20261006-01 — Monthly P&L breakdown by §8 exit condition (stop / risk-off / manual)
*Submitter:* Financial Reporting & Records Owner
- **Problem Statement:** Monthly P&L cannot say how much was lost to stop exits versus risk-off exits versus discretionary exits, which is the basic question for judging whether §7/§8 are working. The data exists (`exit_reason`) but is inconsistent until BLG-SPEC-186 lands.
- **Strategic Alignment:** §8 (three exit conditions) and §10 (risk management summary).
- **Proposed Solution:** Add a per-month table of realised P&L and count by §8 category to the Monthly P&L report.
- **Expected Value:** Months where exit-condition P&L is visible: 0 → all.
- **Effort Estimate:** Medium (1–3 weeks) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `P&L by exit`, `exit condition`). Code: `Reports.js` has no exit-reason grouping.

#### IDEA-financial-reporting-20261006-02 — Snapshot the strategy parameters in force onto each closed trade so historical P&L stays attributable if §11 values change
*Submitter:* Financial Reporting & Records Owner
- **Problem Statement:** A closed trade records prices and fees but not the multipliers and grace length that produced its stops. If settings or §11 change, past results can no longer be tied to the rules that generated them. v9.9 added `active_atr_multiplier` on open positions only.
- **Strategic Alignment:** §12.3 (changes explicit and versioned; backtests, live and reports consistent).
- **Proposed Solution:** On exit, copy the active multiplier, ATR, grace length and parameter source into the trade-history row.
- **Expected Value:** Closed trades with reproducible stop parameters: 0% → 100% from ship.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Mostly reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: refines v9.9 `BLG-BE-135` (open positions only). Code: trade-history write in `position_service.py::exit_position` carries no parameter fields.

#### IDEA-finops-20261006-01 — Stop page views from triggering a full price/ATR fetch and stop rewrite: `MarketRegime.list` calls `GET /positions/analyze` just to read the regime
*Submitter:* FinOps & Resource Architect
- **Problem Statement:** `base44Client.js:315` implements `MarketRegime.list` by calling `/positions/analyze`, which fetches live prices and ATR for every open position and writes stops. Any page that shows regime pays that external-API cost and side effect.
- **Strategic Alignment:** §8.2 (regime is read-only context) and §13.1 (decision support, not hidden automation).
- **Proposed Solution:** Serve regime from a read-only endpoint (or the cached nightly value); keep analyze for explicit/daily use.
- **Expected Value:** External price/ATR calls per regime render: N positions → 0.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `MarketRegime`, `regime endpoint`). Code: no read-only regime endpoint exists (routers list only sector/screener regime views).

#### IDEA-finops-20261006-02 — Inventory the 20 scheduled GitHub workflows: owner, purpose, cron, side effects, minutes
*Submitter:* FinOps & Resource Architect
- **Problem Statement:** 20 workflows run on a schedule. No single list says what each costs or writes; two of them (`daily-snapshot.yml` 16:00 UTC, `nightly-stop-update.yml` 22:30 UTC) both write stops with different parameter sources, which nobody had noticed.
- **Strategic Alignment:** §10 (portfolio-level risk management relies on scheduled jobs behaving as specified).
- **Proposed Solution:** One table in `docs/ops/` listing every scheduled workflow with owner, cron, side effects and monthly minutes; review at each `run audit`.
- **Expected Value:** Scheduled workflows with a recorded owner and side-effect note: unknown → 20 of 20.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog/archive: none (grep `workflow inventory`, `actions minutes`). `github_actions_secrets_ownership_map.md` covers secrets, not schedules.

#### IDEA-frontend-specs-20261006-01 — Trade Entry shows a stop and risk the system will not use: the Stop Price field is ignored by the backend, and the preview uses a 2× fallback instead of §5's 5×
*Submitter:* Frontend Specifications & UX Documentation Owner · **build-and-ship candidate (§2.1 step 2a)**
- **Problem Statement:** Surface: `src/pages/TradeEntry.js`. The page collects a 'Stop Price', computes 'Risk (to stop)' from it, and sends `stop_price` — but `add_position` ignores it and stores `entry − 5×ATR` (§5). When settings have not loaded, the suggested stop uses a hard-coded 2× fallback. The ATR field is labelled '(Optional)' although §4 lists ATR as required. The risk the user sees at entry is not the risk the system then manages.
- **Strategic Alignment:** §4 (ATR required at entry) and §5 (InitialStop = Entry − InitialATRMultiplier × ATR).
- **Proposed Solution:** Show the §5 stop the backend will store (and the ATR it will use) as the authoritative preview; remove or relabel the Stop Price input; fix the fallback to §11.
- **Expected Value:** Entry-time risk figures that differ from the stored stop: every entry with a typed stop → 0.
- **Effort Estimate:** Medium (1–3 weeks) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog/archive: no item (grep `stop_price.*ignor`, `Risk (to stop)`, `TradeEntry`). Code: confirmed `TradeEntry.js:94-95,229-234,417` and `position_service.py::add_position` (stop_price parameter unused).

#### IDEA-frontend-specs-20261006-02 — Fix the UNKNOWN lifecycle tooltip: it only says 'set a stop and R-target', but UNKNOWN also appears after grace when price sits within ±0.5 ATR
*Submitter:* Frontend Specifications & UX Documentation Owner
- **Problem Statement:** `Positions.js:65` tells the user an UNKNOWN badge means a missing plan stop/R-target. `position_lifecycle_service.py` also returns UNKNOWN for any post-grace position within ±0.5 ATR of entry — a common state the tooltip misdescribes, sending the user to edit a plan that is already complete.
- **Strategic Alignment:** §9 (states are deterministic and should be explainable).
- **Proposed Solution:** Tooltip text keyed on the reason the backend returned UNKNOWN (missing ATR vs flat after grace).
- **Expected Value:** UNKNOWN tooltips giving the wrong reason: flat-after-grace cases → 0.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `UNKNOWN state`). Code: confirmed `Positions.js:65`, `position_lifecycle_service.py` final branch.

#### IDEA-head-of-engineering-20261006-01 — One source for §11 stop parameters: the on-load stop recompute reads user-editable settings (form default 2×/3×) while the nightly job hard-codes 5×/2×, and the ratchet keeps whichever is tighter
*Submitter:* Head of Engineering · **build-and-ship candidate (§2.1 step 2a)**
- **Problem Statement:** Surface: `GET /positions/analyze`, consumed by every page that renders market regime. `analyze_positions()` calls `calculate_trailing_stop(settings=<settings row>)`; `run_nightly_trailing_stop_update()` uses constants 5.0/2.0. If the settings row holds anything other than 5/2 — and the Settings form seeds 2/3 when no row exists — the on-load path writes a different stop than §7.2, and §7.3's ratchet makes a tighter one permanent. The production settings row's values could not be checked from this environment.
- **Strategic Alignment:** §7.2, §7.3, §11 ('parameters must be consistent across production backtests, live system logic, and reported performance') and §12.3.
- **Proposed Solution:** Get a Strategy Owner ruling on whether §11 parameters are user-tunable; make both paths read one source; correct the Settings/TradeEntry fallbacks; add an analyze-vs-nightly parity test; check the production settings row and correct any stop already ratcheted from non-§11 values.
- **Expected Value:** Stop-computation paths with independent parameter sources: 2 → 1. Possible non-§11 live stops: unknown → verified 0.
- **Effort Estimate:** Medium (1–3 weeks) · **Reversibility:** Mostly reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: refines `BLG-QA-204` (test does not mock `get_settings()`), which is a test-only gap. No item names the two-source divergence. Code: confirmed `position_service.py:338-341,444-451` vs `:558-581`.

#### IDEA-head-of-engineering-20261006-02 — Separate the regime read from the stop-writing analyze call, so viewing a page never moves a stop
*Submitter:* Head of Engineering
- **Problem Statement:** Page loads reach `analyze_positions()` through `MarketRegime.list`, so simply opening a page can ratchet stops. A GET with persistent side effects makes stop movements hard to attribute and test.
- **Strategic Alignment:** §7.3 (irreversible ratchet should happen at defined times) and §3.
- **Proposed Solution:** Add a read-only regime source for the UI; restrict stop writes to the nightly job and an explicit, documented refresh path.
- **Expected Value:** Stop writes triggered by page views: every regime render → 0.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Mostly reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item. Code: `base44Client.js:315` → `/positions/analyze`.

#### IDEA-head-of-specs-20261006-01 — Reconcile `position_lifecycle_states_registry.md` (5 states, trading days, ±0.5 ATR bands) with `strategy_rules.md` §9 (4 states, 10 calendar days)
*Submitter:* Head of Specs Team
- **Problem Statement:** §9 defines GRACE (days 0–9), LOSING, PROFITABLE, EXITED. The registry and `position_lifecycle_service.py` define GRACE as ≤10 *trading* days *and* within ±0.5 ATR, and add EXIT ZONE and UNKNOWN. So a position on day 3 can be shown as LOSING while §6 says its stop is inactive. Two canonical-looking documents disagree, and §1 says §9 prevails.
- **Strategic Alignment:** §1 (this document prevails), §6, §9.
- **Proposed Solution:** Strategy Owner ruling on whether the lifecycle badge is a §9 state or a separate display overlay; update the registry and, if needed, §9 under §16's change-justification template.
- **Expected Value:** Conflicting state definitions between canonical documents: 1 → 0.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog/archive: no item (grep `position_lifecycle_states_registry`: 0). Docs: registry line 25; strategy_rules §9.

#### IDEA-head-of-specs-20261006-02 — Lint that flags UI text restating strategy formulas or numbers that differ from `strategy_rules.md`
*Submitter:* Head of Specs Team
- **Problem Statement:** Four UI texts found this window contradict §5–§11. Nothing scans for them; they are found by chance.
- **Strategic Alignment:** §1 and §12.3.
- **Proposed Solution:** A script listing every `src/` string containing ATR multiples, grace lengths or stop formulas, compared against an allow-list derived from §5–§11; run in CI as a warning.
- **Expected Value:** Strategy-copy contradictions found by tooling instead of by chance: 0 → all matching the patterns.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `strategy.claim`, `copy.*strategy_rules`: 1 unrelated hit). Code: no such script in `scripts/`.

#### IDEA-head-of-ux-20261006-01 — Positions: the lifecycle badge and the Grace column disagree — a position inside §6's grace window can show a red LOSING badge, and grace copy says 'trading days' where §6 says calendar days
*Submitter:* Head of UX & Design · **build-and-ship candidate (§2.1 step 2a)**
- **Problem Statement:** Surface: `src/pages/Positions.js`. The Grace column (`grace_days_remaining`, calendar days) can say 6 days remain while the lifecycle badge shows LOSING with 'Exits when price rises above entry by 0.5 ATR', because the badge's GRACE needs price within ±0.5 ATR and counts trading days. The GRACE tooltip and the Grace Period Alert both say 'trading days'; §6 says 10 calendar days and the backend's grace window uses calendar days. The user sees two answers to 'is my stop active?'.
- **Strategic Alignment:** §6 (grace: calendar days, stop not enforced) and §9 (states mutually exclusive).
- **Proposed Solution:** While §6 grace is active, the badge shows GRACE with calendar days remaining; tooltips and the alert say calendar days; the post-grace states follow BLG-SPEC-185's ruling.
- **Expected Value:** Positions showing a grace/badge contradiction: any in-grace position outside ±0.5 ATR → 0.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `trading day`, `lifecycle badge`: 0 active). Code: confirmed `Positions.js:61-63,123,1011-1014`, `grace_service.py`, `position_lifecycle_service.py`.

#### IDEA-head-of-ux-20261006-02 — Separate governed strategy parameters from personal preferences on the Settings page
*Submitter:* Head of UX & Design
- **Problem Statement:** The Settings page puts ATR multipliers and hold days in the same editable form as theme, currency and fees, with no signal that changing them alters live stops and departs from §11.
- **Strategic Alignment:** §12 (parameter governance) and §3.
- **Proposed Solution:** Move §11 parameters into a clearly labelled 'Strategy (governed by strategy rules)' panel: read-only with values and source, or editable behind a confirmation that names the consequence, per BLG-BE-138's ruling.
- **Expected Value:** Strategy-parameter edits made without a consequence warning: all → 0.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item. Code: single `SectionCard` 'Strategy Parameters' with plain inputs.

#### IDEA-infra-ops-20261006-01 — Two scheduled jobs write `current_stop` with different parameter sources (`daily-snapshot.yml` → analyze with settings; `nightly-stop-update.yml` → constants)
*Submitter:* Infrastructure & Operations Owner
- **Problem Statement:** `daily-snapshot.yml` (16:00 UTC weekdays) curls `GET /positions/analyze`; `nightly-stop-update.yml` (22:30 UTC) runs the constant-based job. With the §7.3 ratchet, the final stop each day is the tighter of the two, so the effective parameter set depends on job order and on the settings row.
- **Strategic Alignment:** §7.3 and §11.
- **Proposed Solution:** Have one scheduled writer of stops per day, or make both read the single source BLG-BE-138 establishes; document the order.
- **Expected Value:** Scheduled stop writers with differing parameter sources: 2 → 0.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Mostly reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `daily-snapshot`, `nightly-stop`). Code: confirmed crons and paths.

#### IDEA-infra-ops-20261006-02 — Record side effects for each scheduled workflow (which tables each one writes)
*Submitter:* Infrastructure & Operations Owner
- **Problem Statement:** There is no record of which scheduled jobs mutate trading state. The stop-writer overlap above was found only by reading code.
- **Strategic Alignment:** §10.
- **Proposed Solution:** Fold into a scheduled-workflow inventory with a 'writes' column.
- **Expected Value:** Scheduled workflows with documented writes: unknown → 20 of 20.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: none. Same scope as `IDEA-finops-20261006-02`.

#### IDEA-metrics-20261006-01 — Define how each stored exit reason maps to §8's three exit conditions for analytics
*Submitter:* Metrics Definitions & Analytics Canonical Owner
- **Problem Statement:** Exit-reason analytics use 6+ labels; §8 has three conditions. 'Trailing Stop' and 'Stop Loss Hit' are both §8.1; 'Target Reached' and 'Partial Profit Taking' are §8.3 manual exits. Without a defined mapping, exit metrics cannot be read against the strategy.
- **Strategic Alignment:** §8.
- **Proposed Solution:** Add the mapping to `metrics_definitions.md`; analytics group by §8 category.
- **Expected Value:** Exit metrics expressible in §8 terms: 0 → all.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item. Same scope as `IDEA-data-model-20261006-02`.

#### IDEA-metrics-20261006-02 — Define a stop-freshness metric: hours since `stop_calculated_at` for each open position at view time
*Submitter:* Metrics Definitions & Analytics Canonical Owner
- **Problem Statement:** v9.9 made stop recalculation time observable, but no metric says how stale stops typically are or whether the nightly job is keeping up.
- **Strategic Alignment:** §7.1 (ATR recalculated daily) — the metric tests that claim.
- **Proposed Solution:** Define the metric (median and max age across open positions) in `metrics_definitions.md`; show it on System Status.
- **Expected Value:** Visibility of stop staleness: none → daily figure.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `stop freshness`, `stale stop`: 0).

#### IDEA-pmo-lead-20261006-01 — Add a known-false-positive allow-list to `scan_backlog_gate_conditions.py` — BLG-OPS-53 and BLG-FEAT-92 have been excluded by hand three rebalances running
*Submitter:* PMO Lead
- **Problem Statement:** The date-lapse scan flags `BLG-OPS-53` (a ship-date mention) and `BLG-FEAT-92` (a provenance note) every run; each rebalance re-verifies and excludes them manually (2026-09-28, 2026-09-30, 2026-10-06).
- **Strategic Alignment:** §12.3 by analogy — repeated manual corrections should be encoded once.
- **Proposed Solution:** A small allow-list file of item IDs with the reason each date is non-governing; the script reports them separately as 'known non-gate dates'.
- **Expected Value:** Manual false-positive exclusions per rebalance: 2 → 0.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: refines `BLG-GOV-347` (shipped v9.9 date disambiguation), which did not cover single-date non-gate mentions. Code: no allow-list in the script.

#### IDEA-pmo-lead-20261006-02 — Record each release's ready-pool / selected / leftover days in a structured history file, so STEP 7.3 reads it instead of being skipped
*Submitter:* PMO Lead
- **Problem Statement:** STEP 7.3 was recorded 'not re-measured — no plan release since v9.5' at the 2026-09-28 and 2026-09-30 rebalances, although v9.6–v9.9 release planning had all recorded ready-pool figures. Appendix F's runway table also stops at v9.7 and sits outside this engine's write scope.
- **Strategic Alignment:** §10 by analogy — capacity monitoring only works if read every time.
- **Proposed Solution:** Release Planning appends one row per release to `claude/roadmap/ready_pool_history.md`; STEP 7.3 and Appendix F read it.
- **Expected Value:** Rebalances skipping STEP 7.3 for lack of a found figure: 2 of the last 2 → 0.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `ready_pool_history`, `ready-pool history`). Not a code topic beyond the file.

#### IDEA-product-owner-20261006-01 — Exit dialog should pre-select the exit reason the system already knows (stop breached after grace, or risk-off) instead of always defaulting to 'Manual Exit'
*Submitter:* Product Owner · **build-and-ship candidate (§2.1 step 2a)**
- **Problem Statement:** Surface: `src/components/positions/ExitModal.js`. The reason select defaults to 'Manual Exit' for every exit. When the user exits because the system recommended it — §8.1 stop breach or the §8.2 risk-off flag already on the position (`risk_off_exit`) — the trade is still recorded as manual unless they notice and change it, so exit history understates how often the strategy's own exit conditions fired.
- **Strategic Alignment:** §8 (exactly three exit conditions; stop and risk-off exits are system recommendations requiring manual confirmation).
- **Proposed Solution:** Pre-select 'Risk-Off Signal' when `risk_off_exit` is true and 'Stop Loss Hit' when price ≤ stop after grace; show why it was pre-selected; the user can change it.
- **Expected Value:** System-recommended exits recorded as 'Manual': unknown share → ~0.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `ExitModal`, `exit reason`: 1 unrelated test-scope hit). Code: confirmed `ExitModal.js:19,34,356-361`, `risk_off_exit` on `GET /positions`.

#### IDEA-product-owner-20261006-02 — Morning briefing: add a card for §8 exit recommendations (post-grace stop breach, risk-off) — it currently shows the non-§8 'Exit Zone' but not the strategy's own exit conditions
*Submitter:* Product Owner · **build-and-ship candidate (§2.1 step 2a)**
- **Problem Statement:** Surface: `src/components/dashboard/home/MorningBriefing.js` and `morning/`. The morning view has cards for Exit Zone (R-target, not a §8 condition), compliance, earnings, red flags and screener hits, but none for the two system exit recommendations §8 defines. The user has to open Positions to learn that an exit is recommended.
- **Strategic Alignment:** §8.1/§8.2 and §3 (exit signals are recommendations the user must act on).
- **Proposed Solution:** A morning card listing positions with a post-grace stop breach or the risk-off flag, linking to the exit dialog.
- **Expected Value:** Clicks to discover a recommended exit from the home page: ≥1 page change → 0.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item (grep `MorningBriefing`, `stop breach card`: 0). Code: `morning/` holds ComplianceCard, EarningsAlertCard, ExitZoneCard, RedFlagsCard, ScreenerHitsCard only.

#### IDEA-qa-lead-20261006-01 — Playwright: Settings page with no settings row must show §11 defaults (5×, 2×, 10 days)
*Submitter:* QA Lead
- **Problem Statement:** No E2E test covers Settings defaults; the only Settings spec checks heading order/aria. The wrong 2×/3×/5 defaults have shipped untested.
- **Strategic Alignment:** §11.
- **Proposed Solution:** Add a Playwright scenario with an empty settings fixture asserting the three displayed defaults.
- **Expected Value:** Settings default values under E2E coverage: 0 → 3.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item. Code: `tests/e2e/settings-heading-order-and-aria-labelledby-regression.spec.js` only.

#### IDEA-qa-lead-20261006-02 — Unit test asserting every frontend strategy constant equals the §11 value
*Submitter:* QA Lead
- **Problem Statement:** Frontend fallbacks (`TradeEntry.js`, `Settings.js`) have drifted from §11 without failing any test.
- **Strategic Alignment:** §11.
- **Proposed Solution:** A Jest test importing the constants module (BLG-GOV-369) and asserting the §11 values.
- **Expected Value:** Frontend strategy constants under test: 0 → all.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Later
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item.

#### IDEA-qa-testing-20261006-01 — Parity test: for the same position inputs, the on-load analyze path and the nightly job must compute the same stop
*Submitter:* QA & Testing Owner
- **Problem Statement:** Both paths call `calculate_trailing_stop` but with different parameter sources. No test compares them; BLG-QA-204 notes the existing test does not even mock `get_settings()`.
- **Strategic Alignment:** §7.2 and §11.
- **Proposed Solution:** A pytest that feeds identical positions through both paths with a non-§11 settings row and asserts equal stops (it should fail today and pass after BLG-BE-138).
- **Expected Value:** Stop paths with a parity test: 0 → 2.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: refines `BLG-QA-204` (mocking gap in one test). Code: no parity test in `tests/`.

#### IDEA-qa-testing-20261006-02 — Pin `add_position`'s handling of `stop_price` in a test, so the Trade Entry contract is explicit
*Submitter:* QA & Testing Owner
- **Problem Statement:** `add_position` accepts `stop_price` and ignores it. No test states whether that is intended, so a future change could start or stop honouring it silently.
- **Strategic Alignment:** §5.
- **Proposed Solution:** A test asserting the stored initial stop equals `entry − 5×ATR` regardless of `stop_price` (or the new behaviour BLG-FE-197 settles on).
- **Expected Value:** Untested accepted-but-ignored request fields on position entry: 1 → 0.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item. Code: `position_service.py::add_position` signature vs body.

#### IDEA-strategy-owner-20261006-01 — Ruling needed: are §11 parameters user-tunable through Settings at all?
*Submitter:* Strategy Rules & System Intent Owner
- **Problem Statement:** §11 lists production parameters and §12.3 requires changes to be 'rare, explicit, versioned'. The Settings page lets the user change multipliers and hold days freely, and the on-load stop path obeys them. The strategy document and the product disagree on who may change the strategy.
- **Strategic Alignment:** §11, §12.1–§12.3.
- **Proposed Solution:** Rule one of: (a) parameters are fixed — Settings shows them read-only; (b) tunable as a sanctioned personal override — record it in §12 and make every path honour it; (c) tunable only through a §12.3 change record. The ruling is the first step of BLG-BE-138.
- **Expected Value:** Unresolved parameter-authority conflicts: 1 → 0.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: `BLG-GOV-95` (parameter review against live performance) is about the values, not who may change them. No other item.

#### IDEA-strategy-owner-20261006-02 — Ruling needed: is the five-state lifecycle badge a §9 state machine, or a separate display overlay that must defer to §9?
*Submitter:* Strategy Rules & System Intent Owner
- **Problem Statement:** §9 defines four states; the product shows five different ones with different entry rules. Until ruled, UI fixes (BLG-FE-196) can only correct the grace overlap, not the post-grace semantics.
- **Strategic Alignment:** §9 and §1.
- **Proposed Solution:** Rule on the relationship; amend §9 under §16's template if the overlay is adopted as canonical.
- **Expected Value:** Canonical state definitions: 2 conflicting → 1.
- **Effort Estimate:** Small (days to 1 week) · **Reversibility:** Fully reversible · **What Would You Stop?** No view — leave to debate. · **Submitter Recommendation:** Now
- **Overlap checks (§2.0 steps 5–6):** Backlog: no item. Same scope as `IDEA-head-of-specs-20261006-01`.

---

## STEP 5 — Structured Debate

**Debate Queue preflight:** 0 items advancing. **Queue empty — no debates required.** (The Challenger's substantive challenges this cycle are recorded as its two submissions and the STEP 2.4 Product Velocity Concern.)

---

## STEP 6 — Scoring Matrix Overlay

No surviving STEP 5 candidates. `claude/scoring/scored_initiatives.md` not rewritten — no active initiatives to score.

---

## STEP 7 — Workforce Economics Gate

### 7.1 Skill-Silo Alert

**Window:** v9.7, v9.8, v9.9 (U/G/D/P proxy; Owner-field refinement not used — v9.9's Owner values are all compound, see 7.2).

| Release | G+D+P | Total | Governance-story % |
|---------|-------|-------|---------------------|
| v9.7 | 23 | 28 | 82.1% |
| v9.8 | 37 | 39 | 94.9% |
| v9.9 | 33 | 35 | 94.3% |

**Pooled (§7.1 formula): 93 ÷ 102 = 91.2%. Plain per-cycle mean: 90.4%.** Method-break note per `BLG-GOV-367`: the series recorded up to 2026-09-30 used a plain mean (83.7%); the pooled equivalent of that window was 84.8%. On either method the reading **worsened**. > 40% → Skill-Silo Alert.

**Sustained-failure clause:** "If the rolling 3-cycle Skill-Silo average has worsened or remained unresolved for 3 or more consecutive readings" → the average has been above the 40% ceiling at every reading since at least 2026-08-11, and worsened this reading. **Applied: mandatory ≥2 build-and-ship U-items at the next release.** PO commits `BLG-FE-193` and `BLG-FE-198` (both shipped, user-visible changes per their ACs; not audit-shaped). The 2026-09-30 rebalance recorded the clause "not triggered" because readings were improving — a narrower reading of the same text (Friction Item 2 in `lessons_learnt.md`).

**Candidate gate verification (LP-05):** `BLG-FE-193` gate met (STEP 4); `BLG-FE-198` ungated. **Live-status cross-check:** both open in `backlog.md`, neither `✅ COMPLETE` nor archived this session.

**Cross-role pairing rotation note:** read; advisory only, no change to selection.

### 7.2 Cross-Role Workload Balance Check

**Method:** `claude/roadmap/role_share_history.md`, after appending the v9.9 row and breakdown via `scripts/compute_role_share_history.py claude/cycles/2026-09-30__release-v9.9/sprint_backlog.md` (no fallback needed).

Window v9.7–v9.9, 105 stories. Top buckets: Head of Specs Team 17 (16.2%), Director of Quality 13 (12.4%), Frontend Specifications & UX Documentation Owner 11 (10.5%), Head of Specs Team; PMO Lead 10 (9.5%). **All below 40% — no advisory.** Note: all 35 v9.9 Owner values are compound strings, so the raw tally shows no single-role load for that cycle (`BLG-GOV-372`).

### 7.3 Ready-Pool Capacity Gap Trend

Source: v9.6–v9.9 Release Planning `run_manifest.md` `**Result:**` lines.

| Release | Ready pool (d) | Selected (d) | Leftover (d) | Gap to 28-d ceiling |
|---------|----------------|--------------|--------------|---------------------|
| v9.6 | 61.75 | 28.00 | 33.75 | 33.75 |
| v9.7 | 61.35 | 28.00 | 33.35 | 33.35 |
| v9.8 | 46.70 | 28.00 | 18.70 | 18.70 |
| v9.9 | 36.20 | 27.85 | 8.35 | 8.20 |

(v9.7's leftover here follows its manifest's own 61.35 − 28.00; Appendix F records 21.35 for v9.7 from a different pool basis — not reconciled here, outside write scope.)

**Gap narrowing for 3 consecutive releases** → mandatory-review trigger (3 consecutive *widening*) does not apply. **Runway (Appendix F method, trailing-3 Δ leftover using Appendix F's v9.7 basis: −12.40, −2.65, −10.35; mean −8.47 d/cycle):** 8.35 ÷ 8.47 ≈ **1.0 cycle** until the pre-intake pool empties. This run's intake adds ~25 days of mostly ungated items, so v9.10 planning has a pool. Appendix F not updated (outside §4 write scope — Friction Item 1, `BLG-GOV-374`).

**Correction:** the 2026-09-28 and 2026-09-30 rebalances recorded §7.3 as "not re-measured — no `plan release` since v9.5". That was wrong: v9.6–v9.9 release planning each recorded these figures.

---

## STEP 8 — Final Rebalance Decision

**Roadmap initiatives:** no change (0 active initiatives).

**Now horizon — new `v9.10` section (committed backlog items):**
- `BLG-BE-138` — STEP 8.0 Correctness Fast-Track Promotion (P1).
- `BLG-FE-193`, `BLG-FE-198` — §7.1 sustained-failure pull-forward / STEP 2.4 Modify response.

**Displacement candidate flag:** none — no initiative exists. `initiative_register.md` and `displacement_debt_register.md` unchanged.

**Advisories for STEP 8 (§7.1 / §7.2 / §8.1.5):** Skill-Silo Alert 91.2% (mandatory pull-forward applied); cross-role balance — no advisory; §13-adjacent expiry — see STEP 8.1.5.

### STEP 8.0 — Production Correctness Fast-Track

P0/P1 scan of `backlog.md` at run start: 13 items, unchanged set (`BLG-FEAT-73`, `BLG-FE-43/45/54/58/59/62/63/68/69/70/71`, `BLG-SPEC-35`) — all Arc-5-gated feature/spec work; none is a correctness bug or security issue. **New this run:** `BLG-BE-138` (filed P1 at STEP 4) describes a calculation that can show the user a stop other than §7.2's → qualifies. **Promoted to the v9.10 Now horizon.** PO override considered and **not** taken: stops feed exit decisions, so "display-only" does not apply. Live divergence is unverified (production `settings` row unreadable here); verifying it is AC 1. Recorded as "Correctness Fast-Track Promotion" in `DL-083`; net-zero displacement against ~3-5 days of v9.10 P3 debt capacity, named by Release Planning.

### STEP 8.1 — Empty Now Horizon Gate

Condition 1a false after this run (Now holds committed items); condition 1b false (they sit under a version-labelled `v9.10` heading); condition 2 false (a next-release section now exists). **Gate does not fire.** Ends the 8-run Option (b) streak.

### STEP 8.1.5 — §13-Adjacent Initiative Expiry Review

- `IDEA-strategy-owner-20260304-02` / `IDEA-challenger-20260304-01` (`rejected_but_strong.md`): standing PO disposition (2026-09-23) — defer to §12.2's 100-closed-trades-since-2026-09-23 threshold. Reconfirmed; not re-litigated.
- **⚠ §13-adjacent expiry:** `BLG-FEAT-55`, `BLG-SPEC-65`, `BLG-SPEC-66` have been gated on an unopened §13 chat-persistence review since 2026-07-25 — well over 2 rebalance cycles. Surfaced for the Strategy Rules & System Intent Owner to schedule the review or record "not ready, re-check next cycle". Non-blocking.
- `BLG-GOV-358` (gap-risk §13 finding from the last run): resolved — v9.9 ST conducted the retroactive §13 review (`decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md`); item archived.

### Candidate/Item verification — STEP 8.2

Each item proposed for the v9.10 Now section run through the verification subroutine:
- `BLG-BE-138` — active in `backlog.md` (filed this run), no `✅ COMPLETE`/`RA:` marker → verified.
- `BLG-FE-193` — active, no completion marker; `BLG-FE-193` also appears once in `backlog_archive.md` only as a cross-reference inside `BLG-BE-135`'s archived text, not as its own entry → verified.
- `BLG-FE-198` — active (filed this run) → verified.

**STEP 8.2 verification complete — 3 items verified active, 0 excluded.**

---

## STEP 8.5 — Stateless Write Safety Gate

**8.5.A Re-anchoring:** to STEP 8's decisions (v9.10 section with 3 items; no initiative change), STEP 4's dispositions (26 backlog items incl. `BLG-GOV-375`; 44 register rows), STEP 2.4/7.2 history appends, STEP -1.5's applied deferred patch, STEP 11's action-now patch, and lifecycle-required header refreshes.

**8.5.B Write plan:**
- `claude/roadmap/current_roadmap.md` — §3 `v9.10` section; stale "Now horizon empty" note corrected; header refresh
- `claude/roadmap/decision_log.md` — append `DL-083`; stale header refreshed
- `claude/roadmap/product_value_ratio_history.md` — 1 row + sparkline + narrative
- `claude/roadmap/role_share_history.md` — v9.9 row + breakdown + rolling aggregate
- `claude/roadmap/workforce_capacity.md` — new rebalance section; header refresh
- `claude/backlog/backlog.md` — 26 new items; `BLG-FE-193` gate note + Provisional-Target v9.10; headers
- `claude/ideas/ideas_register.md` (44 rows), `ideas_window.json`, `window_summary_IW-20261006-01.md` — STEP -1.6 intake + STEP 4.2
- `claude/system/shared_standards.md` v3.37, `claude/system/roadmap_prompt.md` v9.31, `claude/system/OPERATIONAL_GUIDE.md` v4.223, `claude/system/prompt_change_log.md`, `claude/system/changelogs/shared_standards_changelog.md`, `claude/system/changelogs/roadmap_prompt_changelog.md` — STEP -1.5 / STEP 11 patches under Head of Specs Team sign-off (agent-mediated)
- `claude/cycles/2026-10-06__scheduled/*` — this run's artefacts
- `.claude_current_state.json` — STEP 12 rebalance keys

**Register row verification:** 0 `Status: Advancing` rows — nothing lacks a terminal status.

**BLG-ID collision check:** highest IDs across `backlog.md` + `backlog_archive.md` before writing: BE-137, FE-194, SPEC-184, GOV-368, SEC-40, OPS-178, FEAT-98, FR-05. New IDs start at +1 in each series — no collision.

**8.5.C/D:** every write is inside §4 and traceable to a STEP 8/STEP 4 decision, a STEP -1.5/STEP 11 patch, or a lifecycle header requirement. `OPERATIONAL_GUIDE.md` and the two changelog files are written only as the CLAUDE.md §6 checklist for the `claude/system/*` patches (§4 "STEP 11 action-now patches"). **Passed.**

---

## STEP 9 — Canonical Write

Executed per the 8.5.B plan. **Net-Zero (9.0):** additions (✅ Advance) 0 ≤ kills 0 — passes; the fast-track promotion is net-zero by STEP 8.0's own rule. **Decision log append-only:** `## DL-` heading count 45 → 46 (`DL-083` added); byte-prefix of the pre-run file unchanged (verified with `cmp`). **Effort day-range rule (§16.12):** the three v9.10 items carry day ranges; all other new items are `TBD` and carry ranges anyway. **Post-write park-count verification:** no parked rows exist.

---

## STEP 10 — Publish Delta Summary

See `cycle_summary.md`.

---

## STEP 11 — Lessons Learnt

See `lessons_learnt.md`. Meta-review not due — 1 cycle since `2026-09-30__scheduled`.

---

## STEP 12 — Stage, Commit & Global State Update

See `run_manifest.md` STEP 12 and the commit.
