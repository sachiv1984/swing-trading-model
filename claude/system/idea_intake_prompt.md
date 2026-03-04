**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-03-03
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Team Charter:** claude/charter/team_charter.md

---

# Idea Intake Engine — Governance Prompt

(Window-Controlled, All-Agent, Template-Enforced, Document-Managed)

---

## 1. Purpose

Collect structured idea submissions from all agent roles before a Roadmap Rebalance run, save them to `claude/ideas/submissions/`, and close the window cleanly so the roadmap engine's STEP 4 has a governed, consistent set of inputs to work from.

This engine does **NOT**:
- Evaluate, score, or debate ideas — that is STEP 4 and STEP 5 of the roadmap engine
- Make any decisions about what enters the roadmap
- Modify the roadmap, backlog, or any planning document
- Stay open between runs — the window opens and closes in a single invocation

---

## 2. Invocation Rule (Hard Gate)

This routine executes ONLY when the user issues the explicit command:

```
run ideas [--window-id "<id>"] [--mode "strict|standard"]
```

Rules:
- Invocation must start with `run ideas` (case-insensitive match allowed).
- `--window-id` optional: if omitted, auto-generated as `IW-<YYYYMMDD>-<nn>` (e.g., `IW-20260303-01`). Increment `nn` if a prior window exists for the same date.
- `--mode` optional:
  - `strict`: halt if any agent role fails to submit the minimum required ideas
  - `standard` (default): note non-submitting agents and proceed
- If invocation is not exact, do not run. Treat as conversational.

**Who issues this command:** The PMO Lead persona, prior to issuing `run roadmap`.

**This engine is optional.** The roadmap engine does not require it to have run. If `claude/ideas/submissions/` is empty or absent when `run roadmap` executes, the roadmap engine notes the absence and continues — it does not halt.

**Relationship to roadmap:** Run `run ideas` first, then `run roadmap`. Ideas submitted after `run roadmap` begins are not eligible for the current run.

---

## 3. Canonical Governance Sources (Non-Negotiable)

Binding governance stack (precedence order):

1. `claude/charter/team_charter.md`
2. `claude/charter/document_lifecycle_guide.md`
3. `claude/strategy/strategy_rules.md`
4. Role charters in `claude/agents/`

Shared standards: `claude/system/shared_standards.md`.

---

## 4. Required Roles

All agent roles defined in `claude/agents/` are eligible and expected to submit ideas. This includes:

- Product Owner
- Head of Specs Team
- PMO Lead
- Director of Quality
- Strategy Rules & System Intent Owner
- FinOps & Resource Architect
- Infrastructure & Operations Owner
- Facilitator
- Challenger

**Minimum submissions per agent:** 2 net-new ideas per window (ideas that have not been submitted in a prior window, or that were previously parked and are being resubmitted with updated content).

A resubmitted parked idea counts as 1 net-new idea only if it has been materially updated since it was last parked.

---

## 5. Write Scope Restriction (Hard Gate)

During this routine you may write only to:

- `claude/ideas/submissions/` (create or update individual idea files)
- `claude/ideas/ideas_window.json` (window state file)
- `claude/ideas/` folder (create if absent)

You must **not** modify:
- `claude/roadmap/current_roadmap.md`
- `claude/backlog/backlog.md`
- `claude/ideas/rejected_but_strong.md` (managed by roadmap STEP 4/5 only)
- Any cycle artefact, governance document, or canonical spec

Violation → halt.

---

## 6. Submission File Naming and Location

Each idea is saved as a separate file:

```
claude/ideas/submissions/<agent-slug>-<YYYYMMDD>-<nn>.md
```

Where:
- `<agent-slug>` is the role slug (e.g., `product-owner`, `head-of-specs`, `pmo-lead`, `director-of-quality`, `strategy-owner`, `finops`, `infra-ops`, `facilitator`, `challenger`)
- `<YYYYMMDD>` is today's date
- `<nn>` is a two-digit sequence number per agent per window (e.g., `01`, `02`)

Examples:
- `claude/ideas/submissions/product-owner-20260303-01.md`
- `claude/ideas/submissions/challenger-20260303-01.md`
- `claude/ideas/submissions/challenger-20260303-02.md`

Parked ideas from a prior window that are being carried forward **keep their original filename** — they are not renamed.

---

## 7. Submission Template

Each submission must use the template at `claude/system/idea_template.md`.

Required fields (all must be present and non-empty):

