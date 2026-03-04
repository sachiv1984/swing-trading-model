**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-04
**Cycle:** 2026-03-04__release-v1.8

---

# Lessons Learnt — Release Planning v1.8

**Cycle:** 2026-03-04__release-v1.8
**Release:** v1.8 — Risk Dashboard

---

## LL-01 — Timebox/Capacity Should Be Specified at Invocation

**Observation:** `plan release --version v1.8` was invoked without `--timebox` or `--capacity`. Standard assumptions were applied (2 weeks, solo-dev evenings), but the capacity check returned WARN because the scope significantly exceeds a strict 2-week window.

**Impact:** The WARN is acceptable in standard mode, but the absence of explicit capacity creates ambiguity for Sprint Planning. The FinOps & Resource Architect had to infer from prior release patterns rather than declared constraints.

**Recommendation:** For future releases, specify `--timebox` and `--capacity` explicitly at invocation (e.g., `plan release --version v1.9 --timebox "4 weeks" --capacity "solo-dev evenings"`). This enables a precise capacity check rather than a WARN-based assumption.

**Owner for next cycle:** PMO Lead (to prompt at invocation)

---

## LL-02 — P1 Backlog Items Should Have Clear Release Assignment Before Planning

**Observation:** 7 of 8 BLG-NEW items from IW-20260304-01 are P1 priority. All 7 competed for v1.8 capacity alongside the primary roadmap item. The Release Planning Engine had to make selection decisions (e.g., deferring BLG-NEW-04 and BLG-SPEC-D3) without explicit Product Owner guidance on which P1 items were hard commitments.

**Impact:** Minor scope ambiguity at planning time. The selections made are reasonable but not Product Owner-confirmed.

**Recommendation:** At the roadmap rebalance that introduces BLG-NEW items, explicitly annotate which are v1.8 hard requirements vs v1.8 candidates. This pre-answer removes a scope decision from the Release Planning Engine.

**Owner for next cycle:** Product Owner (to annotate at DL time)

---

## LL-03 — BLG-SPEC-D2 Decision Should Not Enter Release Planning Open

**Observation:** ESC-20260304-01 was raised because BLG-SPEC-D2 (settings endpoint method drift) entered v1.8 planning with an unresolved Product Owner decision (option a vs b). The item has been in the backlog since 2026-03-03. It should have been decided before this cycle opened.

**Impact:** ST-09 is gated; partial EPIC-03 scope is blocked. The release plan is still publishable (Blocks execution: No), but execution will have a hold point.

**Recommendation:** BLG-SPEC items with a "Decision Required" flag should be triaged and decided at the Backlog Management / Roadmap Rebalance stage before entering active release planning. The Product Owner should resolve open decisions on P1 items before `plan release` is issued.

**Owner for next cycle:** Product Owner + PMO Lead (to pre-clear decisions before planning)

---

## LL-04 — Design Gate Engine Is a Hard Pre-Condition for Sprint Planning

**Observation:** EPIC-01 (Risk Dashboard) requires a frontend spec (`risk_dashboard.md`) that does not yet exist. ST-01 is the Design Gate Engine's primary output for this release. This relationship is correctly modelled in the plan, but it means Sprint Planning (`plan sprint`) cannot be issued until the Design Gate run produces and approves the spec.

**Reminder for next phase:** Issue `run design-gate --cycle 2026-03-04__release-v1.8` before `plan sprint`. ST-01 acceptance criteria cannot be finalised without the Design Gate artefact.

**Owner:** PMO Lead
