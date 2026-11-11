**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-11-11

# Backlog Health Report — 2026-11-11

Run: `GROOM-20261111-01`, invoked as `post_ship_closure.md` STEP 12 for `2026-11-06__release-v9.16` (not a dry run). Lock acquired and released.

## Summary

```
Backlog Health Summary — 2026-11-11

Total items reviewed: 317 at the start of this run (including BLG-GOV-419, filed at closure STEP 8); 282 remain after 35 were archived
Complete — Archive: 35
Killed — Archive: 0
Active — Keep: 282
Orphans flagged: 0
Blocked — stale blocker flagged: 0
Spec debt items — resolved: 3 (BLG-SPEC-195, BLG-SPEC-200, BLG-SPEC-201; shipped v9.16 and archived)
Spec debt items — still open: unchanged apart from the three above
Priority misalignments flagged: 0
Promotion candidates: 5
Ambiguous items resolved: 0 (1 surfaced, below)
```

Archived (35): the 33 items bannered at closure STEP 3 (the 29 shipped v9.16 source items, the post-merge trackers `BLG-OPS-215` and `BLG-OPS-218`, and `BLG-AI-23` and `BLG-OPS-48` under STEP 3.1 case (ii)). Also bannered this run with evidence and archived: `BLG-GOV-414` (met, see below) and `BLG-GOV-192` (already met; Release Planning archive list).

**`BLG-GOV-414` is met.** This is the first `groom backlog` after ST-28 merged. STEP 3.1 case (ii) was applied to `BLG-AI-23` (remainder `BLG-AI-27`, shipped as ST-19) and `BLG-OPS-48` (remainders `BLG-OPS-214` and `BLG-OPS-213`, shipped as ST-11 and ST-12; `BLG-SPEC-223` open). Each carries a ✅ COMPLETE banner naming its follow-up items. Neither is named by an open escalation.

## Pre-Scan Results (STEP 1.1–1.3)

- **Gate Field Normalisation:** 0 `**Gate:**` labels in `backlog.md`.
- **Effort Day-Range Validation:** PASS. 0 items are missing a required day range.
- **Field-Completeness Scan:** PASS. 0 items are missing `**Effort:**` or `**Provisional-Target:**`. Five items (`BLG-BE-66`, `BLG-SPEC-81`, `BLG-GOV-235`, `BLG-FEAT-83`, `BLG-QA-122`) carry both fields inline on a pipe-separated line, which a line-start parser misses. They are not gaps.
- **Gate-Inheritance Field-Completeness Scan:** PASS. 0 candidates found.
- **Governance Prompt Duplicate Cross-Check:** PASS. 0 candidates. Prompt changes since the last groom were checked against every open `BLG-GOV-*` item: `post_ship_closure.md` v2.46 (ST-28) and v2.47, `shared_standards.md` v3.42 (ST-25), `OPERATIONAL_GUIDE.md` §8.3 (ST-30), `execution_prompt.md` v3.94, `release_planning_prompt.md` v2.73 and `delivery_verification_prompt.md` v3.18. `BLG-GOV-417` (case (ii) and open escalations) and `BLG-GOV-419` (§1.3a `Provisional-Target`) address gaps these changes leave open; neither restates a fixed problem.

## Release Planning Archive List (STEP 0/1, v1.19)

Source: `claude/cycles/2026-11-06__release-v9.16/run_manifest.md` (0 already-resolved banners).

