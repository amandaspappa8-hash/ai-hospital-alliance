import { useEffect, useState } from "react"
import { useSearchParams } from "react-router-dom"
import hospitalLogo from "../assets/hospital-logo.png"
import { apiGet } from "@/lib/api"
import { mintMedicalReportNFT } from "@/lib/medicalReportBlockchain"

type ReportDraft = {
  patientId?: string
  patientName?: string
  title?: string
  status?: string
  body?: string
  hospitalName?: string
  doctorName?: string
  visitDate?: string
}

type Patient = {
  id: string
  name: string
  age?: number
  gender?: string
  phone?: string
  condition?: string
  department?: string
  status?: string
}

type Note = {
  id: number
  text: string
}

type Order = {
  id: number
  item: string
  type?: string
  priority?: string
  status?: string
}

type VitalSigns = {
  temperature: string
  bloodPressure: string
  heartRate: string
  oxygenSaturation: string
  respiratoryRate: string
}

const exportClinicalPDF = () => {
  const element = document.getElementById("clinical-report")
  if (!element) {
    alert("Clinical report not found")
    return
  }

  const printWindow = window.open("", "_blank", "width=1100,height=1400")
  if (!printWindow) {
    alert("Popup blocked. Please allow popups.")
    return
  }

  printWindow.document.write(`
    <html>
      <head>
        <title>Clinical Report</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            margin: 24px;
            color: #111827;
            background: white;
          }
          #print-root {
            width: 100%;
          }
          .avoid-break {
            page-break-inside: avoid;
            break-inside: avoid;
          }
          @media print {
            body {
              margin: 0;
              padding: 14px;
            }
          }
        </style>
      </head>
      <body>
        <div id="print-root">${element.innerHTML}</div>
      </body>
    </html>
  `)

  printWindow.document.close()
  printWindow.focus()

  setTimeout(() => {
    printWindow.print()
  }, 500)
}

function getMockVitalSigns(patient: Patient): VitalSigns {
  const condition = String(patient.condition ?? "").toLowerCase()
  const status = String(patient.status ?? "").toLowerCase()

  if (condition.includes("chest")) {
    return {
      temperature: "37.2 °C",
      bloodPressure: "145/92 mmHg",
      heartRate: "104 bpm",
      oxygenSaturation: "95%",
      respiratoryRate: "22/min",
    }
  }

  if (condition.includes("fever")) {
    return {
      temperature: "38.6 °C",
      bloodPressure: "118/76 mmHg",
      heartRate: "102 bpm",
      oxygenSaturation: "97%",
      respiratoryRate: "20/min",
    }
  }

  if (condition.includes("oxygen") || status.includes("critical")) {
    return {
      temperature: "37.8 °C",
      bloodPressure: "132/84 mmHg",
      heartRate: "110 bpm",
      oxygenSaturation: "89%",
      respiratoryRate: "26/min",
    }
  }

  return {
    temperature: "36.9 °C",
    bloodPressure: "120/80 mmHg",
    heartRate: "78 bpm",
    oxygenSaturation: "98%",
    respiratoryRate: "16/min",
  }
}

function buildClinicalImpression(patient: Patient, notes: Note[], orders: Order[]) {
  const department = patient.department ?? "General Medicine"
  const condition = patient.condition ?? "Unspecified condition"
  const hasUrgentOrder = orders.some(
    (o) => String(o.priority ?? "").toLowerCase() === "urgent"
  )
  const hasNotes = notes.length > 0

  return `Patient is currently under ${department} care with a presenting condition of ${condition}. ${
    hasNotes
      ? "Clinical notes indicate that the patient has already undergone initial assessment and documentation."
      : "No detailed narrative notes are currently available in the chart."
  } ${
    hasUrgentOrder
      ? "At least one urgent clinical order is active and should be prioritized."
      : "Current listed orders appear routine and should continue to be monitored."
  } Overall, the patient requires continued physician review, monitoring of response to treatment, and reassessment according to clinical workflow.`
}

