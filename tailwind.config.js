/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    "./index.html",               // ← REQUIRED for Radix portals
    "./src/**/*.{js,jsx,ts,tsx}", // ← Your app components
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
