**Owner:** Head of Engineering
**Class:** Canonical Specification (Class 1)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-23 (ST-25, EPIC-06, v9.6, BLG-SPEC-145 — created, seeded with 2 entries)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Backend Decision Log

A lightweight, append-only log of cross-cutting backend decisions that are too small to warrant a stand-alone ADR document (see `docs/adr/ADR-*.md` for full-form records, indexed in `docs/specs/api_contracts/backend_engineering_patterns.md` §Architectural Decision Index) but are still worth recording — a decision another engineer would otherwise have to re-derive from reading code and git history.

**When to use this log vs. a full ADR:** a full `ADR-NNN-<slug>.md` document is for a decision with real considered alternatives, cross-feature blast radius, and a formal Head of Engineering sign-off (see ADR-003 for the shape). This log is for a smaller decision — a pattern choice, a convention, a "why we did it this way not that way" — that is still cross-cutting (affects more than one feature/router/file) but doesn't need that much ceremony. If in doubt, and the decision is genuinely single-feature, it likely belongs in that feature's own spec instead of here.

**How to add an entry:** append a new `## LOG-NNN` block at the bottom using the template below. This file is append-only — do not edit or renumber a prior entry; if a decision is later reversed, add a new entry that supersedes it and update the superseded entry's `**Status:**` field to `Superseded by LOG-NNN` (the entry's own body stays as the historical record).

---

## Template

```
## LOG-NNN — <Short decision title>

**Date:** YYYY-MM-DD
**Decider:** <role>
**Source:** <BLG-xx / ST-xx / commit, if applicable>
**Status:** Active | Superseded by LOG-NNN

**Context:** What problem or question prompted this decision — 2-4 sentences.

**Decision:** The decision itself, stated plainly.

**Consequence:** What this means for future implementers — what to do, and what not to do, as a result.
```

---

## LOG-001 — Test database stub list is AST-derived, not hand-maintained

**Date:** 2026-07-04
**Decider:** Head of Engineering
**Source:** `BLG-QA-73` (resolved v6.6)
**Status:** Active

**Context:** `tests/conftest.py` stubs out database access for the test session via a hardcoded `_DB_STUB_FUNCTIONS` list. Every new `from database import (...)` statement added to any `backend/` module required a matching manual edit to that list — an easy step to forget, and a recurring source of "tests pass locally, fail in CI because a new DB function wasn't stubbed" friction.

**Decision:** `_DB_STUB_FUNCTIONS` is derived automatically at conftest load time via an AST scan of `backend/` for `from database import (...)` statements (vendored/virtualenv paths excluded from the scan), rather than maintained as a literal list in source.

**Consequence:** Adding a new `database` import to any backend module — not just `position_service.py`, the file this was originally scoped to — requires no `conftest.py` edit. Do not re-introduce a hardcoded stub list for a new subsystem "to be explicit" — extend the AST scan's search path instead if a new directory of backend modules needs covering. See `CLAUDE.md §2` for the standing retirement note.

---

## LOG-002 — Cross-router calls use a lazy import inside the calling function, never a module-level import

**Date:** 2026-09-09
**Decider:** Backend Engineering Patterns Owner
**Source:** `docs/specs/api_contracts/backend_engineering_patterns.md` §Lazy imports for cross-router hooks
**Status:** Active

**Context:** FastAPI routers are registered sequentially in `main.py`. A module-level `from backend.routers.b import fn` inside router `a.py`, where `a` is registered before `b`, fails at import time because `b` has not finished initialising yet — this bit `screener.py` needing to trigger cache invalidation in `research.py`, and would bite any future router-to-router call built the same way.

**Decision:** Any router function that needs to call a function defined in a different router does so via a lazy import placed inside the calling function body, not a module-level import at the top of the file. This applies to shared utility functions that themselves need to call into a specific router's function, too.

**Consequence:** Do not "clean up" a lazy cross-router import by hoisting it to the top of the file — that re-introduces the registration-order failure mode, and it will not necessarily reproduce locally if the two routers happen to be registered in a working order today (a later reordering of `main.py`'s router registration can reintroduce the bug with no change to the router file itself). Full pattern detail and a worked example: `backend_engineering_patterns.md` §Lazy imports for cross-router hooks.

---
