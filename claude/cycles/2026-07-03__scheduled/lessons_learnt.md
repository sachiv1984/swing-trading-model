**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-07-03__scheduled
**Last Updated:** 2026-07-03

---

# Lessons Learnt — Roadmap Rebalance 2026-07-03__scheduled

Feature / Trigger: N/A — scheduled rebalance
Run: 2026-07-03__scheduled
Reviewed by: PMO Lead; Head of Specs Team
Date filed: 2026-07-03
Prior cycle checked: 2026-07-02__scheduled

---

## What worked well

1. **All 34 previously-parked ideas were correctly re-parked with valid, specific, non-vague rationales.** The Facilitator's vague-rationale test (§4.1) cleared all 34 on first review — zero challenges required, demonstrating that the prior cycle's idea-intake window produced durable, well-reasoned park rationales rather than placeholder text.
2. **STEP 4.0's two-step gate-condition re-check (backlog.md then backlog_archive.md) found zero staleness this cycle** — a clean pass, in contrast to the prior cycle which caught one stale "not shipped" finding using the same fixed check. Confirms the v8.0 patch continues working as intended.
3. **STEP 8.0 Production Correctness Fast-Track again correctly excluded BLG-SPEC-35** as pre-work rather than a correctness bug — the third consecutive cycle reaching the same correct judgment on this item, showing the fast-track scan is not producing false positives on borderline P1 items.
4. **The outstanding deferred patch (U/G/D/P tagging in `post_ship_closure.md`) was resolved exactly on its own self-declared target date** — filed at `2026-07-02__scheduled` with an explicit fallback target of "next roadmap rebalance," it was unambiguously due this cycle and applied action-now without any STEP -1.5 ambiguity. This is the second consecutive cycle demonstrating that the STEP 11.2 wording fix (cycle_id/date targets, not bare release versions) works as intended.

---

## Friction Log

---

### Friction Item 1

**Classification:**
- Type B — Semantic Mismatch: The same "U-item" label was interpreted differently by Release Planning (nominal tagging) and by this engine's own STEP 2.4 diagnostic (content-based classification)

**Recurrence:** No — first time this specific disagreement is directly caught and quantified, though the underlying general risk was already flagged as Friction Item 3 in `2026-07-02__scheduled` lessons learnt.

**What happened:**
The prior cycle's carry-forward item DF-17/LP-04 asked this cycle to check whether v6.5's release — which deliberately bundled **two** nominal U-item pull-forwards (`BLG-FE-46`, `BLG-FEAT-41`) — corrected the Skill-Silo rolling-3-cycle ceiling breach more effectively than v6.4's single-item attempt. Running this cycle's STEP 2.4 classification independently, only **one** of the two (`BLG-FE-46`) actually classified as U — `BLG-FEAT-41` (the "Claude thesis adoption rate metric") was classified D, because its shipped changelog description names only a metrics-definition spec update (`metrics_definitions.md#Thesis Adoption Rate`) with no user-visible endpoint or UI panel. This means the carry-forward's own premise — "did 2 U-items correct the ceiling better than 1?" — was never actually tested as designed: v6.5 delivered the same effective U-item count (1) as v6.4, and the rolling average predictably got worse again (83.7%, up from 64.8%), consistent with a 1-item correction being insufficient, not evidence that a genuine 2-item correction fails.

**Where in the routine:**
STEP 2.4 (Product Value Ratio Diagnostic) / STEP 7.1 (Skill-Silo Alert) — the disagreement surfaces at the boundary between how Release Planning nominally labels pull-forward candidates and how this engine's own diagnostic classifies them after shipping.

**Root cause:**
Missing artefact — no canonical U/G/D/P tag was recorded on `BLG-FEAT-41` at any point between its selection as a "pull-forward candidate" and its shipping, so nothing forced the two labels (Release Planning's nominal "U-item" designation vs. this engine's content-based classification) to reconcile before the carry-forward comparison was run.

**Blast radius analysis:**
- What would have propagated: a false conclusion that "even 2 U-items doesn't fix the ceiling," which could lead the PO to abandon the multi-item correction strategy prematurely, when the strategy was never actually tried.
- When it would have surfaced: possibly never on its own — would require a session to notice the item-level classification disagreement, exactly as happened this cycle.
- Recovery cost if uncaught: medium — could misdirect `plan release v6.6`'s scoping strategy for the Skill-Silo ceiling based on a confounded data point.

**Process patch:**

→ Immediate patch applied this run (shared with Friction Item 2 below — same underlying fix):
  - File: `claude/system/post_ship_closure.md`
  - Section: STEP 1.1 (Entry Structure) / STEP 1.2 (Entry Rules)
  - Change: `Tech backlog items shipped` lines now require an inline `[U|G|D|P]` classification tag assigned at ship time from the story's actual shipped content, using `roadmap_prompt.md` STEP 2.4's schema. This forces any future "N U-item pull-forward" claim to be reconciled against the same classification this diagnostic uses, at the point of shipping rather than left to later reconstruction.
  - Version: 2.16 → 2.17
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes (bundled with the pre-existing deferred patch this same change resolves; see Process improvements table)

---

### Friction Item 2

