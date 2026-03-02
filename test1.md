Initialize the execution for Cycle v1.7. 

First, read 'claude/cycles/2026-03-02__release-v1.7/stage4_backlog_slice.md' to identify the specific requirements for [ST-01] under [EPIC-01]. 

Next, perform these actions:
1. Create and switch to a new git branch: 'exec/v1.7-foundation'.
2. Execute the technical implementation for [ST-01] (e.g., setting up core directories, project anchors, or base configuration as defined in the slice).
3. Once the code is verified, commit the changes using this EXACT format: "[EPIC-01][ST-01] Initializing foundation and governance anchors".
4. Push the branch to origin.

Confirm once the push is complete so I can verify the GitHub Action trigger.

claude "Use the 'gh' CLI to create a Pull Request from 'exec/v1.7-foundation' to 'main'. Title it '[EPIC-01][ST-01] Foundation & Governance Anchors'. In the body, link it to the issue by writing 'Closes #XX' (replace XX with the actual issue number for ST-01)."
