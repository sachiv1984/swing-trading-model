**Owner:** Head of Specs Team
**Status:** Active
**Version:** 2.8
**Last Updated:** 2026-07-27
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Team Charter:** claude/charter/team_charter.md

---

# Idea Intake Engine — Governance Prompt

(Window-Controlled, Role-Selective, Template-Enforced, Document-Managed)

---

## 1. Purpose

Collect structured idea submissions from all agent roles before a Roadmap Rebalance run, append/update rows in `claude/ideas/ideas_register.md`, and close the window cleanly so the roadmap engine's STEP 4 has a governed, consistent set of inputs to work from.

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

Canonical governance stack: per `claude/system/shared/governance_stack.md`. This routine may not override any entry in that stack.

Shared standards: `claude/system/shared_standards.md`.

---

## 4. Required Roles

The following agent roles are eligible and expected to submit ideas (all roles defined in `claude/agents/` except the Facilitator):

- AI Compliance & Governance Officer
- API Contracts & Documentation Owner
- Backend Engineering Patterns Owner
- Base44 Frontend Prompt Owner
- Challenger
- Cybersecurity & Trust Lead
- Data Model & Domain Schema Owner
- Director of HR
- Director of Quality
- Financial Reporting & Records Owner
- FinOps & Resource Architect
- Frontend Specifications & UX Documentation Owner
- Head of Engineering
- Head of Specs Team
- Head of UX & Design
- Infrastructure & Operations Owner
- Metrics Definitions & Analytics Canonical Owner
- PMO Lead
- Product Owner
- QA Lead
- QA & Testing Owner
- Strategy Rules & System Intent Owner

**Excluded role:** The Facilitator does not submit ideas. The Facilitator's role is to manage the intake process, not to generate submissions. This is a permanent structural exclusion — absent a window count is expected and is not a process error. When computing `agents_not_submitted`, the Facilitator must not be counted as missing.

**Minimum submissions per agent:** 2 net-new ideas per window (ideas that have not been submitted in a prior window, or that were previously parked and are being resubmitted with updated content).

A resubmitted parked idea counts as 1 net-new idea only if it has been materially updated since it was last parked.

---

## 5. Write Scope Restriction (Hard Gate)

During this routine you may write only to:

- `claude/ideas/ideas_register.md` (append new rows; update status fields on re-submitted parked ideas)
- `claude/ideas/ideas_window.json` (window state file)
- `claude/ideas/` folder (create if absent)

You must **not** modify:
- `claude/roadmap/current_roadmap.md`
- `claude/backlog/backlog.md`
- `claude/ideas/rejected_but_strong.md` (managed by roadmap STEP 4/5 only)
- `claude/ideas/submissions/` or `claude/ideas/submissions/archive/` — these are read-only archives
- Any cycle artefact, governance document, or canonical spec

Violation → halt.

---

## 6. Idea ID Convention and Register Location

All ideas are stored as rows in `claude/ideas/ideas_register.md` (schema: per `shared_standards.md §16.5`).

Each new idea is assigned an Idea ID:

```
IDEA-<agent-slug>-<YYYYMMDD>-<nn>
```

Where:
- `<agent-slug>` is the role slug from the table below
- `<YYYYMMDD>` is today's date
- `<nn>` is a two-digit sequence number per agent per window (e.g., `01`, `02`)

| Role | Slug |
|------|------|
| AI Compliance & Governance Officer | `ai-compliance` |
| API Contracts & Documentation Owner | `api-contracts` |
| Backend Engineering Patterns Owner | `backend-engineering` |
| Base44 Frontend Prompt Owner | `base44-frontend` |
| Challenger | `challenger` |
| Cybersecurity & Trust Lead | `cybersecurity` |
| Data Model & Domain Schema Owner | `data-model` |
| Director of HR | `director-of-hr` |
| Director of Quality | `director-of-quality` |
| Financial Reporting & Records Owner | `financial-reporting` |
| FinOps & Resource Architect | `finops` |
| Frontend Specifications & UX Documentation Owner | `frontend-specs` |
| Head of Engineering | `head-of-engineering` |
| Head of Specs Team | `head-of-specs` |
| Head of UX & Design | `head-of-ux` |
| Infrastructure & Operations Owner | `infra-ops` |
| Metrics Definitions & Analytics Canonical Owner | `metrics` |
| PMO Lead | `pmo-lead` |
| Product Owner | `product-owner` |
| QA Lead | `qa-lead` |
| QA & Testing Owner | `qa-testing` |
| Strategy Rules & System Intent Owner | `strategy-owner` |

Examples:
- `IDEA-product-owner-20260303-01`
- `IDEA-challenger-20260303-02`
- `IDEA-ai-compliance-20260303-01`

