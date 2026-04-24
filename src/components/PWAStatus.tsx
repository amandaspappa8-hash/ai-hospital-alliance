import { useState, useEffect } from "react"

export default function PWAStatus() {
  const [isStandalone, setIsStandalone] = useState(false)
  const [isOnline, setIsOnline] = useState(navigator.onLine)

  useEffect(() => {
    setIsStandalone(window.matchMedia("(display-mode: standalone)").matches)

    const onOnline  = () => setIsOnline(true)
    const onOffline = () => setIsOnline(false)
    window.addEventListener("online",  onOnline)
    window.addEventListener("offline", onOffline)
    return () => {
      window.removeEventListener("online",  onOnline)
      window.removeEventListener("offline", onOffline)
    }
  }, [])

  if (!isStandalone && isOnline) return null

  return (
    <div style={{
      display: "flex", alignItems: "center", gap: 6,
      padding: "4px 10px", borderRadius: 20, fontSize: 11, fontWeight: 700,
      background: isOnline ? "rgba(16,185,129,0.1)" : "rgba(239,68,68,0.1)",
      border: `1px solid ${isOnline ? "rgba(16,185,129,0.3)" : "rgba(239,68,68,0.3)"}`,
      color: isOnline ? "#4ade80" : "#f87171",
    }}>
      <div style={{
        width: 6, height: 6, borderRadius: "50%",
        background: isOnline ? "#4ade80" : "#f87171",
        boxShadow: isOnline ? "0 0 6px #4ade80" : "0 0 6px #f87171",
      }} />
      {isStandalone ? "📱 App" : ""} {isOnline ? "Online" : "Offline Mode"}
    </div>
  )
}
