**Owner:** AI Compliance & Governance Officer
**Class:** Class 2 Canonical Specification
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-14
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Related:** docs/specs/ai_journal_model_contract.md; docs/specs/compliance/pt05_entry_checklist_s13_review.md
**Source:** BLG-AI-03 (ST-13, v3.4)

---

# AI Journal Summarisation — Quarterly Review Process

## Purpose

Define the quarterly review process for the AI Journal Summarisation feature (`POST /ai/journal-summary`). This process ensures ongoing §13 compliance, model version currency, and output quality verification.

The AI Compliance & Governance Officer owns this process. Reviews must occur on a quarterly cadence (every 3 months) or immediately following any of these triggers:
- A new Claude model version replaces the current model in `ai_journal_model_contract.md`
- A §13 compliance concern is raised by any team member
- An error rate spike is observed in AI audit logs

---

## Quarterly Review Checklist

### 1. Output Quality Sample

- [ ] Pull the 10 most recent `ai_audit_log` entries via `GET /ai/journal-summary/history`
- [ ] Review summary output for each entry against its source trade notes:
  - [ ] Summary accurately reflects the human-authored notes (no invented content)
  - [ ] No trade decisions or recommendations are stated as conclusions (§13 boundary)
  - [ ] Summary remains in an observational/reflective tone — the AI is summarising, not advising
- [ ] Record pass/fail count in the review record

**Acceptable quality bar:** ≥8 of 10 sample entries rated "accurate and §13 compliant." If fewer than 8 pass, halt and escalate to Product Owner and Strategy Rules & System Intent Owner.

---

### 2. §13 Compliance Re-Confirmation

- [ ] Re-read `docs/specs/compliance/pt05_entry_checklist_s13_review.md` §13 boundary analysis
- [ ] Confirm the AI Journal feature still meets the same §13 boundary: the system summarises what the human recorded; it does not evaluate, score, or recommend
- [ ] Confirm no new feature additions to `/ai/journal-summary` endpoint since last review altered the §13 boundary (check `git log --since="90 days ago" -- backend/routers/ai.py backend/services/ai_service.py`)
- [ ] If any changes are found: file an escalation and require Head of Specs Team sign-off before proceeding

---

### 3. Model Version Contract Update Check (BLG-AI-02)

- [ ] Open `docs/specs/ai_journal_model_contract.md` and note the current model version
- [ ] Verify the model version is still available and not deprecated (check Anthropic changelog or claude.ai/docs)
- [ ] If the current model is deprecated or a newer version is preferred:
  - [ ] Draft an update to `ai_journal_model_contract.md` (new model version, effective date, rationale)
  - [ ] Require Product Owner approval before updating the contract
  - [ ] Update `backend/services/ai_service.py` model constant in the same commit
  - [ ] Follow the contract's version increment procedure (§4 of the model contract)

---

### 4. Error Rate Review

- [ ] Query `ai_audit_log` for error rates: count entries with `error IS NOT NULL` in the past 90 days
- [ ] Acceptable error rate: <5% of total requests
- [ ] If error rate ≥5%: investigate root cause; file a backlog item; escalate if root cause is not clear within 5 business days
- [ ] Review response time distribution: P95 response time should be <10 seconds per `ai_journal_model_contract.md` §6

---

## Review Record Format

Each completed review must be recorded as a comment appended to this document (or in a separate review log file if volume warrants):

```
### Review YYYY-QN
**Date completed:** YYYY-MM-DD
**Reviewer:** AI Compliance & Governance Officer
**Trigger:** Scheduled quarterly / [trigger reason]

| Check | Result | Notes |
|-------|--------|-------|
| Output quality sample (10 entries) | Pass (N/10) / Fail | |
| §13 boundary re-confirmed | Pass / Fail | |
| Model version current | Pass / Update required | |
| Error rate <5% | Pass / Fail (rate: X%) | |

**Overall:** Pass / Fail / Escalation required
**Actions taken:**
- [list any actions]
```

---

## Escalation Path

If any review check fails:

1. **Immediate (same day):** Notify Product Owner and Head of Specs Team
2. **Within 24 hours:** File an escalation record in `claude/backlog/backlog.md` (BLG-AI category)
3. **§13 breach:** Stop using the AI journal feature immediately — disable endpoint (`POST /ai/journal-summary`) until resolved; requires Strategy Rules & System Intent Owner sign-off to re-enable

---

## Scheduling

| Review | Trigger Date |
|--------|-------------|
| Q1 2026 | First quarter after v3.4 ships |
| Q2 2026 onwards | Every 90 days from last completed review |

The AI Compliance & Governance Officer is responsible for initiating each review. The PMO Lead is responsible for flagging if a review is 14+ days overdue.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-14 | Initial creation — BLG-AI-03 (ST-13, v3.4). Defines quarterly review checklist, output quality bar, §13 re-confirmation, model version check, error rate review, record format, escalation path, and schedule. Authority: AI Compliance & Governance Officer. |
