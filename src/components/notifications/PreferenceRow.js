import { Switch } from "../ui/switch";
import { cn } from "../../lib/utils";
import { motion, AnimatePresence } from "framer-motion";

export default function PreferenceRow({ label, description, enabled, saved, error, onToggle }) {
  return (
    <div className="px-6 py-5">
      <div className="flex items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <span className="text-sm font-medium text-white">{label}</span>
            <AnimatePresence>
              {saved && (
                <motion.span
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="text-xs text-emerald-400"
                >
                  Saved
                </motion.span>
              )}
            </AnimatePresence>
          </div>
          <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">{description}</p>
        </div>
        <Switch
          checked={enabled}
          onCheckedChange={onToggle}
          className="data-[state=checked]:bg-cyan-500"
        />
      </div>
      {error && (
        <p className="mt-2 text-xs text-rose-700 dark:text-rose-400">{error}</p>
      )}
    </div>
  );
}
