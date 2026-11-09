import { useEffect, useRef } from "react";
import { useSearchParams } from "react-router-dom";

// Section deep link (analytics.md §19.1; ST-04, EPIC-01, v9.16, BLG-FE-253;
// design: docs/design/2026-11-06__release-v9.16/digest-section-link/decision_record.md §2.2).
//
// When the page URL carries ?section=<id> matching this section, scroll the
// section into view ONCE, after `ready` first becomes true (the section has
// rendered with data, an error state or an empty state — never while it shows
// a skeleton). Smooth unless prefers-reduced-motion is set. Focus then moves to
// the section heading (tabIndex -1, no visible ring). If the user has already
// scrolled by then, do nothing. An unknown or missing section is ignored.
//
// Returns refs for the section wrapper and its heading.
export default function useSectionScroll(sectionId, ready) {
  const [searchParams] = useSearchParams();
  const requested = searchParams.get("section") === sectionId;
  const sectionRef = useRef(null);
  const headingRef = useRef(null);
  const done = useRef(false);
  const userScrolled = useRef(false);

  // Only user-initiated input counts as "the user scrolled": layout shifts
  // while other sections load also fire scroll events.
  useEffect(() => {
    if (!requested) return undefined;
    const SCROLL_KEYS = new Set(["ArrowUp", "ArrowDown", "PageUp", "PageDown", "Home", "End", " "]);
    const onPointer = () => { userScrolled.current = true; };
    const onKey = (e) => { if (SCROLL_KEYS.has(e.key)) userScrolled.current = true; };
    window.addEventListener("wheel", onPointer, { passive: true });
    window.addEventListener("touchmove", onPointer, { passive: true });
    window.addEventListener("keydown", onKey);
    return () => {
      window.removeEventListener("wheel", onPointer);
      window.removeEventListener("touchmove", onPointer);
      window.removeEventListener("keydown", onKey);
    };
  }, [requested]);

  useEffect(() => {
    if (!requested || !ready || done.current) return;
    done.current = true;
    if (userScrolled.current || !sectionRef.current) return;
    let reduceMotion = false;
    try {
      reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    } catch {
      reduceMotion = false;
    }
    sectionRef.current.scrollIntoView({ block: "start", behavior: reduceMotion ? "auto" : "smooth" });
    headingRef.current?.focus({ preventScroll: true });
  }, [requested, ready]);

  return { sectionRef, headingRef };
}
