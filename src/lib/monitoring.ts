import { monitoringEnabled, appEnv } from "./env"

export function initMonitoring() {
  if (!monitoringEnabled) {
    console.info("[monitoring] disabled")
    return
  }

  console.info("[monitoring] enabled", { appEnv })

  window.addEventListener("error", (event) => {
    console.error("[monitoring] window error", {
      message: event.message,
      source: event.filename,
      line: event.lineno,
      column: event.colno,
    })
  })

  window.addEventListener("unhandledrejection", (event) => {
    console.error("[monitoring] unhandled rejection", event.reason)
  })
}
