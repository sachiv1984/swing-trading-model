# claude/schemas/

Tooling metadata for the governance automation layer. **Not** governance content
(`claude/charter/`, `claude/strategy/`, `claude/system/`) — these files may be
updated directly as ordinary engineering work without going through a
prompt-sanctioned STEP. They exist to make parts of CLAUDE.md's hard rules
machine-checkable instead of relying on someone remembering to run a skill.

## Files

- **`state_field_owners.json`** — maps every top-level field in
  `.claude_current_state.json` to the engine that owns writing it. Checked by
  `.claude/hooks/check_state_field_ownership.py` (PostToolUse, warn-only)
  whenever `.claude_current_state.json` is edited, to catch a field going
  unowned/unmaintained the way `prior_cycle` and `last_audit_*` both did
  historically before anyone noticed.

- **`execution_state.schema.json`** — JSON Schema for
  `claude/cycles/<cycle_id>/execution_state.json`, checked by
  `.github/workflows/execution-state-schema-check.yml` on any PR touching the
  file. Exists to make CLAUDE.md §8 step 2b (shared-JSON-field schema-shape
  drift) partly CI-checked. Validated 0/73 failures against every historical
  `execution_state.json` under `claude/cycles/` as of 2026-08-13 (branch
  `chore/governance-automation-tooling`) — re-run the same check after any
  future edit to this schema:

  ```
  python3 -c "
  import json, jsonschema, glob
  schema = json.load(open('claude/schemas/execution_state.schema.json'))
  fail = 0
  for f in sorted(glob.glob('claude/cycles/*/execution_state.json')):
      try:
          jsonschema.validate(json.load(open(f)), schema)
      except jsonschema.ValidationError as e:
          fail += 1
          print('FAIL', f, e.message)
  print(f'{fail} failed')
  "
  ```

  If a future legitimate field addition breaks this against history, that's a
  signal the schema is over-fitted to the current shape — relax the
  offending property's `type` rather than special-casing individual cycles.
