**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-09-28__release-v9.8
**Story:** ST-01 (EPIC-01, BLG-FE-184)

# Decision Record — Remaining `toFixed`/`toLocaleString` Call Sites Migrated to the Shared Formatting Helper

## 1. Problem

73 files / 285 call sites still format money, percentage, R-multiple and "missing" values with ad hoc `toFixed`/`toLocaleString` logic instead of the canonical helper (`src/lib/format.js`), and at least one of those sites (`DEV-REPORTS-ST01-02` precedent shows this class of bug recurs) renders an exact-zero P&L with a colour tone instead of neutral.

## 2. Decision

No new visual design is introduced. This story is scope-of-application, not scope-of-design: every migrated call site must reproduce the already-canonical output table (`design_system.md` §Number and Currency Formatting, `docs/design/2026-09-21__release-v9.6/number-format-convention/decision_record.md`) exactly —

- money (unsigned/signed), percentage, R (computed/user-target), missing (`—`) — formats and rounding unchanged from the existing helper's documented contract.
- Zero P&L renders unsigned, neutral tone, wherever P&L is coloured — this is the already-approved exact-zero convention (`docs/design/2026-08-08__release-v8.5/exact-zero-pnl-colour-convention/decision_record.md`), extended to every remaining site instead of only the Reports page tables it originally covered.

Any call site whose current (pre-migration) output would change under the canonical formula is a bug being fixed by this migration, not a new design choice — Head of UX & Design does not need to approve each one individually; visible-value changes of this kind are covered by the cited decision records and QA's diff against them.

## 3. §13 Compliance

Not applicable — display formatting only, no AI call.

## 4. Frontend Spec Impact

None. The canonical contract lives in `design_system.md` §Number and Currency Formatting (outside this routine's `docs/specs/frontend/pages/` write scope) and is unchanged by this story. No page spec under `docs/specs/frontend/pages/` documents per-page formatting rules that diverge from the canonical helper, so no page spec requires an edit. Existing artefact reviewed and confirmed current — no new design work required (same disposition as `reports.md` v0.9's precedent).

## 5. Testability (CLAUDE.md §2)

Slice AC requires Playwright coverage of the observable AC (zero-P&L neutral tone, and the "0 unmigrated call sites" AC is a code-search assertion, not a rendering one). Per-page visual regressions, if any surface during migration, are covered by each page's existing Playwright suite plus the exact-zero-colour assertion this story adds.

## 6. Approval

Head of UX & Design: confirmed, 2026-09-28.
Product Owner: confirmed, 2026-09-28 — no new design work required; scope is conformance to already-approved convention.
