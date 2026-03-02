

- open_escalations must not change
- deferred_escalations must not change
- accepted_risk_escalations must not change
- deferred_execution_blockers must not change

If any of the required tracked artifacts are missing at sealing time:
- stage2_scope_extraction.md
- stage3_execution_plan.md
- stage4_backlog_slice.md
Then:
- HALT.
- status remains Validated.

