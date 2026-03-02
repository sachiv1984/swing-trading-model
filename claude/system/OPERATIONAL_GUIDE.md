
📘 Swing Trading Model: Operational Runbook
This guide defines the end-to-end flow from high-level strategy to automated code execution.
Step 1: Roadmap Rebalance (Strategy)
When to run: When you want to add new features, change priorities, or alter the long-term direction.
Command:
claude "run roadmap rebalance"

What happens: * Claude analyzes claude/strategy/ and claude/roadmap/.
 * It identifies conflicts or new opportunities.
 * It updates current_roadmap.md with new version targets (e.g., v1.8, v1.9).
 * Output: A revised strategic roadmap.
Step 2: Release Planning (Governance)
When to run: When a roadmap version (e.g., v1.7) is ready to be turned into a concrete work plan.
Command:
claude "plan release --version v1.7 --mode standard --issues gh"

What happens: * State Check: Creates a new folder: claude/cycles/YYYY-MM-DD__release-v1.7/.
 * Extraction: Breaks the roadmap down into EPIC-xx and ST-xx (Stories).
 * Locking: Temporarily locks the backlog to prevent data corruption.
 * Sync: Automatically creates GitHub Issues for every task.
 * Output: A "Sealed" cycle folder and a live GitHub Project board.
Step 3: Execution Loop (Engineering)
When to run: Daily, to actually write the code and close tasks.
3.1: Initialize Task
Identify the next ST-xx in your cycle folder and tell Claude:
claude "Let's start [ST-xx]. Create a new branch 'exec/v1.7-[TaskName]' and implement the requirements from the stage4_backlog_slice.md."

3.2: Governance-Stamped Commit
When the code is ready, you must use the ID prefix to trigger the automation:
claude "Commit with message: [EPIC-xx][ST-xx] Your description here. Then push to origin."

3.3: Pull Request & Auto-Sync
Once pushed, open the PR:
claude "Create a PR for this branch. Title it '[EPIC-xx][ST-xx] Title'. Link it to the issue by adding 'Closes #IssueNumber' in the body."

Result: * GitHub Action closes the issue.
 * Merging to main completes the lifecycle for that task.
Step 4: Cycle Closure
When to run: When all Issues/Stories in the cycle are marked "Closed."
Command:
claude "All tasks for v1.7 are complete. Update the root CLAUDE.md to reflect the version is Shipped and archive the cycle state."

🛡️ Core Rules
 * Never skip IDs: If a commit doesn't have [EPIC-xx][ST-xx], the bot won't see it.
 * Branch naming: Always start execution branches with exec/ to trigger the Governance Sync Loop.
 * Always Pull: Before starting a new task, always run git checkout main and git pull.
Would you like me to help you create the ST-02 implementation plan now, so we can test Step 3.2 of your new guide?
