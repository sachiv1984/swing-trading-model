import { useMemo, useState } from "react";
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription
} from "../ui/dialog";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select";
import { AlertTriangle } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { base44 } from "../../api/base44Client";

function getTodayLocalISO() {
  const d = new Date();
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

export default function ExitModal({ position, open, onClose, onConfirm }) {
  if (!position) return null;

  const [exitData, setExitData] = useState({
    shares: position?.shares ?? 0, // default to full exit; user can reduce
    exit_price: position?.current_price ?? "",
    exit_reason: "manual",
    // Using position.fx_rate as the entry/live rate fallback. This is *exit* FX input; user can override.
    exit_fx_rate: position?.market === "US" ? (position?.fx_rate || 1.27) : 1,
    exit_date: getTodayLocalISO(),
  });

  const { data: settings, isLoading: settingsLoading, isError: settingsError } = useQuery({
    queryKey: ["settings"],
    queryFn: () => base44.entities.Settings.list(),
    initialData: [],
  });

  const settingsData = settings?.[0] || {
    uk_commission: 9.95,
    us_commission: 0,
    stamp_duty_rate: 0.005,
    fx_fee_rate: 0.0015,
  };
  const usingDefaults = settingsLoading || settingsError || !settings?.[0];

  const currencySymbol = position.market === "UK" ? "£" : "$";

  // Parse numeric inputs once
  const exitShares = useMemo(() => Number(exitData.shares) || 0, [exitData.shares]);
  const exitPrice = useMemo(() => Number(exitData.exit_price) || 0, [exitData.exit_price]);
  const exitFxRate = useMemo(() => Number(exitData.exit_fx_rate) || 1, [exitData.exit_fx_rate]);

  // --- Core calculations, normalized for P&L in GBP ---
  const calcs = useMemo(() => {
    // Gross & fees in native currency (USD for US, GBP for UK)
    const grossProceedsNative = exitPrice * exitShares;
    const commission = position.market === "UK" ? settingsData.uk_commission : settingsData.us_commission;
    const stampDutyNative = 0; // no stamp duty on sales
    const fxFeeNative = position.market === "US" ? (grossProceedsNative * settingsData.fx_fee_rate) : 0;
    const totalExitFeesNative = commission + stampDutyNative + fxFeeNative;
    const netProceedsNative = grossProceedsNative - totalExitFeesNative;

    // Convert exit proceeds for P&L in GBP
    const netProceedsGBP = position.market === "US"
      ? netProceedsNative * exitFxRate
      : netProceedsNative;

    // Entry cost (average per share) — native first
    const entryCostPerShareNative = (position.entry_price * position.shares + (position.fees || 0)) / Math.max(position.shares, 1);

    // Determine entry FX to convert the entry *basis* for P&L in GBP
    // If you have a dedicated historical entry FX (e.g., position.entry_fx_rate), prefer it here:
    const entryFxRate = position.market === "US" ? (position.entry_fx_rate || position.fx_rate || exitFxRate) : 1;

    // Convert entry basis to GBP
    const entryCostPerShareGBP = position.market === "US"
      ? entryCostPerShareNative * entryFxRate
      : entryCostPerShareNative;

    const totalEntryCostForExitSharesGBP = entryCostPerShareGBP * exitShares;

    // P&L (GBP)
    const pnlGBP = netProceedsGBP - totalEntryCostForExitSharesGBP;
    const pnlPercent = totalEntryCostForExitSharesGBP > 0 ? (pnlGBP / totalEntryCostForExitSharesGBP) * 100 : 0;
    const isProfit = pnlGBP >= 0;

    // Also compute a GBP value for total fees (for displaying/saving if needed)
    const totalExitFeesGBP = position.market === "US"
      ? totalExitFeesNative * exitFxRate
      : totalExitFeesNative;

    return {
      grossProceedsNative,
      commission,
      fxFeeNative,
      totalExitFeesNative,
      totalExitFeesGBP,
      netProceedsNative,
      netProceedsGBP,
      entryCostPerShareGBP,
      totalEntryCostForExitSharesGBP,
      pnlGBP,
      pnlPercent,
      isProfit,
      entryFxRateUsed: entryFxRate,
    };
  }, [exitPrice, exitShares, exitFxRate, position, settingsData]);

  // Validation
  const errors = {
    shares: exitShares <= 0
      ? "Shares must be greater than 0"
      : exitShares > position.shares
      ? "Cannot exit more than you hold"
      : "",
    exit_price: exitPrice <= 0 ? "Exit price must be greater than 0" : "",
    exit_fx_rate: position.market === "US" && exitFxRate <= 0 ? "FX rate must be greater than 0" : "",
  };
  const isValid = !errors.shares && !errors.exit_price && !errors.exit_fx_rate;

  const handleConfirm = () => {
    if (!isValid) return;

    onConfirm({
      // keep original fields you might persist
      ...position,
      // new/updated exit-specific fields
      shares: exitShares,
      exit_price: exitPrice,
      exit_reason: exitData.exit_reason,
      exit_date: exitData.exit_date,
      exit_fx_rate: exitFxRate,
      status: "closed",

      // computed breakdowns that match the UI
      net_proceeds_native: calcs.netProceedsNative,
      net_proceeds_gbp: calcs.netProceedsGBP,
      exit_fees_native: calcs.totalExitFeesNative,
      exit_fees_gbp: calcs.totalExitFeesGBP,
      pnl_gbp: calcs.pnlGBP,
      pnl_percent: calcs.pnlPercent,
      // optional: include the entry fx used for auditability
      entry_fx_rate_used: calcs.entryFxRateUsed,
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
          {/* Position summary */}
          <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/50 space-y-3">
            <div className="flex justify-between">
              <span className="text-slate-400">Ticker</span>
              <span className="font-medium text-white">{position.ticker}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Total Shares</span>
              <span className="font-medium text-white">{position.shares}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Entry Price</span>
              <span className="font-medium text-white">
                {currencySymbol}{Number(position.entry_price).toFixed(2)}
              </span>
            </div>
            {usingDefaults && (
              <div className="text-xs text-amber-400 pt-1">
                Using default settings while account settings load or if unavailable.
              </div>
            )}
          </div>

          {/* Inputs */}
          <div className="space-y-4">
            <div className="space-y-2">
              <Label className="text-slate-400">Shares to Exit</Label>
              <Input
                type="number"
                step="1"
                value={exitData.shares}
                onChange={(e) => setExitData({ ...exitData, shares: e.target.value })}
                className="bg-slate-800/50 border-slate-700 text-white"
                aria-invalid={!!errors.shares}
                aria-describedby="shares-error"
              />
              {errors.shares && (
                <p id="shares-error" className="text-xs text-rose-400">{errors.shares}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label className="text-slate-400">Exit Price ({currencySymbol})</Label>
              <Input
                type="number"
                step="0.01"
                value={exitData.exit_price}
                onChange={(e) => setExitData({ ...exitData, exit_price: e.target.value })}
                className="bg-slate-800/50 border-slate-700 text-white"
                aria-invalid={!!errors.exit_price}
                aria-describedby="price-error"
              />
              {errors.exit_price && (
                <p id="price-error" className="text-xs text-rose-400">{errors.exit_price}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label className="text-slate-400">Exit Date</Label>
              <Input
                type="date"
                value={exitData.exit_date}
                onChange={(e) => setExitData({ ...exitData, exit_date: e.target.value })}
                className="bg-slate-800/50 border-slate-700 text-white"
              />
            </div>

            {position.market === "US" && (
              <div className="space-y-2">
                <Label className="text-slate-400">FX Rate (USD → GBP)</Label>
                <Input
                  type="number"
                  step="0.0001"
                  value={exitData.exit_fx_rate}
                  onChange={(e) => setExitData({ ...exitData, exit_fx_rate: e.target.value })}
                  className="bg-slate-800/50 border-slate-700 text-white"
                  aria-invalid={!!errors.exit_fx_rate}
                  aria-describedby="fx-error"
                />
                {errors.exit_fx_rate && (
                  <p id="fx-error" className="text-xs text-rose-400">{errors.exit_fx_rate}</p>
                )}
              </div>
            )}

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

          {/* Breakdown — matches your new UI, with explicit currency labelling */}
          {exitData.exit_price && exitData.shares && (
            <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/50 space-y-2" aria-live="polite">
              <p className="text-sm font-medium text-slate-300 mb-3">Exit Cost Breakdown</p>

              <div className="space-y-2 pb-2">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">
                    Gross Value ({exitShares} shares @ {currencySymbol}{exitPrice.toFixed(2)})
                  </span>
                  <span className="text-white">{currencySymbol}{calcs.grossProceedsNative.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Commission</span>
                  <span className="text-rose-400">-{currencySymbol}{calcs.commission.toFixed(2)}</span>
                </div>
                {position.market === "US" && (
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">FX Fee ({(settingsData.fx_fee_rate * 100).toFixed(2)}%)</span>
                    <span className="text-rose-400">-${calcs.fxFeeNative.toFixed(2)}</span>
                  </div>
                )}
                <div className="flex justify-between text-sm pt-2 border-t border-slate-700">
                  <span className="text-slate-400">Total Exit Fees</span>
                  <span className="text-rose-400">
                    -{currencySymbol}{calcs.totalExitFeesNative.toFixed(2)}
                  </span>
                </div>
                <div className="flex justify-between text-sm font-medium pt-2 border-t border-slate-700">
                  <span className="text-slate-300">
                    Net Proceeds {position.market === "US" ? "(USD)" : "(GBP)"}
                  </span>
                  <span className="text-white">
                    {currencySymbol}{calcs.netProceedsNative.toFixed(2)}
                  </span>
                </div>

                {position.market === "US" && (
                  <>
                    <div className="flex justify-between text-sm">
                      <span className="text-slate-400">FX Rate</span>
                      <span className="text-white">{exitFxRate.toFixed(4)}</span>
                    </div>
                    <div className="flex justify-between text-sm font-medium">
                      <span className="text-slate-300">Net Proceeds (GBP)</span>
                      <span className="text-white">£{calcs.netProceedsGBP.toFixed(2)}</span>
                    </div>
                  </>
                )}
              </div>

              <div className="space-y-2 pt-3 border-t-2 border-slate-700">
                <p className="text-xs font-medium text-slate-400 mb-2">P&L Calculation (GBP)</p>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Original Entry Cost ({exitShares} shares)</span>
                  <span className="text-white">£{calcs.totalEntryCostForExitSharesGBP.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Exit Proceeds (after fees)</span>
                  <span className="text-white">£{calcs.netProceedsGBP.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-sm font-bold pt-2 border-t border-slate-700">
                  <span className={calcs.isProfit ? "text-emerald-400" : "text-rose-400"}>Profit/Loss</span>
                  <span className={calcs.isProfit ? "text-emerald-400" : "text-rose-400"}>
                    {calcs.isProfit ? "+" : ""}£{calcs.pnlGBP.toFixed(2)}
                    {" "}
                    ({calcs.isProfit ? "+" : ""}{calcs.pnlPercent.toFixed(2)}%)
                  </span>
                </div>
              </div>
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
            disabled={!isValid}
          >
            Confirm Exit
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
