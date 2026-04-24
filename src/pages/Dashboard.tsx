import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { apiGet } from "@/lib/api"
import { getUser } from "@/lib/auth-storage"

type Patient = { id: string; name: string; status: string; condition: string; department: string }
type Appointment = { id: string; patientName: string; doctor: string; time: string; status: string }
type Alert = { patient_id?: string; message: string; severity?: string }
type Doctor = { id: string; name: string; specialty: string; status: string; rating: number }

const statusColors: Record<string, { bg: string; color: string; glow: string }> = {
  "Active":             { bg: "#052e16", color: "#4ade80", glow: "0 0 8px #4ade8044" },
  "Under Observation":  { bg: "#1c1917", color: "#fb923c", glow: "0 0 8px #fb923c44" },
  "Critical":           { bg: "#450a0a", color: "#f87171", glow: "0 0 8px #f8717144" },
  "Scheduled":          { bg: "#0c1a2e", color: "#60a5fa", glow: "0 0 8px #60a5fa44" },
  "Waiting":            { bg: "#1c1108", color: "#fbbf24", glow: "0 0 8px #fbbf2444" },
  "Available":          { bg: "#052e16", color: "#4ade80", glow: "0 0 8px #4ade8044" },
  "On Call":            { bg: "#1c1108", color: "#fbbf24", glow: "0 0 8px #fbbf2444" },
  "In Surgery":         { bg: "#450a0a", color: "#f87171", glow: "0 0 8px #f8717144" },
  "Offline":            { bg: "#1e1e1e", color: "#64748b", glow: "none" },
  "Completed":          { bg: "#052e16", color: "#4ade80", glow: "0 0 8px #4ade8044" },
}

function Badge({ status }: { status: string }) {
  const s = statusColors[status] ?? { bg: "#1e293b", color: "#94a3b8", glow: "none" }
  return (
    <span style={{
      background: s.bg, color: s.color, padding: "3px 10px", borderRadius: 20,
      fontSize: 11, fontWeight: 700, whiteSpace: "nowrap",
      boxShadow: s.glow, border: `1px solid ${s.color}33`,
    }}>{status}</span>
  )
}

function StatCard({ label, value, icon, gradient, sub, to }: {
  label: string; value: string | number; icon: React.ReactNode
  gradient: string; sub?: string; to: string
}) {
  return (
    <Link to={to} style={{ textDecoration: "none" }}>
      <div style={{
        background: "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
        border: "1px solid rgba(99,179,237,0.15)",
        borderRadius: 20, padding: "22px 24px",
        display: "flex", alignItems: "center", gap: 18, cursor: "pointer",
        boxShadow: "0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05)",
        transition: "all 0.3s",
        position: "relative", overflow: "hidden",
      }}
        onMouseEnter={e => { e.currentTarget.style.borderColor = "rgba(99,179,237,0.4)"; e.currentTarget.style.transform = "translateY(-2px)" }}
        onMouseLeave={e => { e.currentTarget.style.borderColor = "rgba(99,179,237,0.15)"; e.currentTarget.style.transform = "translateY(0)" }}
      >
        <div style={{
          position: "absolute", top: 0, right: 0, width: 120, height: 120,
          background: gradient, borderRadius: "0 20px 0 120px", opacity: 0.15,
        }} />
        <div style={{
          width: 56, height: 56, borderRadius: 16,
          background: gradient, display: "flex", alignItems: "center",
          justifyContent: "center", flexShrink: 0,
          boxShadow: `0 0 20px ${gradient.includes("59,130") ? "rgba(59,130,246,0.4)" : "rgba(168,85,247,0.4)"}`,
        }}>{icon}</div>
        <div>
          <div style={{ fontSize: 32, fontWeight: 900, color: "white", lineHeight: 1, letterSpacing: -1 }}>{value}</div>
          <div style={{ fontSize: 13, color: "#94a3b8", marginTop: 4, fontWeight: 500 }}>{label}</div>
          {sub && <div style={{ fontSize: 11, color: "#4ade80", marginTop: 3, fontWeight: 600 }}>{sub}</div>}
        </div>
      </div>
    </Link>
  )
}

