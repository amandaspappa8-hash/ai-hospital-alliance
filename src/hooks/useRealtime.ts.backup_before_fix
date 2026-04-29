import { useEffect, useRef, useState, useCallback } from "react"

export type RealtimeAlert = {
  id: string
  type: "alert" | "patient" | "lab" | "radiology" | "pharmacy"
  message: string
  severity: "low" | "moderate" | "high" | "critical"
  timestamp: string
  patientId?: string
}

export function useRealtime() {
  const [alerts, setAlerts] = useState<RealtimeAlert[]>([])
  const [connected, setConnected] = useState(false)
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectRef = useRef<ReturnType<typeof setTimeout> | undefined>(undefined)

  const connect = useCallback(() => {
    try {
      const ws = new WebSocket("ws://127.0.0.1:8000/ws/alerts")
      wsRef.current = ws

      ws.onopen = () => {
        setConnected(true)
        console.log("[WS] Connected to real-time alerts")
      }

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data) as RealtimeAlert
          setAlerts(prev => [data, ...prev].slice(0, 50))

          // Browser notification
          if (Notification.permission === "granted" && data.severity === "critical") {
            new Notification("AI Hospital — Critical Alert", {
              body: data.message,
              icon: "/favicon.svg",
              badge: "/favicon.svg",
              tag: data.id,
            })
          }
        } catch {}
      }

      ws.onclose = () => {
        setConnected(false)
        reconnectRef.current = setTimeout(() => connect(), 3000)
      }

      ws.onerror = () => {
        ws.close()
      }
    } catch {
      setConnected(false)
      reconnectRef.current = setTimeout(() => connect(), 5000)
    }
  }, [])

  useEffect(() => {
    // Request notification permission
    if (Notification.permission === "default") {
      Notification.requestPermission()
    }

    connect()

    return () => {
      clearTimeout(reconnectRef.current)
      wsRef.current?.close()
    }
  }, [connect])

  function dismiss(id: string) {
    setAlerts(prev => prev.filter(a => a.id !== id))
  }

  function dismissAll() {
    setAlerts([])
  }

  return { alerts, connected, dismiss, dismissAll }
}
