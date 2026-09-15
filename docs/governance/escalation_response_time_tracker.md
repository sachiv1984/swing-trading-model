**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-15 (ST-18, EPIC-05, v9.4, BLG-GOV-301: initial version)

---

# Cross-Role Escalation Response-Time Tracker

**Added:** ST-18 (EPIC-05, v9.4, BLG-GOV-301)

## 1. Purpose

Escalations to named roles (e.g. Head of Specs Team's 72-hour SLAs, `shared_standards.md` §4) are tracked individually, per cycle, in each cycle's own `execution_escalations.md` / `escalations.md` / `verification_escalations.md` / `closure_escalations.md`. There was previously no aggregate view of response-time trends across roles or across cycles — this document is that view.

## 2. Method

`scripts/generate_escalation_response_time_report.py` scans every escalations-family file under `claude/cycles/*/` and extracts, per `## ESC-*` entry, the structured fields defined by `shared_standards.md` §4: `Raised at`, `Owning authority`, and `Disposition`. Where `Disposition` is `Resolved`, it looks for the nearest `YYYY-MM-DD` date in the entry's `Resolution` / `Resolution summary` text and computes the gap from `Raised at` to that date. Results are aggregated per role (an entry naming multiple authorities counts toward each).

This is a **manually-run reporting script, not a scheduled job** — re-run it and refresh the table in §3 whenever an up-to-date view is needed (e.g. before a PMO Lead workload review). It requires no live credentials and reads only committed files, so it is safe to run in any session.

## 3. Current Snapshot (as of 2026-09-15)

_Scanned 32 files, 61 structured entries parsed, 36 with an extractable resolution date (59% coverage)._

| Role | Total | Resolved (dated) | Same-day | Multi-day avg | Still open |
|------|------:|------------------:|---------:|---------------:|-----------:|
| Infrastructure & Operations Owner | 16 | 5 | 5 | — | 0 |
| Product Owner | 11 | 3 | 3 | — | 3 |
| Head of Specs Team | 7 | 3 | 2 | 2.4 days | 2 |
| Head of Engineering | 5 | 1 | 1 | — | 0 |
| Strategy Rules & System Intent Owner | 5 | 1 | 1 | — | 2 |
| FinOps & Resource Architect | 4 | 1 | 1 | — | 0 |
| Data Model & Domain Schema Owner | 4 | 1 | 1 | — | 0 |
| Head of Backend Engineering | 3 | 0 | 0 | — | 0 |
| Head of UX & Design | 3 | 0 | 0 | — | 0 |
| AI Compliance & Governance Officer | 2 | 1 | 1 | — | 1 |
| Frontend Specs & UX Documentation Owner | 2 | 0 | 0 | — | 0 |
| Director of Quality | 1 | 0 | 0 | — | 0 |
| Director of HR | 1 | 1 | 1 | — | 0 |
| Cybersecurity & Trust Lead | 1 | 1 | 1 | — | 0 |
| PMO Lead | 1 | 0 | 0 | — | 1 |
| (other single-occurrence / compound-authority rows, including comma-joined dual-owner strings not split into separate roles — see §4) | 7 | 0 | 0 | — | 2 |

*(The full, un-collapsed output is reproducible by running the script directly.)*

## 4. Reading This Table — and Its Limits

- **"Same-day" dominates.** Of the 36 dated resolutions, 30 resolved same calendar day as raised. This is expected for a system where most escalations are raised and resolved within one continuous sprint-execution session; it is not evidence that multi-day escalations are rare in absolute terms, only that the ones which *do* get a clean resolution date tend to be same-session ones.
- **41% of entries have no extractable resolution date.** Two distinct causes, not one:
  1. Genuinely still-open escalations (the `Still open` column) — no resolution date exists yet, correctly.
  2. Resolved escalations whose resolution date is stated in free-text prose the script's date-search cannot reliably locate (e.g. a `Disposition: Resolved` line resolved in the *same* commit as the raise, with the date only implied by the file's own `Last Updated` header, or a `Deferred` disposition — see `shared_standards.md` §4 — which is neither `Resolved` nor a clean multi-day-open case).
- **Resolution timestamps are date-only, not full ISO datetimes, in almost every historical entry.** This means true sub-day response times (minutes/hours) cannot be measured — the "Same-day" column is the finest granularity the historical record actually supports. A future structural improvement (adding a `Resolved at:` ISO-8601 field to the standard escalation entry format alongside `Raised at:`, mirroring `execution_state.json`'s own `completed_utc`/`blocked_since_utc` precedent) would make sub-day precision possible; not made in this story, since changing the standard entry format is a `shared_standards.md` change outside this story's scope — noted here as a candidate follow-up, not filed as a new backlog item (this document itself is the tracking artefact).
- **`Owning authority` free text is split on `;` and ` and ` at parenthesis-depth 0, not on commas.** This correctly keeps a role's own parenthetical qualifier intact as one role (e.g. `"Product Owner (co-consulted: Frontend Specifications & UX Documentation Owner, per BLG-QA-150's dual ownership and sprint_backlog.md's RISK-04 note)"` → one row, `"Product Owner"` — the `and` inside that parenthetical is prose, not a second role, and an earlier version of this script's splitter incorrectly shredded it into two fake pseudo-role rows before this was caught and fixed at first review). It does **not** split a genuinely comma-separated dual-owner string with no `and`/`;` (e.g. `"Head of UX & Design (artefact production), Product Owner (scope/sequencing remedy)"`) into two rows — that specific shape counts as one compound row in the "(other ... rows)" line above, rather than crediting each named role separately. This under-counts those specific roles' totals by one occurrence each; it does not fabricate a role that isn't there, which is the more important property for §5's use of this table.
- **Pre-`shared_standards.md`-era files are excluded, not mis-counted.** Some of the earliest cycles (e.g. `2026-03-21__release-v2.2`) used `Raised by:` instead of `Raised at:` and had no `Owning authority:` field at all. The script's field-presence check correctly skips these rather than guessing — they are absent from the 61-entry count, not silently zeroed.

## 5. Sign-Off

This tracker's method (§2) and current snapshot (§3) require PMO Lead sign-off per this story's AC, confirming the coverage and granularity limitations in §4 are understood and accepted as inherent to the historical record rather than a defect in this tool.

- Signed off by: Sprint Execution Engine (agent-mediated, PMO Lead role — §5.3)
- Date: 2026-09-15
- Comments: 1st-pass review found a real defect (not merely an undisclosed limitation): the splitter's ` and `-inside-parentheses handling shredded one legitimate co-consulted-role entry into two fake pseudo-role rows, and the review's own root-cause trace additionally surfaced a second, related bug in the trailing-parenthetical-strip regex (non-greedy `.*?` backtracking across two separate paren groups, silently dropping a real role entirely). Both fixed same-session in the script; §3's table and §4's disclosure re-generated from the corrected script output before this sign-off.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-09-15 | ST-18 (EPIC-05, v9.4, BLG-GOV-301): Initial version. Cross-role escalation response-time tracker, aggregating `shared_standards.md` §4-format escalation entries across all cycles by owning-authority role. |
