# Agent Role Charters

This directory holds the canonical charter for every named authority role in the governance system (per `claude/charter/team_charter.md` §4: "Role charters in `claude/agents/` — individual role responsibilities and operating standards"). Each charter is the source of truth for that role's scope, responsibilities, and boundaries — referenced throughout `claude/system/*.md`'s governance prompts (e.g. as the required-by authority in a sign-off block, or the target of a `delegated_backend`/`delegated_frontend`/`delegated_decision` item per `execution_prompt.md` §5.1).

## Adding a New Role Charter

Start from `_role_charter_template.md` (ST-26, BLG-GOV-183, EPIC-05, v9.3) — it annotates every section common across the existing charters in this directory, with guidance notes on which sections are universal versus role-dependent. Copy it to `<role_name_lowercase_with_underscores>.md`, fill in every section, delete the template's guidance comments and placeholders, and register the new role in `claude/charter/team_charter.md` §4's roster (linking to the new charter file) — the template itself does not register the role; that roster is the canonical list of who exists.

## Current Roles

23 charters as of 2026-09-10 (this file is not auto-generated — if this count or the roster drifts from `team_charter.md` §4's own list, that roster is authoritative; update this count when adding/removing a charter, but do not duplicate the full roster here).
