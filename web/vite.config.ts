import path from "node:path"
import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import tailwindcss from "@tailwindcss/vite"

export default defineConfig({
  plugins: [react(), tailwindcss()],
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
