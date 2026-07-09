**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-09 (PMO Lead direct action, post-ship closure 2026-07-08__release-v6.8 outstanding actions — IDEA-cybersecurity-20260304-01 entry marked Resolved, delivered as BLG-OPS-71/ST-17; entry retained per append-only write scope)

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
