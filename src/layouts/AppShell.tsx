import { PropsWithChildren } from "react"
import { Link, useLocation } from "react-router-dom"
import { LayoutDashboard, Folder, Home, LogIn } from "lucide-react"
import { Separator } from "@/components/ui/separator"

const nav = [
  { to: "/", label: "Home", icon: Home },
  { to: "/overview", label: "Dashboard", icon: LayoutDashboard },
  { to: "/files", label: "File Manager", icon: Folder },
  { to: "/login", label: "Login", icon: LogIn },
]

export default function AppShell({ children }: PropsWithChildren) {
  const { pathname } = useLocation()

  return (
    <div className="min-h-screen bg-background">
      <div className="flex">
        {/* Sidebar */}
        <aside className="hidden md:flex md:w-72 md:flex-col md:border-r md:bg-muted/20">
          <div className="px-6 py-5">
            <div className="text-lg font-semibold">AI Hospital Alliance</div>
            <div className="text-xs text-muted-foreground">Admin Console</div>
          </div>
          <Separator />
          <nav className="p-3 space-y-1">
            {nav.map((item) => {
              const Icon = item.icon
              const active = pathname === item.to
              return (
                <Link
                  key={item.to}
                  to={item.to}
                  className={[
                    "flex items-center gap-3 rounded-xl px-3 py-2 text-sm transition",
                    active
                      ? "bg-muted text-foreground"
                      : "text-muted-foreground hover:bg-muted/60 hover:text-foreground",
                  ].join(" ")}
                >
                  <Icon className="h-4 w-4" />
                  {item.label}
                </Link>
              )
            })}
          </nav>

          <div className="mt-auto p-4 text-xs text-muted-foreground">
            v0.1 • Vite + React + shadcn/ui
          </div>
        </aside>

        {/* Content */}
        <main className="flex-1">
          <header className="sticky top-0 z-10 border-b bg-background/80 backdrop-blur">
            <div className="mx-auto max-w-6xl px-4 py-3 flex items-center justify-between">
              <div className="text-sm text-muted-foreground">
                {pathname === "/" ? "Home" : pathname.replace("/", "")}
              </div>
              <div className="text-xs text-muted-foreground">
                Local • Secure Dev Mode
              </div>
            </div>
          </header>

          <div className="mx-auto max-w-6xl px-4 py-6">{children}</div>
        </main>
      </div>
    </div>
  )
}
