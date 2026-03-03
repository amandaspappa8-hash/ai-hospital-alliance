import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Link } from "react-router-dom"

export default function Home() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-10">

      <div className="flex items-start justify-between gap-6">
        <div>
          <h1 className="text-3xl font-bold">AI Hospital Alliance</h1>

          <p className="mt-2 text-muted-foreground">
            Medical-grade interface starter: Dashboard + File Manager + Auth routes.
          </p>

          <div className="mt-4 flex gap-2">
            <Button asChild>
              <Link to="/overview">Open Dashboard</Link>
            </Button>

            <Button asChild variant="outline">
              <Link to="/files">Open File Manager</Link>
            </Button>
          </div>
        </div>

        <div className="text-sm text-muted-foreground">
          Public
        </div>
      </div>

      <Card className="mt-6">
        <CardContent className="py-5">
          <div className="font-semibold mb-2">Next steps</div>

          <ul className="list-disc pl-5 text-muted-foreground space-y-1">
            <li>Add real modules (patients, appointments, reports)</li>
            <li>Connect API</li>
            <li>Role-based access</li>
          </ul>
        </CardContent>
      </Card>

    </div>
  )
}
