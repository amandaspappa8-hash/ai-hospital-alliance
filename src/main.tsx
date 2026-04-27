import React from "react"
import ReactDOM from "react-dom/client"
import { BrowserRouter } from "react-router-dom"
import App from "./App"
import "./index.css"
import { initMonitoring } from "./lib/monitoring"
import ErrorBoundary from "./components/system/ErrorBoundary"
import PWAInstall from "./components/PWAInstall"

initMonitoring()

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/sw.js")
      .then(reg => console.log("[PWA] Service Worker registered:", reg.scope))
      .catch(err => console.log("[PWA] SW registration failed:", err))
  })
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  // StrictMode أُزيل - كان يشغّل كل effect مرتين ويسبب History API flood
  <ErrorBoundary>
    <BrowserRouter>
      <App />
      <PWAInstall />
    </BrowserRouter>
  </ErrorBoundary>
)
