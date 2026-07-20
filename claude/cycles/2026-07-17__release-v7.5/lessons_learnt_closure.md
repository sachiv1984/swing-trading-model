Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-07-20
Cycle: 2026-07-17__release-v7.5

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: v7.5 UI Feature Expansion Continuation (Command Palette, Alerts, Bulk Actions, Saved Filters)
Run: 2026-07-17__release-v7.5
Reviewed by: PMO Lead
Date filed: 2026-07-20
Prior cycle checked: 2026-07-17__release-v7.4 (`lessons_learnt_closure.md`)

---

## What worked well

- All four RISK-01-conditional items (`BLG-FE-115/116/117/118`) cleared Design Gate and shipped in the same cycle they were scoped into — the structural fix from v7.4's `AMD-20260717-01` retrospective (require design-artefact production as a precursor step, not in-sprint work) held for real this time, closing prior cycle's Carry-Forward item 2 (`BLG-FE-116` design-artefact assignment).
- Zero deviations filed across all four EPICs; the two cross-EPIC merge conflicts (EPIC-03 vs EPIC-02, EPIC-04 vs EPIC-02+EPIC-03) were both resolved cleanly per CLAUDE.md §8 with no data loss.
- `sprint_capacity.md`'s DL-069 baseline forward-flag (`BLG-GOV-249`) was explicitly confirmed matching this cycle rather than forwarded a third time, closing Release Planning lessons_learnt.md Carry-Forward item 2.
- Both Phase 4 friction items had precise, unambiguous process-patch wording already drafted in `lessons_learnt_cycle.md` — no reconstruction needed at closure time to apply them immediately.

---

## Friction Log

### Friction Item 1

**Classification:** Type A — Governance Drift: A documented rule or header requirement was ignored or missed

**Recurrence:** No — first identified this cycle (not checkable against a specific v7.4 closure friction item; distinct file)

