import * as React from "react"
import AdminLayout from "@/layouts/AdminLayout"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"

type Item =
  | { type: "folder"; name: string; items: number; updated: string }
  | { type: "file"; name: string; size: string; tag?: string; updated: string }

const demo: Item[] = [
  { type: "folder", name: "Patients", items: 124, updated: "Today" },
  { type: "folder", name: "Reports", items: 38, updated: "Yesterday" },
  { type: "folder", name: "Radiology", items: 19, updated: "2d ago" },
  { type: "file", name: "Q1-operations-summary.pdf", size: "2.1 MB", tag: "PDF", updated: "Today" },
  { type: "file", name: "ER-triage-protocol.docx", size: "540 KB", tag: "DOCX", updated: "3d ago" },
  { type: "file", name: "inventory-export.csv", size: "88 KB", tag: "CSV", updated: "1w ago" },
]

export default function FileManager() {
  const [view, setView] = React.useState<"grid" | "list">("grid")

  return (
    <AdminLayout
      title="File Manager"
      subtitle="Folders, files, and clinical documents (demo UI)"
      actions={
        <div className="flex items-center gap-2">
          <Button size="sm" variant="outline" onClick={() => setView("list")}>
            List
          </Button>
          <Button size="sm" variant="outline" onClick={() => setView("grid")}>
            Grid
          </Button>
          <Button size="sm">Upload</Button>
        </div>
      }
    >
      {/* Toolbar */}
      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div className="w-full md:max-w-md">
          <Input placeholder="Search files and folders…" />
        </div>

        <div className="flex items-center gap-2">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline">Sort</Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem>Updated (newest)</DropdownMenuItem>
              <DropdownMenuItem>Name (A–Z)</DropdownMenuItem>
              <DropdownMenuItem>Type</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline">New</Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem>Folder</DropdownMenuItem>
              <DropdownMenuItem>Upload file</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>

      <Separator className="my-4" />

      {/* Content */}
      {view === "grid" ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {demo.map((it, idx) => (
            <Card key={idx} className="hover:shadow-sm transition-shadow">
              <CardHeader className="pb-2">
                <CardTitle className="text-base flex items-center justify-between gap-2">
                  <span className="truncate">
                    {it.type === "folder" ? "📁 " : "📄 "}
                    {it.name}
                  </span>
                  {"tag" in it && it.tag ? <Badge variant="secondary">{it.tag}</Badge> : null}
                </CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-muted-foreground">
                {it.type === "folder" ? (
                  <div className="flex items-center justify-between">
                    <span>{it.items} items</span>
                    <span>Updated {it.updated}</span>
                  </div>
                ) : (
                  <div className="flex items-center justify-between">
                    <span>{it.size}</span>
                    <span>Updated {it.updated}</span>
                  </div>
                )}

                <div className="mt-3 flex items-center justify-end gap-2">
                  <Button size="sm" variant="outline">Open</Button>
                  <Button size="sm" variant="outline">Share</Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="p-0">
            <div className="divide-y">
              {demo.map((it, idx) => (
                <div key={idx} className="flex items-center justify-between gap-3 p-4">
                  <div className="min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-base">
                        {it.type === "folder" ? "📁" : "📄"}
                      </span>
                      <div className="truncate font-medium">{it.name}</div>
                      {"tag" in it && it.tag ? <Badge variant="secondary">{it.tag}</Badge> : null}
                    </div>
                    <div className="text-xs text-muted-foreground mt-1">
                      {it.type === "folder"
                        ? `${it.items} items • Updated ${it.updated}`
                        : `${it.size} • Updated ${it.updated}`}
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <Button size="sm" variant="outline">Open</Button>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button size="sm" variant="outline">⋯</Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem>Rename</DropdownMenuItem>
                        <DropdownMenuItem>Move</DropdownMenuItem>
                        <DropdownMenuItem>Share</DropdownMenuItem>
                        <DropdownMenuItem className="text-destructive">Delete</DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </AdminLayout>
  )
}
