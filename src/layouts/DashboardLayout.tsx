import { Outlet, useLocation } from "react-router-dom"
import Sidebar from "@/components/Sidebar"
import Topbar from "@/components/Topbar"

export default function DashboardLayout() {
  const location = useLocation()

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="mx-auto flex w-full max-w-[1400px]">
        <Sidebar currentPath={location.pathname} />
        <main className="min-w-0 flex-1">
          <Topbar />
          <div className="p-4 md:p-6">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  )
}
