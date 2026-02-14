import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "../ui/dialog";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { Textarea } from "../ui/textarea";
import { format, differenceInDays } from "date-fns";
import { BookOpen, Edit2, X } from "lucide-react";
import { cn } from "../../lib/utils";
import { useQuery } from "@tanstack/react-query";
import { base44 } from "../../api/base44Client";

export default function PositionModal({ position, open, onClose, onSave }) {
  const [formData, setFormData] = useState({
    current_price: "",
    stop_price: ""
  });

  const [journalEdit, setJournalEdit] = useState(false);
  const [journalData, setJournalData] = useState({
    entry_note: "",
    tags: []
  });
  const [tagInput, setTagInput] = useState("");
  const [showTagSuggestions, setShowTagSuggestions] = useState(false);

  const { data: existingTags = [] } = useQuery({
    queryKey: ["position-tags"],
    queryFn: async () => {
      const positions = await base44.entities.Position.list();
      const allTags = positions.flatMap(p => p.tags || []);
      return [...new Set(allTags)].sort();
    },
  });

  // ✅ FIXED: Initialize with native prices
  useEffect(() => {
    if (position) {
      setFormData({
        current_price: position.current_price_native || position.current_price || "",
        stop_price: position.stop_price_native || position.stop_price || ""
      });
      setJournalData({
        entry_note: position.entry_note || "",
        tags: position.tags || []
      });
      setJournalEdit(false);
    }
  }, [position]);

  if (!position) return null;

  // ✅ FIXED: Calculate P&L using native prices consistently
  const currentPriceNative = parseFloat(formData.current_price) || 0;
  const entryPriceNative = position.entry_price || 0;  // entry_price is already in native currency
  const shares = position.shares || 0;

  const pnl = (currentPriceNative - entryPriceNative) * shares;
  const pnlPercent = entryPriceNative > 0 ? ((currentPriceNative - entryPriceNative) / entryPriceNative * 100) : 0;
  const isProfit = pnl >= 0;
  const daysHeld = differenceInDays(new Date(), new Date(position.entry_date));
  const currencySymbol = position.market === "UK" ? "£" : "$";

  const defaultTags = ["momentum", "breakout", "pullback", "news-driven", "high-conviction"];
  const allAvailableTags = [...new Set([...existingTags, ...defaultTags])];

  const filteredTags = tagInput
    ? allAvailableTags.filter(tag => 
        tag.toLowerCase().includes(tagInput.toLowerCase()) &&
        !journalData.tags.includes(tag)
      )
    : allAvailableTags.filter(tag => !journalData.tags.includes(tag));

  const handleAddTag = (tag) => {
    if (journalData.tags.length >= 5) return;
    const normalizedTag = tag.toLowerCase().replace(/\s+/g, "-");
    if (!journalData.tags.includes(normalizedTag)) {
      setJournalData(prev => ({ ...prev, tags: [...prev.tags, normalizedTag] }));
    }
    setTagInput("");
    setShowTagSuggestions(false);
  };

  const handleRemoveTag = (tagToRemove) => {
    setJournalData(prev => ({
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

  const handleSave = () => {
    // Convert native prices back to GBP for backend if needed
    let currentPriceForSave = parseFloat(formData.current_price);
    let stopPriceForSave = parseFloat(formData.stop_price);
    
    // If US stock, convert from USD to GBP
    if (position.market === "US" && position.live_fx_rate) {
      currentPriceForSave = currentPriceForSave / position.live_fx_rate;
      stopPriceForSave = stopPriceForSave / position.live_fx_rate;
    }
    
    onSave({
      ...position,
      current_price: currentPriceForSave,
      stop_price: stopPriceForSave,
      entry_note: journalData.entry_note || null,
      tags: journalData.tags.length > 0 ? journalData.tags : null
    });
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      {/* ✅ FIXED: Use grid instead of flex for proper scrolling */}
      <DialogContent className="bg-slate-900 border-slate-700 text-white max-w-lg max-h-[90vh] grid grid-rows-[auto_1fr_auto]">
        {/* Row 1: Header (auto height) */}
        <DialogHeader>
          <DialogTitle className="flex items-center gap-3">
            <span className="text-xl font-bold">{position.ticker}</span>
            <span className="text-xs px-2 py-1 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
              {position.market}
            </span>
          </DialogTitle>
        </DialogHeader>

        {/* Row 2: Scrollable content (1fr = takes available space) */}
        <div className="space-y-6 py-4 overflow-y-auto min-h-0">
          {/* Summary Stats */}
          <div className="grid grid-cols-3 gap-3">
            <div className="p-3 rounded-xl bg-slate-800/50 border border-slate-700/50">
              <p className="text-xs text-slate-500 mb-1">Days Held</p>
              <p className="text-lg font-semibold text-white">{daysHeld}</p>
            </div>
            <div className="p-3 rounded-xl bg-slate-800/50 border border-slate-700/50">
              <p className="text-xs text-slate-500 mb-1">Shares</p>
              <p className="text-lg font-semibold text-white">{shares}</p>
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
                {isProfit ? "+" : ""}{currencySymbol}{Math.abs(pnl).toFixed(2)}
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
                <p className="text-sm text-white">{currencySymbol}{entryPriceNative.toFixed(2)}</p>
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

          {/* Trade Journal */}
          <div className="p-4 rounded-xl bg-slate-800/30 border border-slate-700/50 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-cyan-400" />
                <h4 className="text-sm font-medium text-slate-400">Trade Journal</h4>
              </div>
              {!journalEdit && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setJournalEdit(true)}
                  className="h-8 text-slate-400 hover:text-white hover:bg-slate-800"
                >
                  <Edit2 className="w-3 h-3 mr-1" />
                  Edit
                </Button>
              )}
            </div>

            {!journalEdit ? (
              <div className="space-y-3">
                {journalData.entry_note ? (
                  <div className="p-3 rounded-lg bg-slate-800/50 border border-slate-700/30">
                    <p className="text-sm text-slate-300 whitespace-pre-wrap">{journalData.entry_note}</p>
                  </div>
                ) : (
                  <p className="text-sm text-slate-500 italic">No entry note</p>
                )}

                {journalData.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1.5">
                    {journalData.tags.map((tag) => (
                      <span
                        key={tag}
                        className="px-2 py-1 text-xs rounded-full bg-cyan-500/20 text-cyan-400 border border-cyan-500/30"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              <div className="space-y-3">
                {/* Edit Note */}
                <div className="space-y-2">
                  <Label className="text-slate-400 text-xs">Entry Note</Label>
                  <Textarea
                    value={journalData.entry_note}
                    onChange={(e) => {
                      if (e.target.value.length <= 500) {
                        setJournalData(prev => ({ ...prev, entry_note: e.target.value }));
                      }
                    }}
                    placeholder="Why are you entering this trade? What's your thesis?"
                    className="bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-500 focus:border-cyan-500/50 resize-none"
                    rows={4}
                  />
                  <div className="flex justify-end">
                    <span className={cn(
                      "text-xs",
                      journalData.entry_note.length > 450 ? "text-rose-400" : "text-slate-500"
                    )}>
                      {journalData.entry_note.length}/500
                    </span>
                  </div>
                </div>

                {/* Edit Tags */}
                <div className="space-y-2">
                  <Label className="text-slate-400 text-xs">Tags</Label>
                  {journalData.tags.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {journalData.tags.map((tag) => (
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

                  {journalData.tags.length < 5 && (
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
                        className="bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-500 focus:border-cyan-500/50"
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
                </div>

                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => {
                    setJournalEdit(false);
                    setJournalData({
                      entry_note: position.entry_note || "",
                      tags: position.tags || []
                    });
                  }}
                  className="text-slate-400 hover:text-white hover:bg-slate-800"
                >
                  Cancel
                </Button>
              </div>
            )}
          </div>

          {/* Editable Fields */}
          <div className="space-y-4">
            <div className="space-y-2">
              <Label className="text-slate-400">Current Price ({currencySymbol})</Label>
              <Input
                type="number"
                step="0.01"
                value={formData.current_price}
                onChange={(e) => setFormData({ ...formData, current_price: e.target.value })}
                className="bg-slate-800/50 border-slate-700 text-white focus:border-cyan-500/50"
              />
            </div>
            <div className="space-y-2">
              <Label className="text-slate-400">Stop Price ({currencySymbol}) - Manual Override</Label>
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

        {/* Row 3: Footer (auto height) */}
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
