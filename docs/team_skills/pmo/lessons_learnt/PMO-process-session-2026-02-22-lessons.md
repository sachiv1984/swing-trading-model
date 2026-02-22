# Lessons Learnt — PMO Process Session (QWB Readiness Audit)

**Feature:** Quick Wins Bundle — QWB pre-alignment readiness audit
**Session date:** 2026-02-22
**Reviewed by:** PMO Lead
**Date filed:** 2026-02-22

---

## What worked well

- Readiness audit correctly identified all six bundle items and surfaced
  blocking formula confirmations before the meeting was scheduled.
- Preliminary decisions list (D1–D6) was produced as a complete meeting
  agenda, preventing scope discovery at the meeting.
- Settings table dependency check (§1a) fired correctly — confirmed no
  settings dependency across all six items without manual prompting.

---

## What created friction

### 1. GI-2 violated — "ASAP" used as deadline in Phase Gate Document
**Phase:** Phase 0 — Readiness Audit (action register creation)
**What happened:** The Phase Gate Document was produced with "ASAP" as
the deadline for all pre-meeting actions (A-PRE-01 through A-PRE-06).
GI-2 states "ASAP is not a deadline." The violation was caught and
flagged by the Product Owner before the document was committed.
**Root cause:** The PMO prompt and phase gate template do not enforce
deadline format at creation time. There is no explicit instruction
requiring either a real UTC date or a [MISSING] placeholder with a
separate deadline-setting action. "ASAP" was written as a shorthand
and went undetected until review.
**Impact:** Non-compliant Phase Gate Document produced. Would have
required a corrective patch before Gate R could pass. Caught before
commitment — zero downstream impact on this occasion.

### 2. Repo Change Packs not produced for non-PMO owner actions
**Phase:** Phase 0 — Readiness Audit
**What happened:** Actions A-PRE-01 through A-PRE-06 were stated as
action notices only — no Repo Change Pack (FULL FILE or PATCH UPDATE
with [MISSING] placeholders) was produced for any owner action.
The PMO process rules require that every non-PMO owner action produce
both an Action Notice and a Repo Change Pack that is directly applyable
to the repo without rewriting.
**Root cause:** The PMO prompt contained the Repo Change Pack rule but
the Phase 0 output did not apply it. No enforcement mechanism existed
at the point of action creation.
**Impact:** Owners would have received verbal instructions only, with no
draft artifact to apply. Creates ambiguity and interpretation risk.
Caught at review — corrective artifacts being produced in this session.

### 3. Frontend Spec owner briefing not treated as a mandatory failing gate
**Phase:** Phase 0 — Readiness Audit (Gate R.3)
**What happened:** Gate R.3 (Frontend Spec Readiness) was listed as a
failing gate, but the underlying rule — that the Frontend Spec owner
must be briefed before the meeting is scheduled — was not recorded as
a non-negotiable mandatory gate item. It appeared as a soft advisory
rather than a hard blocker equivalent to the formula confirmation gates.
**Root cause:** `pre_alignment_readiness.md` Section 3 asks whether the
Frontend Spec owner "has enough context to participate" but does not
state that a briefing must have occurred as a prerequisite. The gate
item was therefore written weakly.
**Impact:** Risk that a future readiness audit passes Gate R.3 on the
basis that "the Frontend Spec owner will be briefed at the meeting."
That would allow scope discovery during the meeting rather than before.

---

## Process improvements actioned

### 1. GI-2 enforcement added to PMO prompt and pre_alignment_readiness.md
**Documents updated:**
  - `docs/team_skills/prompt/PMOfeature.md` (PMO prompt)
  - `docs/team_skills/pmo/processess/pre_alignment_readiness.md`
**Version bumps:**
  - PMO prompt: new GI-2 enforcement section added
  - `pre_alignment_readiness.md`: 1.1 → 1.2
**Change:** Explicit rule added: deadlines must be a real UTC date
(PROPOSED if estimated) or [MISSING] with a separate deadline-setting
action assigned to the Product Owner. "ASAP", "TBC", and "by meeting"
are prohibited. Rule applies at action creation, not at review.

### 2. Repo Change Pack rule strengthened in PMO prompt
**Document updated:** `docs/team_skills/prompt/PMOfeature.md`
**Change:** Clarified that every non-PMO owner action requires both an
Action Notice and a Repo Change Pack. If the owner action requires
judgment, the Repo Change Pack must be a DRAFT with [MISSING]
placeholders. The draft must be directly applyable without rewriting.
Owner mode must draft evidence directly into the Phase Gate Document
as a PATCH UPDATE.

### 3. Frontend Spec owner briefing made mandatory in pre_alignment_readiness.md
**Document updated:** `docs/team_skills/pmo/processess/pre_alignment_readiness.md`
**Version bump:** 1.1 → 1.2 (combined with change 1 above)
**Change:** Section 3 updated. New mandatory gate item: "Has the
Frontend Spec owner been briefed on the feature before this audit
completes?" This is now a hard failing gate — not advisory. The meeting
may not be scheduled until written briefing confirmation is recorded.
Rationale added: discovering UX scope at the meeting is equivalent to
discovering a data model gap at the meeting — it changes the effort
estimate and creates pressure that compresses pre-alignment quality.

---

## New skills or templates created

None. All improvements applied to existing documents.

---

## Outstanding actions

| Action | Owner | Target date |
|--------|-------|-------------|
| Apply updated PMO prompt to `docs/team_skills/prompt/PMOfeature.md` | PMO Lead | 2026-02-22T23:59:00Z |
| Apply `pre_alignment_readiness.md` v1.2 patch | PMO Lead | 2026-02-22T23:59:00Z |
| Produce Repo Change Packs for all outstanding A-PRE actions (QWB bundle) | PMO Lead | 2026-02-22T23:59:00Z |
| Replace [MISSING] deadlines in QWB Phase Gate Document | Product Owner | PROPOSED: 2026-02-23T17:00:00Z |
