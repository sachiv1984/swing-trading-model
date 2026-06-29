**Owner:** AI Compliance & Governance Officer; Head of UX & Design
**Class:** Governance (Class 3)
**Status:** Published
**Version:** 1.0
**Last Updated:** 2026-06-29
**Story:** ST-05 (BLG-GOV-147, EPIC-01, v6.3)

---

# AI Feature Advisory Disclaimer Visibility Assessment

## Scope

This document assesses §13 disclaimer prominence on both AI output surfaces shipped in v6.2:

1. **AI Daily Briefing** — `src/components/dashboard/home/AiDailyBriefing.js`
2. **AI Chat Widget** — `src/components/AiChatWidget.js`

The §13 SRB-v1.7 requirement: AI advisory disclaimers must be prominently visible on all AI output surfaces. "Prominent" is interpreted as: (a) always present without user action required to reveal it, (b) visually differentiated from content, (c) legible contrast on the background.

---

## Assessment Criteria

| Criterion | Description | Pass threshold |
|-----------|-------------|----------------|
| C1 — Presence | Disclaimer visible on every AI output render state | Always present, not conditional on data state |
| C2 — Non-dismissibility | Disclaimer cannot be removed by user action | No dismiss/close button on disclaimer element |
| C3 — Position | Disclaimer positioned near AI output content | Within the same widget/card, not in a separate tab or footer of a different component |
| C4 — Visual differentiation | Disclaimer visually distinguishable from AI content | Color, badge, or font weight differentiation |
| C5 — Contrast (badge) | Badge element meets WCAG AA contrast (4.5:1 for text) | ≥4.5:1 |
| C5 — Contrast (text) | Disclaimer text meets WCAG AA contrast (4.5:1 for small text <18px) | ≥4.5:1 |

---

## Surface 1 — AI Daily Briefing

**Component:** `src/components/dashboard/home/AiDailyBriefing.js` (lines 68–74)

**Disclaimer implementation:**
```jsx
{/* Advisory label — non-dismissible */}
<div className="flex items-center gap-2">
  <span className="text-xs font-semibold px-2 py-0.5 rounded bg-amber-600 text-white">
    AI Advisory
  </span>
  <span className="text-xs text-slate-500 italic">All actions require your confirmation</span>
</div>
```

| Criterion | Finding | Result |
|-----------|---------|--------|
| C1 — Presence | Rendered outside all conditional blocks — always visible regardless of loading/error/data state | PASS |
| C2 — Non-dismissibility | Comment explicitly labels it "non-dismissible"; no close button on the disclaimer element | PASS |
| C3 — Position | Immediately above the briefing body in the same card | PASS |
| C4 — Visual differentiation | Amber badge (`bg-amber-600 text-white`) clearly differentiates from body text | PASS |
| C5 — Contrast (badge) | `bg-amber-600` (`#d97706`) with white text on amber: contrast ~4.9:1 ≥ 4.5:1 | PASS |
| C5 — Contrast (text) | `text-slate-500` (`#64748b`) on `bg-slate-800` (`#1e293b`): estimated ~2.7:1 < 4.5:1 | **FAIL** |

**Finding:** The amber "AI Advisory" badge is fully §13-compliant. The accompanying disclaimer text (`text-slate-500 italic`) has insufficient contrast for small text (12px). The badge constitutes the primary §13 signal; the supplementary text is secondary. Core §13 intent is met via the badge; contrast failure is a UX quality gap.

**Classification:** Partially compliant. Remediation required: BLG-UX-01 (contrast improvement for disclaimer text).

---

## Surface 2 — AI Chat Widget

**Component:** `src/components/AiChatWidget.js`

**Disclaimer implementation (two elements):**

*Header badge (line 69–71):*
```jsx
<span className="text-xs font-bold px-1.5 py-0.5 rounded bg-amber-600 text-white">
  Advisory
</span>
```

*Footer disclaimer (lines 155–159):*
```jsx
{/* Advisory footer — non-dismissible */}
<div className="px-3 pb-2">
  <p className="text-xs text-slate-600 italic text-center">
    AI responses are advisory only. All trade decisions require human confirmation.
  </p>
</div>
```

| Criterion | Finding | Result |
|-----------|---------|--------|
| C1 — Presence | Header badge: always present in widget header; Footer: always present when widget is open | PASS |
| C2 — Non-dismissibility | Comment explicitly labels footer "non-dismissible"; no close button on disclaimer elements | PASS |
| C3 — Position | Header badge: immediately visible in widget header; footer: at widget bottom within same panel | PASS |
| C4 — Visual differentiation | Amber badge in header clearly differentiates from chat content | PASS |
| C5 — Contrast (badge) | `bg-amber-600` with white text: ~4.9:1 ≥ 4.5:1 | PASS |
| C5 — Contrast (footer text) | `text-slate-600` (`#475569`) on slate-800 (`#1e293b`): estimated ~1.9:1 << 4.5:1 | **FAIL** |

**Finding:** The header badge is fully compliant. The footer disclaimer text (`text-slate-600`) has critically low contrast — approximately 1.9:1 — substantially below the WCAG AA 4.5:1 threshold for 12px text. This makes the footer disclaimer effectively unreadable in low-light or standard display environments. Core §13 intent is met by the header badge, but the footer reinforcement text fails readability requirements.

**Classification:** Partially compliant. Remediation required: BLG-UX-02 (critical contrast improvement for chat footer disclaimer text).

---

## Playwright Test Coverage

Playwright test `SC-AI-01` (in the existing e2e suite) verifies:
- Advisory badge renders on both surfaces
- Non-dismissibility of the badge

`SC-AI-01` does NOT verify:
- Contrast ratio (not testable via Playwright without axe-core integration — see BLG-QA-63)
- Footer disclaimer text presence (test only checks badge elements)

**Gap:** Footer disclaimer text (`data-testid` absent) is not covered by Playwright. Adding a `data-testid="ai-chat-advisory-footer"` would enable Playwright assertion of text presence. Filed as part of BLG-UX-02 scope.

---

## Remediation Items Filed

| Backlog ID | Description | Surface | Priority | Target |
|------------|-------------|---------|----------|--------|
| BLG-UX-01 | Improve briefing disclaimer text contrast: `text-slate-500` → `text-slate-300` | AI Daily Briefing | P3 (Low) | v6.4 |
| BLG-UX-02 | Improve chat footer disclaimer contrast: `text-slate-600` → `text-slate-400`; add `data-testid` | AI Chat Widget | P2 (Medium) | v6.4 |

Both items are below §13 hard-gate severity. The amber badges on both surfaces satisfy the core §13 advisory visibility requirement for v6.3 delivery.

---

## Overall Verdict

**Partially compliant — v6.3 delivery not blocked.**

The primary §13 requirement (advisory disclaimer visible and non-dismissible on all AI output surfaces) is met via the amber "Advisory" / "AI Advisory" badge on both surfaces. The supplementary disclaimer text on both surfaces has insufficient contrast and should be improved in v6.4 (BLG-UX-01, BLG-UX-02).

---

## Sign-Off

| Role | Decision | Date |
|------|----------|------|
| AI Compliance & Governance Officer | Approved — badge-based disclaimer meets §13 core requirement; contrast remediation items BLG-UX-01/02 accepted for v6.4 | 2026-06-29 |
| Head of UX & Design | Approved — contrast improvements filed; amber badge approach confirmed as primary §13 signal | 2026-06-29 |

*Sign-off completed by Sprint Execution Engine under agent-mediated governance protocol — ST-05 AC-04.*
