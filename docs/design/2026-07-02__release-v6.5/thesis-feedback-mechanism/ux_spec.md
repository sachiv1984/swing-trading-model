**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-02
**Cycle:** 2026-07-02__release-v6.5
**Story:** ST-07 (BLG-FE-46)
**Approved by:** Product Owner — 2026-07-02

---

# UX Spec — Claude Thesis Generation Feedback Mechanism

## Purpose

The Trade Plan form's "Improve with AI" button (`improve-with-ai-btn`, shipped v4.0, `POST /trade-plans/generate-plan`, Claude Haiku 4.5) populates `setup_thesis` and related fields and sets an `isAiDraft` flag, surfaced as the "AI draft" badge. Once generated, the system has no signal on whether that output was actually useful — it cannot distinguish a thesis the trader kept as-is because it was good from one they never got round to fixing. This spec adds a lightweight binary feedback control so thesis quality can be tracked over time (feeds ST-08's `thesis_adoption_rate` metric and future prompt-tuning work).

---

## Placement

Feedback control renders directly beneath the "Setup Thesis" label row, left-aligned under the existing "AI draft" badge, only when an AI draft is present:

```
┌───────────────────────────────────────────────────────────┐
│ SETUP THESIS               [✨ AI draft]  [Generate thesis] [✨ Improve with AI] │
│ 👍 Useful   👎 Not useful                                    │
│ ┌───────────────────────────────────────────────────────┐ │
│ │ <textarea — setup_thesis content>                      │ │
│ └───────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────┘
```

Rationale: attaching feedback to the badge row (rather than a modal or toast) keeps it in the trader's direct line of sight without interrupting the form-filling flow, consistent with this page's existing inline-affordance pattern (badge, generate buttons all sit in the same row).

---

## Trigger Condition

| State | Feedback control visible? |
|-------|---------------------------|
| `isAiDraft === true` (AI draft present, not yet edited) | Yes |
| `isAiDraft === false` (no AI draft, or user has edited the textarea since generation) | No |
| Feedback already submitted for the current AI draft | Control remains visible but shows the confirmed state (see States) |

The control only appears for content produced by **"Improve with AI"** (Claude-backed, `isAiDraft = true`). The pre-existing local **"Generate thesis"** button (`generate-thesis-btn`) is a client-side template fill with no model call and is out of scope — it also sets `isAiDraft = true` today, which conflates the two; see Note below.

**Note (spec correction, in scope for ST-07):** `isAiDraft` is currently set by both `generate-thesis-btn` (local template, no LLM call) and `improve-with-ai-btn` (Claude Haiku 4.5). The feedback control must only appear for genuine Claude-generated drafts. Implementation must distinguish the two — e.g. a separate `isClaudeDraft` flag set only by the `improve-with-ai-btn` handler — so feedback is never solicited for template-only content. This is a build-time correction to existing state, not a new design decision; flagged here so Sprint Execution does not silently inherit the conflated flag.

---

## Control Design

| Element | Spec |
|---------|------|
| Label | None (icons are self-labelling via text) |
| Useful | `👍 Useful` — thumbs-up icon (`ThumbsUp`, lucide-react, matches existing icon set) + text, `text-xs`, muted slate until selected |
| Not useful | `👎 Not useful` — `ThumbsDown`, same styling |
| Layout | Inline, horizontal, small gap (`gap-3`), consistent with the existing badge/button row's `gap-2` idiom |
| Selected state | Selected option fills with colour (`text-emerald-400` for Useful, `text-rose-400` for Not useful); unselected option dims to `text-slate-500` |
| Post-selection | Both buttons become non-interactive (feedback is single-shot per draft — see States); a brief inline confirmation replaces the pair: `"Thanks — feedback recorded."` in `text-xs text-slate-500`, fading after ~2s back to the dimmed two-option display (selected option remains highlighted, so the trader can still see what they chose) |

---

## States

| State | Behaviour |
|-------|-----------|
| No AI draft (`isAiDraft` false, or the Claude-specific flag per the Note above is false) | Control not rendered |
| AI draft present, no feedback given yet | Both options shown, neither selected, both clickable |
| Feedback given | Selected option highlighted, both options disabled, transient "Thanks — feedback recorded." confirmation |
| Trader edits the thesis textarea after feedback was given | Existing `isAiDraft → false` transition on edit (already implemented) hides the control entirely — a fresh "Improve with AI" call is required to show it again, which resets feedback state for the new draft |
| Trader regenerates via "Improve with AI" again (overwriting a previously-rated draft) | Feedback control resets to the un-rated state — each generation is rated independently |

---

## Data Persistence (AC-02)

Recommended approach for Sprint Execution (design gate does not author backend implementation, but records the intended shape for build continuity, per the `open-positions-panel` precedent):

- Add a `thesis_feedback` column (nullable, `useful` \| `not_useful`) to the `claude_audit_log` row written by the `POST /trade-plans/generate-plan` call that produced the draft (the row already exists per-generation with `plan_id`, `model_id`, `prompt_version` — see `docs/specs/api_contracts/ai_thesis_generation.md`). This avoids a new table and keeps feedback attributable to the exact generation call it rates.
- New endpoint: `POST /trade-plans/{plan_id}/thesis-feedback` — body `{ value: "useful" | "not_useful" }` — updates the most recent `claude_audit_log` row for that `plan_id`. Must ship with the standard same-commit obligations (openapi.yaml, API contract `##` heading, `backend/routers/test.py` registration) per CLAUDE.md §2.

This is a recommendation, not a hard constraint on Sprint Execution's implementation — the binding requirement is AC-02 itself ("feedback data persisted"), not this specific mechanism.

---

## Constraints

- Single-shot per draft — no changing a vote once given for the same generation (avoids ambiguous double-counting in the adoption-rate metric); a new generation is required to re-rate
- §13 does not apply to the control itself — it captures trader sentiment about advisory text, it does not gate, score, or influence trade entry
- No new colour tokens — reuses the existing `emerald-400` / `rose-400` profit/loss-style semantic pair already established elsewhere in the app (positive/negative), applied here to useful/not-useful

---

## Accessibility

- Both buttons are real `<button type="button">` elements (not divs), keyboard-focusable and operable via Enter/Space
- `aria-pressed` reflects selected state once feedback is given
- Confirmation text is plain text (not colour-only) and is announced via existing form live-region conventions if present on this page; if none exist, no new live region is introduced by this change (out of scope — page-wide a11y live-region coverage is a separate concern)
