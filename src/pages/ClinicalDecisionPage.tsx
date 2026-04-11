import { useEffect, useMemo, useState } from "react"
import { useNavigate, useSearchParams } from "react-router-dom"
import "../styles/medical-ui.css"
import { apiGet, apiPost } from "@/lib/api"
import VisitTimelineCard from "@/components/clinical/VisitTimelineCard"
import SmartOrdersCard from "@/components/clinical/SmartOrdersCard"
import DigitalSignatureCard from "@/components/clinical/DigitalSignatureCard"
import DecisionEngineCard from "@/components/clinical/DecisionEngineCard"
import { buildVisitTimeline } from "@/lib/visitTimeline"
import { buildSmartOrders } from "@/lib/smartOrders"
import { buildDigitalSignature } from "@/lib/digitalSignature"
import { runSmartDecisionEngine } from "@/lib/smartDecisionEngine"

type Patient = {
  id: string
  name: string
  age?: number
  gender?: string
  department?: string
  status?: string
  condition?: string
}

type Note = {
  id: number
  text: string
}

export default function ClinicalDecisionPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const patientIdFromUrl = searchParams.get("patientId") ?? ""
  const complaintFromUrl = searchParams.get("complaint") ?? ""

  const [patients, setPatients] = useState<Patient[]>([])
  const [selectedPatientId, setSelectedPatientId] = useState(patientIdFromUrl)
  const [text, setText] = useState(
    complaintFromUrl || "chest pain, sweating, shortness of breath"
  )
  const [hr, setHr] = useState("118")
  const [sbp, setSbp] = useState("95")
  const [temp, setTemp] = useState("38.6")
  const [spo2, setSpo2] = useState("91")
  const [notes, setNotes] = useState<Note[]>([])
  const [error, setError] = useState("")
  const [sendingToNotes, setSendingToNotes] = useState(false)

  const [aiSummary, setAiSummary] = useState("")

  useEffect(() => {
    apiGet("/patients")
      .then((data: any) => {
        const rows = Array.isArray(data) ? data : []
        setPatients(rows)
        if (!patientIdFromUrl && rows.length > 0) {
          setSelectedPatientId(rows[0].id)
        }
      })
      .catch(() => {
        setPatients([])
        setError("Failed to load patients")
      })
  }, [patientIdFromUrl])

  const selectedPatient = useMemo(() => {
    return patients.find((p) => String(p.id) === String(selectedPatientId)) || null
  }, [patients, selectedPatientId])

  useEffect(() => {
    if (!selectedPatient?.id) return

    apiGet(`/notes/${selectedPatient.id}`)
      .then((data: any) => setNotes(Array.isArray(data) ? data : []))
      .catch(() => setNotes([]))
  }, [selectedPatient?.id])

  const result = useMemo(() => {
    return {
      impression:
        "Primary concern: Acute Coronary Syndrome. Severity is RED with estimated risk score 90/100.",
      recommendedPlan:
        "Recommended routing: Cardiology, Internal Medicine. Suggested labs: Troponin, CK-MB, CBC, CRP, ABG. Suggested medications: Aspirin, Paracetamol.",
      nextStepSummary:
        "Immediate next steps: Supplemental Oxygen, ICU consideration, immediate emergency management, continuous monitoring.",
    }
  }, [])

  const timelineItems = buildVisitTimeline(selectedPatient)
  const smartOrders = buildSmartOrders(selectedPatient)
  const digitalSignature = buildDigitalSignature("Dr Mohammed Elfallah")
  const decisionResult = runSmartDecisionEngine(selectedPatient)

  const generateClinicalSummary = () => {
    const summary =
      "Clinical Impression:\nCardiac risk suspected\n\n" +
      "Recommended Plan:\nECG + Troponin\n\n" +
      "Next Step:\nAdmit patient"

    setAiSummary(summary)
  }

  async function sendSummaryToNotes() {
    if (!selectedPatient?.id) return
    if (!aiSummary.trim()) return

    setSendingToNotes(true)
    try {
      await apiPost(`/notes/${selectedPatient.id}`, { text: aiSummary })
      const data = await apiGet(`/notes/${selectedPatient.id}`)
      setNotes(Array.isArray(data) ? data : [])
    } finally {
      setSendingToNotes(false)
    }
  }

  return (
    <div style={{ padding: 24, color: "white" }}>
      <h1 className="page-title">AI Clinical Decision Support</h1>

      {error && (
        <div style={{ color: "#fca5a5", marginBottom: 16 }}>{error}</div>
      )}

      <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: 18 }}>
        <div className="med-card" style={{ padding: 18 }}>
          <div style={{ marginBottom: 12, fontWeight: 700 }}>Patient Context</div>

          <select
            value={selectedPatientId}
            onChange={(e) => setSelectedPatientId(e.target.value)}
            style={inputStyle}
          >
            <option value="">Select patient</option>
            {patients.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name} ({p.id})
              </option>
            ))}
          </select>

          <div style={{ marginTop: 16, marginBottom: 8, fontWeight: 700 }}>
            Clinical Complaint Input
          </div>

          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            style={textareaStyle}
          />

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginTop: 12 }}>
            <input value={hr} onChange={(e) => setHr(e.target.value)} style={inputStyle} placeholder="HR" />
            <input value={sbp} onChange={(e) => setSbp(e.target.value)} style={inputStyle} placeholder="SBP" />
            <input value={temp} onChange={(e) => setTemp(e.target.value)} style={inputStyle} placeholder="Temp" />
            <input value={spo2} onChange={(e) => setSpo2(e.target.value)} style={inputStyle} placeholder="SpO2" />
          </div>

          <div style={{ display: "flex", gap: 10, flexWrap: "wrap", marginTop: 16 }}>
            <button onClick={generateClinicalSummary} style={buttonBlue}>
              Generate Clinical Summary
            </button>

            <button onClick={sendSummaryToNotes} style={buttonGreen}>
              {sendingToNotes ? "Sending..." : "Send Summary to Notes"}
            </button>

            <button
              onClick={() => navigate(`/reports?patientId=${selectedPatient?.id ?? ""}`)}
              style={buttonPink}
            >
              Send Summary to Reports
            </button>
          </div>

          {selectedPatient && (
            <div style={{ marginTop: 18, padding: 14, border: "1px solid #374151", borderRadius: 10 }}>
              <div style={{ fontWeight: 700 }}>{selectedPatient.name}</div>
              <div style={{ opacity: 0.75, marginTop: 6 }}>Department: {selectedPatient.department ?? "N/A"}</div>
              <div style={{ opacity: 0.75, marginTop: 6 }}>Condition: {selectedPatient.condition ?? "N/A"}</div>

            </div>
          )}

          <div style={{ display: "grid", gap: 18, marginTop: 18, marginBottom: 18, border: "2px solid #38bdf8", padding: 12, borderRadius: 12 }}>
            <VisitTimelineCard items={timelineItems} />
            <SmartOrdersCard orders={smartOrders} />
            <DecisionEngineCard result={decisionResult} />
            <DigitalSignatureCard signature={digitalSignature} />
          </div>

          {aiSummary && (
            <div className="med-card" style={{ marginTop: 18, padding: 16 }}>
              <h3>AI Clinical Summary</h3>
              <pre style={{ whiteSpace: "pre-wrap" }}>{aiSummary}</pre>
            </div>
          )}

          <div className="med-card" style={{ marginTop: 18, padding: 16 }}>
            <h3>Patient Notes</h3>
            {notes.length === 0 ? (
              <div style={{ opacity: 0.75 }}>No notes for this patient.</div>
            ) : (
              <div style={{ display: "grid", gap: 10 }}>
                {notes.map((note) => (
                  <div key={note.id} style={{ border: "1px solid #374151", borderRadius: 10, padding: 12 }}>
                    {note.text}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div style={{ display: "grid", gap: 18 }}>
          <div className="med-card" style={{ padding: 16 }}>
            <div style={{ fontSize: 18, fontWeight: 700, marginBottom: 12 }}>Clinical Impression</div>
            <div style={summaryTextStyle}>{result.impression}</div>
          </div>

          <div className="med-card" style={{ padding: 16 }}>
            <div style={{ fontSize: 18, fontWeight: 700, marginBottom: 12 }}>Recommended Plan</div>
            <div style={summaryTextStyle}>{result.recommendedPlan}</div>
          </div>

          <div className="med-card" style={{ padding: 16 }}>
            <div style={{ fontSize: 18, fontWeight: 700, marginBottom: 12 }}>Next Step Summary</div>
            <div style={summaryTextStyle}>{result.nextStepSummary}</div>
          </div>
        </div>
      </div>
    </div>
  )
}

const inputStyle: React.CSSProperties = {
  width: "100%",
  padding: "10px 12px",
  borderRadius: 10,
  border: "1px solid #334155",
  background: "#020617",
  color: "white",
}

const textareaStyle: React.CSSProperties = {
  width: "100%",
  minHeight: 140,
  padding: "12px",
  borderRadius: 10,
  border: "1px solid #334155",
  background: "#020617",
  color: "white",
}

const summaryTextStyle: React.CSSProperties = {
  lineHeight: 1.7,
  opacity: 0.95,
}

const buttonBlue: React.CSSProperties = {
  padding: "12px 16px",
  borderRadius: 10,
  border: "1px solid #38bdf8",
  background: "#0284c7",
  color: "white",
  cursor: "pointer",
  fontWeight: 700,
}

const buttonGreen: React.CSSProperties = {
  padding: "12px 16px",
  borderRadius: 10,
  border: "1px solid #22c55e",
  background: "#166534",
  color: "white",
  cursor: "pointer",
  fontWeight: 700,
}

const buttonPink: React.CSSProperties = {
  padding: "12px 16px",
  borderRadius: 10,
  border: "1px solid #f472b6",
  background: "#be185d",
  color: "white",
  cursor: "pointer",
  fontWeight: 700,
}
