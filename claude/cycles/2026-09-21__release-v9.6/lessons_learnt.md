Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-21

---

# Lessons Learnt — Release Planning 2026-09-21__release-v9.6

## Friction Items

**Friction Item 1 — the scripted gate scan is blind to already-completed and already-satisfied backlog items, so a machine-built ready pool contains stale work.** 4 of the 80 items the scan-plus-manual-exclusion pass first produced were not actually open: `BLG-GOV-335`/`336`/`337` carry a `✅ COMPLETE — 2026-09-19` banner (resolved directly in the v9.5 post-ship follow-up; archive pending the next `groom backlog`) and `BLG-GOV-326`'s sole AC (a merge decision) had already been recorded by v9.5 ST-38 in `workforce_capacity.md`. A first-pass selection seated `BLG-GOV-336` and `BLG-GOV-337` as P2 items ahead of everything else; only reading the selected items' bodies caught it. Sprint Planning §3.1 has a pre-seal stale-feature-target check, but Release Planning — where the pool is built — has none. It is the same class of blind spot as the lapsed-date gap already filed as `BLG-GOV-345`: the scan classifies by field presence, not by item state. **Recommendation:** extend `scripts/scan_backlog_gate_conditions.py` (or add a sibling check) to emit a "banner says complete / resolved" list alongside `BLG-GOV-345`'s "date-lapsed — verify" list, and require §1.3a to read both before the pool is fixed. `BLG-GOV-345` (selected, ST-27) is the natural vehicle — its scope should be widened in the same story rather than filed as a separate item.

**Friction Item 2 — §1.4c ignores `Provisional-Target: v<current release>` tagging.** Strict application seated 4 of the 16 ready items horizon-tagged `v9.6` and left 12 (4.80 days) behind — including follow-ups filed against v9.5's own shipped work (`BLG-SPEC-149`–`155`, `BLG-FE-178`/`179`, `BLG-QA-179`/`180`/`181`). Oldest-filed-first ranks the 2026-09-14 idea-intake items above 2026-09-16/18 follow-ups by construction. §1.4c permits a Product Owner override for a specific cycle; none was given, so none was applied. **Recommendation (Product Owner / Head of Specs Team decision, not applied here):** either add an explicit horizon-tag tier to §1.4c (tagged-for-this-release items seated after P2, before round-robin) or state that an unselected `v<current>` tag is expected to be cleared at post-ship groom. Either is better than the current silence, which leaves 12 self-declared "this release" items unexplained.

**Friction Item 3 — the effort-to-days conversion is not reproducible.** v9.5's published total (27.99d) matches neither a band-letter-only reading (26.60d) nor an explicit-range-midpoint reading (28.35d) of its own slice, and `workforce_capacity.md`'s Canonical Effort Band table says items "may still cite their own more specific day range" without saying which wins. This cycle stated its rule explicitly in `run_manifest.md` and gave a sensitivity figure (27.90d band-only). **Recommendation:** add a one-line precedence rule to the `workforce_capacity.md` table (a lightweight reference table — no §6 checklist needed).

**Friction Item 4 — the ready pool is wide but the ready P1 pool is empty.** 76 ready items / 61.75 days (2.2× the 28-day ceiling); 0 P1 (the two scan-ungated P1 items, `BLG-FEAT-73`/`74`, are gate-blocked), 8 P2, 61 P3, 7 P4. Only 3 ungated `BLG-FEAT-*` items exist, all seated. The Skill-Silo pull-forward is therefore satisfied by exactly the minimum; `BLG-FEAT-59` (the rebalance's named secondary) is held by an owner verification due 2026-09-24. `BLG-SPEC-160` (ST-23) is the only route to a further build-and-ship candidate (`BLG-FEAT-74`). Noted for the next rebalance, not actioned here.

## Prompt Change Classification

No process patches proposed this cycle. Friction Items 1–3's recommendations are deferred: Item 1 folds into `BLG-GOV-345`/ST-27's own implementation (Head of Specs Team to widen its scope at Sprint Planning); Item 2 needs a Product Owner decision; Item 3 is a lightweight table edit for the Head of Specs Team. Consistent with how v9.5's own friction items were handled.

```yaml
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-09-21__release-v9.6",
  "phase": "Release",
  "filed_utc": "2026-09-21T09:06:16Z",
  "friction_item_count": 4,
  "action_now_count": 0,
  "deferred_count": 3,
  "status": "Active"
}
```
