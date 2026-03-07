**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-03-06
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

Binding governance stack (precedence order):

1. `claude/charter/team_charter.md`
2. `claude/charter/document_lifecycle_guide.md`
3. `claude/strategy/strategy_rules.md`

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

You must **not** modify:
- `claude/roadmap/current_roadmap.md` — use `manage roadmap` for roadmap changes
- Any cycle artefact, canonical spec, or governance document
- Item content beyond status fields, flags, and section placement

Violation → halt.

---

## 6. Backlog Item Classifications

| Classification | Criteria | Action |
|----------------|----------|--------|
| **Complete — Archive** | Status ✅ COMPLETE with delivery date and evidence reference | Move to `## Closed Items` section; append to archive |
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

For every item in `backlog.md`, apply the classification rules in §6.

Produce an internal classification table:

| Item ID | Title | Current Priority | Classification | Evidence | Action |
|---------|-------|-----------------|----------------|----------|--------|
| BLG-xx | <title> | P0/P1/P2/P3 | <classification> | <ref> | <action> |

Surface all **Ambiguous** items to the Product Owner. Do not proceed past STEP 1 until all ambiguous items are resolved.

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

## STEP 4 — Promotion Shortlist

For each item classified as **Promote Candidate**:

Produce a shortlist for Product Owner review:

| Item ID | Title | Priority | Why Promote | Target Release | Pre-work Status |
|---------|-------|----------|-------------|----------------|-----------------|
| <id> | <title> | P1 | Aligned with v1.9 scope, no blockers | v1.9 | Complete |

This is advisory only. No items are added to the roadmap by this engine. The Product Owner decides which (if any) to advance to the Roadmap Rebalance Engine.

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

## STEP 7 — Release Lock and Commit

Release `claude/backlog/.lock`.

```
git add claude/backlog/backlog.md
git add claude/backlog/backlog_archive.md
git add claude/backlog/backlog_health_<YYYYMMDD>.md
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

| Version | Date | Change |
|---------|------|--------|
| 1.1 | 2026-03-06 | Widened valid trigger windows to include pre-`run roadmap` invocation alongside Post-Ship Closure. Both windows now explicitly equal. Added known gap note for Phase 1 skipped path. Added lock conflict guidance to §2. Expanded §6 classification table to include Blocked — Stale Blocker as a distinct classification. Added stale blocker row to STEP 5 change plan and STEP 6.2/6.3 outputs. Added promotion shortlist advisory note to §6 and health report template. |
| 1.0 | 2026-03-04 | Initial version. |