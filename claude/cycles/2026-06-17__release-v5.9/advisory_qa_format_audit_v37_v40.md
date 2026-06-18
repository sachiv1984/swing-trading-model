Owner: Director of Quality
Class: Advisory Note (Class 3)
Status: Active
Last Updated: 2026-06-17
Cycle: 2026-06-17__release-v5.9
Story: ST-08 (BLG-QA-34)

---

# Advisory Note: QA Evidence File Format Audit — v3.7 to v4.0

## Scope

All QA evidence files from cycles v3.7, v3.8, v3.9, and v4.0 reviewed for
consistency with current QA evidence standard. This audit extends ST-07 (v3.7–v3.9)
to include v4.0.

Cycles reviewed:
- `2026-05-18__release-v3.7` (3 files: EPIC-01, EPIC-03, EPIC-04)
- `2026-05-19__release-v3.8` (3 files: EPIC-01, EPIC-03, EPIC-04)
- `2026-05-21__release-v3.9` (4 files: EPIC-01, EPIC-02, EPIC-03, EPIC-04)
- `2026-05-22__release-v4.0` (3 files: EPIC-01, EPIC-02, EPIC-03)

Total files reviewed: 13

ST-07 findings (v3.7–v3.9) are incorporated here. This note adds v4.0-specific findings.

---

## v4.0-Specific Findings

### Finding 4 — Non-standard Class label in v4.0 files

v4.0 EPIC-01, EPIC-02, EPIC-03 use:
```
**Class:** DoQ Sign-off Required (frontend-visible changes present — ...)
```
or:
```
**Class:** DoQ Sign-off Required
```

This is a descriptive status, not a document class. The canonical class for QA
evidence files is `Class 3 — Operational Record` per `claude/charter/document_lifecycle_guide.md`.

**Severity:** Advisory — sealed files not modified.

### Finding 5 — H1/H2 headings in v4.0 (format advancement)

v4.0 files introduce markdown headings at the file level:
```markdown
# QA Evidence Log — EPIC-01
## Cycle: 2026-05-22__release-v4.0
```

v3.7–v3.9 files use plain-text header blocks without headings. The heading
structure is a format improvement and is reflected in `qa_evidence_template.md`
from v4.0 onward.

**Severity:** Informational — not a defect.

### Finding 6 — Sign-off block format in v4.0

v4.0 sign-off blocks use a compressed inline format:
```
Signed: Director of Quality  Date: 2026-05-24
Role: Director of Quality
```

This omits the `- ` bullet prefix and `Comments:` field used in v3.7–v3.8.
The sign-off date is present (non-blank) in all three v4.0 files.

**Severity:** Advisory — date presence requirement is met; format is non-standard
relative to v3.7–v3.9 but was internally consistent across the v4.0 cycle.

---

## Consolidated Format Inconsistency Register

| Finding | Cycles affected | Type | Severity | Action |
|---------|----------------|------|----------|--------|
| F1 — Retroactive creation | v3.8 EPIC-03, EPIC-04 | Process | Advisory | Gate BLG-GOV-18 resolves (v3.9+) |
| F2 — Class label ("Class 4" / "DoQ Sign-off Required") | v3.7/v3.8 (Class 4); v4.0 (status label) | Format | Advisory | Template update advised |
| F3 — Sign-off block format drift | v3.7–v3.9 (3 variants) | Format | Advisory | Standardise template |
| F4 — v4.0 non-standard Class label | v4.0 (all 3 files) | Format | Advisory | Template update advised |
| F5 — H1/H2 headings introduced v4.0 | v4.0+ | Format | Info | No action — format improvement |
| F6 — v4.0 compressed sign-off block | v4.0 (all 3 files) | Format | Advisory | Standardise template |

---

## Recommended Template Improvements (non-blocking)

1. Standardise `Class:` field to `Class 3 — Operational Record` in `qa_evidence_template.md`
2. Add `- Date:` as a separate line in the autonomous class sign-off block (in addition to inline `— YYYY-MM-DD`)
3. Retain v4.0 heading structure (H1/H2) as the current standard

These are template-level improvements for future cycles. No sealed artefact from
v3.7–v4.0 requires modification.

---

## Disposition

Advisory — informational only. No action required on sealed artefacts.

---

## Director of Quality Sign-Off

- Signed off by: Director of Quality
- Date: 2026-06-17
- Comments: Format audit complete across 13 QA evidence files (v3.7–v4.0).
  All 13 files have sign-off dates present and non-blank. Six advisory findings
  documented; three template improvement recommendations recorded. No sealed
  artefacts modified. Findings shared with Head of Specs Team for template
  maintenance consideration.
