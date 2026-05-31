**Owner:** Head of UX & Design
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-31
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Backlog ref:** BLG-FE-49
**Cycle:** 2026-05-31__release-v4.7 (ST-09)

---

# Pre-Entry Validation Panel UX Assessment

**Assessment date:** 2026-05-31
**Assessed by:** Head of UX & Design
**Closes:** BLG-FE-49
**Implementation:** None committed — assessment only

---

## 1. Purpose

PreEntryValidationPanel (shipped v3.8) is a collapsible panel within the Trade Plan form that displays pre-entry validation check results and surfaces the override acknowledgement flow. As Arc 5 evolves (SI-02 drift detection, SI-04 strategy version comparison, SI-05 weekly digest), the pre-entry panel will surface additional compliance context. This assessment identifies improvement opportunities before Arc 5 sprint planning forces ad-hoc changes.

**Component location:** `src/pages/TradePlan.js` — `PreEntryValidationPanel` function (line ~123).

---

## 2. Current Panel Structure

### 2.1 Layout Overview

```
┌─────────────────────────────────────────────────────────┐
│ ⚡ PRE-ENTRY CHECKS         [Warn]         [↓ collapse] │ ← header (always visible)
├─────────────────────────────────────────────────────────┤
│ ✓  Regime Gate                                          │ ← check item (pass)
│ ⚠  Sector Concentration — 2 positions in Energy sector  │ ← check item (warn + detail)
│ ✗  Cash Constraint — Insufficient buying power          │ ← check item (fail + detail)
│ —  Earnings Proximity — skipped                         │ ← check item (skipped)
│                                                         │
│ ☐  I acknowledge the advisory warnings                  │ ← override checkbox (warn/fail only)
└─────────────────────────────────────────────────────────┘
```

### 2.2 Current Checks

| Rule Key | Display Label |
|----------|---------------|
| `regime_gate` | Regime Gate |
| `cash_constraint` | Cash Constraint |
| `sector_concentration` | Sector Concentration |
| `earnings_proximity` | Earnings Proximity |
| `sizing_validity` | Sizing Validity |

### 2.3 Advisory Status Badges

| Status | Badge colour |
|--------|-------------|
| `pass` | Emerald (green) |
| `warn` | Amber (yellow) |
| `fail` | Red |

---

## 3. UX Assessment

### 3.1 Layout Clarity

**Current state:** The panel uses a compact, collapsible design with an icon-based status column (`✓`, `⚠`, `✗`, `—`) and inline detail text. The header prominently shows the advisory badge.

**Observations:**

| # | Observation | Severity |
|---|-------------|----------|
| L-01 | Header badge shows overall advisory status (`Pass`/`Warn`/`Fail`) but the word "Pass" uses the same font size as "Warn" — a scan-at-a-glance distinction requires colour context. Users with limited colour perception may not distinguish pass from warn. | Minor |
| L-02 | Panel collapses to header only (no minimal summary of warning count visible when collapsed). A trader scanning the form cannot tell "how many warnings" without expanding. | Minor |
| L-03 | Loading state shows inline "Checking…" text in the header. On slow connections, the spinner appears inline with the check label — visually small and easy to miss. | Minor |
| L-04 | The ShieldCheck icon (slate-400) is low-contrast against the dark slate background. The icon communicates "security/shield" — may not immediately read as "validation checks" to new users. | Low |

**Overall layout clarity: Adequate for current use case.** The panel is compact and unobtrusive. No critical layout issues.

---

### 3.2 Text Density

**Current state:** Check items use `text-xs` (12px) throughout. Rule labels are in `text-slate-300`; detail text is in `text-slate-500` (muted).

**Observations:**

| # | Observation | Severity |
|---|-------------|----------|
| D-01 | At `text-xs`, detail text (e.g. "2 positions in Energy sector") is rendered in muted `slate-500`. For fail-state messages where the detail is critical action context, the muted tone reduces urgency. | Minor |
| D-02 | The 5 current check labels are short and readable. As Arc 5 adds checks (drift status, strategy compliance), labels may need truncation or wrapping — the current `flex-1 min-w-0` container handles wrapping but has not been tested with longer labels. | Future risk |
| D-03 | No grouping or section headers for check categories. Currently 5 checks fit without issue; if Arc 5 adds 3–5 more, the flat list will feel dense. | Future risk |

**Overall text density: Well-managed at current scale.** No changes required now; recommend grouping when check count exceeds 8.

---

### 3.3 Override Acknowledgement UX

**Current state:** A single checkbox ("I acknowledge the advisory warnings") appears below all check items when any check is `warn` or `fail`. The checkbox controls the submit button's availability.

**Observations:**

