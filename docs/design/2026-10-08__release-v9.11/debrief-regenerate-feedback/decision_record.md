**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-08__release-v9.11
**Story:** ST-05 (EPIC-01, BLG-FE-205)

# Decision Record — Debrief Regenerate Button, Failure Message and Generated Time

## 1. Problem

In the Post-Trade Debrief section (`TradeDebrief.js`, `trade_history.md` §Post-Trade Debrief):

- **Regenerate is hard to recognise.** It is a `ghost` button in muted slate text with no border or background, so it reads as plain text in both themes.
- **Regenerate failures are silent.** The POST `mutationFn` does not check `res.ok`. A 500 resolves as "success", and the error message only exists in the empty state, which is hidden once a debrief exists.
- **The generated time is never shown.** `generated_at` is in the `GET`/`POST /trades/{id}/debrief` response, but nothing renders it, so a user cannot tell whether Regenerate did anything.

## 2. Decision

### 2.1 Regenerate button

- Use the same `outline` variant as the empty-state **Generate Debrief** button, at `size="sm"` and `text-xs`. This gives a visible border and background from existing tokens in both themes. No new colour.
- Label: "Regenerate". While pending: "Regenerating…" and disabled (unchanged).
- Keep it the only action in the populated state (§13 Condition 4: no other affordance).

### 2.2 Generated time

- Shown on the same row as Regenerate, left of the button, in muted `text-xs`: **"Generated {relative time}"** (for example "Generated 3 min ago"). This is the same pattern as Research's "Updated {relative time}" line. That page has a local `relativeTime` helper, not a shared one, so the story may reuse it or move it into `src/lib/format`.
- `title` attribute holds the absolute local date and time.
- `data-testid="debrief-generated-at"`.
- If `generated_at` is null or missing, the label is omitted. No placeholder.
- After a successful regenerate, the label updates from the new response.

### 2.3 Regenerate failure

- The mutation treats a non-2xx response as an error.
- On error in the **populated** state:
  - The existing debrief stays on screen, unchanged.
  - An inline message appears under the action row in the existing error tone (`text-rose-400`, `text-xs`): **"Could not regenerate the debrief. The previous version is still shown. Try again shortly."**
  - `data-testid="debrief-regenerate-error"`, with `role="status"` so screen readers announce it.
  - The message clears on the next Regenerate click.
- The empty-state error behaviour is unchanged.

### 2.4 Layout

```
[summary text]
[Focus area …]
──────────────────────────────────────────────
Generated 3 min ago                [ Regenerate ]
Could not regenerate the debrief. The previous version is still shown. …   ← error only
```

No change to the section label, AI-generated badge, violet accent border or skeleton.

## 3. States

| State | Action row | Message |
|-------|-----------|---------|
| Populated, idle | "Generated …" + Regenerate | none |
| Regenerating | "Generated …" (previous) + "Regenerating…" (disabled) | none |
| Regenerate succeeded | "Generated just now" + Regenerate | none |
| Regenerate failed | "Generated …" (unchanged) + Regenerate | regenerate error |

## 4. §13 Compliance

Covered by the existing debrief review (`docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md`, CONDITIONAL). No new AI call. The only action stays Regenerate (Condition 4). The timestamp and error message are status information, not affordances.

## 5. Accessibility

- The outline button must pass the axe colour-contrast check for its text and its border (≥3:1 non-text contrast) in both themes. The ST-05 AC requires an axe scan of the debrief section.
- The error message is announced (`role="status"`).

## 6. Frontend Spec Impact

`trade_history.md` v1.14 → v1.15: §Post-Trade Debrief → Populated State and Loading / Error.

## 7. Testability (CLAUDE.md §2)

Playwright, mocked API:

1. Regenerate has a visible border or background in dark and light themes, and the axe scan of `trade-debrief-section` reports no colour-contrast violations.
2. A mocked 500 on POST shows `debrief-regenerate-error` and keeps `debrief-content` with the original text.
3. After a successful mocked POST with a newer `generated_at`, `debrief-generated-at` changes.

## 8. Approval

Head of UX & Design: confirmed, 2026-10-08.
Product Owner: confirmed, 2026-10-08.
