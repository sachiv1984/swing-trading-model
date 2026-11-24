Fixtures for `tests/test_check_e2e_locator_collisions.py` (ST-21, BLG-QA-268, v9.18).

- `b2d93f6d/`: v9.17 ST-01's `src/` diff and `compliance-panel.spec.js` as it was at that commit (SC-COMP-02/03/07 broke in CI). `tests-fixed/` holds the spec after the `6b475ae0` locator fix.
- `99f16e6d/`: v9.17 ST-03's pre-fix `src/` diff, `lifecycle-badge-grace-calendar-days.spec.js` at that commit (SC-LBG-03 broke), and the one component the check reads (`GracePeriodAlertContent`).

CI checks out a shallow clone, so the test reads these files instead of replaying the commits.
