import { NavLink, Link, useLocation } from "react-router-dom"
import { useEffect, useState } from "react"
import {
  FlaskConical,
  LayoutDashboard,
  Brain,
  ClipboardList,
  Users,
  UserSquare2,
  CalendarDays,
  FileText,
  NotebookPen,
  ScanSearch,
  LogOut,
  Pill,
  ShieldPlus,
  Stethoscope,
  Building2,
  HeartPulse,
  BrainCircuit,
  Ambulance,
  ActivitySquare,
  ScanLine, Box,
  Baby,
  BarChart3,
} from "lucide-react"
import { getUser } from "@/lib/auth-storage"
import { getSpecialtiesSummary, type SpecialtyRecord } from "@/lib/specialties"
import { useAppLanguage } from "@/i18n/useAppLanguage"

type Role = "Admin" | "Doctor" | "Radiology"

type Item = {
  title: string
  to: string
  roles: Role[]
  icon: React.ReactNode
}

const items: Item[] = [
  
{
  title: "Live Bed Management",
  to: "/live-bed-management",
  icon: "🛏️",
  roles: ["Admin", "Doctor"],
},
{
  title: "ICU Intelligence Center",
  to: "/icu-intelligence-center",
  icon: "🫀",
  roles: ["Admin", "Doctor"],
},

{
  title: "Radiology Operations Center",
  to: "/radiology-operations-center",
  icon: <ScanLine />,
  roles: ["Admin","Doctor","Radiology"],
},

{
  title: "Laboratory Operations Center",
  to: "/laboratory-operations-center",
  icon: <FlaskConical />,
  roles: ["Admin","Doctor","Radiology"],
},

{
  title: "Emergency Command Center",
  to: "/emergency-command-center",
  icon: "🚑",
  roles: ["Admin", "Doctor"],
},

{
  title: "Autonomous Patient Flow",
  to: "/autonomous-patient-flow",
  icon: "🔄",
  roles: ["Admin", "Doctor"],
},

{
  title: "Hospital Operations Center",
  to: "/hospital-operations-center",
  icon: "🏥",
  roles: ["Admin", "Doctor"],
},
{
    title: "Dashboard",
    to: "/dashboard",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <LayoutDashboard size={18} />,
  },
  {
    title: "Admin Overview",
    to: "/admin",
    roles: ["Admin"],
    icon: <BarChart3 size={18} />,
  },
  {
    title: "AI Routing",
    to: "/ai-routing",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <Brain size={18} />,
  },
  {
    title: "AI Clinical",
    to: "/ai-clinical",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <Brain size={18} />,
  },
  {
    title: "Orders",
    to: "/orders",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <ClipboardList size={18} />,
  },
  {
    title: "Doctors",
    to: "/doctors",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <Stethoscope size={18} />,
  },
  {
    title: "Specialties",
    to: "/specialties",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <Building2 size={18} />,
  },
  {
    title: "Patients",
    to: "/patients",
    roles: ["Admin", "Doctor"],
    icon: <Users size={18} />,
  },
  {
    title: "Appointments",
    to: "/appointments",
    roles: ["Admin", "Doctor"],
    icon: <CalendarDays size={18} />,
  },
  {
    title: "Reports",
    to: "/reports",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <FileText size={18} />,
  },
  {
    title: "Clinical Notes",
    to: "/notes",
    roles: ["Admin", "Doctor"],
    icon: <NotebookPen size={18} />,
  },
  {
    title: "PACS",
    to: "/pacs",
    roles: ["Admin", "Radiology"],
    icon: <ScanSearch size={18} />,
  },
  {
    title: "Laboratory",
    to: "/labs",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <FlaskConical size={18} />,
  },
  {
    title: "Nursing",
    to: "/nursing",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <Users size={18} />,
  },
  {
    title: "Radiology",
    to: "/radiology",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <ScanLine size={18} />,
  },
  {
    title: "3D Viewer",
    to: "/radiology-3d",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <ScanSearch size={18} />,
  },
  {
    title: "VTK Volume",
    to: "/medical-volume-vtk",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <Box size={18} />,
  },
  {
    title: "Surgical AI",
    to: "/real-medical-volume",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <Brain size={18} />,
  },
  {
    title: "Pharmacy",
    to: "/pharmacy",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <Pill size={18} />,
  },
  {
    title: "Logout",
    to: "/logout",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <LogOut size={18} />,
  },
]

const specialtyIconMap: Record<string, React.ReactNode> = {
  Cardiology: <HeartPulse size={16} />,
  Neurology: <BrainCircuit size={16} />,
  Emergency: <Ambulance size={16} />,
  ICU: <ActivitySquare size={16} />,
  Radiology: <ScanLine size={16} />,
  Pediatrics: <Baby size={16} />,
}