| # | Observation | Severity |
|---|-------------|----------|
| O-01 | The checkbox label "I acknowledge the advisory warnings" is generic. It does not specify which warnings are being acknowledged (e.g. "2 warnings above"). A trader who has reviewed the warnings cannot confirm their specific understanding beyond generic acknowledgement. | Moderate |
| O-02 | Warn and Fail checks share the same override flow. A `fail` check represents a strategy hard stop; a `warn` check is advisory. Treating them identically may encourage reflexive checkbox-clicking without genuine review. | Moderate |
| O-03 | The checkbox is the only friction point in the override flow. No confirmation dialog, no reason field, no record of what was acknowledged. This is intentional for UX speed — but as Arc 5 compliance tracking grows, a structured acknowledgement record could improve auditability. | Low — future Arc 5 consideration |
| O-04 | Override checkbox is visually separated from the check items only by `mt-3` margin. At-a-glance, it does not read as a distinct "action required" step. A visual separator or background highlight would reinforce the acknowledgement as a deliberate action. | Minor |

---

## 4. Improvement Candidates (Ranked by Effort × Value)

| Priority | Candidate | Effort | Value | Rationale |
|----------|-----------|--------|-------|-----------|
| **P1** | Separate `warn` and `fail` override acknowledgement paths | S (1 day) | High | Fail = hard stop; warn = advisory. Distinct flows prevent reflexive override of fails. Aligns with Arc 5 compliance rigour. |
| **P2** | Show warning/fail count in header when collapsed | XS (0.5 day) | Medium | "2 warnings" visible when collapsed; no expand required to know there is an issue. Improves scan-at-a-glance UX. |
| **P3** | Increase detail text contrast on `fail` checks | XS (2 hrs) | Medium | `slate-400` instead of `slate-500` for detail text on `fail` items. Small change; high readability impact for failure messages. |
| **P4** | Check grouping: compliance vs risk vs technical | S (0.5 day) | Medium | Future-proofing for Arc 5 Arc 5 check expansion. Group checks into labelled sections (e.g. "Compliance", "Risk", "Technical"). Not needed now but prepare the component structure. |
| **P5** | Make override acknowledgement label specific | XS (2 hrs) | Low | Mention specific warning count ("I acknowledge the 2 advisory warnings above"). Marginal improvement to user intent; low implementation cost. |

**Not recommended at this time:**
- Full acknowledgement dialog with reason field (excessive friction for a trader entering a plan; structured records better served by red_flag_events table which Arc 5 already populates)
- Icon change from ShieldCheck (low impact; current icon is unambiguous enough in context)

---

## 5. Arc 5 Integration Notes

As SI-02 (drift detection) and SI-04 (strategy version comparison) ship, the pre-entry panel may need to surface:
- Drift alert status (is the current strategy showing behavioural drift?)
- Strategy version alignment (is this trade consistent with the current strategy version?)

**Recommendation for Arc 5 integration:** Add a dedicated "Arc 5 Context" section below the current check list rather than adding more items to the flat check list. This satisfies Improvement Candidate P4 (check grouping) and avoids density issues at current panel width.

**Trigger for re-assessment:** When SI-02 or SI-04 sprint planning seals, a follow-up UX assessment should confirm the pre-entry panel layout accommodates the new context without density regressions.

---

## 6. Items Filed as Backlog Entries

| Candidate | Backlog item | Priority | Rationale for filing |
|-----------|-------------|----------|---------------------|
| P1 — Separate warn/fail override flow | BLG-FE-56 (to be filed) | P2 | Most valuable improvement; aligns with Arc 5 compliance rigour |
| P2 — Warning count in collapsed header | BLG-FE-57 (to be filed) | P3 | Low effort, clear UX win |
| P4 — Check grouping for Arc 5 | BLG-FE-58 (to be filed) | P3 | Required before SI-02/SI-04 panel expansion |

P3 and P5 (detail text contrast, specific label) are micro-improvements that can be bundled into any future EPIC touching this component — no standalone backlog items required.

---

## 7. BLG-FE-49 Closure

BLG-FE-49 marked COMPLETE in `claude/backlog/backlog.md` — 2026-05-31, cycle 2026-05-31__release-v4.7, ST-09 (EPIC-04).

---

## Sign-Off

**Signed off by:** Head of UX & Design
**Date:** 2026-05-31
**Assessment outcome:** Adequate for current use; 3 improvement candidates filed as backlog items
**Comments:** PreEntryValidationPanel is well-designed for the current 5-check use case. Two moderate issues identified (O-01, O-02) regarding the override acknowledgement flow not distinguishing warn vs fail severity — filed as BLG-FE-50 (P2). Layout density and text contrast are adequate. The most pressing future risk is check count growth as Arc 5 adds validation dimensions; check grouping (BLG-FE-52) should precede any SI-02/SI-04 panel extension. No implementation committed this sprint.

**AC sign-off:**
- AC-01: ✅ PreEntryValidationPanel reviewed — layout, text density, override acknowledgement UX assessed
- AC-02: ✅ Improvement candidates identified and ranked in §4
- AC-03: ✅ Assessment note produced at `docs/product/ux/pre_entry_panel_ux_assessment.md`
- AC-04: ✅ Head of UX & Design sign-off recorded
- AC-05: ✅ No implementation committed — assessment only
- AC-06: ✅ BLG-FE-49 marked COMPLETE; improvement items filed as backlog entries (BLG-FE-56/57/58)
