# Spec Query Process

**Owner:** Head of Specs Team
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-02-20

---

## Change Log

| Version | Change |
|---------|--------|
| 1.0 | Initial version. Created following 3.2 delivery — spec questions during implementation were handled ad hoc with no documented intake, response, or record-keeping standard. |

---

## Purpose

This document defines how spec questions are raised, answered, and recorded during implementation. It applies to any role that encounters an ambiguity, apparent gap, or conflict in a canonical specification while building against it.

It covers three situations:
- **Ambiguity** — the spec is present but unclear or open to interpretation
- **Gap** — the spec is silent on a scenario that has arisen in implementation
- **Conflict** — two canonical specs appear to contradict each other

It does not cover defects found during verification — those follow `docs/team_skills/quality/defect_lifecycle.md`.

---

## 1. Before Raising a Spec Query

Before raising a query, the engineer (or other role) must:

1. Read the relevant spec section in full — not just the passage that seems ambiguous
2. Check the decisions record for the current feature — the answer may already be there
3. Check the Specs Index to confirm they are reading the right canonical source
4. Check whether the behaviour in question is covered by an adjacent spec domain

If the question remains open after these steps, raise a query.

**Do not guess and build.** If a canonical spec is ambiguous on a point that materially affects implementation, building a guess into the code is harder to fix than asking the question first.

---

## 2. How to Raise a Query

Queries are raised by sending a structured message to the relevant spec owner, with the PMO Lead and Head of Specs Team copied.

**Spec owner identification:** Check the Specs Index (`docs/specs/Specs_Index.md`) for the domain owner. If the query spans two domains, address it to both owners and explicitly flag it as cross-domain.

**Query format:**

```
To:      {Spec owner(s)}
CC:      PMO Lead, Head of Specs Team
Subject: Spec query — {feature name} — {brief description}

Spec:        {document name and section}
Scenario:    {describe the situation in implementation that raised the question}
Ambiguity:   {what exactly is unclear, missing, or conflicting}
Impact:      {what implementation decision depends on the answer}
My reading:  {how I currently interpret it — not a request for validation, just context}
Blocking:    {yes/no — does implementation need to pause pending the answer?}
```

Short is better. The spec owner needs to understand the question, not read a narrative.

---

## 3. Response Turnaround

| Blocking | Expected response |
|----------|-------------------|
| Yes — implementation is paused | Same working day if raised before midday; following morning if raised after midday |
| No — can proceed with current interpretation | Within two working days |

If the spec owner cannot meet the turnaround, they notify the PMO Lead immediately so the PMO Lead can update the Phase Gate Document and communicate to the Head of Engineering.

---

## 4. When an Answer Requires a Spec Patch

The spec owner determines whether the answer requires a spec patch or a recorded clarification.

**A spec patch is required when:**
- The spec was genuinely ambiguous or silent and a new rule is needed
- The answer changes how a future engineer would read the spec
- The answer would affect acceptance criteria or test scenarios

**A recorded clarification is sufficient when:**
- The spec is clear but the reading was incorrect
- The answer is a direct consequence of existing spec language
- No new rule is established

**Spec patch process:**
1. Spec owner authors the patch and commits it with a version increment
2. Spec owner notifies PMO Lead that the patch is committed
3. PMO Lead notifies the QA & Testing Owner — acceptance criteria may need updating
4. PMO Lead notifies Head of Engineering — implementation proceeds against the updated spec

**Recorded clarification process:**
1. Spec owner replies with the answer
2. The PMO Lead records the query and answer in the Phase Gate Document under a Spec Queries section
3. No spec patch required — but if three or more clarifications are needed for the same spec section across a delivery, the spec owner must review that section for revision

---

## 5. Record Keeping

Every spec query and its answer is recorded by the PMO Lead in the Phase Gate Document for the feature, in a Spec Queries section:

```markdown
## Spec Queries

| # | Raised by | Spec | Question summary | Answer summary | Patch? | Date |
|---|-----------|------|------------------|----------------|--------|------|
| SQ-01 | Head of Engineering | `position_form.md §4.2` | Does amber state show when shares field is pre-filled? | Yes — amber triggers whenever calculated shares ≠ field value, regardless of source | No patch | 2026-02-20 |
```

This record is permanent — it is part of the Phase Gate Document which is a Class 7 Delivery Record.

---

## 6. Cross-Domain Queries

If a query spans two spec domains (e.g. a question where both the API contract and the strategy rules are relevant), the query is addressed to both owners simultaneously. The Head of Specs Team is included as a mediator, not just a CC.

The Head of Specs Team coordinates the response to ensure the two domain owners do not give contradictory answers. If they disagree, the Head of Specs Team has the deciding vote. The decision is recorded in the Phase Gate Document.

---

## 7. What This Process Does Not Cover

- Defects found during verification → `docs/team_skills/quality/defect_lifecycle.md`
- Decisions made during pre-alignment → `docs/product/decisions/{id}-{slug}.md`
- Requests to change canonical spec content outside of a delivery → raise with the relevant spec owner directly, the Head of Specs Team is not required as intermediary for routine spec updates
