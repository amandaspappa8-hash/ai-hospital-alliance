import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import path from "path"

export default defineConfig({
  plugins: [react()],

  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
    extensions: [".tsx", ".ts", ".jsx", ".js", ".mjs", ".json"],
  },

  build: {
    chunkSizeWarningLimit: 1200,

    rollupOptions: {
      output: {
        manualChunks: {
          react_vendor: [
            "react",
            "react-dom",
            "react-router-dom"
          ],

          vtk_vendor: [
            "@kitware/vtk.js"
          ],

          three_vendor: [
            "three",
            "@react-three/fiber",
            "@react-three/drei"
          ],

          pdf_vendor: [
            "jspdf",
            "html2canvas"
          ]
        }
      }
    }
  },

  server: {
    host: "0.0.0.0",
    port: 5173
  }
})
