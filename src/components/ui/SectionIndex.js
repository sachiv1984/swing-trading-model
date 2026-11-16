import { useCallback, useEffect, useRef, useState } from "react";
import { useHref, useLocation, useSearchParams } from "react-router-dom";
import { cn } from "../../lib/utils";

// In-page section index (long-page-section-index decision record §2;
// trade_plan.md §5g, strategy_benchmark.md §3a; ST-07, BLG-FE-263, EPIC-02,
// v9.17; reused by ST-06's Performance page).
//
// `sections` lists only the sections that render right now ([{ id, label }]).
// Each section's wrapper carries `id={id}` and SECTION_SCROLL_MARGIN so its
// heading is not hidden under the sticky row or the fixed mobile header.
// A link jumps instantly (no smooth scroll, so no reduced-motion branch),
// moves focus to the section's first heading and sets ?section={id} with a
// replace navigation. The router uses hash routing, so anchors use
// ?section=, never a second "#". Loading with ?section={id} jumps there once
// that section has rendered and the page says its content is `ready` (so
// late data does not shift the section away after the jump); an unknown id
// does nothing.
//
// Current section: the one whose heading most recently crossed the top
// quarter. A section near the end of the page cannot scroll that high, so
// after a jump that leaves the page at its end, the jumped-to section stays
// current until the user scrolls away from the end (implementation note,
// ST-07: otherwise "Checklist" would mark "What-if sizing" after a jump).
// Each link's href is the real hash-router URL with ?section=, so a
// middle-click, "Open in new tab" or a copied link opens the section.

export const SECTION_SCROLL_MARGIN = "scroll-mt-36 lg:scroll-mt-4";
// Strategy Benchmark keeps its year/market filter bar sticky at the top of the
// content column (about 56 px), so its sections clear that too at lg.
export const SECTION_SCROLL_MARGIN_UNDER_STICKY_BAR = "scroll-mt-36 lg:scroll-mt-20";

function atPageEnd() {
  return Math.ceil(window.scrollY + window.innerHeight) >= document.documentElement.scrollHeight - 2;
}

// The section whose top most recently crossed the top quarter of the
// viewport: the last one (in page order) whose top is at or above that line,
// or the first section when none has crossed it yet.
export function currentSectionId(tops, viewportHeight) {
  if (!tops.length) return null;
  const line = viewportHeight * 0.25;
  let current = tops[0].id;
  for (const { id, top } of tops) {
    if (top <= line) current = id;
  }
  return current;
}

function jumpTo(id) {
  const section = document.getElementById(id);
  if (!section) return false;
  const heading = section.querySelector("h1, h2, h3, h4") || section;
  if (!heading.hasAttribute("tabindex")) heading.setAttribute("tabindex", "-1");
  section.scrollIntoView({ block: "start" });
  heading.focus({ preventScroll: true });
  return true;
}

export default function SectionIndex({ sections, ariaLabel = "On this page", className, ready = true }) {
  const [searchParams, setSearchParams] = useSearchParams();
  const requested = searchParams.get("section");
  const [current, setCurrent] = useState(sections[0]?.id ?? null);
  const jumpedFor = useRef(null);
  const pinned = useRef(null);
  const idsKey = sections.map((s) => s.id).join("|");

  // ?section= on load: jump once the section exists. A later change to the
  // param made by this component (a click) has already jumped.
  useEffect(() => {
    if (!ready || !requested || jumpedFor.current === requested) return;
    if (!sections.some((s) => s.id === requested)) return;
    if (jumpTo(requested)) {
      jumpedFor.current = requested;
      pinned.current = atPageEnd() ? requested : null;
      setCurrent(requested);
    }
  }, [requested, idsKey, ready]); // eslint-disable-line react-hooks/exhaustive-deps

  // Current section from IntersectionObserver: no scroll listener, no timer.
  // Runs after every render but reconnects only when the section elements
  // themselves change (same ids, new nodes after a remount included).
  const observed = useRef({ nodes: [], observer: null });
  useEffect(() => {
    const nodes = sections.map((s) => document.getElementById(s.id)).filter(Boolean);
    const prev = observed.current;
    if (nodes.length === prev.nodes.length && nodes.every((n, i) => n === prev.nodes[i])) return;
    prev.observer?.disconnect();
    observed.current = { nodes, observer: null };
    if (!nodes.length || typeof IntersectionObserver === "undefined") return;
    const recompute = () => {
      if (pinned.current) {
        if (atPageEnd()) return;
        pinned.current = null;
      }
      const tops = nodes.map((el) => ({ id: el.id, top: el.getBoundingClientRect().top }));
      setCurrent(currentSectionId(tops, window.innerHeight));
    };
    const observer = new IntersectionObserver(recompute, {
      rootMargin: "0px 0px -75% 0px",
      threshold: [0, 1],
    });
    nodes.forEach((el) => observer.observe(el));
    observed.current.observer = observer;
    recompute();
  });
  useEffect(() => () => observed.current.observer?.disconnect(), []);

  const onClick = useCallback(
    (e, id) => {
      e.preventDefault();
      jumpedFor.current = id;
      jumpTo(id);
      pinned.current = atPageEnd() ? id : null;
      setCurrent(id);
      setSearchParams(
        (prev) => {
          const next = new URLSearchParams(prev);
          next.set("section", id);
          return next;
        },
        { replace: true }
      );
    },
    [setSearchParams]
  );

  const location = useLocation();
  const baseHref = useHref({ pathname: location.pathname });
  const hrefFor = (id) => {
    const params = new URLSearchParams(searchParams);
    params.set("section", id);
    return `${baseHref}?${params.toString()}`;
  };

  if (!sections.length) return null;

  return (
    <nav
      aria-label={ariaLabel}
      data-testid="section-index"
      className={cn(
        "print-hide z-20 min-w-0",
        // Below lg: one sticky row under the fixed mobile header, scrolling
        // sideways inside itself.
        "sticky top-16 -mx-4 px-4 py-2 bg-slate-100/95 dark:bg-slate-950/95 backdrop-blur-sm",
        // lg and up: a sticky 12rem column beside the content.
        "lg:top-4 lg:mx-0 lg:px-0 lg:py-0 lg:bg-transparent lg:dark:bg-transparent lg:backdrop-blur-none lg:self-start lg:w-48",
        className
      )}
    >
      <p className="hidden lg:block mb-2 text-xs font-semibold uppercase tracking-wide text-app-muted">
        {ariaLabel}
      </p>
      <ul className="flex gap-2 overflow-x-auto lg:flex-col lg:gap-0.5 lg:overflow-visible">
        {sections.map(({ id, label }) => {
          const active = current === id;
          return (
            <li key={id} className="shrink-0">
              <a
                href={hrefFor(id)}
                data-testid={`section-link-${id}`}
                aria-current={active ? "true" : undefined}
                onClick={(e) => onClick(e, id)}
                className={cn(
                  "flex items-center whitespace-nowrap text-sm transition-colors",
                  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-500",
                  // Pill, 44 px tall, below lg
                  "min-h-[44px] rounded-full border border-app-line bg-app-raised px-4",
                  // Plain link with a left border at lg
                  "lg:min-h-0 lg:rounded-none lg:border-0 lg:border-l-2 lg:border-transparent lg:bg-transparent lg:px-3 lg:py-1",
                  active
                    ? "font-medium text-app-fg border-cyan-600 dark:border-cyan-400 lg:border-cyan-600 lg:dark:border-cyan-400"
                    : "text-app-muted hover:text-app-fg"
                )}
              >
                {label}
              </a>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
