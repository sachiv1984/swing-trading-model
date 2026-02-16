# design_system.md

## Overview
The Design System defines the shared visual language, interaction patterns, and reusable UI elements for the Position Manager Web App. Its purpose is to ensure consistency, clarity, and accessibility across all pages and components.

---

## Theme & Colors

### Theme Modes
- Default theme: **Dark Mode**
- Optional: **Light Mode toggle** available in the header
- Theme preference is persisted locally so the user’s choice is retained on reload

### Color Usage
The original specification does not define hex values, but design intent indicates consistent usage:

- **Profit and loss colors**  
  - Positive values use a green/positive tone  
  - Negative values use a red/negative tone  

- **Status indicators**  
  - GRACE, PROFITABLE, and LOSING badges have distinct colors to differentiate positions  
  - Tags appear as visually distinct colored pills  

- **Error colors**  
  - Inline errors and error banners use a strong, high‑contrast color to remain visible in dark mode

---

## Typography

No explicit font tokens are defined, but the system consistently uses clear hierarchy across:

- Page titles  
- Section headers  
- Card titles  
- Form labels  
- Data values  

Form labels use consistent patterns such as:
- Title case  
- Required vs optional noted explicitly (e.g., “Exit Note (Optional)”)  
- Inline helper text or character counters where applicable (journal notes)

---

## Spacing & Layout Principles

### Global Layout
The UI follows a consistent structure across pages:

- **Header** with navigation links and theme toggle  
- **Footer** with version and support links  
- **Mobile‑first layout**, adapting upward to larger screens  

### Responsive Behavior
The layout adapts at standard breakpoints:

- Tables collapse into card layouts on mobile  
- Sidebar-style navigation condenses into a mobile menu where applicable  
- Modals become full‑screen on smaller devices  
- Forms stack vertically on narrow viewports  

### Page Composition
Common layout elements include:
- Summary cards (Dashboard, Trade History)  
- Tables (Positions, Trade History)  
- Cards with expandable sections (Journal views)  

Consistent spacing ensures readability and clarity between sections.

---

## Shared UI Components

### Buttons
Buttons follow consistent conventions across pages:

- **Primary actions:**  
  “Enter New Position”, “Confirm Exit”, “Save”, “Daily Monitor”

- **Secondary actions:**  
  “Edit Note”, “Edit Tags”, “Go to Positions”

- **Critical/destructive actions:**  
  Exit flows trigger modals with clear confirmation steps

Buttons include:
- Hover states  
- Disabled states when validation fails  
- Clear loading/error handling where relevant  

### Tables
Used primarily for Positions and Trade History:

- Columns include values such as ticker, prices, P&L, tags, exit reason  
- Support expandable rows for journals  
- Collapse into cards on mobile  

### Cards
Cards appear across:
- Grid view of positions  
- Journal view (open and closed positions)  
- Expandable rows in trade history  

Cards support:
- Title area (ticker/market)  
- Metrics (P&L, dates)  
- Tag display  
- Expand/collapse interactions  

### Inputs & Form Controls
Common input types used across multiple pages:

- **Number inputs** (shares, prices, ATR, FX rate) with decimal rules  
- **Date pickers** (entry date, exit date, transaction date)  
- **Text areas** with character counters for journal notes  
- **Tag input** with autocomplete, pill rendering, and removal  
- **Radio buttons** (for deposit/withdrawal)  
- **Dropdowns** (exit reason selection)

All follow shared validation rules defined in the system.

---

## Interaction States

### Hover & Focus States
- Cards and expandable sections respond visually on hover  
- Buttons show hover and focus states  
- Form fields show focus outlines for accessibility  

### Disabled States
Used when:
- Required fields are incomplete (e.g., Exit Price, FX Rate)  
- Validation rules fail (e.g., insufficient funds, invalid date)  

### Loading States
Used during:
- API data retrieval (Dashboard, Positions, Trade History, Journal)  
- Form submissions (Position Entry, Exit Modal, Cash Management)

### Error States
Errors appear consistently as:
- **Global error banner** for major API failures  
- **Inline field errors** for form-specific issues  
- Contextual messages (e.g., “Insufficient funds”, “FX rate required”)

---

## Accessibility

The application adheres to core accessibility principles:

- Semantic HTML structure  
- Full keyboard navigation  
- Screen reader announcements for dynamic content  
- Color contrast meeting WCAG AA in dark mode  
- Focus trapping and restoration in modals  
- ARIA labels where needed (tables, buttons, inputs)  

---

## Consistency Rules

- Journal notes across the system share identical behaviors:
  - Optional  
  - Max 500 characters  
  - Character counter in editors  
  - Same inline editing pattern  

- Tag rules are consistent everywhere:
  - Lowercase only  
  - Hyphens and numbers allowed  
  - Max 20 characters per tag  
  - Max 10 tags per position  

- Forms across pages reuse consistent validation patterns:
  - Positive numeric values where appropriate  
  - Decimal place limits (e.g., shares, prices, FX rate)  
  - Date validity and ordering  
  - Error messages use consistent phrasing  

---

``
