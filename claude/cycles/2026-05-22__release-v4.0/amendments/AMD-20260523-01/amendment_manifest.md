**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Sealed
**Last Updated:** 2026-05-23
**Amendment ID:** AMD-20260523-01
**Original Cycle:** 2026-05-22__release-v4.0
**Release:** v4.0
**Amendment Reason:** emergency-fix
**Raised by:** PMO Lead
**Raised at:** 2026-05-23T00:05:00Z
**Required ratifying authorities:** Product Owner + Director of Quality
**Ratification status:** Pending

---

# Amendment — AMD-20260523-01

## Summary

Two additions to the v4.0 backlog slice:

1. **ST-12 — Gemini Flash base wiring** (EPIC-03): BLG-BE-19 is a confirmed hard prerequisite for ST-07 (Gemini audit trail) and ST-08 (Gemini cost tracking). Without Gemini wiring in the codebase, EPIC-03 Sprint 2 stories are undeliverable. This was identified in cycle_summary.md as "Pre-sprint Scope Addition — EPIC-03 Prerequisite" but was not included in the original backlog slice.

2. **ST-13 — Starlette security upgrade** (EPIC-02): CVE PYSEC-2026-161 — starlette v0.49.1 has a URL reconstruction authentication bypass vulnerability. Fix: upgrade to ≥1.0.1. Identified by pre-sprint pip-audit scan during sprint planning preflight.

---

## Emergency Evidence

### Evidence for ST-12 (hard-blocker — EPIC-03 prerequisite)

- **Nature:** confirmed undeliverable — EPIC-03 stories ST-07 and ST-08 instrument Gemini API calls; no Gemini code exists in the codebase (no `google-generativeai` dependency, no `gemini_service.py`, no thesis generation endpoint)
- **External reference:** cycle_summary.md §Pre-sprint Scope Addition — EPIC-03 Prerequisite (session observation 2026-05-22); BLG-BE-19 backlog item (2026-05-22)
- **Why this sprint:** ST-07 and ST-08 are Sprint 2 stories. Without BLG-BE-19 as the first EPIC-03 story, Sprint 2 cannot begin execution on EPIC-03. Deferring BLG-BE-19 to a future sprint would make all EPIC-03 stories undeliverable in v4.0.
- **Director of Quality assessment:** XS/S effort addition; QA verification via integration test + endpoint check is within sprint capacity; no additional test scenarios required beyond standard endpoint coverage.

### Evidence for ST-13 (emergency-fix — security CVE)

- **Nature:** security vulnerability — URL reconstruction authentication bypass
- **External reference:** PYSEC-2026-161 (aliases: GHSA-86qp-5c8j-p5mr) — starlette v0.49.1 reconstructs requested URLs from HTTP Host header without validation, allowing path injection into the host part. This may allow authentication bypass when authentication logic depends on the reconstructed URL's path.
- **Fix available:** upgrade to starlette ≥1.0.1
- **Why this sprint:** starlette is the core ASGI framework underlying FastAPI. The vulnerability is a medium-severity authentication bypass applicable to all API endpoints. Deferring to v4.1 leaves all v4.0 production endpoints exposed for the duration of the sprint cycle.
- **Director of Quality assessment:** dependency version bump only; no functional change; existing endpoint tests serve as regression verification; QA sign-off adds one pass/fail line item confirming starlette ≥1.0.1 present in requirements.txt.

---

## Proposed Changes

### Change 1

Type: Add  
Item: ST-12 — Gemini Flash base wiring (BLG-BE-19)  
EPIC: EPIC-03  
Reason: Hard prerequisite for ST-07 (Gemini audit trail) and ST-08 (Gemini cost tracking). EPIC-03 is undeliverable without this story executing first.  
Effort delta: +S (~1 day)  
Dependency impact: ST-12 must execute before ST-07 and ST-08 within EPIC-03; sequencing constraint recorded  
Ratification required from: Product Owner + Director of Quality

### Change 2

Type: Add  
Item: ST-13 — Starlette security upgrade to ≥1.0.1  
EPIC: EPIC-02  
Reason: CVE PYSEC-2026-161 — medium severity authentication bypass; fix required this sprint  
Effort delta: +XS (~0.5 day)  
Dependency impact: none; standalone dependency version bump  
Ratification required from: Product Owner + Director of Quality

---

## Capacity Impact

| Before amendment | After amendment | Delta |
|-----------------|-----------------|-------|
| Firm: ~8–10 days | Firm: ~9.5–11.5 days | +~1.5 days |
| Capacity: ~10 days (solo 2-sprint) | Capacity: ~10 days | — |
| Status: WARN | Status: WARN (slightly increased) | over-allocation risk |

**Note on BLG-BE-19 capacity:** BLG-BE-19 was an implicit prerequisite for ST-07/ST-08. The S effort was always required for EPIC-03 to deliver; this amendment makes it explicit. Net truly new effort is the XS starlette fix (+0.5 day).

Product Owner must explicitly accept the capacity over-allocation in the ratification record.
