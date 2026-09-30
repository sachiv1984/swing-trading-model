Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-30

---

# Lessons Learnt — Release Planning 2026-09-30__release-v9.9

## Friction Items

**Friction Item 1 — the PO Modify directive is only partially satisfiable this cycle: the backend half of a paired idea-intake candidate can seat, the frontend half structurally cannot, in the same release.** `BLG-BE-135` (backend, ungated) seats cleanly as this cycle's build-and-ship candidate — the first cycle able to do so since the directive was raised at `v9.1`. Its paired frontend counterpart `BLG-FE-193`, however, carries a formal `Gate criteria:` field requiring `BLG-BE-135`'s fields to be shipped and live on `GET /positions`, which by definition cannot be true within the same release that ships them. This is a structural one-release lag inherent to any backend-then-frontend idea pair, not a process failure, but it means the directive reads as "fully satisfied" only across two consecutive releases, not within one. **Recommendation:** `v9.10`'s release planning should read this note and treat `BLG-FE-193` as a should-seat candidate once `BLG-BE-135`'s ship is confirmed, rather than re-deriving the dependency from scratch.

**Friction Item 2 — `ESC-CLOSE-20260928-02`'s Option(b) reuse-limits question remains open for a second consecutive cycle without engagement.** As at `v9.8`, this cycle's cited rebalance record (`2026-09-30__scheduled`) is fresh and same-day, so the ambiguity the escalation raised again did not need adjudicating to clear §-1.2. The escalation (SLA due 2026-10-01) should still receive a Head of Specs Team ruling for the general case before a release-planning invocation is run on a day that does not align this favourably with the preceding rebalance.

## Prompt Change Classification

No process patches proposed this cycle. Friction Item 1's recommendation is advisory for the next release-planning session, not a prompt-file change. Friction Item 2 needs the already-tracked `ESC-CLOSE-20260928-02` Head of Specs Team ruling, unaffected by this cycle's clean pass.

```yaml
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-09-30__release-v9.9",
  "phase": "Release",
  "filed_utc": "2026-09-30T18:15:00Z",
  "friction_item_count": 2,
  "action_now_count": 0,
  "deferred_count": 2,
  "status": "Active"
}
```
