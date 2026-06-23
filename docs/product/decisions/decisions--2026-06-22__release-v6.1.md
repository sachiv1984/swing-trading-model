Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Superseded by: claude/cycles/2026-06-22__release-v6.1/closure_record.md — post-ship closure 2026-06-23
Release: v6.1
Cycle: 2026-06-22__release-v6.1
Last Updated: 2026-06-23

---

# Decisions Record — v6.1 Governance Correctness, CI Quality & User Value Foundation

---

## Scope Decisions

| # | Decision | Rationale | Authority |
|---|----------|-----------|-----------|
| SD-01 | BLG-FEAT-25/PT-04 classified as Conditional, not Firm | Gate condition (≥20 closed trades) clearing ~2026-07-02 falls within sprint execution window; STEP 1.4b mandatory classification rule applies | Release Planning Engine STEP 1.4b |
| SD-02 | BLG-GOV-134 (CI OpenAPI drift detection) deferred to v6.2 despite Provisional-Target v6.1 | Rebalance Now section (2026-06-22__scheduled) is the authoritative scope source; item absent from Now table; scope-lock rule prohibits additions during planning | Release Planning Engine STEP 2 scope-lock |
| SD-03 | BLG-QA-62 (Playwright glob auto-registration) deferred to v6.2 | Same authority as SD-02; follow-on item to BLG-QA-60 which is included as S2-03 | Release Planning Engine STEP 2 scope-lock |
| SD-04 | BLG-FE-77 (Watchlist.js ESLint compliance) deferred to v6.2 | Same authority as SD-02 | Release Planning Engine STEP 2 scope-lock |
| SD-05 | BLG-GOV-131 (governance overhead ceiling) included as Firm scope | Roadmap Now section table includes as firm; P2 advisory — proposal document and sprint planning ceiling enforcement, XS/S effort | Rebalance 2026-06-22__scheduled Now section |
| SD-06 | design_gate_required = true for this cycle | BLG-FE-76 (SectorHeatMap new component) and BLG-FE-78 (dashboard badge) both carry UI placement and design decisions that cannot be resolved in code — design sign-off required | Release Planning Engine STEP 1.3 scan |

---

## Sequencing Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| SEQ-01 | EPIC-01 (Governance patches) executes first, before sprint planning seals | GOV-132 and GOV-133 patch the release planning and sprint planning engines respectively — these patches must be applied before the sprint planning engine runs for this cycle to benefit from the correctness fixes; Correctness Fast-Track designation |
| SEQ-02 | EPIC-03 (User Value) requires Design Gate to pass before sprint planning seals | BLG-FE-76 (sector heat-map) has architecture and design dependencies that must be resolved before implementation can proceed safely; design gate is a hard gate for EPIC-03 |
| SEQ-03 | EPIC-04 (Conditional PT-04) gated at sprint planning via PMO Lead gate re-check | Sprint planning engine must verify ≥20 closed trades at preflight before EPIC-04 stories enter firm sprint capacity; if gate not met, EPIC-04 returned to backlog |
| SEQ-04 | EPIC-02 (CI Quality) sequenced after EPIC-01; no hard dependency | CI quality items (XS effort) are independent but logically follow governance correctness — ordering is advisory |

---

## Accepted Risks

| RISK-ID | Risk | Disposition | Accepted by |
|---------|------|-------------|-------------|
| RISK-01 | Governance prompt patches (GOV-132/133) require §6 checklist compliance in same commit — missed checklist step leaves prompts non-compliant | Accepted; §6 checklist mandatory in EPIC-01 execution, verified in QA evidence | Head of Specs Team |
| RISK-02 | CI changes to playwright.yml could inadvertently break existing spec execution | Accepted; full CI run required as DoD after playwright.yml change | Director of Quality |
| RISK-03 | BLG-FE-76 sector heat-map requires new backend endpoint (sector weight aggregation) not yet specced — spec ambiguity risk | Accepted; design gate resolves endpoint spec before EPIC-03 sprint planning | Head of UX & Design; Product Owner |
| RISK-04 | PT-04 gate (≥20 closed trades) may not clear by sprint seal date | Accepted; conditional classification and sprint planning gate re-check mitigate; EPIC-04 returned to backlog if gate not met | PMO Lead |

---

## Supersession Note

*Blank at planning time. To be completed if scope is amended or cycle superseded.*
