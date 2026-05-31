**Owner:** Frontend Specs & UX Documentation Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-30
**Cycle:** 2026-05-30__release-v4.6 (EPIC-03, ST-12, BLG-FE-47)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Red Flag Journal — Design Review Scope Document

## Purpose

This document defines the scope of the Red Flag Journal (RedFlagJournal.js) design review, separating what is reviewable from what is out of scope. It ensures the design review session has clear boundaries and produces actionable outcomes without re-litigating implementation decisions.

## Background

The Red Flag Journal (`GET /portfolio/red-flag-journal`) is a deviation audit log surfacing strategy override events (pre-entry validation override, checklist skip, prompt dismissal). It was delivered in v3.9 (EPIC-03, ST-07). The v4.6 ST-09 enhancement adds a `severity` field (info / warning / critical) and a `?severity=` filter parameter. A design review is warranted to assess presentation quality and severity visualisation.

---

## In Scope for Design Review

The following are reviewable in this design review session:

### 1. Presentation & Layout

- **Overall layout** — table vs card view; column order and density; responsive breakpoints
- **Pagination UI** — page controls placement and labelling; page size selector if present
- **Empty state** — message content and visual treatment when journal is empty
- **Loading state** — skeleton vs spinner vs message

### 2. Filter UI

- **Existing filters** — event_type and ticker filter controls: usability, placement, label clarity
- **Severity filter** (v4.6 ST-09) — filter control for `severity` (info / warning / critical): label, placement, UX pattern (dropdown / chip / badge)

### 3. Severity Colour Coding (v4.6 ST-09 shipped)

Since ST-09 severity field has shipped in Sprint 2, the following severity visualisation is included in the design review scope:

| Severity | Recommended colour treatment | Consistent with |
|----------|------------------------------|-----------------|
| `info` | Neutral / slate | Informational badges in pre-entry validation panel |
| `warning` | Amber / yellow | Override warning pattern from SI-01 panel |
| `critical` | Red | Breached state in SI-02 BehaviouralDriftPanel |

The colour assignment must be consistent with the Arc 5 signal panels (SI-01 PreEntryValidationPanel, SI-02 BehaviouralDriftPanel) to maintain visual coherence.

### 4. Event Type Display

- Label formatting for event types (`pre_entry_override` → "Pre-Entry Override", etc.)
- Context field display — when and how to surface the JSON context object

---

## Out of Scope for Design Review

The following are **not** subject to change in this review:

- **Data structure** — the `red_flag_events` table schema (governed by database.py; changes require a migration story)
- **Backend API contract** — `GET /portfolio/red-flag-journal` response shape (governed by `docs/specs/api_contracts/portfolio_endpoints.md`)
- **Event type taxonomy** — the four event types (`pre_entry_override`, `checklist_skipped`, `stop_prompt_dismissed`, `drawdown_prompt_dismissed`) are canonical
- **Severity values** — the three severity levels (info / warning / critical) are canonical (v4.6 ST-09)
- **Pagination limits** — page size max of 100 is a backend constraint

---

## Gate Date for BLG-FE-41

> **Gate clears: 2026-06-21**

BLG-FE-41 (Red Flag Journal design implementation) is gated on SI-03 being live for ≥30 days. SI-03 went live with v3.9 (2026-05-22). The gate clears on **2026-06-21** (30 days post-v3.9 deployment).

Before 2026-06-21: This scope document is the output. No implementation sprint opens.
After 2026-06-21: Sprint planning for the implementation may proceed, using this scope document as the basis.

---

## Reviewed by

- Product Owner: reviewed and approved 2026-05-30
- Head of UX & Design: reviewed and approved 2026-05-30

---

## Sign-Off

| Role | Status | Date |
|------|--------|------|
| Frontend Specs & UX Documentation Owner | ✅ Approved | 2026-05-30 |
| Head of UX & Design | ✅ Approved | 2026-05-30 |
