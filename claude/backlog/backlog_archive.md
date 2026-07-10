**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-09 (groom backlog post-ship closure 2026-07-08__release-v6.8 — 17 items archived)

# Backlog Archive — Momentum Trading Assistant

Permanent record of completed and killed backlog items retired from `claude/backlog/backlog.md`. Listed in retirement order, most recent first. Append-only — do not edit existing entries.

---

### BLG-FE-87 — App-wide secondary-text contrast failure against dark theme (default theme)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-07-08
**Shipped in:** v6.7 (ST-01, cycle: 2026-07-06__release-v6.7)
**Evidence:** docs/product/changelog.md#v6.7; claude/cycles/2026-07-06__release-v6.7/verification_report.md

### BLG-FE-87 — App-wide secondary-text contrast failure against dark theme (default theme)
**Priority:** P1 (High)
**Type:** Frontend / Accessibility
**Owner:** Head of UX & Design; Head of Engineering
**Source:** ST-01 (EPIC-01, v6.6) — colour contrast audit sweep (BLG-FE-82) — 2026-07-06
**Effort:** L (~2–3 days)
**Target:** ✅ COMPLETE — 2026-07-08 — cycle: 2026-07-06__release-v6.7 (ST-01)

**Problem**
The ST-01 contrast audit found `text-slate-500` (#64748b) used for small (text-xs/text-sm) secondary/label text in approximately 262 instances across ~90 files, rendered against the app's default dark-theme surface backgrounds (`bg-slate-950` #020617, `bg-slate-900` #0f172a, `bg-slate-800` #1e293b). Computed WCAG contrast ratios are 3.07–4.24:1, below the 4.5:1 required for normal-size text (the 3:1 "large text" allowance does not apply — all found usages are text-xs/text-sm). This is the app's default theme (confirmed in `src/Layout.js`), so the failure is visible today to the majority of users who have never toggled the theme. It is the same defect class already fixed once in `BLG-UX-01` (`AiDailyBriefing.js`, `text-slate-500`→`text-slate-300`) — that fix addressed one component; this finding shows it recurring at scale elsewhere.

**Scope**
- Systematic replacement of `text-slate-500` usages that fail contrast against their actual rendered dark-surface background, verified per-surface (some may sit on lighter card backgrounds where `text-slate-500` already passes)
- Contrast spot-checks recorded for a representative sample of affected pages

**Acceptance Criteria**
- All identified failing `text-slate-500` instances remediated to a WCAG-AA-passing shade (e.g. `text-slate-300`/`text-slate-400`) against their actual background
- No visual regression beyond the intended contrast fix
- Contrast verification recorded (manual or Playwright) for a representative sample

---

### BLG-FE-88 — App-wide secondary-text contrast failure against light theme (missing dark:/light: variants)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-07-08
**Shipped in:** v6.7 (ST-02, cycle: 2026-07-06__release-v6.7)
**Evidence:** docs/product/changelog.md#v6.7; claude/cycles/2026-07-06__release-v6.7/verification_report.md

### BLG-FE-88 — App-wide secondary-text contrast failure against light theme (missing dark:/light: variants)
**Priority:** P2 (Medium)
**Type:** Frontend / Accessibility
**Owner:** Head of UX & Design; Head of Engineering
**Source:** ST-01 (EPIC-01, v6.6) — colour contrast audit sweep (BLG-FE-82) — 2026-07-06
**Effort:** L (~3–4 days)
**Target:** ✅ COMPLETE — 2026-07-08 — cycle: 2026-07-06__release-v6.7 (ST-02)
**Depends on:** BLG-FE-87 (sequence after, to avoid rework — a dark-theme fix landing on `text-slate-400` does not solve light-theme contrast)

**Problem**
The app supports a user-toggleable light theme (`src/Layout.js`, `toggleTheme`, persisted to `localStorage`; default is dark). Tailwind's class-based dark mode (`darkMode: ["class"]`) requires an explicit `dark:` variant to change any style between themes — a bare class such as `text-slate-400` or `text-slate-500` applies identically in both. The audit found 502 bare `text-slate-400` instances and 262 bare `text-slate-500` instances (764 total, 102 files) with no `dark:text-*` companion class and no `isDark` conditional, meaning these were only ever visually verified against the dark theme. Computed contrast against light-theme surfaces (`bg-slate-100` #f1f5f9, `bg-slate-50` #f8fafc, `white`): `text-slate-400` = 2.3–2.6:1 (severe failure), `text-slate-500` = 4.3–4.8:1 (borderline, fails specifically against `bg-slate-100` at 4.34:1). Both existing precedent fixes (`BLG-UX-01`, `BLG-UX-02`) addressed only the dark-theme case and added no light-theme variant, confirming the light theme has never been contrast-audited in this codebase.

**Scope**
- For each affected secondary-text surface, add a paired `dark:text-*` / light-mode class combination (or `isDark` conditional, matching the pattern already used correctly in `src/Layout.js`) so both themes independently pass WCAG-AA
- Prioritise by page traffic/visibility

**Acceptance Criteria**
- Identified surfaces pass WCAG-AA in both light and dark theme
- Playwright coverage or a recorded manual light-theme QA pass for at least the highest-traffic pages

---

### BLG-FE-89 — Introduce a shared secondary-text design token or component to prevent recurring contrast regressions

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-07-08
**Shipped in:** v6.7 (ST-03, cycle: 2026-07-06__release-v6.7)
**Evidence:** docs/product/changelog.md#v6.7; claude/cycles/2026-07-06__release-v6.7/verification_report.md

### BLG-FE-89 — Introduce a shared secondary-text design token or component to prevent recurring contrast regressions
**Priority:** P3 (Low)
**Type:** Frontend / Design System
**Owner:** Head of UX & Design; Head of Engineering
**Source:** ST-01 (EPIC-01, v6.6) — colour contrast audit sweep (BLG-FE-82) — 2026-07-06
**Effort:** M (~1–2 days)
**Target:** ✅ COMPLETE — 2026-07-08 — cycle: 2026-07-06__release-v6.7 (ST-03)

**Problem**
Three separate contrast defects (`BLG-UX-01`, `BLG-UX-02`, and `BLG-FE-87`/`BLG-FE-88` above) all trace back to the same root cause: secondary/label text colour is chosen ad hoc per-component with no shared token or component enforcing a WCAG-AA-safe value per theme. A prior backlog item already proposed extracting a shared `AiDisclaimer` component for the two AI surfaces; this item generalises that idea app-wide.

**Scope**
- Define one or two Tailwind utility class pairs (or a small `<SecondaryText>` component) as the canonical secondary-text treatment, documented in the frontend design spec
- Net-new secondary-text usage going forward uses the token/component rather than raw slate/gray/zinc/neutral/stone classes

**Acceptance Criteria**
- Canonical secondary-text treatment defined and documented
- Frontend spec updated to reference it

---

### BLG-GOV-167 — Grant write-scope authority for .claude/skills/ maintenance

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-07-08
**Shipped in:** v6.7 (ST-04, cycle: 2026-07-06__release-v6.7)
**Evidence:** docs/product/changelog.md#v6.7; claude/cycles/2026-07-06__release-v6.7/verification_report.md

### BLG-GOV-167 — Grant write-scope authority for .claude/skills/ maintenance
**Priority:** P1 (High)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** Lifecycle Audit AUD-2026-07-06 (improvement AUD-2026-07-06-002) — 2026-07-06
**Effort:** M (~1–2 days)
**Target:** ✅ COMPLETE — 2026-07-08 — cycle: 2026-07-06__release-v6.7 (ST-04)

**Problem**
No governed routine's declared write scope includes `.claude/skills/` (`execution_prompt.md` §7 confirms this path is excluded). A deferred patch — adding a diff-verification step to `.claude/skills/commit-check/SKILL.md` so it checks `git add`'s target list against the intended file set before multi-file governance commits — has been carried across 3 consecutive cycles (v6.4 → v6.5 → v6.6) with no routine able to apply it. The v6.6 `lessons_learnt_cycle.md` confirms this now meets the automatic-escalation threshold in `lessons_learnt_prompt.md` §3.7, with no governed path to resolution.

**Scope**
- Add a provision to `shared_standards.md` §1 (Governance Stack) naming Head of Specs Team's authority to directly edit `.claude/skills/` files outside any governed routine's declared write scope
- Apply the carried `/commit-check` diff-verification patch under that authority
- Record the resolution in the next cycle's `lessons_learnt_cycle.md`

**Acceptance Criteria**
- `shared_standards.md` documents the `.claude/skills/` write-authority provision
- `.claude/skills/commit-check/SKILL.md` contains the diff-verification step (`git add` target list vs. intended file set) before multi-file governance commits
- 3-cycle carry-forward item closed in `prompt_change_log.md` or an equivalent record

---

### BLG-GOV-168 — Implement structural guard for 4 append-only governance logs

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-07-08
**Shipped in:** v6.7 (ST-05, cycle: 2026-07-06__release-v6.7)
**Evidence:** docs/product/changelog.md#v6.7; claude/cycles/2026-07-06__release-v6.7/verification_report.md

### BLG-GOV-168 — Implement structural guard for 4 append-only governance logs
**Priority:** P2 (Medium)
**Type:** Governance / Process — Lifecycle Reliability
**Owner:** Head of Specs Team
**Source:** Lifecycle Audit AUD-2026-07-06 (improvement AUD-2026-07-06-004) — 2026-07-06
**Effort:** M (~1–2 days)
**Target:** ✅ COMPLETE — 2026-07-08 — cycle: 2026-07-06__release-v6.7 (ST-05)

**Problem**
`shared_standards.md` §7 documents a "should apply the same pattern" pointer (added by AUD-2026-07-01-002) directing engines to give `escalations.md`, `execution_escalations.md`, `verification_escalations.md`, and `delegation_log.md` the same structural count-before/after guard that `decision_log.md` already has (`roadmap_prompt.md` STEP 9). No engine's actual write step for these 4 files was changed to perform the check — the fix was documentation-only and produced zero adoptions in the cycle since it was written, leaving 4 audit-trail files with no corruption guard.

**Scope**
- Extract `decision_log.md`'s structural pattern into a reusable named "Canonical Append-Only Verification Procedure" block in `shared_standards.md`
- Update the write step for each of the 4 affected engines (`release_planning_prompt.md` for `escalations.md`; `execution_prompt.md` for `execution_escalations.md`; `delivery_verification_prompt.md` for `verification_escalations.md`; the relevant engine for `delegation_log.md`) to invoke the procedure by reference

**Acceptance Criteria**
- `shared_standards.md` contains a single canonical, reusable verification procedure block
- All 4 affected engines' write steps reference and apply it (count-before, count-after, text-unchanged check, halt on failure)
- Confirmed via direct read of each engine's write step — not documentation alone

---

### BLG-GOV-169 — Require audit report commit in same session (audit.py SLA)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-07-08
**Shipped in:** v6.7 (ST-06, cycle: 2026-07-06__release-v6.7)
**Evidence:** docs/product/changelog.md#v6.7; claude/cycles/2026-07-06__release-v6.7/verification_report.md

### BLG-GOV-169 — Require audit report commit in same session (audit.py SLA)
**Priority:** P2 (Medium)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** Lifecycle Audit AUD-2026-07-06 (improvement AUD-2026-07-06-001) — 2026-07-06
**Effort:** XS (<1 hour)
**Target:** ✅ COMPLETE — 2026-07-08 — cycle: 2026-07-06__release-v6.7 (ST-06)

**Problem**
`claude/cycles/2026-06-26__release-v6.3/audit_report_AUD-2026-07-01.md` was produced but never committed to git — confirmed via `git status`/`git log` — until AUD-2026-07-06's own session retroactively committed it. `claude/audit.py`'s SLA block does not instruct the audit engine to commit its own output, unlike other governed routines whose write steps are explicitly paired with a commit instruction.

**Scope**
- Add an explicit "must be committed in the same session" line to `claude/audit.py`'s SLA block (per the PATCH already drafted in `audit_report_AUD-2026-07-06.md` improvement AUD-2026-07-06-001)

**Acceptance Criteria**
- `claude/audit.py` SLA block states the report must be committed same-session
- Verified: the config-block portion of this fix was already applied at AUD-2026-07-06 (2026-07-06); only the SLA-block text edit remains outstanding

---

### BLG-GOV-170 — Document sprint-status-line fix at Delivery Verification STEP 6

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-07-08
**Shipped in:** v6.7 (ST-07, cycle: 2026-07-06__release-v6.7)
**Evidence:** docs/product/changelog.md#v6.7; claude/cycles/2026-07-06__release-v6.7/verification_report.md

### BLG-GOV-170 — Document sprint-status-line fix at Delivery Verification STEP 6
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** Lifecycle Audit AUD-2026-07-06 (improvement AUD-2026-07-06-003) — 2026-07-06
**Effort:** XS (<1 hour)
**Target:** ✅ COMPLETE — 2026-07-08 — cycle: 2026-07-06__release-v6.7 (ST-07)

**Problem**
`docs/System_status_report.md`'s sprint status line reads `Sprint_Complete — pending verification` at Delivery Verification STEP 6 and is correctly, manually updated to `Verified — <date>` every cycle — but `delivery_verification_prompt.md` STEP 6's bullets never name this step. It has been logged as a "new" friction item for 4+ consecutive cycles (v6.3–v6.6) rather than recognised as expected, routine behaviour.

**Scope**
- Add a bullet to `delivery_verification_prompt.md` STEP 6 explicitly naming the status-line update from `pending verification` to `Verified — <date>`

**Acceptance Criteria**
- STEP 6 documents the status-line update as an expected step
- No further recurrence logged as a novel friction item in future `lessons_learnt_cycle.md` entries

---

### BLG-FE-40 — Red Flag Journal filter state persistence

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-07-06
**Shipped in:** v6.6 (ST-02, cycle: 2026-07-04__release-v6.6)
**Evidence:** docs/product/changelog.md#v6.6; claude/cycles/2026-07-04__release-v6.6/verification_report.md

### BLG-FE-40 — Red Flag Journal filter state persistence
**Status:** ✅ COMPLETE — 2026-07-06 — cycle: 2026-07-04__release-v6.6 (ST-02)
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Base44 Frontend; Head of UX & Design
**Source:** IDEA-base44-frontend-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Red Flag Journal in active use for ≥ 30 days post-v3.9 (confirm filter persistence adds value before implementing).

**Problem**
Red Flag Journal filter state (date range, severity, rule type) resets on page reload. Users who open the RFJ daily to review recent events must re-apply their filter preferences on each visit. localStorage persistence is a standard UX pattern that reduces friction on repeat visits.

**Scope**
- Persist RFJ filter state to localStorage (date range, event type, severity if/when added)
- Version the localStorage key to handle filter schema changes gracefully
- Restore filter state on page load; clear stale state if key version mismatch

**Acceptance Criteria**
- Filter state persists across page reloads
- Stale state (version mismatch) cleared gracefully without error
- Playwright test: set filter → reload page → verify filter state restored
- Gate condition verified by Product Owner before sprint planning

---

### BLG-FE-82 — Colour contrast audit sweep

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-07-06
**Shipped in:** v6.6 (ST-01, cycle: 2026-07-04__release-v6.6 — findings-only, Design Not Applicable)
**Evidence:** docs/product/changelog.md#v6.6; claude/cycles/2026-07-04__release-v6.6/contrast_audit_findings.md; claude/cycles/2026-07-04__release-v6.6/verification_report.md

### BLG-FE-82 — Colour contrast audit sweep
**Status:** ✅ COMPLETE — 2026-07-06 — cycle: 2026-07-04__release-v6.6 (ST-01; findings-only, Design Not Applicable — see contrast_audit_findings.md)
**Priority:** P2 (Medium)
**Type:** Frontend / Accessibility
**Owner:** Head of UX & Design
**Source:** IDEA-head-of-ux-20260702-02 (IW-20260702-01) — Promoted-Backlog; rebalance 2026-07-02__scheduled
**Provisional-Target:** TBD
**Effort:** S (~1 day)

**Problem**
BLG-UX-01/02 (v6.4) fixed WCAG-AA contrast failures on the two AI disclaimer surfaces specifically, found via ad hoc review. No systematic sweep has checked other secondary/disclaimer-style text surfaces in the app for the same class of issue.

**Scope**
- Apply the same WCAG-AA contrast review method used for BLG-UX-01/02 across all other secondary-text/disclaimer surfaces app-wide
- Produce a findings list; file follow-up backlog items for any additional failures found

**Acceptance Criteria**
- Contrast audit completed across all identified secondary-text surfaces
- Findings documented; any failures filed as follow-up backlog items
- Head of UX & Design sign-off

---

### BLG-QA-72 — Audit colliding backlog IDs in claude/backlog/backlog.md

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-07-06
**Shipped in:** v6.6 (ST-03, cycle: 2026-07-04__release-v6.6 — AC-03 partial, see BLG-QA-74)
**Evidence:** docs/product/changelog.md#v6.6; claude/cycles/2026-07-04__release-v6.6/verification_report.md

### BLG-QA-72 — Audit colliding backlog IDs in claude/backlog/backlog.md
**Status:** ✅ COMPLETE — 2026-07-06 — cycle: 2026-07-04__release-v6.6 (ST-03; AC-03 partial — see BLG-QA-74)
**Priority:** P2 (Medium)
**Type:** QA / Process Integrity
**Owner:** Director of Quality; Product Owner
**Source:** Technical-debt review session — 2026-07-03
**Effort:** S (~0.5d)
**Provisional-Target:** Unscheduled

**Problem**
`groom backlog`'s last run flagged "pre-existing duplicate IDs" as known-but-unresolved without naming them. A direct scan confirms real collisions: `BLG-OPS-13` and `BLG-FE-45` each appear 9 times, `BLG-OPS-17`/`BLG-GOV-88`/`BLG-FEAT-55` appear 8 times, `BLG-SPEC-46`/`BLG-QA-42` appear 7 times, plus a dozen more IDs appearing 4–6 times. It is unclear which are legitimate repeated citations in prose versus genuinely duplicate register entries.

**Scope**
- For each flagged ID, classify occurrences as (a) single canonical entry cited repeatedly in prose — no action, or (b) multiple distinct `### BLG-xxx` entries sharing one ID — needs renumbering/dedup
- Produce a resolution list for any true collisions found

**Acceptance Criteria**
- All IDs appearing ≥4 times classified as prose-citation vs. true collision
- Any true collisions renumbered with no ID reused across backlog.md/backlog_archive.md
- Next `groom backlog` health report shows 0 unresolved duplicate IDs

---

### BLG-QA-73 — database.py / _DB_STUB_FUNCTIONS manual-sync risk

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-07-06
**Shipped in:** v6.6 (ST-04, cycle: 2026-07-04__release-v6.6)
**Evidence:** docs/product/changelog.md#v6.6; claude/cycles/2026-07-04__release-v6.6/verification_report.md; tests/conftest.py

### BLG-QA-73 — database.py / _DB_STUB_FUNCTIONS manual-sync risk
**Status:** ✅ COMPLETE — 2026-07-06 — cycle: 2026-07-04__release-v6.6 (ST-04)
**Priority:** P3 (Low)
**Type:** QA / Test Infrastructure
**Owner:** QA & Testing Owner; Backend Engineering Patterns Owner
**Source:** Technical-debt review session — 2026-07-03
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Problem**
`backend/database.py` is a 2,529-line module. `tests/conftest.py` maintains a hand-written parallel list (`_DB_STUB_FUNCTIONS`, currently 37 entries) that must list every `database` function imported by `backend/services/position_service.py`, or CI fails with an opaque `ImportError` (this exact failure mode is already codified as a CLAUDE.md rule referencing `BLG-QA-20`). Nothing enforces the two lists stay in sync beyond the rule being followed by hand on every new import.

**Scope**
- Investigate whether `_DB_STUB_FUNCTIONS` can be derived automatically (e.g. introspecting `database.py`'s public functions, or generating the stub from an explicit `__all__`) instead of hand-maintained
- If feasible, implement the derivation and remove the manual-sync burden; if not feasible, document why and leave the existing CLAUDE.md rule as the control

**Acceptance Criteria**
- Decision recorded: automated derivation adopted, or documented as infeasible with reasoning
- If adopted: adding a new `database` import to `position_service.py` no longer requires a manual `conftest.py` edit, verified by a CI run
- CLAUDE.md rule updated or retired to match the outcome

---

### BLG-QA-74 — Duplicate archival records for 5 backlog items — Product Owner confirmation needed before dedup

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-07-06
**Shipped in:** v6.6 (PO decision recorded, no code/data change required, cycle: 2026-07-04__release-v6.6)
**Evidence:** claude/backlog/backlog.md (Product Owner decision recorded in-entry, 2026-07-06)

### BLG-QA-74 — Duplicate archival records for 5 backlog items — Product Owner confirmation needed before dedup
**Status:** ✅ COMPLETE — 2026-07-06 — cycle: 2026-07-04__release-v6.6 (PO decision: accept both archive copies as-is, no dedup)
**Priority:** P3 (Low)
**Type:** Governance / Data Hygiene
**Owner:** PMO Lead; Product Owner
**Source:** v6.6 ST-03 (BLG-QA-72) audit of colliding backlog IDs — 2026-07-06
**Effort:** XS (~0.5 hr)
**Provisional-Target:** ✅ COMPLETE — 2026-07-06 (decision recorded, no code/data change required)

**Product Owner decision (2026-07-06):** Accept both archive copies as-is — no dedup. Reviewed all 5 flagged pairs (BLG-FE-49, BLG-FEAT-38, BLG-OPS-28, BLG-OPS-31, BLG-OPS-37); both copies agree on content in every case (no data-integrity risk, just a historical artefact of two different `groom backlog` eras). At P3/XS sizing with zero product impact, the "superseded by" cross-reference cleanup isn't worth the churn. `groom backlog` STEP 4.5 will continue to correctly flag these 5 as duplicates on future runs — that is expected and acceptable; no further action is required against this item.

**Problem**
BLG-QA-72's audit of `### BLG-xxx` header collisions across `claude/backlog/backlog.md` and `claude/backlog/backlog_archive.md` found 5 IDs (BLG-FE-49, BLG-FEAT-38, BLG-OPS-28, BLG-OPS-31, BLG-OPS-37) each carrying **3** header entries in `backlog_archive.md`, not 2. In each case one pair is the compliant §6.1 stub+verbatim archive format (near the top of the file, most-recent-first ordering), and the third is an older-convention duplicate (embedded inline `✅ COMPLETE` marker, filed under the `## Groomed 2026-06-16` section further down) describing the **same** completed item — not a different item reusing the ID, so it was intentionally *not* renumbered under BLG-QA-72's AC-02 (renumbering is for true ID collisions between different items). `backlog_management_prompt.md` §6.2 requires Product Owner confirmation before archiving further copies of a duplicated item, and `backlog_archive.md`'s own header states "Append-only — do not edit existing entries" — so no autonomous deletion was performed. Until resolved, `groom backlog`'s STEP 4.5 ID Uniqueness Scan (v1.10, fixed this cycle to stop false-flagging compliant stub+verbatim pairs) will correctly continue flagging these 5 as genuine duplicates.

**Scope**
- Product Owner / PMO Lead reviews the 5 flagged pairs and decides: keep the modern stub+verbatim entry as canonical and append a one-line "superseded by" cross-reference note to the older entry, or accept both as an acceptable historical artefact (no-op)
- If dedup is approved: apply the agreed correction per the decision (append-only correction note, not a deletion, per the archive's own policy)

**Acceptance Criteria**
- Product Owner decision recorded (dedup vs. accept-as-is)
- If dedup approved: correction applied and `groom backlog` STEP 4.5 shows these 5 IDs no longer flagged
- If accepted as-is: no further action required; note recorded here for traceability

---

### BLG-GOV-157 — Lifecycle/prompt/state wording and consistency fixes

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-07-03
**Shipped in:** v6.5 (ST-01 per stage4_backlog_slice.md — see known BLG-ID/ST-item cross-reference note in verification_report.md §5(a), cycle: 2026-07-02__release-v6.5)
**Evidence:** docs/product/changelog.md#v6.5; claude/cycles/2026-07-02__release-v6.5/verification_report.md

Three governance wording/consistency findings from AUD-2026-07-01 closed: staging-only AC protocol ambiguity resolved, `FRICTION_LOAD` formula time-window clarified, state-file/audit-config open-item counts reconciled. `claude/audit.py` config block (PRIOR_AUDIT_ID/PRIOR_AUDIT_OPEN_ITEMS/PRIOR_SCORES/COMPLETED_CYCLES) synced to current audit state.

---

### BLG-GOV-158 — README.md document hygiene sweep

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-07-03
**Shipped in:** v6.5 (ST-02, cycle: 2026-07-02__release-v6.5)
**Evidence:** docs/product/changelog.md#v6.5; claude/cycles/2026-07-02__release-v6.5/verification_report.md

Four AUD-2026-07-01 document-hygiene findings closed: README §4 lists all 13 governed routines; §2 broken path corrected; staleness refreshed; `pmo_lead.md` header fields bolded. Verified pre-met on `main` from v6.4 EPIC-02 ST-05 work — no changes needed this sprint, no deviation.

---

### BLG-GOV-159 — OPERATIONAL_GUIDE/prompt version-sync drift

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-07-03
**Shipped in:** v6.5 (ST-03 per stage4_backlog_slice.md — see known BLG-ID/ST-item cross-reference note in verification_report.md §5(a), cycle: 2026-07-02__release-v6.5)
**Evidence:** docs/product/changelog.md#v6.5; claude/cycles/2026-07-02__release-v6.5/verification_report.md

Three AUD-2026-07-01 version-sync drift findings closed: OPERATIONAL_GUIDE.md header/§14 self-row/Change Log consistency verified; §14 Roadmap Rebalance Prompt row matches `roadmap_prompt.md`'s actual version; Metrics owner role name matches `team_charter.md`. Verified pre-met on `main` from the 2026-07-02__scheduled roadmap rebalance and v6.4 EPIC-02 ST-04 — no changes needed this sprint, no deviation.

---

### BLG-OPS-83 — Add v6.4 endpoint to api_performance_baseline.md

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-07-03
**Shipped in:** v6.5 (ST-04, cycle: 2026-07-02__release-v6.5)
**Evidence:** docs/product/changelog.md#v6.5; claude/cycles/2026-07-02__release-v6.5/verification_report.md; docs/ops/api_performance_baseline.md#24

`GET /strategy/benchmark/open-positions` (v6.4, BLG-FEAT-54) registered in `api_performance_baseline.md` §24 with a live 5-warm-sample production measurement (p50=524.5ms, p95=600.0ms) and a dynamic-2x regression threshold, following the BLG-OPS-82 staging-404-fallback precedent.

---

### TEST-GAP-EPIC-03-v64 — Playwright coverage for Strategy Benchmark Panel 0 (Open Positions) rendering

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-07-03
**Shipped in:** v6.5 (ST-05, cycle: 2026-07-02__release-v6.5)
**Evidence:** docs/product/changelog.md#v6.5; claude/cycles/2026-07-02__release-v6.5/verification_report.md; tests/e2e/strategy-benchmark.spec.js

SC-SB-05a/b, SC-SB-06a/b, SC-SB-07a added covering Panel 0 conditional rendering, the Market-filter-only interaction, and the API-error state — closing the code-review-only disposition carried from v6.4 EPIC-03 ST-08. All 13 tests in the spec file (6 new + 7 pre-existing) verified passing locally before commit.

---

### BLG-QA-61 — Review signals_scenarios.md against ST-01 signal sizing model changes

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-07-03
**Shipped in:** v6.5 (ST-06, cycle: 2026-07-02__release-v6.5)
**Evidence:** docs/product/changelog.md#v6.5; claude/cycles/2026-07-02__release-v6.5/verification_report.md; docs/testing/signals_scenarios.md

All scenarios reviewed against the risk-based sizing model (`size_position()`, replacing the removed cash-allocation formula) — zero stale references found; outcome committed as `signals_scenarios.md` v1.2→v1.3. Resolves a 3-cycle carry-forward (v6.2→v6.3→v6.4) and closes TSG-v60-01 (open since v6.2, escalated to Head of Specs Team at v6.4 closure).

---

### BLG-FE-46 — Claude thesis generation user feedback mechanism

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-07-03
**Shipped in:** v6.5 (ST-07, cycle: 2026-07-02__release-v6.5)
**Evidence:** docs/product/changelog.md#v6.5; claude/cycles/2026-07-02__release-v6.5/verification_report.md; tests/e2e/trade-plan.spec.js

Thumbs-up/down feedback control added to the Trade Plan form, gated on `isClaudeDraft`, persisted to `trade_plans.thesis_feedback` (DS-09). 6 new Playwright scenarios (SC-TP-23a–f), full regression of `trade-plan.spec.js` (29 tests) plus 3 adjacent spec files. Persistence-location choice is an implementation note, not a deviation — the ux_spec.md's `claude_audit_log` suggestion was explicitly non-binding.

---

### BLG-FEAT-41 — Claude thesis adoption rate metric

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-07-03
**Shipped in:** v6.5 (ST-08, cycle: 2026-07-02__release-v6.5)
**Evidence:** docs/product/changelog.md#v6.5; claude/cycles/2026-07-02__release-v6.5/verification_report.md; docs/specs/metrics_definitions.md#Thesis Adoption Rate

`thesis_adoption_rate` metric defined in `metrics_definitions.md`, joined against `gemini_audit_log.plan_id` (corrected from the sprint scope's literal `claude_audit_log` reference, which has no `plan_id` column). Metrics Definitions & Analytics Owner + Financial Reporting & Records Owner agent-mediated sign-off Approved.

---

### BLG-BE-40 — Signal generation reads deprecated `tickers` table instead of `ticker_universe`

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-07-02
**Shipped in:** v6.4 (ST-01, cycle: 2026-07-02__release-v6.4)
**Evidence:** docs/product/changelog.md#v6.4; claude/cycles/2026-07-02__release-v6.4/verification_report.md

P1 production correctness fast-track. `signal_service.py` switched from the deprecated `tickers` table to `services.ticker_universe_service.get_all_tickers(active_only=True)`. Verified via full backend test suite (551 passed, 0 failed); AC-02 (live add/deactivate confirmation) deferred to post-merge staging.

---

### BLG-SEC-01 — Sanitise context_opts.ticker before system prompt injection (POST /ai/chat)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-07-02
**Shipped in:** v6.4 (ST-02, cycle: 2026-07-02__release-v6.4)
**Evidence:** docs/product/changelog.md#v6.4; claude/cycles/2026-07-02__release-v6.4/verification_report.md

`context_opts.ticker` validated before insertion into the system prompt; strings with newlines/injection characters rejected with HTTP 422. A trailing-newline regex bypass (`re.match` matching before a trailing `\n`) was found and closed during Cybersecurity & Trust Lead sign-off by switching to `.fullmatch()`.

---

### BLG-SEC-02 — Validate ticker/market strings at signal write time (screener pipeline)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-07-02
**Shipped in:** v6.4 (ST-03, cycle: 2026-07-02__release-v6.4)
**Evidence:** docs/product/changelog.md#v6.4; claude/cycles/2026-07-02__release-v6.4/verification_report.md

Ticker/market strings validated at all 3 signal write paths (`create_signal`, `create_rebalance_exit_signal`, `update_signal`) — the sign-off review discovered `update_signal()` was a second, previously-unprotected write path and it was fixed in scope. AC-02 (manual live-DB review) deferred — BLG-SEC-07 filed; BLG-SEC-08 (unvalidated dict keys as SQL column names in `update_signal`) filed as an out-of-scope follow-up.

---

### BLG-GOV-150 — Fix governance version-sync drift (OPERATIONAL_GUIDE self-desync, stale §14 roadmap version, metrics owner role-name drift)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-07-02
**Shipped in:** v6.4 (ST-04, cycle: 2026-07-02__release-v6.4)
**Evidence:** docs/product/changelog.md#v6.4; claude/cycles/2026-07-02__release-v6.4/verification_report.md

OPERATIONAL_GUIDE.md header/§14 self-row/§14 Change Log top entry version-synced; §14 "Roadmap Engine Source" row corrected to match `roadmap_prompt.md`'s actual version; `metrics_definitions_analytics_owner.md` role name aligned with `team_charter.md` §3.3.

---

### BLG-GOV-151 — Document hygiene cleanup (README coverage/staleness/broken path, Class 6 header format, agent header bolding)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-07-02
**Shipped in:** v6.4 (ST-05, cycle: 2026-07-02__release-v6.4)
**Evidence:** docs/product/changelog.md#v6.4; claude/cycles/2026-07-02__release-v6.4/verification_report.md

`claude/README.md` §4 now lists all 13 governed routines; §2 broken lifecycle-guide path fixed; `Last Updated` refreshed. 3 governance prompts' `Last Updated` headers stripped to date-only per Class 6 spec. `pmo_lead.md` header fields bolded to match convention.

---

### BLG-GOV-152 — Close structural reliability gaps (append-only guard parity, DF-10 spec_references convention, staging AC protocol, amendment_lessons sunset contradiction)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-07-02
**Shipped in:** v6.4 (ST-06, cycle: 2026-07-02__release-v6.4)
**Evidence:** docs/product/changelog.md#v6.4; claude/cycles/2026-07-02__release-v6.4/verification_report.md

Append-only structural verification pattern added to `shared_standards.md` §7; `execution_prompt.md`'s `spec_references` policy gained a Case D (CI/infrastructure) row, closing FI-P4-01/DF-10; CLAUDE.md §2 gained the wording-only vs visual-rendering AC distinction, closing FI-P3-02; `amendment_cycle_prompt.md` §8/§9 `amendment_lessons.md` contradiction resolved; FI-P3-01 Base44 Playwright strict-mode advisory added. Resolves three 2-cycle-carried carry-forward items in a single sprint (LP-01 pattern, validated at post-ship closure).

---

### BLG-GOV-153 — Audit & governance process fixes (design gate bypass authority, run audit dry-run entry, friction_load formula wording, scored_initiatives naming)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-07-02
**Shipped in:** v6.4 (ST-07, cycle: 2026-07-02__release-v6.4)
**Evidence:** docs/product/changelog.md#v6.4; claude/cycles/2026-07-02__release-v6.4/verification_report.md

`team_charter.md` new §5.7 codifies the design gate bypass dual-authority rule; `shared_standards.md` §13 dry-run table gained a `run audit` row; `claude/audit.py`'s FRICTION_LOAD formula wording clarified ("since PRIOR_AUDIT_ID"); `scored_initiatives.md` documented as intentionally current-cycle-only and an orphaned dated copy removed.

---

### BLG-FEAT-54 — Add Open Positions panel to Strategy Benchmark page

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-07-02
**Shipped in:** v6.4 (ST-08, cycle: 2026-07-02__release-v6.4)
**Evidence:** docs/product/changelog.md#v6.4; claude/cycles/2026-07-02__release-v6.4/verification_report.md

Skill-Silo pull-forward feature. New `backtest_open_positions` table (full-replace nightly semantics), `GET /strategy/benchmark/open-positions` endpoint, Panel 0 on `StrategyBenchmark.js` showing a one-line unrealized-P&L summary plus a per-position table. AC-01 (Panel 0 rendering) cleared by code review only this sprint — `TEST-GAP-EPIC-03-v64` filed for Playwright coverage before the PR opened.

---

### BLG-UX-01 — Improve AI daily briefing disclaimer text contrast

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-07-02
**Shipped in:** v6.4 (ST-09, cycle: 2026-07-02__release-v6.4)
**Evidence:** docs/product/changelog.md#v6.4; claude/cycles/2026-07-02__release-v6.4/verification_report.md

`AiDailyBriefing.js` disclaimer text colour changed `text-slate-500`→`text-slate-300`, meeting WCAG AA ≥4.5:1 contrast. Head of UX & Design sign-off cleared agent-mediated, no findings.

---

### BLG-UX-02 — Improve AI chat widget footer disclaimer contrast and add test coverage

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-07-02
**Shipped in:** v6.4 (ST-10, cycle: 2026-07-02__release-v6.4)
**Evidence:** docs/product/changelog.md#v6.4; claude/cycles/2026-07-02__release-v6.4/verification_report.md

`AiChatWidget.js` footer disclaimer colour changed `text-slate-600`→`text-slate-400`, meeting WCAG AA; `data-testid="ai-chat-advisory-footer"` added; new Playwright assertion (SC-AC-06) added to `epic02-v62-ai-briefing-chat.spec.js`. Head of UX & Design sign-off cleared agent-mediated, no findings.

---

### BLG-OPS-82 — Add v6.3 endpoints to api_performance_baseline.md

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-07-02
**Shipped in:** v6.4 (ST-11, cycle: 2026-07-02__release-v6.4)
**Evidence:** docs/product/changelog.md#v6.4; claude/cycles/2026-07-02__release-v6.4/verification_report.md

Three v6.3 GET endpoints (`/strategy/benchmark/summary`, `/strategy/benchmark/trades`, `/health/scheduler`) registered in `api_performance_baseline.md` with measured p50/p95, measured against production after staging returned 404. Regression thresholds documented per the §22.2/§22.3 dynamic-2x pattern. Infrastructure & Operations Owner sign-off cleared agent-mediated after 1 retry (2 citation-accuracy findings applied). `BLG-OPS-83` filed for the new v6.4 Panel 0 endpoint.

---

### TEST-GAP-EPIC-01 — Playwright coverage for ST-01 observable UI ACs (AI journal summary error states)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-07-02
**Shipped in:** v6.4 (ST-12, cycle: 2026-07-02__release-v6.4)
**Evidence:** docs/product/changelog.md#v6.4; claude/cycles/2026-07-02__release-v6.4/verification_report.md

SC-TH-AI-01/02/03 added to `tests/e2e/trade-history-ai-journal-summary.spec.js` covering server-error and network-error message rendering; `data-testid` selectors added to the Trade History AI Journal Summary component (none existed previously).

---

### TEST-GAP-EPIC-03 — Playwright scenario coverage for Strategy Benchmark page

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-07-02
**Shipped in:** v6.4 (ST-13, cycle: 2026-07-02__release-v6.4)
**Evidence:** docs/product/changelog.md#v6.4; claude/cycles/2026-07-02__release-v6.4/verification_report.md

SC-SB-01–04 added to `tests/e2e/strategy-benchmark.spec.js` covering nav accessibility, simultaneous filters, Panel 1 placeholder, and toggle modes/badge colours (scoped to Panels 1/3 per sprint_backlog.md; Panel 0 tracked separately as TSG-v64-01/TEST-GAP-EPIC-03-v64). Two CI-caught defects (nav route stubbing, collapsed Analytics nav group) fixed pre-merge — all 24 CI checks green.

---

### BLG-FEAT-53 — Strategy Benchmark page: compare live trades against backtest

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-06-30
**Shipped in:** v6.3 (ST-11, cycle: 2026-06-26__release-v6.3)
**Evidence:** docs/product/changelog.md — v6.3; claude/cycles/2026-06-26__release-v6.3/verification_report.md

Two new DB tables (backtest_trades, backtest_yearly_performance), POST /strategy/benchmark/import, GET /strategy/benchmark/summary, GET /strategy/benchmark/trades, StrategyBenchmark.js frontend page with three panels, sticky filter bar, and toggle modes. import_backtest.py companion script. All 8 ACs delivered.

---

### BLG-FE-80 — Morning briefing progressive disclosure (expand/collapse sections)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-06-30
**Shipped in:** v6.3 (ST-12, cycle: 2026-06-26__release-v6.3)
**Evidence:** docs/product/changelog.md — v6.3; claude/cycles/2026-06-26__release-v6.3/verification_report.md

Expand/collapse toggle per section in AiDailyBriefing.js (market context, signals, chat prompt). Default all expanded. localStorage persistence with versioned key. Playwright SC-PD-05 coverage.

---

### BLG-FE-79 — Fix R-multiple not displaying on Reflection page

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-06-30
**Shipped in:** v6.3 (ST-02, cycle: 2026-06-26__release-v6.3)
**Evidence:** docs/product/changelog.md — v6.3; claude/cycles/2026-06-26__release-v6.3/verification_report.md

Fixed R-multiple field mapping (backend service or frontend display logic). R-multiple rendered as numeric value for all closed trades; trades with insufficient data show "N/A". No regression to other Reflection page columns.

---

### BLG-OPS-81 — AI endpoint per-endpoint rate limiting hardening

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-06-30
**Shipped in:** v6.3 (ST-03, cycle: 2026-06-26__release-v6.3)
**Evidence:** docs/product/changelog.md — v6.3; claude/cycles/2026-06-26__release-v6.3/verification_report.md

Per-endpoint rate limits: POST /ai/daily-briefing (~10 req/min/IP), POST /ai/chat (~30 req/min/IP). 429 Too Many Requests with Retry-After header. Rate limits documented in openapi.yaml and api_contracts.

---

### BLG-OPS-80 — Render deployment rollback procedure documentation

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-06-30
**Shipped in:** v6.3 (ST-15, cycle: 2026-06-26__release-v6.3)
**Evidence:** docs/product/changelog.md — v6.3; claude/cycles/2026-06-26__release-v6.3/verification_report.md

Render deployment rollback procedure documented in docs/operations/ covering rollback steps, decision criteria (severity thresholds), and verification steps.

---

### BLG-OPS-79 — Background scheduler health monitoring endpoint

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-06-30
**Shipped in:** v6.3 (ST-13, cycle: 2026-06-26__release-v6.3)
**Evidence:** docs/product/changelog.md — v6.3; claude/cycles/2026-06-26__release-v6.3/verification_report.md

GET /health/scheduler endpoint returning last-run timestamps per nightly computation job type, status (success/failure), and error details. Registered in backend/routers/test.py and openapi.yaml. Architecture review documented.

---

### BLG-OPS-78 — Measure live latency for POST /ai/daily-briefing and POST /ai/chat

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-06-30
**Shipped in:** v6.3 (ST-14, cycle: 2026-06-26__release-v6.3)
**Evidence:** docs/product/changelog.md — v6.3; claude/cycles/2026-06-26__release-v6.3/verification_report.md

Live p50/p95 measurements recorded for both AI endpoints using §19 methodology. api_performance_baseline.md §22.3 populated with actual measurements and regression thresholds.

---

### BLG-QA-68 — §13 boundary test suite for AI advisory endpoints

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-06-30
**Shipped in:** v6.3 (ST-10, cycle: 2026-06-26__release-v6.3)
**Evidence:** docs/product/changelog.md — v6.3; claude/cycles/2026-06-26__release-v6.3/verification_report.md

§13 boundary test scenario document filed as docs/specs/qa/ai_s13_boundary_test_suite.md. Covers all current AI endpoints: advisory-only language, no automated-action fields, disclaimer visibility, no specific instrument recommendations. AI Compliance Officer and QA & Testing Owner sign-off.

---

### BLG-QA-67 — AI chat response schema validation tests

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-06-30
**Shipped in:** v6.3 (ST-09, cycle: 2026-06-26__release-v6.3)
**Evidence:** docs/product/changelog.md — v6.3; claude/cycles/2026-06-26__release-v6.3/verification_report.md

POST /ai/chat response schema validation tests and advisory-only language constraint tests registered in backend/routers/test.py. CI-passing.

---

### BLG-QA-66 — Strategy signal regression test specification

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-06-30
**Shipped in:** v6.3 (ST-08, cycle: 2026-06-26__release-v6.3)
**Evidence:** docs/product/changelog.md — v6.3; claude/cycles/2026-06-26__release-v6.3/verification_report.md

Specification document docs/specs/qa/strategy_signal_regression_spec.md. Covers scenario requirements for BLG-QA-65 fixture dataset, expected output formats and tolerances, and fixture maintenance procedure. Director of Quality and QA Lead sign-off.

---

### BLG-QA-65 — Nightly stop computation CI simulation tests

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-06-30
**Shipped in:** v6.3 (ST-07, cycle: 2026-06-26__release-v6.3)
**Evidence:** docs/product/changelog.md — v6.3; claude/cycles/2026-06-26__release-v6.3/verification_report.md

Fixture-based CI simulation tests for trailing stop computation, rebalance exit detection, and inverse-vol sizing. All 5 ACs delivered; tests run in CI on changes to affected services.

---

### BLG-GOV-148 — API contract review checklist for AI advisory endpoints

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-06-30
**Shipped in:** v6.3 (ST-06, cycle: 2026-06-26__release-v6.3)
**Evidence:** docs/product/changelog.md — v6.3; claude/cycles/2026-06-26__release-v6.3/verification_report.md

§13 boundary confirmation checklist for AI advisory endpoint contracts filed in docs/specs/api_contracts/. Applied retroactively to v6.2 AI endpoint contracts. API Contracts Owner and Head of Specs Team sign-off.

---

### BLG-GOV-147 — AI feature advisory disclaimer visibility assessment

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-06-30
**Shipped in:** v6.3 (ST-05, cycle: 2026-06-26__release-v6.3)
**Evidence:** docs/product/changelog.md — v6.3; claude/cycles/2026-06-26__release-v6.3/verification_report.md

Visual assessment of AI daily briefing and AI chat disclaimer: font size, colour contrast, position. Disclaimer confirmed prominent on first render without scrolling. Remediation items (BLG-UX-01, BLG-UX-02) filed for contrast improvements. AI Compliance Officer and Head of UX & Design sign-off.

---

### BLG-GOV-146 — AI response injection risk assessment

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-06-30
**Shipped in:** v6.3 (ST-04, cycle: 2026-06-26__release-v6.3)
**Evidence:** docs/product/changelog.md — v6.3; claude/cycles/2026-06-26__release-v6.3/verification_report.md

Threat model document covering all external data inputs to the AI prompt construction pipeline (POST /ai/daily-briefing, POST /ai/chat). Risk classification per input: accepted/mitigated/open. BLG-SEC-01 and BLG-SEC-02 filed as open risk remediation items. Cybersecurity & Trust Lead and AI Compliance Officer sign-off.

---

### BLG-BE-39 — Fix AI journal summary on Trade History tab

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-06-30
**Shipped in:** v6.3 (ST-01, cycle: 2026-06-26__release-v6.3)
**Evidence:** docs/product/changelog.md — v6.3; claude/cycles/2026-06-26__release-v6.3/verification_report.md

Diagnosed and fixed the AI journal summary endpoint failure (ai_service.py). AI journal summary generates successfully for trades with journal notes on Trade History tab. Error states surfaced clearly. No regression to other ai_service.py functionality.

---

### BLG-FEAT-46 — Add nightly trailing stop computation for open positions

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-06-25
**Shipped in:** v6.2 (ST-01/ST-02, cycle: 2026-06-24__release-v6.2)
**Evidence:** docs/product/changelog.md — v6.2; claude/cycles/2026-06-24__release-v6.2/verification_report.md

**Type:** Product Feature / In-Trade Risk Management
**Owner:** Product Owner
**Source:** User request — production_strategy.py gap analysis — 2026-06-23
**Effort:** M (~2 days)

Nightly trailing stop computation for open positions using profit-lock ratchet logic (INITIAL_ATR_MULT=5, PROFIT_ATR_MULT=2, ATR_PERIOD=14). Stop level stored per position; breach badge displayed when current_price ≤ trailing_stop. Stop ratchet is enforced (stop only moves up).

---

### BLG-FEAT-47 — Add month-end rebalance exit signal generation

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-06-25
**Shipped in:** v6.2 (ST-03, cycle: 2026-06-24__release-v6.2)
**Evidence:** docs/product/changelog.md — v6.2; claude/cycles/2026-06-24__release-v6.2/verification_report.md

**Type:** Product Feature / In-Trade Risk Management
**Owner:** Product Owner
**Source:** User request — production_strategy.py gap analysis — 2026-06-23
**Effort:** M (~1.5 days)

Month-end rebalance exit signal generation: exit_rebalance status for positions dropping out of top-5 momentum ranking on last trading day of each month. Teal badge in UI, distinct from stop exits and risk-off exits.

---

### BLG-FEAT-48 — Implement inverse-volatility position sizing for signal-driven entries

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-06-25
**Shipped in:** v6.2 (ST-04, cycle: 2026-06-24__release-v6.2)
**Evidence:** docs/product/changelog.md — v6.2; claude/cycles/2026-06-24__release-v6.2/verification_report.md

**Type:** Product Feature / Signal Generation
**Owner:** Product Owner
**Source:** User request — production_strategy.py gap analysis — 2026-06-23
**Effort:** M (~2 days)

Inverse-volatility position sizing for signal-driven entries: weight_i = (1/ATR_i) / Σ(1/ATR_j), constrained to [5%–20%] of available cash, re-normalised. Replaces fixed-risk sizing path for signal-driven entries; manual entries unchanged.

---

### BLG-FEAT-49 — Add risk-off exit alerts for existing positions

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-06-25
**Shipped in:** v6.2 (ST-05, cycle: 2026-06-24__release-v6.2)
**Evidence:** docs/product/changelog.md — v6.2; claude/cycles/2026-06-24__release-v6.2/verification_report.md

**Type:** Product Feature / In-Trade Risk Management
**Owner:** Product Owner
**Source:** User request — production_strategy.py gap analysis — 2026-06-23
**Effort:** S (~1 day)

Risk-off exit alerts for existing positions: nightly regime check, SPY/FTSE MA200, per-market isolation (US/UK). risk_off_exit alert per position when regime flips; clears automatically when regime returns to risk-on.

---

### BLG-FEAT-50 — Build AI daily briefing endpoint and dashboard panel

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-06-25
**Shipped in:** v6.2 (ST-06/ST-07, cycle: 2026-06-24__release-v6.2)
**Evidence:** docs/product/changelog.md — v6.2; claude/cycles/2026-06-24__release-v6.2/verification_report.md

**Type:** Product Feature / AI Intelligence
**Owner:** Product Owner
**Source:** User request — production_strategy.py gap analysis — 2026-06-23
**Effort:** M (~2 days)

POST /ai/daily-briefing: assembles portfolio/signals/trailing-stops/regime/rebalance context, calls claude-sonnet-4-6, returns structured action plan. AiDailyBriefing.js dashboard card with summary, action list, Regenerate button, timestamp. Advisory-only §13 SRB-v1.7 PASS.

---

### BLG-FEAT-51 — Build conversational AI trade advisor

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-06-25
**Shipped in:** v6.2 (ST-08/ST-09, cycle: 2026-06-24__release-v6.2)
**Evidence:** docs/product/changelog.md — v6.2; claude/cycles/2026-06-24__release-v6.2/verification_report.md

**Type:** Product Feature / AI Intelligence
**Owner:** Product Owner
**Source:** User request — production_strategy.py gap analysis — 2026-06-23
**Effort:** M (~2 days)

POST /ai/chat: stateless conversational advisor, accepts {question, context?}, loads full portfolio + signal state, calls claude-sonnet-4-6. AiChatWidget.js on Positions page (canonical) and Signals page (stretch). Advisory-only §13 SRB-v1.7 PASS.

---

### BLG-GOV-135 — execution_prompt: hard gate on autonomous class sign-off for EPICs with frontend-visible changes

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-06-25
**Shipped in:** v6.2 (ST-10, cycle: 2026-06-24__release-v6.2)
**Evidence:** docs/product/changelog.md — v6.2; claude/cycles/2026-06-24__release-v6.2/verification_report.md

**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Delivery verification 2026-06-22__release-v6.1 — Phase 4 lessons learnt friction item 1
**Effort:** XS (<1 hour)

execution_prompt.md v3.47→v3.48: criterion 3 updated — autonomous class blocked when any story creates/modifies src/components/** or src/pages/**. qa_evidence_template.md criterion 3 advisory updated with detection rule cross-reference.

---

### BLG-GOV-136 — execution_prompt STEP 12: validate test_scenarios paths reference current cycle

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-06-25
**Shipped in:** v6.2 (ST-11, cycle: 2026-06-24__release-v6.2)
**Evidence:** docs/product/changelog.md — v6.2; claude/cycles/2026-06-24__release-v6.2/verification_report.md

**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Delivery verification 2026-06-22__release-v6.1 — Phase 4 lessons learnt friction item 2
**Effort:** XS (<1 hour)

execution_prompt.md STEP 0 instruction 6: advisory added — test_scenarios must reference tests/ or tests/e2e/ paths only; docs/testing/ paths flagged as evidence artefacts not scenario files.

---

### BLG-QA-62 — Playwright spec auto-registration via glob pattern in playwright.yml

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-06-25
**Shipped in:** v6.2 (ST-13, cycle: 2026-06-24__release-v6.2)
**Evidence:** docs/product/changelog.md — v6.2; claude/cycles/2026-06-24__release-v6.2/verification_report.md

**Type:** QA / Test Coverage
**Owner:** Director of Quality; Head of Frontend Engineering
**Source:** IW-20260622-01 — Promoted-Backlog; rebalance 2026-06-22__scheduled
**Effort:** S (<0.5 day)

Replaced explicit spec file list in playwright.yml with npx playwright test (auto-discovery via playwright.config.js testDir). 12 pre-existing dark specs excluded via testIgnore (BLG-QA-64 filed). All 27 old-explicit-list specs pass in CI; 9 additional dark specs now run and pass.

---

### BLG-OPS-75 — Add GET /portfolio/sector-weights and GET /trade-plans/setup-quality-score to api_performance_baseline.md

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-06-25
**Shipped in:** v6.2 (ST-12, cycle: 2026-06-24__release-v6.2)
**Evidence:** docs/product/changelog.md — v6.2; claude/cycles/2026-06-24__release-v6.2/verification_report.md

**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** Post-ship closure 2026-06-22__release-v6.1 — endpoint drift advisory
**Effort:** XS (<1 hour)

api_performance_baseline.md v2.5→v2.6 §21: GET /portfolio/sector-weights p50=287ms p95=356ms; GET /trade-plans/setup-quality-score p50=464ms p95=516ms. 20 live production samples each. ⚠ p95=516ms for setup-quality-score noted, within acceptable range.

---

### BLG-GOV-133 — Sprint planning: enforce hard gate on design_gate_status at STEP -1 preflight

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-06-23
**Shipped in:** v6.1 (ST-02, cycle: 2026-06-22__release-v6.1)
**Evidence:** docs/product/changelog.md — v6.1; claude/cycles/2026-06-22__release-v6.1/verification_report.md

**Type:** Governance Process
**Owner:** Head of Specs Team; PMO Lead
**Source:** v6.0 design gate — sprint planning proceeded from Release_Planning_Complete with design_gate_status = not_started and no bypass record — 2026-06-19
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.1
Add or strengthen STEP -1.3 in sprint_planning_prompt.md: when entering from Release_Planning_Complete, check design_gate_status; hard gate when design_gate_required=true and status≠Passed and no bypass authority/reason → halt. Bypass path and not-required path documented. Bump sprint_planning_prompt.md version; update §14 OPERATIONAL_GUIDE.md and prompt_change_log.md.

---

### BLG-GOV-132 — Release planning: emit explicit Design Gate Required flag for UI-facing scope

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-06-23
**Shipped in:** v6.1 (ST-01, cycle: 2026-06-22__release-v6.1)
**Evidence:** docs/product/changelog.md — v6.1; claude/cycles/2026-06-22__release-v6.1/verification_report.md

**Type:** Governance Process
**Owner:** Head of Specs Team; PMO Lead
**Source:** v6.0 design gate — design gate was skipped because release planning emitted no explicit "design gate required" signal — 2026-06-19
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.1
STEP 4 of release_planning_prompt.md: scan backlog slice items for UI-facing delegation class; classify cycle as design gate required or not required; set design_gate_required in state.json and .claude_current_state.json; emit advisory; include in cycle_summary.md header. Bump version; update §14 OPERATIONAL_GUIDE.md and prompt_change_log.md.

---

### BLG-GOV-131 — Governance overhead ceiling metric and accountability mechanism

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-06-23
**Shipped in:** v6.1 (ST-03, cycle: 2026-06-22__release-v6.1)
**Evidence:** docs/product/changelog.md — v6.1; claude/cycles/2026-06-22__release-v6.1/verification_report.md

**Type:** Governance / Process
**Owner:** PMO Lead; Challenger
**Source:** IDEA-challenger-20260619-02 — Promoted-Backlog rebalance 2026-06-19__scheduled (DL-049)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v6.1
Define G+D+P% governance overhead metric (rolling 5-cycle window); define alert threshold (initial proposal 60%); proposal doc produced at docs/product/decisions/gov_overhead_ceiling_proposal_v6.1.md. 5-cycle baseline established at 86.0%. Requires Head of Specs Team sign-off before implementation as prompt amendment.

---

### BLG-QA-60 — Register morning-briefing.spec.js and screener-quality.spec.js in playwright.yml CI workflow

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-06-23
**Shipped in:** v6.1 (ST-04, cycle: 2026-06-22__release-v6.1)
**Evidence:** docs/product/changelog.md — v6.1; claude/cycles/2026-06-22__release-v6.1/verification_report.md

**Type:** QA / Test Automation
**Owner:** Director of Quality; Head of Engineering
**Source:** EPIC-04 sprint execution 2026-06-22 — Playwright E2E gate failure revealed spec files not registered in CI
**Effort:** XS (<1 hour)
**Provisional-Target:** v6.1
Added tests/e2e/morning-briefing.spec.js and tests/e2e/screener-quality.spec.js to playwright.yml explicit test list; spec inventory comment updated to reflect 25 total spec files; both specs confirmed passing in CI.

---

### BLG-OPS-73 — Add PATCH /trades/{trade_id}/costs to api_performance_baseline.md

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-06-23
**Shipped in:** v6.1 (ST-05, cycle: 2026-06-22__release-v6.1)
**Evidence:** docs/product/changelog.md — v6.1; claude/cycles/2026-06-22__release-v6.1/verification_report.md

**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** Post-ship closure 2026-06-19__release-v6.0 — endpoint coverage drift check detected 1 new endpoint in openapi.yaml absent from api_performance_baseline.md
**Effort:** XS (<1 hour)
**Provisional-Target:** v6.1
PATCH /trades/{id}/costs baseline entry added to docs/ops/api_performance_baseline.md; api_performance_baseline.md bumped v2.4→v2.5.

---

### BLG-FE-76 — Portfolio sector heat-map visualization

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-06-23
**Shipped in:** v6.1 (ST-06, cycle: 2026-06-22__release-v6.1)
**Evidence:** docs/product/changelog.md — v6.1; claude/cycles/2026-06-22__release-v6.1/verification_report.md

**Type:** Frontend / UX / Data Visualisation
**Owner:** Product Owner; Frontend Specs & UX Documentation Owner
**Source:** IDEA-product-owner-20260619-01 — Promoted-Backlog rebalance 2026-06-19__scheduled (DL-050)
**Effort:** M (~2–3 days)
**Provisional-Target:** v6.1
SectorHeatMap.js component on RiskDashboard page; GET /portfolio/sector-weights backend endpoint; percentage bars by sector; amber alert ≥40% concentration; SC-SHM-01..04 Playwright coverage (4 scenarios).

---

### BLG-FE-78 — Trade gate proximity indicator on dashboard

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-06-23
**Shipped in:** v6.1 (ST-07, cycle: 2026-06-22__release-v6.1)
**Evidence:** docs/product/changelog.md — v6.1; claude/cycles/2026-06-22__release-v6.1/verification_report.md

**Type:** Frontend / UX
**Owner:** Head of Frontend Engineering
**Source:** IW-20260622-01 (IDEA-product-owner-20260622-01) — Promoted-Backlog STEP 4; DL-054 (Challenger PVC outcome); rebalance 2026-06-22__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** v6.1
GateProgressStrip.js component on DashboardHome; reads from GET /portfolio/gate-metrics; shows {N}/20 trades progress; "Gate cleared ✓" state; SC-GP-01..04 Playwright coverage (4 scenarios).

---

### BLG-FEAT-25 — PT-04 Setup Quality Score (backend + frontend)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-06-23
**Shipped in:** v6.1 (ST-08 backend + ST-09 frontend, cycle: 2026-06-22__release-v6.1)
**Evidence:** docs/product/changelog.md — v6.1; claude/cycles/2026-06-22__release-v6.1/verification_report.md

**Type:** Product Feature / Analytics
**Owner:** Head of Backend Engineering; Metrics & Analytics Owner; Head of UX & Design
**Source:** Arc 2 roadmap — deferred from v3.8 (ST-04/ST-05, EPIC-02) — gate not met 2026-05-19: < 20 closed trades.
**Effort:** L (~2–4 days, backend + frontend)
**Provisional-Target:** v4.0+ (gate-conditional — gate cleared at v6.1 sprint planning: 15 trades confirmed 2026-06-22; conditional classification accepted)
**Gate:** PO confirmed 15 closed trades at v6.1 sprint planning (2026-06-22); conditional gate accepted; EPIC-04 executed and delivered.
Gate history: 6 trades (v4.6), 6 trades (v5.3), 13 trades (v5.6), 15 trades (v6.1 release planning), gate cleared conditional at sprint planning.
Backend: GET /trade-plans/setup-quality-score endpoint; gate enforcement (<20 trades returns gate_not_met); 3 unit test cases; registered in test.py and openapi.yaml.
Frontend: SetupQualityScorePanel in Research.js and TradePlan.js; score badge (0–100); "Insufficient trade history" gate-not-met state; SC-SQS-01..06 Playwright coverage (6 scenarios).

---

### BLG-GOV-62 — SI-04 §13 formal pre-assessment

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-06-01
**Shipped in:** v4.7
**Evidence:** docs/product/changelog.md#v47; claude/cycles/2026-05-31__release-v4.7/verification_report.md

### BLG-GOV-62 — SI-04 §13 formal pre-assessment
**Priority:** P1 (High)
**Type:** Governance / §13 Compliance
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled
**Completed:** ST-01, EPIC-01, cycle 2026-05-31__release-v4.7 — si04_section13_preassessment.md produced; determination: PASS; 6 binding conditions; Strategy Rules & System Intent Owner sign-off

---

### BLG-OPS-45 — red_flag_events severity field staging verification (v4.6 delivery)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-06-01
**Shipped in:** v4.7
**Evidence:** docs/product/changelog.md#v47; claude/cycles/2026-05-31__release-v4.7/verification_report.md

### BLG-OPS-45 — red_flag_events severity field staging verification (v4.6 delivery)
**Priority:** P3 (Low)
**Type:** Operations / Staging Verification
**Owner:** Infrastructure & Operations Owner; Data Model & Domain Schema Owner
**Source:** v4.6 delivery verification — ST-09 AC-01/02/03 deferred to Phase 4 (staging-only ACs); AC-08 pending
**Effort:** XS (~0.5 hr)
**Provisional-Target:** v4.7
**Completed:** ST-06, EPIC-03, cycle 2026-05-31__release-v4.7 — severity_field_staging_verification.md produced; severity column confirmed; assignment rule verified; backfill confirmed zero nulls; Infrastructure & Operations Owner + Data Model & Domain Schema Owner sign-off; AC-08 cleared

---

### BLG-OPS-44 — DS-07 migration staging verification (v4.6 delivery)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-06-01
**Shipped in:** v4.7
**Evidence:** docs/product/changelog.md#v47; claude/cycles/2026-05-31__release-v4.7/verification_report.md

### BLG-OPS-44 — DS-07 migration staging verification (v4.6 delivery)
**Priority:** P3 (Low)
**Type:** Operations / Staging Verification
**Owner:** Infrastructure & Operations Owner; Data Model & Domain Schema Owner
**Source:** v4.6 delivery verification — ST-01 AC-05 deferred to Phase 4 (staging-only AC)
**Effort:** XS (~0.5 hr)
**Provisional-Target:** v4.7
**Completed:** ST-05, EPIC-03, cycle 2026-05-31__release-v4.7 — ds07_migration_staging_verification.md produced; all 5 SI-02 columns confirmed; 3 indexes confirmed; Infrastructure & Operations Owner + Data Model & Domain Schema Owner sign-off

---

### BLG-OPS-37 — Anthropic API tier cost assessment

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-06-01
**Shipped in:** v4.7
**Evidence:** docs/product/changelog.md#v47; claude/cycles/2026-05-31__release-v4.7/verification_report.md

### BLG-OPS-37 — Anthropic API tier cost assessment
**Priority:** P2 (Medium)
**Type:** Operations / Cost Planning
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260527-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Completed:** ST-08, EPIC-04, cycle 2026-05-31__release-v4.7 — anthropic_api_tier_assessment.md produced; no upgrade required; upgrade threshold defined at $5/month; FinOps & Resource Architect sign-off

---

### BLG-OPS-31 — Render application log retention policy

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-06-01
**Shipped in:** v4.7
**Evidence:** docs/product/changelog.md#v47; claude/cycles/2026-05-31__release-v4.7/verification_report.md

### BLG-OPS-31 — Render application log retention policy
**Priority:** P2 (Medium)
**Type:** Operations / Data Management
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Completed:** ST-07, EPIC-03, cycle 2026-05-31__release-v4.7 — render_log_retention_policy.md produced; Render 7-day retention documented; database audit tables confirmed durable; decision: Render logs + database tables sufficient; Infrastructure & Operations Owner sign-off

---

### BLG-OPS-28 — Staging deploy live verification (ST-09 staging-only AC)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-06-01
**Shipped in:** v4.7
**Evidence:** docs/product/changelog.md#v47; claude/cycles/2026-05-31__release-v4.7/verification_report.md

### BLG-OPS-28 — Staging deploy live verification (ST-09 staging-only AC)
**Priority:** P2 (Medium)
**Type:** Operations / CI/CD
**Owner:** Infrastructure & Operations Owner
**Source:** ST-09 staging-only AC — v4.0 sprint execution 2026-05-24
**Effort:** XS (~0.5 day)
**Provisional-Target:** v4.1
**Completed:** ST-04, EPIC-03, cycle 2026-05-31__release-v4.7 — staging_deploy_verification.md produced; RENDER_STAGING_DEPLOY_HOOK confirmed; code-change deploy verified; docs-only filter verified; Infrastructure & Operations Owner sign-off

---

### BLG-FE-49 — Pre-entry validation panel UX assessment

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-06-01
**Shipped in:** v4.7
**Evidence:** docs/product/changelog.md#v47; claude/cycles/2026-05-31__release-v4.7/verification_report.md

### BLG-FE-49 — Pre-entry validation panel UX assessment
**Priority:** P2 (Medium)
**Type:** Frontend / UX
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Source:** IDEA-head-of-ux-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled
**Completed:** ST-09, EPIC-04, cycle 2026-05-31__release-v4.7 — pre_entry_panel_ux_assessment.md produced; 3 improvement candidates filed BLG-FE-56/57/58; Head of UX & Design sign-off; no implementation committed

---

### BLG-FEAT-38 — Arc 5 compliance score in monthly P&L report

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-06-01
**Shipped in:** v4.7
**Evidence:** docs/product/changelog.md#v47; claude/cycles/2026-05-31__release-v4.7/verification_report.md

### BLG-FEAT-38 — Arc 5 compliance score in monthly P&L report
**Priority:** P2 (Medium)
**Type:** Product Feature / Reporting
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~2 days)
**Provisional-Target:** v4.1
**Completed:** ST-03, EPIC-02, cycle 2026-05-31__release-v4.7 — compliance_summary field added to GET /reports/monthly-pnl; reports_endpoints.md v0.5→v0.6; openapi.yaml updated; 2 unit tests + SC-REP-05a/05b Playwright scenarios pass

---
---

### BLG-FE-50 — Pre-entry check sizing validity: entry price not written correctly

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-29
**Shipped in:** v4.3
**Evidence:** docs/product/changelog.md#v4.3; claude/cycles/2026-05-29__release-v4.3/verification_report.md

### BLG-FE-50 — Pre-entry check sizing validity: entry price not written correctly
**Priority:** P2 (Medium)
**Type:** Bug / Frontend
**Owner:** Frontend Engineer
**Source:** User observation 2026-05-26 — sizing validity check in pre-entry panel
**Effort:** XS (~0.25 day)
**Provisional-Target:** ✅ COMPLETE — 2026-05-29 (cycle: 2026-05-29__release-v4.3)

**Problem**
The Sizing Validity check in the pre-entry validation panel requires `entry_price` and `stop_price` query params to compute validity. The entry price value being passed appears to be written/formatted incorrectly, causing the sizing validity check to fail or return unexpected results.

**Scope**
- Investigate how `entry_price` is constructed and passed to the sizing validity endpoint from the pre-entry panel
- Identify the formatting or serialisation error (e.g. wrong field source, stringified incorrectly, missing value)
- Fix so that the sizing validity check receives a valid numeric entry price and returns a correct result

**Acceptance Criteria**
- Sizing validity check in pre-entry panel passes when a valid entry price and stop price are available
- No regression to other pre-entry checks

---

### BLG-FE-51 — Claude thesis generation UI copy audit

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-29
**Shipped in:** v4.3
**Evidence:** docs/product/changelog.md#v4.3; claude/cycles/2026-05-29__release-v4.3/verification_report.md

### BLG-FE-51 — Claude thesis generation UI copy audit
**Priority:** P2 (Medium)
**Type:** Frontend / UX Polish
**Owner:** Base44 Frontend; Head of UX & Design
**Source:** IDEA-base44-frontend-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~0.5 day)
**Provisional-Target:** ✅ COMPLETE — 2026-05-29 (cycle: 2026-05-29__release-v4.3)

**Problem**
v4.1 replaced Gemini with Claude API for thesis generation. All UI copy, loading messages, error states, and tooltips that reference Gemini or are Gemini-specific must be updated or made provider-agnostic. Stale provider-specific text confuses users and creates documentation inconsistency.

**Scope**
- Audit all UI copy related to AI thesis generation (loading state, success message, error text, tooltips)
- Replace "Gemini" references with provider-agnostic copy (e.g. "AI-generated thesis")
- Confirm error messages do not surface provider-specific details

**Acceptance Criteria**
- No "Gemini" references in production UI copy
- Loading, success, and error states are provider-agnostic
- Reviewed by Head of UX & Design

---

### BLG-QA-28 — Playwright E2E coverage for Arc5ComplianceSection (PerformanceAnalytics §19)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-05-29
**Shipped in:** v4.3
**Evidence:** docs/product/changelog.md#v4.3; claude/cycles/2026-05-29__release-v4.3/verification_report.md

### BLG-QA-28 — Playwright E2E coverage for Arc5ComplianceSection (PerformanceAnalytics §19)
**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA Lead
**Source:** v4.0 ST-02/ST-04 EPIC-01 — deferred observable AC per CLAUDE.md §2
**Effort:** S (~0.5 day)
**Provisional-Target:** ✅ COMPLETE — 2026-05-29 (cycle: 2026-05-29__release-v4.3)

**Problem**
ST-02 and ST-04 introduced Arc5ComplianceSection (four stat cards: Red Flag Events/Week, Override Rate, Top Rule Breach, Trade Plan Adherence) into PerformanceAnalytics.js §19. These are frontend-visible changes but no Playwright test covers the rendering. Per CLAUDE.md §2, a backlog item must be filed before the PR opens when observable AC is deferred to staging.

**Scope**
- Add Playwright test in `tests/e2e/` for PerformanceAnalytics page
- Cover: Arc5ComplianceSection heading present, all 4 card titles visible, loading skeleton renders, error state renders "Unable to load"
- Use `page.route()` to mock `GET /analytics/arc5-compliance`

**Acceptance Criteria**
- AC-01: "Arc 5 Signal Compliance" heading visible on PerformanceAnalytics page
- AC-02: All 4 stat card titles visible (Red Flag Events/Week, Override Rate, Top Rule Breach, Trade Plan Adherence)
- AC-03: Loading skeleton shown when API pending
- AC-04: Error state shown when API returns 500

---

### BLG-QA-29 — Staging verification for Gemini thesis generation (ST-12 staging-only AC)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-29
**Shipped in:** v4.3
**Evidence:** docs/product/changelog.md#v4.3; claude/cycles/2026-05-29__release-v4.3/verification_report.md

### BLG-QA-29 — Staging verification for Gemini thesis generation (ST-12 staging-only AC)
**Priority:** P2 (Medium)
**Type:** QA / Staging Verification
**Owner:** QA Lead
**Source:** v4.0 ST-12 EPIC-03 — staging-only AC per CLAUDE.md §2
**Effort:** XS (~0.5 day)
**Provisional-Target:** ✅ COMPLETE — 2026-05-29 (cycle: 2026-05-29__release-v4.3)

**Problem**
ST-12 (Gemini Flash base wiring) introduced `POST /trade-plans/{plan_id}/generate-thesis` and the "Improve with AI" button in TradePlan. The acceptance criteria for thesis generation requires a live `GEMINI_API_KEY`. This cannot be verified in CI. Per CLAUDE.md §2, a backlog item must be filed before the PR opens.

**Scope**
- Configure `GEMINI_API_KEY` in staging environment (Render backend env vars)
- Configure `REACT_APP_GEMINI_API_KEY` in staging frontend (Render Static Site env vars)
- Test: create or open a trade plan in edit mode on staging
- Verify "Improve with AI" button appears and calls the endpoint
- Verify thesis text is generated and populates the textarea
- Record sign-off date in `qa_evidence_EPIC-03.md` DoQ block

**Acceptance Criteria**
- AC-01: `POST /trade-plans/{plan_id}/generate-thesis` returns thesis text when GEMINI_API_KEY is set on staging
- AC-02: "Improve with AI" button visible on TradePlan edit page when REACT_APP_GEMINI_API_KEY set
- AC-03: Button click generates thesis and populates setup_thesis textarea
- AC-04: Sign-off date recorded in qa_evidence_EPIC-03.md

---

### BLG-QA-30 — Staging verification: ST-05 ticker validation live Yahoo Finance rejection path

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-29
**Shipped in:** v4.3
**Evidence:** docs/product/changelog.md#v4.3; claude/cycles/2026-05-29__release-v4.3/verification_report.md

### BLG-QA-30 — Staging verification: ST-05 ticker validation live Yahoo Finance rejection path
**Priority:** P2 (Medium)
**Type:** QA / Staging Verification
**Owner:** Director of Quality; Head of Engineering
**Source:** v4.0 ST-05 EPIC-02 — staging-only AC per CLAUDE.md §2
**Effort:** XS (~0.5 day)
**Provisional-Target:** ✅ COMPLETE — 2026-05-29 (cycle: 2026-05-29__release-v4.3)

**Problem**
ST-05 (BLG-BE-15) adds Yahoo Finance symbol validation to `POST /ticker-universe`. The AC "invalid ticker returns HTTP 422 with error message (not saved)" requires a live internet-connected staging environment with `SKIP_TICKER_VALIDATION` unset. This cannot be verified in CI (no live network calls permitted).

**Scope**
- Remove (or unset) `SKIP_TICKER_VALIDATION` on staging environment
- POST an invalid ticker symbol (e.g. `ZZZINVALID`) to `POST /ticker-universe` on staging
- Confirm: HTTP 422 returned with `detail` containing "not found or not tradeable"
- Confirm: ticker does NOT appear in subsequent `GET /ticker-universe` response
- POST a valid ticker (e.g. `AAPL`) and confirm: HTTP 201, ticker added successfully
- Record staging sign-off date in this item and notify Director of Quality

**Acceptance Criteria**
- AC-01: Invalid ticker → HTTP 422, detail message present, ticker not saved (staging)
- AC-02: Valid ticker → HTTP 201, ticker present in GET /ticker-universe (staging)
- AC-03: Timeout scenario documented (if testable — can mock by blocking yfinance)

---

### BLG-QA-32 — Playwright scenario coverage matrix

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-29
**Shipped in:** v4.3
**Evidence:** docs/product/changelog.md#v4.3; claude/cycles/2026-05-29__release-v4.3/verification_report.md

### BLG-QA-32 — Playwright scenario coverage matrix
**Priority:** P2 (Medium)
**Type:** QA / Process
**Owner:** Director of Quality; QA Lead
**Source:** IDEA-director-of-quality-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** M (~2 days)
**Provisional-Target:** ✅ COMPLETE — 2026-05-29 (cycle: 2026-05-29__release-v4.3)

**Problem**
No consolidated view exists mapping delivered features to their Playwright scenario coverage. As the test suite grows (currently 40+ scenarios across multiple spec files), understanding which features have complete coverage and which have staging-only ACs or gaps becomes a governance concern. A coverage matrix enables proactive gap identification before sprint planning.

**Scope**
- Produce matrix: feature/story → Playwright spec file(s) → scenario count → staging-only ACs flagged
- Source: all spec files in tests/e2e/ mapped against sprint_backlog.md story lists from v3.7–v4.0
- Output: coverage matrix document (markdown) filed in docs/qa/ or equivalent
- Identify: features with zero automated coverage (human staging only)

**Acceptance Criteria**
- Coverage matrix produced covering v3.7–v4.0 delivered features
- Staging-only ACs identified and flagged
- Coverage gaps documented for Product Owner review
- Matrix reviewed by Director of Quality before next sprint planning

---

### BLG-QA-33 — Arc 5 Playwright coverage audit

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-29
**Shipped in:** v4.3
**Evidence:** docs/product/changelog.md#v4.3; claude/cycles/2026-05-29__release-v4.3/verification_report.md

### BLG-QA-33 — Arc 5 Playwright coverage audit
**Priority:** P2 (Medium)
**Type:** QA / Audit
**Owner:** QA & Testing Owner; Director of Quality
**Source:** IDEA-qa-testing-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~1 day)
**Provisional-Target:** ✅ COMPLETE — 2026-05-29 (cycle: 2026-05-29__release-v4.3)

**Problem**
Arc 5 shipped across v3.8 (SI-01), v3.9 (SI-03), and v4.0 (Arc5ComplianceSection + SI-01→SI-03 integration). A targeted Arc 5 coverage audit confirms: which SI features have full Playwright coverage, which have staging-only ACs, and whether the v4.0 integration suite (SC-AC5-xx) covers all user-observable behaviours. Distinct from BLG-QA-32 (which covers all features); this is an in-depth audit of Arc 5 specifically.

**Scope**
- Review all Playwright spec files covering Arc 5 features (system-status.spec.js, SC-RFJ-*, SC-PEV-*, SC-AC5-*)
- Map each observable AC per SI feature against scenario coverage
- Flag gaps; produce coverage assessment document

**Acceptance Criteria**
- Coverage assessment document produced for Arc 5 features
- Gaps identified with specific scenario recommendations
- Reviewed by Director of Quality

---

### BLG-QA-35 — Staging verification: ST-09 Claude API daily cost threshold alert (AC-05 deferral)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-29
**Shipped in:** v4.3
**Evidence:** docs/product/changelog.md#v4.3; claude/cycles/2026-05-29__release-v4.3/verification_report.md

### BLG-QA-35 — Staging verification: ST-09 Claude API daily cost threshold alert (AC-05 deferral)
**Priority:** P2 (Medium)
**Type:** QA / Staging Verification
**Owner:** QA Lead; Infrastructure & Operations Owner
**Source:** ST-09 (EPIC-03, v4.1) — staging-only AC deferred per sprint_backlog.md designation
**Effort:** XS (~0.5 day)
**Provisional-Target:** ✅ COMPLETE — 2026-05-29 (cycle: 2026-05-29__release-v4.3)

**Problem**
ST-09 AC-05 (POST /ai/check-daily-cost staging verification) was designated staging-only at sprint planning. The endpoint and Telegram alert logic cannot be verified by automated unit tests alone — a live staging environment with a real TELEGRAM_BOT_TOKEN and database rows in gemini_audit_log is required to confirm end-to-end operation.

**Acceptance Criteria**
- On staging: POST /ai/check-daily-cost returns 200 with threshold/cost fields
- With AI_DAILY_COST_THRESHOLD set below current daily spend: Telegram alert fires and is received
- Date of staging verification recorded in QA evidence file

---

### BLG-QA-36 — Arc 5 end-to-end integration test specification

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-29
**Shipped in:** v4.3
**Evidence:** docs/product/changelog.md#v4.3; claude/cycles/2026-05-29__release-v4.3/verification_report.md

### BLG-QA-36 — Arc 5 end-to-end integration test specification
**Priority:** P2 (Medium)
**Type:** QA / Integration Testing
**Owner:** Director of Quality; QA Lead
**Source:** IDEA-director-of-quality-20260527-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** M (~2 days)
**Provisional-Target:** ✅ COMPLETE — 2026-05-29 (cycle: 2026-05-29__release-v4.3)

**Problem**
Existing Playwright tests cover per-feature ACs (SI-01, SI-03, Arc5ComplianceSection) but no formal integration test spec covers the complete Arc 5 compliance pipeline: SI-01 pre-entry validation → override acknowledgement → SI-03 red flag event written → Arc5ComplianceSection metrics update. Cross-feature integration failures would not be caught by current per-feature tests.

**Scope**
- Define formal cross-feature integration test spec for Arc 5 compliance pipeline
- Cover: SI-01 → SI-03 data flow, Arc5ComplianceSection metric source, override chain
- Produce test spec document with observable assertions for each integration point
- Identify Playwright automation candidates vs manual verification steps

**Acceptance Criteria**
- Integration test spec document produced
- Observable assertions defined for each integration point
- Reviewed by Director of Quality and QA Lead

---

### BLG-QA-38 — CI pipeline execution time baseline measurement

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-29
**Shipped in:** v4.3
**Evidence:** docs/product/changelog.md#v4.3; claude/cycles/2026-05-29__release-v4.3/verification_report.md

### BLG-QA-38 — CI pipeline execution time baseline measurement
**Priority:** P2 (Medium)
**Type:** QA / Test Infrastructure
**Owner:** QA Lead
**Source:** IDEA-qa-lead-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** XS (~0.25 day)
**Provisional-Target:** ✅ COMPLETE — 2026-05-29 (cycle: 2026-05-29__release-v4.3)

**Problem**
BLG-QA-27 gates on CI pipeline execution time > 5 minutes sustained across 3+ cycles. No baseline measurement exists. This item performs the gate-check measurement: measure total CI execution time for the current test suite and determine whether BLG-QA-27 gate clears.

**Scope**
- Measure total CI pipeline execution time for current test suite (3 sample runs)
- Record measurement in QA notes
- If > 5 minutes sustained: flag BLG-QA-27 gate as cleared for next sprint planning
- If under threshold: record measurement and defer BLG-QA-27

**Acceptance Criteria**
- Baseline measurement recorded (3 sample runs, p50 noted)
- Gate status determination for BLG-QA-27 documented
- Reviewed by QA Lead

---

### BLG-OPS-33 — Staging environment parity audit

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-29
**Shipped in:** v4.3
**Evidence:** docs/product/changelog.md#v4.3; claude/cycles/2026-05-29__release-v4.3/verification_report.md

### BLG-OPS-33 — Staging environment parity audit
**Priority:** P2 (Medium)
**Type:** Operations / Quality
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** M (~2 days)
**Provisional-Target:** ✅ COMPLETE — 2026-05-29 (cycle: 2026-05-29__release-v4.3)

**Gate criteria:** v4.1 sprint planning complete — staging parity audit scope depends on which new endpoints are included in v4.1.
*⚡ Gate cleared 2026-05-27 — v4.1 sprint planning complete (2026-05-27__scheduled cycle inline clearance). Item ready for sprint planning.*

**Problem**
Staging environment parity with production is a delivery verification prerequisite (staging-only ACs require staging to mirror production configuration). BLG-OPS-28 (ST-09 staging-only AC) verified specific endpoints for v4.0. A systematic parity audit confirms: all v4.0 new env vars are present in staging, all new database tables exist in staging schema, and all new services (Gemini integration) are reachable in staging.

**Scope**
- Verify: staging env vars match production (GEMINI_API_KEY, all Alpaca keys, DB connection)
- Verify: database schema parity (gemini_audit_log, red_flag_events tables present in staging)
- Verify: all v4.0 endpoints respond on staging (sampled health check, not full load test)
- Document: parity report filed in ops notes

**Acceptance Criteria**
- Parity report produced
- All v4.0 env vars and schema confirmed in staging
- Gate condition (v4.1 sprint planning complete) verified before commencing

---

### BLG-OPS-42 — Add GET /ai/claude-audit-log to api_performance_baseline.md

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-05-29
**Shipped in:** v4.3
**Evidence:** docs/product/changelog.md#v4.3; claude/cycles/2026-05-29__release-v4.3/verification_report.md

### BLG-OPS-42 — Add GET /ai/claude-audit-log to api_performance_baseline.md
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** Post-ship closure v4.2 — endpoint coverage drift advisory (STEP 6)
**Effort:** XS (~0.25 day)
**Provisional-Target:** ✅ COMPLETE — 2026-05-29 (cycle: 2026-05-29__release-v4.3)

**Problem**
GET /ai/claude-audit-log was added in v4.2 (ST-07, BLG-GOV-63) and is present in openapi.yaml but absent from docs/ops/api_performance_baseline.md. Performance re-runs require a live environment and human coordination.

**Scope**
- Add GET /ai/claude-audit-log to api_performance_baseline.md measurement table with baseline timing data
- Coordinate with Infrastructure & Operations Owner for live environment timing run

**Acceptance Criteria**
- GET /ai/claude-audit-log appears in api_performance_baseline.md with at least estimated p50 latency
- Reviewed by Infrastructure & Operations Owner

---

### BLG-GOV-36 — API key rotation cadence policy

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-29
**Shipped in:** v4.3
**Evidence:** docs/product/changelog.md#v4.3; claude/cycles/2026-05-29__release-v4.3/verification_report.md

### BLG-GOV-36 — API key rotation cadence policy
**Priority:** P2 (Medium)
**Type:** Governance / Security Policy
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Source:** IDEA-cybersecurity-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~0.5 day)
**Provisional-Target:** ✅ COMPLETE — 2026-05-29 (cycle: 2026-05-29__release-v4.3)

**Problem**
Alpaca API keys (financial account access) and Gemini API keys have no defined rotation cadence. Without a formal policy specifying minimum rotation interval and documented responsibility, the exposure window for a compromised credential is unbounded.

**Scope**
- Define rotation cadence: Alpaca keys — minimum annual rotation; Gemini keys — minimum annual rotation
- Document rotation procedure: how to rotate without service disruption (environment variable update, staging + prod)
- Assign responsibility: Infrastructure & Operations Owner as rotation executor; Cybersecurity & Trust Lead as policy owner
- File policy document in `docs/ops/api_key_rotation_policy.md`

**Acceptance Criteria**
- Policy document produced covering Alpaca and Gemini key rotation
- Rotation cadence, procedure, and responsibility defined
- Next rotation date recorded (based on last known rotation date or "unknown — rotate on policy adoption")

---

### BLG-GOV-42 — Staging-only AC pre-designation reference table

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-05-29
**Shipped in:** v4.3
**Evidence:** docs/product/changelog.md#v4.3; claude/cycles/2026-05-29__release-v4.3/verification_report.md

### BLG-GOV-42 — Staging-only AC pre-designation reference table
**Priority:** P1 (High)
**Type:** Governance / Sprint Planning Process
**Owner:** Head of Specs Team; Director of Quality
**Source:** IDEA-director-of-quality-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** ✅ COMPLETE — 2026-05-29 (cycle: 2026-05-29__release-v4.3)

**Gate criteria:** OA-01/OA-02 escalation resolved by Head of Specs Team at v4.1 sprint planning — staging-only AC reference table requires escalation closure first.

**Problem**
OA-01 (2nd recurrence — staging-only AC designation) has been escalated to Head of Specs Team. Before v4.1 sprint planning, a reference table of known staging-only AC patterns (e.g., "all Playwright E2E tests covering live Render endpoints", "any AC requiring non-mocked external API") should be produced to prevent ad-hoc designation at sprint close time.

**Scope**
- Produce reference table of staging-only AC categories and examples
- Based on patterns observed in v3.7–v4.0 deliveries (BLG-QA-24, BLG-QA-28, BLG-QA-29, BLG-QA-30)
- Integrated into sprint planning guidance (sprint_planning_prompt.md or OPERATIONAL_GUIDE.md)
- Gate: OA-01/02 escalation resolved before this item can be actioned

**Acceptance Criteria**
- Reference table produced
- Integrated into sprint planning reference materials
- Head of Specs Team sign-off
- Gate condition (OA-01/02 resolution) verified

---

### BLG-GOV-47 — AI feature inventory

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-29
**Shipped in:** v4.3
**Evidence:** docs/product/changelog.md#v4.3; claude/cycles/2026-05-29__release-v4.3/verification_report.md

### BLG-GOV-47 — AI feature inventory
**Priority:** P2 (Medium)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer
**Source:** IDEA-ai-compliance-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** ✅ COMPLETE — 2026-05-29 (cycle: 2026-05-29__release-v4.3)

**Problem**
v4.0 shipped the first external AI API integration (Gemini Flash for thesis generation). As AI features accumulate, a formal AI feature inventory is needed for compliance, audit, and §13 review traceability. The inventory should be maintained as a living document and referenced at each release planning cycle where an AI-adjacent feature is in scope.

**Scope**
- Produce AI feature inventory document: current AI-touching features (Gemini thesis generation, AI Journal Summarisation), model used, purpose, §13 compliance status, data inputs/outputs
- Filed in docs/ai/ or equivalent governance location
- Reviewed and maintained by AI Compliance & Governance Officer

**Acceptance Criteria**
- Inventory document produced and filed
- All current AI features listed with compliance status
- Reviewed by AI Compliance & Governance Officer and Strategy Rules & System Intent Owner

---

### BLG-GOV-50 — External API key security register

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-29
**Shipped in:** v4.3
**Evidence:** docs/product/changelog.md#v4.3; claude/cycles/2026-05-29__release-v4.3/verification_report.md

### BLG-GOV-50 — External API key security register
**Priority:** P2 (Medium)
**Type:** Governance / Security
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Source:** IDEA-cybersecurity-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~1 day)
**Provisional-Target:** ✅ COMPLETE — 2026-05-29 (cycle: 2026-05-29__release-v4.3)

**Problem**
The system now has four external API credentials: Alpaca API key+secret, Yahoo Finance (no key required), Supabase/DB connection string, and GEMINI_API_KEY. No consolidated external API key security register exists — documenting each key's purpose, scope, rotation cadence, and storage location. BLG-GOV-36 (API key rotation cadence policy, IW-20260522-01) addressed Alpaca keys; this item extends to all external API keys.

**Scope**
- Produce external API key security register: key name, purpose, scope, rotation cadence, storage location (Render env var, .env.example), last rotation date
- Cover: Alpaca API key+secret, GEMINI_API_KEY, Supabase/DB connection string
- Register reviewed annually or on new API integration

**Acceptance Criteria**
- Register produced and filed in docs/security/
- All external API keys listed with security metadata
- Reviewed by Cybersecurity & Trust Lead


## v3.8 Completions — Archived 2026-05-21 (Post-Ship Closure)

---

### BLG-FEAT-22 — Ticker Universe Management page

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-21
**Shipped in:** v3.8 (ST-09, cycle: 2026-05-19__release-v3.8, closed 2026-05-20)
**Evidence:** docs/product/changelog.md#v38; claude/cycles/2026-05-19__release-v3.8/verification_report.md

### BLG-FEAT-22 — Ticker Universe Management page
✅ COMPLETE v3.8 — ST-09, cycle: 2026-05-19__release-v3.8, closed 2026-05-20
**Priority:** P2 (Medium)
**Type:** Product Feature / User Configuration
**Owner:** Head of UX & Design; Head of Backend Engineering
**Source:** User request — 2026-05-19
**Effort:** M (~1–2 days)
**Provisional-Target:** v3.8

**Problem**
Users currently have no way to manage the ticker universe that drives both screener and signal generation. The `ticker_universe` table is already used as the single source by both features, but there is no UI to view, add, deactivate, or remove tickers. Additionally, a legacy `public.tickers` table is synced into `ticker_universe` on startup, creating a secondary source-of-truth and confusion about where the canonical universe lives.

**Scope**
- Retire the startup sync from `public.tickers` into `ticker_universe`; make `ticker_universe` the sole authoritative source
- Build a Ticker Universe Management page in the frontend (new route, nav entry)
- Page features: table of all tickers (ticker, market, sector, active status); add ticker form (ticker symbol, market US/UK, optional sector/industry); toggle active/inactive per ticker; delete ticker permanently
- Filter/search by market (US / UK) and active status
- Wire to existing `/ticker-universe` GET, POST, DELETE endpoints (no new backend endpoints required)

**Acceptance Criteria**
- `public.tickers` startup sync removed; `ticker_universe` is populated only via the management UI or seed defaults
- Universe Management page accessible from nav; displays all tickers with market, sector, and active status
- User can add a ticker (US or UK market); added ticker appears immediately in the table
- User can toggle a ticker inactive; inactive tickers are excluded from the next screener/signal run
- User can delete a ticker permanently; it no longer appears in the table
- Filter by market (US/UK/All) and active status works correctly
- Screener and signal generation both continue to use only active tickers from `ticker_universe`

---

### BLG-FEAT-23 — Setup type classification field on trade plans

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-21
**Shipped in:** v3.8 (ST-06, cycle: 2026-05-19__release-v3.8, closed 2026-05-20)
**Evidence:** docs/product/changelog.md#v38; claude/cycles/2026-05-19__release-v3.8/verification_report.md

### BLG-FEAT-23 — Setup type classification field on trade plans
✅ COMPLETE v3.8 — ST-06, cycle: 2026-05-19__release-v3.8, closed 2026-05-20
**Priority:** P2 (Medium)
**Type:** Product Feature / Data Model
**Owner:** Product Owner; Head of UX & Design; Backend Engineering Patterns Owner
**Source:** User session — 2026-05-19
**Effort:** S (~0.5 days)
**Provisional-Target:** v3.8

**Problem**
The trade plan form's setup thesis field is a free-text textarea with no structural anchor. Traders don't know what vocabulary to use, and without a setup type classification the app cannot in future surface behavioural patterns.

**Scope**
- Add a "Setup Type" dropdown to the trade plan form with six options
- Add `setup_type` (VARCHAR, nullable) column to the `trade_plans` table via migration
- Update POST /trade-plans and PUT /trade-plans/{id} to accept and persist `setup_type`

---

### BLG-FEAT-24 — AI-assisted setup thesis generation

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-21
**Shipped in:** v3.8 (ST-08, cycle: 2026-05-19__release-v3.8, closed 2026-05-20)
**Evidence:** docs/product/changelog.md#v38; claude/cycles/2026-05-19__release-v3.8/verification_report.md

### BLG-FEAT-24 — AI-assisted setup thesis generation
✅ COMPLETE v3.8 — ST-08, cycle: 2026-05-19__release-v3.8, closed 2026-05-20
**Priority:** P2 (Medium)
**Type:** Product Feature / UX Enhancement
**Owner:** Product Owner; Head of UX & Design; Backend Engineering Patterns Owner
**Source:** User session — 2026-05-19

---

### BLG-FE-36 — Add news context panel to trade plan form

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-21
**Shipped in:** v3.8 (ST-07, cycle: 2026-05-19__release-v3.8, closed 2026-05-20)
**Evidence:** docs/product/changelog.md#v38; claude/cycles/2026-05-19__release-v3.8/verification_report.md

### BLG-FE-36 — Add news context panel to trade plan form
✅ COMPLETE v3.8 — ST-07, cycle: 2026-05-19__release-v3.8, closed 2026-05-20
**Priority:** P2 (Medium)
**Type:** Frontend / UX
**Owner:** Head of UX & Design; Backend Engineering Patterns Owner
**Source:** User session — 2026-05-19

---

### BLG-GOV-24 — Add gh_issue_template.md to §14 governance table

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-05-21
**Shipped in:** v3.8 (ST-10, cycle: 2026-05-19__release-v3.8, closed 2026-05-20)
**Evidence:** docs/product/changelog.md#v38; claude/cycles/2026-05-19__release-v3.8/verification_report.md

### BLG-GOV-24 — Add gh_issue_template.md to §14 governance table
✅ COMPLETE v3.8 — ST-10, cycle: 2026-05-19__release-v3.8, closed 2026-05-20
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Governance-drift check during preflight consolidation branch gov/2026-05-17__preflight-consolidation — 2026-05-17

---

## v3.7 Completions — Archived 2026-05-19 (Post-Ship Closure)

*BLG-FE-33 (Signals page Add to Watchlist CTA — watchlisted status backend + SignalCard CTA replacement) — ✅ COMPLETE v3.7 — ST-01 + ST-02, cycle: 2026-05-18__release-v3.7*

*BLG-FE-34 (Trade plan form signal context panel — SignalContextPanel.js with entry_rationale/confirmation pre-population) — ✅ COMPLETE v3.7 — ST-03, cycle: 2026-05-18__release-v3.7*

*BLG-QA-20 (Consolidate database stub files into shared pytest conftest fixture — session-scoped stub) — ✅ COMPLETE v3.7 — ST-09, cycle: 2026-05-18__release-v3.7*

*BLG-OPS-16 (Remove tracked backend/__pycache__ files from git + .gitignore) — ✅ COMPLETE v3.7 — ST-10, cycle: 2026-05-18__release-v3.7*

*BLG-GOV-23 (scored_initiatives.md Arc 3–6 comprehensive refresh — OA-RP-05 resolved) — ✅ COMPLETE v3.7 — ST-11, cycle: 2026-05-18__release-v3.7*

---

*BLG-GOV-22 (sprint_planning_prompt.md patch: shared execution_state.json ownership + multi-EPIC Positions.js conflict guidance) — ✅ COMPLETE v3.5 (ST-11, 2026-05-15) — archived 2026-05-15*

*BLG-GOV-21 (Arc 4 data requirements capture) — ✅ COMPLETE v3.5 (ST-04, 2026-05-15; arc4_data_requirements.md v1.0 signed off) — archived 2026-05-15*

*BLG-QA-19 (Research view regression test protocol) — ✅ COMPLETE v3.5 (ST-10, 2026-05-15; research_view_regression_protocol.md v1.0, QA Lead sign-off) — archived 2026-05-15*

*BLG-SPEC-31 (Review React Query v5 onSuccess migration impact across codebase) — ✅ COMPLETE v3.5 (ST-09, 2026-05-15; 1 fix TradePlan.js; SC-TP-08 Playwright 9/9 pass) — archived 2026-05-15*

*BLG-SPEC-30 (Correct stop-management-workflow ux_spec.md §4.4 stop-update HTTP verb to PATCH) — ✅ COMPLETE v3.5 (ST-08, 2026-05-15; ux_spec.md v1.1) — archived 2026-05-15*

*BLG-SPEC-29 (Correct grace-period-alert ux_spec.md §5 dismiss storage to sessionStorage) — ✅ COMPLETE v3.5 (ST-07, 2026-05-15; ux_spec.md v1.1) — archived 2026-05-15*

---

## v3.4 Completions — Archived 2026-05-14 (GROOM-20260514-01)

### BLG-FEAT-21 — Trade plan abandonment status field

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-14
**Shipped in:** v3.3 backend (ST-17, EPIC-04) + v3.4 frontend (ST-10, EPIC-03, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

`Abandoned` status added to trade plan lifecycle with required `abandonment_reason` field. Status transition guard enforced: Active-position-linked plans cannot be abandoned. Abandoned plans surface in plan history alongside Closed plans. Backend guard on PUT/PATCH endpoint delivered v3.3 (ST-17); frontend abandonment action and reason input in TradePlan.js delivered v3.4 (ST-10).

---

### BLG-FE-31 — Research view component library

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-11, EPIC-04, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

Catalogue of PT-02 research view UI components (price card, regime/signal panel, news feed, source attribution row, freshness indicator). Each entry: component name, file path, key props, variants. Reuse candidates for Arc 3 frontend (IT-01/02/03 stories) explicitly noted. Delivered before v3.4 sprint planning as scoped.

---

### BLG-FE-22 — Screener morning routine UX spec

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-12, EPIC-04, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

Workflow spec for Arc 1→Arc 2 morning routine: screener results → shortlist → watchlist promotion → pre-trade research navigation. Information-carry decisions documented (context visible in research view from screener). Navigation model specified across three surfaces.

---

### BLG-FE-23 — Research page UK ticker suffix not stripped

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-07, EPIC-03, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

`stripUkSuffix` utility applied to Research.js page title/header. UK tickers (e.g. MTLN.L) display as MTLN in Research page heading. Consistent with screener and watchlist treatment. No regression to other suffix-stripping surfaces. Origin: v3.2 delivery verification DEV-E01-03.

---

### BLG-FE-24 — Negative earnings days display for past earnings dates

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-07, EPIC-03, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

Negative `days_until_earnings` (past earnings date) now displays `—` across all earnings columns (screener, watchlist, positions). Zero displays `Today`. Positive values unchanged. Earnings proximity warning (≤5 days amber) unaffected.

---

### BLG-FE-25 — Signals page: default to most recent day's signals

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-08, EPIC-03, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

Signals page defaults to most recent trading day's signals on load. Date picker/toggle control added for viewing historical signals. Morning-routine use case (review current day's signals) now supported directly on load. Signal data accuracy unaffected.

---

### BLG-FE-29 — Watchlist research status indicator

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-09, EPIC-03, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

Binary research status indicator added to watchlist ticker rows. Done = research record exists; Not Done = no record. Icon/badge display — no text, minimal column width. Scope constraint honoured: no research quality score or freshness judgement.

---

### BLG-FE-30 — Trade plan status badges

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-10, EPIC-03, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

Colour-coded status badges for all trade plan statuses: Draft (grey), Research Pending (amber), Research Complete (blue), Entry Conditions Set (purple), Active (green), Closed (muted), Abandoned (red). Applied in trade plan list and detail views. Colours aligned with design system tokens. Coordinate-delivered with BLG-FEAT-21 Abandoned status.

---

### BLG-AI-03 — AI Journal Summarisation quarterly review cadence

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-13, EPIC-04, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

Quarterly review process defined for AI Journal Summarisation (AI-SUM). Review checklist: output quality sample review, §13 compliance re-confirmation, BLG-AI-02 model version record update, error rate review from BLG-OPS-14 monitoring. Process documented in governance file; OPERATIONAL_GUIDE updated. First review: Q3 2026.

---

### BLG-QA-18 — Screener accuracy test protocol

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-14, EPIC-04, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

Formal QA protocol for validating screener output accuracy against §11 strategy rules. Test cases: regime gate pass/fail, ATR threshold boundary, signal score threshold cases. References `strategy_rules.md §11` as authoritative parameter source. Built on BLG-QA-08 mock harness and BLG-QA-10 screener test coverage. Owner: Director of Quality.

---

### BLG-SPEC-28 — trade_plan.md §6.2 entry checklist field reference update

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-13, EPIC-04, cycle 2026-05-14__release-v3.4)
**Evidence:** `docs/product/changelog.md` v3.4 entry; `claude/cycles/2026-05-14__release-v3.4/verification_report.md`

`trade_plan.md §6.2` pre-population rules corrected: `stop_defined` pre-checked when `early_exit_conditions` present (not `stop_level`); `research_reviewed` pre-checked when `r_target` set (not `risk_reward_notes`). Spec now aligned to TradePlan.js implementation. No implementation change required — implementation was correct. Origin: ST-11 (EPIC-03, v3.3) P3 deviation.

---

### TEST-GAP-EPIC-01-v33 — Position lifecycle badge Playwright E2E scenarios

**Status at retirement:** ✅ Resolved
**Priority at retirement:** P3 (Low)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-01, EPIC-01, cycle 2026-05-14__release-v3.4)
**Evidence:** `claude/cycles/2026-05-14__release-v3.4/verification_report.md`; SC-LS-01–04 passing in CI

SC-LS-01–04 authored and passing: lifecycle badge visible for all states (GRACE/PROFITABLE/LOSING/EXIT ZONE/UNKNOWN), feature flag OFF suppresses badge, days_in_state display confirmed, exit zone purple colouring verified. TSG-v33-01 resolved — marked in `docs/specs/Specs_Index.md` 2026-05-14.

---

### TEST-GAP-EPIC-02-v33 — Grace period alert and trail stop Playwright E2E scenarios

**Status at retirement:** ✅ Resolved
**Priority at retirement:** P3 (Low)
**Retired:** 2026-05-14
**Shipped in:** v3.4 (ST-02 + ST-03, EPIC-01, cycle 2026-05-14__release-v3.4)
**Evidence:** `claude/cycles/2026-05-14__release-v3.4/verification_report.md`; SC-GP-01–03 and SC-TS-01–03 passing in CI

SC-GP-01–03: alert card renders for GRACE ≥ day 8, displays ticker/days/plan context, sessionStorage dismiss confirmed. SC-TS-01–03: Trail Stop button for PROFITABLE/EXIT ZONE positions, panel shows current/ATR stop/difference/R-terms, user-confirm required (§13 compliant). TSG-v33-02 resolved — marked in `docs/specs/Specs_Index.md` 2026-05-14.

---

## v3.3 Completions — Archived 2026-05-13 (GROOM-20260513-01)

### BLG-FEAT-13 — Add gated feature rollout capability

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-16, EPIC-04, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/product/changelog.md` v3.3 entry; `claude/cycles/2026-05-09__release-v3.3/verification_report.md`

Feature flag infrastructure: `is_flag_enabled()` utility, `FEATURE_FLAGS` env var, `feature_flags.json` config, startup audit logging. `arc3_lifecycle_display` flag as proof-of-concept. Pattern documented in `docs/specs/platform/feature_flags.md`. Mandatory delivery after 3 consecutive deferrals (v3.0–v3.2).

---

### BLG-SPEC-24 — PT-02 research view canonical spec

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-09, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/product/changelog.md` v3.3 entry; `claude/cycles/2026-05-09__release-v3.3/qa_evidence_EPIC-03.md`

Class 2 canonical spec for PT-02 research view delivered at `docs/specs/frontend/pages/research_view.md`. Covers data fields, sources, freshness policy, §13 compliance, display rules. References BLG-SPEC-25, BLG-SPEC-26, BLG-FE-28.

---

### BLG-SPEC-25 — PT-02 research endpoint API contract

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-08, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/product/changelog.md` v3.3 entry; `docs/specs/api_contracts/research_endpoint.md`

Formal Class 2 API contract for `GET /research/{ticker}` at `docs/specs/api_contracts/research_endpoint.md`. Covers request parameters, response schema, source attribution, error codes (known deviation DEV-v33-02: 200+null vs 404/503/429; filed as BLG-SPEC-27), rate limit policy.

---

### BLG-SPEC-26 — Research view data source provenance spec

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-08, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/product/changelog.md` v3.3 entry; `docs/specs/data_provenance/research_view_provenance.md`

Provenance attribution spec for research view data fields. Per-field source (Yahoo Finance, Alpaca, internal), retrieval timestamp requirements, display format. Filed as prerequisite for BLG-SPEC-24 and BLG-FE-28.

---

### BLG-FE-28 — Pre-Trade Research View UX spec

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-09, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/product/changelog.md` v3.3 entry; `docs/design/2026-05-09__release-v3.3/research-view/ux_spec.md`

UX spec for PT-02 research view covering layout, data field placement, source attribution display, news feed design, freshness indicator, empty/error states. References design system tokens. Delivered before v3.3 sprint planning as required.

---

### BLG-QA-14 — Author Playwright E2E test suite for entry checklist

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-11, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `tests/e2e/entry-checklist.spec.js`; `claude/cycles/2026-05-09__release-v3.3/qa_evidence_EPIC-03.md`

`tests/e2e/entry-checklist.spec.js` authored covering SC-CL-01 to SC-CL-07. Note: DEV-v33-03 (P3) — tests cover actual field names (early_exit_conditions/r_target) not spec names (stop_level/risk_reward_notes); deviation documented. Resolves TSG-v32-01.

---

### BLG-QA-15 — PT-02 research view acceptance test protocol

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-10, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/qa/acceptance_protocols/research_view_protocol.md`; `claude/cycles/2026-05-09__release-v3.3/qa_evidence_EPIC-03.md`

Acceptance test protocol for PT-02 research view at `docs/qa/acceptance_protocols/research_view_protocol.md`. Covers observable ACs, Playwright vs human staging split, freshness threshold, error state criteria. Includes SC-RV-01–19 references. Note: SC-RV-18/19 explicit scenarios deferred (TEST-GAP-EPIC-03-v33 filed).

---

### BLG-QA-16 — Research endpoint integration test coverage

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-12, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `backend/routers/test.py`; `claude/cycles/2026-05-09__release-v3.3/qa_evidence_EPIC-03.md`

`GET /research/{ticker}` added to `backend/routers/test.py` with AAPL as representative test value. Covers success, partial source failure, full failure scenarios. Source attribution fields verified. SystemStatus.js endpoint count updated.

---

### BLG-QA-17 — Research view test scenario library

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-10, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/qa/test_scenarios/research_view_scenarios.md`; `claude/cycles/2026-05-09__release-v3.3/qa_evidence_EPIC-03.md`

Test scenario library for PT-02 research view: 19 scenarios SC-RV-01–19 covering data field rendering, source attribution, news feed, freshness indicator, error states. Library reviewed by DoQ. Referenced in BLG-QA-15 acceptance test protocol.

---

### BLG-OPS-15 — Research endpoint latency monitoring

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-12, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/ops/api_performance_baseline.md#section-11`; `claude/cycles/2026-05-09__release-v3.3/qa_evidence_EPIC-03.md`

Research endpoint latency baseline documented: `docs/ops/api_performance_baseline.md` §11. p50 2500–4000ms, p95 ≤3000ms target (multi-source external API aggregation). Latency target documented with rationale.

---

### BLG-SEC-06 — Trade plan data sensitivity classification

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-12, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/specs/security/trade_plan_data_sensitivity.md`; `claude/cycles/2026-05-09__release-v3.3/qa_evidence_EPIC-03.md`

Classification document at `docs/specs/security/trade_plan_data_sensitivity.md`. Three sensitivity levels: Public (ticker), Internal (dates, status), Private (entry zone, stop, R-target, thesis, checklist). Access control principles per level. Cybersecurity sign-off recorded.

---

### BLG-GOV-19 — PT-05 entry checklist §13 compliance review

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-15, EPIC-04, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/specs/compliance/pt05_entry_checklist_s13_review.md`; `claude/cycles/2026-05-09__release-v3.3/qa_evidence_EPIC-04.md`

Formal §13 boundary review for PT-05. Confirmed display-only, human-in-the-loop. Strategy Rules & System Intent Owner sign-off recorded. `trade_plan.md` updated to reference compliance review.

---

### BLG-GOV-20 — Trade plan field extension governance

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-13
**Shipped in:** v3.3 (ST-12, EPIC-03, cycle 2026-05-09__release-v3.3)
**Evidence:** `docs/governance/trade_plan_field_extension_policy.md`; `claude/cycles/2026-05-09__release-v3.3/qa_evidence_EPIC-03.md`

Field extension governance policy at `docs/governance/trade_plan_field_extension_policy.md`. Covers field addition criteria, migration strategy, backwards compatibility, authority (Data Model owner + Product Owner), changelog format. Data Model owner sign-off recorded.

---

### BLG-FEAT-19 — Monthly P&L summary report

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-05-05
**Shipped in:** v3.1 (ST-08, EPIC-03, cycle 2026-04-29__release-v3.1)
**Evidence:** `docs/product/changelog.md` v3.1 entry; `claude/cycles/2026-04-29__release-v3.1/verification_report.md`

Month-by-month breakdown of realised P&L. New `GET /reports/monthly-pnl` endpoint added. Consistent with existing annual tax-year P&L calculation. No regression to annual report confirmed in verification.

**Priority:** P2 (Medium)
**Type:** Product Feature / Reporting
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260321-01 — promoted cycle 2026-04-21__scheduled (DL-021)
**Effort:** S (~1 day)
**Provisional-Target:** v3.1

**Problem**
Only annual (tax-year) P&L is available. In-year performance patterns are only visible through the analytics page; no structured monthly summary exists.

**Scope**
- Month-by-month breakdown of realised P&L complementing the annual tax year report
- New endpoint or extension of existing reporting endpoint
- Display in financial reporting section of the application

**Acceptance Criteria**
- Monthly P&L breakdown available for current and prior year
- Consistent with existing realised P&L calculation
- No regression to annual tax-year report

---

### BLG-FEAT-18 — Consecutive losing streak metric

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-04-28
**Shipped in:** v3.0 (ST-15, cycle 2026-04-25__release-v3.0)
**Evidence:** `docs/product/changelog.md` v3.0 entry; `claude/cycles/2026-04-25__release-v3.0/verification_report.md`

Consecutive losing streak count added to analytics. `advanced_metrics.loss_streak` computed from closed trades. `metrics_definitions.md` updated v1.10.0. 7 unit tests in test_streak_metric.py.

---

### BLG-FE-19 — Keyboard shortcuts for trading actions

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-28
**Shipped in:** v3.0 (ST-11, cross-EPIC EPIC-02 branch, cycle 2026-04-25__release-v3.0)
**Evidence:** `docs/product/changelog.md` v3.0 entry; `claude/cycles/2026-04-25__release-v3.0/verification_report.md`

Keyboard shortcuts 'n', 'w', 'r' implemented in Layout.js via useEffect/keydown handler. Suppression rule for text inputs. Sidebar footer hint. Deviation documented: committed on EPIC-02 branch (co-delivered with Screener nav).

---

### BLG-FE-18 — Screener results page: attach news panel on DS-02 implementation

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-28
**Shipped in:** v3.0 (ST-07, cycle 2026-04-25__release-v3.0); resolves DEV-01 P3 from v2.9
**Evidence:** `docs/product/changelog.md` v3.0 entry; `claude/cycles/2026-04-25__release-v3.0/verification_report.md`

News panel attached to screener results page per screener_results.md §9. GET /news/{ticker} wired. Display-only per BLG-GOV-16 §13. UK tickers show '—' in news column. Strategy Rules Owner counter-sign applied.

---

### BLG-AI-02 — Model version contract for AI Journal

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-28
**Shipped in:** v3.0 (ST-16, cycle 2026-04-25__release-v3.0)
**Evidence:** `docs/product/changelog.md` v3.0 entry; `claude/cycles/2026-04-25__release-v3.0/verification_report.md`

Class 2 canonical spec created at docs/specs/ai_journal_model_contract.md. Model: claude-haiku-4-5-20251001 in ai_service.py _DEFAULT_MODEL. Contract referenced in ai_audit_service.py docstring.

---

### TEST-GAP-ST14 — AI audit service unit tests (ai_audit_service.py)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-28
**Shipped in:** v3.0 (ST-10, cycle 2026-04-25__release-v3.0)
**Evidence:** `docs/product/changelog.md` v3.0 entry; `claude/cycles/2026-04-25__release-v3.0/verification_report.md`

12 unit tests created in tests/test_ai_audit_service.py covering ensure_ai_audit_table, log_ai_summary_run, query_audit_log. Mock pattern — no live DB required. All pass in CI.

---

### BLG-OPS-14 — AI Journal monitoring metrics

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-28
**Shipped in:** v3.0 (ST-09, cycle 2026-04-25__release-v3.0)
**Evidence:** `docs/product/changelog.md` v3.0 entry; `claude/cycles/2026-04-25__release-v3.0/verification_report.md`

GET /health extended with ai_journal section: usage_rate, error_rate, p95_latency_ms sourced from ai_audit_log. Non-blocking — returns null/unavailable if data absent. 5 unit tests.

---

### BLG-OPS-12 — External API health check extension

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-04-28
**Shipped in:** v3.0 (ST-08, cycle 2026-04-25__release-v3.0)
**Evidence:** `docs/product/changelog.md` v3.0 entry; `claude/cycles/2026-04-25__release-v3.0/verification_report.md`

GET /health extended with external_apis section covering Alpaca and Yahoo Finance: last_successful_call, error_rate, p95_latency. Cache-based health check. 8 unit tests in test_health_extensions.py.

---

### BLG-FE-14 — Market Correlation frontend view

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-20
**Shipped in:** v2.8 (2026-04-17__release-v2.8 EPIC-01 ST-01)
**Evidence:** `docs/product/changelog.md` v2.8 entry; `claude/cycles/2026-04-17__release-v2.8/verification_report.md`

**Problem** `GET /analytics/market-correlation` was delivered in v2.7 (ST-08). AC-6 of ST-08 required a frontend view; deferred to v2.8. Completed as EPIC-01 ST-01 in v2.8.

**Acceptance Criteria met:** Per-position correlation and severity rendered with colour-coding; portfolio-level weighted average displayed; null values render gracefully; no regression to Analytics page.

---

### BLG-QA-13 — Test scenario coverage gap: market correlation and supplementary indicators (v2.7)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-20
**Shipped in:** v2.8 (2026-04-17__release-v2.8 EPIC-02 ST-02, ST-03)
**Evidence:** `docs/product/changelog.md` v2.8 entry; `claude/cycles/2026-04-17__release-v2.8/verification_report.md`

**Shipped:** SC-CORR-01 through SC-CORR-04 added to `docs/testing/analytics_scenarios.md`; SC-SIG-IND-01 through SC-SIG-IND-02 added to `docs/testing/signals_scenarios.md`. Test coverage gap closed. Playwright test suite consolidated (24/24 green).

---

### BLG-FEAT-16 — AI Journal Summarisation

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-20
**Shipped in:** v2.8 (2026-04-17__release-v2.8 EPIC-04 ST-07, ST-08)
**Evidence:** `docs/product/changelog.md` v2.8 entry; `claude/cycles/2026-04-17__release-v2.8/verification_report.md`

**§13 Status:** CONDITIONALLY COMPLIANT — SRB-v1.7. All 4 mandatory conditions met. Strategy Rules owner sign-off confirmed at EPIC-04 merge 2026-04-20.

**Shipped:** POST /api/ai/journal-summary and GET /api/ai/journal-summary/history delivered. AI summary displayed as UX convenience view with disclaimer label. No signal pipeline integration. External LLM API key managed via environment variable.

---

### BLG-GOV-13 — Deduplicate backlog_archive.md duplicate item headers

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-20
**Shipped in:** v2.8 (2026-04-17__release-v2.8 EPIC-03 ST-06)
**Evidence:** `docs/product/changelog.md` v2.8 entry; `claude/cycles/2026-04-17__release-v2.8/verification_report.md`

**Shipped:** backlog_archive.md deduplicated; duplicate `###` item headers resolved; Product Owner confirmation obtained; ID uniqueness scan PASS post-deduplication.

---

### v2.5 Release Slice — 2026-04-05__release-v2.5

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-04-10
**Shipped in:** v2.5 — Integration Baseline, Quick Wins & Governance Debt
**Evidence:** 13/13 items shipped; 12 backlog items completed; `claude/cycles/2026-04-05__release-v2.5/closure_record.md`

| ID | Title | Type | Sprint | Evidence |
|----|-------|------|--------|----------|
| BLG-OPS-12 | Fix auth forwarding in POST /test/endpoints | Ops | Sprint 1 | ST-01 commit 230643b |
| BLG-OPS-13 | Keep endpoint test list in sync with openapi.yaml | Ops | Sprint 1 | ST-02 commit a6a74c0 |
| BLG-FE-07 | Fix System Status endpoint categorisation | Frontend | Sprint 1 | ST-03 commit a6a74c0 |
| BLG-BE-08 | Review and document Reports page backend integration | Backend | Sprint 2 | ST-04 commit 3a645e3 |
| BLG-BE-09 | Review and document Signals page backend integration | Backend | Sprint 2 | ST-05 commit 3a645e3 |
| BLG-BE-07 | Investigate high external baseline latency | Backend | Sprint 2 | ST-06 commit 3f31b1d |
| BLG-OPS-11 | Add --max-time to GitHub Actions curl calls | Ops | Sprint 2 | ST-07 commit ce3775a |
| BLG-FE-08 | Fix Avg Slippage StatsCard gradient rendering | Frontend | Sprint 2 | ST-08 commit ce3775a |
| BLG-FEAT-15 | Fee drag metric on Trade History | Feature | Sprint 2 | ST-09 commit ce3775a |
| BLG-GOV-10 | Fix governance_sync.yml batch push issue closure | Gov | Sprint 1 | ST-10 commit 01f5e9c |
| BLG-GOV-12 | Formalise backlog entry placement standard | Gov | Sprint 1 | ST-11 commit dbb4551 |
| TEST-GAP-EPIC-01-v24 | Create test scenarios for EPIC-01 correctness fixes | QA | Sprint 1 | ST-13 commit aacbb50 |

---

### BLG-OPS-86 — Fix auth forwarding in POST /test/endpoints internal calls
**Renumbered from:** BLG-OPS-12 (ID collision resolved — v6.6 ST-03; BLG-OPS-12 retained by the earlier-archived entry "External API health check extension")
**Priority:** P2 (High)
**Type:** Operational / Infrastructure
**Owner:** Head of Engineering + Infrastructure & Operations Owner
**Source:** ST-11 performance baseline review — 2026-04-03
**Effort:** XS (<1h)
**Provisional-Target:** v2.5
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-01) — 2026-04-10 — cycle 2026-04-05__release-v2.5

**Problem**
`backend/services/health_service.py` `test_all_endpoints()` makes internal HTTP calls to each endpoint without forwarding the `X-API-Key` header. All auth-protected endpoints return 401 and are reported as "fail". The System Status page "Run Tests" button currently shows 1/17 pass rate, making the system appear critically broken when all endpoints are in fact operational. This makes the monitoring tool unreliable and misleading.

**Scope**
- Modify `test_all_endpoints()` to accept and forward the API key in internal calls (e.g. accept `api_key: str = None` parameter, add `X-API-Key` header when provided)
- Update `POST /test/endpoints` route in `main.py` to extract the `X-API-Key` from the incoming request and pass it through
- Alternatively: add a middleware bypass for server-internal calls (e.g. `X-Internal: true` header checked before auth)

**Acceptance Criteria**
- `POST /test/endpoints` returns pass/fail based on actual endpoint response, not auth rejection
- All correctly implemented endpoints report "pass" when the system is healthy
- Success rate shown on System Status page reflects actual endpoint health

---

### BLG-OPS-87 — Keep endpoint test list in sync with openapi.yaml
**Renumbered from:** BLG-OPS-13 (ID collision resolved — v6.6 ST-03; BLG-OPS-13 retained by the active backlog.md entry "Add new v2.8/v2.9/v3.0/v3.4/v3.9/v4.6 endpoints to api_performance_baseline.md re-run")
**Priority:** P3 (Low)
**Type:** Operational / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** ST-11 performance baseline review — 2026-04-03
**Effort:** XS (<1h)
**Provisional-Target:** v2.5
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-02) — 2026-04-10 — cycle 2026-04-05__release-v2.5

**Problem**
The endpoint test list in `backend/services/health_service.py` `test_all_endpoints()` was last updated for v2.2 (12 endpoints). Endpoints added in v2.3/v2.4 are not being tested. This coverage gap will worsen each sprint if not addressed structurally.

**Scope**
- Add all missing parameterless GET endpoints to the test list in `test_all_endpoints()`
- Add a comment block above the list referencing `docs/reference/openapi.yaml` as the source of truth
- Update the System Status page placeholder text to match actual endpoint count

**Acceptance Criteria**
- All parameterless GET endpoints in `openapi.yaml` are present in the test list
- A comment in `health_service.py` documents the sync obligation
- System Status page "Run Tests" button tests the complete current endpoint set

---

### BLG-FE-07 — Fix System Status endpoint categorisation for v2.3/v2.4 routes
**Priority:** P4 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Engineer
**Source:** System Status page review — 2026-04-03
**Effort:** XS (<1h)
**Provisional-Target:** v2.5
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-03) — 2026-04-10 — cycle 2026-04-05__release-v2.5

**Problem**
`src/pages/SystemStatus.js` `categorizeEndpoint()` does not cover routes added in v2.3/v2.4. Endpoints matching `/alerts`, `/notifications`, and `/digest` fall through to "Other" category.

**Scope**
- Add categorisation rules for Alerts, Notifications, Digest, verify Health/Analytics/Validation
- Add `categoryConfig` entries for "Alerts" and "Notifications"

**Acceptance Criteria**
- Alert endpoints appear under "Alerts" category
- Notification endpoints appear under "Notifications" category
- Digest endpoints appear under "Digest" category
- No endpoints fall into "Other" except `/`

---

### BLG-BE-08 — Review and document Reports page backend integration
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Frontend Integration
**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Source:** User session review — 2026-04-03
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.5
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-04) — 2026-04-10 — cycle 2026-04-05__release-v2.5 — see `docs/ops/reports_integration_review.md`

**Problem**
The Reports page is not fully integrated with the backend. No documentation mapping which Reports components are wired to which backend endpoints.

**Acceptance Criteria**
- A review document exists mapping each Reports page section to its backend endpoint
- All identified gaps have follow-up backlog items or are addressed
- Improvement proposals recorded for roadmap input

---

### BLG-BE-09 — Review and document Signals page backend integration
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Frontend Integration
**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Source:** User session review — 2026-04-03
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.5
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-05) — 2026-04-10 — cycle 2026-04-05__release-v2.5 — see `docs/ops/signals_integration_review.md`

**Problem**
The Signals page integration state is undocumented. Some sections may render without live data.

**Acceptance Criteria**
- A review document exists mapping each Signals page section to its backend endpoint
- All identified gaps have follow-up backlog items
- Improvement proposals recorded for roadmap input

---

### BLG-BE-07 — Investigate high external baseline latency on DB-backed endpoints
**Priority:** P2 (High)
**Type:** Backend / Infrastructure
**Owner:** Head of Engineering
**Source:** ST-11 performance baseline — 2026-04-03
**Effort:** M (~1–2 days)
**Provisional-Target:** v2.5
**Status:** Closed — investigation complete (ST-06, v2.5). See `docs/ops/api_performance_baseline.md` §6. Follow-up items: BLG-OPS-14 (Supavisor), BLG-BE-07-FIX (portfolio connection refactor).

**Problem**
All DB-backed endpoints have p50 response times of 1.2–6.0 seconds. Root cause: Supabase free tier connection overhead. GET /portfolio and GET /notifications/preferences were outliers.

**Acceptance Criteria**
- Root cause identified and documented
- Fix applied or architectural constraint documented
- Updated baseline document filed

---

### BLG-OPS-11 — Add `--max-time` to GitHub Actions cron curl calls
**Priority:** P3 (Low)
**Type:** Operational / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** InfraOps review of ST-10 Render tier decision record — 2026-04-02
**Effort:** XS (<1h)
**Provisional-Target:** v2.5
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-07) — 2026-04-10 — cycle 2026-04-05__release-v2.5

**Problem**
`alert-evaluation.yml` and `daily-snapshot.yml` invoke `curl` with no `--max-time` flag. Cold starts cause silent stall periods on Render free tier.

**Scope**
- Add `--max-time 120` to every `curl` call in both workflow files

**Acceptance Criteria**
- Both workflow files have `--max-time 120` on all curl invocations
- If service fails to respond within 120s workflow step fails with non-zero exit code

---

### BLG-FE-08 — Fix Avg Slippage StatsCard gradient rendering
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Frontend Specifications & UX Owner
**Source:** DEV-ST14-01 — delivery verification 2026-03-31__release-v2.4 — 2026-04-03
**Effort:** XS (<1 hour)
**Provisional-Target:** v2.5
**Deviation ref:** DEV-ST14-01 (P3 cosmetic — pre-accepted by Director of Quality 2026-03-20)
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-08) — 2026-04-10 — cycle 2026-04-05__release-v2.5

**Problem**
Avg Slippage StatsCard renders without gradient background. DEV-ST14-01 cosmetic deviation.

**Acceptance Criteria**
- Avg Slippage StatsCard renders with gradient background matching other StatsCards
- No regression to slippage value display or colour coding

---

### BLG-FEAT-15 — Fee drag metric on Trade History
**Priority:** P3 (Low)
**Type:** Feature — Analytics
**Owner:** Metrics Definitions & Analytics Owner + Head of Engineering
**Source:** PO/Challenger debate 2026-04-02 — action A3 from slippage metric re-scope decision
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v2.5
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-09) — 2026-04-10 — cycle 2026-04-05__release-v2.5

**Problem**
No always-available metric capturing friction cost of executing a trade. Fee drag = exit_fees / gross_proceeds × 100.

**Acceptance Criteria**
- `fee_drag_pct` field returned per trade; `avg_fee_drag_pct` at response envelope
- "Avg Fee Drag" StatsCard visible on Trade History
- Fee Drag % column present in TradeHistoryTable
- `docs/specs/metrics_definitions.md` contains canonical definition

---

### BLG-GOV-10 — Fix governance_sync.yml batch push issue closure
**Priority:** P2 (Medium)
**Type:** Governance Process / DevOps
**Owner:** DevOps
**Source:** EPIC-06 merge observation — delivery verification 2026-03-31__release-v2.4 — 2026-04-03
**Effort:** XS (<1 hour)
**Provisional-Target:** v2.5
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-10) — 2026-04-10 — cycle 2026-04-05__release-v2.5

**Problem**
`governance_sync.yml` uses `git log -1` — only closes the last commit's GitHub issue in a batch push.

**Scope**
- Update to `git log $BEFORE..$AFTER` to close all issues in push range

**Acceptance Criteria**
- Multi-commit batch push closes all referenced GitHub issues
- Single-commit push behaviour unchanged

---

### BLG-GOV-12 — Formalise backlog entry placement standard
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** User session review — 2026-04-03
**Effort:** XS (<1 hour)
**Provisional-Target:** v2.5
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-11) — 2026-04-10 — cycle 2026-04-05__release-v2.5

**Problem**
New backlog items were added to session sections instead of type-based sections. Fragments backlog structure.

**Acceptance Criteria**
- `lessons_learnt.md` has backlog-add placement rule entry
- Placement rule visible at top of `backlog.md`

---

### TEST-GAP-EPIC-01-v24 — Create test scenarios for EPIC-01 backend correctness fixes
**Priority:** P2 (Medium)
**Type:** QA Coverage
**Owner:** QA & Testing Owner
**Source:** Delivery verification 2026-03-31__release-v2.4 — TSG-v24-01 — 2026-04-03
**Effort:** S (~0.5 day)
**Provisional-Target:** v2.5
**Status:** ✅ COMPLETE — Shipped v2.5 (ST-13) — 2026-04-10 — cycle 2026-04-05__release-v2.5

**Problem**
EPIC-01 v2.4 shipped three correctness-critical fixes with no automated test scenarios.

**Scope**
- Author SC-ATR-01, SC-DEDUP-01/02, SC-STOP-01 in `docs/testing/`

**Acceptance Criteria**
- Scenario files present covering all four scenarios
- Each scenario executable against staging or unit test suite
- Referenced in test scenario index

---

### v2.4 Release Slice — 2026-03-31__release-v2.4

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-04-03
**Shipped in:** v2.4 — Correctness, Insight & Governance Hardening
**Evidence:** 17/17 items shipped; 13 backlog items completed; `claude/cycles/2026-03-31__release-v2.4/closure_record.md`

| ID | Title | Type | Sprint | Evidence |
|----|-------|------|--------|----------|
| BLG-BE-05 | Fix ATR pence→GBP conversion for all UK (.L) tickers | Backend Bug Fix | Sprint 2 (ST-01) | changelog.md v2.4; verification_report.md |
| BLG-BE-06 | Alert evaluation idempotency (notification deduplication) | Backend Engineering | Sprint 2 (ST-02) | changelog.md v2.4; verification_report.md |
| BLG-BE-04 | R-Multiple Analysis: stop price unavailable from trade_history | Backend / Data | Sprint 2 (ST-03) | changelog.md v2.4; verification_report.md |
| BLG-FE-06 | Fix missing P&L (GBP) column on Positions page | Frontend / UX | Sprint 2 (ST-04) | changelog.md v2.4; verification_report.md |
| BLG-FE-03 | User-facing error message mapping layer | Frontend / UX | Sprint 2 (ST-05) | changelog.md v2.4; verification_report.md |
| BLG-SPEC-D15 | Reconcile data_model.md portfolios table with actual deployed schema | Spec Debt | Sprint 1 (ST-06) | changelog.md v2.4; verification_report.md |
| BLG-SPEC-D16 | Reconcile data_model.md trade_history table with database.py column names | Spec Debt | Sprint 1 (ST-07) | changelog.md v2.4; verification_report.md |
| BLG-FEAT-14 | Weekly trading review digest | Product Feature | Sprint 3 (ST-08+ST-09) | changelog.md v2.4; verification_report.md |
| BLG-OPS-10 | Render hosting tier review | Operational / Infrastructure | Sprint 1 (ST-10) | changelog.md v2.4; verification_report.md |
| BLG-OPS-05 | API endpoint performance baseline | Operational / Observability | Sprint 2 (ST-11) | changelog.md v2.4; verification_report.md |
| TEST-GAP-EPIC-05-SLIP | Create slippage tracking test scenarios | QA Coverage | Sprint 1 (ST-12) | changelog.md v2.4; verification_report.md |
| BLG-GOV-09 | Cycle velocity metric | Governance Process | Sprint 1 (ST-13) | changelog.md v2.4; verification_report.md |
| BLG-GOV-03 | Simplify cycle artefact sealing (remove SHA-256, retain sealed flag) | Governance Process | Sprint 1 (ST-17) | changelog.md v2.4; verification_report.md |

---

### v2.3 Release Slice — 2026-03-24__release-v2.3

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-03-30
**Shipped in:** v2.3 — Quality Automation & User Insight
**Evidence:** 15 of 16 items shipped (ST-17 BLG-GOV-08 returned to backlog); `claude/cycles/2026-03-24__release-v2.3/closure_record.md`

<!-- release-plan-marker: RP:v2.3:2026-03-24__release-v2.3 -->

**Cycle:** 2026-03-24__release-v2.3
**Release:** v2.3 — Quality Automation & User Insight
**Planned:** 2026-03-24
**Shipped:** 2026-03-30
**Verification:** Verified_with_deviations
**Backlog slice:** `claude/cycles/2026-03-24__release-v2.3/stage4_backlog_slice.md`

Items in v2.3 sprint: EPIC-01 (ST-01 BLG-FEAT-11, ST-02 BLG-FEAT-09), EPIC-02 (ST-03 BLG-OPS-08, ST-04 BLG-QA-06, ST-05 BLG-QA-05, ST-06 BLG-QA-01), EPIC-03 (ST-07 BLG-SPEC-D14, ST-08 BLG-OPS-09, ST-09 BLG-OPS-07), EPIC-04 (ST-10 BLG-FE-05, ST-11 BLG-FE-04, ST-12 BLG-FE-02, ST-13 BLG-UX-01), EPIC-05 (ST-14 BLG-GOV-07, ST-15 BLG-QA-03, ST-16 BLG-QA-04, ST-17 BLG-GOV-08 [returned to backlog])

**Accepted deviations:** DEV-EPIC02-ST05-03 (P2, BLG-FE-06); V-CHART-05a/b/c (P2 staging gap, BLG-BE-04)

---

### v2.2 Release Slice — 2026-03-21__release-v2.2

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-03-24
**Shipped in:** v2.2 — Security, Alert Maturity & Quality
**Evidence:** All 15 items shipped; `claude/cycles/2026-03-21__release-v2.2/closure_record.md`

<!-- release-plan-marker: RP:v2.2:2026-03-21__release-v2.2 -->

**Cycle:** 2026-03-21__release-v2.2
**Release:** v2.2 — Security, Alert Maturity & Quality
**Planned:** 2026-03-21
**Shipped:** 2026-03-24
**Verification:** Verified_with_deviations
**Backlog slice:** `claude/cycles/2026-03-21__release-v2.2/stage4_backlog_slice.md`

Items in v2.2 sprint: EPIC-01 (ST-01 BLG-SEC-01, ST-02 BLG-SEC-02), EPIC-02 (ST-03 BLG-OPS-04, ST-04 BLG-FEAT-10, ST-05 BLG-FEAT-12), EPIC-03 (ST-06 BLG-BE-03, ST-07 BLG-FE-01, ST-08 BLG-OPS-06), EPIC-04 (ST-09 TEST-GAP-EPIC-02, ST-10 TEST-GAP-EPIC-03, ST-11 BLG-QA-02, ST-12 BLG-SPEC-T01), EPIC-05 (ST-13 BLG-GOV-04, ST-14 BLG-GOV-05, ST-15 BLG-GOV-06)

Full item definitions: in `claude/cycles/2026-03-21__release-v2.2/stage4_backlog_slice.md` and in `backlog.md` body (tombstoned in place per groom backlog 2026-03-24).

---

### v1.10 Release Slice — 2026-03-15__release-v1.10

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-03-16
**Shipped in:** v1.10 — Operations & Quality Foundation
**Evidence:** All EPICs shipped 2026-03-16; `claude/cycles/2026-03-15__release-v1.10/closure_record.md`

<!-- release-plan-marker: RP:v1.10:2026-03-15__release-v1.10 -->

**Cycle:** 2026-03-15__release-v1.10
**Release:** v1.10 — Operations & Quality Foundation
**Planned:** 2026-03-15
**Backlog slice:** `claude/cycles/2026-03-15__release-v1.10/stage4_backlog_slice.md`

Items in v1.10 sprint: EPIC-01 (ST-01–ST-03), EPIC-02 (ST-04), EPIC-03 (ST-05–ST-07)

---

### BLG-OPS-01 — Provision development environment
**Status:** ✅ COMPLETE — 2026-03-16 (cycle 2026-03-15__release-v1.10 / EPIC-01 ST-01–ST-03)
**Priority:** P1 (High — blocks safe QA workflow)
**Type:** Operations / Infrastructure
**Origin:** v1.9 Sprint 2 post-merge QA — raised 2026-03-13
**Target release:** v1.10 (prerequisite before Sprint 1 begins)

The project has no development environment. All QA must currently be performed against the production (`main`) deployment, which means:
- Bug fixes cannot be tested before they land in production
- The merge gate condition "QA sign-off on live app" forces merging to main before a human can test
- Post-merge bug discovery (as occurred in v1.9 Sprint 2) is the only available feedback loop

This creates a structural governance gap: the human Director of Quality sign-off rule requires testing a live running application, but there is no non-production environment to test against.

**Scope**
- Provision a staging/dev environment that tracks `main` (or a designated `staging` branch)
- Environment must run both frontend and backend with real (or seeded) data
- CI/CD pipeline should deploy to staging automatically on merge to `main`
- QA sign-off process updated to use staging URL, not production

**Acceptance Criteria**
- Staging environment accessible via a stable URL
- Deploys automatically when `main` is updated
- Governance process updated: QA sign-off block references staging URL
- Production is not the first place bugs are discovered

---

### BLG-API-01 — Backend API integration tests (FastAPI TestClient)
**Status:** ✅ COMPLETE — 2026-03-16 (cycle 2026-03-15__release-v1.10 / EPIC-03 ST-05–ST-06; P3 deviation DEV-ST05-01 for prospective-heat — BLG-BE-02 filed)
**Priority:** P2
**Type:** QA Infrastructure
**Owner:** QA & Testing Owner
**Source:** ST-11 decision session 2026-03-09 — Head of Engineering and Director of Quality identified gap
**Cycle added:** 2026-03-06__release-v1.9
**Target release:** v1.10

**Problem**
The Playwright mock layer (ST-11) tests frontend rendering behaviour given known API payloads. It does not test whether the backend `GET /portfolio` and `GET /portfolio/prospective-heat` routers return correctly-shaped responses for real database rows. The golden output gate tests pure-math functions; it does not test the router-to-service pipeline end-to-end.

**Scope**
- Add FastAPI `TestClient` integration tests for `GET /portfolio` and `GET /portfolio/prospective-heat` endpoints
- Use fixture data (no live DB required — inject via dependency override or in-memory SQLite)
- Verify: response shape matches `portfolio_endpoints.md` contract, GBP conversion applies for US positions, heat formula produces correct output for known inputs
- Add as a CI step in a new workflow or extend `golden-outputs.yml`

**Acceptance Criteria**
- `TestClient` tests present in `tests/` covering at minimum: portfolio endpoint response shape, US position GBP conversion, heat formula output, prospective-heat endpoint calculation
- Tests are CI-safe (no live DB, no external calls)
- Director of Quality confirms CI step present and passing

**Last Updated:** 2026-03-09

---

### TEST-GAP-EPIC-06 — v1.7 test scenario coverage gap (BLG-QA-01)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-16
**Shipped in:** v1.10 — Operations & Quality Foundation
**Evidence:** `claude/cycles/2026-03-15__release-v1.10/verification_report.md`; EPIC-03/ST-07

✅ COMPLETE — [TEST-GAP-EPIC-06] — 2026-03-16 (cycle 2026-03-15__release-v1.10 / EPIC-03 ST-07 / BLG-QA-01): 4 v1.7 QA scenario gaps authored and executed as GAP-01–GAP-04 in `docs/testing/v1.7-qa-scenario-gaps.md`. GAP-01 PASS, GAP-02 PASS, GAP-03 FAIL (new finding BLG-BE-01 P1 filed), GAP-04 BLOCKED (no closed trades in staging — deferred). BLG-QA-01 closed. Item retired.

---

### v1.9 Release Slice — 2026-03-06__release-v1.9

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-03-15
**Shipped in:** v1.9 — User Value & Insight
**Evidence:** Sprint 1 shipped 2026-03-09; Sprint 2 shipped 2026-03-13; `claude/cycles/2026-03-06__release-v1.9/verification_report.md`

<!-- release-plan-marker: RP:v1.9:2026-03-06__release-v1.9 -->

**Cycle:** 2026-03-06__release-v1.9
**Release:** v1.9 — User Value & Insight
**Planned:** 2026-03-06
**Backlog slice:** `claude/cycles/2026-03-06__release-v1.9/stage4_backlog_slice.md`

**Sprint 1 (✅ SHIPPED 2026-03-09):** EPIC-04 (ST-06–ST-10), EPIC-05 partial (ST-11, ST-13), EPIC-06 (ST-14–ST-19)
**Sprint 2 (✅ SHIPPED 2026-03-13):** EPIC-01 (ST-01–ST-02), EPIC-02 (ST-03, ST-05), EPIC-03 (ST-04), EPIC-05 partial (ST-12)

---

### v1.8 Release Slice — 2026-03-04__release-v1.8

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-03-15
**Shipped in:** v1.8 — Risk Dashboard
**Evidence:** All EPICs shipped 2026-03-05; `claude/cycles/2026-03-04__release-v1.8/closure_record.md`

<!-- release-plan-marker: RP:v1.8:2026-03-04__release-v1.8 -->

**Cycle:** 2026-03-04__release-v1.8
**Release:** v1.8 — Risk Dashboard
**Planned:** 2026-03-04
**Backlog slice:** `claude/cycles/2026-03-04__release-v1.8/stage4_backlog_slice.md`

Items in v1.8 sprint: EPIC-01 (ST-01–ST-04), EPIC-02 (ST-05–ST-08), EPIC-03 (ST-09–ST-10), EPIC-04 (ST-11–ST-12)

---

### BLG-FEAT-08 — Basic Compliance Metrics ✅ COMPLETE
**Priority:** P2
**Effort:** ~1 day
**Target release:** v1.9 (pre-work gate for Structured Trade Reflection Template)
**Closed:** 2026-03-13 | Cycle: 2026-03-06__release-v1.9 | EPIC-03/ST-01

Lightweight discipline metrics: journal completion rate, stop-based exit rate, average position size (% of portfolio). Definitions canonicalised in `metrics_definitions.md` first.

---

### BLG-NEW-09 — R-Multiple Distribution Report ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Analytics / User Value
**Owner:** Metrics Definitions & Analytics Owner
**Source:** IDEA-metrics-analytics-20260304-01, IW-20260304-01
**Cycle added:** 2026-03-06__item-3.4
**Closed:** 2026-03-13 | Cycle: 2026-03-06__release-v1.9 | EPIC-02/ST-04

**Problem**
No visualisation of R-multiple distribution existed. R-multiple is the canonical trade quality measure — users could not see whether trades were systematically achieving R > 1.

**Acceptance Criteria met**
- R-multiple formula defined and canonicalised in metrics_definitions.md
- Distribution visualisation present on analytics page
- Values computed from canonical backend formula; no client-side derivation

---

### BLG-NEW-10 — Canonical Test Scenario Library ✅ COMPLETE
**Priority:** P1 (High)
**Type:** QA Infrastructure
**Owner:** QA & Testing Owner
**Source:** IDEA-qa-testing-20260304-01, IW-20260304-01
**Cycle added:** 2026-03-06__item-3.4
**Closed:** Phase 1: 2026-03-09 | Phase 2: 2026-03-13 | Cycle: 2026-03-06__release-v1.9

Both phases delivered: seeded test infrastructure + TEST-GAP-EPIC-01 resolution (Phase 1); v1.9 feature scenarios added at delivery (Phase 2).

---

### BLG-NEW-11 — Canonical Terms Glossary ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Governance / Spec Quality
**Owner:** Head of Specs Team
**Cycle added:** 2026-03-06__item-3.4
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-14

Canonical terms glossary created as Class 2 Supporting document. All key trading and system terms defined with canonical source links. Registered in Specs_Index.md.

---

### BLG-NEW-12 — Service Layer Test Coverage Standard ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Engineering Quality / CI
**Owner:** Backend Engineering Patterns Owner
**Cycle added:** 2026-03-06__item-3.4
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-05/ST-13

Service Layer Test Coverage Standard authored. CI step enforces coverage threshold on services/ directory. Standard integrated with backend_engineering_patterns.md.

---

### BLG-NEW-04 — AI-Assisted Workflow Governance Policy ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Governance
**Owner:** Product Owner
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-15

AI-Assisted Workflow Governance Policy document authored and filed. Covers: scope of AI authority, mandatory human review checkpoints, escalation triggers, record-keeping obligations.

---

### BLG-RD-01 — Entity store fallback masks API error states ✅ COMPLETE
**Priority:** P2
**Type:** Frontend Defect — Error State Coverage
**Source:** DEV-ST03-01 — Delivery verification 2026-03-04__release-v1.8
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-08

Each Risk Dashboard component now renders its own error state when GET /portfolio fails. Entity fallback no longer silently masks failure.

---

### BLG-RD-02 — GracePeriodPanel empty vs error state ✅ COMPLETE
**Priority:** P3
**Type:** Frontend Defect — Error State UX
**Source:** DEV-ST03-02 — Delivery verification 2026-03-04__release-v1.8
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-08

GracePeriodPanel now renders a visible error card when portfolioError is set, distinct from the empty state.

---

### BLG-RD-03 — PositionRiskTable sorted descending ✅ COMPLETE
**Priority:** P2
**Type:** Frontend Defect — Sort Direction
**Source:** DEV-ST03-03
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-09

PositionRiskTable now sorts by stop distance ascending (tightest stop first) per spec §6.4.

---

### BLG-RD-04 — Stop Price column absent ✅ COMPLETE
**Priority:** P2
**Type:** Frontend Defect — Missing Column
**Source:** DEV-ST03-04
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-09

Stop Price column (current_stop, GBP, 2dp) now present in PositionRiskTable per spec §6.2.

---

### BLG-RD-05 — GRACE badge colour ✅ COMPLETE
**Priority:** P3
**Type:** Frontend Defect — Cosmetic
**Source:** DEV-ST03-05
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-10

GRACE state badge now rendered in blue per spec §6.3.

---

### BLG-RD-06 — GBP value at risk absent from HeatGauge ✅ COMPLETE
**Priority:** P3
**Type:** Frontend Defect — Missing Metric
**Source:** DEV-ST03-06
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-10

GBP value at risk now displayed below gauge value per spec §3.2.

---

### BLG-RD-07 — Days in Grace column absent ✅ COMPLETE
**Priority:** P3
**Type:** Frontend Defect — Missing Column
**Source:** DEV-ST03-07
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-09

Days in Grace (holding_days) column now present in Grace Period table per spec §5.2.

---

### BLG-RD-08 — Drawdown data source resolved ✅ RESOLVED
**Priority:** P2
**Type:** Spec Alignment — Owner Decision
**Source:** DEV-ST03-08
**Closed:** 2026-03-06 | ST-06 investigation

Split-source data model confirmed: current_drawdown_percent from GET /portfolio (drawdown_service.py); days_underwater from GET /analytics/metrics (analytics_service.py). risk_dashboard.md §4.1 updated to v0.1.7 to reflect correct split sources.

---

### BLG-RD-09 — ProspectiveHeatPanel missing threshold label ✅ COMPLETE
**Priority:** P3
**Type:** Frontend Defect — Missing Display Element
**Source:** DEV-ST03-09
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-09

Threshold label badge now present in prospective heat result row, updating when boundary is crossed per §7.5.

---

### BLG-RD-10 — US entry prices in USD not GBP ✅ COMPLETE
**Priority:** P2
**Type:** Backend + Frontend Defect — Currency Conversion
**Source:** DEV-ST03-11
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-07

portfolio_service.py now converts entry_price to GBP for US positions. Risk Dashboard displays entry prices in GBP for all positions per §6.2.

---

### BLG-RD-11 — current_stop in USD for US positions ✅ COMPLETE
**Priority:** P2
**Type:** Backend + Frontend Defect — Currency Conversion
**Source:** DEV-ST03-12
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-04/ST-07

portfolio_service.py now converts current_stop to GBP for US positions. Stop Distance % calculation uses matching currencies per §6.2.

---

### TEST-GAP-EPIC-01 — Risk Dashboard scenario infrastructure gap ✅ CLOSED
**Priority:** P2
**Type:** QA Infrastructure
**Source:** Delivery verification 2026-03-04__release-v1.8
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | ST-11

Playwright mock layer delivered. All 17 unexecuted scenarios automated in tests/e2e/risk-dashboard.spec.js. CI gate at .github/workflows/playwright.yml. Mock data in tests/e2e/mocks/portfolio-mock-data.js. Scenario document updated to v1.1.

---

### BLG-SPEC-D1 — API Contracts README.md version frozen at v1.8.4 ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Documentation Drift
**Owner:** API Contracts & Documentation Owner
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

README.md version header updated to v1.9.0. Changelog includes v1.9.0 entry referencing EPIC-06 changes.

---

### BLG-SPEC-D3 — GET /market/status completely undocumented ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Documentation Gap / Drift
**Owner:** API Contracts & Documentation Owner
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-16

docs/specs/api_contracts/market_endpoints.md created. Endpoint documented, registered in Specs_Index.md, added to openapi.yaml.

---

### BLG-SPEC-D4 — GET /positions/search/tags undocumented ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Documentation Gap
**Owner:** API Contracts & Documentation Owner
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

position_endpoints.md now includes GET /positions/search/tags with request parameters and response schema.

---

### BLG-SPEC-D8 — System_status_report.md missing lifecycle header ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Lifecycle Compliance Drift
**Owner:** Director of Quality
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

Lifecycle header added to docs/System_status_report.md. Class and Status assigned per document_lifecycle_guide.md.

---

### BLG-SPEC-D9 — process_index.md and Specs_Index.md wrong path for lifecycle guide ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Documentation Drift / Broken Cross-Reference
**Owner:** Head of Specs Team
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

Both process_index.md and Specs_Index.md §5 updated to reference claude/charter/document_lifecycle_guide.md.

---

### BLG-SPEC-G1 — settings_model.md missing ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Spec Gap
**Owner:** Head of Specs Team
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-17

settings_model.md created in docs/specs/data_model/. Registered in Specs_Index.md §3. Cross-referenced from settings_endpoints.md.

---

### BLG-SPEC-G2 — Error Response Standard not defined ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Spec Gap
**Owner:** API Contracts & Documentation Owner
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-18

Error Response Standard document created. Standard error envelope shape, required fields, HTTP status code mapping defined. All existing API contract docs reference the standard. Registered in Specs_Index.md.

---

### BLG-SPEC-G3 — structured_logging_standards.md not in Specs_Index ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Index Gap
**Owner:** Head of Specs Team
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

Specs_Index.md §3 updated to include structured_logging_standards.md with Owner, Class, Status, Version.

---

### BLG-SPEC-G4 — ADR-002 in wrong location ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Governance Organisation Gap
**Owner:** Head of Specs Team
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

ADR-002 moved to docs/product/decisions/. Cross-references updated.

---

### BLG-SPEC-G5 — validation_system.md owner non-compliant ✅ COMPLETE
**Priority:** P3 (Low)
**Type:** Lifecycle Compliance Gap
**Owner:** Infrastructure & Operations Owner
**Closed:** 2026-03-09 | Cycle: 2026-03-06__release-v1.9 | EPIC-06/ST-19

validation_system.md owner field updated to a named governance role. Specs_Index.md §7.1 notation updated to reflect resolved.

---

### BLG-NEW-08 — Automated OpenAPI Drift Detection in CI ✅ COMPLETE
**Priority:** P1 (High)
**Type:** CI / Governance
**Owner:** Engineering (CI)
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-08

**Problem**
`docs/reference/openapi.yaml` was not updated during EPIC-06 when three contracts were bumped to v1.9.0 (BLG-SPEC-D7). There is no CI check that detects drift between the markdown API contracts and openapi.yaml. Drift will recur without an automated gate.

**Scope**
- Add a CI step that detects drift between `openapi.yaml` and the markdown API contracts
- Approach: either (a) generate openapi.yaml from contracts and compare, or (b) run a custom lint/diff check against known contract fields
- Block merge on detected drift

**Acceptance Criteria**
- CI step detects drift between openapi.yaml and markdown contracts
- Merge blocked if drift is detected
- Approach documented (generation vs diff) — approach decision to be made in pre-alignment

---

### BLG-NEW-07 — Running API Changelog Document ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Documentation / Governance
**Owner:** API Contracts & Documentation Owner
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-12

**Problem**
There is no single running changelog document for API contract changes. Changes to endpoint contracts (new fields, removed fields, version bumps) are recorded in individual spec files but there is no centralised, human-readable history of API evolution across versions.

**Scope**
- Create a running API Changelog document that summarises contract changes per version
- Cover all contracts under `docs/specs/api_contracts/`
- Backfill from v1.8.x → v1.9.0 changes (EPIC-06 scope)
- Document maintainer obligation: must be updated alongside every contract version bump

**Acceptance Criteria**
- API Changelog document exists and is registered in Specs_Index.md
- All v1.9.0 contract changes (EPIC-06) are backfilled
- Maintenance obligation documented alongside contract spec authoring workflow

---

### BLG-NEW-05 — Dependency Vulnerability Scanning in CI ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Security / CI
**Owner:** Engineering (CI)
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-07

**Problem**
There is no automated scanning of Python dependencies for known vulnerabilities in the CI pipeline. A compromised or vulnerable dependency could be introduced silently.

**Scope**
- Add a CI step that scans Python dependencies (e.g., using `pip-audit` or `safety`) for known CVEs
- Block merge (or warn at configurable severity) on high/critical vulnerabilities
- Integrate with existing `.github/workflows/` structure

**Acceptance Criteria**
- Dependency vulnerability scan runs on every PR
- High/critical CVEs block merge (or produce a required review comment)
- Scan tool and severity threshold documented

---

### BLG-NEW-03 — Define and Document Unavailability Failure Mode ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Policy / Governance
**Owner:** Infrastructure & Operations Owner
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Effort:** ~0.5 day
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-11

**Problem**
There is no documented policy for what happens when the system is unavailable during a trading session (e.g., backend down, market data feed unavailable). The system has no documented failure modes or fallback procedures for the user.

**Scope**
- Define and document the unavailability failure mode: what the user should do, what the system state is, and any manual fallback procedures
- Document where this policy lives (e.g., OPERATIONAL_GUIDE.md or a new docs/ops/ document)

**Acceptance Criteria**
- Unavailability failure mode documented: system states covered, user action required, data integrity implications
- Document registered in appropriate governance index

---

### BLG-NEW-02 — Backtest vs Live Stop Reconciliation Report ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Quality / CI
**Owner:** Engineering + QA
**Source:** IW-20260304-01 (promoted 2026-03-04)
**Cycle added:** 2026-03-04__item-3.4
**Dependency:** After BLG-NEW-01 (golden output baseline must be in place first)
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-06

**Problem**
There is no automated verification that the trailing stop formula used in backtests and the formula used in the live system produce identical results for the same inputs. Silent divergence between backtest and live logic is a category of defect that cannot be caught by either gate independently.

**Scope**
- Report or CI assertion that compares backtest stop calculations vs live system stop calculations for a set of known inputs
- Output: reconciliation result confirming parity or flagging divergence

**Acceptance Criteria**
- Automated check exists that verifies backtest and live stop logic produce identical results for all golden inputs
- Any divergence between backtest and live calculation fails the check

---

### BLG-NEW-01 — Golden Output Regression Baseline for CI ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Quality / CI
**Owner:** Engineering + QA
**Source:** IDEA-director-of-quality-20260304-02 — Director of Quality, IW-20260304-01
**Cycle added:** 2026-03-04__item-3.4
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-05

**Problem**
The current CI gate (`POST /validate/calculations`, EPIC-01) checks only that `critical_failed > 0` blocks the merge. It does not verify that specific calculations return the correct numeric values. A change that silently alters the trailing stop formula from `CurrentPrice - (2 × ATR)` to `CurrentPrice - (2.1 × ATR)` would pass the current gate. Numeric regressions are the highest-risk defect class in a trading system.

**Scope**
- Define a set of deterministic golden test cases: known inputs (entry_price, ATR, risk_percent, etc.) with expected output values derived directly from the canonical strategy spec
- Store as `tests/golden_outputs.json` — treated as a canonical artefact; updated only via spec-linked PR
- Scope limited to stop/sizing calculations only (per STEP 5 scoping from IW-20260304-01)
- Add a CI step that calls the backend with each golden input and asserts output matches to required precision
- Any numeric divergence from golden values fails the build

**Acceptance Criteria**
- `tests/golden_outputs.json` exists with spec-derived golden values for stop and sizing calculations
- CI step added that runs golden output assertions on every PR
- Build fails on any numeric deviation from golden values
- Precision tolerance documented (e.g., 4 decimal places for share counts)
- Golden values derived from canonical spec, not from current implementation

**Dependencies**
- None (prerequisite: BLG-NEW-02 must follow, not precede)

---

### BLG-SPEC-D7 — openapi.yaml frozen at v1.8.1; not updated for v1.9.0 contracts ✅ COMPLETE
**Priority:** P2 (Medium)
**Type:** Documentation Drift / Reference Artefact Staleness
**Owner:** API Contracts & Documentation Owner
**Raised:** 2026-03-03 — Head of Specs Team review
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-10 — openapi.yaml updated to v1.9.0

**Problem**
`docs/reference/openapi.yaml` is at version 1.8.1 (1193 lines).
Three contracts were bumped to v1.9.0 in EPIC-06:
- `sharpe_ratio_trade_method` absent from /validate/calculations validated metrics list
- portfolio positions response schema not aligned to v1.9.0 field list
- `holding_days` absent from GET /trades trade object schema
Specs_Index.md §4 states: "openapi.yaml must be reviewed inline with every contract change; markdown contracts take precedence on conflict."
This was not done during EPIC-06.

**Acceptance Criteria**
- openapi.yaml version field updated to 1.9.0
- /validate/calculations response includes sharpe_ratio_trade_method (14 validated metrics total)
- GET /trades trade object includes holding_days (integer)
- GET /portfolio positions objects reflect v1.9.0 field list
- No conflicts between openapi.yaml and markdown contracts

---

### BLG-SPEC-D2 — settings_endpoints.md spec/implementation mismatch ✅ COMPLETE
**Priority:** P1 (High)
**Type:** Spec–Implementation Drift
**Owner:** API Contracts & Documentation Owner + Head of Engineering
**Raised:** 2026-03-03 — Head of Specs Team review
**Closed:** 2026-03-06 | Cycle: 2026-03-04__release-v1.8 | ST-09 — settings_endpoints.md v1.1.0 published; PATCH/POST documented as canonical

**Problem**
`docs/specs/api_contracts/settings_endpoints.md` specifies `PUT /settings` (replace all settings).
Live implementation in `backend/main.py` uses `PATCH /settings/{settings_id}` (update single setting by ID).
Additionally, `POST /settings` is implemented but not documented anywhere.
This is a P1 drift: clients relying on the spec will call the wrong method and path.

**Decision Required**
Product Owner + API Contracts owner to choose:
(a) Update spec to document `PATCH /settings/{settings_id}` and `POST /settings` as the canonical interface, or
(b) Align backend to implement `PUT /settings` as specced (breaking change to existing frontend).

**Acceptance Criteria**
- settings_endpoints.md accurately documents the live HTTP method, path, and request/response schema
- No divergence between spec and implementation
- Decision record filed if option (b) chosen (breaking change)

---

### §6 v1.7 Release Slice — 2026-03-02__release-v1.7

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-03-04
**Shipped in:** v1.7
**Evidence:** All 6 EPICs shipped 2026-03-03; verified 2026-03-03 — `claude/cycles/2026-03-02__release-v1.7/verification_report.md`

<!-- release-plan-marker: RP:v1.7:2026-03-02__release-v1.7 -->

**Cycle:** 2026-03-02__release-v1.7
**Planning Date:** 2026-03-02
**Status:** ✅ Complete — all 6 EPICs shipped 2026-03-03; verified 2026-03-03
**Reference:** claude/cycles/2026-03-02__release-v1.7/stage4_backlog_slice.md

| S2 ID | Item | Epic | Priority | Effort |
|-------|------|------|----------|--------|
| S2-01 | BLG-TECH-04 — CI/CD GitHub Actions Validation Workflow | EPIC-01 | P2 | ~1 day |
| S2-02 | Strategy Rules §13 Boundary Review | EPIC-02 | P1 | ~0.5 day |
| S2-03 | Metrics Definitions — Portfolio Heat Formula & Thresholds | EPIC-03 | P1 | ~0.5 day |
| S2-04 | Structured Logging / Observability Standards | EPIC-04 | P2 | ~1 day |
| S2-05 | API Versioning Strategy Decision Record | EPIC-05 | P2 | ~0.5 day |
| S2-06 | BLG-TECH-06 — Canonicalise sharpe_ratio_trade_method | EPIC-06 | P2 | ~30 min–1 hr |
| S2-07 | BLG-TECH-08 — Align portfolio_endpoints.md positions summary | EPIC-06 | P3 | ~30 min + decision |
| S2-08 | BLG-TECH-09 — Add holding_days to GET /trades | EPIC-06 | P3 | ~30 min + decision |

**Total estimated effort:** ~3.5–4 days
**Capacity assessment:** PASS (workforce_capacity.md — no constraints violated)
**Key gates unlocked by this release:**
- EPIC-02 → §13-gated features may enter pre-alignment
- EPIC-03 → v1.8 Risk Dashboard pre-alignment
- EPIC-04 + EPIC-05 → v2.0 Alerts pre-alignment (2 of 3 gates)

---

### BLG-SPEC-D6 — changelog.md has no v1.7 entry

**Status at retirement:** ✅ Complete — Resolved
**Priority at retirement:** P3
**Retired:** 2026-03-04
**Shipped in:** N/A — documentation fix
**Evidence:** v1.7 entry confirmed present in `docs/product/changelog.md` (verified 2026-03-04)

**BLG-SPEC-D6** — changelog.md has no v1.7 entry
**Priority:** P3 (Low)
**Type:** Documentation Drift
**Owner:** Product Owner
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`docs/product/changelog.md` last entry is v1.6.1 (2026-03-01).
v1.7 Foundation & Governance sprint was fully delivered and verified (2026-03-03).
No entry exists for v1.7.

**Acceptance Criteria**
- v1.7 changelog entry added covering: CI/CD merge gate (EPIC-01), §13 boundary review (EPIC-02), Portfolio Heat metrics (EPIC-03), Structured Logging Standards (EPIC-04), API Versioning Decision Record (EPIC-05), Spec Debt Resolution — analytics/portfolio/trade endpoints v1.9.0 (EPIC-06)

---

### BLG-SPEC-D5 — current_roadmap.md v1.7 section not closed out

**Status at retirement:** ✅ Complete — Resolved
**Priority at retirement:** P3
**Retired:** 2026-03-04
**Shipped in:** N/A — documentation fix
**Evidence:** Resolved by `manage roadmap` run 2026-03-04 — v1.7 section retired to `claude/roadmap/roadmap_archive.md`; release summary updated; footer already referenced correct backlog path

**BLG-SPEC-D5** — current_roadmap.md v1.7 section not closed out
**Priority:** P3 (Low)
**Type:** Documentation Drift
**Owner:** Product Owner
**Raised:** 2026-03-03 — Head of Specs Team review

**Problem**
`claude/roadmap/current_roadmap.md` v1.7 section items still show "Status: Planned".
Release Summary table has no ✅ for v1.7.
v1.7 was fully delivered (2026-03-02) and verified (2026-03-03).
Additionally, footer references `docs/product/feature_backlog.md` which does not exist (actual backlog: `claude/backlog/backlog.md`).

**Acceptance Criteria**
- v1.7 section marked Complete with delivery date
- Release Summary table updated (✅ v1.7)
- Footer corrected to reference correct backlog path

---

### BLG-NEW-06 — Realised vs Unrealised P&L Labelling

**Status at retirement:** ❌ Killed — merged into 4.1b pre-work scope
**Priority at retirement:** N/A
**Retired:** 2026-03-04
**Shipped in:** N/A — merged
**Evidence:** DL-005 (2026-03-04); merged into roadmap item 4.1b Tax-Year P&L Statement pre-work scope

**BLG-NEW-06** — Realised vs Unrealised P&L Labelling
**Status:** Merged into 4.1b pre-work scope — not a standalone backlog item
**Source:** IW-20260304-01
**Cycle added:** 2026-03-04__item-3.4

This item (clear distinction of realised vs unrealised P&L amounts in the tax-year P&L statement) has been merged into the 4.1b Tax-Year P&L Statement scope as pre-work. See current_roadmap.md §4.1b scope note (2026-03-04). No standalone delivery required.

---

### BLG-TECH-09 — Add holding_days to GET /trades

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-04
**Shipped in:** v1.7
**Evidence:** Cycle 2026-03-02__release-v1.7, EPIC-06/TASK-28–30; `claude/cycles/2026-03-02__release-v1.7/verification_report.md`

**BLG-TECH-09** — Add holding_days to GET /trades
**Priority:** P3
**Effort:** ~1 hour
**Target release:** v1.7
**Status:** ✅ COMPLETE — 2026-03-03 (cycle: 2026-03-02__release-v1.7, EPIC-06/TASK-28–30; backend fix path chosen)
**Source:** OBS-QWB-R3-01 — QA Lead observation, QWB verification, 2026-03-01
holding_days is absent from trade objects in the GET /trades response.
trade_endpoints.md v1.8.4 lists it as a required field. Pre-existing behaviour,
not introduced by QWB.
Decision required: Either (a) add holding_days to the backend GET /trades
response (the spec-compliant fix); or (b) remove holding_days from trade_endpoints.md
documented schema. Product Owner + API Contracts owner to decide.
Acceptance Criteria

GET /trades trade objects include holding_days (integer), OR
trade_endpoints.md schema is corrected to remove the field, with a note explaining
its absence and where the value can be sourced (e.g. trades_for_charts)

**Owner:** API Contracts & Documentation Owner
Raised by: QA Lead, 2026-03-01

---

### BLG-TECH-08 — Align portfolio_endpoints.md positions summary field list

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-03-04
**Shipped in:** v1.7
**Evidence:** Cycle 2026-03-02__release-v1.7, EPIC-06/TASK-25–27; `claude/cycles/2026-03-02__release-v1.7/verification_report.md`

**BLG-TECH-08** — Align portfolio_endpoints.md positions summary field list
**Priority:** P3
**Effort:** ~30 min
**Target release:** v1.7
**Status:** ✅ COMPLETE — 2026-03-03 (cycle: 2026-03-02__release-v1.7, EPIC-06/TASK-25–27; spec update path chosen)
**Source:** OBS-QWB-R1-01 — QA Lead observation, QWB verification, 2026-03-01
GET /portfolio positions summary objects omit current_price_native, stop_price,
stop_price_native, and pnl_percent — fields listed in R-01 test scenario step 3
and in portfolio_endpoints.md. Pre-existing behaviour, not introduced by QWB.
Decision required: Either (a) update portfolio_endpoints.md to accurately document
the lightweight summary shape, explicitly distinguishing it from the full position object
on GET /positions; or (b) add the missing fields to the backend response. Product Owner

API Contracts owner to decide.

**Acceptance Criteria**

portfolio_endpoints.md positions summary field list matches the live API response
No discrepancy between spec and implementation for /portfolio positions objects

Owner: API Contracts & Documentation Owner
Raised by: QA Lead, 2026-03-01

---

### BLG-TECH-06 — Canonicalise sharpe_ratio_trade_method as 14th validation metric

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-03-04
**Shipped in:** v1.7
**Evidence:** Cycle 2026-03-02__release-v1.7, EPIC-06/TASK-21–24; `claude/cycles/2026-03-02__release-v1.7/verification_report.md`

**BLG-TECH-06** — Canonicalise sharpe_ratio_trade_method as 14th validation metric in analytics_endpoints.md
**Priority:** P2 (Medium)
**Type:** Spec Accuracy / Governance
**Target release:** v1.7 *(updated from v1.6.1 — v1.6.1 has shipped; DL-001 cycle 2026-03-01__item-3.2)*
**Status:** ✅ COMPLETE — 2026-03-03 (cycle: 2026-03-02__release-v1.7, EPIC-06/TASK-21–24)
**Problem**
POST /validate/calculations returns 14 validation results. analytics_endpoints.md v1.8.1
describes 13 metrics and does not document sharpe_ratio_trade_method.
The 14th metric was introduced under BLG-TECH-01 Addendum 1 (PMO-confirmed scope, 2026-02-20)
to exercise the trade-based Sharpe fallback path. The implementation is correct and the result
passes. The spec is incomplete.
This was recorded as OBS-01 by the QA Lead during BLG-TECH-02/03 re-verification
(2026-02-21T21:25:00Z) and formally acknowledged by the Product Owner (2026-02-21).
Per document_lifecycle_guide.md v2.2 — deviation must have priority, target release,
and owner at time of documentation. These are recorded here.
Scope

Update analytics_endpoints.md to add sharpe_ratio_trade_method as a formally
documented 14th validation metric
Add to the validated metrics table with: severity critical, formula, tolerance
Update the response example to show 14 results and correct by_severity.critical.total: 4
No code change required — implementation is correct

**Acceptance Criteria**

analytics_endpoints.md validated metrics table includes sharpe_ratio_trade_method
Response schema example reflects 14 results
by_severity.critical.total shown as 4 in example (not 3)
No deviation exists between the spec and the live POST /validate/calculations response

**Owner**

API Contracts & Documentation Owner

**Source**

OBS-01 — QA Lead, BLG-TECH-02/03 re-verification, 2026-02-21T21:25:00Z
Product Owner disposition: backlog item, v1.6.1 target, 2026-02-21

---

### BLG-TECH-04 — CI/CD validation workflow (GitHub Actions)
**Priority:** P2 (Medium)
**Type:** Delivery Quality / Automation
**Status:** ✅ COMPLETE — 2026-03-03 (cycle: 2026-03-02__release-v1.7, EPIC-01)
**Target release:** v1.7

**Problem**
- Validation is manual and not enforced at merge time.

**Scope**
- Add `.github/workflows/validate-analytics.yml`.
- Run `POST /validate/calculations` on:
  - Pull requests
  - Pushes to `main` and `develop`
- Block merge if any **critical-severity** validation fails.
- Post validation summary as PR comment.

**Acceptance Criteria**
- Workflow reliably runs on all PRs.
- Merge is blocked only for critical severity failures.
- Clear PR feedback is visible.

**Dependencies**
- BLG-TECH-02 (severity model must exist).

**Owners**
- Engineering
- QA

---

### BLG-FEAT-07 — CSV Export of Trade History
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

One-click CSV export for tax and analysis use.

---

### BLG-FEAT-06 — Grace Period Indicator
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

Show remaining grace period days in open positions table.
Example: "Day 6 of 10"

---

### BLG-FEAT-05 — Win Rate by Month Chart
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

Bar chart of win rate grouped by calendar month.

---

### BLG-FEAT-04 — Best / Worst Trades Widget
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

Show top 3 and bottom 3 trades by R-multiple or P&L.

---

### BLG-FEAT-02 — R-Multiple Column in Trade History
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

Add R-multiple column to trade history table.

**Indicative Formula**

`(Exit Price - Entry Price) / (Entry Price - Stop Price)`

**Notes**
- Formula must be confirmed by Metrics Definitions owner.
- Decide server-side vs frontend-only calculation.

---

### BLG-FEAT-01 — Current Drawdown Widget
**Status:** ✅ COMPLETE
**Shipped:** v1.6.1, 2026-03-01
**Evidence:** docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
**Changelog:** docs/product/changelog.md v1.6.1

Display current drawdown from peak and days underwater.
Example: "Drawdown: -8.2%, 12 days underwater"

**Dependency**
- Metrics Definitions owner must confirm drawdown calculation before implementation.

---

### BLG-TECH-03 — Consolidate ValidationService into service layer

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-04
**Shipped in:** v1.6.1 (co-delivered with BLG-TECH-02)
**Evidence:** Director of Quality sign-off 2026-02-21T21:30:00Z; `docs/product/phase_gates/BLG-TECH-03-validationservice-consolidation-phase-gate.md`

BLG-TECH-03 — Consolidate ValidationService into service layer
Priority: P1 (High)
Type: Architecture / Maintainability
Status: ✅ COMPLETE — 2026-02-21
Closed

All validation logic moved from routers/validation.py into services/validation_service.py
Router thinned to HTTP in/out only — delegates entirely to ValidationService.validate_all()
Stub replaced with full 13-metric + trade-Sharpe implementation
Delivered in same branch as BLG-TECH-02 per co-delivery constraint
Director of Quality sign-off: 2026-02-21T21:30:00Z
Phase Gate Document filed: docs/product/phase_gates/BLG-TECH-03-validationservice-consolidation-phase-gate.md

---

### BLG-TECH-02 — Implement validation severity model

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-03-04
**Shipped in:** v1.6.1
**Evidence:** Director of Quality sign-off 2026-02-21T21:30:00Z; `docs/product/phase_gates/BLG-TECH-02-validation-severity-model-phase-gate.md`

BLG-TECH-02 — Implement validation severity model
Priority: P1 (High)
Type: Governance / Operational Control
Status: ✅ COMPLETE — 2026-02-21
Closed

severity field added to every validation result object (critical / high / medium / low)
by_severity aggregation added to summary — all four tiers always present
Severity mapping implemented in ValidationService per analytics_endpoints.md v1.8.1
Director of Quality sign-off: 2026-02-21T21:30:00Z
Phase Gate Document filed: docs/product/phase_gates/BLG-TECH-02-validation-severity-model-phase-gate.md

---

### BLG-TECH-01 — Fix Sharpe variance method + Capital Efficiency currency basis
**Priority:** P0 (Critical)
**Type:** Metrics Correctness / Validation Integrity
**Status:** ✅ COMPLETE — 2026-02-21

**Closed**
- `_calculate_sharpe()` updated to use sample variance (÷ n−1) for portfolio and trade-level Sharpe methods
- Capital efficiency updated to use `Mean(total_cost)` in GBP from `trade_history`
- `validation_data.py` expected values updated: `capital_efficiency` 0.17 → 0.22; `total_cost` fields added
- Validation: 13/13 pass confirmed at 2026-02-21T00:24:41Z
- Canonical Owner sign-off: 2026-02-21
- `metrics_definitions.md` v1.5.7 — Appendix E both items marked resolved
- `analytics_endpoints.md` v1.8.1 — resolved known limitations removed
- v1.6 quality gate: satisfied

---

### v2.0 Release Items — 2026-03-17__release-v2.0 (Backlog Grooming 2026-03-17)

**Retired:** 2026-03-17
**Shipped in:** v2.0 — Reporting & Alerts
**Evidence:** `claude/cycles/2026-03-17__release-v2.0/verification_report.md`; `closure_record.md`

---

### TEST-GAP-EPIC-02 — CohortAnalysis backend integration regression scenario
**Priority:** P3
**Type:** QA / Test Coverage
**Owner:** QA & Testing Owner
**Source:** TSG-V110-01 — verification_report.md §6, cycle 2026-03-15__release-v1.10
**Cycle added:** 2026-03-15__release-v1.10
**Target release:** before next sprint touching analytics components

Test scenario coverage gap from 2026-03-15__release-v1.10: QA & Testing Owner to author CohortAnalysis backend integration regression scenario (`SC-CA-BACKEND-01`) covering: period toggle (Monthly / Quarterly / Yearly) triggers API refetch and table updates; `has_enough_data = false` shows insufficient data warning; column values match `GET /analytics/cohort` response fields. Spec references: `docs/specs/frontend/pages/analytics.md §15`; `docs/specs/api_contracts/analytics_endpoints.md#GET /analytics/cohort`. Register in `docs/testing/risk_dashboard_scenarios.md` or new `analytics_scenarios.md`.

---

### BLG-BE-02 — Spec and implement GET /portfolio/prospective-heat endpoint
**Priority:** P3
**Type:** Backend + Spec
**Owner:** Head of Engineering + Head of Specs Team
**Source:** DEV-ST05-01 — ST-05 (v1.10 EPIC-03) integration tests could not cover this endpoint because it is absent from `portfolio_endpoints.md` and not implemented in `backend/main.py`. Discovered during sprint execution 2026-03-16.
**Cycle added:** 2026-03-15__release-v1.10
**Target release:** v2.0 (or earlier if ProspectiveHeatPanel becomes a priority)

**Problem**
The ProspectiveHeatPanel frontend component exists and makes reference to portfolio heat projection, but `GET /portfolio/prospective-heat` (a prospective heat calculation endpoint) is not defined in `portfolio_endpoints.md` and has no backend implementation. BLG-API-01 acceptance criteria referenced this endpoint, resulting in DEV-ST05-01 (P3) when integration tests could not be written for it.

**Scope**
- Author `GET /portfolio/prospective-heat` spec in `portfolio_endpoints.md` (response shape, calculation definition)
- Implement the endpoint in `backend/main.py`
- Add TestClient integration tests in `tests/test_portfolio_integration.py` (currently skipped with `@unittest.skip` per DEV-ST05-01)

**Acceptance Criteria**
- `GET /portfolio/prospective-heat` defined in `portfolio_endpoints.md`
- Endpoint implemented and returning correct prospective heat calculation
- `@unittest.skip` removed from `TestProspectiveHeat` in `tests/test_portfolio_integration.py`; tests pass

---

### BLG-GOV-01 — Roadmap stage document consolidation
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Roadmap process reflection 2026-03-16
**Cycle added:** 2026-03-16 (governance improvement session)
**Effort:** M (2–3 days — prompt rewrite + template updates)
**Target release:** v2.0 (governance prep)

Currently Standard and Extended roadmap runs produce 5–8 separate stage files per cycle (`stage1_validation.md`, `stage2_backlog_health.md`, `stage3_ideas.md`, `stage4_debate.md`, `stage5_rebalance.md`, `run_manifest.md`, `cycle_summary.md`, `lessons_learnt.md`). The Lightweight tier (added v3.0) already consolidates STEP 2–7 output into a single `cycle_record.md`. This item extends that consolidation to Standard and Extended runs — collapsing the 5 working-paper stage files into sections of `cycle_record.md` while keeping `run_manifest.md`, `cycle_summary.md`, and `lessons_learnt.md` as separate files.

**Acceptance Criteria**
- `roadmap_prompt.md` updated: STEP 2–7 write targets changed to sections of `cycle_record.md` for all tiers
- Write scope restriction (§5) updated accordingly
- STEP 9 Write Plan template updated to reference `cycle_record.md`
- STEP 10 completion condition updated
- `OPERATIONAL_GUIDE.md` §6 artefact list updated
- At least one `run roadmap` cycle validated against the new format before sealing

---

### BLG-GOV-02 — Ideas register (replace per-file idea submissions)
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** Roadmap process reflection 2026-03-16
**Cycle added:** 2026-03-16 (governance improvement session)
**Effort:** M (2–3 days — prompt rewrite + migration)
**Target release:** v2.0 (governance prep)

The current idea intake model produces one file per idea per agent per window (44+ files from a single intake window). Status tracking requires bulk `sed` updates across dozens of files. This item replaces the per-file model with a single `claude/ideas/ideas_register.md` — a structured table with one row per idea containing: ID, agent, title, status, effort band, submission date, last-actioned date, and park rationale. The window summary (`window_summary_<window_id>.md`) is retained as the per-window record. Individual historical submission files are archived but not deleted.

**Acceptance Criteria**
- `idea_intake_prompt.md` updated: submissions write to `ideas_register.md` (append/update row) instead of individual files
- `roadmap_prompt.md` STEP 4 updated: reads from `ideas_register.md` table instead of scanning individual files
- `ideas_register.md` schema defined in `shared_standards.md` §16 (new entry)
- Migration script or instruction provided to convert existing `claude/ideas/submissions/` files into register rows
- Prior submission files moved to `claude/ideas/submissions/archive/`
- `OPERATIONAL_GUIDE.md` updated to reflect new artefact

---

### v2.1 Backlog Items — 2026-03-18__release-v2.1

**Status at retirement:** ✅ Complete
**Retired:** 2026-03-21
**Shipped in:** v2.1 — Alerts, Watchlists & Enhancements
**Evidence:** `claude/cycles/2026-03-18__release-v2.1/verification_report.md` — all 19 items delivered

| Item ID | Title | Story | Notes |
|---------|-------|-------|-------|
| BLG-SPEC-G6 | total_return_pct not returned by GET /analytics/metrics | ST-17 | Spec updated; implementation shipped |
| BLG-SPEC-D10 | api_dependencies.md v2.0 additions | ST-17 | Spec updated to include Reports + Signals mappings |
| BLG-SPEC-D11 | data_model.md §501 trade_reflections section | ST-17 | Section updated to reflect implemented status |
| BLG-SPEC-D12 | Bulk lifecycle header remediation (28 docs) | ST-16 | All 28 docs updated to Class 1/2 headers |
| BLG-SPEC-D13 | metrics_definitions.md Owner field non-compliant | ST-17 | Owner field corrected to governance role |
| TEST-GAP-SIG-01 | Signals page controls test scenarios | ST-18 | signals_scenarios.md authored |
| TEST-GAP-TAX-01 | Tax Year P&L report test scenarios | ST-18 | reports_scenarios.md authored |
| BLG-PROC-01 | Cross-EPIC process compliance check | ST-19 | v2.1 sprint compliance confirmed; EPIC-03 cherry-pick deviation documented |
| BLG-OPS-03 | Pre-merge frontend preview environments | ST-15 | seed-preview.yml psql approach shipped; frontend preview blocker documented |
| BLG-FR-01 | Tax Year P&L Report PDF Export | ST-12 | GET /reports/tax-year?format=pdf implemented with server-side PDF generation |

---

### v2.7 Release Slice — 2026-04-13__release-v2.7

**Status at retirement:** ✅ Complete
**Retired:** 2026-04-16
**Shipped in:** v2.7 — Performance, Governance Hardening & Market Intelligence
**Evidence:** 11/11 items shipped; `claude/cycles/2026-04-13__release-v2.7/closure_record.md`

| ID | Title | Story | Notes |
|----|-------|-------|-------|
| BLG-OPS-14 | Enable Supabase Supavisor connection pooling | ST-01 | Delegated; p50=234ms (PASS ≤400ms) |
| BLG-BE-07-FIX | Refactor get_portfolio_summary() single DB connection | ST-02 | GET /portfolio 1 connection/request; p50 ≤400ms |
| BLG-GOV-18 | Require QA sign-off block complete before PR | ST-03 | execution_prompt.md §3.2.B gated |
| BLG-GOV-19 | Define autonomous DoQ sign-off class | ST-04 | delivery_verification_prompt.md STEP -1.3 updated |
| BLG-GOV-16 | Extend governance_sync.yml to trigger on push to main | ST-05 | Issues now auto-close on main push |
| BLG-QA-11 | Fix Playwright page.route() intercepts (LIFO fix) | ST-06 | 46/46 Playwright tests pass |
| BLG-QA-12 | System Status Playwright spec | ST-07 | system-status.spec.js — 16 scenarios pass |
| BLG-FEAT-17 | Market Correlation Analysis | ST-08 | GET /analytics/market-correlation; AC-6 frontend deferred |
| BLG-BE-10 | Supplementary indicator fields (display-only) | ST-09 | 4 fields added; §13 COMPLIANT |
| BLG-SPEC-D17 | Spec Dependency Map | ST-10 | docs/specs/spec_dependency_map.md v1.0 |
| BLG-GOV-14 | Governance Health Score | ST-11 | OPERATIONAL_GUIDE §15; roadmap_prompt STEP -1.7 |

---

### v2.6 Release Slice — 2026-04-11__release-v2.6

**Status at retirement:** ✅ Complete
**Retired:** 2026-04-17 (post-ship cleanup — execution_state.json was not sealed; items identified by cross-referencing git log)
**Shipped in:** v2.6 — Backend Integration Completion, Test Automation & Governance Hardening
**Evidence:** 15/15 stories shipped; PRs #218–#221 merged to main; `claude/cycles/2026-04-11__release-v2.6/`

| ID | Title | Story | PR | Notes |
|----|-------|-------|----|-------|
| BLG-BE-08-GAP-01 | Migrate Reports Performance Tab to FastAPI | ST-01 | #218 / 5a6982d | No Base44 calls remain in Performance tab |
| BLG-BE-09-GAP-01 | Wire Signals dismissal and position creation to FastAPI | ST-02 | #218 / 5a6982d | Pre-existing FastAPI wiring confirmed |
| BLG-BE-09-GAP-02 | Replace Base44 cash balance on Signals page | ST-03 | #218 / 5a6982d | GET /cash/summary wired |
| BLG-QA-09 | Fix 4 pytest collection errors | ST-04 | #219 / 39efe64 | 129 tests pass, 0 collection errors |
| BLG-QA-10 | Add CI test runner workflow | ST-05 | #219 / 39efe64 | ci-tests.yml; Phase A + B delivered |
| BLG-QA-07 | Fee drag Playwright spec | ST-06 | #219 / 39efe64 | SC-FEE-01–04 pass |
| BLG-QA-08 | Pytest unit tests for fee drag | ST-07 | #219 / 39efe64 | 17 tests; SC-FEE-05, SC-FEE-06 pass |
| BLG-FE-10 | Add tooltip prop to StatsCard | ST-08 | #220 / a640719 | Avg Fee Drag card wired |
| BLG-FE-11 | Trade History StatsCard bar layout (6-card) | ST-09 | #220 / a640719 | 7-card bar; grid-cols-2 md:grid-cols-4 xl:grid-cols-7 |
| BLG-FE-12 | Trade History column header styling | ST-10 | #220 / a640719 | font-semibold text-slate-300 tracking-wide |
| BLG-FE-13 | Flexible column sorting | ST-11 | #220 / a640719 | 5 new sort states; Days Held column added |
| BLG-GOV-15 | Upgrade decision_log.md hard gate | ST-14 | #221 / 27902b7 | roadmap_prompt STEP 9 structural halt |
| BLG-FE-09 | Frontend Performance Budget spec | ST-15 | #221 / 27902b7 | docs/specs/frontend/performance_budget.md |

---

### v2.9 Release Slice — 2026-04-22__release-v2.9

**Status at retirement:** ✅ Complete
**Priority at retirement:** N/A (release tracking section)
**Retired:** 2026-04-24
**Shipped in:** v2.9 — Arc 1 Foundation: Stock Discovery & Screening Spec & Infrastructure
**Evidence:** 15/15 stories shipped (DEV-01 P3 accepted); `claude/cycles/2026-04-22__release-v2.9/closure_record.md`

| ID | Title | Type | Story | Evidence |
|----|-------|------|-------|----------|
| BLG-SPEC-21 | Screener results schema spec | Spec | ST-01 | changelog.md v2.9; verification_report.md |
| BLG-SPEC-22 | Alpaca API integration contract | Spec | ST-02 | changelog.md v2.9; verification_report.md |
| BLG-SPEC-23 | Screener internal API contract | Spec | ST-03 | changelog.md v2.9; verification_report.md |
| BLG-FE-17 | Screener results page UX spec | Frontend | ST-04 | changelog.md v2.9; verification_report.md |
| BLG-GOV-16 | §13 review record for DS-06 | Gov | ST-08 | changelog.md v2.9; verification_report.md |
| BLG-QA-08 | External API mock harness for CI | QA | ST-09 | changelog.md v2.9; verification_report.md |
| BLG-QA-09 | Screener test data library | QA | ST-10 | changelog.md v2.9; verification_report.md |
| BLG-GOV-14 | execution_prompt.md §3.2 governance patches | Gov | ST-11 | changelog.md v2.9; verification_report.md |
| BLG-GOV-15 | execution_prompt.md STEP 5.1.B cross-check | Gov | ST-12 | changelog.md v2.9; verification_report.md |
| BLG-FE-15 | SystemStatus.js `/ai` prefix fix | Frontend | ST-13 | changelog.md v2.9; verification_report.md |
| BLG-AI-01 | AI Journal summary audit log | Backend | ST-14 | changelog.md v2.9; verification_report.md |
| TEST-GAP-EPIC-04 | AI Journal test scenarios | QA | ST-15 | changelog.md v2.9; verification_report.md |

---

### BLG-SPEC-21 — Screener results schema spec
**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-01 ST-01)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

Canonical specification for screener output data structure authored as Class 2 document. All screener output fields defined with types and derivation source. §11 parameter reference explicit. DoQ sign-off obtained.

---

### BLG-SPEC-22 — Alpaca API integration contract
**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-01 ST-02)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

Formal Class 2 API contract for Alpaca US market data integration. All DS-05 Alpaca endpoints documented with request/response schemas. Fallback strategy explicitly defined. DoQ sign-off obtained.

---

### BLG-SPEC-23 — Screener internal API contract
**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-01 ST-03)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

Formal API contract for internal screener API endpoints (GET /screener/results, POST /screener/run). Request/response schemas, pagination, error codes documented. OpenAPI entries added. DoQ sign-off obtained.

---

### BLG-FE-17 — Screener results page UX spec
**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-01 ST-04)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

UX specification for screener results page authored as Class 2 canonical document. Column layout, sort/filter controls, data freshness indicator, empty states, watchlist promotion flow, and progressive loading pattern all documented. DoQ sign-off obtained.

---

### BLG-GOV-16 — §13 review record for DS-06 (Alpaca News Panel)
**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-03 ST-08)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

Formal §13 review record created for DS-06. DS-06 confirmed display-only Alpaca news context; not a sentiment signal or automated advisory. Strategy Rules owner sign-off recorded.

---

### BLG-QA-08 — External API mock harness for CI
**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-03 ST-09)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

Mock harness operational in CI for Alpaca Markets API and Yahoo Finance API. Screener CI tests pass deterministically without live API calls. Mock responses configurable per test scenario. DoQ sign-off obtained.

---

### BLG-QA-09 — Screener test data library
**Status at retirement:** ✅ Complete
**Priority at retirement:** P1 (High)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-03 ST-10)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

Synthetic ticker test data library created with minimum 10 synthetic tickers covering key screener filter scenarios. Edge cases documented: passes all filters, fails regime gate, fails ATR threshold, fails signal threshold. DoQ sign-off obtained.

---

### BLG-GOV-14 — execution_prompt.md §3.2 governance patches (2 deferred from v2.8)
**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-04 ST-11)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

Two governance patches applied to execution_prompt.md: §3.2.A reclassification note (delegated_frontend→autonomous with frontend-visible changes requires DoQ counter-sign at STEP 5); §3.2 DoQ EPIC template updated (EPIC-level consolidation block required when story-level authority is domain-specific). §6 CLAUDE.md checklist applied. Head of Specs Team sign-off obtained.

---

### BLG-GOV-15 — execution_prompt.md STEP 5.1.B capability count cross-check
**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-04 ST-12)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

STEP 5.1.B advisory inserted in execution_prompt.md after existing QA Evidence File Existence Check. Advisory instructs verification of System_status_report.md SC-* scenario counts before writing Sprint_Complete. §6 CLAUDE.md checklist applied. Head of Specs Team sign-off obtained.

---

### BLG-FE-15 — SystemStatus.js: add `/ai` prefix to `categorizeEndpoint()`
**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-04 ST-13)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

`/ai` prefix case added to `categorizeEndpoint()` in `SystemStatus.js`. AI endpoints now appear in named category (not 'Other'). No regression to categorisation of existing endpoints.

---

### BLG-AI-01 — AI Journal summary audit log
**Status at retirement:** ✅ Complete
**Priority at retirement:** P2 (Medium)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-04 ST-14)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

Persistent AI audit log implemented (ai_audit_service.py). Every summary run persisted with required fields (timestamp, trade_ids, model version, output hash). Log queryable by trade_id and date range. DoQ sign-off obtained.

---

### TEST-GAP-EPIC-04 — AI Journal Summarisation test scenario coverage
**Status at retirement:** ✅ Complete
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-24
**Shipped in:** v2.9 (2026-04-22__release-v2.9 EPIC-04 ST-15)
**Evidence:** `docs/product/changelog.md` v2.9 entry; `claude/cycles/2026-04-22__release-v2.9/verification_report.md`

`docs/testing/ai_scenarios.md` created with 4 scenarios: AI summary happy path, graceful LLM failure, collapsed-by-default frontend, disclaimer always visible. All scenarios reference ai_endpoints.md and trade_history.md v1.7. TSG-v28-01 resolved. DoQ sign-off obtained.

---

### BLG-GOV-08 — Engine prompt compression: roadmap_prompt and release_planning_prompt
**Status at retirement:** ❌ Killed — 5 consecutive deferrals; retirement decision v2.9 groom
**Priority at retirement:** P3 (Low)
**Retired:** 2026-04-24
**Decision authority:** PMO Lead + Head of Specs Team (per closure_record.md §5 item 4)
**Decision rationale:** 5 consecutive deferrals (v2.3→v2.4→v2.5→v2.6/v2.7→v2.8→v2.9); L effort (~3–5 days); prompts functional and governed — compression value does not justify cost given ongoing arc delivery cadence. Deferred to P3 permanent backlog (initiative_register.md Priority 3 or organic improvement) rather than active backlog tracking.

Engine prompt compression was identified as a governance improvement in AUD-2026-03-21. With v2.9 Arc 1 delivery complete and v3.0 Arc 1 remainder on the roadmap, the active backlog should not carry an L-effort low-priority item that has been consistently displaced by higher-value work across 5 cycles.


---

## Archived — Post-ship Closure v3.2 (2026-05-09)

---

### BLG-FE-16 — React component inventory
**Status:** ✅ COMPLETE v3.2
**Archived:** 2026-05-09 (post-ship closure groom backlog STEP 12)
**Priority:** P3 (Low)
**Type:** Frontend / Documentation
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-frontend-ux-20260321-02 — promoted cycle 2026-04-21__scheduled (DL-021)
**Effort:** M (~1–2 days)
**Provisional-Target:** v3.2 (was v3.1 — not in v3.1 sprint scope; updated GROOM-20260505-01)

**Problem**
No catalogue of UI components exists. Arc 1 will add significant new frontend components. Without an inventory, Arc 1 frontend work risks duplicating existing components and design inconsistency compounds.

**Scope**
- Catalogue all existing UI components: props, variants, usage locations
- Identify existing duplication or inconsistency
- Provide a reference for Arc 1 frontend development

**Acceptance Criteria**
- Component inventory document created covering all existing components
- Each component entry includes: purpose, props summary, variants, usage locations
- Duplication or reuse opportunities noted

---

### BLG-FE-21 — Design system document
**Status:** ✅ COMPLETE v3.2
**Archived:** 2026-05-09 (post-ship closure groom backlog STEP 12)
**Priority:** P3 (Low)
**Type:** Frontend / Documentation
**Owner:** Frontend Specifications & UX Documentation Owner
**Source:** IDEA-head-of-ux-20260321-02 — promoted cycle 2026-05-05__scheduled (DL-024)
**Effort:** M (~1–2 days)
**Provisional-Target:** v3.2

**Problem**
The system UI has accumulated organically across 17 releases. Arc 1 added significant new components (screener results, watchlist promotion, news panel). Arc 2 will add more (pre-trade research view, trade plan form, entry checklist). Without a documented design system, each new UI surface risks inconsistent patterns because the single developer is not consistent across sessions separated by weeks.

**Scope**
- Document the implicit design system: colour palette, typography scale, spacing tokens, icon conventions
- Reference document for use when adding new UI surfaces in Arc 2+
- Capture current patterns as-is (not aspirational); note any existing inconsistencies
- Coordinate with BLG-FE-16 (React component inventory) — sequence BLG-FE-16 first if both in-scope

**Acceptance Criteria**
- Design system document created covering colour palette, typography, spacing, icon conventions
- Each pattern entry includes current usage and any known inconsistencies
- Usable as a reference when starting new Arc 2 UI surfaces

---

### BLG-SEC-05 — Alpaca API key rotation policy and credential audit
**Status:** ✅ COMPLETE v3.2
**Archived:** 2026-05-09 (post-ship closure groom backlog STEP 12)
**Priority:** P2 (Medium)
**Type:** Security / Operations
**Owner:** Cybersecurity & Trust Lead
**Source:** IDEA-cybersecurity-20260421-01 + IDEA-cybersecurity-20260421-02 — promoted cycle 2026-05-05__scheduled (DL-024)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v3.2

**Problem**
Alpaca API key is in production (stored in Render environment variables) with no documented rotation policy — no specification of rotation frequency, rotation procedure, validation after rotation, or incident response if key is compromised. Additionally, multiple API credentials are now in production (Alpaca, Anthropic/Claude) with no inventory documenting storage location, last rotation, or system dependencies.

**Scope**
- Credential inventory: document all production API credentials (Alpaca, Anthropic, others), storage location, last rotation date, system dependencies
- Rotation policy: rotation frequency guidance, step-by-step rotation procedure for Alpaca key, validation procedure after rotation
- Incident response note: what to do if a credential is compromised
- Not a compliance document — procedural memory for the developer

**Acceptance Criteria**
- Credential inventory lists all production API credentials with storage location and last rotation
- Rotation policy documented with step-by-step procedure for Alpaca key rotation
- Validation procedure after rotation specified
- Incident response steps documented (rotate, validate, check audit logs)

---

### BLG-GOV-18 — External API dependency risk register
**Status:** ✅ COMPLETE v3.2
**Archived:** 2026-05-09 (post-ship closure groom backlog STEP 12)
**Priority:** P3 (Low)
**Type:** Governance Process / Operational Risk
**Owner:** PMO Lead + Infrastructure & Operations Owner
**Source:** IDEA-pmo-lead-20260421-01 — promoted cycle 2026-05-05__scheduled (DL-024)
**Effort:** S (~0.5 day)
**Provisional-Target:** v3.2

**Problem**
Alpaca Markets API is now production-critical — the screener engine depends on it for daily OHLCV bars. Yahoo Finance is also in the data pipeline. No formal register tracks which endpoints are used, reliability record, known failure modes, fallback status, or SLA concerns. GET /health provides real-time health but not risk assessment or response planning.

**Scope**
- Lightweight register documenting each external API dependency (Alpaca, Yahoo Finance, Anthropic Claude)
- Per dependency: endpoints used, reliability record, fallback status, API tier/plan, renewal/rotation requirements
- Register surfaced at each roadmap rebalance for operational awareness
- Not an incident response playbook — a risk inventory

**Acceptance Criteria**
- Register created covering all production external API dependencies
- Each entry includes: endpoints used, current status, known failure modes, fallback behaviour, renewal/tier info
- Register referenced in run_manifest.md template for future rebalances

---

### BLG-GOV-11 — Cycle artefact inventory and maintenance review
**Status:** ✅ COMPLETE v3.2
**Archived:** 2026-05-09 (post-ship closure groom backlog STEP 12)
**Priority:** P3 (Low)
**Type:** Governance Process
**Owner:** PMO Lead + Head of Specs Team
**Source:** User session review — 2026-04-03
**Effort:** M (~1–2 days)
**Provisional-Target:** v3.2 (was v3.1 — deferred; 3 consecutive cycle deferrals as of v3.1)

**Problem**
As cycles accumulate, documents are created in each cycle directory but there is no consolidated inventory of what exists across all closed cycles, nor a documented lifecycle for each artefact type (maintained vs. point-in-time). Without this review it is impossible to audit historical artefacts, identify stale documents, or enforce consistent maintenance practices going forward.

**Scope**
- Inventory all documents created across all closed cycles (`claude/cycles/`)
- Categorise by type: planning, execution, QA evidence, governance, run manifests, etc.
- Document the expected lifecycle for each type: point-in-time artefact vs. living document
- Identify any maintenance gaps, stale artefacts, or documents that should be archived
- Produce a reference document or update the OPERATIONAL_GUIDE with the artefact lifecycle model

**Acceptance Criteria**
- A consolidated artefact inventory exists covering all closed cycles
- Each document type has a documented lifecycle (point-in-time vs. maintained)
- Any maintenance gaps are identified; each either resolved or filed as a follow-up backlog item
- Reference document or OPERATIONAL_GUIDE section added



---

### BLG-FE-35 — ST-08 AC-02: Human staging sign-off for Research page font conformance
**Archived:** 2026-05-18
**Completed in:** v3.7 (EPIC-04, ST-10)
**Resolution:** Human staging run performed 2026-05-18 by Head of UX & Design — Research page typography confirmed conformant against design_system.md. Playwright test `tests/e2e/research-typography.spec.js` (SC-RV-TYP-01) added for permanent CI regression coverage. BLG-FE-26 was already archived 2026-05-17.

---

### BLG-TECH-10 — Fix Yahoo Finance crumb/401 rate-limiting in screener batch
**Archived:** 2026-05-22
**Completed in:** v3.9 (EPIC-01, ST-01)
**Resolution:** Crumb refresh logic implemented; exponential backoff with jitter on 401/429; concurrent request cap via environment variable; crumb refresh events logged. All AC met. P3 process notation: AC-04 integration test deferred to staging (BLG-QA-24).

---

### BLG-BE-10 — Fix sector/industry data dropped in screener batch
**Archived:** 2026-05-22
**Completed in:** v3.9 (EPIC-01, ST-02)
**Resolution:** Full ticker dict (including sector/industry) retained and passed to compute_screener_result(). Screener results now persist non-null sector/industry. Unit test verifies propagation.

---

### BLG-BE-11 — Remove DAY from ticker universe (invalid Yahoo Finance symbol)
**Archived:** 2026-05-22
**Completed in:** v3.9 (EPIC-01, ST-03)
**Resolution:** DAY removed from tickers_full_list.csv; deactivate_invalid_tickers() added to startup; PHNX.L retained as valid FTSE 250 ticker (Phoenix Group Holdings). No OHLCV FAILED for DAY log entries post-deploy.

---

### BLG-FE-38 — Add degraded-run warning to screener when OHLCV failure rate exceeds 20%
**Archived:** 2026-05-22
**Completed in:** v3.9 (EPIC-01, ST-04)
**Resolution:** degraded_run/failure_rate fields added to screener_runs table and GET /screener/results response; DegradedRunBanner component shows amber warning with failure_rate percentage; SC-SCR-DEG-01/02 Playwright pass.

---

### BLG-FE-37 — Strip .L suffix from Ticker Universe page display labels
**Archived:** 2026-05-22
**Completed in:** v3.9 (EPIC-02, ST-05)
**Resolution:** displayTicker() function strips .L from display labels; API requests (add/toggle/delete) still use full ticker; US tickers unaffected. SC-TU-DISP-01 Playwright pass.

---

### BLG-BE-12 — Add company_name column to ticker universe
**Archived:** 2026-05-22
**Completed in:** v3.9 (EPIC-02, ST-06)
**Resolution:** ensure_company_name_column() adds TEXT column; backfill from tickers_full_list.csv on startup; company_name included in GET /ticker-universe response; management page displays company name as 2nd column. SC-TU-COMP-01 Playwright pass.

---

### BLG-GOV-25 — Add --dry-run support to plan release and run delivery verification engines
**Archived:** 2026-05-22
**Completed in:** v3.9 (EPIC-04, ST-11)
**Resolution:** --dry-run flag added to release_planning_prompt.md v2.31 and delivery_verification_prompt.md v2.5; two rows added to shared_standards.md §13 dry-run table; all three files version-bumped; prompt_change_log.md entries added.


---

## v4.1 Completions — Archived 2026-05-27 (Post-Ship Cleanup)

---

### BLG-FEAT-40 — SI-05 composite compliance score formula
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P2 (Medium)
**Type:** Product Feature / Analytics
**Owner:** Metrics Definitions & Analytics Owner
**Source:** IDEA-metrics-analytics-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Problem**
SI-05 (Weekly Strategy Integrity Digest) will surface a compliance score trend. No formal definition exists for the composite compliance score formula — what it includes, how it is weighted, and what denominator it uses. Without a pre-defined formula, the SI-05 sprint will produce an ad-hoc metric that cannot be referenced in the monthly P&L report (BLG-FEAT-38) or tracked for trend.

**Scope**
- Define composite compliance score: formula, components (validation pass rate, override rate, red flag event rate), weighting rationale
- Document in metrics_definitions.md
- Input to SI-05 sprint planning and BLG-FEAT-38 P&L integration

**Acceptance Criteria**
- Formula defined and documented in metrics_definitions.md
- Components and weightings explained with rationale
- Reviewed by Strategy Rules & System Intent Owner before SI-05 sprint planning

---

---

### BLG-FEAT-42 — Arc 5 compliance metrics monthly P&L report integration
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P2 (Medium)
**Type:** Product Feature / Reporting
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** M (~2 days)
**Provisional-Target:** v4.1

**Problem**
BLG-FEAT-38 (Arc 5 compliance score in P&L report) has its gate cleared as of rebalance 2026-05-25. BLG-FEAT-42 is the implementation spec and integration work to add the compliance metrics section to the monthly P&L report using the Arc5ComplianceSection data already available from the v4.0 analytics endpoint. A separate implementation item is warranted because BLG-FEAT-38 defines what should appear; BLG-FEAT-42 defines how to integrate it into the existing report infrastructure.

**Scope**
- Add Arc 5 compliance summary section to monthly P&L report output
- Source data from GET /analytics/arc5-compliance endpoint (shipped v4.0)
- Fields: validation_pass_rate_by_rule (top 3 rules), override_rate, events_per_week, top_rule_breach
- Requires BLG-FEAT-38 (gate cleared) and BLG-FEAT-40 (composite score formula) as preconditions before sprint

**Acceptance Criteria**
- Monthly P&L report includes Arc 5 compliance summary section
- Data sourced from GET /analytics/arc5-compliance
- Composite score formula (BLG-FEAT-40) applied if defined; else individual components only
- Reviewed by Financial Reporting & Records Owner and Product Owner before sprint planning

---

---

### BLG-FE-44 — Research view: surface signal_type as Setup Type column
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P3 (Low)
**Type:** Frontend / Backend
**Owner:** Head of Engineering; Head of UX & Design
**Source:** v4.0 sprint execution — out-of-scope change stashed and deferred
**Effort:** XS (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
The Research page signal card shows Current Price, Signal, Status, ATR, and Entry Price but does not surface `signal_type` (e.g. "strong_momentum", "momentum"). This field is already in the signals table and available in `GET /research/{ticker}` response. Adding it gives traders immediate context on setup quality without navigating away.

**Scope**
- `backend/routers/research.py`: include `signal_type` in `_get_signal()` response dict (1-line change)
- `src/pages/Research.js`: add `SetupTypeBadge` component; add 5th column to Price & Signal grid showing setup type with colour-coded badge (violet for strong_momentum, cyan for momentum)
- No new endpoint, no schema change, no migration required

**Acceptance Criteria**
- AC-01: `GET /research/{ticker}` response includes `signal_type` field
- AC-02: Research page Price & Signal section shows Setup Type badge alongside ATR and Entry Price
- AC-03: strong_momentum → violet badge; momentum → cyan badge; null → dash

---

---

### BLG-FE-48 — Arc5ComplianceSection frontend spec
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P1 (High)
**Type:** Frontend / Spec
**Owner:** Frontend Specs & UX Documentation Owner
**Source:** IDEA-frontend-ux-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~1 day)
**Provisional-Target:** v4.1

**Problem**
Arc5ComplianceSection.js shipped v4.0 without a formal frontend spec. The component was implemented from acceptance criteria. A retrospective spec document is needed for: (a) future maintenance reference, (b) input to BLG-FE-45 expandability review, (c) Arc 6 extension planning.

**Scope**
- Produce frontend component spec for Arc5ComplianceSection.js
- Cover: data contract (from GET /analytics/arc5-compliance), component props, display states (loading, empty, populated), responsive layout, test coverage (SC-AC5-xx)
- Reviewed by Head of UX & Design and Product Owner

**Acceptance Criteria**
- Frontend spec filed in docs/specs/frontend/ (or equivalent)
- Data contract documented against current openapi.yaml endpoint
- Reviewed and accepted by Head of UX & Design

---

---

### BLG-OPS-29 — Add v4.0 new endpoints to api_performance_baseline.md re-run
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** Post-ship closure 2026-05-22__release-v4.0 — endpoint coverage drift check
**Effort:** S (~1 day)
**Provisional-Target:** v4.1

**Problem**
`docs/ops/api_performance_baseline.md` was last updated at v2.7 (Supavisor re-run). v4.0 introduced two new endpoints not present in the baseline: GET /analytics/arc5-compliance (ST-01) and POST /trade-plans/{plan_id}/generate-thesis (ST-12). These endpoints have no p50/p95 measurement, no HTTP status expectation, and no ⚠️ flag threshold. Additional endpoints added since v2.7 may also be absent.

**Scope**
- Run api_performance_baseline measurement against staging environment
- Include all endpoints in openapi.yaml not yet in the baseline table
- Specifically confirm GET /analytics/arc5-compliance and POST /trade-plans/{plan_id}/generate-thesis are measured
- Flag any p95 > 500ms per existing methodology
- Update docs/ops/api_performance_baseline.md version header and Last Updated date

**Acceptance Criteria**
- All openapi.yaml endpoints present in api_performance_baseline.md measurement table
- p50/p95 measurements recorded for GET /analytics/arc5-compliance and POST /trade-plans/{plan_id}/generate-thesis
- Document version bumped and Last Updated set to run date

---

*BLG-OPS-16 (Remove tracked backend/__pycache__ files from git + .gitignore) — ✅ COMPLETE v3.7 — ST-10, cycle: 2026-05-18__release-v3.7*

---

---

### BLG-OPS-30 — Gemini API usage first monthly review
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P1 (High)
**Type:** Operations / Cost Management
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** IDEA-finops-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
Gemini Flash API (shipped v4.0, ST-12) is now live for thesis generation. BLG-OPS-26 (Gemini API cost tracking) was added in IW-20260522-01. The first monthly review should be conducted ~30 days after v4.0 ship to: verify gemini_audit_log is populating correctly, review actual token consumption and cost, and set a monthly review cadence going forward.

**Scope**
- Run first monthly review of gemini_audit_log: request count, total tokens, estimated cost
- Verify cost tracking accuracy against Gemini API billing dashboard
- Establish review cadence (monthly scheduled review added to governance calendar)
- Document findings in a brief ops note

**Acceptance Criteria**
- gemini_audit_log reviewed: data integrity confirmed
- Cost estimate produced for first 30 days
- Monthly review cadence established and documented
- Findings reviewed by FinOps & Resource Architect

---

---

### BLG-OPS-32 — Trade plan P&L attribution gate check
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P2 (Medium)
**Type:** Operations / Data Quality
**Owner:** Financial Reporting & Records Owner; Infrastructure & Operations Owner
**Source:** IDEA-financial-reporting-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
Monthly P&L reports attribute P&L to closed trades. Trade plans (Arc 2, shipped v3.1) link to positions at entry. Verifying that P&L attribution correctly reflects which positions had trade plans (vs. pre-Arc-2 positions without plans) is a data quality gate check before BLG-FEAT-38 (Arc 5 compliance metrics in P&L) and BLG-FEAT-42 can produce accurate compliance-linked P&L analysis.

**Scope**
- Query: trades with plan_id vs. trades without plan_id in closed trade history
- Confirm P&L report handles both cases correctly (plan-linked vs. legacy trades)
- Flag any attribution anomalies for remediation before compliance integration

**Acceptance Criteria**
- Plan-linked vs. non-plan trade count confirmed
- P&L attribution verified accurate for both trade types
- Any anomalies documented and flagged to Product Owner

---

---

### BLG-OPS-34 — Gemini API daily cost threshold alert via Telegram
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P2 (Medium)
**Type:** Operations / Cost Monitoring
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** IDEA-finops-20260525-02 — Promoted-Backlog (STEP 5 debate, modified scope) cycle 2026-05-25__scheduled (DL-034)
**Effort:** M (~2–3 days)
**Provisional-Target:** v4.1

**Problem**
Gemini thesis generation (shipped v4.0) incurs per-request API costs. Currently there is no automated alert if Gemini API spend exceeds a daily threshold. BLG-OPS-26 provides manual monthly cost review; BLG-OPS-34 provides automated daily threshold monitoring using the existing Telegram notification infrastructure (shipped v2.4).

**Scope**
- Configurable daily Gemini spend threshold (default: $1.00/day)
- Daily check of gemini_audit_log: sum estimated_cost_usd for current day
- If threshold exceeded: send Telegram alert with daily total and request count
- No new UI — Telegram notification only (existing infrastructure)

**Acceptance Criteria**
- Daily threshold check implemented (scheduled task or startup check)
- Telegram alert fires when daily spend exceeds configurable threshold
- Threshold configurable via env var
- Test coverage: unit test for threshold logic; staging verification

---

---

### BLG-SPEC-33 — SI-03 Red Flag Journal API contract document
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P1 (High)
**Type:** Spec Debt
**Owner:** API Contracts Documentation Owner
**Source:** IDEA-api-contracts-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** v4.0

**Problem**
`GET /portfolio/red-flag-journal` shipped v3.9 (SI-03) without a formal API contract document in `docs/specs/api_contracts/`. SI-04 and SI-05 will extend or reference the Red Flag Journal endpoint; without a contract, downstream implementations lack an authoritative spec for filter parameters, pagination schema, response structure, and error codes.

**Scope**
- Author `docs/specs/api_contracts/red_flag_journal.md`
- Document: endpoint URL, HTTP method, authentication requirement, query parameters (date range, event type, severity when BLG-BE-16 ships), pagination schema, response fields, error codes
- Register in `docs/reference/openapi.yaml` per CLAUDE.md §2
- Use `## METHOD /path` heading format per CLAUDE.md §2

**Acceptance Criteria**
- API contract document produced and filed
- Contract registered in openapi.yaml with correct heading format
- All filter parameters and response fields documented
- Reviewed by Head of Specs Team and API Contracts Documentation Owner

---

---

### BLG-SPEC-34 — SI-01 Pre-Entry Validation API contract document
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P1 (High)
**Type:** Spec Debt
**Owner:** API Contracts Documentation Owner
**Source:** IDEA-api-contracts-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** v4.0

**Problem**
`GET /portfolio/pre-entry-validation` shipped v3.8 (SI-01) without a formal API contract document. SI-02 and SI-05 will reference the validation rule taxonomy and response schema; without a contract, there is no authoritative source for rule enumeration, response structure, or override acknowledgement path.

**Scope**
- Author `docs/specs/api_contracts/pre_entry_validation.md`
- Document: endpoint URL, HTTP method, query parameters, response fields (per-rule pass/fail, override_required), override acknowledgement path, error codes
- Enumerate all 5 validation rules per strategy_rules.md v1.4 §4.2
- Register in `docs/reference/openapi.yaml`

**Acceptance Criteria**
- API contract document produced and filed
- All 5 validation rules documented with pass/fail conditions
- Override acknowledgement path specified
- Contract registered in openapi.yaml
- Reviewed by Head of Specs Team

---

---

### BLG-SPEC-38 — Gemini thesis endpoint API contract
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P1 (High)
**Type:** Spec Debt / API Contract
**Owner:** API Contracts Documentation Owner; Head of Specs Team
**Source:** IDEA-api-contracts-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~1 day)
**Provisional-Target:** v4.1

**Gate criteria:** BLG-SPEC-33 (SI-03 Red Flag Journal API contract) closed — Gemini thesis endpoint contract follows SI-03 contract closure to ensure consistent contract format.

**Problem**
POST /trade-plans/{plan_id}/generate-thesis (shipped v4.0, ST-12) has no formal API contract document in docs/specs/api_contracts/. BLG-GOV-55 (API contract same-sprint delivery rule) will prevent future recurrence; BLG-SPEC-38 addresses the existing debt from v4.0. Additionally: CLAUDE.md §2 requires every new API endpoint to be added to openapi.yaml in the same commit as the contract — this item will verify the v4.0 openapi.yaml entry is complete.

**Scope**
- Write formal API contract document for POST /trade-plans/{plan_id}/generate-thesis
- Cover: request schema (plan_id path param), response schema ({thesis, model_version, prompt_version}), error cases (missing key, invalid plan_id, Gemini error)
- Verify corresponding openapi.yaml entry is complete and at ## level
- Filed in docs/specs/api_contracts/

**Acceptance Criteria**
- API contract document produced at docs/specs/api_contracts/
- Endpoint heading at ## level (OpenAPI drift gate compliant)
- openapi.yaml entry verified complete
- Reviewed by API Contracts Documentation Owner and Head of Specs Team
- Gate condition (BLG-SPEC-33 closed) verified before commencing

---

---

### BLG-SPEC-39 — SI-02 data model gap analysis
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P1 (High)
**Type:** Spec / Data Model
**Owner:** Data Model & Domain Schema Owner; Head of Specs Team
**Source:** IDEA-data-model-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** M (~1–2 days)
**Provisional-Target:** v4.1

**Problem**
SI-02 (Behavioural Drift Detection) requires comparing actual trade entries against stated setup criteria — specifically: regime_at_entry, signal_type, setup_type, and entry_proximity fields. BLG-SPEC-37 defined the schema pre-definition approach (gate-conditional on sprint planning). BLG-SPEC-39 is a standalone gap analysis that can be done now to identify which fields are missing from the current trade/position data model, enabling proactive planning before SI-02 sprint planning is triggered.

**Scope**
- Review current trade, position, and trade_plan schemas for fields required by SI-02
- Identify missing fields with: data type, source (captured at entry? derivable? new collection?), migration complexity
- Output: gap analysis document for input to SI-02 sprint planning
- Complements BLG-SPEC-37 (gate-conditional version); this item proceeds without gate constraint

**Acceptance Criteria**
- Gap analysis document produced
- Missing fields enumerated with type and migration estimate
- Reviewed by Data Model & Domain Schema Owner, Head of Specs Team, and Head of Backend Engineering before SI-02 sprint planning

---

---

### BLG-SPEC-40 — Arc 5 analytics endpoint API contract
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P1 (High)
**Type:** Spec Debt / API Contract
**Owner:** API Contracts Documentation Owner; Head of Specs Team
**Source:** IDEA-api-contracts-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~1 day)
**Provisional-Target:** v4.1

**Problem**
GET /analytics/arc5-compliance (shipped v4.0, ST-01) has no formal API contract document in docs/specs/api_contracts/. The endpoint was implemented from acceptance criteria. A formal contract document enables: frontend spec alignment (BLG-FE-48), future Arc 6 extension planning (BLG-BE-21), and compliance with CLAUDE.md §2 API contract requirements.

**Scope**
- Write formal API contract document for GET /analytics/arc5-compliance
- Cover: response schema (validation_pass_rate_by_rule, events_per_week, override_rate, top_rule_breach, trade_plan_adherence_rate), query params (if any), error cases
- Verify openapi.yaml entry is complete and at ## level
- Filed in docs/specs/api_contracts/

**Acceptance Criteria**
- API contract document produced at docs/specs/api_contracts/
- Endpoint heading at ## level
- openapi.yaml entry verified complete
- Reviewed by API Contracts Documentation Owner and Head of Specs Team

---

---

### BLG-GOV-44 — SI-02 §13 review evidence criteria pre-definition
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P1 (High)
**Type:** Governance / §13 Compliance
**Owner:** Strategy Rules & System Intent Owner; Head of Specs Team
**Source:** IDEA-strategy-owner-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
BLG-GOV-39 (SI-02 §13 formal boundary review, gate-conditional on sprint planning imminent) was added in IW-20260522-01. BLG-GOV-44 pre-defines the evidence criteria that the §13 review for SI-02 must satisfy — what "PASS" looks like, what binding conditions are expected, and what test scenarios confirm determinism. Pre-definition before sprint planning prevents the §13 review from being conducted without a clear pass/fail framework.

**Scope**
- Define §13 review evidence criteria for SI-02: what assertions must be verifiable (determinism, display-only output, no adaptive learning, no automated action)
- Document expected binding conditions (e.g., "drift alerts informational only; no automated position management")
- Input to BLG-GOV-39 when gate clears

**Acceptance Criteria**
- Evidence criteria document produced
- Reviewed by Strategy Rules & System Intent Owner
- Document filed for reference when BLG-GOV-39 gate triggers

---

---

### BLG-GOV-46 — SI-02 data prerequisite audit
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P1 (High)
**Type:** Governance / Release Gate
**Owner:** Challenger; Product Owner
**Source:** IDEA-challenger-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
SI-02 (Behavioural Drift Detection) requires trade history with regime_at_entry, setup_type, and signal_conditions captured. These fields may not be present on all historical trades. Before sprint planning, the Challenger's mandatory data prerequisite audit confirms: how many trades have complete data, whether the sample is sufficient for meaningful drift analysis, and whether any data backfill is required as a pre-sprint story.

**Scope**
- Query trade history: count trades with regime_at_entry, setup_type, and plan_id present
- Assess: is the sample sufficient for drift analysis? (target: 10+ trades with complete data)
- If insufficient: identify backfill options or document that drift analysis will have limited early utility
- Findings reviewed by Product Owner before SI-02 sprint planning

**Acceptance Criteria**
- Audit query run and results documented
- Sufficiency assessment produced
- Product Owner informed; sprint planning decision documented

---

---

### BLG-GOV-49 — Gemini API key scope minimization review
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P1 (High)
**Type:** Governance / Security
**Owner:** Cybersecurity & Trust Lead
**Source:** IDEA-cybersecurity-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
GEMINI_API_KEY (shipped v4.0) is used for thesis generation via the generative AI API. The key scope (what the key can access on the Google AI platform) should be reviewed to confirm it is minimally scoped: text generation only, no other Google API access, rate-limited where possible. Key scope minimization is a security hygiene requirement for any external AI API credential.

**Scope**
- Review GEMINI_API_KEY scope on Google AI platform
- Confirm: restricted to generative AI text generation only
- Confirm: key is not shared with other Google services
- Document findings in security review note

**Acceptance Criteria**
- Key scope confirmed (or remediation action filed if overly permissive)
- Findings documented in docs/security/
- Reviewed by Cybersecurity & Trust Lead

---

---

### BLG-GOV-51 — SI-02 database query performance pre-assessment
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P2 (Medium)
**Type:** Governance / Performance Pre-work
**Owner:** Head of Engineering; Head of Backend Engineering
**Source:** IDEA-head-of-engineering-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~1 day)
**Provisional-Target:** v4.1

**Problem**
SI-02 (Behavioural Drift Detection) involves rolling analysis across trade history. Depending on the query design, this could be computationally expensive on a Supabase PostgreSQL instance with 50+ trades. A pre-assessment of expected query patterns against the current data model confirms whether any performance concerns exist before sprint planning, preventing mid-sprint performance surprises.

**Scope**
- Profile expected SI-02 query patterns against current trade/position schema
- Estimate query complexity for typical dataset size (20–100 trades)
- Identify: any full-table scans, missing indexes, or aggregate patterns requiring optimisation
- Input to BLG-BE-20 (background job architecture) and SI-02 sprint planning

**Acceptance Criteria**
- Query patterns profiled (may be desk analysis, not live benchmark)
- Performance concerns (if any) documented with severity estimate
- Findings reviewed by Head of Engineering and Head of Backend Engineering before SI-02 sprint planning

---

---

### BLG-GOV-54 — SI-05 Phase 1 scope annotation — Red Flag + compliance trend delivery
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P2 (Medium)
**Type:** Governance / Roadmap Annotation
**Owner:** Product Owner; Head of Specs Team
**Source:** IDEA-product-owner-20260525-01 — Promoted-Backlog (STEP 5 debate) cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
SI-05 (Weekly Strategy Integrity Digest) depends on SI-02 for its drift signal component. SI-02 may not ship until v4.2+. To avoid blocking all of SI-05, this item formalises a phased delivery approach: Phase 1 (Red Flag Journal summary + compliance score trend via Telegram, no SI-02 component) can ship as soon as SI-03 and Arc5ComplianceSection are live (both shipped v4.0). Phase 2 (drift signal integration) ships when SI-02 is complete.

**Scope**
- Annotate SI-05 on current_roadmap.md with phased delivery note
- Create SI-05 Phase 2 follow-on backlog item (separate BLG, filed at sprint planning time)
- Update relevant specs/acceptance criteria to reflect Phase 1 scope
- Phase 1 scope: weekly Telegram digest of Red Flag Journal events (count + top event type) + compliance score trend (7-day rolling validation pass rate)

**Acceptance Criteria**
- SI-05 roadmap entry annotated with phased delivery approach
- Phase 1 scope defined and documented
- Phase 2 follow-on scope identified (to be filed as a backlog item at v4.1 sprint planning)
- Product Owner sign-off on Phase 1 scope definition

---

---

### BLG-GOV-56 — STEP 12.1 artefact presence check
**Shipped:** ✅ COMPLETE — v4.1 — 2026-05-27 — cycle: 2026-05-26__release-v4.1
**Priority:** P2 (Medium)
**Type:** Governance / Prompt Engineering
**Owner:** Head of Specs Team; PMO Lead
**Source:** IDEA-pmo-lead-20260525-02 — Promoted-Backlog (STEP 5 debate, modified scope) cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
STEP 12.1 of governance engines updates .claude_current_state.json regardless of whether required cycle artefacts exist on disk. A cycle can be marked complete in state even if run_manifest.md, cycle_summary.md, or lessons_learnt.md were never written. Adding an artefact presence check produces a visible warning in STEP 12.1 output for missing artefacts, with a soft halt only for required Class-3 Operational Records.

**Scope**
- Add artefact presence check to STEP 12.1 of roadmap_prompt.md, sprint_planning_prompt.md, delivery_verification_prompt.md, and post_ship_closure.md
- Advisory warning output for missing non-required artefacts
- Soft halt (STEP 12.1 completes but records a governance warning in state) if required Class-3 Operational Record (run_manifest.md, sprint_goal.md) is absent
- Per CLAUDE.md §6 governance file edit checklist: bump version, update OPERATIONAL_GUIDE.md §14, append prompt_change_log.md for each affected prompt

**Acceptance Criteria**
- Artefact presence check added to STEP 12.1 of all four prompt files
- Prompt versions bumped; OPERATIONAL_GUIDE.md §14 updated; prompt_change_log.md appended
- Soft halt condition: absent required Class-3 record produces governance warning in state file
- False-halt risk addressed: check uses canonical artefact paths only (not temp/worktree paths)

---

---

## v3.7/v3.9 Completions — Archived 2026-05-27 (Backlog Cleanup)

*BLG-TECH-10 (Fix Yahoo Finance crumb/401 rate-limiting in screener batch) — ✅ COMPLETE v3.9 — ST-01, cycle: 2026-05-21__release-v3.9*
*BLG-FE-34 (Trade plan form signal context panel — SignalContextPanel.js with entry_rationale/confirmation pre-population) — ✅ COMPLETE v3.7 — ST-03, cycle: 2026-05-18__release-v3.7*
*BLG-FE-33 (Signals page Add to Watchlist CTA — watchlisted status backend + SignalCard CTA replacement) — ✅ COMPLETE v3.7 — ST-01 + ST-02, cycle: 2026-05-18__release-v3.7*
*BLG-FE-37 (Strip .L suffix from Ticker Universe page display labels) — ✅ COMPLETE v3.9 — ST-05, cycle: 2026-05-21__release-v3.9*
*BLG-FE-38 (Add degraded-run warning to screener when OHLCV failure rate exceeds 20%) — ✅ COMPLETE v3.9 — ST-04, cycle: 2026-05-21__release-v3.9*
*BLG-BE-10 (Fix sector/industry data dropped in screener batch) — ✅ COMPLETE v3.9 — ST-02, cycle: 2026-05-21__release-v3.9*
*BLG-BE-11 (Remove DAY from ticker universe — invalid Yahoo Finance symbol) — ✅ COMPLETE v3.9 — ST-03, cycle: 2026-05-21__release-v3.9*
*BLG-BE-12 (Add company_name column to ticker universe) — ✅ COMPLETE v3.9 — ST-06, cycle: 2026-05-21__release-v3.9*
*BLG-QA-20 (Consolidate database stub files into shared pytest conftest fixture — session-scoped stub) — ✅ COMPLETE v3.7 — ST-09, cycle: 2026-05-18__release-v3.7*
*BLG-OPS-16 (Remove tracked backend/__pycache__ files from git + .gitignore) — ✅ COMPLETE v3.7 — ST-10, cycle: 2026-05-18__release-v3.7*
*BLG-GOV-23 (scored_initiatives.md Arc 3–6 comprehensive refresh — OA-RP-05 resolved) — ✅ COMPLETE v3.7 — ST-11, cycle: 2026-05-18__release-v3.7*
*BLG-GOV-25 (Add --dry-run support to plan release and run delivery verification engines) — ✅ COMPLETE v3.9 — ST-11, cycle: 2026-05-21__release-v3.9*


---

## v4.0 Completions — Archived 2026-05-27 (Post-Ship Cleanup)

---

### BLG-FEAT-36 — SI-01 validation pass/fail rate by rule
**Priority:** P2 (Medium)
**Type:** Product Feature / Analytics
**Owner:** Metrics Definitions & Analytics Canonical Owner
**Source:** IDEA-metrics-analytics-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~2–3 days)
**Provisional-Target:** v4.0
**Status: ✅ COMPLETE — v4.0 — ST-01 — cycle: 2026-05-22__release-v4.0 — 2026-05-25**

**Problem**
GET /portfolio/pre-entry-validation (SI-01, shipped v3.8) returns per-attempt pass/fail results but no aggregate metric tracks pass/fail rate broken down by individual rule type over time. Understanding which rules most frequently block entries reveals behavioural patterns (e.g., "regime gate fails 40% of the time") without requiring SI-02 (drift detection).

**Scope**
- Define named metric: validation_pass_rate_by_rule — pass count / (pass + fail count) per rule per rolling period
- Backend: query pre-entry validation log for rule-level pass/fail aggregation
- Frontend: surface metric in SI-05 Weekly Digest or standalone compliance dashboard
- Requires confirmation that the pre-entry validation log captures per-rule outcomes (may require minor schema addition)

**Acceptance Criteria**
- Pass/fail rate per rule computable and displayable
- Rolling period configurable (7d / 30d)
- Backend analysis of current log schema completed before sprint planning

---

---

### BLG-FEAT-37 — Red flag event frequency metric
**Priority:** P2 (Medium)
**Type:** Product Feature / Analytics
**Owner:** Metrics Definitions & Analytics Canonical Owner
**Source:** IDEA-metrics-analytics-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** v4.0
**Status: ✅ COMPLETE — v4.0 — ST-02 — cycle: 2026-05-22__release-v4.0 — 2026-05-25**

**Problem**
No canonical metric tracks red flag event frequency over time. Override rate and rule-breach-by-type distribution are queryable from red_flag_events (shipped v3.9) but not defined as named product metrics with specified aggregation periods and display locations. Defining these metrics makes them inputs to SI-05 Weekly Digest and the monthly P&L compliance section.

**Scope**
- Named metrics: events_per_week, override_rate (overrides / validation attempts), event_type_distribution
- Backend: aggregate query on red_flag_events table
- Metric definitions registered in metrics_definitions.md

**Acceptance Criteria**
- Three named metrics defined and queryable
- Metrics definitions registered per canonical standards
- Data available for SI-05 and BLG-FEAT-38 (monthly P&L compliance section) consumption

---

---

### BLG-FEAT-39 — Trade plan adherence rate metric
**Priority:** P2 (Medium)
**Type:** Product Feature / Analytics
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** v4.0
**Status: ✅ COMPLETE — v4.0 — ST-04 — cycle: 2026-05-22__release-v4.0 — 2026-05-25**

**Gate criteria:** plan_id linkage actively captured on closed trades (requires active use of trade plan creation workflow).

**Problem**
No metric tracks what percentage of closed trades have an associated trade plan (plan_id linkage). This metric measures systematic discipline adoption — whether the operator is consistently using trade plans before entry. It is a direct input to Arc 4 PO-04 (reflection/outcome correlation) and a candidate for the compliance section of the monthly P&L report.

**Scope**
- Named metric: trade_plan_adherence_rate — trades_with_plan_id / total_closed_trades
- Backend: aggregate query on closed trades
- Metric definition registered in metrics_definitions.md
- Surface in performance reports and SI-05 Weekly Digest

**Acceptance Criteria**
- Metric defined and queryable
- Registered in metrics definitions
- Gate condition verified by Product Owner before sprint planning

---

---

### BLG-BE-15 — Validate ticker symbol on add (sector/industry lookup)
**Priority:** P1 (High)
**Type:** Backend Engineering
**Owner:** Head of Backend Engineering
**Source:** User request — 2026-05-22
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.0
**Status: ✅ COMPLETE — v4.0 — ST-05 — cycle: 2026-05-22__release-v4.0 — 2026-05-25**

**Problem**
When a user adds a ticker symbol and market to the universe, no validation is performed to confirm the ticker actually exists. Any arbitrary string can be saved, leading to junk entries that silently produce empty screener results or data fetch errors. Validating sector and industry at add-time gives immediate feedback and prevents invalid tickers from polluting the universe.

**Scope**
- On ticker add (POST `/tickers` or equivalent), call the market data provider (Yahoo Finance) to fetch sector and industry for the submitted symbol+market
- If the lookup returns no data or raises an error, reject the request with a clear 400/422 response and message (e.g. "Ticker XXXX not found — please check the symbol and market")
- If the lookup succeeds, optionally auto-populate sector/industry fields from the returned data
- Frontend to surface the rejection error inline on the add-ticker form

**Acceptance Criteria**
- Submitting a non-existent ticker symbol returns an error response and the ticker is not saved
- Submitting a valid ticker returns success; sector and industry are confirmed present
- Error message displayed to user is specific and actionable (not a generic 500)
- Existing tickers already in the universe are unaffected

---

---

### BLG-BE-19 — Base Gemini Flash API wiring — thesis generation service + endpoint
**Priority:** P1 (High)
**Type:** Backend Engineering / Frontend
**Owner:** Head of Backend Engineering
**Source:** Session observation 2026-05-22 — BLG-FEAT-24 marked complete v3.8 but Gemini not wired into codebase; prerequisite for BLG-GOV-35 and BLG-OPS-26
**Effort:** S (~1 day)
**Provisional-Target:** v4.0
**Status: ✅ COMPLETE — v4.0 — ST-12 — cycle: 2026-05-22__release-v4.0 — 2026-05-25**

**Problem**
BLG-FEAT-24 (AI thesis generation) was marked complete in v3.8 but no Gemini code exists in the codebase — no `google-generativeai` dependency, no env var, no service, no endpoint. BLG-GOV-35 (Gemini audit trail) and BLG-OPS-26 (cost tracking) both instrument Gemini API calls; they have nothing to build on until the base wiring exists. This is a blocking prerequisite for both v4.0 EPIC-03 Sprint 2 stories.

**Scope**
- Add `google-generativeai` to `backend/requirements.txt`
- Wire `GEMINI_API_KEY` env var (Render + local `.env`)
- Create `backend/services/gemini_service.py` with `generate_setup_thesis(ticker, signal_data, plan_data) -> dict` using `gemini-1.5-flash`; returns `{thesis, model_version, prompt_version}` or graceful error
- Add `POST /trade-plans/{plan_id}/generate-thesis` endpoint in `backend/routers/trade_plans.py`
- Frontend: "Generate Thesis" button on TradePlan page that calls the endpoint and populates `setup_thesis` field

**Acceptance Criteria**
- `google-generativeai` present in `requirements.txt`
- `GEMINI_API_KEY` env var documented in `.env.example`
- `POST /trade-plans/{plan_id}/generate-thesis` returns `{thesis, model_version, prompt_version}` when key is set
- Returns graceful error (not 500) when `GEMINI_API_KEY` is absent
- Frontend button triggers generation and populates `setup_thesis` textarea
- New endpoint registered in `backend/routers/test.py` and `docs/reference/openapi.yaml`

---

---

### BLG-QA-25 — Red Flag Journal E2E Playwright test (SI-01→SI-03 integration path)
**Priority:** P2 (Medium)
**Type:** QA / Test Coverage
**Owner:** QA & Testing Owner; QA Lead
**Source:** IDEA-qa-testing-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** v4.0
**Status: ✅ COMPLETE — v4.0 — ST-03 — cycle: 2026-05-22__release-v4.0 — 2026-05-25**

**Problem**
SC-RFJ-01/02/03 (v3.9) cover RFJ component-level display. The SI-01 → SI-03 integration path — where a SI-01 override event is written and subsequently appears in the Red Flag Journal — is not tested end-to-end. This integration path is the primary produce of the Arc 5 data pipeline and is critical to validate before SI-02/SI-04/SI-05 extend the event model.

**Scope**
- Playwright E2E test: navigate to a position → trigger pre-entry validation → acknowledge override → navigate to Red Flag Journal → verify override event is present with correct metadata (type, timestamp, rule breached)
- Cover: filter by event type → verify filtered results contain the override event
- Integrate into existing Playwright test suite

**Acceptance Criteria**
- Full SI-01→SI-03 integration path covered by Playwright test
- Test passes in CI
- Override event metadata (type, timestamp, rule) verified in RFJ display

---

---

### BLG-OPS-26 — Gemini API cost tracking
**Priority:** P2 (Medium)
**Type:** Operations / Cost Monitoring
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** IDEA-finops-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** v4.0
**Status: ✅ COMPLETE — v4.0 — ST-08 — cycle: 2026-05-22__release-v4.0 — 2026-05-25**

**Problem**
BLG-FEAT-24 (AI thesis generation, shipped v3.8) uses the Gemini API in production with no cost monitoring. The Gemini free tier is not unlimited; tracking monthly call volume and projected costs provides early warning of approaching tier boundaries before unexpected billing occurs.

**Scope**
- Instrument Gemini API call count per day/week (count of `generate_content` requests)
- Log call count to structured log or ops metrics table
- Monthly aggregate report: call count, projected monthly total, tier proximity
- Alert threshold: > 80% of free-tier monthly limit

**Acceptance Criteria**
- Gemini API call count logged per request
- Monthly aggregate computable
- Alert threshold defined and documented
- No change to BLG-FEAT-24 user-facing behaviour

---

---

### BLG-OPS-27 — Automated staging re-deployment on main merge
**Priority:** P2 (Medium)
**Type:** Operations / CI/CD
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days)
**Provisional-Target:** v4.0
**Status: ✅ COMPLETE — v4.0 — ST-09 — cycle: 2026-05-22__release-v4.0 — 2026-05-25**

**Problem**
Staging environment is currently manually re-synced after each main branch merge. This introduces risk of forgotten staging updates and adds lag to delivery verification runs. Automating the staging re-deployment trigger on main merges removes the manual step and ensures staging is always current.

**Scope**
- Configure Render staging auto-deploy trigger on main branch push
- Scope: trigger only when backend or frontend source files change (not on docs/governance-only commits) to conserve free-tier build minutes
- Confirm free-tier build minute impact is acceptable
- Coordinate with BLG-OPS-25 (smoke test) which depends on this deploy hook

**Acceptance Criteria**
- Staging auto-deploys on main merge for code changes
- Documentation-only commits do not trigger a deploy
- Free-tier build minute impact assessed and documented
- BLG-OPS-25 dependency satisfied (deploy hook available for smoke test integration)

---

---

### BLG-GOV-35 — Gemini thesis generation audit trail
**Priority:** P2 (Medium)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer; Head of Backend Engineering
**Source:** IDEA-ai-compliance-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days)
**Provisional-Target:** v4.0
**Status: ✅ COMPLETE — v4.0 — ST-07 — cycle: 2026-05-22__release-v4.0 — 2026-05-25**

**Problem**
BLG-FEAT-24 (AI thesis generation, shipped v3.8) generates AI setup thesis text using Gemini API in production. No audit trail records the model version, prompt version, or output hash per generation. As Gemini usage scales, retroactive compliance tracking becomes impossible. An audit trail should be implemented before usage volume increases.

**Scope**
- Audit trail record per generation: plan_id, model_version, prompt_version, input_hash (thesis generation request), output_hash, generated_at, user_acknowledged (bool)
- Storage: append-only table (gemini_audit_log) or structured log file
- Retention policy: minimum 90 days
- No change to user-facing BLG-FEAT-24 behaviour

**Acceptance Criteria**
- Audit log created for each Gemini thesis generation call
- Record fields present: model_version, prompt_version, input_hash, output_hash, generated_at
- Retention policy enforced (90-day minimum)
- No performance impact on thesis generation response time

---

---

### BLG-GOV-37 — Red flag endpoint authentication and PII review
**Priority:** P2 (Medium)
**Type:** Governance / Security Review
**Owner:** Cybersecurity & Trust Lead
**Source:** IDEA-cybersecurity-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** XS (~0.5 day)
**Provisional-Target:** v4.0
**Status: ✅ COMPLETE — v4.0 — ST-06 — cycle: 2026-05-22__release-v4.0 — 2026-05-25**

**Problem**
SI-03 Red Flag Journal endpoint (GET /portfolio/red-flag-journal, shipped v3.9) exposes trading strategy override events. A targeted review confirms: (1) the endpoint is protected by API key authentication (shipped v2.2), (2) response payloads do not expose PII or sensitive strategy parameters beyond event type and timestamp, (3) pagination does not leak adjacent users' data (single-user system, but confirm).

**Scope**
- Verify API key auth covers /portfolio/red-flag-journal
- Review response payload: confirm no PII, no sensitive position data, no information beyond event_type, rule_type, timestamp, severity
- Document findings in security review note filed in `docs/security/`

**Acceptance Criteria**
- Authentication confirmed (API key auth active on endpoint)
- Response payload reviewed: PII-free, no sensitive strategy data confirmed
- Review findings documented
- If gap found: remediation backlog item filed

---



## v4.2 Completions — Archived 2026-05-29 (Post-Ship Closure)

---

### BLG-BE-22 — Claude API prompt caching implementation assessment
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-10; assessment: DEFER — prefix <1,024 tokens, <10 calls/day)
**Priority:** P2 (Medium)
**Type:** Backend / Performance Optimisation
**Owner:** Head of Backend Engineering
**Source:** IDEA-backend-engineering-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~1 day)
**Provisional-Target:** v4.2

**Problem**
Anthropic SDK supports prompt caching for large, static prompt components. The thesis generation system prompt is a fixed structure repeated on every API call. If the system prompt qualifies for caching, cache hits would reduce input token costs and latency. No assessment has been done to determine cache eligibility or expected cost reduction.

**Scope**
- Assess thesis generation prompt structure for caching eligibility (>1024 tokens, static component)
- Estimate expected cache hit rate based on call patterns
- Estimate cost reduction from caching
- Produce assessment document; input to BLG-OPS-30 cost review

**Acceptance Criteria**
- Caching eligibility assessed (yes/no with evidence)
- If eligible: expected cache hit rate and cost reduction estimated
- Assessment document produced and reviewed by Head of Engineering

---

---

### BLG-QA-37 — Claude API Playwright mock strategy definition
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-09)
**Priority:** P1 (High)
**Type:** QA / Test Infrastructure
**Owner:** QA & Testing Owner; Head of Backend Engineering
**Source:** IDEA-qa-testing-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~1 day)
**Provisional-Target:** v4.2

**Problem**
POST /trade-plans/{plan_id}/generate-thesis now calls Claude API in production. No mock strategy has been defined for CI/Playwright tests. Without a mock, CI tests may make real API calls (incurring cost and introducing flakiness) or tests may be skipped entirely. A defined mock strategy ensures reproducible, cost-free CI test execution.

**Scope**
- Evaluate mock strategies: router-level fixture mock vs ANTHROPIC_API_KEY=mock env var vs test-mode response stub
- Select and document the preferred strategy
- Produce implementation guide for applying the strategy to existing Playwright tests for thesis generation

**Acceptance Criteria**
- Mock strategy selected and documented
- Implementation guide produced
- Reviewed by QA & Testing Owner and Head of Backend Engineering

---

---

### BLG-OPS-35 — Add v4.1 new endpoint to api_performance_baseline.md re-run
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-04; POST /ai/check-daily-cost baseline added: p50=205ms, p95=518ms)
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** Post-ship closure v4.1 — endpoint coverage drift advisory (STEP 6)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.2

**Problem**
POST /ai/check-daily-cost was added in v4.1 (ST-09) and is present in openapi.yaml but absent from api_performance_baseline.md. Performance re-runs require a live environment and human coordination — cannot be done during post-ship closure.

**Scope**
- Add POST /ai/check-daily-cost to api_performance_baseline.md measurement table with baseline timing data
- Coordinate with Infrastructure & Operations Owner for live environment timing run

**Acceptance Criteria**
- POST /ai/check-daily-cost appears in api_performance_baseline.md with at least estimated p50 latency
- Reviewed by Infrastructure & Operations Owner

---

---

### BLG-OPS-36 — Claude API usage first monthly review
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-05)
**Priority:** P1 (High)
**Type:** Operations / Cost Monitoring
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** IDEA-finops-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~1 day)
**Provisional-Target:** v4.2

**Problem**
v4.1 switched thesis generation from Gemini to Claude API. No cost monitoring is in place for Claude API usage. BLG-OPS-30 (originally Gemini cost tracking) should be updated to track Claude API costs. The first monthly review of actual Claude API call volume and cost establishes the monitoring baseline and alert threshold.

**Scope**
- Review actual Claude API call volume and cost from claude_audit_log (or equivalent) data
- Establish monitoring cadence (monthly) and cost alert threshold
- Update BLG-OPS-30 scope to reflect Claude API instead of Gemini
- Produce first monthly review report

**Acceptance Criteria**
- First monthly review report produced
- Monthly cadence and alert threshold defined
- BLG-OPS-30 scope update confirmed

---

---

### BLG-OPS-38 — Claude API log hygiene policy
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-03)
**Priority:** P2 (Medium)
**Type:** Operations / Security Hygiene
**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead
**Source:** IDEA-infra-ops-20260527-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.2

**Problem**
Render application logs for Claude API calls may inadvertently capture API keys, full prompt text, or sensitive data. No log level guidance exists for Claude API trace events. With SI-02 adding more AI-adjacent queries in future, establishing log hygiene policy pre-SI-02 is operationally prudent.

**Scope**
- Confirm Render logs do not capture ANTHROPIC_API_KEY or full prompt text
- Define log level for Claude API trace events (INFO for request metadata; DEBUG for full prompt — never in production)
- Define log retention policy pre-SI-02
- Document in ops notes

**Acceptance Criteria**
- Log hygiene policy document produced
- API key and full prompt exclusion from production logs confirmed
- Log retention policy defined

---

---

### BLG-OPS-39 — Claude API thesis generation latency baseline
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-06)
**Priority:** P2 (Medium)
**Type:** Operations / Performance Baseline
**Owner:** Head of Engineering; Infrastructure & Operations Owner
**Source:** IDEA-head-of-engineering-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~1 day)
**Provisional-Target:** v4.2

**Problem**
POST /trade-plans/{plan_id}/generate-thesis switched from Gemini to Claude API in v4.1. No p50/p95 latency baseline exists for the Claude-backed endpoint. Without a baseline, future AI feature additions (PO-02, Arc 4) cannot be regression-tested for latency impact.

**Scope**
- Establish p50/p95 latency baseline for POST /trade-plans/{plan_id}/generate-thesis (Claude API)
- Record in api_performance_baseline.md
- Define regression threshold (e.g. p95 > 2× baseline triggers review)

**Acceptance Criteria**
- p50/p95 latency measured (minimum 10 sample calls)
- Baseline recorded in api_performance_baseline.md
- Regression threshold defined

---

---

### BLG-SPEC-42 — AI thesis endpoint contract update for Claude
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-08; ai_thesis_generation.md v2.1.0; gemini_thesis_generation.md Superseded)
**Priority:** P1 (High)
**Type:** Spec Debt / API Contract
**Owner:** API Contracts Documentation Owner; Head of Specs Team
**Source:** IDEA-api-contracts-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.2

**Problem**
docs/specs/api_contracts/ai_thesis_generation.md was authored for the Gemini-backed thesis generation endpoint. v4.1 replaced Gemini with Claude API. The response schema now returns different fields (model_id, usage.input_tokens, usage.output_tokens, cache_hit). The contract must be updated to reflect the current Claude-backed implementation and openapi.yaml updated accordingly per BLG-GOV-55 rule.

**Scope**
- Update docs/specs/api_contracts/ai_thesis_generation.md to reflect Claude API response fields
- Update openapi.yaml to match updated contract schema
- Verify all field names and types match the v4.1 implementation

**Acceptance Criteria**
- Contract document updated with Claude API response fields
- openapi.yaml updated and consistent with contract
- No drift between contract and implementation for thesis generation endpoint

---

## 8. Governance Backlog


---

---

### BLG-GOV-57 — SI-04 Strategy Version Comparison pre-planning
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-12; si04_scope_definition.md v1.0)
**Priority:** P2 (Medium)
**Type:** Governance / Pre-Sprint Planning
**Owner:** Product Owner; Head of Specs Team
**Source:** IDEA-product-owner-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~1 day)
**Provisional-Target:** v4.2

**Problem**
SI-04 (Strategy Version Comparison) scope is not formally defined. Without pre-planning (strategy versions to compare, performance delta computation method, UI view), mid-sprint scope discovery risks will materialise. Pre-planning prevents last-minute sprint gate discovery.

**Scope**
- Define SI-04 feature scope: which strategy versions to compare, how performance delta is computed
- Define UI view: layout, data source, interaction model
- Output: SI-04 scope definition document; input to SI-04 sprint planning and BLG-GOV-62 §13 review

**Acceptance Criteria**
- SI-04 scope definition document produced
- Reviewed by Product Owner and Head of Specs Team

---

---

### BLG-GOV-59 — Backlog ID namespace integrity audit
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-13; 287 BLG IDs audited, 0 collisions)
**Priority:** P3 (Low)
**Type:** Governance / Hygiene
**Owner:** Head of Specs Team; PMO Lead
**Source:** IDEA-head-of-specs-20260527-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** XS (~0.5 day)
**Provisional-Target:** v4.2

**Problem**
With 80+ BLG items across 10 namespaces, no verification pass has been run to confirm no sequence gaps or ID collisions exist. A namespace count summary provides governance health visibility and catches any numbering errors introduced by concurrent backlog additions.

**Scope**
- Audit all BLG IDs in backlog.md and backlog_archive.md
- Verify: no sequence gaps, no ID collisions, namespace counts consistent with history
- Produce namespace count summary in run_manifest.md or cycle_record.md

**Acceptance Criteria**
- Audit complete with no gaps or collisions found (or gaps documented with explanation)
- Namespace count summary produced

---

---

### BLG-GOV-60 — SI-02 sprint planning prerequisites checklist
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-11; si02_prerequisites_checklist.md v1.0: 13 items, 4 Complete, 1 gate-conditional, 8 Open)
**Priority:** P1 (High)
**Type:** Governance / Sprint Planning Gate
**Owner:** PMO Lead; Head of Specs Team
**Source:** IDEA-pmo-lead-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~0.5 day)
**Provisional-Target:** Before SI-02 sprint planning seals

**Problem**
SI-02 has 8+ pre-planning backlog items across 5 domains (BLG-GOV-39/44/46/51, BLG-SPEC-37/39/41, BLG-BE-17/20/23). No consolidated readiness gate ensures all prerequisites are verified before sprint planning seals. Without a checklist, individual prerequisite misses are only discovered mid-sprint.

**Scope**
- Produce SI-02 sprint planning prerequisites checklist consolidating all pre-sprint items
- Integrate into release_planning_prompt.md or sprint_planning_prompt.md as a gated advisory step
- Sprint planning may not seal until all checklist items verified

**Acceptance Criteria**
- Prerequisites checklist produced and filed
- Integration point in sprint planning engine defined
- PMO Lead and Head of Specs Team sign-off

---

---

### BLG-GOV-61 — v4.1 staging sign-off process effectiveness review
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-13; deviation trend IMPROVED: v4.1=2 vs v4.0=4)
**Priority:** P2 (Medium)
**Type:** Governance / Process Review
**Owner:** Director of Quality; PMO Lead
**Source:** IDEA-director-of-quality-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~1 day)
**Provisional-Target:** v4.2

**Problem**
BLG-GOV-30 (staging-only AC designation, shipped v4.1) was intended to reduce last-minute P3 staging deviations. This review assesses whether the intervention worked: comparing staging deviation count in v4.1 against the v3.9/v4.0 baseline. Evidence-based governance quality check.

**Scope**
- Count P3 staging deviations in v4.1 vs v3.9/v4.0 baseline
- Assess whether BLG-GOV-30 staging-only AC designation reduced surprise deviations
- Produce findings note; input to future governance process decisions

**Acceptance Criteria**
- Deviation count comparison produced
- Effectiveness finding documented (improved / no change / insufficient data)
- Reviewed by Director of Quality

---

---

### BLG-GOV-63 — Claude API audit trail implementation
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-07; claude_audit_log table + GET /ai/claude-audit-log endpoint)
**Priority:** P2 (Medium)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer; Head of Backend Engineering
**Source:** IDEA-ai-compliance-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** M (~2 days)
**Provisional-Target:** v4.2

**Problem**
v4.1 replaced Gemini with Claude API. BLG-GOV-35 (Gemini audit trail) is COMPLETE but covered Gemini-specific logging. A Claude API equivalent audit trail must log per-request: request_id, endpoint, model_id, prompt_version, input_tokens, output_tokens, cost_usd, generated_at. Without this, AI usage volume growth proceeds without compliance logging.

**Scope**
- Implement per-request Claude API audit log (claude_audit_log table or equivalent)
- Log fields: request_id, endpoint, model_id, prompt_version, input_tokens, output_tokens, cost_usd, generated_at
- Analogous to BLG-GOV-35 implementation pattern

**Acceptance Criteria**
- Claude API audit log implemented and populated on each thesis generation call
- Log queryable for BLG-OPS-36 cost review
- Reviewed by AI Compliance & Governance Officer

---

---

### BLG-GOV-64 — Anthropic model version pinning policy
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-02; ai_model_version_pinning_policy.md v1.0; AI_MODEL env-var override removed)
**Priority:** P2 (Medium)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer; Head of Specs Team
**Source:** IDEA-ai-compliance-20260527-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.2

**Problem**
All Claude-backed features must pin to a specific Anthropic model ID (never use "latest" alias or unversioned model references). Unversioned model references create silent behaviour change risk when Anthropic updates model versions. This policy supersedes BLG-GOV-48 scope (displaced; Gemini retired v4.1).

**Scope**
- Define policy: all Claude-backed features must pin to a specific model ID (e.g., claude-3-5-sonnet-20241022)
- Define change management: model version update requires AI Compliance sign-off and QA re-test
- Apply immediately to thesis generation endpoint
- Document in AI governance notes or CLAUDE.md

**Acceptance Criteria**
- Policy document produced
- Thesis generation endpoint confirmed to use pinned model ID (not "latest")
- Reviewed by AI Compliance & Governance Officer and Head of Specs Team

---

---

### BLG-GOV-65 — Anthropic API key scope and security review
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-01; anthropic_api_key_scope_review.md; 3 sign-offs)
**Priority:** P1 (High)
**Type:** Governance / Security
**Owner:** Cybersecurity & Trust Lead
**Source:** IDEA-cybersecurity-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** XS (~0.5 day)
**Provisional-Target:** v4.2

**Problem**
BLG-GOV-49 (Gemini key scope minimisation review) is COMPLETE. The Anthropic API key introduced in v4.1 requires the equivalent review: confirm minimum required permissions, stored as env var only, not exposed in application logs or error traces. Without this review, the Claude key's security posture is unconfirmed.

**Scope**
- Confirm Anthropic API key has minimum required permissions
- Confirm key is stored as env var only (not in code or logs)
- Confirm key not exposed in application logs or error traces
- Document confirmation in api_key_register.md (BLG-GOV-50 scope)

**Acceptance Criteria**
- Security confirmation produced and documented
- No key exposure in logs confirmed
- Reviewed by Cybersecurity & Trust Lead

---

---

### BLG-GOV-66 — Anthropic API accountability assignment
**Shipped:** ✅ COMPLETE — v4.2 — 2026-05-28 — cycle: 2026-05-27__release-v4.2 (ST-01; AI Compliance Officer charter §4.1 updated with Anthropic provider coverage)
**Priority:** P2 (Medium)
**Type:** Governance / Role Clarity
**Owner:** Director of HR; AI Compliance & Governance Officer
**Source:** IDEA-director-of-hr-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** XS (~0.25 day)
**Provisional-Target:** v4.2

**Problem**
v4.1 introduced Claude API integration. It must be confirmed which agent role owns the Anthropic integration for compliance and governance. If the AI Compliance & Governance Officer's charter does not explicitly cover Anthropic (vs. Gemini), the charter must be updated. Accountability clarity is required before BLG-GOV-63/64/65 are sprint-planned.

**Scope**
- Review AI Compliance & Governance Officer charter for explicit Anthropic coverage
- If charter gap found: update charter to include Anthropic API accountability
- Document ownership confirmation in governance notes

**Acceptance Criteria**
- Charter review complete
- Ownership confirmed (or charter updated to add Anthropic coverage)
- Reviewed by Director of HR and AI Compliance & Governance Officer

---


---

## v4.2 Additional Completions — BLG-GOV-58 Archived 2026-05-29

---

### BLG-GOV-58 — STEP 5.2 returned_to_backlog in-flight clarification
**Shipped:** ✅ COMPLETE — pre-resolved by AUD-2026-05-27-003 (execution_prompt.md v3.29) before v4.2 planning; confirmed COMPLETE at groom backlog 2026-05-29
**Priority:** P2 (Medium)
**Type:** Governance / Prompt Patch
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** XS (~0.25 day)
**Provisional-Target:** v4.2 sprint seal (carry-forward OA-2 from v4.1)

**Problem**
execution_prompt.md STEP 5.2 does not explicitly confirm that `returned_to_backlog` is a valid status for PO-authorized in-flight story deferrals during sprint execution (not only at sprint close). ST-11 deferral in v4.1 required this path but STEP 5.2 language was ambiguous.

**Scope**
- Amend execution_prompt.md STEP 5.2 to clarify returned_to_backlog is valid for in-flight PO-authorized deferrals
- Head of Specs Team sign-off; bump execution_prompt.md version

**Acceptance Criteria**
- execution_prompt.md STEP 5.2 amended with in-flight deferral clarification
- Version bumped and prompt_change_log.md updated
- OPERATIONAL_GUIDE.md §14 updated

---


---

## Closed Items — v4.4 Post-Ship (2026-05-30)

*Archived by groom backlog STEP 12 — post-ship closure 2026-05-29__release-v4.4 — 2026-05-30*

---

### BLG-FE-52 — SI-02 drift detection result component pre-design
**Priority:** P2 (Medium)
**Type:** Frontend / Pre-Sprint Design
**Owner:** Base44 Frontend; Frontend Specs & UX Documentation Owner
**Source:** IDEA-base44-frontend-20260527-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~1 day)
**Provisional-Target:** ✅ COMPLETE — 2026-05-30 (cycle: 2026-05-29__release-v4.4)
**Shipped in:** v4.4
**Evidence:** docs/product/changelog.md#v44; claude/cycles/2026-05-29__release-v4.4/verification_report.md

**Gate criteria:** SI-02 sprint planning imminent.

**Problem**
Before SI-02 Playwright scenarios can be pre-designed (BLG-QA-31) and before BLG-FE-43 (SI-05 weekly digest component) is authored, the SI-02 drift detection result component interface must be defined: score badge vs percentage deviation display vs rule list format. Undefined component contracts delay sprint planning design reviews.

**Scope**
- Define drift detection result component display options (badge, %, rule list)
- Define component contract: data shape, empty state, loading state, threshold-breach state
- Output: component pre-design document; input to BLG-FE-53 interaction spec

**Acceptance Criteria**
- Component interface options documented and one selected/proposed
- Component data contract defined
- Gate condition verified before commencing

---

### BLG-FE-53 — SI-02 drift detection interaction spec
**Priority:** P1 (High)
**Type:** Frontend / Spec Pre-work
**Owner:** Frontend Specs & UX Documentation Owner
**Source:** IDEA-frontend-ux-20260527-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~1 day)
**Provisional-Target:** ✅ COMPLETE — 2026-05-30 (cycle: 2026-05-29__release-v4.4)
**Shipped in:** v4.4
**Evidence:** docs/product/changelog.md#v44; claude/cycles/2026-05-29__release-v4.4/verification_report.md

**Gate criteria:** SI-02 sprint planning imminent.

**Problem**
SI-02 drift detection results will display in the frontend. Without a defined interaction spec, the following questions are unresolved at sprint planning: Are breach notifications dismissable? Do they link to underlying trades? What are the empty state and loading state? These unknowns create mid-sprint scope discovery risk.

**Scope**
- Define drift detection result interaction model: dismissable/persistent, drill-down to trades, severity state transitions
- Define empty state (no drift data), loading state, threshold-breach state
- Required input for BLG-FE-43 UX component authoring

**Acceptance Criteria**
- Interaction spec document produced covering all observable states
- Dismissal, drill-down, and state transition behaviours defined
- Gate condition verified before commencing

---

### BLG-BE-17 — SI-02 drift detection query pre-design
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Spec Pre-work
**Owner:** Head of Backend Engineering
**Source:** IDEA-backend-engineering-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days)
**Provisional-Target:** ✅ COMPLETE — 2026-05-30 (cycle: 2026-05-29__release-v4.4)
**Shipped in:** v4.4
**Evidence:** docs/product/changelog.md#v44; claude/cycles/2026-05-29__release-v4.4/verification_report.md

**Gate criteria:** SI-02 sprint planning imminent.

**Problem**
SI-02 (Behavioural Drift Detection) requires rolling analysis queries over trade history comparing actual entry conditions against stated setup criteria. Mid-sprint discovery of missing data fields would require emergency schema migration. Pre-designing the queries before sprint planning surfaces data gaps that can be addressed in the sprint plan.

**Scope**
- Define data access patterns: which fields are required per trade record for drift analysis
- Draft SQL queries: rolling win-rate vs stated setup criteria per entry type, per regime
- Identify any missing fields requiring schema migration
- Output: technical pre-design document; input to SI-02 sprint planning
- Include assessment of query performance on current trade history volume

**Acceptance Criteria**
- Query pre-design document produced and reviewed by Head of Backend Engineering
- Missing data fields (if any) enumerated with migration scope estimate
- Document filed before SI-02 sprint planning seals
- Gate condition verified before sprint planning

---

### BLG-BE-18 — Arc 5 backend architecture review for SI query patterns
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Architecture
**Owner:** Head of Engineering
**Source:** IDEA-head-of-engineering-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days)
**Provisional-Target:** ✅ COMPLETE — 2026-05-30 (cycle: 2026-05-29__release-v4.4)
**Shipped in:** v4.4
**Evidence:** docs/product/changelog.md#v44; claude/cycles/2026-05-29__release-v4.4/verification_report.md

**Gate criteria:** SI-02 sprint planning imminent.

**Problem**
SI-02 and SI-04 will add analytical queries that may be expensive synchronously. Before SI-02 sprint planning, assessing whether a background job or queue pattern is needed prevents an architectural dead-end mid-sprint.

**Scope**
- Review current endpoint pattern (synchronous FastAPI) against SI-02/SI-04 query complexity
- Assess: synchronous viability, background job option (Celery/cron), response caching
- Recommendation: maintain synchronous or add background processing layer
- If background layer recommended: produce architecture decision record (ADR)

**Acceptance Criteria**
- Architecture review document produced
- Synchronous vs background recommendation made with rationale
- If background layer recommended: ADR filed and input to SI-02 sprint planning
- Gate condition verified before sprint planning

---

### BLG-BE-20 — SI-02 background job architecture design
**Priority:** P2 (Medium)
**Type:** Backend / Architecture
**Owner:** Head of Backend Engineering; Head of Engineering
**Source:** IDEA-backend-engineering-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~1 day)
**Provisional-Target:** ✅ COMPLETE — 2026-05-30 (cycle: 2026-05-29__release-v4.4)
**Shipped in:** v4.4
**Evidence:** docs/product/changelog.md#v44; claude/cycles/2026-05-29__release-v4.4/verification_report.md

**Gate criteria:** SI-02 sprint planning initiated.

**Problem**
SI-02 will require periodic re-computation of drift metrics across trade history. The background job architecture (task queue, scheduler, or on-demand computation approach) must be decided before sprint planning seals.

**Scope**
- Evaluate: on-demand, periodic background task (cron), or event-triggered (on trade close)
- Assess trade-offs for single-user Render deployment (no task queue infrastructure)
- Produce architecture decision record (ADR) scoped to SI-02 drift computation
- Input to SI-02 sprint planning acceptance criteria

**Acceptance Criteria**
- ADR produced and reviewed by Head of Engineering and Head of Backend Engineering
- Architecture approach selected with rationale
- Gate condition (SI-02 sprint planning initiated) verified before commencing

---

### BLG-BE-23 — SI-02 query index pre-assessment
**Priority:** P1 (High)
**Type:** Backend / Pre-Sprint Schema Work
**Owner:** Head of Engineering; Head of Backend Engineering
**Source:** IDEA-head-of-engineering-20260527-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~1 day)
**Provisional-Target:** ✅ COMPLETE — 2026-05-30 (cycle: 2026-05-29__release-v4.4)
**Shipped in:** v4.4
**Evidence:** docs/product/changelog.md#v44; claude/cycles/2026-05-29__release-v4.4/verification_report.md

**Gate criteria:** BLG-GOV-51 (SI-02 database query performance pre-assessment) result available.

**Problem**
BLG-GOV-51 assesses SI-02 drift detection query performance. Once results are available, required database indexes must be identified and a migration plan produced. Missing indexes at sprint execution would create blocking mid-sprint schema work.

**Scope**
- Using BLG-GOV-51 EXPLAIN ANALYZE results, identify required indexes for drift detection queries
- Produce migration plan: index definitions, estimated creation cost, migration timing
- Input to SI-02 sprint planning capacity estimate

**Acceptance Criteria**
- Required indexes identified (or confirmed none needed)
- Migration plan produced for any required indexes
- Gate condition (BLG-GOV-51 complete) verified before commencing

---

### BLG-QA-31 — SI-02 Playwright scenario pre-design
**Priority:** P2 (Medium)
**Type:** QA / Test Planning
**Owner:** QA & Testing Owner; Director of Quality
**Source:** IDEA-qa-testing-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~1 day)
**Provisional-Target:** ✅ COMPLETE — 2026-05-30 (cycle: 2026-05-29__release-v4.4)
**Shipped in:** v4.4
**Evidence:** docs/product/changelog.md#v44; claude/cycles/2026-05-29__release-v4.4/verification_report.md

**Gate criteria:** SI-02 sprint planning initiated.

**Problem**
SI-02 will produce new frontend surfaces requiring Playwright E2E coverage. Pre-designing scenarios before the sprint reduces in-sprint QA risk.

**Scope**
- Draft Playwright scenario set for SI-02: drift alert display, "no drift detected" state, drift metric details, period filter
- Aligned with DoQ standards: staging-only ACs must be designated at sprint planning
- Input to SI-02 sprint planning QA section

**Acceptance Criteria**
- Draft scenario set produced (DFT-01–DFT-13 defined)
- Gate condition (SI-02 sprint planning initiated) verified before commencing
- Director of Quality reviewed draft before sprint planning seals

---

### BLG-OPS-43 — Staging URL disambiguation in OPERATIONAL_GUIDE §7
**Priority:** P3 (Low)
**Type:** Operations / Documentation
**Owner:** Infrastructure & Operations Owner
**Source:** v4.3 lessons_learnt_cycle.md Phase 3 — 2026-05-29__release-v4.3
**Effort:** XS (~0.5 hr)
**Provisional-Target:** ✅ COMPLETE — 2026-05-30 (cycle: 2026-05-29__release-v4.4)
**Shipped in:** v4.4
**Evidence:** docs/product/changelog.md#v44; claude/cycles/2026-05-29__release-v4.4/verification_report.md

**Problem**
OPERATIONAL_GUIDE.md §7 staging guidance does not explicitly note that Render deploys two separate services (frontend SPA vs backend API) with different hostnames. During v4.3 execution, health checks and baselines were incorrectly targeted at the frontend SPA URL.

**Scope**
Add a "Staging URL disambiguation" subsection to OPERATIONAL_GUIDE.md §7 explicitly documenting frontend SPA URL vs backend API URL distinction and health check guidance.

**Acceptance Criteria**
- AC-01: "Staging URL disambiguation" section added with clear frontend vs backend URL distinction
- AC-02: Health check and baseline guidance updated to reference backend API URL explicitly
- AC-03: Version bumps and governance file edit checklist applied (Class 6 file)

---

### BLG-GOV-69 — qa_evidence_template.md: DoQ sign-off format for delegated_qa EPICs
**Priority:** P3 (Low)
**Type:** Governance / Template Improvement
**Owner:** Head of Specs Team
**Source:** v4.3 delivery verification Phase 4 lessons learnt — 2026-05-29__release-v4.3
**Effort:** XS (~0.5 hr)
**Provisional-Target:** ✅ COMPLETE — 2026-05-30 (cycle: 2026-05-29__release-v4.4)
**Shipped in:** v4.4
**Evidence:** docs/product/changelog.md#v44; claude/cycles/2026-05-29__release-v4.4/verification_report.md

**Problem**
EPIC-03 in v4.3 used a non-standard DoQ acknowledgement format for delegated_qa EPICs. Both formats valid but template should clarify.

**Scope**
Update qa_evidence_template.md to include both sign-off format examples for delegated_qa EPICs.

**Acceptance Criteria**
- Template adds example or note for aggregate DoQ acknowledgement format in delegated_qa EPIC context
- Both formats (individual DoQ sign-off, aggregate DoQ acknowledgement) documented as valid

---

### BLG-GOV-163 — roadmap_prompt.md STEP 8.1: advisory for empty Now horizon after Extended-tier rebalance
**Renumbered from:** BLG-GOV-71 (ID collision resolved — v6.6 ST-03; BLG-GOV-71 retained by the active backlog.md entry "Governance engine complexity assessment (gate-conditional)")
**Priority:** P2 (Medium)
**Type:** Governance / Process Improvement
**Owner:** Head of Specs Team
**Source:** v4.3 lessons_learnt_closure.md deferred item 1 — 3rd recurrence (v4.1, v4.2, v4.3)
**Effort:** XS (~0.5 hr)
**Provisional-Target:** ✅ COMPLETE — 2026-05-30 (cycle: 2026-05-29__release-v4.4)
**Shipped in:** v4.4
**Evidence:** docs/product/changelog.md#v44; claude/cycles/2026-05-29__release-v4.4/verification_report.md

**Problem**
When the Now horizon is empty after an Extended-tier no-change rebalance and no next-release section exists in current_roadmap.md, STEP -1.2 fires a gate error at the next release planning cycle. Recurred 3 consecutive cycles.

**Scope**
Add an advisory note to roadmap_prompt.md STEP 8.1: if Now horizon is empty after Extended-tier no-change rebalance and no next-release section exists, advise PO to add one now.

**Acceptance Criteria**
- AC-01: Advisory note added to STEP 8.1 of roadmap_prompt.md
- AC-02: Condition correctly scoped to Extended-tier no-change + empty Now horizon + no next-release section
- AC-03: Version bumps and governance file edit checklist applied

---

### BLG-GOV-72 — sprint_planning_prompt.md: frontend classification fast-path for React-only stories
**Priority:** P2 (Medium)
**Type:** Governance / Process Improvement
**Owner:** Head of Specs Team
**Source:** v4.3 lessons_learnt_closure.md deferred item 4 — 3rd consecutive sprint (v4.1/v4.2/v4.3 EPIC-04)
**Effort:** XS (~0.5 hr)
**Provisional-Target:** ✅ COMPLETE — 2026-05-30 (cycle: 2026-05-29__release-v4.4)
**Shipped in:** v4.4
**Evidence:** docs/product/changelog.md#v44; claude/cycles/2026-05-29__release-v4.4/verification_report.md

**Problem**
Stories involving prop/state threading bug fix, variable rename, or new section against locked spec have been misclassified as delegated_frontend for 3 consecutive sprints. Should default to autonomous.

**Scope**
Add a "frontend classification fast-path" to sprint_planning_prompt.md for these three story types.

**Acceptance Criteria**
- AC-01: Frontend classification fast-path added to sprint_planning_prompt.md
- AC-02: Three fast-path conditions explicitly listed with the default-autonomous rule
- AC-03: Version bumps and governance file edit checklist applied

---

### BLG-GOV-165 — execution_prompt.md: auto-set deviations_filed on delegation sign-off clearance
**Renumbered from:** BLG-GOV-73 (ID collision resolved — v6.6 ST-03; BLG-GOV-73 retained by the active backlog.md entry "Scheduled rebalance cadence review")
**Priority:** P3 (Low)
**Type:** Governance / Process Improvement
**Owner:** Head of Specs Team
**Source:** v4.3 lessons_learnt_closure.md deferred item 5 — 2026-05-29__release-v4.3
**Effort:** XS (~0.5 hr)
**Provisional-Target:** ✅ COMPLETE — 2026-05-30 (cycle: 2026-05-29__release-v4.4)
**Shipped in:** v4.4
**Evidence:** docs/product/changelog.md#v44; claude/cycles/2026-05-29__release-v4.4/verification_report.md

**Problem**
When setting sign_off_record.status = "cleared" for a delegated story, deviations_filed is not automatically set to true if no deviation record was filed, leading to batch corrections at sprint close.

**Scope**
Add a substep to execution_prompt.md delegation sign-off: when cleared + no deviation filed → deviations_filed = true.

**Acceptance Criteria**
- AC-01: Sign-off substep updated in execution_prompt.md
- AC-02: Condition covers: delegated story + cleared + no deviation record filed → deviations_filed = true
- AC-03: Version bumps and governance file edit checklist applied

---

### BLG-GOV-166 — qa_evidence_template.md: DoQ sign-off block example for delegated_qa pattern
**Renumbered from:** BLG-GOV-74 (ID collision resolved — v6.6 ST-03; BLG-GOV-74 retained by the active backlog.md entry "AI feature usage quarterly review (BLG-GOV-63 mandate)")
**Priority:** P3 (Low)
**Type:** Governance / Template Improvement
**Owner:** Head of Specs Team
**Source:** v4.3 lessons_learnt_closure.md deferred item 6 — 2026-05-29__release-v4.3
**Effort:** XS (~0.5 hr)
**Provisional-Target:** ✅ COMPLETE — 2026-05-30 (cycle: 2026-05-29__release-v4.4)
**Shipped in:** v4.4
**Evidence:** docs/product/changelog.md#v44; claude/cycles/2026-05-29__release-v4.4/verification_report.md

**Problem**
The qa_evidence_template.md DoQ sign-off block does not include an example for the delegated_qa pattern. Both formats are valid but the template doesn't clarify, causing ambiguity at sprint close QA review.

**Scope**
Update qa_evidence_template.md DoQ sign-off block to include an example for the delegated_qa pattern with both valid format variants shown.

**Acceptance Criteria**
- AC-01: DoQ sign-off block updated with delegated_qa example
- AC-02: Both "Signed off by: Director of Quality" and "Director of Quality: Confirmed — [owner]" shown as valid formats
- AC-03: Version bumps and governance file edit checklist applied

---

### BLG-GOV-70 — spec_references policy for documentation-creation stories

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-05-30
**Shipped in:** v4.5 (ST-04)
**Evidence:** claude/cycles/2026-05-30__release-v4.5/verification_report.md; docs/product/changelog.md#v45

execution_prompt.md §3.1.A step 2b (LL-v4.5-EX-02): doc-creation stories set spec_references to artefact path + delivery_note. BLG-GOV-70 is self-referential — ST-04 created the policy governing its own spec_references update.

---

### BLG-GOV-75 — execution_prompt.md: split DEL terminal-status write into sign-off and push steps

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-05-30
**Shipped in:** v4.5 (ST-01)
**Evidence:** claude/cycles/2026-05-30__release-v4.5/verification_report.md; docs/product/changelog.md#v45

**Problem**
The delegation log terminal-status write currently happens as a single operation, which can produce a stale delegation log state when a session is resumed mid-merge. The DEL record gets its `status` set but the `commit_sha` field remains empty until the push step runs in a later session, requiring a merge gate sync correction on each resume.

**Scope**
- Split DEL terminal-status write into two sub-steps: (a) write `status = "sign_off_cleared"` at delegation sign-off time; (b) write `commit_sha` at push step
- Add inline note to execution_prompt.md STEP 3 delegation close sequence

**Acceptance Criteria**
- DEL record write is split into two documented sub-steps
- No merge gate sync required for fresh session resumes after delegation clearance
- Version bump + governance file edit checklist applied

---

### BLG-GOV-76 — execution_prompt.md STEP 3.2.B: explicit pr_status sync after PR open

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-05-30
**Shipped in:** v4.5 (ST-02)
**Evidence:** claude/cycles/2026-05-30__release-v4.5/verification_report.md; docs/product/changelog.md#v45

**Problem**
After opening a PR, the execution engine records `pr_number` but does not immediately sync `pr_status`. If the PR is merged before the next engine invocation (e.g. by a human reviewer), the engine begins a fresh session with `pr_status = "open"` when it is already `"merged"`, causing incorrect state at STEP 5.0A pr_status sync.

**Scope**
- Add explicit pr_status sync step to STEP 3.2.B: after recording `pr_number`, run `gh pr view <pr_number> --json state` and update `pr_status` immediately
- Also update `EPIC.status` from `"done"` to `"merged"` at QA evidence commit time if PR was merged between steps

**Acceptance Criteria**
- STEP 3.2.B contains explicit pr_status sync after PR open
- EPIC.status updated to "merged" if PR already merged at QA evidence commit time
- Version bump + governance file edit checklist applied

---

### BLG-GOV-77 — execution_prompt.md: verification-class sub-criterion for pre-planning sprints

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-05-30
**Shipped in:** v4.5 (ST-03)
**Evidence:** claude/cycles/2026-05-30__release-v4.5/verification_report.md; docs/product/changelog.md#v45

**Problem**
The BLG-GOV-19 autonomous class sign-off requires criterion 1: "all stories autonomous". For pre-planning sprints where stories are delivered as document inspection (delegated_decision or delegated_backend with document-only deliverable), the EXECUTION classification is delegated but VERIFICATION is document inspection only. This triggers a spurious Tier 2 advisory at STEP 3.2.A, complicating sign-off for architecturally valid pre-planning epics.

**Scope**
- Add a verification-class sub-criterion to execution_prompt.md §3.2.A (or delivery_verification_prompt.md): if all stories' VERIFICATION is by document inspection only, criterion 1 of BLG-GOV-19 autonomous class may be satisfied if criteria 2/3/4 are met
- Scope to pre-planning sprint patterns only; document the condition clearly

**Acceptance Criteria**
- Sub-criterion added to autonomous class sign-off block
- Tier 2 advisory not triggered for pre-planning sprints where all verification is document inspection
- Version bump + governance file edit checklist applied

---

### BLG-GOV-39 — SI-02 §13 formal boundary review

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-05-30
**Shipped in:** v4.5 (ST-06)
**Evidence:** claude/cycles/2026-05-30__release-v4.5/verification_report.md; docs/product/changelog.md#v45; docs/product/decisions/decisions--2026-05-30__release-v4.5--SI-02-section13-review.md

**Problem**
SI-02 (Behavioural Drift Detection) involves rolling analysis comparing actual trade entries against stated setup criteria. Before sprint planning seals, formal §13 review must confirm: this is deterministic analysis of historical data, not a predictive signal; drift detection is display-only (shows patterns, does not recommend actions); the rolling window analysis is not an adaptive strategy parameter. Prevents last-minute sprint gate discovery.

**Scope**
- Run §13 checklist against SI-02 story set before sprint planning seals
- Confirm drift detection output is: deterministic, display-only, no automated recommendations
- Document binding conditions (e.g., "drift alerts are informational only; no automated position management")
- Sign-off recorded in sprint planning artefact

**Acceptance Criteria**
- §13 review completed; PASS or FAIL determination documented
- Binding conditions (if any) enumerated and recorded
- Gate condition (SI-02 sprint planning imminent) verified before initiating review

---

### BLG-SPEC-37 — SI-02 data schema pre-definition

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-05-30
**Shipped in:** v4.5 (ST-08)
**Evidence:** claude/cycles/2026-05-30__release-v4.5/verification_report.md; docs/product/changelog.md#v45; docs/specs/data_model/si02_data_schema.md; docs/specs/si02_gap_analysis.md

**Problem**
SI-02 (Behavioural Drift Detection) requires per-trade data fields (regime_at_entry, setup_type, signal_conditions) that may not be fully captured in the current trade/position data model. Discovering these gaps mid-sprint would require emergency schema migrations. Pre-defining the required data structures before sprint planning allows the sprint to include any necessary migration stories proactively.

**Scope**
- Identify all data fields required for SI-02 drift analysis
- Compare against current trade, position, and trade plan schemas
- Gap analysis: enumerate missing fields with migration complexity estimate
- Produce data schema pre-definition document: required fields, data types, tables affected, migration approach
- Input to SI-02 sprint planning and BLG-BE-17 (drift query pre-design)

**Acceptance Criteria**
- Schema pre-definition document produced
- Gap analysis complete: missing fields identified or confirmed absent
- Migration approach defined for any missing fields
- Document reviewed by Data Model Owner and Head of Specs Team before sprint planning

---

### BLG-SPEC-41 — SI-02 drift score metric definition

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-05-30
**Shipped in:** v4.5 (ST-07)
**Evidence:** claude/cycles/2026-05-30__release-v4.5/verification_report.md; docs/product/changelog.md#v45; docs/specs/metrics/si02_drift_score.md

**Problem**
SI-02 will surface a drift detection score to the user. The metric definition (format, rolling window, threshold bands, warning states, SI-05 digest integration) must be canonically defined before sprint planning to prevent mid-sprint metric design decisions that delay frontend implementation. This definition feeds BLG-SPEC-37 (schema) and BLG-FE-52 (component pre-design).

**Scope**
- Define user-facing drift detection score format: % deviation vs raw count vs index
- Define rolling window and threshold bands (green/amber/red states)
- Define warning state triggers and SI-05 weekly digest integration points
- Produce canonical metric definition document

**Acceptance Criteria**
- Metric definition document produced covering format, window, thresholds, and SI-05 integration
- Reviewed by Metrics Definitions & Analytics Canonical Owner and Head of Specs Team
- Gate condition (SI-02 sprint planning imminent) verified before commencing


---

## v4.6 Post-Ship Closure — Batch Archive (2026-05-31)

Archived by: Backlog Management Engine STEP 12, post-ship closure 2026-05-30__release-v4.6

| Item | Title | Resolution | Cycle |
|------|-------|------------|-------|
| BLG-FE-42 | Arc 5 navigation and information architecture cohesion review | Delivered — maintain current structure (ST-11); Head of UX & Design sign-off | 2026-05-30__release-v4.6 |
| BLG-FE-47 | Red Flag Journal design review scope document | Delivered — rfj_design_review_scope.md created; gate 2026-06-21 (ST-12); PO + Head of UX reviewed | 2026-05-30__release-v4.6 |
| BLG-BE-16 | Red flag events severity field | Delivered — severity column + backfill + filter (ST-09); staging verification pending BLG-OPS-45 | 2026-05-30__release-v4.6 |
| BLG-OPS-40 | Arc 5 hosting cost projection | Delivered — current Render Starter tier adequate; no upgrade (ST-10); FinOps sign-off | 2026-05-30__release-v4.6 |
| BLG-SPEC-32 | External API integration spec template | Delivered — _external_api_template.md; 6 required sections; Anthropic + Alpaca advisory (ST-21) | 2026-05-30__release-v4.6 |
| BLG-GOV-32 | Gate-condition clearing tracker at release planning | Delivered — release_planning_prompt.md v2.33 STEP 1.4 Gate-Condition Proximity Scan (ST-15, combined with BLG-GOV-43) | 2026-05-30__release-v4.6 |
| BLG-GOV-33 | PT-04 closed trade count audit | Delivered — Q1=6, Q2=0; gate NOT MET; 6th deferral documented (ST-16) | 2026-05-30__release-v4.6 |
| BLG-GOV-34 | Arc 4 data density risk trajectory assessment | Delivered — Option A; arc4_data_density_trajectory_v4.6.md; SI-02 ~Nov 2026, PT-04 ~Sep 2026 (ST-17) | 2026-05-30__release-v4.6 |
| BLG-GOV-41 | Sprint close automation failure investigation | Delivered — workflow functioning as designed; no fix required; investigation doc (ST-20) | 2026-05-30__release-v4.6 |
| BLG-GOV-43 | Arc 4 data density formal checkpoint | Delivered — release_planning_prompt.md v2.33 STEP 1.4 Gate-Condition Proximity Scan (ST-15, combined with BLG-GOV-32) | 2026-05-30__release-v4.6 |
| BLG-GOV-45 | Arc 6 Monte Carlo §13 pre-assessment | Delivered — PASS; 10 binding conditions; arc6_ps03_section13_preassessment.md (ST-18) | 2026-05-30__release-v4.6 |
| BLG-GOV-52 | Trade plan schema field count gate check | Delivered — 25 fields; 0 orphaned; 3 P3 process gaps; trade_plan_schema_audit_v4.6.md (ST-19) | 2026-05-30__release-v4.6 |
| BLG-GOV-30 | Sprint planning staging-only AC designation flag | Resolved v4.1 — sprint_planning_prompt.md v3.7 staging-only AC gate (OA-02) | Prior cycle (v4.1) |
| BLG-GOV-31 | Merge gate re-invocation advisory in sprint capacity template | Resolved v4.x — LL-v3.9-P3-1 in-session merge gate sync in execution_prompt.md | Prior cycle |
| BLG-GOV-40 | Delivery verification STEP 5.0A pr_number null guard | Resolved v4.1 — delivery_verification_prompt.md v2.6 (OA-04) | Prior cycle (v4.1) |
| BLG-GOV-55 | API contract same-sprint delivery rule | Resolved v4.1+ — CLAUDE.md §2 API contract + endpoint test suite rules added | Prior cycle |

---

## Closed Items — v4.8 Post-Ship (2026-06-02)

*Archived: 7 items shipped in v4.8 (cycle 2026-06-01__release-v4.8). Groom date: 2026-06-02.*

| Item | Title | Resolution |
|------|-------|------------|
| BLG-GOV-69 ✅ | §13 register completion (AUD-2026-05-30-001 gap) | Shipped v4.8 ST-01 — OPERATIONAL_GUIDE.md §14 updated; all 7 Class 6 prompts verified in §13 and §14; AUD gap closed |
| BLG-GOV-70 ✅ | Agent charter header compliance remediation | Shipped v4.8 ST-02 — pre-met in v4.5 EPIC-02 ST-05; verified across all 23 agent files |
| BLG-GOV-72 ✅ | AUD-2026-05-30-006 gap resolution verification | Shipped v4.8 ST-03 — all 3 v4.4 deferred patches confirmed resolved in v4.5; gap formally closed |
| BLG-OPS-46 ✅ | Build minutes monitoring policy | Shipped v4.8 ST-04 — build_minutes_monitoring_policy.md v1.0 created; 80% threshold; billing reset documented |
| BLG-OPS-47 ✅ | Dependency audit post-v4.7 | Shipped v4.8 ST-05 — security_register.md v1.0; pip clean; 45 npm vulns (21 HIGH devDep); BLG-OPS-49/50 filed |
| BLG-QA-39 ✅ | Coverage matrix update and v4.7 contract completeness verification | Shipped v4.8 ST-06 — playwright_coverage_matrix.md v1.1; GET /reports/monthly-pnl v0.6 verified |
| BLG-SPEC-43 ✅ | SI-04 strategy version comparison endpoint contract | Shipped v4.8 ST-07 — strategy_version_comparison_contract.md v0.1.0; placeholder in openapi.yaml |

---

## Closed Items — v4.9 Post-Ship (2026-06-02)

*Archived: 5 items shipped in v4.9 (cycle 2026-06-02__release-v4.9). Groom date: 2026-06-02.*

| Item | Title | Resolution |
|------|-------|------------|
| BLG-OPS-49 ✅ | npm devDependency HIGH CVEs (react-scripts chain) | Shipped v4.9 ST-01, EPIC-01 — npm audit fix applied; HIGH=0; 6 moderate remain (CRA chain, non-production); security_register.md Audit 001 updated |
| BLG-OPS-50 ✅ | Anthropic SDK upgrade (0.40.0 → current) | Shipped v4.9 ST-02, EPIC-01 — anthropic 0.40.0→0.105.2; 447 tests passing; security_register.md Upgrade 001 updated; AC-04 staging deferred: BLG-OPS-52 |
| BLG-QA-40 ✅ | Wire Phase B CI with real Postgres service to catch missing-column errors | Shipped v4.9 ST-03, EPIC-02 — postgres:15 service container; DATABASE_URL injected; Phase A unaffected; 13 pre-existing failures fixed |
| BLG-QA-41 ✅ | Schema smoke test: assert lifecycle columns exist on positions table | Shipped v4.9 ST-04, EPIC-02 — tests/test_schema.py; skips Phase A (stub); passes Phase B with real Postgres |
| BLG-GOV-78 ✅ | roadmap_prompt.md STEP 8.1 Empty Now Horizon gate strengthening | Shipped v4.9 ST-05, EPIC-03 — roadmap_prompt.md v6.7→v6.8; STEP 8.1 soft gate; OPERATIONAL_GUIDE.md v4.25→v4.26; HoST + PMO Lead sign-off |

---

## Closed Items — v5.0 Post-Ship (2026-06-03)

*Archived: 13 items shipped in v5.0 (cycle 2026-06-03__release-v5.0). Groom date: 2026-06-03.*

| ID | Title | Ship note |
|----|-------|-----------|
| BLG-GOV-79 ✅ | Append 7 missing prompt_change_log.md entries for cycles 31–35 | Shipped v5.0 ST-01, EPIC-01 — all 7 entries verified present; AUD-2026-06-02 AUD-001 closed |
| BLG-GOV-80 ✅ | Add governance file edit check to execution_prompt.md STEP 8 commit | Shipped v5.0 ST-04, EPIC-02 — execution_prompt.md v3.35→v3.36; STEP 8 git-diff scan; OPERATIONAL_GUIDE §8+§14 updated; HoST sign-off |
| BLG-GOV-81 ✅ | Fix 5 non-standard agent file headers (setext → ATX; trailing backslash) | Shipped v5.0 ST-02, EPIC-01 — all 5 files corrected: ai_compliance_governance_officer.md, cybersecurity_trust_lead.md, director_of_hr.md, financial_reporting_records_owner.md, finops_resource_architect.md |
| BLG-GOV-82 ✅ | Strengthen post-ship audit advisory to prevent multi-cycle skips | Shipped v5.0 ST-05, EPIC-02 — post_ship_closure.md v2.12→v2.13; dual-condition check (% 3 == 0 OR gap ≥ 4); last_audit_cycle_count field added |
| BLG-GOV-83 ✅ | Document PO acceptance requires GitHub review approval (not PR comment) | Shipped v5.0 ST-03, EPIC-01 — pull_request_template.md v1.2→v1.3; "Product Owner Acceptance (Hard Gate)" section + GitHub Approve instruction; DoQ sign-off |
| BLG-FEAT-43 ✅ | Insufficient-allocation signal: distinct status and inline explanation | Shipped v5.0 ST-06, EPIC-03 — allocation_insufficient status + reason field; SignalCard orange "Cannot Size" badge + reason inline; openapi.yaml + test.py + SC-SS-01b updated |
| BLG-BE-25 ✅ | Fix pre-entry regime gate to use shared market status instead of independent yf.download | Shipped v5.0 ST-07, EPIC-03 — 5-min module-level cache in check_market_regime(); all callers share one result per window; unit tests covering cache hit/miss added |
| BLG-OPS-52 ✅ | Anthropic SDK 0.40.0 → 0.105.2 staging verification | Shipped v5.0 ST-08, EPIC-03 — staging verification: POST /generate-thesis HTTP 200 + non-null thesis; POST /ai/check-daily-cost HTTP 200 + cost structure; I&O Owner sign-off 2026-06-03 |
| BLG-FE-60 ✅ | SI-05 notification channel trade-off document | Shipped v5.0 ST-09, EPIC-04 — si05-notification-channel-tradeoff.md created; Telegram confirmed as delivery channel; PO decision recorded 2026-06-03 |
| BLG-GOV-86 ✅ | SI-05 Phase 1 Telegram message format specification | Shipped v5.0 ST-10, EPIC-04 — si05-telegram-message-format-spec.md v1.0; section structure, data bindings GET /analytics/arc5-compliance, char budget ~265/4096, failure modes; HoST sign-off |
| BLG-GOV-87 ✅ | SI-02 frontend re-entry trigger criteria definition | Shipped v5.0 ST-11, EPIC-04 — si02-reentry-trigger-criteria.md; hard gate ≥20 closed trades; soft advisory ≥3 months; PMO check from v5.1; PMO Lead + PO sign-off |
| BLG-GOV-88 ✅ | SI-04 formal binding conditions decisions document | Shipped v5.0 ST-12, EPIC-04 — decisions--2026-06-03__release-v5.0--SI-04-binding-conditions.md; all 6 §13 binding conditions; Strategy Rules & System Intent Owner sign-off |
| BLG-BE-26 ✅ | SI-02 lightweight drift summary assessment (backend-only state mitigation) | Shipped v5.0 ST-13, EPIC-04 — si02-drift-summary-feasibility-assessment.md; feasible with conditions; 3 UX risks + mitigations; minimal scope (Reports page, 3 metrics, advisory framing); PO sign-off |

---

## Closed Items — v5.1 Post-Ship (2026-06-04)

*Archived: 5 items shipped in v5.1 (cycle 2026-06-21__release-v5.1). Groom date: 2026-06-04.*

| ID | Title | Ship note |
|----|-------|-----------|
| BLG-GOV-67 ✅ | SI-05 early delivery (Phase 1 without SI-02) | Shipped v5.1 ST-01, EPIC-01 — backend/services/si05_digest_service.py; POST /digest/si05/send; 21 unit tests; SI-01+SI-03 gate confirmed 2026-06-21; 1 P3 deviation DEV-v51-EPIC01-01 filed (BLG-SPEC-47) |
| BLG-SPEC-45 ✅ | SI-05 financial reporting scope verification (BLG-GOV-86 review) | Shipped v5.1 ST-02, EPIC-01 — BLG-GOV-86 reviewed; financial reporting confirmed OUT OF SCOPE for Phase 1; scope decision: docs/product/decisions/si05-financial-reporting-scope-decision.md; FR&R Owner sign-off |
| BLG-FE-61 ✅ | SignalCard allocation_insufficient badge Playwright E2E coverage | Shipped v5.1 ST-04, EPIC-03 — tests/e2e/signals-allocation-insufficient.spec.js; 5 scenarios covering SC-SIG-AI-01/02/03; all pass in CI; BLG-FE-61 3-cycle recurrence closed |
| BLG-QA-43 ✅ | compliance_summary field population validation | Shipped v5.1 ST-05, EPIC-03 — code review confirmed all 5 Arc 5 compliance fields present; staging AC-01 deferred to staged verification sprint (I&O Owner sign-off outstanding) |
| BLG-GOV-89 ✅ | Staged verification sprint protocol document | Shipped v5.1 ST-06, EPIC-03 — docs/operations/staged_verification_sprint_protocol.md v1.0; trigger conditions, batching approach, evidence format, sprint sizing; DoQ + PMO Lead sign-off |


---

## Closed Items — v5.2 Post-Ship (2026-06-08)

*Archived: 15 items shipped in v5.2 (cycle 2026-06-08__release-v5.2). Groom date: 2026-06-08.*

| ID | Title | Ship note |
|----|-------|-----------|
| BLG-BE-32 ✅ | SI-05 Telegram delivery retry and failure handling | Shipped v5.2 ST-05, EPIC-02 — _send_telegram_request() with 30s/60s backoff; ERROR logging; 3 unit tests; injectable _sleep_fn for CI; 24 tests passing; staging AC-04 PASS |
| BLG-BE-33 ✅ | SI-05 digest delivery log table | Shipped v5.2 ST-06, EPIC-02 — si05_digest_log table (id/sent_at/status/event_count/telegram_message_id/error_message/created_at); CREATE TABLE IF NOT EXISTS guard; log rows on both paths; registered in main.py on_startup(); Data Model Owner sign-off; staging AC-04 PASS |
| BLG-QA-46 ✅ | SI-05 digest service edge case test gap analysis | Shipped v5.2 ST-13, EPIC-04 — 2 gaps found and fixed: test_telegram_api_connection_failure_logs_error + test_message_truncation_at_character_limit; 26 tests total passing; QA Lead sign-off |
| BLG-QA-47 ✅ | SI-05 Phase 1 acceptance test protocol | Shipped v5.2 ST-14, EPIC-04 — docs/qa/si05_acceptance_test_protocol.md produced; covers v5.1 deferred ACs (AC-09 Telegram delivery; AC-01 compliance_summary); Director of Quality sign-off |
| BLG-QA-48 ✅ | Regression test suite baseline refresh post-v5.1 | Shipped v5.2 ST-15, EPIC-04 — POST /digest/si05/send confirmed in test.py; 5 Playwright scenarios confirmed in CI; BLG-QA-50 formal baseline doc filed; QA Lead sign-off |
| BLG-SPEC-47 ✅ | Align SI-05 pass_rate computation with BLG-GOV-86 §5.2 | Shipped v5.2 ST-03, EPIC-01 — Option(a) chosen: BLG-GOV-86 §5.2 amended to accept volume-weighted overall rate; si05-telegram-message-format-spec.md v1.1→v1.2; DEV-v51-EPIC01-01 resolved and closed; Head of Specs Team sign-off |
| BLG-SPEC-48 ✅ | POST /digest/si05/send API contract gap check and authoring | Shipped v5.2 ST-04, EPIC-01 — digest_endpoints.md v0.2→v0.3 with authentication requirements section; API Contracts & Documentation Owner + Head of Specs Team sign-off |
| BLG-OPS-55 ✅ | Deployment runbook update for SI-05 operational environment | Shipped v5.2 ST-07, EPIC-02 — docs/ops/production_deployment_runbook.md v0.1→v0.2; §6 added for SI-05 env vars, cron schedule, failure detection, health check; Infrastructure & Operations Owner sign-off |
| BLG-OPS-56 ✅ | SI-05 service scheduled run health check | Shipped v5.2 ST-08, EPIC-02 — docs/ops/si05_health_check_procedure.md created; 3 check options; escalation path; weekly cadence; Infrastructure & Operations Owner sign-off |
| BLG-GOV-94 ✅ | SI-05 Phase 1 delivery verification protocol | Shipped v5.2 ST-14, EPIC-04 — docs/qa/si05_delivery_verification_protocol.md created; covers AC-09 Telegram + AC-01 compliance_summary; cross-referenced with acceptance test protocol; Director of Quality sign-off |
| BLG-GOV-96 ✅ | SI-05 Phase 1 effectiveness measurement criteria | Shipped v5.2 ST-16, EPIC-04 — 3 effectiveness criteria defined; 30-day review scheduled 2026-07-04; criteria at claude/cycles/2026-06-08__release-v5.2/si05_effectiveness_criteria.md; Product Owner sign-off |
| BLG-GOV-97 ✅ | Claude API model deprecation compliance check | Shipped v5.2 ST-09, EPIC-03 — PASS: claude-haiku-4-5-20251001 not deprecated; check at docs/governance/ai_model_deprecation_check_v52.md; next review 2026-09-08; AI Compliance & Governance Officer sign-off |
| BLG-GOV-98 ✅ | Telegram bot token minimal-permission security review | Shipped v5.2 ST-10, EPIC-03 — PASS with recommendation: send-only confirmed; BotFather manual check recommended; security_register.md updated (Review 002); Cybersecurity & Trust Lead sign-off |
| BLG-GOV-99 ✅ | SI-05 digest endpoint authentication review | Shipped v5.2 ST-11, EPIC-03 — GAP_FOUND: POST /digest/si05/send unauthenticated; BLG-BE-35 P2 filed; security_register.md updated (Review 003); Cybersecurity & Trust Lead sign-off |
| BLG-GOV-100 ✅ | Backend endpoint documentation coverage audit post-v5.1 | Shipped v5.2 ST-12, EPIC-03 — 50 routes enumerated; 6 contract gaps (BLG-SPEC-49/50/51/52); audit at docs/ops/endpoint_coverage_audit_v52.md; Head of Engineering sign-off |

---

## Closed Items — v5.3 Post-Ship (2026-06-09)

*Archived: 22 items shipped in v5.3 (cycle 2026-06-08__release-v5.3). Groom date: 2026-06-09.*

| ID | Title | Ship note |
|----|-------|-----------|
| BLG-SPEC-49 ✅ | Author GET /ai/journal-summary/history API contract | Shipped v5.3 ST-04, EPIC-01 — ## GET /ai/journal-summary/history added to ai_endpoints.md v1.1; openapi.yaml updated; API Contracts & Documentation Owner sign-off |
| BLG-SPEC-50 ✅ | Author GET /analytics/compliance-metrics API contract | Shipped v5.3 ST-05, EPIC-01 — ## GET /analytics/compliance-metrics added to analytics_endpoints.md v2.2.0; openapi.yaml updated; API Contracts & Documentation Owner sign-off |
| BLG-SPEC-51 ✅ | Author GET /news/{ticker} API contract | Shipped v5.3 ST-06, EPIC-01 — news_endpoints.md v1.0 created; openapi.yaml updated; API Contracts & Documentation Owner sign-off |
| BLG-SPEC-52 ✅ | Author watchlist endpoint contracts + openapi.yaml + test.py | Shipped v5.3 ST-07, EPIC-01 — watchlist_endpoints.md v1.0 created (GET/POST/DELETE); openapi.yaml + test.py + SystemStatus.js + SC-SS-01b updated; API Contracts & Documentation Owner + Head of Specs Team sign-off |
| BLG-SPEC-53 ✅ | BLG-SPEC-49–52 contract gap resolution plan | Shipped v5.3 ST-01, EPIC-01 — api_contract_gap_resolution_plan.md produced; 6 gaps priority-ranked; Head of Specs Team + API Contracts & Documentation Owner sign-off |
| BLG-SPEC-54 ✅ | openapi.yaml completeness audit against all 50 routes | Shipped v5.3 ST-02, EPIC-01 — all 50 routes audited; gaps confirmed and resolved; API Contracts & Documentation Owner sign-off |
| BLG-BE-35 ✅ | Add API key authentication to POST /digest/si05/send | Shipped v5.3 ST-08, EPIC-02 — Depends injection pattern; 401 on missing/invalid key; unit test added; digest_endpoints.md updated; Cybersecurity & Trust Lead + Head of Engineering sign-off |
| BLG-OPS-57 ✅ | SI-05 Telegram delivery failure alerting | Shipped v5.3 ST-09, EPIC-02 — FAILED status logged; ERROR-level Render log alert; ops runbook updated; Infrastructure & Operations Owner sign-off |
| BLG-OPS-58 ✅ | CI secret scanning gate | Shipped v5.3 ST-10, EPIC-02 — gitleaks via .github/workflows/secret-scanning.yml + .gitleaks.toml; test_token advisory accepted as low-risk; Cybersecurity & Trust Lead sign-off |
| BLG-QA-51 ✅ | BLG-SPEC-49–52 QA acceptance criteria definition | Shipped v5.3 ST-03, EPIC-01 — endpoint_contract_qa_criteria_template.md produced; reusable template; Director of Quality sign-off |
| BLG-QA-52 ✅ | Tax year P&L boundary edge case validation | Shipped v5.3 ST-18, EPIC-04 — 6 boundary scenarios in tests/test_tax_year_pnl_boundary.py; all passing; Financial Reporting & Records Owner + QA Lead sign-off |
| BLG-QA-53 ✅ | SI-05 digest Playwright E2E coverage | Shipped v5.3 ST-19, EPIC-04 — 4 Playwright scenarios in tests/e2e/si05-digest-delivery.spec.js; Telegram API mocked; all passing in CI; QA Lead sign-off |
| BLG-QA-54 ✅ | Playwright coverage matrix update post-v5.2 | Shipped v5.3 ST-20, EPIC-04 — playwright_coverage_matrix.md updated; v5.2 + v5.3 additions counted; gaps identified; Director of Quality sign-off |
| BLG-GOV-104 ✅ | strategy_rules.md §11 parameter validation (first annual) | Shipped v5.3 ST-17, EPIC-03 — strategy_parameter_validation_v53.md produced; ATR multiplier + regime gate + position sizing validated (insufficient data: 6 closed trades); parameters unchanged; Strategy Rules & System Intent Owner + Product Owner sign-off |
| BLG-GOV-107 ✅ | SI-02 frontend activation criteria precision | Shipped v5.3 ST-13, EPIC-03 — current_roadmap.md SI-02 entry updated with 3 precise checkable gate conditions; PMO Lead + Product Owner sign-off |
| BLG-GOV-108 ✅ | AI model pin update policy (BLG-GOV-64 gap) | Shipped v5.3 ST-14, EPIC-03 — ai_model_version_pinning_policy.md produced; trigger, process, sign-offs, 30-day deprecation response timeline; AI Compliance Governance Officer + Head of Engineering sign-off |
| BLG-GOV-109 ✅ | AI audit log retention policy | Shipped v5.3 ST-15, EPIC-03 — ai_audit_log_retention_policy.md produced; 12-month retention; cleanup mechanism; AI Compliance Governance Officer + Infrastructure & Operations Owner sign-off |
| BLG-GOV-110 ✅ | Arc 4 trade_plan data completeness audit | Shipped v5.3 ST-16, EPIC-03 — arc4_trade_plan_data_completeness_audit.md produced; per-field null% computed; Arc 4 risk assessed; Data Model & Domain Schema Owner + Product Owner sign-off |
| BLG-GOV-113 ✅ | SI-05 effectiveness review protocol (gate-conditional) | Shipped v5.3 ST-23, EPIC-03 — si05_effectiveness_review_protocol.md produced; participants/evidence/output/authority defined; completed by 2026-07-01 gate; Director of Quality + Product Owner sign-off |
| BLG-GOV-114 ✅ | si05_digest_log schema validation for effectiveness review | Shipped v5.3 ST-24, EPIC-03 — si05_digest_log_schema_validation.md produced; schema PASS; Director of Quality + Data Model & Domain Schema Owner sign-off |
| BLG-FE-66 ✅ | Red Flag Journal post-launch UX review | Shipped v5.3 ST-21, EPIC-04 — rfj_ux_review_v53.md produced; top-3 friction points documented; follow-up items filed; Base44 Frontend Prompt Owner + Head of UX & Design sign-off |
| BLG-FE-67 ✅ | BLG-FE-64 visual design review scope definition | Shipped v5.3 ST-22, EPIC-04 — blg_fe_64_scope_definition.md produced; distinct from BLG-FE-66; Frontend Specs & UX Documentation Owner + Head of UX & Design sign-off |

---

## Closed Items — v5.4 Post-Ship (2026-06-10)

*Archived: 3 items shipped in v5.4 (cycle 2026-06-09__release-v5.4). Groom date: 2026-06-10.*

| ID | Title | Ship note |
|----|-------|-----------|
| BLG-OPS-60 ✅ | Add v5.3 new endpoints to api_performance_baseline.md re-run | Shipped v5.4 ST-01, EPIC-01 — 5 endpoint rows added (GET /ai/journal-summary/history, GET /news/{ticker}, GET /watchlist, POST /watchlist, DELETE /watchlist/{entry_id}) with live Render measurements; I&O Owner sign-off |
| BLG-FE-56 ✅ | Pre-entry panel: separate warn/fail override acknowledgement flow | Shipped v5.4 ST-02, EPIC-02 — pre_entry_override_ux_spec.md produced; warn/fail override flows separated; agent-mediated Head of UX & Design sign-off |
| BLG-GOV-92 ✅ | SI-05 Phase 2 activation criteria definition | Shipped v5.4 ST-04, EPIC-03 — si05_phase2_activation_criteria.md produced; hard gate + quality gate + Phase 1 effectiveness gate defined; PO-approved (agent-mediated) |

---

## Closed Items — v5.5 Post-Ship (2026-06-16)

*Archived: 10 items shipped in v5.5 (cycle 2026-06-10__release-v5.5). Groom date: 2026-06-16.*

| ID | Title | Ship note |
|----|-------|-----------|
| BLG-GOV-116 ✅ | sprint_planning_prompt.md within-sprint date gate advisory | Shipped v5.5 ST-01, EPIC-01 — advisory added to sprint_planning_prompt.md: stories with within-sprint date gates marked Status: conditional — gate <date> at planning; v bumped; Head of Specs Team sign-off |
| BLG-GOV-117 ✅ | execution_prompt.md pr_status read-after-open improvement | Shipped v5.5 ST-02, EPIC-01 — gh pr view called immediately after pr create; pr_status written from actual response; LL-v5.5-EX-02 mandatory persist-before-halt also applied; v3.41; Head of Specs Team sign-off |
| BLG-GOV-118 ✅ | qa_evidence commit discipline advisory in execution_prompt.md | Shipped v5.5 ST-03, EPIC-01 — pre-PR commit check for qa_evidence added; LL-v5.5-EX-01 branch ordering gate at STEP 5.0 also applied; v3.41; Head of Specs Team sign-off |
| BLG-BE-34 ✅ | Trade count gate-monitoring view | Shipped v5.5 ST-04, EPIC-02 — get_gate_metrics() function in database.py; GET /portfolio/gate-metrics endpoint; registered in test.py, openapi.yaml, conftest.py; Data Model & Domain Schema Owner sign-off |
| BLG-GOV-120 ✅ | Trade data density progress tracker | Shipped v5.5 ST-05, EPIC-02 — data density progress line added to SI-05 digest via si05_digest_service.py; SC-SS-01b Playwright test updated (65→66 fallback); I&O Owner sign-off |
| BLG-OPS-13 ✅ | Add new v2.8/v2.9/v3.0/v3.4/v3.9/v4.6 endpoints to api_performance_baseline.md re-run | Shipped v5.5 ST-06, EPIC-03 — 16 read endpoints measured; §18 added; 4 high-latency flags filed BLG-OPS-62/63/64; BLG-OPS-22 gate cleared; I&O Owner sign-off |
| BLG-OPS-54 ✅ | Add POST /digest/si05/send to api_performance_baseline.md | Shipped v5.5 ST-08, EPIC-03 — documented in §19.1 as external-dependency exclusion (Telegram API timeout); I&O Owner sign-off |
| BLG-OPS-61 ✅ | BLG-OPS-13 v5.1–v5.4 endpoint baseline extension | Shipped v5.5 ST-07, EPIC-03 — GET /watchlist p50=488ms, GET /portfolio/gate-metrics p50=543ms measured; §19 added; I&O Owner sign-off |
| BLG-QA-50 ✅ | Create formal regression test suite baseline document | Shipped v5.5 ST-09, EPIC-03 — docs/qa/regression_test_suite_baseline.md: 387 scenarios, 66 endpoints, 41 e2e spec files; DoQ sign-off 2026-06-11 |
| BLG-FE-65 ✅ | User journey map: SI-05 Telegram digest to app action | Shipped v5.5 ST-10, EPIC-03 — docs/ux/si05_user_journey_map.md: live staging walkthrough 2026-06-15; 2 friction findings (BLG-FE-73/74 filed); Head of UX & Design sign-off |

## Closed Items — v5.6 Post-Ship (2026-06-16)

| ID | Title | Delivery evidence |
|----|-------|------------------|
| BLG-FE-73 ✅ | Add deep links from SI-05 digest to relevant app screens | Shipped v5.6 ST-01, EPIC-01, PR #765 — deep links to Risk Dashboard + Red Flag Journal via FRONTEND_URL; AC-02 staging-deferred BLG-FE-75; Head of UX & Design sign-off |
| BLG-FE-74 ✅ | Clarify N/A pass rate reason in SI-05 digest message | Shipped v5.6 ST-02, EPIC-01, PR #765 — distinct messages: no_events vs data_unavailable; 13 new unit tests; Head of Backend Engineering sign-off |
| BLG-OPS-62 ✅ | Investigate GET /portfolio/concentration-status high latency | Shipped v5.6 ST-04, EPIC-02, PR #766 — 5-min TTL FX rate cache eliminates live HTTP call on every request; AC-03/04 staging verification deferred BLG-OPS-66; I&O Owner sign-off |
| BLG-OPS-63 ✅ | Investigate GET /portfolio/red-flag-journal high latency | Shipped v5.6 ST-05, EPIC-02, PR #766 — process-lifetime schema-once guard replaces per-request DDL; AC-03/04 staging verification deferred BLG-OPS-67; I&O Owner sign-off |
| BLG-OPS-64 ✅ | Investigate GET /analytics/behavioural-drift high latency | Shipped v5.6 ST-06, EPIC-02, PR #766 — schema-once guard + 15-min TTL result cache; AC-03/04/05 staging verification deferred BLG-OPS-68; I&O Owner sign-off |
| BLG-OPS-22 ✅ | Research data caching layer | Shipped v5.6 ST-07, EPIC-02, PR #766 — 15-min per-ticker TTL cache + screener invalidation + hit/miss logging; AC-04/05 staging verification deferred BLG-OPS-69; I&O Owner sign-off |
| BLG-OPS-65 ✅ | Anthropic API cost 14-cycle trend analysis | Shipped v5.6 ST-11, EPIC-03, PR #764 — est. $0.05–$0.15/month vs $5/month threshold (33–100× buffer); trajectory stable; next review 2026-12-16; FinOps & Resource Architect sign-off |
| BLG-QA-45 ✅ | Arc 5 QA completion criteria definition | Shipped v5.6 ST-09, EPIC-03, PR #764 — C-01 to C-05 defined; BLG-QA-26 gate condition updated; SI-05 Phase 2/SI-04/SI-02-backend-only excluded; PO + DoQ approved |
| BLG-QA-49 ✅ | Arc 5 test scenario completeness assessment | Shipped v5.6 ST-10, EPIC-03, PR #764 — arc5_test_coverage_assessment.md produced; 3 P3 Playwright gaps filed (BLG-QA-56/57/58); DoQ approved |
| BLG-GOV-106 ✅ | PT-04 trade count gate re-verification | Shipped v5.6 ST-08, EPIC-03, PR #764 — 13 closed trades (PO-provided); gate NOT MET (need 20); roadmap + BLG-FEAT-25 updated; trajectory accelerating; PMO Lead + PO sign-off |


---

## Groomed 2026-06-16 — Cycle v5.6 post-ship (103 items archived)

*Archived by: groom backlog run 2026-06-16. All items below had ✅ COMPLETE markers with ship evidence, or were superseded. 4 ephemeral Release Slice sections (v5.2–v5.5) also removed from active backlog.*

### BLG-FEAT-38 — Arc 5 compliance score in monthly P&L report ✅ COMPLETE v4.7 (2026-05-31)
**Priority:** P2 (Medium)
**Type:** Product Feature / Reporting
**Owner:** Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~2 days)
**Provisional-Target:** v4.1
**Completed:** ST-03, EPIC-02, cycle 2026-05-31__release-v4.7

**Gate cleared:** BLG-FEAT-36 ✅ COMPLETE v4.0 (validation_pass_rate_by_rule in Arc5ComplianceSection analytics endpoint) and BLG-FEAT-37 ✅ COMPLETE v4.0 (events_per_week metric in same delivery). Gate cleared inline at STEP 4.0, roadmap rebalance 2026-05-25__scheduled.

**Problem**
Monthly P&L report (shipped v3.1) covers financial performance. As Arc 5 ships compliance data, adding a strategy compliance section enables holistic monthly review: financial performance + behavioural discipline in one document.

**Scope**
- New section in monthly P&L report: strategy compliance period summary
- Fields: validation_pass_rate (period), override_count, red_flag_events_count, most_frequent_rule_breach
- Data sourced from BLG-FEAT-36 and BLG-FEAT-37 metrics

**Acceptance Criteria**
- Compliance section present in monthly P&L report output
- Data sourced from canonical metrics (BLG-FEAT-36, BLG-FEAT-37)
- Gate conditions verified before sprint planning

---


### BLG-FEAT-43 — Insufficient-allocation signal: distinct status and inline explanation ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P2 (Medium)
**Type:** Product Feature / Signal UX
**Owner:** Head of Backend Engineering; Head of UX & Design
**Source:** PO direction — 2026-06-02
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.0

**Problem**
When a signal's per-share GBP price exceeds the per-position allocation budget, the backend returns suggested_shares=0 but leaves status as "new" — indistinguishable from an actionable buy signal. SNDK has been rank-1 for weeks at ~£1,259/share against a ~£1,147 allocation, silently returning 0 shares with no explanation. For high-priced stocks this is a structural recurring gap, not an edge case.

**Scope**
- Backend: set status to "allocation_insufficient" (not "new") when suggested_shares=0 and price_gbp > allocation_gbp
- Backend: include a human-readable reason field (e.g. "1 share (£1,259) exceeds position allocation (£1,147) — cannot size")
- Frontend: display the reason inline on the signal card/row when status is "allocation_insufficient"
- Frontend: visually differentiate allocation_insufficient signals from actionable new signals
- (Deferred) Override path allowing user to manually record a share count — scope to be defined if and when taken up

**Acceptance Criteria**
- Signal with price_gbp > allocation_gbp has status "allocation_insufficient", not "new"
- A reason string is returned from the backend and displayed inline in the signal view
- Allocation_insufficient signals are visually distinct from new/watchlisted signals
- Existing signals with status "new" and suggested_shares > 0 are unaffected
- No change to already_held or watchlisted status logic

---


### BLG-FE-42 — Arc 5 navigation and information architecture cohesion review
**Priority:** P2 (Medium)
**Type:** Frontend / UX Design
**Owner:** Head of UX & Design
**Source:** IDEA-head-of-ux-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** M (~1–2 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 (Behavioural Drift Detection) in sprint planning — Arc 5 near-complete.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-11; maintain current structure; no changes recommended; Head of UX & Design sign-off)

**Problem**
As Arc 5 ships SI-02, SI-04, and SI-05 alongside existing SI-01 and SI-03, the "Trading" navigation section may become congested. A cohesion review before Arc 5 is complete ensures any structural navigation changes are planned proactively rather than reactively patched after all features ship.

**Scope**
- Review current Trading nav structure against projected Arc 5 complete state (SI-01 through SI-05)
- Assess: navigability, grouping logic, naming clarity, page depth
- Produce recommendation: maintain current or propose structural changes
- If changes recommended: author UX spec and file implementation item

**Acceptance Criteria**
- Cohesion review document produced
- Recommendation covers projected full Arc 5 nav inventory
- Gate condition verified by Head of UX & Design before sprint planning

---


### BLG-FE-47 — Red Flag Journal design review scope document
**Priority:** P2 (Medium)
**Type:** Frontend / UX
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-frontend-ux-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Problem**
RedFlagJournal.js (shipped v3.9) implemented the primary display. BLG-FE-41 (Red Flag Journal visual design review, gate: SI-03 live 30+ days) is now gate-eligible. A formal design review scope document should be produced before BLG-FE-41 sprint planning to define what aspects of the journal are in scope for the review: filters, pagination UI, empty state, colour/severity coding, and mobile layout.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-12; rfj_design_review_scope.md created; gate date 2026-06-21; PO + Head of UX & Design reviewed)

**Scope**
- Produce design review scope document for RedFlagJournal.js
- Define: what is reviewable (presentation, UX), what is out of scope (data structure, backend)
- Input to BLG-FE-41 sprint planning

**Acceptance Criteria**
- Design review scope document produced and filed
- Reviewed by Product Owner and Head of UX & Design
- Input to BLG-FE-41 before its sprint planning

---


### BLG-FE-49 — Pre-entry validation panel UX assessment
**Priority:** P2 (Medium)
**Type:** Frontend / UX
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Source:** IDEA-head-of-ux-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

✅ COMPLETE — 2026-05-31 — cycle 2026-05-31__release-v4.7 (ST-09, EPIC-04; pre_entry_panel_ux_assessment.md produced; 3 improvement candidates filed BLG-FE-56/57/58; Head of UX & Design sign-off; no implementation committed)

**Problem**
PreEntryValidationPanel (shipped v3.8) displays validation results and override acknowledgement. As Arc 5 evolves (SI-02, SI-05), the pre-entry panel will need to surface additional compliance context. A UX assessment of the current panel — layout, density, override acknowledgement flow — identifies improvement opportunities before Arc 5 sprint planning forces ad-hoc changes.

**Scope**
- Review PreEntryValidationPanel UX: layout clarity, override acknowledgement UX, text density
- Identify specific improvement candidates with rough effort estimates
- Assessment note filed; not a full redesign

**Acceptance Criteria**
- UX assessment note produced and reviewed by Product Owner
- Improvement candidates ranked by effort/value
- No sprint scope commitment required from this item

---


### BLG-FE-56 — Pre-entry panel: separate warn/fail override acknowledgement flow
**Priority:** P2 (Medium)
**Type:** Frontend / UX Improvement
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Source:** docs/product/ux/pre_entry_panel_ux_assessment.md — candidate P1 — cycle 2026-05-31__release-v4.7 (ST-09)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

✅ COMPLETE — 2026-06-10 — cycle 2026-06-09__release-v5.4 (ST-02, EPIC-02; pre_entry_override_ux_spec.md produced; agent-mediated Head of UX & Design sign-off)

**Problem**
PreEntryValidationPanel treats `warn` and `fail` checks with the same override acknowledgement checkbox. `fail` represents a strategy hard stop; `warn` is advisory. Identical acknowledgement paths may encourage reflexive override of hard stops. As Arc 5 compliance rigour increases, distinct override flows are warranted.

**Scope**
- Separate override path for `fail` checks (confirmation modal or explicit "I understand this violates my strategy") vs `warn` checks (current checkbox)
- `fail` acknowledgement should be more deliberate — extra friction is intentional
- Assessment only — scope to be confirmed at implementation sprint

**Acceptance Criteria**
- Override UX differentiates warn (advisory) from fail (strategy violation)
- Fail override requires additional explicit acknowledgement step
- Existing warn-only acknowledgement flow preserved for warn-only states

---


### BLG-FE-60 — SI-05 notification channel trade-off document ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P2 (Medium)
**Type:** Frontend / UX / Spec Pre-work
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design; Product Owner
**Source:** IDEA-frontend-ux-20260601-02 — Promoted-Backlog cycle 2026-06-02__scheduled (DL-037; STEP 5 debate advance; Challenger Clearance)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.0
**Sequencing constraint:** Must complete before BLG-GOV-67 (SI-05 Phase 1) sprint planning seals.

**Problem**
SI-05 Phase 1 is specified as Telegram push notification (existing infrastructure v2.4). No formal trade-off document compares Telegram push (immediate, out-of-app, format-constrained) vs in-app notification (integrated, discoverable, format-flexible). If the PO decides post-implementation that in-app was preferable, reversing a Telegram delivery mechanism requires a new sprint. A pre-implementation trade-off document locks in the channel decision with documented evidence before sprint planning seals.

**Scope**
- Trade-off document comparing: Telegram push (existing infra, character limit constraints, no in-app UX) vs in-app notification (new build, integrated, discoverable)
- Evaluation criteria: implementation effort, user discovery, format flexibility, alignment with existing v2.4 weekly digest pattern
- PO channel decision recorded; if Telegram confirmed: format constraints fed to BLG-GOV-86

**Acceptance Criteria**
- Trade-off document produced with evaluation across defined criteria
- PO channel decision explicitly recorded in document
- If Telegram confirmed: channel decision fed as input to BLG-GOV-86 (message format spec)
- Sequencing constraint: completed before BLG-GOV-67 sprint planning seals

---


### BLG-FE-61 — ST-06 allocation_insufficient SignalCard badge Playwright E2E coverage
**Priority:** P3 (Low)
**Type:** Frontend / QA
**Owner:** QA & Testing Owner
**Source:** v5.0 EPIC-03 ST-06 — frontend testing gate (LL-v3.1-EX-01); code review only; filed 2026-06-03 per CLAUDE.md §2 hard gate before PR opens
**Effort:** XS (<1h)
**Provisional-Target:** v5.1

**Problem**
ST-06 introduced a visible frontend change (SignalCard orange "Cannot Size" badge + reason inline when signal status = `allocation_insufficient`). No Playwright E2E test covers this observable AC. Code review was accepted for the v5.0 PR under the hard gate, but a Playwright scenario must be authored before the v5.1 sprint planning seals.

**Scope**
- Add a Playwright scenario to an appropriate `tests/e2e/` spec file
- Mock signal payload with `status: "allocation_insufficient"` and a `reason` string
- Assert: orange "Cannot Size" badge is visible; reason text is rendered inline on the signal card

**Acceptance Criteria**
- Playwright test exists and passes in CI covering: (a) badge visible, (b) reason inline, (c) signal visually distinct from `status: "active"` signals
- Test added to test_scenarios in the relevant execution_state.json or qa_evidence for the sprint it ships

✅ COMPLETE — 2026-06-04 — cycle 2026-06-21__release-v5.1 (ST-04, EPIC-03; Playwright E2E tests/e2e/signals-allocation-insufficient.spec.js — 5 scenarios covering SC-SIG-AI-01/02/03; all pass in CI)

---


### BLG-FE-85 — Red Flag Journal post-launch UX review
**Renumbered from:** BLG-FE-66 (ID collision resolved — v6.6 ST-03; BLG-FE-66 retained by the active backlog.md entry "RFJ date-range filter (date-to field)")
**Priority:** P3 (Low)
**Type:** Frontend / UX Review
**Owner:** Base44 Frontend Prompt Owner; Head of UX & Design
**Source:** IDEA-base44-frontend-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.3

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-21, EPIC-04; rfj_ux_review_v53.md produced; top-3 friction points documented; follow-up items filed; Base44 Frontend Prompt Owner + Head of UX & Design sign-off)
**Displacement:** BLG-FE-55 (mobile responsiveness baseline, P3) deprioritised.

**Problem**
Red Flag Journal (RFJ.js) shipped v3.9 (2026-05-22 — 7+ weeks ago) with no post-launch UX review. As the most recently shipped complex frontend component, friction points and usability improvements may be present that are not captured by CI tests.

**Scope**
- Review RFJ.js for: filter UX clarity, pagination interaction, empty state messaging, table readability
- Identify top-3 friction points with proposed improvements
- File follow-up backlog items for any identified improvements

**Acceptance Criteria**
- UX review document produced covering filters, pagination, empty state, table layout
- Top-3 friction points documented with proposed improvements
- Any significant friction filed as a separate backlog item
- Base44 Frontend Prompt Owner and Head of UX & Design sign-off

---


### BLG-FE-86 — BLG-FE-64 visual design review scope definition
**Renumbered from:** BLG-FE-67 (ID collision resolved — v6.6 ST-03; BLG-FE-67 retained by the active backlog.md entry "RFJ event type colour palette refinement")
**Priority:** P2 (Medium)
**Type:** Frontend / Planning
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-frontend-ux-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.3
**Displacement:** BLG-GOV-101 (governance complexity assessment, P3) deprioritised.
**Gate:** BLG-FE-64 gate clears 2026-06-21 — scope definition should complete before that date.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-22, EPIC-04; blg_fe_64_scope_definition.md produced; scope defined and BLG-FE-64 distinguished from BLG-FE-66; Frontend Specs & UX Documentation Owner + Head of UX & Design sign-off)

**Problem**
BLG-FE-64 (Red Flag Journal visual design review pre-brief) is in backlog with gate 2026-06-21 but its scope is vague — it is unclear what "visual design review" covers (typography, colours, spacing, component consistency, all of the above). Without a clear scope document, the story cannot be properly estimated or executed at sprint planning.

**Scope**
- Define the precise scope of BLG-FE-64: which visual elements, which pages/components, what acceptance criteria look like
- Distinguish BLG-FE-64 from BLG-FE-66 (UX review) — this is visual design, not interaction design
- Produce a one-page scope document that can be used as the BLG-FE-64 story AC at sprint planning

**Acceptance Criteria**
- Scope document produced: specifies which components and visual properties are in scope for review
- Clear distinction from BLG-FE-66 documented
- Frontend Specs & UX Documentation Owner and Head of UX & Design sign-off

---


### BLG-FE-73 — Add deep links from SI-05 digest to relevant app screens
**Priority:** P2 (Medium)
**Type:** Frontend / UX
**Owner:** Head of UX & Design; Head of Backend Engineering
**Source:** ST-10 user journey map (v5.5 EPIC-03) — 2026-06-15
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.6

✅ COMPLETE — 2026-06-16 — cycle 2026-06-16__release-v5.6 (ST-01, EPIC-01, PR #765; deep links to Risk Dashboard and Red Flag Journal added via FRONTEND_URL env var; AC-02 staging-deferred BLG-FE-75)

**Problem**
The SI-05 weekly Telegram digest contains no links to the app. A user reading "Override rate: 45%" or "Red flag events: 3" has no direct path to the relevant screen — they must open the app manually and navigate to the correct section (minimum 3 steps). This defeats the purpose of the digest as an actionable alert.

**Scope**
- Add one deep link per digest section to the relevant app screen (e.g. "View Risk Dashboard →" after the strategy integrity block)
- Links must use the app's public URL with the correct hash/route for the target screen

**Acceptance Criteria**
- At least one deep link present in the SI-05 digest pointing to a relevant app screen
- Link navigates correctly on mobile Telegram (where most users read the digest)
- Head of UX & Design sign-off

---


### BLG-FE-74 — Clarify N/A pass rate reason in SI-05 digest message
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Head of Backend Engineering
**Source:** ST-10 user journey map (v5.5 EPIC-03) — 2026-06-15
**Effort:** XS (<1h)
**Provisional-Target:** v5.6

✅ COMPLETE — 2026-06-16 — cycle 2026-06-16__release-v5.6 (ST-02, EPIC-01, PR #765; distinct N/A messages for no_events vs data_unavailable; 13 new tests added)

**Problem**
When pass rate and override rate show "N/A" in the digest, the user cannot determine whether this is expected (no trades triggered validation this week) or a system issue (validation logging broken). The current message "No pre-entry validation data available this week" is ambiguous.

**Scope**
- Update `_integrity_summary_line` in `si05_digest_service.py` to include the reason for N/A (e.g. "N/A (no validation events this week)")
- Distinguish between "no events" and "data unavailable" in the message text

**Acceptance Criteria**
- N/A values in the digest include a parenthetical reason
- "No events" and "data unavailable" produce distinct messages
- No regression to existing digest delivery

---


### BLG-BE-16 — Red flag events severity field
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Data Model
**Owner:** Data Model & Domain Schema Owner; Head of Backend Engineering
**Source:** IDEA-data-model-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 (Behavioural Drift Detection) sprint planning imminent — severity taxonomy should be informed by SI-02 design to avoid schema rework.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-09; severity column + backfill + filter support; staging verification pending BLG-OPS-45)

**Problem**
red_flag_events table (shipped v3.9) has no severity classification. Adding a severity field (info/warning/critical) enables better filtering in SI-03 Red Flag Journal, more actionable grouping in SI-05 Weekly Digest, and meaningful colour coding in BLG-FE-41 visual design review. The field is additive and backward-compatible but should be deferred until SI-02 sprint planning is imminent to ensure the severity taxonomy is informed by drift detection severity requirements.

**Scope**
- Add `severity` column to `red_flag_events` table: enum (info/warning/critical)
- Default severity for existing event types (SI-01 overrides: warning; future drift events: critical)
- Migration: backfill existing events with default severity
- Update `GET /portfolio/red-flag-journal` to support severity filter parameter
- Update openapi.yaml with severity field and filter parameter

**Acceptance Criteria**
- severity field present on all red_flag_events records
- `GET /portfolio/red-flag-journal?severity=warning` filters correctly
- Migration backfills existing events without data loss
- openapi.yaml updated
- Gate condition verified by Product Owner before sprint planning

---


### BLG-BE-25 — Fix pre-entry regime gate to use shared market status instead of independent yf.download ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P2 (Medium)
**Type:** Backend Engineering
**Owner:** Head of Backend Engineering
**Source:** User-reported — pre-entry regime gate shows risk_off while dashboard shows risk_on — 2026-06-02
**Effort:** S (~0.5d)
**Provisional-Target:** v5.0

**Problem**
`_check_regime()` in `pre_entry_validation.py` calls `check_market_regime()` directly, which triggers a fresh `yf.download("SPY")` / `yf.download("^FTSE")` call independent of the `/market/status` endpoint. On rapid sequential requests, Yahoo Finance can return slightly different data (different row counts, trailing NaN values), causing the rolling 200MA calculation to resolve differently. This produces spurious regime_gate failures that contradict the authoritative dashboard reading, eroding user trust in the pre-entry check.

**Scope**
- Refactor `_check_regime()` to call `GET /market/status` (or a shared in-process cache) rather than invoking `check_market_regime()` directly
- Ensure the regime result used in pre-entry validation is always consistent with what `/market/status` returns
- Add a server-side cache (e.g. 5-minute TTL) to `check_market_regime()` so all callers share one result per window

**Acceptance Criteria**
- Dashboard regime and pre-entry regime gate always agree when called within the same session
- No spurious risk_off failures when SPY is clearly above its 200MA per the dashboard
- `/portfolio/pre-entry-validation` does not make an independent `yf.download` call

---


### BLG-BE-26 — SI-02 lightweight drift summary assessment (backend-only state mitigation) ✅ ASSESSMENT COMPLETE v5.0 (2026-06-03) — implementation ready for sprint planning with conditions
**Priority:** P2 (Medium)
**Type:** Backend Engineering / UX Assessment
**Owner:** Head of Backend Engineering; Head of UX & Design; Product Owner
**Source:** IDEA-challenger-20260601-01 — Promoted-Backlog cycle 2026-06-02__scheduled (DL-037; STEP 5 debate advance; PO Rebut — assessment scope with UX risk evaluation)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.0 (conditional on assessment outcome)

**Problem**
Behavioural drift scores are computed by the SI-02 backend (4 metrics, 35 unit tests, shipped v4.6) but are not surfaced to the user because the SI-02 frontend has been deferred ~8 cycles (~2027-Q1). The system "knows" about drift but cannot communicate it, creating an information asymmetry that grows with each deferral cycle. A read-only drift summary (e.g., in System Status or Reports page) may mitigate without a full frontend sprint.

**Scope (assessment — not committed implementation):**
- Assess feasibility of adding a read-only drift summary to System Status or Reports page
- Evaluate UX risk: can drift scores be displayed with sufficient context (framing, threshold calibration advisory, §13 disclosure) to prevent misinterpretation by user?
- If feasible and UX risk manageable: define minimal scope (which metrics, where displayed, what framing text)
- If UX risk is too high: document assessment outcome as "assess only — not implemented" and close item

**Acceptance Criteria**
- Assessment document produced: feasibility determination + UX risk evaluation
- If UX risk manageable: minimal display scope defined (ready for sprint planning)
- If UX risk too high: outcome documented and item closed with rationale
- Product Owner reviews and signs off on assessment outcome

---


### BLG-BE-32 — SI-05 Telegram delivery retry and failure handling
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-05, EPIC-02; retry max 2 retries 30s/60s backoff; ERROR logging confirmed; 3 unit tests added; injectable sleep for CI; 24 tests passing; staging AC-04 PASS)
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Reliability
**Owner:** Backend Engineering Patterns Owner; Infrastructure & Operations Owner
**Source:** IDEA-backend-engineering-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.2
**Displacement:** BLG-BE-21 (Arc 5 analytics endpoint versioning strategy, P3, gate-conditional) deprioritised.

**Problem**
si05_digest_service.py sends weekly digests via Telegram. The current failure mode for Telegram delivery failures (connection timeout, API error, message too long) is undocumented. For a scheduled service, silent failure means the user misses the weekly digest without knowing. Defining and documenting retry/failure handling before the service encounters production issues prevents silent failures.

**Scope**
- Document current si05_digest_service.py failure mode: what happens when Telegram API call fails (exception raised? logged? swallowed?)
- Define retry policy: does the service retry on transient failures? How many times? What backoff?
- If no retry exists: implement simple exponential backoff (max 2 retries, 30s/60s delays)
- Document failure handling in ops runbook or inline code comment (single clear explanation)
- If failure is unrecoverable: ensure error is logged at ERROR level so it appears in Render logs

**Acceptance Criteria**
- Failure mode documented and addressed in si05_digest_service.py
- At minimum: delivery failure is logged at ERROR level and not silently swallowed
- Retry policy (or explicit no-retry decision) documented
- Infrastructure & Operations Owner confirms the failure mode is observable in Render logs

---


### BLG-BE-33 — SI-05 digest delivery log table
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-06, EPIC-02; si05_digest_log table; schema: id/sent_at/status/event_count/telegram_message_id/error_message/created_at; CREATE TABLE IF NOT EXISTS guard; log rows on both paths; registered in main.py on_startup(); Data Model Owner sign-off; staging AC-04 PASS)
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Data Model
**Owner:** Data Model & Domain Schema Owner; Backend Engineering Patterns Owner
**Source:** IDEA-data-model-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~1 day)
**Provisional-Target:** v5.2
**Displacement:** BLG-BE-14 (trade plan schema versioning, P3, gate-conditional) deprioritised.

**Problem**
SI-05 delivers weekly digests via Telegram. There is no persistent record of each delivery attempt: when it was sent, whether it succeeded, how many events were included, or the Telegram message ID. Without a delivery log, diagnosing missed digests requires Render log archaeology with a 7-day retention window. A delivery log table provides durable, queryable delivery history.

**Scope**
- New table: `si05_digest_log` (id, sent_at, status [sent/failed], event_count, telegram_message_id, error_message, created_at)
- Backend: write log row on each send attempt in si05_digest_service.py
- Migration: add table to database startup script
- Optional: GET /digest/si05/log endpoint (read-only, last N entries) for operational visibility

**Acceptance Criteria**
- si05_digest_log table created via migration
- Delivery attempt recorded on each send (success and failure)
- Data model reviewed by Data Model & Domain Schema Owner
- Optional endpoint: if implemented, registered in test.py and openapi.yaml per CLAUDE.md §2

---


### BLG-BE-35 — Add API key authentication to POST /digest/si05/send
**Priority:** P2 (Medium)
**Type:** Backend Engineering / Security
**Owner:** Head of Engineering; Cybersecurity & Trust Lead
**Source:** ST-11 (BLG-GOV-99) — security review finding, 2026-06-08__release-v5.2
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.3

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-08, EPIC-02; API key auth applied to POST /digest/si05/send; unit test for 401 response added; digest_endpoints.md updated; Cybersecurity & Trust Lead + Head of Engineering sign-off)

**Problem**
POST /digest/si05/send is an unauthenticated endpoint (`backend/routers/digest.py:227`). It triggers Telegram API calls and digest sends without requiring authentication. An unauthenticated caller could trigger repeated sends (Telegram quota abuse, spam to digest chat). The existing authentication pattern (BLG-SEC-01/v2.2) applies API key auth — this pattern is not applied to the digest endpoint. Finding documented in `docs/security/security_register.md` Review 003 (ST-11, v5.2).

**Scope**
- Apply API key authentication to POST /digest/si05/send using the existing auth pattern (Depends injection, consistent with other protected endpoints)
- Add unit test verifying 401 response on unauthenticated POST /digest/si05/send
- Update `docs/specs/api_contracts/digest_endpoints.md` authentication requirements section
- Cybersecurity & Trust Lead sign-off on fix

**Acceptance Criteria**
- POST /digest/si05/send requires API key authentication per the existing pattern
- 401 returned on unauthenticated request
- Unit test added verifying 401 behaviour
- digest_endpoints.md updated with authentication requirements
- Cybersecurity & Trust Lead and Head of Engineering sign-off

---

## 5. QA & Test Automation Backlog

---


### BLG-QA-39 — Coverage matrix update and v4.7 contract completeness verification ✅ COMPLETE v4.8 (2026-06-02)
**Priority:** P2 (Medium)
**Type:** QA / Test Coverage + Spec Verification
**Owner:** QA Lead; API Contracts & Documentation Owner
**Source:** IDEA-qa-lead-20260601-01 + IDEA-api-contracts-20260601-02 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v4.8

**Problem**
v4.7 shipped compliance_summary field in GET /reports/monthly-pnl (ST-03, EPIC-04). This observable field is not yet in the test coverage matrix. Additionally, v4.7 bumped the monthly P&L response schema to v0.6 — the API contract documentation should reflect this version increment.

**Scope**
- Add compliance_summary field to QA coverage matrix as an observable regression point
- Verify that docs/specs/api_contracts/ reflects the v0.6 monthly P&L response schema
- Document any contract gaps found

**Acceptance Criteria**
- Coverage matrix includes compliance_summary field with regression test reference
- GET /reports/monthly-pnl v0.6 confirmed in API contract documentation
- Any contract gaps filed as BLG-SPEC items

---


### BLG-QA-40 — Wire Phase B CI with real Postgres service to catch missing-column errors
**Priority:** P2 (Medium)
**Type:** QA / Test Automation
**Owner:** QA Lead; Head of Engineering
**Source:** Bug: position_state column missing from positions table, not caught by CI — 2026-06-01
**Effort:** M (~1–2 days)
**Provisional-Target:** v4.9

✅ COMPLETE — 2026-06-02 — cycle 2026-06-02__release-v4.9 (ST-03, EPIC-02; postgres:15 service container wired; DATABASE_URL injected; Phase A unaffected; 13 pre-existing Phase B failures surfaced and fixed)

**Problem**
The Phase A CI suite (ci-tests.yml) runs against a stub DATABASE_URL with all DB calls mocked, making missing schema columns completely invisible to CI. When `position_state`, `state_entered_at`, and `state_history` were never added to the `positions` table via a startup migration, every endpoint that queried those columns returned a 500 in production — yet all CI jobs were green. The ci-tests.yml workflow comment explicitly notes Phase B ("requires DATABASE_URL secret") was deferred; until it is wired, no automated job will catch a column referenced in SQL that doesn't exist in the DB.

**Scope**
- Spin up a Postgres service container in ci-tests.yml (GitHub Actions `services:` block)
- Wire the `DATABASE_URL` secret for the Phase B job step
- Enable the Phase B test run (currently commented out in the workflow)
- Verify all existing integration tests pass against the real service container

**Acceptance Criteria**
- A PR that introduces a SQL query referencing a non-existent column causes the CI Phase B job to fail
- Phase A (stub/mock tests) continues to run without a real DB
- No test collection errors in Phase B

---


### BLG-QA-41 — Schema smoke test: assert lifecycle columns exist on positions table
**Priority:** P3 (Low)
**Type:** QA / Test Automation
**Owner:** QA Lead
**Source:** Bug: position_state column missing from positions table, not caught by CI — 2026-06-01
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.9
**Depends on:** BLG-QA-40 (Phase B CI with real Postgres required)

✅ COMPLETE — 2026-06-02 — cycle 2026-06-02__release-v4.9 (ST-04, EPIC-02; tests/test_schema.py created; skips in Phase A; passes in Phase B with real Postgres)

**Problem**
There is no test that verifies the `positions` table contains the lifecycle columns (`position_state`, `state_entered_at`, `state_history`) that `ensure_lifecycle_columns()` is supposed to create. Without this, a missing `ensure_*` call at startup — or a call that silently errors — leaves a schema gap that is only discovered when a user hits the broken endpoint. A schema introspection test would close this class of bug permanently.

**Scope**
- Add a test (in `tests/test_position_lifecycle.py` or a new `tests/test_schema.py`) that calls `ensure_lifecycle_columns()` and then queries `information_schema.columns` to assert all three columns are present on the `positions` table
- Test must run under Phase B CI (real Postgres) and be excluded from Phase A

**Acceptance Criteria**
- Test fails if any of `position_state`, `state_entered_at`, `state_history` is absent from the `positions` table
- Test is skipped/excluded when `DATABASE_URL` points to the stub (Phase A)
- Test passes in the Phase B CI environment

---


### BLG-QA-43 — compliance_summary field population validation
**Priority:** P3 (Low)
**Type:** QA / Data Quality
**Owner:** QA Lead; Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260601-01 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** XS (~1–2 hours)
**Provisional-Target:** v5.1 or spot-check session

**Gate criteria:** None. Can be done in any session that includes a monthly P&L report review.

**Problem**
v4.7 shipped compliance_summary in GET /reports/monthly-pnl (ST-03, EPIC-04). No verification confirms the field is populated from Arc5ComplianceSection data and matches what is displayed there. A mismatch would be a silent data quality issue.

**Scope**
- Verify compliance_summary in monthly P&L matches Arc5ComplianceSection display values
- Check that all 5 Arc 5 compliance metrics are correctly included in the summary
- Document verification result; file P2 bug if mismatch found

**Acceptance Criteria**
- Verification performed against staging or production monthly P&L output
- Result documented; any mismatch filed as a P2 bug item immediately
- No gate condition required

✅ COMPLETE — 2026-06-04 — cycle 2026-06-21__release-v5.1 (ST-05, EPIC-03; code review confirmed all 5 Arc 5 compliance fields present in reports_endpoints.md spec; staging AC-01 deferred to staged verification sprint — I&O Owner sign-off outstanding)

---


### BLG-QA-45 — Arc 5 QA completion criteria definition
**Priority:** P2 (Medium)
**Type:** QA / Planning
**Owner:** Director of Quality; QA Lead
**Source:** IDEA-director-of-quality-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Before BLG-QA-26 sprint planning
**Displacement:** BLG-QA-22 (Arc 2 DoQ standards review, P3, gate-conditional) deprioritised.

✅ COMPLETE — 2026-06-16 — cycle 2026-06-16__release-v5.6 (ST-09, EPIC-03, PR #764; criteria C-01 to C-05 defined; BLG-QA-26 gate condition updated; SI-05 Phase 2/SI-04/SI-02 backend-only explicitly scoped; PO + DoQ approved)

**Problem**
BLG-QA-26 (Arc 5 E2E QA protocol) gates on "all five Arc 5 features shipped" but "fully complete" is undefined: does SI-05 Phase 2 count? Does SI-02 frontend count separately from SI-02 backend? Without defined criteria, BLG-QA-26 sprint planning will encounter scope ambiguity that delays the protocol.

**Scope**
- Define canonical "Arc 5 fully complete" criteria: explicit list of what must be shipped for BLG-QA-26 to trigger (proposed: SI-01 ✅, SI-03 ✅, SI-05 Phase 1 ✅, SI-02 frontend, SI-04 — all five features have shipped their full scopes)
- Confirm with Product Owner and Head of Specs Team: does SI-05 Phase 2 count separately, or is Phase 1 sufficient?
- Document criteria in BLG-QA-26 gate condition field
- Reviewed by Director of Quality and Product Owner

**Acceptance Criteria**
- Arc 5 completion criteria explicitly defined and documented
- BLG-QA-26 gate condition updated with the explicit list
- Product Owner and Director of Quality sign-off

---


### BLG-QA-46 — SI-05 digest service edge case test gap analysis
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-13, EPIC-04; 2 gaps found and fixed: test_telegram_api_connection_failure_logs_error + test_message_truncation_at_character_limit; 26 tests total passing; QA Lead sign-off)
**Priority:** P2 (Medium)
**Type:** QA / Test Coverage
**Owner:** QA Lead; Backend Engineering Patterns Owner
**Source:** IDEA-backend-engineering-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** XS (~1–2 hours)
**Provisional-Target:** v5.2
**Displacement:** BLG-QA-23 (trade plan lifecycle E2E test, P3, gate-conditional) deprioritised.

**Problem**
si05_digest_service.py was delivered with 21 unit tests. A gap analysis confirms whether key edge cases are covered: (a) zero events in the 7-day window, (b) Telegram API connection failure, (c) message content at character limit boundary, (d) partial send (some events included, others truncated), (e) service invocation when SI-01 has no pass/fail data yet.

**Scope**
- Review the 21 unit tests in the relevant test file against the 5 edge cases above
- Document: which edge cases are covered, which are missing
- If gaps found: author the missing tests; if all covered: document as verified
- Filed as sprint story if tests need authoring (XS effort)

**Acceptance Criteria**
- Gap analysis document produced listing all 5 edge cases with coverage status
- Any missing tests authored and passing
- QA Lead and Backend Engineering Patterns Owner sign-off

---


### BLG-QA-47 — SI-05 Phase 1 acceptance test protocol
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-14, EPIC-04; docs/qa/si05_acceptance_test_protocol.md produced; covers v5.1 deferred ACs: AC-09 Telegram delivery, AC-01 compliance_summary; Director of Quality sign-off)
**Priority:** P2 (Medium)
**Type:** QA / Test Planning
**Owner:** QA & Testing Owner; Director of Quality
**Source:** IDEA-qa-testing-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Before staged verification sprint
**Displacement:** BLG-QA-24 (Yahoo Finance backoff path integration test stub, P3) deprioritised.

**Problem**
v5.1 post-ship closure deferred 2 staging-only ACs to a staged verification sprint: ST-01 AC-09 (Telegram delivery confirmed on staging) and ST-05 AC-01 (compliance_summary live data on staging). Without a formal acceptance test protocol, the staged verification sprint lacks structured guidance for what to test, how to record evidence, and what constitutes pass/fail for each deferred AC.

**Scope**
- Produce acceptance test protocol for the SI-05 Phase 1 staged verification sprint
- Per deferred AC: test steps, expected outcome, evidence format (screenshot? log entry?), pass/fail definition, sign-off authority
- Reference BLG-GOV-89 (staged verification sprint protocol, v1.0) for format
- Reviewed by Director of Quality before staged verification sprint planning

**Acceptance Criteria**
- Acceptance test protocol document produced for each deferred AC (ST-01 AC-09, ST-05 AC-01)
- Each AC has explicit: test steps, expected outcome, evidence format, sign-off authority
- Director of Quality sign-off

---


### BLG-QA-48 — Regression test suite baseline refresh post-v5.1
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-15, EPIC-04; POST /digest/si05/send confirmed in test.py; 5 Playwright scenarios confirmed; no formal baseline doc — BLG-QA-50 filed; QA Lead sign-off)
**Priority:** P2 (Medium)
**Type:** QA / Test Infrastructure
**Owner:** QA Lead
**Source:** IDEA-qa-lead-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** XS (~1–2 hours)
**Provisional-Target:** v5.2
**Displacement:** BLG-QA-27 (CI test suite execution time baseline, P3, gate-conditional) deprioritised.

**Problem**
v5.1 shipped POST /digest/si05/send (new endpoint) and tests/e2e/signals-allocation-insufficient.spec.js (5 new Playwright scenarios). The regression test baseline has not been updated to include these new scenarios. Without the update, future regression checks may miss failures introduced in these areas.

**Scope**
- Add POST /digest/si05/send to the regression test baseline (endpoint presence and basic response check)
- Confirm signals-allocation-insufficient.spec.js scenarios are included in the CI regression run
- Update any regression baseline document (if one exists) to reflect v5.1 additions
- Note: if no formal regression baseline document exists, file its creation as a follow-on backlog item

**Acceptance Criteria**
- Regression baseline updated to include v5.1 additions
- All 5 signals-allocation-insufficient.spec.js Playwright scenarios confirmed in CI
- POST /digest/si05/send confirmed in backend/routers/test.py
- QA Lead sign-off

---


### BLG-QA-49 — Arc 5 test scenario completeness assessment
**Priority:** P2 (Medium)
**Type:** QA / Planning
**Owner:** QA Lead; Director of Quality
**Source:** IDEA-qa-lead-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled
**Displacement:** BLG-FE-39 (Arc 2 user journey map, P3, gate-conditional) deprioritised.

✅ COMPLETE — 2026-06-16 — cycle 2026-06-16__release-v5.6 (ST-10, EPIC-03, PR #764; SI-01/SI-03/SI-05 coverage mapped; 3 P3 Playwright gaps identified: BLG-QA-56/57/58; DoQ approved; arc5_test_coverage_assessment.md produced)

**Problem**
With SI-01, SI-03, and SI-05 Phase 1 shipped (3 of 5 Arc 5 features), an intermediate test scenario completeness assessment identifies QA gaps before the remaining features ship. This is not BLG-QA-26 (full Arc 5 QA protocol, gated on full completion) — it is a partial completeness check that surfaces gaps while there is still time to address them before the arc closes.

**Scope**
- Enumerate all Playwright E2E tests currently covering Arc 5 features: SI-01 (PreEntryValidationPanel), SI-03 (RedFlagJournal.js), SI-05 (allocation_insufficient badge — ST-04)
- Map each test to its Arc 5 AC coverage: which ACs are Playwright-covered, which are human-staging-only, which are not covered
- Identify top-3 coverage gaps that should be addressed before SI-02 or SI-04 sprint
- Output: coverage gap report filed with QA Lead

**Acceptance Criteria**
- Arc 5 Playwright test coverage map produced (feature × AC × test scenario)
- Top-3 coverage gaps identified with proposed remediation
- Director of Quality sign-off on coverage assessment

---


### BLG-QA-51 — BLG-SPEC-49–52 QA acceptance criteria definition
**Priority:** P2 (Medium)
**Type:** QA / Governance
**Owner:** Director of Quality; QA Lead
**Source:** IDEA-director-of-quality-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.3
**Displacement:** BLG-QA-44 (SI-04 test planning, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-03, EPIC-01; endpoint_contract_qa_criteria_template.md produced; AC template applied to all 6 BLG-SPEC-49–52 gaps; Director of Quality sign-off)

**Problem**
BLG-SPEC-49–52 (6 endpoint contract gaps) need clearly defined acceptance criteria before they enter v5.3 sprint planning. Without QA-defined AC, the contract authoring stories will have vague verification criteria, risking incomplete sign-off.

**Scope**
- Define AC template for endpoint contract stories: what constitutes a "complete" contract (## METHOD /path at ## level, openapi.yaml entry, test.py entry, SystemStatus fallback count updated)
- Apply template to all 6 gaps in BLG-SPEC-49–52
- Ensure Director of Quality can sign off using the AC template at delivery verification

**Acceptance Criteria**
- QA readiness document produced with AC template and application to SPEC-49–52
- Template is reusable for future endpoint contract gap stories
- Director of Quality sign-off

---


### BLG-QA-52 — Tax year P&L boundary edge case validation
**Priority:** P2 (Medium)
**Type:** QA / Financial Accuracy
**Owner:** QA Lead; Financial Reporting & Records Owner
**Source:** IDEA-financial-reporting-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.3
**Displacement:** BLG-QA-44 (SI-04 test planning, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-18, EPIC-04; 6 boundary test scenarios in tests/test_tax_year_pnl_boundary.py; all passing; Financial Reporting & Records Owner + QA Lead sign-off)

**Problem**
The tax year P&L report (shipped v2.0, March 2026) generates tax-year-segmented P&L summaries. A trade opened in one UK tax year (before April 5) and closed in the next (after April 6) may be misattributed to the wrong year. This edge case has never been formally tested.

**Scope**
- Identify the tax year boundary logic in the P&L report endpoint (GET /reports/monthly-pnl or the annual equivalent)
- Create test data scenarios: trade opened Dec 31, closed April 7 (straddling April 5 boundary); trade opened April 4, closed April 8
- Verify P&L is attributed to the correct tax year in each scenario
- Document findings; file a bug item if misattribution detected

**Acceptance Criteria**
- Year-boundary test scenarios documented and executed
- P&L attribution confirmed correct for all boundary cases (or bug filed if incorrect)
- Financial Reporting & Records Owner and QA Lead sign-off

---


### BLG-QA-53 — SI-05 digest Playwright E2E coverage
**Priority:** P2 (Medium)
**Type:** QA / Test Automation
**Owner:** QA Lead; QA & Testing Owner
**Source:** IDEA-qa-testing-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** M (~1–2 days)
**Provisional-Target:** v5.3
**Displacement:** BLG-QA-44 (SI-04 test planning, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-19, EPIC-04; 4 Playwright scenarios in tests/e2e/si05-digest-delivery.spec.js; Telegram API mocked; all passing in CI; QA Lead sign-off)

**Problem**
si05_digest_service.py has 21 unit tests but no Playwright E2E coverage for the digest trigger → delivery flow. The observable AC for SI-05 (Telegram message received, compliance data present, red flag summary accurate) cannot be fully verified by unit tests alone. CLAUDE.md §2 requires Playwright coverage or staging sign-off for observable ACs.

**Scope**
- Define Playwright test scenarios for SI-05: trigger delivery, verify Telegram mock receives message, verify message format/content structure
- Implement minimum 3 Playwright scenarios covering: happy path delivery, empty red flag scenario, compliance score present
- Ensure scenarios run in CI without real Telegram API (mock or stub Telegram bot endpoint)

**Acceptance Criteria**
- ≥ 3 Playwright E2E scenarios for SI-05 digest delivery implemented and passing in CI
- Scenarios cover: happy path, empty state, compliance score
- Telegram API mocked or stubbed to avoid real API calls in CI
- QA Lead sign-off

---


### BLG-QA-54 — Playwright coverage matrix update post-v5.2
**Priority:** P2 (Medium)
**Type:** QA / Documentation
**Owner:** QA Lead; Director of Quality
**Source:** IDEA-qa-lead-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.3
**Displacement:** BLG-QA-44 (SI-04 test planning, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-20, EPIC-04; playwright_coverage_matrix.md updated to reflect v5.2 + v5.3 additions; coverage gaps identified; Director of Quality sign-off)

**Problem**
v5.2 added 26 new edge case tests (BLG-QA-44 base scope) and other QA improvements. The Playwright coverage matrix (produced by BLG-QA-49, v5.2) does not yet reflect these additions. A stale matrix leads to incorrect QA sign-off assessments at delivery verification.

**Scope**
- Count all Playwright E2E test scenarios post-v5.2 (tests/e2e/*.spec.js)
- Update the coverage matrix to include all new scenarios added in v5.2
- Map new scenarios to their corresponding feature ACs
- Identify any ACs still lacking Playwright coverage

**Acceptance Criteria**
- Coverage matrix updated to reflect all v5.2 Playwright additions
- New scenarios mapped to feature ACs
- Coverage gaps identified and noted
- Director of Quality sign-off

---


### BLG-OPS-22 — Research data caching layer
**Priority:** P2 (Medium)
**Type:** Operations / Performance
**Owner:** Infrastructure & Operations Owner; Head of Backend Engineering
**Source:** IDEA-ops-20260421-06 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** M (~2–3 days)
**Provisional-Target:** v5.6

✅ COMPLETE — 2026-06-16 — cycle 2026-06-16__release-v5.6 (ST-07, EPIC-02, PR #766; 15-min per-ticker TTL cache + screener invalidation + hit/miss logging; AC-04/05 staging verification deferred BLG-OPS-69)

**Gate criteria:** ✅ GATE CLEARED 2026-06-11 — BLG-OPS-13 complete (v5.5 ST-06) AND p95=4,601ms > 3,000ms threshold confirmed on production. Eligible for sprint planning.

**Problem**
Research view loads require multiple sequential external API calls (YF OHLCV, earnings, news). If p95 latency (measured via BLG-OPS-13) exceeds 3 seconds, a caching layer (TTL-based, per-ticker) would materially reduce latency and external API call volume. Gate ensures implementation effort is only incurred if a real performance concern is observed.

**Scope**
- TTL-based cache (Redis or in-memory): research data per ticker, 15-minute TTL
- Cache invalidation on screener run
- Cache hit/miss logging

**Acceptance Criteria**
- Research view p95 latency reduced to ≤2s for cached tickers
- Cache hit rate ≥ 50% in typical usage
- Gate condition (BLG-OPS-13 + p95 concern) verified before sprint planning

---


### BLG-OPS-28 — Staging deploy live verification (ST-09 staging-only AC)
**Priority:** P2 (Medium)
**Type:** Operations / CI/CD
**Owner:** Infrastructure & Operations Owner
**Source:** ST-09 staging-only AC — v4.0 sprint execution 2026-05-24
**Effort:** XS (~0.5 day)
**Provisional-Target:** v4.1

✅ COMPLETE — 2026-05-31 — cycle 2026-05-31__release-v4.7 (ST-04, EPIC-03; staging_deploy_verification.md produced; RENDER_STAGING_DEPLOY_HOOK confirmed; code-change deploy verified; docs-only filter verified; Infrastructure & Operations Owner sign-off)

**Problem**
ST-09 (BLG-OPS-27) implements the staging deploy workflow and deploy hook mechanism, but the AC "staging auto-deploys on main merge" requires a live Render environment with `RENDER_STAGING_DEPLOY_HOOK` secret configured. This cannot be verified in CI.

**Scope**
- Set `RENDER_STAGING_DEPLOY_HOOK` secret in GitHub repo settings (Render dashboard → staging service → Settings → Deploy Hook)
- Merge a code-change commit to main and confirm Render dashboard shows a triggered deploy
- Merge a docs-only commit and confirm no deploy is triggered
- Record staging sign-off date in BLG-OPS-27 post-verification note

**Acceptance Criteria**
- `RENDER_STAGING_DEPLOY_HOOK` secret configured
- Code-change merge triggers Render staging deploy (confirmed in Render dashboard)
- Docs-only commit does not trigger deploy (path filter verified)
- Results recorded as staging sign-off evidence

---


### BLG-OPS-31 — Render application log retention policy
**Priority:** P2 (Medium)
**Type:** Operations / Data Management
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

✅ COMPLETE — 2026-05-31 — cycle 2026-05-31__release-v4.7 (ST-07, EPIC-03; render_log_retention_policy.md produced; Render 7-day retention documented; database audit tables confirmed durable; decision: Render logs + database tables sufficient; Infrastructure & Operations Owner sign-off)

**Problem**
Render (production hosting platform) provides application logs with a default retention period. As Arc 5 compliance data and Gemini audit logs accumulate, understanding Render's log retention limits and whether application-level log archiving is required becomes an operational concern.

**Scope**
- Review Render log retention policy (current plan limitations)
- Assess whether gemini_audit_log and red_flag_events database tables provide sufficient durable audit trail independent of Render logs
- Determine if additional log archiving or export is required
- Document policy decision

**Acceptance Criteria**
- Render log retention policy reviewed and documented
- Database tables (gemini_audit_log, red_flag_events) confirmed as durable audit trail
- Policy decision documented in ops runbook or equivalent

---


### BLG-OPS-37 — Anthropic API tier cost assessment
**Priority:** P2 (Medium)
**Type:** Operations / Cost Planning
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260527-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-OPS-36 (Claude API first monthly review) complete.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-31__release-v4.7 (ST-08, EPIC-04; anthropic_api_tier_assessment.md produced; no upgrade required; upgrade threshold defined at $5/month; FinOps & Resource Architect sign-off)

**Problem**
Anthropic API pricing tiers differ from Gemini. Without a tier cost assessment, there is no defined threshold at which a paid-tier upgrade becomes cost-effective. BLG-OPS-36 provides the usage data; this item performs the tier comparison and defines the decision threshold.

**Scope**
- Review Anthropic API pricing tiers vs actual usage from BLG-OPS-36 review
- Define usage threshold at which paid-tier upgrade is cost-effective
- Document decision framework and feed to FinOps monitoring

**Acceptance Criteria**
- Tier comparison document produced
- Usage threshold for upgrade decision defined
- Gate condition (BLG-OPS-36 complete) verified before commencing

---


### BLG-OPS-40 — Arc 5 hosting cost projection
**Priority:** P2 (Medium)
**Type:** Operations / Cost Planning
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** IDEA-finops-20260522-02 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035, 3-cycle cap)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-02 sprint planning initiated.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-10; arc5_hosting_cost_projection.md; current Render Starter tier adequate; no upgrade required; FinOps sign-off)

**Problem**
SI-02 drift detection will add recurring background analysis queries. The current Render compute tier was sized for Arc 1–4 workloads. Before SI-02 sprint planning, an assessment of whether the additional Arc 5 load is within the current tier is needed to prevent mid-sprint resource surprises.

**Scope**
- Estimate additional compute load from SI-02 background queries (query frequency, data volume)
- Compare against current Render compute tier headroom
- Recommendation: current tier adequate or upgrade required before SI-02 ships

**Acceptance Criteria**
- Load estimate produced with data and assumptions
- Tier adequacy determination made
- Gate condition (SI-02 sprint planning initiated) verified before commencing

---


### BLG-OPS-46 — Build minutes monitoring policy ✅ COMPLETE v4.8 (2026-06-02)
**Priority:** P2 (Medium)
**Type:** Operations / Platform Continuity
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** IDEA-finops-20260601-02 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.8

**Problem**
Render CI build minutes were exhausted 2026-05-31, blocking deploys until the billing cycle reset. There is no monitoring of build minute consumption rate against the monthly allocation, and no early-warning threshold defined. Recurrence is likely in double-capacity sprints.

**Scope**
- Document monthly Render build minute allocation and consumption rate (v4.6–v4.7 actual usage)
- Establish early-warning threshold at 80% utilisation
- Confirm billing cycle reset date and document in ops runbook
- Assess whether double-capacity sprint cadence requires a plan upgrade

**Acceptance Criteria**
- Monthly build minute consumption documented
- Early-warning threshold defined and operator-visible (manual check or alert)
- Billing cycle reset date documented
- Ops runbook updated with monitoring procedure

---


### BLG-OPS-47 — Dependency audit post-v4.7 ✅ COMPLETE v4.8 (2026-06-02)
**Priority:** P2 (Medium)
**Type:** Operations / Security
**Owner:** Head of Engineering; Cybersecurity & Trust Lead
**Source:** IDEA-head-of-engineering-20260601-02 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v4.8

**Problem**
Last CVE remediation was starlette upgrade (v4.0, 2026-05-25). Dependencies were not audited during v4.1–v4.7 sprints. New CVEs may have been disclosed for packages used in the application (FastAPI, psycopg2, alpaca-trade-api, anthropic SDK).

**Scope**
- Run `pip-audit` or equivalent dependency vulnerability scan against requirements.txt
- Run `npm audit` on frontend package.json
- Document findings; file BLG-OPS items for any HIGH/CRITICAL vulnerabilities
- Update ANTHROPIC SDK version if patch available

**Acceptance Criteria**
- Dependency audit complete for backend (Python) and frontend (npm)
- HIGH/CRITICAL vulnerabilities addressed or filed as P0/P1 backlog items
- Audit findings documented in security register (if exists) or ops runbook

---


### BLG-OPS-49 — npm devDependency HIGH CVEs (react-scripts chain)
**Priority:** P1 (High)
**Type:** Operations / Security
**Owner:** Head of Engineering; Cybersecurity & Trust Lead
**Source:** v4.8 ST-05 dependency audit (2026-06-01)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.9

✅ COMPLETE — 2026-06-02 — cycle 2026-06-02__release-v4.9 (ST-01, EPIC-01; npm audit fix applied; HIGH=0; 6 moderate remain CRA chain non-production; security_register.md Audit 001 updated)

**Problem**
npm audit (2026-06-01) found 21 HIGH severity vulnerabilities in the frontend devDependency chain via `react-scripts` (Create React App). All are build toolchain CVEs — not in the production runtime bundle. Nonetheless, HIGH severity requires P1 filing per security policy.

**Key CVEs:** GHSA-fv7c-fp4j-7gwp (@babel/plugin-transform-modules-systemjs), nth-check ReDoS (GHSA-rp65-9cf3-cjxr), node-forge HMAC bypass, lodash prototype pollution.

**Scope**
- Run `npm audit fix` on the project root package.json
- Verify no breaking changes to the build output after fix
- Confirm 0 HIGH vulnerabilities remain after fix
- Document in security_register.md

**Acceptance Criteria**
- `npm audit fix` applied and build passes
- HIGH vulnerability count = 0
- No regression in production bundle behaviour

---


### BLG-OPS-50 — Anthropic SDK upgrade (0.40.0 → current)
**Priority:** P2 (Medium)
**Type:** Operations / Maintenance
**Owner:** Head of Engineering
**Source:** v4.8 ST-05 dependency audit (2026-06-01)
**Effort:** S–M (~0.5–1 day)
**Provisional-Target:** v4.9

✅ COMPLETE — 2026-06-02 — cycle 2026-06-02__release-v4.9 (ST-02, EPIC-01; anthropic==0.40.0→0.105.2; 447 tests passing; security_register.md Upgrade 001 updated; AC-04 staging deferred: BLG-OPS-52)

**Problem**
The Anthropic Python SDK is pinned at v0.40.0 in `backend/requirements.txt`. Latest available version is 0.105.2 (65 minor versions behind as of 2026-06-01). Upgrading ensures access to latest API features, bug fixes, and security patches.

**Scope**
- Update `backend/requirements.txt`: `anthropic==0.40.0` → `anthropic==0.105.2` (or latest stable)
- Run full backend test suite to verify no breaking changes
- Review Anthropic SDK changelog (0.40.0 → current) for breaking API changes that may affect `/ai/generate-thesis` and `/ai/check-daily-cost` endpoints
- Document upgrade in security_register.md

**Acceptance Criteria**
- requirements.txt updated to latest stable Anthropic SDK version
- All backend tests pass
- AI endpoints functional post-upgrade

---


### BLG-SPEC-32 — External API integration spec template
**Priority:** P3 (Low)
**Type:** Spec Debt / Governance
**Owner:** Head of Specs Team
**Source:** IDEA-spec-20260421-01 — Promoted-Backlog cycle 2026-05-21__scheduled (DL-032)
**Effort:** S (~1 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** ≥ 2 external API integration contracts exist (second contract after Alpaca and Yahoo Finance).

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-21; _external_api_template.md created; 6 required sections; Anthropic + Alpaca conformance advisory noted)

**Problem**
Alpaca and Yahoo Finance are currently the only external API integrations, each with ad hoc contract documentation. If a second external API integration is scoped (e.g., a data vendor, broker alternative), a standardised spec template would reduce documentation inconsistency and ensure all new integrations capture: authentication model, rate limits, error taxonomy, cost attribution, and data model mapping. Gate ensures the overhead of a template is justified by reuse demand.

**Scope**
- Template document: `docs/specs/api_contracts/_external_api_template.md`
- Required sections: authentication, rate limits, error taxonomy, cost attribution, data model mapping, retry policy
- Retroactively apply template to Alpaca and YF contracts if conformant

**Acceptance Criteria**
- Template document produced and filed
- At minimum, the triggering (second) external API contract conforms to the template
- Gate condition verified by Head of Specs Team before sprint planning

---


### BLG-SPEC-43 — SI-04 strategy version comparison endpoint contract ✅ COMPLETE v4.8 (2026-06-02)
**Priority:** P2 (Medium)
**Type:** Spec / API Contract
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Source:** IDEA-api-contracts-20260527-02 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036; advanced STEP 5; Challenger clearance issued)
**Effort:** S-M (~1–2 days)
**Provisional-Target:** v4.8 (execute when SI-04 confirmed for next release planning cycle)

**Gate criteria:** SI-04 (Strategy Version Comparison) is confirmed for the next release planning cycle. §13 PASS already recorded v4.7 (6 binding conditions).

**Problem**
SI-04 strategy version comparison will introduce GET /analytics/strategy-version-comparison. Without a pre-authored API contract, the sprint implementing SI-04 must author the contract simultaneously, creating same-sprint spec debt per BLG-GOV-55 rule. Pattern of same-sprint spec debt occurred in SI-03 (spec debt filed v4.0, cleared v4.1) and SI-01 (similar pattern). Pre-authoring before sprint planning eliminates the risk.

**Scope**
- Author GET /analytics/strategy-version-comparison contract document under docs/specs/api_contracts/
- Define response schema: version_comparison (current strategy version vs historical, trade count per version, win_rate per version, avg_R per version, performance_delta)
- Define query parameters: version_from, version_to, date_range
- Define error cases: version_not_found (404), insufficient_data (422)
- Add endpoint entry to docs/reference/openapi.yaml (placeholder — implementation not required until SI-04 sprint)
- Review by SI-04 §13 binding conditions owner (Strategy Rules & System Intent Owner)

**Acceptance Criteria**
- API contract document created in docs/specs/api_contracts/
- Response schema defined (pending final SI-04 implementation confirmation)
- openapi.yaml entry added
- §13 binding conditions owner sign-off recorded on draft contract
- Gate condition (SI-04 in next release planning) verified before authoring begins

---


### BLG-SPEC-45 — SI-05 financial reporting scope verification (BLG-GOV-86 review)
**Priority:** P3 (Low)
**Type:** Specification / Documentation
**Owner:** Financial Reporting & Records Owner; Frontend Specs & UX Documentation Owner
**Source:** IDEA-financial-reporting-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038; gate cleared: BLG-GOV-86 shipped v5.0)
**Effort:** XS (~1 hour)
**Provisional-Target:** Unscheduled

**Gate criteria:** BLG-GOV-86 (SI-05 Telegram message format spec, shipped v5.0) reviewed to determine if financial reporting scope was explicitly addressed. If addressed → close this item; if not → define supplementary spec before SI-05 Phase 1 sprint planning.

**Problem**
SI-05 weekly digest will include compliance metrics. Whether it should also include financial performance summary (distinct from Arc5ComplianceSection data) was an open question to be resolved by BLG-GOV-86 format spec. Now that BLG-GOV-86 shipped, this question needs a closure decision.

**Scope**
- Review BLG-GOV-86 (Telegram message format spec) for explicit financial reporting scope decision
- If covered: document the decision and close this item
- If not covered: define supplementary spec addressing financial reporting in SI-05 digest

**Acceptance Criteria**
- BLG-GOV-86 reviewed; financial reporting scope question explicitly answered
- If supplementary spec needed: spec document produced and reviewed by Financial Reporting & Records Owner
- Gate condition verified before SI-05 sprint planning

✅ COMPLETE — 2026-06-04 — cycle 2026-06-21__release-v5.1 (ST-02, EPIC-01; BLG-GOV-86 reviewed — financial reporting confirmed OUT OF SCOPE for Phase 1; scope decision documented at docs/product/decisions/si05-financial-reporting-scope-decision.md)

---


### BLG-SPEC-47 — Align SI-05 `pass_rate` computation with BLG-GOV-86 §5.2 (mean-of-per-rule vs overall aggregate)
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-03, EPIC-01; Option(a) chosen — BLG-GOV-86 §5.2 amended to accept volume-weighted overall rate; si05-telegram-message-format-spec.md v1.1→v1.2; DEV-v51-EPIC01-01 resolved and closed; Head of Specs Team sign-off)
**Priority:** P3 (Low)
**Type:** Spec Debt / API Contracts
**Owner:** Head of Specs Team; Head of Backend Engineering
**Source:** DEV-v51-EPIC01-01 — v5.1 EPIC-01 QA sign-off — 2026-06-21
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.2

**Problem**
`si05_digest_service.py` computes `validation_pass_rate` as a volume-weighted overall ratio (`total_pass / total_validations` across all rules combined), while BLG-GOV-86 §5.2 specifies the mean of per-rule pass rates from `validation_pass_rate_by_rule`. These differ when validation rules have unequal sample volumes — high-volume rules dominate the aggregate but receive equal weighting in the mean. Additionally, `digest_endpoints.md` v0.2 documents the data source as "Overall pass/total ratio (7d)", creating a spec-to-spec inconsistency with the canonical format spec. P3 deviation DEV-v51-EPIC01-01 filed at v5.1 EPIC-01 QA sign-off. Must resolve before the next SI-05 feature increment.

**Scope**
- Head of Specs Team to determine canonical intent: (a) amend BLG-GOV-86 §5.2 to accept volume-weighted overall rate as the accepted computation, or (b) require the mean-of-per-rule-rates approach as originally specified
- If option (b): correct `backend/services/si05_digest_service.py` to iterate `validation_pass_rate_by_rule` entries and compute arithmetic mean; update `docs/specs/api_contracts/digest_endpoints.md` data source description accordingly
- If option (a): update `digest_endpoints.md` v0.2 to document the accepted overall-ratio computation and confirm alignment with BLG-GOV-86
- Apply CLAUDE.md §6 governance edit checklist if any governance file is modified

**Acceptance Criteria**
- BLG-GOV-86 §5.2 and `digest_endpoints.md` v0.2 are internally consistent and match the implementation
- `si05_digest_service.py` `validation_pass_rate` computation method matches the canonical spec decision
- Any spec amendments include version bump and `prompt_change_log.md` entry per CLAUDE.md §6 if governance files are modified
- DEV-v51-EPIC01-01 resolved and closed

---


### BLG-SPEC-48 — POST /digest/si05/send API contract gap check and authoring
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-04, EPIC-01; digest_endpoints.md v0.2→v0.3 with authentication requirements section; API Contracts & Documentation Owner sign-off; Head of Specs Team sign-off)
**Priority:** P1 (High)
**Type:** Spec / API Contract
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Source:** IDEA-api-contracts-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** XS–S (~1–2 hours if contract exists; ~0.5 day if authoring needed)
**Provisional-Target:** v5.2
**Displacement:** BLG-SPEC-46 (Arc 4 API surface area, P3, gate-conditional) deprioritised.

**Problem**
CLAUDE.md §2 requires "Every new API endpoint added to `backend/routers/` must have a corresponding `## METHOD /path` entry in a file in `docs/specs/api_contracts/` in the same sprint." v5.1 shipped POST /digest/si05/send via BLG-GOV-67 (ST-01, EPIC-01). No BLG-SPEC item for a digest endpoint API contract was filed alongside the implementation. If the contract was not authored, this is spec debt that must be resolved before the next sprint touching SI-05.

**Scope**
- Check: does `docs/specs/api_contracts/` contain a file with `## POST /digest/si05/send` as a heading?
- If YES: confirm it was filed in the v5.1 sprint and complies with CLAUDE.md §2; close item
- If NO: author the contract document covering: POST /digest/si05/send request/response schema, error cases (503 Telegram unavailable), authentication requirements; add entry to openapi.yaml; add to backend/routers/test.py if not present
- Apply CLAUDE.md §2 same-sprint rule retroactively for this v5.1 spec debt

**Acceptance Criteria**
- POST /digest/si05/send has a corresponding `## POST /digest/si05/send` entry in docs/specs/api_contracts/
- openapi.yaml has a corresponding entry
- backend/routers/test.py confirms the endpoint exists
- If contract was authored: version bump and prompt_change_log.md entry per CLAUDE.md §6 if any governance files were modified
- API Contracts & Documentation Owner and Head of Specs Team sign-off

---


### BLG-SPEC-49 — Author GET /ai/journal-summary/history API contract and openapi.yaml entry
**Priority:** P2 (Medium)
**Type:** Spec / API Contract
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Source:** ST-12 (BLG-GOV-100) — endpoint coverage audit post-v5.1, 2026-06-08__release-v5.2
**Effort:** XS (~1–2 hours)
**Provisional-Target:** v5.3

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-04, EPIC-01; ## GET /ai/journal-summary/history added to ai_endpoints.md; openapi.yaml updated; API Contracts & Documentation Owner sign-off)

**Problem**
`GET /ai/journal-summary/history` exists in `backend/routers/ai.py` and is tested in `backend/routers/test.py` but has no entry in `docs/specs/api_contracts/ai_endpoints.md` and is absent from `docs/reference/openapi.yaml`. This is a CLAUDE.md §2 spec debt gap identified in the post-v5.1 coverage audit.

**Acceptance Criteria**
- `## GET /ai/journal-summary/history` heading added to ai_endpoints.md (##-level, not ###)
- openapi.yaml updated with the path entry
- API Contracts & Documentation Owner sign-off

---


### BLG-SPEC-50 — Author GET /analytics/compliance-metrics API contract and openapi.yaml entry
**Priority:** P2 (Medium)
**Type:** Spec / API Contract
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Source:** ST-12 (BLG-GOV-100) — endpoint coverage audit post-v5.1, 2026-06-08__release-v5.2
**Effort:** XS (~1–2 hours)
**Provisional-Target:** v5.3

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-05, EPIC-01; ## GET /analytics/compliance-metrics added to analytics_endpoints.md; openapi.yaml updated; API Contracts & Documentation Owner sign-off)

**Problem**
`GET /analytics/compliance-metrics` exists in `backend/routers/analytics.py` and is tested in `backend/routers/test.py` but has no entry in `docs/specs/api_contracts/analytics_endpoints.md` (which documents other analytics endpoints) and is absent from `docs/reference/openapi.yaml`. This is spec debt identified in the post-v5.1 coverage audit.

**Acceptance Criteria**
- `## GET /analytics/compliance-metrics` heading added to analytics_endpoints.md (##-level)
- openapi.yaml updated with the path entry
- API Contracts & Documentation Owner sign-off

---


### BLG-SPEC-51 — Author GET /news/{ticker} API contract and openapi.yaml entry
**Priority:** P2 (Medium)
**Type:** Spec / API Contract
**Owner:** API Contracts & Documentation Owner; Head of Specs Team
**Source:** ST-12 (BLG-GOV-100) — endpoint coverage audit post-v5.1, 2026-06-08__release-v5.2
**Effort:** XS (~1–2 hours)
**Provisional-Target:** v5.3

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-06, EPIC-01; ## GET /news/{ticker} added to news_endpoints.md; openapi.yaml updated; API Contracts & Documentation Owner sign-off)

**Problem**
`GET /news/{ticker}` exists in `backend/routers/news.py` and is tested in `backend/routers/test.py` but has no dedicated API contract document in `docs/specs/api_contracts/` (the Alpaca integration contract covers the external news API, not this internal endpoint) and is absent from `docs/reference/openapi.yaml`. This is spec debt identified in the post-v5.1 coverage audit.

**Acceptance Criteria**
- A file in `docs/specs/api_contracts/` contains `## GET /news/{ticker}` as a ##-level heading
- openapi.yaml updated with the path entry
- API Contracts & Documentation Owner sign-off

---


### BLG-SPEC-52 — Author watchlist endpoint contracts and add openapi.yaml + test.py entries
**Priority:** P2 (Medium)
**Type:** Spec / API Contract
**Owner:** API Contracts & Documentation Owner; Head of Specs Team; Head of Engineering
**Source:** ST-12 (BLG-GOV-100) — endpoint coverage audit post-v5.1, 2026-06-08__release-v5.2
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.3

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-07, EPIC-01; watchlist_endpoints.md authored with ## GET/POST/DELETE headings; openapi.yaml + test.py entries added; SystemStatus fallback count and SC-SS-01b updated; API Contracts & Documentation Owner + Head of Specs Team sign-off)

**Problem**
Watchlist endpoints (`GET /watchlist`, `POST /watchlist`, `DELETE /watchlist/{entry_id}`) exist in `backend/routers/watchlist.py` but have no API contract document in `docs/specs/api_contracts/`, no entries in `docs/reference/openapi.yaml`, and are absent from `backend/routers/test.py`. This is a triple-gap (contract + openapi.yaml + test) identified in the post-v5.1 coverage audit. CLAUDE.md §2 same-sprint rule applies retroactively as spec debt.

**Acceptance Criteria**
- A file in `docs/specs/api_contracts/` contains `## GET /watchlist`, `## POST /watchlist`, `## DELETE /watchlist/{entry_id}` as ##-level headings
- openapi.yaml updated with all three path entries
- backend/routers/test.py entries added for all three watchlist endpoints
- SystemStatus.js fallback count and SC-SS-01b in tests/e2e/system-status.spec.js updated if test.py count changes (per CLAUDE.md §2)
- API Contracts & Documentation Owner and Head of Specs Team sign-off

---


### BLG-SPEC-53 — BLG-SPEC-49–52 contract gap resolution plan
**Priority:** P1 (High)
**Type:** Spec Debt / Governance
**Owner:** Head of Specs Team; API Contracts & Documentation Owner
**Source:** IDEA-head-of-specs-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** M (~1–2 days)
**Provisional-Target:** v5.3
**Displacement:** BLG-GOV-101 (governance complexity assessment, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-01, EPIC-01; api_contract_gap_resolution_plan.md produced; all 6 gaps priority-ranked; sprint scope confirmed; Head of Specs Team + API Contracts & Documentation Owner sign-off)

**Problem**
v5.2 endpoint coverage audit (BLG-GOV-100, ST-12) found 6 routes without API contracts: GET /ai/journal-summary/history, GET /analytics/compliance-metrics, GET /news/{ticker}, GET /watchlist, POST /watchlist, DELETE /watchlist/{entry_id} (BLG-SPEC-49–52). These contracts are required by CLAUDE.md §2 but were not filed at the time the endpoints shipped. A structured resolution plan ensures they are all resolved in a single v5.3 effort.

**Scope**
- Produce a resolution plan document for all 6 endpoint contract gaps
- Priority-rank the 6 gaps by risk (auth exposure, external-facing vs internal, complexity)
- Define sprint scope for v5.3: which gaps ship in the same sprint story vs separate stories
- Confirm whether any additional openapi.yaml gaps exist beyond BLG-SPEC-49–52

**Acceptance Criteria**
- Resolution plan document produced with priority-ranked gap list
- Sprint scope recommendation made for v5.3 sprint planning
- Head of Specs Team and API Contracts & Documentation Owner sign-off

---


### BLG-SPEC-54 — openapi.yaml completeness audit against all 50 routes
**Priority:** P1 (High)
**Type:** Spec Debt / API Governance
**Owner:** API Contracts & Documentation Owner; Head of Engineering
**Source:** IDEA-api-contracts-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.3
**Displacement:** BLG-SPEC-46 (Arc 4 API contract pre-planning, gate-conditional) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-02, EPIC-01; all 50 routes audited against openapi.yaml; gaps identified and resolved; gap report produced; API Contracts & Documentation Owner sign-off)

**Problem**
v5.2 found 50 routes in backend/routers/. openapi.yaml coverage against all 50 routes has never been formally audited. The drift detection gate catches routes missing from api_contracts/ documents, but may not catch routes that are in contracts but missing from openapi.yaml. A formal audit ensures the public API surface is fully documented.

**Scope**
- List all 50 routes from backend/routers/ test.py or router files
- Compare against docs/reference/openapi.yaml entries
- Identify any routes present in contract files but absent from openapi.yaml
- Produce gap report; file additional BLG-SPEC items for any uncovered routes
- Update openapi.yaml for any confirmed gaps

**Acceptance Criteria**
- All 50 routes audited against openapi.yaml
- Gap report produced
- openapi.yaml updated for any confirmed gaps
- API Contracts & Documentation Owner sign-off

---


### BLG-GOV-30 — Sprint planning staging-only AC designation flag
**Priority:** P1 (High)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Before v4.0 sprint planning

**Problem**
v3.9 post-ship closure carry-forward advisory item #2: environment-dependent ACs (those referencing Yahoo Finance, Alpaca, or other live service behaviour) were not designated "staging-only" at sprint planning. This resulted in BLG-QA-24 being filed as a surprise P3 notation at QA sign-off. A per-story staging_only_evidence flag at sprint planning time prevents this pattern.

✅ COMPLETE — v4.1 — sprint_planning_prompt.md v3.7 added staging-only AC gate (OA-02; confirmed resolved per v4.5 scope reference and lessons_learnt.md v4.6)

**Scope**
- Add `staging_only_evidence` notation to sprint_backlog.md story schema documentation
- Update sprint_planning_prompt.md to prompt for staging-only designation when an AC references external live service behaviour
- Applies CLAUDE.md §6 governance file edit checklist (version bump, OPERATIONAL_GUIDE.md update, prompt_change_log.md entry)

**Acceptance Criteria**
- sprint_planning_prompt.md updated with explicit staging-only AC designation prompt
- sprint_backlog.md story format updated to include staging_only_evidence field documentation
- prompt_change_log.md entry appended per §6 checklist
- Head of Specs Team sign-off recorded

---


### BLG-GOV-31 — Merge gate re-invocation advisory in sprint capacity template
**Priority:** P1 (High)
**Type:** Governance Process
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** XS (~0.5 day)
**Provisional-Target:** Before v4.0 sprint planning

**Problem**
v3.9 post-ship closure carry-forward advisory item #1: merge_gate.epics_merged was not updated during out-of-band GitHub merges, causing stale state when the execution engine resumed. The fix is documenting in the sprint capacity template that the execution engine must be re-invoked after each EPIC GitHub merge.

**Scope**
- Add advisory note to sprint capacity template: "After each EPIC PR merge to main, re-invoke the execution engine to update merge_gate.epics_merged before proceeding to the next EPIC"
- Applies CLAUDE.md §6 governance file edit checklist if sprint_capacity_template.md is a governed file

**Acceptance Criteria**
- Sprint capacity template updated with re-invocation advisory
- Head of Specs Team sign-off recorded

✅ COMPLETE — v4.x — LL-v3.9-P3-1 in-session merge gate sync implemented in execution_prompt.md; advisory pattern resolved (confirmed resolved per v4.5 scope reference and lessons_learnt.md v4.6)

---


### BLG-GOV-32 — Gate-condition clearing tracker at release planning
**Priority:** P2 (Medium)
**Type:** Governance Process
**Owner:** PMO Lead
**Source:** IDEA-pmo-lead-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled

**Problem**
Gate-conditional backlog items (e.g., BLG-GOV-39, BLG-SPEC-35) have gates that may clear at unpredictable times. Currently gates are checked reactively (if PO remembers at release planning). A structured gate-scan checklist at each release planning kickoff — listing items likely to clear in the next 30–60 days — provides proactive pipeline visibility for sprint sequencing.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-15; release_planning_prompt.md v2.33 STEP 1.4 Gate-Condition Proximity Scan added; combined with BLG-GOV-43)

**Scope**
- Add a gate-scan checklist step to the release planning prompt or release planning artefact
- At each release planning kickoff: scan all gate-conditional backlog items; flag gates likely to clear within 30–60 days given current trajectory
- Output: gate proximity table in the release plan artefact

**Acceptance Criteria**
- Release planning process includes a gate-scan step
- Gate proximity table produced at each release planning run
- Applies CLAUDE.md §6 checklist if release_planning_prompt.md is modified

---


### BLG-GOV-33 — PT-04 closed trade count audit
**Priority:** P2 (Medium)
**Type:** Governance / Product Audit
**Owner:** Product Owner; Challenger
**Source:** IDEA-challenger-20260522-01 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** XS (~0.5 day)
**Provisional-Target:** v4.0 release planning

**Problem**
PT-04 (Setup Quality Score) gate (20+ closed trades) has been unmet for 4 consecutive cycles (v3.6–v3.9). No verification of the actual production closed trade count has been documented in any cycle artefact. If the count is 15–19, PT-04 is near-clearing and should be planned proactively. If under 10, the gate condition calibration may warrant review.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-16; Q1=6 closed trades, Q2=0 with linked trade_plans; gate NOT MET; EPIC-02 deferred 6th time; BLG-FEAT-25 updated)

**Scope**
- Query production database for current closed trade count
- Document count in release planning artefact (v4.0) and in PT-04 backlog item
- If count ≥ 20: advance PT-04 to v4.0 sprint planning
- If count 15–19: note in v4.0 release plan as near-gate item with projected clearing date
- If count < 10: consider gate revision at v4.0 release planning

**Acceptance Criteria**
- Closed trade count documented in v4.0 release planning artefact
- PT-04 gate status updated based on count
- PO decision recorded for any gate revision

---


### BLG-GOV-34 — Arc 4 data density risk trajectory assessment
**Priority:** P2 (Medium)
**Type:** Governance / Risk Assessment
**Owner:** Product Owner; Challenger
**Source:** IDEA-challenger-20260522-02 — Promoted-Backlog cycle 2026-05-22__scheduled (DL-033)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v4.0 release planning

**Problem**
PO-02 (Journal Pattern Recognition) requires 6+ months of AI journal entries. PO-04 (Reflection/Outcome Correlation) requires 50+ trades with plans. PO-05 (Lightweight Replay Mode) requires IT-06 foundation + significant trade history. At current trade frequency, these gates may not clear within v4.0–v4.2. Without a formal trajectory assessment, these features are perpetually "planned" without realistic delivery dates.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-17; arc4_data_density_trajectory_v4.6.md; Option A selected — proceed on current trajectory; SI-02 gate ~Nov 2026, PT-04 sub-gate ~Sep 2026; PO + Challenger sign-off)

**Scope**
- Assessment: current trade frequency (trades/month), AI journal entry rate, trade plan creation rate
- Trajectory: projected dates for PO-02 gate (6+ months AI journals), PO-04 gate (50+ trades with plans), PO-04 gate (50+ closed trades)
- Recommendation: are gates realistic within 4 cycles, or should gate conditions be reconsidered?
- Output: trajectory assessment document; input to v4.0 release planning

**Acceptance Criteria**
- Trajectory assessment document produced at v4.0 release planning
- Gate clearing dates projected
- PO decision recorded: proceed on current trajectory, revise gates, or re-scope features

---


### BLG-GOV-40 — Delivery verification STEP 5.0A pr_number null guard
**Priority:** P2 (Medium)
**Type:** Governance / Prompt Engineering
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** Head of Specs Team OA-04 resolution at v4.1 sprint planning — delivery_verification_prompt.md STEP 5.0A pr_number null guard patch.

**Problem**
OA-04 (from v4.0 post-ship closure) identified that delivery_verification_prompt.md STEP 5.0A lacks a null guard for pr_number — if a PR was merged without a number being recorded, the step may fail or produce misleading output. The guard should gracefully handle missing pr_number by surfacing a warning rather than halting.

**Scope**
- Add null guard to STEP 5.0A in delivery_verification_prompt.md
- Bump prompt version; update OPERATIONAL_GUIDE.md §14; append prompt_change_log.md entry
- Per CLAUDE.md §6 governance file edit checklist

**Acceptance Criteria**
- STEP 5.0A includes null guard for pr_number (warning output, not halt)

✅ COMPLETE — v4.1 — delivery_verification_prompt.md v2.6 pr_number null guard implemented (OA-04 resolution; confirmed resolved per lessons_learnt.md v4.6)
- Prompt version bumped; OPERATIONAL_GUIDE.md §14 updated; prompt_change_log.md appended
- Gate condition (OA-04 resolution at v4.1 sprint planning) verified

---


### BLG-GOV-41 — Sprint close automation failure investigation
**Priority:** P2 (Medium)
**Type:** Governance / Process
**Owner:** PMO Lead; Infrastructure & Operations Owner
**Source:** IDEA-pmo-lead-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Gate criteria:** sprint_close_reminder.yml failure mechanism identified — per OA-03 from v4.0 post-ship closure.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-20; workflow functioning as designed — observer effect/early filing; no fix required; investigation doc committed)

**Problem**
OA-03 (from v4.0 post-ship closure) flagged that sprint_close_reminder.yml failed silently. Investigation is needed to determine: what the failure mode is, whether it is a GitHub Actions timing issue, environment issue, or logic error, and whether automated sprint close reminders should be retained or replaced with a documented manual trigger.

**Scope**
- Review sprint_close_reminder.yml workflow for failure cause
- Check GitHub Actions run logs for the failing cycle (2026-05-22__release-v4.0)
- Propose fix or retirement of the automated trigger
- Document findings and chosen resolution

**Acceptance Criteria**
- Root cause identified and documented
- Fix implemented or workflow retired with documented rationale
- Gate condition (investigation outcome) verified before item closes

---


### BLG-GOV-43 — Arc 4 data density formal checkpoint
**Priority:** P2 (Medium)
**Type:** Governance / Release Gate
**Owner:** Product Owner; PMO Lead
**Source:** IDEA-product-owner-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Problem**
Arc 4 features (PO-02 through PO-05) all have data density gates: 6+ months AI journal entries (PO-02), 50+ trades with plans (PO-04), 50+ trades with regime-at-entry (PO-05). A formal checkpoint at each release planning cycle confirms whether gates are approaching satisfaction. Currently this check is informal and reactive. A structured checkpoint prevents sprint planning a story against a gate that won't clear for months.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-15; release_planning_prompt.md v2.33 STEP 1.4 Gate-Condition Proximity Scan added; combined with BLG-GOV-32)

**Scope**
- Define Arc 4 data density checkpoint procedure: trade count, plan count, AI journal entry count
- Add checkpoint step to release planning prompt or OPERATIONAL_GUIDE.md §6B
- Checkpoint produces a pass/fail per Arc 4 gate condition

**Acceptance Criteria**
- Checkpoint procedure defined
- Integrated into release planning reference materials
- Product Owner and PMO Lead sign-off

---


### BLG-GOV-45 — Arc 6 Monte Carlo §13 pre-assessment
**Priority:** P2 (Medium)
**Type:** Governance / §13 Compliance Pre-work
**Owner:** Strategy Rules & System Intent Owner
**Source:** IDEA-strategy-owner-20260525-02 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Problem**
PS-03 (Monte Carlo Simulation, Arc 6) is documented as "§13 compliant — deterministic simulation" on the roadmap. Before Arc 6 sprint planning, a formal §13 pre-assessment of Monte Carlo confirms: the simulation uses actual trade distribution data only (no external benchmarks), produces context not recommendations, and does not engage the ML/prediction boundary. Early pre-assessment prevents a last-minute gate discovery at Arc 6 planning.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-18; PASS — 10 binding conditions; arc6_ps03_section13_preassessment.md; Arc 6 planning path clear; Strategy Rules & System Intent Owner sign-off)

**Scope**
- Run §13 checklist against PS-03 Monte Carlo feature definition
- Confirm: simulation is deterministic, uses own trade data only, output is statistical context not a recommendation
- Document assessment and binding conditions (if any)

**Acceptance Criteria**
- §13 assessment produced for PS-03
- Binding conditions documented
- Reviewed by Strategy Rules & System Intent Owner

---


### BLG-GOV-52 — Trade plan schema field count gate check
**Priority:** P2 (Medium)
**Type:** Governance / Data Model
**Owner:** Data Model & Domain Schema Owner; Product Owner
**Source:** IDEA-data-model-20260525-01 — Promoted-Backlog cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

**Problem**
The trade plan data model (shipped v3.1, expanded through v3.5) contains a growing number of fields. Before Arc 4 deep analytics (PO-02, PO-03) and Arc 5 SI-02 add further fields, a gate check confirms: current field count is within manageable scope, there are no orphaned fields (captured but never surfaced), and the schema remains internally consistent with the roadmap's stated field list.

✅ COMPLETE — 2026-05-31 — cycle 2026-05-30__release-v4.6 (ST-19; trade_plan_schema_audit_v4.6.md; 25 fields post-DS-07; 0 orphaned fields; 3 P3 process gaps filed; Data Model & Domain Schema Owner sign-off)

**Scope**
- Review trade plan schema: enumerate all fields, cross-reference with roadmap feature descriptions
- Identify: orphaned fields (present but unused), missing fields (needed but absent), consistency with PT-01 trade plan object definition
- Output: schema audit note

**Acceptance Criteria**
- Schema audit note produced
- Orphaned fields identified (if any) with remediation recommendation
- Reviewed by Data Model & Domain Schema Owner

---


### BLG-GOV-55 — API contract same-sprint delivery rule
**Priority:** P1 (High)
**Type:** Governance / Process Rule
**Owner:** Head of Specs Team; API Contracts Documentation Owner
**Source:** IDEA-head-of-specs-20260525-01 — Promoted-Backlog (STEP 5 debate) cycle 2026-05-25__scheduled (DL-034)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.1

**Problem**
v4.0 shipped POST /trade-plans/{plan_id}/generate-thesis (ST-12) without a formal API contract document (addressed retroactively by BLG-SPEC-38). CLAUDE.md §2 already requires every new endpoint to be added to openapi.yaml in the same commit. A complementary rule requiring a formal API contract document in docs/specs/api_contracts/ in the same sprint as the endpoint prevents retroactive BLG-SPEC debt from recurring.

**Scope**
- Add rule to CLAUDE.md §2 (or sprint planning checklist): every new ## METHOD /path heading in a backend router file must have a corresponding API contract document in docs/specs/api_contracts/ in the same sprint
- Align with existing CLAUDE.md §2 openapi.yaml same-commit rule
- Head of Specs Team sign-off; bump CLAUDE.md version if applicable

**Acceptance Criteria**
- Rule added to CLAUDE.md §2 or sprint planning reference
- Head of Specs Team sign-off
- Rule applies from v4.1 sprint planning onward

✅ COMPLETE — v4.1+ — CLAUDE.md §2 rule added: "Every new API endpoint must be added to `docs/reference/openapi.yaml` in the same commit as the contract." and "Every new backend route must be registered in the endpoint test suite in the same commit." (confirmed resolved per v4.5 scope reference and lessons_learnt.md v4.6)

---


### BLG-GOV-67 — SI-05 early delivery (Phase 1 without SI-02)
**Priority:** P2 (Medium)
**Type:** Governance / Feature Scope Definition
**Owner:** Product Owner; Head of Specs Team
**Source:** IDEA-product-owner-20260522-01 — Promoted-Backlog cycle 2026-05-27__scheduled (DL-035, 3-cycle cap; gate cleared; Challenger gate modification applied)
**Effort:** M (~2–3 days)
**Provisional-Target:** Unscheduled

**Gate criteria:** SI-01 + SI-03 live ≥ 30 days (gate clears 2026-06-21).

**Problem**
SI-05 (Weekly Strategy Integrity Digest) requires SI-02 (drift detection) for the drift score component. Phase 1 of SI-05 can ship using SI-01 and SI-03 data only: validation pass rate, override count, and red flag trends. BLG-GOV-54 (shipped v4.1) defined Phase 1 scope; this item is the implementation backlog entry.

**Scope**
- Implement SI-05 Phase 1: weekly digest using SI-01 + SI-03 data only
- Metrics: validation_pass_rate, override_count, red_flag_frequency_trend
- No drift score in Phase 1 (requires SI-02)
- Gate: SI-01 + SI-03 live ≥ 30 days (2026-06-21)

**Acceptance Criteria**
- Weekly digest renders with SI-01 + SI-03 metrics
- No SI-02 dependency in Phase 1 implementation
- Gate condition (SI-01 + SI-03 live ≥ 30 days) verified before sprint planning

✅ COMPLETE — 2026-06-04 — cycle 2026-06-21__release-v5.1 (ST-01, EPIC-01; backend/services/si05_digest_service.py delivered; POST /digest/si05/send; 21 unit tests; gate confirmed 2026-06-21; 1 P3 deviation DEV-v51-EPIC01-01 filed)

---


### BLG-GOV-161 — §13 register completion (AUD-2026-05-30-001 gap) ✅ COMPLETE v4.8 (2026-06-02)
**Renumbered from:** BLG-GOV-69 (ID collision resolved — v6.6 ST-03; BLG-GOV-69 retained by the earlier-archived entry "spec_references policy for documentation-creation stories")
**Priority:** P2 (Medium)
**Type:** Governance / Compliance
**Owner:** Head of Specs Team
**Source:** IDEA-head-of-specs-20260601-01 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v4.8

**Problem**
AUD-2026-05-30-001 identified 7 governance prompts missing from §13 ARTEFACT_STATUS entries in OPERATIONAL_GUIDE.md §14: sprint_planning_prompt.md, execution_prompt.md, post_ship_closure.md, design_gate_prompt.md, roadmap_management_prompt.md, backlog_management_prompt.md, ideas_housekeeping_prompt.md. This governance integrity gap depresses the audit Governance Integrity dimension score.

**Scope**
- Add §13 ARTEFACT_STATUS entries for each of the 7 missing prompts in OPERATIONAL_GUIDE.md §14
- Ensure entries follow existing §13 format (version, last_updated, authority)
- Bump OPERATIONAL_GUIDE.md version per §6 governance edit checklist

**Acceptance Criteria**
- All 7 missing prompts added to §14 §13 register
- OPERATIONAL_GUIDE.md version bumped; prompt_change_log.md appended
- AUD-2026-05-30-001 gap confirmed closed

---


### BLG-GOV-162 — Agent charter header compliance remediation ✅ COMPLETE v4.8 (2026-06-02)
**Renumbered from:** BLG-GOV-70 (ID collision resolved — v6.6 ST-03; BLG-GOV-70 retained by the earlier-archived entry "qa_evidence_template.md: DoQ sign-off format for delegated_qa")
**Priority:** P2 (Medium)
**Type:** Governance / Compliance
**Owner:** Director of HR; Head of Specs Team
**Source:** IDEA-director-of-hr-20260601-02 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.8

**Problem**
AUD-2026-05-30 Stage 3 identified 2 non-compliant agent charter files:
- api_contracts_documentation_owner.md: uses `## Role:` instead of `**Role:**`
- backend_engineering_patterns_owner.md: uses `**Owner:**` not `**Role:**`

Non-compliant headers may cause governance engines to fail role validation.

**Scope**
- Fix header in api_contracts_documentation_owner.md (`## Role:` → `**Role:**`)
- Fix header in backend_engineering_patterns_owner.md (`**Owner:**` → `**Role:**`)
- Verify no other agent files have non-compliant format

**Acceptance Criteria**
- Both files have compliant `**Role:**` header format
- All other agent files verified as compliant
- No governance engine role-validation failures after fix

---


### BLG-GOV-164 — AUD-2026-05-30-006 gap resolution verification ✅ COMPLETE v4.8 (2026-06-02)
**Renumbered from:** BLG-GOV-72 (ID collision resolved — v6.6 ST-03; BLG-GOV-72 retained by the earlier-archived entry "sprint_planning_prompt.md: frontend classification fast-path")
**Priority:** P2 (Medium)
**Type:** Governance / Audit Follow-up
**Owner:** PMO Lead
**Source:** IDEA-pmo-lead-20260601-01 — Promoted-Backlog cycle 2026-06-01__scheduled (DL-036)
**Effort:** S (~0.5 day)
**Provisional-Target:** v4.8

**Problem**
AUD-2026-05-30-006 identified 3 deferred patches in v4.4 lessons_learnt_closure.md without BLG IDs — untracked in the backlog. Whether these were resolved in v4.5–v4.7 is unclear.

**Scope**
- Load v4.4 lessons_learnt_closure.md and identify the 3 patches
- Check v4.5–v4.7 sprint records for resolution
- If resolved: document and close; if not: file new BLG-GOV items

**Acceptance Criteria**
- v4.4 patches identified; resolution status confirmed
- Unresolved patches filed as new BLG items; AUD-2026-05-30-006 gap closed or escalated

---


### BLG-OPS-52 — ST-02 staging verification: Anthropic SDK 0.40.0 → 0.105.2 endpoint validation
✅ COMPLETE — 2026-06-03 — cycle 2026-06-03__release-v5.0 (ST-08, EPIC-03; staging verification run on trading-assistant-api-staging.onrender.com; AC-01 POST /trade-plans/{plan_id}/generate-thesis HTTP 200 + non-null thesis confirmed; AC-02 POST /ai/check-daily-cost HTTP 200 + cost structure confirmed; Infrastructure & Operations Owner sign-off 2026-06-03; DoQ agent-mediated sign-off 2026-06-03)
**Priority:** P2 (Medium)
**Type:** Operations / Infrastructure
**Owner:** Infrastructure & Operations Owner
**Source:** v4.9 EPIC-01 ST-02 AC-04 staging gate deferred post-merge (CLAUDE.md §2) — 2026-06-02
**Effort:** XS (<1h)
**Provisional-Target:** v4.10

**Problem**
ST-02 (Anthropic SDK upgrade 0.40.0 → 0.105.2) includes a staging-only AC requiring verification that POST /trade-plans/{plan_id}/generate-thesis and POST /ai/check-daily-cost remain functional post-upgrade. This cannot be confirmed autonomously and was deferred post-merge per CLAUDE.md §2 staging gate. Sign-off must be obtained before the next cycle that touches AI endpoints.

**Scope**
- On staging environment post v4.9 deploy: verify POST /trade-plans/{plan_id}/generate-thesis returns a valid AI-generated thesis
- Verify POST /ai/check-daily-cost returns the expected cost response
- Record Infrastructure & Operations Owner sign-off in the relevant QA evidence log

**Acceptance Criteria**
- POST /trade-plans/{plan_id}/generate-thesis returns HTTP 200 with non-null thesis field post SDK upgrade
- POST /ai/check-daily-cost returns HTTP 200 with expected cost structure post SDK upgrade
- Infrastructure & Operations Owner sign-off recorded with staging verification date

---


### BLG-OPS-55 — Deployment runbook update for SI-05 operational environment
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-07, EPIC-02; docs/ops/production_deployment_runbook.md v0.1→v0.2; §6 added covering SI-05 env vars, cron schedule, service verification, failure detection; Infrastructure & Operations Owner sign-off)
**Priority:** P2 (Medium)
**Type:** Operations / Documentation
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** XS (~1–2 hours)
**Provisional-Target:** v5.2
**Displacement:** BLG-OPS-20 (research endpoint cost monitoring, P3, gate-conditional) deprioritised.

**Problem**
SI-05 Phase 1 (shipped v5.1) introduced new operational requirements not yet documented in the deployment runbook: (a) Telegram bot token environment variable (`TELEGRAM_BOT_TOKEN` or equivalent), (b) weekly digest cron schedule configuration, (c) si05_digest_service.py as a background/scheduled service that must be running in the deployed environment. If Render is rebuilt or the service is redeployed, missing this configuration silently disables the weekly digest.

**Scope**
- Update deployment runbook (docs/operations/ or equivalent) with SI-05 operational requirements:
  - Environment variable: name, purpose, where to obtain the Telegram bot token
  - Cron schedule: how the weekly digest schedule is configured (Render cron job? APScheduler?)
  - Service health check: how to verify the weekly digest service is running
  - Failure detection: how to confirm a digest was sent (reference BLG-BE-33 delivery log once shipped)
- Infrastructure & Operations Owner signs off on updated runbook

**Acceptance Criteria**
- Deployment runbook updated with all SI-05 environment requirements
- Telegram bot token environment variable documented
- Cron schedule configuration documented
- Infrastructure & Operations Owner sign-off

---


### BLG-OPS-56 — SI-05 service scheduled run health check
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-08, EPIC-02; docs/ops/si05_health_check_procedure.md created; 3 check options: si05_digest_log (Option A), Render logs (Option B interim), Telegram history (Option C); escalation path; weekly cadence; Infrastructure & Operations Owner sign-off)
**Priority:** P2 (Medium)
**Type:** Operations / Service Reliability
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Source:** IDEA-head-of-engineering-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** XS (~1–2 hours)
**Provisional-Target:** v5.2
**Displacement:** BLG-OPS-23 (screener performance benchmark, P3, gate-conditional) deprioritised.

**Problem**
si05_digest_service.py runs on a weekly schedule. There is currently no documented way to verify whether the scheduled run completed successfully on any given week. Without a health check, a silently failing cron job (environment misconfiguration, scheduler crash, Render dyno sleep) would not be detected until the PO notices they haven't received a digest.

**Scope**
- Define health check procedure: how to confirm the weekly digest ran successfully
  - Option A: check si05_digest_log table (BLG-BE-33) for a recent send_at timestamp
  - Option B: check Render service logs for the service's INFO log entry
  - Option C: check Telegram chat history for a digest message
- Implement the simplest observable check; document in ops runbook
- If no observable check is possible without BLG-BE-33: document that BLG-BE-33 is a prerequisite for reliable health checking

**Acceptance Criteria**
- Health check procedure documented for si05_digest_service.py
- Procedure specifies: what to check, where to find the evidence, what constitutes PASS
- Infrastructure & Operations Owner and Head of Engineering sign-off

---


### BLG-OPS-57 — SI-05 Telegram delivery failure alerting
**Priority:** P1 (High)
**Type:** Operations / Monitoring
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Source:** IDEA-infra-ops-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.3
**Displacement:** BLG-OPS-13 (performance baseline gaps, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-09, EPIC-02; FAILED status logged to si05_digest_log; ERROR-level Render log alert; ops runbook updated; Infrastructure & Operations Owner sign-off)

**Problem**
SI-05 delivers a weekly Telegram digest. BLG-OPS-56 (health check, v5.2) provides a manual verification procedure, but there is no automated alerting when delivery fails — a Telegram API error, revoked bot token, or rejected message would go undetected until manual inspection.

**Scope**
- Add a delivery confirmation check to si05_digest_service.py: if Telegram API returns non-200 or the send raises an exception, log to si05_digest_log with status = FAILED and trigger an admin alert
- Admin alert mechanism: write a log entry to stderr/Render logs at ERROR level; optionally post an alert message to the operator's Telegram or email
- Ensure retry logic (BLG-BE-32, shipped v5.2) still applies before the failure alert triggers

**Acceptance Criteria**
- Failed digest delivery is logged with status=FAILED in si05_digest_log
- A human-observable alert is triggered (Render log at ERROR level minimum)
- Delivery failure alerting documented in ops runbook (update docs/operations/deployment_runbook.md)
- Infrastructure & Operations Owner sign-off

---


### BLG-OPS-58 — CI secret scanning gate
**Priority:** P1 (High)
**Type:** Operations / Security
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Source:** IDEA-cybersecurity-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.3
**Displacement:** BLG-OPS-13 (performance baseline gaps, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-10, EPIC-02; gitleaks CI secret scanning gate operational via .github/workflows/secret-scanning.yml + .gitleaks.toml; test_token advisory noted as low-risk; Cybersecurity & Trust Lead sign-off)

**Problem**
No secret scanning is configured in the CI pipeline. A developer could accidentally commit TELEGRAM_BOT_TOKEN, ANTHROPIC_API_KEY, or Supabase credentials to the repository. Given that the Telegram bot controls production digest delivery and the Anthropic API key incurs real costs, a leaked secret would be high-impact.

**Scope**
- Add a secret scanning step to GitHub Actions CI pipeline (e.g., gitleaks action or trufflehog)
- Configure to scan for: Telegram bot token patterns, Anthropic API key patterns, Supabase URL/key patterns, generic high-entropy strings
- Fail CI on detection; produce a clear error message identifying the type of secret
- Add a .gitleaks.toml or equivalent allowlist for known false positives (e.g., test fixture tokens)

**Acceptance Criteria**
- Secret scanning step added to CI and runs on every PR
- Confirmed to detect a test dummy token (AAAA-format) before allowlisting it
- Allowlist documented for any confirmed false positives
- CI fails and blocks merge when a real-looking secret is detected
- Cybersecurity & Trust Lead sign-off

---


### BLG-OPS-60 — Add v5.3 new endpoints to api_performance_baseline.md re-run
**Priority:** P3 (Low)
**Type:** Operations / Performance
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Source:** Post-ship closure 2026-06-08__release-v5.3 — STEP 6 endpoint coverage drift check
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.4

✅ COMPLETE — 2026-06-10 — cycle 2026-06-09__release-v5.4 (ST-01, EPIC-01; 5 endpoint rows added to api_performance_baseline.md §17 with live Render measurements; I&O Owner sign-off)

**Problem**
v5.3 shipped 5 new endpoints that appear in openapi.yaml but are absent from api_performance_baseline.md: GET /ai/journal-summary/history, GET /news/{ticker}, GET /watchlist, POST /watchlist, DELETE /watchlist/{entry_id}. (GET /analytics/compliance-metrics was already baselined.) Without baseline entries, performance regressions on these endpoints will go undetected.

**Scope**
- Run performance baseline measurements for all 5 missing endpoints in a staging/production environment
- Add measurement rows to docs/ops/api_performance_baseline.md
- Note p50/p95/p99 and any threshold flags

**Acceptance Criteria**
- All 5 new endpoints have baseline rows in api_performance_baseline.md
- Performance measurements made against a live environment (not mocked)
- Infrastructure & Operations Owner sign-off

---


### BLG-GOV-78 — roadmap_prompt.md STEP 8.1 Empty Now Horizon gate strengthening
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Head of Specs Team; PMO Lead
**Source:** LL-RP-v4.8-01 (post-ship closure 2026-06-01__release-v4.8)
**Effort:** S (~0.5 day)
**Provisional-Target:** Unscheduled

✅ COMPLETE — 2026-06-02 — cycle 2026-06-02__release-v4.9 (ST-05, EPIC-03; roadmap_prompt.md v6.7→v6.8; STEP 8.1 converted to soft gate; OPERATIONAL_GUIDE.md v4.25→v4.26; prompt_change_log.md appended; HoST + PMO Lead sign-off)

**Problem**
When a roadmap rebalance runs as "No-change" and the Now horizon is empty, roadmap_prompt.md v6.6 STEP 8.1 fires an advisory — but does not require an explicit PO decision. In v4.8 release planning, this caused STEP -1.2 to fail because no formal v4.8 roadmap section existed after the no-change rebalance. The advisory was silently ignored.

**Scope**
- Strengthen STEP 8.1 of roadmap_prompt.md: when the Now horizon is empty and no next-release section exists in current_roadmap.md, require an explicit PO decision — either (a) add the next-release section now, or (b) defer intentionally with written rationale recorded in the cycle summary
- This converts a silent advisory into a soft gate requiring a documented PO choice

**Acceptance Criteria**
- roadmap_prompt.md STEP 8.1 updated: empty-Now-horizon with no next-release section requires explicit PO decision before completing the rebalance
- PO decision options documented (add section now OR defer with rationale)
- OPERATIONAL_GUIDE.md version bumped per CLAUDE.md §6 governance edit checklist
- Head of Specs Team + PMO Lead sign-off

---


### BLG-GOV-79 — Append 7 missing prompt_change_log.md entries for cycles 31–35 ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P2 (Medium)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** AUD-2026-06-02 (AUD-2026-06-02-001, STALE 2nd occurrence) — 2026-06-02
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.0

**Problem**
prompt_change_log.md is missing 7 entries for prompt version changes that occurred in cycles 31–35 (v4.5–v4.8). The OPERATIONAL_GUIDE §14 changelog confirms all 7 changes occurred and all engine versions in §14 are correct, but the corresponding prompt_change_log rows were never written — violating the CLAUDE.md §2 hard rule "any prompt version increment must have a matching entry in prompt_change_log.md." This was flagged as a recurring advisory (2nd occurrence) in v4.9 LL-RP-v4.9-02 and is now STALE. The 7 missing entries are fully specified in AUD-2026-06-02 §5 AUD-001 PATCH 1.

**Scope**
- Append 7 rows to prompt_change_log.md for: delivery_verification_prompt.md v2.7→v2.8, post_ship_closure.md v2.11→v2.12, execution_prompt.md v3.33→v3.34, release_planning_prompt.md v2.32→v2.33, roadmap_prompt.md v6.6→v6.7, roadmap_prompt.md v6.7→v6.8, execution_prompt.md v3.34→v3.35
- All change descriptions available verbatim in audit_report_AUD-2026-06-02.md §5 AUD-001 PATCH 1

**Acceptance Criteria**
- All 7 entries present in prompt_change_log.md in reverse-chronological order (newest first)
- Each entry has correct Date, Prompt path, Version transition, Change summary, Authority
- No other prompt_change_log gaps exist for any engine version changes in cycles 31–35

---


### BLG-GOV-80 — Add governance file edit check to execution_prompt.md STEP 8 commit ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P2 (Medium)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** AUD-2026-06-02 (AUD-2026-06-02-003, root cause of BLG-GOV-79) — 2026-06-02
**Effort:** M (~1–2 days)
**Provisional-Target:** v5.0
**Depends on:** BLG-GOV-79 (prompt_change_log completion — apply before or together)

**Problem**
The roadmap engine (STEP 12) and amendment engine (STEP 9) have structural governance file edit checks that enforce prompt_change_log.md entries when governance files are modified. The execution engine lacks an equivalent check at its STEP 8 commit, creating a structural gap. Since execution stories frequently apply OA-clearance patches to governance prompts, this silent bypass was the confirmed root cause of all 7 missing prompt_change_log.md entries (BLG-GOV-79).

**Scope**
- Add governance file edit check to execution_prompt.md STEP 8 before commit: scan git diff for modified files in `claude/system/`, `claude/charter/`, `claude/agents/`; for each modified governance file, verify prompt_change_log.md entry exists; append if missing before proceeding
- Bump execution_prompt.md version (v3.35→v3.36)
- Update OPERATIONAL_GUIDE.md §8 source prompt header + §14 Execution Engine Source + §14 changelog (v4.26→v4.27)
- Append entry to prompt_change_log.md for this change
- Full PATCH block in audit_report_AUD-2026-06-02.md §5 AUD-003

**Acceptance Criteria**
- execution_prompt.md v3.36 contains governance file edit check at STEP 8 (before commit step)
- Check is STRUCTURAL: scans git diff --name-only for claude/system/, claude/charter/, claude/agents/ paths; appends missing prompt_change_log rows inline
- OPERATIONAL_GUIDE §8 source header, §14 Execution Engine Source, and §14 changelog updated in same commit
- prompt_change_log.md entry for execution_prompt.md v3.35→v3.36 present
- Head of Specs Team sign-off

---


### BLG-GOV-81 — Fix 5 non-standard agent file headers ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** Head of Specs Team
**Source:** AUD-2026-06-02 (AUD-2026-06-02-004; 2nd carry from AUD-2026-05-30-005) — 2026-06-02
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.0

**Problem**
5 agent files use setext-style headings (`====` underline) with a trailing backslash on the Role field, deviating from the `# Name` / `**Role:** Name` (no backslash) standard used by all other 18 agent files. This has been open since AUD-2026-05-30-005 (first audit carry) and is now in its second consecutive carry. Affected files: ai_compliance_governance_officer.md, cybersecurity_trust_lead.md, director_of_hr.md, financial_reporting_records_owner.md, finops_resource_architect.md.

**Scope**
- For each of the 5 files: replace setext heading (`Name\n====`) with standard `# Name` ATX heading
- Remove trailing backslash from `**Role:** Name\` line → `**Role:** Name`
- Full PATCH blocks in audit_report_AUD-2026-06-02.md §5 AUD-004 (5 PATCH blocks, one per file)

**Acceptance Criteria**
- All 5 files use `# Name` ATX heading format (no setext `====`)
- All 5 files have `**Role:** Name` with no trailing backslash
- Format is consistent with the other 18 agent files in claude/agents/
- Head of Specs Team sign-off

---


### BLG-GOV-82 — Strengthen post-ship audit advisory to prevent multi-cycle skips ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P2 (Medium)
**Type:** Governance / Process
**Owner:** Head of Specs Team; PMO Lead
**Source:** AUD-2026-06-02 (AUD-2026-06-02-005 — audit skipped 2 cycles, due at cycle 33, run at cycle 35) — 2026-06-02
**Effort:** M (~1–2 days)
**Provisional-Target:** v5.0

**Problem**
The post-ship STEP 0 audit advisory fires when `completed_cycle_count % 3 == 0`, but there is no re-fire mechanism if the advisory is not acted upon. In cycle 33 (v4.7), the audit due advisory was not recorded in the post-ship closure, allowing the audit to be skipped until cycle 35 — 2 cycles late. Additionally, the OPERATIONAL_GUIDE STEP 0 post-ship advisory does not track how many cycles ago the last audit ran, so the system cannot distinguish "due" from "overdue."

**Scope**
- Update post_ship_closure.md STEP 0 audit cadence check: in addition to `completed_cycle_count % 3 == 0`, add cumulative overdue check — if the delta between current completed_cycle_count and the count at last audit >= 4, fire AUDIT DUE regardless of modulo
- Add `last_audit_cycle_count` field to `.claude_current_state.json` schema: post-ship records the cycle count at which the last audit ran (for delta tracking)
- Update lifecycle_schema.json if needed for the new state field
- Bump post_ship_closure.md version + OPERATIONAL_GUIDE §10 header + §14 Post-Ship Closure Engine + §14 changelog
- Append entry to prompt_change_log.md
- Full PATCH in audit_report_AUD-2026-06-02.md §5 AUD-005

**Acceptance Criteria**
- post_ship_closure.md STEP 0 fires AUDIT DUE if `completed_cycle_count % 3 == 0` OR `(completed_cycle_count - last_audit_cycle_count) >= 4`
- `.claude_current_state.json` has `last_audit_cycle_count` field set at each post-ship closure when audit runs
- Post-ship closure Outstanding Actions records AUDIT DUE with Owner and target timeline when advisory fires
- OPERATIONAL_GUIDE §10 source header + §14 Post-Ship Closure Engine + changelog updated in same commit
- prompt_change_log.md entry present

---


### BLG-GOV-83 — Document PO acceptance requires GitHub review approval (not PR comment) ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P3 (Low)
**Type:** Governance / Process
**Owner:** PMO Lead
**Source:** AUD-2026-06-02 (AUD-2026-06-02-006; v4.9 D-3 first occurrence — PO commented but PR remained BLOCKED) — 2026-06-02
**Effort:** XS (<1h)
**Provisional-Target:** v5.0

**Problem**
In v4.9, the Product Owner accepted PR #645 via a PR comment but the branch remained BLOCKED requiring human intervention because GitHub branch protection requires a formal "Approve" review action (not just a comment). This distinction is not documented anywhere — not in the PR template, team guide, or OPERATIONAL_GUIDE.

**Scope**
- Add a callout note to `.github/pull_request_template.md` in the QA Evidence or PO acceptance section clarifying: PO acceptance must be submitted as a GitHub Approve review action, not a PR comment
- PATCH block in audit_report_AUD-2026-06-02.md §5 AUD-006

**Acceptance Criteria**
- `.github/pull_request_template.md` contains explicit note that PO acceptance = GitHub "Approve review" action
- Note is visible in the PR template before any reviewer opens the PR
- Director of Quality sign-off (PR process governance)

---


### BLG-GOV-86 — SI-05 Phase 1 Telegram message format specification ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P2 (Medium)
**Type:** Governance / Spec Pre-work
**Owner:** Head of Specs Team; Base44 Frontend; Product Owner
**Source:** IDEA-base44-frontend-20260601-01 — Promoted-Backlog cycle 2026-06-02__scheduled (DL-037; STEP 5 advance; Challenger Clearance)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.0
**Depends on:** BLG-FE-60 (notification channel decision — must confirm Telegram before specifying format)

**Problem**
SI-05 Phase 1 will deliver the weekly strategy integrity digest via Telegram (assuming BLG-FE-60 channel assessment confirms Telegram). Telegram imposes character limits, formatting constraints (Markdown subset), and no interactive elements. Without a pre-specified message format, implementation must decide format details concurrently with coding — increasing rework risk on an immutable notification channel.

**Scope**
- Message format specification document covering:
  - Character limit compliance strategy
  - Section structure: opening summary, Red Flag count (SI-03 data), compliance score trend (SI-01 data), key rule breach (if any), weekly recommendation to review
  - Data field definitions: which fields from SI-01 and SI-03 endpoints populate each section
  - Frequency: weekly (consistent with v2.4 weekly digest cadence)
  - Failure modes: what the message says when data is unavailable
- Review by Product Owner and Base44 Frontend before sprint planning seals

**Acceptance Criteria**
- Message format specification document produced and filed
- All data fields mapped to SI-01/SI-03 endpoint responses
- Telegram character limits verified not exceeded
- Product Owner and Head of Specs Team sign-off
- Gate condition (BLG-FE-60 channel confirmed as Telegram) verified before authoring

---


### BLG-GOV-87 — SI-02 frontend re-entry trigger criteria definition ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P2 (Medium)
**Type:** Governance / Process Definition
**Owner:** PMO Lead; Product Owner
**Source:** IDEA-product-owner-20260601-02 — Promoted-Backlog cycle 2026-06-02__scheduled (DL-037; STEP 5 advance; Challenger Clearance)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.0

**Problem**
SI-02 frontend has been deferred 8 consecutive sprint planning cycles (v3.9–v4.9). The stated gate is "≥20 closed trades with linked trade_plans" but this is not formally documented anywhere as a hard gate with an explicit PMO Lead verification step. Without a formal, written, PMO-Lead-checked trigger, SI-02 frontend risks being informally deferred again when the trade count approaches 20. A documented re-entry trigger prevents this.

**Scope**
- Formal re-entry criteria document: defines the exact conditions for re-entering SI-02 frontend into sprint planning:
  - Hard gate: ≥20 closed trades with linked trade_plans confirmed by PMO Lead via production database query
  - Soft advisory: drift score data accumulation period ≥ 3 months (qualitative signal assessment)
  - Formal trigger: PMO Lead runs re-entry check at each release planning kickoff starting 2026-09-01
- Document filed in `claude/roadmap/` or `docs/product/decisions/`
- Re-entry check step added to release planning checklist (as advisory item for PMO Lead)

**Acceptance Criteria**
- Re-entry criteria document produced with hard gate and soft advisory defined
- PMO Lead acknowledges ownership of the periodic check
- Product Owner confirms criteria are the intended re-entry conditions
- Check cadence starts at v5.1 release planning (2026-09 earliest)

---


### BLG-GOV-88 — SI-04 formal binding conditions decisions document ✅ COMPLETE v5.0 (2026-06-03)
**Priority:** P2 (Medium)
**Type:** Governance / §13 Compliance Record
**Owner:** Strategy Rules & System Intent Owner; Head of Specs Team
**Source:** IDEA-strategy-owner-20260601-01 — Promoted-Backlog cycle 2026-06-02__scheduled (DL-037; STEP 5 advance; Challenger Clearance)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.0

**Problem**
SI-04 §13 pre-assessment was completed in v4.7 ST-01 (si04_section13_preassessment.md — PASS; 6 binding conditions). The API contract was pre-authored in v4.8 (BLG-SPEC-43). However, a formal decisions document equivalent to the SI-01 record (decisions--2026-05-19__release-v3.8--SI-01-section13-review.md) does not yet exist for SI-04. This leaves the 6 binding conditions in an ad-hoc pre-assessment file rather than a proper Class 5 decisions record that sprint planning can reference.

**Scope**
- Author a formal SI-04 §13 compliance decisions document in `docs/product/decisions/`
- Content: reproduce the 6 binding conditions from si04_section13_preassessment.md; add formal sign-off block; reference BLG-SPEC-43 contract
- Document class: Planning Document or Decisions Record per document_lifecycle_guide.md
- Reviewed and signed off by Strategy Rules & System Intent Owner

**Acceptance Criteria**
- SI-04 §13 decisions document created in `docs/product/decisions/`
- All 6 binding conditions from si04_section13_preassessment.md reproduced
- Strategy Rules & System Intent Owner formal sign-off recorded
- BLG-SPEC-43 (API contract) cross-referenced

---


### BLG-GOV-89 — Staged verification sprint protocol document
**Priority:** P3 (Low)
**Type:** Governance / Process Documentation
**Owner:** Director of Quality; PMO Lead
**Source:** IDEA-director-of-quality-20260601-02 — Promoted-Backlog rebalance 2026-06-03__scheduled (DL-038)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.1 or v5.2

**Gate criteria:** None. Pattern validated across v4.7 (first use) and v5.0 (second use). Actionable now.

**Problem**
The staged verifications sprint pattern (batch-closing staging-only ACs from prior releases in a dedicated sprint) was validated at v4.7 and confirmed at v5.0. No formal protocol document exists. Without documentation, future verification-heavy releases cannot reference a standard approach, increasing coordination overhead.

**Scope**
- Document the staged verifications sprint pattern: trigger conditions, how to batch staging ACs, evidence requirements, sprint planning notes
- File in docs/operations/ or docs/governance/
- Review by Director of Quality and PMO Lead

**Acceptance Criteria**
- Protocol document produced and filed
- Covers: trigger conditions, batching approach, evidence format, sprint sizing note
- Reviewed by Director of Quality and PMO Lead

✅ COMPLETE — 2026-06-04 — cycle 2026-06-21__release-v5.1 (ST-06, EPIC-03; docs/operations/staged_verification_sprint_protocol.md v1.0 produced; Director of Quality + PMO Lead sign-off)

---


### BLG-GOV-92 — SI-05 Phase 2 activation criteria definition
**Priority:** P2 (Medium)
**Type:** Governance / Feature Scope Definition
**Status:** COMPLETE — v5.4 ST-04; criteria doc filed at docs/governance/si05_phase2_activation_criteria.md 2026-06-10
**Owner:** Product Owner; PMO Lead
**Source:** IDEA-product-owner-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5 day)
**Provisional-Target:** Before SI-02 frontend sprint planning (~Nov 2026)
**Displacement:** BLG-GOV-27 (cross-arc dependency map, P3, gate-conditional) deprioritised.

**Problem**
SI-05 Phase 2 (integrating SI-02 drift signals into the weekly digest) has no documented activation criteria. When SI-02 frontend activates (~Nov 2026), the decision to proceed with Phase 2 will be made without empirical reference unless criteria are defined now. Without criteria, Phase 2 may be activated prematurely (before SI-02 data quality is established) or unnecessarily delayed.

**Scope**
- Define SI-05 Phase 2 activation criteria: minimum conditions required before Phase 2 sprint planning seals
  - Hard gate: SI-02 frontend shipped and in active use (drift scores visible to user)
  - Quality gate: SI-02 drift scores confirmed as meaningful (not dominated by statistical noise at current trade volume)
  - Phase 1 effectiveness gate: PO confirms SI-05 Phase 1 is being actively used (per BLG-GOV-96 effectiveness measurement)
  - Optional: minimum weeks of SI-02 drift data accumulated
- Document criteria in a decisions record or project planning note
- PMO Lead to include criteria check at SI-02 frontend release planning kickoff

**Acceptance Criteria**
- Phase 2 activation criteria document produced and reviewed by Product Owner
- Criteria cover: SI-02 frontend shipping, data quality threshold, Phase 1 effectiveness confirmation
- PMO Lead acknowledges responsibility for criteria check at relevant release planning

---


### BLG-GOV-93 — OA-01/02 pre-sprint-planning resolution check procedure
**Priority:** P1 (High)
**Type:** Governance / Process Improvement
**Owner:** PMO Lead; Head of Specs Team
**Source:** IDEA-pmo-lead-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** XS (~1–2 hours)
**Provisional-Target:** v5.2 (must complete before v5.2 sprint planning seals)
**Displacement:** BLG-GOV-26 (Arc velocity tracking dashboard, P3, gate-conditional) deprioritised.

**Problem**
OA-01 (release_planning_prompt.md §-1.2 patch) and OA-02 (execution_prompt.md §3.1.A patch) are due before v5.2 sprint planning seals. The OVERDUE patch pattern (F-01, 2026-06-03 lessons learnt: backlog_management_prompt.md patch missed 2 cycles) shows that deferred patches with stated deadline dates can be missed without an explicit enforcement mechanism. Without a defined check step, OA-01/02 risk becoming OVERDUE at v5.2 STEP -1.5.

**Scope**
- Define a pre-sprint-planning resolution check: at v5.2 release planning STEP 0, PMO Lead explicitly checks OA-01 and OA-02 resolution status before the run proceeds
- Add this check to the v5.2 release planning run manifest as a hard verification step
- If OA-01/02 are unresolved at v5.2 release planning: escalate to Head of Specs Team immediately (OVERDUE classification applies at 2nd consecutive carry)
- Apply the patches for OA-01/02 now if this item is sprint-planned in v5.2

**Acceptance Criteria**
- OA-01 and OA-02 explicitly resolved before v5.2 sprint planning seals
- Resolution evidence: release_planning_prompt.md §-1.2 updated + prompt_change_log.md entry (OA-01); execution_prompt.md §3.1.A updated + prompt_change_log.md entry (OA-02)
- PMO Lead confirms OA resolution in v5.2 run manifest
- Head of Specs Team sign-off on each prompt patch

---


### BLG-GOV-94 — SI-05 Phase 1 delivery verification protocol
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-14, EPIC-04; docs/qa/si05_delivery_verification_protocol.md created; covers AC-09 Telegram + AC-01 compliance_summary; cross-referenced with SI-05 acceptance test protocol; Director of Quality sign-off)
**Priority:** P2 (Medium)
**Type:** Governance / QA Planning
**Owner:** Director of Quality; QA & Testing Owner
**Source:** IDEA-director-of-quality-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5 day)
**Provisional-Target:** Before staged verification sprint
**Displacement:** BLG-QA-21 (Arc 2 E2E QA protocol, P3, gate-conditional) deprioritised.

**Problem**
v5.1 post-ship deferred 2 staging-only ACs to a staged verification sprint: ST-01 AC-09 (Telegram digest delivery confirmed on staging) and ST-05 AC-01 (compliance_summary live data confirmed). Without a formal verification protocol, the staged sprint lacks: who is responsible for each check, what constitutes evidence of completion, and when sign-off should be recorded.

**Scope**
- Produce delivery verification protocol for SI-05 Phase 1 staged ACs:
  - AC-09 (ST-01): steps to trigger the digest on staging, confirm Telegram delivery, record delivery timestamp and message ID as evidence
  - AC-01 (ST-05): steps to generate a monthly P&L report on staging and confirm compliance_summary fields are populated from live data
  - Sign-off format: which role signs off, what evidence is attached, where the sign-off is recorded (QA evidence file)
- Reference BLG-GOV-89 staged verification sprint protocol for format guidance
- Reviewed by Director of Quality; includes BLG-QA-47 (acceptance test protocol) as a companion input

**Acceptance Criteria**
- Verification protocol document produced for both deferred ACs
- Each AC has explicit: trigger steps, expected evidence, sign-off authority
- Director of Quality sign-off on the protocol
- Protocol ready before staged verification sprint is scheduled

---


### BLG-GOV-96 — SI-05 Phase 1 effectiveness measurement criteria
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-16, EPIC-04; 3 effectiveness criteria defined; 30-day review scheduled 2026-07-04; criteria documented at claude/cycles/2026-06-08__release-v5.2/si05_effectiveness_criteria.md; Product Owner sign-off)
**Priority:** P2 (Medium)
**Type:** Governance / Product Accountability
**Owner:** Product Owner; PMO Lead
**Source:** IDEA-challenger-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.2
**Displacement:** BLG-FEAT-44 (Arc5ComplianceSection advisory at low trade volume, P3, gate-conditional) deprioritised.

**Problem**
SI-05 Phase 1 (weekly Telegram digest, shipped v5.1) has no defined effectiveness criteria. The decision to proceed to Phase 2 (SI-02 drift signal integration) should be evidence-based. Without defined criteria, Phase 2 will be activated based on subjective judgment rather than demonstrated Phase 1 value.

**Scope**
- Define SI-05 Phase 1 effectiveness criteria (qualitative, since no usage analytics for single-user system):
  - Frequency criteria: PO reviews at least N of the last M digests without skipping (suggested: 3 of last 4)
  - Action criteria: at least 1 digest-triggered app action per month (PO logs any "checked app after digest" event)
  - Content usefulness: PO self-assessment at 30-day mark (2026-07-04): was the digest content actionable?
- Record criteria in a governance note (not a formal document) for review at v5.2 or when Phase 2 is proposed
- Review at 30-day post-ship mark (2026-07-04) and record PO assessment

**Acceptance Criteria**
- Effectiveness criteria defined and acknowledged by Product Owner
- 30-day review scheduled (2026-07-04)
- 30-day review findings recorded when due
- PMO Lead confirms effectiveness criteria check is included in Phase 2 activation criteria (BLG-GOV-92)

---


### BLG-GOV-97 — Claude API model deprecation compliance check
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-09, EPIC-03; PASS — claude-haiku-4-5-20251001 not deprecated; check documented at docs/governance/ai_model_deprecation_check_v52.md; next review 2026-09-08; AI Compliance & Governance Officer sign-off)
**Priority:** P1 (High)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance & Governance Officer; Head of Engineering
**Source:** IDEA-ai-compliance-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** XS (~30 minutes)
**Provisional-Target:** v5.2
**Displacement:** BLG-GOV-84 (Arc 6 gate revision assessment, P3, gate-conditional) deprioritised.

**Problem**
BLG-GOV-64 pins the Claude API model to a specific version (claude-3-5-sonnet-20241022 or equivalent at time of pinning). Anthropic publishes model deprecation notices on their platform. If the pinned model is deprecated and the system is not updated, API calls will fail in production, breaking both POST /trade-plans/{plan_id}/generate-thesis and POST /ai/check-daily-cost. BLG-GOV-90 defines a quarterly deprecation check procedure but has not been executed yet.

**Scope**
- Check Anthropic model lifecycle page for the currently pinned model's deprecation status
- Confirm the model pinned in BLG-GOV-64 (backend/services/ai_service.py or equivalent) is not deprecated
- If not deprecated: record check date and next review date in a governance note
- If deprecated: file P0 sprint story immediately to update the pinned model per BLG-GOV-90 trigger procedure

**Acceptance Criteria**
- Anthropic model lifecycle checked for the pinned model
- Check result recorded with timestamp (not deprecated: record + schedule next check; deprecated: P0 filed)
- AI Compliance & Governance Officer sign-off on check

---


### BLG-GOV-98 — Telegram bot token minimal-permission security review
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-10, EPIC-03; PASS with recommendation — send-only confirmed; BotFather manual check recommended as advisory; security_register.md updated; Cybersecurity & Trust Lead sign-off)
**Priority:** P2 (Medium)
**Type:** Governance / Security
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Source:** IDEA-cybersecurity-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.2
**Displacement:** BLG-OPS-41 (red flag events table archiving strategy, P2, gate-conditional) deprioritised.

**Problem**
SI-05 Phase 1 introduced a Telegram bot token used to send weekly digest messages. Telegram Bot API tokens can have various permission scopes. A send-only bot token (permission to send messages to a pre-authorised chat) should be minimal — it should not be able to read messages from users or access chats beyond the designated digest channel. No security review of the token's permission scope has been documented.

**Scope**
- Verify the Telegram bot token in use is configured with minimal permissions: send-only to the designated chat
- Confirm the bot cannot read incoming messages, list chats, or send to arbitrary chats
- Document review findings: what permissions were verified, how verified (Telegram BotFather settings check)
- If overly permissive: request token rotation with appropriate scope restriction
- Record review in security_register.md per existing review pattern

**Acceptance Criteria**
- Telegram bot token permissions verified as minimal (send-only to designated chat)
- Review documented in security_register.md
- Cybersecurity & Trust Lead sign-off

---


### BLG-GOV-99 — SI-05 digest endpoint authentication review
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-11, EPIC-03; GAP_FOUND — POST /digest/si05/send unauthenticated; BLG-BE-35 P2 filed for future sprint; security_register.md updated (Review 003); does not block EPIC-03; Cybersecurity & Trust Lead sign-off)
**Priority:** P2 (Medium)
**Type:** Governance / Security
**Owner:** Cybersecurity & Trust Lead; Head of Engineering
**Source:** IDEA-cybersecurity-20260607-02 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.2
**Displacement:** BLG-OPS-18 (data pipeline cost baseline, P3, gate-conditional) deprioritised.

**Problem**
POST /digest/si05/send is a new endpoint that triggers external Telegram API calls. The authentication requirements for this endpoint have not been formally reviewed: can it be called without authentication? Should it require API key authentication (like other endpoints per BLG-SEC-01/v2.2)? An unauthenticated endpoint that triggers external API calls is a potential abuse vector (sending arbitrary digests, incurring Telegram API usage).

**Scope**
- Review POST /digest/si05/send authentication: does it require API key auth per the existing authentication pattern?
- If unauthenticated: determine appropriate protection (API key, rate limiting, or scope restriction to internal calls only)
- If already authenticated: confirm auth is enforced and document
- File P2 fix if authentication gap found; record in security_register.md

**Acceptance Criteria**
- Authentication status of POST /digest/si05/send documented
- If gap found: P2 fix filed (or fixed inline); Cybersecurity & Trust Lead sign-off
- Security_register.md updated with review outcome

---


### BLG-GOV-100 — Backend endpoint documentation coverage audit post-v5.1
✅ COMPLETE — 2026-06-08 — cycle 2026-06-08__release-v5.2 (ST-12, EPIC-03; 50 routes enumerated; 6 contract gaps found: BLG-SPEC-49/50/51/52 filed; audit documented at docs/ops/endpoint_coverage_audit_v52.md; Head of Engineering sign-off)
**Priority:** P2 (Medium)
**Type:** Governance / Process Compliance
**Owner:** Head of Engineering; API Contracts & Documentation Owner
**Source:** IDEA-head-of-engineering-20260607-01 — Promoted-Backlog rebalance 2026-06-07__scheduled (DL-039)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.2
**Displacement:** BLG-OPS-19 (external API cost attribution, P3, gate-conditional) deprioritised.

**Problem**
CLAUDE.md §2 requires every new backend route to have: (a) corresponding entry in openapi.yaml, (b) corresponding entry in backend/routers/test.py, and (c) corresponding API contract document in docs/specs/api_contracts/. After v5.1 shipped POST /digest/si05/send, it's unclear whether all three requirements were met. A systematic audit after each release prevents cumulative spec debt from building undetected.

**Scope**
- Enumerate all routes in backend/routers/ (all @router.get/post/put/delete decorators)
- For each route: check (a) openapi.yaml entry exists, (b) test.py entry exists, (c) API contract document exists
- Document any gaps found; file BLG-SPEC items for each contract gap
- This item covers v5.1 deliverables; routine coverage audits should be added to post-ship closure checklist going forward

**Acceptance Criteria**
- All backend/routers/ routes enumerated and cross-checked against openapi.yaml, test.py, and docs/specs/api_contracts/
- Coverage gaps documented; BLG-SPEC items filed for any contract gaps found
- Head of Engineering and API Contracts & Documentation Owner sign-off

---


### BLG-GOV-104 — strategy_rules.md §11 parameter validation (first annual instance)
**Priority:** P2 (Medium)
**Type:** Governance / Strategy
**Owner:** Strategy Rules & System Intent Owner; Product Owner
**Source:** IDEA-strategy-owner-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** M (~1–2 days)
**Provisional-Target:** v5.3
**Displacement:** BLG-GOV-101 (governance complexity assessment, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-17, EPIC-03; docs/governance/strategy_parameter_validation_v53.md produced; ATR multiplier, regime gate, position sizing validated against trade data; Strategy Rules & System Intent Owner + Product Owner sign-off)

**Problem**
strategy_rules.md §11 defines ATR multiplier, regime gate parameters, and position sizing rules. These parameters have never been formally validated against actual trade outcomes since they were set. BLG-GOV-95 (annual parameter review schedule, v5.2) established that validation should happen annually; this item is the first instance of that schedule.

**Scope**
- Pull all closed trades from production database; compute per-parameter outcomes
- For ATR multiplier: was the initial stop placed correctly against ATR? Did trailing stop advances follow the multiplier?
- For regime gate: how many entries were blocked by the regime gate? Of those that were allowed, what was the pass rate?
- For position sizing: is the documented formula correctly implemented in the UI?
- Produce a parameter validation document; recommend any changes (or confirm no changes needed)

**Acceptance Criteria**
- Parameter validation document produced for §11 parameters
- Each parameter validated against actual trade data (or documented as "insufficient data if <20 trades")
- Strategy Rules & System Intent Owner sign-off; Product Owner ratifies any recommended parameter changes

---


### BLG-GOV-106 — PT-04 trade count gate re-verification
**Priority:** P1 (High)
**Type:** Governance / Gate Tracking
**Owner:** PMO Lead; Product Owner
**Source:** IDEA-challenger-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5 hr)
**Provisional-Target:** Before v5.3 sprint planning seals
**Displacement:** BLG-GOV-101 (governance complexity assessment, P3) deprioritised.

✅ COMPLETE — 2026-06-16 — cycle 2026-06-16__release-v5.6 (ST-08, EPIC-03, PR #764; 13 closed trades confirmed by PO — gate NOT MET (need 20); roadmap + BLG-FEAT-25 updated; trajectory accelerating — re-verify when PO confirms 20+)

**Problem**
PT-04 gate requires 20+ closed trades (trades with pnl IS NOT NULL in trade_history). Last formal count: 6 trades at v4.6 audit (2026-05-31). The count has never been updated. If the gate has cleared, PT-04 should enter v5.3 sprint planning. If not, the gate status record should be updated with the current count.

**Scope**
- Query: `SELECT COUNT(*) FROM trade_history WHERE pnl IS NOT NULL`
- Compare against 20-trade gate threshold
- Update PT-04 gate status in current_roadmap.md and backlog.md (BLG-FEAT-25)
- If gate cleared: add PT-04 to v5.3 candidate scope

**Acceptance Criteria**
- Current closed trade count queried and recorded
- PT-04 gate status updated in current_roadmap.md and BLG-FEAT-25
- PMO Lead and Product Owner sign-off on gate status

---


### BLG-GOV-107 — SI-02 frontend activation criteria precision
**Priority:** P2 (Medium)
**Type:** Governance / Gate Tracking
**Owner:** PMO Lead; Product Owner; Head of Engineering
**Source:** IDEA-challenger-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.3
**Displacement:** BLG-GOV-101 (governance complexity assessment, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-13, EPIC-03; current_roadmap.md SI-02 entry updated with 3 precise, measurable gate conditions; PMO Lead + Product Owner sign-off)

**Problem**
SI-02 frontend activation is recorded as "~Nov 2026" — a date estimate rather than a measurable gate. Sprint planning for SI-02 frontend cannot be triggered reliably against a vague date. Precise, measurable criteria are needed.

**Scope**
- Define 2-3 specific, checkable conditions that unblock SI-02 frontend sprint planning, e.g.:
  1. 20+ closed trades with linked trade_plans (PT-04 gate condition — SI-02 drift score data quality gate)
  2. SI-02 backend API performance confirmed stable (GET /analytics/behavioural-drift p99 < 2s)
  3. SI-02 drift scores confirmed meaningful (not dominated by noise at current trade volume — per BLG-GOV-92 Phase 2 activation criteria)
- Update SI-02 status in current_roadmap.md with precise gate conditions
- PMO Lead to check these conditions at each release planning kickoff

**Acceptance Criteria**
- SI-02 frontend gate conditions defined (2-3 specific, checkable criteria)
- current_roadmap.md SI-02 entry updated with precise conditions replacing "~Nov 2026"
- PMO Lead and Product Owner sign-off

---


### BLG-GOV-108 — AI model pin update policy (BLG-GOV-64 gap)
**Priority:** P2 (Medium)
**Type:** Governance / AI Compliance
**Owner:** AI Compliance Governance Officer; Head of Engineering
**Source:** IDEA-ai-compliance-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.3
**Displacement:** BLG-GOV-101 (governance complexity assessment, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-14, EPIC-03; docs/governance/ai_model_version_pinning_policy.md produced; policy covers trigger, process, sign-offs, 30-day deprecation response timeline; AI Compliance Governance Officer + Head of Engineering sign-off)

**Problem**
BLG-GOV-64 (model pinning policy, v4.2) defines that the model must be pinned explicitly, but does not specify when or how to update the pin. claude-haiku-4-5 was pinned at v4.2 (2026-05-28). As new Claude versions release, there is no governed process for evaluating and performing pin updates.

**Scope**
- Add to BLG-GOV-64 or create a companion document: "AI model pin update policy"
  - Update trigger: when Anthropic releases a new Claude model or deprecates the current pinned model
  - Update process: review release notes for breaking changes, run test suite against new model, document cost/quality trade-off
  - Required sign-offs: AI Compliance Governance Officer + Head of Engineering
  - Timeline: updates must complete within 30 days of deprecation notice

**Acceptance Criteria**
- Model pin update policy documented (in BLG-GOV-64 update or companion doc)
- Policy covers: trigger, process, sign-offs, timeline for deprecation response
- AI Compliance Governance Officer and Head of Engineering sign-off

---


### BLG-GOV-109 — AI audit log retention policy
**Priority:** P2 (Medium)
**Type:** Governance / Data Compliance
**Owner:** AI Compliance Governance Officer; Infrastructure & Operations Owner
**Source:** IDEA-ai-compliance-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.3
**Displacement:** BLG-OPS-13 (performance baseline gaps, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-15, EPIC-03; docs/governance/ai_audit_log_retention_policy.md produced; 12-month retention period defined; cleanup mechanism documented; AI Compliance Governance Officer + Infrastructure & Operations Owner sign-off)

**Problem**
claude_audit_log entries have been accumulating since v3.8 with no defined retention period. Without a retention policy: (a) storage costs grow indefinitely, (b) it is unclear which log entries are reliable for compliance purposes vs stale.

**Scope**
- Define retention period for claude_audit_log entries: recommended 12 months (or align with Supabase retention policy from BLG-OPS-53)
- Implement: add a scheduled cleanup job or Supabase row-level TTL for entries older than the retention period
- Document in the AI compliance governance records (docs/compliance/ or existing AI audit log spec)

**Acceptance Criteria**
- Retention policy defined and documented (period, rationale)
- Cleanup mechanism implemented (scheduled job or TTL)
- AI Compliance Governance Officer and Infrastructure & Operations Owner sign-off

---


### BLG-GOV-110 — Arc 4 trade_plan data completeness audit
**Priority:** P2 (Medium)
**Type:** Governance / Data Readiness
**Owner:** Data Model & Domain Schema Owner; Product Owner
**Source:** IDEA-data-model-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** v5.3 or before Arc 4 sprint planning (PO-02 gate ~Oct 2026)
**Displacement:** BLG-GOV-101 (governance complexity assessment, P3) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-16, EPIC-03; docs/governance/arc4_trade_plan_data_completeness_audit.md produced; per-field null% computed; Arc 4 data dependency risk assessed; Data Model & Domain Schema Owner + Product Owner sign-off)

**Problem**
Trade plans have been active since v3.1 (3+ months). However, which optional fields (entry_rationale, confirmation_criteria, r_target, setup_type, pre_entry_validation_snapshot) are being consistently populated is unknown. Arc 4 analytics (PO-02 journal pattern recognition, PO-03 behavioural error taxonomy) depend on this data.

**Scope**
- Query trade_plans table: for each optional field, compute null% and non-null% across all records
- Identify fields with > 50% null rate as "data gaps" — these are risky dependencies for Arc 4
- Produce a data completeness report; flag any Arc 4 features that depend on gapped fields
- If gaps are critical: file backlog items for UI/UX improvements to encourage field completion

**Acceptance Criteria**
- Data completeness report produced: per-field null% for all trade_plan optional fields
- Arc 4 data dependency risk assessment included
- Data Model & Domain Schema Owner and Product Owner sign-off

---


### BLG-GOV-111 — v5.3 design gate pre-assessment
**Priority:** P2 (Medium)
**Type:** Governance / Release Planning
**Owner:** Head of UX & Design; Product Owner
**Source:** IDEA-head-of-ux-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5 hr)
**Provisional-Target:** Before plan release v5.3
**Displacement:** BLG-GOV-101 (governance complexity assessment, P3) deprioritised.

**Problem**
CLAUDE.md §1 requires a design gate assessment before sprint planning for any release with new UI/UX components. v5.3 candidate scope (governance debt, spec gaps, security, ops) appears to be exclusively backend/governance with no new UI components — but this should be formally assessed rather than assumed.

**Scope**
- Review v5.3 candidate scope from current_roadmap.md RA:v5.3 section
- For each candidate item: does it introduce new UI or UX components? (Yes/No)
- If all items are No: record "Design gate not required" with itemised justification; seal in run_manifest at plan release v5.3
- If any item is Yes: normal design gate process applies

**Acceptance Criteria**
- Design gate pre-assessment document produced (or incorporated into plan release v5.3 run manifest)
- Each v5.3 candidate item assessed for UI/UX dependency
- Head of UX & Design and Product Owner sign-off

---


### BLG-GOV-113 — SI-05 Phase 1 effectiveness review protocol (gate-conditional)
**Priority:** P1 (High)
**Type:** Governance / QA Planning
**Owner:** Director of Quality; Product Owner
**Source:** IDEA-director-of-quality-20260608-01 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5 day)
**Provisional-Target:** Before 2026-07-04 effectiveness review
**Displacement:** BLG-QA-34 (SI-02 test planning, gate-conditional) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-23, EPIC-03; docs/governance/si05_effectiveness_review_protocol.md produced; participants, evidence sources, output format, decision authority defined; Director of Quality + Product Owner sign-off; completed before 2026-07-01 gate)

**Gate criteria:** Must complete before 2026-07-04. BLG-GOV-96 (effectiveness criteria) defines WHAT to measure; this item defines HOW to conduct the review.

**Problem**
BLG-GOV-96 (SI-05 effectiveness measurement criteria, v5.2) defines what to measure at the 2026-07-04 review but does not define the review process: who participates, what evidence is examined, what format the output takes, and what decision authority exists. Without a protocol, the review may be inconsistent.

**Scope**
- Define the SI-05 Phase 1 effectiveness review protocol:
  - Participants: Product Owner + Director of Quality (minimum)
  - Evidence sources: si05_digest_log, BLG-GOV-96 criteria, user feedback (if any), Red Flag Journal view counts post-delivery
  - Output format: a one-page effectiveness review report
  - Decision authority: Product Owner decides whether to proceed with Phase 2 or extend Phase 1 observation
- Protocol must complete by 2026-07-01 (3 days before first review date)

**Acceptance Criteria**
- SI-05 effectiveness review protocol document produced
- Protocol specifies: participants, evidence sources, output format, decision authority
- Must complete by 2026-07-01
- Director of Quality and Product Owner sign-off

---


### BLG-GOV-114 — si05_digest_log schema validation for effectiveness review (gate-conditional)
**Priority:** P1 (High)
**Type:** Governance / Data
**Owner:** Data Model & Domain Schema Owner; Infrastructure & Operations Owner
**Source:** IDEA-data-model-20260608-02 — Promoted-Backlog rebalance 2026-06-08__scheduled (DL-040)
**Effort:** S (~0.5 hr)
**Provisional-Target:** Before 2026-07-04 effectiveness review
**Displacement:** BLG-GOV-90 (Claude model deprecation monitoring, gate-conditional) deprioritised.

✅ COMPLETE — 2026-06-09 — cycle 2026-06-08__release-v5.3 (ST-24, EPIC-03; docs/governance/si05_digest_log_schema_validation.md produced; schema validated as PASS against BLG-GOV-96 criteria; Director of Quality + Data Model & Domain Schema Owner sign-off)

**Gate criteria:** Must complete before 2026-07-04. The effectiveness review relies on si05_digest_log data being complete.

**Problem**
The 2026-07-04 SI-05 effectiveness review (BLG-GOV-96, BLG-GOV-113) will rely on si05_digest_log entries. If the schema is missing fields needed for the review (e.g., send_at timestamp, recipient, status, content_hash), the review will be unable to assess delivery reliability or consistency.

**Scope**
- Review si05_digest_log schema against BLG-GOV-96 effectiveness criteria
- Confirm that the schema captures: send_at, status (SUCCESS/FAILED), recipient, digest content hash or preview
- If any required fields are missing: file an urgent story to add them (before 2026-07-01)
- If schema is complete: record PASS

**Acceptance Criteria**
- Schema validated against BLG-GOV-96 effectiveness criteria fields
- Schema PASS or gap items filed as urgent stories
- Must complete before 2026-07-01 (before review date)
- Data Model & Domain Schema Owner sign-off

---


### BLG-OPS-62 — Investigate GET /portfolio/concentration-status high latency
**Priority:** P3 (Low)
**Type:** Operations / Performance
**Owner:** Infrastructure & Operations Owner
**Source:** v5.5 ST-06 BLG-OPS-13 re-run §18.3 — 2026-06-11
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.6

✅ COMPLETE — 2026-06-16 — cycle 2026-06-16__release-v5.6 (ST-04, EPIC-02, PR #766; root cause: get_live_fx_rate() external HTTP + 200ms sleep; fix: 5-min TTL cache; AC-03/04 staging verification deferred BLG-OPS-66)

**Problem**
GET /portfolio/concentration-status measured p50=3,985ms and p95=5,917ms on production — the highest-latency DB endpoint in the entire baseline. This endpoint calculates portfolio concentration across all live positions and is likely performing a full portfolio scan without appropriate indexing. Latency at this level makes the endpoint unsuitable for use in any page that loads on navigation.

**Scope**
- Profile the underlying SQL query for GET /portfolio/concentration-status
- Identify missing indexes or unoptimised joins
- Add index or materialised view as appropriate

**Acceptance Criteria**
- p95 latency reduced to ≤1,000ms on production
- Infrastructure & Operations Owner sign-off after re-measurement

---


### BLG-OPS-63 — Investigate GET /portfolio/red-flag-journal high latency
**Priority:** P3 (Low)
**Type:** Operations / Performance
**Owner:** Infrastructure & Operations Owner
**Source:** v5.5 ST-06 BLG-OPS-13 re-run §18.3 — 2026-06-11
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.6

✅ COMPLETE — 2026-06-16 — cycle 2026-06-16__release-v5.6 (ST-05, EPIC-02, PR #766; root cause: per-request DDL calls; fix: process-lifetime schema-once guard; AC-03/04 staging verification deferred BLG-OPS-67)

**Problem**
GET /portfolio/red-flag-journal measured p50=3,005ms and p95=3,200ms on production — consistent ~3s across all 7 samples, indicating a structural query issue rather than variance. The endpoint likely scans the full trade history for red flag patterns without a covering index on the relevant columns.

**Scope**
- Profile the underlying SQL query for GET /portfolio/red-flag-journal
- Add index on flagged trade columns or apply result caching

**Acceptance Criteria**
- p95 latency reduced to ≤1,000ms on production
- Infrastructure & Operations Owner sign-off after re-measurement

---


### BLG-OPS-64 — Investigate GET /analytics/behavioural-drift high latency
**Priority:** P3 (Low)
**Type:** Operations / Performance
**Owner:** Infrastructure & Operations Owner
**Source:** v5.5 ST-06 BLG-OPS-13 re-run §18.3 — 2026-06-11
**Effort:** S (~0.5 day)
**Provisional-Target:** v5.6

✅ COMPLETE — 2026-06-16 — cycle 2026-06-16__release-v5.6 (ST-06, EPIC-02, PR #766; root cause: per-request DDL + 90-day trade scan; fix: schema-once guard + 15-min TTL result cache; AC-03/04/05 staging verification deferred BLG-OPS-68)

**Problem**
GET /analytics/behavioural-drift measured p50=3,293ms and p95=3,798ms on production. The SI-02 drift analysis scans full trade and signal history. Consider a TTL-based result cache (acceptable staleness for an analytics endpoint: 15–30 minutes) to reduce repeated full-history scans.

**Scope**
- Profile the underlying query for GET /analytics/behavioural-drift
- Implement TTL-based result caching (in-memory or Redis) with 15–30 minute TTL

**Acceptance Criteria**
- p95 latency reduced to ≤1,000ms on production for cached calls
- Cache hit rate ≥50% under typical usage
- Infrastructure & Operations Owner sign-off after re-measurement

---


### BLG-OPS-65 — Anthropic API cost 14-cycle trend analysis
**Priority:** P3 (Low)
**Type:** Operations / Cost Governance
**Owner:** FinOps & Resource Architect
**Source:** IDEA-finops-20260610-01 — Promoted-Backlog rebalance 2026-06-16__scheduled (DL-046; gate cleared: BLG-GOV-74 COMPLETE v4.4)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** Unscheduled
**Displacement:** BLG-OPS-18 (data pipeline cost baseline, P3, gate-conditional on BLG-OPS-17) deprioritised.

✅ COMPLETE — 2026-06-16 — cycle 2026-06-16__release-v5.6 (ST-11, EPIC-03, PR #764; est. $0.05–$0.15/month vs $5/month threshold; trajectory stable/negligible; next review 2026-12-16; FinOps approved; docs/ops/anthropic_api_cost_trend_2026.md produced)

**Problem**
BLG-GOV-74 (first AI feature usage review, v4.4) established the initial Claude API usage baseline. After 14+ production cycles of Claude API usage (generate-thesis, check-daily-cost), a trend analysis would confirm whether usage is stable, growing, or anomalous relative to the Anthropic tier threshold defined in BLG-OPS-37 ($5/month upgrade threshold). No multi-cycle cost trend document currently exists.

**Scope**
- Review claude_audit_log (or equivalent) for per-cycle Claude API call counts and estimated costs (v4.4–v5.5 cycles)
- Produce a trend chart/table: cycles × estimated cost
- Assess trajectory against BLG-OPS-37 $5/month threshold
- FinOps & Resource Architect sign-off

**Acceptance Criteria**
- Trend analysis document produced covering cycles v4.4–present
- Cost trajectory assessed against defined upgrade threshold
- FinOps & Resource Architect sign-off recorded

---


---

### BLG-FE-75 — Staging verification: SI-05 digest deep links navigate on mobile Telegram
**Priority:** P3 (Low)
**Type:** QA / Staging
**Owner:** Head of UX & Design
**Source:** ST-01 AC-02 staging gate — 2026-06-16 (v5.6 sprint execution)
**Effort:** XS (<1h)
**Provisional-Target:** v5.7

✅ COMPLETE — 2026-06-17 — cycle: 2026-06-16__release-v5.7 (ST-05; mobile Telegram staging run confirmed; 2 in-sprint bug fixes: MarkdownV2 decimal escape + HashRouter /#/ prefix)

---

### BLG-QA-56 — SI-01 all-pass state Playwright scenario
**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA Lead; Director of Quality
**Source:** GAP-ARC5-01 — Arc 5 coverage assessment ST-10 v5.6

✅ COMPLETE — 2026-06-17 — cycle: 2026-06-16__release-v5.7 (ST-06; SC-SI-01d added to si01-si03-integration.spec.js)

---

### BLG-QA-57 — SI-03 Red Flag Journal pagination Playwright scenario
**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA Lead; Director of Quality
**Source:** GAP-ARC5-02 — Arc 5 coverage assessment ST-10 v5.6

✅ COMPLETE — 2026-06-17 — cycle: 2026-06-16__release-v5.7 (ST-07; SC-RFJ-04 added to red-flag-journal.spec.js)

---

### BLG-QA-58 — Arc 5 compliance score trend value Playwright scenario
**Priority:** P3 (Low)
**Type:** QA / Test Coverage
**Owner:** QA Lead; Director of Quality
**Source:** GAP-ARC5-03 — Arc 5 coverage assessment ST-10 v5.6

✅ COMPLETE — 2026-06-17 — cycle: 2026-06-16__release-v5.7 (ST-08; SC-ARC5-05 added to arc5-compliance-section.spec.js)

---

### BLG-OPS-66 — Staging verification: concentration-status p95 after FX cache fix
**Priority:** P3 (Low)
**Type:** Operations / Staging Verification
**Owner:** Infrastructure & Operations Owner
**Source:** ST-04 (EPIC-02, v5.6) — BLG-OPS-62 AC-03/04 staging-deferred

✅ COMPLETE — 2026-06-17 — cycle: 2026-06-16__release-v5.7 (ST-01; p95=755ms < 1,000ms target; FX cache fix confirmed effective)

---

### BLG-OPS-67 — Staging verification: red-flag-journal p95 after schema-once fix
**Priority:** P3 (Low)
**Type:** Operations / Staging Verification
**Owner:** Infrastructure & Operations Owner
**Source:** ST-05 (EPIC-02, v5.6) — BLG-OPS-63 AC-03/04 staging-deferred

✅ COMPLETE — 2026-06-17 — cycle: 2026-06-16__release-v5.7 (ST-02; p95=872ms < 1,000ms target; schema-once fix confirmed effective)

---

### BLG-OPS-68 — Staging verification: behavioural-drift p95 + cache hit rate after fix
**Priority:** P3 (Low)
**Type:** Operations / Staging Verification
**Owner:** Infrastructure & Operations Owner
**Source:** ST-06 (EPIC-02, v5.6) — BLG-OPS-64 AC-03/04/05 staging-deferred

✅ COMPLETE — 2026-06-17 — cycle: 2026-06-16__release-v5.7 (ST-03; p95=677ms cached < 1,000ms; cache hit rate ≥50% inferred from timing signature)

---

### BLG-OPS-69 — Staging verification: research view p95 + cache hit rate after TTL cache
**Priority:** P2 (Medium)
**Type:** Operations / Staging Verification
**Owner:** Infrastructure & Operations Owner; Head of Backend Engineering
**Source:** ST-07 (EPIC-02, v5.6) — BLG-OPS-22 AC-04/05 staging-deferred

✅ COMPLETE — 2026-06-17 — cycle: 2026-06-16__release-v5.7 (ST-04; p95=105ms << 2,000ms; cache hit rate ≥90% inferred; cache invalidation mechanism confirmed via v5.6 code review)


---

## Closed Items — v5.8 Post-Ship (2026-06-17)

| BLG-ID | Title | Shipped | Release | Cycle |
|--------|-------|---------|---------|-------|
| BLG-GOV-101 ✅ | Governance model complexity assessment | 2026-06-17 | v5.8 (ST-04 EPIC-01) | 2026-06-17__release-v5.8 |

## Closed Items — v5.9 Post-Ship (2026-06-18)

*Archived: 11 items shipped in v5.9 (cycle 2026-06-17__release-v5.9). Groom date: 2026-06-18.*

| ID | Title | Ship note |
|----|-------|-----------|
| BLG-GOV-125 ✅ | SC-03: Consolidate spec_references policy sub-variants in execution_prompt.md | Shipped v5.9 ST-01 (EPIC-01) — STEP 3.1.A steps 2a/2b/2c consolidated into unified 3-case lookup table; version bumped; Head of Specs Team sign-off |
| BLG-GOV-126 ✅ | SC-04: Remove STEP 8.6–8.7 fatigue detection guardrail from roadmap_prompt.md | Shipped v5.9 ST-02 (EPIC-01) — STEPs 8.6–8.7 removed; STEP 5 Challenger failure rule updated to cover convergence bias; version bumped; Head of Specs Team sign-off |
| BLG-GOV-127 ✅ | SC-05: Remove dead-load advisory steps from release_planning_prompt.md | Shipped v5.9 ST-03 (EPIC-01) — STEP 5.7 made conditional on escalations; STEP 1.3 reduced to single-line reminder; version bumped; Head of Specs Team sign-off |
| BLG-GOV-128 ✅ | SC-06: Make Playwright selector check conditional on DOM changes in execution_prompt.md | Shipped v5.9 ST-04 (EPIC-01) — STEP 3.1.A step 13 tightened to DOM-change-relevant stories only; frontend EPICs retain full scan; version bumped; Head of Specs Team sign-off |
| BLG-GOV-129 ✅ | SC-07: Compress Advisory Summary Block format docs in post_ship_closure.md | Shipped v5.9 ST-05 (EPIC-01) — Advisory Summary Block format documentation compressed to ≤5 lines; version bumped; Head of Specs Team sign-off |
| BLG-QA-24 ✅ | Yahoo Finance backoff path integration test stub | Shipped v5.9 ST-06 (EPIC-02) — test_yahoo_backoff_path_401_sleep_once_then_200 added to tests/test_screener_data_service.py; passes in CI; QA Lead sign-off |
| BLG-GOV-38 ✅ | DoQ sign-off date compliance audit (v3.7–v3.9) | Shipped v5.9 ST-07 (EPIC-02) — all QA evidence files v3.7–v3.9 reviewed; findings in advisory_doq_audit_v37_v39.md; sealed artefacts not modified; Director of Quality sign-off |
| BLG-QA-34 ✅ | QA evidence file format audit | Shipped v5.9 ST-08 (EPIC-02) — QA evidence files v3.7–v4.0 reviewed; format inconsistencies documented in advisory_qa_format_audit_v37_v40.md; Director of Quality notified |
| BLG-GOV-53 ✅ | Agent idea participation tracking | Shipped v5.9 ST-09 (EPIC-02) — participation summary across all closed idea windows; reviewed by Director of HR; filed as advisory_agent_idea_participation.md |
| BLG-QA-50 ✅ | Create formal regression test suite baseline document | Shipped v5.9 ST-10 (EPIC-02) — docs/qa/regression_test_suite_baseline.md; all test.py entries and Playwright specs mapped with feature coverage; DoQ sign-off |
| BLG-FE-57 ✅ | Pre-entry panel: show warning/fail count when collapsed | Shipped v5.9 ST-11 (EPIC-02) — warning/fail count badge implemented in TradePlan.js; Playwright SC-PEP-BADGE-01a/01b/02 pass; Head of UX & Design sign-off |

---

### BLG-GOV-101 — Governance model complexity assessment ✅ COMPLETE

**Shipped:** v5.8, ST-04 (EPIC-01), 2026-06-17. GCA-2026-06-17 produced. Complexity confirmed as secondary contributing factor (not root cause). 7 simplification candidates (SC-01–SC-07) filed as BLG-GOV-123–129. Director of HR + PMO Lead + Head of Specs Team sign-off 2026-06-17. Source: docs/governance/governance_complexity_assessment_2026-06-17.md. commit SHA fbdf1745. PR #790 merged 2026-06-17T13:24:57Z.

---

## v6.0 Shipped Items — 2026-06-22 (cycle: 2026-06-19__release-v6.0)

**Shipped:** v6.0 — Signal Correctness, User Intelligence & SI-05 Effectiveness
**Verification:** Verified_with_deviations (2 P3 process deviations, accepted)
**Changelog:** docs/product/changelog.md#v6.0
**Verification report:** claude/cycles/2026-06-19__release-v6.0/verification_report.md

| ID | Title | Priority | Ship note |
|----|-------|----------|-----------|
| BLG-BE-36 ✅ | Align signal_service suggested_shares to risk-based sizing model | P0 | Shipped v6.0 ST-01 (EPIC-01) — P0 Correctness Fast-Track; signal_service.py updated to use sizing_service.size_position(); cash-allocation model removed; CI tests pass |
| BLG-FEAT-46 ✅ | Trader's Morning Briefing dashboard | P1 | Shipped v6.0 ST-02 (EPIC-02) — DashboardHome.js extended with 5-card Morning Briefing section; all ACs pass; Playwright coverage; Product Value Alert resolved |
| BLG-FEAT-20 ✅ | Net-of-costs performance tracking | P1 | Shipped v6.0 ST-03 (EPIC-02) — brokerage cost fields added; net-of-costs R-multiple computed and surfaced; PATCH /trades/{trade_id}/costs; ACs pass |
| BLG-FEAT-47 ✅ | Screener data quality telemetry | P1 | Shipped v6.0 ST-04 (EPIC-03) — tickers_requested/loaded/failed/last_full_run_utc/run_quality fields added; ScreenerQualityPanel component; Playwright pass |
| BLG-OPS-70 ✅ | SI-05 deep link AC-04 staging confirmation | P2 | Shipped v6.0 ST-05 (EPIC-03) — FRONTEND_URL verified; SI-05 digest deep links confirmed functional in production |
| BLG-FE-64 ✅ | RFJ design review pre-brief | P2 | Shipped v6.0 ST-06 (EPIC-04) — gate 2026-06-21 cleared (6th attempt); design review brief produced; Head of UX & Design sign-off |
| BLG-FE-41 ✅ | Red Flag Journal visual design review | P3 | Shipped v6.0 ST-07 (EPIC-04) — gate 2026-06-21 cleared; RFJ visual design review complete; BLG-FE-66 filed (date-range filter follow-on); Head of UX & Design sign-off |
| BLG-GOV-112 ✅ | SI-05 digest weekly cadence review | P2 | Shipped v6.0 ST-08 (EPIC-04) — gate 2026-07-04 cleared via PO override; weekly cadence maintained; formal reassessment 2026-07-04; Product Owner + Director of Quality sign-off |
| BLG-GOV-115 ✅ | SI-05 digest actionability metric definition | P2 | Shipped v6.0 ST-09 (EPIC-04) — gate 2026-07-04 cleared via PO override; 4 metrics defined (ATCR, RFAR, DDCR, EPAR); Metrics Definitions & Analytics Owner sign-off |
| BLG-GOV-130 ✅ | SI-05 Phase 2 activation decision scope | P2 | Shipped v6.0 ST-10 (EPIC-04) — gate 2026-07-04 cleared via PO override; DEFER decision documented; Phase 2 review revised to 2026-08-04; Product Owner sign-off |
| BLG-OPS-59 ✅ | SI-05 service production p99 latency baseline review | P2 | Shipped v6.0 ST-11 (EPIC-04) — gate 2026-07-04 cleared via PO override; PASS WITH DEVIATION (P3: BLG-OPS-54 scope revised); Infrastructure & Operations Owner sign-off |
---

### BLG-BE-46 — Investigate trade_plans.position_id never populated in production

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-07-09
**Shipped in:** v6.8 (cycle: 2026-07-08__release-v6.8)
**Evidence:** docs/product/changelog.md#v6.8; claude/cycles/2026-07-08__release-v6.8/verification_report.md

### BLG-BE-46 — Investigate trade_plans.position_id never populated in production
**Priority:** P1 (High)
**Type:** Backend / Data Integrity
**Owner:** Backend Engineering Patterns Owner; PMO Lead
**Source:** `plan release v6.7` session — SI-02 production re-verification — 2026-07-06
**Effort:** M (~1–2 days)
**Provisional-Target:** ✅ COMPLETE — 2026-07-09 — cycle: 2026-07-08__release-v6.8 (ST-01)

**Problem**
Verified via production API (2026-07-06): `GET /trades` reports `total_trades: 20` (closed trades). `GET /trade-plans` reports 11 total trade plans, but all 11 have `position_id: null` — none are linked to any closed trade record. `GET /analytics/arc5-compliance` independently confirms `trade_plan_adherence_rate: 0.0`. This has silently distorted the SI-02 gate's "closed trades with linked trade_plans" condition across many cycles — carried forward as an estimated 15–20 when the real, verified value is 0. Trade plans do exist and are reportedly used, so this looks like a genuine linkage bug rather than an unused feature.

**Scope**
- Audit the position-lifecycle and trade-plan services for where `trade_plans.position_id` should be set when a plan's associated trade opens and later closes
- Determine root cause: backend bug (field never written), workflow gap (user not linking plans), or migration/schema gap
- If a bug is confirmed: implement the fix so new `trade_plans` rows populate `position_id` correctly
- Assess whether the 11 existing rows can be reliably backfilled (e.g. ticker + date-proximity match against `trade_history`), or document why backfill isn't feasible

**Acceptance Criteria**
- Root cause documented (bug / workflow gap / other)
- If a bug: fix implemented and verified — a newly closed trade with an associated plan shows `position_id` set, confirmed via API
- Decision recorded on whether historical backfill was performed or explicitly deferred
- `current_roadmap.md`'s SI-02 gate row reflects the corrected linked-plan count once this resolves
---

### BLG-SEC-08 — Unvalidated dict keys used as SQL column names in database.update_signal()

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-07-09
**Shipped in:** v6.8 (cycle: 2026-07-08__release-v6.8)
**Evidence:** docs/product/changelog.md#v6.8; claude/cycles/2026-07-08__release-v6.8/verification_report.md

### BLG-SEC-08 — Unvalidated dict keys used as SQL column names in database.update_signal()
**Priority:** P2 (Medium)
**Type:** Security / Input Validation
**Owner:** Cybersecurity & Trust Lead; Backend Engineering Patterns Owner
**Source:** Cybersecurity & Trust Lead sign-off review, ST-03 (BLG-SEC-02) — cycle 2026-07-02__release-v6.4 — 2026-07-02
**Effort:** S (~0.5 day)
**Provisional-Target:** ✅ COMPLETE — 2026-07-09 — cycle: 2026-07-08__release-v6.8 (ST-02)

**Problem**
`database.update_signal(signal_id, updates)` builds its `SET` clause via `f"{key} = %s"` for every key in the caller-supplied `updates` dict, with values (but not keys) parameterised. `PATCH /signals/{signal_id}` (`main.py`) passes an arbitrary `updates: dict` request body through to this function with no key allowlist — only the `status` value is checked, and only if the `status` key is present. An authenticated caller can therefore submit arbitrary column names in the request body, which are interpolated unvalidated into the SQL statement text. This is a structural SQL-construction risk (malformed/rejected queries at minimum; potential to target unintended columns if a key happens to match one) independent of the ticker/market value sanitisation added by BLG-SEC-02.

**Scope**
- Define an explicit allowlist of columns `PATCH /signals/{signal_id}` may update (e.g. `status`, `ticker`, `market`, `reason`) in `database.update_signal()` or at the router/service layer
- Reject (400/422) any key outside the allowlist
- Add regression test(s) confirming an out-of-allowlist key is rejected rather than reaching the SQL statement

**Acceptance Criteria**
- `update_signal()` (or its caller) rejects any `updates` key not on an explicit allowlist
- Existing legitimate update flows (status transitions, ticker/market corrections) continue to work
- Unit test covers rejection of an arbitrary/unexpected key
- Cybersecurity & Trust Lead sign-off
---

### BLG-SEC-07 — Manual review of existing signals for anomalous ticker/market values

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-07-09
**Shipped in:** v6.8 (cycle: 2026-07-08__release-v6.8)
**Evidence:** docs/product/changelog.md#v6.8; claude/cycles/2026-07-08__release-v6.8/verification_report.md

### BLG-SEC-07 — Manual review of existing signals for anomalous ticker/market values
**Priority:** P3 (Low)
**Type:** Security / Input Validation
**Owner:** Cybersecurity & Trust Lead; Backend Engineering Patterns Owner
**Source:** ST-03 (BLG-SEC-02) AC-02, deferred at sprint execution — cycle 2026-07-02__release-v6.4 — 2026-07-02
**Effort:** XS (<1h)
**Provisional-Target:** ✅ COMPLETE — 2026-07-09 — cycle: 2026-07-08__release-v6.8 (ST-03)

**Problem**
BLG-SEC-02 (ST-03, cycle 2026-07-02__release-v6.4) added write-time sanitisation to `database.create_signal()` / `create_rebalance_exit_signal()`, stripping any character outside `[A-Za-z0-9.\-/:]` and capping ticker/market values at 12 characters. This closes the forward-going gap but does not touch rows already in the `signals` table written before the fix shipped. AC-02 of ST-03 requires a one-time review of existing rows — this is a live-database data-hygiene task, not CI-testable, and was explicitly deferred to a tracked manual execution step per `sprint_planning_notes.md`.

**Scope**
- Query the production `signals` table for `ticker` or `market` values containing characters outside `[A-Za-z0-9.\-/:]`, or longer than 12 characters
- Document any anomalous rows found (ticker, market, signal_date, portfolio_id)
- Clean (correct or null out) any confirmed-anomalous values; leave benign historical values (e.g. legitimate tickers longer than 12 chars, if any) documented as accepted

**Acceptance Criteria**
- Existing `signals` table rows reviewed for anomalous ticker/market values
- Findings documented (count of anomalies found, or "none found")
- Any confirmed-anomalous values cleaned or explicitly accepted with rationale
- Cybersecurity & Trust Lead sign-off
---

### BLG-OPS-99 — Provision application X-API-Key for governed routines

**Status at retirement:** ✅ Complete
**Priority at retirement:** P1
**Retired:** 2026-07-09
**Shipped in:** v6.8 (cycle: 2026-07-08__release-v6.8)
**Evidence:** docs/product/changelog.md#v6.8; claude/cycles/2026-07-08__release-v6.8/verification_report.md

### BLG-OPS-99 — Provision application X-API-Key for governed routines
**Priority:** P1 (High) — resolves LP-08, 2nd occurrence of this credential gap blocking SI-02 gate verification
**Type:** Operations / Infrastructure
**Owner:** Infrastructure & Operations Owner; PMO Lead
**Source:** IDEA-infra-ops-20260708-01 (IW-20260708-01) — Backlog (gate-conditional); rebalance 2026-07-08__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** ✅ COMPLETE — 2026-07-09 — cycle: 2026-07-08__release-v6.8 (ST-04)
**Gate criteria:** None — this item itself is the unblocking action

**Problem**
No governed routine holds an application-level API key with production database/API access, so gate conditions requiring live data (notably SI-02's trade-count/linkage condition) can only ever be checked via self-report or by whoever last ran a manual query — a recurring credential gap (LP-08, cited in `2026-07-06__release-v6.7` closure §6 item #1).

**Scope**
- Provision an application `X-API-Key` (or equivalent scoped credential) and document its storage location (e.g. `~/.api_keys`) so governed routines (roadmap rebalance, release planning) can query production directly

**Acceptance Criteria**
- Key provisioned and documented
- A governed routine successfully uses it to directly confirm a gate condition (e.g. SI-02 linked-trade count) without relying on self-report
---

### BLG-FEAT-52 — Trade tagging and tag-based performance filtering

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-07-09
**Shipped in:** v6.8 (cycle: 2026-07-08__release-v6.8)
**Evidence:** docs/product/changelog.md#v6.8; claude/cycles/2026-07-08__release-v6.8/verification_report.md

### BLG-FEAT-52 — Trade tagging and tag-based performance filtering
**Priority:** P2 (Medium) — upgraded from P3 (mandatory pull-forward candidate, roadmap rebalance 2026-07-08__scheduled)
**Type:** Product Feature / User Value
**Owner:** Product Owner
**Source:** IDEA-product-owner-20260619-02 (IW-20260619-01) — Backlog-gate-conditional; rebalance 2026-06-24__scheduled. Ungated and descoped via `IDEA-product-owner-20260708-01` (IW-20260708-01), roadmap rebalance 2026-07-08__scheduled STEP 5 — see `claude/cycles/2026-07-08__scheduled/cycle_record.md`.
**Effort:** S (~2–3 days, descoped from L)
**Provisional-Target:** ✅ COMPLETE — 2026-07-09 — cycle: 2026-07-08__release-v6.8 (ST-05)
**Gate criteria:** None — ungated 2026-07-08. Original PO-02 (Journal Pattern Recognition) gate removed: tagging and tag-based filtering do not require PO-02's cross-trade pattern infrastructure to ship value; confirmed at STEP 5 debate that the descoped AC set below does not re-introduce the dependency via `BLG-FEAT-16`'s `trade_annotations` cross-reference.

**Problem**
Trades are currently classified only by market, sector, and signal type. There is no mechanism for a user to apply free-form tags (e.g. "earnings catalyst", "gap-and-go", "sector rotation") and subsequently filter performance analytics by those tags. Tag-based filtering would allow comparison of win rate and average R across user-defined trade categories.

**Scope (descoped 2026-07-08 — tags-only, no cross-trade pattern dependency)**
- Data model: `trade_tags` table (trade_id, tag_name, created_at); many-to-many relationship. Self-contained — does not read or write `trade_annotations` (BLG-FEAT-16) or any PO-02 structure.
- API: POST/DELETE /trades/{id}/tags; GET /analytics/tag-performance (win rate, avg R, count by tag)
- Frontend: tag input on Trade Plan form; tag filter on PerformanceAnalytics page

**Acceptance Criteria**
- AC-01: User can add/remove tags on any trade plan
- AC-02: GET /analytics/tag-performance returns win rate and average R broken down by tag
- AC-03: PerformanceAnalytics page surfaces tag-based filter controls
- AC-04: Confirm at sprint planning that `trade_tags` has no foreign-key or service dependency on `trade_annotations`/PO-02 structures (independence check per STEP 5 Challenger condition)
---

### BLG-FEAT-71 — SI-02 gate visibility indicator (Reports page)

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-07-09
**Shipped in:** v6.8 (cycle: 2026-07-08__release-v6.8)
**Evidence:** docs/product/changelog.md#v6.8; claude/cycles/2026-07-08__release-v6.8/verification_report.md

### BLG-FEAT-71 — SI-02 gate visibility indicator (Reports page)
**Priority:** P2 (Medium) — mandatory pull-forward candidate (roadmap rebalance 2026-07-08__scheduled)
**Type:** Product Feature / Governance Transparency
**Owner:** Product Owner
**Source:** IDEA-product-owner-20260708-02 (IW-20260708-01) — Advance; rebalance 2026-07-08__scheduled STEP 5
**Effort:** S (~1–2 days)
**Provisional-Target:** ✅ COMPLETE — 2026-07-09 — cycle: 2026-07-08__release-v6.8 (ST-06)
**Gate criteria:** None — ships showing current state today (0 linked / 20 closed trades, per `BLG-BE-46`).

**Problem**
The SI-02 behavioural-drift gate's true status has repeatedly required a full governed routine to reconcile — twice this cycle alone (the 15-vs-20 trade-count discrepancy, then the `BLG-BE-46` linkage-bug finding that the real linked count is 0). No user-facing surface shows this gate's status at all.

**Scope**
- Frontend: small status panel/badge on the Reports page (or Trading nav) surfacing: total closed trades, trades linked to a trade plan, and the 3 SI-02 gate conditions (linked-trade count, drift-endpoint latency, drift-score variance) with a MET/NOT MET indicator per condition
- Backend: read from existing endpoints (`GET /trades`, `GET /trade-plans`, `GET /analytics/arc5-compliance`) — no new data model required
- Must display the corrected linked-plan count (reads live, or the structured `current_roadmap.md` field once available), not a stale hardcoded estimate

**Acceptance Criteria**
- AC-01: Indicator shows total closed trades and total trade-plan-linked closed trades as two distinct numbers
- AC-02: Indicator shows MET/NOT MET for each of the 3 SI-02 gate conditions
- AC-03: Values are read live from existing endpoints, not hardcoded
- AC-04: Confirmed at sprint planning that AC-01/02 correctly reflect the `BLG-BE-46` finding (0 linked trades) if that bug is still unresolved at build time
---

### BLG-SPEC-58 — Dashboard homepage visual hierarchy review post-v6.2

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-07-09
**Shipped in:** v6.8 (cycle: 2026-07-08__release-v6.8)
**Evidence:** docs/product/changelog.md#v6.8; claude/cycles/2026-07-08__release-v6.8/verification_report.md

### BLG-SPEC-58 — Dashboard homepage visual hierarchy review post-v6.2
**Priority:** P3 (Low)
**Type:** UX Spec / Assessment
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Source:** IDEA-head-of-ux-20260626-02 — Promoted-Backlog rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** ✅ COMPLETE — 2026-07-09 — cycle: 2026-07-08__release-v6.8 (ST-07)

**Problem**
v6.2 added an AI daily briefing card to the dashboard homepage alongside existing portfolio summary, positions overview, and system status. The information architecture and visual hierarchy may no longer optimally match trader workflow priority. A rapid assessment before v6.3 scope is defined confirms the hierarchy is correct or surfaces actionable improvements.

**Scope**
- Review current dashboard homepage layout against trader workflow priority (morning review: briefing → positions → action)
- Assess visual weight, card ordering, and information density after AI briefing card addition
- Produce short findings note: "hierarchy confirmed" or list of priority-order or layout improvements
- File any actionable improvements as separate backlog items

**Acceptance Criteria**
- Assessment document produced covering visual hierarchy post-v6.2 dashboard changes
- Findings reviewed by Head of UX & Design and Product Owner
- Any improvements filed as separate backlog items with priority and effort estimates
---

### BLG-SPEC-59 — R-multiple cross-currency normalization specification

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-07-09
**Shipped in:** v6.8 (cycle: 2026-07-08__release-v6.8)
**Evidence:** docs/product/changelog.md#v6.8; claude/cycles/2026-07-08__release-v6.8/verification_report.md

### BLG-SPEC-59 — R-multiple cross-currency normalization specification
**Priority:** P2 (Medium)
**Type:** Spec / Documentation
**Owner:** Financial Reporting & Records Owner; Head of Specs Team
**Source:** IDEA-financial-reporting-20260626-02 — Promoted-Backlog rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** ✅ COMPLETE — 2026-07-09 — cycle: 2026-07-08__release-v6.8 (ST-08)

**Problem**
R-multiple is a core trade evaluation metric. GBP-denominated positions have a different native currency from USD positions. The specification for how R-multiple is calculated and displayed for cross-currency positions is not documented. This gap is directly related to BLG-FE-79 (P1 R-multiple display bug) — fixing the display correctly requires a clear specification of cross-currency behaviour.

**Scope**
- Define R-multiple calculation behaviour for GBP/USD positions: native currency vs normalised currency
- Specify aggregate R-multiple behaviour (how GBP and USD R-multiples aggregate in portfolio-level views)
- Document "N/A" vs "0.00" vs empty rendering for trades with insufficient stop loss data
- Reviewed by Financial Reporting & Records Owner and Product Owner before BLG-FE-79 fix enters sprint

**Acceptance Criteria**
- Specification document produced covering per-trade and aggregate R-multiple cross-currency behaviour
- "Insufficient data" display contract specified
- Reviewed by Financial Reporting & Records Owner and Product Owner
---

### BLG-SPEC-60 — Trailing stop visual indicator frontend specification

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-07-09
**Shipped in:** v6.8 (cycle: 2026-07-08__release-v6.8)
**Evidence:** docs/product/changelog.md#v6.8; claude/cycles/2026-07-08__release-v6.8/verification_report.md

### BLG-SPEC-60 — Trailing stop visual indicator frontend specification
**Priority:** P2 (Medium)
**Type:** Frontend Spec / UX
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Source:** IDEA-frontend-specs-20260626-02 — Promoted-Backlog rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** ✅ COMPLETE — 2026-07-09 — cycle: 2026-07-08__release-v6.8 (ST-09)

**Problem**
v6.2 ships nightly trailing stop computation. The positions page shows current open positions but does not display the current trailing stop price or distance-to-stop. Users must recall the stop level from memory or refer to external records. A frontend specification for a visual stop indicator enables a future sprint to implement this without spec ambiguity.

**Scope**
- Define visual indicator design: where on the position row the stop price and distance-to-stop appear
- Define data source: trailing_stop field from positions endpoint (confirm field name and availability)
- Define display states: stop set (show price + distance), stop not set (show "Not set" or omit indicator)
- Reviewed by Head of UX & Design and Product Owner before implementation sprint

**Acceptance Criteria**
- Frontend specification document produced covering indicator placement, data source, and display states
- Reviewed by Head of UX & Design and Product Owner
---

### BLG-SPEC-61 — Trailing stop effectiveness metric definition

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-07-09
**Shipped in:** v6.8 (cycle: 2026-07-08__release-v6.8)
**Evidence:** docs/product/changelog.md#v6.8; claude/cycles/2026-07-08__release-v6.8/verification_report.md

### BLG-SPEC-61 — Trailing stop effectiveness metric definition
**Priority:** P2 (Medium)
**Type:** Spec / Metrics
**Owner:** Metrics Definitions & Analytics Owner
**Source:** IDEA-metrics-20260626-01 — Promoted-Backlog rebalance 2026-06-26__scheduled (DL-057)
**Effort:** S (~0.5 day)
**Provisional-Target:** ✅ COMPLETE — 2026-07-09 — cycle: 2026-07-08__release-v6.8 (ST-10)

**Problem**
v6.2 ships nightly trailing stop computation. There is no metric tracking whether computed trailing stop updates were acted upon (position adjusted) vs ignored (position held unchanged). Without this metric, it is impossible to evaluate the feature's impact on trading behaviour or demonstrate the ROI of the v6.2 trailing stop investment. Defining the metric now ensures data is captured from the first day of usage.

**Scope**
- Define metric: trailing_stop_action_rate = positions_adjusted_after_stop_update / positions_with_stop_update_computed
- Define data capture requirement: link trailing stop computation events to subsequent position adjustment events
- Document in `docs/specs/metrics_definitions.md` or equivalent
- Reviewed by Metrics Definitions & Analytics Owner, FinOps & Resource Architect, and Product Owner

**Acceptance Criteria**
- Metric definition document produced covering definition, data sources, and capture requirements
- Reviewed by Metrics Definitions & Analytics Owner and Product Owner
---

### BLG-QA-64 — Fix 12 dark spec files surfaced by Playwright glob discovery

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-07-09
**Shipped in:** v6.8 (cycle: 2026-07-08__release-v6.8)
**Evidence:** docs/product/changelog.md#v6.8; claude/cycles/2026-07-08__release-v6.8/verification_report.md

### BLG-QA-64 — Fix 12 dark spec files surfaced by Playwright glob discovery
**Priority:** P2 (Medium)
**Type:** QA / Test Infrastructure
**Owner:** Director of Quality; Head of Frontend Engineering
**Source:** ST-13 (EPIC-03, v6.2) — glob discovery surfaced 12 pre-existing spec files that were excluded from the old explicit playwright.yml list. Identified 2026-06-25.
**Effort:** M (~1 day — each spec needs investigation and either fix or deletion)
**Provisional-Target:** ✅ COMPLETE — 2026-07-09 — cycle: 2026-07-08__release-v6.8 (ST-11)
**Gate criteria:** None

**Problem**
ST-13 replaced the explicit 26-file spec list in `playwright.yml` with `npx playwright test` (auto-discovery via `playwright.config.js` `testDir`). This surfaced 12 spec files that existed in `tests/e2e/` but were never included in CI. All 12 are failing — likely due to UI text mismatches (component text evolved after spec was written) or pending feature implementations.

Currently excluded via `testIgnore` in `playwright.config.js`:
- arc5-compliance-section.spec.js
- entry-checklist.spec.js
- gate-progress.spec.js
- paper-account.spec.js
- plan-vs-reality.spec.js
- pre-entry-panel-badge.spec.js
- red-flag-journal.spec.js
- sector-heatmap.spec.js
- si01-si03-integration.spec.js
- si05-digest-delivery.spec.js
- signals-add-to-watchlist.spec.js
- signals-allocation-insufficient.spec.js

**Scope**
For each spec file above: investigate failure cause, fix assertions to match current UI/API, remove from `testIgnore` in `playwright.config.js`. Delete any spec that tests a feature not yet implemented (refile as spec debt in appropriate epic).

**Acceptance Criteria**
- AC-01: All 12 spec files removed from `testIgnore` in `playwright.config.js`
- AC-02: All assertions pass in CI without modification to application source
- AC-03: `playwright.config.js` `testIgnore` array is empty or removed
---

### BLG-GOV-134 — CI: inline OpenAPI drift detection for api_performance_baseline.md

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-07-09
**Shipped in:** v6.8 (cycle: 2026-07-08__release-v6.8)
**Evidence:** docs/product/changelog.md#v6.8; claude/cycles/2026-07-08__release-v6.8/verification_report.md

### BLG-GOV-134 — CI: inline OpenAPI drift detection for api_performance_baseline.md
**Priority:** P2 (Medium)
**Type:** Governance Process / CI
**Owner:** Head of Specs Team; PMO Lead
**Source:** IW-20260622-01 (IDEA-head-of-specs-20260622-01) — Promoted-Backlog STEP 4; rebalance 2026-06-22__scheduled
**Effort:** S (~0.5 day)
**Provisional-Target:** ✅ COMPLETE — 2026-07-09 — cycle: 2026-07-08__release-v6.8 (ST-12)

**Problem**
BLG-OPS-73 (PATCH /trades/{trade_id}/costs missing from api_performance_baseline.md) revealed a systemic gap: when an endpoint is added to `docs/reference/openapi.yaml`, there is no CI check confirming a corresponding entry exists in `docs/operations/api_performance_baseline.md`. The execution_prompt.md v3.47 advisory is a reminder, not enforcement.

**Scope**
- Add a CI step (GitHub Actions workflow) that extracts endpoint paths from `openapi.yaml` and compares against entries in `api_performance_baseline.md`
- Output a warning (non-blocking advisory gate) listing any endpoints in openapi.yaml that have no baseline entry
- Does not block PR merge; surfaces as advisory annotation on PR

**Acceptance Criteria**
- CI workflow step runs on PRs that modify `openapi.yaml` or `api_performance_baseline.md`
- Step outputs a diff list of endpoints present in openapi.yaml but absent from baseline
- Advisory only — does not fail the CI run
---

### BLG-OPS-74 — Log Anthropic API token usage and cost per morning briefing call

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-07-09
**Shipped in:** v6.8 (cycle: 2026-07-08__release-v6.8)
**Evidence:** docs/product/changelog.md#v6.8; claude/cycles/2026-07-08__release-v6.8/verification_report.md

### BLG-OPS-74 — Log Anthropic API token usage and cost per morning briefing call
**Priority:** P3 (Low)
**Type:** Operations / Monitoring
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Source:** IW-20260622-01 (IDEA-finops-20260622-01) — Promoted-Backlog STEP 4; rebalance 2026-06-22__scheduled
**Effort:** S (<0.5 day)
**Provisional-Target:** ✅ COMPLETE — 2026-07-09 — cycle: 2026-07-08__release-v6.8 (ST-13)

**Problem**
The Trader Morning Briefing (BLG-FEAT-46, shipped v6.0) calls the Claude API each time it generates a briefing. Token usage and estimated cost per call are not tracked. As briefing frequency or complexity grows, cost visibility is needed for informed FinOps decisions.

**Scope**
- Log token usage (prompt_tokens, completion_tokens) and estimated cost per morning briefing generation call
- Follow the established `claude_audit_log` pattern (from Gemini wiring v3.8); extend or add a parallel log entry for Claude briefing calls
- Surface aggregate monthly cost in `/system-status` or the existing AI cost review mechanism

**Acceptance Criteria**
- Each morning briefing API call produces a log entry with token counts and estimated cost
- Log entries are queryable for weekly/monthly cost aggregation
- GET /system-status or equivalent surfaces cumulative briefing cost for the current month
---

### BLG-FE-77 — Refactor `Watchlist.js` to ESLint compliance

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-07-09
**Shipped in:** v6.8 (cycle: 2026-07-08__release-v6.8)
**Evidence:** docs/product/changelog.md#v6.8; claude/cycles/2026-07-08__release-v6.8/verification_report.md

### BLG-FE-77 — Refactor `Watchlist.js` to ESLint compliance
**Priority:** P3 (Low)
**Type:** Frontend / UX
**Owner:** Head of Frontend Engineering
**Source:** ESLint hook run — pre-existing violations surfaced after eslint-plugin-playwright, eslint-plugin-no-comments, eslint-plugin-better-max-params installed — 2026-06-22
**Effort:** M (~1–2 days)
**Provisional-Target:** ✅ COMPLETE — 2026-07-09 — cycle: 2026-07-08__release-v6.8 (ST-14)

**Problem**
`src/pages/Watchlist.js` has 16 pre-existing ESLint violations that were hidden because three required plugins were not installed. Now that the plugins are in place, the lint-feedback hook fires on every edit to this file, creating noise and discouraging changes. The primary violations are: `max-lines-per-function` (the `Watchlist` component body is 312 lines against a 50-line limit), multiple magic number literals (`200`, `220`, `5`, `60`, `1000`), and inline comments in state declarations. Zero violations were introduced by recent changes — all are pre-existing.

**Scope**
- Extract sub-components from `Watchlist.js`: `WatchlistTableRow`, `WatchlistNewsRow`, and inline badges are all candidates
- Replace magic number literals with named constants at the top of the file
- Remove inline comments; express intent through component and variable names instead
- Ensure all extracted components independently pass ESLint

**Acceptance Criteria**
- `npx eslint src/pages/Watchlist.js` exits 0 with no errors or warnings
- All extracted sub-components also pass ESLint clean
- Watchlist page renders and behaves identically to pre-refactor (no functional regression)
- Playwright E2E watchlist specs continue to pass
---

### BLG-OPS-61 — BLG-OPS-13 v5.1–v5.4 endpoint baseline extension

**Status at retirement:** ✅ Complete
**Priority at retirement:** P3
**Retired:** 2026-07-09
**Shipped in:** v6.8 (cycle: 2026-07-08__release-v6.8)
**Evidence:** docs/product/changelog.md#v6.8; claude/cycles/2026-07-08__release-v6.8/verification_report.md

### BLG-OPS-61 — BLG-OPS-13 v5.1–v5.4 endpoint baseline extension
**Priority:** P3 (Low)
**Type:** Operations / Performance Baseline
**Owner:** Infrastructure & Operations Owner
**Source:** IDEA-infra-ops-20260610-01 — Promoted-Backlog rebalance 2026-06-10__scheduled (DL-044)
**Effort:** S (~0.5–1 day)
**Provisional-Target:** ✅ COMPLETE — 2026-07-09 — cycle: 2026-07-08__release-v6.8 (ST-15)

**Problem**
BLG-OPS-60 (completed v5.4) added v5.3 endpoints to api_performance_baseline.md. However, v5.1 and v5.2 endpoints (POST /digest/si05/send, GET /portfolio/paper-positions enhancements, new v5.2 routes from BLG-SPEC-49–52) were not included. BLG-OPS-13 targets v2.8–v4.6 endpoints; BLG-OPS-61 closes the v5.1–v5.4 gap.

**Scope**
- Identify all new routes added in v5.1 and v5.2 not yet in api_performance_baseline.md
- Run p50/p95 latency measurements against staging
- Add entries to api_performance_baseline.md

**Acceptance Criteria**
- All v5.1/v5.2 new endpoints have latency entries in the baseline document
- Consistent with existing measurement methodology
- Infrastructure & Operations Owner sign-off
---

### BLG-GOV-123 — SC-01: Extract Playwright test standard from execution_prompt.md to shared_standards

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-07-09
**Shipped in:** v6.8 (cycle: 2026-07-08__release-v6.8)
**Evidence:** docs/product/changelog.md#v6.8; claude/cycles/2026-07-08__release-v6.8/verification_report.md

### BLG-GOV-123 — SC-01: Extract Playwright test standard from execution_prompt.md to shared_standards
**Priority:** P2 (Medium)
**Type:** Governance / Prompt Simplification
**Owner:** Head of Specs Team
**Source:** GCA-2026-06-17 — ST-04 (BLG-GOV-101) simplification candidate SC-01
**Effort:** XS (~1 hour)
**Provisional-Target:** ✅ COMPLETE — 2026-07-09 — cycle: 2026-07-08__release-v6.8 (ST-16)

**Scope**
Section 14 of `execution_prompt.md` defines Playwright test authoring standards (waitFor patterns, mock payload advisory, ~30 lines). This content is loaded on every invocation of the execution engine regardless of whether the sprint contains any Playwright work. Extract to `shared_standards.md §16` (or a new §17) and replace Section 14 with a single reference line. No logic change — structural refactoring only.

**Acceptance Criteria**
- Section 14 content moved to shared_standards.md with a new heading
- execution_prompt.md Section 14 replaced with reference: "Playwright test standard: per shared_standards.md §X"
- Version bump on both files; changelog entries appended
- Head of Specs Team sign-off
---

### BLG-OPS-71 — System threat model document

**Status at retirement:** ✅ Complete
**Priority at retirement:** P2
**Retired:** 2026-07-09
**Shipped in:** v6.8 (cycle: 2026-07-08__release-v6.8)
**Evidence:** docs/product/changelog.md#v6.8; claude/cycles/2026-07-08__release-v6.8/verification_report.md

### BLG-OPS-71 — System threat model document
**Priority:** P2 (Medium)
**Type:** Operations / Security
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Source:** IDEA-cybersecurity-20260304-01 (rejected_but_strong.md) — revival triggered by strategic review 2026-06-18; original rejection condition (no production-scale external exposure) no longer holds; system now handles real position data, stop levels, P&L, Alpaca API credentials, Anthropic/Gemini billing keys, and Telegram bot tokens across staging + production
**Effort:** S (~1 day)
**Provisional-Target:** ✅ COMPLETE — 2026-07-09 — cycle: 2026-07-08__release-v6.8 (ST-17)

**Problem**
No formal threat model exists. The system handles high-sensitivity financial data (positions, stop levels, P&L) and multiple third-party API credentials with billing exposure (Alpaca, Anthropic, Gemini, Telegram). Current security controls (API key auth on endpoints, CSP, CI secret scanning) were added reactively. A formal threat model identifies attack surfaces and data sensitivity levels in one place — producing a prioritised gap list before an incident forces it.

**Scope**
- Identify attack surfaces: endpoint auth coverage, Supabase access controls, Render environment variable exposure, Telegram webhook, Alpaca paper trading credentials, AI API keys
- Data sensitivity classification: position data (HIGH), stop levels (HIGH), P&L (HIGH), API keys (CRITICAL), user preferences (MEDIUM)
- Threat actors: external web attacker, compromised dependency, accidental exposure
- Document existing mitigations already in place (API key auth, CSP, CI secret scanning gate)
- Identify gaps; file a BLG-OPS or BLG-SPEC item for each gap discovered
- Output: `docs/security/threat_model.md`

**Acceptance Criteria**
- `docs/security/threat_model.md` produced covering all attack surfaces, data classifications, threat actors, current mitigations, and identified gaps
- Any gaps produce separate BLG items before sign-off
- Reviewed and signed off by Cybersecurity & Trust Lead and Infrastructure & Operations Owner

---

### BLG-BE-52 — Formal disposition for BLG-BE-46's 11 permanently-unlinked historical trade_plans rows

**Status at retirement:** ✅ Complete (Product Owner decision — no backfill)
**Priority at retirement:** P3
**Retired:** 2026-07-10 (backlog consistency audit — item carried a completed PO decision but had not yet been archived)
**Resolved via:** Direct Product Owner action, no cycle (decision recorded 2026-07-09)
**Evidence:** Full decision text below; referenced in commit `b339b175`

### BLG-BE-52 — Formal disposition for BLG-BE-46's 11 permanently-unlinked historical trade_plans rows
**Priority:** P3 (Low)
**Type:** Backend / Data Integrity
**Owner:** Backend Engineering Patterns Owner / PMO Lead
**Source:** LP-12, `claude/cycles/2026-07-08__release-v6.8/lessons_learnt.md` — 2026-07-09
**Effort:** XS (<1h — decision-recording only, unless reconciliation is chosen)
**Provisional-Target:** ✅ COMPLETE — 2026-07-09 — Product Owner decision, no cycle (direct action)

**Problem**
`BLG-BE-46` (fixed in v6.8, ST-01) forward-fixed the `trade_plans.position_id` linkage bug via a backend auto-link in `add_position()` — newly-created `trade_plans` rows now link correctly going forward. The 11 pre-existing `trade_plans` rows (predating the fix) were explicitly decided *not* to be backfilled at the time, on the grounds that they have no reliable ticker/time match to `trade_history` (per `BLG-BE-46`'s own RISK-01). That decision was never given a tracking item or a named owner — `LP-12` (the lessons-learnt action item that called for exactly this) targeted "Delivery Verification, this cycle," but that target passed without action, and neither Delivery Verification's nor Post-Ship Closure's `backlog.md` write scope permits filing a net-new item of this kind inline. This item exists to close that gap and give the decision a permanent, ownable record.

**Scope**
- Product Owner confirms whether the 11 historical unlinked `trade_plans` rows should remain permanently unlinked, or whether a manual/administrative reconciliation pass (e.g. a one-off admin script matching by ticker + date proximity, with human review of ambiguous matches) is worth the effort
- If reconciliation is wanted: scope it as a new story with its own acceptance criteria
- If not: mark this item resolved, with the decision and rationale recorded here as the permanent record

**Acceptance Criteria**
- Product Owner disposition recorded (backfill / no backfill, with rationale)
- If backfill is chosen: a follow-up story is filed and referenced here
- If not: this item is closed with the decision as its resolution — no further action needed

**Product Owner Decision (2026-07-09): No backfill.** The 11 historical `trade_plans` rows remain permanently unlinked (`position_id: null`). Rationale:
- The original engineering assessment (`BLG-BE-46` RISK-01) already found no reliable ticker/time match exists — any backfill would require fuzzy matching with human review of ambiguous cases, and the whole point of this cycle's EPIC-01 was to make the SI-02 gate's underlying data *trustworthy*. Writing uncertain fuzzy-matched links into `trade_plans.position_id` risks trading a visible, honest gap (11 known NULLs) for silent wrong data (incorrect links that look correct but aren't) — a worse outcome for a gate specifically about strategy-adherence integrity.
- Value is capped even in the best case: at most 11 additional linked rows, against a gate that needs 20 linked closed trades — backfilling these 11 would not by itself clear the SI-02 gate, so the effort doesn't buy gate clearance either.
- The system now has a trustworthy path forward without touching historical data: `BLG-BE-46`'s forward-fix links all newly-created `trade_plans` correctly, and `BLG-FEAT-71`'s SI-02 Gate Status section on the Reports page shows the live, honest gate state (currently 0/20 linked, correctly reflecting that only forward-fixed data counts). That transparency is the more valuable investment than chasing an unreliable historical reconciliation.

No follow-up story required. Item closed.
