import { useEffect, useMemo, useState } from "react"
import { useNavigate, useSearchParams } from "react-router-dom"
import { apiGet, apiPost } from "@/lib/api"
import jsPDF from "jspdf"
import html2canvas from "html2canvas"
import QRCode from "qrcode"

type Patient = {
  id: string
  name: string
  department?: string
  status?: string
  age?: number
  gender?: string
  phone?: string
  condition?: string
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
  department?: string
  note?: string
}

type LabOrder = {
  id: string
  patientId: string
  patientName: string
  section: string
  tests: string[]
  priority: string
  status: string
  result?: string
}

type RadiologyOrder = {
  id: string
  patientId: string
  patientName: string
  section: string
  studies: string[]
  priority: string
  status: string
  studyUid?: string
  report?: string
}

type PacsStudy = {
  studyInstanceUID: string
  patientId: string
  patientName?: string
  modality?: string
  studyDate?: string
  studyDescription?: string
}

type TabKey = "overview" | "notes" | "orders"

type SuggestedOrder = {
  name: string
  priority: string
  category: string
}

type ClinicalRouteResponse = {
  chief_complaint: string
  triage_level: string
  urgency_score: number
  route_to: string[]
  suggested_orders: SuggestedOrder[]
  red_flags: string[]
  next_actions: string[]
  rationale: string[]
}

type ClinicalOrdersResponse = {
  patient_id: string
  clinical_route: ClinicalRouteResponse
  created_orders: Order[]
  skipped_existing_orders?: string[]
}

