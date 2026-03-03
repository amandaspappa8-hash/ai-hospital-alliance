import * as React from "react"
import AppSidebar from "@/components/app/AppSidebar"
import { SidebarProvider, SidebarInset, SidebarTrigger } from "@/components/ui/sidebar"
import { Separator } from "@/components/ui/separator"
import { Breadcrumb, BreadcrumbItem, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from "@/components/ui/breadcrumb"
import { useLocation } from "react-router-dom"

function useCrumbs() {
  const { pathname } = useLocation()
  const parts = pathname.split("/").filter(Boolean)
  return parts
}

export default function AdminLayout({ children }: { children: React.ReactNode }) {
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
              {parts.length > 0 && <BreadcrumbSeparator />}
              {parts.map((p, idx) => {
                const isLast = idx === parts.length - 1
                return (
                  <React.Fragment key={idx}>
                    <BreadcrumbItem>
                      <BreadcrumbPage className={isLast ? "font-medium" : "text-muted-foreground"}>
                        {p}
                      </BreadcrumbPage>
                    </BreadcrumbItem>
                    {!isLast && <BreadcrumbSeparator />}
                  </React.Fragment>
                )
              })}
            </BreadcrumbList>
          </Breadcrumb>
        </header>

        <main className="p-4">{children}</main>
      </SidebarInset>
    </SidebarProvider>
  )
}
