---
title: Frontend Development Guide
description: Conventions, patterns, and workflow for frontend development without Base44
status: Living Document
created: 2026-03-21
---

# Frontend Development Guide

This document captures the patterns, conventions, and workflow established during active use of Base44 as a frontend scaffolding tool, and defines how Claude Code replicates and extends that role going forward.

---

## 1. Background: Base44 vs Claude Code

**Base44** was used as a rapid UI scaffolding tool — given a natural-language prompt, it would generate a complete React page or component following consistent visual conventions. It was particularly good at:

- Translating prose specs into working component structure
- Applying consistent Tailwind dark-theme styling without drift
- Separating concerns (page vs modal vs sub-component) instinctively

**Claude Code** handles the full delivery lifecycle: governance, backend, tests, and code review. The shift to Claude Code for frontend means:

- No context switch between tools
- Tighter integration with the backend API contracts
- Better understanding of cross-cutting concerns (routing, prefill patterns, existing component reuse)
- Ability to catch and fix issues Base44 missed (e.g. `fill_price` field dropped, `@/` alias that doesn't resolve, `DialogDescription` accessibility gap)

The trade-off is that Claude Code benefits from explicit pattern documentation — Base44 had its own baked-in conventions. This document is that substitute.

---

## 2. Project Structure

```
src/
  pages/              # One file per route page (e.g. Watchlist.js)
  components/
    ui/               # Shared primitives (Button, Input, Label, Dialog, etc.)
    <feature>/        # Feature-scoped components (e.g. watchlist/WatchlistModal.js)
  lib/
    utils.js          # cn() and other general helpers
  pages.config.js     # Route → component mapping (add new pages here)
  utils/index.js      # createPageUrl routes (add new routes here)
  Layout.js           # App shell: sidebar nav, theme toggle, mobile header
```

**When adding a new page:**
1. Create `src/pages/<PageName>.js`
2. Add import + entry to `src/pages.config.js`
3. Add route entry to `src/utils/index.js`
4. Add nav item to `src/Layout.js` `navItems` array (with correct icon)

---

## 3. Import Conventions

Always use **relative imports**. The project has no `@/` webpack alias.

```js
// ✅ Correct
import { Button } from "../components/ui/button";
import { cn } from "../../lib/utils";

// ❌ Wrong (Base44 convention — does not resolve here)
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
```

---

## 4. Visual Design System

### Colour palette

| Purpose | Dark mode | Light mode |
|---------|-----------|------------|
| Page background | `bg-slate-950` | `bg-slate-100` |
| Card / panel | `bg-slate-900` or `bg-gradient-to-br from-slate-900 to-slate-800` | `bg-white` |
| Border | `border-slate-700/50` | `border-slate-200` |
| Primary text | `text-white` | `text-slate-900` |
| Muted text | `text-slate-400` | `text-slate-600` |
| Label text | `text-slate-400 text-xs` | same |

### Primary action buttons

```jsx
className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 shadow-lg shadow-violet-500/25"
```

### Destructive action buttons

```jsx
className="bg-rose-600 hover:bg-rose-500 text-white border-0"
```

### Ghost / secondary buttons

```jsx
className="text-slate-400 hover:text-white hover:bg-slate-800"
```

### Status / tag badges (pill shape)

```jsx
<span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ...">
```

Status colour mappings:
- Success / active → `bg-emerald-500/20 text-emerald-400 border-emerald-500/30`
- Warning / watch → `bg-amber-500/20 text-amber-400 border-amber-500/30`
- Neutral / inactive → `bg-slate-700/50 text-slate-400 border-slate-600/30`
- UK market → `bg-blue-500/20 text-blue-400 border-blue-500/30`
- US market → `bg-violet-500/20 text-violet-400 border-violet-500/30`

### Cards / data panels

```jsx
<div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700/50 overflow-hidden">
```

### Input fields

```jsx
className="bg-slate-800/50 border-slate-700 text-white placeholder:text-slate-500 h-9"
```

---

## 5. Component Separation Principle

**Rule:** Extract into a separate component file any element that:
- Has its own local state
- Has a distinct lifecycle (open/close)
- Would make the parent file exceed ~200 lines

**Good examples from Base44:**
- `WatchlistModal.js` extracted from `Watchlist.js` — modal has its own form state, API calls, and confirm flow
- `SkeletonTable` / `EmptyState` as sub-components within a page file (small enough to keep co-located)

**Anti-pattern:** Embedding a full modal with API calls directly inside the page component.

---

## 6. Modal / Dialog Pattern

Use the unified modal state pattern:

```js
const [modal, setModal] = useState(null); // null | { mode, entry }

// Open add
setModal({ mode: "add" })

// Open edit
setModal({ mode: "edit", entry })

// Open edit with delete confirm pre-shown
setModal({ mode: "edit-confirm", entry })

// Close
setModal(null)
```

Modal component props convention:
```js
function FeatureModal({ mode, entry, onClose, onAdded, onUpdated, onDeleted })
```

Always include `DialogDescription` for accessibility even if visually invisible:
```jsx
<DialogDescription className="text-slate-400">
  {/* brief description of what the modal does */}
</DialogDescription>
```

---

## 7. List / Table State Patterns

### Row removal with fade-out animation

Use an object (not an array) to track in-flight removals — supports concurrent fades:

```js
const [removing, setRemoving] = useState({}); // { [id]: true }

const fadeOutAndRemove = (id) => {
  setRemoving((prev) => ({ ...prev, [id]: true }));
  setTimeout(() => {
    setEntries((prev) => prev.filter((e) => e.id !== id));
    setRemoving((prev) => {
      const next = { ...prev };
      delete next[id];
      return next;
    });
  }, 200);
};
```

Apply to row:
```jsx
<tr className={cn("transition-all duration-200", removing[entry.id] ? "opacity-0" : "opacity-100")}>
```

### Skeleton loader

Co-locate a `SkeletonTable` component in the page file for data-loading state:
```jsx
function SkeletonTable() {
  return (
    <div className="divide-y divide-slate-700/30">
      {Array.from({ length: 4 }).map((_, i) => (
        <div key={i} className="flex gap-6 px-5 py-4">
          <div className="h-4 w-16 bg-slate-700 rounded animate-pulse" />
          {/* ... */}
        </div>
      ))}
    </div>
  );
}
```

### Empty state

Co-locate an `EmptyState` component with a CTA:
```jsx
function EmptyState({ onAdd }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center px-6">
      <Eye className="w-12 h-12 text-slate-600 mb-4" />
      <h3 className="text-lg font-semibold text-white mb-2">...</h3>
      <p className="text-sm text-slate-400 mb-6">...</p>
      <Button onClick={onAdd} className="bg-gradient-to-r from-cyan-500 to-violet-500 ...">
        Add Item
      </Button>
    </div>
  );
}
```

---

## 8. API Fetch Pattern

```js
const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";
```

Use `useCallback` for fetch functions that appear in `useEffect` deps:

```js
const fetchEntries = useCallback(async () => {
  setLoadError(false);
  setLoading(true);
  try {
    const res = await fetch(`${API_BASE}/endpoint`);
    if (!res.ok) throw new Error();
    const json = await res.json();
    setData(json.data);
  } catch {
    setLoadError(true);
  } finally {
    setLoading(false);
  }
}, []);

useEffect(() => {
  fetchEntries();
}, [fetchEntries]);
```

All API responses follow `{ status: "ok", data: ... }` — always destructure `.data`.

**Conflict (409) handling** — surface inline, do not throw:
```js
if (res.status === 409) {
  setFieldError("This item already exists.");
  setSubmitting(false);
  return;
}
```

---

## 9. Navigation and Routing

### Navigate with state (prefill pattern)

```js
navigate("/TargetPage", {
  state: {
    feature_prefill: {
      id: entry.id,
      field1: entry.field1,
      field2: entry.field2,
    },
  },
});
```

### Read prefill in the target page

```js
const location = useLocation();
const prefill = location.state?.feature_prefill || null;

const [formData, setFormData] = useState({
  field1: prefill?.field1 || "",
  field2: prefill?.field2 || "",
});
```

### Fire-and-forget cleanup after success

```js
onSuccess: () => {
  if (prefill?.id) {
    fetch(`${API_BASE}/source-resource/${prefill.id}`, { method: "DELETE" })
      .catch(() => {})
      .finally(() => navigate(createPageUrl("DestinationPage")));
  } else {
    navigate(createPageUrl("DestinationPage"));
  }
}
```

---

## 10. Layout and Navigation Registration

### Adding a nav item

In `src/Layout.js`, add to the `navItems` array:
```js
{ name: "Display Name", icon: IconName, page: "PageName" },
```

**Icon selection** — prefer semantic icons:
- Dashboard → `LayoutDashboard`
- Positions → `Briefcase`
- Signals → `Zap`
- Watchlist → `Eye`
- Trade Entry → `PlusCircle`
- History → `History`
- Reports → `FileBarChart`
- Analytics → `TrendingUp`
- Risk → `ShieldAlert`
- System → `Activity`
- Notifications → `Bell`
- Settings → `Settings`

### isActive logic for grouped pages

When multiple pages share one nav highlight (e.g. Notifications + NotificationPreferences both highlight "Notifications"):

```js
const NOTIFICATIONS_PAGES = ["notifications", "NotificationPreferences"];
const isActive = (pageName) =>
  pageName === "notifications"
    ? NOTIFICATIONS_PAGES.includes(currentPageName)
    : currentPageName === pageName;
```

Do not simplify this — it handles the grouped-pages case.

---

## 11. Form Validation Patterns

- Ticker symbols: `/^[A-Z0-9.]{1,10}$/` — auto-uppercase on input
- Price fields: `type="number" step="0.01"` — treat empty string as `null` before sending to API
- Required field errors: set error state string, display below the field in `text-xs text-rose-400`
- Add `border-rose-500/60` to the input when there is an error

---

## 12. Sorting

Sort at read time, not render time. Return a new array (`[...arr].sort()`):

```js
function sortEntries(entries) {
  return [...entries].sort((a, b) => {
    const sigDiff = (ORDER[a.status] ?? 99) - (ORDER[b.status] ?? 99);
    if (sigDiff !== 0) return sigDiff;
    return a.ticker.localeCompare(b.ticker);
  });
}
```

Re-sort on add and on update:
```js
setEntries((prev) => sortEntries([...prev, newEntry]));
setEntries((prev) => sortEntries(prev.map((e) => (e.id === entry.id ? entry : e))));
```

---

## 13. Workflow: Frontend Stories Without Base44

1. **Read the API contract** — check `docs/specs/api_contracts/` for endpoint shapes and response formats before writing any fetch call.
2. **Check existing components** — look in `src/components/ui/` before adding new primitives.
3. **Write the page** — page file owns: state, fetch logic, sort/filter, event handlers. Keep it under ~250 lines.
4. **Extract modal/forms** — if the page has a create/edit/delete flow, extract it to `src/components/<feature>/FeatureModal.js`.
5. **Register the route** — update `pages.config.js`, `utils/index.js`, `Layout.js`.
6. **Preserve existing behaviour** — when touching shared files like `Layout.js` or `TradeEntry.js`, read the whole file first and identify what must be preserved (e.g. `fill_price` field, `NOTIFICATIONS_PAGES` isActive logic).
7. **Test the prefill flow** — if the page navigates to another page with state, verify the receiving page reads it correctly and cleans up on success.