**Parked ideas from a prior window** are already rows in `ideas_register.md` — they are not renamed or re-entered. The intake engine surfaces them for agent review and updates their status if resubmitted.

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

## STEP -0.5 — Stale Idea Horizon Check (Advisory)

Before opening the window, the Facilitator must check `claude/ideas/ideas_register.md` for rows with `Status: Parked-cycle-2`.

- Count all rows with `Status: Parked-cycle-2`.
- If **15 or more rows** are at `Parked-cycle-2`: surface the following advisory in the window announcement and in the window summary (STEP 4):

  > ⚠️ **Stale warning:** {n} ideas are currently at Parked-cycle-2. At the next roadmap rebalance run, all of these will reach the stale threshold (Parked-cycle-3) and require mandatory active Product Owner disposition per §4.5. To reduce the STEP 4 burden at that run, the PO may wish to pre-emptively review and withdraw any ideas that are clearly no longer relevant before the roadmap run.

- If fewer than 15 rows are at `Parked-cycle-2`: no advisory. Proceed to STEP 0.

This check is advisory only — it does not halt the window or change classification logic.

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
  "register_path": "claude/ideas/ideas_register.md",
  "closed_utc": ""
}
```

Populate `eligible_agents` by reading all agent files in `claude/agents/` and extracting the role names.

Create `claude/ideas/ideas_register.md` if it does not exist (use the header from `shared_standards.md §16.5`).

Announce the open window to the user:
```
Submission window <window_id> is open.
Eligible agents: <list>
Minimum submissions per agent: 2 net-new ideas
Template: claude/system/idea_template.md
Register: claude/ideas/ideas_register.md

Parked ideas from prior windows are available for resubmission. Review claude/ideas/ideas_register.md for any rows with Status: Parked-cycle-<n>.
```

---

## STEP 1 — Load Prior Parked Ideas

Read `claude/ideas/ideas_register.md` for any rows with `Status: Parked-cycle-<n>` (where `<n>` is any positive integer).

For each parked idea:
- Surface it to the submitting agent as a candidate for resubmission
- Note the original submission date, window ID, and current park count
- The agent may: resubmit with updates (register row updated: Status reset to `Submitted`, Park Rationale updated), leave it parked (no action — cycle count will increment in STEP 4 of the next roadmap run), or withdraw it (register row updated: Status set to `Withdrawn`)

Record the count of parked ideas surfaced in `ideas_window.json`.

---

## STEP 2 — Solicit Submissions

For each eligible agent role (in the order they appear in `eligible_agents`), invoke the agent perspective and produce idea submissions using `claude/system/idea_template.md`.

### 2.0 Parked Queue Pre-Check (Required — before any new submission)

Before generating new idea submissions, each agent must:

1. Read `claude/ideas/ideas_register.md` for any rows where:
   - `Status` is `Parked-cycle-<n>` (any park count), **and**
   - the `Submitter` column contains the agent's name or slug
2. For each such parked idea: assess whether any planned new submission covers substantially similar scope (same initiative, same problem statement, same endpoint or feature area).
3. **If overlap detected:**
   - Resubmit the parked idea with updated content (register row Status reset to `Submitted`, Park Rationale updated with new context) rather than creating a new entry.
   - Note the overlap explicitly in the submission or Park Rationale field.
   - A resubmitted parked idea counts as 1 net-new submission (if materially updated).
4. **If no overlap:** proceed to generate new submissions per §2.1.

This check prevents duplicate submissions that burden STEP 4 with unnecessary classification work (friction type D, recurring — meta-review patch 2026-06-02, idea_intake_prompt.md v2.4).

5. **Backlog scope overlap check (mandatory act, non-blocking outcome — v2.8, `2026-07-27__scheduled` Friction Item 1):** Before finalising each new submission topic, the submitting agent must grep `claude/backlog/backlog.md` for keyword matches against the planned topic (title nouns, feature/mechanism name). This is a required step, not an optional scan — record the result explicitly:
   - **No overlap found:** proceed with the submission as planned.
   - **Overlap found with an active BLG-ID:** either drop the topic and submit a different net-new idea instead, or — only if the idea provides materially new scope or rationale not captured by the existing item — keep it and note the relationship in the submission's Purpose/Rationale field (e.g. "refines BLG-XX-nn, adds <specific new angle>").
   A submission that restates an existing backlog item with no materially new angle is not a valid net-new submission and does not count toward the agent's minimum. This closes a gap where the check existed as prose (pre-v2.8: "Advisory only... briefly scan") but was not actually performed at submission-generation time across 20+ consecutive idea-intake windows, so overlap was only ever caught later (if at all) by STEP 4's PO classification — by `2026-07-27__scheduled`, backlog saturation had pushed the undetected-overlap rate to 52% of a single window's submissions (23 of 44), a materially higher rejection cost than performing the check up front.

### 2.1 Per-Agent Process

For each agent:
1. Switch to that agent's perspective (per the delegation model in the roadmap prompt §4)
2. Generate a minimum of 2 net-new idea submissions for that agent
3. Each submission must fully complete all required template fields (per §7)
4. Append a new row to `claude/ideas/ideas_register.md` using the Idea ID convention in §6 and the schema from `shared_standards.md §16.5`. Set Status to `Submitted`.
5. Update `ideas_window.json.submissions_received` with the Idea ID

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
- In `standard` mode: record in `ideas_window.json` as `submitted: 0` and note the gap. No register rows are added for non-submitting agents. Continue.

---

## STEP 3 — Close Submission Window

Update `claude/ideas/ideas_window.json`:

Compute `per_agent_submission_count` before writing: for each agent slug in `eligible_agents`, count the number of Idea IDs in `submissions_received` whose value contains that agent's slug. Write the resulting map alongside `agents_submitted`.

```json
{
  "status": "Closed",
  "closed_utc": "<ISO-8601 UTC>",
  "total_submissions": <n>,
  "agents_submitted": [<list of agent slugs that submitted>],
  "agents_not_submitted": [<list of agent slugs with 0 submissions>],
  "per_agent_submission_count": {"<agent-slug>": <int>, ...},
  "parked_ideas_carried": <n>,
  "new_submissions": <n>
}
```

---

## STEP 4 — Produce Window Summary

Write: `claude/ideas/window_summary_<window_id>.md`

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

| Idea ID | Agent | Title | Original Window | Parked Cycle |
|---------|-------|-------|----------------|--------------|
| ... | | | | |

## Notes

<Any gaps, non-compliant submissions flagged, or process notes>
```

