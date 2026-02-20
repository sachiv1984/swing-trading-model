import { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { base44 } from "../api/base44Client";
import { motion } from "framer-motion";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import PageHeader from "../components/ui/PageHeader";
import { Save, Loader2, CheckCircle2, Sliders, CreditCard, Palette, TrendingUp } from "lucide-react";
import { toast } from "sonner";
import { cn } from "../lib/utils";

export default function Settings() {
  const queryClient = useQueryClient();
  const [formData, setFormData] = useState(null);
  const [saved, setSaved] = useState(false);
  const [fieldErrors, setFieldErrors] = useState({});  // DEF-004: inline field error state

  const { data: settings, isLoading } = useQuery({
    queryKey: ["settings"],
    queryFn: () => base44.entities.Settings.list(),
  });

  const defaults = {
    min_hold_days: 5,
    atr_multiplier_initial: 2,
    atr_multiplier_trailing: 3,
    atr_period: 14,
    default_risk_percent: 1.0,       // NEW — pre-populates position sizing calculator
    default_currency: "GBP",
    theme: "dark",
    uk_commission: 9.95,
    us_commission: 0,
    stamp_duty_rate: 0.005,
    fx_fee_rate: 0.0015,
    min_trades_for_analytics: 10,
  };

  // Dependency array is [settings] only — adding formData causes an infinite loop
  useEffect(() => {
    if (formData) return;

    if (settings?.[0]) {
      setFormData({ ...defaults, ...settings[0] });
    } else if (settings && settings.length === 0) {
      setFormData(defaults);
    }
  }, [settings]);

  const saveMutation = useMutation({
    mutationFn: async (data) => {
      if (data.id) {
        return base44.entities.Settings.update(data.id, data);
      } else {
        return base44.entities.Settings.create(data);
      }
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["settings"] });
      // Capture the id returned on first-time create so subsequent saves use update
      setFormData(prev => ({ ...prev, id: data.id }));
      setFieldErrors({});  // DEF-004: clear any previous field errors on successful save
      setSaved(true);
      toast.success("Settings saved successfully");
      setTimeout(() => setSaved(false), 2000);
    },
    // DEF-004: surface backend validation errors to the user
    onError: (error) => {
      const detail = error?.data?.detail;

      // Pydantic returns an array of validation errors — parse field-level messages
      if (Array.isArray(detail)) {
        const errors = {};
        detail.forEach((err) => {
          // loc is e.g. ["body", "default_risk_percent"] — take the last element as field name
          const field = err.loc?.[err.loc.length - 1];
          if (field) {
            errors[field] = err.msg?.replace("Value error, ", "") ?? "Invalid value";
          }
        });
        setFieldErrors(errors);
        toast.error("Please fix the errors below before saving");
      } else {
        // Fallback for non-Pydantic errors
        setFieldErrors({});
        toast.error(
          typeof detail === "string"
            ? detail
            : "Failed to save settings — please check your values and try again"
        );
      }
    },
  });

  const handleChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    // DEF-004: clear field error when user edits that field
    if (fieldErrors[field]) {
      setFieldErrors((prev) => ({ ...prev, [field]: undefined }));
    }
  };

  const handleSave = () => {
    saveMutation.mutate(formData);
  };

  if (isLoading || !formData) {
    return (
      <div className="flex items-center justify-center py-20">
        <Loader2 className="w-8 h-8 animate-spin text-slate-500" />
      </div>
    );
  }

  const SectionCard = ({ icon: Icon, title, iconColor, children }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 p-6"
    >
      <div className="flex items-center gap-3 mb-6">
        <div className={cn("p-2.5 rounded-xl", iconColor)}>
          <Icon className="w-5 h-5" />
        </div>
        <h3 className="font-semibold text-white">{title}</h3>
      </div>
      {children}
    </motion.div>
  );

  return (
    <div className="space-y-6 max-w-2xl mx-auto">
      <PageHeader
        title="Settings"
        description="Configure your strategy parameters and preferences"
        actions={
          <Button
            onClick={handleSave}
            disabled={saveMutation.isPending}
            className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 shadow-lg shadow-violet-500/25"
          >
            {saveMutation.isPending ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Saving...
              </>
            ) : saved ? (
              <>
                <CheckCircle2 className="w-4 h-4 mr-2" />
                Saved!
              </>
            ) : (
              <>
                <Save className="w-4 h-4 mr-2" />
                Save Settings
              </>
            )}
          </Button>
        }
      />

      {/* Strategy Parameters */}
      <SectionCard
        icon={Sliders}
        title="Strategy Parameters"
        iconColor="bg-cyan-500/20 text-cyan-400"
      >
        <div className="space-y-6">
          {/* Row 1 — ATR Period (solo, matching existing layout) */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label className="text-slate-400">Minimum Hold Days</Label>
              <Input
                type="number"
                value={formData.min_hold_days}
                onChange={(e) => handleChange("min_hold_days", parseInt(e.target.value))}
                className="bg-slate-800/50 border-slate-700 text-white"
              />
              <p className="text-xs text-slate-500">Days before stop can trail</p>
            </div>
            <div className="space-y-2">
              <Label className="text-slate-400">ATR Period</Label>
              <Input
                type="number"
                value={formData.atr_period}
                onChange={(e) => handleChange("atr_period", parseInt(e.target.value))}
                className="bg-slate-800/50 border-slate-700 text-white"
              />
              <p className="text-xs text-slate-500">Lookback for ATR calculation</p>
            </div>
          </div>

          {/* Row 2 — ATR Multipliers */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label className="text-slate-400">Initial Stop (ATR Multiple)</Label>
              <Input
                type="number"
                step="0.1"
                value={formData.atr_multiplier_initial}
                onChange={(e) => handleChange("atr_multiplier_initial", parseFloat(e.target.value))}
                className="bg-slate-800/50 border-slate-700 text-white"
              />
              <p className="text-xs text-slate-500">e.g., 5 = Entry − 5×ATR (wide stop for losing positions)</p>
            </div>
            <div className="space-y-2">
              <Label className="text-slate-400">Trailing Stop (ATR Multiple)</Label>
              <Input
                type="number"
                step="0.1"
                value={formData.atr_multiplier_trailing}
                onChange={(e) => handleChange("atr_multiplier_trailing", parseFloat(e.target.value))}
                className="bg-slate-800/50 border-slate-700 text-white"
              />
              <p className="text-xs text-slate-500">e.g., 2 = High − 2×ATR (tight trailing stop for profitable positions)</p>
            </div>
          </div>

          {/* Row 3 — Default Risk % */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label className="text-slate-400">Default Risk % Per Trade</Label>
              <Input
                type="number"
                step="0.1"
                min="0.01"
                max="100"
                value={formData.default_risk_percent}
                onChange={(e) => handleChange("default_risk_percent", parseFloat(e.target.value))}
                className={cn(
                  "bg-slate-800/50 border-slate-700 text-white",
                  fieldErrors.default_risk_percent && "border-red-500 focus:border-red-500"
                )}
              />
              {/* DEF-004: show inline error if backend rejected the value */}
              {fieldErrors.default_risk_percent ? (
                <p className="text-xs text-red-400">{fieldErrors.default_risk_percent}</p>
              ) : (
                <p className="text-xs text-slate-500">Pre-populates the position sizing calculator</p>
              )}
            </div>
          </div>
        </div>
      </SectionCard>

      {/* Commission & Fees */}
      <SectionCard
        icon={CreditCard}
        title="Commission & Fees"
        iconColor="bg-violet-500/20 text-violet-400"
      >
        <div className="space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label className="text-slate-400">UK Commission (£)</Label>
              <Input
                type="number"
                step="0.01"
                value={formData.uk_commission}
                onChange={(e) => handleChange("uk_commission", parseFloat(e.target.value))}
                className="bg-slate-800/50 border-slate-700 text-white"
              />
            </div>
            <div className="space-y-2">
              <Label className="text-slate-400">US Commission ($)</Label>
              <Input
                type="number"
                step="0.01"
                value={formData.us_commission}
                onChange={(e) => handleChange("us_commission", parseFloat(e.target.value))}
                className="bg-slate-800/50 border-slate-700 text-white"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label className="text-slate-400">UK Stamp Duty Rate</Label>
              <Input
                type="number"
                step="0.001"
                value={formData.stamp_duty_rate}
                onChange={(e) => handleChange("stamp_duty_rate", parseFloat(e.target.value))}
                className="bg-slate-800/50 border-slate-700 text-white"
              />
              <p className="text-xs text-slate-500">Default: 0.005 (0.5%)</p>
            </div>
            <div className="space-y-2">
              <Label className="text-slate-400">US FX Fee Rate</Label>
              <Input
                type="number"
                step="0.0001"
                value={formData.fx_fee_rate}
                onChange={(e) => handleChange("fx_fee_rate", parseFloat(e.target.value))}
                className="bg-slate-800/50 border-slate-700 text-white"
              />
              <p className="text-xs text-slate-500">Default: 0.0015 (0.15%)</p>
            </div>
          </div>
        </div>
      </SectionCard>

      {/* Preferences */}
      <SectionCard
        icon={Palette}
        title="Preferences"
        iconColor="bg-fuchsia-500/20 text-fuchsia-400"
      >
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label className="text-slate-400">Default Currency</Label>
            <Select
              value={formData.default_currency}
              onValueChange={(value) => handleChange("default_currency", value)}
            >
              <SelectTrigger className="bg-slate-800/50 border-slate-700 text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-slate-800 border-slate-700">
                <SelectItem value="GBP">GBP (£)</SelectItem>
                <SelectItem value="USD">USD ($)</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <Label className="text-slate-400">Theme</Label>
            <Select
              value={formData.theme}
              onValueChange={(value) => handleChange("theme", value)}
            >
              <SelectTrigger className="bg-slate-800/50 border-slate-700 text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-slate-800 border-slate-700">
                <SelectItem value="dark">Dark</SelectItem>
                <SelectItem value="light">Light</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </SectionCard>

      {/* Analytics */}
      <SectionCard
        icon={TrendingUp}
        title="Analytics"
        iconColor="bg-emerald-500/20 text-emerald-400"
      >
        <div className="space-y-2">
          <Label className="text-slate-400">Minimum Trades for Analytics</Label>
          <Input
            type="number"
            step="1"
            min="1"
            value={formData.min_trades_for_analytics || 10}
            onChange={(e) => handleChange("min_trades_for_analytics", parseInt(e.target.value))}
            className="bg-slate-800/50 border-slate-700 text-white"
          />
          <p className="text-xs text-slate-500">Minimum number of closed trades required to display analytics</p>
        </div>
      </SectionCard>
    </div>
  );
}
