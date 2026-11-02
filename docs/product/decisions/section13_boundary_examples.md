**Owner:** Strategy Rules & System Intent Owner; Head of Specs Team
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-11-02 (created — ST-52, EPIC-07, v9.14, BLG-GOV-186)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Companion to:** `claude/strategy/strategy_rules.md` §13 (System boundaries). This document explains §13 with examples; it does not amend it. Where the two disagree, §13 governs.

---

# Section 13 Boundary — Worked Examples

## Purpose

`strategy_rules.md` §13 says what this system is and is not. Most §13 questions in recent cycles were not about the principle but about where a specific feature or sentence falls. This document gives one or two "inside the boundary" and "outside the boundary" examples for each sub-clause, taken where possible from real rulings, so a designer, spec author or reviewer can check a proposal against a precedent before raising a review. An example here never replaces a §13 review where §13 requires one.

Each example names the clause it illustrates and, where one exists, the ruling or review record behind it.

## §13.1 — What this system is

A deterministic, risk-managed momentum framework running one explicit, human-designed strategy, with a human in the loop.

**Inside the boundary**
- **Fail-closed entry check on missing data.** When a market's index data cannot be measured, the pre-entry regime check fails for that market and new entries there are blocked until it is measured; open positions keep their stops (`ESC-EXEC-20261029-01`, v9.14 ST-03). Same inputs, same answer, and the human still decides every trade.
- **Position size from a written formula.** US sizing is `RiskAmount × FX / StopDistance`, stated in §4.1.3 (`ESC-EXEC-20261030-01`, v9.14 ST-09). The system calculates; the user places the order.

**Outside the boundary**
- **Silently assuming a value.** Treating an unmeasured regime as risk-on, or a failed FX fetch as a fixed 1.27, makes the output depend on a hidden default rather than the rule. This is why v9.14 ST-03 to ST-05 replaced both with a visible unknown or last-known state.
- **A "smart" default that varies by user history.** For example, choosing a stop multiple per user from their past results. That is no longer a single explicit strategy (§13.2, "adaptive").

## §13.2 — What this system is not

Not a trading bot, broker, adaptive or multi-strategy platform, ML/AI prediction system, options/futures system, or real-time execution system.

**Inside the boundary**
- **AI text that describes, with code-checked guardrails.** The journal summary may say "Stops were tightened after the loss." (past tense, a description of the notes). Code fails the summary on advisory wording such as "Consider tightening stops on volatile names." (`ESC-EXEC-20261030-02`, v9.14 ST-15). The AI describes; it does not advise a change.
- **Attributing a note only to the position it is about.** A chat stop-time note is attached to the focus ticker only when the sentence names no other ticker-like token (`ESC-EXEC-20261030-03`, v9.14 ST-17). The system does not present text as being about a position it is not about.

**Outside the boundary**
- **"Auto-exit when the stop is hit."** Placing or simulating an order on the user's behalf makes it an execution engine. Stops are shown and recalculated; the exit is always a manual action (§8).
- **An AI suggestion to change the rules.** For example "Your win rate would improve with a 3× ATR stop." That is an AI-driven, adaptive recommendation about the strategy itself, whatever the confidence.

## §13.3 — Design boundary rationale, including the gap-risk display-only carve-out

Human-in-the-loop is a principle. Gap risk monitoring is excluded, except for a display-only flag computed on request, tied to a known, dated, ticker-specific event before the next session, already recognised by a canonical rule. The strategy stays fixed.

**Inside the boundary**
- **Earnings gap-risk flag, US positions, on request.** The Overnight/Weekend Gap Risk Flag shows when a US position has a scheduled earnings date (§4.2.3) between tomorrow and the next trading day. It is computed when the page loads, is specific to that ticker's event, and the user can act on it with a manual exit (§8.3) before the gap (`decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md`, v9.10 addendum).
- **A fixed, explicit strategy shown as such.** Showing the active strategy version and its Change Log is in bounds: the strategy is visible, not configurable.

**Outside the boundary**
- **The removed weekend-hold trigger.** Flagging every open position each Friday is uniform across positions and tied to no ticker-specific event. §13.3 calls that noise without a decision, and it was removed in v9.10 (`BLG-BE-136`).
- **"Gap alert" push notification, or a realised-gap detector.** Evaluating in the background, notifying, or reacting after a gap has happened are each named exclusions. Adding a new event type (for example ex-dividend dates) to the flag also needs its own §13 review before it ships, even if it is display-only.

## §13.4 — On-demand compliance recheck continuity note

