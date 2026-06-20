**Owner:** Infrastructure & Operations Owner
**Class:** Staging Evidence Record (Class 4)
**Status:** Pending I&O Owner sign-off
**Version:** 1.0
**Last Updated:** 2026-06-20
**Story:** ST-11 — SI-05 service production p99 latency baseline review
**Cycle:** 2026-06-19__release-v6.0
**Delegation:** DEL-20260620-05
**P3 Deviation:** Measurement at 16 days post-launch (2026-06-20) vs AC-01 post-4-week (2026-07-04) spec. PO gate override accepted.

---

# SI-05 p99 Latency Baseline Review — Staging Evidence

## Purpose

Establish the production p99 latency baseline for `POST /digest/si05/send` at 16 days post-launch (gate-override measurement window). Compare against the BLG-OPS-54 pre-launch baseline. Record PASS or file an investigation item.

---

## Review Procedure (I&O Owner to complete)

### Step 1 — Extract p99 from Render Production Logs

**Target endpoint:** `POST /digest/si05/send`
**Measurement window:** 2026-06-04 (SI-05 go-live) to 2026-06-20 (today, 16 days)
**Log source:** Render production log stream (service: swing-trading-backend or equivalent)

Query to run (adjust service name as needed):
```
Filter: POST /digest/si05/send  (or SI-05 dispatch jobs in log)
Aggregate: p99 response duration
Period: 2026-06-04 00:00 UTC – 2026-06-20 23:59 UTC
Sample size: record total request count
```

**Result (I&O Owner to fill):**
- p99 latency (ms): _______________
- Total request count in window: _______________
- Measurement timestamp: _______________

---

### Step 2 — BLG-OPS-54 Pre-launch Baseline Comparison

**Pre-launch baseline (from BLG-OPS-54):**
- Baseline p99 (ms): _______________ *(retrieve from BLG-OPS-54 record)*
- Baseline measurement date: _______________

**Threshold:** PASS if production p99 ≤ 2× BLG-OPS-54 baseline p99

**Comparison:**
- Production p99: _______________ ms
- 2× BLG-OPS-54 baseline: _______________ ms
- Production within threshold? YES / NO

---

### Step 3 — Record Outcome

**AC-03 outcome:**

- [ ] **PASS** — production p99 ≤ 2× BLG-OPS-54 baseline
- [ ] **FAIL — investigation item filed**

If FAIL: Investigation item reference: _______________

---

### Step 4 — Sign-Off (AC-04)

- **Reviewed by:** Infrastructure & Operations Owner
- **Date:** _______________
- **Notes:**

---

## P3 Deviation Record

| Field | Value |
|-------|-------|
| Deviation class | P3 |
| AC-01 spec | Post-4-week measurement (≥ 2026-07-02) |
| Actual measurement | 16 days post-launch (2026-06-20) |
| Override authority | Product Owner gate override, 2026-06-20 |
| Intent preserved | Yes — production latency baseline vs. pre-launch baseline; data source unchanged |
| Risk | Smaller request sample at 16 days; p99 may be less stable than at 4 weeks. I&O Owner should note sample count. |

---

## Commit Instructions (I&O Owner)

Once sign-off is complete, commit this completed document to the EPIC-04 branch:

```
Branch: exec/2026-06-19__release-v6.0/EPIC-04
Commit: [EPIC-04][ST-11] Add SI-05 p99 latency baseline review — I&O Owner sign-off
```

GitHub issue: #814

Then update `execution_state.json` ST-11 status to `done`.
