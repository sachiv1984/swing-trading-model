**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-16__release-v9.13
**Story:** ST-22 (EPIC-03, BLG-FE-208)

# Decision Record — Useful / Not-Useful Rating on AI Chat Answers

## 1. Problem

`metrics_definitions.md` § AI Chat Engagement defines a Response Acceptance Rate: answers rated useful ÷ answers rated. The AI Trade Advisor widget has no rating control and nothing stores a rating. The measure is therefore "not instrumented", and the 2027-01-03 AI feature usage review cannot report it.

## 2. Decision

### 2.1 Which answers can be rated

Only AI answers that the server identifies as a model response. `POST /ai/chat` returns an `answer_id` for those (the `claude_audit_log` row the rating attaches to). Fixed fallback messages carry none and get no control: "Unable to get a response…", "Unable to load portfolio data.", and "unavailable — ANTHROPIC_API_KEY not configured". User bubbles never get a control.

### 2.2 Control

It follows the trade-plan thesis feedback pattern (`trade_plan.md` §5b, v6.5 design source):

- Placed directly under the AI bubble, left-aligned, `gap-3`, `mt-1`.
- Two buttons: `ThumbsUp` + "Useful" and `ThumbsDown` + "Not useful". Lucide 12 px icons, `text-xs`.
- Each is a real `<button>` with `aria-pressed`. The group has `role="group"` and `aria-label="Rate this answer"`.
- `data-testid="chat-rating"` on the group; `chat-rating-useful` and `chat-rating-not-useful` on the buttons.

### 2.3 States

| State | Display |
|-------|---------|
| Unrated | Both buttons `text-slate-400`, hover `text-slate-200` |
| Saving | Both disabled, clicked one shows its selected colour |
| Rated (persisted) | Selected: Useful `text-emerald-400`, Not useful `text-rose-400`. Both stay disabled (one rating per answer). A muted "Thanks — recorded." follows for 3 s, then the control remains in its selected state. |
| Save failed | Both re-enabled and unselected. Inline `text-xs text-rose-400` "Couldn't save your rating. Try again." (`role="status"`) |
| Already rated (server reports a prior rating, e.g. 409) | Shown as Rated with the stored value |

**Tokens:** the chat panel is a fixed dark surface in both themes (`bg-slate-900`; bubbles `bg-slate-700`, `positions.md` §AI Trade Advisor Widget). So single dark tokens apply here, as for the existing bubbles. On `slate-900`: `slate-400` 6.96:1, `emerald-400` 9.29:1, `rose-400` 6.63:1.

### 2.4 Scope

Rating does not change the answer, the conversation or any record other than the rating itself. The widget's history still clears on close. The rating is stored server-side, so it persists after close.

## 3. §13 Compliance

The rating measures answer usefulness and is not an input to any signal, score or recommendation (`decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md`, PASS). The widget's §13 constraint is unchanged: no trade action is executable from the widget.

## 4. Frontend Spec Impact

`positions.md` v2.19 → v2.20: §AI Trade Advisor Widget gains §Answer Rating, and its States table gains the rating states.

## 5. Obligations for Sprint Execution

- `POST /ai/chat` returns `answer_id` for model responses. Update `ai_endpoints.md` and `openapi.yaml` in the same commit.
- The rating write route follows RISK-04's chain (contract `##` heading, `openapi.yaml`, `routers/test.py`, `SystemStatus.js` fallback count, `SC-SS-01b`). Storage needs its `data_model.md` DS entry with Live Confirmation on staging and production (AC 2, RISK-01).
- A second rating for the same `answer_id` is rejected, not overwritten (AC 1 "once").

## 6. Testability (CLAUDE.md §2)

- Playwright (AC 1): rate an answer Useful. Assert the POST, the selected state and disabled buttons. Re-open the widget, ask again, and assert the rating endpoint still holds the first rating (unit test for persistence).
- Playwright: a fallback message ("Unable to get a response…") shows no `chat-rating`.
- Beyond the slice ACs (add these or file a backlog item before the PR opens): the save-failed state re-enables the buttons.

## 7. Approval

Head of UX & Design: confirmed, 2026-10-16.
Product Owner: confirmed, 2026-10-16.
