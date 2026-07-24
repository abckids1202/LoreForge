/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#1f2328",
        parchment: "#f7f3eb",
        paper: "#fffdf8",
        line: "#ddd4c4",
        violet: "#6f42c1",
        ember: "#b85c38",
        teal: "#167c80",
        moss: "#56734d",
      },
      boxShadow: {
        soft: "0 18px 40px rgba(31, 35, 40, 0.08)",
      },
    },
  },
  plugins: [],
};
