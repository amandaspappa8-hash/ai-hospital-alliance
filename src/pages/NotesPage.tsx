import { useEffect, useState } from "react"
import { apiGet, apiPost } from "@/lib/api"

export default function NotesPage() {
  const [patientId, setPatientId] = useState("P-1001")
  const [notes, setNotes] = useState<any[]>([])
  const [text, setText] = useState("")

  useEffect(() => {
    if (!patientId) return

    apiGet(`/notes/${patientId}`)
      .then((data: any) => setNotes(Array.isArray(data) ? data : []))
      .catch(() => setNotes([]))
  }, [patientId])

  async function add() {
    if (!text.trim()) return

    await apiPost(`/notes/${patientId}`, { text })
    const data = await apiGet(`/notes/${patientId}`)
    setNotes(Array.isArray(data) ? data : [])
    setText("")
  }

  return (
    <div style={{ padding: 24, color: "white" }}>
      <h1 style={{ fontSize: 32, fontWeight: 700, marginBottom: 8 }}>Clinical Notes</h1>
      <p style={{ opacity: 0.7, marginBottom: 20 }}>Create and view notes for the selected patient.</p>

      <div style={{ background: "#111827", border: "1px solid #374151", borderRadius: 12, padding: 20, maxWidth: 700 }}>
        <div style={{ marginBottom: 12 }}>
          <div style={{ marginBottom: 6 }}>Patient ID</div>
          <input
            value={patientId}
            onChange={(e) => setPatientId(e.target.value)}
            style={inputStyle}
          />
        </div>

        <div style={{ marginBottom: 12 }}>
          <div style={{ marginBottom: 6 }}>New Note</div>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Write clinical note..."
            style={textareaStyle}
          />
        </div>

        <button onClick={add} style={buttonStyle}>
          Add Note
        </button>
      </div>

      <div style={{ marginTop: 20, background: "#111827", border: "1px solid #374151", borderRadius: 12, padding: 20, maxWidth: 700 }}>
        <h2 style={{ fontSize: 24, fontWeight: 700, marginBottom: 12 }}>Patient Notes</h2>

        {notes.length === 0 ? (
          <div style={{ opacity: 0.7 }}>No notes for this patient.</div>
        ) : (
          <div style={{ display: "grid", gap: 10 }}>
            {notes.map((note: any) => (
              <div
                key={note.id}
                style={{
                  background: "#0b1220",
                  border: "1px solid #374151",
                  borderRadius: 10,
                  padding: 12,
                }}
              >
                {note.text}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

const inputStyle: React.CSSProperties = {
  width: "100%",
  padding: "10px 12px",
  borderRadius: 10,
  border: "1px solid #374151",
  background: "#030712",
  color: "white",
}

const textareaStyle: React.CSSProperties = {
  width: "100%",
  minHeight: 120,
  padding: "12px",
  borderRadius: 10,
  border: "1px solid #374151",
  background: "#030712",
  color: "white",
}

const buttonStyle: React.CSSProperties = {
  padding: "12px 18px",
  borderRadius: 10,
  border: "1px solid #22c55e",
  background: "#166534",
  color: "white",
  cursor: "pointer",
  fontWeight: 600,
}
