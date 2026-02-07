import { useEffect, useMemo, useState } from "react";
import {Dialog,DialogContent,DialogHeader,DialogTitle,DialogFooter,DialogDescription,} from "../ui/dialog";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import {Select,SelectContent,SelectItem,SelectTrigger,SelectValue,} from "../ui/select";
import { AlertTriangle } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { base44 } from "../../api/base44Client";

export default function ExitModal({ position, open, onClose, onConfirm }) {
  // Unconditional hooks
  const [exitData, setExitData] = useState({
    shares: "",
    exit_price: "",
    exit_reason: "Manual Exit",
    exit_fx_rate: 1,
    exit_date: new Date().toISOString().split("T")[0],
  });

  // Seed/reset when position changes
  useEffect(() => {
    if (!position) return;
    setExitData({
      shares: String(position.shares ?? ""),
      // Use current_price_native for display (shows USD for US stocks, GBP for UK)
      exit_price: String(
        position.current_price_native ?? position.current_price ?? ""
      ),
      exit_reason: "Manual Exit",
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

  // Validation logic
  const isValidShares =
    !!position && exitShares > 0 && exitShares <= Number(position.shares || 0);
  const isValidPrice = exitPrice > 0;
  const canSubmit = !!position && isValidShares && isValidPrice;

  // === EXIT PROCEEDS CALCULATION ===
  
  // For US stocks: Calculate in USD first, then convert to GBP
  // For UK stocks: Calculate directly in GBP
  let grossProceeds, commission, fxFee, netProceeds, netProceedsGBP;
  
  if (position && position.market === "US") {
    // US Stock Exit Calculation
    // 1. Calculate gross proceeds in USD
    grossProceeds = exitPrice * exitShares; // USD
    
    // 2. Commission (from settings, usually $0 for US stocks)
    commission = Number(settingsData.us_commission || 0); // USD
    
    // 3. FX Fee: 0.15% of gross proceeds in USD
    fxFee = grossProceeds * Number(settingsData.fx_fee_rate || 0.0015); // USD
    
    // 4. Net proceeds in USD
    const netProceedsUSD = grossProceeds - commission - fxFee; // USD
    
    // 5. Convert to GBP using user's FX rate
    netProceedsGBP = netProceedsUSD / exitFxRate; // GBP
    
    // For display purposes
    netProceeds = netProceedsUSD; // Keep USD for breakdown display
    
  } else if (position) {
    // UK Stock Exit Calculation
    grossProceeds = exitPrice * exitShares; // GBP
    commission = Number(settingsData.uk_commission || 0); // GBP
    fxFee = 0; // No FX fee for UK stocks
    netProceeds = grossProceeds - commission; // GBP
    netProceedsGBP = netProceeds; // Already in GBP
  }

  // === ENTRY COST CALCULATION - FIXED FOR MISSING total_cost ===
  
  // CRITICAL: position object doesn't have total_cost field!
  // We need to calculate it from entry_price and shares
  
  let totalPositionCost = 0;
  
  if (position) {
    if (position.total_cost !== undefined) {
      // If total_cost exists, use it
      totalPositionCost = Number(position.total_cost);
    } else {
      // Calculate entry cost from entry_price, shares, and fees
      const entryPrice = Number(position.entry_price || 0); // In native currency
      const shares = Number(position.shares || 0);
      const entryFxRate = Number(position.fx_rate || 1);
      
      if (position.market === "US") {
        // US Stock: entry_price is in USD, need to convert to GBP
        const grossCostUSD = entryPrice * shares;
        const entryCommission = Number(settingsData.us_commission || 0);
        const entryFxFee = grossCostUSD * Number(settingsData.fx_fee_rate || 0.0015);
        const totalCostUSD = grossCostUSD + entryCommission + entryFxFee;
        
        // Convert to GBP using ENTRY fx_rate
        totalPositionCost = totalCostUSD / entryFxRate;
      } else {
        // UK Stock: entry_price is in GBP
        const grossCostGBP = entryPrice * shares;
        const entryCommission = Number(settingsData.uk_commission || 0);
        const stampDuty = grossCostGBP * Number(settingsData.stamp_duty_rate || 0.005);
        totalPositionCost = grossCostGBP + entryCommission + stampDuty;
      }
    }
  }
  
  const totalPositionShares = position ? Number(position.shares || 0) : 0;
  
  console.log('Entry cost calculation:', {
    totalPositionCost,
    totalPositionShares,
    exitShares,
    entryPrice: position?.entry_price,
    entryFxRate: position?.fx_rate,
    market: position?.market,
    calculatedFromFields: !position?.total_cost
  });
  
  // Calculate cost per share (this includes all entry fees distributed across shares)
  const costPerShare = totalPositionShares > 0 
    ? totalPositionCost / totalPositionShares 
    : 0;
  
  // Calculate entry cost for just the shares being exited
  const entryCostForExitShares = costPerShare * exitShares;

  // === P&L CALCULATION ===
  
  // P&L = Net Proceeds (GBP) - Entry Cost (GBP)
  const pnl = netProceedsGBP - entryCostForExitShares;
  const pnlPercent =
    entryCostForExitShares > 0
      ? (pnl / entryCostForExitShares) * 100
      : 0;
  const isProfit = pnl >= 0;

  // Actions - FIX: Ensure proper number conversion and validation
  const handleConfirm = () => {
    if (!canSubmit || !position) {
      console.error("Invalid exit data:", { 
        exitShares, 
        exitPrice, 
        canSubmit,
        exitData 
      });
      return;
    }
    
    // Parse and validate numbers explicitly
    const parsedShares = parseFloat(exitData.shares);
    const parsedPrice = parseFloat(exitData.exit_price);
    const parsedFxRate = parseFloat(exitData.exit_fx_rate);
    
    // Double check validation
    if (isNaN(parsedShares) || parsedShares <= 0) {
      console.error("Invalid shares:", exitData.shares);
      return;
    }
    
    if (isNaN(parsedPrice) || parsedPrice <= 0) {
      console.error("Invalid price:", exitData.exit_price);
      return;
    }
    
    // Build payload
    const exitPayload = {
      position_id: position.id,
      shares: parsedShares,
      exit_price: parsedPrice,
      exit_reason: exitData.exit_reason,
      exit_date: exitData.exit_date,
    };

    // Only include fx_rate if it's a US position and has a valid value
    if (position.market === "US") {
      if (isNaN(parsedFxRate) || parsedFxRate <= 0) {
        console.error("Invalid FX rate for US position:", exitData.exit_fx_rate);
        return;
      }
      exitPayload.fx_rate = parsedFxRate;
    }

    console.log("Sending exit payload:", exitPayload);
    onConfirm(exitPayload);
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
                      min="0.01"
                      max={position.shares}
                      value={exitData.shares}
                      onChange={(e) =>
                        setExitData({ ...exitData, shares: e.target.value })
                      }
                      className="bg-slate-800/50 border-slate-700 text-white h-9"
                    />
                    {!isValidShares && exitData.shares && (
                      <p className="text-xs text-rose-400 mt-1">
                        Must be between 0.01 and {position.shares}
                      </p>
                    )}
                  </div>
                  <div className="space-y-1">
                    <Label className="text-xs text-slate-400">
                      Exit Price ({currencySymbol})
                    </Label>
                    <Input
                      type="number"
                      step="0.01"
                      min="0.01"
                      value={exitData.exit_price}
                      onChange={(e) =>
                        setExitData({ ...exitData, exit_price: e.target.value })
                      }
                      className="bg-slate-800/50 border-slate-700 text-white h-9"
                    />
                    {!isValidPrice && exitData.exit_price && (
                      <p className="text-xs text-rose-400 mt-1">
                        Price must be greater than 0
                      </p>
                    )}
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
                      <Label className="text-xs text-slate-400">FX Rate (GBP/USD)</Label>
                      <Input
                        type="number"
                        step="0.0001"
                        min="0.0001"
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
                      <SelectItem value="Manual Exit">Manual Exit</SelectItem>
                      <SelectItem value="Stop Loss Hit">Stop Loss Hit</SelectItem>
                      <SelectItem value="Target Reached">Target Reached</SelectItem>
                      <SelectItem value="Risk-Off Signal">Risk-Off Signal</SelectItem>
                      <SelectItem value="Trailing Stop">Trailing Stop</SelectItem>
                      <SelectItem value="Partial Profit Taking">Partial Profit Taking</SelectItem>
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
                      <span className="text-slate-400">
                        Gross Value {position.market === "US" ? "(USD)" : ""}
                      </span>
                      <span className="text-white">
                        {currencySymbol}
                        {grossProceeds.toFixed(2)}
                      </span>
                    </div>
                    
                    {/* ALWAYS show commission (even if $0.00) */}
                    <div className="flex justify-between">
                      <span className="text-slate-400">Commission</span>
                      <span className={commission > 0 ? "text-rose-400" : "text-slate-500"}>
                        {commission > 0 ? "-" : ""}
                        {currencySymbol}
                        {commission.toFixed(2)}
                      </span>
                    </div>
                    
                    {/* Show FX fee for US stocks */}
                    {position.market === "US" && (
                      <div className="flex justify-between">
                        <span className="text-slate-400">FX Fee (0.15%)</span>
                        <span className="text-rose-400">
                          -${fxFee.toFixed(2)}
                        </span>
                      </div>
                    )}
                    
                    {/* For US stocks, show USD net proceeds before conversion */}
                    {position.market === "US" && (
                      <>
                        <div className="flex justify-between">
                          <span className="text-slate-400">
                            Net Proceeds (USD)
                          </span>
                          <span className="text-white">
                            ${netProceeds.toFixed(2)}
                          </span>
                        </div>
                        <div className="flex justify-between text-xs opacity-75">
                          <span className="text-slate-400">
                            @ 1.{(exitFxRate - 1).toFixed(4).substring(2)}
                          </span>
                          <span className="text-slate-400">
                            ÷ {exitFxRate.toFixed(4)} = GBP
                          </span>
                        </div>
                      </>
                    )}
                    
                    <div className="flex justify-between pt-1.5 border-t border-slate-700 font-medium">
                      <span className="text-slate-300">Net Proceeds (GBP)</span>
                      <span className="text-white">
                        £{netProceedsGBP.toFixed(2)}
                      </span>
                    </div>
                  </div>

                  <div className="space-y-1.5 pt-2 border-t-2 border-slate-700 text-xs">
                    <div className="flex justify-between">
                      <span className="text-slate-400">Entry Cost (incl. fees)</span>
                      <span className="text-white">
                        £{entryCostForExitShares.toFixed(2)}
                      </span>
                    </div>
                    <div className="flex justify-between font-bold pt-1.5 border-t border-slate-700">
                      <span className={isProfit ? "text-emerald-400" : "text-rose-400"}>
                        Realized P&L
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
