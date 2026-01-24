import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

export function DataTable({ children, className }) {
  return (
    <div className={cn(
      "rounded-2xl border border-slate-700/50 bg-gradient-to-br from-slate-900 to-slate-800 backdrop-blur-sm overflow-hidden",
      className
    )}>
      <div className="overflow-x-auto">
        <table className="w-full">
          {children}
        </table>
      </div>
    </div>
  );
}

export function TableHeader({ children }) {
  return (
    <thead className="bg-slate-800/50 border-b border-slate-700/50">
      <tr>{children}</tr>
    </thead>
  );
}

export function TableHead({ children, className }) {
  return (
    <th className={cn(
      "px-6 py-4 text-left text-xs font-medium text-slate-400 uppercase tracking-wider",
      className
    )}>
      {children}
    </th>
  );
}

export function TableBody({ children }) {
  return <tbody className="divide-y divide-slate-700/30">{children}</tbody>;
}

export function TableRow({ children, className, onClick }) {
  return (
    <motion.tr
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className={cn(
        "hover:bg-slate-800/30 transition-colors",
        onClick && "cursor-pointer",
        className
      )}
      onClick={onClick}
    >
      {children}
    </motion.tr>
  );
}

export function TableCell({ children, className }) {
  return (
    <td className={cn("px-6 py-4 text-sm text-slate-300", className)}>
      {children}
    </td>
  );
}
