import { Link } from "react-router-dom"
import { useCurrentUser } from "@/hooks/use-current-user"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

export default function Topbar() {
  const user = useCurrentUser()

  return (
    <header className="flex items-center justify-between border-b bg-background px-4 py-3 md:px-6">
      <div>
        <h1 className="text-lg font-semibold">AI Hospital Alliance</h1>
        <p className="text-sm text-muted-foreground">
          Medical-grade hospital workspace
        </p>
      </div>

      <div className="flex items-center gap-3">
        {user ? (
          <>
            <div className="hidden text-right sm:block">
              <div className="text-sm font-medium">{user.name}</div>
              <div className="text-xs text-muted-foreground">{user.username}</div>
            </div>

            <Badge variant="secondary">{user.role}</Badge>

            <Link to="/logout">
              <Button variant="outline">Logout</Button>
            </Link>
          </>
        ) : (
          <Link to="/login">
            <Button>Login</Button>
          </Link>
        )}
      </div>
    </header>
  )
}
