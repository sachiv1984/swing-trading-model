**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-11-03__release-v9.15

# Post-Gate-Correction Addendum — 2026-11-03__release-v9.15

Corrections below are additive to the sealed `stage4_backlog_slice.md` — they do not replace or edit its content. Sprint Planning and Sprint Execution must read both files together as the combined authoritative scope.

## ST-01 — The acknowledgement needs a ruling against §4.2.6 before it is built
**Found at:** Design Gate STEP 1 / STEP 2.2
**Correction:** AC 2 says "save requires the acknowledgement". `strategy_rules.md` §4.2.6 (binding) says the pre-entry advisory panel "must never prevent, gate, or auto-reject" a submission, and that any hard submission gate needs a new §13 review. The Trade Plan path's acknowledgement does not disable Save today, and the Strategy Rules & System Intent Owner's 2026-11-03 confirmation for this item calls the checks "display-only". §4.2.1 (v1.20) also says entries in an unknown-regime market "are blocked", which reads against §4.2.6. ST-01's first sub-step is therefore a dated Strategy Rules & System Intent Owner ruling:
- **Branch A (acknowledge to proceed):** Submit is disabled until a WARN/FAIL is acknowledged. The ruling must state that a user-passable acknowledgement is not a "hard submission gate" under §4.2.6, or a §13 review must be completed as §4.2.6 requires. If the ruling clarifies §4.2.6 or §4.2.1 text, that is a `strategy_rules.md` write under `execution_prompt.md` §7 case (c), which needs the owner's confirmation of that AC line in the sealed `sprint_backlog.md` sign-off summary, the same treatment as RISK-03.
- **Branch B (advisory only):** Submit stays enabled, as on the plan path. AC 2 is then met by the regime check showing its FAIL/unknown state and the acknowledgement being offered.

Both branches are designed (`docs/design/2026-11-03__release-v9.15/trade-entry-pre-entry-checks/decision_record.md` §2.3; `position_form.md` v1.12 §Pre-Entry Checks). The story deletes the branch not taken. AC 1, AC 3 and AC 4 are unchanged. Separately, AC 1's "Record overrides from this path" Scope bullet means `POST /portfolio/position` gains an optional `pre_entry_override_acknowledged` field: contract and `openapi.yaml` in the same commit.
**Date:** 2026-11-03

## ST-16 — Both win-rate widgets exist only on the legacy Dashboard page that ST-12 deletes
**Found at:** Design Gate STEP 1
**Correction:** `WinRateWidget` and `WinRateChart` are rendered only by `src/pages/Dashboard.js` (the pre-v7.3 widget page at `/Dashboard`). `src/pages/DashboardHome.js` and `src/components/dashboard/home/` render no win-rate widget. ST-12 removes `Dashboard.js` and the components only it uses, and ST-12's Scope bullet 1 already asked whether ST-16's fix "belongs on `DashboardHome` instead": there is no `DashboardHome` site to move it to. As sliced, ST-16 (0.5d) fixes two widgets that ST-12 then deletes in the same sprint. This gate changes no scope. At Sprint Planning the Product Owner decides between:
- keeping ST-16 as sliced (its Playwright tests are deleted with the page in ST-12);
- deferring or closing ST-16 as superseded by ST-12, recording on `BLG-FE-240` that the defect leaves with the page;
- adding a win rate to the Dashboard home, which is new UI. That needs its own design pass and belongs in ST-09's Today/status-card spec, not in v9.15 code.
**Date:** 2026-11-03
