import { useEffect, useState } from "react"
import { apiGet, apiPost } from "@/lib/api"

type Order = {
  id: number
  type: string
  department: string
  note: string
  status: string
}

type AiDraft = {
  patientId?: string
  patientName?: string
  patientAge?: number | null
  patientGender?: string | null
  labs?: string[]
  drugs?: string[]
  routing?: string[]
  alerts?: string[]
  actions?: string[]
  severity?: string
  riskScore?: number
}

export default function OrdersPage() {
  const [patientId, setPatientId] = useState("P-1001")
  const [department, setDepartment] = useState("Lab")
  const [orderType, setOrderType] = useState("Clinical Chemistry")
  const [note, setNote] = useState("AI suggested order")
  const [orders, setOrders] = useState<Order[]>([])
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [bulkSaving, setBulkSaving] = useState(false)
  const [error, setError] = useState("")
  const [aiDraft, setAiDraft] = useState<AiDraft | null>(null)

  async function loadOrders(pid: string) {
    setLoading(true)
    setError("")
    try {
      const data = await apiGet<Order[]>(`/orders/${pid}`)
      setOrders(Array.isArray(data) ? data : [])
    } catch (err) {
      console.error(err)
      setError("Failed to load orders")
      setOrders([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadOrders(patientId)
  }, [patientId])

  useEffect(() => {
    const draft = localStorage.getItem("AI_ORDER_DRAFT")
    if (draft) {
      try {
        const data = JSON.parse(draft) as AiDraft
        setAiDraft(data)

        if (data.patientId) {
          setPatientId(data.patientId)
        }

        if (data.labs && data.labs.length > 0) {
          setDepartment("Lab")
          setOrderType(data.labs[0])
          setNote("AI suggested lab order")
        } else if (data.drugs && data.drugs.length > 0) {
          setDepartment("Pharmacy")
          setOrderType(data.drugs[0])
          setNote("AI suggested medication")
        } else if (data.routing && data.routing.length > 0) {
          setDepartment(data.routing[0])
          setOrderType("Referral")
          setNote("AI suggested referral")
        }
      } catch (e) {
        console.error("Invalid AI order draft", e)
      } finally {
        localStorage.removeItem("AI_ORDER_DRAFT")
      }
    }
  }, [])

  async function createOrder() {
    setSaving(true)
    setError("")
    try {
      await apiPost(`/orders/${patientId}`, {
        type: orderType,
        department,
        note,
      })
      await loadOrders(patientId)
      setNote("")
    } catch (err) {
      console.error(err)
      setError("Failed to create order")
    } finally {
      setSaving(false)
    }
  }

  async function createAllAiOrders() {
    if (!aiDraft) return

    setBulkSaving(true)
    setError("")

    try {
      const tasks: Promise<unknown>[] = []

      for (const lab of aiDraft.labs ?? []) {
        tasks.push(
          apiPost(`/orders/${patientId}`, {
            type: lab,
            department: "Lab",
            note: "AI suggested lab order",
          })
        )
      }

      for (const drug of aiDraft.drugs ?? []) {
        tasks.push(
          apiPost(`/orders/${patientId}`, {
            type: drug,
            department: "Pharmacy",
            note: "AI suggested medication order",
          })
        )
      }

      for (const route of aiDraft.routing ?? []) {
        tasks.push(
          apiPost(`/orders/${patientId}`, {
            type: "Referral",
            department: route,
            note: "AI suggested referral",
          })
        )
      }

      await Promise.all(tasks)
      await loadOrders(patientId)
      setAiDraft(null)
      alert("All AI orders created successfully")
    } catch (err) {
      console.error(err)
      setError("Failed to create AI orders")
    } finally {
      setBulkSaving(false)
    }
  }

  return (
    <div style={{ padding: "24px", color: "white" }}>
      <h1 style={{ fontSize: "30px", marginBottom: "8px" }}>Orders Engine</h1>
      <p style={{ opacity: 0.8, marginBottom: "20px" }}>
        Clinical workflow orders for labs, imaging, pharmacy, and referrals
      </p>

      {aiDraft && (
        <div
          style={{
            background: "#0f172a",
            border: "1px solid #38bdf8",
            borderRadius: "12px",
            padding: "18px",
            maxWidth: "760px",
            marginBottom: "20px",
          }}
        >
          <div style={{ fontSize: "20px", fontWeight: 700, marginBottom: "12px" }}>
            AI Order Draft
          </div>

          <div style={{ marginBottom: "10px" }}>
            <strong>Patient:</strong> {aiDraft.patientName ?? "Unknown"} ({patientId})
          </div>

          <div style={{ marginBottom: "10px" }}>
            <strong>Age:</strong> {aiDraft.patientAge ?? "N/A"} | <strong>Gender:</strong> {aiDraft.patientGender ?? "N/A"}
          </div>

          <div style={{ marginBottom: "10px" }}>
            <strong>Severity:</strong> {aiDraft.severity ?? "N/A"} | <strong>Risk:</strong> {aiDraft.riskScore ?? "N/A"}/100
          </div>

          {aiDraft.actions && aiDraft.actions.length > 0 && (
            <div style={{ marginBottom: "10px" }}>
              <strong>Recommended Actions:</strong> {aiDraft.actions.join(" | ")}
            </div>
          )}

          {aiDraft.routing && aiDraft.routing.length > 0 && (
            <div style={{ marginBottom: "10px" }}>
              <strong>Routing:</strong> {aiDraft.routing.join(", ")}
            </div>
          )}

          {aiDraft.labs && aiDraft.labs.length > 0 && (
            <div style={{ marginBottom: "10px" }}>
              <strong>Suggested Labs:</strong> {aiDraft.labs.join(", ")}
            </div>
          )}

          {aiDraft.drugs && aiDraft.drugs.length > 0 && (
            <div style={{ marginBottom: "10px" }}>
              <strong>Suggested Medications:</strong> {aiDraft.drugs.join(", ")}
            </div>
          )}

          {aiDraft.alerts && aiDraft.alerts.length > 0 && (
            <div style={{ marginBottom: "10px" }}>
              <strong>Alerts:</strong> {aiDraft.alerts.join(" | ")}
            </div>
          )}

          <button
            onClick={createAllAiOrders}
            style={{
              marginTop: "12px",
              padding: "12px 18px",
              borderRadius: "10px",
              border: "1px solid #38bdf8",
              background: "#0284c7",
              color: "white",
              cursor: "pointer",
              fontWeight: 700,
            }}
          >
            {bulkSaving ? "Creating AI Orders..." : "Create All AI Orders"}
          </button>
        </div>
      )}

      <div
        style={{
          background: "#111827",
          border: "1px solid #374151",
          borderRadius: "12px",
          padding: "18px",
          maxWidth: "640px",
          marginBottom: "20px",
        }}
      >
        <div style={{ marginBottom: "12px" }}>
          <label>Patient ID</label>
          <input
            value={patientId}
            onChange={(e) => setPatientId(e.target.value)}
            style={inputStyle}
          />
        </div>

        <div style={{ marginBottom: "12px" }}>
          <label>Department</label>
          <select
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
            style={inputStyle}
          >
            <option value="Lab">Lab</option>
            <option value="Radiology">Radiology</option>
            <option value="Emergency">Emergency</option>
            <option value="Cardiology">Cardiology</option>
            <option value="Internal Medicine">Internal Medicine</option>
            <option value="Pharmacy">Pharmacy</option>
          </select>
        </div>

        <div style={{ marginBottom: "12px" }}>
          <label>Order Type</label>
          <input
            value={orderType}
            onChange={(e) => setOrderType(e.target.value)}
            style={inputStyle}
          />
        </div>

        <div style={{ marginBottom: "12px" }}>
          <label>Note</label>
          <textarea
            value={note}
            onChange={(e) => setNote(e.target.value)}
            style={textareaStyle}
          />
        </div>

        <button onClick={createOrder} style={buttonStyle}>
          {saving ? "Creating..." : "Create Order"}
        </button>
      </div>

      {error && <div style={{ color: "#fca5a5", marginBottom: "16px" }}>{error}</div>}

      <div
        style={{
          background: "#111827",
          border: "1px solid #374151",
          borderRadius: "12px",
          padding: "18px",
          maxWidth: "760px",
        }}
      >
        <div style={{ fontSize: "20px", fontWeight: 700, marginBottom: "12px" }}>
          Patient Orders
        </div>

        {loading ? (
          <div>Loading...</div>
        ) : orders.length === 0 ? (
          <div style={{ opacity: 0.8 }}>No orders for this patient.</div>
        ) : (
          <div style={{ display: "grid", gap: "10px" }}>
            {orders.map((order) => (
              <div key={order.id} style={cardStyle}>
                <div style={{ fontWeight: 700 }}>
                  #{order.id} — {order.type}
                </div>
                <div style={{ opacity: 0.82, marginTop: "4px" }}>
                  {order.department} • {order.status}
                </div>
                {order.note && (
                  <div style={{ opacity: 0.75, marginTop: "6px" }}>{order.note}</div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

const inputStyle: React.CSSProperties = {
  width: "100%",
  marginTop: "6px",
  padding: "12px",
  borderRadius: "10px",
  border: "1px solid #374151",
  background: "#030712",
  color: "white",
}

const textareaStyle: React.CSSProperties = {
  width: "100%",
  minHeight: "100px",
  marginTop: "6px",
  padding: "12px",
  borderRadius: "10px",
  border: "1px solid #374151",
  background: "#030712",
  color: "white",
}

const buttonStyle: React.CSSProperties = {
  padding: "12px 18px",
  borderRadius: "10px",
  border: "1px solid #22c55e",
  background: "#166534",
  color: "white",
  cursor: "pointer",
  fontWeight: 600,
}

const cardStyle: React.CSSProperties = {
  padding: "12px",
  background: "#0b1220",
  border: "1px solid #374151",
  borderRadius: "10px",
}
