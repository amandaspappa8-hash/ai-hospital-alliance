import { useMemo, useState } from "react"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { formulary, searchDrugs } from "@/lib/formulary"

export default function DrugFormularyPage() {
  const [q, setQ] = useState("")
  const rows = useMemo(() => searchDrugs(q), [q])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Drug Formulary</h1>
        <p className="text-sm text-muted-foreground">Hospital-approved medications list (demo data).</p>
      </div>

      <Card className="rounded-2xl">
        <CardHeader>
          <CardTitle className="text-base">Search</CardTitle>
        </CardHeader>
        <CardContent className="flex gap-3">
          <Input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search by name / generic / strength / ATC..." />
          <Badge variant="secondary">{rows.length} drugs</Badge>
        </CardContent>
      </Card>

      <Card className="rounded-2xl">
        <CardHeader>
          <CardTitle className="text-base">Formulary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="rounded-xl border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Strength</TableHead>
                  <TableHead>Form</TableHead>
                  <TableHead>Route</TableHead>
                  <TableHead>ATC</TableHead>
                  <TableHead>Tags</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {rows.map((d) => (
                  <TableRow key={d.id}>
                    <TableCell className="font-medium">
                      {d.name}
                      {d.genericName && d.genericName !== d.name ? (
                        <div className="text-xs text-muted-foreground">{d.genericName}</div>
                      ) : null}
                    </TableCell>
                    <TableCell>{d.strength ?? "-"}</TableCell>
                    <TableCell>{d.form ?? "-"}</TableCell>
                    <TableCell>{d.route}</TableCell>
                    <TableCell className="text-xs">{d.atc ?? "-"}</TableCell>
                    <TableCell className="space-x-1">
                      {(d.tags ?? []).slice(0, 3).map((t) => (
                        <Badge key={t} variant="secondary">{t}</Badge>
                      ))}
                    </TableCell>
                  </TableRow>
                ))}
                {rows.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} className="text-sm text-muted-foreground">
                      No matches.
                    </TableCell>
                  </TableRow>
                ) : null}
              </TableBody>
            </Table>
          </div>

          <div className="mt-3 text-xs text-muted-foreground">
            Demo formulary ({formulary.length} items). Later we connect to real drug database / national formulary.
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
