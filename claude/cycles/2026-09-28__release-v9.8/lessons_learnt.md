Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-28

---

# Lessons Learnt — Release Planning 2026-09-28__release-v9.8

## Friction Items

**Friction Item 1 — the PO Modify directive (seat ≥1-2 build-and-ship U-items) has gone unsatisfiable for lack of ready candidates across 5 non-consecutive cycles, with no change in backlog composition.** The rebalance's PVR 0.089 🔴 Alert reading (4th consecutive) repeats the same "seat U-items" instruction it has issued at `v9.1`–`v9.4`, and this cycle's ready pool again holds 0 genuine new-feature candidates — the only `BLG-FEAT-*` items ever filed remain `73`/`76` (structurally gate-blocked, one hard-depends on the other) plus the now-shipped-and-retired `74`. No new feature-shaped idea has surfaced through several consecutive idea-intake windows. **Recommendation:** a Product Owner review of whether idea-intake windows are adequately prompting for genuine build-and-ship candidates, since re-flagging an empty pool each cycle without addressing the intake side will keep producing the same finding.

**Friction Item 2 — §-1.2's Option(b) reuse question resolved itself by timing this cycle, not by ruling.** `ESC-CLOSE-20260928-02` (still open, SLA 2026-10-01) asks whether §-1.2 should require its cited rebalance record to postdate the immediately-prior release-planning cycle. This cycle's rebalance happened to run same-day and does postdate `v9.7`, so the ambiguity did not need adjudicating to clear the gate here. The escalation itself should still receive a Head of Specs Team ruling for the general case — the next release-planning invocation may not be so fortunately timed, and this cycle's clean pass should not be read as having resolved the underlying question.

**Friction Item 3 — the effort-to-days parsing convention for `XS (<1h)` items needed an explicit tie-break this cycle for the first time at scale.** 18 of the 65 ready-pool items carry the exact string `XS (<1h)` (an hour-denominated qualifier, not a day range) — a naive "extract the first number" parse would read the `1` as `1.0 day`, an 6-7x overstatement relative to the canonical `XS` band midpoint (0.15d). This session applied the canonical-table fallback (0.15d) for any `<1h` qualifier rather than the literal digit, consistent with `workforce_capacity.md`'s existing precedence rule, but the rule's own text does not explicitly address the hour-vs-day unit mismatch case — it was inferred, not read directly off a stated example. **Recommendation:** add one explicit worked example to `workforce_capacity.md`'s effort-to-days precedence rule covering an `XS (<1h)` (or any hour-denominated) qualifier, so a future session does not need to re-derive the same inference.

## Prompt Change Classification

No process patches proposed this cycle. Friction Items 1–3's recommendations are deferred: Item 1 needs a Product Owner review of idea-intake prompting; Item 2 needs the already-tracked `ESC-CLOSE-20260928-02` Head of Specs Team ruling (unaffected by this cycle's clean pass); Item 3 is a lightweight `workforce_capacity.md` worked-example addition.

```yaml
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-09-28__release-v9.8",
  "phase": "Release",
  "filed_utc": "2026-09-28T11:15:00Z",
  "friction_item_count": 3,
  "action_now_count": 0,
  "deferred_count": 3,
  "status": "Active"
}
```
