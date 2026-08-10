**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-10 (ST-16, BLG-FE-65, v8.5 — full re-walkthrough; original 2026-06-15 findings superseded by BLG-FE-73/74 fixes shipped v5.6, 2 days after the original walkthrough); prior — 2026-06-15 (ST-10, EPIC-03, v5.5 — initial walkthrough)
**Source:** ST-16 (EPIC-05, v8.5) — BLG-FE-65 (re-walkthrough); originally ST-10 (EPIC-03, v5.5) — BLG-FE-65

---

# User Journey Map: SI-05 Telegram Digest → App Action

## Overview

This document maps the user journey from receiving the SI-05 weekly strategy integrity digest in Telegram to taking action in the app.

**2026-08-10 re-walkthrough method:** No live production/staging Telegram delivery is reachable from this execution environment. The message content below is reconstructed directly from the current shipped implementation (`backend/services/si05_digest_service.py`, format spec `docs/product/decisions/si05-telegram-message-format-spec.md`, BLG-GOV-86) rather than a live-received message — the same class of substitution used elsewhere this sprint where live/staging access is unavailable (see `st03_sec02_false_positive_rate_assessment.md`). This re-walkthrough was triggered by discovering, while reviewing this document for ST-16, that it was stale: **both of its two HIGH/MEDIUM friction findings (F-01, F-02) were already fixed** in `v5.6` (`BLG-FE-73`/`BLG-FE-74`, shipped 2026-06-17 — 2 days after the original 2026-06-15 walkthrough), but the document itself was never updated to reflect that, leaving it describing a pre-fix digest as the current state.

---

## Digest Message (Reconstructed from current shipped code)

```
---
📋 Strategy Integrity

✅ Pre-entry pass rate (7d): N/A (no validation events this week)
🚨 Red flag events (7d): 0
⚠️ Override rate (7d): N/A (no validation events this week)
🔍 Top rule breach: None

No pre-entry validation events this week.

🔗 Risk Dashboard · Red Flag Journal

📊 Closed trades: 14 / Gate 1: 20 / Gate 2: 50 / Gate 3: 100
```

Two structural changes since the 2026-06-15 message: (1) the `N/A` lines now carry a parenthetical reason (`no validation events this week` / `data unavailable`, `_format_pass_rate`/`_format_override_rate` in `si05_digest_service.py`) — this is BLG-FE-74's fix; (2) a new deep-link footer line (`🔗 Risk Dashboard · Red Flag Journal`, `_format_deep_links()`) links directly to `{FRONTEND_URL}/#/RiskDashboard` and `{FRONTEND_URL}/#/RedFlagJournal` — this is BLG-FE-73's fix. The deep-link footer is conditional on the `FRONTEND_URL` env var being configured; it silently omits itself if not (`_format_deep_links()` returns `""` when unset) — confirmed configured and working end-to-end (including a `HashRouter /#/` prefix fix and a MarkdownV2 decimal-escape fix) per `BLG-FE-75`'s dedicated staging-verification record (shipped 2026-06-17, `backlog_archive.md`).

---

## 1. Entry Points

**Entry points in the digest: 2** (superseding the original "None" finding).

The deep-link footer provides direct navigation to `Risk Dashboard` and `Red Flag Journal` — the two screens the digest content is most actionable against. `Weekly Digest` gain/plan-count context and the `Closed trades / Gate progress` line still have no direct link.

---

## 2. Navigation Steps (Digest → App Action)

| Digest Item | Intended App Destination | Navigation Steps (current) | Navigation Steps (2026-06-15, pre-fix) |
|-------------|---------------------------|------------------------------|--------------------------------------------|
| Pre-entry pass rate | Risk Dashboard → Pre-entry Validation section | **1** — tap `Risk Dashboard` deep link | 3 |
| Red flag events (7d) | Red Flag Journal | **1** — tap `Red Flag Journal` deep link | 3 |
| Override rate | Risk Dashboard | **1** — tap `Risk Dashboard` deep link | 3 |
| Top rule breach | Risk Dashboard → Pre-entry validation rule breakdown | **1** to Risk Dashboard, then manual scroll to rule breakdown (no anchor-level deep link) | 3 |
| Closed trades / Gate progress | System Status or Portfolio | 3 — unchanged, still no deep link | 3 |

