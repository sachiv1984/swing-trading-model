import { useState } from "react";
import { motion } from "framer-motion";
import { TrendingUp, TrendingDown, Edit2, LogOut } from "lucide-react";
import { Button } from "../ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "../ui/dialog";
import { cn } from "../../lib/utils";
import { differenceInDays } from "date-fns";

export default function PositionCard({ position, onEdit, onExit }) {
  const [showNoteModal, setShowNoteModal] = useState(false);
  const pnl = position.pnl || 0;
  const pnlPercent = position.pnl_percent || 0;
  const isProfit = pnl >= 0;
  const daysHeld = differenceInDays(new Date(), new Date(position.entry_date));
  const currencySymbol = position.market === "UK" ? "£" : "$";
  
  // Use native prices for display
  const displayCurrentPrice = position.current_price_native || position.current_price;
  const displayStopPrice = position.stop_price_native || position.stop_price;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn(
        "relative overflow-hidden rounded-2xl border p-5 transition-all",
        "bg-gradient-to-br from-slate-900 to-slate-800 backdrop-blur-sm",
        "border-slate-700/50 hover:border-slate-600/50"
      )}
    >
      <div className="flex items-start justify-between mb-4">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-lg font-bold text-white">{position.ticker}</h3>
            <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
              {position.market}
            </span>
          </div>
          <p className="text-sm text-slate-500 mt-1">
            {daysHeld} days held • {position.shares} shares
          </p>
        </div>
        <div className={cn(
          "flex items-center gap-1.5 px-3 py-1.5 rounded-xl",
          isProfit ? "bg-emerald-500/20" : "bg-rose-500/20"
        )}>
          {isProfit ? (
            <TrendingUp className="w-4 h-4 text-emerald-400" />
          ) : (
            <TrendingDown className="w-4 h-4 text-rose-400" />
          )}
          <span className={cn(
            "text-sm font-semibold",
            isProfit ? "text-emerald-400" : "text-rose-400"
          )}>
            {isProfit ? "+" : ""}{pnlPercent.toFixed(2)}%
          </span>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4 mb-4">
        <div className="p-3 rounded-xl bg-slate-800/50">
          <p className="text-xs text-slate-500 mb-1">Entry</p>
          <p className="text-sm font-semibold text-white">
            {currencySymbol}{position.entry_price.toFixed(2)}
          </p>
        </div>
        <div className="p-3 rounded-xl bg-slate-800/50">
          <p className="text-xs text-slate-500 mb-1">Current</p>
          <p className="text-sm font-semibold text-white">
            {currencySymbol}{displayCurrentPrice?.toFixed(2) || "—"}
          </p>
        </div>
        <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20">
          <p className="text-xs text-slate-500 mb-1">Stop</p>
          <p className="text-sm font-semibold text-rose-400">
            {currencySymbol}{displayStopPrice?.toFixed(2) || "—"}
          </p>
        </div>
      </div>

      {/* Note & Tags Preview */}
      {(position.entry_note || position.tags?.length > 0) && (
        <div className="mb-4 p-3 rounded-xl bg-slate-800/30 border border-slate-700/30">
          {position.entry_note && (
            <button
              onClick={() => setShowNoteModal(true)}
              className="w-full text-left mb-2 text-sm text-slate-400 italic hover:text-slate-300 transition-colors"
            >
              {position.entry_note.length > 80 
                ? `${position.entry_note.substring(0, 80)}...` 
                : position.entry_note}
            </button>
          )}
          {position.tags?.length > 0 && (
            <div className="flex flex-wrap gap-1.5">
              {position.tags.slice(0, 3).map((tag) => (
                <span
                  key={tag}
                  className="px-2 py-0.5 text-xs rounded-full bg-cyan-500/20 text-cyan-400 border border-cyan-500/30"
                >
                  {tag}
                </span>
              ))}
              {position.tags.length > 3 && (
                <span className="px-2 py-0.5 text-xs text-slate-500">
                  +{position.tags.length - 3} more
                </span>
              )}
            </div>
          )}
        </div>
      )}

      <div className="flex items-center gap-2 pt-4 border-t border-slate-700/50">
        <Button
          variant="ghost"
          size="sm"
          className="flex-1 text-slate-400 hover:text-white hover:bg-slate-800"
          onClick={() => onEdit(position)}
        >
          <Edit2 className="w-4 h-4 mr-2" />
          Edit
        </Button>
        <Button
          variant="ghost"
          size="sm"
          className="flex-1 text-rose-400 hover:text-rose-300 hover:bg-rose-500/10"
          onClick={() => onExit(position)}
        >
          <LogOut className="w-4 h-4 mr-2" />
          Exit
        </Button>
      </div>
      
      {/* Subtle glow */}
      <div className={cn(
        "absolute -bottom-10 -right-10 w-32 h-32 rounded-full blur-3xl opacity-20",
        isProfit ? "bg-emerald-500" : "bg-rose-500"
      )} />

      {/* Note Modal */}
      <Dialog open={showNoteModal} onOpenChange={setShowNoteModal}>
        <DialogContent className="bg-slate-900 border-slate-700 text-white max-w-md">
          <DialogHeader>
            <DialogTitle className="text-cyan-400">Trade Entry Note</DialogTitle>
          </DialogHeader>
          <div className="py-4">
            <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">
              {position.entry_note}
            </p>
            {position.tags?.length > 0 && (
              <div className="mt-4 pt-4 border-t border-slate-700/50">
                <p className="text-xs text-slate-500 mb-2">Tags:</p>
                <div className="flex flex-wrap gap-2">
                  {position.tags.map((tag) => (
                    <span
                      key={tag}
                      className="px-2 py-1 text-xs rounded-full bg-cyan-500/20 text-cyan-400 border border-cyan-500/30"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </motion.div>
  );
}
