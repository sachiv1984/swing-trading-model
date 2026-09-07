**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-04 (created — v9.1 ST-17, BLG-QA-108)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Tier 1/Tier 2 DoQ Severity-Labelling Consistency Spot-Check

## Purpose

BLG-QA-108: "DoQ severity tiering (Tier 1/Tier 2) is applied per verification report without a periodic cross-report consistency check — risk of drift in how similar findings are labelled across cycles." Scope per the item: "Sample the last 5 `verification_report.md` files; confirm comparable findings received comparable tier labels; document any drift found."

## Canonical Definition (source of truth for what "compliant" labelling means)

`claude/system/delivery_verification_prompt.md` §-1.3 defines exactly two conditions:
- **Tier 1:** a merged EPIC's `qa_evidence_EPIC-xx.md` is missing entirely (or, by extension in later cycles' usage, a `Signed off by:`/`Date:` field is blank) → hard halt.
- **Tier 2:** the signer field is populated but does not match a recognised compliant authority format (literal `Director of Quality`, `Sprint Execution Engine (autonomous class)` with all 4 BLG-GOV-19 criteria met, or `Sprint Execution Engine (agent-mediated, <Role> role — §5.3)`) → flag, require Director of Quality counter-sign (non-halting in standard mode).

## Sample (as specified: last 5 cycles)

`2026-08-11__release-v8.6`, `2026-08-12__release-v8.7`, `2026-08-14__release-v8.8`, `2026-08-17__release-v8.9`, `2026-08-21__release-v9.0`.

## Findings — Last 5 Cycles (in-scope sample)

**No drift found.** All 5 verification reports phrase the Tier 1/Tier 2 check consistently and apply it to a comparable underlying situation (every merged EPIC in every one of these 5 cycles had a non-blank, correctly-formatted signer — no cycle in this window actually triggered either tier):

| Cycle | Phrasing used | Outcome |
|-------|---------------|---------|
| v8.6 | "no Tier 1 or Tier 2 flags" | Clean |
| v8.7 | "compliant, no Tier 2 counter-sign required" | Clean |
| v8.8 | "no Tier 2 flags" | Clean |
| v8.9 | "no Tier 2 counter-sign required" | Clean |
| v9.0 | "no Tier 2 counter-sign required" | Clean |

Minor wording variance exists (e.g. v8.6 explicitly says "no Tier 1 or Tier 2," the other 4 mention only Tier 2 since Tier 1's blank-field condition is implicitly covered by "all fields non-blank" stated earlier in the same paragraph in each case) — this is stylistic, not a substantive labelling inconsistency: in every one of the 5, the same underlying fact (signer present and correctly formatted) produced the same non-flagged outcome.

## Findings — Broader Historical Context (beyond the 5-cycle sample, for completeness)

A wider scan of every `verification_report.md` that mentions "Tier 1" surfaced a **real, but already-resolved, terminology drift** predating the sampled window:

- **`2026-05-19__release-v3.8`, `2026-05-21__release-v3.9`, `2026-06-21__release-v5.1`** (3 cycles, 2026-05-19 to 2026-06-21) used **"Tier 1 compliant ✓"** as a positive confirmation label for a directly-signed-by-Director-of-Quality (or fully-qualified autonomous-class) EPIC — i.e., "cleared the base tier," with no reference to "blank" at all. This is a looser reading than the canonical definition, which only ever defines Tier 1 as the missing-evidence hard-halt condition — never as a positive confirmatory label.
- **`2026-06-19__release-v6.0`** used a transitional merged phrasing, "Tier 1/2 compliant," for the same underlying situation.
- **From `2026-07-02__release-v6.4` onward** (and continuously through the sampled window and into `2026-08-21__release-v9.0` — at least 15 consecutive cycles checked), phrasing stabilised on the canonical-definition-aligned form: "Tier 1 (blank) not triggered" / "No Tier 1 (blank) or Tier 2 (wrong authority) conditions found." This is the form used throughout the 5-cycle sample above.

**Assessment:** this is a real historical instance of exactly the drift BLG-QA-108 was written to catch — three cycles used "Tier 1" as an informal positive-confirmation label rather than the canonical missing-evidence condition. It self-corrected roughly 5-6 cycles later (by `v6.4`) and has remained stable and canonical-definition-aligned for the ~15 most recent cycles, including the entire 5-cycle window this story specifically samples. Per BLG-QA-108's own acceptance criteria ("any labelling drift found is either corrected going forward or explicitly justified"): this instance is corrected going forward — no action is required, since the drift predates the sampled window by a wide margin and has not recurred since. Recorded here for the historical record rather than left undocumented, which was the entire premise of this backlog item.

## Assessment

No labelling drift found within the specified 5-cycle sample. One historical instance of drift found via a broader scan, already self-corrected well before the sampled window and stable since. No corrective action required; no backlog item filed (the underlying issue no longer exists in current practice).

## Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-09-04
- Comments: Spot-check complete against the exact 5-cycle sample specified by the acceptance criteria, plus a broader historical scan for context (not required by the AC but strengthens the finding). Genuine drift identified and documented, correctly scoped as historical/resolved rather than live. Satisfies BLG-QA-108's acceptance criteria.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-09-04 | Initial creation — v9.1 ST-17, BLG-QA-108. |
