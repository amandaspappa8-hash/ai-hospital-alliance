import { useEffect, useState, useCallback } from "react"
import { apiGet } from "@/lib/api"
import { getUser } from "@/lib/auth-storage"

type Patient = { id: string; name: string; department: string; status: string; condition: string; gender: string; age: number }
type Doctor = { id: string; name: string; specialty: string; status: string; rating: number; patients_count: number }
type Appointment = { id: string; status: string; department: string; date?: string }

const DEPT_COLORS: Record<string, string> = {
  Cardiology: "#ef4444", Emergency: "#f97316", ICU: "#06b6d4",
  Neurology: "#a855f7", Pediatrics: "#fbbf24", Orthopedics: "#10b981", Radiology: "#3b82f6",
}
const STATUS_COLORS: Record<string, string> = {
  Active: "#4ade80", "Under Observation": "#fb923c", Critical: "#f87171", Discharged: "#94a3b8"
}
const GENDER_COLORS: Record<string, string> = { Male: "#3b82f6", Female: "#ec4899" }

// Animated counter hook
function useCounter(target: number, duration = 1000) {
  const [value, setValue] = useState(0)
  useEffect(() => {
    if (target === 0) return
    const steps = 30
    const increment = target / steps
    let current = 0
    const timer = setInterval(() => {
      current += increment
      if (current >= target) { setValue(target); clearInterval(timer) }
      else setValue(Math.round(current))
    }, duration / steps)
    return () => clearInterval(timer)
  }, [target, duration])
  return value
}

function KpiCard({ label, value, color, icon, sub }: { label: string; value: number | string; color: string; icon: string; sub?: string }) {
  const numVal = typeof value === "number" ? value : 0
  const animated = useCounter(numVal)
  return (
    <div style={{
      padding: "18px 20px", borderRadius: 18,
      background: `linear-gradient(135deg, ${color}10, ${color}05)`,
      border: `1px solid ${color}30`,
      display: "flex", alignItems: "center", gap: 14,
      transition: "transform 0.2s", cursor: "default",
    }}
      onMouseEnter={e => (e.currentTarget.style.transform = "translateY(-2px)")}
      onMouseLeave={e => (e.currentTarget.style.transform = "translateY(0)")}
    >
      <div style={{
        width: 46, height: 46, borderRadius: 14,
        background: `${color}20`, display: "flex",
        alignItems: "center", justifyContent: "center", fontSize: 22, flexShrink: 0
      }}>{icon}</div>
      <div>
        <div style={{ fontSize: 24, fontWeight: 900, color, lineHeight: 1 }}>
          {typeof value === "number" ? animated : value}
        </div>
        <div style={{ fontSize: 11, color: "#64748b", marginTop: 3 }}>{label}</div>
        {sub && <div style={{ fontSize: 10, color: color, marginTop: 2, opacity: 0.8 }}>{sub}</div>}
      </div>
    </div>
  )
}

