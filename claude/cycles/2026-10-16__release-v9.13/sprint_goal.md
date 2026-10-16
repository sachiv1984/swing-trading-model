# Sprint Goal — 2026-10-16__release-v9.13

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-10-16
**Cycle:** 2026-10-16__release-v9.13

## Goal

Make the Daily Position Monitor's exit confirmation record real exits through `POST /positions/{id}/exit` (BLG-FE-226, P1), give exit reasons one allowed list mapped to §8, and make CI fail on any frontend call to a route that does not exist. Also ship v9.13's stop and sizing correctness, AI output safety, operations and governance items.

## Release Context

- Release: v9.13
- Feature: v9.13 — Monitor Exit Fix, Exit Reasons & API Call Integrity
- Roadmap item: `BLG-FE-226` (Monitor exit confirmation calls a missing route, P1), with `BLG-FE-227` and `BLG-BE-182` (P2). All three are committed in the `current_roadmap.md` v9.13 section by rebalance `2026-10-16__scheduled` (DL-086). The follow-through on the defect class comes from EPIC-04 (`BLG-QA-228`, `BLG-QA-227`).

## Confirmed by

Product Owner: Confirmed (as drafted)
Date: 2026-10-16
