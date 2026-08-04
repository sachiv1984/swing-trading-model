# Git Hooks

**commit-msg** — lints the commit message format on `exec/**` branches per `CLAUDE.md`'s non-negotiable commit format (`[EPIC-xx][ST-xx] <description>` / `[EPIC-xx][ST-xx][ST-yy] <description>` / `[GOVERNANCE] <description>`). No-op on `main` and any other branch.

## Installation

Automatic on `npm install` (via the `prepare` script in `package.json`, which runs `git config core.hooksPath scripts/git-hooks`). To install manually:

```
git config core.hooksPath scripts/git-hooks
```

## Testing

```
bash scripts/git-hooks/test_commit_msg.sh
```
