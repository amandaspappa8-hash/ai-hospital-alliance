import { useMemo, useState } from "react"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"

type ApptStatus = "upcoming" | "completed" | "cancelled"

type Appt = {
  id: string
  patient: string
  doctor: string
  department: string
  date: string // YYYY-MM-DD
  time: string // HH:mm
  status: ApptStatus
}

const APPTS: Appt[] = [
  { id: "A-9001", patient: "Sarah Jones", doctor: "Dr. Priscilla", department: "Cardiology", date: "2026-02-15", time: "10:30", status: "upcoming" },
  { id: "A-9002", patient: "John Smith", doctor: "Dr. Cooper", department: "Neurology", date: "2026-02-15", time: "12:00", status: "upcoming" },
  { id: "A-8990", patient: "Emily Brown", doctor: "Dr. Lane", department: "Orthopedics", date: "2026-02-12", time: "09:00", status: "completed" },
  { id: "A-8988", patient: "Patient B", doctor: "Dr. Kumar", department: "ER", date: "2026-02-11", time: "15:15", status: "cancelled" },
]

function apptBadge(s: ApptStatus) {
  if (s === "upcoming") return <Badge>Upcoming</Badge>
  if (s === "completed") return <Badge variant="secondary">Completed</Badge>
  return <Badge variant="outline">Cancelled</Badge>
}

export default function AppointmentsPage() {
  const [tab, setTab] = useState<"list" | "calendar">("list")
  const [q, setQ] = useState("")
  const [status, setStatus] = useState<ApptStatus | "all">("all")

  const [date, setDate] = useState<Date | undefined>(new Date())

  const rows = useMemo(() => {
    const query = q.trim().toLowerCase()
    return APPTS.filter((a) => {
      const matchesQuery =
        !query ||
        a.patient.toLowerCase().includes(query) ||
        a.doctor.toLowerCase().includes(query) ||
        a.id.toLowerCase().includes(query)

      const matchesStatus = status === "all" ? true : a.status === status

      return matchesQuery && matchesStatus
    })
  }, [q, status])

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">Appointments</h1>
          <p className="text-sm text-muted-foreground">List + Calendar view, with create dialog.</p>
        </div>

        <Dialog>
          <DialogTrigger asChild>
            <Button>+ New appointment</Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-lg">
            <DialogHeader>
              <DialogTitle>Create appointment</DialogTitle>
            </DialogHeader>

            <div className="grid gap-3">
              <Input placeholder="Patient name" />
              <Input placeholder="Doctor name" />
              <div className="grid grid-cols-2 gap-2">
                <Input placeholder="Date (YYYY-MM-DD)" />
                <Input placeholder="Time (HH:mm)" />
              </div>

              <Select defaultValue="upcoming">
                <SelectTrigger>
                  <SelectValue placeholder="Status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="upcoming">Upcoming</SelectItem>
                  <SelectItem value="completed">Completed</SelectItem>
                  <SelectItem value="cancelled">Cancelled</SelectItem>
                </SelectContent>
              </Select>

              <div className="flex gap-2 pt-2">
                <Button className="flex-1">Save</Button>
                <Button variant="outline" className="flex-1">
                  Cancel
                </Button>
              </div>

              <p className="text-xs text-muted-foreground">
                Demo UI only — next step: connect API + validation + RBAC.
              </p>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      <Tabs value={tab} onValueChange={(v) => setTab(v as any)}>
        <TabsList>
          <TabsTrigger value="list">List</TabsTrigger>
          <TabsTrigger value="calendar">Calendar</TabsTrigger>
        </TabsList>

        <TabsContent value="list" className="mt-4">
          <Card className="rounded-2xl">
            <CardHeader className="pb-3">
              <CardTitle className="text-base">Appointments</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex flex-col gap-3 md:flex-row md:items-center">
                <div className="flex-1">
                  <Input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search by patient, doctor, ID..." />
                </div>
                <Select value={status} onValueChange={(v) => setStatus(v as any)}>
                  <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="Status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All statuses</SelectItem>
                    <SelectItem value="upcoming">Upcoming</SelectItem>
                    <SelectItem value="completed">Completed</SelectItem>
                    <SelectItem value="cancelled">Cancelled</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="rounded-xl border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="w-[110px]">ID</TableHead>
                      <TableHead>Patient</TableHead>
                      <TableHead>Doctor</TableHead>
                      <TableHead>Date</TableHead>
                      <TableHead>Time</TableHead>
                      <TableHead>Status</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {rows.map((a) => (
                      <TableRow key={a.id}>
                        <TableCell className="font-medium">{a.id}</TableCell>
                        <TableCell>{a.patient}</TableCell>
                        <TableCell className="text-muted-foreground">{a.doctor}</TableCell>
                        <TableCell>{a.date}</TableCell>
                        <TableCell>{a.time}</TableCell>
                        <TableCell>{apptBadge(a.status)}</TableCell>
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
        </TabsContent>

        <TabsContent value="calendar" className="mt-4">
          <div className="grid gap-4 lg:grid-cols-3">
            <Card className="rounded-2xl lg:col-span-1">
              <CardHeader className="pb-3">
                <CardTitle className="text-base">Pick a date</CardTitle>
              </CardHeader>
              <CardContent>
                <Calendar mode="single" selected={date} onSelect={setDate} />
              </CardContent>
            </Card>

            <Card className="rounded-2xl lg:col-span-2">
              <CardHeader className="pb-3">
                <CardTitle className="text-base">Day schedule</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-muted-foreground">
                Demo: connect selected date to real schedule list + time slots.
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
