# analytics.md

## Purpose & User Goals
The Analytics page provides users with deeper insights into portfolio performance, risk, and trading behavior.  
While not heavily detailed in the original requirements, its purpose is consistent with the broader system:

- Help users understand trends in their trading outcomes  
- Highlight performance drivers (e.g., winning vs losing trades)  
- Support long‑term strategy refinement  
- Provide visual summaries beyond raw trade history data  

This page complements the Dashboard (short‑term view) and Trade History (detailed past trades) by offering a higher‑level analytical perspective.

---

## Layout Structure

### Summary Metrics
A set of top‑level analytics that may include:
- Total closed trades  
- Average holding period  
- Average R/R (if calculated)  
- Win rate and loss rate  
- P&L distribution summary  

These values help ground the user before exploring more detailed analytics.

---

### Performance Charts
Possible analytics visualizations include:
- **Equity curve** — cumulative P&L over time  
- **Distribution charts** — histogram of trade returns  
- **Market regime impact** — performance grouped by market signals  
- **Tag‑based performance** — comparing strategy tags over time  
  - Useful for identifying which strategies work best  

Charts should be easy to visually parse and should highlight trends, not noise.

---

### Filters & Segmentation
Filters similar to Trade History may be available:

- Date range selector  
- Tag filters  
- Market filters (US / UK)  
- Exit reason (optional)  
- Time grouping (weekly, monthly, quarterly)

The goal is to allow the user to explore "Why?" behind their performance.

---

### Insights Section (Optional but Recommended)
Text or metric‑based insights may summarize:

- Best and worst performing tags  
- Performance clusters (e.g., profitable months)  
- Common patterns in losing trades  
- Any unusual outliers  

This section helps convert raw data into actionable understanding.

---

## Key Components Used
- Summary metric cards  
- Line, bar, or distribution charts  
- Filters (tags, date range, market)  
- Tag pills  
- Card layouts for insights or breakdowns  

---

## States

### Loading State
- Chart placeholders  
- Skeleton metric cards  

### Empty State
Appears when:
- No closed trades exist  
- Filters produce no data  

Displays:
- A simple message indicating insufficient data for analytics  

### Error State
- Global error banner when analytics data fails to load  
- Retry action available  

---

## Responsive Behavior
- Charts scale responsively, shrinking or stacking vertically  
- Filters collapse into a vertical stack on mobile  
- Metric cards reorganize into a 1‑ or 2‑column layout  
- Insight cards become full‑width  

---

## UX Notes
- Analytics should never overwhelm the user — prioritize clarity over complexity  
- Use visual grouping and consistent color usage across charts  
- Tag‑based analytics should mirror tag visuals from Trade History and Positions  
- Avoid requiring users to interpret unfamiliar financial metrics  
- Emphasize practical insights that connect back to user actions (e.g., position entries/exits, journaling patterns)  

---

``
