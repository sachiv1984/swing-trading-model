# Strategy Rules & System Intent Owner
## Role: Strategy Rules & System Intent Owner

This document defines the **skills, responsibilities, and operating standards** for the role responsible for owning, maintaining, and evolving the **Strategy Rules** for the Momentum Trading Assistant.

This role acts as the **guardian of trading intent, rule determinism, and strategic coherence** across the system.

The strategy specification is treated as a **behavioral contract**, not a suggestion or implementation detail.

---

## 1. Core Responsibility

The primary responsibility of this role is to ensure that the trading strategy remains:
- **Deterministic** — rules behave the same way every time
- **Explicit** — no hidden or implied decision logic
- **Aligned** — backtests, live system, and documentation match
- **Intentional** — every rule exists for a clear strategic reason

This role owns **what the system is trying to do**, not how it is coded.

---

## 2. Strategy Intent & Rule Ownership

### Required skills
- Strong understanding of momentum‑based trading strategies
- Ability to reason about risk, drawdowns, and regime changes
- Comfort distinguishing intent from implementation

### Expectations
- Every rule answers:
  - What problem does this solve?
  - What risk does it control?
  - What trade‑off does it introduce?
- Strategy rules are:
  - Complete
  - Unambiguous
  - Free from implicit assumptions
- If behavior matters to outcomes, it is documented here

---

## 3. Determinism & Rule Integrity

### Required skills
- Ability to reason about state machines and rule sequencing
- High attention to edge cases and timing effects
- Comfort enforcing “frozen” behavior

### Expectations
- Rules do not depend on:
  - Hidden state
  - Manual interpretation
  - Unspecified timing
- Order of operations (e.g. grace period → trailing stop → exit) is explicit
- Rules do not conflict or override each other silently

---

## 4. Risk Management Stewardship

### Required skills
- Deep understanding of position‑level and portfolio‑level risk
- Ability to reason about downside protection vs opportunity cost

### Expectations
- Risk rules are:
  - Documented in plain language
  - Justified with strategic rationale
- Grace periods, stops, and overrides are intentional
- Stops never loosen unless explicitly redesigned and documented

---

## 5. Lifecycle & State Modeling

### Required skills
- Ability to reason about position lifecycle stages
- Comfort modeling states and transitions

### Expectations
- All position states are:
  - Explicitly named
  - Clearly defined
  - Mutually exclusive
- Transitions between states are deterministic
- UI, backend logic, and analytics interpret states consistently

---

## 6. Alignment with Other Specs

### Required skills
- Systems thinking across specifications
- Ability to detect intent drift between domains

### Expectations
- Strategy rules align with:
  - Data model semantics (e.g. stops, prices, P&L)
  - Metrics definitions (e.g. drawdown, Sharpe, R‑Multiple)
  - Frontend behavior (what the user sees and can do)
- Conflicts are resolved at the **strategy level**, not patched downstream

---

## 7. Change Management & Strategy Evolution

### Required skills
- Strong judgment about when to change vs hold
- Ability to analyze impact on historical results
- Clear written communication

### Expectations
- Strategy changes are:
  - Rare
  - Explicit
  - Versioned
- Changes document:
  - What changed
  - Why it changed
  - What historical comparability is affected
- Experimental ideas do not leak into canonical rules

### Lifecycle & Versioning Compliance (mandatory)
- All strategy documents must follow the lifecycle states, header block, and versioning rules defined in:
  - `docs/documentation_team/guides/DOC_LIFECYCLE_GUIDE.md`

---

## 8. Documentation Clarity & Authority

### Required skills
- Clear, authoritative writing
- Ability to explain strategy without marketing language
- Comfort stating boundaries

### Writing standards
- Rules are written as **statements**, not suggestions
- Ambiguous language is avoided (“generally”, “usually”)
- System boundaries are explicit (what the system is and is not)

---

## 9. Operational Mindset

### Required skills
- Discipline over novelty
- Comfort maintaining long‑lived rules
- Bias toward robustness over optimization

### Expectations
- The strategy doc is kept aligned with:
  - Backtests
  - Live behavior
  - Settings defaults
- Small clarifications are made proactively
- The strategy is trusted enough to explain performance outcomes

---

## 10. Definition of Success

Someone doing this role well enables:
- Predictable system behavior
- Explainable trading outcomes
- Consistent backtest‑to‑live performance
- Clear understanding of why trades were held or exited
- Reduced “why did this happen?” investigations

The strategy becomes a **stable decision framework**, not a black box.

---

## Guiding Principle

> If a rule can change outcomes,
> it must be **explicit, intentional, and owned**.

This role exists to protect strategic intent over time.
