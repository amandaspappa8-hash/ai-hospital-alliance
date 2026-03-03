import * as React from "react"
import { NavLink } from "react-router-dom"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarRail,
  SidebarSeparator,
} from "@/components/ui/sidebar"

type Item = { title: string; to: string }

const workspace: Item[] = [
  { title: "Home", to: "/" },
  { title: "Overview", to: "/overview" },
  { title: "Dashboard", to: "/dashboard" },
]

const clinical: Item[] = [
  { title: "Patients", to: "/patients" },
  { title: "Appointments", to: "/appointments" },
  { title: "Clinical Notes", to: "/notes" },
]

const orders: Item[] = [
  { title: "Prescriptions", to: "/prescriptions" },
  { title: "Labs", to: "/labs" },
  { title: "Imaging", to: "/imaging" },
  { title: "CT / MRI", to: "/ct-mri" },
]

const documents: Item[] = [
  { title: "Files", to: "/files" },
  { title: "Reports", to: "/reports" },
  { title: "PACS / DICOM", to: "/pacs" },
]

const pharmacy: Item[] = [
  { title: "Formulary", to: "/formulary" },
  { title: "Medications", to: "/medications" },
  { title: "Interactions & Allergies", to: "/interactions" },
]

const system: Item[] = [
  { title: "Settings", to: "/settings" },
  { title: "Logout", to: "/logout" },
]
  
function NavSection({ label, items }: { label: string; items: Item[] }) {
  return (
    <SidebarGroup>
      <SidebarGroupLabel>{label}</SidebarGroupLabel>
      <SidebarGroupContent>
        <SidebarMenu>
          {items.map((item) => (
            <SidebarMenuItem key={item.to}>
              <SidebarMenuButton asChild>
                <NavLink
                  to={item.to}
                  className={({ isActive }) =>
                    isActive ? "font-medium text-foreground" : "text-muted-foreground"
                  }
                  end
                >
                  <span>{item.title}</span>
                </NavLink>
              </SidebarMenuButton>
            </SidebarMenuItem>
          ))}
        </SidebarMenu>
      </SidebarGroupContent>
    </SidebarGroup>
  )
}

export default function AppSidebar() {
  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="px-2">
        <div className="flex items-center gap-2 px-2 py-2">
          <div className="size-8 rounded-md bg-primary/10" />
          <div className="flex flex-col leading-tight">
            <span className="text-sm font-semibold">AI Hospital Alliance</span>
            <span className="text-xs text-muted-foreground">Admin</span>
          </div>
        </div>
      </SidebarHeader>

      <SidebarSeparator />

      <SidebarContent>
        <NavSection label="Workspace" items={workspace} />
        <NavSection label="Clinical" items={clinical} />
        <NavSection label="Orders" items={orders} />
        <NavSection label="Documents" items={documents} />
        <NavSection label="Pharmacy" items={pharmacy} />
        <NavSection label="System" items={system} />
      </SidebarContent>

      <SidebarSeparator />

      <SidebarFooter className="p-2">
        <div className="rounded-md border p-3 text-xs text-muted-foreground">
          Secure Dev Mode
        </div>
      </SidebarFooter>

      <SidebarRail />
    </Sidebar>
  )
}

