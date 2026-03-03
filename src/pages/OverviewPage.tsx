import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { OverviewChart, RecentActivity } from "@/components/app/OverviewWidgets"

export default function OverviewPage() {
  const stats = [
    { title: "Total Patients", value: "2,420" },
    { title: "New Appointments", value: "226" },
    { title: "Pending Reports", value: "193" },
    { title: "Bed Occupancy", value: "78%" },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Overview</h1>
        <p className="text-sm text-muted-foreground">Hospital operations snapshot.</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((s) => (
          <Card key={s.title} className="rounded-2xl">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm text-muted-foreground">{s.title}</CardTitle>
            </CardHeader>
            <CardContent className="text-2xl font-bold">{s.value}</CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <OverviewChart />
        </div>
        <RecentActivity />
      </div>
    </div>
  )
}
