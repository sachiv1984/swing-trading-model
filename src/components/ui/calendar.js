import * as React from "react"
import { ChevronLeft, ChevronRight } from "lucide-react"
import { DayPicker } from "react-day-picker"

import { cn } from "../../lib/utils"
import { buttonVariants } from "../ui/button"

// ST-17 (EPIC-05, v7.10, BLG-FE-122): rewritten against react-day-picker
// v9+'s API (v10.0.1 installed — see package.json). The classNames map and
// icon override below previously used the pre-v9 API (`caption`, `table`,
// `head_row`, `head_cell`, `nav_button_previous`, `day_selected`, etc., and
// separate `IconLeft`/`IconRight` component overrides) — none of these keys
// or components exist in the installed v9+ library, so this component would
// not have rendered correctly against it. Renamed per v9+'s `UI`/`DayFlag`/
// `SelectionState` enums (node_modules/react-day-picker/dist/esm/UI.d.ts):
//   caption -> month_caption, table -> month_grid, head_row -> weekdays,
//   head_cell -> weekday, row -> week, nav_button_previous -> button_previous,
//   nav_button_next -> button_next, day -> day_button (the cell itself is now
//   `day`), day_selected -> selected, day_today -> today, day_outside ->
//   outside, day_disabled -> disabled, day_range_middle -> range_middle,
//   day_range_start/end -> range_start/end, day_hidden -> hidden.
// v9+ also merges the day cell and its selection-state modifiers onto one
// element (the cell itself gets `data-selected`/`data-today`/etc. plus the
// combined classNames), so the old `[&:has([aria-selected])]` parent-selector
// workarounds are no longer needed — the day cell's own modifier classes
// (`selected`, `today`, `outside`, ...) apply directly.
function Calendar({
  className,
  classNames,
  showOutsideDays = true,
  ...props
}) {
  return (
    (<DayPicker
      showOutsideDays={showOutsideDays}
      className={cn("p-3", className)}
      classNames={{
        months: "flex flex-col sm:flex-row space-y-4 sm:space-x-4 sm:space-y-0",
        month: "space-y-4",
        month_caption: "flex justify-center pt-1 relative items-center",
        caption_label: "text-sm font-medium",
        nav: "space-x-1 flex items-center",
        button_previous: cn(
          buttonVariants({ variant: "outline" }),
          "h-7 w-7 bg-transparent p-0 opacity-50 hover:opacity-100 absolute left-1"
        ),
        button_next: cn(
          buttonVariants({ variant: "outline" }),
          "h-7 w-7 bg-transparent p-0 opacity-50 hover:opacity-100 absolute right-1"
        ),
        month_grid: "w-full border-collapse space-y-1",
        weekdays: "flex",
        weekday:
          "text-muted-foreground rounded-md w-8 font-normal text-[0.8rem]",
        week: "flex w-full mt-2",
        day: cn(
          "relative p-0 text-center text-sm focus-within:relative focus-within:z-20",
          props.mode === "range"
            ? "[&:has(>.range-end)]:rounded-r-md [&:has(>.range-start)]:rounded-l-md first:[&:has(.selected)]:rounded-l-md last:[&:has(.selected)]:rounded-r-md"
            : "[&:has(.selected)]:rounded-md"
        ),
        day_button: cn(
          buttonVariants({ variant: "ghost" }),
          "h-8 w-8 p-0 font-normal"
        ),
        range_start: "range-start bg-accent rounded-l-md",
        range_end: "range-end bg-accent rounded-r-md",
        selected:
          "selected bg-primary text-primary-foreground hover:bg-primary hover:text-primary-foreground focus:bg-primary focus:text-primary-foreground rounded-md",
        today: "bg-accent text-accent-foreground rounded-md",
        outside: "text-muted-foreground opacity-50",
        disabled: "text-muted-foreground opacity-50",
        range_middle:
          "range-middle bg-accent text-accent-foreground",
        hidden: "invisible",
        chevron: "h-4 w-4",
        ...classNames,
      }}
      components={{
        Chevron: ({ className, orientation, ...props }) =>
          orientation === "right" ? (
            <ChevronRight className={cn("h-4 w-4", className)} {...props} />
          ) : (
            <ChevronLeft className={cn("h-4 w-4", className)} {...props} />
          ),
      }}
      {...props} />)
  );
}
Calendar.displayName = "Calendar"

export { Calendar }
