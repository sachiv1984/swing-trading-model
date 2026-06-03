**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-06-03
**Cycle:** 2026-06-03__release-v5.0
**Story:** ST-11 (EPIC-04, v5.0)
**Backlog ref:** BLG-GOV-87

---

# SI-02 Frontend Feature — Re-Entry Trigger Criteria

**Feature:** SI-02 — Behavioural Drift Detection (frontend display)
**Document scope:** Defines the formal criteria that must be met before SI-02 frontend delivery is re-entered into sprint planning
**Governance reference:** `claude/roadmap/current_roadmap.md` — Arc 2, SI-02

---

## Background

SI-02 (Behavioural Drift Detection) was assessed in v4.5 §13 review and implementation began in v4.6. The backend drift detection service is implemented and live. The frontend display component was deferred pending sufficient data accumulation (drift scores require a meaningful sample of closed trades with drift data before the UI can provide useful signal).

This document records the formal criteria that govern when SI-02 frontend delivery may re-enter sprint planning. It is referenced at each release planning kickoff to determine whether SI-02 frontend implementation should be promoted to the active sprint scope.

---

## Re-Entry Gate Criteria

### Hard Gate (Required — Mandatory, not advisory)

**Criterion H-01:** ≥ 20 closed trades with linked `trade_plans` confirmed by PMO Lead via direct production database query.

**How to verify:** PMO Lead runs the following query (or equivalent) against the production database at the release planning kickoff:

```sql
SELECT COUNT(*) 
FROM trades t
JOIN trade_plans tp ON tp.id = t.trade_plan_id
WHERE t.status = 'closed'
  AND t.trade_plan_id IS NOT NULL;
```

If the count returns ≥ 20: hard gate passed. Record the count and date in the release planning notes.

**Rationale:** The behavioural drift score is computed from drift between closed-trade outcomes and trade plan expectations. With fewer than 20 data points, the drift score is statistically thin — displaying it would risk user misinterpretation of noise as signal. The 20-trade threshold is the minimum sample for meaningful drift interpretation.

**Authority to confirm:** PMO Lead, via direct database query. No proxy or estimate acceptable — must be a confirmed count from production.

### Soft Advisory (Supporting, not blocking)

**Criterion S-01:** Drift score data has been accumulating for ≥ 3 months (qualitative signal).

**How to assess:** At release planning kickoff, check when the SI-02 backend service first produced drift scores. If ≥ 3 months of data has accumulated, this advisory criterion is satisfied.

**Rationale:** Even with 20 closed trades, if all trades closed within the same 2-week market regime, the drift scores may not reflect meaningful behavioural variation. Three months of accumulation provides a diversity of market conditions in the drift signal.

**Note:** This criterion is advisory. If H-01 (≥ 20 closed trades) is met but S-01 is not, PMO Lead and Product Owner may still choose to proceed with SI-02 frontend delivery. The PMO Lead must record the rationale for proceeding before S-01 is met.

---

## Periodic Check Cadence

**Check trigger:** PMO Lead checks re-entry criteria at **every release planning kickoff** starting with v5.1 (2026-09 earliest).

**Check record:** At each release planning kickoff, PMO Lead records the following in the release planning notes or sprint planning notes:
- Date of check
- Closed trade count (from production query)
- Whether H-01 (≥ 20 closed trades) is met: Yes / No
- Whether S-01 (≥ 3 months data) is met: Yes / No
- Decision: Promote SI-02 frontend to sprint scope / Defer (with rationale)

**Responsibility:** PMO Lead owns this periodic check. If PMO Lead is unavailable at release planning, the Product Owner or designated release manager must perform the check.

---

## When Criteria Are Met

When both H-01 is confirmed AND S-01 is met (or PO accepts rationale for S-01 waiver):
1. PMO Lead records gate clearance in the release planning notes
2. SI-02 frontend stories (deferred from their current backlog state) are promoted to the active sprint scope in the next sprint planning session
3. This document is updated with the clearance date and confirmed trade count

---

## Product Owner Confirmation

The re-entry criteria above represent the intended conditions for SI-02 frontend delivery.

**Product Owner:** Confirmed
**Date:** 2026-06-03
**Comments:** The hard gate of ≥ 20 closed trades with linked trade plans is the right threshold — it ensures the frontend has enough data to display meaningful drift signal rather than noise. The 3-month soft advisory is appropriate context but should not be a hard block if the trade count is met. PMO Lead check cadence starting v5.1 (2026-09) is confirmed.

---

## PMO Lead Acknowledgement

PMO Lead acknowledges ownership of the periodic re-entry check cadence.

**PMO Lead:** Acknowledged
**Date:** 2026-06-03
**Check cadence:** Every release planning kickoff starting v5.1 (2026-09 earliest)
**Comments:** Will run the database query at each release planning kickoff and record the result in the release planning notes. If criteria are met, will surface SI-02 frontend promotion to sprint planning immediately.
