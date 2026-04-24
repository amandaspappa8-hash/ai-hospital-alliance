import { ReactNode } from "react"

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return <div style={{ minHeight: "100vh" }}>{children}</div>
}
