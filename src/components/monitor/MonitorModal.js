import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "../ui/dialog";
import { Button } from "../ui/button";
import { CheckCircle2, XCircle, Loader2, AlertTriangle } from "lucide-react";
import StatusBadge from "../ui/StatusBadge";
import { cn } from "../../lib/utils";

export default function MonitorModal({ 
  open, 
  onClose, 
  positions, 
  marketRegimes, 
  isLoading,
  onConfirmExits 
}) {
  const [selectedExits, setSelectedExits] = useState([]);

  const getPositionStatus = (position) => {
    const regime = marketRegimes?.find(r => r.market === position.market);
    const isMarketRiskOff = regime?.status === "risk_off";
    const isStopHit = position.current_price && position.stop_price && 
                      position.current_price <= position.stop_price;
    
    if (isStopHit) return { status: "exit", reason: "Stop price hit" };
    if (isMarketRiskOff) return { status: "exit", reason: "Market risk off" };
    return { status: "hold", reason: "Position OK" };
  };

  const toggleExit = (positionId) => {
    setSelectedExits(prev => 
      prev.includes(positionId)
        ? prev.filter(id => id !== positionId)
        : [...prev, positionId]
    );
  };

  const handleConfirm = () => {
    const positionsToExit = positions.filter(p => selectedExits.includes(p.id));
    onConfirmExits(positionsToExit);
    setSelectedExits([]);
  };

  const exitSuggestions = positions?.filter(p => getPositionStatus(p).status === "exit") || [];

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="bg-slate-900 border-slate-700 text-white max-w-2xl max-h-[80vh] overflow-hidden flex flex-col">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-amber-500/20">
              <AlertTriangle className="w-5 h-5 text-amber-400" />
            </div>
            Daily Position Monitor
          </DialogTitle>
        </DialogHeader>

        <div className="flex-1 overflow-y-auto py-4">
          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="w-8 h-8 animate-spin text-slate-500" />
            </div>
          ) : positions?.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-slate-500">No open positions to monitor</p>
            </div>
          ) : (
            <div className="space-y-3">
              {positions?.map((position) => {
                const { status, reason } = getPositionStatus(position);
                const isExitSuggested = status === "exit";
                const isSelected = selectedExits.includes(position.id);
                const currencySymbol = position.market === "UK" ? "£" : "$";

                return (
                  <div
                    key={position.id}
                    onClick={() => isExitSuggested && toggleExit(position.id)}
                    className={cn(
                      "p-4 rounded-xl border transition-all",
                      isExitSuggested && "cursor-pointer",
                      isSelected 
                        ? "bg-rose-500/10 border-rose-500/30" 
                        : isExitSuggested
                          ? "bg-amber-500/5 border-amber-500/20 hover:border-amber-500/40"
                          : "bg-slate-800/30 border-slate-700/50"
                    )}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        {isExitSuggested ? (
                          isSelected ? (
                            <div className="p-2 rounded-lg bg-rose-500/20">
                              <XCircle className="w-5 h-5 text-rose-400" />
                            </div>
                          ) : (
                            <div className="p-2 rounded-lg bg-amber-500/20">
                              <AlertTriangle className="w-5 h-5 text-amber-400" />
                            </div>
                          )
                        ) : (
                          <div className="p-2 rounded-lg bg-emerald-500/20">
                            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                          </div>
                        )}
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="font-semibold text-white">{position.ticker}</span>
                            <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                              {position.market}
                            </span>
                          </div>
                          <p className="text-xs text-slate-500 mt-0.5">{reason}</p>
                        </div>
                      </div>
                      <StatusBadge status={status} />
                    </div>
                    
                    {isExitSuggested && (
                      <div className="mt-3 pt-3 border-t border-slate-700/50 grid grid-cols-3 gap-4 text-sm">
                        <div>
                          <p className="text-xs text-slate-500">Current</p>
                          <p className="text-white font-medium">
                            {currencySymbol}{position.current_price?.toFixed(2) || "—"}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-slate-500">Stop</p>
                          <p className="text-rose-400 font-medium">
                            {currencySymbol}{position.stop_price?.toFixed(2) || "—"}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-slate-500">Entry</p>
                          <p className="text-slate-300">
                            {currencySymbol}{position.entry_price?.toFixed(2)}
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>

        <DialogFooter className="border-t border-slate-700 pt-4">
          <div className="flex items-center justify-between w-full">
            <p className="text-sm text-slate-500">
              {selectedExits.length > 0 
                ? `${selectedExits.length} position${selectedExits.length > 1 ? "s" : ""} selected for exit`
                : exitSuggestions.length > 0 
                  ? `${exitSuggestions.length} exit suggestion${exitSuggestions.length > 1 ? "s" : ""}`
                  : "All positions healthy"
              }
            </p>
            <div className="flex gap-2">
              <Button 
                variant="ghost" 
                onClick={onClose} 
                className="text-slate-400 hover:text-white hover:bg-slate-800"
              >
                Close
              </Button>
              {selectedExits.length > 0 && (
                <Button 
                  onClick={handleConfirm}
                  className="bg-rose-600 hover:bg-rose-500 text-white"
                >
                  Exit Selected
                </Button>
              )}
            </div>
          </div>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
