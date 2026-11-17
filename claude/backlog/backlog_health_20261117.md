**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-11-17

# Backlog Health Report — 2026-11-17

Run: `GROOM-20261117-01`, invoked as `post_ship_closure.md` STEP 12 for `2026-11-11__release-v9.17` (not a dry run). Lock acquired and released.

## Summary

```
Backlog Health Summary — 2026-11-17

Total items reviewed: 336 at the start of this run (including BLG-QA-268, filed at closure STEP 8); 312 remain after 24 were archived
Complete — Archive: 24
Killed — Archive: 0
Active — Keep: 312
Orphans flagged: 0
Blocked — stale blocker flagged: 0
Spec debt items — resolved: 1 (BLG-SPEC-202; shipped v9.17 ST-19 and archived)
Spec debt items — still open: unchanged apart from the one above
Priority misalignments flagged: 0
Promotion candidates: 8
Ambiguous items resolved: 0 (2 surfaced, below)
```

Archived (24): the 18 v9.17 source items with ✅ COMPLETE banners (17 bannered at closure STEP 3, plus `BLG-BE-211`, bannered at its post-merge backfill on 2026-11-16); the 5 items fixed on their EPIC branch before merge (`BLG-FE-295`, `BLG-FE-296`, `BLG-FE-298`, `BLG-FE-300`, `BLG-FE-303`); and `BLG-FE-237`, bannered this run on the ST-06 evidence (`qa_evidence_EPIC-02.md`; `verification_report.md` §5 "for `groom backlog` to close").

Kept open as post-merge trackers (closure STEP 3.1 case (i)): `BLG-OPS-217` (ST-15 AC 2–3) and `BLG-GOV-419` (ST-18 AC 2).

## Pre-Scan Results (STEP 1.1–1.3)

- **Gate Field Normalisation:** 0 `**Gate:**` labels in `backlog.md`.
- **Effort Day-Range Validation:** PASS. 0 items are missing a required day range.
- **Field-Completeness Scan:** PASS. 0 items are missing `**Effort:**` or `**Provisional-Target:**`.
- **Gate-Inheritance Field-Completeness Scan:** PASS. 0 candidates found.
- **Governance Prompt Duplicate Cross-Check:** PASS. 0 candidates. Prompt changes since the last groom: `release_planning_prompt.md` v2.74 (`ESC-CLOSE-20261111-01`) and v2.75 (ST-18, which met `BLG-GOV-419` AC 1; AC 2 is the open post-merge remainder, not a duplicate); `execution_prompt.md` v3.95 and `post_ship_closure.md` v2.48 (this closure). `BLG-GOV-420` (pre-commit review and impact statement), `BLG-GOV-421` (prompt size budget on direct-to-main commits) and `BLG-GOV-422` (design gate premise checks) address gaps these changes do not cover. `BLG-QA-268` was filed by this closure for the part of `LL-v9.17-P3-01` that v3.95 did not apply.

## Release Planning Archive List (STEP 0/1)

Source: `claude/cycles/2026-11-11__release-v9.17/run_manifest.md` (0 already-resolved banners).

| Item | Outcome |
|------|---------|
| `BLG-QA-75` | Kept (Active). Carried again as "bundles the gated CI limb". No completion banner; its gate text is a Release Planning §1.3a decision |

## Ephemeral Section Cleanup (STEP 1.5)

None found.

## Spec-Debt Deep Review

Not due: invocation 1 of 3 since the marker `2026-11-06__release-v9.16`. (Closure STEP 7.2 ran `check_specs_index_freshness.py` anyway: `journal.md` and `performance.md` are unregistered. `journal.md` is already tracked by `BLG-SPEC-221`; both are in closure record §6 row 3.)

## Promotion Candidates

| Item ID | Title | Priority | Why Promote | Target Release | Pre-work Status |
|---------|-------|----------|-------------|----------------|-----------------|
| `BLG-GOV-422` | Design gate: check each new view's data source and write worked examples | P2 | PO direction 2026-11-12 (seat next release), with the 2026-11-13 scope extension; v9.17 `LL-v9.17-P3-02` | v9.18 (tag reads `TBD`) | Ready; scope extension not yet written into the item |
| `BLG-QA-262` | Unit-test pure frontend logic in CI | P2 | PO direction 2026-11-12 | v9.18 (tag reads `TBD`) | Ready |
| `BLG-FE-294` | Show "earnings unknown" instead of nothing when a lookup fails | P2 | Accepted P2 found defect (PO + DoQ, 2026-11-13) | v9.18 (tag reads `TBD`) | Ready |
| `BLG-UX-08` | First-principles UX re-review when the programme ships | P2 | Gate met this run: every item in `BLG-FE-244`–`266` and `BLG-SPEC-214`–`216` is closed | v9.18 | Gate to be cleared in place by Release Planning §1.3a |
| `BLG-BE-213` | Use the live FX rate, not a hard-coded 1.27 | P2 | Ungated P2, tagged v9.18 | v9.18 | Ready |
| `BLG-GOV-420` | Require the pre-commit code review and impact statement | P2 | Ungated P2, tagged v9.18 | v9.18 | Ready |
| `BLG-GOV-421` | Enforce the prompt size budget on direct-to-main commits | P2 | Ungated P2, tagged v9.18 | v9.18 | Ready |
| `BLG-BE-208` | Use one native-entry function on every position path | P2 | Ungated P2 | `TBD` | Ready |

