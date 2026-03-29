---
name: dev-file
description: File a formal deviation record (DEV-*) when an implemented story doesn't fully meet its acceptance criteria. Use this skill whenever a story is found to have a gap, bug, or AC shortfall during delivery verification or QA sign-off — when someone says "this doesn't meet the spec", "file a deviation", "log this as a deviation", "this is a P2 issue", or when the DoQ sign-off block identifies unmet acceptance criteria. Also use proactively during sprint execution when you discover that what was built differs from the canonical spec.
---

# Dev File

Files a correctly-formatted, correctly-IDed deviation record into the right QA evidence log.

## Step 0 — Load lessons

Read `.claude/skills/lessons_learnt.md`. Look for entries tagged `[dev-file]` and apply them. If the file doesn't exist, continue.

## Step 1 — Gather inputs

Collect the following. Infer what you can from context; ask only for what you genuinely cannot determine:

| Field | Required | Guidance |
|-------|----------|---------|
| EPIC | Yes | Which EPIC the story belongs to (EPIC-01 through EPIC-0N) |
| Story | Yes | Which ST item (ST-01, ST-02, etc.) |
| AC reference | Yes | Which acceptance criterion was not met (e.g. "AC-2.3" or quote the criterion) |
| Expected behaviour | Yes | What the spec or AC says should happen |
| Actual behaviour | Yes | What was actually observed |
| Priority | Yes | P1 High / P2 Medium / P3 Low (see guide below) |
| Backlog action | Yes | New BLG item ID if one should be filed, "Cosmetic — no backlog action", or "Accepted as-is" |
| Notes | No | Optional: workaround, context, reproduction steps |

**Priority guide:**
- **P1** — Functional defect that breaks a user workflow or corrupts data. Blocks the next release if not resolved.
- **P2** — Functional gap or spec deviation with a workaround. Should be resolved within 1–2 cycles.
- **P3** — Cosmetic, low-impact, or edge-case gap. Can be deferred without user impact.

## Step 2 — Determine the deviation ID

Read the target qa_evidence file to find the highest DEV-{EPIC}{story} sequence number already filed. The ID format is:

```
DEV-EPIC{nn}-ST{nn}-{seq}
```

Examples: `DEV-EPIC02-ST05-01`, `DEV-EPIC03-ST07-02`

- If no deviations exist yet for this EPIC+story, start at `-01`
- If `-01` exists, use `-02`, etc.
- Grep the qa_evidence file and the qa_evidence files from the prior cycle to be sure:

```
grep -r "DEV-EPIC{nn}-ST{nn}" claude/cycles/{cycle_id}/ 2>/dev/null
```

## Step 3 — Find the qa_evidence file

The qa_evidence file path is:
```
claude/cycles/{cycle_id}/qa_evidence_{EPIC}.md
```

where `{cycle_id}` comes from `.claude_current_state.json` → `active_cycle`.

The deviation block goes at the end of the story's section in that file — after the acceptance criteria checklist, before the `---` separator.

## Step 4 — Write the deviation block

Insert the following block at the correct location in the qa_evidence file:

```markdown
### {DEV-ID}
**Priority:** {P1|P2|P3}
**Story:** {ST-nn}
**AC:** {AC reference or quoted criterion}
**Expected:** {what the spec/AC says}
**Actual:** {what was observed}
**Impact:** {who is affected, how severe, whether it blocks anything}
**Backlog action:** {BLG-xxx filed / Cosmetic — no backlog action / Accepted as-is}
{**Notes:** {optional notes} — only if notes were provided}
```

## Step 5 — Update the EPIC consolidation block

Every qa_evidence file has a consolidation table near the end. Find the row for the affected story and update the Deviations column to reference the new DEV-ID.

If the consolidation block doesn't exist yet (the sprint is still early), skip this step — it will be completed at verification time.

## Step 6 — Update execution_state.json

Find the story entry in `claude/cycles/{cycle_id}/execution_state.json`. Set:
```json
"deviations_filed": true
```

(If the field is already `true` because a prior deviation exists, leave it — it stays true.)

## Step 7 — Create a backlog item if P1 or P2

If the deviation is P1 or P2, and the Backlog action is not "Accepted as-is":
- If a BLG item ID was already determined, confirm it or create it now using the `/backlog-add` skill
- If no BLG item was identified yet, prompt the user: "This is a P{n} deviation — do you want to file a backlog item now, or defer that decision?"

P3 cosmetic deviations do not require a backlog item unless the user requests one.

## Step 8 — Confirm

Tell the user:
- The deviation ID assigned
- The file it was written to
- The priority and backlog action
- Whether execution_state.json was updated

## Error handling and lessons learnt

If the ID was wrong, the wrong file was modified, or the format was off, fix it immediately and append to `.claude/skills/lessons_learnt.md`:

```
| {YYYY-MM-DD} | dev-file | {what went wrong — e.g. "wrong seq number", "wrong qa_evidence file"} | {correct approach} |
```

Common mistakes to watch for:
- Checking only the current cycle for existing DEV-IDs — also check prior cycles to be safe
- Writing the deviation outside the correct story section — always confirm the `## ST-nn` heading before inserting
- Forgetting to update `deviations_filed` in execution_state.json
