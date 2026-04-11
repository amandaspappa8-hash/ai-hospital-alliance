import { useEffect, useState } from "react"
import { apiGet, apiPost } from "@/lib/api"
import type { Patient } from "@/types/patient"

type ClinicalRoute = {
  chief_complaint: string
  triage_level: string
  urgency_score: number
  route_to: string[]
  suggested_orders: Array<{
    name: string
    priority: string
    category: string
  }>
  red_flags: string[]
  next_actions: string[]
  rationale: string[]
}

type ClinicalResult = {
  patient_id?: string
  clinical_route?: ClinicalRoute
  created_orders?: Array<{
    id: number
    type: string
    department: string
    note: string
    status: string
  }>
  skipped_existing_orders?: string[]
}

export default function AIRoutingPage() {
  const [text, setText] = useState("chest pain, sweating, nausea, shortness of breath")
  const [patients, setPatients] = useState<Patient[]>([])
  const [selectedPatientId, setSelectedPatientId] = useState("")
  const [age, setAge] = useState("58")
  const [gender, setGender] = useState("male")
  const [loadingPatients, setLoadingPatients] = useState(true)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [aiResult, setAiResult] = useState<ClinicalResult | null>(null)

  useEffect(() => {
    async function loadPatients() {
      setLoadingPatients(true)
      try {
        const data = await apiGet<Patient[]>("/patients")
        const rows = Array.isArray(data) ? data : []
        setPatients(rows)
        if (rows.length > 0) {
          setSelectedPatientId(rows[0].id)
        }
      } catch (err) {
        console.error(err)
        setError("Failed to load patients")
      } finally {
        setLoadingPatients(false)
      }
    }

    loadPatients()
  }, [])

  async function runAI() {
    if (!selectedPatientId) return

    setLoading(true)
    setError("")
    setAiResult(null)

    try {
      const res = await apiPost<ClinicalResult>(
        `/ai/clinical-route-and-create-orders/${selectedPatientId}`,
        {
          chief_complaint: text,
          symptoms: text.split(",").map((s) => s.trim()).filter(Boolean),
          age: Number(age),
          gender,
        }
      )
      setAiResult(res)
    } catch (e) {
      console.error(e)
      setError("Failed to run AI routing")
    } finally {
      setLoading(false)
    }
  }

  const route = aiResult?.clinical_route

  return (
    <div style={{ padding: 30, color: "white" }}>
      <h1 style={{ fontSize: 28, marginBottom: 8 }}>AI Clinical Routing</h1>
      <p style={{ opacity: 0.8, marginBottom: 20 }}>
        AI-powered triage, routing, and order generation
      </p>

      <div
        style={{
          background: "#111827",
          border: "1px solid #374151",
          borderRadius: 12,
          padding: 18,
          maxWidth: 900,
        }}
      >
        <div style={{ marginBottom: 12 }}>
          <label>Select Patient</label>
          <select
            value={selectedPatientId}
            onChange={(e) => setSelectedPatientId(e.target.value)}
            style={inputStyle}
            disabled={loadingPatients}
          >
            {patients.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name} ({p.id})
              </option>
            ))}
          </select>
        </div>

        <div style={{ marginBottom: 12 }}>
          <label>Age</label>
          <input
            value={age}
            onChange={(e) => setAge(e.target.value)}
            style={inputStyle}
          />
        </div>

        <div style={{ marginBottom: 12 }}>
          <label>Gender</label>
          <input
            value={gender}
            onChange={(e) => setGender(e.target.value)}
            style={inputStyle}
          />
        </div>

        <div style={{ marginBottom: 12 }}>
          <label>Symptoms / Chief Complaint</label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            style={textareaStyle}
          />
        </div>

        <button onClick={runAI} style={buttonStyle} disabled={loading || loadingPatients}>
          {loading ? "Running..." : "Run AI + Create Orders"}
        </button>
      </div>

      {error && (
        <div style={{ color: "#fca5a5", marginTop: 16, marginBottom: 16 }}>
          {error}
        </div>
      )}

      {route && (
        <div
          style={{
            marginTop: 24,
            maxWidth: 900,
            display: "grid",
            gap: 16,
          }}
        >
          <div style={panelStyle}>
            <div style={sectionTitle}>Clinical Route</div>
            <div><strong>Chief Complaint:</strong> {route.chief_complaint}</div>
            <div style={{ marginTop: 8 }}><strong>Triage Level:</strong> {route.triage_level}</div>
            <div style={{ marginTop: 8 }}><strong>Urgency Score:</strong> {route.urgency_score}</div>
          </div>

          <div style={panelStyle}>
            <div style={sectionTitle}>Route To</div>
            {route.route_to?.length ? route.route_to.map((item, i) => (
              <div key={i} style={itemStyle}>{item}</div>
            )) : <div style={{ opacity: 0.8 }}>No routing suggestions.</div>}
          </div>

          <div style={panelStyle}>
            <div style={sectionTitle}>Suggested Orders</div>
            {route.suggested_orders?.length ? route.suggested_orders.map((order, i) => (
              <div key={i} style={cardStyle}>
                <div style={{ fontWeight: 700 }}>{order.name}</div>
                <div style={{ opacity: 0.8, marginTop: 4 }}>
                  {order.category} • {order.priority}
                </div>
              </div>
            )) : <div style={{ opacity: 0.8 }}>No suggested orders.</div>}
          </div>

          <div style={panelStyle}>
            <div style={sectionTitle}>Red Flags</div>
            {route.red_flags?.length ? route.red_flags.map((item, i) => (
              <div key={i} style={itemStyle}>{item}</div>
            )) : <div style={{ opacity: 0.8 }}>No red flags.</div>}
          </div>

          <div style={panelStyle}>
            <div style={sectionTitle}>Next Actions</div>
            {route.next_actions?.length ? route.next_actions.map((item, i) => (
              <div key={i} style={itemStyle}>{item}</div>
            )) : <div style={{ opacity: 0.8 }}>No next actions.</div>}
          </div>

          <div style={panelStyle}>
            <div style={sectionTitle}>Rationale</div>
            {route.rationale?.length ? route.rationale.map((item, i) => (
              <div key={i} style={itemStyle}>{item}</div>
            )) : <div style={{ opacity: 0.8 }}>No rationale.</div>}
          </div>

          <div style={panelStyle}>
            <div style={sectionTitle}>Created Orders</div>
            {aiResult?.created_orders?.length ? aiResult.created_orders.map((order) => (
              <div key={order.id} style={cardStyle}>
                <div style={{ fontWeight: 700 }}>
                  #{order.id} — {order.type}
                </div>
                <div style={{ opacity: 0.8, marginTop: 4 }}>
                  {order.department} • {order.status}
                </div>
                {order.note && (
                  <div style={{ opacity: 0.75, marginTop: 6 }}>{order.note}</div>
                )}
              </div>
            )) : <div style={{ opacity: 0.8 }}>No orders were created.</div>}
          </div>
        </div>
      )}
    </div>
  )
}

const inputStyle: React.CSSProperties = {
  width: "100%",
  padding: "12px",
  borderRadius: "10px",
  border: "1px solid #374151",
  background: "#030712",
  color: "white",
  marginTop: "8px",
}

const textareaStyle: React.CSSProperties = {
  width: "100%",
  minHeight: "140px",
  padding: "12px",
  borderRadius: "10px",
  border: "1px solid #374151",
  background: "#030712",
  color: "white",
  marginTop: "10px",
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

const panelStyle: React.CSSProperties = {
  padding: 16,
  borderRadius: 12,
  background: "#111827",
  border: "1px solid #374151",
}

const sectionTitle: React.CSSProperties = {
  fontSize: 18,
  fontWeight: 700,
  marginBottom: 12,
}

const itemStyle: React.CSSProperties = {
  padding: "10px 12px",
  marginBottom: 8,
  borderRadius: 10,
  background: "#0b1220",
  border: "1px solid #374151",
}

const cardStyle: React.CSSProperties = {
  padding: "12px",
  background: "#0b1220",
  border: "1px solid #374151",
  borderRadius: "10px",
  marginBottom: "10px",
}
