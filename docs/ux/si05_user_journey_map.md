**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-15
**Source:** ST-10 (EPIC-03, v5.5) — BLG-FE-65

---

# User Journey Map: SI-05 Telegram Digest → App Action

## Overview

This document maps the user journey from receiving the SI-05 weekly strategy integrity digest in Telegram to taking action in the app. The walkthrough was conducted on 2026-06-15 using a live digest delivered to staging.

**Digest received:** 2026-06-15  
**Environment:** Staging (`trading-assistant-api-staging.onrender.com`)

---

## Digest Message (Observed)

```
---
📋 Strategy Integrity

✅ Pre-entry pass rate (7d): N/A
🚨 Red flag events (7d): 0
⚠️ Override rate (7d): N/A
🔍 Top rule breach: None

No pre-entry validation data available this week.
📊 Closed trades: 14 / Gate 1: 20 / Gate 2: 50 / Gate 3: 100
```

---

## 1. Entry Points

**Entry points in the digest: None.**

The digest contains no hyperlinks or references to specific app screens. It is a read-only informational message. The user receives the digest passively and must navigate to the app independently if they wish to act on its contents.

---

## 2. Navigation Steps (Digest → App Action)

Because there are no links, every journey from digest to app action requires the user to open the app manually. The steps for each actionable item in the digest are:

| Digest Item | Intended App Destination | Navigation Steps |
|-------------|-------------------------|------------------|
| Pre-entry pass rate | Risk Dashboard → Pre-entry Validation section | 1. Open app → 2. Navigate to Risk Dashboard → 3. Find pre-entry validation panel |
| Red flag events (7d) | Red Flag Journal | 1. Open app → 2. Navigate to Portfolio → 3. Find Red Flag Journal section |
| Override rate | Risk Dashboard | 1. Open app → 2. Navigate to Risk Dashboard |
| Top rule breach | Risk Dashboard → Pre-entry validation rule breakdown | 1. Open app → 2. Navigate to Risk Dashboard → 3. Find rule breach detail |
| Closed trades / Gate progress | System Status or Portfolio | 1. Open app → 2. Navigate to System Status page |

**Minimum steps to reach any actionable screen: 3** (open app → navigate to section → find specific panel). No digest item can be acted on in fewer than 3 steps.

---

## 3. Friction Findings

### F-01 — No deep links from digest to app (HIGH)
The digest contains zero links to the app. A user reading "Red flag events: 3" or "Override rate: 45%" has no direct path to the relevant app screen. They must remember where in the app to find that information and navigate there manually. This is the primary friction point.

**Impact:** High — defeats the purpose of the digest as an actionable alert. The user is informed but not directed.  
**Recommended fix:** Add one deep link per digest section pointing to the relevant app screen (e.g. "View Risk Dashboard →" after the strategy integrity block).  
**Backlog item:** BLG-FE-73 (filed — see §4)

### F-02 — N/A values with no explanation path
Pass rate and override rate show "N/A" with the explanation "No pre-entry validation data available this week." The user has no way to determine whether this is expected (no trades triggered validation) or a system issue (validation logging broken) without opening the app and checking manually.

**Impact:** Medium — creates ambiguity. A user who has been active that week may be confused about why no data is shown.  
**Recommended fix:** Add a parenthetical to the N/A line indicating the reason (e.g. "N/A (no validation events this week)" vs "N/A (data unavailable — check System Status)").  
**Backlog item:** BLG-FE-74 (filed — see §4)

### F-03 — Gate progress line has no context for new users
The "Closed trades: 14 / Gate 1: 20 / Gate 2: 50 / Gate 3: 100" line is compact but opaque. A user who hasn't read the documentation doesn't know what the gates represent or why they matter.

**Impact:** Low — existing users understand the gate concept; new users may be confused.  
**Recommended fix:** The gate line could include a brief label on first receipt, or a "What are gates?" link. Low priority given current single-user context.  
**Backlog item:** not filed (P4 — accept risk for now)

---

## 4. Backlog Items Filed

| ID | Title | Priority |
|----|-------|----------|
| BLG-FE-73 | Add deep links from SI-05 digest to relevant app screens | P2 |
| BLG-FE-74 | Clarify N/A pass rate reason in SI-05 digest message | P3 |

---

## 5. Sign-Off

- **Signed off by:** Head of UX & Design
- **Date:** 2026-06-15
- **Comments:** Walkthrough completed on live staging digest received 2026-06-15. Primary finding: no entry points from digest to app — BLG-FE-73 filed. Secondary finding: N/A ambiguity — BLG-FE-74 filed. Gate progress line noted as low-priority friction. Journey map complete.
