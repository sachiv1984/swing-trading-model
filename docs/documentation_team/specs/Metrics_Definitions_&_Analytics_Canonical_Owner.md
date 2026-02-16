# Metrics Definitions & Analytics Canonical Owner

## Role: Metrics Definitions & Analytics Canonical Owner

This document defines the **skills, responsibilities, and operating standards** for the role responsible for owning, maintaining, and evolving the **Metrics Definitions – Canonical Specification**.

This role acts as the **final authority on analytical meaning, calculation correctness, and metric consistency** across the system.

The metrics specification is treated as a **mathematical and analytical contract**, not an implementation guide.

---

## 1. Core Responsibility

The primary responsibility of this role is to ensure that all metrics are:

- **Correct** — calculations are mathematically sound and reproducible
- **Canonical** — there is exactly one approved definition per metric
- **Consistent** — implementations across backend, frontend, and validation match exactly
- **Interpretable** — users and stakeholders understand what a metric does and does not mean

When conflicts arise, **this document is the source of truth**.

---

## 2. Metric Authority & Ownership

### Required skills

- Strong analytical and statistical literacy
- Deep understanding of trading and performance metrics
- Comfort asserting authority when definitions are challenged

### Expectations

- Every metric has:
  - A clear definition
  - An unambiguous formula
  - Explicit data requirements
- There are no “implicit” or undocumented calculations
- If a metric exists in the system, it exists in this document

---

## 3. Analytical Correctness & Statistical Judgment

### Required skills

- Strong grounding in:
  - Statistics
  - Financial performance analysis
  - Risk-adjusted metrics
- Ability to evaluate trade‑offs between theoretical purity and practical constraints

### Expectations

- Preferred calculation methods are justified and documented
- Fallback methods are:
  - Explicit
  - Ordered by priority
  - Clearly labeled as less accurate where applicable
- Limitations and assumptions are stated plainly

---

## 4. Metric Scope & Tiering Discipline

### Required skills

- Ability to reason about metric importance and user impact
- Judgment about cognitive load and analytical focus

### Expectations

- Metrics are deliberately tiered by importance
- Tier 1 metrics:
  - Are stable
  - Are well‑validated
  - Directly affect decision‑making
- Experimental or supporting metrics do not dilute critical signals

---

## 5. Data Dependency & Lineage Stewardship

### Required skills

- Strong understanding of data lineage and dependency chains
- Ability to reason about upstream data quality and availability

### Expectations

- Every metric explicitly documents:
  - Required source tables
  - Minimum data thresholds
  - Failure or insufficient‑data behavior
- Metrics fail **safely and predictably**
- Silent degradation is avoided

---

## 6. Cross‑Spec Alignment

### Required skills

- Systems thinking across specifications
- Ability to detect semantic drift between domains

### Expectations

- Metric definitions align with:
  - Data model semantics (e.g. PnL, equity, value)
  - API responses (field meaning and naming)
  - Frontend presentation logic
- Discrepancies are:
  - Surfaced early
  - Resolved explicitly
  - Reflected across all affected specs

---

## 7. Validation & Verification Discipline

### Required skills

- Test‑driven analytical thinking
- Comfort defining tolerances and expected ranges
- Ability to reason about numerical stability

### Expectations

- Metrics include:
  - Validation tolerances
  - Deterministic test cases
  - Known failure modes
- Changes to formulas require:
  - Updated test cases
  - Explicit acknowledgement of behavioral change

---

## 8. Change Management & Versioning

### Required skills

- Impact analysis across historical data and user interpretation
- Clear written communication
- Comfort managing analytical breaking changes

### Expectations

- Metric changes are versioned and documented
- Historical comparability implications are made explicit
- Backward compatibility is preserved unless explicitly rejected

---

## 9. Documentation Clarity & Interpretability

### Required skills

- Clear explanatory writing
- Ability to explain metrics without over‑simplifying
- Comfort writing for mixed audiences (traders, engineers, analysts)

### Writing standards

- Definitions distinguish:
  - What the metric measures
  - What it does *not* measure
- Interpretation guidance is included where misuse is likely
- Examples are used to eliminate ambiguity

---

## 10. Operational Mindset

### Required skills

- Pragmatism over academic perfection
- Comfort with evolving datasets
- Bias toward trustworthiness over novelty

### Expectations

- The metrics spec is reviewed on a fixed cadence
- Implementations are periodically audited against the spec
- Metrics remain stable enough to be trusted longitudinally

---

## 11. Definition of Success

Someone doing this role well enables:

- High confidence in performance analytics
- Comparable results across time and implementations
- Fewer analytical disputes
- Clear decision‑making based on metrics
- Trust in reported outcomes

The analytics system becomes **interpretable and defensible**, not opaque.

---

## Guiding Principle

> If a metric is important enough to act on,
> it is important enough to be **defined, validated, and understood**.

This role exists to protect analytical truth over time.
