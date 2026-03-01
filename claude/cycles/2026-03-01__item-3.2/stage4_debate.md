# Stage 4 — Structured Debate

**Cycle:** 2026-03-01__item-3.2
**Date:** 2026-03-01
**Authorities:** Product Owner (chair), Challenger (non-decision)

---

## Pre-Debate Re-Anchoring

Top 2 constraints most likely to block an easy yes:

1. **§13 system boundaries** — the system is not a configurable strategy builder, not ML-based, not automated. Any item touching these boundaries requires a formal strategy rules revision.
2. **No addition without displacement** — every Add requires a named Stop; stops ≥ adds is absolute.

---

## Candidate A — 4.1a: CSV Export of Trade History

### 5.0 Required Case (Product Owner)
1. **Problem:** None — solved. BLG-FEAT-07 shipped this feature in v1.6.1.
2. **Strategy/roadmap advancement:** N/A — superseded.
3. **What happens if we don't do it:** Nothing. Already delivered.
4. **What stops to fund it:** N/A.

**Product Owner position:** Kill.

### 5.1 Challenger Counter-Argument
- **Challenger position:** Reject
- **Evidence:** `strategy_rules.md` §14 (canonical truth overrides planning documents); `document_lifecycle_guide.md` §8 (feature shipped → planning documents updated to Superseded)
- **Reason:** An active planning item with no remaining work is a documentation integrity failure. Keeping it active creates false planning debt and clutters the roadmap, violating the lifecycle requirement that planning documents reflect real decisions.
- **Consequence:** Future runs will continue evaluating a ghost item, consuming governance attention and obscuring true roadmap state.

### 5.2 Product Owner Response
Accept — Reject/Kill. Challenger's argument is correct and consistent with the stated position.

### Outcome: ❌ Kill — superseded by BLG-FEAT-07 (shipped v1.6.1, 2026-03-01)

---

## Candidate B — 4.3: Signal Exposure Enhancement

### 5.0 Required Case (Product Owner)
1. **Problem:** Users cannot adjust `top_n` or `lookback_days` signal parameters. Both are hardcoded in the backend, limiting personalisation of signal output.
2. **Strategy/roadmap advancement:** Advances signal utility for daily trading decisions. Narrow-scope frontend task once spec gate is cleared. Backend already supports both parameters.
3. **What happens if we don't do it:** Users cannot tune signal output. Low urgency but real daily friction.
4. **What stops to fund it:** None — item is gated. It cannot enter pre-alignment until §13 review confirms parameters are formally user-configurable. No resource allocation triggered by retaining on gated list.

### 5.1 Challenger Counter-Argument
- **Challenger position:** Park
- **Evidence:** `strategy_rules.md` §13.2 ("not a multi-strategy or configurable strategy platform") and §13.3 ("strategy builder... would change the nature of the system")
- **Reason:** Exposing configurable parameters risks ongoing boundary policing and scope creep into configurable strategy territory. The item should not appear as an active roadmap item until the §13 gate is explicitly cleared — parking removes ambiguity about whether it can be quietly progressed.
- **Consequence:** If retained as "gated" without active gate resolution, the item creates ambiguity about whether the §13 review is a real blocker or a soft note.

### 5.2 Product Owner Response
Rebut — Maintain in gated list. The item is already classified as "Planned — gated" with an explicit pre-condition. The §13 boundary review is a v1.7 item with named owners (Strategy Rules owner + Product Owner). The gate is real, enforced, and visible. Parking it loses the visibility of the gate dependency. The scope boundary note in the roadmap item (no parameters beyond `top_n` and `lookback_days`) addresses the Challenger's scope creep concern. Item remains gated with explicit pre-condition confirmed.

### Outcome: ✅ Advance — confirmed as gated (no displacement required; not consuming resources until gate clears)

---

## Candidate C — 3.5: Alerts & Notifications

### 5.0 Required Case (Product Owner)
1. **Problem:** No proactive notification of critical trading events (stop approaching, grace period ending, regime change). Users must actively check the system — easy to miss time-sensitive signals.
2. **Strategy/roadmap advancement:** Directly advances the human-in-the-loop model by ensuring decision support reaches the user at the right moment. Serves `strategy_rules.md` §2 intent (defend profits, enforce asymmetric risk) by enabling timely awareness.
3. **What happens if we don't do it:** Users miss warnings. Decision-support value degrades in proportion to check frequency.
4. **What stops to fund it:** Item occupies existing v2.0 slot. Re-evaluation, not new addition. No new stop required.

### 5.1 Challenger Counter-Argument
- **Challenger position:** Park (defer beyond v2.0)
- **Evidence:** `strategy_rules.md` §3 (human-in-the-loop, system is decision support only, does not execute trades) and §13.1 ("deterministic decision-support engine... human-in-the-loop by design")
- **Reason:** Alerts introduces async processing, email/SMS delivery, and notification preference management — a significantly more complex infrastructure layer than anything shipped to date. QA planning session has not occurred; the testing surface for notification delivery is materially larger than the ~4–5 day estimate. Pre-requisites (observability standards, API versioning) remain incomplete. Advancing to v2.0 without all pre-requisites resolved and without QA planning risks an under-resourced delivery with silent async failure modes.
- **Consequence:** If v2.0 pre-alignment opens before observability standards are in place, async failures will be unobservable. Without QA planning, notification delivery may ship untested at realistic scale.

### 5.2 Product Owner Response
Modify — retain in v2.0 but elevate pre-conditions to explicit hard gates. The Challenger's concern is valid. The three pre-conditions (observability standards complete, API versioning decision record complete, QA planning session complete) are already stated in the roadmap but as notes, not hard gates. Elevating them to hard gates addresses the Challenger's concern: v2.0 pre-alignment may not open until all three are confirmed. Displacement: item occupies existing v2.0 slot — no new displacement required.

### Outcome: ✅ Advance — retain in v2.0 with pre-conditions elevated to explicit hard gates

---

## Summary

| Candidate | Outcome | Decision owner |
|-----------|---------|----------------|
| 4.1a CSV Export | ❌ Kill (superseded) | Product Owner |
| 4.3 Signal Exposure | ✅ Advance (gated) | Product Owner |
| 3.5 Alerts & Notifications | ✅ Advance (hard gates confirmed) | Product Owner |
