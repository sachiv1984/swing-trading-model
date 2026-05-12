**Owner:** PMO Lead
**Class:** Policy Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-10

---

# Backlog Deferral Policy

## Purpose

This policy defines when a backlog item requires explicit Product Owner re-deferral and what action must be taken for items that have been deferred repeatedly without engagement.

---

## Policy

### 3-Cycle Deferral Rule

Any backlog item that has been deferred **3 or more consecutive cycles** without delivery AND without a named Product Owner re-deferral must be actioned before the next backlog health check can close.

A cycle counts as a deferral if:
- The item had a target release that passed without delivery, OR
- The item's target release was updated to the next cycle without a recorded PO decision

### Named Re-Deferral

To re-defer an item beyond 3 consecutive cycles, the Product Owner must append a named re-deferral note directly to the backlog item in `claude/backlog/backlog.md`:

```
> PO re-deferral YYYY-MM-DD: [reason]
```

**Required fields:**
- Date: ISO-8601 format (YYYY-MM-DD)
- Reason: one sentence explaining why the item is deferred again and not killed

A named re-deferral resets the consecutive deferral counter.

### Enforcement

During `groom backlog` (Backlog Management Engine STEP 3.5):
1. Items with 3+ consecutive deferrals and no PO re-deferral are flagged as health-check blockers.
2. Each flagged item is surfaced to the Product Owner with three options:
   - Add a named re-deferral with target release
   - Assign a release and move to active scope
   - Kill the item

The health check cannot be marked complete while flagged items remain without a PO decision.

### Kill Recommendation

Items with 3+ consecutive deferrals and no Product Owner engagement in 2+ cycles should be surfaced as kill candidates. Killing an item moves it to the `## Closed Items` section of `backlog.md` with status `Killed` and the reason.

---

## Authority

The Product Owner has sole authority to re-defer, assign, or kill items under this policy. The Backlog Management Engine surfaces the flags; it does not take action autonomously.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-10 | Initial creation — ST-14 (EPIC-04, v3.3), resolves OA-03/CF-03 from v3.2 post-ship closure. |
