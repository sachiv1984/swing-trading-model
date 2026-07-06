**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 4)
**Status:** Approved
**Last Updated:** 2026-07-06
**Cycle:** 2026-07-06__release-v6.7
**Covers:** ST-01 (BLG-FE-87), ST-02 (BLG-FE-88), ST-03 (BLG-FE-89)
**Design Source:** Extends `claude/cycles/2026-07-04__release-v6.6/contrast_audit_findings.md`

---

# UX Decision Record — Secondary-Text Contrast Remediation

## 1. Problem

`claude/cycles/2026-07-04__release-v6.6/contrast_audit_findings.md` established that:
- 262 bare `text-slate-500` instances (~90 files) fail WCAG-AA against the app's default dark-theme surfaces (3.07–4.24:1 vs the 4.5:1 requirement) — Finding 1 / BLG-FE-87.
- 764 bare `text-slate-400`/`text-slate-500` instances (102 files) have no `dark:`/light-mode companion and fail badly when the app is toggled to light mode (`text-slate-400` as low as 2.34:1) — Finding 2 / BLG-FE-88.
- No shared token exists to prevent a fourth recurrence — Finding 3 / BLG-FE-89.

This record makes the concrete colour decision the audit deferred, so ST-01/ST-02 implementation and ST-03's token can proceed without further design review.

## 2. Method

Computed WCAG 2.1 contrast ratios (standard relative-luminance formula) for each candidate Tailwind slate shade against the three ambient surface colours already in use (`src/Layout.js`): dark theme `bg-slate-950` / `bg-slate-900` / `bg-slate-800`, light theme `white` / `bg-slate-50` / `bg-slate-100`. All affected instances are `text-xs`/`text-sm` (12–14px regular) so the 4.5:1 normal-text threshold applies throughout — no large-text 3:1 allowance.

## 3. Decision — Canonical Secondary-Text Token (ordinary label/secondary text)

| Theme | Class | Worst-case ratio (darkest/lightest surface in use) | Result |
|---|---|---|---|
| Dark | `text-slate-400` | 5.71:1 vs `bg-slate-800` | PASS (was `text-slate-500`, 3.07:1 FAIL) |
| Light | `text-slate-600` | 6.92:1 vs `bg-slate-100` | PASS (was bare `text-slate-400`/`text-slate-500`, 2.34–4.34:1 FAIL/borderline) |

**Canonical class pair:** `text-slate-600 dark:text-slate-400`

`text-slate-400` was chosen over the audit's own dark-theme precedent (`text-slate-300`, used by BLG-UX-01) because it is the minimum shade that clears all three dark surfaces with margin while staying visually closer to the original "muted" secondary-text intent — `text-slate-300` reads closer to primary text at this weight. `text-slate-600` was chosen over `text-slate-500` for light because `text-slate-500` fails against `bg-slate-100` (4.34:1) — one of the three light surfaces in active use — so it cannot be the single token value across all light surfaces.

**Rejected:** a single non-`dark:`-varying value. Tailwind's `darkMode: ["class"]` strategy requires an explicit `dark:` variant to differ by theme (confirmed in Finding 2); no single hex value clears both dark and light 4.5:1 requirements simultaneously (dark surfaces are near-black, light surfaces are near-white).

## 4. Decision — Elevated/Compliance Disclaimer Text (exception, not the generic token)

Two pre-existing instances (`BLG-UX-01` dashboard Advisory Label, `BLG-UX-02` AI chat footer) were deliberately given stronger-than-generic dark-theme treatment ahead of this cycle because they carry §13 compliance-disclosure weight, not because they are ordinary secondary text:

| Instance | Dark (existing, unchanged) | Light (new — was missing) |
|---|---|---|
| Dashboard Advisory Label (`dashboard.md` §Advisory, v2.5) | `text-slate-300` (9.85:1 vs `bg-slate-800`, retained) | `text-slate-700` (9.45:1 vs `bg-slate-100`) |
| AI Chat Widget footer (`positions.md` §Footer, v1.9) | `text-slate-400` (5.71:1 — already matches the generic dark token) | `text-slate-600` (6.92:1 — generic light token; no reason to diverge) |

**Rule:** do not collapse the Dashboard Advisory Label onto the generic token — its dark value was chosen for extra headroom on a compliance-sensitive surface and must not regress. Add a light companion only.

## 5. Scope Boundary (what this record does NOT decide)

- **Icon-only usages** (e.g. `Loader2`/`BookOpen` Lucide icons carrying a `text-slate-*` class for `currentColor` fill/stroke) are out of scope. BLG-FE-87/88 ACs are scoped to "secondary/label **text**"; icon contrast is governed by WCAG 1.4.11 (non-text, 3:1), a separate criterion not audited here. ST-01/ST-02 execution must not silently reclassify icon instances as in-scope without a new backlog item.
- **Bare `text-slate-300` instances** (e.g. `trade_history.md` column headers, `reflections.md` "Hold" column) are out of the filed scope of BLG-FE-87 (262 `text-slate-500` instances) and BLG-FE-88 (502 `text-slate-400` + 262 `text-slate-500` = 764 instances). `text-slate-300` bare-class light-theme risk is a real, symmetric gap but was not in the audited/filed instance count — flagged as a candidate follow-up finding for a future audit, not remediated in this cycle.

## 6. Sequencing (unchanged from backlog)

1. **ST-01** — replace failing bare `text-slate-500` → `text-slate-400` (dark-theme fix, in-scope instances only).
2. **ST-02** — add the light-mode companion (`text-slate-600` bare / `dark:text-slate-400`) to every in-scope instance, including the ones just touched by ST-01 and the two pre-existing disclaimer instances (§4).
3. **ST-03** — document `text-slate-600 dark:text-slate-400` as the canonical secondary-text token in `docs/specs/frontend/design_system.md` §Color Usage / §Accessibility. **Note:** `design_system.md` is outside this Design Gate engine's write scope (§5 of `design_gate_prompt.md` permits only `docs/specs/frontend/pages/`) — the actual edit to `design_system.md` is deferred to ST-03's own Sprint Execution commit. This decision record is the locked design source ST-03 must implement verbatim; no further design review is required at execution time.

## 7. Approval

**Head of UX & Design:** confirmed 2026-07-06
**Product Owner:** confirmed 2026-07-06
