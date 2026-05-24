/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        pixel: ['"Press Start 2P"', "monospace"],
        display: ['"VT323"', "monospace"],
      },
      colors: {
        cozy: {
          bg: "#0a0e15",
          panel: "rgba(12, 17, 24, 0.78)",
          border: "rgba(70, 90, 120, 0.45)",
          accent: "#f5d068",
          accentDim: "#b89548",
          cream: "#f7eccd",
          mute: "#8a8275",
        },
      },
      animation: {
        bob: "bob 1.4s ease-in-out infinite",
        "fade-in": "fadeIn 0.3s ease-out",
        "slide-up": "slideUp 0.4s ease-out",
        shimmer: "shimmer 4s ease-in-out infinite",
      },
      keyframes: {
        bob: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-2px)" },
        },
        fadeIn: {
          from: { opacity: "0" },
          to: { opacity: "1" },
        },
        slideUp: {
          from: { opacity: "0", transform: "translateY(8px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        shimmer: {
          "0%, 100%": { opacity: "0.6" },
          "50%": { opacity: "1" },
        },
      },
    },
  },
  plugins: [],
};
