**Filed by:** Base44 Frontend Prompt Owner
**Feature slug:** ai-briefing-progressive-disclosure
**Version:** v1
**Story:** ST-12 (BLG-FE-80, EPIC-03, v6.3)
**Filed:** 2026-06-30
**Integration status:** Implemented directly (agent-mediated — no Base44 platform submission)

---

# Base44 Prompt — AI Briefing Progressive Disclosure

## Context

File to modify: `src/components/dashboard/home/AiDailyBriefing.js`

This component renders the AI daily briefing card on the DashboardHome page. It was shipped in v6.2. The existing component shows three content areas always fully expanded:
1. A summary paragraph (market context)
2. An ordered list of signal actions
3. No chat prompt section currently exists

The component fetches via `api.ai.dailyBriefing()` (POST /ai/daily-briefing). Response shape:

```json
{
  "summary": "string | null",
  "actions": [{ "type": "MONITOR|EXIT|ENTER|HOLD", "ticker": "string", "description": "string" }],
  "generated_at": "ISO8601 string | null",
  "advisory": true,
  "model": "string | null"
}
```

Current imports: `useState` from react; `api` from base44Client; `RefreshCw`, `AlertTriangle` from lucide-react.

Existing data-testid attributes that must be preserved:
- `ai-daily-briefing-card` — outer wrapper div
- `regenerate-briefing-btn` — regenerate button
- `briefing-loading` — loading skeleton
- `briefing-error` — error paragraph
- `briefing-empty` — empty state paragraph
- `briefing-content` — outer div wrapping all sections (when briefing loaded)
- `briefing-actions` — `<ol>` element for action list
- `briefing-no-actions` — empty actions paragraph

## Task

Add expand/collapse progressive disclosure to `AiDailyBriefing.js`. Wrap the briefing content in three collapsible sections:

1. **Market Context** — contains `briefing.summary` paragraph
2. **Signals** — contains `briefing.actions` ordered list (or no-actions fallback)
3. **Ask the AI** — a new section with an inline chat input that calls `api.ai.chat(question, briefing.summary)`

## Requirements

### Section structure

Each section is a `<div>` with:
- A `<button>` toggle showing the section label and a chevron icon (ChevronDown when expanded, ChevronRight when collapsed)
- The section content, rendered only when expanded (`!collapsed`)

Toggle button must have:
- `aria-expanded={!collapsed}` attribute
- `data-testid="section-toggle-{sectionKey}"` where sectionKey is: `market_context`, `signals`, `chat_prompt`

Section content wrapper must have:
- `data-testid="section-content-{sectionKey}"`

### localStorage persistence

- Key: `ai-briefing-collapsed-sections-v1` (versioned to handle future schema changes)
- Value: JSON object mapping sectionKey → boolean (`true` = collapsed)
- Read on component mount (lazy initialiser to `useState`)
- Write on every toggle
- Default state when no localStorage entry: all sections expanded (empty object `{}` → all keys absent → all expanded)

### Chat Prompt section

The "Ask the AI" section contains:
- A text input (`data-testid="briefing-chat-input"`, placeholder "Ask about today's briefing…")
- A send button (`data-testid="briefing-chat-send"`) — disabled when input is empty or loading
- Error state: `<p data-testid="briefing-chat-error">` when API call fails
- Response: `<p data-testid="briefing-chat-response">` when response received
- Calls `api.ai.chat(question.trim(), briefing.summary || null)`
- Enter key submits (when not loading)

### Default state

When localStorage has no entry for this key, all three sections must be expanded. This ensures no UX regression for new users.

### Icons

Add imports: `ChevronDown`, `ChevronRight`, `Send` from `lucide-react`. Remove unused `AlertTriangle` import.

### Styling

Match existing slate-900 / slate-700 / slate-300 colour scheme. Section toggle buttons: `text-xs font-semibold text-slate-400 hover:text-slate-300 hover:bg-slate-800`. Sections bordered with `border border-slate-700 rounded-lg overflow-hidden`.

## Acceptance criteria checklist

- [ ] AC-01: Each of the three sections has a visible expand/collapse toggle
- [ ] AC-02: Sections collapse and expand without losing content (content rerenders correctly after expand)
- [ ] AC-03: Collapse state persists via localStorage with key `ai-briefing-collapsed-sections-v1`
- [ ] AC-04: Default state (no localStorage entry) is all sections expanded
- [ ] AC-05: Playwright test `SC-PD-05`: expand all → collapse market context → reload → verify market context still collapsed, other sections still expanded

## Playwright test coverage

File: `tests/e2e/ai-briefing-progressive-disclosure.spec.js`

Tests to include:
- SC-PD-01: All three section headers visible after briefing loads
- SC-PD-02: Toggle buttons have `aria-expanded` attribute
- SC-PD-03a/b/c: Collapse hides content; expand restores it (for each section)
- SC-PD-04: Default state all expanded when localStorage empty
- SC-PD-05: AC-05 — expand all → collapse market context → reload → market context still collapsed

Mock `POST /ai/daily-briefing` to return `BRIEFING_PAYLOAD` with summary and 2 actions. Use `page.addInitScript` to control localStorage state. Use `page.reload()` for the reload step.
