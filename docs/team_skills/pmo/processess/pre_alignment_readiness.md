# Pre-Alignment Readiness Audit

**Owner:** PMO Lead
**Type:** PMO Process Template
**Status:** Canonical
**Version:** 1.1
**Last Updated:** 2026-02-21

---

## Purpose

Run this audit before any pre-alignment meeting is scheduled for a feature. Its job is to surface scope gaps, missing data model fields, outdated specs, and unrealistic effort estimates **before** the meeting opens — not during it.

A feature that passes this audit is ready for pre-alignment. A feature that fails it needs remediation first.

---

## When to Run

- Triggered by the PMO Lead when the Product Owner nominates a roadmap item for pre-alignment
- Must be complete before invitations are sent for the pre-alignment meeting
- If the audit reveals significant scope gaps, the Product Owner must revise the roadmap entry before the meeting is scheduled

---

## Inputs Required

Before running the audit, collect:

- The roadmap item entry (from `docs/product/roadmap.md`)
- The feature description in plain language (what the feature does, what it reads, what it writes)
- The current version of any specs the feature is expected to touch

---

## Audit Checklist

### 1. Data Model Readiness

For every field the feature reads or writes:

- [ ] Does the field already exist in `data_model.md`?
- [ ] If not: is the field type, constraint, default, and migration strategy clear enough to spec before the meeting?
- [ ] If schema changes are needed: has the Data Model owner been notified and given time to prepare?

**Failure condition:** Any required field does not exist and has not been pre-designed. This expands scope and will change the effort estimate. Do not schedule the meeting until the field is at least pre-designed.

#### 1a. Settings Table Dependency *(added v1.1)*

- [ ] Does the feature read from or write to the settings table in any way? (e.g. a user preference that pre-populates a widget, a configurable threshold, a default value)
- [ ] If yes: does the required field already exist in `data_model.md` and `settings_endpoints.md`?
- [ ] If yes: is the Settings page UI spec (`settings.md`) current and does it include the field?
- [ ] If the field does not yet exist: has the scope been updated to include the field definition, migration script, settings endpoint change, and settings page UI update?

**Failure condition:** A settings field dependency is not identified until the pre-alignment meeting. This adds a full spec domain (data model migration, settings endpoint update, settings page UI) that will change the effort estimate. The 3.2 Position Sizing Calculator pre-alignment discovered `default_risk_percent` at the meeting rather than before it — this check exists to prevent that recurrence.

---

### 2. API Contract Readiness

For every endpoint the feature calls or introduces:

- [ ] If an existing endpoint is being modified: is the current contract documented in `api_contracts/`?
- [ ] If a new endpoint is needed: does the API Contracts owner know it is coming and have enough context to draft it?
- [ ] Are there any existing endpoints the feature depends on that are currently undocumented or inaccurate?

**Failure condition:** A required endpoint is undocumented or the API Contracts owner has not been briefed. Schedule a pre-briefing before the meeting.

---

### 3. Frontend Spec Readiness

- [ ] Is the relevant component or page spec (e.g. `position_form.md`, `settings.md`) up to date?
- [ ] Does the Frontend Spec owner have enough context to participate in the pre-alignment meeting?
- [ ] Are there UX decisions that need to be pre-resolved before the meeting (e.g. widget placement, interaction model)?

**Failure condition:** Significant UX decisions are unresolved and would dominate the meeting. Pre-resolve or scope the UX design as a pre-meeting deliverable.

---

### 4. Strategy Rules Readiness

- [ ] Does the feature touch any calculation, rule, or lifecycle behaviour defined in `strategy_rules.md`?
- [ ] If yes: is the relevant section current and accurate?
- [ ] Are there any rules implied by the feature that are not yet documented?

**Failure condition:** The feature requires new canonical rules that do not yet exist. The Strategy Rules owner must be briefed before the meeting, and the section must be drafted before spec work begins.

---

### 5. Effort Estimate Review

- [ ] Does the roadmap effort estimate account for all of: backend implementation, data migration, API contract authoring, frontend spec updates, settings changes, and QA review?
- [ ] Has the effort estimate been reviewed against the actual scope of spec changes required?
- [ ] If the audit has surfaced additional scope (e.g. new data model fields, settings table dependencies, additional spec updates): has the estimate been revised?

**Failure condition:** The estimate does not reflect actual scope. Revise the roadmap entry before scheduling the meeting. An inaccurate estimate creates delivery pressure that compresses pre-alignment quality.

---

### 6. Decisions Inventory

- [ ] What decisions are known to be open for this feature?
- [ ] Who owns each decision?
- [ ] Are there any decisions that must be made by a specific role that may not be present in the pre-alignment meeting?

Produce a preliminary decisions list. This becomes the agenda for the pre-alignment meeting.

---

## Outputs

### Readiness Report

A short document (or inline summary) covering:

- **Go / No-Go recommendation** — is the feature ready to enter pre-alignment?
- **Gaps found** — list any fields, endpoints, rules, or decisions that need pre-work
- **Revised effort estimate** — if the audit changed the scope picture
- **Pre-meeting actions** — list any work that must be done before the meeting is scheduled, with owners assigned
- **Preliminary decisions list** — the agenda for the pre-alignment meeting

---

## Escalation

If the audit reveals that significant pre-work is needed and the Product Owner is under pressure to start the feature immediately:

- The PMO Lead documents the gaps explicitly
- Presents the options: (a) complete the pre-work first, or (b) proceed with known gaps and accept higher risk of scope discovery during the meeting
- The Product Owner decides — but the decision and its rationale are recorded

The PMO Lead does not make this call unilaterally.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.1 | 2026-02-21 | Added Section 1a — Settings Table Dependency check. Identified via lessons learnt for 3.2 Position Sizing Calculator: `default_risk_percent` settings field was discovered at the pre-alignment meeting rather than during the readiness audit, causing an estimate change from 1–2 days to 2–3 days. |
| 1.0 | 2026-02-19 | Initial version |