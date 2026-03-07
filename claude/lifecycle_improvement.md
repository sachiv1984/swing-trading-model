Implement lifecycle state machine hardening for this repository.

Goal:
Ensure the development lifecycle cannot skip phases, deadlock, or drift due to inconsistent state management.

Instruction:
Prefer modifying existing files over creating new ones.

Important:

If lifecycle phases are already defined in the Sprint Planning Operational Playbook, derive the transition order from the playbook rather than inventing a new lifecycle.

Ensure existing active cycle state files remain valid under the new schema. If necessary, migrate current state values rather than invalidating them.

Scope:
Only modify files related to lifecycle state management, including:

- `.claude_current_state.json`
- cycle `state.json` files
- lifecycle state schemas
- prompts that read or write lifecycle state
- the Sprint Planning Operational Playbook / lifecycle guide

Tasks:

1. Establish a single source of truth for lifecycle state.

2. Ensure the lifecycle behaves as a deterministic state machine where every phase has:
   - a clear entry condition
   - a clear completion condition
   - exactly one valid next phase (or a defined branching rule).

3. Add validation rules that prevent:
   - skipping phases
   - writing invalid lifecycle states
   - multiple agents overwriting lifecycle state simultaneously.

4. Implement phase transition guards so lifecycle state can only move forward according to the defined phase order.

5. Add a recovery rule allowing a cycle to safely resume if execution stops mid-phase.

6. Update any prompts that read or write lifecycle state so they enforce the new rules.

7. Update the Sprint Planning Operational Playbook so the documented lifecycle rules match the implemented state machine behaviour.

Output only:

1. Files modified
2. Updated lifecycle state schema
3. Allowed phase transition table

Keep all changes minimal and consistent with the existing repository structure.
Do not add unnecessary documentation or commentary.