| Field | Required |
|-------|---------|
| Problem Statement | Yes |
| Strategic Alignment — strategy section reference | Yes |
| Strategic Alignment — alignment rationale | Yes |
| Proposed Solution | Yes |
| Expected Value | Yes |
| Effort Estimate — selection made | Yes |
| Reversibility — selection made | Yes |
| What Would You Stop? | Yes — "No view — leave to debate" is acceptable; blank is not |
| Submitter Recommendation — selection made | Yes |

The "What Would You Stop?" field is a prompt to think, not a binding commitment. An answer of "No view — leave to debate" is valid. Displacement decisions are made during STEP 5 of the roadmap engine when all candidates and constraints are visible simultaneously.

If any required field is empty or contains only a placeholder:
- In `strict` mode: the submission is invalid. Record it as non-compliant and do not save it to submissions.
- In `standard` mode: save the file with a `[FIELD REQUIRED]` flag on the incomplete field. The roadmap engine's STEP 4 will treat any `[FIELD REQUIRED]` submission as ineligible to advance until the field is completed.

---

## Mandatory End-to-End Process

---

## STEP -1 — Preflight Gate (Hard Gate)

### -1.1 No Active Window

Read `claude/ideas/ideas_window.json` if it exists:
- If `status = Open`: halt — a window is already open. Close it first or re-invoke with the same `--window-id` to resume.
- If `status = Closed` or file does not exist: proceed.

### -1.2 Required Files Present

Verify:
- `claude/charter/team_charter.md`
- `claude/agents/` folder with at least one agent file
- `claude/system/idea_template.md`

If any missing: halt and report.

### -1.3 Write Permission Test

Create a temporary marker in `claude/ideas/` and confirm it can be written. Remove it. If fails: halt.

---

## STEP 0 — Open Submission Window

Create or update `claude/ideas/ideas_window.json`:

```json
{
  "window_id": "<IW-YYYYMMDD-nn>",
  "opened_utc": "<ISO-8601 UTC>",
  "opened_by": "PMO Lead",
  "status": "Open",
  "mode": "strict | standard",
  "eligible_agents": [],
  "submissions_received": [],
  "submissions_path": "claude/ideas/submissions/",
  "closed_utc": ""
}
```

Populate `eligible_agents` by reading all agent files in `claude/agents/` and extracting the role names.

Create `claude/ideas/submissions/` folder if it does not exist.

Announce the open window to the user:
```
Submission window <window_id> is open.
Eligible agents: <list>
Minimum submissions per agent: 2 net-new ideas
Template: claude/system/idea_template.md
Submit to: claude/ideas/submissions/

Parked ideas from prior windows are available for resubmission. Review claude/ideas/submissions/ for any files with Status: Parked.
```

---

## STEP 1 — Load Prior Parked Ideas

Read `claude/ideas/submissions/` for any files with `**Status:** Parked`.

For each parked idea:
- Surface it to the submitting agent as a candidate for resubmission
- Note the original submission date and window ID
- The agent may: resubmit with updates (file updated, status reset to `Submitted`), leave it parked (no action), or withdraw it (file updated, status set to `Withdrawn`)

Record the count of parked ideas surfaced in `ideas_window.json`.

---

## STEP 2 — Solicit Submissions

For each eligible agent role (in the order they appear in `eligible_agents`), invoke the agent perspective and produce idea submissions using `claude/system/idea_template.md`.

### 2.1 Per-Agent Process

For each agent:
1. Switch to that agent's perspective (per the delegation model in the roadmap prompt §4)
2. Generate a minimum of 2 net-new idea submissions for that agent
3. Each submission must fully complete all required template fields
4. Save each submission to `claude/ideas/submissions/` using the naming convention in §6
5. Update `ideas_window.json.submissions_received` with the filename

### 2.2 Submission Quality Check

After generating each submission, verify:
- All required fields are present and non-empty (or contain a valid "no view" response where permitted)
- Strategic alignment cites a specific section of `strategy_rules.md` — not generic alignment
- Expected value names a specific metric or outcome — not "improved performance"
- In `strict` mode: a submission failing this check is discarded and regenerated
- In `standard` mode: a submission failing this check is saved with `[FIELD REQUIRED]` flags

### 2.3 Missing Agent Handling

If an agent role exists in `claude/agents/` but produces no submissions (e.g. their charter indicates a very narrow domain):
- In `strict` mode: halt and report which agent failed to submit the minimum.
- In `standard` mode: record in `ideas_window.json` as `submitted: 0` and note the gap. Continue.

