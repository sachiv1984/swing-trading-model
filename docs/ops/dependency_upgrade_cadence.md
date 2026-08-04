**Owner:** Head of Engineering; Infrastructure & Operations Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-04
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Created by:** ST-19 (BLG-OPS-116, EPIC-04, v8.2)

---

# Backend Dependency Upgrade Cadence

## Purpose

`backend/requirements.txt` pins every dependency to an exact version (`==`). Exact pinning gives reproducible builds but means no dependency ever updates itself — without a deliberate review cadence, pinned versions drift indefinitely behind upstream, accumulating unpatched CVEs and eventually forcing a large, risky multi-version jump instead of small, regular ones. This document defines that cadence.

## Cadence

**Quarterly**, aligned to calendar quarters (Jan–Mar, Apr–Jun, Jul–Sep, Oct–Dec). Review during the first completed sprint cycle of each new quarter — do not block a specific sprint's scope on it; fold it into that sprint's operations/CI-hardening-type EPIC if one exists, or file it as a standalone backlog item (`BLG-OPS-*`, Type: Operations / Infrastructure) if none does.

**Rationale for quarterly (not monthly or annual):** `backend/requirements.txt` currently pins 16 dependencies (`fastapi`, `starlette`, `uvicorn`, `pandas`, `numpy`, `requests`, `python-dateutil`, `pydantic`, `psycopg2-binary`, `sqlalchemy`, `httpx`, `anthropic`, `pytest`, `pytest-cov`, `reportlab`, `yfinance`). Monthly is disproportionate overhead for a dependency set this size with no history of urgent CVEs (the existing `Dependency CVE Scan (pip-audit)` CI gate already catches urgent security issues continuously, independent of this cadence). Annual is too infrequent — it risks exactly the large-jump problem this cadence exists to prevent, and several of these packages (`fastapi`, `pydantic`, `anthropic`) ship frequent minor releases.

## Review Procedure

1. Run `backend/.venv/bin/python3 -m pip list --outdated` (per `CLAUDE.md` §9 — the project virtualenv, not system Python) to list every dependency with a newer version available.
2. For each outdated dependency, check its changelog/release notes for the versions between the pinned version and latest — flag any breaking (major-version) changes.
3. Upgrade patch and minor versions directly (low risk, run the full test suite after). Major-version upgrades get their own backlog item if breaking changes are found — do not bundle a breaking major upgrade into the routine quarterly pass.
4. Re-run `backend/.venv/bin/python3 -m pip_audit` (per `sprint_planning_notes.md`'s existing Pre-Sprint Vulnerability Scan convention) after upgrading, to confirm no new CVEs were introduced by the upgrade itself.
5. Run the full backend test suite (`backend/.venv/bin/python3 -m pytest`) to confirm no regressions.
6. Record the review outcome in this document's Review Log below (date, versions changed, any deferred major-version items filed as backlog items).

## Review Log

| Date | Reviewed by | Outcome |
|------|--------------|---------|
| 2026-08-04 | Sprint Execution Engine (ST-19, EPIC-04, v8.2) | Cadence established (this document). First scheduled review: **2026-10-01** (start of Q4 2026 — the next full quarter boundary after this document's creation; Q3 2026 is already 2/3 elapsed and does not warrant a review this close to Q4). |

## First Review Scheduled

**2026-10-01** (start of Q4 2026), per the Cadence section above. Owner: Head of Engineering. To be actioned at the first sprint of that quarter, or filed as a standalone `BLG-OPS-*` backlog item if no sprint EPIC naturally covers it.
