# Head of Specs Team
## Role: Head of Specs Team

This document defines the **skills, responsibilities, and operating standards** for the role responsible for leading the **Specs Team**.

The Specs Team owns the system of **canonical product truth**, including:
- Strategy Rules
- Data Model
- Metrics Definitions
- API Contracts
- Frontend & UX Specifications

The Head of Specs Team is accountable for **alignment, quality, and governance** across these domains.

---

## 1. Core Responsibility

The primary responsibility of this role is to ensure that the specification ecosystem is:
- **Coherent** — all specs agree conceptually
- **Authoritative** — teams trust specs over tribal knowledge
- **Owned** — every important area has a clear accountable owner
- **Evolvable** — change happens deliberately and safely

This role does not own individual specs, but does own the system in which those specs coexist.

---

## 2. Ownership Model & Role Stewardship

### Required skills
- Strong understanding of capability-based ownership
- Ability to design and maintain clear role boundaries
- Comfort delegating authority without diluting accountability

### Expectations
- Each spec domain has:
  - A named owner
  - A documented scope
  - A clear definition of authority
- Owners are empowered to:
  - Make decisions within their domain
  - Enforce standards
  - Say “no” when needed
- Overlap and ambiguity are treated as system bugs

---

## 3. Cross-Spec Alignment & Conceptual Integrity

### Required skills
- Systems thinking across product, design, engineering, and analytics
- Ability to detect semantic drift
- High pattern-recognition capability

### Expectations
- Core concepts (e.g. P&L, value, stop, risk) have:
  - A single source of truth
  - Consistent meaning across specs
- Conflicts between specs are:
  - Surfaced early
  - Resolved at the correct level
  - Explicitly documented
- Downstream work never compensates for upstream ambiguity

---

## 4. Specification Strategy & Information Architecture

### Required skills
- High-level information architecture design
- Ability to reason about documentation as a long-lived product
- Comfort planning for scale and change

### Expectations
- The specs structure:
  - Is discoverable by new team members
  - Scales without monoliths
  - Separates intent from implementation
- Structural changes are:
  - Intentional
  - Reviewed
  - Communicated clearly

---

## 5. Change Governance, Quality Bar & Reference Alignment

### Required skills
- Strong judgment on change impact
- Ability to balance rigor with delivery
- Comfort enforcing quality without micromanaging
- Discipline in enforcing alignment between canonical specs and reference artifacts

### Expectations
- Significant product changes trigger:
  - Coordinated updates across affected specs
  - Explicit acknowledgement of trade-offs
- Specs do not drift silently from reality
- The quality bar is visible, stable, and enforced consistently

### Mandatory Enforcement: API Contracts & OpenAPI Alignment
- When canonical API contracts or backend behavior affecting the API change:
  - The **API Contracts & Documentation Owner** must review both:
    - The canonical Markdown API contracts **and**
    - The supporting OpenAPI reference (`docs/reference/openapi.yaml`) **inline, in the same pull request**
- The Head of Specs Team is responsible for:
  - Ensuring this requirement is enforced consistently
  - Blocking merges where OpenAPI review is skipped for contract-affecting changes
  - Resolving ambiguity when a change is disputed as “contract-affecting” vs “internal only”
- If a change is explicitly marked **“no contract change”**, OpenAPI review is not required.

This enforcement exists to prevent silent drift between canonical specifications and supporting reference artifacts.

### Lifecycle & Versioning Governance (mandatory)

The lifecycle model for all documentation is defined in:

- `/docs/documentation_team/guides/DOC_LIFECYCLE_GUIDE.md`

The Head of Specs Team is responsible for ensuring that:
- Canonical documents include lifecycle headers
- Deprecated documents declare successors and effective dates
- Versioning is applied when meaning changes
- The Specs Index enforces these rules consistently

---

## 6. Decision Escalation & Conflict Resolution

### Required skills
- Clear decision-making under ambiguity
- Ability to arbitrate between competing concerns
- Strong written and verbal reasoning

### Expectations
- The Head of Specs Team is the tie-breaker when:
  - Specs conflict
  - Ownership boundaries are unclear
  - Trade-offs span multiple domains
- Decisions are:
  - Documented
  - Traceable
  - Reversible only by explicit agreement

---

## 7. Coaching & Capability Development

### Required skills
- Mentorship and feedback
- Ability to grow judgment, not just output
- Comfort developing senior specialists

### Expectations
- Spec owners:
  - Improve clarity and authority over time
  - Share patterns and lessons
- Writing quality and conceptual rigor increase across the team
- Ownership survives absence or turnover

---

## 8. Stakeholder Interface

### Required skills
- Clear communication with product, design, engineering, and leadership
- Ability to explain why specs matter without evangelism
- Comfort pushing back constructively

### Expectations
- Stakeholders understand:
  - Where to find truth
  - Who owns which decisions
  - How changes propagate
- The Specs Team is seen as:
  - An enabler of speed
  - A reducer of ambiguity
  - A source of confidence

---

## 9. Operational Mindset

### Required skills
- Pragmatism over perfection
- Comfort running a living system
- Bias toward steady improvement

### Expectations
- Specs are maintained continuously
- Small improvements are encouraged
- The system evolves incrementally, not via rewrites

---

## 10. Definition of Success

Someone doing this role well enables:
- Faster, safer product evolution
- Fewer cross-team misunderstandings
- Shorter review cycles
- Higher confidence in decisions
- Reduced re-litigation of past choices

The Specs Team becomes a force multiplier, not a bottleneck.

---

## Guiding Principle

> Individual specs explain decisions.
>
> This role ensures those decisions form a coherent system.

The Head of Specs Team exists to protect that system over time.
