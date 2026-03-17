**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-17

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

---

## IDEA-cybersecurity-20260304-02 — Sensitive Data Classification Policy

**Submitter:** Cybersecurity & Trust Lead
**Window:** IW-20260304-01 (2026-03-04)
**Rejected in:** 2026-03-17__item-v1.10

**Core idea:** Formal data classification policy defining sensitivity levels for all data handled by the system (position data, P&L, stop levels, user preferences) and appropriate handling requirements for each level.

**Why rejected:** Same reasoning as IDEA-cybersecurity-20260304-01. Strong merit as pre-scale governance work. No immediate compliance driver.

**Revival condition:** Same as IDEA-cybersecurity-20260304-01. Complementary to the threat model — both should be considered together.
