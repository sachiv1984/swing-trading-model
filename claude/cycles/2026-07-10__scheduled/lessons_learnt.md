**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Filed
**Report Date:** 2026-07-10

---

# Lessons Learnt — Roadmap Rebalance 2026-07-10__scheduled

## Friction Log

---

### Friction Item 1

**Classification:**
- Type A — Governance Drift: `roadmap_prompt.md` STEP 2.4 instructs engines to "read the tag, don't re-derive it, when one exists... from `post_ship_closure.md` v2.17 onward, each 'Tech backlog items shipped' line carries an inline `[U|G|D|P]` tag assigned at ship time." No such tags, or a "Tech backlog items shipped" line, were found in any of `v6.4`–`v6.8`'s `closure_record.md` files — all post-dating the claimed v2.17 convention.

**Recurrence:** Not checkable (this is the first cycle to actually attempt reading the tags directly from cycle artefacts rather than reusing a prior cycle's own aggregate figures).

**What happened:**
At STEP 2.4 this cycle, the prior cycle's window (v6.3–v6.7) could be reused as a starting aggregate (per the "reuse verbatim" fallback used at `2026-07-03__scheduled` for a similar reason), but reconstructing the new v6.4–v6.8 window still required v6.8's individual story classification. Searching `v6.4`–`v6.8` cycle folders for the documented tag convention found nothing — every `closure_record.md` lacks both the literal `[U]`/`[G]`/`[D]`/`[P]` markers and the "Tech backlog items shipped" line the instruction names. The ratio was instead reconstructed by judgment from each release's `current_roadmap.md` summary-table description, then cross-checked for consistency against the prior cycle's authoritative aggregate (found consistent — see `run_manifest.md`).

**Where in the routine:**
STEP 2.4 (Product Value Ratio Diagnostic).

**Root cause:**
Either the tagging convention was never actually implemented in `post_ship_closure.md`'s closure-record template despite being documented as in effect, or it was implemented under different wording that a literal-string search does not catch. Not determinable without reading `post_ship_closure.md`'s own STEP text, which is outside this engine's read requirement and write scope.

**Blast radius analysis:**
- What would have propagated: every future STEP 2.4 computation continuing to silently fall back to judgment-based reconstruction while believing it should be reading authoritative tags — the reconstruction-variance risk this exact convention was introduced to prevent (per the `2026-07-02__scheduled`/`2026-07-03__scheduled` friction items cited in `roadmap_prompt.md` §2.4's own text) remains live and undetected.
- When it would have surfaced: the next time two independent sessions compute the same historical window and get different splits (the original failure mode this convention exists to prevent).
- Recovery cost if uncaught: low-medium — judgment-based reconstruction is still internally consistent (verified this cycle), but the intended authoritative-source guarantee is not actually in effect.

**Process patch:**

→ Deferred patch (cannot apply this run — `post_ship_closure.md` is outside this engine's Write Scope §4):
  - File: `claude/system/post_ship_closure.md`
  - Section: the step that writes `closure_record.md`'s shipped-items list (referenced by `roadmap_prompt.md` STEP 2.4 as being in effect "from v2.17 onward")
  - Change required: verify whether the `[U|G|D|P]` inline-tag convention is actually implemented in the current step text; if present but worded differently than a literal-bracket search catches, align the wording; if genuinely absent despite the v2.17 changelog claim, implement it or correct `roadmap_prompt.md` §2.4's claim to match actual behaviour.
  - Owner: Head of Specs Team
  - Target: next `run post-ship` invocation, or next session with `post_ship_closure.md` write access.

---

## Recurrence Escalations

None this cycle.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|--------------------------|
| `claude/system/roadmap_prompt.md` | STEP 6 | Overwrite-verification instruction added (read-before-write + re-read-after-write), resolving the due deferred patch from `2026-07-08__scheduled` Friction Item 1 | v8.5→v8.6 | Yes |
| `claude/system/shared_standards.md` | §9 (new §9.1) | Version/state header cross-check note added, resolving the STEP 11.4 meta-review's Type A Governance Drift pattern | v3.12→v3.13 | Yes |
| `claude/system/OPERATIONAL_GUIDE.md` | §14 + Change Log | Version-reference sync for the above 2 patches | v4.88→v4.89 | Yes |

---

## New files created this run

- `claude/cycles/2026-07-10__scheduled/run_manifest.md`
- `claude/cycles/2026-07-10__scheduled/cycle_record.md`
- `claude/cycles/2026-07-10__scheduled/cycle_summary.md`
- `claude/cycles/2026-07-10__scheduled/meta_review.md`
- `claude/cycles/2026-07-10__scheduled/lessons_learnt.md` (this file)
- `claude/ideas/window_summary_IW-20260710-01.md` (committed separately as part of the idea intake window close)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|------------------|-------|--------|
| `claude/system/post_ship_closure.md` | Shipped-items list step | Verify/align the `[U|G|D|P]` inline-tag convention (this cycle's Friction Item 1) | Head of Specs Team | Next `run post-ship` invocation |
| `CLAUDE.md` | §6 Governance File Edit Checklist, step 1 | Amend to require reading the file's own Change Log table's top row before bumping the header version field (carried from `2026-07-08__scheduled`) | Head of Specs Team | Next session with direct `CLAUDE.md` write access (outside any phase engine's declared scope) |
| `claude/system/roadmap_prompt.md` | STEP 0.C (Run Tier Determination) | Abbreviated-manifest exception for "0 active initiatives + no backlog/register change since prior scheduled run" (carried from `2026-07-08__scheduled`) | Head of Specs Team | Next scheduled rebalance where the condition genuinely recurs (did not recur this cycle — backlog changed materially) |

---

## Escalations

None raised by this engine this cycle.

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | The Product Value Ratio has now alerted 2 consecutive times (0.26, then 0.18) with no roadmap-level intervention available (0 active initiatives) — the only lever is backlog-level pull-forward naming, which this cycle exercised (`BLG-FEAT-64`/`BLG-FEAT-65`). | `plan release v6.9` should treat these 2 items as the anchor scope decision, not merely available candidates — if release planning declines both without written PO rationale, the pattern from `2026-07-08__scheduled` (where the rebalance-level naming became the actual release scope) would be broken for the first time. | Release Planning |
| 2 | This cycle's STEP 2.4 computation found no inline `[U|G|D|P]` tags in any `v6.4`–`v6.8` `closure_record.md`, despite `roadmap_prompt.md` §2.4 claiming the convention is in effect "from v2.17 onward." | Future STEP 2.4 runs should not assume the tag-read shortcut will work without first confirming a tagged line actually exists in the target cycle's `closure_record.md` — check before relying on it, and expect to fall back to judgment-based reconstruction, cross-checked against the prior cycle's authoritative aggregate for consistency. | Roadmap |

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-10__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-07-10T16:00:00Z",
  "friction_item_count": 1,
  "action_now_count": 2,
  "deferred_count": 3,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
