import AdminLayout from "@/layouts/AdminLayout"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"

const stats = [
  { title: "Total Patients", value: "2,420", hint: "+4.7% / month" },
  { title: "New Appointments", value: "226", hint: "+10.3% / month" },
  { title: "Pending Reports", value: "193", hint: "-2.5% / month" },
  { title: "Active Beds", value: "106", hint: "Stable" },
]

const rows = [
  { id: "A-1021", name: "Sara Ali", dept: "Cardiology", status: "In Review" },
  { id: "A-1022", name: "John Smith", dept: "Neurology", status: "Approved" },
  { id: "A-1023", name: "Mona Omar", dept: "Radiology", status: "Pending" },
  { id: "A-1024", name: "Khaled Noor", dept: "Orthopedics", status: "Approved" },
]

function StatusBadge({ s }: { s: string }) {
  if (s === "Approved") return <Badge>Approved</Badge>
  if (s === "Pending") return <Badge variant="secondary">Pending</Badge>
  return <Badge variant="outline">In Review</Badge>
}

export default function Dashboard() {
  return (
    <AdminLayout
      title="Dashboard"
      subtitle="Overview of key hospital metrics"
      actions={<Button variant="outline" size="sm">New</Button>}
    >
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((s) => (
          <Card key={s.title}>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">{s.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-semibold">{s.value}</div>
              <div className="text-xs text-muted-foreground">{s.hint}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="mt-6 flex items-center justify-between gap-3">
        <div className="text-sm font-medium">Recent Appointments</div>
        <div className="w-full max-w-sm">
          <Input placeholder="Search patient…" />
        </div>
      </div>

      <Separator className="my-4" />

      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-base">Appointments</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[120px]">Ref</TableHead>
                  <TableHead>Patient</TableHead>
                  <TableHead>Department</TableHead>
                  <TableHead className="text-right">Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {rows.map((r) => (
                  <TableRow key={r.id}>
                    <TableCell className="font-medium">{r.id}</TableCell>
                    <TableCell>{r.name}</TableCell>
                    <TableCell className="text-muted-foreground">{r.dept}</TableCell>
                    <TableCell className="text-right">
                      <StatusBadge s={r.status} />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </AdminLayout>
  )
}
