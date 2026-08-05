Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-05
Cycle: 2026-08-05__release-v8.3

# Lessons Learnt — Release Planning — v8.3

## What worked well

- The STEP 1.4a.1 Sunset Criteria (added at `v8.1` via `BLG-GOV-280`) made this cycle's `BLG-FEAT-73`/`BLG-FEAT-74` disposition mechanical rather than an ad hoc judgment call — exactly as `v8.2`'s lessons learnt anticipated: the count reached 4 of 4 this cycle and the mandatory Option (b) disposition followed directly from the rule's own text, with no fresh reasoning required about when enough was enough.
- Being aware in advance that `BLG-GOV-286` exists (filed the prior commit, this same session, for exactly this class of scan gap) prompted a deliberate full-text "gate" grep across every draft candidate before commit, rather than relying on the field-label-only automated pass alone — this is what caught `BLG-GOV-74`'s `**Gate date:**` field before it reached `backlog.md`.
- Deliberately balancing this cycle's EPIC composition (governance at ~19% of items / ~22% of effort) against `v8.2`'s own self-flagged `RISK-03` (governance cluster at ~44%) kept the release from repeating that concentration without needing a fresh escalation to force the correction.

## Friction Log

### Friction Item 1

**Classification:** Type C — Self-caught verification error (scan-methodology gap, not a prompt defect)

**Recurrence:** 4th consecutive Release Planning cycle with a related self-caught ungated-candidate scan miss (`v8.0`: gate-field-name variant on `BLG-BE-24`/`BLG-OPS-48`; `v8.1`: scan line-window bounds on the same two items; `v8.2`: `BLG-OPS-48` again, a 3rd distinct failure mode, escalated and actioned via `BLG-GOV-286`; `v8.3`, this cycle: `BLG-GOV-74`, a 4th distinct failure mode — `**Gate date:**` as a standalone field, not embedded in `Provisional-Target` text and not a `**Gate criteria:**`/`gate-conditional` match either).

**What happened:** The initial P1/P2 ungated-candidate scan (field-label regex for `**Gate criteria:**`, `gate-conditional` type tags, and `gate status unverified` text) did not check for a standalone `**Gate date:**` field — a third field-name variant distinct from the two already known (`Gate criteria:`, and gate text embedded inside `Provisional-Target:`). `BLG-GOV-74` was briefly included in a draft P2 candidate list. It was caught before any `backlog.md` write via a deliberate full-text re-read (grepping every candidate's block for the substring "gate"), prompted specifically by knowing `BLG-GOV-286` exists and is not yet implemented — not by the automated scan itself, which still missed it.

**Where in the routine:** STEP 2 scope extraction (candidate identification) — caught before the STEP 4 backlog write, so no revert was needed (contrast `v8.2`'s Friction Item 1, which required reverting an already-applied `backlog.md` edit).

**Root cause:** Same structural gap named at `v8.0`–`v8.2` and already tracked as `BLG-GOV-286` (P1, filed the commit immediately prior to this session, by Head of Specs Team, scoped for a future sprint story): `release_planning_prompt.md` still does not define or require a canonical, mechanically-reliable scan procedure for identifying gated vs. ungated candidates. This instance adds a third known field-name variant (`**Gate date:**`) to the two `BLG-GOV-286` was filed to already cover — worth folding into that item's eventual implementation scope rather than filing a new tracking item.

**Blast radius analysis:**
- What would have propagated: had this gone uncaught, `BLG-GOV-74` would have been committed to `stage4_backlog_slice.md`/`backlog.md` as firm scope ~24 days before its own stated gate condition clears, then surfaced as blocked/premature at Sprint Planning or Execution.
- Recovery cost if uncaught: low — same class as the three prior instances (manual removal, capacity re-check, ST renumbering), one stage later than ideal.

**Process patch:** Not filed as a new item — `BLG-GOV-286` already exists as the tracking item for this exact class of gap and has not yet shipped (still scoped for a future sprint story, not yet a sprint story itself). This instance is recorded here as additional evidence for that item's priority and as a concrete field-name variant (`**Gate date:**`) its eventual implementation should explicitly cover, alongside the two variants already named in its filing. Recommendation for whoever implements `BLG-GOV-286`: the canonical scan should check, at minimum, `**Gate criteria:**`, `**Gate date:**`, `**Gate:**`, `gate-conditional` type tags, and gate language embedded in `**Provisional-Target:**` field text — four variants now observed across `v8.0`–`v8.3`.

## Recurrence Escalations

None filed here. `v8.2`'s own Recurrence Escalation 1 (3rd consecutive instance) was already actioned in the commit immediately prior to this session (`4254e8c0`, Head of Specs Team review — `BLG-GOV-286` filed, `BLG-OPS-48` fixed directly). This cycle's 4th instance (`BLG-GOV-74`) is additional evidence for that already-open item, not a fresh escalation requiring separate action — the corrective mechanism is already in motion, just not yet shipped.

## Process improvements actioned this run

None (this engine's write scope does not extend to filing new backlog items or patching `release_planning_prompt.md`/`claude/system/*`; `BLG-GOV-286` already exists and covers this class of gap).

## Outstanding deferred patches

| Patch | Target | Rationale |
|-------|--------|-----------|
| `BLG-GOV-286` implementation (canonical, scripted gate-detection procedure for Release Planning's scope-selection scan) — should now explicitly cover 4 observed field-name variants: `Gate criteria:`, `Gate date:`, embedded-in-`Provisional-Target` text, and `gate-conditional` type tags | Next sprint that pulls `BLG-GOV-286` into scope | 4th consecutive cycle with a related self-caught miss; item already filed and open, just not yet implemented |

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | The ungated-candidate scope-selection scan has now produced a self-caught miss at 4 consecutive Release Planning cycles (`v8.0`–`v8.3`), each a distinct field-name/embedding variant. `BLG-GOV-286` already exists to fix this class structurally but has not yet been pulled into a sprint. | The next sprint planning session with capacity available should prioritise pulling `BLG-GOV-286` into scope — it is P1 and has now accumulated 4 cycles of supporting evidence. | Release Planning / Sprint Planning |
| 2 | `BLG-FEAT-73`/`BLG-FEAT-74` are now formally parked (STEP 1.4a.1 sunset trigger fired and resolved this cycle). | If either item's gate condition changes materially (SI-02 linked-trade-plan count moves, or §13 pre-clearance for FEAT-74 is run), the next Release Planning session should re-evaluate them as fresh candidates rather than treating "parked" as permanent. | Release Planning |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-08-05__release-v8.3",
  "phase": "Release",
  "filed_utc": "2026-08-05T09:58:00Z",
  "friction_item_count": 1,
  "action_now_count": 0,
  "deferred_count": 1,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
