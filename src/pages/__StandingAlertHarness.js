/**
 * Test-only harness for the StandingAlert / StandingAlertStack component
 * (ST-04, EPIC-04, v7.7, BLG-FE-120).
 *
 * StandingAlert has no product integration this cycle (see
 * docs/design/2026-07-21__release-v7.7/standing-alert-component/ux_spec.md §3
 * — the Notification Feed integration point is identified for BLG-FE-116's
 * future work, not wired here). This route exists solely so Playwright can
 * exercise the real, rendered component (theme context, Tailwind classes)
 * rather than relying on an isolated unit-test renderer this project does
 * not have (no @testing-library/react dependency). Not linked from any nav,
 * not registered in pages.config.js, not discoverable in the app UI.
 */
import { useState } from "react";
import { StandingAlertStack } from "../components/ui/StandingAlert";

const SEED_ALERTS = [
  { id: "a1", severity: "info", message: "Info alert one" },
  { id: "a2", severity: "warning", message: "Warning alert two" },
  { id: "a3", severity: "critical", message: "Critical alert three" },
  { id: "a4", severity: "info", message: "Info alert four (overflow)" },
];

export default function StandingAlertHarness() {
  const [alerts, setAlerts] = useState(SEED_ALERTS);
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="p-8" data-testid="standing-alert-harness">
      <StandingAlertStack
        alerts={alerts}
        expanded={expanded}
        onToggleExpanded={() => setExpanded(true)}
        onDismiss={(id) => setAlerts((prev) => prev.filter((a) => a.id !== id))}
      />
      <button
        type="button"
        data-testid="harness-reset"
        onClick={() => { setAlerts(SEED_ALERTS); setExpanded(false); }}
      >
        Reset
      </button>
    </div>
  );
}