**Minimum steps to reach any actionable screen: 1** (down from 3) for 3 of the 5 digest items; the 4th (top rule breach) drops from 3 to effectively ~1.5 (lands on the right page, still requires scroll/find); only the 5th (closed trades / gate progress) is unchanged.

---

## 3. Friction Findings (2026-08-10 re-assessment)

### F-01 — No deep links from digest to app (HIGH) — **RESOLVED**
Original finding: the digest contained zero links, forcing manual navigation for every item. **Status: fixed** by `BLG-FE-73` (shipped v5.6, 2026-06-17) — confirmed live in `si05_digest_service.py`'s `_format_deep_links()`. Superseded, no longer an open finding.

### F-02 — N/A values with no explanation path (MEDIUM) — **RESOLVED**
Original finding: `N/A` values gave no reason (data-unavailable vs. no-events-this-week). **Status: fixed** by `BLG-FE-74` (shipped v5.6, 2026-06-17) — confirmed live in `_format_pass_rate()`/`_format_override_rate()`'s `na_reason` parameter, distinguishing `no_events` vs `data_unavailable`.

### F-03 — Gate progress line has no context for new users (LOW) — **STILL OPEN, UNCHANGED**
The `Closed trades: 14 / Gate 1: 20 / Gate 2: 50 / Gate 3: 100` line remains compact and opaque to a first-time reader; no deep link or explanatory context was added by either v5.6 fix (out of scope for both). Disposition unchanged from the original walkthrough: low priority, not filed (P4 — accept risk for now), given the current single-user context.

### F-04 — New: deep links land on the page, not the specific panel (LOW) — **NEW FINDING**
The `Risk Dashboard` deep link (`#/RiskDashboard`) lands on the top of the Risk Dashboard page, not scrolled/anchored to the pre-entry-validation or override-rate panel specifically — for the "Top rule breach" digest item in particular, the user still has to find the rule-breakdown section manually after arriving. This is a real, but minor, residual gap: it took step count from 3 to ~1.5 for that item, not fully to 1 like the other two Risk-Dashboard-bound items.

**Impact:** Low — the deep link still gets the user to the right page in one action; only fine-grained in-page scrolling remains manual.
**Recommended fix:** Add a URL fragment/anchor (e.g. `#/RiskDashboard?section=pre-entry-validation`) if `RiskDashboard.js` supports scroll-to-anchor; otherwise low priority given the coarse-grained link already resolved the majority of the original friction.
**Backlog item:** not filed — low priority, and the fix approach depends on whether `RiskDashboard.js` already supports a query-param/anchor scroll target (not verified in this pass; a follow-up story would need to check that first before scoping the fix). Filed as a documented observation only, per this story's "any *significant* friction filed" AC threshold — this does not clear that bar on its own.

---

## 4. Backlog Items Filed

| ID | Title | Priority | Status |
|----|-------|----------|--------|
| BLG-FE-73 | Add deep links from SI-05 digest to relevant app screens | P2 | ✅ Shipped v5.6 |
| BLG-FE-74 | Clarify N/A pass rate reason in SI-05 digest message | P3 | ✅ Shipped v5.6 |

No new backlog item filed this re-walkthrough — F-04 does not meet the "significant friction" threshold this story's AC requires for filing (see F-04 disposition above); F-03 remains an accepted, unfiled low-priority item from the original walkthrough.

---

## 5. Sign-Off

- **Signed off by:** Head of UX & Design (agent-mediated, per `execution_prompt.md` §5.3)
- **Date:** 2026-08-10
- **Comments:** Re-walkthrough triggered by finding the document stale during ST-16 review (both prior HIGH/MEDIUM findings already fixed 2 days after the original walkthrough, document never updated). Current entry-point count: 2 (was 0). Minimum navigation steps: 1 (was 3) for 3 of 5 digest items. One new low-priority observation (F-04) recorded, does not meet the filing threshold. F-03 unchanged, remains an accepted low-priority gap. Journey map re-verified complete and current as of 2026-08-10.
