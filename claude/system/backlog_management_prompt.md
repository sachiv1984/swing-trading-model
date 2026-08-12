**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.14
**Last Updated:** 2026-08-12 (STEP 1.5 gains a 4th ephemeral-section type — Roadmap Rebalance/Delivery Verification idea-intake "New Items" sections, AUD-2026-08-12-003)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Team Charter:** claude/charter/team_charter.md

---

# Backlog Management Engine — Governance Prompt

(Completed Item Archiving, Priority Revalidation, Orphan Detection, Health Summary)

---

## 1. Purpose

This engine maintains the health and accuracy of `claude/backlog/backlog.md`. Its job is to:

- Archive completed and killed items (move to a closed section — not delete)
- Revalidate priorities on remaining items against the current roadmap
- Flag orphaned items (no roadmap home, no cycle activity)
- Flag blocked items where the blocker is unresolved or stale
- Promote candidates to the roadmap consideration list
- Produce a backlog health summary

This engine does **NOT**:
- Make product prioritisation decisions
- Add items to the roadmap — that requires the Roadmap Rebalance Engine
- Change the scope or definition of any backlog item
- Touch the roadmap document — use `manage roadmap` for roadmap changes

---

## 2. Invocation Rule (Hard Gate)

This routine executes ONLY when the user issues the explicit command:

```
groom backlog [--dry-run]
```

Rules:
- Invocation must start with `groom backlog` (case-insensitive match allowed).
- `--dry-run`: optional — produces the health summary and change plan without writing any files. Outputs the plan to the user and halts before STEP 6.
- If invocation is not exact, do not run. Treat as conversational.

**Who issues this command:** Product Owner or PMO Lead.

**Valid trigger windows:**

| Window | Rationale |
|--------|-----------|
| After Post-Ship Closure is confirmed | Ensures the backlog reflects shipped state before any new cycle opens |
| Immediately before `run roadmap` | Gives the Roadmap Rebalance Engine a clean, accurate backlog to work from |

Both windows are equally valid. Either may be used independently.

**Known gap:** If Phase 1 is skipped and `plan release` is invoked directly, the backlog will not have been groomed since the last Post-Ship Closure. In this case, `groom backlog` should be run before `plan release` is issued. This is not yet a formal trigger — teams skipping Phase 1 regularly should raise this for promotion to a full trigger window.

**Lock conflict:** If `claude/backlog/.lock` is held by an active Phase 1B cycle when this engine is invoked, the preflight gate will halt. Do not attempt to clear a live lock — wait for the owning cycle to release it, or confirm with the PMO Lead that the owning cycle is inactive before following the stale lock protocol.

**This engine is optional but strongly recommended** at both trigger windows above to prevent backlog decay.

---

## 3. Canonical Governance Sources (Non-Negotiable)

Canonical governance stack: per `claude/system/shared/governance_stack.md`. This routine may not override any entry in that stack.

---

## 4. Required Roles

| Role | Function in this engine |
|------|------------------------|
| Product Owner | Confirms classification for ambiguous items; decides promote-to-roadmap candidates |
| Head of Specs Team | Spec debt item triage; lifecycle compliance |
| Facilitator | Executes the engine steps; enforces write scope |

---

## 5. Write Scope Restriction (Hard Gate)

During this routine you may write only to:

- `claude/backlog/backlog.md` (archive completed items, update status fields, add flags, reorder within sections — no content changes to item definitions)
- `claude/backlog/backlog_archive.md` (append archived items — create if absent)
- `.claude_current_state.json` (Phase 1M state fields only: `last_groom_backlog_utc`, `last_groom_backlog_outcome`)

You must **not** modify:
- `claude/roadmap/current_roadmap.md` — use `manage roadmap` for roadmap changes
- Any cycle artefact, canonical spec, or governance document
- Item content beyond status fields, flags, and section placement

Violation → halt.

---

## 6. Backlog Item Classifications

