import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import { Button } from "./button";

// ST-05 (EPIC-01, v9.6, BLG-FE-181): the single primary next-action for an empty state, passed
// to DataState's `emptyAction`. Rule (design_system.md v1.21 §Data States, decision_record.md
// §2.1): exactly one action, labelled "<Verb> <object>" (2-4 words, sentence case, no trailing
// period). Creation actions render as a button, navigation actions as a text link
// (decision_record.md §2.4). Provide `to` (route) or `onClick`.
// Design: docs/design/2026-09-21__release-v9.6/empty-state-next-action/decision_record.md
export default function EmptyStateAction({ to, onClick, variant = "link", disabled = false, children }) {
  if (variant === "button") {
    const cls = "bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0";
    return to ? (
      <Button asChild className={cls}>
        <Link to={to} data-testid="empty-state-action">{children}</Link>
      </Button>
    ) : (
      <Button onClick={onClick} disabled={disabled} className={cls} data-testid="empty-state-action">
        {children}
      </Button>
    );
  }
  return (
    <Link
      to={to}
      data-testid="empty-state-action"
      className="text-sm text-cyan-400 hover:text-cyan-300 underline underline-offset-2 transition-colors"
    >
      {children}
    </Link>
  );
}

EmptyStateAction.propTypes = {
  to: PropTypes.string,
  onClick: PropTypes.func,
  variant: PropTypes.oneOf(["link", "button"]),
  disabled: PropTypes.bool,
  children: PropTypes.node.isRequired,
};
