import { useMemo, useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet"
import { Separator } from "@/components/ui/separator"

type PatientStatus = "in_care" | "waiting" | "discharged"
type Department = "Cardiology" | "Neurology" | "Orthopedics" | "ER" | "Radiology" | "Lab"

type Patient = {
  id: string
  name: string
  department: Department
  status: PatientStatus
  age: number
  phone: string
  lastVisit: string
}

const PATIENTS: Patient[] = [
  { id: "P-10291", name: "Sarah Jones", department: "Cardiology", status: "in_care", age: 52, phone: "+218 91 000 0001", lastVisit: "2026-02-14" },
  { id: "P-10274", name: "John Smith", department: "Neurology", status: "waiting", age: 61, phone: "+218 92 000 0002", lastVisit: "2026-02-13" },
  { id: "P-10260", name: "Emily Brown", department: "Orthopedics", status: "discharged", age: 37, phone: "+218 93 000 0003", lastVisit: "2026-02-10" },
  { id: "P-10241", name: "Patient A", department: "Radiology", status: "in_care", age: 45, phone: "+218 94 000 0004", lastVisit: "2026-02-15" },
  { id: "P-10211", name: "Patient B", department: "ER", status: "waiting", age: 29, phone: "+218 95 000 0005", lastVisit: "2026-02-15" },
  { id: "P-10198", name: "Patient C", department: "Lab", status: "in_care", age: 70, phone: "+218 96 000 0006", lastVisit: "2026-02-12" },
]

function statusBadge(status: PatientStatus) {
  switch (status) {
    case "in_care":
      return <Badge>In care</Badge>
    case "waiting":
      return <Badge variant="secondary">Waiting</Badge>
    case "discharged":
      return <Badge variant="outline">Discharged</Badge>
  }
}

export default function PatientsPage() {
  const [q, setQ] = useState("")
  const [dept, setDept] = useState<Department | "all">("all")
  const [status, setStatus] = useState<PatientStatus | "all">("all")

  const [open, setOpen] = useState(false)
  const [selected, setSelected] = useState<Patient | null>(null)

  const rows = useMemo(() => {
    const query = q.trim().toLowerCase()
    return PATIENTS.filter((p) => {
      const matchesQuery =
        !query ||
        p.name.toLowerCase().includes(query) ||
        p.id.toLowerCase().includes(query) ||
        p.phone.toLowerCase().includes(query)

      const matchesDept = dept === "all" ? true : p.department === dept
      const matchesStatus = status === "all" ? true : p.status === status

      return matchesQuery && matchesDept && matchesStatus
    })
  }, [q, dept, status])

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">Patients</h1>
          <p className="text-sm text-muted-foreground">Search, filter, and open patient details.</p>
        </div>
        <Button
          onClick={() => {
            setSelected({
              id: "NEW",
              name: "New Patient",
              department: "ER",
              status: "waiting",
              age: 0,
              phone: "",
              lastVisit: new Date().toISOString().slice(0, 10),
            })
            setOpen(true)
          }}
        >
          + New Patient
        </Button>
      </div>

      <Card className="rounded-2xl">
        <CardHeader className="pb-3">
          <CardTitle className="text-base">Patients list</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Filters */}
          <div className="flex flex-col gap-3 md:flex-row md:items-center">
            <div className="flex-1">
              <Input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search by name, ID, phone..." />
            </div>

            <div className="flex gap-2">
              <Select value={dept} onValueChange={(v) => setDept(v as any)}>
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Department" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All departments</SelectItem>
                  <SelectItem value="Cardiology">Cardiology</SelectItem>
                  <SelectItem value="Neurology">Neurology</SelectItem>
                  <SelectItem value="Orthopedics">Orthopedics</SelectItem>
                  <SelectItem value="ER">ER</SelectItem>
                  <SelectItem value="Radiology">Radiology</SelectItem>
                  <SelectItem value="Lab">Lab</SelectItem>
                </SelectContent>
              </Select>

              <Select value={status} onValueChange={(v) => setStatus(v as any)}>
                <SelectTrigger className="w-[160px]">
                  <SelectValue placeholder="Status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All statuses</SelectItem>
                  <SelectItem value="in_care">In care</SelectItem>
                  <SelectItem value="waiting">Waiting</SelectItem>
                  <SelectItem value="discharged">Discharged</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <Separator />

          {/* Table */}
          <div className="rounded-xl border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[120px]">ID</TableHead>
                  <TableHead>Name</TableHead>
                  <TableHead>Department</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead className="text-right">Action</TableHead>
                </TableRow>
              </TableHeader>

              <TableBody>
                {rows.map((p) => (
                  <TableRow key={p.id}>
                    <TableCell className="font-medium">{p.id}</TableCell>
                    <TableCell>{p.name}</TableCell>
                    <TableCell className="text-muted-foreground">{p.department}</TableCell>
                    <TableCell>{statusBadge(p.status)}</TableCell>
                    <TableCell className="text-right">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          setSelected(p)
                          setOpen(true)
                        }}
                      >
                        Open
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}

                {rows.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={5} className="py-10 text-center text-muted-foreground">
                      No results.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      {/* Details Sheet */}
      <Sheet open={open} onOpenChange={setOpen}>
        <SheetContent className="w-full sm:max-w-lg">
          <SheetHeader>
            <SheetTitle>Patient details</SheetTitle>
          </SheetHeader>

          <div className="mt-6 space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1">
                <div className="text-xs text-muted-foreground">ID</div>
                <div className="font-medium">{selected?.id ?? "-"}</div>
              </div>
              <div className="space-y-1">
                <div className="text-xs text-muted-foreground">Status</div>
                <div>{selected ? statusBadge(selected.status) : "-"}</div>
              </div>
              <div className="space-y-1">
                <div className="text-xs text-muted-foreground">Name</div>
                <div className="font-medium">{selected?.name ?? "-"}</div>
              </div>
              <div className="space-y-1">
                <div className="text-xs text-muted-foreground">Department</div>
                <div className="font-medium">{selected?.department ?? "-"}</div>
              </div>
              <div className="space-y-1">
                <div className="text-xs text-muted-foreground">Age</div>
                <div className="font-medium">{selected?.age ?? "-"}</div>
              </div>
              <div className="space-y-1">
                <div className="text-xs text-muted-foreground">Phone</div>
                <div className="font-medium">{selected?.phone ?? "-"}</div>
              </div>
            </div>

            <Separator />

            <div className="space-y-2">
              <div className="text-sm font-semibold">Notes</div>
              <p className="text-sm text-muted-foreground">
                This is a UI template. Next: connect real patient profile + visits + documents.
              </p>
            </div>

            <div className="flex gap-2 pt-2">
              <Button className="flex-1">Save</Button>
              <Button variant="outline" className="flex-1" onClick={() => setOpen(false)}>
                Close
              </Button>
            </div>
          </div>
        </SheetContent>
      </Sheet>
    </div>
  )
}
