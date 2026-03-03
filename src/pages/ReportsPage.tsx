import { useMemo, useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"

type ReportStatus = "pending" | "in_review" | "completed"

type Report = {
  id: string
  title: string
  patient: string
  type: "Radiology" | "Lab" | "Discharge" | "ER"
  status: ReportStatus
  updated: string
}

const REPORTS: Report[] = [
  { id: "R-7711", title: "CT Head", patient: "Patient A", type: "Radiology", status: "in_review", updated: "Today" },
  { id: "R-7709", title: "CBC Panel", patient: "Patient C", type: "Lab", status: "pending", updated: "Yesterday" },
  { id: "R-7701", title: "Discharge Summary", patient: "Emily Brown", type: "Discharge", status: "completed", updated: "3d ago" },
  { id: "R-7688", title: "ER Triage", patient: "Patient B", type: "ER", status: "pending", updated: "1w ago" },
]

function rBadge(s: ReportStatus) {
  if (s === "pending") return <Badge variant="secondary">Pending</Badge>
  if (s === "in_review") return <Badge>In review</Badge>
  return <Badge variant="outline">Completed</Badge>
}

export default function ReportsPage() {
  const [tab, setTab] = useState<"all" | "pending" | "completed">("all")
  const [q, setQ] = useState("")

  const rows = useMemo(() => {
    const query = q.trim().toLowerCase()
    return REPORTS.filter((r) => {
      const matchesQuery =
        !query ||
        r.title.toLowerCase().includes(query) ||
        r.patient.toLowerCase().includes(query) ||
        r.id.toLowerCase().includes(query)

      const matchesTab =
        tab === "all" ? true : tab === "pending" ? r.status !== "completed" : r.status === "completed"

      return matchesQuery && matchesTab
    })
  }, [q, tab])

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">Reports</h1>
          <p className="text-sm text-muted-foreground">Reports queue with quick actions.</p>
        </div>
        <Button variant="outline">Export</Button>
      </div>

      <Card className="rounded-2xl">
        <CardHeader className="pb-3">
          <CardTitle className="text-base">Reports</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
            <div className="w-full md:max-w-sm">
              <Input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search reports..." />
            </div>

            <Tabs value={tab} onValueChange={(v) => setTab(v as any)}>
              <TabsList>
                <TabsTrigger value="all">All</TabsTrigger>
                <TabsTrigger value="pending">Pending</TabsTrigger>
                <TabsTrigger value="completed">Completed</TabsTrigger>
              </TabsList>
              <TabsContent value={tab} />
            </Tabs>
          </div>

          <div className="rounded-xl border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[110px]">ID</TableHead>
                  <TableHead>Title</TableHead>
                  <TableHead>Patient</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>

              <TableBody>
                {rows.map((r) => (
                  <TableRow key={r.id}>
                    <TableCell className="font-medium">{r.id}</TableCell>
                    <TableCell>{r.title}</TableCell>
                    <TableCell className="text-muted-foreground">{r.patient}</TableCell>
                    <TableCell>{r.type}</TableCell>
                    <TableCell>{rBadge(r.status)}</TableCell>
                    <TableCell className="text-right">
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button size="sm" variant="outline">
                            Menu
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem>Open</DropdownMenuItem>
                          <DropdownMenuItem>Assign reviewer</DropdownMenuItem>
                          <DropdownMenuItem>Mark completed</DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </TableCell>
                  </TableRow>
                ))}

                {rows.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={6} className="py-10 text-center text-muted-foreground">
                      No results.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
