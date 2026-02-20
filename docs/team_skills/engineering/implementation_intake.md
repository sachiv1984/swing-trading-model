# Engineering Implementation Intake

**Owner:** Head of Engineering
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-02-20

---

## Change Log

| Version | Change |
|---------|--------|
| 1.0 | Initial version. Created following 3.2 delivery gap assessment — engineering intake when implementation was declared open was undocumented. No standard existed for confirming inputs, identifying spec versions, or understanding the escalation path for spec questions. |

---

## Purpose

This checklist is run by the Head of Engineering when implementation is declared open by the PMO Lead. It takes approximately fifteen minutes and ensures that:

- Engineering has read the right documents before writing a line of code
- Spec versions are confirmed and locked
- The escalation path for spec questions is understood
- Any immediate feasibility concerns are surfaced before implementation starts — not discovered mid-build

This intake is not a gate that can be waived. If any item cannot be checked, the Head of Engineering notifies the PMO Lead before proceeding.

---

## Inputs

The following must be available before running this intake:

- [ ] PMO Lead has communicated implementation open with scope document location
- [ ] All canonical specs listed in the scope document are committed and at the versions stated

---

## Intake Checklist

### 1. Scope Document

- [ ] I have read the full scope document at `docs/product/scope/scope--{id}-{slug}.md`
- [ ] I understand what is in scope and what is explicitly out of scope
- [ ] The effort estimate in the scope document is consistent with what I know now — if not, I have raised this with the PMO Lead before starting
- [ ] I have noted the target release version

### 2. Canonical Specifications

For each spec listed in the scope document Section 2:

- [ ] I have read the relevant sections (not just the summary in the scope document)
- [ ] I have confirmed the spec version I am working against matches the version listed in the scope document
- [ ] I understand which spec owns which decisions — I know where to look if questions arise

Spec versions locked for this feature (fill in at intake):

| Spec | Version | Key sections |
|------|---------|--------------|
| {spec} | {version} | {sections} |

### 3. Test Scenarios

- [ ] I have located the test scenario document at `docs/testing/{id}-{slug}-test-scenarios.md`
- [ ] I have read the scenarios — I understand what the QA Lead will be executing and what the acceptance criteria require
- [ ] If any scenario describes behaviour I cannot implement as written, I have flagged it to the PMO Lead now — not after I have built it differently

### 4. Spec Query Path

I understand the following before starting:

- [ ] **Spec questions go to the spec owner, not the PMO Lead.** The PMO Lead coordinates but does not answer spec content questions.
- [ ] **The spec query process is at `docs/team_skills/specs/spec_query_process.md`.** I will use this format when raising a question.
- [ ] **If implementation must pause pending a spec answer, I notify the PMO Lead immediately** so the Phase Gate Document and stakeholder communications are updated.
- [ ] **I do not build a guess into the code** if a spec is ambiguous on a point that materially affects the implementation. I raise the question first.

### 5. Feasibility

- [ ] I have reviewed the scope against the current codebase and am not aware of any architectural blocker
- [ ] If there is a concern I cannot resolve without starting: I have raised it to the PMO Lead with a clear description of the risk and what decision is needed. I have not silently started anyway.

### 6. Engineering Team Readiness

- [ ] The engineer(s) assigned to this feature have been identified
- [ ] They have access to the scope document and canonical specs
- [ ] They understand the spec query path and know not to build around ambiguities without asking

---

## After Intake

Once all items are checked:

- The Head of Engineering confirms readiness to the PMO Lead
- The PMO Lead updates the Phase Gate Document with implementation start date and assigned engineer(s)
- Implementation begins

If items cannot be checked:

- Head of Engineering documents which items are blocked and why
- PMO Lead is notified before implementation begins
- No code is written for in-scope items until all blockers are resolved
