import { useCallback, useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Search } from "lucide-react";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "../components/ui/tabs";
import PageHeader from "../components/ui/PageHeader";
import { Input } from "../components/ui/input";
import { PAGE_LABELS } from "../lib/pageLabels";
import { cn } from "../lib/utils";
import { journalSection, redFlagTicker } from "../lib/journalFilter";
import ReflectionsSection from "../components/journal/ReflectionsSection";
import RedFlagsSection from "../components/journal/RedFlagsSection";
import PositionNotesSection from "../components/journal/PositionNotesSection";

// Journal (journal.md v1.1; ST-05, BLG-FE-258, EPIC-02, v9.17): one page for
// trade reflections, rule red flags and position notes. ?section= picks the
// tab and ?ticker= holds the shared ticker filter; both use replace
// navigation, so switching tabs or typing adds no history entries. A section
// fetches only when its tab is first opened, then stays mounted (hidden) so
// its own filters and data survive tab switches. The filter box keeps its text
// in local state and copies it to ?ticker=: react-router 7 applies location
// updates inside startTransition, which cannot drive a controlled input. No AI-generated text and no
// /ai/* call on this page (journal.md §6, §8).

const SECTIONS = [
  { value: "reflections", label: "Reflections" },
  { value: "red-flags", label: "Red flags" },
  { value: "notes", label: "Position notes" },
];

const RED_FLAG_DEBOUNCE_MS = 300;

export default function Journal() {
  const [searchParams, setSearchParams] = useSearchParams();
  const section = journalSection(searchParams.get("section"));
  const urlTicker = searchParams.get("ticker") || "";
  const [ticker, setTicker] = useState(urlTicker);
  // Values this page wrote to ?ticker= and has not yet seen come back. A URL
  // value not in this set came from outside (a link, Back), so the box adopts it.
  const pendingWrites = useRef(new Set());

  const [opened, setOpened] = useState(() => new Set([section]));
  const [counts, setCounts] = useState({});
  // Red flags is filtered by the server: it gets the ticker 300 ms after
  // typing stops, or at once on Enter (journal.md §3).
  const [redFlagFilter, setRedFlagFilter] = useState(() => redFlagTicker(ticker));

  useEffect(() => {
    setOpened((prev) => (prev.has(section) ? prev : new Set(prev).add(section)));
  }, [section]);

  useEffect(() => {
    if (pendingWrites.current.has(urlTicker)) {
      pendingWrites.current.delete(urlTicker);
      return;
    }
    pendingWrites.current.clear();
    setTicker(urlTicker);
  }, [urlTicker]);

  useEffect(() => {
    const next = redFlagTicker(ticker);
    if (next === redFlagFilter) return undefined;
    const timer = setTimeout(() => setRedFlagFilter(next), RED_FLAG_DEBOUNCE_MS);
    return () => clearTimeout(timer);
  }, [ticker, redFlagFilter]);

  const updateParam = useCallback(
    (key, value) => {
      setSearchParams(
        (prev) => {
          const next = new URLSearchParams(prev);
          if (value) next.set(key, value);
          else next.delete(key);
          return next;
        },
        { replace: true }
      );
    },
    [setSearchParams]
  );

  const changeTicker = useCallback(
    (value) => {
      setTicker(value);
      pendingWrites.current.add(value);
      updateParam("ticker", value);
    },
    [updateParam]
  );

  const clearTicker = useCallback(() => {
    changeTicker("");
    setRedFlagFilter("");
  }, [changeTicker]);

  const countSetters = {
    reflections: useCallback((n) => setCounts((c) => ({ ...c, reflections: n })), []),
    "red-flags": useCallback((n) => setCounts((c) => ({ ...c, "red-flags": n })), []),
    notes: useCallback((n) => setCounts((c) => ({ ...c, notes: n })), []),
  };

  return (
    <div className="space-y-6 min-w-0">
      <PageHeader
        title={PAGE_LABELS.Journal}
        description="Your reflections, rule red flags and position notes in one place."
      />

      <Tabs
        value={section}
        onValueChange={(value) => updateParam("section", value)}
        activationMode="automatic"
        className="space-y-4"
      >
        <TabsList
          aria-label="Journal sections"
          data-testid="journal-tabs"
          className="flex h-auto w-full max-w-full justify-start overflow-x-auto gap-1 rounded-xl border border-app-line bg-app-raised p-1 sm:w-auto sm:inline-flex"
        >
          {SECTIONS.map(({ value, label }) => {
            const count = counts[value];
            return (
              <TabsTrigger
                key={value}
                value={value}
                data-testid={`journal-tab-${value}`}
                className={cn(
                  "shrink-0 rounded-lg px-3 py-1.5 text-app-muted hover:text-app-fg",
                  "data-[state=active]:bg-app-surface data-[state=active]:text-app-fg",
                  "focus-visible:ring-cyan-500 focus-visible:ring-offset-0"
                )}
              >
                {label}
                {opened.has(value) && typeof count === "number" && (
                  <span data-testid={`journal-tab-count-${value}`}> ({count})</span>
                )}
              </TabsTrigger>
            );
          })}
        </TabsList>

        <div className="relative w-full sm:max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" aria-hidden="true" />
          <Input
            data-testid="journal-ticker-filter"
            aria-label="Filter by ticker"
            value={ticker}
            onChange={(e) => changeTicker(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") setRedFlagFilter(redFlagTicker(e.currentTarget.value));
            }}
            placeholder="Filter by ticker…"
            className="bg-app-raised border-app-line text-app-fg placeholder:text-app-muted pl-10"
          />
        </div>

        {SECTIONS.map(({ value }) => (
          <TabsContent
            key={value}
            value={value}
            forceMount
            data-testid={`journal-panel-${value}`}
            className="mt-0 data-[state=inactive]:hidden"
          >
            {opened.has(value) && value === "reflections" && (
              <ReflectionsSection ticker={ticker} onCount={countSetters.reflections} onClearFilter={clearTicker} />
            )}
            {opened.has(value) && value === "red-flags" && (
              <RedFlagsSection ticker={redFlagFilter} onCount={countSetters["red-flags"]} onClearTicker={clearTicker} />
            )}
            {opened.has(value) && value === "notes" && (
              <PositionNotesSection ticker={ticker} onCount={countSetters.notes} onClearTicker={clearTicker} />
            )}
          </TabsContent>
        ))}
      </Tabs>
    </div>
  );
}
