import { useMemo, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Textarea } from "@/components/ui/textarea"

import {
  findDrugById,
  getInteractionsForDrugIds,
  searchDrugs,
} from "@/lib/formulary"

import type { Drug } from "@/lib/formulary"

type RxLine = {
  drugId: string
  dose: string
  frequency: string
  duration: string
  notes?: string
}

type PatientContext = {
  age?: number
  allergies?: string[] // free text demo
  eGFR?: number
  pregnancy?: boolean
  diabetes?: boolean
}

function severityBadgeVariant(sev: "minor" | "moderate" | "major") {
  if (sev === "major") return "destructive" as const
  if (sev === "moderate") return "default" as const
  return "secondary" as const
}

export default function PrescriptionsPage() {
  // patient demo context
  const [patient, setPatient] = useState<PatientContext>({
    age: 54,
    allergies: ["penicillin"],
    eGFR: 42,
    diabetes: true,
    pregnancy: false,
  })

  // drug search
  const [q, setQ] = useState("")
  const results = useMemo(() => searchDrugs(q), [q])

  // rx lines
  const [rx, setRx] = useState<RxLine[]>([])
  const drugIds = useMemo(() => rx.map((r) => r.drugId), [rx])

  const interactionFindings = useMemo(() => getInteractionsForDrugIds(drugIds), [drugIds])

  // clinical flags (simple demo rules)
  const flags = useMemo(() => {
    const out: { severity: "minor" | "moderate" | "major"; title: string; detail: string }[] = []

    for (const line of rx) {
      const d = findDrugById(line.drugId)
      if (!d) continue

      // allergy demo
      if ((patient.allergies ?? []).some((a) => a.toLowerCase().includes("penicillin"))) {
        if ((d.tags ?? []).includes("beta-lactam")) {
          out.push({
            severity: "major",
            title: "Allergy risk",
            detail: `${d.name}: patient allergy includes "penicillin" (demo).`,
          })
        }
      }

      // renal demo
      if (typeof patient.eGFR === "number" && patient.eGFR < 45) {
        if (d.renalAdjust) {
          out.push({
            severity: "moderate",
            title: "Renal adjustment",
            detail: `${d.name}: ${d.renalAdjust} (patient eGFR ${patient.eGFR}).`,
          })
        }
      }

      // pregnancy demo
      if (patient.pregnancy) {
        if (d.pregnancy === "D" || d.pregnancy === "X") {
          out.push({
            severity: "major",
            title: "Pregnancy warning",
            detail: `${d.name}: pregnancy category ${d.pregnancy} (demo).`,
          })
        }
      }
    }

    // add interaction findings as flags too
    for (const itx of interactionFindings) {
      const a = findDrugById(itx.a)?.name ?? itx.a
      const b = findDrugById(itx.b)?.name ?? itx.b
      out.push({
        severity: itx.severity,
        title: `Interaction: ${a} + ${b}`,
        detail: `${itx.summary} — ${itx.recommendation}`,
      })
    }

    // de-dup by title+detail
    const keySet = new Set<string>()
    return out.filter((x) => {
      const k = `${x.title}|${x.detail}`
      if (keySet.has(k)) return false
      keySet.add(k)
      return true
    })
  }, [rx, patient, interactionFindings])

  function addDrug(d: Drug) {
    setRx((prev) => {
      if (prev.some((x) => x.drugId === d.id)) return prev
      return [
        ...prev,
        {
          drugId: d.id,
          dose: d.strength ?? "",
          frequency: "BID",
          duration: "5 days",
          notes: "",
        },
      ]
    })
  }

  function updateLine(idx: number, patch: Partial<RxLine>) {
    setRx((prev) => prev.map((x, i) => (i === idx ? { ...x, ...patch } : x)))
  }

  function removeLine(idx: number) {
    setRx((prev) => prev.filter((_, i) => i !== idx))
  }

  const exportJson = useMemo(() => {
    return JSON.stringify(
      {
        patient,
        prescription: rx.map((r) => ({
          ...r,
          drug: findDrugById(r.drugId),
        })),
        safety: {
          flags,
        },
        meta: {
          createdAt: new Date().toISOString(),
          version: "demo-1",
        },
      },
      null,
      2
    )
  }, [patient, rx, flags])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Smart Prescriptions</h1>
        <p className="text-sm text-muted-foreground">
          Create prescriptions linked to the hospital formulary, with safety checks (demo).
        </p>
      </div>

      {/* Patient context */}
      <Card className="rounded-2xl">
        <CardHeader>
          <CardTitle className="text-base">Patient context (demo)</CardTitle>
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-5">
          <div className="space-y-2">
            <div className="text-xs text-muted-foreground">Age</div>
            <Input
              value={patient.age ?? ""}
              onChange={(e) => setPatient((p) => ({ ...p, age: Number(e.target.value || 0) }))}
              placeholder="e.g. 54"
            />
          </div>

          <div className="space-y-2 md:col-span-2">
            <div className="text-xs text-muted-foreground">Allergies (comma separated)</div>
            <Input
              value={(patient.allergies ?? []).join(", ")}
              onChange={(e) =>
                setPatient((p) => ({
                  ...p,
                  allergies: e.target.value
                    .split(",")
                    .map((s) => s.trim())
                    .filter(Boolean),
                }))
              }
              placeholder="e.g. penicillin, latex"
            />
          </div>

          <div className="space-y-2">
            <div className="text-xs text-muted-foreground">eGFR</div>
            <Input
              value={patient.eGFR ?? ""}
              onChange={(e) => setPatient((p) => ({ ...p, eGFR: Number(e.target.value || 0) }))}
              placeholder="e.g. 42"
            />
          </div>

          <div className="space-y-2">
            <div className="text-xs text-muted-foreground">Diabetes (true/false)</div>
            <Input
              value={String(!!patient.diabetes)}
              onChange={(e) => setPatient((p) => ({ ...p, diabetes: e.target.value === "true" }))}
              placeholder="true"
            />
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Search + add */}
        <Card className="rounded-2xl">
          <CardHeader>
            <CardTitle className="text-base">Add from Formulary</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Search drugs (name / generic / strength / ATC)..."
            />

            <div className="rounded-xl border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Drug</TableHead>
                    <TableHead>Route</TableHead>
                    <TableHead className="w-[120px]"></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {results.slice(0, 10).map((d) => (
                    <TableRow key={d.id}>
                      <TableCell className="font-medium">
                        {d.name}
                        <div className="text-xs text-muted-foreground">
                          {(d.strength ?? "").trim()} {(d.form ?? "").trim()}
                        </div>
                      </TableCell>
                      <TableCell className="text-xs">{d.route}</TableCell>
                      <TableCell className="text-right">
                        <Button size="sm" onClick={() => addDrug(d)}>
                          Add
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                  {results.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={3} className="text-sm text-muted-foreground">
                        No matches.
                      </TableCell>
                    </TableRow>
                  ) : null}
                </TableBody>
              </Table>
            </div>

            <div className="text-xs text-muted-foreground">
              Tip: Later we connect to national drug database + hospital rules + insurance formulary.
            </div>
          </CardContent>
        </Card>

        {/* Safety panel */}
        <Card className="rounded-2xl">
          <CardHeader>
            <CardTitle className="text-base">Safety checks</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex items-center gap-2">
              <Badge variant={flags.some((f) => f.severity === "major") ? "destructive" : "secondary"}>
                {flags.length} findings
              </Badge>
              <span className="text-xs text-muted-foreground">
                Demo rules: allergy / renal / pregnancy + drug–drug interactions
              </span>
            </div>

            <div className="space-y-2">
              {flags.length === 0 ? (
                <div className="text-sm text-muted-foreground">No warnings detected (demo).</div>
              ) : (
                flags.map((f, idx) => (
                  <div key={idx} className="rounded-xl border p-3">
                    <div className="flex items-center justify-between gap-3">
                      <div className="font-medium">{f.title}</div>
                      <Badge variant={severityBadgeVariant(f.severity)}>{f.severity}</Badge>
                    </div>
                    <div className="mt-1 text-sm text-muted-foreground">{f.detail}</div>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Prescription builder */}
      <Card className="rounded-2xl">
        <CardHeader>
          <CardTitle className="text-base">Prescription</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="rounded-xl border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Drug</TableHead>
                  <TableHead>Dose</TableHead>
                  <TableHead>Frequency</TableHead>
                  <TableHead>Duration</TableHead>
                  <TableHead>Notes</TableHead>
                  <TableHead className="w-[80px]"></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {rx.map((line, idx) => {
                  const d = findDrugById(line.drugId)
                  return (
                    <TableRow key={line.drugId}>
                      <TableCell className="font-medium">
                        {d?.name ?? line.drugId}
                        <div className="text-xs text-muted-foreground">
                          {d?.strength ?? ""} {d?.form ?? ""} • {d?.route ?? ""}
                        </div>
                      </TableCell>
                      <TableCell>
                        <Input value={line.dose} onChange={(e) => updateLine(idx, { dose: e.target.value })} />
                      </TableCell>
                      <TableCell>
                        <Input value={line.frequency} onChange={(e) => updateLine(idx, { frequency: e.target.value })} />
                      </TableCell>
                      <TableCell>
                        <Input value={line.duration} onChange={(e) => updateLine(idx, { duration: e.target.value })} />
                      </TableCell>
                      <TableCell>
                        <Input value={line.notes ?? ""} onChange={(e) => updateLine(idx, { notes: e.target.value })} />
                      </TableCell>
                      <TableCell className="text-right">
                        <Button variant="outline" size="sm" onClick={() => removeLine(idx)}>
                          Remove
                        </Button>
                      </TableCell>
                    </TableRow>
                  )
                })}
                {rx.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} className="text-sm text-muted-foreground">
                      No medications added yet.
                    </TableCell>
                  </TableRow>
                ) : null}
              </TableBody>
            </Table>
          </div>

          <div className="grid gap-3 lg:grid-cols-2">
            <div>
              <div className="text-sm font-medium mb-2">Export (JSON)</div>
              <Textarea value={exportJson} readOnly className="min-h-[220px] font-mono text-xs" />
            </div>

            <div className="space-y-3">
              <div className="text-sm font-medium">Actions</div>
              <div className="flex flex-wrap gap-2">
                <Button
                  variant="default"
                  onClick={() => {
                    navigator.clipboard.writeText(exportJson)
                  }}
                >
                  Copy JSON
                </Button>

                <Button
                  variant="outline"
                  onClick={() => {
                    setRx([])
                  }}
                >
                  Clear prescription
                </Button>
              </div>

              <div className="rounded-xl border p-3 text-sm text-muted-foreground">
                <div className="font-medium text-foreground">Next upgrade (we will do it):</div>
                <ul className="list-disc pl-5 mt-2 space-y-1">
                  <li>ICD/diagnosis → suggested meds + guidelines</li>
                  <li>Dose calculator (weight, age, eGFR, hepatic)</li>
                  <li>Real drug DB + national formulary + insurance rules</li>
                  <li>PDF print with signature + QR + audit trail</li>
                </ul>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