**Classification:**
- Type B — Semantic Mismatch: Independently re-deriving the v6.3 U/G/D/P split (as a sanity check against the prior cycle's authoritative table) produced a different result than the table already on file

**Recurrence:** Related to (but not a literal recurrence of) Friction Item 3 from `2026-07-02__scheduled` — that item predicted this exact class of variance; this cycle is the first direct empirical confirmation of it.

**What happened:**
While preparing this cycle's STEP 2.4 table, an independent re-classification of v6.3's 15 stories (as a methodology check) produced U=3/D=9 rather than the prior cycle's on-file U=2/D=10 — a one-story swing (`BLG-BE-39`, the AI journal summary bug fix, judged differently: "backend correctness fix" vs. "visible bug-fix output"). This cycle used the prior cycle's authoritative table for v6.1–v6.4 rather than the freshly re-derived numbers, specifically to avoid compounding the variance — but the discrepancy itself is now directly confirmed empirically, not just theoretical.

**Where in the routine:**
STEP 2.4 — Product Value Ratio Diagnostic

**Root cause:**
Same missing artefact as Friction Item 1 — no canonical U/G/D/P tag exists for stories shipped before this cycle's patch (v6.1–v6.5 will not benefit from the fix; only v6.6 onward will).

**Blast radius analysis:**
- What would have propagated: continued small variances each time the 5-cycle window is independently re-derived rather than carried forward, slowly eroding confidence in the ratio trend line.
- When it would have surfaced: the next time two different sessions compute the same historical cycle's split and compare notes (as happened here).
- Recovery cost if uncaught: low — this cycle mitigated it by deliberately reusing the prior authoritative table rather than the fresh re-derivation, so no incorrect ratio was published. Cost is really about future variance, not this cycle's output.

**Process patch:**

→ Same immediate patch as Friction Item 1 (`post_ship_closure.md` v2.16→v2.17) — going forward, stories will carry their tag at ship time, closing this gap for all cycles from v6.6 onward. No separate patch needed; recorded here as a second, independent piece of evidence for the same fix.

---

## Recurrence Escalations

None this cycle. Friction Items 1 and 2 are new findings this cycle (not open prior-cycle outstanding actions left unresolved) — both fully addressed by the single action-now patch applied this run.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/post_ship_closure.md` | STEP 1.1 / STEP 1.2 | `Tech backlog items shipped` lines require an inline `[U\|G\|D\|P]` classification tag at ship time (resolves the deferred patch filed `2026-07-02__scheduled` Friction Item 3, and this cycle's Friction Items 1 and 2) | v2.16→v2.17 | Yes |
| `claude/system/OPERATIONAL_GUIDE.md` | §10 header, §14 table, Change Log | Version/source rows updated to v2.17; document Version 4.75→4.76 | v4.75→v4.76 | Yes |
| `claude/system/roadmap_prompt.md` | STEP 2.4 | STEP 11.4 meta-review action — STEP 2.4 now reads the inline `[U\|G\|D\|P]` tag when present instead of re-deriving it; closes the read-side gap left by the write-side patch above | v8.0→v8.1 | Yes |
| `claude/system/OPERATIONAL_GUIDE.md` | §6 header, §13 register, §14 table, Change Log | Version/source rows updated to v8.1; document Version 4.76→4.77 | v4.76→v4.77 | Yes |

---

## New files created this run

- `claude/cycles/2026-07-03__scheduled/run_manifest.md`
- `claude/cycles/2026-07-03__scheduled/cycle_record.md`
- `claude/cycles/2026-07-03__scheduled/cycle_summary.md`
- `claude/cycles/2026-07-03__scheduled/lessons_learnt.md` (this file)

---

## Outstanding deferred patches

None this cycle — the one deferred patch carried into this cycle (`post_ship_closure.md` U/G/D/P tagging) was resolved action-now, not re-deferred.

---

## Escalations

None this cycle.

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Skill-Silo rolling-3-cycle average worsened again to 83.7% (from 64.8%), and the "did 2 U-items correct it" carry-forward test (DF-17/LP-04) was confounded by BLG-FEAT-41's D-reclassification — the 2-item strategy was never actually tested. | `plan release v6.6` should commit at least 2 items that clearly satisfy the U classification under `roadmap_prompt.md` STEP 2.4's content-based test (visible UI/endpoint surface, not just a metrics/spec-definition update) — a genuine test of the multi-item correction hypothesis has still not occurred. | Release Planning |
| 2 | The now-resolved U/G/D/P ship-time tagging patch (`post_ship_closure.md` v2.17) only applies to stories shipped from v6.6 onward — the v6.1–v6.5 historical window used in STEP 2.4 remains judgment-reconstructed and will drop out of the 5-cycle window naturally by v7.0. | No action needed before v7.0 — the window will self-correct as untagged historical cycles age out; flagging only so a future session doesn't attempt to retroactively tag v6.1–v6.5 (not warranted; the fix is prospective by design). | Roadmap |

---

## STEP 11.4 — Meta-Review

**Trigger:** 3 cycles since last meta-review (`2026-06-26__scheduled`). **Due this cycle — completed.**

See `meta_review.md` for full analysis. Summary: 2 patterns identified (Type B Semantic Mismatch recurring 2+ cycles; Type C Dependency Stall recurring 2 cycles). Pattern 1 (Type B) actioned this cycle with a companion read-side patch (`roadmap_prompt.md` v8.0→v8.1) alongside the write-side patch already applied at STEP 11.2. Pattern 2 (Type C) confirmed already resolved via prior cycles' patches — no new action required. `last_meta_review_cycle` updated to `2026-07-03__scheduled` at STEP 12.

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-03__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-07-03T00:00:00Z",
  "friction_item_count": 2,
  "action_now_count": 2,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
