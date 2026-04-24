import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { apiGet } from "@/lib/api"

type Doctor = { id: string; name: string; specialty: string; status: string; rating: number; schedule: string }

const META: Record<string, { icon: string; color: string; desc: string }> = {
  Cardiology: { icon: "❤️", color: "#ef4444", desc: "Heart Center — ECG, Chest Pain, Vascular" },
  Neurology:  { icon: "🧠", color: "#a855f7", desc: "Brain & Nerve — Stroke, EEG, Neuroimaging" },
  Emergency:  { icon: "🚑", color: "#f97316", desc: "Emergency Dept — Triage, Rapid Response" },
  ICU:        { icon: "🏥", color: "#06b6d4", desc: "Critical Care — Ventilation, Monitoring" },
  Pediatrics: { icon: "🧒", color: "#fbbf24", desc: "Children Care — Growth, Fever, Outpatient" },
}

export default function EmergencyPage() {
  const meta = META["Emergency"]
  const [doctors, setDoctors] = useState<Doctor[]>([])

  useEffect(() => {
    apiGet<Doctor[]>("/doctors/summary")
      .then(d => setDoctors((Array.isArray(d) ? d : []).filter((doc: Doctor) => doc.specialty === "Emergency")))
      .catch(() => setDoctors([]))
  }, [])

  return (
    <div style={{ minHeight: "100vh", background: "linear-gradient(135deg,#020817,#0f1629)", padding: "28px 32px", fontFamily: "Inter,Arial,sans-serif", color: "white" }}>
      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        <div style={{ marginBottom: 24 }}>
          <Link to="/specialties" style={{ color: "#64748b", fontSize: 12, textDecoration: "none" }}>← Specialties</Link>
          <div style={{ fontSize: 12, color: meta.color, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase" as const, margin: "8px 0 4px" }}>◈ AI HOSPITAL ALLIANCE</div>
          <h1 style={{ margin: 0, fontSize: 28, fontWeight: 900, color: "white" }}>{meta.icon} Emergency</h1>
          <p style={{ color: "#475569", fontSize: 13, marginTop: 6 }}>{meta.desc}</p>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 14, marginBottom: 24 }}>
          {[
            { label: "Specialists", value: doctors.length || "—", color: meta.color },
            { label: "Status", value: "Operational", color: "#10b981" },
            { label: "AI Support", value: "Enabled", color: "#3b82f6" },
          ].map(({ label, value, color }) => (
            <div key={label} style={{ padding: "16px 18px", borderRadius: 16, background: `${color}08`, border: `1px solid ${color}22` }}>
              <div style={{ fontSize: 10, color: "#64748b", textTransform: "uppercase" as const, letterSpacing: 1 }}>{label}</div>
              <div style={{ fontSize: 22, fontWeight: 900, color, marginTop: 6 }}>{value}</div>
            </div>
          ))}
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18 }}>
          <div style={{ background: "linear-gradient(135deg,#0f172a,#1a2540)", border: `1px solid ${meta.color}22`, borderRadius: 20, padding: 22 }}>
            <div style={{ fontWeight: 800, fontSize: 14, color: "white", marginBottom: 16 }}>👨‍⚕️ Emergency Specialists</div>
            {doctors.length === 0 ? (
              <div style={{ color: "#64748b", fontSize: 13 }}>No Emergency specialists found.</div>
            ) : doctors.map(d => (
              <Link key={d.id} to={`/doctors/${d.id}`} style={{ textDecoration: "none" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 12, padding: "10px 12px", borderRadius: 12, background: `${meta.color}06`, border: `1px solid ${meta.color}15`, marginBottom: 8, transition: "all 0.2s" }}>
                  <div style={{ width: 36, height: 36, borderRadius: 10, background: `${meta.color}22`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16 }}>👨‍⚕️</div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 700, color: "white", fontSize: 13 }}>{d.name}</div>
                    <div style={{ color: "#64748b", fontSize: 11 }}>⭐ {d.rating} · {d.schedule}</div>
                  </div>
                  <span style={{ padding: "2px 8px", borderRadius: 20, fontSize: 11, fontWeight: 700, background: d.status === "Available" ? "rgba(16,185,129,0.15)" : "rgba(251,191,36,0.15)", color: d.status === "Available" ? "#4ade80" : "#fbbf24" }}>{d.status}</span>
                </div>
              </Link>
            ))}
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
            <div style={{ background: "linear-gradient(135deg,#0f172a,#1a2540)", border: `1px solid ${meta.color}22`, borderRadius: 20, padding: 22 }}>
              <div style={{ fontWeight: 800, fontSize: 14, color: "white", marginBottom: 14 }}>⚡ Quick Actions</div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
                {[
                  { label: "New Appointment", to: "/appointments", icon: "📅" },
                  { label: "Patient Records",  to: "/patients",     icon: "🧑‍⚕️" },
                  { label: "Lab Orders",       to: "/labs/orders",  icon: "🧬" },
                  { label: "AI Diagnosis",     to: "/ai/clinical",  icon: "🤖" },
                ].map(item => (
                  <Link key={item.to} to={item.to} style={{ textDecoration: "none" }}>
                    <div style={{ padding: "10px 12px", borderRadius: 10, background: `${meta.color}08`, border: `1px solid ${meta.color}20`, display: "flex", alignItems: "center", gap: 8, cursor: "pointer" }}>
                      <span style={{ fontSize: 14 }}>{item.icon}</span>
                      <span style={{ fontSize: 11, fontWeight: 600, color: meta.color }}>{item.label}</span>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
