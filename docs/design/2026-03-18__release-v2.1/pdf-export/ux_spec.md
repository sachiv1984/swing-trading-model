**Owner:** Head of UX & Design
**Status:** Approved
**Approved by:** Product Owner
**Approved date:** 2026-03-18
**Cycle:** 2026-03-18__release-v2.1
**Items:** ST-12 (BLG-FR-01)
**Frontend spec target:** docs/specs/frontend/pages/reports.md (update — v0.1 → v0.2)

---

# UX Spec — Tax Year P&L PDF Export (ST-12)

## 1. Purpose & User Goal

The user wants a portable, print-consistent record of their tax year P&L — one they can attach to their personal records or share with an accountant. The current browser-print path is inconsistent across browsers.

**User goal:** Download a well-formatted PDF of the current tax year P&L report in one click.

---

## 2. Placement

The PDF export button lives in the **page header**, right-aligned, alongside (or just below) the year selector.

**Suggested layout order (left to right):**
```
[Year Selector ▼]                    [Download PDF]
```

On narrow screens: stacked vertically — year selector above, Download PDF button below (full width).

---

## 3. Button Specification

| Property | Value |
|----------|-------|
| Label | **"Download PDF"** |
| Icon | Download arrow icon (left of label) — optional; use design system convention |
| Style | Secondary button (not primary — the primary action on this page is selecting the year) |
| Position | Page header, right-aligned |

---

## 4. Button States

### 4.1 Default (idle)
- Label: **"Download PDF"**
- Enabled when: the page has loaded successfully and `trades[]` may be empty or populated (the PDF is valid for empty years too — it records absence of trades).

### 4.2 Generating (loading)
- Triggered immediately on click.
- Label changes to: **"Generating…"** with a small spinner replacing the download icon.
- Button is disabled while generating (prevent double-click).
- Duration: typically 1–5 seconds for server-side generation; button re-enables on completion or error.

### 4.3 Success
- The browser receives the PDF as a file download (Content-Disposition: attachment).
- Button returns to idle state after the download begins.
- No success toast required — the file download dialog is sufficient feedback.

### 4.4 Error
- If the API returns an error during PDF generation:
  - Button returns to idle state.
  - A toast notification appears: **"PDF generation failed. Please try again."** (auto-dismiss after 5s).

---

## 5. Interaction Flow

```
User clicks "Download PDF"
→ Button → "Generating…" (disabled)
→ GET /reports/tax-year?format=pdf&year=YYYY request sent
→ On success: browser file download begins → button → idle
→ On error: button → idle + error toast
```

---

## 6. Content (for reference — backend concern, not frontend decision)

The PDF content is determined by the backend. The frontend does not control PDF content. For reference:
- Report title: "Tax Year P&L — [tax_year_label]"
- Generation timestamp (UTC)
- Summary bar values
- Trades table (all rows for the selected year)
- Disclaimer text (same as the page disclaimer)

---

## 7. Relationship to Existing Browser Print

The existing browser-print path (if any) may remain as a fallback but is not prominently surfaced. The "Download PDF" button is the canonical export action going forward.

---

## 8. UX Decisions Recorded

| Decision | Rationale |
|----------|-----------|
| Secondary button style (not primary) | Year selection is the primary page action; PDF export is secondary |
| Header placement (not per-section) | The entire page is a single report; a single header-level export is the correct scope |
| "Generating…" state on button (not page spinner) | Scoped feedback prevents the page from feeling locked; user can read the report while generating |
| No success toast | Browser download dialog provides sufficient confirmation; double-toasting would be noise |
| Error toast (not inline) | PDF generation failure is not tied to a specific page element; a page-level toast is appropriate |
| PDF enabled for empty year | An empty tax year is a valid state — zero trades is a meaningful record |
