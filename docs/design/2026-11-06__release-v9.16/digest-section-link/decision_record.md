**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-11-06__release-v9.16
**Stories:** ST-04 (EPIC-01, BLG-FE-253)

# Decision Record — Section Link from the Weekly Digest to Strategy Compliance

## 1. Problem

The SI-05 weekly digest reports a "Top rule breach" with the pre-entry pass rate and override rate. Its footer has two page-level links, Risk Dashboard and Red Flag Journal (`si05_digest_service.py` `_format_deep_links()`). Journey map F-04 (`docs/ux/si05_user_journey_map.md`) says the user must find the rule breakdown by hand after following the Risk Dashboard link.

The slice assumes a "pre-entry validation" section on the Risk Dashboard. There isn't one. `risk_dashboard.md` v0.1.15 has heat, drawdown, grace period, position risk, sector concentration, exposure trend and prospective heat, and nothing from `pre_entry_validation_log`. The Top Rule Breach figure, with the override rate and red-flag frequency, is shown in **Analytics §19, Arc 5 Signal Compliance** (`Arc5ComplianceSection.js`, `GET /analytics/arc5-compliance`).

## 2. Decision

**Product Owner decision (the user, in session, 2026-11-06):** add a third digest link to the Analytics section. The Risk Dashboard link keeps pointing at the top of its page.

### 2.1 Section query

- **Format:** `?section=<id>` on the page route. With the hash router: `{FRONTEND_URL}/#/PerformanceAnalytics?section=strategy-compliance`.
- **First id:** `strategy-compliance`, on the wrapper of the §19 section (`id="strategy-compliance"`, plus `data-testid="analytics-section-strategy-compliance"`).
- **Mechanism:** a small shared hook (for example `useSectionScroll()`) so other pages can add ids later. This story adds only the one id.

### 2.2 Scroll behaviour (motion; §6 motion rule)

- Scroll **once**, after the section's first render with data or with its error or empty state. Do not scroll while it shows a loading skeleton, because the layout above it is still settling.
- `scrollIntoView({ block: "start" })`. Use `behavior: "smooth"` only when `prefers-reduced-motion` is not set; otherwise jump instantly.
- After scrolling, move focus to the section heading (`tabIndex={-1}`) so keyboard and screen-reader users land in the same place. Do not show a visible focus ring for this programmatic focus.
- No highlight, pulse or other animation.
- If the user scrolls before the section is ready, do not scroll them afterwards.
- **Unknown or missing `section`:** the page loads at the top, as it does now. Show no error.
- The query stays in the URL. Reloading scrolls again, which is acceptable.

### 2.3 Digest footer

`🔗 [Risk Dashboard](…/#/RiskDashboard) · [Red Flag Journal](…/#/RedFlagJournal) · [Strategy Compliance](…/#/PerformanceAnalytics?section=strategy-compliance)`

MarkdownV2 escaping applies to the URL part as now. Only `)` and `\` need escaping. `?` and `=` do not.

## 3. §13 Compliance

Navigation only. No new data, ranking or advice.

## 4. Frontend Spec Impact

- `pages/analytics.md` v2.2 → v2.3: new §19.1 "Section Link", with the id and the behaviour in §2.2.

## 5. Obligations for Sprint Execution

- Backend: `_format_deep_links()` gains the third link, and the existing digest formatting test is updated. No API contract change, because the digest is a Telegram message, not an endpoint response.
- Journey map F-04 is updated to resolved, with the date and this story.

## 6. Testability (CLAUDE.md §2)

Playwright:
- `/#/PerformanceAnalytics?section=strategy-compliance` puts the section in the viewport, and its heading has focus. Run this with reduced motion emulated.
- `?section=unknown` loads at the top with no error.

Unit test: the digest footer contains the Strategy Compliance URL.

## 7. Approval

Head of UX & Design: Approved (agent-mediated, Design Gate Engine, 2026-11-06). Product Owner: Approved (the user, in session, 2026-11-06), Analytics link option.
