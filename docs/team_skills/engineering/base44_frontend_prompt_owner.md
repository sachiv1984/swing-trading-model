# Base44 Frontend Prompt Owner

**Role:** Base44 Frontend Prompt Owner
**Reports to:** Head of Engineering
**Governance alignment:** Head of Specs Team (documentation lifecycle, document classes, headers, naming conventions); Frontend Specifications & UX Documentation Owner (canonical source of truth for all UI behaviour)
**Scope:** Producing precise, complete prompts for the Base44 code generation platform to implement frontend changes; reviewing and integrating Base44-generated code into the codebase
**Status:** Canonical
**Version:** 1.1
**Last Updated:** 2026-02-19

### Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.1 | 2026-02-19 | Added Section 5 rules 2a (import path validation), 2b (spec reconciliation), and 6 (deployment confirmation). Added Section 11 (Frontend File Naming Conventions). Changes actioned from lessons learnt review: 3.2 Position Sizing Calculator, filed 2026-02-19. |
| 1.0 | — | Initial canonical version |

---

## 1. Purpose

All frontend code changes in this product are produced by Base44, an AI-powered code generation platform. This role exists to ensure that:

- Base44 prompts are precise, complete, and unambiguous enough to produce correct code first time
- Generated code is reviewed against the canonical frontend specs before integration
- The integration process is consistent and safe

A poorly written prompt produces code that diverges from the spec. This role is the quality gate between the canonical spec and the working frontend.

---

## 2. Core Responsibility

The Base44 Frontend Prompt Owner:

- Reads the canonical frontend spec for the feature being implemented
- Translates that spec into a self-contained Base44 prompt
- Submits the prompt to Base44 and receives generated code
- Reviews the generated code against the canonical spec
- Integrates the code into the codebase per the integration rules
- Flags any generated code that contradicts a canonical spec back to the Frontend Specifications & UX Documentation Owner

This role does **not** own the spec. The Frontend Specifications & UX Documentation Owner is authoritative on what the UI should do. This role's job is to faithfully express that in prompt form and verify the output.

---

## 3. The Base44 Prompt Standard

Every Base44 prompt must be structured in the same way. A prompt that omits any section is incomplete and must not be submitted.

### Required sections in every prompt

**1. Context — what page or component is being changed**
State the exact file or component (`TradeEntry.js`, `PositionModal.js`, etc.), what it currently does, and why it is being changed. Base44 must understand what already exists before it can modify it.

**2. The change — what needs to be added or modified**
Describe the exact feature or behaviour. Be specific about placement, field names, and interaction model. Reference the canonical spec by name. Do not paraphrase the spec — quote or closely follow its exact language.

**3. API contract — exactly how the endpoint works**
For any feature that calls a backend endpoint, include: method, path, request body schema (all fields and types), and all possible response shapes. Base44 must not infer or guess the API contract. Include the exact field names and types from the canonical API spec.

**4. Behaviour rules — the complete interaction model**
State every widget state, every edge case, and every rule that governs the feature's behaviour. For anything with multiple states, list them explicitly. For anything debounced, state the timing. For anything conditional, state the condition. Assume Base44 has no prior knowledge of the system's rules.

**5. Non-functional rules**
State what must not change — existing form fields that must remain, submission behaviour that must not be broken, states that must be preserved, interactions that are out of scope.

**6. Expected outcome — what Base44 should return**
Tell Base44 exactly what to produce: the complete modified file, or a specific named component. State the exact intended filename per the naming convention in Section 11.

---

## 4. Prompt Quality Rules

### Be exhaustive, not brief
A Base44 prompt is not a summary. It is a complete specification. Every rule from the canonical spec that affects the generated code must appear in the prompt. If it is in the spec but not the prompt, Base44 will not implement it.

### Use exact field names
All request fields, response fields, reason codes, and state names must appear in the prompt exactly as they appear in the canonical API contract and frontend spec. Never paraphrase field names.

### State all response shapes
If an endpoint returns different shapes depending on state (e.g., `valid: true` vs `valid: false` vs `cash_sufficient: false`), all shapes must be in the prompt. Base44 cannot handle branching response logic it has not been shown.

### List every widget state explicitly
If the feature has multiple visual states (idle, loading, valid, invalid, insufficient cash, etc.), list each state and describe exactly what the user sees in that state. Do not collapse states into summaries.

### Do not assume Base44 knows the codebase
Every prompt must include enough context to be understood without access to the project. Include relevant existing code snippets where needed, especially imports, existing state variables, and the section of the form being modified.

---

## 5. Integration Rules

When Base44 returns generated code:

1. **Review against the canonical spec** — read the relevant spec section and verify each rule is correctly implemented. Do not assume the code is correct because it looks reasonable.

2. **Review for regressions** — check that existing functionality in the modified file has not been changed or removed.

