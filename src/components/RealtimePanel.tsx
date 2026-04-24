import { useState } from "react"
import { useRealtime, type RealtimeAlert } from "@/hooks/useRealtime"

const SEVERITY_STYLE: Record<string, { bg: string; color: string; border: string }> = {
  critical: { bg: "rgba(239,68,68,0.12)",  color: "#f87171", border: "rgba(239,68,68,0.4)" },
  high:     { bg: "rgba(245,158,11,0.10)", color: "#fbbf24", border: "rgba(245,158,11,0.3)" },
  moderate: { bg: "rgba(59,130,246,0.08)", color: "#60a5fa", border: "rgba(59,130,246,0.3)" },
  low:      { bg: "rgba(16,185,129,0.08)", color: "#4ade80", border: "rgba(16,185,129,0.3)" },
}

const TYPE_ICON: Record<string, string> = {
  alert: "🚨", patient: "🧑‍⚕️", lab: "🧬", radiology: "🩻", pharmacy: "💊",
}

export default function RealtimePanel() {
  const { alerts, connected, dismiss, dismissAll } = useRealtime()
  const [open, setOpen] = useState(false)

  const criticalCount = alerts.filter(a => a.severity === "critical").length
  const hasAlerts = alerts.length > 0

  return (
    <>
      {/* Bell button */}
      <div style={{ position: "relative", display: "inline-block" }}>
        <button
          onClick={() => setOpen(o => !o)}
          style={{
            width: 38, height: 38, borderRadius: 10, border: "none",
            background: hasAlerts ? "rgba(239,68,68,0.15)" : "rgba(255,255,255,0.06)",
            color: hasAlerts ? "#f87171" : "#94a3b8",
            cursor: "pointer", fontSize: 17, display: "flex",
            alignItems: "center", justifyContent: "center",
            boxShadow: criticalCount > 0 ? "0 0 12px rgba(239,68,68,0.4)" : "none",
            transition: "all 0.2s",
          }}
        >
          🔔
        </button>

        {/* Badge */}
        {hasAlerts && (
          <div style={{
            position: "absolute", top: -4, right: -4,
            width: 18, height: 18, borderRadius: "50%",
            background: criticalCount > 0 ? "#ef4444" : "#3b82f6",
            color: "white", fontSize: 10, fontWeight: 900,
            display: "flex", alignItems: "center", justifyContent: "center",
            boxShadow: "0 0 8px rgba(239,68,68,0.6)",
          }}>{alerts.length > 9 ? "9+" : alerts.length}</div>
        )}

        {/* Connection dot */}
        <div style={{
          position: "absolute", bottom: -2, left: -2,
          width: 8, height: 8, borderRadius: "50%",
          background: connected ? "#4ade80" : "#64748b",
          boxShadow: connected ? "0 0 6px #4ade80" : "none",
          border: "1px solid #020817",
        }} />
      </div>

      {/* Panel */}
      {open && (
        <div style={{
          position: "fixed", top: 60, right: 20, width: 360, zIndex: 1000,
          background: "linear-gradient(135deg,#0f172a,#1a2540)",
          border: "1px solid rgba(59,130,246,0.2)",
          borderRadius: 16, boxShadow: "0 20px 60px rgba(0,0,0,0.6)",
          overflow: "hidden",
        }}>
          {/* Header */}
          <div style={{
            padding: "14px 16px", display: "flex", justifyContent: "space-between",
            alignItems: "center", borderBottom: "1px solid rgba(255,255,255,0.06)",
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <div style={{
                width: 8, height: 8, borderRadius: "50%",
                background: connected ? "#4ade80" : "#64748b",
                boxShadow: connected ? "0 0 8px #4ade80" : "none",
              }} />
              <span style={{ fontWeight: 700, color: "white", fontSize: 13 }}>
                Real-time Alerts {connected ? "(Live)" : "(Offline)"}
              </span>
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              {hasAlerts && (
                <button onClick={dismissAll} style={{
                  padding: "4px 10px", borderRadius: 6, fontSize: 11, fontWeight: 600,
                  background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.3)",
                  color: "#f87171", cursor: "pointer",
                }}>Clear all</button>
              )}
              <button onClick={() => setOpen(false)} style={{
                width: 24, height: 24, borderRadius: 6, border: "none",
                background: "rgba(255,255,255,0.06)", color: "#64748b",
                cursor: "pointer", fontSize: 14,
              }}>×</button>
            </div>
          </div>

          {/* Alerts list */}
          <div style={{ maxHeight: 400, overflowY: "auto" }}>
            {alerts.length === 0 ? (
              <div style={{ padding: 32, textAlign: "center" }}>
                <div style={{ fontSize: 32, marginBottom: 8 }}>✓</div>
                <div style={{ color: "#4ade80", fontSize: 13, fontWeight: 600 }}>All systems normal</div>
                <div style={{ color: "#475569", fontSize: 11, marginTop: 4 }}>
                  {connected ? "Monitoring live..." : "Connecting..."}
                </div>
              </div>
            ) : (
              alerts.map(alert => {
                const s = SEVERITY_STYLE[alert.severity] ?? SEVERITY_STYLE.low
                return (
                  <div key={alert.id} style={{
                    padding: "12px 16px", borderBottom: "1px solid rgba(255,255,255,0.04)",
                    background: s.bg, display: "flex", gap: 10, alignItems: "flex-start",
                  }}>
                    <span style={{ fontSize: 18, flexShrink: 0 }}>{TYPE_ICON[alert.type] ?? "🔔"}</span>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 3 }}>
                        <span style={{
                          fontSize: 10, fontWeight: 800, color: s.color,
                          textTransform: "uppercase", letterSpacing: 1,
                        }}>{alert.severity}</span>
                        <span style={{ fontSize: 10, color: "#475569" }}>
                          {new Date(alert.timestamp).toLocaleTimeString()}
                        </span>
                      </div>
                      <div style={{ color: "#cbd5e1", fontSize: 12, lineHeight: 1.5 }}>{alert.message}</div>
                      {alert.patientId && (
                        <div style={{ color: "#475569", fontSize: 11, marginTop: 3 }}>
                          Patient: {alert.patientId}
                        </div>
                      )}
                    </div>
                    <button onClick={() => dismiss(alert.id)} style={{
                      width: 20, height: 20, borderRadius: 4, border: "none",
                      background: "rgba(255,255,255,0.06)", color: "#64748b",
                      cursor: "pointer", fontSize: 12, flexShrink: 0,
                    }}>×</button>
                  </div>
                )
              })
            )}
          </div>
        </div>
      )}
    </>
  )
}
