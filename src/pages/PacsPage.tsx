import { useMemo } from "react"
import { useSearchParams, Link } from "react-router-dom"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

import { getStudyById, listStudies, clearImagingDemo } from "@/lib/imaging-store"

export default function PacsPage() {
  const [params] = useSearchParams()
  const studyId = params.get("study")

  const studies = useMemo(() => listStudies(), [])
  const selected = studyId ? getStudyById(studyId) : undefined

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">PACS</h1>
          <p className="text-sm text-muted-foreground">
            Study list + viewer placeholder. Next step: OHIF + DICOMweb + real PACS integration.
          </p>
        </div>

        <div className="flex gap-2">
          <Button asChild variant="outline">
            <Link to="/imaging">Create Order</Link>
          </Button>
          <Button
            variant="outline"
            onClick={() => {
              clearImagingDemo()
              window.location.href = "/pacs"
            }}
          >
            Clear Demo Data
          </Button>
        </div>
      </div>

      {selected ? (
        <Card className="rounded-2xl">
          <CardHeader>
            <CardTitle className="text-base">Viewer (Demo)</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex flex-wrap gap-2">
              <Badge variant="secondary">{selected.modality}</Badge>
              <Badge variant="secondary">{selected.status}</Badge>
              <Badge variant="secondary">{selected.seriesCount} series</Badge>
              <Badge variant="secondary">{selected.instanceCount} instances</Badge>
            </div>

            <div className="rounded-xl border p-4">
              <div className="font-medium">{selected.description}</div>
              <div className="text-sm text-muted-foreground">
                Patient: {selected.patientName} ({selected.patientId})
              </div>
              <div className="text-sm text-muted-foreground">
                Study: {selected.studyId} • {new Date(selected.studyDate).toLocaleString()}
              </div>

              <div className="mt-4 text-sm">
                ✅ Demo viewer works. Next: embed OHIF viewer and load this study via DICOMweb endpoint.
              </div>
            </div>

            <Button asChild variant="outline">
              <Link to="/pacs">Back to list</Link>
            </Button>
          </CardContent>
        </Card>
      ) : null}

      <Card className="rounded-2xl">
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="text-base">Studies</CardTitle>
          <Badge variant="secondary">{studies.length} studies</Badge>
        </CardHeader>
        <CardContent>
    <div className="rounded-xl border overflow-hidden">
  {!studyId ? (
    <div className="p-6 space-y-3">
      <div className="text-sm text-muted-foreground">
        اختر دراسة من Imaging لعرضها داخل عارض الأشعة الذكي (OHIF)
      </div>

      <Button asChild>
        <Link to="/imaging">Go to Imaging Orders</Link>
      </Button>
    </div>
  ) : (
    <div className="space-y-4 p-4">
      <div className="flex items-center justify-between">
        <div className="text-sm">
          Study UID:
          <span className="font-mono ml-2">{studyId}</span>
        </div>

        <Button
          variant="outline"
          onClick={() =>
            window.open(
              `http://localhost:3001/viewer?StudyInstanceUIDs=${encodeURIComponent(
                studyId
              )}`,
              "_blank"
            )
          }
        >
          Open in Full OHIF Viewer
        </Button>
      </div>

      <div className="rounded-xl border overflow-hidden h-[75vh]">
        <iframe
          title="OHIF Viewer"
          className="w-full h-full"
          src={`http://localhost:3001/viewer?StudyInstanceUIDs=${encodeURIComponent(
            studyId
          )}`}
        />
      </div>
    </div>
  )}
</div>

          <div className="mt-3 text-xs text-muted-foreground">
            Real integration plan: DICOM MWL → modality acquires → DICOM C-STORE to PACS → DICOMweb to viewer.
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
