**Owner:** Head of Specs Team
**Status:** Active

# QA Evidence Template

Used by the Sprint Execution Engine at STEP 3.2.A and STEP 3.1.C. Read this file when creating or completing `qa_evidence_EPIC-xx.md`.

---

## File Header Block

```
Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: <date>
```

---

## Consolidation Block

**EPIC:** EPIC-xx — <title>
**Cycle:** <cycle_id>
**Sprint goal:** <text>
**Test scenarios used:** <list paths from `test_scenarios` field, or "Derived from spec + AC">

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-xx | <spec file#section> | <one line> | <criteria text> | Pass / Fail | None / DEV-ref |

*(Reconcile any partial per-item entries from STEP 3.1.C into this table. Do not duplicate — one row per ST item.)*

**QA test coverage:**
- Scenarios run: <list scenario file names, or "manual acceptance review">
- Regression areas checked: <list affected spec domains>
- Known deviations filed: <list deviation refs or "None">

---

## Standard Sign-Off Block

> **Authoring note:** When completing the sign-off block, update all AC table rows from "Pending"/"Awaiting QA" to "Pass" or "Pass with notes" in the same edit. Sign-off block and AC table must be consistent.
> **Date field requirement:** The `Date:` field must be non-blank before the PR can be opened and before the merge gate runs. Fill in the date when signing off, not at sprint close.

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object
- Signed off by: Director of Quality
- Date: <fill in — must be non-blank>
- Comments:

---

## BLG-GOV-19 Autonomous Class Sign-Off Block

Use this block ONLY when all four qualifying criteria in `execution_prompt.md §3.2.A` are met.

```
**Autonomous class eligibility check (BLG-GOV-19):**
- [ ] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ / ✗
- [ ] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓ / ✗
- [ ] Criterion 3: No frontend-visible change — confirm no React page or UI component was created or modified (check src/pages/ and src/components/) — ✓ / ✗
- [ ] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓ / ✗

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: <today's date — must be non-blank>
- Comments: Autonomous class sign-off — all four qualifying criteria met (all stories autonomous, all AC code-review-verifiable, no frontend changes, engine signer populated).
```
