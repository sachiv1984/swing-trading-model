**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Release:** v2.8
**Cycle:** 2026-04-17__release-v2.8
**Last Updated:** 2026-04-17

---

# Lessons Learnt — Release Planning v2.8

## Planning Observations

| # | Observation | Classification |
|---|-------------|----------------|
| 1 | **Carry-forward actioning effective.** All 7 v2.7 carry-forward items were cleanly addressed at planning time — CF-1/CF-2 became sprint stories, CF-4/CF-5 confirmed as in-scope items, CF-6 actioned in this session (scope doc created). The carry-forward mechanism is functioning as designed. | Positive — process working |
| 2 | **BLG-GOV-08 (engine prompt compression) 4-cycle deferral pattern.** Deferred v2.4–v2.7 (4 cycles). PO decision made: final deferral to v2.9 with explicit retirement review if not actioned. The pattern of indefinite deferral for L-effort governance items warrants tracking. | Process observation — advisory |
| 3 | **First external LLM API dependency (EPIC-04).** BLG-FEAT-16 introduces an external API not previously present in the system. Operational concerns: cost, latency, key management, staging test required. | New technical pattern — advisory |
| 4 | **Strategy Rules sign-off on AI feature is an in-sprint gate.** SRB-v1.7 conditional compliance was established in v2.4 but the in-sprint implementation sign-off is new territory. Sprint Planning Engine should surface this as a pre-sprint decision rather than discovering it mid-sprint. | Risk — pre-sprint decision required (flagged in cycle_summary.md) |

## Action Summary

### Immediate Actions Applied: 0

None required — no governance file changes identified at planning time.

### Deferred to Next Cycle: 1

| # | Action | Owner | Target |
|---|--------|-------|--------|
| 1 | gh_issue_template.md lacks **Version:** header field — add per Class 6 standard | Head of Specs Team | v2.8 sprint (advisory) |

### Carry-Forward: 0

No new carry-forward items for v2.9 at this stage.

---

// ARTEFACT_STATUS
```json
{
  "cycle_id": "2026-04-17__release-v2.8",
  "phase": "Release",
  "status": "Published",
  "artefacts": {
    "run_manifest": "present",
    "release_plan": "present",
    "stage4_backlog_slice": "present",
    "stage4_issue_manifest": "present",
    "scope_document": "present",
    "decisions_record": "present",
    "cycle_summary": "present",
    "lessons_learnt": "present"
  },
  "generated_utc": "2026-04-17T00:25:00Z"
}
```
