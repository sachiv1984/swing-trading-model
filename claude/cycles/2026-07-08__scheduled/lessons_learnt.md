**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-07-08__scheduled
**Last Updated:** 2026-07-08

---

# Lessons Learnt — Roadmap Rebalance 2026-07-08__scheduled

Feature / Trigger: N/A — scheduled rebalance
Run: 2026-07-08__scheduled
Reviewed by: PMO Lead; Head of Specs Team
Date filed: 2026-07-08
Prior cycle checked: 2026-07-06__scheduled

---

## What worked well

1. **STEP -1.5's prior-cycle outstanding-action check correctly surfaced and resolved both deferred patches from `2026-07-06__scheduled`**, including recognising that the SI-02 patch had already been re-triaged and re-targeted to this exact engine by `2026-07-06__release-v6.7` closure (LP-09) rather than treating the shipped-release stale-target rule as an automatic OVERDUE halt — the intervening governed routine's correction was honoured rather than re-litigated.
2. **STEP 2.3's SI-02 gate re-check caught and corrected a materially wrong prior estimate mid-cycle**, using `BLG-BE-46` (filed the same day, independently, during the `plan release v6.7` session) to replace the "15 confirmed / 20 self-reported, close to threshold" narrative with the actual finding: 0 linked trade-plans due to a data-integrity bug, worse than believed. The newly-added structured field in `current_roadmap.md` was updated to reflect this correction within the same session it was created.
3. **The STEP 2.4 Product Value Alert (ratio 0.26, first time below the 0.30 floor) produced a genuinely mandatory, well-evidenced pull-forward outcome** rather than a repeat advisory note — 2 concrete, ungated, build-and-ship-shaped U-item candidates were identified, debated, and approved in the same session, both directly responsive to open friction (SI-02 gate confusion, an unnecessarily-gated tagging feature).
4. **The idea intake window (`IW-20260708-01`) correctly handled a fully-empty register** (0 open ideas, a first in the reviewed history) without any special-casing — all 22 agents submitted cleanly, including PMO Lead's tracked resubmission of a previously-rejected idea whose revival condition had been confirmed Met.

---

## Friction Log

---

### Friction Item 1

**Classification:**
- Type A — Governance Drift: `claude/scoring/scored_initiatives.md` had not been overwritten per `roadmap_prompt.md` STEP 6's explicit instruction ("this file reflects only the current cycle's scoring — it is overwritten each run... do not create cycle-dated copies") for at least 6 cycles — the file's last write was `2026-06-08__scheduled`; every scheduled/completion rebalance since then that reached STEP 6 either skipped the write or appended instead of overwriting, and no engine caught the drift until this cycle's write attempt.

**Recurrence:** Not checkable (no prior lessons learnt file flagged this specific compliance gap; it had simply gone unnoticed for ~6 cycles of silent non-compliance).

**What happened:**
At STEP 6 this cycle, reading `scored_initiatives.md` before writing revealed a long accumulated history of dated sections going back to 2026-03-31, with the most recent being `2026-06-08__scheduled` — despite the explicit "overwritten each run" instruction and the explicit "no cycle-dated copies" prohibition in the same STEP 6 text. This cycle restored the specified behaviour (full overwrite, current-cycle-only content).

**Where in the routine:**
STEP 6 — Scoring Matrix Overlay.

**Root cause:**
Process gap — no verification step exists anywhere in the routine to confirm STEP 6's write actually resulted in a file containing only the current cycle's content; the instruction existed but had no enforcement mechanism, so accumulated drift went undetected across many cycles.

**Blast radius analysis:**
- What would have propagated: continued unbounded accumulation of historical scoring sections, eventually making the file large enough to be unreliable "decision support only" reading material — defeating its stated purpose of showing only current-cycle context.
- When it would have surfaced: never, absent a direct read-before-write comparison (which is what caught it this cycle) — a silent, slowly-worsening failure.
- Recovery cost if uncaught: low today (single overwrite), but would have compounded — recovery cost rises the longer the drift continues since more historical content accumulates that a future cycle might mistakenly treat as still-relevant.

**Process patch:**

→ Deferred patch (cannot apply this run — requires a design decision on where the verification lives, and this run has no time budget left to design a new sub-step without risking a rushed addition to an already-large routine):
  - File: `claude/system/roadmap_prompt.md`
  - Section: STEP 6
  - Change required: Add an explicit verification instruction — "Before writing, if the file already exists, confirm it does not already contain a section dated to a prior cycle; if it does, this is non-compliant drift, not intentional history — overwrite fully rather than append." This makes the existing "overwritten each run" instruction self-enforcing rather than relying on an editor noticing on read.
  - Owner: Head of Specs Team
  - Target: next scheduled or completion-triggered `run roadmap` invocation.

---

### Friction Item 2

**Classification:**
- Type B — Semantic Mismatch: `ideas_register.md`'s Status enum has no dedicated value for "STEP 5 debate resolved into a governance/prompt process patch rather than a roadmap/backlog addition" — the same undocumented reuse of `Promoted-Added` for this case occurred twice now, independently, without either occurrence noting the schema gap.

