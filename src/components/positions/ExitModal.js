export default function ExitModal({ position, open, onClose, onConfirm }) {
  const [exitData, setExitData] = useState({
    shares: position?.shares || 0,
    exit_price: position?.current_price || "",
    exit_reason: "manual",
    exit_fx_rate: position?.market === "US" ? (position?.fx_rate || 1.27) : 1,
    exit_date: new Date().toISOString().split("T")[0]
  });

  const { data: settings } = useQuery({
    queryKey: ["settings"],
    queryFn: () => base44.entities.Settings.list(),
    initialData: [],
  });

  const settingsData = settings?.[0] || {
    uk_commission: 9.95,
    us_commission: 0,
    stamp_duty_rate: 0.005,
    fx_fee_rate: 0.0015
  };

  if (!position) return null;

  const currencySymbol = position.market === "UK" ? "£" : "$";
  const exitPrice = parseFloat(exitData.exit_price) || 0;
  const exitShares = parseFloat(exitData.shares) || 0;
  const exitFxRate = parseFloat(exitData.exit_fx_rate) || 1;
  
  // Calculate exit proceeds
  const grossProceeds = exitPrice * exitShares;
  const commission = position.market === "UK" ? settingsData.uk_commission : settingsData.us_commission;
  const stampDuty = 0; // No stamp duty on sales
  const fxFee = position.market === "US" ? (grossProceeds * settingsData.fx_fee_rate) : 0;
  const totalExitFees = commission + stampDuty + fxFee;
  const netProceeds = grossProceeds - totalExitFees;
  const netProceedsGBP = position.market === "US" ? (netProceeds * exitFxRate) : netProceeds;
  
  // Calculate original entry cost for the shares being exited
  const entryCostPerShare = (position.entry_price * position.shares + (position.fees || 0)) / position.shares;
  const totalEntryCostForExitShares = entryCostPerShare * exitShares;
  
  // Calculate P&L
  const pnl = netProceedsGBP - totalEntryCostForExitShares;
  const pnlPercent = (pnl / totalEntryCostForExitShares) * 100;
  const isProfit = pnl >= 0;

  const handleConfirm = () => {
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
      exit_fees: totalFees
    });
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="bg-slate-900 border-slate-700 text-white max-w-md max-h-[90vh] flex flex-col">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-rose-400">
            <AlertTriangle className="w-5 h-5" />
            Exit Position
          </DialogTitle>
          <DialogDescription className="text-slate-400">
            You are about to close your position in {position.ticker}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 py-4 overflow-y-auto flex-1">
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
              <div className="font-medium text-white">{currencySymbol}{position.entry_price.toFixed(2)}</div>
            </div>
          </div>

          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1">
                <Label className="text-xs text-slate-400">Shares to Exit</Label>
                <Input
                  type="number"
                  step="1"
                  value={exitData.shares}
                  onChange={(e) => setExitData({ ...exitData, shares: e.target.value })}
                  className="bg-slate-800/50 border-slate-700 text-white h-9"
                />
              </div>
              <div className="space-y-1">
                <Label className="text-xs text-slate-400">Exit Price ({currencySymbol})</Label>
                <Input
                  type="number"
                  step="0.01"
                  value={exitData.exit_price}
                  onChange={(e) => setExitData({ ...exitData, exit_price: e.target.value })}
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
                  onChange={(e) => setExitData({ ...exitData, exit_date: e.target.value })}
                  className="bg-slate-800/50 border-slate-700 text-white h-9"
                />
              </div>
              {position.market === "US" && (
                <div className="space-y-1">
                  <Label className="text-xs text-slate-400">FX Rate</Label>
                  <Input
                    type="number"
                    step="0.0001"
                    value={exitData.exit_fx_rate}
                    onChange={(e) => setExitData({ ...exitData, exit_fx_rate: e.target.value })}
                    className="bg-slate-800/50 border-slate-700 text-white h-9"
                  />
                </div>
              )}
            </div>
            <div className="space-y-1">
              <Label className="text-xs text-slate-400">Exit Reason</Label>
              <Select
                value={exitData.exit_reason}
                onValueChange={(value) => setExitData({ ...exitData, exit_reason: value })}
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

          {exitData.exit_price && exitData.shares && (
            <div className="p-3 rounded-lg bg-slate-800/50 border border-slate-700/50 space-y-2">
              <p className="text-xs font-semibold text-slate-300 mb-2">Exit Cost Breakdown</p>
              
              <div className="space-y-1.5 text-xs">
                <div className="flex justify-between">
                  <span className="text-slate-400">Gross Value</span>
                  <span className="text-white">{currencySymbol}{grossProceeds.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Commission</span>
                  <span className="text-rose-400">-{currencySymbol}{commission.toFixed(2)}</span>
                </div>
                {position.market === "US" && (
                  <div className="flex justify-between">
                    <span className="text-slate-400">FX Fee</span>
                    <span className="text-rose-400">-{currencySymbol}{fxFee.toFixed(2)}</span>
                  </div>
                )}
                <div className="flex justify-between pt-1.5 border-t border-slate-700 font-medium">
                  <span className="text-slate-300">Net Proceeds</span>
                  <span className="text-white">{position.market === "US" ? `£${netProceedsGBP.toFixed(2)}` : `£${netProceeds.toFixed(2)}`}</span>
                </div>
              </div>

              <div className="space-y-1.5 pt-2 border-t-2 border-slate-700 text-xs">
                <div className="flex justify-between">
                  <span className="text-slate-400">Entry Cost</span>
                  <span className="text-white">£{totalEntryCostForExitShares.toFixed(2)}</span>
                </div>
                <div className="flex justify-between font-bold pt-1.5 border-t border-slate-700">
                  <span className={isProfit ? "text-emerald-400" : "text-rose-400"}>P&L</span>
                  <span className={isProfit ? "text-emerald-400" : "text-rose-400"}>
                    {isProfit ? "+" : ""}£{pnl.toFixed(2)} ({isProfit ? "+" : ""}{pnlPercent.toFixed(2)}%)
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
            disabled={!exitData.exit_price || !exitData.shares}
          >
            Confirm Exit
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
