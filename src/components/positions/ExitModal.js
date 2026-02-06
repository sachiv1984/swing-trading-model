import { useEffect, useMemo, useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogDescription,
} from "../ui/dialog";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";
import { AlertTriangle } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { base44 } from "../../api/base44Client";

export default function ExitModal({ position, open, onClose, onConfirm }) {
  // Unconditional hooks
  const [exitData, setExitData] = useState({
    shares: "",
    exit_price: "",
    exit_reason: "manual",
    exit_fx_rate: 1,
    exit_date: new Date().toISOString().split("T")[0],
  });

  // Seed/reset when position changes
  useEffect(() => {
    if (!position) return;
    setExitData({
      shares: String(position.shares ?? ""),
      exit_price: String(
        position.current_price_native ?? position.current_price ?? ""
      ),
      exit_reason: "manual",
      exit_fx_rate:
        position.market === "US"
          ? position.live_fx_rate ?? position.fx_rate ?? 1.27
          : 1,
      exit_date: new Date().toISOString().split("T")[0],
    });
  }, [position]);

  // Load settings
  const { data: settings } = useQuery({
    queryKey: ["settings"],
    queryFn: () => base44.entities.Settings.list(),
    initialData: [],
  });

  const settingsData = useMemo(() => {
    return settings && settings[0]
      ? settings[0]
      : {
          uk_commission: 9.95,
          us_commission: 0,
          stamp_duty_rate: 0.005,
          fx_fee_rate: 0.0015,
        };
  }, [settings]);

  // Derived values (guarded)
  const currencySymbol = position && position.market === "UK" ? "£" : "$";

  const exitPrice = Number(exitData.exit_price) || 0;
  const exitShares = Number(exitData.shares) || 0;
  const exitFxRate = Number(exitData.exit_fx_rate) || 1;

  const isValidShares =
    !!position && exitShares > 0 && exitShares <= Number(position.shares || 0);
  const isValidPrice = exitPrice > 0;
  const canSubmit = !!position && isValidShares && isValidPrice;

  // Proceeds (trade CCY -> GBP if US)
  const grossProceeds = exitPrice * exitShares;
  const commission = position
    ? position.market === "UK"
      ? Number(settingsData.uk_commission || 0)
      : Number(settingsData.us_commission || 0)
    : 0;
  const stampDuty = 0; // no stamp duty on sales
  const fxFee =
    position && position.market === "US"
      ? grossProceeds * Number(settingsData.fx_fee_rate || 0)
      : 0;
  const totalExitFees = commission + stampDuty + fxFee;
  const netProceeds = grossProceeds - totalExitFees;
  const netProceedsGBP =
    position && position.market === "US" ? netProceeds * exitFxRate : netProceeds;

  // Entry cost for exited shares (includes original fees if present)
  const totalEntryCost = position
    ? (Number(position.fees) || 0) +
      (Number(position.entry_price) || 0) * (Number(position.shares) || 0)
    : 0;
  const entryCostPerShare =
    position && Number(position.shares) > 0
      ? totalEntryCost / Number(position.shares)
      : 0;
  const totalEntryCostForExitShares = entryCostPerShare * exitShares;

  // P&L
  const pnl = netProceedsGBP - totalEntryCostForExitShares;
  const pnlPercent =
    totalEntryCostForExitShares > 0
      ? (pnl / totalEntryCostForExitShares) * 100
      : 0;
  const isProfit = pnl >= 0;

  // Actions
  const handleConfirm = () => {
    if (!canSubmit || !position) return;
    onConfirm({
      ...position,
      shares: exitShares,
      exit_price: exitPrice,
      exit_reason: exitData.exit_reason,
      exit_date: exitData.exit_date,
      pnl: pnl,
      pnl_percent: pnlPercent,
      status: "closed",
      exit_fx_rate: exitFxRate,
      exit_fees: totalExitFees,
    });
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      {/* GRID SHELL so the body row always scrolls */}
      <DialogContent className="bg-slate-900 border-slate-700 text-white max-w-md max-h-[90vh] grid grid-rows-[auto_1fr_auto]">
        {/* Row 1: Header */}
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-rose-400">
            <AlertTriangle className="w-5 h-5" />
            Exit Position
          </DialogTitle>
          <DialogDescription className="text-slate-400">
            {position ? (
              <>You are about to close your position in {position.ticker}</>
            ) : (
              <>No position selected</>
            )}
          </DialogDescription>
        </DialogHeader>

        {/* Row 2: Scrollable body */}
        <div className="space-y-4 py-4 overflow-y-auto min-h-0">
          {!position ? null : (
            <>
              {/* Top summary */}
              <div className="p-3 rounded-lg bg-slate-800/50 border border-slate-700/50 grid grid-cols-3 gap-3 text-center">
                <div>
                  <div className="text-xs text-slate-400">Ticker</div>
                  <div className="font-medium text-white">{position.ticker}</div>
                </div>
                <div>
                  <div className="text-xs text-slate-400">Total Shares</div>
                  <div className="font-medium text-white">{position.shares}</div>
                </div>
                <div>
                  <div className="text-xs text-slate-400">Entry Price</div>
                  <div className="font-medium text-white">
                    {currencySymbol}
                    {Number(position.entry_price || 0).toFixed(2)}
                  </div>
                </div>
              </div>

              {/* Form */}
              <div className="space-y-3">
                <div className="grid grid-cols-2 gap-3">
                  <div className="space-y-1">
                    <Label className="text-xs text-slate-400">Shares to Exit</Label>
                    <Input
                      type="number"
                      step="0.01"
                      value={exitData.shares}
                      onChange={(e) =>
                        setExitData({ ...exitData, shares: e.target.value })
                      }
                      className="bg-slate-800/50 border-slate-700 text-white h-9"
                    />
                  </div>
                  <div className="space-y-1">
                    <Label className="text-xs text-slate-400">
                      Exit Price ({currencySymbol})
                    </Label>
                    <Input
                      type="number"
                      step="0.01"
                      value={exitData.exit_price}
                      onChange={(e) =>
                        setExitData({ ...exitData, exit_price: e.target.value })
                      }
                      className="bg-slate-800/50 border-slate-700 text-white h-9"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div className="space-y-1">
                    <Label className="text-xs text-slate-400">Exit Date</Label>
                    <Input
                      type="date"
                      value={exitData.exit_date}
                      onChange={(e) =>
                        setExitData({ ...exitData, exit_date: e.target.value })
                      }
                      className="bg-slate-800/50 border-slate-700 text-white h-9"
                    />
                  </div>
                  {position.market === "US" ? (
                    <div className="space-y-1">
                      <Label className="text-xs text-slate-400">FX Rate</Label>
                      <Input
                        type="number"
                        step="0.0001"
                        value={exitData.exit_fx_rate}
                        onChange={(e) =>
                          setExitData({
                            ...exitData,
                            exit_fx_rate: e.target.value,
                          })
                        }
                        className="bg-slate-800/50 border-slate-700 text-white h-9"
                      />
                    </div>
                  ) : null}
                </div>

                <div className="space-y-1">
                  <Label className="text-xs text-slate-400">Exit Reason</Label>
                  <Select
                    value={exitData.exit_reason}
                    onValueChange={(value) =>
                      setExitData({ ...exitData, exit_reason: value })
                    }
                  >
                    <SelectTrigger className="bg-slate-800/50 border-slate-700 text-white h-9">
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

              {/* Breakdown */}
              {exitData.exit_price && exitData.shares ? (
                <div className="p-3 rounded-lg bg-slate-800/50 border border-slate-700/50 space-y-2">
                  <p className="text-xs font-semibold text-slate-300 mb-2">
                    Exit Cost Breakdown
                  </p>

                  <div className="space-y-1.5 text-xs">
                    <div className="flex justify-between">
                      <span className="text-slate-400">Gross Value</span>
                      <span className="text-white">
                        {currencySymbol}
                        {grossProceeds.toFixed(2)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Commission</span>
                      <span className="text-rose-400">
                        -{currencySymbol}
                        {commission.toFixed(2)}
                      </span>
                    </div>
                    {position.market === "US" ? (
                      <div className="flex justify-between">
                        <span className="text-slate-400">FX Fee</span>
                        <span className="text-rose-400">
                          -{currencySymbol}
                          {fxFee.toFixed(2)}
                        </span>
                      </div>
                    ) : null}
                    <div className="flex justify-between pt-1.5 border-t border-slate-700 font-medium">
                      <span className="text-slate-300">Net Proceeds</span>
                      <span className="text-white">
                        {position.market === "US"
                          ? `£${netProceedsGBP.toFixed(2)}`
                          : `£${netProceeds.toFixed(2)}`}
                      </span>
                    </div>
                  </div>

                  <div className="space-y-1.5 pt-2 border-t-2 border-slate-700 text-xs">
                    <div className="flex justify-between">
                      <span className="text-slate-400">Entry Cost</span>
                      <span className="text-white">
                        £{totalEntryCostForExitShares.toFixed(2)}
                      </span>
                    </div>
                    <div className="flex justify-between font-bold pt-1.5 border-t border-slate-700">
                      <span className={isProfit ? "text-emerald-400" : "text-rose-400"}>
                        P&amp;L
                      </span>
                      <span className={isProfit ? "text-emerald-400" : "text-rose-400"}>
                        {isProfit ? "+" : ""}
                        £{pnl.toFixed(2)} ({isProfit ? "+" : ""}
                        {pnlPercent.toFixed(2)}%)
                      </span>
                    </div>
                  </div>
                </div>
              ) : null}
            </>
          )}
        </div>

        {/* Row 3: Footer */}
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
            disabled={!canSubmit}
          >
            Confirm Exit
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