**Recurrence:** Yes — the same situation (a debated idea resolving to a process patch, not a roadmap/backlog item) occurred at `2026-07-06__scheduled` (`IDEA-challenger-20260702-01`), but was not flagged as a friction item there — this run is the first to name it explicitly, on its second occurrence.

**What happened:**
At STEP 8.5.B (write plan), determining the correct register Status for `IDEA-pmo-lead-20260708-02` (cadence review, resolved as a deferred prompt-patch proposal) required working through the schema definitions in `shared_standards.md §16.5` and finding no clean fit — `Promoted-Added` is documented as "✅ Promoted to roadmap," which this candidate technically wasn't. The same ambiguity must have been worked through identically at `2026-07-06__scheduled` for `IDEA-challenger-20260702-01`, since that idea also resolved as a prompt patch and was also given `Promoted-Added` — but neither cycle recorded this as a documentation gap until now.

**Where in the routine:**
STEP 8.5.B (Write Plan — register row status verification).

**Root cause:**
Naming inconsistency / template omission — the register schema was designed around two clean outcomes (roadmap/backlog addition vs. rejection) and doesn't account for the third outcome type (process/prompt patch) that STEP 5 debates can legitimately produce.

**Blast radius analysis:**
- What would have propagated: a future cycle re-deriving the same ambiguity a third time, potentially reaching a different (inconsistent) resolution — e.g. inventing a new ad hoc status value instead of reusing `Promoted-Added`, fragmenting the schema further.
- When it would have surfaced: the next time a STEP 5 debate resolves into a process patch rather than a roadmap/backlog item — plausible within 1–3 cycles given this is now the 2nd occurrence in 3 cycles.
- Recovery cost if uncaught: low (single schema clarification), but the inconsistency-fragmentation risk compounds each time it recurs undocumented.

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/shared_standards.md`
  - Section: §16.5, Status column definition
  - Change: Clarified that `Promoted-Added` also covers this case, citing both occurrences (`IDEA-challenger-20260702-01`, `IDEA-pmo-lead-20260708-02`) as precedent.
  - Version: v3.9 → v3.10
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — appended to `claude/system/prompt_change_log.md`

---

### Friction Item 3

**Classification:**
- Type A — Governance Drift: `OPERATIONAL_GUIDE.md`'s top `**Version:**`/`**Last Updated:**` header fields were found lagging behind the Change Log table's own recorded bumps by 3 versions (header read 4.80; the table's own top rows recorded bumps up to 4.83) at the start of this cycle's STEP -1.5 governance-file edits.

**Recurrence:** Yes — appeared in `2026-07-06__scheduled` (this exact pattern, described in that cycle's own Change Log entries for v4.79, v4.80, and v4.81, each explicitly "correcting a repeat header-drift"). This is the 4th documented occurrence of the identical failure mode.

**What happened:**
When updating `OPERATIONAL_GUIDE.md` for the STEP -1.5 deferred-patch resolutions this cycle, the header showed `Version: 4.80`, but the Change Log table's most recent rows (4.81, 4.82, 4.83, all dated 2026-07-06) showed the document had already been bumped three further times without the header field being updated to match — each time, apparently, the editor updated the Change Log table (the historical record) but not the header field (the current-state indicator), the same failure mode as the 3 prior recorded occurrences. Corrected this cycle to 4.84, then again to 4.85 for this cycle's own second patch batch.

**Where in the routine:**
STEP -1.5 / STEP 11 (governance file edits, per the CLAUDE.md §6 Governance File Edit Checklist).

**Root cause:**
Process gap — the Governance File Edit Checklist (CLAUDE.md §6) instructs "bump the version in the file's own header" as step 1, without instructing the editor to first check the Change Log table for the *actual* current version. An editor who trusts the header field alone (rather than cross-checking the table) will under-increment, exactly as happened 4 times now. This is a structural gap, not an individual lapse — the same failure recurring identically across 4 independent sessions suggests the instruction itself invites the error.

**Blast radius analysis:**
- What would have propagated: a 5th recurrence at the next governance-file edit, and every edit thereafter, indefinitely — this failure mode shows no sign of self-correcting since the fix applied each time (backfilling the header) doesn't address why the header falls behind in the first place.
- When it would have surfaced: the next `run roadmap`, `plan release`, or any routine performing a Governance File Edit Checklist update to `OPERATIONAL_GUIDE.md`.
- Recovery cost if uncaught: low per-incident (a header field correction), but the *pattern* itself — 4 occurrences and counting — represents a standing minor governance-integrity gap that erodes confidence in the header field as a quick-reference version indicator.

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/OPERATIONAL_GUIDE.md`
  - Section: Directly above the Change Log table
  - Change: Added an explicit note instructing future editors to read the table's own top row for the actual current version before bumping the header field, rather than trusting the header field in isolation.
  - Version: v4.84 → v4.85 (folded into the same batch as Friction Item 2's companion OPERATIONAL_GUIDE.md update)
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — appended to `claude/system/prompt_change_log.md`

→ Deferred patch (systemic prevention — the immediate patch above addresses `OPERATIONAL_GUIDE.md` itself, but the root instruction lives in `CLAUDE.md §6`, which is outside this engine's write scope):
  - File: `CLAUDE.md`
  - Section: §6 Governance File Edit Checklist, step 1
  - Change required: Amend step 1 ("Bump the version in the file's own header") to read "Bump the version in the file's own header — first read the highest version already recorded in the file's own Change Log table (if one exists) to confirm the header field is not already behind it."
  - Owner: Head of Specs Team
  - Target: next session with direct CLAUDE.md write access (outside any single phase engine's declared write scope — requires either a dedicated governance session or explicit user authorisation to edit CLAUDE.md directly).

---

## Recurrence Escalations

Friction Item 2 and Friction Item 3 are both marked Recurrence = Yes. Neither had an *open, unresolved* prior outstanding action carried forward (each prior occurrence was independently closed/backfilled at the time) — so neither meets the automatic-escalation bar under §6.4 ("recurrence with an open prior outstanding action"). Recorded here as visible patterns per §3.7, not as escalations.

None meet the formal escalation bar this cycle.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/backlog_management_prompt.md` | STEP 1 (new §1.1) | Gate Field Label Normalization mandatory pre-scan added (resolves `2026-07-06__scheduled` Friction Item 1) | v1.10→v1.11 | Yes |
| `claude/system/roadmap_prompt.md` | STEP 2.3 | SI-02 structured-field read instruction added (resolves `2026-07-06__scheduled` Friction Item 2, re-routed via `2026-07-06__release-v6.7` closure LP-09) | v8.3→v8.4 | Yes |
| `claude/system/shared_standards.md` | §16.5 | `Promoted-Added` status usage clarified for process-patch-only debate outcomes | v3.9→v3.10 | Yes |
| `claude/system/OPERATIONAL_GUIDE.md` | §6/§6M/§13/§14 + Change Log | Version-reference sync for the above 3 patches, across 2 update batches | v4.80→v4.85 | Yes (2 entries) |

---

## New files created this run

- `claude/cycles/2026-07-08__scheduled/run_manifest.md`
- `claude/cycles/2026-07-08__scheduled/cycle_record.md`
- `claude/cycles/2026-07-08__scheduled/cycle_summary.md`
- `claude/cycles/2026-07-08__scheduled/lessons_learnt.md` (this file)
- `claude/ideas/window_summary_IW-20260708-01.md` (committed separately as part of the idea intake window close)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/roadmap_prompt.md` | STEP 6 | Add a verification instruction confirming the scoring-matrix write is a true overwrite (no accumulated prior-cycle sections) before writing | Head of Specs Team | Next `run roadmap` invocation |
| `CLAUDE.md` | §6 Governance File Edit Checklist, step 1 | Amend to require reading the file's own Change Log table's top row before bumping the header version field | Head of Specs Team | Next session with CLAUDE.md write access (outside any phase engine's declared scope) |
| `claude/system/roadmap_prompt.md` | STEP 0.C (Run Tier Determination) | Add a documented exception allowing an abbreviated manifest for scheduled runs where 0 active initiatives exist **and** no backlog/ideas-register change occurred since the immediately prior scheduled run — resolves STEP 5 Candidate 3 (`IDEA-pmo-lead-20260708-02`, cycle cadence review), Modified by PO to a narrowly-scoped deferred patch rather than an action-now structural tier change (Challenger raised a governance-complexity counter-argument, citing `GCA-2026-06-17`) | Head of Specs Team | Next scheduled rebalance where the "0 active initiatives + no register/backlog change since prior scheduled run" condition recurs |

---

## Escalations

None raised by this engine this cycle.

---

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | The SI-02 gate's true blocker is now a data-integrity bug (`BLG-BE-46`, `trade_plans.position_id` never populated), not trade-count proximity — the 20-trade self-report was in fact accurate, but the linked-plan join condition returns 0. | `plan release`/`plan sprint` should treat SI-02 frontend work as blocked on `BLG-BE-46`'s resolution, not on trade-count accumulation — re-verifying by trade count alone will not clear this gate. | Release Planning; Sprint Planning |
| 2 | Two mandatory pull-forward candidates (`BLG-FEAT-52` ungated, `BLG-FEAT-71` new) were approved this cycle in direct response to the first-ever Product Value Alert (ratio 0.26). | `plan release` should treat these as the anchor U-items for its scope decision, not merely available candidates — the STEP 2.4 alert's mandatory-pull-forward clause was actioned on this engine's side; release planning completes the loop by actually shipping them. | Release Planning |
| 3 | `IDEA-infra-ops-20260708-01`/new backlog item `BLG-OPS-99` (X-API-Key provisioning) remains unresolved for a 2nd consecutive cycle citing this exact gap (LP-08) — no governed routine has production data/API access. | Any future engine invocation attempting to verify a data-dependent gate (SI-02 or otherwise) should expect to rely on backlog findings like `BLG-BE-46` rather than live queries, until this is provisioned. | All |

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-07-08__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-07-08T18:00:00Z",
  "friction_item_count": 3,
  "action_now_count": 2,
  "deferred_count": 3,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
