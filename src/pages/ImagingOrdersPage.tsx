import { useMemo, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

import { createOrder, listOrders, type Modality } from "@/lib/imaging-store"

export default function ImagingOrdersPage() {
  const [patientId, setPatientId] = useState("P-10023")
  const [patientName, setPatientName] = useState("Demo Patient")
  const [modality, setModality] = useState<Modality | "">("")
  const [studyDescription, setStudyDescription] = useState("Chest imaging")
  const [priority, setPriority] = useState<"ROUTINE" | "URGENT">("ROUTINE")
  const [tick, setTick] = useState(0)

  const orders = useMemo(() => {
    void tick
    return listOrders()
  }, [tick])

  function submit() {
    if (!modality) return
    createOrder({
      patientId,
      patientName,
      modality,
      studyDescription,
      priority,
    })
    setTick((t) => t + 1)
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Imaging Orders</h1>
        <p className="text-sm text-muted-foreground">
          Create orders for MRI/CT/US/X-ray and physiologic tests (ECG/EEG). Demo store now — later DICOM/HL7.
        </p>
      </div>

      <Card className="rounded-2xl">
        <CardHeader>
          <CardTitle className="text-base">Create order</CardTitle>
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-6">
          <div className="space-y-2 md:col-span-2">
            <div className="text-xs text-muted-foreground">Patient Name</div>
            <Input value={patientName} onChange={(e) => setPatientName(e.target.value)} />
          </div>

          <div className="space-y-2">
            <div className="text-xs text-muted-foreground">Patient ID</div>
            <Input value={patientId} onChange={(e) => setPatientId(e.target.value)} />
          </div>

          <div className="space-y-2">
            <div className="text-xs text-muted-foreground">Modality</div>
            <Select onValueChange={(v) => setModality(v as Modality)}>
              <SelectTrigger>
                <SelectValue placeholder="Choose..." />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="XRAY">X-Ray</SelectItem>
                <SelectItem value="CT">CT</SelectItem>
                <SelectItem value="MRI">MRI</SelectItem>
                <SelectItem value="ULTRASOUND">Ultrasound</SelectItem>
                <SelectItem value="ECG">ECG</SelectItem>
                <SelectItem value="EEG">EEG</SelectItem>
                <SelectItem value="PET">PET</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2 md:col-span-2">
            <div className="text-xs text-muted-foreground">Study Description</div>
            <Input value={studyDescription} onChange={(e) => setStudyDescription(e.target.value)} />
          </div>

          <div className="space-y-2">
            <div className="text-xs text-muted-foreground">Priority</div>
            <Select onValueChange={(v) => setPriority(v as "ROUTINE" | "URGENT")} defaultValue="ROUTINE">
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ROUTINE">Routine</SelectItem>
                <SelectItem value="URGENT">Urgent</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="flex items-end">
            <Button className="w-full" onClick={submit} disabled={!modality}>
              Send Order
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card className="rounded-2xl">
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="text-base">Orders Queue</CardTitle>
          <Badge variant="secondary">{orders.length} orders</Badge>
        </CardHeader>
        <CardContent>
          <div className="rounded-xl border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Patient</TableHead>
                  <TableHead>Modality</TableHead>
                  <TableHead>Description</TableHead>
                  <TableHead>Priority</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Created</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {orders.map((o) => (
                  <TableRow key={o.id}>
                    <TableCell className="font-medium">
                      {o.patientName}
                      <div className="text-xs text-muted-foreground">{o.patientId}</div>
                    </TableCell>
                    <TableCell>{o.modality}</TableCell>
                    <TableCell className="text-sm">{o.studyDescription}</TableCell>
                    <TableCell>
                      <Badge variant={o.priority === "URGENT" ? "destructive" : "secondary"}>{o.priority}</Badge>
                    </TableCell>
                    <TableCell>{o.status}</TableCell>
                    <TableCell className="text-xs text-muted-foreground">
                      {new Date(o.createdAt).toLocaleString()}
                    </TableCell>
                  </TableRow>
                ))}
                {orders.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} className="text-sm text-muted-foreground">
                      No orders yet. Create one above.
                    </TableCell>
                  </TableRow>
                ) : null}
              </TableBody>
            </Table>
          </div>

          <div className="mt-3 text-xs text-muted-foreground">
            Next: we will push orders to real devices using DICOM MWL (imaging) and HL7 ORU (ECG/EEG results).
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
