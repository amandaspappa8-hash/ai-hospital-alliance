import { useState } from "react"
import { Link, useLocation } from "react-router-dom"
import { getUser, clearAuth } from "@/lib/auth-storage"

type NavItem = {
  label: string; to: string; icon: string; color: string
  children?: { label: string; to: string }[]
}

const NAV: NavItem[] = [
  { label: "Dashboard",    to: "/dashboard",   icon: "⚡", color: "#3b82f6" },
  { label: "Overview",     to: "/overview",    icon: "📊", color: "#6366f1" },
  { label: "Patients",     to: "/patients",    icon: "🧑‍⚕️", color: "#10b981",
    children: [
      { label: "All Patients",   to: "/patients" },
      { label: "Clinical Notes", to: "/notes" },
      { label: "Orders",         to: "/orders" },
    ]
  },
  { label: "Doctors",      to: "/doctors",      icon: "👨‍⚕️", color: "#06b6d4" },
  { label: "Appointments", to: "/appointments", icon: "📅",   color: "#a855f7" },
  { label: "Nursing",      to: "/nursing",      icon: "🩺",   color: "#ec4899" },
  { label: "Radiology",    to: "/radiology",    icon: "🩻",   color: "#f97316",
    children: [
      { label: "AI Image Analysis", to: "/radiology" },
      { label: "Radiology Orders",  to: "/radiology/imaging" },
      { label: "PACS Viewer",       to: "/radiology/pacs" },
      { label: "CT / MRI",          to: "/radiology/ct-mri" },
    ]
  },
  { label: "Laboratory",   to: "/labs",         icon: "🧬",   color: "#10b981",
    children: [
      { label: "AI Lab Interpreter", to: "/labs" },
      { label: "Lab Orders",         to: "/labs/orders" },
      { label: "Test Catalog",       to: "/labs/catalog" },
    ]
  },
  { label: "Pharmacy",     to: "/pharmacy",     icon: "💊",   color: "#f43f5e",
    children: [
      { label: "FDA Drug Search",      to: "/pharmacy" },
      { label: "Medications",          to: "/pharmacy/medications" },
      { label: "Interactions",         to: "/pharmacy/interactions" },
      { label: "Drug Formulary",       to: "/pharmacy/formulary" },
      { label: "Discharge Counseling", to: "/pharmacy/discharge" },
      { label: "Prescriptions",        to: "/pharmacy/prescriptions" },
    ]
  },
  { label: "Specialties",  to: "/specialties",  icon: "🏥",   color: "#8b5cf6",
    children: [
      { label: "Cardiology",  to: "/specialties/cardiology" },
      { label: "Neurology",   to: "/specialties/neurology" },
      { label: "Emergency",   to: "/specialties/emergency" },
      { label: "ICU",         to: "/specialties/icu" },
      { label: "Pediatrics",  to: "/specialties/pediatrics" },
    ]
  },
  { label: "AI Engine",    to: "/ai-routing",   icon: "🤖",   color: "#6366f1",
    children: [
      { label: "AI Routing",           to: "/ai-routing" },
      { label: "Clinical Decision AI", to: "/ai/clinical" },
    ]
  },
  { label: "Reports",      to: "/reports",      icon: "📄",   color: "#f59e0b" },
  { label: "File Manager", to: "/files",        icon: "📁",   color: "#64748b" },
  { label: "Settings",     to: "/settings",     icon: "⚙️",   color: "#475569" },
]

