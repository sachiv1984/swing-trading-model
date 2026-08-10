/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    "./public/index.html",           // <-- REQUIRED for Radix portals
    "./src/**/*.{js,jsx,ts,tsx}",    // <-- your components
  ],
  theme: {
    extend: {
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        // ST-06 (BLG-FE-145, EPIC-03, v8.5): `--muted`/`--muted-foreground` are
        // defined in src/index.css but were never registered here, so every
        // `-muted` utility class (text-muted-foreground, bg-muted,
        // border-muted, fill-muted, fill-muted-foreground) compiled to an
        // empty rule -- Tailwind only generates utilities for color tokens it
        // knows about. Design Pre-Approved (design_gate.md) -- restores an
        // already-canonical token, no new visual design decision. Scoped to
        // -muted per this story's AC; other similarly-unregistered shadcn
        // tokens (card, popover, primary, secondary, accent, destructive,
        // border, input, ring) are a separate, broader gap -- filed as
        // BLG-FE-146, out of this story's scope.
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        // (all your Base44 extended colors here)
      },
      keyframes: {
        'accordion-down': {
          from: { height: '0' },
          to:   { height: 'var(--radix-accordion-content-height)' },
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to:   { height: '0' },
        },
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
        'fade-in': 'fade-in 0.2s ease-out',
      },
    },
  },
  plugins: [
    require("tailwindcss-animate"),
  ],
}
