### STEP 5 Postcondition — Release Roadmap Lock (Strict)

After roadmap_txn state = committed:

- Remove `claude/roadmap/.lock`
- Update state.json:
  - locks.roadmap_lock.status = "released"
  - locks.roadmap_lock.owned = false
  - artifacts.roadmap_lock = "released"

If removal fails:
- Record blocker and HALT.

