**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-15
**Cycle:** 2026-09-15__release-v9.5

# Design Gate Record — 2026-09-15__release-v9.5

## Gate Status: PASSED

Completed: 2026-09-15
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

43 of 43 items cleared — 3 Design Required (ST-41, ST-42, ST-43), 1 Design Pre-Approved (ST-40 — existing convention covers a missed call site), 39 Design Not Applicable (pure backend/ops/CI-CD/test-coverage/spec-documentation/governance-process items with no user-visible effect). No blocked items. `sprint_planning_pre_condition` is met.

**Classification note:** the sealed backlog slice flagged all 4 EPIC-06 items (`BLG-FE-177`/ST-40, `BLG-FE-175`/ST-41, `BLG-FE-176`/ST-42, `BLG-UX-05`/ST-43) as `design_gate_required: true` at Release Planning (all carry an observable UI acceptance criterion). STEP 1 review confirmed all 4 as genuinely design-gate-relevant; ST-41/ST-42 also independently qualify under the §6 motion/timing-sensitive-interaction special rule (BLG-FE-131). ST-40 was reviewed and downgraded from the default Design Required to Design Pre-Approved on explicit confirmation (see its Rationale cell) — an already-established, already-spec'd convention (`trade_plan.md` §9 Status Badge Scheme / `STATUS_LABELS`) applies directly; no new visual/interaction decision is needed, only correct application at a missed call site.

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | CI-blocking test_changelog_service.py failure | Design Not Applicable | CI test fix, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-02 | Backend logging JSON Lines format | Design Not Applicable | Backend/infra log format, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-03 | Validate limit/offset on screener endpoints | Design Not Applicable | Backend API param validation (400 vs 500), no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-04 | Consolidate ATR trailing-stop recalculation logic | Design Not Applicable | Backend logic consolidation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-05 | nightly-stop-update / rebalance-exit live trigger | Design Not Applicable | Ops/scheduler investigation + wiring, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-06 | AI audit log cost-monitoring follow-ons | Design Not Applicable | Backend/ops cost-monitoring sub-items, no UI. §13 pre-check: extends monitoring of already-shipped AI-audit-log data, does not introduce/extend an AI-provider call — pre-check does not apply. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-07 | api_call_log retention/purge policy | Design Not Applicable | DB retention/purge, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 | get_api_session_report() self-inclusive baseline | Design Not Applicable | Backend anomaly-baseline logic fix, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 | api_performance_baseline.md new endpoint row | Design Not Applicable | Docs + live measurement re-run, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | Recurring quarterly hosting-cost trend review | Design Not Applicable | Process cadence + first review, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 | Synthetic uptime monitor for /health | Design Not Applicable | Infra/observability monitor, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 | Document dashboard-only deploy path-filter gotcha | Design Not Applicable | Ops runbook doc, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 | claude_audit_log latency column / real anomaly data | Design Not Applicable | DB column + backend wiring for an existing anomaly-check endpoint's real data source, no UI. §13 pre-check: supplies real latency data to an already-shipped AI-endpoint-monitoring check, does not itself introduce/extend an AI-provider call — pre-check does not apply. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-14 | Provision read-only staging DATABASE_URL | Design Not Applicable | Infra/credential provisioning, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-15 | Arc 4 E2E test strategy pre-design (PO-02/03/04) | Design Not Applicable | Test-strategy document, no UI. §13 pre-check: defines a *mocking* approach for future PO-02/03/04 AI calls (no real AI call introduced); the PO-02/03/04 boundary question itself is owned by `BLG-SPEC-35` (open, P1) and this item does not bypass it — pre-check does not apply to this planning-only item. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-16 | Extract governance_sync.yml bash logic | Design Not Applicable | CI/CD tooling refactor, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 | Unit test coverage for check_contract_example_freshness.py | Design Not Applicable | Backend test coverage, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 | Playwright coverage matrix stale file-inventory count | Design Not Applicable | Docs correction, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 | ST-09 cross-browser evaluation stale CI baseline | Design Not Applicable | Docs correction, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-20 | SignalCard spec consolidation runtime evidence | Design Not Applicable | Docs correction (evidence recording), no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 | qa_evidence_EPIC-03.md test-count claim | Design Not Applicable | Docs correction, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-22 | data_model.md positions table live-schema confirmation | Design Not Applicable | Spec verification note, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-23 | Arc 4 API contract pre-authoring (PO-02/03/04) | Design Not Applicable | Stub contract files only, explicitly "No implementation" per the item's own scope — no code path calls an AI provider. §13 pre-check considered: `BLG-SPEC-35` (PO-02 §13 boundary review) remains open/P1/unresolved; this item's own AC explicitly routes new boundary questions *to* that open review rather than bypassing it, and Arc 4 (PO-02/03/04) itself remains data-density-gate-blocked (~2026-10). Pre-check does not apply to a stub-only, non-implementing item — consistent with the `2026-09-14__release-v9.4` gate's treatment of AI-adjacent non-calling items (ST-09/ST-10/ST-21/ST-22/ST-23 there). Flagged to Strategy Rules & System Intent Owner for awareness that `BLG-SPEC-35` should not remain open indefinitely once Arc 4 pre-authoring work begins landing. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-24 | Data model v3 pre-definition for Arc 4 journal intelligence | Design Not Applicable | Schema pre-definition document only, no migration SQL, no UI. §13 pre-check: same basis as ST-23 — pre-definition only, no AI-provider call introduced or extended; `BLG-SPEC-35` remains the governing open review. Pre-check does not apply. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-25 | position_endpoints.md example JSON reconciliation | Design Not Applicable | Docs fix (internal consistency of an example payload), no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-26 | Triage contract example-payload freshness findings | Design Not Applicable | Docs/script triage, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-27 | Path-aware check_orphaned_specs.py | Design Not Applicable | Detector tooling change, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-28 | Spec debt dashboard sort key mishandles same-day items | Design Not Applicable | `docs/specs/spec_debt_dashboard.md` is a generated Class 3 markdown operational record (`scripts/generate_spec_debt_dashboard.py`), not a rendered app page — confirmed no `src/` reference to it. No UI. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-29 | Canonical position/trade lifecycle state diagram | Design Not Applicable | Diagram added to `data_model.md` (governance/spec documentation), not an app-rendered UI element | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-30 | Consolidate divergent empty-state copy patterns | Design Not Applicable | AC is confirm-and-document only ("Confirmed status... recorded"; "Canonical pattern documented if a genuine remaining gap is confirmed") — no shipped UI copy change is required by this item's own acceptance criteria; if a genuine gap is confirmed during execution and a copy change is made, that would need its own design-gate pass at that time. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-31 | Resolving-commit Known Deviation field discipline | Design Not Applicable | Governance process rule, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-32 | Wire wall-clock cost logging (§22) into an engine's STEP list | Design Not Applicable | Governance prompt instrumentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-33 | Codify opportunistic in-file fixes backlog-entry rule | Design Not Applicable | Governance process rule, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-34 | record-visual-qa skill doc drift reconciliation | Design Not Applicable | Skill documentation reconciliation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-35 | PO decision record for ST-20 trade-tagging taxonomy call | Design Not Applicable | Decision-record filing, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-36 | Lightweight role-retirement process | Design Not Applicable | Governance process, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-37 | Cross-role pairing rotation note | Design Not Applicable | Governance doc note, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-38 | Cost-per-cycle wall-clock rollup | Design Not Applicable | Governance doc rollup table, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-39 | Formalise STEP 8.0.5/8.2 candidate-verification subroutine | Design Not Applicable | Governance prompt refactor, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-40 | Fix trade plan link display: formatted text not snake_case | Design Pre-Approved | Flagged `design_gate_required: true` at Release Planning; reviewed and downgraded — the raw value is `TradeEntry.js`'s "Link to Trade Plan" `<Select>` rendering `plan.status` unformatted. An already-approved, already-spec'd convention exists (`trade_plan.md` §9 Status Badge Scheme, backed by `TradePlan.js`'s own `STATUS_LABELS` map) that this call site simply fails to apply — not a new visual/interaction decision, a missed application of an existing one. Product Owner confirmed the downgrade. | N/A | `trade_plan.md` v1.12 (existing, locked reference — §9 Status Badge Scheme / `STATUS_LABELS` convention applies as-is) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-41 | Bring 4 motion-timing non-compliant components under 500ms | Design Required | Motion/timing-sensitive-interaction special rule (§6, BLG-FE-131) — always Design Required. Target release (this cycle) and per-component remediation approach were already fixed at the `2026-09-14__release-v9.4` design gate; this story is the implementation of that already-approved plan. | `docs/design/2026-09-14__release-v9.4/motion-timing-target-release/decision_record.md` (existing, reviewed and confirmed current) | `design_system.md` v1.14 §Accessibility (existing, confirmed current — no change this gate) | ✅ Cleared | Head of UX & Design |
| ST-42 | Bring 9 non-conforming toast call sites into line with Toast Notification Timing standard | Design Required | Motion/timing-sensitive-interaction special rule (§6, BLG-FE-131) — toast duration is timing behaviour. The standard and the exact 9-call-site inventory were already fixed at the `2026-09-14__release-v9.4` design gate; this story is the implementation of that already-approved plan. | `docs/design/2026-09-14__release-v9.4/toast-timing-standard/decision_record.md` (existing, reviewed and confirmed current) | `design_system.md` v1.17 §Shared UI Components → Toast Notification Timing (existing, confirmed current — no change this gate) | ✅ Cleared | Head of UX & Design |
| ST-43 | Arc 5 low-trade-volume advisory: threshold/remaining-count + placement | Design Required | New copy content (threshold + remaining-trades count) and a layout/placement change (below → above the stat grid) — both explicit §6 Design Required criteria ("new data displayed", "changed interaction/layout"). New decision produced this gate, extending the `2026-09-07__release-v9.2` advisory decision. Confirmed no existing Playwright assertion (`SC-ARC5-09`/`SC-ARC5-10a/b/c`) depends on wording removed or DOM order changed — copy is a pure append preserving both substrings the tests assert; placement reorder has no order-dependent assertion. | `docs/design/2026-09-15__release-v9.5/arc5-low-volume-advisory-placement/decision_record.md` (new, produced this gate) | `arc5_compliance_section.md` v1.3.0 → v1.4.0 (bumped this gate) | ✅ Cleared | Head of UX & Design + Product Owner |

## Blocked Items

None.

## Notes

- **§13 pre-check scope:** every item was checked against the mandatory §13 boundary pre-check (STEP 1). No item in this cycle's 43-item scope introduces or extends a *new* call to an AI/LLM provider. The AI-adjacent items (ST-06, ST-13, ST-15, ST-23, ST-24) all monitor, audit, prepare mocking strategy for, or pre-author non-implementing specification surface around an already-shipped or still-data-gated AI touchpoint, rather than adding a new live call — flagged individually in the Rationale column above for traceability. `BLG-SPEC-35` (PO-02 §13 boundary review) remains open/P1/unresolved and is the governing review for when Arc 4 (PO-02/03/04) implementation work — not pre-authoring — is eventually scheduled; ST-23/ST-24 explicitly route new boundary questions to it rather than bypassing it.
- **Motion/timing-sensitive interactions (§6, BLG-FE-131):** two items this cycle — ST-41 and ST-42 — both classified Design Required under the special rule. Both are implementation of remediation plans already fixed and approved at the prior (`2026-09-14__release-v9.4`) design gate; no new design decision was required, only confirmation the existing artefacts and frontend spec sections remain current, which Head of UX & Design did (STEP 2.1).
- **Downgrade recorded (§6 disagreement clause):** ST-40 was flagged `design_gate_required: true` at Release Planning (default-to-Design-Required for any observable UI AC) and downgraded to Design Pre-Approved this gate on Product Owner's explicit confirmation, per §6's "Product Owner explicitly accepts a lower classification" provision — see its Rationale cell for the basis (existing, already-spec'd `STATUS_LABELS` convention applies directly; no new decision needed).
- **Design artefacts produced this run:** `arc5-low-volume-advisory-placement` (new, ST-43), under `docs/design/2026-09-15__release-v9.5/`. ST-41 and ST-42 reused existing artefacts from `docs/design/2026-09-14__release-v9.4/` without modification.
- **Frontend specs touched:** `docs/specs/frontend/components/arc5_compliance_section.md` v1.3.0 → v1.4.0 (Low-Trade-Volume Advisory copy + placement, ST-43). No other frontend spec required a version bump this gate — `trade_plan.md`, `design_system.md` were confirmed current as locked references only.
