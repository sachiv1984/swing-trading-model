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
// ST-09 (BLG-FE-264, EPIC-03, v9.16): title text-app-fg and subtitle
// text-app-muted (design_system.md v1.25 §Semantic Colour Tokens rule 5). The
// title is solid primary text; the gradient-clipped title it replaces could
// not be checked by axe color-contrast.
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
          <h1 className="text-2xl font-bold text-app-fg tracking-tight">
            {title}
          </h1>
          {description && (
            <p className="text-sm text-app-muted mt-1">{description}</p>
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