function SectionCard({ title, children, to, accent = "#3b82f6" }: {
  title: string; children: React.ReactNode; to?: string; accent?: string
}) {
  return (
    <div style={{
      background: "linear-gradient(135deg, #0f172a 0%, #1a2540 100%)",
      border: `1px solid ${accent}22`,
      borderRadius: 20, padding: 22,
      boxShadow: "0 4px 24px rgba(0,0,0,0.3)",
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 18 }}>
        <div style={{
          fontWeight: 800, fontSize: 15, color: "white",
          display: "flex", alignItems: "center", gap: 8,
        }}>
          <div style={{ width: 3, height: 18, background: accent, borderRadius: 2, boxShadow: `0 0 8px ${accent}` }} />
          {title}
        </div>
        {to && (
          <Link to={to} style={{
            color: accent, fontSize: 12, textDecoration: "none", fontWeight: 600,
            padding: "4px 12px", border: `1px solid ${accent}44`, borderRadius: 20,
          }}>View all →</Link>
        )}
      </div>
      {children}
    </div>
  )
}

// ── SVG Icons ────────────────────────────────────────────────────────────────

const Icons = {
  patients: (
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>
      <path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
    </svg>
  ),
  calendar: (
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/>
      <line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
      <path d="M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01"/>
    </svg>
  ),
  alert: (
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
      <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
    </svg>
  ),
  doctor: (
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2a5 5 0 1 0 0 10A5 5 0 0 0 12 2z"/>
      <path d="M2 20c0-4 4-7 10-7s10 3 10 7"/>
      <path d="M17 13v4m-2-2h4"/>
    </svg>
  ),
  bell: (
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
      <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
      <circle cx="19" cy="5" r="3" fill="#f87171" stroke="none"/>
    </svg>
  ),
  radiology: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="12" cy="12" r="3"/>
      <line x1="12" y1="3" x2="12" y2="9"/><line x1="12" y1="15" x2="12" y2="21"/>
      <line x1="3" y1="12" x2="9" y2="12"/><line x1="15" y1="12" x2="21" y2="12"/>
    </svg>
  ),
  lab: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v11l-4 5h14l-4-5V3"/>
    </svg>
  ),
  pharmacy: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>
    </svg>
  ),
  pacs: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/>
      <line x1="12" y1="17" x2="12" y2="21"/>
      <circle cx="12" cy="10" r="3"/><line x1="7" y1="7" x2="7" y2="7"/>
    </svg>
  ),
  ai: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2z"/>
      <circle cx="9" cy="13" r="1" fill="currentColor"/><circle cx="15" cy="13" r="1" fill="currentColor"/>
    </svg>
  ),
  reports: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
      <polyline points="14 2 14 8 20 8"/>
      <line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>
      <polyline points="10 9 9 9 8 9"/>
    </svg>
  ),
  nursing: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
    </svg>
  ),
  specialties: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
      <polyline points="9 22 9 12 15 12 15 22"/>
    </svg>
  ),
}

const quickLinks = [
  { label: "Radiology",   icon: Icons.radiology,   to: "/radiology",   color: "#06b6d4" },
  { label: "Labs",        icon: Icons.lab,          to: "/labs",        color: "#a78bfa" },
  { label: "Pharmacy",    icon: Icons.pharmacy,     to: "/pharmacy",    color: "#f43f5e" },
  { label: "PACS",        icon: Icons.pacs,         to: "/pacs",        color: "#0ea5e9" },
  { label: "AI Engine",   icon: Icons.ai,           to: "/ai-routing",  color: "#10b981" },
  { label: "Reports",     icon: Icons.reports,      to: "/reports",     color: "#f59e0b" },
  { label: "Nursing",     icon: Icons.nursing,      to: "/nursing",     color: "#ec4899" },
  { label: "Specialties", icon: Icons.specialties,  to: "/specialties", color: "#8b5cf6" },
]

const deptList = [
  { name: "Cardiology",  color: "#f43f5e", to: "/specialties/cardiology",
    icon: <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg> },
  { name: "Neurology",   color: "#a78bfa", to: "/specialties/neurology",
    icon: <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/></svg> },
  { name: "Emergency",   color: "#f97316", to: "/specialties/emergency",
    icon: <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg> },
  { name: "ICU",         color: "#06b6d4", to: "/specialties/icu",
    icon: <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg> },
  { name: "Pediatrics",  color: "#fbbf24", to: "/specialties/pediatrics",
    icon: <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/></svg> },
  { name: "Radiology",   color: "#10b981", to: "/radiology",
    icon: <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="12" cy="12" r="3"/></svg> },
]

