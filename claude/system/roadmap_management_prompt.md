**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.5
**Last Updated:** 2026-08-18 (ST-22, EPIC-06, v8.9, BLG-GOV-260: STEP 5.2 gains a stale RA: marker pruning rule)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Team Charter:** claude/charter/team_charter.md

---

# Roadmap Management Engine — Governance Prompt

(Document Lifecycle Enforcement, Completed Item Retirement, Active Roadmap Hygiene)

---

## 1. Purpose

This engine enforces the lifecycle of `claude/roadmap/current_roadmap.md`. Its job is to keep the active roadmap readable and accurate by:

- Retiring completed items to `claude/roadmap/roadmap_archive.md`
- Ensuring the active roadmap reflects only: current version, planned releases, and gated/deferred items
- Updating the release summary table
- Flagging stale "Planned" items that have had no cycle activity

This engine does **NOT**:
- Change priorities, scope, or strategic positioning of any item
- Move items between releases
- Make product decisions
- Replace the Roadmap Rebalance Engine — it manages documents, not decisions

---

## 2. Invocation Rule (Hard Gate)

This routine executes ONLY when the user issues the explicit command:

```
manage roadmap [--dry-run]
```

Rules:
- Invocation must start with `manage roadmap` (case-insensitive match allowed).
- `--dry-run`: optional — produces the change plan and proposed archive entries without writing any files. Outputs the plan to the user and halts before STEP 5.
- If invocation is not exact, do not run. Treat as conversational.

**Who issues this command:** Product Owner or PMO Lead.

**Valid trigger windows:**

| Window | Rationale |
|--------|-----------|
| After Post-Ship Closure is confirmed | Ensures the roadmap reflects shipped state before any new cycle opens |
| Immediately before `run roadmap` | Gives the Roadmap Rebalance Engine a clean, accurate roadmap to work from |

Both windows are equally valid. Either may be used independently.

**Known gap:** If Phase 1 is skipped and `plan release` is invoked directly, the roadmap will not have been cleaned since the last Post-Ship Closure. In this case, `manage roadmap` should be run before `plan release` is issued. This is not yet a formal trigger — teams skipping Phase 1 regularly should raise this for promotion to a full trigger window.

**This engine is optional but strongly recommended** at both trigger windows above to prevent roadmap document decay.

---

## 3. Canonical Governance Sources (Non-Negotiable)

Canonical governance stack: per `claude/system/shared/governance_stack.md`. This routine may not override any entry in that stack.

---

## 4. Required Roles

| Role | Function in this engine |
|------|------------------------|
| Product Owner | Confirms retirement classification for any ambiguous item |
| PMO Lead | Verifies cycle evidence for completed items before retirement |
| Head of Specs Team | Lifecycle compliance sign-off on the archive document |
| Facilitator | Executes the engine steps; enforces write scope |

---

## 5. Write Scope Restriction (Hard Gate)

During this routine you may write only to:

- `claude/roadmap/current_roadmap.md` (retire completed items, update release summary, update status fields)
- `claude/roadmap/roadmap_archive.md` (append retired items — create if absent)
- `claude/roadmap/initiative_register.md` (move retired items from Active Initiatives to Completed table — STEP 5.4 only)
- `claude/roadmap/` folder (create archive file if absent)
- `.claude_current_state.json` (Phase 1M state fields only: `last_manage_roadmap_utc`, `last_manage_roadmap_outcome`)

You must **not** modify:
- `claude/backlog/backlog.md` — use `groom backlog` engine for backlog changes
- Any cycle artefact, canonical spec, or governance document
- Item content beyond status fields and location (no scope changes, no priority changes)

Violation → halt.

---

## 6. Item Classification Rules

Before writing anything, classify every item in `current_roadmap.md`:

| Classification | Criteria | Action |
|----------------|----------|--------|
| **Active — Keep** | Status is Planned, In Progress, or Gated; not yet started or currently being worked | No change |
| **Complete — Retire** | Status is ✅ Complete with verified delivery date and cycle reference | Retire to archive |
| **Killed — Retire** | Status is ❌ Killed with decision log reference | Retire to archive |
| **Stale — Flag** | Status is Planned but no cycle activity in last 2+ completed cycles | Add stale flag; do not retire |
| **Ambiguous — Confirm** | Marked complete but no verification report reference or cycle ID | Surface to Product Owner for explicit confirmation before retiring |

**Hard rule:** An item may not be retired to the archive unless it has at least one of:
- A verification report reference, or
- A decision log entry (for kills/deferrals), or
- Explicit Product Owner confirmation recorded in the engine run log

---

## Mandatory End-to-End Process

---

## STEP -1 — Preflight Gate (Hard Gate)

### -1.1 Required Files Present

Verify:
- `claude/charter/team_charter.md`
- `claude/charter/document_lifecycle_guide.md`
- `claude/roadmap/current_roadmap.md`
- `claude/roadmap/decision_log.md`

If any missing: halt and report.

