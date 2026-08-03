/* ============================================================================
 * tailwind.desyk.js — config para Tailwind CDN en los prototipos HTML.
 *
 * Deriva de node_modules/@simetrikinc/desyk-components/dist/tailwind-preset.cjs
 * (los mismos nombres de utilidad que usa el producto), para poder escribir
 * `bg-sidebar`, `text-muted-foreground`, `bg-accent`, `text-info` igual que en
 * el repo — y que el HTML sea comparable 1:1 con el TSX.
 *
 * Uso en el prototipo:
 *   <link rel="stylesheet" href="../design/tokens.css">
 *   <script src="https://cdn.tailwindcss.com"></script>
 *   <script src="../design/tailwind.desyk.js"></script>
 *
 * NOTA: `bg-tooltip` / `text-tooltip-foreground` existen en el preset de desyk
 * pero el token `--tooltip` NO está definido en dist/styles.css ni en el
 * globals.css del OC — por eso se omiten acá. No usarlos.
 * ========================================================================= */

tailwind.config = {
  darkMode: ["class"],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          "Inter", "ui-sans-serif", "system-ui", "-apple-system",
          "BlinkMacSystemFont", "Segoe UI", "Roboto", "Helvetica Neue",
          "Arial", "Noto Sans", "sans-serif",
        ],
      },
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        success: {
          DEFAULT: "hsl(var(--success))",
          foreground: "hsl(var(--success-foreground))",
        },
        warning: {
          DEFAULT: "hsl(var(--warning))",
          foreground: "hsl(var(--warning-foreground))",
        },
        info: {
          DEFAULT: "hsl(var(--info))",
          foreground: "hsl(var(--info-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        scroll: {
          DEFAULT: "hsl(var(--scroll))",
          foreground: "hsl(var(--scroll-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        sidebar: {
          DEFAULT: "hsl(var(--sidebar-background))",
          foreground: "hsl(var(--sidebar-foreground))",
          primary: "hsl(var(--sidebar-primary))",
          "primary-foreground": "hsl(var(--sidebar-primary-foreground))",
          accent: "hsl(var(--sidebar-accent))",
          "accent-foreground": "hsl(var(--sidebar-accent-foreground))",
          border: "hsl(var(--sidebar-border))",
          ring: "hsl(var(--sidebar-ring))",
        },
        ai: {
          purple: "hsl(var(--ai-purple))",
          blue: "hsl(var(--ai-blue))",
          "gray-primary": "hsl(var(--ai-gray-primary))",
          "gray-secondary": "hsl(var(--ai-gray-secondary))",
        },
        chart: {
          1: "hsl(var(--chart-1))", 2: "hsl(var(--chart-2))",
          3: "hsl(var(--chart-3))", 4: "hsl(var(--chart-4))",
          5: "hsl(var(--chart-5))", 6: "hsl(var(--chart-6))",
          7: "hsl(var(--chart-7))", 8: "hsl(var(--chart-8))",
        },
      },
      backgroundImage: {
        "ai-gradient-primary": "var(--ai-gradient-primary)",
        "ai-gradient-secondary": "var(--ai-gradient-secondary)",
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      padding: { 0.5: "2px" },
    },
  },
};
