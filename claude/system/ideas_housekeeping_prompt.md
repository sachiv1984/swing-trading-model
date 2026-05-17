**Owner:** PMO Lead
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-16
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Team Charter:** claude/charter/team_charter.md

---

# Ideas Housekeeping Engine — Governance Prompt

(Ideas Register Archiving, Rejected-But-Strong Revival Review)

---

## 1. Purpose

This engine performs two housekeeping tasks against the ideas pipeline:

1. **Archive terminal rows** from `claude/ideas/ideas_register.md` into `claude/ideas/ideas_register_archive.md` — keeping the active register lean and readable.
2. **Review revival conditions** in `claude/ideas/rejected_but_strong.md` — surfacing any entries whose stated gate condition appears to have been met in the just-closed cycle.

This engine does **NOT**:
- Promote ideas to the backlog — that requires the Roadmap Rebalance Engine.
- Add or modify entries in `rejected_but_strong.md`.
- Change the scope or definition of any idea entry.
- Modify the backlog, roadmap, or any cycle artefact.

---

## 2. Invocation Rule

### 2.1 Subroutine Invocation (Primary)

This engine is invoked as a subroutine from:

| Caller | Trigger point | Pass-through flags |
|--------|---------------|--------------------|
| `post_ship_closure.md` STEP 12.5 | After STEP 12 (`groom backlog`) completes | `--dry-run` |
| `roadmap_prompt.md` STEP -1.5 (advisory) | Before STEP 1 debate, if not run at post-ship | `--dry-run` |

### 2.2 Standalone Invocation

This routine may also be invoked standalone:

```
run ideas housekeeping [--dry-run]
```

Rules:
- Invocation must match `run ideas housekeeping` (case-insensitive).
- `--dry-run`: produces the archive plan and revival advisory without writing any files. Outputs the plan to the user and halts before STEP 3.
- If invocation is not exact, do not run. Treat as conversational.

**Who issues this command:** PMO Lead.

**Valid standalone trigger windows:**

| Window | Rationale |
|--------|-----------|
| After Post-Ship Closure (if not already run as subroutine) | Ensures register reflects shipped state before new cycle opens |
| Immediately before `run roadmap` | Gives the Roadmap Engine a clean, uncluttered register |

---

## 3. Canonical Governance Sources (Non-Negotiable)

Canonical governance stack: per `claude/system/shared/governance_stack.md`. This routine may not override any entry in that stack.

---

## 4. Required Roles

| Role | Function in this engine |
|------|------------------------|
| PMO Lead | Confirms ambiguous classification; reviews revival advisory output |
| Facilitator | Executes engine steps; enforces write scope |

---

## 5. Write Scope Restriction (Hard Gate)

During this routine you may write only to:

- `claude/ideas/ideas_register.md` (remove archived rows — content verbatim, no rewording)
- `claude/ideas/ideas_register_archive.md` (append archived rows — create if absent)

You must **not** modify:
- `claude/ideas/rejected_but_strong.md`
- `claude/ideas/ideas_register.md` row content beyond removing terminal rows
- Any backlog, roadmap, cycle artefact, canonical spec, or governance document

Violation → halt.

---

## 6. Terminal Status Classification

### 6.1 Archive-eligible (terminal)

| Status | Condition | Notes |
|--------|-----------|-------|
| `Promoted-Added` | Always | Idea lifecycle complete; backlog item tracks from here |
| `Promoted-Rejected` | Always | Idea was evaluated and closed |
| `Rejected` | Step 5 column shows `❌ Rejected (not strong)` AND idea ID does NOT appear in `rejected_but_strong.md` | Confirm cross-reference before archiving |
| `Rejected` | Park Rationale contains "Retired", "Permanently closed", or equivalent explicit closure language AND idea ID does NOT appear in `rejected_but_strong.md` | Confirm cross-reference before archiving |

### 6.2 Keep (non-terminal)

| Status / Condition | Reason |
|--------------------|--------|
| `Parked-cycle-<n>` or non-zero Park Count with no terminal Step 5 | Still in evaluation |
| `Rejected` AND idea ID present in `rejected_but_strong.md` | Revival conditions may be met |
| `Rejected` AND Step 5 shows `❌ Rejected (strong)` | Candidate for `rejected_but_strong.md` — flag to PMO Lead if not already present |
| `Submitted` | Not yet evaluated |

### 6.3 Ambiguous — Confirm

If a row's terminal status cannot be determined from the Status, Step 4, and Step 5 columns alone: surface to PMO Lead before archiving. Do not archive under uncertainty.

---

## Mandatory End-to-End Process

---

## STEP -1 — Preflight Gate (Hard Gate)

Verify the following files are present and readable:

- `claude/ideas/ideas_register.md`
- `claude/ideas/rejected_but_strong.md`
- `claude/charter/team_charter.md`

If any missing: halt and report.

If invoked as a subroutine from post-ship: read the just-closed `cycle_id` from `.claude_current_state.json` — required for STEP 2.

---

## STEP 1 — Ideas Register: Identify and Archive Terminal Rows

### 1.1 Classify all rows

Read every row in `claude/ideas/ideas_register.md`. For each row apply §6 classification:

- Mark as **Archive** if terminal per §6.1.
- Mark as **Keep** if non-terminal per §6.2.
- Mark as **Ambiguous** if classification cannot be determined — surface each to PMO Lead before proceeding.

### 1.2 Dry-run output

