**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-04
**Cycle:** 2026-03-04__release-v1.8

---

# Escalations — Release Planning Engine

**Cycle:** 2026-03-04__release-v1.8

---

## ESC-20260304-01

**Escalation ID:** ESC-20260304-01
**Date/time raised:** 2026-03-04
**Routine:** Release Planning Engine
**Cycle ID:** 2026-03-04__release-v1.8
**Trigger type:** Other (execution pre-condition — decision required)
**Release impacted:** v1.8

**Blocking statement:**
`docs/specs/api_contracts/settings_endpoints.md` (BLG-SPEC-D2) documents `PUT /settings` but the live implementation uses `PATCH /settings/{settings_id}` and `POST /settings`. Before EPIC-03/ST-09 can be executed, the Product Owner and API Contracts & Documentation Owner must decide: (a) update the spec to document the live contract, or (b) align the backend to implement PUT /settings as specced (breaking change). This decision gate was identified in the backlog and must be resolved before ST-09 work begins.

**Owning authority:** Product Owner (final decision), API Contracts & Documentation Owner (implementation recommendation)
**Required responders:** Product Owner, API Contracts & Documentation Owner, Head of Engineering

**Due-by / SLA:** Before EPIC-03/ST-09 execution begins (next planning checkpoint)

**Unblock criteria:**
Product Owner has declared option (a) or (b). If option (b), a breaking change decision record is filed at `docs/product/decisions/`.

**Evidence required:**
- Written declaration of option chosen by Product Owner
- If option (b): decision record at `docs/product/decisions/settings-method-change-v1.8.md`

**Disposition:** Deferred
**Deferred by:** PMO Lead (per Release Planning Engine rules — schedule/delivery deferral)
**Deferred reason:** Other EPICs (01, 02, 04) are fully independent and unblocked. EPIC-03/ST-09 specifically requires this decision; the rest of the release proceeds without it.
**Next trigger:**
- Trigger type: event
- Trigger condition: Product Owner declares decision at any point before EPIC-03/ST-09 sprint execution begins
- Target date: Before Sprint Execution of EPIC-03 begins
**Blocks execution:** No
**Safe to proceed scope:** EPIC-01 (Risk Dashboard), EPIC-02 (CI Quality), EPIC-04 (Governance Docs), and EPIC-03/ST-10 (openapi.yaml update) may all proceed without this decision. Only ST-09 is blocked.

**Resolution summary:** Open — pending Product Owner decision.
