**Owner:** Product Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-15 (ST-15, EPIC-04, v9.4, BLG-SPEC-138: initial version)

---

# Placement Decision — Governance Metrics in `metrics_definitions.md`

**Added:** ST-15 (EPIC-04, v9.4, BLG-SPEC-138)

## 1. Question Being Decided

`BLG-SPEC-138`'s actual, still-open AC (its own 2026-09-08 note is explicit that the literal "Appendix D" heading-collision symptom was already fixed by `ST-48`, relabelling the section to "Appendix F" — that fix did not touch this question): **does governance-process metrics content (Product Value Ratio rolling-window handling, Skill-Silo skill-category taxonomy) belong in `docs/specs/metrics_definitions.md` — a Class 1, API-facing canonical spec governing `GET /analytics/metrics` — or should it move to `docs/governance/`?**

## 2. What's There Now

`metrics_definitions.md` §Appendix F ("Governance Metrics — Cross-Reference Only") already carries an explicit scope note (added `ST-40`/`ST-35`, v9.2): these metrics are **not** returned by `GET /analytics/metrics`, are exempt from the document's own Completeness Guarantee, and are documented here "because [the Metrics Definitions & Analytics Canonical Owner] is this system's single accountable owner of metric-definition rigor generally, governance metrics included — not because they belong to the API surface this document otherwise governs." The appendix is explicitly a **definitional cross-reference**, not a second source of truth — "the authoritative computation for each metric below lives in its cited governance prompt" (`roadmap_prompt.md` STEP 2.4 for PVR, §7.1/§7.2 for the skill taxonomy).

## 3. Decision

**Option A — keep the content in `metrics_definitions.md`, affirming the existing v9.2 rationale.** Selected.

**Reasoning:**

1. **The confusion risk the backlog item names is already addressed, not just asserted.** `BLG-SPEC-138`'s problem statement worries a reader of an API-facing spec could be confused by governance content appearing alongside it. The existing Appendix F scope note directly answers that: it states up front that these metrics are not part of the API surface, are exempt from the Completeness Guarantee, and names the actual authoritative computation location. A reader who gets that far has already been told exactly what this is and isn't — the risk is disclosed, not silent.
2. **"Single accountable owner of metric-definition rigor" is a real, not merely rhetorical, benefit.** Splitting metric *definitions* (as opposed to metric *computation*, which already correctly lives in the governance prompts) across two documents by subject-matter (product vs. governance) rather than by role would mean the Metrics Definitions & Analytics Canonical Owner's own definitional standards — naming conventions, boundary-case handling, sign-off format — would need to be maintained identically in two places, or would drift. Keeping all metric *definitions* under one owner's document, with computation correctly delegated out to governance prompts already, is the more consistent structure.
3. **Moving cost is real, benefit is not.** Relocating would require updating every existing cross-reference into `metrics_definitions.md#Appendix F` from `roadmap_prompt.md` and elsewhere, for a document-organisation preference with no corresponding gain now that the actual confusion risk (item 1) is already handled at the point of contact.
4. **This is not a new decision manufactured to avoid work — it is the same conclusion the Metrics Definitions & Analytics Canonical Owner already reached in v9.2** when writing the scope note in the first place (agent-mediated sign-off, 2026-09-08, on both subsections). Re-examining it here with the specific "should this move" question the backlog item asks, rather than assuming the v9.2 author's rationale, the same conclusion holds up: nothing in `BLG-SPEC-138`'s framing identifies a problem the existing scope note fails to solve.

**Option B (rejected) — relocate to `docs/governance/`.** Would fragment definitional-rigor ownership across two documents for a cosmetic-organisation gain, while requiring an unbounded cross-reference update with no clear consumer benefit. Rejected.

## 4. Action Taken

No relocation. Per the AC's own framing ("relocate ... if the decision is to move it"), that action is not triggered by this decision. `metrics_definitions.md` Appendix F's existing content and scope note stand as-is, now backed by an explicit placement decision it did not previously have on record.

## 5. Sign-Off

- Signed off by: Product Owner
- Signed off by: Metrics Definitions & Analytics Canonical Owner
- Date: 2026-09-15
- Comments: Acting on explicit user direction to resolve `ST-15`'s escalation (`ESC-EXEC-20260915-01`) in these two roles' capacity, per `execution_prompt.md` §5. Decision reviewed against `BLG-SPEC-138`'s actual (post-`ST-48`-correction) AC, not its now-superseded heading-collision framing.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-09-15 | ST-15 (EPIC-04, v9.4, BLG-SPEC-138): Initial version. Placement decision — governance metrics content stays in `metrics_definitions.md` Appendix F, affirming the existing v9.2 scope-note rationale. No relocation. |
