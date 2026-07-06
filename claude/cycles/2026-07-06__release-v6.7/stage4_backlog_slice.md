**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v6.7
**Cycle:** 2026-07-06__release-v6.7
**Last Updated:** 2026-07-06
**Sprint Backlog Source:** This slice is authoritative. Sprint Planning Engine reads this file at Phase 2.

---

# v6.7 Backlog Slice — 2026-07-06__release-v6.7

<!-- release-plan-marker: RP:v6.7:2026-07-06__release-v6.7 -->

---

## EPIC-01 — UX & Accessibility Contrast Remediation

**Purpose:** Close the mandatory Skill-Silo pull-forward requirement (≥2 build-and-ship U-items) via a systematic dark-theme and light-theme secondary-text contrast remediation, then generalise the fix into a shared design token to prevent a third recurrence.

**Sprint assignment:** Sprint 1

**Maps to:** S2-01, S2-02, S2-03

---

### ST-01 — Dark-theme secondary-text contrast fix (BLG-FE-87)

**Type:** Firm
**Effort:** L (~2–3 days)
**Owner:** Head of UX & Design; Head of Engineering
**Backlog ref:** BLG-FE-87
**Delegation class:** delegated_frontend
**Sprint:** Sprint 1
**EPIC:** EPIC-01

**Context:** The ST-01 (v6.6) contrast audit found `text-slate-500` used for small secondary/label text in ~262 instances across ~90 files, rendered against the app's default dark-theme surfaces at 3.07–4.24:1 contrast — below the 4.5:1 WCAG-AA requirement. This is the app's default theme, so the failure is visible today to the majority of users. Same defect class as `BLG-UX-01`, now found recurring at scale.

**Acceptance criteria:**
- AC-01: Systematic replacement of `text-slate-500` usages that fail contrast against their actual rendered dark-surface background, verified per-surface
- AC-02: Contrast spot-checks recorded for a representative sample of affected pages
- AC-03: Playwright coverage or recorded staging sign-off per CLAUDE.md's frontend-visible-change rule

---

### ST-02 — Light-theme secondary-text contrast fix (BLG-FE-88)

**Type:** Firm
**Effort:** L (~3–4 days)
**Owner:** Head of UX & Design; Head of Engineering
**Backlog ref:** BLG-FE-88
**Delegation class:** delegated_frontend
**Sprint:** Sprint 1
**Depends on:** ST-01 (sequence after, to avoid rework)
**EPIC:** EPIC-01

**Context:** Tailwind's class-based dark mode requires an explicit `dark:` variant; bare classes apply identically in both themes. The audit found 502 bare `text-slate-400` and 262 bare `text-slate-500` instances (764 total, 102 files) with no `dark:`/light-mode companion, meaning these were only ever visually verified against the dark theme. Light-theme contrast: `text-slate-400` = 2.3–2.6:1 (severe failure), `text-slate-500` = 4.3–4.8:1 (borderline fail against `bg-slate-100`).

**Acceptance criteria:**
- AC-01: For each affected secondary-text surface, add a paired `dark:text-*` / light-mode class combination (or `isDark` conditional) so both themes independently pass WCAG-AA
- AC-02: Prioritised by page traffic/visibility
- AC-03: Playwright coverage or a recorded manual light-theme QA pass for at least the highest-traffic pages

---

### ST-03 — Shared secondary-text design token (BLG-FE-89)

**Type:** Firm
**Effort:** M (~1–2 days)
**Owner:** Head of UX & Design; Head of Engineering
**Backlog ref:** BLG-FE-89
**Delegation class:** autonomous
**Sprint:** Sprint 1
**Recommended sequencing:** After ST-01/ST-02 (documents the canonical treatment based on the concrete fixes landed)
**EPIC:** EPIC-01

**Context:** Three separate contrast defects (`BLG-UX-01`, `BLG-UX-02`, `BLG-FE-87`/`BLG-FE-88`) all trace back to the same root cause: secondary/label text colour chosen ad hoc per-component with no shared token or component enforcing a WCAG-AA-safe value per theme.

