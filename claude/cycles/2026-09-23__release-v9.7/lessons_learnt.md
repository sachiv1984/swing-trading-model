Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-23

---

# Lessons Learnt — Release Planning 2026-09-23__release-v9.7

## Friction Items

**Friction Item 1 — a second "already resolved but not scan-detectable" item slipped through, using a different convention than the one caught at `v9.6`.** `BLG-FE-189` carried a full `**Resolution (2026-09-22):**` block (fixed same-session, Playwright-covered) but no `✅ COMPLETE` banner — the convention `v9.6`'s Friction Item 1 flagged. A banner-presence check (the fix `v9.6` recommended) would **not** have caught this one; `backlog.md` now has at least two distinct "this is actually done" conventions in active use, and the gate scan detects neither. **Recommendation:** widen the recommended scan/sibling-check (still unimplemented — `BLG-GOV-345`/ST-27 from `v9.6` was scoped narrower, to date-lapsed gates only, not to this) to also flag any item body containing `**Resolution (...):**` or `**Resolved (...):**`, alongside the existing gate-language and date-lapsed flags.

**Friction Item 2 — the `VH` effort band has no canonical midpoint, and this cycle needed one for the first time.** `BLG-FEAT-74` is the first-ever ready item carrying `Effort: VH (>2 weeks)`; `workforce_capacity.md`'s Canonical Effort Band → Days Conversion Table stops at `L` (~3.5d). A Product Owner ad hoc estimate (12.0d) was used, surfaced and confirmed via direct question this session rather than derived mechanically. **Recommendation:** add a `VH` row to the canonical table once a second real `VH` item is scored, so a future cycle doesn't need to re-derive this ad hoc — same lightweight-table-edit pattern as `v9.6`'s own Friction Item 3 fix.

**Friction Item 3 — the STEP -1.2 Option(b) equivalence has now been cited twice from the same rebalance record, whose own prose named only the first release.** `2026-09-19__scheduled`'s STEP 8.1 Option(b) decision explicitly said "this rebalance immediately precedes `plan release v9.6`" — it was written to justify opening `v9.6`, not a second, later release. No rebalance has run since, so this cycle reused it anyway on the grounds that the underlying condition (empty Now horizon, backlog-driven cadence) is unchanged. This is a new variant of the general 15-cycle staleness pattern already normal in this repo — not "a rebalance is stale by elapsed time" but "a rebalance's own Option(b) rationale named a specific release that has already been consumed." **Recommendation:** a Head of Specs Team ruling on whether §-1.2 should require the cited Option(b) record to postdate the *immediately prior* release-planning cycle (forcing a fresh rebalance every 2 releases at minimum), or whether unlimited reuse until the next rebalance runs is the intended design. Not actioned here — flagged only.

**Friction Item 4 — the ready pool finally produced a genuine ready P1 item, ending a run of cycles with an empty ready-P1 pool.** `v9.6`'s own Friction Item 4 noted 0 ready P1 items (both `BLG-FEAT-73`/`74` gate-blocked). This cycle, `BLG-FEAT-74`'s §13 gate cleared (`ESC-EXEC-20260921-05`, 2026-09-23) — the first ready P1 item this backlog has produced since at least `v8.0` (per the `v8.1` Perennial-Return retroactive assessment). `BLG-FEAT-73` remains the sole gate-blocked P1, not re-checkable before 2026-11-09 or 10 new linked `trade_plans`. Noted as a positive signal for the next rebalance's Skill-Silo discussion — this cycle satisfies the build-and-ship rotation guideline organically, without needing a manufactured pull-forward.

## Prompt Change Classification

No process patches proposed this cycle. Friction Items 1–3's recommendations are deferred: Item 1 needs a Head of Specs Team decision on widening the still-unimplemented scan-detection fix from `v9.6`; Item 2 is a lightweight `workforce_capacity.md` table edit; Item 3 needs a Head of Specs Team ruling on §-1.2's precedent-reuse rule.

```yaml
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-09-23__release-v9.7",
  "phase": "Release",
  "filed_utc": "2026-09-23T19:15:00Z",
  "friction_item_count": 4,
  "action_now_count": 0,
  "deferred_count": 3,
  "status": "Active"
}
```