Also directed by the PO for the next release: `BLG-QA-260` (P3; its `Provisional-Target` v9.17 is stale and it needs a dated PO override).

Note: This list is advisory only. No items are added to the roadmap by this engine.

## Priority Alignment Notes

No misalignments found. The open P1 items (`BLG-FEAT-73`, `BLG-FE-43`–`71`, `BLG-SPEC-35`) are gated on later arcs and carry no near release target. No release is scoped: `current_roadmap.md` §1 "Next planned release" is `[TBD]`.

## Orphans Flagged

None.

## Blocked Items — Stale Blockers

None.

## Spec Debt Status

| Item ID | Spec | Status | Action taken |
|---------|------|--------|-------------|
| `BLG-SPEC-202` | `positions.md#Position Lifecycle State Badge` | Resolved (v9.17 ST-19, option (b)) | Archived |

## Deferral Age Validation (STEP 3.5)

- **Stale release tags:** 23 open items still read `Provisional-Target: v9.17`, the release just shipped: `BLG-FE-277`, `BLG-FE-279`, `BLG-QA-254`, `BLG-FE-280`, `BLG-SPEC-228`, `BLG-FEAT-101`, `BLG-QA-255`, `BLG-UX-09`, `BLG-BE-212`, `BLG-GOV-418`, `BLG-FE-283`, `BLG-FE-284`, `BLG-FE-285`, `BLG-QA-258`, `BLG-QA-259`, `BLG-OPS-216`, `BLG-FE-286`, `BLG-QA-260`, `BLG-UX-10`, `BLG-FE-287`, `BLG-QA-261`, `BLG-OPS-219`, `BLG-GOV-419`.
- **26 open items still read `v9.16`:** `BLG-OPS-211`, `BLG-FE-267`–`270`, `BLG-QA-244`, `BLG-BE-203`, `BLG-BE-206`, `BLG-GOV-409`–`412`, `BLG-SPEC-220`, `BLG-QA-246`, `BLG-FE-274`, `BLG-SPEC-221`, `BLG-QA-247`, `BLG-SPEC-222`, `BLG-QA-248`, `BLG-QA-249`, `BLG-QA-250`, `BLG-OPS-212`, `BLG-SPEC-223`, `BLG-BE-207`, `BLG-QA-252`, `BLG-QA-253`.
- **41 open items still read `v9.15`:** `BLG-TECH-25`–`33`, `BLG-GOV-384`, `BLG-QA-229`, `BLG-BE-191`, `BLG-FE-233`, `BLG-UX-06`, `BLG-UX-07`, `BLG-BE-195`, `BLG-FE-234`, `BLG-SPEC-209`, `BLG-QA-230`, `BLG-FE-235`, `BLG-QA-231`–`234`, `BLG-QA-236`, `BLG-GOV-399`, `BLG-OPS-201`, `BLG-SPEC-210`, `BLG-QA-239`, `BLG-BE-196`–`199`, `BLG-OPS-205`, `BLG-FE-236`, `BLG-BE-201`, `BLG-BE-202`, `BLG-FE-238`, `BLG-GOV-402`, `BLG-SPEC-212`, `BLG-GOV-403`.
- These now span three shipped releases (90 items). Under `ESC-CLOSE-20260923-01` the tags carry no selection weight, and `Provisional-Target` edits are outside this engine's status-and-flags scope. Retargeting is closure record §6 row 8. No item has a target that passed with an explicit deferral, so no 3-cycle deferral flag is raised beyond the stale-tag list.

## Items Requiring Product Owner Decision

- **Ambiguous — Confirm: `BLG-FE-224`** (amber-600 text on light surfaces). The v9.17 slice said it is superseded when ST-08 (`BLG-FE-265`) completes, but 1 `text-amber-600` remains in `src/` outside Replay, so its AC is not met. Confirm: close as superseded (the remainder moves to `BLG-FE-288`), or keep open.
- **Ambiguous — Confirm: `BLG-FE-242`** (Trade History filter and Exit dialog light-theme fill). Same supersession note. `ExitModal.js` now carries a light and dark pair; the saved-filter picker and the dedicated light-theme Trade History axe scan were not checked here. Confirm against its ACs before closing.
- **`BLG-UX-08` gate met.** The user asked to be reminded when the programme's last item shipped. Seat the re-review or record why not.