| Item | Outcome |
|------|---------|
| `BLG-GOV-192` | Bannered this run (evidence: `roadmap_management_prompt.md` §5.5 governance-drift cadence and `run audit`'s §14 check; `run_manifest.md` "explicitly ungated" list) and archived |
| `BLG-QA-75` | Kept (Active). Release Planning carried it as "bundles the gated CI limb". It has no completion banner, and its gate text is a Release Planning §1.3a decision |
| `BLG-OPS-197`, `BLG-GOV-399` (retarget off v9.15) | `BLG-OPS-197` shipped (ST-13) and is archived. `BLG-GOV-399` still reads v9.15; `Provisional-Target` edits are outside this engine's status-and-flags scope (see Deferral Age Validation) |

## Ephemeral Section Cleanup (STEP 1.5)

None found.

## Spec-Debt Deep Review

Due: invocation 3 of 3 since the marker `2026-10-16__release-v9.13`. The marker is advanced to `2026-11-06__release-v9.16`.

- `scripts/check_specs_index_freshness.py` reported **1 addition**: `docs/specs/frontend/pages/journal.md` (added in v9.15 ST-10) is not registered in `Specs_Index.md`. **Already tracked** by `BLG-SPEC-221`, so no new item is filed.
- 1 REMOVAL reported, `qa_evidence_EPIC-xx.md`. **Not a gap:** it is a placeholder pattern in TSG section prose, as at the last deep review.
- Items filed: 0. Candidates already tracked: 1. Candidates confirmed not-a-gap: 1.

## Priority Alignment Notes

No misalignments found. No P0/P1 item is open with a release target. No release is scoped: `current_roadmap.md` §1 "Next planned release" is `[TBD]`.

## Orphans Flagged

None.

## Blocked Items — Stale Blockers

None.

## Spec Debt Status

| Item ID | Spec | Status | Action taken |
|---------|------|--------|-------------|
| `BLG-SPEC-195` | `ai_endpoints.md#POST /ai/journal-summary` | Resolved (v9.16 ST-21) | Archived |
| `BLG-SPEC-200` | `data_model_positions_dictionary.md` | Resolved (v9.16 ST-22) | Archived |
| `BLG-SPEC-201` | `settings.md` | Resolved (v9.16 ST-23) | Archived |

## Deferral Age Validation (STEP 3.5)

- **Stale release tags:** 28 open items still read `Provisional-Target: v9.16`, the release just shipped: `BLG-FE-254`, `BLG-OPS-211`, `BLG-FE-267`–`270`, `BLG-QA-244`, `BLG-BE-203`, `BLG-BE-205`, `BLG-BE-206`, `BLG-GOV-409`–`412`, `BLG-SPEC-220`, `BLG-QA-246`, `BLG-FE-274`, `BLG-SPEC-221`, `BLG-QA-247`, `BLG-SPEC-222`, `BLG-QA-248`, `BLG-QA-249`, `BLG-QA-250`, `BLG-OPS-212`, `BLG-SPEC-223`, `BLG-BE-207`, `BLG-QA-252`, `BLG-QA-253`.
- **43 open items still read `v9.15`**, two releases back: `BLG-TECH-25`–`33`, `BLG-GOV-384`, `BLG-QA-229`, `BLG-BE-191`, `BLG-FE-233`, `BLG-UX-06`, `BLG-UX-07`, `BLG-BE-195`, `BLG-FE-234`, `BLG-SPEC-209`, `BLG-OPS-195`, `BLG-QA-230`, `BLG-FE-235`, `BLG-QA-231`–`234`, `BLG-QA-236`, `BLG-GOV-399`, `BLG-OPS-201`, `BLG-SPEC-210`, `BLG-QA-239`, `BLG-BE-196`, `BLG-BE-197`, `BLG-OPS-205`, `BLG-BE-198`, `BLG-BE-199`, `BLG-FE-236`, `BLG-BE-201`, `BLG-FE-237`, `BLG-BE-202`, `BLG-FE-238`, `BLG-GOV-402`, `BLG-SPEC-212`, `BLG-GOV-403`. Each has now passed two named releases unseated. None has three consecutive passed targets yet, so none is a 3-cycle deferral flag. If they are not retargeted or seated at v9.17, most become 3-cycle deferrals at the next groom. Retargeting is for the item owners or Release Planning.
- `BLG-OPS-217` (P2, accepted) reads `TBD`, although its acceptance record says "Tracked at P2 for v9.17".

## Feature-ID Gate Staleness (Release Planning Friction Item 2, `LL-v9.16-Release-02`)

The gate scan lists 14 gating-item-shipped items. Five of them are gated on roadmap features that shipped long ago, plus a usage condition, and their Scope was written for that era's app: `BLG-FEAT-26` and `BLG-FEAT-62` (PT-04, v6.1), `BLG-FEAT-31` (PT-02), `BLG-FEAT-33` and `BLG-FEAT-34` (PT-05). If a gate scan clears one, its Scope needs re-reading against the current app before it is seated, as the v9.16 slice had to do for `BLG-FE-39` and `BLG-QA-21`–`23`. This engine does not edit gates or scope. Flagged for the item owners and the next `plan release` gate scan.

## ID Uniqueness Scan (STEP 4.5)

PASS for this run's additions: every new archive ID appears exactly twice, as a compliant §6.1 stub + verbatim pair. No active ID appears in the archive. The 5 pre-existing archive triplicates are unchanged.

## Promotion Candidates

| Item ID | Title | Priority | Why Promote | Target Release | Pre-work Status |
|---------|-------|----------|-------------|----------------|-----------------|
| `BLG-FE-282` | Pre-fill the Trade Plan stop from the §5 suggested stop | P2 | Accepted found defect (PO + DoQ); Known Deviation `DEV-v9.16-ST27-01`; recommended first | v9.17 | None needed |
| `BLG-FE-281` | Research "Create Trade Plan" drops the market | P2 | Accepted found defect (PO + DoQ) | v9.17 | None needed |
| `BLG-FE-278` | Trade Plan pre-entry acknowledgement not reset when the result changes | P2 | Accepted found gap (PO + DoQ) | v9.17 | None needed |
| `BLG-BE-211` | No backend path moves a linked plan to `closed` | P2 | Accepted found defect (PO + DoQ) | v9.17 | None needed |
| `BLG-OPS-217` | 665 of 7,105 weekly production market-data calls fail | P2 | Accepted found defect (PO + DoQ) | `TBD` (acceptance says v9.17) | None needed |

Note: This list is advisory only. No items are added to the roadmap by this engine.

## Items Requiring Product Owner Decision

- **`BLG-FE-254`, Ambiguous — Confirm:** ST-06 shipped every sealed AC, but the source item's AC still covers every observable `dashboard.md` §1B AC, including TL-09 and TL-10 (Stops moved group). `BLG-BE-205` supplies the data, but its ACs do not include the two Playwright ACs. Under STEP 3.1 case (i) it stays open (closure record §6). Add TL-09/TL-10 to `BLG-BE-205`'s ACs and banner `BLG-FE-254`, or keep both open.
- **Legacy governance items `BLG-GOV-200` and `BLG-GOV-201`:** they still have a Proposed solution but no AC (v9.15 closure §6 row 5). Release Planning v9.16 counted them in the ready pool at 1.25d each. Add ACs, or kill them, before either is seated.

## Run Notes

- The archive move was checked against a pre-run copy: removed IDs are exactly the 35 archived, 0 IDs were added, every `## ` heading is unchanged, and `check_backlog_item_integrity.py` passes.
