
import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription } from "../ui/dialog";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { CheckCircle2 } from "lucide-react";

export default function PositionEntryModal({ signal, open, onClose, onConfirm }) {
  const [positionData, setPositionData] = useState({
    shares: signal?.suggested_shares || 0,
    entry_price: signal?.current_price || 0,
    stop_price: signal?.initial_stop || 0,
    entry_date: new Date().toISOString().split("T")[0]
  });

  if (!signal) return null;

  const isUS = signal.market === "US";
  const currencySymbol = isUS ? "$" : "£";
  const fxRate = isUS ? 1.3611 : 1;

  const handleConfirm = () => {
    onConfirm({
      ticker: signal.ticker,
      market: signal.market,
      entry_date: positionData.entry_date,
      entry_price: parseFloat(positionData.entry_price),
      shares: parseFloat(positionData.shares),
      stop_price: parseFloat(positionData.stop_price),
      atr_value: signal.atr_value || 0,
      current_price: parseFloat(positionData.entry_price),
      fx_rate: fxRate,
      status: "open"
    }, signal.id);
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="bg-slate-900 border-slate-700 text-white max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-cyan-400 text-xl">
            <CheckCircle2 className="w-6 h-6" />
            Confirm Position Entry
          </DialogTitle>
          <DialogDescription className="text-slate-400">
            Review and confirm the details for {signal.ticker}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 py-4">
          {/* Signal Summary */}
          <div className="p-4 rounded-lg bg-gradient-to-br from-cyan-500/10 to-violet-500/10 border border-cyan-500/30">
            <div className="grid grid-cols-2 gap-3 text-center">
              <div>
                <div className="text-xs text-slate-400">Ticker</div>
                <div className="text-lg font-bold text-white">{signal.ticker}</div>
              </div>
              <div>
                <div className="text-xs text-slate-400">Market</div>
                <div className="text-lg font-bold text-white">{signal.market} {isUS ? "🇺🇸" : "🇬🇧"}</div>
              </div>
            </div>
          </div>

          {/* Editable Fields */}
          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1">
                <Label className="text-xs text-slate-400">Shares</Label>
                <Input
                  type="number"
                  step="0.01"
                  value={positionData.shares}
                  onChange={(e) => setPositionData({ ...positionData, shares: e.target.value })}
                  className="bg-slate-800/50 border-slate-700 text-white h-10"
                />
              </div>
              <div className="space-y-1">
                <Label className="text-xs text-slate-400">Entry Price ({currencySymbol})</Label>
                <Input
                  type="number"
                  step="0.01"
                  value={positionData.entry_price}
                  onChange={(e) => setPositionData({ ...positionData, entry_price: e.target.value })}
                  className="bg-slate-800/50 border-slate-700 text-white h-10"
                />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1">
                <Label className="text-xs text-slate-400">Stop Price ({currencySymbol})</Label>
                <Input
                  type="number"
                  step="0.01"
                  value={positionData.stop_price}
                  onChange={(e) => setPositionData({ ...positionData, stop_price: e.target.value })}
                  className="bg-slate-800/50 border-slate-700 text-white h-10"
                />
              </div>
              <div className="space-y-1">
                <Label className="text-xs text-slate-400">Entry Date</Label>
                <Input
                  type="date"
                  value={positionData.entry_date}
                  onChange={(e) => setPositionData({ ...positionData, entry_date: e.target.value })}
                  className="bg-slate-800/50 border-slate-700 text-white h-10"
                />
              </div>
            </div>
          </div>

          {/* Cost Summary */}
          <div className="p-3 rounded-lg bg-slate-800/50 border border-slate-700/50">
            <div className="flex justify-between text-sm mb-1">
              <span className="text-slate-400">Total Cost (inc. fees)</span>
              <span className="text-white font-bold">£{signal.total_cost.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Momentum</span>
              <span className="text-emerald-400 font-bold">+{signal.momentum_percent.toFixed(1)}%</span>
            </div>
          </div>
        </div>

        <DialogFooter>
          <Button 
            variant="ghost" 
            onClick={onClose} 
            className="text-slate-400 hover:text-white hover:bg-slate-800"
          >
            Cancel
          </Button>
          <Button 
            onClick={handleConfirm} 
            className="bg-gradient-to-r from-cyan-600 to-violet-600 hover:from-cyan-500 hover:to-violet-500 text-white"
          >
            Confirm Entry
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
