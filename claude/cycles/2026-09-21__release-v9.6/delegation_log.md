Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-22 (DEL-20260921-01 Unblocked — ST-09 trailing-stop entry-floor decision ratified); prior — 2026-09-21 (cycle open, 6 delegation records created)

---

# Delegation Log - 2026-09-21__release-v9.6

Append-only. Do not edit previous entries.

---

## DEL-20260921-01

- **ST Item:** ST-09 - calculate_trailing_stop's entry-price floor for profitable positions diverges from strategy_rules.md §7.2/§7.3 and from the backtest tool
- **EPIC:** EPIC-03
- **Classification:** delegated_decision
- **Assigned to:** Strategy Rules & System Intent Owner
- **GitHub Issue:** #1726
- **Branch:** exec/2026-09-21__release-v9.6/EPIC-03
- **Delegated at:** 2026-09-21T15:51:14Z
- **What is needed:** Confirm/rule on the trailing-stop entry-price-floor decision (options i/ii/iii in ESC-EXEC-20260921-01); engine will add the golden-output case autonomously.
- **Unblock criteria:** see ESC-EXEC-20260921-01
- **Commit format required:** `[EPIC-03][ST-09] <description>` pushed to `exec/2026-09-21__release-v9.6/EPIC-03` (EPIC branch is cut from post-merge main at that EPIC's turn)
- **Status:** Unblocked — in-session credential/action provisioning not applicable (no external credential needed); Strategy Rules & System Intent Owner ruling obtained directly within this session (agent-mediated, §5.3, on explicit user direction) per execution_prompt.md §5.2. Ruling: Option (i) — see ESC-EXEC-20260921-01 Resolution (Addendum) for full rationale. Sign-off cleared 2026-09-22T08:14:51Z; commit `f771d5c9` pushed same timestamp (golden-output case + implementation cross-check). No multi-session parking occurred (LL-v8.2-P3-04 in-session completion pattern).

---

## DEL-20260921-02

- **ST Item:** ST-16 - Confirm synthetic uptime monitor live-fire and notification delivery (ST-11 follow-up)
- **EPIC:** EPIC-04
- **Classification:** delegated_decision
- **Assigned to:** Infrastructure & Operations Owner
- **GitHub Issue:** #1733
- **Branch:** exec/2026-09-21__release-v9.6/EPIC-04
- **Delegated at:** 2026-09-21T15:51:14Z
- **What is needed:** Perform/enable the Actions-write live-fire run and confirm real Telegram receipt (ESC-EXEC-20260921-02).
- **Unblock criteria:** see ESC-EXEC-20260921-02
- **Commit format required:** `[EPIC-04][ST-16] <description>` pushed to `exec/2026-09-21__release-v9.6/EPIC-04` (EPIC branch is cut from post-merge main at that EPIC's turn)
- **Status:** Pending

---

## DEL-20260921-03

- **ST Item:** ST-22 - DS-17 unique index migration not yet applied to live positions table
- **EPIC:** EPIC-06
- **Classification:** delegated_decision
- **Assigned to:** Data Model & Domain Schema Owner + Infrastructure & Operations Owner
- **GitHub Issue:** #1739
- **Branch:** exec/2026-09-21__release-v9.6/EPIC-06
- **Delegated at:** 2026-09-21T15:51:14Z
- **What is needed:** Apply the DS-17 up-migration to the live positions table after re-running the duplicate pre-check, and confirm (ESC-EXEC-20260921-04).
- **Unblock criteria:** see ESC-EXEC-20260921-04
- **Commit format required:** `[EPIC-06][ST-22] <description>` pushed to `exec/2026-09-21__release-v9.6/EPIC-06` (EPIC branch is cut from post-merge main at that EPIC's turn)
- **Status:** Pending

---

## DEL-20260921-04

- **ST Item:** ST-23 - PO-05 (Lightweight Replay Mode) §13 determinism pre-clearance review, standalone
- **EPIC:** EPIC-06
- **Classification:** delegated_decision
- **Assigned to:** Strategy Rules & System Intent Owner
- **GitHub Issue:** #1740
- **Branch:** exec/2026-09-21__release-v9.6/EPIC-06
- **Delegated at:** 2026-09-21T15:51:14Z
- **What is needed:** Issue the dated §13 determination for PO-05 (ESC-EXEC-20260921-05).
- **Unblock criteria:** see ESC-EXEC-20260921-05
- **Commit format required:** `[EPIC-06][ST-23] <description>` pushed to `exec/2026-09-21__release-v9.6/EPIC-06` (EPIC branch is cut from post-merge main at that EPIC's turn)
- **Status:** Pending

---

## DEL-20260921-05

- **ST Item:** ST-28 - Re-confirm §13 boundary review cadence
- **EPIC:** EPIC-07
- **Classification:** delegated_decision
- **Assigned to:** Strategy Rules & System Intent Owner
- **GitHub Issue:** #1745
- **Branch:** exec/2026-09-21__release-v9.6/EPIC-07
- **Delegated at:** 2026-09-21T15:51:14Z
- **What is needed:** Decide schedule-now vs defer-with-concrete-trigger for the §13 boundary review (ESC-EXEC-20260921-06).
- **Unblock criteria:** see ESC-EXEC-20260921-06
- **Commit format required:** `[EPIC-07][ST-28] <description>` pushed to `exec/2026-09-21__release-v9.6/EPIC-07` (EPIC branch is cut from post-merge main at that EPIC's turn)
- **Status:** Pending

---

## DEL-20260921-06

- **ST Item:** ST-29 - Revisit sprint capacity band given sustained ≥90% utilisation
- **EPIC:** EPIC-07
- **Classification:** delegated_decision
- **Assigned to:** Product Owner
- **GitHub Issue:** #1746
- **Branch:** exec/2026-09-21__release-v9.6/EPIC-07
- **Delegated at:** 2026-09-21T15:51:14Z
- **What is needed:** Supply the hold/raise decision on the sprint capacity band (ESC-EXEC-20260921-07).
- **Unblock criteria:** see ESC-EXEC-20260921-07
- **Commit format required:** `[EPIC-07][ST-29] <description>` pushed to `exec/2026-09-21__release-v9.6/EPIC-07` (EPIC branch is cut from post-merge main at that EPIC's turn)
- **Status:** Pending

---

