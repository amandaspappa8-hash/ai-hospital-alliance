import * as React from "react"
import { useLocation } from "react-router-dom"
import { LayoutDashboard, Brain, Activity, ClipboardList, Stethoscope, Users, CalendarDays, FileText, HeartPulse } from "lucide-react"

import AppSidebar from "@/components/app/AppSidebar"
import { SidebarProvider, SidebarInset, SidebarTrigger } from "@/components/ui/sidebar"
import { Separator } from "@/components/ui/separator"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"

type AdminLayoutProps = {
  children: React.ReactNode
  title?: string
  subtitle?: string
  actions?: React.ReactNode
}

function useCrumbs() {
  const { pathname } = useLocation()
  return pathname.split("/").filter(Boolean)
}

function titleFromPart(part: string) {
  return part
    .replace(/[-_]/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase())
}

export default function AdminLayout({ children, title, subtitle, actions }: AdminLayoutProps) {
  const parts = useCrumbs()

  return (
    <SidebarProvider>
      <AppSidebar />

      <SidebarInset>
        <header className="sticky top-0 z-10 flex h-14 items-center gap-2 border-b bg-background px-4">
          <SidebarTrigger />
          <Separator orientation="vertical" className="h-6" />

          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem>
                <BreadcrumbPage>AI Hospital Alliance</BreadcrumbPage>
              </BreadcrumbItem>

              {parts.map((p, i) => (
                <React.Fragment key={`${p}-${i}`}>
                  <BreadcrumbSeparator />
                  <BreadcrumbItem>
                    <BreadcrumbPage>{titleFromPart(p)}</BreadcrumbPage>
                  </BreadcrumbItem>
                </React.Fragment>
              ))}
            </BreadcrumbList>
          </Breadcrumb>

          {/* right side */}
          <div className="ml-auto flex items-center gap-2">{actions}</div>
        </header>

        {/* optional page heading */}
        {(title || subtitle) && (
          <div className="px-4 pt-4">
            {title && <h1 className="text-2xl font-semibold">{title}</h1>}
            {subtitle && <p className="text-sm text-muted-foreground">{subtitle}</p>}
          </div>
        )}

        <main className="p-4 md:p-6">{children}</main>
      </SidebarInset>
    </SidebarProvider>
  )
}
