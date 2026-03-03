import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts"

const visitors = [
  { d: "Mon", v: 120 },
  { d: "Tue", v: 160 },
  { d: "Wed", v: 140 },
  { d: "Thu", v: 220 },
  { d: "Fri", v: 180 },
  { d: "Sat", v: 260 },
  { d: "Sun", v: 240 },
]

const recent = [
  { id: "P-10291", name: "Patient A", dept: "Cardiology", status: "In Review" },
  { id: "P-10274", name: "Patient B", dept: "Radiology", status: "Completed" },
  { id: "P-10260", name: "Patient C", dept: "ER", status: "Pending" },
  { id: "P-10241", name: "Patient D", dept: "Lab", status: "In Review" },
]

export function OverviewChart() {
  return (
    <Card className="rounded-2xl">
      <CardHeader>
        <CardTitle className="text-sm">Visitors Statistics</CardTitle>
      </CardHeader>
      <CardContent className="h-56">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={visitors}>
            <XAxis dataKey="d" tickLine={false} axisLine={false} />
            <YAxis tickLine={false} axisLine={false} width={30} />
            <Tooltip />
            <Line type="monotone" dataKey="v" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}

export function RecentActivity() {
  return (
    <Card className="rounded-2xl">
      <CardHeader>
        <CardTitle className="text-sm">Recent Activity</CardTitle>
      </CardHeader>
      <CardContent className="text-sm">
        <div className="grid grid-cols-4 gap-2 pb-2 font-medium text-muted-foreground">
          <div>ID</div>
          <div>Name</div>
          <div>Department</div>
          <div>Status</div>
        </div>
        <div className="space-y-2">
          {recent.map((r) => (
            <div key={r.id} className="grid grid-cols-4 gap-2 items-center">
              <div className="font-mono text-xs">{r.id}</div>
              <div>{r.name}</div>
              <div className="text-muted-foreground">{r.dept}</div>
              <div>
                <Badge variant={r.status === "Completed" ? "default" : "secondary"}>
                  {r.status}
                </Badge>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
