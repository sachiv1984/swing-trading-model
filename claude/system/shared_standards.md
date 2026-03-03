**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-03-02

# Shared Standards — All Governed Routines

This file defines standards that apply across all three governance prompts. Each prompt references this file rather than repeating these definitions. When a prompt says "per shared_standards", read this file.

---

## 1. Governance Stack (Precedence Order)

All governed routines operate under this binding stack:

1. `claude/charter/team_charter.md`
2. `claude/charter/document_lifecycle_guide.md`
3. `claude/strategy/strategy_rules.md`
4. Role charters in `claude/agents/`

No routine, user instruction, or delivery pressure may override the above.

---

## 2. Hard Gate Semantics

A **hard gate** is a condition that must be satisfied before execution may continue. When a hard gate fails:

1. Stop execution immediately
2. Output the halt report (§5 below)
3. Update state to `Blocked` before halting (do not halt without writing state)
4. Wait for user — do not attempt to self-resolve

A hard gate may only be cleared by the relevant domain authority. The Facilitator may not waive a hard gate.

---

## 3. Identifier Standards

| Type | Format | Required at |
|------|--------|-------------|
| Scope items | `S2-01`, `S2-02` | Stage 2 (Release Planning) |
| Epics | `EPIC-01`, `EPIC-02` | Stage 3 (Release Planning) |
| Stories | `ST-01`, `ST-02` | Sprint Backlog |
| Tasks | `TASK-01` | Sprint Backlog (optional) |
| Risks | `RISK-01`, `RISK-02` | Stage 3 (Release Planning) |
| Escalations (Release) | `ESC-YYYYMMDD-nn` | Escalations file |
| Escalations (Execution) | `ESC-EXEC-YYYYMMDD-nn` | Execution escalations file |
| Delegation records | `DEL-YYYYMMDD-nn` | Delegation log |

IDs must be stable — never renumber existing IDs. Missing IDs on required fields is a Process Integrity failure that halts execution.

---

## 4. Escalation Record Format

Used in: `claude/cycles/<cycle_id>/escalations.md` and `claude/cycles/<cycle_id>/execution_escalations.md`

These files are **append-only**. Never edit a previous entry.

### Header (create on first write)

```
Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: <date>
```

### Entry format

```
## <ESC-ID>

- **Raised at:** <ISO-8601 UTC>
- **Routine:** <Roadmap Rebalance | Release Planning | Sprint Execution>
- **Cycle ID:** <cycle_id>
- **Step:** <step number or name>
- **ST/EPIC item:** <if applicable>
- **Trigger type:** Lifecycle | Strategy | Quality | Workforce | GitHub | Human-Delegation | Other
- **Blocking statement:** <one paragraph, precise and factual>
- **Owning authority:** <role>
- **Unblock criteria:** <what must be true to resume>
- **SLA due-by:** <date/time>
- **Blocks execution:** Yes | No
- **Disposition:** Open | Resolved | Accepted Risk | Deferred
- **Resolution summary:** <complete when closing; include evidence links>
```

### Escalation SLAs

| Trigger Type | SLA | Can Be Accepted Risk? |
|-------------|-----|-----------------------|
| Lifecycle / Process Integrity | 24 hours | **Never** |
| Strategy boundary | 72 hours | **Never** |
| Quality | Before execution | **Never** |
| Workforce / Capacity | Next planning checkpoint | Yes — Product Owner only |
| Schedule / Delivery | Next planning checkpoint | Yes — Product Owner only |

Strategy, Quality, and Lifecycle escalations may never be marked Accepted Risk. Attempting to do so is a governance violation requiring a routine halt.

---

## 5. Standard Halt Report Format

When a hard gate fires or a blocking condition is encountered, output exactly this structure:

```
🛑 HALT — <Gate Name>

Routine:     <Roadmap Rebalance | Release Planning | Sprint Execution>
Cycle:       <cycle_id>
Step:        <step number>
Gate:        <gate name>

What failed:
  <specific condition that failed — one sentence per failed item>

Evidence found:
  <what was checked and what was found — be specific, not generic>

Evidence missing:
  <what would be needed to pass this gate>

State written:
  <confirm state file updated to Blocked, or explain why not>

To resume:
  <exact command to re-invoke once the condition is resolved>
  e.g.: run sprint --cycle "2026-03-02__release-v1.7"
```