| Classification | Criteria | Action |
|----------------|----------|--------|
| **Complete — Archive** | Item heading line OR the first body line immediately following the heading contains `✅ COMPLETE` with delivery date and evidence reference | Move to `## Closed Items` section; append to archive |
| **Killed — Archive** | Status ❌ Killed or superseded with decision reference | Move to `## Closed Items` section; append to archive |
| **Active — Keep** | Open, prioritised, has a roadmap home or is a standalone improvement | No change |
| **Orphan — Flag** | Open, no roadmap home, no cycle activity, no blocker | Add orphan flag; surface for Product Owner review |
| **Blocked — Stale Blocker** | Open, has a stated blocker, blocker status not updated in 2+ cycles | Add staleness note to blocker field; do not flag as orphan; surface for owner review |
| **Promote Candidate** | Open, high priority, aligns with next planned release, no pre-work outstanding | Add to promotion shortlist for Product Owner consideration — advisory only |
| **Spec Debt — Validate** | BLG-SPEC-* items; check if owning spec has been updated | Confirm open/resolved; update status |
| **Ambiguous — Confirm** | Appears complete (referenced in changelog or verification) but status not updated | Surface to Product Owner before archiving |

**Note on promotion candidates:** The promotion shortlist produced by this engine is advisory only. No items are added to the roadmap by this engine. The Product Owner decides which (if any) candidates to advance, and the Roadmap Rebalance Engine executes any additions.

---

## Mandatory End-to-End Process

---

## STEP -1 — Preflight Gate (Hard Gate)

### -1.1 Required Files Present

Verify:
- `claude/charter/team_charter.md`
- `claude/charter/document_lifecycle_guide.md`
- `claude/backlog/backlog.md`
- `claude/roadmap/current_roadmap.md` (needed for alignment check)

If any missing: halt and report.

### -1.2 Concurrency Lock Check

Check `claude/backlog/.lock`. If lock exists and is not owned by this run: halt and report the owning cycle_id. Do not proceed. Do not attempt to clear a live lock without PMO Lead confirmation and evidence that the owning cycle is inactive.

### -1.3 Header Compliance Check

Verify `backlog.md` has a compliant Class 4 header (Owner, Status, Class, Last Updated).
If non-compliant: apply header remediation only before proceeding.

### -1.4 Dry-Run Check

If `--dry-run` flag present: note it. Continue through STEP 5. Halt before STEP 6 and output the full change plan to the user.

---

## STEP 0 — Acquire Lock and Load

Acquire `claude/backlog/.lock` with the run identifier `GROOM-<YYYYMMDD>-<nn>`.

Load `claude/backlog/backlog.md` in full.
Load `claude/roadmap/current_roadmap.md` for alignment checking.
Load `claude/roadmap/decision_log.md` for kill/deferral references.
Load `docs/product/changelog.md` if present (to cross-check completed items).

---

## STEP 1 — Classify All Items

### 1.1 Gate Field Label Normalization (Mandatory Pre-Scan)

Before classifying, grep `backlog.md` and `backlog_archive.md` for any `**Gate:**` field label (non-canonical synonym). The canonical label is `**Gate criteria:**` — items using `**Gate:**` are silently miscounted as ungated (Actionable) by the roadmap engine's STEP 3.1 automated scan, which searches only for the literal string `**Gate criteria:**`. Normalise every `**Gate:**` occurrence found to `**Gate criteria:**` (label only — do not alter the condition text). Record the count normalised in the health summary under a `Gate Field Normalisation` line. (Added v1.11 — closes the deferred patch from `2026-07-06__scheduled` roadmap rebalance lessons learnt, Friction Item 1: `BLG-FEAT-52` was found using the non-canonical label and silently excluded from the D-gated count.)

### 1.2 Effort Day-Range Validation (Mandatory Pre-Scan, §16.12)

Before classifying, scan `backlog.md` for items whose `**Provisional-Target:**` names a specific release (`v<X.Y>`, not `TBD`/`Unscheduled`) but whose `**Effort:**` field carries a bare letter (`S`/`M`/`L`/`XS`) with no day range in parentheses. For each such item found:
- Flag it in the health summary under a **Missing Effort Day-Range** subsection.
- Do **not** backfill the day range yourself — estimating it requires domain judgment from the item's owner, not mechanical inference.
- Note: this is a validation/flagging check only, distinct from §1.1's Gate Field Label Normalization, which does auto-correct (a pure label synonym, not a judgment call).

