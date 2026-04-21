/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          black: "#0D0D12",
          surface: "#16161E",
          purple: "#7C3AED",
          neon: "#10B981",
          gray: "#94A3B8"
        }
      }
    },
  },
  plugins: [],
}