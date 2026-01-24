import { motion } from "framer-motion";
import { GripVertical, X, Maximize2, Minimize2 } from "lucide-react";
import { Button } from "../ui/button";
import { cn } from "@/lib/utils";

export default function DashboardWidget({ 
  id,
  title, 
  children, 
  onRemove, 
  isEditing,
  size = "normal",
  dragHandleProps,
  className
}) {
  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      className={cn(
        "relative rounded-2xl bg-gradient-to-br from-slate-900/80 to-slate-800/80 dark:from-slate-900 dark:to-slate-800 border border-slate-700/50 overflow-hidden",
        "bg-white/80 dark:bg-transparent",
        isEditing && "ring-2 ring-cyan-500/50 ring-offset-2 ring-offset-slate-950",
        className
      )}
    >
      {isEditing && (
        <div className="absolute top-2 right-2 z-10 flex items-center gap-1">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onRemove(id)}
            className="h-7 w-7 bg-slate-800/80 hover:bg-rose-500/80 text-slate-400 hover:text-white"
          >
            <X className="w-4 h-4" />
          </Button>
        </div>
      )}
      
      {isEditing && (
        <div 
          {...dragHandleProps}
          className="absolute top-2 left-2 z-10 p-1.5 rounded-lg bg-slate-800/80 cursor-grab active:cursor-grabbing text-slate-400 hover:text-white"
        >
          <GripVertical className="w-4 h-4" />
        </div>
      )}
      
      {children}
    </motion.div>
  );
}
