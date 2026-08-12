**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-08-12__release-v8.7
**Story:** ST-21 (EPIC-07, BLG-SPEC-124)

# Decision Record — Canonical "Gated" `DataState` Variant

## 1. Problem

The roadmap carries several feature surfaces that exist in the codebase but are not yet unlocked (SI-02, SI-04, SI-05 Phase 2, the Arc 5 UX-prep cluster, etc. — see `BLG-GOV-303`'s Roadmap Unlock Tracker for the full list). None of `DataState`'s existing branches (`loading` / `error` / `empty`) fit this case: `empty` communicates "no data yet, but the feature is live and will fill in from your own actions" — a locked feature is a categorically different message ("this will unlock once a system-wide condition is met; nothing you do here changes that"). Surfaces have been rendering gated features ad hoc (inconsistent copy, some using `empty`, which misleads users into thinking the surface is actionable). This decision formalises a dedicated `gated` branch.

## 2. Decision

Add a `gated` prop to `DataState` (`src/components/ui/DataState.js`), evaluated **before** `loading`/`error`/`empty` — a gated feature never fires its underlying data fetch in the first place, so there is no loading/error/empty state to reach:

**Priority order:** `gated` → `loading` → `error` → `empty` → children.

### Visual treatment

| Element | Spec |
|---------|------|
| Icon | `Lock` (lucide-react), `text-slate-400 dark:text-slate-500` — explicit light+dark pair, no dark-only token (per `design_system.md`'s Card Hierarchy precedent) |
| Outer padding / sizing | Same as the branch it replaces at each call site — reuses `compact`/default sizing exactly like `empty` does; `gated` is a content-branch choice, not a new sizing system |
| Heading | `text-sm font-semibold` (default) / `text-xs font-semibold` (`compact`) — same tier rule as `empty` |
| Body | `text-xs`, one sentence, present tense |
| CTA | None by default. A gated surface is not user-actionable — there is no button that unlocks it — so `DataState`'s optional `emptyAction` pattern does not apply to `gated`. If a call site wants a "Learn more" link to the Roadmap Unlock Tracker, that is a per-consumer addition, not part of this shared pattern. |

### Copy pattern

Distinct wording from the `empty` microcopy pattern (v1.8) is required so a user cannot mistake "not unlocked" for "no data yet, add some":

- **Heading:** `"<Feature name> — Locked"` (not `"No <noun>"` — that phrasing implies user-fillable).
- **Body:** states the gate condition in plain language, present tense, ends with a full stop — e.g. `"Unlocks once 20 closed trades are linked to a plan."` Numeric conditions should state the target, not the app's live progress toward it (progress numbers go stale between renders unless a consumer explicitly wires a live count; the static condition text does not).
- **Optional `gatedProgress`:** a consumer may pass a short progress string (e.g. `"3 of 20"`) rendered as a muted subtext line beneath the body, for surfaces that already have the live count on hand. Optional — omitting it is not a gap.

### Interaction

The gated branch's content region is inert — no hover/focus affordances on the locked content itself (there is nothing to interact with underneath). This distinguishes it from a disabled *button*, which retains a visible disabled affordance; `gated` is a full content-region replacement, same mechanism as `empty`.

## 3. §13 Compliance

Purely a display/interaction spec for existing, already-approved gate conditions (sourced from each feature's own canonical gate definition, cross-referenced via `BLG-GOV-303`'s Roadmap Unlock Tracker). No new predictive or advisory content introduced.

## 4. Frontend Spec Impact

`design_system.md` §Shared UI Components → Cards → Data States gains a new "Gated variant" subsection, alongside the existing Compact/Inline variant entries.

## 5. Approval

Head of UX & Design: confirmed, 2026-08-12.
Product Owner: confirmed, 2026-08-12.
