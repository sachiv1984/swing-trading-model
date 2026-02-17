# API Contracts & Documentation Owner
## Role: API Contracts & Documentation Owner

This document describes the **skills, responsibilities, and operating standards** for the role responsible for owning, maintaining, and evolving the API contracts in `specs/api_contracts/`.

This role acts as the **guardian of API clarity, correctness, and reviewability** across teams.

---

## 1. Core Responsibility

The primary responsibility of this role is to ensure that API contracts remain:
- **Accurate** — always reflect actual backend behavior
- **Reviewable** — easy to scan, reason about, and approve incrementally
- **Stable** — changes are intentional, well-scoped, and communicated
- **Developer-friendly** — optimized for real client usage, not just backend implementation

The documentation is treated as a **first-class product artifact**, not an afterthought.

---

## 2. Domain Ownership & Structure

### Required skills
- Strong understanding of **domain-driven API design**
- Ability to group endpoints by **business capability**, not technical layers
- Discipline to prevent cross-domain leakage

### Expectations
- Each `*_endpoints.md` file:
  - Owns a single, clear domain
  - Has a consistent internal structure
  - Avoids duplication of conventions or rules defined elsewhere
- Cross-cutting rules live only in `conventions.md`
- High-level orientation and navigation live only in `README.md`

---

## 3. API Design & Contract Literacy

### Required skills
- Deep understanding of:
  - HTTP semantics (methods, status codes, idempotency)
  - REST-style resource modeling
  - Deterministic vs mutating operations
- Ability to translate backend behavior into clear contracts
- Comfort reasoning about edge cases, defaults, and validation rules

### Expectations
- Every endpoint definition clearly answers:
  - What does this do?
  - When is it safe to call repeatedly?
  - What inputs are required vs optional?
  - What happens when something goes wrong?
- No undocumented behavior is relied upon by clients

---

## 4. Change Management & Version Discipline

### Required skills
- Strong change impact analysis
- Ability to distinguish:
  - Clarification vs behavioral change
  - Non-breaking vs breaking change
- Clear written communication

### Expectations
- Any API change must result in:
  - An explicit documentation update
  - Clear indication of what changed and why
- Backward compatibility is preserved unless explicitly agreed otherwise
- Documentation makes it obvious:
  - What clients can rely on
  - What might change in the future


### Lifecycle & Versioning Compliance (mandatory)
All documentation owned by this role must follow the lifecycle states,
header block, and versioning rules defined in:
- `/docs/documentation_team/guides/DOC_LIFECYCLE_GUIDE.md`

---

## 5. Precision Writing & Technical Communication

### Required skills
- Clear, concise technical writing
- Ability to explain complex behavior without ambiguity
- Comfort writing for multiple audiences (frontend, backend, QA)

### Writing standards
- Prefer short sections and bullet points over long prose
- Use examples to remove ambiguity
- Avoid speculative language (“might”, “should usually”)
- Prefer deterministic phrasing (“always”, “never”, “must”)

---

## 6. Consistency & Review Hygiene

### Required skills
- High attention to detail
- Pattern recognition across endpoints
- Willingness to say “no” to inconsistency

### Expectations
- Field names, response shapes, and terminology are consistent across files
- Similar endpoints are documented in similar ways
- Inconsistencies are either:
  - Fixed, or
  - Explicitly documented (with rationale)

---

## 7. Frontend–Backend Contract Stewardship

### Required skills
- Empathy for frontend consumers
- Understanding of UI workflows and failure modes
- Ability to anticipate misuse or misinterpretation of APIs

### Expectations
- Documentation makes it difficult for clients to:
  - Accidentally calculate server-owned values
  - Misuse live prices vs execution prices
  - Misinterpret currency or FX behavior
- “Frontend responsibilities” are explicit where needed
- Contracts reduce back-and-forth clarification work

---

## 8. Operational Mindset

### Required skills
- Pragmatism over theoretical purity
- Comfort working with evolving systems
- Balance completeness with readability

### Expectations
- Documentation is kept continuously up to date
- Small improvements are made opportunistically
- Docs are trusted enough to be used in:
  - Code reviews
  - Onboarding
  - Incident investigation

---

## 9. Tooling & Workflow Expectations

### Familiarity with
- Markdown (GitHub-flavored)
- Pull-request-based review workflows
- Diff-friendly documentation practices
- Optional: OpenAPI/schema formats (as reference, not replacement)

### Working practices
- Documentation changes are reviewed like code
- Large changes are broken into reviewable chunks
- Files are kept intentionally small and focused

---

## 10. Definition of Success

Someone doing this role well enables:
- Faster frontend development
- Safer backend changes
- Shorter reviews
- Fewer misunderstandings
- Higher confidence in production behavior

The documentation becomes a **shared source of truth**, not a liability.

---

## Guiding Principle

> If an API behavior is important enough to rely on,
> it is important enough to be **clearly documented**.

This role exists to enforce that principle over time.