export default function Sidebar() {
  const { pathname } = useLocation()
  const user = getUser()
  const [expanded, setExpanded] = useState<string | null>(() => {
    for (const item of NAV) {
      if (item.children?.some(c => pathname.startsWith(c.to))) return item.label
    }
    return null
  })

  function isActive(to: string) {
    return pathname === to || (to !== "/dashboard" && pathname.startsWith(to + "/"))
  }

  return (
    <aside style={{
      width: 250, minHeight: "100vh", flexShrink: 0,
      background: "linear-gradient(180deg,#060d1f 0%,#0a1428 100%)",
      borderRight: "1px solid rgba(59,130,246,0.1)",
      display: "flex", flexDirection: "column",
      position: "sticky", top: 0, height: "100vh", overflowY: "auto",
    }}>

      {/* Logo */}
      <div style={{ padding: "18px 16px 14px", borderBottom: "1px solid rgba(59,130,246,0.1)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{
            width: 36, height: 36, borderRadius: 10,
            background: "linear-gradient(135deg,#1d4ed8,#7c3aed)",
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 17, boxShadow: "0 0 16px rgba(37,99,235,0.5)",
          }}>🏥</div>
          <div>
            <div style={{ fontWeight: 900, fontSize: 12, color: "white", letterSpacing: 0.5 }}>AI Hospital</div>
            <div style={{ fontSize: 9, color: "#3b82f6", fontWeight: 700, letterSpacing: 2 }}>ALLIANCE</div>
          </div>
        </div>
      </div>

      {/* User */}
      <div style={{ padding: "10px 16px", borderBottom: "1px solid rgba(255,255,255,0.04)", display: "flex", alignItems: "center", gap: 8 }}>
        <div style={{
          width: 30, height: 30, borderRadius: 8, flexShrink: 0,
          background: "linear-gradient(135deg,#059669,#10b981)",
          display: "flex", alignItems: "center", justifyContent: "center", fontSize: 13,
        }}>👤</div>
        <div style={{ minWidth: 0 }}>
          <div style={{ fontSize: 11, fontWeight: 700, color: "white", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
            {user?.name ?? "User"}
          </div>
          <div style={{ fontSize: 9, color: "#3b82f6", fontWeight: 700 }}>{user?.role}</div>
        </div>
      </div>

      {/* Nav */}
      <nav style={{ flex: 1, padding: "10px 8px", overflowY: "auto" }}>
        {NAV.map(item => {
          const active = isActive(item.to)
          const open = expanded === item.label

          return (
            <div key={item.label} style={{ marginBottom: 2 }}>
              {item.children ? (
                <>
                  <div onClick={() => setExpanded(open ? null : item.label)} style={{
                    display: "flex", alignItems: "center", gap: 8,
                    padding: "8px 10px", borderRadius: 10, cursor: "pointer",
                    background: open || active ? `${item.color}14` : "transparent",
                    border: `1px solid ${open || active ? item.color + "30" : "transparent"}`,
                    transition: "all 0.15s",
                  }}
                    onMouseEnter={e => { if (!open && !active) e.currentTarget.style.background = "rgba(255,255,255,0.04)" }}
                    onMouseLeave={e => { if (!open && !active) e.currentTarget.style.background = "transparent" }}
                  >
                    <span style={{ fontSize: 15, width: 18, textAlign: "center" }}>{item.icon}</span>
                    <span style={{ fontSize: 12, fontWeight: 600, color: open || active ? item.color : "#94a3b8", flex: 1 }}>{item.label}</span>
                    <span style={{ fontSize: 9, color: "#475569", transition: "transform 0.2s", transform: open ? "rotate(180deg)" : "none", display: "inline-block" }}>▼</span>
                  </div>
                  {open && (
                    <div style={{ marginLeft: 18, borderLeft: `1px solid ${item.color}30`, paddingLeft: 10, marginTop: 2, marginBottom: 4 }}>
                      {item.children.map(child => (
                        <Link key={child.to} to={child.to} style={{ textDecoration: "none" }}>
                          <div style={{
                            padding: "6px 10px", borderRadius: 8, marginBottom: 1,
                            fontSize: 11, fontWeight: 500,
                            color: pathname === child.to ? item.color : "#64748b",
                            background: pathname === child.to ? `${item.color}12` : "transparent",
                            transition: "all 0.15s",
                          }}
                            onMouseEnter={e => { if (pathname !== child.to) { e.currentTarget.style.color = "#94a3b8"; e.currentTarget.style.background = "rgba(255,255,255,0.03)" }}}
                            onMouseLeave={e => { if (pathname !== child.to) { e.currentTarget.style.color = "#64748b"; e.currentTarget.style.background = "transparent" }}}
                          >{child.label}</div>
                        </Link>
                      ))}
                    </div>
                  )}
                </>
              ) : (
                <Link to={item.to} style={{ textDecoration: "none" }}>
                  <div style={{
                    display: "flex", alignItems: "center", gap: 8,
                    padding: "8px 10px", borderRadius: 10,
                    background: active ? `${item.color}14` : "transparent",
                    border: `1px solid ${active ? item.color + "30" : "transparent"}`,
                    boxShadow: active ? `0 0 10px ${item.color}18` : "none",
                    transition: "all 0.15s",
                  }}
                    onMouseEnter={e => { if (!active) e.currentTarget.style.background = "rgba(255,255,255,0.04)" }}
                    onMouseLeave={e => { if (!active) e.currentTarget.style.background = "transparent" }}
                  >
                    <span style={{ fontSize: 15, width: 18, textAlign: "center" }}>{item.icon}</span>
                    <span style={{ fontSize: 12, fontWeight: 600, color: active ? item.color : "#94a3b8", flex: 1 }}>{item.label}</span>
                    {active && <div style={{ width: 5, height: 5, borderRadius: "50%", background: item.color, boxShadow: `0 0 6px ${item.color}` }} />}
                  </div>
                </Link>
              )}
            </div>
          )
        })}
      </nav>

      {/* Logout */}
      <div style={{ padding: "10px 8px", borderTop: "1px solid rgba(255,255,255,0.04)" }}>
        <button onClick={() => { clearAuth(); window.location.href = "/login" }} style={{
          width: "100%", padding: "9px 10px", borderRadius: 10, fontSize: 12, fontWeight: 700,
          background: "rgba(239,68,68,0.08)", border: "1px solid rgba(239,68,68,0.2)",
          color: "#f87171", cursor: "pointer", textAlign: "left",
          display: "flex", alignItems: "center", gap: 8,
        }}>
          🚪 Logout
        </button>
      </div>
    </aside>
  )
}