function BarChart({ data, colors, title, accentColor }: {
  data: Record<string, number>; colors: Record<string, string>; title: string; accentColor: string
}) {
  const max = Math.max(...Object.values(data), 1)
  const sorted = Object.entries(data).sort((a, b) => b[1] - a[1])
  return (
    <div style={{ background: "linear-gradient(135deg,#0f172a,#131f35)", border: "1px solid rgba(99,102,241,0.12)", borderRadius: 20, padding: 22 }}>
      <div style={{ fontWeight: 800, fontSize: 13, color: "white", marginBottom: 18, display: "flex", alignItems: "center", gap: 8 }}>
        <div style={{ width: 3, height: 16, background: accentColor, borderRadius: 2 }} />
        {title}
      </div>
      {sorted.map(([label, value]) => (
        <div key={label} style={{ marginBottom: 14 }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
            <span style={{ fontSize: 12, color: "#94a3b8" }}>{label}</span>
            <span style={{ fontSize: 12, fontWeight: 700, color: colors[label] ?? "#64748b" }}>{value}</span>
          </div>
          <div style={{ height: 7, borderRadius: 4, background: "rgba(255,255,255,0.06)", overflow: "hidden" }}>
            <div style={{
              height: "100%", width: `${Math.round((value / max) * 100)}%`,
              background: `linear-gradient(90deg, ${colors[label] ?? "#64748b"}, ${colors[label] ?? "#64748b"}88)`,
              borderRadius: 4, transition: "width 1.2s cubic-bezier(0.4,0,0.2,1)"
            }} />
          </div>
        </div>
      ))}
    </div>
  )
}

function DonutChart({ data, colors, title, accentColor }: {
  data: Record<string, number>; colors: Record<string, string>; title: string; accentColor: string
}) {
  const total = Object.values(data).reduce((s, v) => s + v, 0)
  let cumulative = 0
  const segments = Object.entries(data).map(([label, value]) => {
    const pct = total > 0 ? (value / total) * 100 : 0
    const start = cumulative
    cumulative += pct
    return { label, value, pct, start }
  })
  const r = 38, cx = 50, cy = 50
  function arc(start: number, end: number) {
    const s = (start / 100) * 2 * Math.PI - Math.PI / 2
    const e = (end / 100) * 2 * Math.PI - Math.PI / 2
    const x1 = cx + r * Math.cos(s), y1 = cy + r * Math.sin(s)
    const x2 = cx + r * Math.cos(e), y2 = cy + r * Math.sin(e)
    return `M ${cx} ${cy} L ${x1} ${y1} A ${r} ${r} 0 ${end - start > 50 ? 1 : 0} 1 ${x2} ${y2} Z`
  }
  return (
    <div style={{ background: "linear-gradient(135deg,#0f172a,#131f35)", border: "1px solid rgba(99,102,241,0.12)", borderRadius: 20, padding: 22 }}>
      <div style={{ fontWeight: 800, fontSize: 13, color: "white", marginBottom: 18, display: "flex", alignItems: "center", gap: 8 }}>
        <div style={{ width: 3, height: 16, background: accentColor, borderRadius: 2 }} />
        {title}
      </div>
      {total === 0 ? (
        <div style={{ color: "#64748b", fontSize: 13, textAlign: "center", padding: "20px 0" }}>No data</div>
      ) : (
        <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
          <svg width="100" height="100" viewBox="0 0 100 100" style={{ flexShrink: 0 }}>
            {segments.map(seg => (
              <path key={seg.label} d={arc(seg.start, seg.start + seg.pct)}
                fill={colors[seg.label] ?? "#64748b"} opacity={0.9} />
            ))}
            <circle cx={cx} cy={cy} r={20} fill="#0f172a" />
            <text x={cx} y={cy + 4} textAnchor="middle" fill="white" fontSize="10" fontWeight="800">{total}</text>
          </svg>
          <div style={{ flex: 1 }}>
            {segments.map(seg => (
              <div key={seg.label} style={{ display: "flex", justifyContent: "space-between", marginBottom: 6, fontSize: 11 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                  <div style={{ width: 8, height: 8, borderRadius: 2, background: colors[seg.label] ?? "#64748b", flexShrink: 0 }} />
                  <span style={{ color: "#94a3b8" }}>{seg.label}</span>
                </div>
                <span style={{ color: "white", fontWeight: 700 }}>{seg.value} <span style={{ color: "#64748b" }}>({Math.round(seg.pct)}%)</span></span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function LineChart({ title, accentColor }: { title: string; accentColor: string }) {
  // Simulated weekly trend data
  const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
  const admissions = [12, 18, 15, 22, 19, 14, 17]
  const discharges = [8, 12, 10, 16, 14, 10, 13]
  const w = 260, h = 100, padL = 30, padB = 20, padT = 10
  const maxVal = Math.max(...admissions, ...discharges)
  const toX = (i: number) => padL + (i / (days.length - 1)) * (w - padL - 10)
  const toY = (v: number) => padT + ((maxVal - v) / maxVal) * (h - padB - padT)
  const line = (data: number[]) => data.map((v, i) => `${i === 0 ? "M" : "L"} ${toX(i)} ${toY(v)}`).join(" ")

  return (
    <div style={{ background: "linear-gradient(135deg,#0f172a,#131f35)", border: "1px solid rgba(99,102,241,0.12)", borderRadius: 20, padding: 22 }}>
      <div style={{ fontWeight: 800, fontSize: 13, color: "white", marginBottom: 4, display: "flex", alignItems: "center", gap: 8 }}>
        <div style={{ width: 3, height: 16, background: accentColor, borderRadius: 2 }} />
        {title}
      </div>
      <div style={{ fontSize: 11, color: "#64748b", marginBottom: 16 }}>Weekly patient flow</div>
      <svg width="100%" viewBox={`0 0 ${w} ${h}`} style={{ overflow: "visible" }}>
        {/* Grid lines */}
        {[0, 0.25, 0.5, 0.75, 1].map(t => (
          <line key={t} x1={padL} x2={w - 10} y1={padT + t * (h - padB - padT)} y2={padT + t * (h - padB - padT)}
            stroke="rgba(255,255,255,0.05)" strokeWidth="1" />
        ))}
        {/* Lines */}
        <path d={line(admissions)} fill="none" stroke="#3b82f6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        <path d={line(discharges)} fill="none" stroke="#10b981" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" strokeDasharray="4 2" />
        {/* Dots */}
        {admissions.map((v, i) => <circle key={i} cx={toX(i)} cy={toY(v)} r="3" fill="#3b82f6" />)}
        {discharges.map((v, i) => <circle key={i} cx={toX(i)} cy={toY(v)} r="3" fill="#10b981" />)}
        {/* X labels */}
        {days.map((d, i) => (
          <text key={d} x={toX(i)} y={h - 2} textAnchor="middle" fill="#475569" fontSize="8">{d}</text>
        ))}
      </svg>
      <div style={{ display: "flex", gap: 16, marginTop: 8 }}>
        {[{ color: "#3b82f6", label: "Admissions" }, { color: "#10b981", label: "Discharges" }].map(({ color, label }) => (
          <div key={label} style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 11, color: "#94a3b8" }}>
            <div style={{ width: 20, height: 2, background: color, borderRadius: 1 }} />
            {label}
          </div>
        ))}
      </div>
    </div>
  )
}

function AlertsPanel({ patients }: { patients: Patient[] }) {
  const critical = patients.filter(p => p.status === "Critical")
  const observation = patients.filter(p => p.status === "Under Observation")
  const alerts = [
    ...critical.map(p => ({ type: "critical", msg: `${p.name} — Critical in ${p.department}`, color: "#ef4444" })),
    ...observation.slice(0, 3).map(p => ({ type: "warning", msg: `${p.name} — Under Observation`, color: "#f97316" })),
  ].slice(0, 6)

  return (
    <div style={{ background: "linear-gradient(135deg,#0f172a,#131f35)", border: "1px solid rgba(239,68,68,0.15)", borderRadius: 20, padding: 22 }}>
      <div style={{ fontWeight: 800, fontSize: 13, color: "white", marginBottom: 16, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <div style={{ width: 3, height: 16, background: "#ef4444", borderRadius: 2 }} />
          Active Alerts
        </div>
        {alerts.length > 0 && (
          <div style={{ fontSize: 10, background: "#ef444420", color: "#ef4444", padding: "2px 8px", borderRadius: 20, fontWeight: 700 }}>
            {alerts.length} ACTIVE
          </div>
        )}
      </div>
      {alerts.length === 0 ? (
        <div style={{ color: "#4ade80", fontSize: 13, textAlign: "center", padding: "16px 0" }}>✅ All systems normal</div>
      ) : (
        alerts.map((alert, i) => (
          <div key={i} style={{
            display: "flex", alignItems: "center", gap: 10, padding: "10px 12px",
            borderRadius: 10, background: `${alert.color}08`, border: `1px solid ${alert.color}20`,
            marginBottom: 8
          }}>
            <div style={{ width: 8, height: 8, borderRadius: "50%", background: alert.color, flexShrink: 0, boxShadow: `0 0 6px ${alert.color}` }} />
            <span style={{ fontSize: 12, color: "#cbd5e1", flex: 1 }}>{alert.msg}</span>
            <span style={{ fontSize: 10, color: alert.color, fontWeight: 700 }}>{alert.type === "critical" ? "CRITICAL" : "WATCH"}</span>
          </div>
        ))
      )}
    </div>
  )
}

function TopDoctors({ doctors }: { doctors: Doctor[] }) {
  const top = [...doctors].sort((a, b) => b.rating - a.rating).slice(0, 5)
  return (
    <div style={{ background: "linear-gradient(135deg,#0f172a,#131f35)", border: "1px solid rgba(99,102,241,0.12)", borderRadius: 20, padding: 22 }}>
      <div style={{ fontWeight: 800, fontSize: 13, color: "white", marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
        <div style={{ width: 3, height: 16, background: "#f59e0b", borderRadius: 2 }} />
        Top Performing Doctors
      </div>
      {top.map((d, i) => (
        <div key={d.id} style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 12, padding: "8px 10px", borderRadius: 12, background: i === 0 ? "rgba(245,158,11,0.06)" : "transparent" }}>
          <div style={{
            width: 28, height: 28, borderRadius: 8, flexShrink: 0,
            background: i === 0 ? "linear-gradient(135deg,#f59e0b,#d97706)" : "rgba(255,255,255,0.06)",
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 12, fontWeight: 800, color: i === 0 ? "white" : "#64748b"
          }}>#{i + 1}</div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontSize: 12, fontWeight: 700, color: "white", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
              {d.name}
            </div>
            <div style={{ fontSize: 10, color: "#64748b" }}>{d.specialty}</div>
          </div>
          <div style={{ textAlign: "right", flexShrink: 0 }}>
            <div style={{ fontSize: 13, fontWeight: 800, color: "#f59e0b" }}>⭐ {d.rating}</div>
            <div style={{ fontSize: 10, color: "#64748b" }}>{d.patients_count} pts</div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default function AdminOverviewPage() {
  const user = getUser()
  const [patients, setPatients] = useState<Patient[]>([])
  const [doctors, setDoctors] = useState<Doctor[]>([])
  const [appointments, setAppointments] = useState<Appointment[]>([])
  const [loading, setLoading] = useState(true)
  const [lastRefresh, setLastRefresh] = useState(new Date())
  const [timeFilter, setTimeFilter] = useState<"today" | "week" | "month">("today")

  const fetchData = useCallback(() => {
    setLoading(true)
    Promise.all([
      apiGet<Patient[]>("/patients").catch(() => []),
      apiGet<Doctor[]>("/doctors/summary").catch(() => []),
      apiGet<Appointment[]>("/appointments").catch(() => []),
    ]).then(([p, d, a]) => {
      setPatients(Array.isArray(p) ? p : [])
      setDoctors(Array.isArray(d) ? d : [])
      setAppointments(Array.isArray(a) ? a : [])
      setLastRefresh(new Date())
    }).finally(() => setLoading(false))
  }, [])

  useEffect(() => { fetchData() }, [fetchData])

  // Analytics
  const deptCount = patients.reduce((a, p) => { a[p.department] = (a[p.department] || 0) + 1; return a }, {} as Record<string, number>)
  const statusCount = patients.reduce((a, p) => { a[p.status] = (a[p.status] || 0) + 1; return a }, {} as Record<string, number>)
  const genderCount = patients.reduce((a, p) => { a[p.gender] = (a[p.gender] || 0) + 1; return a }, {} as Record<string, number>)
  const availDoctors = doctors.filter(d => d.status === "Available").length
  const avgRating = doctors.length > 0 ? (doctors.reduce((s, d) => s + d.rating, 0) / doctors.length).toFixed(1) : "—"
  const criticalRate = patients.length > 0 ? Math.round(((statusCount["Critical"] ?? 0) / patients.length) * 100) : 0
  const occupancyRate = Math.min(Math.round((patients.length / Math.max(doctors.length * 10, 1)) * 100), 100)

  const appointmentStatus = appointments.reduce((a, ap) => {
    a[ap.status] = (a[ap.status] || 0) + 1; return a
  }, {} as Record<string, number>)

  return (
    <div style={{ padding: "24px 28px", fontFamily: "Inter,Arial,sans-serif", color: "white", minHeight: "100vh", maxWidth: 1400 }}>

      {/* Header */}
      <div style={{ marginBottom: 24, display: "flex", alignItems: "flex-start", justifyContent: "space-between", flexWrap: "wrap", gap: 12 }}>
        <div>
          <div style={{ fontSize: 11, color: "#6366f1", fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 6 }}>
            ◈ AI HOSPITAL ALLIANCE — ANALYTICS
          </div>
          <h1 style={{ margin: 0, fontSize: 26, fontWeight: 900, color: "white" }}>📊 Hospital Analytics Dashboard</h1>
          <p style={{ color: "#475569", fontSize: 12, marginTop: 4 }}>
            {new Date().toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" })}
            {" · "}{user?.name}
            {" · "}<span style={{ color: "#4ade80" }}>●</span> Live
          </p>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          {/* Time filter */}
          <div style={{ display: "flex", background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 10, overflow: "hidden" }}>
            {(["today", "week", "month"] as const).map(t => (
              <button key={t} onClick={() => setTimeFilter(t)} style={{
                padding: "6px 14px", fontSize: 11, fontWeight: 700, border: "none", cursor: "pointer",
                background: timeFilter === t ? "#6366f1" : "transparent",
                color: timeFilter === t ? "white" : "#64748b",
                textTransform: "capitalize", transition: "all 0.2s"
              }}>{t}</button>
            ))}
          </div>
          {/* Refresh button */}
          <button onClick={fetchData} style={{
            padding: "6px 16px", fontSize: 11, fontWeight: 700,
            background: "rgba(99,102,241,0.15)", border: "1px solid rgba(99,102,241,0.3)",
            borderRadius: 10, color: "#818cf8", cursor: "pointer"
          }}>
            ↻ Refresh
          </button>
        </div>
      </div>

      {/* Last refresh */}
      <div style={{ fontSize: 10, color: "#334155", marginBottom: 20 }}>
        Last updated: {lastRefresh.toLocaleTimeString()}
      </div>

      {/* KPI Cards - Row 1 */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 12, marginBottom: 20 }}>
        <KpiCard label="Total Patients" value={patients.length} color="#3b82f6" icon="🧑‍⚕️" sub={`${statusCount["Active"] ?? 0} active`} />
        <KpiCard label="Available Doctors" value={availDoctors} color="#10b981" icon="👨‍⚕️" sub={`of ${doctors.length} total`} />
        <KpiCard label="Appointments" value={appointments.length} color="#a855f7" icon="📅" sub={`${appointmentStatus["Scheduled"] ?? 0} scheduled`} />
        <KpiCard label="Critical Cases" value={statusCount["Critical"] ?? 0} color="#ef4444" icon="⚠️" sub={`${criticalRate}% rate`} />
        <KpiCard label="Avg Doctor Rating" value={avgRating} color="#f59e0b" icon="⭐" sub="out of 5.0" />
        <KpiCard label="Bed Occupancy" value={`${occupancyRate}%`} color="#06b6d4" icon="🏥" sub="estimated" />
      </div>

      {/* Charts Row 1 */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 16, marginBottom: 16 }}>
        <BarChart data={deptCount} colors={DEPT_COLORS} title="Patients by Department" accentColor="#6366f1" />
        <DonutChart data={statusCount} colors={STATUS_COLORS} title="Patient Status Distribution" accentColor="#10b981" />
        <DonutChart data={genderCount} colors={GENDER_COLORS} title="Gender Distribution" accentColor="#ec4899" />
      </div>

      {/* Charts Row 2 */}
      <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr 1fr", gap: 16, marginBottom: 16 }}>
        <LineChart title="Patient Flow Trend" accentColor="#3b82f6" />
        <TopDoctors doctors={doctors} />
        <AlertsPanel patients={patients} />
      </div>

      {/* Summary Cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12 }}>
        {[
          {
            title: "Busiest Department",
            value: Object.entries(deptCount).sort((a, b) => b[1] - a[1])[0]?.[0] ?? "—",
            sub: `${Object.entries(deptCount).sort((a, b) => b[1] - a[1])[0]?.[1] ?? 0} patients`,
            icon: "🏥", color: "#6366f1"
          },
          {
            title: "Under Observation",
            value: statusCount["Under Observation"] ?? 0,
            sub: "needs monitoring",
            icon: "👁️", color: "#f97316"
          },
          {
            title: "Discharged Today",
            value: statusCount["Discharged"] ?? 0,
            sub: "successfully",
            icon: "✅", color: "#10b981"
          },
          {
            title: "Critical Rate",
            value: `${criticalRate}%`,
            sub: criticalRate > 10 ? "⚠️ Above average" : "✅ Normal range",
            icon: "📊", color: criticalRate > 10 ? "#ef4444" : "#4ade80"
          },
        ].map(({ title, value, sub, icon, color }) => (
          <div key={title} style={{
            padding: "18px 20px", borderRadius: 18,
            background: "linear-gradient(135deg,#0f172a,#131f35)",
            border: `1px solid ${color}20`,
            transition: "transform 0.2s", cursor: "default"
          }}
            onMouseEnter={e => (e.currentTarget.style.transform = "translateY(-2px)")}
            onMouseLeave={e => (e.currentTarget.style.transform = "translateY(0)")}
          >
            <div style={{ fontSize: 26, marginBottom: 10 }}>{icon}</div>
            <div style={{ fontSize: 20, fontWeight: 900, color }}>{value}</div>
            <div style={{ fontSize: 12, color: "white", marginTop: 4, fontWeight: 600 }}>{title}</div>
            <div style={{ fontSize: 11, color: "#64748b", marginTop: 3 }}>{sub}</div>
          </div>
        ))}
      </div>

      {/* Loading overlay */}
      {loading && (
        <div style={{
          position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)",
          display: "flex", alignItems: "center", justifyContent: "center", zIndex: 50
        }}>
          <div style={{ fontSize: 14, color: "#818cf8", fontWeight: 700 }}>⏳ Loading analytics...</div>
        </div>
      )}
    </div>
  )
}
