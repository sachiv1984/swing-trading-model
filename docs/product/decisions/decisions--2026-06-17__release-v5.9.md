**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Superseded
**Release:** v5.9
**Cycle:** 2026-06-17__release-v5.9
**Last Updated:** 2026-06-17
**Scope revision:** v1 — 2026-06-17: EPIC-02 replaced; 8 date-gated items deferred; 6 ungated items added.

---

# Planning Decisions — v5.9

## Scope Decisions

| Decision | Rationale | Authority |
|----------|-----------|-----------|
| All date-gated items removed from v5.9 scope | Items with gate dates (2026-06-21, ~2026-06-23, 2026-07-04) deferred to v5.10. Release should only contain items executable immediately. | Product Owner |
| BLG-GOV-125–129 firm (SC-03–SC-07) | All five SC items ready now; no gate conditions. GCA-2026-06-17 confirmed. | Head of Specs Team |
| BLG-QA-24, BLG-QA-34, BLG-QA-50 added | QA coverage and test infrastructure items with no gate conditions. Ready to execute. | Director of Quality |
| BLG-GOV-38, BLG-GOV-53 added | Governance audit and process record items with no gate conditions. Ready to execute. | PMO Lead |
| BLG-FE-57 added | Small UX improvement to PreEntryValidationPanel with no gate condition. XS effort. Requires Playwright coverage per CLAUDE.md §2. | Head of UX & Design |
| BLG-FE-64/41 deferred to v5.10 | Gate 2026-06-21; date-gated. BLG-FE-64 will be 6th consecutive deferral — mandatory carry-forward to v5.10 release planning. | Product Owner |
| SI-05 effectiveness review items (BLG-GOV-112/113/115, BLG-OPS-59, BLG-GOV-130) deferred to v5.10 | Gate 2026-07-04; date-gated. v5.10 will be the SI-05 effectiveness review release. | Product Owner |

## Sequencing Decisions

| Decision | Rationale |
|----------|-----------|
| EPIC-01 merges first | Governance prompt changes; independent of EPIC-02. |
| EPIC-02 merges after EPIC-01 | No hard dependency, but sequencing avoids any governance prompt version conflict. |
| Single sprint | All 11 stories are ungated; estimated ~13–17 hours total. Single sprint sufficient. |

## Accepted Risks

None.

## Escalations

None.

## Supersession note

*(Completed at Post-Ship Closure)*