**What happened:** `claude/system/changelogs/delivery_verification_changelog.md` (the companion per-file changelog for `delivery_verification_prompt.md`, required by `shared_standards.md` §11's Companion per-file changelog rule added 2026-07-17) had fallen significantly behind — its top row read version 2.3/2026-05-17 while the live prompt was at version 3.4 at the start of this run. `prompt_change_log.md` and `OPERATIONAL_GUIDE.md` §14 had both stayed correctly in sync throughout; only this one companion file drifted, echoing the same pattern the companion-changelog rule was created to catch for `roadmap_prompt_changelog.md` three days earlier.

**Where in the routine:** STEP 8 — Lessons Learnt Review and Application (immediate-action application of the Phase 4 friction items required a version bump to `delivery_verification_prompt.md`, which surfaced the companion file's staleness)

**Root cause:** document staleness — the Companion per-file changelog rule (`shared_standards.md` v3.17, 2026-07-17) postdates most of `delivery_verification_prompt.md`'s version history, so the gap predates the rule's existence and had not yet been swept.

**Blast radius analysis:**
- What would have propagated: no functional impact — `prompt_change_log.md` and `OPERATIONAL_GUIDE.md` §14 remained authoritative and in sync throughout, so no engine misread a version number. The only exposure is a misleading per-file changelog for any reader consulting it in isolation.
- When it would have surfaced: next `governance-drift` skill check or lifecycle audit cross-referencing all companion changelogs against `prompt_change_log.md`.
- Recovery cost if uncaught: low (single file backfill) — no downstream engine reads this file as a state source.

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: `claude/system/changelogs/delivery_verification_changelog.md`
  - Section: full table body
  - Change required: backfill the missing 2.4–3.4 version rows (matching detail level already present in `prompt_change_log.md`'s historical entries for this file) so the companion changelog is fully continuous, not just resynced going forward.
  - Owner: Head of Specs Team
  - Target: next roadmap review (same disposition precedent as the `roadmap_prompt_changelog.md` partial backfill, `2026-07-17__scheduled`)

This run added the current 3.4→3.5 entry at the top of the table (restoring sync going forward) but did not backfill the historical gap, consistent with the precedent set for `roadmap_prompt_changelog.md`.

---

## Recurrence Escalations

None.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/delivery_verification_prompt.md` | STEP 2.1 | Added `Staging-deferred (per CLAUDE.md §2 / shared_standards.md §16.11)` as an explicitly accepted `Result` value alongside `Pass`/`Pass with notes`/`Fail`, conditioned on a confirmed pre-PR backlog item | 3.4 → 3.5 | Yes |
| `claude/system/templates/qa_evidence_template.md` | Standard Sign-Off Block | Agent-mediated DoQ sign-off must use `Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)`, not the literal `Director of Quality` string, so signer provenance is visible in the field itself | 1.7 → 1.8 | Yes |
| `claude/system/OPERATIONAL_GUIDE.md` | §9, §14 | Source prompt header and governance table updated to match both bumps above | 4.102 → 4.103 | Yes |
| `claude/system/changelogs/delivery_verification_changelog.md` | Table (top row only) | Current-version entry added to restore going-forward sync (historical backfill deferred — see Friction Item 1) | n/a (companion changelog, not itself versioned) | Not applicable |

Both immediate actions resolve `lessons_learnt_cycle.md` Phase 4 friction items 1 and 2 in full (both were `defer` classification at Phase 4 time pending Head of Specs Team confirmation; that authority is one of this routine's three required roles, so both were re-classified `immediate` and applied now per the non-deferrable immediate-action rule rather than deferred a further cycle).

---

## New files created this run

None (`closure_state.json` and `closure_record.md` are standard STEP 0/STEP 9 outputs, not "improvement" artefacts).

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/changelogs/delivery_verification_changelog.md` | Table body | Backfill missing 2.4–3.4 historical version rows | Head of Specs Team | next roadmap review |
| n/a (`lessons_learnt_cycle.md` Phase 3 friction item 1) | Shared-file merge-conflict collision surface (`backend/routers/test.py`, `src/pages/SystemStatus.js`, `tests/e2e/system-status.spec.js`, `docs/specs/data_model.md`, `docs/ops/api_performance_baseline.md`, `docs/reference/openapi.yaml`) | Consider a structural fix (e.g. per-EPIC append-only manifest files aggregated at build/CI time) to remove the recurring cross-EPIC merge-conflict surface — 2nd consecutive multi-EPIC sprint to hit this pattern (also seen `2026-07-10__release-v6.9`) | Head of Engineering | next roadmap review |
| n/a (`lessons_learnt_cycle.md` Phase 3 friction item 2) | Coding standard / lint rule | Require `Array.isArray(...)` guards on any `.map()`/`.filter()` call over a JSON API response field (`json.data \|\| []` weak-guard pattern reused across ≥2 EPICs this sprint before being caught in EPIC-04's own DoQ pass) | Head of Engineering | next roadmap review |
| `claude/roadmap/current_roadmap.md` §3 | Next-release scoping | Roadmap Now-horizon is empty following v7.5's ship — no anchor items currently named for the next cycle; `Next planned release` reset to `[TBD]` | Product Owner / PMO Lead | before next `plan release` |

Note: the Phase 3 items above were classified `defer` (not `decision_required`) at Phase 4 review time with named owner and target already specified; STEP 8 re-confirms that classification stands — both require Head of Engineering-led design work spanning more than this session and are correctly deferred rather than applied immediately.

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Two consecutive multi-EPIC sprints (`2026-07-10__release-v6.9`, `2026-07-17__release-v7.5`) have hit the same shared-file cross-EPIC merge-conflict pattern across `backend/routers/test.py`, `src/pages/SystemStatus.js`, `tests/e2e/system-status.spec.js`, `docs/specs/data_model.md`, `docs/ops/api_performance_baseline.md`, and `docs/reference/openapi.yaml`. | Sprint Planning should flag this collision-surface risk explicitly when scoping ≥3 EPICs that each register new endpoints, and Head of Engineering should evaluate the per-EPIC append-only manifest structural fix named in the Phase 3 friction log. | Sprint Planning / Roadmap |
| 2 | `src/pages/SystemStatus.js` `categorizeEndpoint()` does not have an `includes()` branch for either of v7.5's two new top-level path prefixes (`/price-alerts`, `/saved-filters`) — both endpoints will silently fall into the `'Other'` category rather than their own named category. | Frontend engineer should add `/price-alerts` and `/saved-filters` branches (or a general fallback naming scheme) to `categorizeEndpoint()` before the next System Status review; not a hard gate (existing behaviour degrades gracefully to `'Other'`, no error). | Sprint Planning |

