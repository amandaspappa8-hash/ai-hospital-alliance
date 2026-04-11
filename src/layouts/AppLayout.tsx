import AppSidebar from "@/components/app/AppSidebar"
import { Outlet, useLocation } from "react-router-dom"
import { getUser } from "@/lib/auth-storage"
import { useAppLanguage } from "@/i18n/useAppLanguage"

function getPageTitle(pathname: string, t: (key: string) => string) {
  if (pathname.startsWith("/dashboard")) return t("nav.dashboard")
  if (pathname.startsWith("/ai-routing")) return t("layout.title.aiRouting")
  if (pathname.startsWith("/orders")) return t("layout.title.orders")
  if (pathname.startsWith("/patients")) return t("nav.patients")
  if (pathname.startsWith("/patient-profile")) return t("nav.patientProfile")
  if (pathname.startsWith("/appointments")) return t("nav.appointments")
  if (pathname.startsWith("/reports")) return t("nav.reports")
  if (pathname.startsWith("/notes")) return t("layout.title.notes")
  if (pathname.startsWith("/pacs")) return t("nav.pacs")
  return t("app.name")
}

function getPageSubtitle(pathname: string, t: (key: string) => string) {
  if (pathname.startsWith("/dashboard")) return t("layout.subtitle.dashboard")
  if (pathname.startsWith("/ai-routing")) return t("layout.subtitle.aiRouting")
  if (pathname.startsWith("/orders")) return t("layout.subtitle.orders")
  if (pathname.startsWith("/patients")) return t("layout.subtitle.patients")
  if (pathname.startsWith("/patient-profile")) return t("layout.subtitle.patientProfile")
  if (pathname.startsWith("/appointments")) return t("layout.subtitle.appointments")
  if (pathname.startsWith("/reports")) return t("layout.subtitle.reports")
  if (pathname.startsWith("/notes")) return t("layout.subtitle.notes")
  if (pathname.startsWith("/pacs")) return t("layout.subtitle.pacs")
  return t("layout.subtitle.default")
}

export default function AppLayout() {
  const location = useLocation()
  const user = getUser()
  const { t } = useAppLanguage()

  const title = getPageTitle(location.pathname, t)
  const subtitle = getPageSubtitle(location.pathname, t)

  return (
    <div
      style={{
        display: "flex",
        minHeight: "100vh",
        background: "#020617",
      }}
    >
      <AppSidebar />

      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        <header
          style={{
            position: "sticky",
            top: 0,
            zIndex: 10,
            background: "rgba(2, 6, 23, 0.92)",
            backdropFilter: "blur(8px)",
            borderBottom: "1px solid #1e293b",
            padding: "18px 28px",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              gap: 16,
            }}
          >
            <div>
              <div style={{ color: "white", fontSize: 24, fontWeight: 800 }}>
                {title}
              </div>
              <div style={{ color: "#94a3b8", fontSize: 14, marginTop: 4 }}>
                {subtitle}
              </div>
            </div>

            <div
              style={{
                background: "#0f172a",
                border: "1px solid #1e293b",
                borderRadius: 14,
                padding: "10px 14px",
                minWidth: 180,
              }}
            >
              <div style={{ color: "#94a3b8", fontSize: 12 }}>
                {t("user.currentUser")}
              </div>
              <div style={{ color: "white", fontWeight: 700, marginTop: 2 }}>
                {user?.name ?? t("user.guest")}
              </div>
              <div style={{ color: "#38bdf8", fontSize: 13, marginTop: 2 }}>
                {user?.role ?? t("user.noRole")}
              </div>
            </div>
          </div>
        </header>

        <main style={{ padding: 28, color: "white", flex: 1 }}>
          <div
            style={{
              maxWidth: 1400,
            }}
          >
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  )
}
