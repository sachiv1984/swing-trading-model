# README.md

## Purpose
This documentation set defines the **front‑end user experience and interface specifications** for the Position Manager Web App. Its goal is to clearly describe **what users see and how they interact with the product**, while keeping technical implementation details secondary.

The specs are intentionally structured to support:
- Clear UX intent and behavior
- Consistent design decisions across the app
- Parallel work between design, front‑end engineering, and QA

---

## Intended Audience

- **Designers (primary audience)**
  Use these documents to understand page goals, layout, states, interactions, and accessibility expectations.

- **Front‑end Engineers (secondary audience)**
  Use these documents to align implementation with UX intent, shared patterns, and component responsibilities.

- **QA / Testers**
  Use page states, validation rules, and error handling patterns to derive test scenarios.

---

## How the Documentation Is Structured

The specs are split by **concern and scope** to reduce cognitive load and make information easy to find:

- **Design System**
  Foundational visual and interaction rules shared across the application.

- **Pages**
  User‑facing screens, documented by purpose, layout, states, and user understanding.

- **Components**
  Reusable UI building blocks used across multiple pages.

- **Patterns**
  Cross‑cutting UX behaviors (e.g., validation, error handling, API dependencies) that should remain consistent everywhere.

Each file is focused, readable in isolation, and avoids unnecessary implementation detail unless required for clarity.

---

## Navigation

### Design System
- ./design_system.md

### Pages
- ./pages/dashboard.md
- ./pages/positions.md
- ./pages/trade_history.md
- ./pages/analytics.md
- ./pages/settings.md
- ./pages/system_status.md

### Components
- ./components/position_form.md
- ./components/exit_modal.md
- ./components/cash_management_modal.md
- ./components/journal_components.md
- ./components/position_detail_modal.md

### UX Patterns
- ./patterns/error_handling.md
- ./patterns/api_dependencies.md

---

## How to Use These Specs

- Start with the **page spec** to understand user goals and layout.
- Refer to **components** for detailed interaction and state behavior.
- Apply **patterns** to ensure consistent UX across the application.
- Use the **design system** as the source of truth for visual and interaction standards.
- Consult **api_dependencies.md** to understand which surfaces depend on which endpoints — essential for assessing change impact and validating states.

Together, these documents form a modular, designer‑friendly front‑end specification that separates **UI intent from technical detail** while remaining precise enough to implement and test confidently.
