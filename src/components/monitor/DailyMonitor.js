import { useRef, useState } from "react";
import PropTypes from "prop-types";
import { useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { Play } from "lucide-react";
import { base44 } from "../../api/base44Client";
import { Button } from "../ui/button";
import MonitorModal from "./MonitorModal";
import ExitModal from "../positions/ExitModal";
import { EXIT_REASON_RISK_OFF, EXIT_REASON_STOP } from "../../lib/exitCondition";

// Daily Position Monitor entry point (positions.md §Daily Position Monitor
// Exit Queue). Moved from the legacy widget Dashboard's Quick Actions to the
// Positions page header when that page was removed (ST-12, BLG-FE-247, v9.15;
// Product Owner ruling ESC-EXEC-20261104-05 option (a)). The Monitor, exit
// queue and pre-select behaviour are carried over unchanged.

// Monitor suggestion → ExitModal pre-selection
// (positions.md §Daily Position Monitor Exit Queue).
export function monitorPreselect(position, reason) {
  if (reason === "Stop price hit") {
    return {
      reason: EXIT_REASON_STOP,
      note: "Pre-selected from the Daily Position Monitor: the price is at or below the trailing stop and the grace period has ended.",
    };
  }
  if (reason === "Market risk off") {
    const market = position?.market === "UK" ? "UK" : "US";
    return {
      reason: EXIT_REASON_RISK_OFF,
      note: `Pre-selected from the Daily Position Monitor: the ${market} market is in a risk-off regime.`,
    };
  }
  return null;
}

export default function DailyMonitor({ positions, isLoading }) {
  const queryClient = useQueryClient();
  const [monitorOpen, setMonitorOpen] = useState(false);
  // Exit queue started from the Monitor: { items: [{ position, reason }], index }
  const [exitQueue, setExitQueue] = useState(null);
  // The queue the current exit request belongs to. A cancel clears it, so a
  // request that finishes after Cancel/Escape records its exit but does not
  // advance a queue that no longer exists.
  const activeQueueRef = useRef(null);
  const [monitorRestoreSelection, setMonitorRestoreSelection] = useState(null);

  // "Exit Selected" in the Monitor starts a queue: one ExitModal per selected
  // position, each recorded through POST /positions/{id}/exit after the user
  // confirms it (§8.1, §13). Nothing is submitted in bulk.
  const handleExitPositions = (exits) => {
    if (!exits.length) return;
    const queue = { items: exits, index: 0 };
    setMonitorRestoreSelection(null);
    setMonitorOpen(false);
    activeQueueRef.current = queue;
    setExitQueue(queue);
  };

  const queued = exitQueue ? exitQueue.items[exitQueue.index] : null;

  const handleQueuedExit = async (exitPayload) => {
    const queue = exitQueue;
    // Throws on a network error or non-2xx; ExitModal keeps the queue and shows the error.
    await base44.entities.Position.exit(exitPayload);

    queryClient.invalidateQueries({ queryKey: ["positions"] });
    queryClient.invalidateQueries({ queryKey: ["allPositions"] });
    queryClient.invalidateQueries({ queryKey: ["portfolio"] });
    queryClient.invalidateQueries({ queryKey: ["portfolioApi"] });
    queryClient.invalidateQueries({ queryKey: ["trades"] });

    // Cancelled while this request was in flight: the exit is recorded, the
    // queue stays ended.
    if (activeQueueRef.current !== queue) return;

    const next = queue.index + 1;
    if (next < queue.items.length) {
      const advanced = { ...queue, index: next };
      activeQueueRef.current = advanced;
      setExitQueue(advanced);
    } else {
      const n = queue.items.length;
      activeQueueRef.current = null;
      setExitQueue(null);
      toast.success(`Exited ${n} position${n === 1 ? "" : "s"}.`);
    }
  };

  // Cancel / ✕ / Escape ends the queue; the Monitor reopens with the
  // positions not yet exited still selected. Recorded exits stay recorded.
  const handleQueueCancel = () => {
    if (!exitQueue) return;
    activeQueueRef.current = null;
    setMonitorRestoreSelection(exitQueue.items.slice(exitQueue.index).map((i) => i.position.id));
    setExitQueue(null);
    setMonitorOpen(true);
  };

  return (
    <>
      <Button
        variant="outline"
        onClick={() => setMonitorOpen(true)}
        data-testid="daily-monitor-button"
      >
        <Play className="w-4 h-4 mr-2" />
        Daily Monitor
      </Button>

      <MonitorModal
        open={monitorOpen}
        onClose={() => {
          setMonitorOpen(false);
          // A restored selection applies to the reopen after a cancelled queue only.
          setMonitorRestoreSelection(null);
        }}
        positions={positions}
        isLoading={isLoading}
        onConfirmExits={handleExitPositions}
        restoreSelection={monitorRestoreSelection}
      />

      <ExitModal
        position={queued?.position || null}
        open={!!queued}
        onClose={handleQueueCancel}
        onConfirm={handleQueuedExit}
        preselect={queued ? monitorPreselect(queued.position, queued.reason) : null}
        queue={exitQueue ? { index: exitQueue.index + 1, total: exitQueue.items.length } : null}
      />
    </>
  );
}

DailyMonitor.propTypes = {
  positions: PropTypes.array.isRequired,
  isLoading: PropTypes.bool,
};