Do not halt with a terse message. Always output the full halt report so the user knows exactly what is needed.

---

## 6. GitHub CLI Commands (Standard Operations)

Use `gh` CLI for all GitHub operations. Do not use the GitHub API directly.

### Issue operations

```bash
# Create issue (body content per claude/system/gh_issue_template.md)
gh issue create \
  --title "[ST-xx] <title>" \
  --body "<populated gh_issue_template.md>" \
  --label "sprint" --label "EPIC-xx"

# Update issue to in-progress
gh issue edit <number> --add-label "in-progress"

# View issue (to check if it exists)
gh issue list --search "[ST-xx]" --json number,title,state
```

**Issue body format:** Use `claude/system/gh_issue_template.md` as the body template. Variable mapping:
- `{{ID}}` → EPIC-xx (the parent epic)
- `{{ST_ID}}` → ST-xx (the story)
- `{{TITLE}}` → story title from `sprint_backlog.md`
- `{{CYCLE_ID}}` → active cycle_id from `.claude_current_state.json`
- `{{PARENT_EPIC}}` → EPIC-xx
- `{{OBJECTIVE_TEXT}}`, `{{AC_1}}` etc. → from acceptance criteria in `sprint_backlog.md`

**Do not manually close issues** that will be closed by `governance_sync.yml` on push. Issues are auto-closed by CI when a commit with `[EPIC-xx][ST-xx]` format is pushed to an `exec/**` branch.

### PR operations

```bash
# Create PR
gh pr create \
  --title "[EPIC-xx] <epic description>" \
  --body "<body per prompt spec>" \
  --base main \
  --head exec/<cycle_id>/EPIC-xx

# Check PR status
gh pr view <number> --json state,reviews,statusCheckRollup

# List open PRs for this cycle
gh pr list --search "exec/<cycle_id>" --json number,title,state
```

### Branch operations

```bash
# Create EPIC branch from main
git checkout main && git pull
git checkout -b exec/<cycle_id>/EPIC-xx
git push -u origin exec/<cycle_id>/EPIC-xx

# Check if branch exists remotely
git ls-remote --heads origin exec/<cycle_id>/EPIC-xx
```

---

## 7. Append-Only File Rule

The following files are append-only within their cycle. Never edit a previous entry:

- `claude/cycles/<cycle_id>/escalations.md`
- `claude/cycles/<cycle_id>/execution_escalations.md`
- `claude/cycles/<cycle_id>/delegation_log.md`
- `claude/roadmap/decision_log.md`

If a correction is needed to a previous entry, append a correction note referencing the original entry ID. Do not overwrite.

---

## 8. Resumability Protocol

Every governed routine is resumable. On every invocation:

1. **First action:** Read the relevant state file (`state.json` or `execution_state.json`)
2. If the file exists and status is not `not_started` or `Initialized`: you are resuming
3. Skip all completed steps (any step whose output artefact exists and is valid)
4. Re-evaluate all `blocked_*` items: check whether their unblock criteria are now met
5. Resume from the first incomplete or newly unblocked item
6. Never re-execute a step that already produced a valid output

If the state file does not exist: this is a fresh run. Proceed from STEP -1.

---

## 9. Lifecycle Compliance Quick Reference

Every governed artefact must have a complete header. Minimum required fields by class:

| Class | Required Fields |
|-------|----------------|
| Class 1 (Canonical) | Owner, Status: Canonical, Version, Last Updated |
| Class 3 (Operational Record) | Owner, Status: Operational Record, Report Date, Filed |
| Class 4 (Planning Document) | Owner, Class: Planning Document (Class 4), Status, Last Updated |
| Class 6 (Governance Prompt) | Owner, Status: Active, Version, Last Updated |

A document without a complete header is non-compliant and must not be relied upon. Non-compliant documents discovered during a routine: apply header remediation (headers only) and continue.