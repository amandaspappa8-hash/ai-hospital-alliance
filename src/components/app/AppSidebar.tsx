import { NavLink, useLocation } from "react-router-dom"
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
  ScanLine,
  Baby,
  BarChart3,
} from "lucide-react"
import { getUser } from "@/lib/auth-storage"
import { getSpecialtiesSummary, type SpecialtyRecord } from "@/lib/specialties"
import { useAppLanguage } from "@/i18n/useAppLanguage"

type Role = "Admin" | "Doctor" | "Radiology"

type Item = {
  titleKey: string
  to: string
  roles: Role[]
  icon: React.ReactNode
}

const items: Item[] = [
  {
    titleKey: "nav.dashboard",
    to: "/dashboard",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <LayoutDashboard size={18} />,
  },
  {
    titleKey: "nav.adminOverview",
    to: "/admin-overview",
    roles: ["Admin"],
    icon: <BarChart3 size={18} />,
  },
  {
    titleKey: "nav.aiRouting",
    to: "/ai-routing",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <Brain size={18} />,
  },
  {
    titleKey: "nav.clinicalDecision",
    to: "/clinical-decision",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <ShieldPlus size={18} />,
  },
  {
    titleKey: "nav.orders",
    to: "/orders",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <ClipboardList size={18} />,
  },
  {
    titleKey: "nav.doctors",
    to: "/doctors",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <Stethoscope size={18} />,
  },
  {
    titleKey: "nav.specialties",
    to: "/specialties",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <Building2 size={18} />,
  },
  {
    titleKey: "nav.patients",
    to: "/patients",
    roles: ["Admin", "Doctor"],
    icon: <Users size={18} />,
  },
  {
    titleKey: "nav.patientProfile",
    to: "/patient-profile",
    roles: ["Admin", "Doctor"],
    icon: <UserSquare2 size={18} />,
  },
  {
    titleKey: "nav.appointments",
    to: "/appointments",
    roles: ["Admin", "Doctor"],
    icon: <CalendarDays size={18} />,
  },
  {
    titleKey: "nav.reports",
    to: "/reports",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <FileText size={18} />,
  },
  {
    titleKey: "nav.notes",
    to: "/notes",
    roles: ["Admin", "Doctor"],
    icon: <NotebookPen size={18} />,
  },
  {
    titleKey: "nav.pacs",
    to: "/pacs",
    roles: ["Admin", "Radiology"],
    icon: <ScanSearch size={18} />,
  },
  {
    titleKey: "nav.labs",
    to: "/labs",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <FlaskConical size={18} />,
  },
  {
    titleKey: "nav.nurses",
    to: "/nurses",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <Users size={18} />,
  },
  {
    titleKey: "nav.radiology",
    to: "/radiology",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <ScanLine size={18} />,
  },
  {
    titleKey: "nav.pharmacy",
    to: "/pharmacy",
    roles: ["Admin", "Doctor", "Radiology"],
    icon: <Pill size={18} />,
  },
  {
    titleKey: "nav.logout",
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
          {t("app.name")}
        </div>
        <div style={{ fontSize: 13, opacity: 0.7, marginTop: 6 }}>
          {t("app.tagline")}
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
          {t("user.signedInAs")}
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
          {t("label.language")}
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
                <span>{t(item.titleKey)}</span>
              </NavLink>

              {isSpecialtiesRoot && showSpecialtyChildren && (
                <div
                  style={{
                    marginTop: 8,
                    marginLeft: 12,
                    paddingLeft: 12,
                    borderLeft: "1px dashed #334155",
                    display: "flex",
                    flexDirection: "column",
                    gap: 8,
                  }}
                >
                  {specialties.map((specialty) => (
                    <NavLink
                      key={specialty.title}
                      to={specialty.route}
                      style={({ isActive }) => ({
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
                      })}
                    >
                      <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
                        {specialtyIconMap[specialty.title] ?? <Building2 size={16} />}
                        {specialty.title}
                      </span>
                      <span
                        style={{
                          minWidth: 28,
                          textAlign: "center",
                          padding: "2px 8px",
                          borderRadius: 999,
                          background: "#0f172a",
                          color: "#7dd3fc",
                          fontSize: 12,
                          fontWeight: 700,
                        }}
                      >
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
