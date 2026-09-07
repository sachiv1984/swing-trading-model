**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-04 (created — v9.1 ST-16, BLG-QA-142)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Definition-of-Done Compliance Spot-Check — Last 5 Release Cycles

## Purpose

BLG-QA-142: "No periodic spot-check confirms DoQ sign-off blocks across recent cycles genuinely meet the Definition-of-Done bar (as opposed to the automated staleness lint at `BLG-QA-98`, which only checks for stale 'Pending' rows, not substantive compliance)." This distinguishes from `BLG-QA-98` explicitly — this is a substantive read of sign-off content, not a lint for blank fields.

## Definition-of-Done Checklist Used

No single "Definition of Done" document exists as a standalone canonical artefact. The operational DoD for a DoQ sign-off is defined jointly by `claude/system/templates/qa_evidence_template.md`'s Standard Sign-Off Block and `execution_prompt.md` STEP 4's merge gate table. This spot-check applies both:

**From the Standard Sign-Off Block (per-EPIC):**
1. All acceptance criteria verified against canonical spec (checkbox)
2. No unresolved P0 or P1 deviations (checkbox)
3. Regression areas checked (checkbox)
4. Frontend direct-URL-construction check, where applicable (checkbox)
5. `Signed off by:` field non-blank, matching a recognised compliant format
6. `Date:` field non-blank
7. `Comments:` substantive — not blank, especially for "Pass with notes" rows

**From the merge gate table (STEP 4) / completion condition (§12):**
8. `spec_references` populated for all `done` ST items
9. Every AC in the backlog slice appears in the evidence table (own row or named in a consolidated row)
10. `qa_signed_off = true` set in `execution_state.json` in the same commit as the sign-off block

## Sample

All 30 `qa_evidence_EPIC-xx.md` files across the 5 most recent completed release cycles: `2026-08-11__release-v8.6` (6 EPICs), `2026-08-12__release-v8.7` (7), `2026-08-14__release-v8.8` (7), `2026-08-17__release-v8.9` (6), `2026-08-21__release-v9.0` (5).

## Method

Extracted `Signed off by:`/signer-equivalent, `Date:`, and checkbox count from every file; spot-checked a sample against items 8–10 by cross-referencing `execution_state.json` and reading the AC/evidence table directly.

## Findings

**Finding 1 — Items 5–7 (signer, date, comments): fully compliant across all 30 files.** Every file across all 5 cycles has a non-blank signer (recognised format: literal `Director of Quality`, `Sprint Execution Engine (autonomous class)`, or `Sprint Execution Engine (agent-mediated, <Role> role — §5.3)`) and a non-blank date. No stale-Pending rows found (consistent with `BLG-QA-98`'s own lint, which already screens for this — no drift found here).

**Finding 2 — Items 1–4 (checkbox list): systemic structural drift at `2026-08-21__release-v9.0` (moderate, self-corrected).** All 5 of v9.0's `qa_evidence_EPIC-xx.md` files use a differently-structured sign-off block — a code-fenced narrative paragraph ending in `Signed: <role>` / `Date: <date>`, with **no checkbox list at all** (0 of the 4 required checkboxes present, vs. exactly 4/4 in every file from the other 4 cycles sampled). Read in full, the narrative substance covers the same ground in all 5 cases (e.g. EPIC-01: "No unresolved P0/P1 deviations... EPIC-01 ready for PR"; EPIC-02/04/05: explicit "No P0/P1 deviations" or "No P0 deviations" statements) — this is a **template/structural** non-conformance, not a substantive gap. `claude/cycles/2026-08-21__release-v9.0/verification_report.md` correctly extracted the signer value and treated it as Tier 1/Tier 2 compliant despite the format difference (see the companion spot-check, `tier_labelling_consistency_spotcheck_2026-09-04.md`, which confirms this is not a severity-labelling drift — signer authority format itself was unaffected).
- **Already corrected going forward:** the current cycle's own `qa_evidence_EPIC-01.md`/`qa_evidence_EPIC-02.md` (`2026-09-03__release-v9.1`) both use the canonical checkbox + `- Signed off by:` + `- Date:` format again — confirmed by direct inspection. No corrective backlog item is filed for this reason: per BLG-QA-142's own acceptance criteria ("any labelling drift found is either corrected going forward or explicitly justified"), the "corrected going forward" condition is already met without intervention. Recorded here so the one-cycle deviation is documented and traceable, per this story's purpose.

**Finding 3 — Item 8 (spec_references) — spot-checked, no gap found.** Sampled `execution_state.json` entries for `2026-08-17__release-v8.9` (EPIC-01, EPIC-03) and `2026-08-21__release-v9.0` (EPIC-01, EPIC-02) — all `done` stories carry non-empty `spec_references` or the structured `spec_reference_not_applicable: true` exemption with a populated reason (e.g. v9.0 ST-01/ST-18, confirmed via that cycle's own `verification_report.md` line 173). No bare `[]` found for a story lacking the exemption.

**Finding 4 — Item 9 (AC-table completeness) — spot-checked on 3 files, no gap found.** `qa_evidence_EPIC-01.md` (v9.0), `qa_evidence_EPIC-02.md` (v8.9), `qa_evidence_EPIC-03.md` (v8.6) each have one evidence-table row per ST item with no AC silently omitted from the table (confirmed by cross-reading each row's "What was built"/"Acceptance criteria" cells against that EPIC's own `sprint_backlog.md` section — a fuller audit of the remaining 27 files was not performed given this story's `S` effort scope; not extrapolated as a general clean bill).

**Finding 5 — Item 10 (`qa_signed_off` flag) — spot-checked, minor documentation-staleness note (already flagged by v9.0's own verification, not new).** `2026-08-21__release-v9.0/verification_report.md` itself already recorded a non-blocking staleness note: `qa_evidence_EPIC-01.md`'s AC table still shows ST-02's `Result` as "Returned to backlog," predating that story's final resolution after the EPIC's PR merged; `execution_state.json` is confirmed authoritative and correct. Not re-litigated here — cited for completeness since it falls within this spot-check's scope, but it is not a new finding.

## Assessment

DoQ sign-off blocks across the last 5 cycles substantively meet the Definition-of-Done bar. The one structural drift found (Finding 2) never produced an actual quality gap — all required content was present in prose form — and has already self-corrected in the very next cycle. No corrective backlog item filed; no further action recommended beyond this documentation.

## Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-09-04
- Comments: Spot-check complete. Checklist derived explicitly from `qa_evidence_template.md` + `execution_prompt.md` STEP 4/§12 (no separate DoD document exists) rather than assumed. One genuine, previously-undocumented finding (v9.0's system-wide sign-off-block structural drift) surfaced, assessed as non-blocking (substance present, already self-corrected), and documented per the story's own "corrected going forward or explicitly justified" standard. Satisfies BLG-QA-142's acceptance criteria.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-09-04 | Initial creation — v9.1 ST-16, BLG-QA-142. |