### -1.2 Header Compliance Check

Verify `current_roadmap.md` has a compliant Class 4 header (Owner, Class, Status, Last Updated).
If non-compliant: apply header remediation only (no content change), record in run log.

### -1.3 Dry-Run Check

If `--dry-run` flag present: note it. Continue through STEP 4. Halt before STEP 5 and output the full change plan to the user.

---

## STEP 0 — Load and Read

Load `claude/roadmap/current_roadmap.md` in full.

Load `claude/roadmap/decision_log.md` to verify kill/deferral decisions.

Load `claude/roadmap/roadmap_archive.md` if it exists (to avoid duplicate entries).

Note the current version declared in §1 of the roadmap.

---

## STEP 1 — Classify All Items

For every item in `current_roadmap.md`, apply the classification rules in §6.

Produce an internal classification table:

| Item | Current Status | Classification | Evidence | Action |
|------|---------------|----------------|----------|--------|
| <item name> | <status> | Complete — Retire / Keep / Stale — Flag / Ambiguous | <cycle ref or DL ref> | <action> |

Surface all **Ambiguous** items to the Product Owner with the specific missing evidence. Do not proceed past STEP 1 until all ambiguous items are resolved — either confirmed for retirement or reclassified as Keep.

---

## STEP 2 — Stale Item Review

For each item classified as **Stale — Flag**:

- Add a stale notation to the item in `current_roadmap.md`:
  ```
  > ⚠️ **Stale Notice:** This item has had no cycle activity since <last cycle ref>. Review at next roadmap rebalance.
  ```
- Do not retire stale items — they require a Roadmap Rebalance Engine run to make a prioritisation decision

Record all stale items in the run log.

---

## STEP 3 — Prepare Archive Entries

For each item classified as **Complete — Retire** or **Killed — Retire**, prepare the archive entry:

```markdown
---

## <Item Name>

**Original roadmap location:** <§ reference>
**Status at retirement:** ✅ Complete | ❌ Killed
**Retired from active roadmap:** <date>
**Shipped version:** <version | "N/A — killed">
**Cycle reference:** <cycle_id | "N/A">
**Verification report:** <path | "N/A">
**Decision log reference:** <DL entry | "N/A">
**Retirement confirmed by:** Product Owner

### Original Roadmap Entry

<verbatim copy of the item's full roadmap entry — do not edit>
```

---

## STEP 4 — Produce Change Plan

Produce a complete change plan listing every file and every change:

| File | Action | Item | Reason |
|------|--------|------|--------|
| `current_roadmap.md` | Remove item | <item> | Complete — retiring to archive |
| `current_roadmap.md` | Add stale flag | <item> | No cycle activity |
| `current_roadmap.md` | Update release summary table | Release Summary §8 | Reflect retired items |
| `roadmap_archive.md` | Append | <item> | Retirement |

If `--dry-run`: output this plan and halt. Do not write.

Surface the plan to the user and confirm before proceeding to STEP 5.

---

## STEP 5 — Execute Writes

Execute in this order:

### 5.1 Create or update `claude/roadmap/roadmap_archive.md`

If file does not exist, create with header:

```markdown
**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** <date>

# Roadmap Archive — Momentum Trading Assistant

This document is the permanent record of completed and killed roadmap items retired from `claude/roadmap/current_roadmap.md`. Items are listed in retirement order, most recent first.

Entries are append-only. Do not edit existing entries.

---
```

Append each archive entry prepared in STEP 3.

### 5.2 Update `claude/roadmap/current_roadmap.md`

- Remove all retired items from their sections
- Add stale flags to stale items
- Update the Release Summary table (§8 or equivalent): mark retired items as shipped (✅) or killed (❌) with the shipped version
- Update the `**Last Updated:**` header field
- Do not change any other content — no rewording, no scope changes, no priority reordering
- **Stale `RA:` marker pruning (ST-22, BLG-GOV-260, v8.9):** `<!-- roadmap-annotation-marker: RA:vX.Y:cycle_id -->` blocks (which may appear in §1, §3, §4, §8, or any other section of `current_roadmap.md` — scan the **whole document**, not any one section) retire to a one-line pointer (`*RA:vX.Y retired — see roadmap_archive.md <date> (post-ship closure <cycle_id>).*`) once their release ships or is superseded. These one-line pointers themselves accumulate indefinitely across the document with no forcing function to remove them, even though `roadmap_archive.md` remains the permanent record for anything they'd otherwise re-surface. In this same STEP, scan the entire document and prune (delete outright — the line, not just its content) any already-retired `*RA:vX.Y retired...*` pointer line whose version `vX.Y` is more than 3 releases older than the current highest-numbered release referenced anywhere in `current_roadmap.md` (§1's "Next planned release" or the most recent §8 Release Summary row, whichever is higher). "More than 3 releases older" means: count the number of *shipped* release versions strictly between `vX.Y` and the current highest version (inclusive of the current highest, exclusive of `vX.Y` itself) — if that count exceeds 3, prune. **Scope restriction — numeric identifiers only:** this rule applies only to pointers whose identifier is a numeric release version matching the `vX.Y` pattern (e.g. `RA:v4.4`, `RA:v6.2`). Some retired `RA:` pointers carry a non-version identifier instead (e.g. `RA:Gated-carry-forward-2026-07-27`, recording a gated-item removal rather than a release retirement) — the "how many releases older" computation has no defined answer for these, so leave any `RA:` pointer without a numeric `vX.Y` identifier untouched by this rule regardless of age. Do not prune an active (non-retired) `<!-- roadmap-annotation-marker -->` block under any circumstance — this rule applies only to already-retired one-line pointers. Record the count pruned in the STEP 5.3 run log (new `RA: markers pruned` field, default 0).

