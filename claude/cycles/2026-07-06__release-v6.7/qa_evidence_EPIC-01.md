Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-08

# QA Evidence — EPIC-01 (UX & Accessibility Contrast Remediation)

**EPIC:** EPIC-01 — UX & Accessibility Contrast Remediation
**Cycle:** 2026-07-06__release-v6.7
**Sprint goal:** Eliminate app-wide secondary-text WCAG-AA contrast failures across both dark and light themes and lock the fix into a shared design token, while closing out the full AUD-2026-07-06 governance-hardening backlog.
**Test scenarios used:** tests/e2e/secondary-text-contrast.spec.js (SC-CTR-01a, SC-CTR-01b, SC-CTR-02a, SC-CTR-02b)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | ux_spec.md §3, §6; positions.md v2.0, dashboard.md v2.6, reflections.md v0.2 | Systematic replacement of bare `text-slate-500` → `text-slate-400` (226 in-scope text instances, 59 files); 33 icon-only instances excluded | AC-01: systematic replacement verified per-surface — AC-02: contrast spot-checks recorded — AC-03: Playwright coverage (SC-CTR-01a/01b) | Pass | None |
| ST-02 | ux_spec.md §3, §4, §6; positions.md v2.0, dashboard.md v2.6, reflections.md v0.2 | Added `text-slate-600 dark:text-slate-400` pairing to 697 bare `text-slate-400` instances (101 files); fixed 1 broken pre-existing pairing; applied disclaimer exception (AiDailyBriefing.js); 29 icon-only instances excluded | AC-01: paired class combination added so both themes independently pass WCAG-AA — AC-02: prioritised by traffic (top-10 audited files covered) — AC-03: Playwright coverage (SC-CTR-02a/02b, light theme) | Pass | None |
| ST-03 | ux_spec.md §3, §4, §6; design_system.md v1.0 | Canonical secondary-text token transcribed verbatim into design_system.md §Color Usage and §Accessibility | AC-01: token defined and documented — AC-02: frontend spec (design_system.md) updated to reference it | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/e2e/secondary-text-contrast.spec.js` (4 scenarios: dark-theme empty-state/footer color, light-theme empty-state/footer color) — all passing, confirmed via direct execution (not inferred). Full regression suite (`tests/e2e/` — 431 spec files) run twice (after ST-01, after ST-02): 428 passed, 3 skipped (pre-existing, unrelated), 0 regressions attributable to this EPIC's changes. One transient timing flake (`alert-nav-badge.spec.js` SC-ANB-05) observed on one full-suite run; re-run 3× in isolation, passed 3/3 — confirmed pre-existing flake unrelated to contrast changes (no `text-slate` reference in that spec or its underlying component).
- Regression areas checked: full `tests/e2e/` suite (431 spec files covering all pages/components) — see commit messages for exact pass counts. Cross-spec selector check (LL-v3.2-P3-02) performed at each story: found and fixed 3 stale `.text-slate-500`/`.text-slate-400` CSS-class selectors in existing specs whose target elements this EPIC modified (`fee-drag-trade-history.spec.js`, `slippage-tracking.spec.js`, `research-typography.spec.js`) — all 3 re-verified passing after the fix, in the same commit as the source change that broke them.
- Known deviations filed: None. All AC met without divergence from the locked design record.

**Agent-mediated DoQ review finding, resolved in-session:** Initial review (Director of Quality role, §5.3) found that `src/Layout.js` (the app shell/sidebar, rendered on every page) was outside the scope of both the ST-01/ST-02 scripted transformations — those scripts walked only `src/pages` and `src/components`, missing the 3 top-level `src/*.js` files. Layout.js uses an `isDark ? A : B` JS-ternary pattern (not Tailwind's `dark:` class variant) for theme-conditional styling, and 4 of its 14 secondary-text instances had the exact failure profile from the design record (e.g. `isDark ? "text-slate-500" : "text-slate-500"` — same failing colour in both themes). The other 10 `isDark` instances in Layout.js were already correctly theme-differentiated (e.g. `isDark ? "text-slate-400 ..." : "text-slate-600 ..."`) and did not need correction. Fixed the 4 genuine instances to `isDark ? "text-slate-400" : "text-slate-600"` (the ternary-idiom equivalent of the canonical `text-slate-600 dark:text-slate-400` pair), verified via Babel parse (0 errors) and full e2e suite re-run (429 passed, 3 skipped, 0 failed). Per LL-v3.4-P3-03 (intent check advisory): implementation now matches spec intent — no spec deviation filed, this is an implementation note.

**Method note:** Given the scale (~90–102 files per the v6.6 audit), remediation was performed via a scripted, audited transformation: (1) reproduced the exact audit grep pattern from `contrast_audit_findings.md` to enumerate every candidate instance; (2) classified each match as icon (Lucide component tag, out of scope per ux_spec.md §5) or text (in scope) using the codebase's actual `lucide-react` import list (106 icon names) as the exclusion set; (3) applied the exact canonical class values from the locked design record — no new color decisions were made during execution. Every file touched was verified for JS/JSX syntax validity (Babel parse, 0 errors across all 159 touched-directory files) and the full e2e suite was run after each story.

---

## Frontend Testing Gate Check (LL-v3.1-EX-01)

| AC | Observable? | Evidence method | Reference |
|----|-------------|------------------|-----------|
| ST-01 AC-01 (colour replacement) | Yes — colour rendering | Playwright (computed style assertion) | SC-CTR-01a, SC-CTR-01b |
| ST-01 AC-02 (spot-checks) | No — documentation of computed ratios | Code review (values match ux_spec.md §3 exactly) | N/A |
| ST-02 AC-01 (paired classes) | Yes — colour rendering, theme-dependent | Playwright (computed style assertion, light theme) | SC-CTR-02a, SC-CTR-02b |
| ST-03 AC-01/AC-02 (token documentation) | No — documentation-only, no UI change | Code review (verbatim transcription confirmed) | N/A |

No AC in this EPIC is "code review only" for an observable/colour/rendering claim — all observable ACs have Playwright coverage. No backlog item required for deferred staging (BLG-GOV-19 autonomous class does not apply to this EPIC per BLG-GOV-135 detection rule — `src/components/**` and `src/pages/**` were modified — but the frontend testing gate itself is satisfied via Playwright, independent of the sign-off class).

---

## Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked (full e2e suite, 2 full runs)
- [ ] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, no new URL construction introduced by this EPIC
- Signed off by: [pending agent-mediated review — Director of Quality role, §5.3]
- Date:
- Comments:
