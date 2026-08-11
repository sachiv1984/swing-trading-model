**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-09 (Product Owner direct action — IDEA-cybersecurity-20260304-02 entry marked Resolved as superseded by BLG-OPS-71's threat_model.md §3; prior — PMO Lead direct action, post-ship closure 2026-07-08__release-v6.8 outstanding actions — IDEA-cybersecurity-20260304-01 entry marked Resolved, delivered as BLG-OPS-71/ST-17; entries retained per append-only write scope)

---

# Rejected-But-Strong Ideas Register

This document captures ideas that were rejected from active roadmap/backlog consideration but carry enough merit that they should be reconsidered when the blocking condition is resolved. These are not permanently closed — they are deferred pending a specific gate.

---

## IDEA-strategy-owner-20260304-02 — ATR Parameter Sensitivity Analysis

**Submitter:** Strategy Rules & System Intent Owner
**Window:** IW-20260304-01 (2026-03-04)
**Rejected in:** 2026-03-17__item-v1.10

**Core idea:** Systematic sensitivity analysis of current ATR multiplier parameters to validate or refine the strategy's numerical constants. Would produce evidence for whether current ATR settings are well-calibrated or should be adjusted.

**Why rejected:** Any formal analysis that could lead to ATR parameter changes requires a §13.2 boundary review (strategy is a versioned behavioural contract; parameter changes require formal versioning). No §13 review path is currently open. Cannot advance without a formal §13 gate clearance process.

**Revival condition:** §13 review opened specifically for ATR parameter calibration; Strategy Rules & System Intent Owner proposes scope and evidence criteria; new §13.2 review documented.

---

## IDEA-challenger-20260304-01 — Force Explicit Evidence Review for ATR Parameter Selection

**Submitter:** Challenger
**Window:** IW-20260304-01 (2026-03-04)
**Rejected in:** 2026-03-17__item-v1.10

**Core idea:** Governance mechanism requiring explicit evidence review (e.g. backtested sensitivity data) before any ATR parameter is selected or changed. Would add a documented review gate to the strategy parameter selection process.

**Why rejected:** Companion to IDEA-strategy-owner-20260304-02 (above). Same §13 constraint applies: strategy parameters are a versioned behavioural contract; changing the review process for parameters requires the same §13 scope decision.

**Revival condition:** Same as IDEA-strategy-owner-20260304-02. Both ideas should be considered together if §13 ATR review is opened.

---

## IDEA-cybersecurity-20260304-01 — System Threat Model Document

**Submitter:** Cybersecurity & Trust Lead
**Window:** IW-20260304-01 (2026-03-04)
**Rejected in:** 2026-03-17__item-v1.10

**Core idea:** Formal threat model document for the system — identifying attack surfaces, threat actors, data sensitivity levels, and mitigations. Particularly relevant for a system handling real financial data (positions, P&L, stop levels).

**Why rejected:** No active security incident or compliance requirement driving urgency. Current single-user deployment limits immediate threat surface. Strong merit as pre-scale governance — rejected only due to timing and capacity constraints.

**Revival condition:** System approaches multi-user scale, external exposure increases, or a security-related compliance requirement emerges. Should be prioritised at that point without a new idea submission.

**PMO Lead Decision (2026-07-09):** Revival condition confirmed **Met** — the strategic review of 2026-06-18 (external exposure: real position data, stop levels, P&L, and multiple billing-exposed API credentials across staging + production) triggered a direct revival ahead of a formal re-submission, and the threat model was delivered in full at cycle `2026-07-08__release-v6.8` (ST-17, `BLG-OPS-71`).

**Status: RESOLVED (2026-07-09, post-ship closure 2026-07-08__release-v6.8).** Delivered as `docs/security/threat_model.md` v1.0 — covers attack surfaces, data classification, threat actors, and current mitigations per this entry's original scope; 2 new gaps found and filed (`BLG-SEC-12`, `BLG-SEC-13`); dual sign-off from Cybersecurity & Trust Lead and Infrastructure & Operations Owner. This entry is retained per the write-scope append-only rule for this file (governed routines may not delete `rejected_but_strong.md` entries) — kept for audit trail, superseded by `BLG-OPS-71`.

---

## IDEA-cybersecurity-20260304-02 — Sensitive Data Classification Policy

**Submitter:** Cybersecurity & Trust Lead
**Window:** IW-20260304-01 (2026-03-04)
**Rejected in:** 2026-03-17__item-v1.10

**Core idea:** Formal data classification policy defining sensitivity levels for all data handled by the system (position data, P&L, stop levels, user preferences) and appropriate handling requirements for each level.

**Why rejected:** Same reasoning as IDEA-cybersecurity-20260304-01. Strong merit as pre-scale governance work. No immediate compliance driver.

**Revival condition:** Same as IDEA-cybersecurity-20260304-01. Complementary to the threat model — both should be considered together.

**Product Owner Decision (2026-07-09): Resolved as superseded — no standalone document commissioned.** The companion threat model (`docs/security/threat_model.md`, `BLG-OPS-71`) shipped with its own §3 Data Classification table covering exactly this idea's original scope: API keys/secrets (CRITICAL), position data/stop levels/P&L (HIGH), signals/screener results (MEDIUM), settings/user preferences (MEDIUM), AI audit logs (MEDIUM) — with rationale per tier. Combined with the existing `docs/specs/security/trade_plan_data_sensitivity.md` (trade-plan field-level classification plus per-tier access control rules, live since v3.3), the system now has a written, sensitivity-tiered view of all data it handles. A dedicated standalone "Sensitive Data Classification Policy" document would substantially duplicate `threat_model.md §3` for no added value — the natural home for a system-wide classification table turned out to be the threat model itself, not a separate artefact. Checked for the one real gap versus `trade_plan_data_sensitivity.md`'s pattern (explicit per-tier access-control/handling rules beyond trade-plan fields): the system's single shared-API-key auth model doesn't support per-tier ACLs the way trade-plan portfolio-scoping does, so a system-wide access-control writeup wouldn't currently describe anything beyond "authenticate, then trust" — not a gap worth a dedicated document today. If a genuine handling-requirement gap surfaces later (e.g. at incident review or a future audit), file it as a specific `BLG-SEC` item at that time rather than reviving this broader idea.

**Status: RESOLVED (2026-07-09, Product Owner direct action).** This entry is retained per the write-scope append-only rule for this file — kept for audit trail, superseded by `BLG-OPS-71` (`docs/security/threat_model.md` §3).

---

## IDEA-ai-compliance-20260321-01 — Governed Decision Audit Log

**Submitter:** AI Compliance & Governance Officer
**Window:** IW-20260321-01 (2026-03-21)
**Rejected in:** cycle 2026-05-05__scheduled (strong)

**Core idea:** Searchable record of all governance decisions (roadmap additions, sprint commitments, deviation approvals) in structured format — enabling retrospective audit of why specific governance decisions were made.

**Why rejected:** `decision_log.md` provides adequate partial coverage at current governance volume. Searchable audit log with structured format deferred until governance volume increases substantially and the overhead of structured decision capture is warranted. Rejected as strong because the idea has genuine merit — current tooling is adequate but would not scale to a higher-volume governance environment.

**Revival condition:** Governance decision volume increases substantially (e.g. concurrent multi-team delivery, external audit requirements, or compliance review mandating structured decision capture). PMO Lead to raise for re-evaluation at that point.

---

## IDEA-pmo-lead-20260619-02 — Sprint Velocity Trend Chart

**Submitter:** PMO Lead
**Window:** IW-20260619-01 (2026-06-19)
**Rejected in:** 2026-06-24__scheduled (3-cycle hard cap; third consecutive park decision)

**Core idea:** A visualisation of sprint velocity trend across the last 10 rebalance cycles — delivered stories per sprint, U/G/D story breakdown, and delivery rate. Would make velocity trajectory immediately visible at rebalance time rather than requiring manual changelog analysis.

**Why rejected:** velocity_metrics.md (the canonical data source) does not exist. The underlying data infrastructure for automated velocity trending has not been established. Building a chart before the data file exists would produce nothing actionable. Hard cap reached at third consecutive park.

**Revival condition:** velocity_metrics.md created and populated with at least 5 cycles of structured data (story counts, U/G/D classification, delivery rate). PMO Lead to assess and raise for re-evaluation once the file is established and updated for 2+ rebalances.

**PMO Lead Decision (2026-07-08):** Revival condition confirmed **Met** — `velocity_metrics.md` now carries 49 structured rows spanning far more than 5 cycles and 2 rebalances (created 2026-07-03, updated at every post-ship closure since, most recently 2026-07-08 for v6.7). Decision: resubmit this idea at the next `run ideas` intake window rather than let it carry a third time.

**Status: RESOLVED (2026-07-08, roadmap rebalance 2026-07-08__scheduled).** Resubmitted as `IDEA-pmo-lead-20260708-01` in window `IW-20260708-01`, classified Backlog (gate-conditional) at STEP 4, added to `backlog.md` as `BLG-GOV-188`. This entry is retained per the write-scope append-only rule for this file (roadmap engine may not delete rejected_but_strong.md entries) — kept for audit trail, superseded by `BLG-GOV-188`.

---

## IDEA-challenger-20260809-02 — SI-02 Gate Threshold Calibration Challenge (9+ consecutive NOT MET readings)

**Submitter:** Challenger
**Window:** IW-20260809-01 (2026-08-09)
**Rejected in:** 2026-08-11__scheduled (strong)

**Core idea:** Challenge whether the SI-02 ≥20-linked-trade-plans gate threshold is genuinely calibrated for this system's actual single-user trade cadence, given 9+ consecutive scheduled-rebalance readings of NOT MET with 0 linked trade plans throughout.

**Why rejected:** This exact question was formally reviewed and answered 4 days prior to this submission — `BLG-GOV-237` ("SI-02 trade-count gate threshold calibration review") shipped in `v8.3` (2026-08-07) with a documented conclusion of "still appropriate." Re-opening the same question without new evidence beyond what `BLG-GOV-237`'s review already considered is not a valid basis to re-litigate a recently-closed formal determination. Rejected as strong because the underlying concern is legitimate and well-evidenced (the 9+ consecutive NOT MET streak is real and is the single largest structural blocker in the current roadmap — see `cycle_record.md` 2026-08-11__scheduled STEP 2.3/STEP 7.1) — the rejection is about timing and duplication, not about the merit of eventually revisiting gate calibration.

**Revival condition:** Material new evidence not considered by `BLG-GOV-237`'s review — e.g. a materially changed trade cadence, a structural change to how trade plans are linked (such as `BLG-BE-91`, filed this same cycle, landing and still failing to move the linked-count), or a sustained further period (e.g. 6+ more months) of zero linked trade plans despite `BLG-BE-91`'s enforcement fix being live. Head of Specs Team or Strategy Rules & System Intent Owner to raise for re-evaluation if any of these occur.
