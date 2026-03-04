**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-04
**Cycle:** 2026-03-04__release-v1.8

---

# Sprint Goal — 2026-03-04__release-v1.8

## Goal

Ship a fully functional Risk Dashboard page giving the trader daily visibility into portfolio heat, drawdown, grace period status, and per-position risk, while simultaneously establishing automated correctness gates (golden output CI, vulnerability scanning, OpenAPI drift detection) and closing the highest-priority spec and governance debt carried from v1.7.

## Release Context

- **Release:** v1.8
- **Primary feature:** Risk Dashboard page
- **Roadmap item:** §3.4 Risk Dashboard (expanded scope)
- **Supporting scope:** EPIC-02 CI Quality, EPIC-03 Spec Debt, EPIC-04 Governance Docs

## Success Condition

The sprint goal is achieved when:
1. The Risk Dashboard page is live, renders correctly against canonical heat thresholds, and passes all ST-04 acceptance scenarios.
2. Golden output CI baseline, vulnerability scanning, and OpenAPI drift detection are all active in the CI pipeline.
3. `settings_endpoints.md` is corrected and `openapi.yaml` is updated to v1.9.0.
4. Unavailability policy and API changelog documents exist and are lifecycle-compliant.

## Confirmed by

**Product Owner:** Confirmed
**Date:** 2026-03-04
