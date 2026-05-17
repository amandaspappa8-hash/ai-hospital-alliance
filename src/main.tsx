import React from "react"
import ReactDOM from "react-dom/client"
import { BrowserRouter } from "react-router-dom"
import App from "./App"
import "./index.css"
import { initMonitoring } from "./lib/monitoring"
import ErrorBoundary from "./components/system/ErrorBoundary"

initMonitoring()

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .getRegistrations()
      .then((registrations) => registrations.forEach((registration) => registration.unregister()))
      .catch(err => console.log("[PWA] SW cleanup failed:", err))
  })
}

const rootElement = document.getElementById("root")

if (!rootElement) {
  throw new Error("AI Hospital Alliance failed to start: missing #root element.")
}

ReactDOM.createRoot(rootElement).render(
  // StrictMode أُزيل - كان يشغّل كل effect مرتين ويسبب History API flood
  <ErrorBoundary>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </ErrorBoundary>
)