const globalAhosNav = [
  


["AHOS 56.3 Safety Center", "/ahos/56.3/unified-safety-center"],
["AHOS 56.1 Physician Review", "/ahos/56.1/physician-review"],
["AHOS 56.0 Orchestration", "/ahos/56.0/avatar-orchestration"],
["AHOS 55.9 Voice Memory", "/ahos/55.9/avatar-voice-memory-pipeline"],
["AHOS 55.8 Avatar Memory", "/ahos/55.8/avatar-memory-audit"],
["AHOS 55.7 Voice Context", "/ahos/55.7/voice-clinical-context"],
["🏥 Operations","/hospital-operations-center"],
  ["🛏️ Bed Management","/live-bed-management"],
  ["🧠 ICU Intelligence","/icu-intelligence-center"],
  ["🚨 Emergency Command","/emergency-command-center"],
  ["👥 Patient Flow","/autonomous-patient-flow"],
  ["🩻 Radiology Ops","/radiology-operations-center"],
  ["🧪 Laboratory Ops","/laboratory-operations-center"],
  ["💊 Pharmacy Ops","/pharmacy-operations-center"],
  
["🤖 Medical AI Avatar","/medical-ai-avatar"],
["🧑‍⚕️ Arabic Avatar Command","/arabic-avatar-command"],
["AHOS 55.6 Real Avatar", "/ahos/55.6/real-digital-human-avatar"],
["👩‍⚕️ Digital Human Avatar","/digital-human-avatar"],
["🧠 Enterprise Avatar","/enterprise-avatar-dashboard"],
["🎤 Voice & Video Avatar","/realtime-medical-avatar"],
["🧠 AHOS Brain","/ahos-26-0-autonomous-brain"],

  ["🌍 Situation Room","/ahos-25-8-situation-room"],
  ["🚨 Crisis Command","/ahos-25-9-crisis-command-center"],
  ["🌐 Federation 3D","/ahos-25-7-global-federation-3d-map"],
  ["🧬 Neural Network","/ahos-25-6-neural-network"],
  ["❤️ Cardiology","/specialties/cardiology"],
  ["🧠 Neurology","/specialties/neurology"],
  ["🚑 Emergency","/specialties/emergency"],
  ["🏥 ICU","/specialties/icu"],
  ["👶 Pediatrics","/specialties/pediatrics"],
  ["🩻 Radiology","/radiology"],
  ["🧊 Radiology 3D","/radiology-3d"],
  ["🧬 CT/MRI Engine","/medical-volume-vtk"],
  ["📡 Real Medical Volume","/real-medical-volume"],
  ["📺 PACS","/pacs"],
  ["🧪 Labs","/labs"],
  ["💊 Smart Pharmacy","/pharmacy"],
  ["📡 AI Ultrasound","/ai-ultrasound-x"],
  ["🤖 AI Clinical","/ai-clinical"],
  ["🧭 AI Routing","/ai-routing"],
  ["🧠 Clinical Decision","/clinical-decision"]
];

