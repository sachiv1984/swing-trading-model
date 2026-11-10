import { motion } from "framer-motion";
import { cn } from "../../lib/utils";

// ST-09 (BLG-FE-264, EPIC-03, v9.16): the table shell uses the semantic colour
// tokens (design_system.md v1.25 §Semantic Colour Tokens rule 5): container
// app-raised/app-line, header cells app-muted, body cells app-fg, dividers
// app-line. Fills that need an alpha (header band, row hover) keep explicit
// light/dark pairs, since tokens take no opacity modifier (rule 2).

export function DataTable({ children, className }) {
  return (
    <div className={cn(
      "rounded-2xl border border-app-line bg-app-raised backdrop-blur-sm overflow-hidden",
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
    <thead className="bg-slate-50 dark:bg-slate-800/50 border-b border-app-line">
      <tr>{children}</tr>
    </thead>
  );
}

export function TableHead({ children, className, ...props }) {
  return (
    <th className={cn(
      "px-6 py-4 text-left text-xs font-medium text-app-muted uppercase tracking-wider",
      className
    )} {...props}>
      {children}
    </th>
  );
}

export function TableBody({ children }) {
  return <tbody className="divide-y divide-app-line">{children}</tbody>;
}

export function TableRow({ children, className, onClick, ...rest }) {
  return (
    <motion.tr
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className={cn(
        "hover:bg-slate-50 dark:hover:bg-slate-800/30 transition-colors",
        onClick && "cursor-pointer",
        className
      )}
      onClick={onClick}
      {...rest}
    >
      {children}
    </motion.tr>
  );
}

export function TableCell({ children, className, colSpan }) {
  return (
    <td className={cn("px-6 py-4 text-sm text-app-fg", className)} colSpan={colSpan}>
      {children}
    </td>
  );
}
