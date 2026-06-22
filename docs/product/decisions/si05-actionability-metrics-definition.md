**Owner:** Metrics Definitions & Analytics Owner; Infrastructure & Operations Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-20
**BLG-ID:** BLG-GOV-115
**Cycle:** 2026-06-19__release-v6.0
**Story:** ST-09

---

# SI-05 Digest Actionability Metric Definitions

**Purpose:** Formally define the metrics used to evaluate whether SI-05 (Trader's Weekly Digest) content is actionable for the recipient. These metrics feed:
- BLG-GOV-112 weekly cadence review (ST-08)
- BLG-GOV-96 SI-05 Phase 1 effectiveness criteria
- Future SI-05 Phase 2 activation decision (ST-10)

---

## Background

SI-05 delivers a weekly Telegram digest summarising Red Flag Journal events, arc compliance status, and upcoming earnings for open/watchlisted positions. "Actionability" means the digest prompts the trader to take a specific, meaningful action on a position or watchlist item. Metrics must be derivable from existing data sources without requiring new instrumentation.

---

## Metric Definitions

### Metric 1 — Alert-to-Trade Conversion Rate (ATCR)

**Definition:** Proportion of weekly digest deliveries that are followed by a trade action (entry, exit, or size adjustment) within 48 hours on a ticker mentioned in that digest.

**Formula:**
```
ATCR = (weeks where ≥1 trade action followed a digest mention within 48h)
       ÷ (total digest delivery weeks)
```

**Data sources:**
- `si05_digest_log`: delivery timestamp, tickers included per digest
- `trades` table: `entry_date`, `ticker` — join on ticker + 48-hour window post-delivery

**Interpretation:**
- ATCR ≥ 0.30 (30% of weeks): digest prompts action — HIGH actionability
- ATCR 0.15–0.29: moderate actionability — monitor trend
- ATCR < 0.15: low actionability — cadence or content review warranted

**Feeds:** BLG-GOV-96 effectiveness criterion; BLG-GOV-112 cadence review evidence

---

### Metric 2 — Red Flag Acknowledgement Rate (RFAR)

**Definition:** Proportion of Red Flag events included in a digest where the associated position was reviewed, adjusted, or exited within 7 days of the digest delivery.

**Formula:**
```
RFAR = (red flag events in digest followed by position review/exit within 7 days)
       ÷ (total red flag events surfaced across all digest deliveries)
```

**Data sources:**
- `red_flag_events` table: `event_date`, `ticker`, `severity`
- `si05_digest_log`: which red flags were included in each delivery
- `positions` table + `trades` table: position status changes within 7-day window

**Interpretation:**
- RFAR ≥ 0.50: red flags are actioned — HIGH effectiveness
- RFAR 0.25–0.49: partial action — investigate severity vs. ignored pattern
- RFAR < 0.25: red flags not being acted on — content relevance or delivery timing concern

**Feeds:** BLG-GOV-96 effectiveness criterion; BLG-GOV-112 cadence review evidence

---

### Metric 3 — Digest Delivery Consistency Rate (DDCR)

**Definition:** Proportion of scheduled delivery windows (weekly, Sunday evening) where a digest was successfully delivered within ±2 hours of the scheduled time.

**Formula:**
```
DDCR = (digests delivered within ±2h of scheduled window)
       ÷ (total scheduled delivery windows in measurement period)
```

**Data sources:**
- `si05_digest_log`: `sent_at` timestamp, delivery status
- Scheduled window: Sunday 18:00–20:00 local time (Europe/London)

**Interpretation:**
- DDCR ≥ 0.95: delivery is reliable — no operational action required
- DDCR 0.80–0.94: occasional slippage — monitor; investigate if trend
- DDCR < 0.80: reliability issue — escalate to Infrastructure & Operations Owner

**Feeds:** BLG-GOV-112 cadence review (delivery reliability input); ST-11 latency review context

---

### Metric 4 — Earnings Proximity Action Rate (EPAR)

**Definition:** Proportion of digest deliveries that include an earnings alert for an open position where the trader takes a documented position management action (size reduction, protective stop tightening, or planned exit) before the earnings date.

**Formula:**
```
EPAR = (digest earnings alerts followed by documented position action before earnings date)
       ÷ (total digest earnings alerts for open positions)
```

**Data sources:**
- `si05_digest_log` + earnings data: tickers with earnings in next 7 days from delivery date
- `positions` table: open positions at delivery time
- `trades` table: position size adjustments, stop changes, exits before earnings date

**Interpretation:**
- EPAR ≥ 0.40: earnings risk being managed — HIGH actionability
- EPAR 0.20–0.39: partial management — consider prominence of earnings alerts in digest
- EPAR < 0.20: earnings alerts not prompting action — review digest formatting or delivery timing

**Feeds:** BLG-GOV-96 effectiveness criterion; future digest content design decisions

---

## Measurement Period

- **Primary baseline period:** 2026-06-04 (SI-05 go-live) to measurement date
- **Minimum meaningful period:** 4 weeks (4 digest cycles) — note that current measurement at 2026-06-20 covers ~2–3 delivery cycles; metrics improve in reliability with more data
- **Review cadence:** Metrics evaluated at each effectiveness review; ATCR and RFAR are primary effectiveness indicators

---

## Data Source Summary

| Metric | Primary table(s) | Join key |
|--------|-----------------|----------|
| ATCR | si05_digest_log, trades | ticker + date window |
| RFAR | red_flag_events, si05_digest_log, positions, trades | ticker + date window |
| DDCR | si05_digest_log | sent_at vs. scheduled window |
| EPAR | si05_digest_log, earnings data, positions, trades | ticker + earnings date |

---

## Review Sign-Off

- Reviewed by: Metrics Definitions & Analytics Owner
- Date:
- Notes:
