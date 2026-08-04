# Git Hooks

Two hooks, both wired via a single `core.hooksPath .githooks` setting (git dispatches by filename, so multiple hook types coexist here without conflict).

## `pre-commit` (EPIC-02/ST-05, EPIC-10/ST-10)

- Blocks a commit that adds a new backend route (`@router.*` decorator) without a matching `backend/routers/test.py` registration (`scripts/check_router_test_registration.py`).
- Runs a local gitleaks secrets scan of staged changes (degrades to a warning, not a block, if gitleaks isn't installed locally — the CI-level gate still catches a leaked secret on push).

## `commit-msg` (ST-21, EPIC-04, v8.2)

- Lints the commit message format on `exec/**` branches per `CLAUDE.md`'s non-negotiable commit format (`[EPIC-xx][ST-xx] <description>` / `[EPIC-xx][ST-xx][ST-yy] <description>` / `[GOVERNANCE] <description>`). No-op on `main` and any other branch.

## Installation

Automatic on `npm install` (via the `prepare` script in `package.json`, which runs `git config core.hooksPath .githooks`). To install manually:

```
git config core.hooksPath .githooks
```

## Testing

```
bash .githooks/test_commit_msg.sh
```
