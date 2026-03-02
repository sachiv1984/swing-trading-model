# CLAUDE.md — System Anchor

## 1. Governance Engines
- **Release Planning:** `claude/system/release_planning_prompt.md`
- **Roadmap Rebalance:** `claude/system/roadmap_prompt.md`
- **Lifecycle Rules:** `claude/charter/document_lifecycle_guide.md`

## 2. Command Aliases (Delegated Authority)
- `run planning v<version>`: Execute the Release Planning Engine for the specified version.
- `run roadmap --item-id <id>`: Execute the Roadmap Rebalance Engine for a completed item.
- `sync gh`: Parse the active `stage4_backlog_slice.md` and create/update GitHub Issues.

## 3. Operational Protocols
- **State Check:** Always refer to `.claude_current_state.json` for the `active_cycle`.
- **Naming:** All branches must follow `exec/<cycle_id>/<epic_id>`.
- **Commit Standards:** Every commit must include the `[EPIC-xx][ST-xx]` prefix.
- **Write Scope:** Respect Section 5 (Write Scope Restriction) of the invoked engine.
