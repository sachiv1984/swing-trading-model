# Lessons Learnt — BLG-TECH-02 + BLG-TECH-03: Validation Severity Model & Service Layer Consolidation

**Items:** BLG-TECH-02 — Implement validation severity model (High)
          BLG-TECH-03 — Consolidate ValidationService into service layer (Medium)
**Type:** Tech Backlog (P1 — co-delivered)
**Closed:** 2026-02-21T21:30:00Z
**Reviewed by:** PMO Lead
**Date filed:** 2026-02-21

> **Note on template applicability:** BLG-TECH-02 and BLG-TECH-03 are co-delivered P1 items
> that ran under the defect_run.md v1.1 process rather than the standard feature pre-alignment
> process. This record uses the tech_backlog_lessons_learnt.md template structure.
> The two defects are reviewed jointly given their co-delivery constraint and shared
> deployment history.

---

## What worked well

- Root cause identification was fast and unambiguous. Both defects had clear canonical specs
  (`analytics_endpoints.md` v1.8.1` and `backend_engineering_patterns.md` §3) and the gap
  between spec and implementation was immediately evident from code inspection.

- The co-delivery constraint was correctly identified at G1, enforced throughout every gate,
  and honoured in the fix — a single branch, single PR, single deployment. The constraint
  prevented the risk of a severity model being added to a router that was architecturally
  non-compliant.

- The Director of Quality's independent review caught a genuine record inconsistency (G4 gate
  header) before the document was filed as immutable. The process worked as designed:
  sign-off was withheld, the correction was made, and sign-off was granted on the corrected
  record. The gate served its purpose.

- QA Lead scope decision on re-verification was well-reasoned. Correctly identified that
  `AnalyticsService` and `validation_data.py` were untouched and that full re-run was not
  warranted. Scoped to six targeted scenarios. All six passed.

- The defect_run.md v1.1 Phase Gate Document structure provided a complete, auditable record
  from LOGGED to CLOSED. All five role actions (QA Lead, Head of Engineering x2, Head of
  Specs Team, Infra & Ops Documentation Owner) were independently confirmed with evidence
  before gate items passed.

---

## What created friction

### Issue 1 — Production deploys did not match the delivered files (PRIMARY FINDING)

**What happened:** Two successive 500 errors in production following the initial deploy.

- **First error:** `KeyError: 'pass'` — `_build_summary` in the production file indexed
  `by_severity[tier][v["status"]]` directly. Status values are `"pass"/"warn"/"fail"` but
  tier dict keys are `"passed"/"warned"/"failed"`. The `_by_severity()` function in the
  delivered file used explicit `if/elif` mapping and was correct. The production file was not
  the delivered file.

- **Second error:** `ValidationService.__init__() missing 1 required positional argument:
  'analytics_service'` — the production router was calling `ValidationService()` with no
  argument. The delivered router correctly passed `AnalyticsService()`. Again, the production
  file was not the delivered file.

**Root cause:** Engineering deployed files that were not the files produced in this session.
The deployment was not verified against the delivered artefacts before going live. There was
no pre-deployment file verification step in the Engineering process.

**Impact:** Two hotfixes required. Production was in a 500 error state between initial deploy
and hotfix 2. QA re-verification was blocked until the second hotfix was deployed and
confirmed working. Director of Quality formally noted this as a process failure requiring
lessons learnt.

---

### Issue 2 — Deploy confirmation was verbal, not written

**What happened:** G4.1 (fix deployed to verification environment) was accepted on verbal
confirmation from the Head of Engineering. All other gate items in the entire defect run had
written evidence with name and date. G4.1 was the only exception.

**Root cause:** No written deployment confirmation requirement existed in the defect_run.md
G4 gate definition. The PMO Lead accepted verbal confirmation in the interest of pace.

**Impact:** Minor in isolation, but compounded Issue 1. If a written confirmation had been
required — including a statement that the deployed files matched the delivered artefacts —
the mismatch might have been caught before the 500 errors occurred. A written step creates
a moment of verification; verbal confirmation does not.

---

### Issue 3 — G4 gate status header not updated when G4.2 was completed

**What happened:** When the QA Lead re-verification evidence was recorded and G4.2 was
closed, the gate status header was not updated from `🟡 1 OF 2 ITEMS PASS` to
`✅ ALL G4 ITEMS PASS`. The Director of Quality caught this during independent review and
withheld sign-off until it was corrected.

**Root cause:** The PMO Lead updated the gate item evidence blocks but did not update the
gate-level status header. The update procedure for gate closure does not have an explicit
checklist step for the header.

**Impact:** Director of Quality sign-off was withheld pending correction. Correction was
made immediately and sign-off granted. No downstream delay. However, if the Director of
Quality had not caught this, the filed record would have been internally inconsistent and
immutable.

---

## Process improvements actioned

### 1. Deployment verification requirement added to defect_run.md G4 gate definition

**Document updated:** `docs/team_skills/pmo/processess/defect_run.md`
**Version bump:** 1.1 → 1.2
**Change:** G4.1 gate item definition now requires written deployment confirmation from
Engineering. Confirmation must explicitly state:
  - The fix is deployed to the verification environment
  - The deployed files match the delivered artefacts (file-by-file)
  - The branch/commit reference of the deployment
  - Engineering name and UTC timestamp

Verbal confirmation is no longer sufficient for G4.1. PMO Lead may not pass G4.1 without
written evidence meeting all four criteria.

---

### 2. Gate status header update added as explicit PMO step in defect_run.md

**Document updated:** `docs/team_skills/pmo/processess/defect_run.md`
**Version bump:** 1.2 (same document update as above)
**Change:** Gate closure procedure section added. When all items within a gate pass, the
PMO Lead must update the gate-level status header to `✅ ALL {GATE} ITEMS PASS` before
moving to the next gate. This is a mandatory step — gates with all items passing but a
stale or incorrect header are non-compliant with GI-5 (no ambiguity survives a phase
transition).

---

### 3. Pre-deployment file verification step added to Engineering deployment checklist

**Document updated:** `docs/team_skills/engineering/deployment_checklist.md`
*(or equivalent — Head of Engineering to confirm canonical location)*
**Version bump:** To be applied by Head of Engineering
**Change:** A pre-deployment verification step must be added requiring the deploying
engineer to confirm that each file being deployed matches the reviewed and approved
artefact. For session-produced artefacts, this means explicitly opening and comparing
the output file against the file being deployed before pushing. This step must be
completed before marking the deployment as done.

**Owner of implementation:** Head of Engineering
**Target:** Before next defect is in FIX IN PROGRESS state

---

## New skills or templates created

None. Process improvements are additive changes to existing documents.

---

## Outstanding actions

| Action | Owner | Target |
|--------|-------|--------|
| Update `defect_run.md` v1.1 → v1.2 with G4.1 written evidence requirement and gate header closure step | PMO Lead | Before next defect enters FIX IN PROGRESS |
| Add pre-deployment file verification step to Engineering deployment checklist | Head of Engineering | Before next defect enters FIX IN PROGRESS |
| Confirm canonical location of Engineering deployment checklist to PMO Lead | Head of Engineering | 2026-02-21 |
| Notify Product Owner of OBS-01 (`sharpe_ratio_trade_method` not canonicalised in `analytics_endpoints.md` v1.8.1) and raise backlog item | PMO Lead | Before v1.6.1 ships |
| Track `backend_engineering_patterns.md` version governance action (no version number — non-compliant with `document_lifecycle_guide.md` §2 Class 1) | PMO Lead → Head of Specs Team | Before v1.6.1 pre-alignment closes |