import { createContext, useCallback, useContext, useLayoutEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { foldedItems, isFolded } from "../../../lib/quietDay";

// Quiet-day collapse (dashboard.md v4.4 §3A; ST-09, BLG-UX-11, v9.18). Each
// foldable element reports whether it is folded; the page renders the
// "Nothing to show: …" line from those reports and hides the containers whose
// elements have all folded. Elements stay mounted while folded, so their
// queries keep running and a later Refresh can unfold them.

const QuietDayContext = createContext(null);

export function QuietDayProvider({ children }) {
  const [folded, setFolded] = useState(() => new Set());
  const [revealed, setRevealed] = useState(() => new Set());

  const report = useCallback((key, isFoldedNow) => {
    setFolded((prev) => {
      if (prev.has(key) === isFoldedNow) return prev;
      const next = new Set(prev);
      if (isFoldedNow) next.add(key);
      else next.delete(key);
      return next;
    });
  }, []);

  // A disclosure entry reveals its card for the rest of the visit (not persisted).
  const toggleReveal = useCallback((key) => {
    setRevealed((prev) => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  }, []);

  const value = useMemo(() => ({ folded, revealed, report, toggleReveal }), [folded, revealed, report, toggleReveal]);
  return <QuietDayContext.Provider value={value}>{children}</QuietDayContext.Provider>;
}

export function useQuietDay() {
  return useContext(QuietDayContext);
}

// Reports this element's fold state and returns true when it should not render.
// Outside a provider (any page other than the Dashboard) nothing folds.
export function useQuietDayFold(foldKey, state) {
  const ctx = useContext(QuietDayContext);
  const foldedNow = Boolean(foldKey) && isFolded(state);
  const report = ctx?.report;
  // A layout effect, so the page's containers and line update before paint
  // (no empty panel flashes when cached data folds a card on its first render);
  // the cleanup removes the key when the element unmounts.
  useLayoutEffect(() => {
    if (!report || !foldKey) return undefined;
    report(foldKey, foldedNow);
    return () => report(foldKey, false);
  }, [report, foldKey, foldedNow]);
  if (!ctx || !foldKey) return false;
  return foldedNow && !ctx.revealed.has(foldKey);
}

export function NothingToShowLine() {
  const ctx = useQuietDay();
  if (!ctx) return null;
  const items = foldedItems(ctx.folded, ctx.revealed);
  if (items.length === 0) return null;
  return (
    <p className="text-sm text-app-muted" data-testid="dashboard-nothing-to-show">
      Nothing to show:{" "}
      {items.map((item, i) => (
        <span key={item.key}>
          {i > 0 && " · "}
          {item.disclosure ? (
            <button
              type="button"
              aria-expanded={ctx.revealed.has(item.key)}
              // Only while expanded, so it never names an id that is not rendered.
              aria-controls={ctx.revealed.has(item.key) ? `dashboard-${item.key}` : undefined}
              onClick={() => ctx.toggleReveal(item.key)}
              className="text-app-fg underline-offset-2 hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-500 rounded-sm"
              data-testid={`nothing-to-show-${item.key}`}
            >
              {item.name}
            </button>
          ) : (
            <Link
              to={item.to}
              className="text-app-fg underline-offset-2 hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-500 rounded-sm"
              data-testid={`nothing-to-show-${item.key}`}
            >
              {item.name}
            </Link>
          )}
        </span>
      ))}
    </p>
  );
}
