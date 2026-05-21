**Owner:** PMO Lead
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-05-21

---

# Shared Preflight Common Checks

Callable subroutine invoked from STEP -1 preflight blocks across execution-phase engines. Implements the three universally required hard gates: required files present, required authority roles, and write permission.

## Parameters (caller must supply)

- `{required_files[]}`: list of file paths that must exist before the engine may proceed
- `{required_roles[]}`: list of role names whose agent files must be present and well-formed in `claude/agents/` (omit if this engine does not require a role check at preflight — e.g. verification engines that confirm roles during execution)
- `{write_test_path}`: path for the temporary write-permission marker, e.g. `claude/cycles/<cycle_id>/.write_test` (omit or mark `--dry-run: skip` if the engine conditionally skips the write test)

## Procedure

Execute all applicable sub-checks in order. Each is a hard gate — halt on first failure.

### 1. Required Files Present

For each path in `{required_files}`:
- Confirm the file exists.
- If any are missing: halt and report exactly which files are absent.

### 2. Required Authority Roles Exist

For each role name in `{required_roles}`:
- Locate the corresponding agent file under `claude/agents/`.
- Confirm the file exists and contains a `**Role:**` line matching the role name.
- If any agent file is missing or malformed: halt and report which roles are absent.

Skip this sub-check entirely if `{required_roles}` is empty.

### 3. Write Permission Test (Non-Destructive)

Create the file at `{write_test_path}` and confirm it can be written. Remove it immediately.
- If write fails: halt — report path and failure reason.
- If the file is not removed here (unexpected error), the calling engine's STEP 0 must clean it up before proceeding. Do not leave test marker files in cycle folders.

Skip this sub-check if `{write_test_path}` is marked `--dry-run: skip` by the caller.

## Halt semantics

All halts follow the standard halt report format per `claude/system/shared_standards.md`. Record the blocker before halting; do not proceed past a failed hard gate.

---

*This subroutine is shared across Roadmap Rebalance, Release Planning, Sprint Execution, Delivery Verification, and Post-Ship Closure engines. Sprint Planning is excluded (uses a different numbered-list preflight style).*
