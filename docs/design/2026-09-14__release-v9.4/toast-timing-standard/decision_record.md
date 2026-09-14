**Owner:** Head of UX & Design
**Cycle:** 2026-09-14__release-v9.4
**Story:** ST-27 (BLG-UX-04, EPIC-06)
**Status:** Approved

## Classification note

Reclassified from an initial Design Pre-Approved read to **Design Required** during STEP 1 — toast display duration is timing-sensitive interaction behaviour under the §6 motion/timing special rule (BLG-FE-131), which applies "even when no new component or layout change is involved" and "regardless of whether a shipped animation actually changes" (per the `2026-09-07__release-v9.2` ST-05 precedent — a guideline authored with no shipped change that cycle was still Design Required). ST-27 authors a new toast-timing standard; the same treatment applies.

## Context

`design_system.md` currently documents only `sonner`'s default ~4s auto-dismiss and one explicit override (`ConfirmationModal`'s undo-window toast, 5s). No standard exists for varying toast duration by message length or severity — each call site currently either accepts the library default or picks an ad hoc override.

## Decision

1. **Standard duration rule** (by severity, the simpler and more consistently-derivable of the two AC-suggested axes — message length varies continuously and would require a formula rather than a lookup, message severity already has a fixed, small enum matching the existing chip/badge conventions elsewhere in the system):

| Severity | Duration | Rationale |
|----------|----------|-----------|
| Success / informational (default) | 4s (`sonner` default, unchanged) | Matches existing behaviour — no regression for the common case |
| Warning | 6s | Needs more read time than a routine confirmation |
| Error | 8s, or manual dismiss if the message includes a required next action | Errors requiring the user to act must not disappear before they can read and respond |
| Undo-actionable (`ConfirmationModal` undo-window) | Unchanged — already explicitly 5s default, carries its own countdown | Pre-existing exception, not superseded |

2. **Message-length exception:** any toast whose body text exceeds ~80 characters gets a **minimum** floor of 6s regardless of the severity table above (reading time), applied as a floor, not a replacement for the severity-based value.
3. **Non-conforming screens** (documentation only this cycle, no remediation): a full inventory of every `sonner` call site was not performed as part of this gate (scope: standard-setting, not an app-wide audit) — flagged as the same deferred-audit pattern already used for the motion-vs-contrast guideline (ST-05/v9.2) and this cycle's own ST-13. The inventory itself becomes ST-27's own execution-phase deliverable (its AC already calls for "list of non-conforming screens produced for future remediation").

## Rationale

Severity-based durations reuse an axis (severity) the system already has fixed vocabulary for (success/warning/error, matching `StandingAlert`'s own severity variants above) rather than inventing a length-based formula from scratch; the length exception is added as a floor to avoid the common failure mode of a short-duration toast carrying a long, unreadable message.

## Sign-off

Head of UX & Design: Approved, 2026-09-14.
Product Owner: Approved, 2026-09-14.