export default function AppSidebar() {
  const { t, language, setLanguage } = useAppLanguage()
  const user = getUser()
  const role = user?.role as Role | undefined
  const location = useLocation()

  const [specialties, setSpecialties] = useState<SpecialtyRecord[]>([])

  useEffect(() => {
    async function loadSpecialties() {
      try {
        const data = await getSpecialtiesSummary()
        setSpecialties(data)
      } catch (err) {
        console.error("Failed to load specialties summary", err)
        setSpecialties([])
      }
    }

    loadSpecialties()
  }, [])

  const visibleItems = role ? items.filter((item) => item.roles.includes(role)) : []
  const showSpecialtyChildren = location.pathname.startsWith("/specialties")
  const showPharmacyChildren = location.pathname.startsWith("/pharmacy")
  

  return (
    <aside
      style={{
        width: 280,
        padding: 20,
        background: "#0f172a",
        color: "white",
        minHeight: "100vh",
        borderRight: "1px solid #1e293b",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div
        style={{
          padding: "8px 4px 18px",
          borderBottom: "1px solid #1e293b",
          marginBottom: 18,
        }}
      >
        <div style={{ fontWeight: 800, fontSize: 22, letterSpacing: 0.2 }}>
          AI Hospital Alliance
        </div>
        <div style={{ fontSize: 13, opacity: 0.7, marginTop: 6 }}>
          Healthcare Command Center
        </div>
      </div>

      <div
        style={{
          background: "#111827",
          border: "1px solid #1f2937",
          borderRadius: 14,
          padding: 14,
          marginBottom: 18,
        }}
      >
        <div style={{ fontSize: 13, opacity: 0.7, marginBottom: 6 }}>
          Signed in as
        </div>
        <div style={{ fontWeight: 700 }}>
          {user ? user.name : t("user.guest")}
        </div>
        <div style={{ fontSize: 14, color: "#93c5fd", marginTop: 4 }}>
          {user ? user.role : t("user.noRole")}
        </div>
      </div>

      <div
        style={{
          background: "#111827",
          border: "1px solid #1f2937",
          borderRadius: 14,
          padding: 14,
          marginBottom: 18,
        }}
      >
        <div style={{ fontSize: 13, opacity: 0.7, marginBottom: 8 }}>
          Language
        </div>
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value as "ar" | "en" | "fr" | "it" | "tzm")}
          style={{
            width: "100%",
            background: "#020617",
            color: "white",
            border: "1px solid #334155",
            borderRadius: 10,
            padding: "10px 12px",
          }}
        >
          <option value="en">English</option>
          <option value="ar">العربية</option>
          <option value="fr">Français</option>
          <option value="it">Italiano</option>
          <option value="tzm">Tamaziɣt</option>
        </select>
      <div style={{marginTop:24}}>
        <div style={{
          color:"#67e8f9",
          fontWeight:900,
          marginBottom:12,
          borderTop:"1px solid rgba(255,255,255,0.08)",
          paddingTop:14,
          letterSpacing:1
        }}>
          🌍 Global AHOS Navigation
        </div>

        <div style={{
          maxHeight:420,
          overflowY:"auto",
          display:"grid",
          gap:8,
          paddingRight:4
        }}>
          {globalAhosNav.map(([label,to])=>(
            <Link
              key={to}
              to={to}
              style={{
                textDecoration:"none",
                color:"#e2e8f0",
                background:"rgba(15,23,42,0.65)",
                border:"1px solid rgba(34,211,238,0.15)",
                borderRadius:12,
                padding:"8px 12px",
                fontSize:13,
                fontWeight:700
              }}
            >
              {label}
            </Link>
          ))}
        </div>
      </div>

      </div>

      <nav style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        {visibleItems.map((item) => {
          const isSpecialtiesRoot = item.to === "/specialties"

          return (
            <div key={item.to}>
              <NavLink
                to={item.to}
                style={({ isActive }) => ({
                  display: "flex",
                  alignItems: "center",
                  gap: 12,
                  padding: "12px 14px",
                  borderRadius: 12,
                  color: isActive ? "#ffffff" : "#cbd5e1",
                  background: isActive ? "#0ea5e9" : "transparent",
                  textDecoration: "none",
                  fontWeight: isActive ? 700 : 500,
                  border: isActive ? "1px solid #38bdf8" : "1px solid transparent",
                })}
              >
                {item.icon}
                <span>{item.title}</span>
              </NavLink>

              {item.to === "/pharmacy" && showPharmacyChildren && (
                <div style={{ marginTop: 8, marginLeft: 12, paddingLeft: 12, borderLeft: "1px dashed #334155", display: "flex", flexDirection: "column", gap: 8 }}>
                  {[
                    { title: "Medications", to: "/pharmacy/medications" },
                    { title: "Drug Formulary", to: "/pharmacy/formulary" },
                    { title: "Drug Interactions", to: "/pharmacy/interactions" },
                    { title: "Discharge Meds", to: "/pharmacy/discharge" },
                    { title: "Prescriptions", to: "/pharmacy/prescriptions" },
                  ].map((child) => (
                    <NavLink key={child.to} to={child.to} style={({ isActive }) => ({
                      display: "flex",
                      alignItems: "center",
                      gap: 8,
                      padding: "10px 12px",
                      borderRadius: 10,
                      color: isActive ? "#ffffff" : "#cbd5e1",
                      background: isActive ? "#1d4ed8" : "#0b1220",
                      textDecoration: "none",
                      fontSize: 14,
                      border: "1px solid #1e293b",
                    })}>
                      <Pill size={16} />
                      <span>{child.title}</span>
                    </NavLink>
                  ))}
                </div>
              )}

              {isSpecialtiesRoot && showSpecialtyChildren && (
                <div style={{ marginTop: 8, marginLeft: 12, paddingLeft: 12, borderLeft: "1px dashed #334155", display: "flex", flexDirection: "column", gap: 8 }}>
                  {specialties.map((specialty) => (
                    <NavLink key={specialty.title} to={specialty.route} style={({ isActive }) => ({
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                      gap: 10,
                      padding: "10px 12px",
                      borderRadius: 10,
                      color: isActive ? "#ffffff" : "#cbd5e1",
                      background: isActive ? "#1d4ed8" : "#0b1220",
                      textDecoration: "none",
                      fontSize: 14,
                      border: "1px solid #1e293b",
                    })}>
                      <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
                        {specialtyIconMap[specialty.title] ?? <Building2 size={16} />}
                        {specialty.title}
                      </span>
                      <span style={{ minWidth: 28, textAlign: "center", padding: "2px 8px", borderRadius: 999, background: "#0f172a", color: "#7dd3fc", fontSize: 12, fontWeight: 700 }}>
                        {specialty.activeCases}
                      </span>
                    </NavLink>
                  ))}
                </div>
              )}
            </div>
          )
        })}
      </nav>

    </aside>
  )
}