### 5.4 Update `claude/roadmap/initiative_register.md`

For every item classified as **Complete — Retire** or **Killed — Retire**, update the `initiative_register.md`:

1. **Load** the Active Initiatives table in `initiative_register.md`.
2. **Find** the row for the retiring item by ID or name (match against the row's Initiative ID or Initiative name column).
3. **Remove** the row from the Active Initiatives table.
4. **Append** a new row to the Completed table:

   | ID | Initiative | Shipped | Release |
   |----|-----------|---------|---------|
   | `<id>` | `<name>` | `<ship date>` | `<version>` |

   - `Shipped`: use the verified ship date from the cycle reference or the roadmap item's delivery date
   - `Release`: use the version string from the roadmap (e.g. `v2.1`)
5. If the Active Initiatives table has no remaining rows after removal, replace its contents with a placeholder: `*No active initiatives as of <date>. [v2.2] scope TBD.*` (adjust version as appropriate).
6. Update the `**Last Updated:**` field in `initiative_register.md`.

**Hard rule:** Do not skip this step. If a completed item exists in `current_roadmap.md` but has no row in `initiative_register.md`, record the gap in the run log (STEP 5.3) and continue — do not halt.

### 5.3 Write run log

Write: `claude/roadmap/manage_roadmap_log_<YYYYMMDD>.md`

```markdown
**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** <date>

# Roadmap Management Run Log — <date>

## Summary

Items retired: <n>
Items flagged stale: <n>
Items kept active: <n>
Ambiguous items resolved: <n>
RA: markers pruned: <n>   # ST-22, BLG-GOV-260, v8.9 — default 0 if none met the >3-releases-older threshold

## Retired Items

| Item | Status | Cycle | Archive ref |
|------|--------|-------|-------------|
| <name> | Complete / Killed | <cycle_id> | roadmap_archive.md |

## Stale Items Flagged

| Item | Last cycle activity | Notice added |
|------|---------------------|-------------|
| <name> | <cycle_id> | Yes |

## Ambiguous Items

| Item | Resolution | Confirmed by |
|------|-----------|-------------|
| <name> | <confirmed retire / kept active> | Product Owner |

## Write Scope Verification

- All writes within Section 5 scope: Yes
- No content changes beyond status and location: Yes
- No backlog modifications: Yes
```

---

## STEP 6 — Update Global State and Commit

Update `.claude_current_state.json`:
```json
{
  "last_manage_roadmap_utc": "<ISO-8601 UTC>",
  "last_manage_roadmap_outcome": "<n> items retired, <n> flagged stale, <n> kept active"
}
```

```
git add claude/roadmap/current_roadmap.md
git add claude/roadmap/roadmap_archive.md
git add claude/roadmap/initiative_register.md
git add claude/roadmap/manage_roadmap_log_<YYYYMMDD>.md
git add .claude_current_state.json
git commit -m "[GOVERNANCE] Roadmap management run <date> — <n> items retired, <n> flagged stale"
git push origin <current-branch>
```

If git operations unavailable: output exact files and commit message. Mark as "Ready to commit."

---

## 7. Completion Condition

The run is complete when:

- All items classified and actioned
- Ambiguous items resolved before any write
- `roadmap_archive.md` updated with all retired items
- `current_roadmap.md` contains only active, planned, gated, and stale-flagged items
- Run log written
- Commit complete (or commit manifest produced)

---

## 8. Governance Invariants

- **No content changes.** Retirement moves items; it does not reword, reprioritise, or rescope them. The archived entry is verbatim.
- **No retirement without evidence.** An item with no verification reference and no decision log entry may not be retired without explicit Product Owner confirmation.
- **Stale items are flagged, not decided.** Only the Roadmap Rebalance Engine may park or kill a stale item.
- **Archive is append-only.** Retired items are permanent records. Do not edit existing archive entries.
- **Backlog is out of scope.** This engine does not touch `claude/backlog/backlog.md`. Use `groom backlog` for backlog changes.
- **Dry-run is safe.** `--dry-run` never writes. It is always safe to run.

---

## Change Log

See: [`claude/system/changelogs/roadmap_management_changelog.md`](changelogs/roadmap_management_changelog.md)
