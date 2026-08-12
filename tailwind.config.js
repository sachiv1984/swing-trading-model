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
        // already-canonical token, no new visual design decision.
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        // ST-04 (BLG-FE-147, EPIC-03, v8.6): the remaining shadcn tokens
        // defined in src/index.css but never registered here -- same root
        // cause as the -muted gap above (v8.5/ST-06), broader scope. Every
        // `bg-card`/`text-card-foreground`/`bg-popover`/`text-primary`/
        // `bg-secondary`/`bg-accent`/`bg-destructive`/`border-border`/
        // `bg-input`/`ring-ring` (and their sibling utility forms --
        // border-, text-, fill-, stroke-, ring- variants actually in use,
        // per src/ grep) compiled to an empty rule until now. Design
        // Pre-Approved (design_gate.md) -- restores already-canonical
        // tokens, no new visual design decision.
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))',
        },
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
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