export default function Dashboard() {
  const user = getUser()
  const [patients, setPatients]   = useState<Patient[]>([])
  const [appointments, setAppointments] = useState<Appointment[]>([])
  const [alerts, setAlerts]       = useState<Alert[]>([])
  const [doctors, setDoctors]     = useState<Doctor[]>([])
  const [loading, setLoading]     = useState(true)

  useEffect(() => {
    Promise.all([
      apiGet<Patient[]>("/patients").catch(() => []),
      apiGet<Appointment[]>("/appointments").catch(() => []),
      apiGet<Alert[]>("/alerts").catch(() => []),
      apiGet<Doctor[]>("/doctors/summary").catch(() => []),
    ]).then(([p, a, al, d]) => {
      setPatients(Array.isArray(p) ? p : [])
      setAppointments(Array.isArray(a) ? a : [])
      setAlerts(Array.isArray(al) ? al : [])
      setDoctors(Array.isArray(d) ? d : [])
    }).finally(() => setLoading(false))
  }, [])

  const critical  = patients.filter(p => p.status === "Critical").length
  const available = doctors.filter(d => d.status === "Available").length

  return (
    <div style={{
      
      background: "linear-gradient(135deg, #020817 0%, #0f1629 50%, #0a1628 100%)",
      padding: "28px 32px", fontFamily: "Inter, Arial, sans-serif", color: "white",
    }}>
      {/* Animated background grid */}
      <div style={{
        position: "fixed", inset: 0, zIndex: 0, pointerEvents: "none",
        backgroundImage: "linear-gradient(rgba(59,130,246,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(59,130,246,0.03) 1px, transparent 1px)",
        backgroundSize: "60px 60px",
      }} />

      <div style={{ position: "relative", zIndex: 1, maxWidth: 1400, margin: "0 auto" }}>

        {/* ── Header ── */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 32 }}>
          <div>
            <div style={{ fontSize: 12, color: "#3b82f6", fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 6 }}>
              ◈ AI HOSPITAL ALLIANCE — COMMAND CENTER
            </div>
            <h1 style={{ margin: 0, fontSize: 28, fontWeight: 900, letterSpacing: -0.5,
              background: "linear-gradient(135deg, #fff 0%, #94a3b8 100%)",
              WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
              Welcome, {user?.name ?? "Doctor"} 👋
            </h1>
            <p style={{ margin: "6px 0 0", color: "#475569", fontSize: 13, fontWeight: 500 }}>
              {user?.role} · {new Date().toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long", year: "numeric" })}
            </p>
          </div>
          <div style={{ display: "flex", gap: 10 }}>
            <Link to="/patients" style={{
              background: "linear-gradient(135deg, #2563eb, #1d4ed8)",
              color: "white", padding: "11px 20px", borderRadius: 12, textDecoration: "none",
              fontSize: 13, fontWeight: 700, boxShadow: "0 0 20px rgba(37,99,235,0.4)",
              border: "1px solid rgba(99,179,237,0.3)",
            }}>+ New Patient</Link>
            <Link to="/appointments" style={{
              background: "rgba(255,255,255,0.05)", color: "white", padding: "11px 20px",
              borderRadius: 12, textDecoration: "none", fontSize: 13, fontWeight: 700,
              border: "1px solid rgba(255,255,255,0.1)", backdropFilter: "blur(10px)",
            }}>📅 Schedule</Link>
          </div>
        </div>

        {/* ── Stats ── */}
        {loading ? (
          <div style={{ color: "#3b82f6", marginBottom: 28, fontSize: 14 }}>⟳ Loading systems...</div>
        ) : (
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(210px, 1fr))", gap: 16, marginBottom: 28 }}>
            <StatCard label="Total Patients"     value={patients.length}     icon={Icons.patients} gradient="linear-gradient(135deg,#2563eb,#7c3aed)" sub="↑ 47% from last month" to="/patients" />
            <StatCard label="Appointments Today" value={appointments.length} icon={Icons.calendar}  gradient="linear-gradient(135deg,#7c3aed,#a855f7)" sub="↑ 12% from last month"  to="/appointments" />
            <StatCard label="Critical Patients"  value={critical}            icon={Icons.alert}     gradient="linear-gradient(135deg,#dc2626,#b91c1c)" sub="Requires attention"      to="/patients" />
            <StatCard label="Available Doctors"  value={available}           icon={Icons.doctor}    gradient="linear-gradient(135deg,#059669,#047857)" sub="On duty now"             to="/doctors" />
            <StatCard label="Active Alerts"      value={alerts.length}       icon={Icons.bell}      gradient="linear-gradient(135deg,#d97706,#b45309)" sub="Requires review"         to="/alerts" />
          </div>
        )}

        {/* ── Main Grid ── */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 300px", gap: 20, marginBottom: 20 }}>

          {/* Patients Table */}
          <SectionCard title="Recent Patients" to="/patients" accent="#3b82f6">
            {patients.length === 0 ? <div style={{ color: "#64748b", fontSize: 13 }}>No patients.</div> : (
              <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
                <thead>
                  <tr>
                    {["Patient", "Dept", "Status", ""].map(h => (
                      <th key={h} style={{ textAlign: "left", paddingBottom: 12, color: "#475569", fontWeight: 600, fontSize: 11, textTransform: "uppercase", letterSpacing: 1 }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {patients.slice(0, 6).map((p, i) => (
                    <tr key={p.id} style={{ borderTop: "1px solid rgba(255,255,255,0.04)" }}>
                      <td style={{ padding: "11px 0" }}>
                        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                          <div style={{
                            width: 32, height: 32, borderRadius: 10, flexShrink: 0,
                            background: "linear-gradient(135deg,#1e3a5f,#2563eb22)",
                            border: "1px solid rgba(59,130,246,0.3)",
                            display: "flex", alignItems: "center", justifyContent: "center", fontSize: 14,
                          }}>👤</div>
                          <div>
                            <div style={{ fontWeight: 700, color: "white" }}>{p.name}</div>
                            <div style={{ color: "#475569", fontSize: 11 }}>{p.id}</div>
                          </div>
                        </div>
                      </td>
                      <td style={{ padding: "11px 0", color: "#64748b" }}>{p.department ?? "—"}</td>
                      <td style={{ padding: "11px 0" }}><Badge status={p.status} /></td>
                      <td style={{ padding: "11px 0" }}>
                        <Link to={`/patients/${p.id}`} style={{
                          color: "#3b82f6", fontSize: 12, textDecoration: "none", fontWeight: 600,
                          padding: "3px 10px", border: "1px solid rgba(59,130,246,0.3)", borderRadius: 8,
                        }}>View</Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </SectionCard>

          {/* Appointments */}
          <SectionCard title="Today's Appointments" to="/appointments" accent="#7c3aed">
            {appointments.length === 0 ? <div style={{ color: "#64748b", fontSize: 13 }}>No appointments.</div> : (
              <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                {appointments.slice(0, 5).map((a) => (
                  <div key={a.id} style={{
                    display: "flex", alignItems: "center", gap: 12, padding: "12px 14px",
                    borderRadius: 12, background: "rgba(124,58,237,0.06)",
                    border: "1px solid rgba(124,58,237,0.15)",
                  }}>
                    <div style={{
                      width: 40, height: 40, borderRadius: 12, flexShrink: 0,
                      background: "linear-gradient(135deg,#4c1d95,#7c3aed44)",
                      border: "1px solid rgba(124,58,237,0.4)",
                      display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16,
                    }}>👤</div>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ fontWeight: 700, color: "white", fontSize: 13 }}>{a.patientName}</div>
                      <div style={{ color: "#64748b", fontSize: 11, marginTop: 2 }}>{a.doctor} · {a.time}</div>
                    </div>
                    <Badge status={a.status} />
                  </div>
                ))}
              </div>
            )}
          </SectionCard>

          {/* Right Column */}
          <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>

            {/* Alerts */}
            <SectionCard title="Active Alerts" accent="#ef4444">
              {alerts.length === 0 ? (
                <div style={{
                  padding: "16px", borderRadius: 12, textAlign: "center",
                  background: "rgba(16,185,129,0.06)", border: "1px solid rgba(16,185,129,0.2)",
                  color: "#4ade80", fontSize: 13, fontWeight: 600,
                }}>✓ All systems normal</div>
              ) : (
                <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                  {alerts.slice(0, 3).map((al, i) => (
                    <div key={i} style={{
                      padding: "10px 12px", borderRadius: 10,
                      background: "rgba(239,68,68,0.06)", border: "1px solid rgba(239,68,68,0.2)",
                    }}>
                      <div style={{ color: "#fca5a5", fontSize: 11, fontWeight: 700 }}>{al.patient_id ?? "SYSTEM"}</div>
                      <div style={{ color: "#94a3b8", fontSize: 12, marginTop: 2 }}>{al.message}</div>
                    </div>
                  ))}
                </div>
              )}
            </SectionCard>

            {/* Quick Access */}
            <SectionCard title="Quick Access" accent="#06b6d4">
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
                {quickLinks.map((item) => (
                  <Link key={item.to} to={item.to} style={{ textDecoration: "none" }}>
                    <div style={{
                      padding: "10px 12px", borderRadius: 10,
                      background: `${item.color}08`,
                      border: `1px solid ${item.color}22`,
                      display: "flex", alignItems: "center", gap: 8,
                      color: item.color, fontSize: 12, fontWeight: 600,
                      cursor: "pointer", transition: "all 0.2s",
                    }}
                      onMouseEnter={e => { e.currentTarget.style.background = `${item.color}18`; e.currentTarget.style.borderColor = `${item.color}55` }}
                      onMouseLeave={e => { e.currentTarget.style.background = `${item.color}08`; e.currentTarget.style.borderColor = `${item.color}22` }}
                    >
                      {item.icon}{item.label}
                    </div>
                  </Link>
                ))}
              </div>
            </SectionCard>

          </div>
        </div>

        {/* ── Bottom Row ── */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>

          {/* Doctors */}
          <SectionCard title="Doctor Directory" to="/doctors" accent="#10b981">
            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              {doctors.slice(0, 5).map((d) => (
                <div key={d.id} style={{
                  display: "flex", alignItems: "center", gap: 12,
                  padding: "10px 14px", borderRadius: 12,
                  background: "rgba(16,185,129,0.04)", border: "1px solid rgba(16,185,129,0.1)",
                }}>
                  <div style={{
                    width: 38, height: 38, borderRadius: 10, flexShrink: 0,
                    background: "linear-gradient(135deg,#064e3b,#10b98122)",
                    border: "1px solid rgba(16,185,129,0.3)",
                    display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16,
                  }}>👨‍⚕️</div>
                  <div style={{ flex: 1 }}>
                    <div style={{ color: "white", fontWeight: 700, fontSize: 13 }}>{d.name}</div>
                    <div style={{ color: "#64748b", fontSize: 11, marginTop: 2 }}>
                      {d.specialty} · ⭐ {d.rating}
                    </div>
                  </div>
                  <Badge status={d.status} />
                </div>
              ))}
            </div>
          </SectionCard>

          {/* Departments */}
          <SectionCard title="Hospital Departments" to="/specialties" accent="#f59e0b">
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10 }}>
              {deptList.map((s) => (
                <Link key={s.to} to={s.to} style={{ textDecoration: "none" }}>
                  <div style={{
                    padding: "16px 12px", borderRadius: 14, textAlign: "center",
                    background: `${s.color}08`, border: `1px solid ${s.color}22`,
                    cursor: "pointer", transition: "all 0.2s",
                  }}
                    onMouseEnter={e => { e.currentTarget.style.background = `${s.color}18`; e.currentTarget.style.transform = "translateY(-2px)" }}
                    onMouseLeave={e => { e.currentTarget.style.background = `${s.color}08`; e.currentTarget.style.transform = "translateY(0)" }}
                  >
                    <div style={{ color: s.color, marginBottom: 6 }}>{s.icon}</div>
                    <div style={{ color: "white", fontSize: 12, fontWeight: 700 }}>{s.name}</div>
                  </div>
                </Link>
              ))}
            </div>
          </SectionCard>

        </div>
      </div>
    </div>
  )
}
