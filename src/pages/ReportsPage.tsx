import { useEffect, useState, useRef } from "react"
import { apiGet } from "@/lib/api"
import { getUser } from "@/lib/auth-storage"

type Report = { id: string; patient_id: string; title: string; type: string; status: string; body: string }
type Patient = { id: string; name: string; age: number; gender: string; condition: string; department: string; status: string }

const TYPE_COLOR: Record<string, string> = {
  Cardiology: "#ef4444", Clinical: "#3b82f6", ICU: "#06b6d4",
  Endocrine: "#f59e0b", Surgery: "#f97316", Neurology: "#a855f7",
  Pediatrics: "#fbbf24", Orthopedics: "#10b981",
}

const STATUS_COLOR: Record<string, string> = {
  Ready: "#4ade80", "In Progress": "#fbbf24", Draft: "#94a3b8",
}

export default function ReportsPage() {
  const user = getUser()
  const [reports, setReports] = useState<Report[]>([])
  const [patients, setPatients] = useState<Patient[]>([])
  const [loading, setLoading] = useState(true)
  const [selected, setSelected] = useState<Report | null>(null)
  const [filterType, setFilterType] = useState("All")
  const [filterStatus, setFilterStatus] = useState("All")
  const [search, setSearch] = useState("")
  const [generating, setGenerating] = useState(false)
  const printRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    Promise.all([
      apiGet<Report[]>("/reports").catch(() => []),
      apiGet<Patient[]>("/patients").catch(() => []),
    ]).then(([r, p]) => {
      setReports(Array.isArray(r) ? r : [])
      setPatients(Array.isArray(p) ? p : [])
    }).finally(() => setLoading(false))
  }, [])

  function getPatient(id: string) {
    return patients.find(p => p.id === id)
  }

  function printReport(report: Report) {
    const patient = getPatient(report.patient_id)
    const w = window.open("", "_blank")
    if (!w) return
    w.document.write(`
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>${report.title}</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: Arial, sans-serif; color: #1a1a1a; background: white; padding: 40px; }
    .header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #2563eb; }
    .logo { font-size: 22px; font-weight: 900; color: #2563eb; }
    .logo-sub { font-size: 11px; color: #64748b; letter-spacing: 2px; text-transform: uppercase; }
    .report-id { font-size: 12px; color: #94a3b8; text-align: right; }
    h1 { font-size: 20px; font-weight: 800; color: #1e293b; margin: 20px 0 8px; }
    .badge { display: inline-block; padding: 4px 14px; border-radius: 20px; font-size: 11px; font-weight: 700; background: #dbeafe; color: #1d4ed8; margin-bottom: 20px; }
    .section { margin-bottom: 20px; }
    .section-title { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #64748b; margin-bottom: 8px; }
    .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .info-item { padding: 10px 14px; background: #f8fafc; border-radius: 8px; border-left: 3px solid #2563eb; }
    .info-label { font-size: 10px; color: #94a3b8; text-transform: uppercase; }
    .info-value { font-size: 14px; font-weight: 700; color: #1e293b; margin-top: 2px; }
    .body-text { padding: 16px; background: #f8fafc; border-radius: 10px; font-size: 14px; line-height: 1.8; color: #334155; border-left: 3px solid #10b981; }
    .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between; font-size: 11px; color: #94a3b8; }
    .signature { text-align: right; }
    .sig-line { width: 200px; border-bottom: 1px solid #94a3b8; margin: 30px 0 6px auto; }
    @media print { body { padding: 20px; } }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <div class="logo">🏥 AI Hospital Alliance</div>
      <div class="logo-sub">Clinical Report System · Powered by AI</div>
    </div>
    <div class="report-id">
      <div>Report ID: ${report.id}</div>
      <div>Date: ${new Date().toLocaleDateString("en-GB", { day: "2-digit", month: "long", year: "numeric" })}</div>
      <div>Status: ${report.status}</div>
    </div>
  </div>

  <h1>${report.title}</h1>
  <span class="badge">${report.type}</span>

  ${patient ? `
  <div class="section">
    <div class="section-title">Patient Information</div>
    <div class="info-grid">
      <div class="info-item"><div class="info-label">Full Name</div><div class="info-value">${patient.name}</div></div>
      <div class="info-item"><div class="info-label">Patient ID</div><div class="info-value">${patient.id}</div></div>
      <div class="info-item"><div class="info-label">Age / Gender</div><div class="info-value">${patient.age} years · ${patient.gender}</div></div>
      <div class="info-item"><div class="info-label">Department</div><div class="info-value">${patient.department}</div></div>
      <div class="info-item"><div class="info-label">Condition</div><div class="info-value">${patient.condition}</div></div>
      <div class="info-item"><div class="info-label">Status</div><div class="info-value">${patient.status}</div></div>
    </div>
  </div>
  ` : ""}

  <div class="section">
    <div class="section-title">Clinical Report</div>
    <div class="body-text">${report.body}</div>
  </div>

  <div class="signature">
    <div class="sig-line"></div>
    <div style="font-size:12px;color:#475569;">Authorized by: ${user?.name ?? "System Admin"}</div>
    <div style="font-size:11px;color:#94a3b8;">${user?.role ?? "Admin"} · AI Hospital Alliance</div>
  </div>

  <div class="footer">
    <div>Generated by AI Hospital Alliance System · ${new Date().toLocaleString()}</div>
    <div>Confidential Medical Document</div>
  </div>

  <script>window.onload = () => { window.print(); }</script>
</body>
</html>`)
    w.document.close()
  }

  async function generateAIReport(report: Report) {
    setGenerating(true)
    const patient = getPatient(report.patient_id)
    try {
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          system: "You are a senior hospital clinician. Generate a professional clinical report in English. Be concise, clear, and medically accurate.",
          messages: [{
            role: "user",
            content: `Generate a complete clinical report for:
Report: ${report.title}
Type: ${report.type}
Patient: ${patient?.name ?? "Unknown"}, Age ${patient?.age}, ${patient?.gender}
Condition: ${patient?.condition}
Current: ${report.body}

Write a professional medical report with: Summary, Findings, Assessment, Plan.`
          }]
        })
      })
      const data = await res.json()
      const text = data.content?.[0]?.text ?? ""
      setSelected({ ...report, body: text })
    } catch {
      alert("Claude AI not connected — using existing report")
    } finally { setGenerating(false) }
  }

  const types = ["All", ...Array.from(new Set(reports.map(r => r.type)))]
  const statuses = ["All", "Ready", "In Progress", "Draft"]

  const filtered = reports.filter(r => {
    const matchSearch = r.title.toLowerCase().includes(search.toLowerCase()) || r.patient_id.toLowerCase().includes(search.toLowerCase())
    const matchType = filterType === "All" || r.type === filterType
    const matchStatus = filterStatus === "All" || r.status === filterStatus
    return matchSearch && matchType && matchStatus
  })

  return (
    <div style={{ padding: "24px 28px", fontFamily: "Inter,Arial,sans-serif", color: "white", minHeight: "100vh" }}>

      <div style={{ marginBottom: 22 }}>
        <div style={{ fontSize: 11, color: "#f59e0b", fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 6 }}>◈ AI HOSPITAL ALLIANCE</div>
        <h1 style={{ margin: 0, fontSize: 26, fontWeight: 900, color: "white" }}>📄 Clinical Reports</h1>
        <p style={{ color: "#475569", fontSize: 13, marginTop: 4 }}>AI-generated · Print-ready · {reports.length} reports</p>
      </div>

      {/* Stats */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 12, marginBottom: 18 }}>
        {[
          { label: "Total Reports", value: reports.length, color: "#3b82f6" },
          { label: "Ready", value: reports.filter(r => r.status === "Ready").length, color: "#4ade80" },
          { label: "In Progress", value: reports.filter(r => r.status === "In Progress").length, color: "#fbbf24" },
          { label: "Report Types", value: new Set(reports.map(r => r.type)).size, color: "#a855f7" },
        ].map(({ label, value, color }) => (
          <div key={label} style={{ padding: "14px 16px", borderRadius: 14, background: `${color}08`, border: `1px solid ${color}22` }}>
            <div style={{ fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }}>{label}</div>
            <div style={{ fontSize: 24, fontWeight: 900, color, marginTop: 4 }}>{value}</div>
          </div>
        ))}
      </div>

      {/* Filters */}
      <div style={{ display: "flex", gap: 10, marginBottom: 18, flexWrap: "wrap" }}>
        <input value={search} onChange={e => setSearch(e.target.value)} placeholder="🔍 Search reports..." style={{ flex: 1, minWidth: 200, padding: "10px 14px", borderRadius: 12, fontSize: 13, background: "rgba(255,255,255,0.05)", border: "1px solid rgba(245,158,11,0.3)", color: "white", outline: "none" }} />
        <select value={filterType} onChange={e => setFilterType(e.target.value)} style={{ padding: "10px 14px", borderRadius: 12, fontSize: 13, background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)", color: "white", outline: "none" }}>
          {types.map(t => <option key={t} value={t}>{t}</option>)}
        </select>
        <select value={filterStatus} onChange={e => setFilterStatus(e.target.value)} style={{ padding: "10px 14px", borderRadius: 12, fontSize: 13, background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)", color: "white", outline: "none" }}>
          {statuses.map(s => <option key={s} value={s}>{s}</option>)}
        </select>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: selected ? "1fr 420px" : "1fr", gap: 16 }}>

        {/* Reports list */}
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {loading ? <div style={{ color: "#64748b", padding: 20 }}>Loading reports...</div> :
            filtered.map(r => {
              const patient = getPatient(r.patient_id)
              const tc = TYPE_COLOR[r.type] ?? "#64748b"
              const sc = STATUS_COLOR[r.status] ?? "#94a3b8"
              return (
                <div key={r.id} onClick={() => setSelected(selected?.id === r.id ? null : r)} style={{
                  padding: "16px 20px", borderRadius: 16, cursor: "pointer",
                  background: selected?.id === r.id ? `${tc}10` : "linear-gradient(135deg,#0f172a,#1a2540)",
                  border: `1px solid ${selected?.id === r.id ? tc + "40" : "rgba(255,255,255,0.08)"}`,
                  transition: "all 0.2s",
                }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                    <div style={{ flex: 1 }}>
                      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6 }}>
                        <span style={{ fontWeight: 800, color: "white", fontSize: 14 }}>{r.title}</span>
                        <span style={{ padding: "2px 10px", borderRadius: 20, fontSize: 11, fontWeight: 700, background: `${tc}15`, color: tc, border: `1px solid ${tc}30` }}>{r.type}</span>
                        <span style={{ padding: "2px 10px", borderRadius: 20, fontSize: 11, fontWeight: 700, background: `${sc}15`, color: sc }}>{r.status}</span>
                      </div>
                      <div style={{ color: "#64748b", fontSize: 12 }}>
                        {r.id} · Patient: <strong style={{ color: "#94a3b8" }}>{patient?.name ?? r.patient_id}</strong>
                        {patient && <span> · {patient.age}y · {patient.department}</span>}
                      </div>
                      <div style={{ color: "#475569", fontSize: 12, marginTop: 6, lineHeight: 1.5 }}>{r.body.slice(0, 120)}...</div>
                    </div>
                    <div style={{ display: "flex", gap: 6, flexShrink: 0, marginLeft: 12 }}>
                      <button onClick={e => { e.stopPropagation(); generateAIReport(r) }} disabled={generating} style={{ padding: "6px 12px", borderRadius: 8, background: "rgba(124,58,237,0.1)", color: "#a78bfa", fontSize: 11, fontWeight: 700, border: "1px solid rgba(124,58,237,0.25)", cursor: "pointer" }}>
                        {generating ? "..." : "🤖 AI"}
                      </button>
                      <button onClick={e => { e.stopPropagation(); printReport(r) }} style={{ padding: "6px 12px", borderRadius: 8, background: "rgba(59,130,246,0.1)", color: "#60a5fa", fontSize: 11, fontWeight: 700, border: "1px solid rgba(59,130,246,0.25)", cursor: "pointer" }}>
                        🖨️ Print
                      </button>
                    </div>
                  </div>
                </div>
              )
            })
          }
        </div>

        {/* Report Detail */}
        {selected && (
          <div style={{ background: "linear-gradient(135deg,#0f172a,#1a2540)", border: "1px solid rgba(245,158,11,0.2)", borderRadius: 20, padding: 22, position: "sticky", top: 20, height: "fit-content" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 18 }}>
              <div style={{ fontWeight: 800, fontSize: 15, color: "white" }}>{selected.title}</div>
              <button onClick={() => setSelected(null)} style={{ width: 28, height: 28, borderRadius: 8, border: "none", background: "rgba(255,255,255,0.06)", color: "#64748b", cursor: "pointer", fontSize: 16 }}>×</button>
            </div>

            {(() => {
              const patient = getPatient(selected.patient_id)
              return patient ? (
                <div style={{ marginBottom: 16 }}>
                  <div style={{ fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1, marginBottom: 8 }}>Patient</div>
                  <div style={{ padding: "12px 14px", borderRadius: 12, background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)" }}>
                    <div style={{ fontWeight: 700, color: "white", fontSize: 14 }}>{patient.name}</div>
                    <div style={{ color: "#64748b", fontSize: 12, marginTop: 3 }}>{patient.age}y · {patient.gender} · {patient.department}</div>
                    <div style={{ color: "#94a3b8", fontSize: 12, marginTop: 2 }}>{patient.condition}</div>
                  </div>
                </div>
              ) : null
            })()}

            <div style={{ fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1, marginBottom: 8 }}>Report Content</div>
            <div style={{ padding: "14px 16px", borderRadius: 12, background: "rgba(255,255,255,0.03)", border: "1px solid rgba(16,185,129,0.15)", color: "#cbd5e1", fontSize: 13, lineHeight: 1.8, maxHeight: 300, overflowY: "auto", whiteSpace: "pre-wrap" }}>
              {selected.body}
            </div>

            <div style={{ display: "flex", gap: 8, marginTop: 16 }}>
              <button onClick={() => generateAIReport(selected)} disabled={generating} style={{ flex: 1, padding: "10px", borderRadius: 12, background: generating ? "rgba(124,58,237,0.2)" : "linear-gradient(135deg,#7c3aed,#4f46e5)", color: "white", border: "none", fontWeight: 700, fontSize: 13, cursor: generating ? "not-allowed" : "pointer" }}>
                {generating ? "⟳ Generating..." : "🤖 AI Report"}
              </button>
              <button onClick={() => printReport(selected)} style={{ flex: 1, padding: "10px", borderRadius: 12, background: "linear-gradient(135deg,#2563eb,#1d4ed8)", color: "white", border: "none", fontWeight: 700, fontSize: 13, cursor: "pointer" }}>
                🖨️ Print PDF
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
