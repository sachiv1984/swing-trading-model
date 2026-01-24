import { useState } from "react";
import { useMutation, useQueryClient, useQuery } from "@tanstack/react-query";
import { base44 } from "../api/base44Client";
import { useNavigate } from "react-router-dom";
import { createPageUrl } from "../utils";
import { motion } from "framer-motion";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import PageHeader from "../components/ui/PageHeader";
import { ArrowLeft, Calculator, Loader2, CheckCircle2 } from "lucide-react";
import { Link } from "react-router-dom";
import { cn } from "../lib/utils";

export default function TradeEntry() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  
  const [formData, setFormData] = useState({
    ticker: "",
    market: "UK",
    entry_date: new Date().toISOString().split("T")[0],
    shares: "",
    entry_price: "",
    fx_rate: "1",
    atr_value: "",
  });

  const { data: settings } = useQuery({
    queryKey: ["settings"],
    queryFn: () => base44.entities.Settings.list(),
  });

  const currentSettings = settings?.[0] || {
    atr_multiplier_initial: 2,
    uk_commission: 9.95,
    us_commission: 0,
    stamp_duty_rate: 0.005,
  };

  const createMutation = useMutation({
    mutationFn: (data) => base44.entities.Position.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["positions"] });
      navigate(createPageUrl("Positions"));
    },
  });

  const handleChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const detectMarket = (ticker) => {
    if (ticker.endsWith(".L") || /^[A-Z]{2,4}$/.test(ticker)) {
      return "UK";
    }
    return "US";
  };

  const handleTickerChange = (value) => {
    const market = detectMarket(value.toUpperCase());
    setFormData((prev) => ({
      ...prev,
      ticker: value.toUpperCase(),
      market,
      fx_rate: market === "US" ? "1.27" : "1",
    }));
  };

  const calculateCosts = () => {
    const shares = parseFloat(formData.shares) || 0;
    const price = parseFloat(formData.entry_price) || 0;
    const fxRate = parseFloat(formData.fx_rate) || 1;
    const atr = parseFloat(formData.atr_value) || 0;

    const grossValue = shares * price;
    const grossValueGBP = formData.market === "US" ? grossValue / fxRate : grossValue;

    const commission = formData.market === "UK" 
      ? currentSettings.uk_commission 
      : currentSettings.us_commission;

    const stampDuty = formData.market === "UK" 
      ? grossValueGBP * currentSettings.stamp_duty_rate 
      : 0;

    const totalCost = grossValueGBP + commission + stampDuty;

    const initialStop = price - (atr * currentSettings.atr_multiplier_initial);
    const riskPerShare = price - initialStop;
    const totalRisk = riskPerShare * shares;
    const totalRiskGBP = formData.market === "US" ? totalRisk / fxRate : totalRisk;

    return {
      grossValue,
      grossValueGBP,
      commission,
      stampDuty,
      totalCost,
      initialStop,
      riskPerShare,
      totalRisk: totalRiskGBP,
      currencySymbol: formData.market === "UK" ? "£" : "$",
    };
  };

  const costs = calculateCosts();
  const isFormValid = formData.ticker && formData.shares && formData.entry_price;

  const handleSubmit = () => {
    if (!isFormValid) return;

    createMutation.mutate({
      ticker: formData.ticker,
      market: formData.market,
      entry_date: formData.entry_date,
      shares: parseFloat(formData.shares),
      entry_price: parseFloat(formData.entry_price),
      current_price: parseFloat(formData.entry_price),
      fx_rate: parseFloat(formData.fx_rate),
      atr_value: parseFloat(formData.atr_value) || null,
      stop_price: costs.initialStop > 0 ? costs.initialStop : null,
      fees: costs.commission + costs.stampDuty,
      status: "open",
    });
  };

  return (
    <div className="space-y-6 max-w-2xl mx-auto">
      <PageHeader
        title="Enter New Position"
        description="Add a new trade to your portfolio"
        actions={
          <Link to={createPageUrl("Positions")}>
            <Button variant="ghost" className="text-slate-400 hover:text-white hover:bg-slate-800">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back
            </Button>
          </Link>
        }
      />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-6"
      >
        <div className="space-y-6">
          {/* Ticker & Market */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label className="text-slate-400">Ticker Symbol</Label>
              <Input
                value={formData.ticker}
                onChange={(e) => handleTickerChange(e.target.value)}
                placeholder="e.g., AAPL or VOD.L"
                className="bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-500 focus:border-cyan-500/50 focus:ring-cyan-500/20"
              />
            </div>
            <div className="space-y-2">
              <Label className="text-slate-400">Market</Label>
              <Select
                value={formData.market}
                onValueChange={(value) => handleChange("market", value)}
              >
                <SelectTrigger className="bg-slate-800/50 border-slate-700 text-white">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-slate-800 border-slate-700">
                  <SelectItem value="UK">UK</SelectItem>
                  <SelectItem value="US">US</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Entry Date */}
          <div className="space-y-2">
            <Label className="text-slate-400">Entry Date</Label>
            <Input
              type="date"
              value={formData.entry_date}
              onChange={(e) => handleChange("entry_date", e.target.value)}
              className="bg-slate-800/50 border-slate-700 text-white"
            />
          </div>

          {/* Shares & Price */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label className="text-slate-400">Number of Shares</Label>
              <Input
                type="number"
                value={formData.shares}
                onChange={(e) => handleChange("shares", e.target.value)}
                placeholder="0"
                className="bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-500"
              />
            </div>
            <div className="space-y-2">
              <Label className="text-slate-400">Fill Price ({costs.currencySymbol})</Label>
              <Input
                type="number"
                step="0.01"
                value={formData.entry_price}
                onChange={(e) => handleChange("entry_price", e.target.value)}
                placeholder="0.00"
                className="bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-500"
              />
            </div>
          </div>

          {/* FX Rate (for US) */}
          {formData.market === "US" && (
            <div className="space-y-2">
              <Label className="text-slate-400">FX Rate (USD/GBP)</Label>
              <Input
                type="number"
                step="0.0001"
                value={formData.fx_rate}
                onChange={(e) => handleChange("fx_rate", e.target.value)}
                className="bg-slate-800/50 border-slate-700 text-white"
              />
            </div>
          )}

          {/* ATR */}
          <div className="space-y-2">
            <Label className="text-slate-400">ATR Value (Optional)</Label>
            <Input
              type="number"
              step="0.01"
              value={formData.atr_value}
              onChange={(e) => handleChange("atr_value", e.target.value)}
              placeholder="For stop calculation"
              className="bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-500"
            />
            {formData.atr_value && costs.initialStop > 0 && (
              <p className="text-xs text-slate-500">
                Initial stop: <span className="text-rose-400">{costs.currencySymbol}{costs.initialStop.toFixed(2)}</span>
                {" "}({currentSettings.atr_multiplier_initial}x ATR below entry)
              </p>
            )}
          </div>
        </div>
      </motion.div>

      {/* Cost Summary */}
      {isFormValid && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-6"
        >
          <div className="flex items-center gap-2 mb-4">
            <div className="p-2 rounded-lg bg-cyan-500/20">
              <Calculator className="w-5 h-5 text-cyan-400" />
            </div>
            <h3 className="font-semibold text-white">Cost Breakdown</h3>
          </div>

          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Gross Value</span>
              <span className="text-white">
                {costs.currencySymbol}{costs.grossValue.toFixed(2)}
                {formData.market === "US" && (
                  <span className="text-slate-500 ml-1">(£{costs.grossValueGBP.toFixed(2)})</span>
                )}
              </span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Commission</span>
              <span className="text-white">£{costs.commission.toFixed(2)}</span>
            </div>
            {costs.stampDuty > 0 && (
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Stamp Duty (0.5%)</span>
                <span className="text-white">£{costs.stampDuty.toFixed(2)}</span>
              </div>
            )}
            <div className="pt-3 border-t border-slate-700">
              <div className="flex justify-between">
                <span className="font-medium text-white">Total Cost</span>
                <span className="font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-violet-400">
                  £{costs.totalCost.toFixed(2)}
                </span>
              </div>
            </div>
            {costs.initialStop > 0 && (
              <div className="pt-3 border-t border-slate-700">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Risk (to initial stop)</span>
                  <span className="text-rose-400 font-medium">£{costs.totalRisk.toFixed(2)}</span>
                </div>
              </div>
            )}
          </div>
        </motion.div>
      )}

      {/* Submit Button */}
      <div className="flex justify-end gap-3">
        <Link to={createPageUrl("Positions")}>
          <Button variant="ghost" className="text-slate-400 hover:text-white hover:bg-slate-800">
            Cancel
          </Button>
        </Link>
        <Button
          onClick={handleSubmit}
          disabled={!isFormValid || createMutation.isPending}
          className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 shadow-lg shadow-violet-500/25 disabled:opacity-50"
        >
          {createMutation.isPending ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Creating...
            </>
          ) : (
            <>
              <CheckCircle2 className="w-4 h-4 mr-2" />
              Create Position
            </>
          )}
        </Button>
      </div>
    </div>
  );
}
