**Owner:** PMO Lead
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-14

---

# ESCALATION HANDLING SUBROUTINE — Callable (Delegated Authority)

Trigger:
- Invoke whenever any step produces ⛔ Blockers AND `--auto-escalate=true`, OR when `status=Blocked`.

Create or append:
- `claude/cycles/<cycle_id>/escalations.md`

Escalations file rules:
- Location is always within the cycle folder.
- Append-only within the cycle (do not edit previous entries).
- Start with header:
  - Owner: PMO Lead
  - Class: Planning Document (Class 4)
  - Status: Active
  - Last Updated: <date>

**Escalation entry format, SLAs, append-only rule, and Accepted Risk constraints:** follow `claude/system/shared_standards.md §4` exactly.

### Deferred Governance Constraint (Hard Gate)
- Only owning authority may mark Deferred (by domain).
- Deferred requires trigger and Blocks execution field.
- No auto-carry; must be re-acknowledged next cycle.
- Deferred does not bypass Strategy/Quality/Lifecycle blocks; publish depends on publish gate.

### Decision Record Controls (Minimal Anti-Drift Set)
- Typed decisions only: AR or SRB.
- Naming:
  - AR: docs/product/decisions/AR-<release>-<cycle_id>-<esc_id>.md
  - SRB: docs/product/decisions/SRB-<release>-<cycle_id>-<esc_id>.md
- Mandatory template: header + required sections; missing field → HALT.

### Escalation Mutation Rule (Hard Gate)
If resolving an escalation modifies assumptions or Stage 2/3/4 artifacts or decision records:
- Update assumptions in state.json
- Execute RESUME PRECHECK invalidation map
- Do not proceed until required invalidated steps are re-run

### Escalation → State update rules
After processing escalations, update state.json:
- open_escalations, deferred_escalations, accepted_risk_escalations
- deferred_execution_blockers = deferred items with Blocks execution=Yes

If any Open escalations remain:
- status = Blocked
- HALT

---

*This subroutine is shared across Release Planning, Sprint Planning, and Delivery Verification engines.*