function buildRecommendations(patient: Patient, orders: Order[]) {
  const condition = String(patient.condition ?? "").toLowerCase()
  const department = patient.department ?? "Clinical Department"

  const base = [
    "Continue routine clinical monitoring and reassessment.",
    "Review all pending orders and confirm completion status.",
    "Update physician notes after the next clinical evaluation.",
  ]

  if (condition.includes("chest")) {
    base.unshift("Rule out acute cardiac cause and monitor for symptom progression.")
  } else if (condition.includes("fever")) {
    base.unshift("Investigate possible infectious source and monitor temperature trend.")
  } else if (condition.includes("oxygen")) {
    base.unshift("Closely monitor oxygen saturation and respiratory stability.")
  } else {
    base.unshift(`Maintain protocol-based follow-up under ${department}.`)
  }

  if (orders.length === 0) {
    base.push("Consider entering diagnostic or supportive orders if clinically indicated.")
  }

  return base
}

export default function ReportsPage() {
  const [searchParams] = useSearchParams()
  const patientIdFromUrl = searchParams.get("patientId") ?? ""
  const [patients, setPatients] = useState<Patient[]>([])
  const [selectedPatientId, setSelectedPatientId] = useState(patientIdFromUrl || "P-1001")
  const [loadingPatients, setLoadingPatients] = useState(true)
  const [loadingReport, setLoadingReport] = useState(true)
  const [error, setError] = useState("")

  const [report, setReport] = useState<ReportDraft>({
    patientId: "P-1001",
    patientName: "Loading...",
    title: "Official Clinical Summary",
    status: "draft",
    body: "Generating report...",
    hospitalName: "AI Hospital Alliance",
    doctorName: "Dr. Mohammed Al-Fallah, PharmD",
    visitDate: new Date().toLocaleString(),
  })

  const [patient, setPatient] = useState<Patient | null>(null)
  const [notes, setNotes] = useState<Note[]>([])
  const [orders, setOrders] = useState<Order[]>([])
  const [vitals, setVitals] = useState<VitalSigns | null>(null)
  const [clinicalImpression, setClinicalImpression] = useState("")
  const [recommendations, setRecommendations] = useState<string[]>([])
  const [mintingBlockchain, setMintingBlockchain] = useState(false)
  const [mintResult, setMintResult] = useState("")

  useEffect(() => {
    if (patientIdFromUrl) {
      setSelectedPatientId(patientIdFromUrl)
    }
  }, [patientIdFromUrl])

  useEffect(() => {
    async function loadPatients() {
      try {
        setLoadingPatients(true)
        const data = await apiGet<Patient[]>("/patients")
        const rows = Array.isArray(data) ? data : []
        setPatients(rows)

        if (rows.length > 0) {
          setSelectedPatientId((current) => {
            const exists = rows.some((p) => p.id === current)
            return exists ? current : rows[0].id
          })
        }
      } catch (err) {
        console.error(err)
        setError("Failed to load patients list")
        setPatients([])
      } finally {
        setLoadingPatients(false)
      }
    }

    loadPatients()
  }, [])


  async function handleMintToBlockchain() {
    try {
      if (!patient) {
        alert("Patient data is not loaded yet")
        return
      }

      setMintingBlockchain(true)
      setMintResult("")

      const patientAddress = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
      const reportId = report.patientId || patient.id || "REPORT-UNKNOWN"
      const reportHash = btoa(
        JSON.stringify({
          patientId: patient.id,
          patientName: patient.name,
          title: report.title,
          body: report.body,
          visitDate: report.visitDate,
        })
      ).slice(0, 64)

      const metadataURI = `local://report/${reportId}`

      const result = await mintMedicalReportNFT({
        patient: patientAddress,
        reportId,
        reportHash,
        metadataURI,
      })

      setMintResult(
        `Blockchain mint success | tx: ${result.txHash} | total tokens: ${result.totalTokens}`
      )
    } catch (err: any) {
      console.error(err)
      setMintResult(err?.message || "Blockchain mint failed")
    } finally {
      setMintingBlockchain(false)
    }
  }


  useEffect(() => {
    let cancelled = false

    async function loadReport() {
      if (!selectedPatientId) return

      try {
        setLoadingReport(true)
        setError("")

        const draftKey = `AI_REPORT_DRAFT_${selectedPatientId}`
        const rawDraft = localStorage.getItem(draftKey)

        let parsed: ReportDraft | null = null
        if (rawDraft) {
          try {
            parsed = JSON.parse(rawDraft) as ReportDraft
          } catch (err) {
            console.error("Invalid patient draft:", err)
          }
        }

        const [currentPatient, currentNotes, currentOrders] = await Promise.all([
          apiGet<Patient>(`/patients/${selectedPatientId}`),
          apiGet<Note[]>(`/notes/${selectedPatientId}`),
          apiGet<Order[]>(`/orders/${selectedPatientId}`),
        ])

        if (cancelled) return

        const safeNotes = Array.isArray(currentNotes) ? currentNotes : []
        const safeOrders = Array.isArray(currentOrders) ? currentOrders : []

        setPatient(currentPatient)
        setNotes(safeNotes)
        setOrders(safeOrders)

        const currentVitals = getMockVitalSigns(currentPatient)
        const currentImpression = buildClinicalImpression(
          currentPatient,
          safeNotes,
          safeOrders
        )
        const currentRecommendations = buildRecommendations(
          currentPatient,
          safeOrders
        )

        setVitals(currentVitals)
        setClinicalImpression(currentImpression)
        setRecommendations(currentRecommendations)

        setReport({
          patientId: parsed?.patientId ?? currentPatient.id,
          patientName: parsed?.patientName ?? currentPatient.name,
          title: parsed?.title ?? "Official Clinical Summary",
          status: parsed?.status ?? (parsed ? "official-draft" : "auto-generated"),
          body: parsed?.body ?? currentImpression,
          hospitalName: parsed?.hospitalName ?? "AI Hospital Alliance",
          doctorName: parsed?.doctorName ?? "Dr. Mohammed Al-Fallah, PharmD",
          visitDate: parsed?.visitDate ?? new Date().toLocaleString(),
        })
      } catch (err) {
        console.error(err)
        if (cancelled) return
        setError("Failed to generate report")
        setPatient(null)
        setNotes([])
        setOrders([])
        setVitals(null)
        setClinicalImpression("")
        setRecommendations([])
      } finally {
        if (!cancelled) {
          setLoadingReport(false)
        }
      }
    }

    loadReport()

    return () => {
      cancelled = true
    }
  }, [selectedPatientId])

  return (
    <div style={{ padding: 24, color: "white" }}>
      <h1 style={{ fontSize: 30, marginBottom: 8 }}>Reports</h1>
      <p style={{ opacity: 0.8, marginBottom: 20 }}>
        Official clinical and AI-generated reports
      </p>

      <div
        style={{
          display: "flex",
          gap: 12,
          alignItems: "center",
          flexWrap: "wrap",
          marginBottom: 20,
        }}
      >
        <select
          value={selectedPatientId}
          onChange={(e) => setSelectedPatientId(e.target.value)}
          disabled={loadingPatients || patients.length === 0}
          style={{
            minWidth: 280,
            padding: "10px 12px",
            borderRadius: 8,
            border: "1px solid #374151",
            background: "#0f172a",
            color: "white",
          }}
        >
          {patients.length === 0 ? (
            <option value="">No patients available</option>
          ) : (
            patients.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name} ({p.id})
              </option>
            ))
          )}
        </select>

        <button
          onClick={exportClinicalPDF}
          style={{
            background: "#2563eb",
            color: "#fff",
            padding: "10px 16px",
            borderRadius: 8,
            border: "none",
            cursor: "pointer",
            fontWeight: 700,
          }}
        >
          Print / Save PDF
        </button>

        <button
          onClick={handleMintToBlockchain}
          disabled={mintingBlockchain || loadingReport || !patient}
          style={{
            background: mintingBlockchain ? "#475569" : "#059669",
            color: "#fff",
            padding: "10px 16px",
            borderRadius: 8,
            border: "none",
            cursor: mintingBlockchain ? "not-allowed" : "pointer",
            fontWeight: 700,
            opacity: mintingBlockchain || loadingReport || !patient ? 0.7 : 1,
          }}
        >
          {mintingBlockchain ? "Minting to Blockchain..." : "Mint Medical Report NFT"}
        </button>
      </div>

      {error && (
        <div style={{ color: "#fecaca", marginBottom: 16 }}>{error}</div>
      )}

      {mintResult && (
        <div
          style={{
            marginBottom: 16,
            padding: 12,
            borderRadius: 10,
            background: "#052e16",
            color: "#bbf7d0",
            border: "1px solid #166534",
            wordBreak: "break-word",
          }}
        >
          {mintResult}
        </div>
      )}

      <div
        id="clinical-report"
        style={{
          background: "white",
          color: "#111827",
          borderRadius: 18,
          padding: 28,
          maxWidth: 1000,
          boxShadow: "0 12px 30px rgba(15, 23, 42, 0.12)",
        }}
      >
        <div
          className="avoid-break"
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            borderBottom: "3px solid #dbeafe",
            paddingBottom: 18,
            marginBottom: 24,
            gap: 16,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <img
              src={hospitalLogo}
              alt="Hospital Logo"
              style={{ height: 64, width: 64, objectFit: "contain" }}
            />
            <div>
              <div style={{ fontSize: 28, fontWeight: 800, color: "#0f172a" }}>
                {report.hospitalName}
              </div>
              <div style={{ color: "#475569", fontSize: 15 }}>
                Advanced Clinical Decision Report
              </div>
            </div>
          </div>

          <div
            style={{
              textAlign: "right",
              fontSize: 14,
              background: "#f8fafc",
              border: "1px solid #e2e8f0",
              borderRadius: 12,
              padding: 12,
              minWidth: 240,
            }}
          >
            <div>
              <strong>Doctor:</strong> {report.doctorName}
            </div>
            <div>
              <strong>Date:</strong> {report.visitDate}
            </div>
            <div>
              <strong>Status:</strong> {report.status}
            </div>
          </div>
        </div>

        <div className="avoid-break" style={{ marginBottom: 22 }}>
          <div style={{ fontSize: 24, fontWeight: 800, marginBottom: 6 }}>
            {report.title}
          </div>
          <div style={{ color: "#475569" }}>
            Patient: {report.patientName} ({report.patientId})
          </div>
        </div>

        <div
          className="avoid-break"
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
            gap: 14,
            marginBottom: 22,
          }}
        >
          <div
            style={{
              background: "#f8fafc",
              border: "1px solid #e2e8f0",
              borderRadius: 14,
              padding: 16,
            }}
          >
            <div style={{ fontWeight: 800, marginBottom: 12, color: "#0f172a" }}>
              Patient Overview
            </div>
            <div style={{ display: "grid", gap: 8, fontSize: 14 }}>
              <div><strong>Name:</strong> {patient?.name ?? "—"}</div>
              <div><strong>ID:</strong> {patient?.id ?? "—"}</div>
              <div><strong>Age:</strong> {patient?.age ?? "—"}</div>
              <div><strong>Gender:</strong> {patient?.gender ?? "—"}</div>
              <div><strong>Phone:</strong> {patient?.phone ?? "—"}</div>
              <div><strong>Department:</strong> {patient?.department ?? "—"}</div>
              <div><strong>Condition:</strong> {patient?.condition ?? "—"}</div>
              <div><strong>Status:</strong> {patient?.status ?? "—"}</div>
            </div>
          </div>

          <div
            style={{
              background: "#eff6ff",
              border: "1px solid #bfdbfe",
              borderRadius: 14,
              padding: 16,
            }}
          >
            <div style={{ fontWeight: 800, marginBottom: 12, color: "#1d4ed8" }}>
              Vital Signs
            </div>
            <div style={{ display: "grid", gap: 10, fontSize: 14 }}>
              <div><strong>Temperature:</strong> {vitals?.temperature ?? "—"}</div>
              <div><strong>Blood Pressure:</strong> {vitals?.bloodPressure ?? "—"}</div>
              <div><strong>Heart Rate:</strong> {vitals?.heartRate ?? "—"}</div>
              <div><strong>O₂ Saturation:</strong> {vitals?.oxygenSaturation ?? "—"}</div>
              <div><strong>Respiratory Rate:</strong> {vitals?.respiratoryRate ?? "—"}</div>
            </div>
          </div>
        </div>

        <div
          className="avoid-break"
          style={{
            background: "#f8fafc",
            border: "1px solid #e5e7eb",
            borderRadius: 14,
            padding: 18,
            marginBottom: 18,
          }}
        >
          <div style={{ fontWeight: 800, marginBottom: 12, fontSize: 18 }}>
            Clinical Notes
          </div>
          <div style={{ display: "grid", gap: 10 }}>
            {loadingReport ? (
              <div>Loading notes...</div>
            ) : notes.length === 0 ? (
              <div>No clinical notes recorded.</div>
            ) : (
              notes.map((note) => (
                <div
                  key={note.id}
                  style={{
                    background: "white",
                    border: "1px solid #e5e7eb",
                    borderRadius: 10,
                    padding: 12,
                    lineHeight: 1.6,
                  }}
                >
                  {note.text}
                </div>
              ))
            )}
          </div>
        </div>

        <div
          className="avoid-break"
          style={{
            background: "#f8fafc",
            border: "1px solid #e5e7eb",
            borderRadius: 14,
            padding: 18,
            marginBottom: 18,
          }}
        >
          <div style={{ fontWeight: 800, marginBottom: 12, fontSize: 18 }}>
            Clinical Orders
          </div>
          <div style={{ display: "grid", gap: 10 }}>
            {loadingReport ? (
              <div>Loading orders...</div>
            ) : orders.length === 0 ? (
              <div>No clinical orders recorded.</div>
            ) : (
              orders.map((order) => (
                <div
                  key={order.id}
                  style={{
                    display: "grid",
                    gridTemplateColumns: "minmax(0, 1.5fr) repeat(3, minmax(0, 1fr))",
                    gap: 10,
                    background: "white",
                    border: "1px solid #e5e7eb",
                    borderRadius: 10,
                    padding: 12,
                    fontSize: 14,
                  }}
                >
                  <div><strong>Item:</strong> {order.item}</div>
                  <div><strong>Type:</strong> {order.type ?? "—"}</div>
                  <div><strong>Priority:</strong> {order.priority ?? "—"}</div>
                  <div><strong>Status:</strong> {order.status ?? "—"}</div>
                </div>
              ))
            )}
          </div>
        </div>

        <div
          className="avoid-break"
          style={{
            background: "#fff7ed",
            border: "1px solid #fed7aa",
            borderRadius: 14,
            padding: 18,
            marginBottom: 18,
          }}
        >
          <div style={{ fontWeight: 800, marginBottom: 12, fontSize: 18, color: "#9a3412" }}>
            Clinical Impression
          </div>
          <div style={{ lineHeight: 1.8, whiteSpace: "pre-wrap" }}>
            {loadingReport ? "Generating clinical impression..." : clinicalImpression}
          </div>
        </div>

        <div
          className="avoid-break"
          style={{
            marginBottom: 18,
          }}
        >
          <div style={{ fontWeight: 800, marginBottom: 12, fontSize: 18 }}>
            Recommendation Boxes
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
              gap: 12,
            }}
          >
            {recommendations.map((item, index) => (
              <div
                key={index}
                style={{
                  background: index === 0 ? "#ecfeff" : "#f8fafc",
                  border: index === 0 ? "1px solid #a5f3fc" : "1px solid #e5e7eb",
                  borderRadius: 14,
                  padding: 16,
                  minHeight: 90,
                  display: "flex",
                  alignItems: "flex-start",
                  lineHeight: 1.6,
                }}
              >
                <div>
                  <div
                    style={{
                      fontWeight: 800,
                      marginBottom: 6,
                      color: index === 0 ? "#0f766e" : "#0f172a",
                    }}
                  >
                    Recommendation {index + 1}
                  </div>
                  <div>{item}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div
          className="avoid-break"
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "end",
            marginTop: 34,
            paddingTop: 22,
            borderTop: "2px dashed #cbd5e1",
            gap: 20,
          }}
        >
          <div>
            <div style={{ fontWeight: 800, marginBottom: 28 }}>
              Physician Signature: __________________________
            </div>
            <div>{report.doctorName}</div>
            <div style={{ color: "#64748b", fontSize: 14 }}>Attending Clinical Reviewer</div>
          </div>

          <div
            style={{
              border: "2px solid #93c5fd",
              color: "#1d4ed8",
              borderRadius: "999px",
              padding: "10px 18px",
              fontWeight: 800,
              fontSize: 14,
            }}
          >
            VERIFIED HOSPITAL COPY
          </div>
        </div>

        <div
          style={{
            marginTop: 28,
            fontSize: 12,
            color: "#64748b",
            textAlign: "center",
          }}
        >
          AI Hospital Alliance • Confidential Medical Document • Auto-generated clinical decision support format
        </div>
      </div>
    </div>
  )
}
