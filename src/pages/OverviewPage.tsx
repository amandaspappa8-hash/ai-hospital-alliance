import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { apiGet } from "@/lib/api"
import { getUser } from "@/lib/auth-storage"

export default function OverviewPage() {
  const user = getUser()
  const [stats, setStats] = useState({ patients: 0, doctors: 0, appointments: 0, alerts: 0 })

  useEffect(() => {
    Promise.all([
      apiGet<any[]>("/patients").catch(() => []),
      apiGet<any[]>("/doctors/summary").catch(() => []),
      apiGet<any[]>("/appointments").catch(() => []),
      apiGet<any[]>("/alerts").catch(() => []),
    ]).then(([p, d, a, al]) => setStats({
      patients: p.length, doctors: d.length,
      appointments: a.length, alerts: al.length,
    }))
  }, [])

  const sections = [
    { title: "Patients",     value: stats.patients,     icon: "🧑‍⚕️", color: "#3b82f6", to: "/patients" },
    { title: "Doctors",      value: stats.doctors,      icon: "👨‍⚕️", color: "#10b981", to: "/doctors" },
    { title: "Appointments", value: stats.appointments, icon: "📅",   color: "#a855f7", to: "/appointments" },
    { title: "Alerts",       value: stats.alerts,       icon: "🔔",   color: "#ef4444", to: "/alerts" },
  ]

  return (
    <div style={{ minHeight: "100vh", background: "linear-gradient(135deg,#020817,#0f1629)", padding: "28px 32px", fontFamily: "Inter,Arial,sans-serif", color: "white" }}>
      <div style={{ maxWidth: 1200, margin: "0 auto" }}>
        <div style={{ marginBottom: 28 }}>
          <div style={{ fontSize: 12, color: "#3b82f6", fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 6 }}>◈ AI HOSPITAL ALLIANCE — OVERVIEW</div>
          <h1 style={{ margin: 0, fontSize: 28, fontWeight: 900, background: "linear-gradient(135deg,#fff,#94a3b8)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>📊 System Overview</h1>
          <p style={{ color: "#475569", fontSize: 13, marginTop: 6 }}>{user?.name} · {user?.role} · {new Date().toLocaleDateString()}</p>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 16, marginBottom: 28 }}>
          {sections.map(s => (
            <Link key={s.to} to={s.to} style={{ textDecoration: "none" }}>
              <div style={{ padding: "22px 20px", borderRadius: 18, background: `${s.color}08`, border: `1px solid ${s.color}22`, cursor: "pointer", transition: "all 0.2s" }}
                onMouseEnter={e => e.currentTarget.style.transform = "translateY(-2px)"}
                onMouseLeave={e => e.currentTarget.style.transform = "translateY(0)"}
              >
                <div style={{ fontSize: 28, marginBottom: 8 }}>{s.icon}</div>
                <div style={{ fontSize: 32, fontWeight: 900, color: s.color }}>{s.value}</div>
                <div style={{ fontSize: 13, color: "#94a3b8", marginTop: 4 }}>{s.title}</div>
              </div>
            </Link>
          ))}
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 16 }}>
          {[
            { title: "Radiology",  icon: "🩻", color: "#f97316", to: "/radiology", desc: "AI Image Analysis · PACS · CT/MRI" },
            { title: "Laboratory", icon: "🧬", color: "#10b981", to: "/labs",      desc: "AI Interpreter · 50,000+ References" },
            { title: "Pharmacy",   icon: "💊", color: "#f43f5e", to: "/pharmacy",  desc: "FDA Database · RxNorm · MAR" },
            { title: "AI Engine",  icon: "🤖", color: "#6366f1", to: "/ai-routing",desc: "Clinical Decision · Diagnosis AI" },
            { title: "Specialties",icon: "🏥", color: "#8b5cf6", to: "/specialties",desc: "6 Departments · Cardiology · ICU" },
            { title: "Reports",    icon: "📄", color: "#f59e0b", to: "/reports",   desc: "Clinical Reports · Auto-generated" },
          ].map(item => (
            <Link key={item.to} to={item.to} style={{ textDecoration: "none" }}>
              <div style={{ padding: "20px 22px", borderRadius: 18, background: `${item.color}06`, border: `1px solid ${item.color}20`, cursor: "pointer", transition: "all 0.2s" }}
                onMouseEnter={e => { e.currentTarget.style.background = `${item.color}12`; e.currentTarget.style.transform = "translateY(-2px)" }}
                onMouseLeave={e => { e.currentTarget.style.background = `${item.color}06`; e.currentTarget.style.transform = "translateY(0)" }}
              >
                <div style={{ fontSize: 26, marginBottom: 8 }}>{item.icon}</div>
                <div style={{ fontWeight: 800, color: "white", fontSize: 16, marginBottom: 6 }}>{item.title}</div>
                <div style={{ color: "#64748b", fontSize: 12, lineHeight: 1.5 }}>{item.desc}</div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}
