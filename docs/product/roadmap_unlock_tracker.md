**Owner:** PMO Lead; Product Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-13
**Story:** ST-19 (BLG-GOV-303, EPIC-07, v8.7)
**Cross-referenced from:** `claude/roadmap/current_roadmap.md` §6 — **pending** (see "Write-scope note" below)

---

# Roadmap Unlock Tracker

## Purpose

`BLG-GOV-303`: the roadmap's remaining gated features each state their own gate condition individually (`current_roadmap.md`'s Arc 4/Arc 5/Arc 6 tables), but there was no single place showing all gates and their current clearance status together — this cycle's own findings (per multiple prior `STEP 2.3`/`STEP 7.1` rebalance entries) had to be manually cross-referenced each time to establish that most of the roadmap is blocked on a small number of shared root causes. This document is that single place.

**Write-scope note:** This document lives at `docs/product/roadmap_unlock_tracker.md`, not under `claude/roadmap/` — `execution_prompt.md` §7 explicitly prohibits Sprint Execution from writing to `claude/roadmap/*` (roadmap files are owned by the Roadmap Rebalance/`manage roadmap` engines). The AC's "cross-referenced from `current_roadmap.md` §6" therefore cannot be completed by this story directly; §6 currently still shows only its single stale Alpaca Paper Trading row. **Action required:** the next `run roadmap` or `manage roadmap` invocation should replace §6's content with a pointer to this document (one line: `See docs/product/roadmap_unlock_tracker.md for the full gated-feature tracker.`), since those engines hold write access to `claude/roadmap/current_roadmap.md` that Sprint Execution does not.

**Source note:** Cross-checked against `scripts/scan_backlog_gate_conditions.py`'s output (2026-08-13 run: 294 backlog items scanned, 175 gated) — that script covers *all* gated backlog debt items (a much broader, item-level scan); this tracker is deliberately narrower, covering only the named **roadmap-level Arc feature gates** (`current_roadmap.md`'s Arc 4/5/6 tables), which is what `BLG-GOV-303`'s problem statement actually names (SI-02, SI-04, SI-05 Phase 2, PO-02/04/05, PS-01–05). The two are complementary, not duplicative — see §4 below for how they relate.

---

## 1. Roadmap Feature Gates — Current Status (2026-08-13)

| Feature | ID | Gate condition | Current status | Shared blocker group |
|---------|-----|-----------------|-----------------|----------------------|
| Behavioural Drift Detection (frontend) | SI-02 | (1) ≥20 closed trades with linked `trade_plans` in production; (2) `GET /analytics/behavioural-drift` p99 < 2s over 7d; (3) drift scores show non-trivial variance (≥10 closed trades in the 90d analysis window, per `si02_drift_score.md` §2) | **NOT MET** — condition (1): 0 linked trades (11 trade-plan rows, 0 with `position_id` set), last live-confirmed 2026-07-28; condition (2): unconfirmed either way; condition (3): last confirmed FAILING 2026-07-17 (`insufficient_data`, `trade_count_in_window: 9`, `_MIN_TRADES = 10`) | **Group A — trade-plan linkage** |
| Weekly Strategy Integrity Digest (Phase 2) | SI-05 | Depends on SI-02 drift signal integration (Phase 1 — Red Flag summary + compliance trend — already shipped, v5.0-era) | **NOT MET** — blocked transitively on SI-02 | Group A (via SI-02) |
| Reflection ↔ Outcome Correlation | PO-04 | Requires PO-01 + PO-02 data foundation; gate: 50+ trades with plans | **NOT MET** — 20 total closed trades ever recorded (last formally confirmed 2026-07-28), far short of 50 | **Group B — total trade volume** |
| Edge Analysis Dashboard | PS-01 | Gate: 100+ trades with plans and lifecycle data | **NOT MET** — 20 total closed trades | Group B |
| Regime-Conditional Performance | PS-02 | Gate: 50+ trades; requires regime-at-entry capture (Arc 2 — already shipped) | **NOT MET** — 20 total closed trades | Group B |
| Monte Carlo Simulation | PS-03 | Gate: 50+ trades; deterministic simulation, §13 COMPLIANT | **NOT MET** — 20 total closed trades | Group B |
| Strategy Decay Detection | PS-04 | Gate: 18+ months of trade history | **NOT MET** — system live since ~2026-03 (v1.5), well under 18 months as of 2026-08 | **Group C — elapsed time** |
| Personal Benchmark Comparison | PS-05 | Gate: 12+ months of history | **NOT MET** — under 12 months as of 2026-08 | Group C |
| Journal Pattern Recognition | PO-02 | Requires 6+ months of AI-summarised journal entries (`BLG-FEAT-16` live and actively used) | **Not independently re-verified this pass** — a distinct data axis (journal-entry volume/duration, not trade count); no structured field tracks this the way SI-02's does. Flagged as a tracking gap (§3) rather than asserted met/unmet without evidence. | Not grouped — distinct axis |
| Lightweight Replay Mode | PO-05 | States "Requires Alpaca paper trading foundation (IT-06)" — **IT-06 already shipped v3.5 (2026-05-15)** | **Ambiguous.** The Arc 4 feature table names no gate beyond IT-06, which is met — but PO-05 is referenced elsewhere (`current_roadmap.md` rebalance prose, v8.4-era) as still "gate-blocked" alongside SI-02 frontend, with no restated numeric condition. Flagged as a tracking gap (§3): either PO-05's true gate needs to be stated explicitly (likely a trade-volume threshold, unstated), or the "still gate-blocked" characterisation is itself stale now that IT-06 shipped. | Not grouped — needs clarification |

