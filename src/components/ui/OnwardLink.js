import { Link } from "react-router-dom";
import { ArrowRight } from "lucide-react";
import { cn } from "../../lib/utils";

// Onward link (navigation.md v2.0 §Onward Links; ST-03, EPIC-01, v9.16,
// BLG-FE-252): an in-page link to the next page a user is likely to need,
// beyond the sidebar. Label is the target's canonical label (glossary §UI Labels).
export default function OnwardLink({ to, label, className, testId = "onward-link", onClick }) {
  return (
    <Link
      to={to}
      data-testid={testId}
      onClick={onClick}
      className={cn(
        "inline-flex items-center gap-1 text-sm font-medium text-cyan-700 hover:text-cyan-900 dark:text-cyan-400 dark:hover:text-cyan-300 transition-colors print-hide",
        className
      )}
    >
      {label}
      <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
    </Link>
  );
}
