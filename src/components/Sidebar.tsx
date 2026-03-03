import { Link } from "react-router-dom"
import { cn } from "@/lib/utils"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import {
  LayoutDashboard,
  Users,
  Calendar,
  FileText,
  Settings,
  HeartPulse,
} from "lucide-react"

type Props = { currentPath: string }

const nav = [
  { to: "/overview", label: "Overview", icon: LayoutDashboard },
  { to: "/patients", label: "Patients", icon: Users, badge: "New" },
  { to: "/appointments", label: "Appointments", icon: Calendar },
  { to: "/reports", label: "Reports", icon: FileText },
  { to: "/settings", label: "Settings", icon: Settings },
]

export default function Sidebar({ currentPath }: Props) {
  return (
    <aside className="sticky top-0 hidden h-screen w-[280px] shrink-0 border-r bg-card/30 backdrop-blur md:block">
      <div className="flex h-full flex-col">
        <div className="p-5">
          <div className="flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary text-primary-foreground">
              <HeartPulse className="h-5 w-5" />
            </div>
            <div className="leading-tight">
              <div className="font-semibold">AI Hospital Alliance</div>
              <div className="text-xs text-muted-foreground">Medical-grade UI</div>
            </div>
          </div>
        </div>

        <Separator />

        <nav className="flex-1 space-y-1 p-3">
          {nav.map((item) => {
            const active = currentPath === item.to
            const Icon = item.icon
            return (
              <Link
                key={item.to}
                to={item.to}
                className={cn(
                  "flex items-center justify-between rounded-xl px-3 py-2 text-sm transition",
                  active
                    ? "bg-primary/10 text-primary"
                    : "text-muted-foreground hover:bg-muted hover:text-foreground"
                )}
              >
                <span className="flex items-center gap-2">
                  <Icon className="h-4 w-4" />
                  {item.label}
                </span>
                {item.badge ? <Badge variant="secondary">{item.badge}</Badge> : null}
              </Link>
            )
          })}
        </nav>

        <div className="p-4 text-xs text-muted-foreground">
          v0.1 • Vite + Tailwind + shadcn/ui
        </div>
      </div>
    </aside>
  )
}
