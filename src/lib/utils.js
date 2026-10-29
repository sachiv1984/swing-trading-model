import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"

// ST-25 (BLG-FE-221, v9.13): twMerge drops a conflicting earlier utility, so a
// caller's className (e.g. a Button's bg-emerald-700) replaces the variant's
// default (bg-primary) instead of depending on CSS order.
export function cn(...inputs) {
  return twMerge(clsx(inputs))
}