---

## STEP 3 — Close Submission Window

Update `claude/ideas/ideas_window.json`:

```json
{
  "status": "Closed",
  "closed_utc": "<ISO-8601 UTC>",
  "total_submissions": <n>,
  "agents_submitted": [<list of agent slugs that submitted>],
  "agents_not_submitted": [<list of agent slugs with 0 submissions>],
  "parked_ideas_carried": <n>,
  "new_submissions": <n>
}
```

---

## STEP 4 — Produce Window Summary

Write: `claude/ideas/submissions/window_summary_<window_id>.md`

```markdown
**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** <date>
**Window:** <window_id>

# Idea Intake Summary — <window_id>

## Window Status: Closed

Opened: <date/time>
Closed: <date/time>

## Submission Counts

| Agent | New Submissions | Parked Resubmitted | Total |
|-------|-----------------|--------------------|-------|
| <role> | N | N | N |
| ... | | | |
| **Total** | **N** | **N** | **N** |

## Agents Without Minimum Submissions

<List any agents below 2 net-new submissions, or "None — all agents met minimum">

## Ideas Available for Roadmap STEP 4

| Idea ID | Agent | Title | Recommendation | Status |
|---------|-------|-------|----------------|--------|
| IDEA-xx | <role> | <title> | Advance / Park / Reject | Submitted |
| ... | | | | |

## Parked Ideas Carried Forward (Not Resubmitted)

| Idea ID | Agent | Title | Original Window |
|---------|-------|-------|----------------|
| ... | | | |

## Notes

<Any gaps, non-compliant submissions flagged, or process notes>
```

---

## STEP 5 — Commit

```
git add claude/ideas/submissions/
git add claude/ideas/ideas_window.json
git commit -m "[GOVERNANCE] Idea intake window closed: <window_id> — <n> submissions"
git push origin <current-branch>
```

If git operations unavailable: output exact files and commit message. Mark as "Ready to commit."

---

## 8. Completion Condition

The run is complete when:

- `ideas_window.json` status = `Closed`
- All agent submissions are saved to `claude/ideas/submissions/` (or gaps are recorded)
- `window_summary_<window_id>.md` exists
- STEP 5 commit complete (or commit manifest produced)

---

## 9. Document Lifecycle — Post-Roadmap Run

The roadmap engine's STEP 4 is responsible for managing idea documents after a roadmap run. The intake engine does not handle post-run cleanup. For reference, the expected outcomes are:

| Idea outcome in roadmap STEP 4/5 | Document action |
|----------------------------------|-----------------|
| ✅ Promoted to roadmap (Add decision in STEP 8) | Status updated to `Promoted` — file remains as historical record |
| ❌ Rejected | Status updated to `Rejected`; if strong, copied to `claude/ideas/rejected_but_strong.md` |
| 🅿 Parked | Status remains `Parked` (or updated to `Parked` if it was `Submitted`) — stays in submissions for next window |
| Withdrawn by agent | Status updated to `Withdrawn` — file remains as record |

The submissions folder is never bulk-cleared. Document state is managed item by item.

---

## 10. Governance Invariants

- **Window-controlled only.** No submissions are accepted outside an open window managed by this engine.
- **Template compliance is mandatory.** An incomplete submission is either discarded (strict) or flagged (standard) — it is never silently accepted.
- **No decisions made here.** The intake engine collects and structures. The roadmap engine decides.
- **Parked ideas persist.** A parked idea is never deleted by the intake engine. It stays until the roadmap engine or the submitting agent withdraws it.
- **Displacement is not required at submission time.** The "What Would You Stop?" field invites thinking — it is not a gate. Displacement is determined in STEP 5 of the roadmap engine where all candidates and constraints are visible simultaneously.
- **All agent roles submit.** Domain breadth matters — a narrow domain does not exempt an agent from the minimum. If no net-new ideas exist, the agent records that explicitly rather than submitting nothing.


---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.1 | 2026-03-03 | Removed "Proposed Displacement" as a required submission field. Replaced with "What Would You Stop?" as a non-binding thinking prompt — "No view — leave to debate" is a valid answer. Displacement is now determined in STEP 5 of the roadmap engine. Updated required fields table, submission quality check, and governance invariants accordingly. Updated idea_template.md to match. |
| 1.0 | 2026-03-03 | Initial version. |