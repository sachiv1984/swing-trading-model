**Owner:** Product Owner
**Class:** Operational Record (Class 3)
**Status:** Active — Awaiting PO Channel Decision
**Last Updated:** 2026-06-03
**Cycle:** 2026-06-03__release-v5.0
**Story:** ST-09 (EPIC-04, v5.0)
**Backlog ref:** BLG-FE-60

---

# SI-05 Phase 1 — Notification Channel Trade-Off Analysis

**Feature:** SI-05 — Weekly Strategy Integrity Digest
**Decision scope:** Which notification channel to use for SI-05 Phase 1 weekly digest delivery
**Options evaluated:** (A) Telegram (existing v2.4 infrastructure) vs (B) In-app notification (new build)
**Decision required from:** Product Owner

---

## Background

SI-05 Phase 1 will deliver a weekly strategy integrity digest summarising key SI-01 and SI-03 metrics: validation pass rate, override count, and red flag frequency trend. This digest must be delivered to the user on a weekly cadence.

Two delivery channel options have been identified. The Product Owner must record their channel decision in the **Decision Record** section below before ST-10 (message format specification) can proceed.

---

## Option A — Telegram (Existing v2.4 Infrastructure)

### Description

The Telegram digest infrastructure was built in v2.4 and delivers the weekly performance digest. SI-05 could reuse this infrastructure to add a second weekly message (strategy integrity metrics) or combine them into one enhanced weekly digest.

### Implementation effort

| Component | Effort |
|-----------|--------|
| Telegram bot/token setup | ✅ Already configured (v2.4) |
| Scheduled trigger | ✅ Already configured (v2.4) |
| New message template | S (~3 hrs) — format spec via ST-10 |
| SI-01/SI-03 data integration | S (~3 hrs) — call existing API endpoints |
| **Total new effort** | **~6 hrs** |

### Format and constraints

Telegram imposes:
- **Character limit:** ~4,096 characters per message (Markdown-formatted). Well within budget for a summary digest.
- **Markdown subset:** Bold (`*text*`), italic, code blocks, links. No tables, no HTML.
- **No interactive elements:** No buttons, menus, or forms.
- **No file attachments in basic messages** (photos/files require separate message types).

The v2.4 digest format is: headline metric → 3–5 bullet points → closing advisory. SI-05 could follow the same pattern or extend the existing v2.4 message.

### Advantages

- **No new infrastructure.** Bot, token, scheduling, and delivery are already operational.
- **Low effort.** Only new message content and SI-01/SI-03 data binding needed.
- **Immediate reach.** User is already using the v2.4 Telegram digest — SI-05 lands in the same channel.
- **Consistent UX.** User has a single place for weekly trading self-review (Telegram).
- **Character limit not a concern** for the 3 planned metrics + explanatory text.

### Disadvantages

- **External channel dependency.** Telegram availability is outside the system's control.
- **No in-app visibility.** User must open Telegram to see the digest — not visible within the trading dashboard.
- **Character limit constrains rich formatting.** Tables, conditional colour-coding, and expandable sections are not possible.
- **Separation from trade data.** User sees the integrity digest in Telegram but must return to the app for detailed trade history context.

---

## Option B — In-App Notification (New Build)

### Description

Build a new in-app notification system that delivers SI-05 weekly digests within the trading dashboard. Could appear as a notification badge, banner, or dedicated digest panel in the app.

### Implementation effort

| Component | Effort |
|-----------|--------|
| Notification storage/model | M (~5 hrs) |
| Backend digest generation service | S (~3 hrs) |
| Scheduled trigger (weekly cron) | S (~2 hrs) |
| Frontend notification component | M (~5 hrs) |
| Notification read/dismiss logic | S (~2 hrs) |
| **Total new effort** | **~17 hrs** |

### Format and constraints

- **Rich display options:** Tables, colour-coding, expandable sections, links to trade history — all possible.
- **Interactive affordances:** Dismiss, expand, link-to-detail all possible within the same UX.
- **No character limit.**
- **In-app context:** User sees the digest while actively reviewing their portfolio — highest relevance context.

### Advantages

- **Rich formatting.** Full Markdown, tables, conditional display — presentation quality is higher.
- **In-app discoverability.** Digest appears within the user's natural workflow — no app switch.
- **Future extensibility.** In-app notification system can serve other digest types (earnings alerts, regime change, drawdown warnings).
- **Direct context links.** "View full red flag journal" link within the notification is possible.

### Disadvantages

- **3× higher effort** than Telegram (~17 hrs vs ~6 hrs).
- **New infrastructure build.** No existing notification system — requires schema, backend service, frontend component.
- **Lower urgency for Phase 1.** The user is already on Telegram for v2.4 — adding a second channel for SI-05 creates fragmentation unless v2.4 is also migrated.
- **Risk of feature sprawl.** Building a generic notification system for SI-05 might over-invest given the simple 3-metric digest.

---

## Alignment with v2.4 Weekly Digest Pattern

SI-05 Phase 1 (3 metrics: validation_pass_rate, override_count, red_flag_frequency_trend) aligns naturally with the v2.4 weekly digest format:

| v2.4 field | SI-05 equivalent |
|-----------|-----------------|
| Portfolio value | Validation pass rate |
| Weekly P&L | Override count this week |
| Win/loss summary | Red flag frequency trend |
| Risk advisory | Strategy integrity summary |

If Telegram is confirmed, SI-05 could extend the v2.4 message format with a "Strategy Integrity" section, making the existing digest richer rather than creating a separate message.

---

## Recommendation

**Recommendation: Option A — Telegram**

Rationale: SI-05 Phase 1 scope is 3 metrics delivered weekly. The Telegram infrastructure is already operational, the effort delta (6 hrs vs 17 hrs) is significant, and the user's established habit of reading the v2.4 Telegram digest ensures the SI-05 content will be seen. Option B is appropriate if SI-05 evolves to a richer, multi-metric dashboard — but for Phase 1, Option A is the proportionate choice.

This recommendation does not preclude building in-app notifications in a future cycle (Arc 6 or later).

---

## Decision Record

**ACTION REQUIRED FROM PRODUCT OWNER:**

Please record your channel decision below. ST-10 (message format specification for Telegram, or in-app notification spec) cannot begin until this decision is recorded.

**Channel selected:** _(Product Owner to record: Telegram / In-app notification)_

**Date of decision:** _______

**Rationale (optional):** _______

**If Telegram confirmed:** BLG-FE-60 gate condition for BLG-GOV-86 (ST-10) is met. Engine will proceed to author the Telegram message format specification.

**If In-app notification confirmed:** ST-10 scope shifts to in-app notification spec. PO to confirm revised ST-10 scope at sprint execution start.

**Product Owner sign-off:** _(Product Owner to sign here once decision is recorded)_

---

## Head of UX & Design Review

**Review by:** _(Head of UX & Design to record: review completed / acknowledged)_

**Date:** _______

**Comments:** _______
