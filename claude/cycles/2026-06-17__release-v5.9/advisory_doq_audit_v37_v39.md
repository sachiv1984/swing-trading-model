Owner: Director of Quality
Class: Advisory Note (Class 3)
Status: Active
Last Updated: 2026-06-17
Cycle: 2026-06-17__release-v5.9
Story: ST-07 (BLG-GOV-38)

---

# Advisory Note: DoQ Sign-Off Date Compliance Audit — v3.7 to v3.9

## Scope

All QA evidence files from cycles v3.7, v3.8, and v3.9 reviewed for:
1. Header fields present (Owner, Class, Status, Last Updated)
2. DoQ sign-off date field present and non-blank
3. Sign-off block format consistent with current standard

Cycles reviewed:
- `2026-05-18__release-v3.7` (3 files: EPIC-01, EPIC-03, EPIC-04)
- `2026-05-19__release-v3.8` (3 files: EPIC-01, EPIC-03, EPIC-04)
- `2026-05-21__release-v3.9` (4 files: EPIC-01, EPIC-02, EPIC-03, EPIC-04)

Total files reviewed: 10

---

## Findings

### Finding 1 — Retroactive creation (v3.8 EPIC-03, EPIC-04)

`claude/cycles/2026-05-19__release-v3.8/qa_evidence_EPIC-03.md` and
`claude/cycles/2026-05-19__release-v3.8/qa_evidence_EPIC-04.md` were created
retroactively after their respective PRs (#453, #452) had already merged
(2026-05-20T19:27:04Z and 2026-05-20T19:26:29Z). Both files note this explicitly.

**Severity:** Advisory — sign-off dates are present and non-blank (2026-05-20).
No retroactive modification required. The retroactive pattern was a recurrence
of the same issue from v3.7 EPIC-01 (sign-off "applied retrospectively").
Gate `BLG-GOV-18` (pre-PR sign-off date check) was implemented in v3.9 ST-12
(EPIC-04) to prevent future occurrences.

### Finding 2 — Header class inconsistency across v3.7–v3.9

v3.7 and v3.8 files use `Class: Planning Document (Class 4)`.
v3.9 EPIC-03 and EPIC-04 use `**Class:** QA Evidence Log (Class 3)` (bold markdown, different class name).
v4.0 files switch to `**Class:** DoQ Sign-off Required` (non-standard class label).

The canonical class for QA evidence files is `Class 3 — Operational Record`
(document_lifecycle_guide.md). The "Planning Document (Class 4)" label in v3.7/v3.8
is incorrect and the "DoQ Sign-off Required" label in v4.0 is non-standard.

**Severity:** Advisory — sealed artefacts are not modified retroactively.
Current template (`claude/system/templates/qa_evidence_template.md`) should be
verified to use the correct class label. No action required on sealed files.

### Finding 3 — Sign-off block format drift

v3.7/v3.8 sign-off block format:
```
- Signed off by: Director of Quality (sachiv.patel@hotmail.co.uk)
- Date: 2026-05-18
- Comments: ...
```

v3.9 EPIC-03/04 sign-off block format (autonomous class):
```
**DoQ Sign-off:** Director of Quality — 2026-05-22
**Sign-off basis:** BLG-GOV-19 autonomous class — ...
```

v3.9 EPIC-02 sign-off block format:
```
- Signed off by: Director of Quality
- Date: 2026-05-22
- Sign-off method: agent_mediated
```

Three distinct formats across a 3-cycle window. The autonomous class format lacks
a dedicated `Date:` field on a separate line, which makes machine-readable auditing
harder.

**Severity:** Advisory — all dates are present; no gate failures. The template
should standardise the autonomous class block to include `- Date:` on a separate
line alongside the inline `— YYYY-MM-DD` notation.

---

## Summary

| File | Header present | Date non-blank | Format conformant | Notes |
|------|---------------|----------------|-------------------|-------|
| v3.7 EPIC-01 | ✓ | ✓ (2026-05-18) | Minor drift | Retrospective sign-off noted |
| v3.7 EPIC-03 | ✓ | ✓ (2026-05-18) | Autonomous | — |
| v3.7 EPIC-04 | ✓ | ✓ (2026-05-18) | Standard | — |
| v3.8 EPIC-01 | ✓ | ✓ (2026-05-20) | Standard | — |
| v3.8 EPIC-03 | ✓ | ✓ (2026-05-20) | Standard | Retroactive creation |
| v3.8 EPIC-04 | ✓ | ✓ (2026-05-20) | Standard | Retroactive creation |
| v3.9 EPIC-01 | ✓ | ✓ (2026-05-22) | Standard | — |
| v3.9 EPIC-02 | ✓ | ✓ (2026-05-22) | Agent-mediated | — |
| v3.9 EPIC-03 | ✓ | ✓ (2026-05-22) | Autonomous (inline) | — |
| v3.9 EPIC-04 | ✓ | ✓ (2026-05-22) | Autonomous (inline) | — |

**Overall:** All 10 files have sign-off dates present and non-blank. No gate
failures identified. Three advisory findings filed above; no retroactive
modifications required on sealed artefacts.

---

## Disposition

Advisory — informational only. No action required on sealed artefacts.

---

## Director of Quality Sign-Off

- Signed off by: Director of Quality
- Date: 2026-06-17
- Comments: Advisory review complete. Findings 1–3 documented. Gate BLG-GOV-18
  (introduced v3.9) addresses the retroactive creation pattern. Class label
  inconsistency is a template-level improvement; the qa_evidence_template.md
  should be verified separately. No sealed artefacts modified.
