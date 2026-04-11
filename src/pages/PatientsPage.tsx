import { useEffect, useMemo, useState } from "react"
import { useNavigate, useSearchParams } from "react-router-dom"
import { apiGet } from "@/lib/api"
import { createDoctorAssignment } from "@/lib/doctorAssignments"

type Patient = {
  id: string
  name: string
  age?: number
  gender?: string
  phone?: string
  condition?: string
  department?: string
  status?: string
}

export default function PatientsPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()

  const doctorId = searchParams.get("doctorId") ?? ""
  const doctorName = searchParams.get("doctorName") ?? ""

  const [patients, setPatients] = useState<Patient[]>([])
  const [q, setQ] = useState("")
  const [department, setDepartment] = useState("all")
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [selectedId, setSelectedId] = useState("")
  const [assigning, setAssigning] = useState(false)
  const [marCount, setMarCount] = useState(0)

  useEffect(() => {
    async function loadPatients() {
      try {
        setLoading(true)
        setError("")

        const data = await apiGet<Patient[]>("/patients")
        setPatients(Array.isArray(data) ? data : [])
      } catch (err) {
        console.error("ERROR:", err)
        setError("Failed to load patients")
        setPatients([])
      } finally {
        setLoading(false)
      }
    }

    loadPatients()
  }, [])

  const filtered = useMemo(() => {
    const query = q.trim().toLowerCase()

    return patients.filter((p) => {
      const matchesText =
        !query ||
        p.id.toLowerCase().includes(query) ||
        p.name.toLowerCase().includes(query) ||
        String(p.department ?? "").toLowerCase().includes(query) ||
        String(p.condition ?? "").toLowerCase().includes(query)

      const matchesDepartment =
        department === "all" ||
        String(p.department ?? "").toLowerCase() === department.toLowerCase()

      return matchesText && matchesDepartment
    })
  }, [patients, q, department])

  const selected =
    patients.find((p) => p.id === selectedId) ||
    filtered[0] ||
    null

  const handleAssignPatient = async () => {
    if (!selected || !doctorName || !doctorId) return

    try {
      setAssigning(true)

      await createDoctorAssignment(doctorId, {
        patientId: selected.id,
        patientName: selected.name,
        department: selected.department,
        condition: selected.condition,
        status: "Assigned",
      })

      alert(`Patient ${selected.name} assigned to ${doctorName}`)
      navigate(`/doctors/${doctorId}`)
    } catch (err) {
      console.error(err)
      alert("Failed to assign patient")
    } finally {
      setAssigning(false)
    }
  }

  return (
    <div style={{ padding: "24px", color: "white" }}>
      <h1 style={{ fontSize: "30px", marginBottom: "8px" }}>Patients System</h1>
      <p style={{ opacity: 0.8, marginBottom: "20px" }}>
        Electronic Medical Record workspace
      </p>

      {doctorName && (
        <div
          style={{
            background: "#0f172a",
            border: "1px solid #0f766e",
            color: "#ccfbf1",
            borderRadius: "14px",
            padding: "14px 16px",
            marginBottom: "18px",
          }}
        >
          <div style={{ fontWeight: 800, marginBottom: 4 }}>
            Assign patient workflow for {doctorName}
          </div>
          <div style={{ opacity: 0.85, fontSize: 14 }}>
            Doctor ID: {doctorId || "N/A"} • Select a patient, then assign from the summary panel.
          </div>
        </div>
      )}

      <div style={{ marginBottom: "16px", opacity: 0.8 }}>
        Total patients: {patients.length} | Filtered: {filtered.length}
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "380px minmax(0,1fr)",
          gap: "20px",
          alignItems: "start",
        }}
      >
        <div
          style={{
            background: "#111827",
            border: "1px solid #374151",
            borderRadius: "16px",
            padding: "16px",
          }}
        >
          <div style={{ display: "grid", gap: "12px", marginBottom: "16px" }}>
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Search by ID, name, department, condition"
              style={{
                width: "100%",
                padding: "12px",
                borderRadius: "10px",
                border: "1px solid #4b5563",
                background: "#0f172a",
                color: "white",
              }}
            />

            <select
              value={department}
              onChange={(e) => setDepartment(e.target.value)}
              style={{
                width: "100%",
                padding: "12px",
                borderRadius: "10px",
                border: "1px solid #4b5563",
                background: "#0f172a",
                color: "white",
              }}
            >
              <option value="all">All departments</option>
              <option value="cardiology">Cardiology</option>
              <option value="neurology">Neurology</option>
              <option value="orthopedics">Orthopedics</option>
              <option value="icu">ICU</option>
              <option value="emergency">Emergency</option>
            </select>
          </div>

          {loading && <p>Loading patients...</p>}
          {error && <p style={{ color: "#fca5a5" }}>{error}</p>}

          {!loading && !error && filtered.length === 0 && (
            <p>No patients found.</p>
          )}

          {!loading && !error && filtered.length > 0 && (
            <div style={{ display: "grid", gap: "10px" }}>
              {filtered.map((p) => {
                const active = selected?.id === p.id

                return (
                  <button
                    key={p.id}
                    onClick={() => setSelectedId(p.id)}
                    style={{
                      textAlign: "left",
                      padding: "14px",
                      borderRadius: "12px",
                      border: active ? "1px solid #60a5fa" : "1px solid #374151",
                      background: active ? "#1e3a8a" : "#0f172a",
                      color: "white",
                      cursor: "pointer",
                    }}
                  >
                    <div style={{ fontWeight: 700 }}>{p.name}</div>
                    <div style={{ fontSize: "13px", opacity: 0.8 }}>
                      ID: {p.id}
                    </div>
                    <div style={{ fontSize: "13px", opacity: 0.8 }}>
                      {p.department ?? "No department"} • {p.condition ?? "No condition"}
                    </div>
                  </button>
                )
              })}
            </div>
          )}
        </div>

        <div
          style={{
            background: "#111827",
            border: "1px solid #374151",
            borderRadius: "16px",
            padding: "20px",
            minHeight: "500px",
          }}
        >
          <h2 style={{ marginTop: 0, marginBottom: "16px" }}>Patient Summary</h2>

          {!selected ? (
            <p>Select a patient to view details.</p>
          ) : (
            <div style={{ display: "grid", gap: "12px" }}>
              <div><strong>Name:</strong> {selected.name}</div>
              <div><strong>ID:</strong> {selected.id}</div>
              <div><strong>Age:</strong> {selected.age ?? "—"}</div>
              <div><strong>Gender:</strong> {selected.gender ?? "—"}</div>
              <div><strong>Phone:</strong> {selected.phone ?? "—"}</div>
              <div><strong>Department:</strong> {selected.department ?? "—"}</div>
              <div><strong>Condition:</strong> {selected.condition ?? "—"}</div>
              <div><strong>Status:</strong> {selected.status ?? "—"}</div>
              <div><strong>MAR Count:</strong> {marCount}</div>

              <div
                style={{
                  marginTop: "16px",
                  display: "flex",
                  gap: "12px",
                  flexWrap: "wrap",
                }}
              >
                <button
                  onClick={() => navigate(`/patient-profile?id=${selected.id}`)}
                  style={{
                    padding: "12px 16px",
                    borderRadius: "10px",
                    border: "none",
                    background: "#2563eb",
                    color: "white",
                    cursor: "pointer",
                    fontWeight: 600,
                  }}
                >
                  Open Patient Profile
                </button>

                <button
                  onClick={() => navigate(`/nurses?patientId=${selected.id}`)}
                  style={{
                    padding: "12px 16px",
                    borderRadius: "10px",
                    border: "none",
                    background: "#7c3aed",
                    color: "white",
                    cursor: "pointer",
                    fontWeight: 600,
                  }}
                >
                  Open Nursing Station
                </button>


                {doctorName && (
                  <button
                    onClick={handleAssignPatient}
                    disabled={assigning}
                    style={{
                      padding: "12px 16px",
                      borderRadius: "10px",
                      border: "none",
                      background: "#0f766e",
                      color: "white",
                      cursor: assigning ? "not-allowed" : "pointer",
                      opacity: assigning ? 0.7 : 1,
                      fontWeight: 700,
                    }}
                  >
                    {assigning ? "Assigning..." : "Assign Selected Patient"}
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
