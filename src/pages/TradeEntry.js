import { useState } from "react";
import { useMutation, useQueryClient, useQuery } from "@tanstack/react-query";
import { base44 } from "../api/base44Client";
import { useNavigate } from "react-router-dom";
import { createPageUrl } from "../utils";
import { motion } from "framer-motion";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Textarea } from "../components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import PageHeader from "../components/ui/PageHeader";
import { ArrowLeft, Calculator, Loader2, CheckCircle2, X } from "lucide-react";
import { Link } from "react-router-dom";
import { cn } from "../lib/utils";
import PositionSizingWidget from '../components/trades/PositionSizingWidget';

export default function TradeEntry() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [formData, setFormData] = useState({
    ticker: "",
    market: "UK",
    entry_date: new Date().toISOString().split("T")[0],
    shares: "",
    entry_price: "",
    stop_price: "",
    fx_rate: "1",
    atr_value: "",
    entry_note: "",
    tags: [],
  });

  const [tagInput, setTagInput] = useState("");
  const [showTagSuggestions, setShowTagSuggestions] = useState(false);

  const { data: settings } = useQuery({
    queryKey: ["settings"],
    queryFn: () => base44.entities.Settings.list(),
  });

  const { data: existingTags = [] } = useQuery({
    queryKey: ["position-tags"],
    queryFn: async () => {
      const positions = await base44.entities.Position.list();
      const allTags = positions.flatMap(p => p.tags || []);
      return [...new Set(allTags)].sort();
    },
  });

  const currentSettings = settings?.[0] || {
    atr_multiplier_initial: 2,
    uk_commission: 9.95,
    us_commission: 0,
    stamp_duty_rate: 0.005,
    fx_fee_rate: 0.0015,
  };

  // Read default_risk_percent from settings for PositionSizingWidget
  const defaultRiskPercent = settings?.[0]?.default_risk_percent ?? 1.0;

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

  const defaultTags = ["momentum", "breakout", "pullback", "news-driven", "high-conviction"];
  const allAvailableTags = [...new Set([...existingTags, ...defaultTags])];

  const filteredTags = tagInput
    ? allAvailableTags.filter(tag =>
        tag.toLowerCase().includes(tagInput.toLowerCase()) &&
        !formData.tags.includes(tag)
      )
    : allAvailableTags.filter(tag => !formData.tags.includes(tag));

  const handleAddTag = (tag) => {
    if (formData.tags.length >= 5) return;
    const normalizedTag = tag.toLowerCase().replace(/\s+/g, "-");
    if (!formData.tags.includes(normalizedTag)) {
      setFormData(prev => ({ ...prev, tags: [...prev.tags, normalizedTag] }));
    }
    setTagInput("");
    setShowTagSuggestions(false);
  };

  const handleRemoveTag = (tagToRemove) => {
    setFormData(prev => ({
      ...prev,
      tags: prev.tags.filter(tag => tag !== tagToRemove)
    }));
  };

  const handleTagInputKeyDown = (e) => {
    if (e.key === "Enter" && tagInput.trim()) {
      e.preventDefault();
      handleAddTag(tagInput.trim());
    }
  };

  // ─────────────────────────────────────────────────────────────────────────────
  // Cost preview — client-side estimate for display only.
  // These values are NOT passed to the backend on submission.
  // Authoritative fee and stop calculations are performed server-side by
  // POST /portfolio/position per strategy_rules.md §4.1.
  // ─────────────────────────────────────────────────────────────────────────────
  const estimateCosts = () => {
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

    const fxFee = formData.market === "US"
      ? grossValueGBP * (currentSettings.fx_fee_rate || 0.0015)
      : 0;

    const totalCost = grossValueGBP + commission + stampDuty + fxFee;

    // ATR-derived stop hint — shown as a suggestion in the UI only
    const suggestedStop = atr > 0 ? price - (atr * currentSettings.atr_multiplier_initial) : 0;

    // Risk calculation uses the user's manually entered stop_price if set,
    // otherwise falls back to the ATR-derived suggestion
    const effectiveStop = parseFloat(formData.stop_price) || suggestedStop;
    const riskPerShare = effectiveStop > 0 ? price - effectiveStop : 0;
    const totalRisk = riskPerShare * shares;
    const totalRiskGBP = formData.market === "US" ? totalRisk / fxRate : totalRisk;

    return {
      grossValue,
      grossValueGBP,
      commission,
      stampDuty,
      fxFee,
      totalCost,
      suggestedStop,
      riskPerShare,
      totalRisk: totalRiskGBP,
      currencySymbol: formData.market === "UK" ? "£" : "$",
    };
  };

  const costs = estimateCosts();
  const isFormValid = formData.ticker && formData.shares && formData.entry_price;

  const handleSubmit = () => {
    if (!isFormValid) return;

    // Note: fees are NOT passed here — the backend calculates authoritative fees
    // via POST /portfolio/position. stop_price uses the user's manual input.
    createMutation.mutate({
      ticker: formData.ticker,
      market: formData.market,
      entry_date: formData.entry_date,
      shares: parseFloat(formData.shares),
      entry_price: parseFloat(formData.entry_price),
      current_price: parseFloat(formData.entry_price),
      fx_rate: parseFloat(formData.fx_rate),
      atr_value: parseFloat(formData.atr_value) || null,
      stop_price: parseFloat(formData.stop_price) || null,
      status: "open",
      entry_note: formData.entry_note || null,
      tags: formData.tags.length > 0 ? formData.tags : null,
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

          {/* Entry Price */}
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

          {/* FX Rate (US only) */}
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

          {/* ATR & Stop Price */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label className="text-slate-400">ATR Value (Optional)</Label>
              <Input
                type="number"
                step="0.01"
                value={formData.atr_value}
                onChange={(e) => handleChange("atr_value", e.target.value)}
                placeholder="For stop suggestion"
                className="bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-500"
              />
              {formData.atr_value && costs.suggestedStop > 0 && (
                <p className="text-xs text-slate-500">
                  Suggested stop:{" "}
                  <span className="text-rose-400">
                    {costs.currencySymbol}{costs.suggestedStop.toFixed(2)}
                  </span>{" "}
                  ({currentSettings.atr_multiplier_initial}× ATR)
                </p>
              )}
            </div>
            <div className="space-y-2">
              <Label className="text-slate-400">Stop Price ({costs.currencySymbol})</Label>
              <Input
                type="number"
                step="0.01"
                value={formData.stop_price}
                onChange={(e) => handleChange("stop_price", e.target.value)}
                placeholder="0.00"
                className="bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-500"
              />
            </div>
          </div>

          {/* Position Sizing Widget — calls POST /portfolio/size, backend-authoritative */}
          <Positionsizingwidget
            entryPrice={parseFloat(formData.entry_price) || null}
            stopPrice={parseFloat(formData.stop_price) || null}
            market={formData.market}
            fxRate={parseFloat(formData.fx_rate) || null}
            shares={formData.shares}
            onSharesChange={(val) => handleChange("shares", val)}
            defaultRiskPercent={defaultRiskPercent}
          />

          {/* Shares */}
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

          {/* Entry Note */}
          <div className="space-y-2">
            <Label className="text-slate-400">Entry Note (Optional)</Label>
            <Textarea
              value={formData.entry_note}
              onChange={(e) => {
                if (e.target.value.length <= 500) {
                  handleChange("entry_note", e.target.value);
                }
              }}
              placeholder="Why are you entering this trade? What's your thesis?"
              className="bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-500 focus:border-cyan-500/50 focus:ring-cyan-500/20 resize-none"
              rows={4}
            />
            <div className="flex justify-end">
              <span className={cn(
                "text-xs",
                formData.entry_note.length > 450 ? "text-rose-400" : "text-slate-500"
              )}>
                {formData.entry_note.length}/500
              </span>
            </div>
          </div>

          {/* Tags */}
          <div className="space-y-2">
            <Label className="text-slate-400">Tags (Optional)</Label>
            <div className="space-y-2">
              {formData.tags.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {formData.tags.map((tag) => (
                    <span
                      key={tag}
                      className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium bg-cyan-500/20 text-cyan-400 border border-cyan-500/30"
                    >
                      {tag}
                      <button
                        onClick={() => handleRemoveTag(tag)}
                        className="hover:text-cyan-300 transition-colors"
                      >
                        <X className="w-3 h-3" />
                      </button>
                    </span>
                  ))}
                </div>
              )}

              {formData.tags.length < 5 && (
                <div className="relative">
                  <Input
                    value={tagInput}
                    onChange={(e) => {
                      setTagInput(e.target.value);
                      setShowTagSuggestions(e.target.value.length > 0);
                    }}
                    onFocus={() => setShowTagSuggestions(true)}
                    onBlur={() => setTimeout(() => setShowTagSuggestions(false), 200)}
                    onKeyDown={handleTagInputKeyDown}
                    placeholder="Type to add tags..."
                    className="bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-500 focus:border-cyan-500/50 focus:ring-cyan-500/20"
                  />
                  {showTagSuggestions && filteredTags.length > 0 && (
                    <div className="absolute z-10 w-full mt-1 bg-slate-800 border border-slate-700 rounded-lg shadow-xl max-h-48 overflow-auto">
                      {filteredTags.slice(0, 10).map((tag) => (
                        <button
                          key={tag}
                          onClick={() => handleAddTag(tag)}
                          className="w-full px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-700 hover:text-white transition-colors"
                        >
                          {tag}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {formData.tags.length >= 5 && (
                <p className="text-xs text-slate-500">Maximum 5 tags reached</p>
              )}
            </div>
          </div>
        </div>
      </motion.div>

      {/* Cost Preview — client-side estimate only. Actual fees calculated server-side. */}
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
            <h3 className="font-semibold text-white">Estimated Cost</h3>
            <span className="text-xs text-slate-500 ml-1">(preview — actual fees calculated on submission)</span>
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
            {costs.fxFee > 0 && (
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">FX Fee (0.15%)</span>
                <span className="text-white">£{costs.fxFee.toFixed(2)}</span>
              </div>
            )}
            <div className="pt-3 border-t border-slate-700">
              <div className="flex justify-between">
                <span className="font-medium text-white">Est. Total Cost</span>
                <span className="font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-violet-400">
                  £{costs.totalCost.toFixed(2)}
                </span>
              </div>
            </div>
            {costs.riskPerShare > 0 && (
              <div className="pt-3 border-t border-slate-700">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Risk (to stop)</span>
                  <span className="text-rose-400 font-medium">£{costs.totalRisk.toFixed(2)}</span>
                </div>
              </div>
            )}
          </div>
        </motion.div>
      )}

      {/* Submit */}
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