export default function PatientProfilePage() {
  const openPatientPacs = (studyUid?: string) => {
    const uid =
      patientPacsStudy?.studyInstanceUID ||
      studyUid ||
      latestRadiologyOrder?.studyUid ||
      ""

    if (!uid) {
      alert("No PACS study mapped for this patient yet")
      window.location.href = `/radiology?patientId=${selectedId}`
      return
    }

    window.open(
      `http://127.0.0.1:3005/viewer?StudyInstanceUIDs=${encodeURIComponent(uid)}`,
      "_blank",
      "noopener,noreferrer"
    )
  }

  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const patientIdFromUrl = searchParams.get("id") ?? ""

  const [patients, setPatients] = useState<Patient[]>([])
  const [selectedId, setSelectedId] = useState("")
  const [q, setQ] = useState("")
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [tab, setTab] = useState<TabKey>("overview")

  const [notes, setNotes] = useState<Note[]>([])
  const [noteText, setNoteText] = useState("")
  const [savingNote, setSavingNote] = useState(false)

  const [orders, setOrders] = useState<Order[]>([])
  const [labOrders, setLabOrders] = useState<LabOrder[]>([])
  const [radiologyOrders, setRadiologyOrders] = useState<RadiologyOrder[]>([])
  const [pacsStudies, setPacsStudies] = useState<PacsStudy[]>([])

  const [chiefComplaint, setChiefComplaint] = useState("chest pain")
  const [symptomsText, setSymptomsText] = useState("sweating, nausea, shortness of breath")
  const [ageInput, setAgeInput] = useState("58")
  const [genderInput, setGenderInput] = useState("male")
  const [aiLoading, setAiLoading] = useState(false)
  const [aiError, setAiError] = useState("")
  const [aiResult, setAiResult] = useState<ClinicalRouteResponse | null>(null)

  const [qrCode, setQrCode] = useState("")
  const [visitId, setVisitId] = useState("")

  const generateOfficialReport = async () => {
    if (!selected) return

    try {
      const notesData = await apiGet<Note[]>(`/notes/${selected.id}`)
      const ordersData = await apiGet<Order[]>(`/orders/${selected.id}`)
      const currentLabOrders = await apiGet<LabOrder[]>(`/labs/orders/${selected.id}`)
      const currentRadiologyOrders = await apiGet<RadiologyOrder[]>(`/radiology/orders/${selected.id}`)

      const notesText =
        Array.isArray(notesData) && notesData.length > 0
          ? notesData.map((n) => `- ${n.text}`).join("\n")
          : "No clinical notes recorded."

      const ordersText =
        Array.isArray(ordersData) && ordersData.length > 0
          ? ordersData
              .map(
                (o) =>
                  `- ${o.item} | Type: ${o.type ?? "N/A"} | Priority: ${o.priority ?? "N/A"} | Status: ${o.status ?? "Pending"}`
              )
              .join("\n")
          : "No clinical orders recorded."

      const labText =
        Array.isArray(currentLabOrders) && currentLabOrders.length > 0
          ? currentLabOrders
              .map(
                (o) =>
                  `- ${o.tests.join(", ")} | ${o.section} | ${o.priority} | ${o.status} | Result: ${o.result || "N/A"}`
              )
              .join("\n")
          : "No lab orders recorded."

      const radiologyText =
        Array.isArray(currentRadiologyOrders) && currentRadiologyOrders.length > 0
          ? currentRadiologyOrders
              .map(
                (o) =>
                  `- ${o.studies.join(", ")} | ${o.section} | ${o.priority} | ${o.status} | Report: ${o.report || "N/A"}`
              )
              .join("\n")
          : "No radiology orders recorded."

      const body = `Patient Name: ${selected.name}
Patient ID: ${selected.id}
Age: ${selected.age ?? "N/A"}
Gender: ${selected.gender ?? "N/A"}
Phone: ${selected.phone ?? "N/A"}
Condition: ${selected.condition ?? "N/A"}
Department: ${selected.department ?? "N/A"}
Patient Status: ${selected.status ?? "N/A"}

Clinical Notes:
${notesText}

Clinical Orders:
${ordersText}

Laboratory Orders:
${labText}

Radiology Orders:
${radiologyText}

Official Clinical Impression:
This official draft was generated from the patient profile view. It summarizes the currently available chart data, notes, clinical orders, lab orders, and radiology studies for physician review and final validation.`

      const draft = {
        patientId: selected.id,
        patientName: selected.name,
        title: "Official Clinical Summary",
        status: "official-draft",
        body,
        hospitalName: "AI Hospital Alliance",
        doctorName: "Dr. Mohammed Al-Fallah, PharmD",
        visitDate: new Date().toLocaleString(),
      }

      localStorage.setItem(`AI_REPORT_DRAFT_${selected.id}`, JSON.stringify(draft))
      window.location.href = `/reports?patientId=${selected.id}`
    } catch (err) {
      console.error("Failed to generate official report:", err)
      alert("Failed to generate official report")
    }
  }

  useEffect(() => {
    const id =
      "VIS-" +
      new Date().getFullYear() +
      "-" +
      Math.floor(Math.random() * 100000)

    setVisitId(id)

    QRCode.toDataURL(id).then((url) => {
      setQrCode(url)
    })
  }, [])

  useEffect(() => {
    apiGet<Patient[]>("/patients")
      .then((data) => {
        const rows = Array.isArray(data) ? data : []
        setPatients(rows)

        if (patientIdFromUrl) {
          setSelectedId(patientIdFromUrl)
        } else if (rows.length > 0) {
          setSelectedId(rows[0].id)
        }
      })
      .catch((err) => {
        console.error(err)
        setError("Failed to load patients")
      })
      .finally(() => setLoading(false))
  }, [patientIdFromUrl])

  const filtered = useMemo(() => {
    const query = q.trim().toLowerCase()
    return patients.filter((p) => {
      return (
        !query ||
        String(p.id ?? "").toLowerCase().includes(query) ||
        String(p.name ?? "").toLowerCase().includes(query) ||
        String(p.department ?? "").toLowerCase().includes(query) ||
        String(p.condition ?? "").toLowerCase().includes(query)
      )
    })
  }, [patients, q])

  const selected =
    patients.find((p) => p.id === selectedId) ||
    filtered[0] ||
    patients[0] ||
    null

  useEffect(() => {
    if (!selected?.id) return

    setAgeInput(String(selected.age ?? 58))
    setGenderInput(selected.gender ?? "male")

    Promise.all([
      apiGet<Note[]>(`/notes/${selected.id}`).catch(() => []),
      apiGet<Order[]>(`/orders/${selected.id}`).catch(() => []),
      apiGet<LabOrder[]>(`/labs/orders/${selected.id}`).catch(() => []),
      apiGet<RadiologyOrder[]>(`/radiology/orders/${selected.id}`).catch(() => []),
      apiGet<PacsStudy[]>("/pacs/studies").catch(() => []),
    ])
      .then(([notesData, ordersData, labData, radiologyData, pacsData]) => {
        setNotes(Array.isArray(notesData) ? notesData : [])
        setOrders(Array.isArray(ordersData) ? ordersData : [])
        setLabOrders(Array.isArray(labData) ? labData : [])
        setRadiologyOrders(Array.isArray(radiologyData) ? radiologyData : [])
        setPacsStudies(
          Array.isArray(pacsData)
            ? pacsData.filter((study) => study.patientId === selected.id)
            : []
        )
      })
      .catch((err) => {
        console.error(err)
      })
  }, [selected?.id])

  const exportClinicalPDF = async () => {
    const input = document.getElementById("clinical-report")
    if (!input) return

    const canvas = await html2canvas(input, { scale: 2 })
    const imgData = canvas.toDataURL("image/png")

    const pdf = new jsPDF("p", "mm", "a4")
    const imgWidth = 210
    const imgHeight = (canvas.height * imgWidth) / canvas.width

    pdf.addImage(imgData, "PNG", 0, 0, imgWidth, imgHeight)
    pdf.save(`Clinical_Report_${visitId || "report"}.pdf`)
  }

  async function addNote() {
    if (!selected?.id || !noteText.trim()) return
    setSavingNote(true)

    try {
      await apiPost(`/notes/${selected.id}`, { text: noteText.trim() })
      const data = await apiGet<Note[]>(`/notes/${selected.id}`)
      setNotes(Array.isArray(data) ? data : [])
      setNoteText("")
    } catch (err) {
      console.error(err)
    } finally {
      setSavingNote(false)
    }
  }

  async function runAIAndCreateOrders() {
    if (!selected?.id) return

    setAiLoading(true)
    setAiError("")

    try {
      const payload = {
        chief_complaint: chiefComplaint.trim(),
        symptoms: symptomsText.split(",").map((item) => item.trim()).filter(Boolean),
        age: ageInput.trim() ? Number(ageInput) : undefined,
        gender: genderInput.trim() || undefined,
      }

      const result = await apiPost<ClinicalOrdersResponse>(
        `/ai/clinical-route-and-create-orders/${selected.id}`,
        payload,
      )

      setAiResult(result.clinical_route)

      const latestOrders = await apiGet<Order[]>(`/orders/${selected.id}`)
      setOrders(Array.isArray(latestOrders) ? latestOrders : [])
    } catch (err) {
      console.error(err)
      setAiError("Failed to create AI draft orders")
    } finally {
      setAiLoading(false)
    }
  }

  const latestLabOrder = labOrders[0]
  const latestRadiologyOrder = radiologyOrders.length > 0 ? radiologyOrders[radiologyOrders.length - 1] : null
  const patientPacsStudy = pacsStudies.find((study) => study.patientId === selectedId) || pacsStudies[0] || null

  return (
    <div style={{ padding: "24px", color: "white" }}>
      <h1 style={{ fontSize: "30px", marginBottom: "8px" }}>Patient Profile</h1>
      <p style={{ opacity: 0.8, marginBottom: "20px" }}>
        Electronic Medical Record workspace
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "320px minmax(0,1fr)", gap: "20px", alignItems: "start" }}>
        <div style={{ background: "#111827", border: "1px solid #374151", borderRadius: "12px", padding: "16px" }}>
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Search patient..."
            style={inputStyle}
          />

          <div style={{ marginTop: "14px" }}>
            {loading && <div>Loading patients...</div>}
            {error && <div style={{ color: "#fca5a5" }}>{error}</div>}

            {!loading && !error && filtered.map((p) => {
              const active = selected?.id === p.id
              return (
                <div
                  key={p.id}
                  onClick={() => setSelectedId(p.id)}
                  style={{
                    padding: "12px",
                    marginBottom: "10px",
                    borderRadius: "10px",
                    cursor: "pointer",
                    border: "1px solid #374151",
                    background: active ? "#172033" : "#0b1220",
                  }}
                >
                  <div style={{ fontWeight: 700 }}>{p.name}</div>
                  <div style={{ opacity: 0.75, fontSize: "14px", marginTop: "4px" }}>
                    {p.id} • {p.department ?? "General"}
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        <div>
          {!selected ? (
            <div>No patient selected.</div>
          ) : (
            <>
              <div style={{ background: "#111827", border: "1px solid #374151", borderRadius: "12px", padding: "20px", marginBottom: "18px" }}>
                <div style={{ fontSize: "28px", fontWeight: 700 }}>{selected.name}</div>

                <div style={{ opacity: 0.8, marginTop: "6px" }}>
                  {selected.id} • {selected.department ?? "General"} • {selected.status ?? "Unknown"}
                </div>

                <div style={{ display: "flex", gap: "10px", flexWrap: "wrap", marginTop: "16px" }}>
                  <button
                    onClick={() => navigate(`/clinical-decision?patientId=${selected.id}&complaint=${encodeURIComponent(selected.condition ?? "")}`)}
                    style={{
                      padding: "12px 18px",
                      borderRadius: "10px",
                      border: "1px solid #38bdf8",
                      background: "#0284c7",
                      color: "white",
                      cursor: "pointer",
                      fontWeight: 700,
                    }}
                  >
                    Open AI Clinical Decision
                  </button>

                  <button
                    onClick={() => navigate(`/labs?patientId=${selected.id}`)}
                    style={{
                      padding: "12px 18px",
                      borderRadius: "10px",
                      border: "1px solid #22c55e",
                      background: "#166534",
                      color: "white",
                      cursor: "pointer",
                      fontWeight: 700,
                    }}
                  >
                    Open Labs
                  </button>

                  <button
                    onClick={() => window.location.href = `/radiology?patientId=${selected.id}`}
                    style={{
                      padding: "12px 18px",
                      borderRadius: "10px",
                      border: "1px solid #06b6d4",
                      background: "#0e7490",
                      color: "white",
                      cursor: "pointer",
                      fontWeight: 700,
                    }}
                  >
                    Open Radiology
                  </button>

                  <button
                    onClick={() => window.location.href = `/pharmacy?patientId=${selected.id}`}
                    style={{
                      padding: "10px 14px",
                      borderRadius: "10px",
                      border: "1px solid rgba(148,163,184,0.25)",
                      background: "rgba(15,23,42,0.65)",
                      color: "white",
                      cursor: "pointer",
                    }}
                  >
                    Open Pharmacy
                  </button>
                </div>

                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(180px,1fr))", gap: "12px", marginTop: "18px" }}>
                  <InfoCard label="Age" value={selected.age ?? "N/A"} />
                  <InfoCard label="Gender" value={selected.gender ?? "N/A"} />
                  <InfoCard label="Phone" value={selected.phone ?? "N/A"} />
                  <InfoCard label="Condition" value={selected.condition ?? "No active note"} />
                </div>
              </div>

              <div style={{ display: "flex", gap: "10px", marginBottom: "18px", flexWrap: "wrap" }}>
                <TabButton active={tab === "overview"} onClick={() => setTab("overview")}>Overview</TabButton>
                <TabButton active={tab === "notes"} onClick={() => setTab("notes")}>Notes</TabButton>
                <TabButton active={tab === "orders"} onClick={() => setTab("orders")}>Orders</TabButton>
              </div>

              {tab === "overview" && (
                <div style={{ display: "grid", gap: "18px" }}>
                  <Panel title="Integrated Clinical Snapshot">
                    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))", gap: "12px" }}>
                      <InfoCard label="Manual Orders" value={orders.length} />
                      <InfoCard label="Lab Orders" value={labOrders.length} />
                      <InfoCard label="Radiology Orders" value={radiologyOrders.length} />
                      <InfoCard label="Clinical Notes" value={notes.length} />
                    </div>

                    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(260px,1fr))", gap: "12px", marginTop: "14px" }}>
                      <div style={cardStyle}>
                        <div style={{ fontWeight: 700, marginBottom: "8px" }}>Latest Lab Result</div>
                        {latestLabOrder ? (
                          <>
                            <div>{latestLabOrder.tests.join(", ")}</div>
                            <div style={{ opacity: 0.75, marginTop: "6px" }}>{latestLabOrder.status}</div>
                            <div style={{ opacity: 0.85, marginTop: "8px" }}>
                              {latestLabOrder.result || "No result yet"}
                            </div>
                          </>
                        ) : (
                          <div style={{ opacity: 0.75 }}>No lab order yet.</div>
                        )}
                      </div>

                      <div style={cardStyle}>
                        <div style={{ fontWeight: 700, marginBottom: "8px" }}>Latest Radiology Report</div>
                        {latestRadiologyOrder ? (
                          <>
                            <div>{latestRadiologyOrder.studies.join(", ")}</div>
                            <div style={{ opacity: 0.75, marginTop: "6px" }}>{latestRadiologyOrder.status}</div>
                            <div style={{ opacity: 0.85, marginTop: "8px" }}>
                              {latestRadiologyOrder.report || "No report yet"}
                            </div>
                          </>
                        ) : (
                          <div style={{ opacity: 0.75 }}>No radiology order yet.</div>
                        )}
                      </div>
                    </div>
                  </Panel>

                  <Panel title="AI Clinical Workflow">
                    <div style={{ display: "grid", gap: "12px" }}>
                      <div>
                        <div style={labelStyle}>Chief Complaint</div>
                        <input value={chiefComplaint} onChange={(e) => setChiefComplaint(e.target.value)} style={inputStyle} />
                      </div>

                      <div>
                        <div style={labelStyle}>Symptoms (comma separated)</div>
                        <textarea value={symptomsText} onChange={(e) => setSymptomsText(e.target.value)} style={textareaStyle} />
                      </div>

                      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(160px,1fr))", gap: "12px" }}>
                        <div>
                          <div style={labelStyle}>Age</div>
                          <input value={ageInput} onChange={(e) => setAgeInput(e.target.value)} style={inputStyle} />
                        </div>
                        <div>
                          <div style={labelStyle}>Gender</div>
                          <input value={genderInput} onChange={(e) => setGenderInput(e.target.value)} style={inputStyle} />
                        </div>
                      </div>

                      <button onClick={runAIAndCreateOrders} style={buttonStyle}>
                        {aiLoading ? "Processing..." : "Run AI + Create Draft Orders"}
                      </button>

                      {aiError && <div style={{ color: "#fca5a5" }}>{aiError}</div>}
                    </div>
                  </Panel>

                  {aiResult && (
                    <>
                      <Panel title="AI Triage Result">
                        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(180px,1fr))", gap: "12px" }}>
                          <InfoCard label="Triage Level" value={aiResult.triage_level} />
                          <InfoCard label="Urgency Score" value={aiResult.urgency_score} />
                          <InfoCard label="Chief Complaint" value={aiResult.chief_complaint} />
                        </div>
                      </Panel>

                      <Panel title="Route To">
                        <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
                          {aiResult.route_to.map((item) => (
                            <span key={item} style={pillStyle}>{item}</span>
                          ))}
                        </div>
                      </Panel>

                      <Panel title="Suggested Orders">
                        <div style={{ display: "grid", gap: "10px" }}>
                          {aiResult.suggested_orders.map((item) => (
                            <div key={item.name} style={cardStyle}>
                              <div style={{ fontWeight: 700 }}>{item.name}</div>
                              <div style={{ opacity: 0.8, marginTop: "4px" }}>
                                {item.priority} • {item.category}
                              </div>
                            </div>
                          ))}
                        </div>
                      </Panel>
                    </>
                  )}

                  <Panel title="Clinical Report PDF">
                    <button onClick={exportClinicalPDF} style={buttonStyle}>
                      Export Clinical Report PDF
                    </button>

                    <div
                      id="clinical-report"
                      style={{
                        marginTop: "18px",
                        background: "white",
                        color: "#111827",
                        padding: "40px",
                        borderRadius: "12px",
                        position: "relative",
                        width: "800px",
                        maxWidth: "100%",
                        overflow: "hidden",
                      }}
                    >
                      <div
                        style={{
                          position: "absolute",
                          top: "38%",
                          left: "16%",
                          fontSize: "76px",
                          color: "#e5e7eb",
                          transform: "rotate(-30deg)",
                          opacity: 0.3,
                          fontWeight: "bold",
                          pointerEvents: "none",
                        }}
                      >
                        AI HOSPITAL
                      </div>

                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", borderBottom: "2px solid #e5e7eb", paddingBottom: "16px" }}>
                        <div>
                          <div style={{ fontSize: "28px", fontWeight: 800 }}>AI Hospital Alliance</div>
                          <div style={{ color: "#6b7280", marginTop: "4px" }}>Clinical Medical Report</div>
                          <div style={{ color: "#6b7280", marginTop: "4px" }}>Department: {selected.department ?? "General Medicine"}</div>
                        </div>

                        <div style={{ textAlign: "right" }}>
                          {qrCode ? <img src={qrCode} style={{ height: 90 }} /> : null}
                          <div style={{ fontSize: "10px", marginTop: "6px" }}>Scan Verification</div>
                        </div>
                      </div>

                      <div style={{ display: "flex", justifyContent: "space-between", marginTop: "16px", fontSize: "14px" }}>
                        <div><b>Visit ID:</b> {visitId}</div>
                        <div><b>Date:</b> {new Date().toLocaleDateString()}</div>
                      </div>

                      <div
                        style={{
                          display: "grid",
                          gridTemplateColumns: "1fr 1fr",
                          gap: "30px",
                          marginTop: "30px",
                        }}
                      >
                        <div>
                          <p><b>Patient Name:</b> {selected.name}</p>
                          <p><b>Age:</b> {selected.age ?? "N/A"}</p>
                          <p><b>Gender:</b> {selected.gender ?? "N/A"}</p>
                          <p><b>Phone:</b> {selected.phone ?? "N/A"}</p>
                        </div>

                        <div>
                          <p><b>Department:</b> {selected.department ?? "General"}</p>
                          <p><b>Status:</b> {selected.status ?? "Unknown"}</p>
                          <p><b>Condition:</b> {selected.condition ?? "N/A"}</p>
                          <p><b>Patient ID:</b> {selected.id}</p>
                        </div>
                      </div>

                      <div style={{ marginTop: "28px" }}>
                        <div style={{ fontSize: "18px", fontWeight: 700, marginBottom: "8px" }}>Clinical Impression</div>
                        <div style={{ lineHeight: 1.7 }}>
                          {aiResult
                            ? `Patient triage level is ${aiResult.triage_level} with urgency score ${aiResult.urgency_score}. Chief complaint: ${aiResult.chief_complaint}.`
                            : "AI generated clinical summary will appear here after running the AI workflow."}
                        </div>
                      </div>

                      <div style={{ marginTop: "24px" }}>
                        <div style={{ fontSize: "18px", fontWeight: 700, marginBottom: "8px" }}>Laboratory Summary</div>
                        <div style={{ lineHeight: 1.7 }}>
                          {latestLabOrder
                            ? `${latestLabOrder.tests.join(", ")} — ${latestLabOrder.status} — ${latestLabOrder.result || "No result yet"}`
                            : "No laboratory data yet."}
                        </div>
                      </div>

                      <div style={{ marginTop: "24px" }}>
                        <div style={{ fontSize: "18px", fontWeight: 700, marginBottom: "8px" }}>Radiology Summary</div>
                        <div style={{ lineHeight: 1.7 }}>
                          {latestRadiologyOrder
                            ? `${latestRadiologyOrder.studies.join(", ")} — ${latestRadiologyOrder.status} — ${latestRadiologyOrder.report || "No report yet"}`
                            : "No radiology data yet."}
                        </div>
                      </div>

                      <div style={{ marginTop: "60px" }}>
                        <p style={{ fontSize: 12, color: "#666" }}>Doctor Digital Signature</p>

                        <img
                          src="/assets/sign.png"
                          style={{ height: 60, marginTop: 10 }}
                          onError={(e) => {
                            ;(e.currentTarget as HTMLImageElement).style.display = "none"
                          }}
                        />

                        <div style={{ borderTop: "1px solid #000", width: 220, marginTop: 10 }}></div>

                        <p style={{ fontWeight: "bold", marginTop: 5 }}>
                          Dr Mohammed Elfallah
                        </p>
                      </div>
                    </div>
                  </Panel>
                </div>
              )}

              {tab === "notes" && (
                <Panel title="Clinical Notes">
                  <textarea
                    value={noteText}
                    onChange={(e) => setNoteText(e.target.value)}
                    placeholder="Write note for this patient..."
                    style={textareaStyle}
                  />

                  <button onClick={addNote} style={buttonStyle}>
                    {savingNote ? "Saving..." : "Add Note"}
                  </button>

                  <div style={{ marginTop: "18px" }}>
                    {notes.length === 0 ? (
                      <div style={{ opacity: 0.75 }}>No notes for this patient yet.</div>
                    ) : (
                      <div style={{ display: "grid", gap: "10px" }}>
                        {notes.map((note) => (
                          <div key={note.id} style={cardStyle}>{note.text}</div>
                        ))}
                      </div>
                    )}
                  </div>
                </Panel>
              )}

              {tab === "orders" && (
                <div style={{ display: "grid", gap: "18px" }}>
                  <Panel title="Manual Clinical Orders">
                    {orders.length === 0 ? (
                      <div style={{ opacity: 0.75 }}>No manual orders for this patient yet.</div>
                    ) : (
                      <div style={{ display: "grid", gap: "10px" }}>
                        {orders.map((order) => (
                          <div key={order.id} style={cardStyle}>
                            <div style={{ fontWeight: 700 }}>#{order.id} — {order.type}</div>
                            <div style={{ opacity: 0.82, marginTop: "4px" }}>
                              {order.department} • {order.status}
                            </div>
                            {order.note && <div style={{ opacity: 0.75, marginTop: "6px" }}>{order.note}</div>}
                          </div>
                        ))}
                      </div>
                    )}
                  </Panel>

                  <Panel title="Laboratory Orders">
                    {labOrders.length === 0 ? (
                      <div style={{ opacity: 0.75 }}>No lab orders for this patient yet.</div>
                    ) : (
                      <div style={{ display: "grid", gap: "10px" }}>
                        {labOrders.map((order) => (
                          <div key={order.id} style={cardStyle}>
                            <div style={{ fontWeight: 700 }}>{order.id} — {order.tests.join(", ")}</div>
                            <div style={{ opacity: 0.82, marginTop: "4px" }}>
                              {order.section} • {order.priority} • {order.status}
                            </div>
                            <div style={{ opacity: 0.75, marginTop: "6px" }}>
                              Result: {order.result || "Not available yet"}
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </Panel>

                  <Panel title="Radiology Orders">
                    {radiologyOrders.length === 0 ? (
                      <div style={{ opacity: 0.75 }}>No radiology orders for this patient yet.</div>
                    ) : (
                      <div style={{ display: "grid", gap: "10px" }}>
                        {radiologyOrders.map((order) => (
                          <div key={order.id} style={cardStyle}>
                            <div style={{ fontWeight: 700 }}>{order.id} — {order.studies.join(", ")}</div>
                            <div style={{ opacity: 0.82, marginTop: "4px" }}>
                              {order.section} • {order.priority} • {order.status}
                            </div>
                            <div style={{ opacity: 0.75, marginTop: "6px" }}>
                              Report: {order.report || "Not available yet"}
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </Panel>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  )
}

function TabButton({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: "10px 14px",
        borderRadius: "10px",
        border: "1px solid #374151",
        background: active ? "#166534" : "#111827",
        color: "white",
        cursor: "pointer",
      }}
    >
      {children}
    </button>
  )
}

function InfoCard({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div style={{ background: "#0b1220", border: "1px solid #374151", borderRadius: "10px", padding: "14px" }}>
      <div style={{ opacity: 0.72, fontSize: "14px" }}>{label}</div>
      <div style={{ marginTop: "8px", fontWeight: 700 }}>{value}</div>
    </div>
  )
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div style={{ background: "#111827", border: "1px solid #374151", borderRadius: "12px", padding: "16px" }}>
      <div style={{ fontSize: "18px", fontWeight: 700, marginBottom: "12px" }}>{title}</div>
      {children}
    </div>
  )
}

const inputStyle: React.CSSProperties = {
  width: "100%",
  padding: "10px 12px",
  borderRadius: "10px",
  border: "1px solid #374151",
  background: "#030712",
  color: "white",
}

const textareaStyle: React.CSSProperties = {
  width: "100%",
  minHeight: "120px",
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

const labelStyle: React.CSSProperties = {
  marginBottom: "6px",
  opacity: 0.8,
  fontSize: "14px",
}

const pillStyle: React.CSSProperties = {
  padding: "8px 12px",
  borderRadius: "999px",
  background: "#166534",
  border: "1px solid #22c55e",
}

const cardStyle: React.CSSProperties = {
  padding: "12px",
  background: "#0b1220",
  border: "1px solid #374151",
  borderRadius: "10px",
}