If no items found: note "Effort Day-Range Validation: PASS — 0 items missing a required day range" in the health summary. (Added v1.12 — closes the escalated decision from `2026-07-14__release-v7.1` post-ship closure, Release Planning Friction Item 1: bare-letter effort bands on items with a specific `Provisional-Target` forced Release Planning STEP 4.5 to infer day ranges by analogy, right when that cycle's capacity check landed at a WARN threshold with zero buffer.)

### 1.3 Governance Prompt Duplicate Cross-Check (LL-v7.10-P3-01)

Before confirming any open `BLG-GOV-*` backlog item as still-open, grep `claude/system/prompt_change_log.md` for entries against the same prompt file the item names, filed **after** the item's own `**Source:**` filing date. If a matching version-transition entry exists whose change description already covers the item's stated problem, flag the item as a **probable-duplicate candidate** in the health summary under a `Governance Prompt Duplicate Candidates` line, for the item's named owner to confirm disposition (close as pre-met, or leave open if the fix only partially covers the item). Do not close the item automatically — this is a flag for owner review, not an auto-resolution.

If no candidates found: note "Governance Prompt Duplicate Cross-Check: PASS — 0 candidates found" in the health summary. (Added v1.13 — closes the deferred patch from post-ship closure `2026-07-28__release-v7.10` Phase 3 lessons learnt: 3 of 23 stories that cycle — `ST-16`/EPIC-04, `ST-21`/EPIC-06, `ST-23`/EPIC-06, 13% of scope — reached sprint execution already fully resolved by a prior-sprint governance fix, requiring the STEP 3.1.A pre-met verification path instead of fresh delivery, because none were caught as stale/duplicate by backlog grooming before being pulled into sprint scope.)

For every item in `backlog.md`, apply the classification rules in §6.

Produce an internal classification table:

| Item ID | Title | Current Priority | Classification | Evidence | Action |
|---------|-------|-----------------|----------------|----------|--------|
| BLG-xx | <title> | P0/P1/P2/P3 | <classification> | <ref> | <action> |

Surface all **Ambiguous** items to the Product Owner. Do not proceed past STEP 1 until all ambiguous items are resolved.

---

## STEP 1.5 — Ephemeral Section Cleanup

Identify sections in `backlog.md` that were appended by governance engines and are now obsolete. Four types are considered ephemeral:

1. **Completed Release Slice sections** (added by the Release Planning Engine): any section headed `## Release Slice — v<x.y>` or `## Last Release Slice — v<x.y>` or `## Prior Release Slice — v<x.y>` where the release is marked ✅ COMPLETE or all stories are marked as shipped. Canonical home is the cycle directory (`claude/cycles/<cycle_id>/`).
2. **Resolved Test Scenario Gap sections** (added by the Delivery Verification Engine): any section headed `### TEST-GAP-EPIC-xx-v<yy>` or `## Test Scenario Gaps — ...` where all items are marked ✅ RESOLVED or ✅ COMPLETE.
3. **Resolved "Returned to Backlog" sections**: any section headed `## Returned to Backlog — ...` where all listed items are marked ✅ DELIVERED.
4. **Roadmap Rebalance / Delivery Verification idea-intake "New Items" sections** (added AUD-2026-08-12-003, closing a gap where 4 such sections dated `2026-07-24__scheduled` through `2026-08-11__scheduled` accumulated unpromoted across 4+ groom runs): any section headed `## Roadmap Rebalance <date>__scheduled — New Items (...)` or `## Delivery Verification <date>__release-v<x.y> — New Items`. Unlike types 1–3, items in this section carry no completion marker of their own — the section is a staging area for newly-added items, not a completion-tracked list, so it has no "all resolved" condition to wait for.

For each ephemeral section found:
- Types 1–3: if ALL items are resolved/complete, queue for removal from `backlog.md` in STEP 6.2. If ANY items are still open, extract them to the appropriate §1–§8 type section with a new item entry, then queue the parent section for removal.
- Type 4: **always** relocate every item in the section to its correct §1–§8 type section (creating the section heading if it does not yet exist — see §1–§8 in the Placement Rule at the top of `backlog.md`) at the very next `groom backlog` run after the section was created, regardless of individual item status, then queue the parent section for removal. Do not leave a type-4 section in place past the one `groom backlog` run that immediately follows its creation.
- Record each section in the change plan with action: `Remove — ephemeral section (all resolved)`, `Remove — ephemeral section (open items extracted to §<n>)`, or `Remove — ephemeral section (all items relocated to §<n>)` for type 4.

---

## STEP 2 — Priority Revalidation

For each **Active — Keep** item, check alignment with the current roadmap:

- Does the item have a target release on the roadmap?
- Is the item's stated priority consistent with its target release timing?
- Has the item's blocking dependency (if any) been resolved?

Flag any items where:
- Priority is P0/P1 but target release is 2+ versions away — likely needs downgrade review
- Priority is P3 but item is referenced in a planned release — likely needs upgrade review
- Blocker is marked resolved but item is still listed as blocked

Record priority alignment notes in the health summary (do not change priorities without Product Owner confirmation).

---

## STEP 3 — Spec Debt Validation

For each item prefixed `BLG-SPEC-*`:

- Check if the referenced spec has been updated since the item was raised
- If the spec has been updated and the deviation/gap is resolved: mark as **Complete — Archive**
- If the spec has been updated but the gap remains: update the item's "raised" note with current status
- If the spec owner is unknown or the item is older than 2 cycles with no activity: add a staleness note

---

## STEP 3.5 — Deferral Age Validation (OA-03/CF-03)

For each **Active — Keep** or **Parked** item, check consecutive deferral count:

1. Count the number of consecutive cycles in which the item was deferred (no release assignment reached, or target release changed in each cycle without delivery). A cycle counts as a deferral if: (a) the item had a target release that passed without delivery, or (b) the item was explicitly moved to the next cycle.
2. If an item has been deferred **3 or more consecutive cycles** without a named re-deferral from the Product Owner:
   - Flag as a **3-cycle deferral** in the health summary.
   - Surface to Product Owner: "⚠ Deferral flag: [Item ID] [Title] has been deferred 3+ consecutive cycles without PO re-deferral. Action required: add named re-deferral note, assign a release, or kill the item."
   - Items with 3+ consecutive deferrals and no PO re-deferral are health-check blockers — they cannot be carried forward silently.

**Named re-deferral format:** Append to the backlog item:
```
> PO re-deferral YYYY-MM-DD: [reason]
```
A named re-deferral resets the consecutive deferral count. If no re-deferral is on record after 3 cycles, the item must be actioned before the backlog health check can close.

**Kill recommendation:** If an item has 3+ consecutive deferrals and no PO engagement in 2+ cycles, surface as a kill candidate with rationale.

---

## STEP 4 — Promotion Shortlist

For each item classified as **Promote Candidate**:

Produce a shortlist for Product Owner review:

| Item ID | Title | Priority | Why Promote | Target Release | Pre-work Status |
|---------|-------|----------|-------------|----------------|-----------------|
| <id> | <title> | P1 | Aligned with v1.9 scope, no blockers | v1.9 | Complete |

This is advisory only. No items are added to the roadmap by this engine. The Product Owner decides which (if any) to advance to the Roadmap Rebalance Engine.

**Endpoint reference check (LL-v1.10-P3-2):** Before listing an item as a Promote Candidate, scan the item's acceptance criteria for endpoint references (e.g., `GET /path/endpoint`). For each referenced endpoint, verify it exists in the canonical spec file (e.g., `portfolio_endpoints.md`, `analytics_endpoints.md`, or whichever spec covers that endpoint). If any referenced endpoint cannot be found in the canonical spec:
- Add a note to the item in `backlog.md`: `> ⚠️ **Spec gap:** AC references \`<endpoint>\` which does not exist in the canonical spec. Resolve before promoting to sprint scope.`
- Do not include the item in the Promote Candidate shortlist until the spec gap is resolved or the AC is corrected.

This check prevents backlog items with unresolvable acceptance criteria from reaching sprint scope, where they would cause mid-sprint deviations (as occurred with BLG-API-01 → DEV-ST05-01 in cycle 2026-03-15__release-v1.10).

---

## STEP 4.5 — ID Uniqueness Scan (LL-RP-v22-01)

Before producing the health summary, scan for duplicate item IDs across the closed items table (`## Closed Items` section in `backlog.md`) and the backlog archive (`backlog_archive.md`):

1. Collect all item IDs from `## Closed Items` in `backlog.md`
2. Collect all item IDs from `backlog_archive.md`
3. Identify any ID that appears more than once across either list

**§6.1 stub+verbatim exemption (BLG-QA-72, v6.6 ST-03):** The §6.1 archive format deliberately writes each ID's `### BLG-xxx — Title` header **twice** in immediate succession — once for the retirement stub (`**Status at retirement:**` / `**Retired:**` / `**Shipped in:**` / `**Evidence:**` block) and once as the first line of the verbatim full-entry copy that follows it. Before flagging an ID as a duplicate:
- If the ID appears **exactly twice**, the two headers carry the **same title text**, and the first occurrence is immediately followed by a `**Status at retirement:**` line: this is a compliant §6.1 stub+verbatim pair, not a duplicate. Do not flag.
- If the ID appears more than twice, or appears twice with **different title text**, or twice with the same title but *without* the `**Status at retirement:**` stub marker preceding the first: this is a genuine duplicate — flag per below.

For each genuine duplicate found:
- Record it in the health summary under a **Duplicate IDs** subsection
- Flag it in the change plan with action: `Investigate — duplicate ID in closed items`
- Do not archive further copies of a duplicated item without Product Owner confirmation

If no genuine duplicates found: note "ID uniqueness: PASS" in the health summary.

---

## STEP 5 — Produce Health Summary and Change Plan

Write an internal health summary:

```
Backlog Health Summary — <date>

Total items reviewed: <n>
Complete — Archive: <n>
Killed — Archive: <n>
Active — Keep: <n>
Orphans flagged: <n>
Blocked — stale blocker flagged: <n>
Spec debt items — resolved: <n>
Spec debt items — still open: <n>
Priority misalignments flagged: <n>
Promotion candidates: <n>
Ambiguous items resolved: <n>
```

Produce change plan:

| File | Action | Item | Reason |
|------|--------|------|--------|
| `backlog.md` | Move to Closed section | BLG-xx | Complete — archive |
| `backlog.md` | Add orphan flag | BLG-xx | No roadmap home or cycle activity |
| `backlog.md` | Add stale blocker note | BLG-xx | Blocker not updated in 2+ cycles |
| `backlog_archive.md` | Append | BLG-xx | Archiving completed item |

If `--dry-run`: output health summary and change plan. Halt. Do not write.

Surface the plan to the user and confirm before proceeding to STEP 6.

---

## STEP 6 — Execute Writes

Execute in this order:

### 6.1 Create or update `claude/backlog/backlog_archive.md`

If file does not exist, create with header:

```markdown
**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** <date>

# Backlog Archive — Momentum Trading Assistant

Permanent record of completed and killed backlog items retired from `claude/backlog/backlog.md`. Listed in retirement order, most recent first. Append-only — do not edit existing entries.

---
```

For each Complete — Archive and Killed — Archive item, append:

```markdown
---

### <Item ID> — <Title>

**Status at retirement:** ✅ Complete | ❌ Killed
**Priority at retirement:** P0 / P1 / P2 / P3
**Retired:** <date>
**Shipped in:** <version | "N/A — killed">
**Evidence:** <changelog entry / verification report / decision log ref>

<verbatim copy of the item's full backlog entry — do not edit>
```

### 6.2 Update `claude/backlog/backlog.md`

- Move all Complete — Archive and Killed — Archive items to a `## Closed Items` section at the bottom of the file (or remove entirely if archive is confirmed as the record)
- Add orphan flags: `> ⚠️ **Orphan Notice:** No roadmap home or cycle activity detected. Review at next Roadmap Rebalance.`
- Add stale blocker notes: `> ⚠️ **Stale Blocker:** Blocker status not updated in 2+ cycles. Owner review required.`
- Update `**Last Updated:**` header field
- Do not change item definitions, priorities, or descriptions — status and flags only

**Post-write verification:** After completing all STEP 6.2 writes, run two checks on the active sections of `backlog.md` (§1–§8 type sections, above any `## Closed Items` section):
1. Grep heading lines for `✅ COMPLETE` or `❌ Killed` in the heading itself.
2. Grep the line immediately following each `### BLG-` heading for a `✅ COMPLETE` or `❌ Killed` marker (the standard body-line completion format).

If any are found by either check, the archive move is incomplete — return to STEP 6.2 and remove the item from the active body before proceeding. Do not proceed to STEP 6.3 with any terminal-status items remaining in the active backlog sections.

### 6.3 Write health report

Write: `claude/backlog/backlog_health_<YYYYMMDD>.md`

```markdown
**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** <date>

# Backlog Health Report — <date>

## Summary

<Health summary from STEP 5>

## Promotion Candidates

<Promotion shortlist from STEP 4, or "None identified">
Note: This list is advisory only. No items are added to the roadmap by this engine.

## Priority Alignment Notes

<List of items with priority/roadmap misalignment, or "No misalignments found">

## Orphans Flagged

| Item ID | Title | Last activity | Flag added |
|---------|-------|--------------|------------|
| <id> | <title> | <cycle_id or "none"> | Yes |

## Blocked Items — Stale Blockers

| Item ID | Title | Blocker | Last updated | Flag added |
|---------|-------|---------|-------------|------------|
| <id> | <title> | <blocker description> | <cycle_id or "none"> | Yes |

## Spec Debt Status

| Item ID | Spec | Status | Action taken |
|---------|------|--------|-------------|
| <id> | <spec path> | Resolved / Still open | Archived / Updated |

## Items Requiring Product Owner Decision

<Any items that need a follow-up decision, or "None">
```

---

## STEP 7 — Release Lock, Update Global State, and Commit

Release `claude/backlog/.lock`.

Update `.claude_current_state.json`:
```json
{
  "last_groom_backlog_utc": "<ISO-8601 UTC>",
  "last_groom_backlog_outcome": "<n> archived, <n> orphans flagged, <n> stale blockers flagged, <n> promote candidates"
}
```

```
git add claude/backlog/backlog.md
git add claude/backlog/backlog_archive.md
git add claude/backlog/backlog_health_<YYYYMMDD>.md
git add .claude_current_state.json
git commit -m "[GOVERNANCE] Backlog grooming run <date> — <n> items archived, <n> orphans flagged"
git push origin <current-branch>
```

If git operations unavailable: output exact files and commit message. Mark as "Ready to commit."

---

## 7. Completion Condition

The run is complete when:

- All items classified and actioned
- Ambiguous items resolved before any write
- Archive updated with all completed/killed items
- Health report written
- Lock released
- Commit complete (or commit manifest produced)

---

## 8. Governance Invariants

- **No content changes.** Archiving moves items; it does not reword or reprioritise them. The archived entry is verbatim.
- **No roadmap writes.** This engine does not touch `current_roadmap.md`. Use `manage roadmap`.
- **Archive is append-only.** Archived items are permanent records. Do not edit existing archive entries.
- **Promotion shortlist is advisory.** No items are added to the roadmap by this engine. The Roadmap Rebalance Engine executes any additions following a Product Owner decision.
- **Lock discipline.** The lock must be acquired before any write and released after commit. A live lock owned by another cycle must not be cleared without PMO Lead confirmation. A stale lock may only be cleared by the PMO Lead following the stale lock protocol.
- **Dry-run is safe.** `--dry-run` never writes. It is always safe to run.
- **Priority revalidation is advisory.** This engine flags misalignments; it does not change priorities.

---

## Change Log

See: [`claude/system/changelogs/backlog_management_changelog.md`](changelogs/backlog_management_changelog.md)
