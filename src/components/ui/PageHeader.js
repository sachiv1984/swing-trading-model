import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { ChevronLeft } from "lucide-react";
import OnwardLink from "./OnwardLink";

// `parent` (navigation.md v2.0 §Parent Links; ST-02, EPIC-01, v9.16,
// BLG-FE-251): pages without a sidebar entry pass { label, to } and get a
// left-chevron link to their parent above the heading. It does not replace
// any "Back" button, which depends on how the user arrived.
// `onward` (navigation.md v2.0 §Onward Links; ST-03, BLG-FE-252): { label, to }
// renders the page's required onward link under the description.
export default function PageHeader({ title, description, actions, parent, onward }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-8"
    >
      {parent && (
        <Link
          to={parent.to}
          data-testid="parent-link"
          className="inline-flex items-center gap-1 mb-2 text-sm font-medium text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white transition-colors print-hide"
        >
          <ChevronLeft className="w-4 h-4" aria-hidden="true" />
          {parent.label}
        </Link>
      )}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-slate-900 via-slate-700 to-slate-500 dark:from-white dark:via-slate-300 dark:to-slate-400 bg-clip-text text-transparent tracking-tight">
            {title}
          </h1>
          {description && (
            <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">{description}</p>
          )}
          {onward && (
            <div className="mt-2">
              <OnwardLink to={onward.to} label={onward.label} />
            </div>
          )}
        </div>
        {actions && (
          <div className="flex items-center gap-3 print-hide">
            {actions}
          </div>
        )}
      </div>
    </motion.div>
  );
}
