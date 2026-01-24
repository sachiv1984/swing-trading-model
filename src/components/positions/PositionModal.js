import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "../ui/dialog";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { format, differenceInDays } from "date-fns";
import { cn } from "../../lib/utils";

export default function PositionModal({ position, open, onClose, onSave }) {
  const [formData, setFormData] = useState({
    current_price: "",
    stop_price: ""
  });

  useEffect(() => {
    if (position) {
      setFormData({
        current_price: position.current_price || "",
        stop_price: position.stop_price || ""
      });
    }
  }, [position]);

  if (!position) return null;

  const pnl = (formData.current_price - position.entry_price) * position.shares;
  const pnlPercent = ((formData.current_price - position.entry_price) / position.entry_price * 100);
  const isProfit = pnl >= 0;
  const daysHeld = differenceInDays(new Date(), new Date(position.entry_date));
  const currencySymbol = position.market === "UK" ? "£" : "$";

  const handleSave = () => {
    onSave({
      ...position,
      current_price: parseFloat(formData.current_price),
      stop_price: parseFloat(formData.stop_price)
    });
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="bg-slate-900 border-slate-700 text-white max-w-lg">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-3">
            <span className="text-xl font-bold">{position.ticker}</span>
            <span className="text-xs px-2 py-1 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
              {position.market}
            </span>
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-6 py-4">
          {/* Summary Stats */}
          <div className="grid grid-cols-3 gap-3">
            <div className="p-3 rounded-xl bg-slate-800/50 border border-slate-700/50">
              <p className="text-xs text-slate-500 mb-1">Days Held</p>
              <p className="text-lg font-semibold text-white">{daysHeld}</p>
            </div>
            <div className="p-3 rounded-xl bg-slate-800/50 border border-slate-700/50">
              <p className="text-xs text-slate-500 mb-1">Shares</p>
              <p className="text-lg font-semibold text-white">{position.shares}</p>
            </div>
            <div className={cn(
              "p-3 rounded-xl border",
              isProfit 
                ? "bg-emerald-500/10 border-emerald-500/30" 
                : "bg-rose-500/10 border-rose-500/30"
            )}>
              <p className="text-xs text-slate-500 mb-1">P&L</p>
              <p className={cn(
                "text-lg font-semibold",
                isProfit ? "text-emerald-400" : "text-rose-400"
              )}>
                {isProfit ? "+" : ""}{currencySymbol}{pnl.toFixed(2)}
              </p>
            </div>
          </div>

          {/* Entry Details */}
          <div className="p-4 rounded-xl bg-slate-800/30 border border-slate-700/50 space-y-3">
            <h4 className="text-sm font-medium text-slate-400">Entry Details</h4>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-xs text-slate-500">Entry Date</p>
                <p className="text-sm text-white">{format(new Date(position.entry_date), "MMM d, yyyy")}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500">Entry Price</p>
                <p className="text-sm text-white">{currencySymbol}{position.entry_price.toFixed(2)}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500">ATR Value</p>
                <p className="text-sm text-white">{position.atr_value?.toFixed(2) || "—"}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500">FX Rate</p>
                <p className="text-sm text-white">{position.fx_rate?.toFixed(4) || "1.0000"}</p>
              </div>
            </div>
          </div>

          {/* Editable Fields */}
          <div className="space-y-4">
            <div className="space-y-2">
              <Label className="text-slate-400">Current Price</Label>
              <Input
                type="number"
                step="0.01"
                value={formData.current_price}
                onChange={(e) => setFormData({ ...formData, current_price: e.target.value })}
                className="bg-slate-800/50 border-slate-700 text-white focus:border-cyan-500/50"
              />
            </div>
            <div className="space-y-2">
              <Label className="text-slate-400">Stop Price (Manual Override)</Label>
              <Input
                type="number"
                step="0.01"
                value={formData.stop_price}
                onChange={(e) => setFormData({ ...formData, stop_price: e.target.value })}
                className="bg-slate-800/50 border-slate-700 text-white focus:border-rose-500/50"
              />
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
            onClick={handleSave} 
            className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0"
          >
            Save Changes
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
