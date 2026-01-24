import { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { base44 } from "../api/base44Client";
import { motion } from "framer-motion";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import PageHeader from "../components/ui/PageHeader";
import { Settings as SettingsIcon, Save, Loader2, CheckCircle2, Sliders, CreditCard, Palette } from "lucide-react";
import { toast } from "sonner";
import { cn } from "@/lib/utils";

export default function Settings() {
  const queryClient = useQueryClient();
  const [formData, setFormData] = useState(null);
  const [saved, setSaved] = useState(false);

  const { data: settings, isLoading } = useQuery({
    queryKey: ["settings"],
    queryFn: () => base44.entities.Settings.list(),
  });

  useEffect(() => {
    if (settings?.[0]) {
      setFormData(settings[0]);
    } else if (settings && settings.length === 0) {
      setFormData({
        min_hold_days: 5,
        atr_multiplier_initial: 2,
        atr_multiplier_trailing: 3,
        atr_period: 14,
        default_currency: "GBP",
        theme: "dark",
        uk_commission: 9.95,
        us_commission: 0,
        stamp_duty_rate: 0.005,
      });
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
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["settings"] });
      setSaved(true);
      toast.success("Settings saved successfully");
      setTimeout(() => setSaved(false), 2000);
    },
  });

  const handleChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
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
              <p className="text-xs text-slate-500">e.g., 2 = Entry - 2×ATR</p>
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
              <p className="text-xs text-slate-500">e.g., 3 = High - 3×ATR</p>
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
 
