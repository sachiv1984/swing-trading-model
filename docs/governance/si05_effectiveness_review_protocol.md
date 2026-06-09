**Owner:** Product Owner; Director of Quality
**Class:** Governance Document (Class 1)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-09
**Cycle:** 2026-06-08__release-v5.3 (ST-23, BLG-GOV-113)
**Must complete by:** 2026-07-01

---

# SI-05 Phase 1 Effectiveness Review Protocol

## 1. Purpose

This protocol defines the process for the SI-05 Phase 1 effectiveness review — who participates, what evidence is examined, what format the output takes, and what decision authority exists. The review must complete by 2026-07-01.

The **what to measure** is defined in `claude/cycles/2026-06-08__release-v5.2/si05_effectiveness_criteria.md` (BLG-GOV-96). This protocol defines **how** the review is conducted.

## 2. Participants

| Role | Responsibility |
|------|----------------|
| **Product Owner** | Leads the review; provides self-assessment on all three effectiveness criteria; decides on Phase 2 activation |
| **Director of Quality** | Reviews evidence completeness; verifies si05_digest_log data supports the assessment; signs off the review record |

No other participants are required for Phase 1.

## 3. Evidence Sources

| Evidence | Source | What to Check |
|----------|--------|---------------|
| **Digest delivery record** | `si05_digest_log` table — query: `SELECT sent_at, status, event_count FROM si05_digest_log ORDER BY sent_at DESC LIMIT 10` | Confirm digests were delivered (status='sent') at expected weekly cadence |
| **Frequency criterion** | PO self-report | Did PO review ≥4 of the last 5 digests? (Criterion 1, BLG-GOV-96) |
| **Action criterion** | PO self-report | Was there ≥1 digest-triggered app action in the review period? (Criterion 2, BLG-GOV-96) |
| **Content usefulness** | PO self-assessment | Was the digest content actionable? (Criterion 3, BLG-GOV-96) |
| **RFJ view counts** | Render logs or `red_flag_events` query | Were Red Flag Journal entries being viewed/acted on after digest sends? |

## 4. Review Output Format

The review produces a single record appended to `claude/cycles/2026-06-08__release-v5.2/si05_effectiveness_criteria.md` under a new section `## 30-Day Review — 2026-07-04 (or nearest date)`:

```
## Effectiveness Review Record

**Date conducted:** YYYY-MM-DD
**Conducted by:** Product Owner, Director of Quality

### Criterion 1 — Frequency
[PASS/FAIL] — PO reviewed N of last M digests

### Criterion 2 — Action  
[PASS/FAIL] — [describe action(s) or none]

### Criterion 3 — Content Usefulness
[PASS/FAIL] — [PO self-assessment]

### Overall Assessment
[All criteria PASS / N criteria FAIL]

### Phase 2 Activation Decision
[PROCEED / DEFER — with rationale]
Decision authority: Product Owner

### DoQ Sign-off
- Director of Quality: [name/role] — Date: YYYY-MM-DD
```

## 5. Decision Authority

The **Product Owner** holds sole decision authority on Phase 2 activation. The Director of Quality's role is to verify evidence completeness and sign off that the review was conducted per this protocol — not to override the PO's decision.

Phase 2 activation requires:
- All 3 BLG-GOV-96 criteria PASS, OR
- PO explicitly overrides with documented rationale and DoQ acknowledgement

## 6. Timeline

| Milestone | Date |
|-----------|------|
| Review window opens | 2026-06-30 (5 days before deadline) |
| Review must complete | 2026-07-01 |
| Phase 2 activation decision | Same date as review |
| Record filed | Within 2 working days of review |

## 7. Sign-Off

| Role | Status | Date |
|------|--------|------|
| Product Owner | Approved (agent-mediated) | 2026-06-09 |
| Director of Quality | Approved (agent-mediated) | 2026-06-09 |
