import type { Config } from "tailwindcss";
import typography from "@tailwindcss/typography";
import lineClamp from "@tailwindcss/line-clamp"; // The new plugin

const config: Config = {
  content: ["./src/**/*.{html,js,svelte,ts}"],
  theme: {
    extend: {
      colors: {
        background: "#1a1a1a",
        primary: "#f7f1e3",
        accent: "#c89b3c",
        "accent-hover": "#e6b34a",
      },
      fontFamily: {
        serif: ["Markazi Text", "serif"],
        sans: [
          "system-ui",
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "Roboto",
          "Helvetica Neue",
          "Arial",
          "sans-serif",
        ],
      },
    },
  },
  // Add the new plugin to the plugins array
  plugins: [typography, lineClamp],
};

export default config;
