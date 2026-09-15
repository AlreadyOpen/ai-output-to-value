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
    },
  },
  build: {
    outDir: "../site/ui",
    emptyOutDir: true,
    lib: {
      entry: path.resolve(__dirname, "src/main.tsx"),
      formats: ["es"],
      fileName: () => "aiov-ui.js",
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
