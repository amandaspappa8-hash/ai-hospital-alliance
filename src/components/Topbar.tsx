import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Bell, Search } from "lucide-react"

export default function Topbar() {
  return (
    <header className="sticky top-0 z-10 border-b bg-background/70 backdrop-blur">
      <div className="flex items-center gap-3 p-4 md:p-5">
        <div className="relative w-full max-w-md">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input className="pl-9" placeholder="Search patients, reports, appointments..." />
        </div>

        <div className="ml-auto flex items-center gap-2">
          <Button variant="outline" size="icon" className="rounded-xl">
            <Bell className="h-4 w-4" />
          </Button>

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <button className="flex items-center gap-2 rounded-xl border bg-card px-2 py-1.5 hover:bg-muted">
                <Avatar className="h-7 w-7">
                  <AvatarFallback>MF</AvatarFallback>
                </Avatar>
                <span className="hidden text-sm md:block">Mohammed</span>
              </button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-48">
              <DropdownMenuItem>Profile</DropdownMenuItem>
              <DropdownMenuItem>Team</DropdownMenuItem>
              <DropdownMenuItem>Sign out</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  )
}