**Acceptance criteria:**
- AC-01: Define one or two Tailwind utility class pairs (or a small `<SecondaryText>` component) as the canonical secondary-text treatment, documented in the frontend design spec
- AC-02: Frontend spec updated to reference it

---

## EPIC-02 — Governance Process Hardening (AUD-2026-07-06 Follow-Through)

**Purpose:** Resolve the full Lifecycle Audit AUD-2026-07-06 improvement backlog (overall score 81, all 17 prior findings resolved), including the 3-cycle-carried `.claude/skills/` write-scope escalation.

**Sprint assignment:** Sprint 1

**Maps to:** S2-04, S2-05, S2-06, S2-07

---

### ST-04 — `.claude/skills/` write-scope authority + commit-check patch (BLG-GOV-167)

**Type:** Firm
**Effort:** M (~1–2 days)
**Owner:** Head of Specs Team
**Backlog ref:** BLG-GOV-167
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-02

**Context:** No governed routine's declared write scope includes `.claude/skills/`. A deferred patch — adding a diff-verification step to `.claude/skills/commit-check/SKILL.md` — has carried across 3 consecutive cycles (v6.4 → v6.5 → v6.6) with no governed path to resolution; now meets the automatic-escalation threshold.

**Acceptance criteria:**
- AC-01: `shared_standards.md` documents a `.claude/skills/` write-authority provision naming Head of Specs Team
- AC-02: `.claude/skills/commit-check/SKILL.md` contains the diff-verification step (`git add` target list vs. intended file set) before multi-file governance commits
- AC-03: 3-cycle carry-forward item closed in `prompt_change_log.md`

---

### ST-05 — Structural guard for 4 append-only governance logs (BLG-GOV-168)

**Type:** Firm
**Effort:** M (~1–2 days)
**Owner:** Head of Specs Team
**Backlog ref:** BLG-GOV-168
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-02

**Context:** `shared_standards.md` §7 documents a pointer directing engines to give `escalations.md`, `execution_escalations.md`, `verification_escalations.md`, and `delegation_log.md` the same structural count-before/after guard `decision_log.md` already has — but no engine's actual write step was changed. The fix was documentation-only and produced zero adoptions.

**Acceptance criteria:**
- AC-01: `shared_standards.md` contains a single canonical, reusable verification procedure block
- AC-02: All 4 affected engines' write steps (`release_planning_prompt.md`, `execution_prompt.md`, `delivery_verification_prompt.md`, and the `delegation_log.md`-owning engine) reference and apply it
- AC-03: Confirmed via direct read of each engine's write step — not documentation alone

---

### ST-06 — `audit.py` SLA — same-session commit requirement (BLG-GOV-169)

**Type:** Firm
**Effort:** XS (<1 hour)
**Owner:** Head of Specs Team
**Backlog ref:** BLG-GOV-169
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-02

**Context:** An audit report was produced but never committed until a later session retroactively committed it — `claude/audit.py`'s SLA block does not instruct the audit engine to commit its own output.

**Acceptance criteria:**
- AC-01: `claude/audit.py` SLA block states the report must be committed same-session

---

### ST-07 — Delivery Verification STEP 6 status-line documentation (BLG-GOV-170)

**Type:** Firm
**Effort:** XS (<1 hour)
**Owner:** Head of Specs Team
**Backlog ref:** BLG-GOV-170
**Delegation class:** autonomous
**Sprint:** Sprint 1
**EPIC:** EPIC-02

**Context:** The sprint status-line update (`pending verification` → `Verified — <date>`) is correctly performed every cycle but `delivery_verification_prompt.md` STEP 6 never names it — logged as a "new" friction item for 4+ consecutive cycles rather than recognised as expected behaviour.

**Acceptance criteria:**
- AC-01: STEP 6 documents the status-line update as an expected step

---

## Summary

| EPIC | Stories | Firm | Conditional | Total effort estimate |
|------|---------|------|-------------|------------------------|
| EPIC-01 | ST-01, ST-02, ST-03 | 3 | 0 | ~7.5 days |
| EPIC-02 | ST-04, ST-05, ST-06, ST-07 | 4 | 0 | ~3.2 days |
| **Total** | **7** | **7** | **0** | **~10.7 days** |
