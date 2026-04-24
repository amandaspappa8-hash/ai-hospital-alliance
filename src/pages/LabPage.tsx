import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { apiGet } from "@/lib/api"

export default function LabPage() {
  const { patientId } = useParams<{ patientId: string }>()
  const [orders, setOrders] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    apiGet<any[]>(`/labs/orders/${patientId}`)
      .then(d => setOrders(Array.isArray(d) ? d : []))
      .catch(() => setOrders([]))
      .finally(() => setLoading(false))
  }, [patientId])

  return (
    <div style={{ minHeight: "100vh", background: "linear-gradient(135deg,#020817,#0f1629)", padding: "28px 32px", fontFamily: "Inter,Arial,sans-serif", color: "white" }}>
      <div style={{ maxWidth: 1000, margin: "0 auto" }}>
        <div style={{ marginBottom: 24 }}>
          <div style={{ fontSize: 12, color: "#10b981", fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 6 }}>◈ LABORATORY</div>
          <h1 style={{ margin: 0, fontSize: 26, fontWeight: 900, color: "white" }}>🧬 Lab Orders — {patientId}</h1>
        </div>
        <div style={{ background: "linear-gradient(135deg,#0f172a,#1a2540)", border: "1px solid rgba(16,185,129,0.2)", borderRadius: 20, padding: 22 }}>
          {loading ? <div style={{ color: "#64748b" }}>Loading...</div> : orders.length === 0 ? (
            <div style={{ color: "#64748b" }}>No lab orders for {patientId}</div>
          ) : orders.map((o, i) => (
            <div key={i} style={{ padding: "14px 16px", borderRadius: 12, marginBottom: 10, background: "rgba(16,185,129,0.06)", border: "1px solid rgba(16,185,129,0.2)" }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
                <span style={{ fontWeight: 800, color: "white" }}>{o.id}</span>
                <span style={{ padding: "2px 10px", borderRadius: 20, fontSize: 11, fontWeight: 700, background: "rgba(16,185,129,0.15)", color: "#4ade80" }}>{o.status}</span>
              </div>
              <div style={{ color: "#94a3b8", fontSize: 13 }}>{o.section} · {(o.tests ?? []).join(", ")}</div>
              {o.result && <div style={{ color: "#4ade80", fontSize: 12, marginTop: 6 }}>Result: {o.result}</div>}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