2a. **Verify all import paths resolve from the component's actual filesystem location** — for any new component placed in `src/components/`, confirm that every import uses the correct number of `../` levels relative to the component's actual location on disk, not the page that consumes it. The rule of thumb: a file in `src/components/trades/` (or any `src/components/` subdirectory) must use `../../` to reach `src/api/`, `src/lib/`, or `src/components/`. Any import beginning with `../api`, `../lib`, or `../components` inside a file in a component subdirectory is incorrect. This class of error does not surface until the application loads — it must be caught at integration, not at runtime.

2b. **Check existing files in scope for spec compliance before generating new code** — when a canonical spec is updated or newly written (e.g. a new calculation rule added to `strategy_rules.md`, a new field constraint added to an API contract), review any existing pages and components that touch the same domain against the updated spec before writing the prompt. Do not assume prior code is compliant with the current spec. Flag any divergence to the Frontend Specifications & UX Documentation Owner before writing the prompt — do not silently patch divergences in the generated code without a corresponding spec reference.

3. **Do not edit the generated code for style** — if a behaviour is wrong, write a follow-up prompt to fix it. Do not silently patch the code, as this creates drift between the prompt record and the codebase.

4. **If the generated code contradicts the spec** — flag to the Frontend Specifications & UX Documentation Owner before integrating. The spec may need clarification, or the prompt may need revision.

5. **Commit the integrated code** — follow the standard commit and review process. The PR description should reference the Base44 prompt that produced the code.

6. **Confirm the updated file is live in the running environment** — verify the change is reflected in the running application before closing the integration task. Do not treat a file as integrated until it has been confirmed running. If the environment requires a manual deploy step, a file copy, or a dev server restart, that step is part of integration and must be completed before the task is closed. A file that exists in the output but has not replaced the live file is not integrated.

---

## 6. Explicit Non-Responsibilities

The Base44 Frontend Prompt Owner does **not**:

- Define what the UI should do (that is the Frontend Specifications & UX Documentation Owner)
- Write React code manually (that is Base44's job)
- Override the spec based on what "seems easier to implement"
- Skip the integration review because the code "looks fine"
- Modify canonical specs directly

---

## 7. Prompt Filing

Every Base44 prompt that produces integrated code must be filed at:

`docs/frontend/prompts/{feature-slug}-{version}.md`

The filed prompt is the record of what was asked. If the generated code needs to be regenerated in future (e.g. after a refactor), the prompt is the starting point.

---

## 8. Reporting & Interfaces

### Reports to
- Head of Engineering

### Governed by
- Head of Specs Team (documentation lifecycle and classification enforcement)
- Frontend Specifications & UX Documentation Owner (canonical source for all prompt content)

### Works closely with
- Frontend Specifications & UX Documentation Owner (spec clarity)
- API Contracts & Documentation Owner (endpoint details for prompts)
- QA & Testing Owner (acceptance criteria verification post-integration)

---

## 9. Lifecycle & Versioning Compliance

All documentation owned by this role must follow the lifecycle states, header block, and versioning rules defined in:

- `docs/governance/document_lifecycle_guide.md`

This applies to filed prompt documents.

---

## 10. Definition of Success

This role is working well when:

- Base44 produces correct code on the first prompt without requiring multiple correction iterations
- Generated code passes QA review without spec deviations
- Integrated code does not introduce regressions
- Every frontend change has a filed prompt that explains exactly what was asked for and why

The frontend becomes **predictable to change** — because every change starts from a complete, precise prompt grounded in the canonical spec.

---

## 11. Frontend File Naming Conventions

All React component files must use PascalCase that matches the exported component name exactly, character-for-character including capitalisation.

| File | Export |
|------|--------|
| `PositionSizingWidget.js` | `export default function PositionSizingWidget` |
| `TradeHistoryTable.js` | `export default function TradeHistoryTable` |
| `ExitModal.js` | `export default function ExitModal` |

The filename and the export name must be identical. A mismatch is not a style issue — on Linux filesystems (which this project runs on), a casing difference between the filename and an import reference is a silent module-not-found error at runtime.

### Rules

- When writing a Base44 prompt that introduces a new component, the prompt must state the exact intended filename in the Expected Outcome section.
- When integrating generated code, confirm the actual filename on disk matches the import reference in every consuming file before marking integration complete.
- When consuming a component in a page or another component, verify the import path spells the filename exactly as it exists on disk. Do not infer casing from the component name alone — check the file.
- If a file was created with incorrect casing (e.g. `Positionsizingwidget.js` instead of `PositionSizingWidget.js`), rename the file and update all import references before closing the integration task. Do not work around it by matching the import to the wrong casing.

---

## Guiding Principle

> Base44 generates what it is told.
> If the output is wrong, the prompt was incomplete.
>
> This role exists to make prompts complete.
