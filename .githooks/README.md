# Git Hooks

Two hooks, both wired via a single `core.hooksPath .githooks` setting (git dispatches by filename, so multiple hook types coexist here without conflict).

## `pre-commit` (EPIC-02/ST-05, EPIC-10/ST-10)

- Blocks a commit that adds a new backend route (`@router.*` decorator) without a matching `backend/routers/test.py` registration (`scripts/check_router_test_registration.py`).
- Runs a local gitleaks secrets scan of staged changes (degrades to a warning, not a block, if gitleaks isn't installed locally — the CI-level gate still catches a leaked secret on push).

## `commit-msg` (ST-21, EPIC-04, v8.2)

- Lints the commit message format on `exec/**` branches per `CLAUDE.md`'s non-negotiable commit format (`[EPIC-xx][ST-xx] <description>` / `[EPIC-xx][ST-xx][ST-yy] <description>` / `[GOVERNANCE] <description>`). No-op on `main` and any other branch.

## Secrets-scanning false-positive override procedure (ST-12, BLG-SEC-36, EPIC-03, v9.4)

Both the local `pre-commit` hook and the CI-level gate (`.github/workflows/secret-scanning.yml`) run gitleaks against the same `.gitleaks.toml`. Confirmed to actually block a deliberately-planted test secret: `tests/test_secrets_scanning_hook.py::test_hook_blocks_a_planted_secret` (skipped when `gitleaks` isn't on `PATH` — install it locally to run this check; CI always has it via `gitleaks/gitleaks-action@v2`).

When gitleaks flags a match that is **not** a real secret (a false positive — e.g. a high-entropy string that is actually a UI storage-key constant, a documented synthetic test fixture, or similar), do not delete or reword the flagged content just to dodge the scanner. Instead:

1. **Confirm it is genuinely not a secret.** If there is any doubt, treat it as real and rotate/remove it — do not allowlist first and ask later.
2. **Add a scoped allowlist entry to `.gitleaks.toml`**, using one of gitleaks v8.21's two schema-valid forms only:
   - `[[rules.allowlists]]` nested under a specific `[[rules]]` block — scopes the suppression to one named rule ID (e.g. `generic-api-key`). Preferred — narrowest blast radius.
   - A single global `[allowlist]` table (singular, not an array) — applies regardless of which rule fires. Use only when the false positive isn't tied to one rule.
   - **Do not** use a bare top-level `[[allowlists]]` (plural, unnested) — gitleaks v8.21 silently ignores this form (see the fix comment at the top of `.gitleaks.toml`, `BLG-SEC-26`); an allowlist written this way looks like it works but does nothing, and the finding stays live in CI.
3. **Scope the entry as tightly as possible**: set `paths` to the exact file(s) the false positive occurs in, and `regexes` to the exact matched string (`regexTarget = "match"`) rather than allowlisting a whole rule ID or an entire directory.
4. **Document the rationale inline** in the entry's `description` field — what the string actually is and why it isn't a secret (see the existing entries in `.gitleaks.toml` for the expected level of detail).
5. **Verify locally before committing**: `gitleaks detect --source . --config .gitleaks.toml --no-git` and confirm the finding is now clean and no previously-suppressed real finding has reappeared.
6. **Get Cybersecurity & Trust Lead sign-off** on the `.gitleaks.toml` change (this role owns the file per its header) before merging.

## Installation

Automatic on `npm install` (via the `prepare` script in `package.json`, which runs `git config core.hooksPath .githooks`). To install manually:

```
git config core.hooksPath .githooks
```

## Testing

```
bash .githooks/test_commit_msg.sh
```
