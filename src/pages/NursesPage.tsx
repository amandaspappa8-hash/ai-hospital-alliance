import { useEffect, useMemo, useState } from "react"
import { useNavigate, useSearchParams } from "react-router-dom"
import { apiDelete, apiGet, apiPost, apiPut } from "@/lib/api"

type Patient = {
  id: string
  name: string
  age?: number
  gender?: string
  department?: string
  status?: string
  condition?: string
}

type NursingVital = {
  id: number
  temperature: string
  bloodPressure: string
  heartRate: string
  respiratoryRate: string
  oxygenSaturation: string
  time: string
}

type NursingNote = {
  id: number
  text: string
}

type MARItem = {
  id: number
  medication: string
  dose: string
  route: string
  schedule: string
  status: string
  givenAt?: string
  createdAt?: string
}

export default function NursesPage() {
  const navigate = useNavigate()
  const [searchParams, setSearchParams] = useSearchParams()
  const patientIdFromUrl = searchParams.get("patientId") ?? ""

  const [patients, setPatients] = useState<Patient[]>([])
  const [selectedPatientId, setSelectedPatientId] = useState(patientIdFromUrl)
  const [vitals, setVitals] = useState<NursingVital[]>([])
  const [notes, setNotes] = useState<NursingNote[]>([])
  const [mar, setMar] = useState<MARItem[]>([])
  const [error, setError] = useState("")
  const [successMessage, setSuccessMessage] = useState("")
  const [marFilter, setMarFilter] = useState<"all" | "Pending" | "Given">("all")
  const [marSearch, setMarSearch] = useState("")
  const [editingMarId, setEditingMarId] = useState<number | null>(null)

  const [vitalForm, setVitalForm] = useState({
    temperature: "",
    bloodPressure: "",
    heartRate: "",
    respiratoryRate: "",
    oxygenSaturation: "",
    time: "",
  })

  const [noteForm, setNoteForm] = useState({
    text: "",
  })

  const [marForm, setMarForm] = useState({
    medication: "",
    dose: "",
    route: "",
    schedule: "",
    status: "Pending",
    givenAt: "",
  })

  useEffect(() => {
    if (!successMessage) return
    const t = setTimeout(() => setSuccessMessage(""), 2500)
    return () => clearTimeout(t)
  }, [successMessage])

  useEffect(() => {
    apiGet("/patients")
      .then((data) => {
        const list = Array.isArray(data) ? data : []
        setPatients(list)
        if (patientIdFromUrl) {
          setSelectedPatientId(patientIdFromUrl)
        } else if (list.length > 0) {
          setSelectedPatientId(list[0].id)
          setSearchParams({ patientId: list[0].id })
        }
      })
      .catch(() => setError("Failed to load patients"))
  }, [])

  useEffect(() => {
    if (!selectedPatientId) return

    setSearchParams({ patientId: selectedPatientId })

    Promise.all([
      apiGet(`/nursing/vitals/${selectedPatientId}`),
      apiGet(`/nursing/notes/${selectedPatientId}`),
      apiGet(`/mar/${selectedPatientId}`),
    ])
      .then(([v, n, m]) => {
        setVitals(Array.isArray(v) ? v : [])
        setNotes(Array.isArray(n) ? n : [])
        setMar(Array.isArray(m) ? m : [])
      })
      .catch(() => setError("Failed to load nursing data"))
  }, [selectedPatientId])

  const selectedPatient = useMemo(
    () => patients.find((p) => p.id === selectedPatientId),
    [patients, selectedPatientId]
  )

  const filteredMar = useMemo(() => {
    let items = [...mar]

    items.sort((a, b) => {
      const rank = (status: string) => {
        if (status === "Pending") return 0
        if (status === "Given") return 1
        return 2
      }
      return rank(a.status) - rank(b.status)
    })

    if (marFilter !== "all") {
      items = items.filter((item) => item.status === marFilter)
    }

    const q = marSearch.trim().toLowerCase()
    if (q) {
      items = items.filter((item) => item.medication.toLowerCase().includes(q))
    }

    return items
  }, [mar, marFilter, marSearch])

  const totalMarCount = mar.length
  const pendingMarCount = mar.filter((item) => item.status === "Pending").length
  const givenMarCount = mar.filter((item) => item.status === "Given").length

  const resetMarForm = () => {
    setMarForm({
      medication: "",
      dose: "",
      route: "",
      schedule: "",
      status: "Pending",
      givenAt: "",
    })
    setEditingMarId(null)
  }

  const submitVital = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await apiPost(`/nursing/vitals/${selectedPatientId}`, vitalForm)
      const refreshed = await apiGet(`/nursing/vitals/${selectedPatientId}`)
      setVitals(Array.isArray(refreshed) ? refreshed : [])
      setVitalForm({
        temperature: "",
        bloodPressure: "",
        heartRate: "",
        respiratoryRate: "",
        oxygenSaturation: "",
        time: "",
      })
      setSuccessMessage("Vital signs saved")
    } catch {
      setError("Failed to save vital signs")
    }
  }

  const submitNote = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await apiPost(`/nursing/notes/${selectedPatientId}`, noteForm)
      const refreshed = await apiGet(`/nursing/notes/${selectedPatientId}`)
      setNotes(Array.isArray(refreshed) ? refreshed : [])
      setNoteForm({ text: "" })
      setSuccessMessage("Note saved")
    } catch {
      setError("Failed to save nursing note")
    }
  }

  const submitMAR = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      if (editingMarId !== null) {
        await apiPut(`/mar/${selectedPatientId}/${editingMarId}`, marForm)
      } else {
        await apiPost(`/mar/${selectedPatientId}`, marForm)
      }

      const refreshed = await apiGet(`/mar/${selectedPatientId}`)
      setMar(Array.isArray(refreshed) ? refreshed : [])
      resetMarForm()
      setSuccessMessage(editingMarId !== null ? "MAR updated" : "MAR added")
    } catch {
      setError("Failed to save MAR item")
    }
  }

  const markAsGiven = async (itemId: number) => {
    try {
      const now = new Date()
      const hh = String(now.getHours()).padStart(2, "0")
      const mm = String(now.getMinutes()).padStart(2, "0")

      await apiPut(`/mar/${selectedPatientId}/${itemId}/status`, {
        status: "Given",
        givenAt: `${hh}:${mm}`,
      })

      const refreshed = await apiGet(`/mar/${selectedPatientId}`)
      setMar(Array.isArray(refreshed) ? refreshed : [])
      setSuccessMessage("Medication marked as given")
    } catch {
      setError("Failed to update MAR status")
    }
  }

  const markAllPendingAsGiven = async () => {
    try {
      const pending = mar.filter((item) => item.status === "Pending")
      if (pending.length === 0) return

      const now = new Date()
      const hh = String(now.getHours()).padStart(2, "0")
      const mm = String(now.getMinutes()).padStart(2, "0")
      const givenAt = `${hh}:${mm}`

      await Promise.all(
        pending.map((item) =>
          apiPut(`/mar/${selectedPatientId}/${item.id}/status`, {
            status: "Given",
            givenAt,
          })
        )
      )

      const refreshed = await apiGet(`/mar/${selectedPatientId}`)
      setMar(Array.isArray(refreshed) ? refreshed : [])
      setMarFilter("Given")
      setSuccessMessage("All pending meds marked as given")
    } catch {
      setError("Failed to update MAR")
    }
  }

  const startEditMarItem = (item: MARItem) => {
    setEditingMarId(item.id)
    setMarForm({
      medication: item.medication,
      dose: item.dose,
      route: item.route,
      schedule: item.schedule,
      status: item.status,
      givenAt: item.givenAt || "",
    })
  }

  const deleteMarItem = async (itemId: number) => {
    const ok = window.confirm("Delete this MAR item?")
    if (!ok) return

    try {
      await apiDelete(`/mar/${selectedPatientId}/${itemId}`)
      const refreshed = await apiGet(`/mar/${selectedPatientId}`)
      setMar(Array.isArray(refreshed) ? refreshed : [])
      setSuccessMessage("MAR item deleted")
    } catch {
      setError("Failed to delete MAR item")
    }
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(180deg, #0f172a 0%, #111827 100%)",
        color: "#f8fafc",
        padding: 24,
      }}
    >
      <div style={{ display: "grid", gap: 20 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 12 }}>
          <div>
            <h1 style={{ margin: 0, fontSize: 42, fontWeight: 800 }}>Nursing Station • NEW UI</h1>
            <div style={{ marginTop: 8, color: "#cbd5e1" }}>
              SMART NURSING WORKFLOW • GLASS VERSION ACTIVE
            </div>
          </div>

          {selectedPatientId && (
            <button
              onClick={() => navigate(`/patient-profile?id=${selectedPatientId}`)}
              style={{
                border: "1px solid rgba(148,163,184,0.35)",
                borderRadius: 14,
                padding: "12px 16px",
                background: "rgba(255,255,255,0.08)",
                color: "#e5e7eb",
                fontWeight: 700,
                cursor: "pointer",
              }}
            >
              Open Patient Profile
            </button>
          )}
        </div>

        {error && (
          <div
            style={{
              background: "linear-gradient(180deg, rgba(127,29,29,0.5), rgba(69,10,10,0.55))",
              border: "1px solid rgba(248,113,113,0.45)",
              color: "#fecaca",
              borderRadius: 20,
              padding: 16,
            }}
          >
            {error}
          </div>
        )}

        {successMessage && (
          <div
            style={{
              background: "linear-gradient(180deg, rgba(20,83,45,0.5), rgba(5,46,22,0.55))",
              border: "1px solid rgba(74,222,128,0.45)",
              color: "#bbf7d0",
              borderRadius: 20,
              padding: 16,
            }}
          >
            {successMessage}
          </div>
        )}

        <div style={{ display: "grid", gridTemplateColumns: "1.1fr 2fr", gap: 20 }}>
          <div
            style={{
              background: "linear-gradient(180deg, rgba(30,41,59,0.92), rgba(15,23,42,0.92))",
              border: "1px solid rgba(96,165,250,0.28)",
              borderRadius: 24,
              padding: 22,
              boxShadow: "0 10px 30px rgba(0,0,0,0.25)",
            }}
          >
            <h2 style={{ marginTop: 0, marginBottom: 16, fontSize: 28 }}>Patients</h2>
            <div style={{ display: "grid", gap: 14 }}>
              {patients.map((patient) => (
                <button
                  key={patient.id}
                  onClick={() => setSelectedPatientId(patient.id)}
                  style={{
                    textAlign: "left",
                    padding: 16,
                    borderRadius: 18,
                    border:
                      selectedPatientId === patient.id
                        ? "1px solid rgba(56,189,248,0.95)"
                        : "1px solid rgba(148,163,184,0.22)",
                    background:
                      selectedPatientId === patient.id
                        ? "linear-gradient(135deg, rgba(37,99,235,0.34), rgba(14,165,233,0.18))"
                        : "linear-gradient(180deg, rgba(15,23,42,0.55), rgba(30,41,59,0.55))",
                    boxShadow:
                      selectedPatientId === patient.id
                        ? "0 0 0 1px rgba(59,130,246,0.18), 0 10px 24px rgba(2,132,199,0.18)"
                        : "0 8px 18px rgba(15,23,42,0.16)",
                    color: "#f8fafc",
                    cursor: "pointer",
                  }}
                >
                  <div style={{ fontSize: 18, fontWeight: 800 }}>{patient.name}</div>
                  <div style={{ marginTop: 6, color: "#cbd5e1" }}>{patient.id}</div>
                  <div style={{ marginTop: 6, color: "#e2e8f0" }}>
                    {patient.department ?? "General"} • {patient.condition ?? "-"}
                  </div>
                </button>
              ))}
            </div>
          </div>

          <div style={{ display: "grid", gap: 20 }}>
            <div
              style={{
                background: "linear-gradient(180deg, rgba(30,41,59,0.92), rgba(15,23,42,0.92))",
                border: "1px solid rgba(96,165,250,0.28)",
                borderRadius: 24,
                padding: 22,
                boxShadow: "0 10px 30px rgba(0,0,0,0.25)",
              }}
            >
              <h2 style={{ marginTop: 0, marginBottom: 16, fontSize: 28 }}>Selected Patient</h2>
              {selectedPatient ? (
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
                  <div><strong>Name:</strong> {selectedPatient.name}</div>
                  <div><strong>ID:</strong> {selectedPatient.id}</div>
                  <div><strong>Age:</strong> {selectedPatient.age ?? "-"}</div>
                  <div><strong>Gender:</strong> {selectedPatient.gender ?? "-"}</div>
                  <div><strong>Department:</strong> {selectedPatient.department ?? "-"}</div>
                  <div><strong>Status:</strong> {selectedPatient.status ?? "-"}</div>
                  <div style={{ gridColumn: "1 / -1" }}><strong>Condition:</strong> {selectedPatient.condition ?? "-"}</div>
                </div>
              ) : (
                <div>No patient selected</div>
              )}
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
              <form
                onSubmit={submitVital}
                style={{
                  background: "linear-gradient(180deg, rgba(30,41,59,0.92), rgba(15,23,42,0.92))",
                  border: "1px solid rgba(96,165,250,0.28)",
                  borderRadius: 24,
                  padding: 22,
                }}
              >
                <h3 style={{ marginTop: 0, marginBottom: 14, fontSize: 24 }}>Add Vitals</h3>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10 }}>
                  <input style={inputStyle} placeholder="Temp" value={vitalForm.temperature} onChange={(e) => setVitalForm({ ...vitalForm, temperature: e.target.value })} />
                  <input style={inputStyle} placeholder="BP" value={vitalForm.bloodPressure} onChange={(e) => setVitalForm({ ...vitalForm, bloodPressure: e.target.value })} />
                  <input style={inputStyle} placeholder="HR" value={vitalForm.heartRate} onChange={(e) => setVitalForm({ ...vitalForm, heartRate: e.target.value })} />
                  <input style={inputStyle} placeholder="RR" value={vitalForm.respiratoryRate} onChange={(e) => setVitalForm({ ...vitalForm, respiratoryRate: e.target.value })} />
                  <input style={inputStyle} placeholder="SpO2" value={vitalForm.oxygenSaturation} onChange={(e) => setVitalForm({ ...vitalForm, oxygenSaturation: e.target.value })} />
                  <input style={inputStyle} placeholder="Time" value={vitalForm.time} onChange={(e) => setVitalForm({ ...vitalForm, time: e.target.value })} />
                </div>
                <div style={{ marginTop: 14 }}>
                  <button type="submit" style={primaryBtn}>Save Vitals</button>
                </div>
              </form>

              <form
                onSubmit={submitNote}
                style={{
                  background: "linear-gradient(180deg, rgba(30,41,59,0.92), rgba(15,23,42,0.92))",
                  border: "1px solid rgba(96,165,250,0.28)",
                  borderRadius: 24,
                  padding: 22,
                }}
              >
                <h3 style={{ marginTop: 0, marginBottom: 14, fontSize: 24 }}>Add Note</h3>
                <textarea
                  style={{ ...inputStyle, minHeight: 132, resize: "vertical" }}
                  placeholder="Write nursing note..."
                  value={noteForm.text}
                  onChange={(e) => setNoteForm({ text: e.target.value })}
                />
                <div style={{ marginTop: 14 }}>
                  <button type="submit" style={primaryBtn}>Save Note</button>
                </div>
              </form>
            </div>

            <form
              onSubmit={submitMAR}
              style={{
                background: "linear-gradient(180deg, rgba(30,41,59,0.92), rgba(15,23,42,0.92))",
                border: "1px solid rgba(96,165,250,0.28)",
                borderRadius: 24,
                padding: 22,
              }}
            >
              <h3 style={{ marginTop: 0, marginBottom: 14, fontSize: 24 }}>
                {editingMarId !== null ? "Edit Medication Administration Record (MAR)" : "Medication Administration Record (MAR)"}
              </h3>

              <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr 1fr 1.4fr", gap: 10 }}>
                <input style={inputStyle} placeholder="Medication" value={marForm.medication} onChange={(e) => setMarForm({ ...marForm, medication: e.target.value })} />
                <input style={inputStyle} placeholder="Dose" value={marForm.dose} onChange={(e) => setMarForm({ ...marForm, dose: e.target.value })} />
                <input style={inputStyle} placeholder="Route" value={marForm.route} onChange={(e) => setMarForm({ ...marForm, route: e.target.value })} />
                <input style={inputStyle} placeholder="Schedule" value={marForm.schedule} onChange={(e) => setMarForm({ ...marForm, schedule: e.target.value })} />
              </div>

              <div style={{ display: "flex", gap: 10, marginTop: 14, flexWrap: "wrap" }}>
                <button type="submit" style={primaryBtn}>
                  {editingMarId !== null ? "Update MAR" : "Add MAR"}
                </button>
                {editingMarId !== null && (
                  <button type="button" style={secondaryBtn} onClick={resetMarForm}>
                    Cancel Edit
                  </button>
                )}
              </div>
            </form>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1.3fr", gap: 20 }}>
              <div
                style={{
                  background: "linear-gradient(180deg, rgba(30,41,59,0.92), rgba(15,23,42,0.92))",
                  border: "1px solid rgba(96,165,250,0.28)",
                  borderRadius: 24,
                  padding: 22,
                }}
              >
                <h3 style={{ marginTop: 0, marginBottom: 14, fontSize: 24 }}>Vital History</h3>
                <div style={{ display: "grid", gap: 12 }}>
                  {vitals.length === 0 ? (
                    <div style={{ color: "#cbd5e1" }}>No vitals yet</div>
                  ) : vitals.map((item) => (
                    <div style={itemStyle} key={item.id}>
                      <div><strong>Temp:</strong> {item.temperature} °C</div>
                      <div><strong>BP:</strong> {item.bloodPressure}</div>
                      <div><strong>HR:</strong> {item.heartRate}</div>
                      <div><strong>RR:</strong> {item.respiratoryRate}</div>
                      <div><strong>SpO2:</strong> {item.oxygenSaturation}%</div>
                      <div style={{ marginTop: 8, color: "#cbd5e1" }}>{item.time}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div
                style={{
                  background: "linear-gradient(180deg, rgba(30,41,59,0.92), rgba(15,23,42,0.92))",
                  border: "1px solid rgba(96,165,250,0.28)",
                  borderRadius: 24,
                  padding: 22,
                }}
              >
                <h3 style={{ marginTop: 0, marginBottom: 14, fontSize: 24 }}>Nursing Notes</h3>
                <div style={{ display: "grid", gap: 12 }}>
                  {notes.length === 0 ? (
                    <div style={{ color: "#cbd5e1" }}>No notes yet</div>
                  ) : notes.map((item) => (
                    <div style={itemStyle} key={item.id}>
                      {item.text}
                    </div>
                  ))}
                </div>
              </div>

              <div
                style={{
                  background: "linear-gradient(180deg, rgba(30,41,59,0.92), rgba(15,23,42,0.92))",
                  border: "1px solid rgba(96,165,250,0.28)",
                  borderRadius: 24,
                  padding: 22,
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap", alignItems: "center" }}>
                  <h3 style={{ margin: 0, fontSize: 24 }}>MAR List</h3>
                  <button type="button" style={secondaryBtn} onClick={markAllPendingAsGiven}>
                    Mark all Pending as Given
                  </button>
                </div>

                <div style={{ display: "flex", gap: 10, flexWrap: "wrap", marginTop: 14 }}>
                  <div style={itemStyle}><strong>Total:</strong> {totalMarCount}</div>
                  <div style={itemStyle}><strong>Pending:</strong> {pendingMarCount}</div>
                  <div style={itemStyle}><strong>Given:</strong> {givenMarCount}</div>
                </div>

                <div style={{ display: "flex", gap: 8, marginTop: 14, flexWrap: "wrap" }}>
                  <button type="button" style={secondaryBtn} onClick={() => setMarFilter("all")}>All</button>
                  <button type="button" style={secondaryBtn} onClick={() => setMarFilter("Pending")}>Pending</button>
                  <button type="button" style={secondaryBtn} onClick={() => setMarFilter("Given")}>Given</button>
                </div>

                <div style={{ display: "flex", gap: 8, marginTop: 14 }}>
                  <input
                    style={inputStyle}
                    placeholder="Search medication name..."
                    value={marSearch}
                    onChange={(e) => setMarSearch(e.target.value)}
                  />
                  <button type="button" style={secondaryBtn} onClick={() => setMarSearch("")}>Clear</button>
                  <button
                    type="button"
                    style={secondaryBtn}
                    onClick={() => {
                      setMarSearch("")
                      setMarFilter("all")
                    }}
                  >
                    Reset
                  </button>
                </div>

                <div style={{ display: "grid", gap: 12, marginTop: 16 }}>
                  {filteredMar.length === 0 ? (
                    <div style={{ color: "#cbd5e1" }}>No MAR items for this filter or search.</div>
                  ) : filteredMar.map((m) => (
                    <div style={itemStyle} key={m.id}>
                      <div style={{ fontSize: 18, fontWeight: 800 }}>{m.medication}</div>
                      <div style={{ marginTop: 6, color: "#e2e8f0" }}>
                        {m.dose} • {m.route} • {m.schedule}
                      </div>

                      <div
                        style={{
                          display: "inline-block",
                          marginTop: 10,
                          padding: "6px 10px",
                          borderRadius: 999,
                          fontSize: 13,
                          fontWeight: 800,
                          background: m.status === "Given" ? "#dcfce7" : "#fef3c7",
                          color: m.status === "Given" ? "#166534" : "#92400e",
                        }}
                      >
                        {m.status}{m.givenAt ? ` at ${m.givenAt}` : ""}
                      </div>

                      {m.createdAt && (
                        <div style={{ marginTop: 8, color: "#cbd5e1", fontSize: 13 }}>
                          Created: {m.createdAt}
                        </div>
                      )}

                      <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginTop: 12 }}>
                        {m.status !== "Given" && (
                          <button type="button" style={primaryBtn} onClick={() => markAsGiven(m.id)}>
                            Mark as Given
                          </button>
                        )}
                        <button type="button" style={secondaryBtn} onClick={() => startEditMarItem(m)}>
                          Edit
                        </button>
                        <button type="button" style={secondaryBtn} onClick={() => deleteMarItem(m.id)}>
                          Delete
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  )
}

const inputStyle: React.CSSProperties = {
  width: "100%",
  border: "1px solid rgba(148,163,184,0.35)",
  borderRadius: 14,
  padding: "12px 14px",
  background: "rgba(255,255,255,0.08)",
  color: "#f8fafc",
  outline: "none",
}

const primaryBtn: React.CSSProperties = {
  border: "none",
  borderRadius: 14,
  padding: "12px 16px",
  background: "linear-gradient(135deg, #0ea5e9, #2563eb)",
  color: "white",
  fontWeight: 700,
  cursor: "pointer",
}

const secondaryBtn: React.CSSProperties = {
  border: "1px solid rgba(148,163,184,0.35)",
  borderRadius: 14,
  padding: "12px 16px",
  background: "rgba(255,255,255,0.08)",
  color: "#e5e7eb",
  fontWeight: 700,
  cursor: "pointer",
}

const itemStyle: React.CSSProperties = {
  background: "linear-gradient(180deg, rgba(37,99,235,0.18), rgba(15,23,42,0.30))",
  border: "1px solid rgba(96,165,250,0.26)",
  borderRadius: 18,
  padding: 16,
  boxShadow: "0 8px 18px rgba(0,0,0,0.18)",
}
