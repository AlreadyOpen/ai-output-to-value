import path from "node:path"
import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import tailwindcss from "@tailwindcss/vite"

export default defineConfig({
  plugins: [react(), tailwindcss()],
  define: {
    // Base UI ships development guards that reference process.env.NODE_ENV.
    // This is a browser-only bundle, so replace that Node expression at build
    // time rather than relying on a global `process` object in the browser.
    "process.env.NODE_ENV": JSON.stringify("production"),
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      // The claim gate is one module shared with the native MCP server. It lives outside
      // web/, so point its two dependencies at this package's copies instead of relying on
      // packages/mcp/node_modules being installed.
      "@gate-core": path.resolve(__dirname, "../packages/mcp/src/gate-core.mjs"),
      "ajv/dist/2020.js": path.resolve(__dirname, "node_modules/ajv/dist/2020.js"),
      "ajv-formats": path.resolve(__dirname, "node_modules/ajv-formats"),
    },
  },
  build: {
    outDir: "../site/ui",
    emptyOutDir: true,
    lib: {
      // aiov-ui.js is the interactive UI; gate-core.js is the claim gate on its own, loaded
      // by WebMCP on pages that do not mount the UI.
      entry: {
        "aiov-ui": path.resolve(__dirname, "src/main.tsx"),
        "gate-core": path.resolve(__dirname, "src/gate-core-entry.ts"),
      },
      formats: ["es"],
      fileName: (_format, entryName) => `${entryName}.js`,
      cssFileName: "aiov-ui",
    },
    rollupOptions: {
      output: {
        assetFileNames: (assetInfo) =>
          assetInfo.name?.endsWith(".css") ? "aiov-ui.css" : "assets/[name][extname]",
      },
    },
  },
})