A user-triggered re-run of SI-01's existing deterministic rules against one open position, with no new rule logic, scheduling, persistence or SI-02 interaction.

**Inside the boundary**
- **"Recheck Compliance" on one position.** The user presses the button, the existing SI-01 checks run against current data, and the result is shown until the modal closes (BLG-FEAT-64, v6.9).
- **Fixing a bug in an existing SI-01 check.** Correcting a check so it matches its written rule changes no boundary: the recheck still re-runs approved logic.

**Outside the boundary**
- **"Recheck all positions every morning".** Scheduling the recheck turns an on-demand action into background evaluation, which §13.4 states it does not have. It would need its own review.
- **Saving the recheck result as a standing "non-compliant" badge.** Persisting a flag creates a new decision surface; the §13.4 clearance depends on the result being point-in-time.

## §13.5 — Semi-annual boundary re-attestation cadence

Every roster feature with a §13 clearance is re-confirmed every 6 months; a new feature joins the roster in the same commit that records its own clearance.

**Inside the boundary**
- **Joining the roster with the clearance.** ST-25's monthly P&L narrative (v9.11) recorded its CONDITIONAL review and added its roster row together, naming the binding condition that re-attestation must check (Condition 5).
- **Re-attesting a narrowed feature.** The v9.14 ST-17 ruling narrowed when a code-written stop note is attached. At the next re-attestation, the BLG-FEAT-50/51 row records it as covered by the existing clearance ("narrows a code-written note, adds no AI authority"), with no full re-review.

**Outside the boundary**
- **Shipping a cleared AI feature without a roster row.** The cadence then never re-checks it. The thesis-generation contract was in exactly this position and was added to the roster for its first formal re-attestation.
- **Treating re-attestation as a full re-review, or a full re-review as re-attestation.** A behavioural change outside the clearance's stated scope needs a fresh §13 review (procedure step 2), not a "still fine" log line.

## §13.6 — SI-02 gate-history review trigger

If SI-02's gate goes from PASS to non-PASS twice within a rolling 6 months, a full §13 boundary review of SI-02 is triggered ahead of its §13.5 date.

**Inside the boundary**
- **One breach, then recalibration.** A single PASS→non-PASS crossing is the gate doing its job. A threshold fix goes through its own `BLG-SPEC-*` path (as `BLG-SPEC-72` and `BLG-SPEC-86` did) and does not trigger §13.6.
- **Two breaches inside 6 months, logged and reviewed.** For example, breaches dated 2027-01-10 and 2027-05-02. The trigger is recorded in `section13_reattestation_log.md` tagged `Trigger: SI-02 gate-history (§13.6)`, and a full review asks whether drift is still an occasional deviation.

**Outside the boundary**
- **Answering a second breach by loosening the threshold only.** Two breaches in 6 months is defined as a boundary signal. Retuning without the §13.6 review skips the question the clause exists to ask.
- **Applying §13.6 to another roster feature.** The trigger is specific to SI-02, the only roster feature with a recurring dated gate history. Extending it is a change to §13 itself, which needs the owner's sign-off.

## Strategy Rules & System Intent Owner Review

**Strategy Rules & System Intent Owner — 2026-11-02** (Sprint Execution Engine, agent-mediated in that role per `execution_prompt.md` §5.3; ST-52 AC 2). Each section was checked against the clause it cites:

| Clause | Finding |
|--------|---------|
| §13.1 | Both inside examples are deterministic and human-in-the-loop, and both are backed by dated rulings. The outside examples match the reason for v9.14 ST-03 to ST-05 and the "adaptive" exclusion. Agreed. |
| §13.2 | The journal and stop-note examples quote the v9.14 rulings accurately. "Auto-exit" and "AI rule-change suggestion" are clear execution and adaptive/AI cases. Agreed. |
| §13.3 | The earnings flag example states all four carve-out conditions (on request, ticker-specific, before the next session, recognised by §4.2.3) and the US-only scope. The weekend-hold removal and notification examples match the named exclusions, and the ex-dividend example correctly needs its own review. Agreed. |
| §13.4 | The examples keep the clearance's three limits: on request, no scheduling, no persistence. Agreed. |
| §13.5 | The examples follow the Maintenance rule and procedure step 2. Agreed. |
| §13.6 | The dates are illustrative only, and the example says so. The examples separate threshold fixes from the boundary review, as the clause's rationale does. Agreed. |

Outcome: **Approved.** No `strategy_rules.md` change is needed. This document is explanatory, and §13 governs where they differ.