---

## STEP 5 — Commit

```
git add claude/ideas/ideas_register.md
git add claude/ideas/ideas_window.json
git add claude/ideas/window_summary_<window_id>.md
git commit -m "[GOVERNANCE] Idea intake window closed: <window_id> — <n> submissions"
git push origin <current-branch>
```

If git operations unavailable: output exact files and commit message. Mark as "Ready to commit."

---

## 8. Completion Condition

The run is complete when:

- `ideas_window.json` status = `Closed`
- All agent submissions are appended as rows in `claude/ideas/ideas_register.md` (or gaps are recorded)
- `claude/ideas/window_summary_<window_id>.md` exists
- STEP 5 commit complete (or commit manifest produced)

---

## 9. Register Row Lifecycle — Post-Roadmap Run

The roadmap engine's STEP 4 is responsible for managing idea register rows after a roadmap run. The intake engine does not handle post-run status updates. For reference, the expected outcomes are:

| Idea outcome in roadmap STEP 4/5 | Register row action |
|----------------------------------|---------------------|
| ✅ Promoted to roadmap (Add decision in STEP 8) | Status updated to `Promoted-Added` — row remains as permanent record |
| ❌ Rejected — strong | Status updated to `Rejected`; core content copied to `claude/ideas/rejected_but_strong.md` |
| ❌ Rejected — not strong | Status updated to `Rejected` |
| 🅿 Parked | Status updated to `Parked-cycle-1` on first park; Park Count incremented; Park Rationale updated. Ideas at `Parked-cycle-3` or above require active Product Owner disposition — silent re-park is not permitted |
| Withdrawn by agent | Status updated to `Withdrawn` — row remains as record |

Register rows are never deleted. Status is managed in-place.

---

## 10. Governance Invariants

- **Window-controlled only.** No submissions are accepted outside an open window managed by this engine.
- **Template compliance is mandatory.** An incomplete submission is either discarded (strict) or flagged (standard) — it is never silently accepted.
- **No decisions made here.** The intake engine collects and structures. The roadmap engine decides.
- **Parked ideas persist.** A parked idea row is never deleted by the intake engine. It stays until the roadmap engine or the submitting agent withdraws it.
- **Parked cycle count is authoritative.** The `Parked-cycle-<n>` Status and the Park Count column in `ideas_register.md` are the single sources of truth for how many consecutive roadmap runs an idea has remained parked. The roadmap engine's stale idea expiry logic keys on these values.
- **Displacement is not required at submission time.** The "What Would You Stop?" field invites thinking — it is not a gate. Displacement is determined in STEP 5 of the roadmap engine where all candidates and constraints are visible simultaneously.
- **All agent roles submit.** Domain breadth matters — a narrow domain does not exempt an agent from the minimum. If no net-new ideas exist, the agent records that explicitly rather than submitting nothing.

---

## Change Log

See: [`claude/system/changelogs/idea_intake_changelog.md`](changelogs/idea_intake_changelog.md)