If `--dry-run`: output the full classification list (Archive / Keep / Ambiguous) grouped by classification. State the total counts. Halt — do not proceed to 1.3.

### 1.3 Archive terminal rows

For each row classified Archive:
1. Append the row verbatim to `claude/ideas/ideas_register_archive.md` under the heading `## Archived <YYYY-MM-DD>` (create the file and heading if absent; append to an existing dated heading if already present from this run).
2. Remove the row from `claude/ideas/ideas_register.md`.

Do not reword, reorder, or modify any row content. Archive is verbatim.

### 1.4 Update header

Update the `**Last Updated:**` field in `claude/ideas/ideas_register.md` to today's date with a brief note, e.g.:
```
**Last Updated:** 2026-05-16 (ideas_housekeeping — N rows archived)
```

### 1.5 Output

Report: rows archived (count and IDEA IDs), rows kept (count), ambiguous rows surfaced (count and IDEA IDs).

---

## STEP 2 — Rejected-But-Strong: Revival Condition Review

### 2.1 Load context

Read `claude/ideas/rejected_but_strong.md`. For each entry note the IDEA ID and its **Revival condition** text.

If invoked as post-ship subroutine: also read the just-closed cycle's `claude/cycles/<cycle_id>/sprint_backlog.md` (completed stories), the cycle closure record, and any OAs logged in post-ship STEP 6.

If invoked standalone or from roadmap: read `claude/roadmap/decision_log.md` and the most recent closed cycle's sprint_backlog for context.

### 2.2 Evaluate each revival condition

For each entry assess whether the revival condition appears to have been met, partially met, or remains unmet, based on what shipped in the most recently closed cycle and the current governance state.

This assessment is judgment-based — revival conditions are narrative, not mechanical. Apply reasonable interpretation. When in doubt, mark as Unmet and note the uncertainty.

| Assessment | Meaning |
|------------|---------|
| **Met** | The stated gate condition is satisfied based on shipped items or documented decisions |
| **Partially met** | Meaningful progress toward the gate condition but not fully satisfied |
| **Unmet** | No evidence the gate condition has been satisfied |

### 2.3 Output

For each entry output:

```
IDEA ID:          <id>
Title:            <title>
Revival condition: <condition text>
Assessment:       Met / Partially met / Unmet
Evidence:         <brief rationale — shipped story IDs or governance decisions, or "none observed">
```

### 2.4 Advisory

If any entry is assessed **Met** or **Partially met**:

Produce an advisory block for inclusion in the post-ship Advisory Summary (or standalone output):

> ⚠ Rejected-But-Strong Revival: N idea(s) in `rejected_but_strong.md` have revival conditions that appear Met or Partially Met following the just-closed cycle. PMO Lead should review and decide whether to re-submit these ideas via `run ideas` before the next roadmap run.
>
> [List each: IDEA ID — Title — Assessment]

If all entries are Unmet: note "Rejected-But-Strong: all revival conditions remain unmet — no action required."

This step is advisory only. It does not modify `rejected_but_strong.md` or submit ideas to the register.

---

## STEP 3 — Ideas Pipeline Health Check (Advisory)

After STEP 2 completes, count the remaining active items in `claude/backlog/backlog.md` (items not marked COMPLETE, CLOSED, or ARCHIVED).

If the active backlog count is **5 or fewer**:
- Scan `claude/ideas/ideas_register.md` for rows with `Status: Parked-cycle-<n>` whose Park Rationale references a specific backlog item ID (any `BLG-` reference).
- For each such row, check whether the referenced item has shipped (present in a prior cycle's `sprint_backlog.md` as a completed ST story, or marked COMPLETE in `backlog.md`).
- If M ≥ 1 such rows exist: add to advisory output — "⚠ Ideas Pipeline: active backlog nearly clear (N items). M parked ideas have gate conditions that may now be satisfied — consider `run ideas` before next roadmap run."

This step is advisory only — it does not halt execution and does not modify any file.

---

## STEP 4 — Subroutine Handoff / Standalone Close

### If invoked as subroutine from post-ship:

Return the following to the calling engine for inclusion in the Advisory Summary block:
- STEP 1 archive summary (counts and IDEA IDs)
- STEP 2 revival advisory block (or "no action required" note)
- STEP 3 pipeline health advisory (or "pipeline healthy — no action required" note)

Do **not** commit — the calling engine (post-ship STEP 13) owns the commit.

### If invoked standalone:

Output the full STEP 1 and STEP 2 results to the user.

Commit artefacts modified by this run:

```
git add claude/ideas/ideas_register.md
git add claude/ideas/ideas_register_archive.md    (if modified or created)
```

Commit message format:
```
[GOVERNANCE] Ideas housekeeping <YYYYMMDD> — N rows archived, revival review complete
```

---

## 7. Governance Invariants

- **No content changes.** Archiving moves rows verbatim — no rewording, reprioritising, or editing.
- **Archive is append-only.** Archived entries are permanent records. Do not edit existing archive entries.
- **No promotion.** This engine never adds items to the backlog or roadmap. The revival advisory is informational only.
- **Cross-reference before archiving.** Any `Rejected` row must be confirmed absent from `rejected_but_strong.md` before archiving.
- **Dry-run is safe.** `--dry-run` never writes. Always safe to run.
- **Subroutine does not commit.** When invoked as a subroutine, the calling engine owns the commit.

---

## Change Log

See: [`claude/system/changelogs/ideas_housekeeping_changelog.md`](changelogs/ideas_housekeeping_changelog.md)
