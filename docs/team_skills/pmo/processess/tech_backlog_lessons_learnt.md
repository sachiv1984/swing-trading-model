# Tech Backlog Lessons Learnt

**Owner:** PMO Lead
**Type:** PMO Process Template
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-02-21

---

## Purpose

Run this review when a P0 or P1 tech backlog item is closed. Its job is to identify how the issue arose, why it wasn't caught sooner, and what process change prevents recurrence.

Tech backlog items — particularly correctness and governance issues — often carry the most systemic lessons precisely because they represent failures that reached the system. They deserve a review of their own.

This template is a lightweight variant of `lessons_learnt.md`. It applies when an item ships without a formal pre-alignment phase and scope document — typically tech debt, correctness fixes, and governance items.

---

## When to Run

- Triggered by the PMO Lead when a P0 or P1 tech backlog item is closed
- P2 items: run at the PMO Lead's discretion, particularly if the item revealed a systemic pattern
- Must be complete before the next release ships
- Filed alongside the standard `lessons_learnt.md` if a tech item shipped alongside a feature

---

## Review Structure

Work through each section. For each section: did this item represent a failure that could recur, and if so, what specifically needs to change?

---

### Section 1 — Origin

- When was this issue introduced?
- Was it an implementation error, a spec gap, a miscommunication, or a known shortcut?
- Was it present from the initial implementation of the affected feature?
- **Action trigger:** If the issue was introduced at implementation → check whether the readiness audit or spec review process should have caught it. Update `pre_alignment_readiness.md` if a check is missing.

---

### Section 2 — Detection

- How was the issue identified? (Spec review, user report, validation failure, manual audit)
- If it was a known deviation documented in a spec: when was it documented, and what was its assigned priority and target release at that time?
- Was there a system in place that should have caught this but didn't? (e.g. validation, CI, QA review)
- If a system failed to catch it: what was the root cause of that failure?
- **Action trigger:** If a detection system failed → identify whether the failure was a coverage gap, a calibration problem, or a process gap, and update the relevant document.

---

### Section 3 — Resolution

- Was the correct fix unambiguous once the item was prioritised? (Yes → good canonical spec. No → spec gap)
- Was the canonical spec the source of truth for the fix, or was there ambiguity about what "correct" looks like?
- Were the acceptance criteria clear enough to verify the fix?
- Did the fix require Canonical Owner sign-off, and was that sign-off the right gate?
- **Action trigger:** If the fix was ambiguous → identify the spec that should have provided clarity and ensure it is updated.

---

### Section 4 — Why It Wasn't Fixed Sooner

- Was the issue known before it became a priority? (Check: spec "known limitations", backlog, documentation)
- If known: did it have a priority tier, a target release, and a named owner at the time it was documented?
- If not: why not? Was the triage process missing, skipped, or unclear?
- Was there pressure to defer that was inappropriate given the severity?
- **Action trigger:** If the item was known but untriaged → apply the known deviation triage rule (lifecycle guide §X). If the triage rule didn't exist or wasn't followed → escalate to Head of Specs Team.

---

### Section 5 — Process Improvements

For each failure mode identified above:

- What specific process change prevents this recurrence?
- Which template, rule, or document needs updating?
- Who owns the update?
- What is the target date?

Improvements must be actioned before the next item of the same type enters the system.

---

## Output

### Lessons Learnt Record

Filed at `docs/product/lessons_learnt/{blg-id}-lessons.md`:

```markdown
# Lessons Learnt — {BLG-ID}: {Item Name}

**Item:** {BLG-ID} — {Item Name}
**Type:** Tech Backlog ({Priority})
**Closed:** {date}
**Reviewed by:** PMO Lead
**Date filed:** {date}

> Note on template applicability: {state whether standard or adapted template used and why}

## What worked well
{2–3 bullet points}

## What created friction
{Each issue: what happened, root cause, impact}

## Process improvements actioned
{Each improvement: what changed, which document updated, version bumped}

## New skills or templates created
{List any new files created}

## Outstanding actions
{Owner | Action | Target date}
```

---

## Escalation

If the lessons learnt review reveals a systemic issue that cannot be resolved by updating a PMO or validation template — for example, a spec governance gap, a validation architecture problem, or a recurring failure mode across multiple items — escalate to:

- **Head of Specs Team** — for spec governance, canonical source of truth, or deviation triage issues
- **Head of Engineering** — for validation architecture or implementation process failures
- **Product Owner** — for prioritisation failures (known P0 items deferred without explicit decision)

The PMO Lead does not absorb systemic issues into local template fixes. They are surfaced explicitly.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-02-21 | Initial version. Created as a result of lessons learnt for BLG-TECH-01 — no process existed for tech backlog items that ship without a pre-alignment phase. |