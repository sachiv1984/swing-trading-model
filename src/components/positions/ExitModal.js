import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { AlertTriangle } from "lucide-react";
import { cn } from "@/lib/utils";

export default function ExitModal({ position, open, onClose, onConfirm }) {
  const [exitData, setExitData] = useState({
    exit_price: position?.current_price || "",
    exit_reason: "manual"
  });

  if (!position) return null;

  const currencySymbol = position.market === "UK" ? "£" : "$";
  const exitPrice = parseFloat(exitData.exit_price) || 0;
  const pnl = (exitPrice - position.entry_price) * position.shares;
  const pnlPercent = ((exitPrice - position.entry_price) / position.entry_price * 100);
  const isProfit = pnl >= 0;

  const handleConfirm = () => {
    onConfirm({
      ...position,
      exit_price: exitPrice,
      exit_reason: exitData.exit_reason,
      exit_date: new Date().toISOString().split("T")[0],
      pnl: pnl,
      pnl_percent: pnlPercent,
      status: "closed"
    });
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="bg-slate-900 border-slate-700 text-white max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-rose-400">
            <AlertTriangle className="w-5 h-5" />
            Exit Position
          </DialogTitle>
          <DialogDescription className="text-slate-400">
            You are about to close your position in {position.ticker}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 py-4">
          <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/50 space-y-3">
            <div className="flex justify-between">
              <span className="text-slate-400">Ticker</span>
              <span className="font-medium text-white">{position.ticker}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Shares</span>
              <span className="font-medium text-white">{position.shares}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Entry Price</span>
              <span className="font-medium text-white">{currencySymbol}{position.entry_price.toFixed(2)}</span>
            </div>
          </div>

          <div className="space-y-4">
            <div className="space-y-2">
              <Label className="text-slate-400">Exit Price</Label>
              <Input
                type="number"
                step="0.01"
                value={exitData.exit_price}
                onChange={(e) => setExitData({ ...exitData, exit_price: e.target.value })}
                className="bg-slate-800/50 border-slate-700 text-white"
              />
            </div>
            <div className="space-y-2">
              <Label className="text-slate-400">Exit Reason</Label>
              <Select
                value={exitData.exit_reason}
                onValueChange={(value) => setExitData({ ...exitData, exit_reason: value })}
              >
                <SelectTrigger className="bg-slate-800/50 border-slate-700 text-white">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-slate-800 border-slate-700">
                  <SelectItem value="manual">Manual Exit</SelectItem>
                  <SelectItem value="stop_hit">Stop Hit</SelectItem>
                  <SelectItem value="target">Target Reached</SelectItem>
                  <SelectItem value="market_regime">Market Regime</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {exitData.exit_price && (
            <div className={cn(
              "p-4 rounded-xl text-center border",
              isProfit 
                ? "bg-emerald-500/10 border-emerald-500/30" 
                : "bg-rose-500/10 border-rose-500/30"
            )}>
              <p className="text-sm text-slate-400 mb-1">Estimated P&L</p>
              <p className={cn(
                "text-2xl font-bold",
                isProfit ? "text-emerald-400" : "text-rose-400"
              )}>
                {isProfit ? "+" : ""}{currencySymbol}{pnl.toFixed(2)}
              </p>
              <p className={cn(
                "text-sm",
                isProfit ? "text-emerald-400/70" : "text-rose-400/70"
              )}>
                {isProfit ? "+" : ""}{pnlPercent.toFixed(2)}%
              </p>
            </div>
          )}
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
            className="bg-rose-600 hover:bg-rose-500 text-white"
            disabled={!exitData.exit_price}
          >
            Confirm Exit
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
