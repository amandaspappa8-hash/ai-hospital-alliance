import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import path from "path"
import { VitePWA } from "vite-plugin-pwa"

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: "autoUpdate",
      devOptions: { enabled: true },
      includeAssets: ["favicon.svg"],
      manifest: {
        name: "AI Hospital Alliance",
        short_name: "AI Hospital",
        description: "Smart Medical Platform — AI Diagnosis, Pharmacy, Radiology",
        theme_color: "#0f172a",
        background_color: "#020817",
        display: "standalone",
        orientation: "portrait",
        start_url: "/dashboard",
        scope: "/",
        lang: "ar",
        icons: [
          { src: "/pwa-192.png", sizes: "192x192", type: "image/png" },
          { src: "/pwa-512.png", sizes: "512x512", type: "image/png" },
          { src: "/pwa-512.png", sizes: "512x512", type: "image/png", purpose: "any maskable" },
        ],
        screenshots: [
          { src: "/screenshot-wide.png", sizes: "1280x720", type: "image/png", form_factor: "wide", label: "Dashboard" },
          { src: "/screenshot-mobile.png", sizes: "390x844", type: "image/png", form_factor: "narrow", label: "Mobile View" },
        ],
        shortcuts: [
          { name: "Dashboard",  short_name: "Home",     url: "/dashboard",  icons: [{ src: "/pwa-192.png", sizes: "192x192" }] },
          { name: "Patients",   short_name: "Patients", url: "/patients",   icons: [{ src: "/pwa-192.png", sizes: "192x192" }] },
          { name: "Pharmacy",   short_name: "Pharmacy", url: "/pharmacy",   icons: [{ src: "/pwa-192.png", sizes: "192x192" }] },
          { name: "Radiology",  short_name: "X-Ray",    url: "/radiology",  icons: [{ src: "/pwa-192.png", sizes: "192x192" }] },
          { name: "Laboratory", short_name: "Labs",     url: "/labs",       icons: [{ src: "/pwa-192.png", sizes: "192x192" }] },
        ],
        categories: ["medical", "health", "productivity"],
        prefer_related_applications: false,
      },
      workbox: {
        globPatterns: ["**/*.{js,css,html,ico,png,svg,woff2}"],
        navigateFallback: "/index.html",
        navigateFallbackDenylist: [/^\/api/, /^\/ws/],
        runtimeCaching: [
          {
            urlPattern: /^http:\/\/127\.0\.0\.1:8000\/(?!ws).*/i,
            handler: "NetworkFirst",
            options: {
              cacheName: "api-cache",
              expiration: { maxEntries: 200, maxAgeSeconds: 300 },
              networkTimeoutSeconds: 5,
              cacheableResponse: { statuses: [0, 200] },
            },
          },
          {
            urlPattern: /^https:\/\/api\.fda\.gov\/.*/i,
            handler: "CacheFirst",
            options: {
              cacheName: "fda-cache",
              expiration: { maxEntries: 100, maxAgeSeconds: 86400 },
              cacheableResponse: { statuses: [0, 200] },
            },
          },
          {
            urlPattern: /^https:\/\/rxnav\.nlm\.nih\.gov\/.*/i,
            handler: "CacheFirst",
            options: {
              cacheName: "rxnorm-cache",
              expiration: { maxEntries: 100, maxAgeSeconds: 86400 },
              cacheableResponse: { statuses: [0, 200] },
            },
          },
        ],
      },
    }),
  ],
  resolve: {
    alias: { "@": path.resolve(__dirname, "./src") },
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
    proxy: {
      "/auth":        "http://127.0.0.1:8000",
      "/patients":    "http://127.0.0.1:8000",
      "/orders":      "http://127.0.0.1:8000",
      "/appointments":"http://127.0.0.1:8000",
      "/notes":       "http://127.0.0.1:8000",
      "/pacs":        "http://127.0.0.1:8000",
      "/ai":          "http://127.0.0.1:8000",
      "/doctors":     "http://127.0.0.1:8000",
      "/reports":     "http://127.0.0.1:8000",
      "/nursing":     "http://127.0.0.1:8000",
      "/alerts":      "http://127.0.0.1:8000",
      "/labs":        "http://127.0.0.1:8000",
      "/mar":         "http://127.0.0.1:8000",
      "/drug-intel":  "http://127.0.0.1:8000",
      "/radiology":   "http://127.0.0.1:8000",
      "/specialties": "http://127.0.0.1:8000",
      "/patient":     "http://127.0.0.1:8000",
      "/ws":          { target: "ws://127.0.0.1:8000", ws: true },
    },
  },
})
