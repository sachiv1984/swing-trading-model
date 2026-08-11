Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-11

# Execution Escalations — 2026-08-11__release-v8.6

---

## ESC-EXEC-20260811-01

- **Raised at:** 2026-08-11T23:10:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-08-11__release-v8.6
- **Step:** STEP 3.1 (ST-25 execution)
- **ST/EPIC item:** ST-25, EPIC-06
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-25's AC ("Both items carry the 2026-08-10 re-check confirmation inline in backlog.md") targets `BLG-FE-146` and `BLG-FE-139`, both of which are no longer in `claude/backlog/backlog.md` — they were retired to `claude/backlog/backlog_archive.md` on 2026-08-10, marked "✅ Complete", shipped in v8.5 (ST-19/ST-20 respectively). The underlying gate condition the AC asks to re-annotate ("trigger condition still unmet") is now factually false — a real `ChartContainer`/`ui/calendar.js` consumer was shipped in the same v8.5 cycle, after `BLG-GOV-297` (this story's source) was filed but before this story executed. Additionally, `execution_prompt.md` §7's write scope does not list `claude/backlog/backlog_archive.md` among permitted paths (only `backlog.md`, and only for new-item addition) — even if the annotation were still factually accurate, this routine has no write access to apply it there.
- **Owning authority:** Head of Specs Team
- **Unblock criteria:** A decision on whether (a) this story is moot and should be closed as superseded-by-completion with no file edit, or (b) a different, currently-out-of-scope artefact should instead carry a historical note, or (c) `backlog_archive.md` write access should be granted to this routine for this narrow case.
- **SLA due-by:** 2026-08-12T23:10:00Z (24h, Lifecycle/Process Integrity)
- **Blocks execution:** No
- **Disposition:** Open
- **Resolution summary:** (pending)

---

## ESC-EXEC-20260811-02

- **Raised at:** 2026-08-11T23:15:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-08-11__release-v8.6
- **Step:** STEP 3.1 (ST-26 execution)
- **ST/EPIC item:** ST-26, EPIC-06
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-26's AC ("`BLG-GOV-288`'s AC text matches the actual, correct implementation site") targets `BLG-GOV-288`, which is also no longer in `claude/backlog/backlog.md` — retired to `claude/backlog/backlog_archive.md` on 2026-08-10, marked "✅ Complete", shipped in v8.5 (ST-23). Same write-scope gap as `ESC-EXEC-20260811-01`: `backlog_archive.md` is not a permitted write path for this routine, and the item is already shipped/complete regardless of whether its historical AC text said "STEP 0" vs the actual "STEP 7" implementation site.
- **Owning authority:** Head of Specs Team
- **Unblock criteria:** Same as `ESC-EXEC-20260811-01` — a decision on closing this story as superseded, or granting narrow archive-write access.
- **SLA due-by:** 2026-08-12T23:15:00Z (24h, Lifecycle/Process Integrity)
- **Blocks execution:** No
- **Disposition:** Open
- **Resolution summary:** (pending)