**Excluded (already shipped, not gated):** SI-01 (v3.8), SI-03 (v3.9), IT-06 (v3.5), PO-01 (v3.5–v3.6). **SI-04** (Strategy Version Comparison) shipped in full at v7.7 (`BLG-FEAT-75`) — the Arc 5 feature table's own gate-condition text ("Requires version-tagged trade history from Arc 2 onwards") was never updated after shipment and is stale; SI-04 does not belong in a "still gated" list. Not corrected in `current_roadmap.md` by this story (`claude/roadmap/*` is outside `execution_prompt.md` §7's write scope for Sprint Execution) — flagged here for `manage roadmap`'s next pass.

---

## 2. Shared Root Cause

Per `BLG-GOV-303`'s own problem statement, this cycle's findings confirm: **the back half of the roadmap is substantially blocked on a small number of shared data-density conditions, not on distinct per-feature blockers.**

- **Group A (trade-plan linkage):** 1 feature gate (SI-02), 1 transitively-blocked feature (SI-05 Phase 2). Root cause: 0 of 11 trade-plan rows carry a linked `position_id`, despite `BLG-BE-46`'s auto-link forward-fix shipping 2026-07-09 and `BLG-FE-109`'s UX nudge shipping 2026-07-16 — the fix works going forward but no trade has actually been opened via the linking flow since. **This is the same underlying condition `BLG-BE-91` (v8.6) hardened the DB-level safeguard for** (`trade_plans_active_requires_position_check` CHECK constraint) and `ST-07`/`BLG-BE-96` (this same v8.7 cycle) re-audited — see `docs/specs/data_model.md#DS-12`.
- **Group B (total trade volume):** 4 feature gates (PO-04, PS-01, PS-02, PS-03), all requiring 50–100+ total closed trades against a current count of 20.
- **Group C (elapsed time):** 2 feature gates (PS-04, PS-05), requiring 12–18+ months of trade history against a system live since ~2026-03 (5 months as of this writing).

None of these three groups can be accelerated by engineering work — they are properties of actual trading activity and calendar time, not code. This is consistent with `BLG-BE-91`'s framing (v8.6): the most direct lever available is closing the trade-plan linkage gap (Group A), since it's the one blocker with an identified, already-partially-shipped code fix rather than a pure waiting condition.

---

## 3. Tracking Gaps Found (this pass)

- **PO-02** has no structured live-check field (unlike SI-02's detailed block) — its 6-month journal-volume gate has never been formally re-verified against production data as far as this tracker's sources show. Recommend a future `BLG-GOV-30x`-class item to add one.
- **PO-05**'s actual current gate condition is ambiguous now that its stated prerequisite (IT-06) has shipped — either the feature table needs an explicit restated gate, or its "still gate-blocked" characterisation elsewhere in `current_roadmap.md` needs correcting. Not resolved here (would require a Product Owner scope decision, out of this story's authority).
- **SI-04's Arc 5 table row** is stale (still describes a pre-implementation gate condition for a feature that shipped 4 releases ago via a different mechanism than the row describes). Flagged for `manage roadmap`'s next pass, not corrected here (write-scope boundary).

---

## 4. Relationship to `scripts/scan_backlog_gate_conditions.py`

That script scans **all** backlog debt items (`claude/backlog/backlog.md`) for a `**Gate criteria:**`/`**Gate:**`/`**Gate date:**` field — as of this run, 175 of 294 items. Most of those are small, item-level "defer this specific backlog task until X" conditions (e.g. "defer until SI-04 sprint planning"), not roadmap-level Arc feature gates. This tracker's §1 table is the narrower, curated subset `BLG-GOV-303` actually asked for — the named roadmap-flagship features, not the full backlog-debt gate inventory. A future consolidation (out of this story's scope) could cross-link backlog items whose gate condition names one of §1's feature IDs (e.g. any backlog item gated on "SI-02 shipping") directly to this tracker's row for that feature, to show the downstream item count waiting on each root cause.

---

## Sign-off

**PMO Lead (agent-mediated, §5.3):** Confirmed — 2026-08-13. Roadmap feature gate table built from `current_roadmap.md`'s own Arc 4/5/6 source data (SI-02's already-detailed structured field taken verbatim; PS-01–05/PO-04 derived from the Arc 6/Arc 4 tables' own stated gate text plus the confirmed 20-total-closed-trades figure); cross-checked against `scan_backlog_gate_conditions.py`'s broader item-level scan to confirm scope boundary (§4). Two tracking gaps (PO-02, PO-05) and one stale roadmap row (SI-04) surfaced and disclosed rather than silently resolved without evidence.

**Product Owner (agent-mediated, §5.3):** Confirmed — 2026-08-13. Shared-root-cause grouping (§2) is directionally consistent with `BLG-BE-91`'s (v8.6) prior framing that trade-plan linkage is the most actionable lever; no scope decision required from this sign-off (the PO-05/PO-02 gaps in §3 are flagged, not resolved, and correctly deferred to a future Product Owner decision rather than assumed here).
