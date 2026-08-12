**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.9
**Last Updated:** 2026-08-11 (ST-24, EPIC-06, v8.6, BLG-GOV-296 — "Known deviations filed" line reworded to "Known deviations" with a wording note, so a "None found" line reads consistently alongside every story's deviations_filed: true, per shared_standards.md §16.15)

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

*(Result column: use "Pass", "Pass with notes", or "Fail". "Pending DoQ" and "Awaiting QA" are pre-signing placeholders only — must be updated to "Pass"/"Fail" before sign-off block is completed.)*

*(Reconcile any partial per-item entries from STEP 3.1.C into this table. Do not duplicate — one row per ST item.)*

> **Requirement (OA-3/ST-03, elevated from advisory to hard requirement v1.7 — post-ship closure `2026-07-16__release-v7.3` STEP 8, Phase 4 lessons learnt):** Every AC in the backlog slice must appear in the evidence table — either as its own row, or explicitly named in a consolidated row's Evidence column (e.g. "Covers AC-01, AC-02, AC-03"). No AC may be silently absent from the table, even when it is functionally addressed elsewhere in the log (e.g. "What was built" narrative or "Regression areas checked"). This closes the gap found at `2026-07-16__release-v7.3` delivery verification, where an AC was addressed in prose but never listed in the evidence table itself.

**QA test coverage:**
- Scenarios run: <list scenario file names, or "manual acceptance review">
- Regression areas checked: <list affected spec domains>
- Known deviations: <list deviation refs, or "None found — all stories' deviation checks completed with nothing to file">

> **Wording note (ST-24, EPIC-06, v8.6, BLG-GOV-296):** the line above reads "Known deviations" (checks performed), not "Known deviations filed" — `execution_state.json`'s per-story `deviations_filed: true` means the deviation *check* completed, not that a deviation was necessarily found/filed (see `shared_standards.md` §16.15). Using "None found — all deviation checks completed" instead of a bare "Known deviations filed: None" avoids reading as contradictory next to every story row's `deviations_filed: true`.

---

## Standard Sign-Off Block

> **Authoring note:** When completing the sign-off block, update all AC table rows from "Pending"/"Awaiting QA" to "Pass" or "Pass with notes" in the same edit. Sign-off block and AC table must be consistent.
> **Date field requirement:** The `Date:` field must be non-blank before the PR can be opened and before the merge gate runs. Fill in the date when signing off, not at sprint close.
> **Signer format requirement (v6.3 Phase 4 LL, applied v6.4 post-ship closure):** The `Signed off by:` value must be exactly one of: `Director of Quality`, `Sprint Execution Engine (autonomous class)`, or `Sprint Execution Engine (agent-mediated, <Role Name> role — §X.Y)` (or one of the two delegated-QA aggregate formats below). No other format is compliant — Tier 2 sign-off format flags at Delivery Verification STEP -1.3 are triggered by deviation from these exact strings.
> **Agent-mediated provenance requirement (v7.5 Phase 4 LL, applied v7.5 post-ship closure):** When Director of Quality sign-off is performed by the engine acting in the Director of Quality role under explicit user direction (rather than by a human), the `Signed off by:` field **must** use `Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)` — not the literal `Director of Quality` string. This makes true signer provenance visible directly in the sign-off field itself rather than relying on cross-referencing `sprint_close.md` prose. The literal `Director of Quality` string is reserved for an actual human sign-off.

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object
- Signed off by: Director of Quality
- Date: <fill in — must be non-blank>
- Comments:

> **Delegated-QA sign-off pattern (BLG-GOV-69/74):** When individual stories within an EPIC used the `delegated_qa` delegation class (each story signed off by its domain owner, not the Director of Quality directly), two valid sign-off formats are accepted for the EPIC-level DoQ sign-off block:
>
> **Format (i) — Individual sign-off:**
> - Signed off by: Director of Quality
> - Date: YYYY-MM-DD
> - Comments: Story-level sign-offs provided by [owner names] for [N] stories; reviewed and acknowledged in aggregate.
>
> **Format (ii) — Aggregate acknowledgement:**
> - Signed off by: Director of Quality: Confirmed — [owner] ([N] stories), YYYY-MM-DD
> - Date: YYYY-MM-DD
>
> Both variants are valid. The `Date:` field must be non-blank in both formats before the PR can be opened and before the merge gate runs. The EPIC-level DoQ block is always required even when per-story sign-offs have been collected — it represents the Director of Quality's acknowledgement of the aggregate evidence.

---

## Mixed-Class EPIC Signer Format Note (ST-11 / LL-v5.2-P4-01)

When an EPIC contains **both** `delegated_backend` (or `delegated_frontend`) stories AND `autonomous` stories in the same EPIC:

- The sign-off block `Signed off by:` field **must** use the exact format:
  ```
  Sprint Execution Engine (agent-mediated, <Role Name> role — §5.3)
  ```
  where `<Role Name>` is the agent role that cleared the sign-off (e.g. `Head of Engineering`, `Cybersecurity & Trust Lead`, `Infrastructure & Operations Owner`).

- For multiple authority sign-offs in the same EPIC, list all on separate lines:
  ```
  Sprint Execution Engine (agent-mediated, Cybersecurity & Trust Lead role — §5.3)
  Sprint Execution Engine (agent-mediated, Head of Engineering role — §5.3)
  ```

- The BLG-GOV-19 autonomous class format (`Sprint Execution Engine (autonomous class)`) is only valid when **all** stories in the EPIC are `autonomous` with no `delegated_*` classification. A single `delegated_backend` story in the EPIC disqualifies the autonomous class — use the agent-mediated format above.

- **Rationale:** This prevents ambiguity at delivery verification about which authority cleared which story's AC, especially when one authority covers multiple stories.

---

## BLG-GOV-19 Autonomous Class Sign-Off Block

Use this block ONLY when all four qualifying criteria in `execution_prompt.md §3.2.A` are met.

```
**Autonomous class eligibility check (BLG-GOV-19):**
- [ ] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ / ✗
- [ ] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓ / ✗
- [ ] Criterion 3: No frontend-visible change — confirm no React page or UI component was created or modified (check `src/pages/` and `src/components/`) — ✓ / ✗
  - **Detection rule (BLG-GOV-135 — execution_prompt.md §3.2.A):** if any story in this EPIC creates or modifies a file under `src/components/**` or `src/pages/**`, this criterion is automatically unmet and the autonomous class path is unavailable, regardless of Playwright test coverage.
  - **Criterion 3 fail-path:** If any story in this EPIC has observable AC (frontend-visible change, UI rendering, user interaction) — autonomous class does not apply regardless of Playwright test coverage. Use the Standard Sign-Off Block above instead; record Playwright test file references in the DoQ Comments field.
- [ ] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓ / ✗

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: <today's date — must be non-blank>
- Comments: Autonomous class sign-off — all four qualifying criteria met (all stories autonomous, all AC code-review-verifiable, no frontend changes, engine signer populated).
```
