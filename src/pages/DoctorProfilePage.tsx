import { useEffect, useMemo, useState } from "react"
import { useNavigate, useParams } from "react-router-dom"
import { getDoctorById, type DoctorRecord } from "@/lib/doctors"
import {
  getDoctorAssignments,
  removeDoctorAssignment,
  updateDoctorAssignmentStatus,
  type DoctorAssignmentRecord,
} from "@/lib/doctorAssignments"
import {
  createAppointment,
  getAppointments,
  type AppointmentRecord,
} from "@/lib/appointments"
import {
  addDoctorNote,
  getDoctorNotes,
  removeDoctorNote,
  type DoctorNoteRecord,
} from "@/lib/doctorNotes"

function exportDoctorSummaryPDF() {
  const element = document.getElementById("doctor-summary-report")
  if (!element) {
    alert("Doctor summary not found")
    return
  }

  const printWindow = window.open("", "_blank", "width=1100,height=1400")
  if (!printWindow) {
    alert("Popup blocked. Please allow popups.")
    return
  }

  printWindow.document.write(`
    <html>
      <head>
        <title>Doctor Summary Report</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            margin: 24px;
            color: #111827;
            background: white;
          }
          #print-root {
            width: 100%;
          }
          .avoid-break {
            page-break-inside: avoid;
            break-inside: avoid;
          }
          @media print {
            body {
              margin: 0;
              padding: 14px;
            }
          }
        </style>
      </head>
      <body>
        <div id="print-root">${element.innerHTML}</div>
      </body>
    </html>
  `)

  printWindow.document.close()
  printWindow.focus()

  setTimeout(() => {
    printWindow.print()
  }, 500)
}

function statusColor(status: DoctorRecord["status"]) {
  if (status === "Available") return { bg: "#dcfce7", color: "#166534" }
  if (status === "On Call") return { bg: "#fef3c7", color: "#92400e" }
  if (status === "In Surgery") return { bg: "#fee2e2", color: "#991b1b" }
  return { bg: "#e5e7eb", color: "#374151" }
}

function assignmentTone(status?: string) {
  const value = String(status ?? "").toLowerCase()
  if (value === "completed") return { bg: "#dcfce7", color: "#166534" }
  if (value === "in follow-up") return { bg: "#fef3c7", color: "#92400e" }
  return { bg: "#dbeafe", color: "#1d4ed8" }
}

function appointmentTone(status?: string) {
  const value = String(status ?? "").toLowerCase()
  if (value.includes("scheduled")) return { bg: "#dbeafe", color: "#1d4ed8" }
  if (value.includes("waiting")) return { bg: "#fef3c7", color: "#92400e" }
  if (value.includes("completed")) return { bg: "#dcfce7", color: "#166534" }
  return { bg: "#e5e7eb", color: "#374151" }
}

export default function DoctorProfilePage() {
  const { doctorId = "" } = useParams()
  const navigate = useNavigate()

  const [doctor, setDoctor] = useState<DoctorRecord | null>(null)
  const [assignments, setAssignments] = useState<DoctorAssignmentRecord[]>([])
  const [appointments, setAppointments] = useState<AppointmentRecord[]>([])
  const [doctorNotes, setDoctorNotes] = useState<DoctorNoteRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [busyId, setBusyId] = useState<number | null>(null)

  const [showCreateAppointment, setShowCreateAppointment] = useState(false)
  const [creatingAppointment, setCreatingAppointment] = useState(false)
  const [appointmentPatient, setAppointmentPatient] = useState("")
  const [appointmentDepartment, setAppointmentDepartment] = useState("")
  const [appointmentTime, setAppointmentTime] = useState("")

  const [showQuickNote, setShowQuickNote] = useState(false)
  const [quickNoteText, setQuickNoteText] = useState("")

  async function loadDoctorProfile() {
    if (!doctorId) return

    try {
      setLoading(true)
      setError("")

      const doctorData = await getDoctorById(doctorId)

      const [assignmentsData, appointmentsData] = await Promise.all([
        getDoctorAssignments(doctorId),
        getAppointments(),
      ])

      const doctorAppointments = Array.isArray(appointmentsData)
        ? appointmentsData.filter((item) =>
            item.doctor.toLowerCase().includes(doctorData.name.toLowerCase())
          )
        : []

      setDoctor(doctorData)
      setAssignments(assignmentsData)
      setAppointments(doctorAppointments)
      setDoctorNotes(getDoctorNotes(doctorId))
      setAppointmentDepartment(doctorData.specialty || doctorData.department || "")
    } catch (err) {
      console.error(err)
      setError("Failed to load doctor profile")
      setDoctor(null)
      setAssignments([])
      setAppointments([])
      setDoctorNotes([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadDoctorProfile()
  }, [doctorId])

  const badge = useMemo(
    () =>
      doctor
        ? statusColor(doctor.status)
        : { bg: "#e5e7eb", color: "#374151" },
    [doctor]
  )

  const assignmentStats = useMemo(() => {
    const assigned = assignments.filter(
      (item) => String(item.status ?? "").toLowerCase() === "assigned"
    ).length

    const followUp = assignments.filter(
      (item) => String(item.status ?? "").toLowerCase() === "in follow-up"
    ).length

    const completed = assignments.filter(
      (item) => String(item.status ?? "").toLowerCase() === "completed"
    ).length

    return {
      total: assignments.length,
      assigned,
      followUp,
      completed,
    }
  }, [assignments])

  const handleStatusChange = async (assignmentId: number, status: string) => {
    if (!doctorId) return

    try {
      setBusyId(assignmentId)
      await updateDoctorAssignmentStatus(doctorId, assignmentId, status)
      setAssignments((current) =>
        current.map((item) =>
          item.id === assignmentId ? { ...item, status } : item
        )
      )
    } catch (err) {
      console.error(err)
      alert("Failed to update assignment status")
    } finally {
      setBusyId(null)
    }
  }

  const handleRemove = async (assignmentId: number) => {
    if (!doctorId) return

    try {
      setBusyId(assignmentId)
      await removeDoctorAssignment(doctorId, assignmentId)
      setAssignments((current) =>
        current.filter((item) => item.id !== assignmentId)
      )
    } catch (err) {
      console.error(err)
      alert("Failed to remove assignment")
    } finally {
      setBusyId(null)
    }
  }

  const handleCreateAppointment = async () => {
    if (!doctor) return
    if (!appointmentPatient.trim() || !appointmentDepartment.trim() || !appointmentTime.trim()) {
      alert("Please fill patient name, department, and time")
      return
    }

    try {
      setCreatingAppointment(true)

      const created = await createAppointment({
        patient: appointmentPatient.trim(),
        department: appointmentDepartment.trim(),
        doctor: doctor.name,
        time: appointmentTime.trim(),
        status: "Scheduled",
      })

      setAppointments((current) => [...current, created])
      setAppointmentPatient("")
      setAppointmentTime("")
      setShowCreateAppointment(false)
    } catch (err) {
      console.error(err)
      alert("Failed to create appointment")
    } finally {
      setCreatingAppointment(false)
    }
  }

  const handleCreateQuickNote = () => {
    if (!doctorId) return
    if (!quickNoteText.trim()) {
      alert("Please enter a note")
      return
    }

    const created = addDoctorNote(doctorId, quickNoteText.trim())
    setDoctorNotes((current) => [created, ...current])
    setQuickNoteText("")
    setShowQuickNote(false)
  }

  const handleRemoveNote = (noteId: number) => {
    if (!doctorId) return
    removeDoctorNote(doctorId, noteId)
    setDoctorNotes((current) => current.filter((note) => note.id !== noteId))
  }

  return (
    <div style={{ padding: 24, color: "#e5eef8" }}>
      <div style={{ marginBottom: 20, display: "flex", gap: 12, flexWrap: "wrap" }}>
        <button
          onClick={() => navigate("/doctors")}
          style={{
            padding: "10px 14px",
            borderRadius: 12,
            border: "1px solid #334155",
            background: "#0f172a",
            color: "white",
            cursor: "pointer",
            fontWeight: 700,
          }}
        >
          ← Back to Doctors
        </button>

        {doctor?.specialty && (
          <button
            onClick={() => navigate(`/specialties/${doctor.specialty.toLowerCase()}`)}
            style={{
              padding: "10px 14px",
              borderRadius: 12,
              border: "1px solid #334155",
              background: "#1e293b",
              color: "white",
              cursor: "pointer",
              fontWeight: 700,
            }}
          >
            Open {doctor.specialty}
          </button>
        )}

        <button
          onClick={exportDoctorSummaryPDF}
          style={{
            padding: "10px 14px",
            borderRadius: 12,
            border: "none",
            background: "#2563eb",
            color: "white",
            cursor: "pointer",
            fontWeight: 800,
          }}
        >
          Export Doctor Summary PDF
        </button>
      </div>

      {error && <div style={{ color: "#fecaca", marginBottom: 16 }}>{error}</div>}
      {loading && <div style={{ marginBottom: 16 }}>Loading doctor profile...</div>}

      {!loading && !doctor ? <div>Doctor not found.</div> : null}

      {doctor && (
        <div
          id="doctor-summary-report"
          style={{
            display: "grid",
            gridTemplateColumns: "1.2fr 1fr",
            gap: 20,
          }}
        >
          <div
            className="avoid-break"
            style={{
              background: "#f8fafc",
              color: "#0f172a",
              borderRadius: 26,
              padding: 24,
              boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
            }}
          >
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "120px 1fr",
                gap: 20,
                alignItems: "center",
                marginBottom: 24,
              }}
            >
              <div
                style={{
                  width: 120,
                  height: 120,
                  borderRadius: 28,
                  background: "#dbeafe",
                  color: "#1d4ed8",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: 40,
                  fontWeight: 800,
                }}
              >
                {doctor.name
                  .split(" ")
                  .slice(0, 2)
                  .map((p) => p[0])
                  .join("")}
              </div>

              <div>
                <div style={{ fontSize: 30, fontWeight: 800, marginBottom: 6 }}>
                  {doctor.name}
                </div>
                <div style={{ color: "#475569", fontSize: 17, marginBottom: 8 }}>
                  {doctor.specialty} • {doctor.department}
                </div>
                <div
                  style={{
                    display: "inline-block",
                    background: badge.bg,
                    color: badge.color,
                    padding: "7px 12px",
                    borderRadius: 999,
                    fontWeight: 800,
                    fontSize: 13,
                  }}
                >
                  {doctor.status}
                </div>
              </div>
            </div>

            <div
              className="avoid-break"
              style={{
                background: "white",
                border: "1px solid #e2e8f0",
                borderRadius: 20,
                padding: 18,
                display: "grid",
                gap: 12,
                marginBottom: 18,
              }}
            >
              <InfoRow label="Doctor ID" value={doctor.id} />
              <InfoRow label="Department" value={doctor.department} />
              <InfoRow label="Specialty" value={doctor.specialty} />
              <InfoRow label="Experience" value={doctor.experience} />
              <InfoRow label="Schedule" value={doctor.schedule} />
              <InfoRow label="Phone" value={doctor.phone} />
            </div>

            <div
              style={{
                display: "flex",
                gap: 12,
                flexWrap: "wrap",
              }}
            >
              <button
                onClick={() =>
                  navigate(
                    `/appointments?doctorId=${encodeURIComponent(doctor.id)}&doctorName=${encodeURIComponent(doctor.name)}`
                  )
                }
                style={{
                  padding: "12px 16px",
                  borderRadius: 14,
                  border: "none",
                  background: "#2563eb",
                  color: "white",
                  cursor: "pointer",
                  fontWeight: 800,
                }}
              >
                Book Appointment
              </button>

              <button
                onClick={() => setShowCreateAppointment((v) => !v)}
                style={{
                  padding: "12px 16px",
                  borderRadius: 14,
                  border: "none",
                  background: "#7c3aed",
                  color: "white",
                  cursor: "pointer",
                  fontWeight: 800,
                }}
              >
                Create Appointment
              </button>

              <button
                onClick={() => setShowQuickNote((v) => !v)}
                style={{
                  padding: "12px 16px",
                  borderRadius: 14,
                  border: "none",
                  background: "#0f766e",
                  color: "white",
                  cursor: "pointer",
                  fontWeight: 800,
                }}
              >
                Create Quick Note
              </button>

              <button
                onClick={() =>
                  navigate(
                    `/patients?doctorId=${encodeURIComponent(doctor.id)}&doctorName=${encodeURIComponent(doctor.name)}`
                  )
                }
                style={{
                  padding: "12px 16px",
                  borderRadius: 14,
                  border: "none",
                  background: "#ea580c",
                  color: "white",
                  cursor: "pointer",
                  fontWeight: 800,
                }}
              >
                Assign Patient
              </button>
            </div>

            {showCreateAppointment && (
              <div
                style={{
                  marginTop: 18,
                  background: "#ffffff",
                  border: "1px solid #e2e8f0",
                  borderRadius: 20,
                  padding: 18,
                  display: "grid",
                  gap: 12,
                }}
              >
                <div style={{ fontSize: 18, fontWeight: 800 }}>Quick Create Appointment</div>

                <input
                  value={appointmentPatient}
                  onChange={(e) => setAppointmentPatient(e.target.value)}
                  placeholder="Patient name"
                  style={inputStyle}
                />

                <input
                  value={appointmentDepartment}
                  onChange={(e) => setAppointmentDepartment(e.target.value)}
                  placeholder="Department"
                  style={inputStyle}
                />

                <input
                  value={appointmentTime}
                  onChange={(e) => setAppointmentTime(e.target.value)}
                  placeholder="Time e.g. 2026-03-17 16:00"
                  style={inputStyle}
                />

                <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
                  <button
                    onClick={handleCreateAppointment}
                    disabled={creatingAppointment}
                    style={{
                      padding: "10px 14px",
                      borderRadius: 12,
                      border: "none",
                      background: "#2563eb",
                      color: "white",
                      cursor: creatingAppointment ? "not-allowed" : "pointer",
                      opacity: creatingAppointment ? 0.7 : 1,
                      fontWeight: 800,
                    }}
                  >
                    {creatingAppointment ? "Creating..." : "Save Appointment"}
                  </button>

                  <button
                    onClick={() => setShowCreateAppointment(false)}
                    style={{
                      padding: "10px 14px",
                      borderRadius: 12,
                      border: "1px solid #cbd5e1",
                      background: "#fff",
                      color: "#0f172a",
                      cursor: "pointer",
                      fontWeight: 700,
                    }}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}

            {showQuickNote && (
              <div
                style={{
                  marginTop: 18,
                  background: "#ffffff",
                  border: "1px solid #e2e8f0",
                  borderRadius: 20,
                  padding: 18,
                  display: "grid",
                  gap: 12,
                }}
              >
                <div style={{ fontSize: 18, fontWeight: 800 }}>Quick Clinical Note</div>

                <textarea
                  value={quickNoteText}
                  onChange={(e) => setQuickNoteText(e.target.value)}
                  placeholder="Write a quick doctor note..."
                  rows={5}
                  style={{
                    ...inputStyle,
                    resize: "vertical",
                    minHeight: 120,
                  }}
                />

                <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
                  <button
                    onClick={handleCreateQuickNote}
                    style={{
                      padding: "10px 14px",
                      borderRadius: 12,
                      border: "none",
                      background: "#0f766e",
                      color: "white",
                      cursor: "pointer",
                      fontWeight: 800,
                    }}
                  >
                    Save Note
                  </button>

                  <button
                    onClick={() => setShowQuickNote(false)}
                    style={{
                      padding: "10px 14px",
                      borderRadius: 12,
                      border: "1px solid #cbd5e1",
                      background: "#fff",
                      color: "#0f172a",
                      cursor: "pointer",
                      fontWeight: 700,
                    }}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}
          </div>

          <div style={{ display: "grid", gap: 20 }}>
            <div
              className="avoid-break"
              style={{
                background: "#f8fafc",
                color: "#0f172a",
                borderRadius: 26,
                padding: 22,
                boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
              }}
            >
              <div style={{ fontSize: 18, fontWeight: 800, marginBottom: 14 }}>
                Performance Snapshot
              </div>
              <div style={{ display: "grid", gap: 12 }}>
                <MetricCard title="Patients Today" value={String(doctor.patients)} />
                <MetricCard title="Average Rating" value={`⭐ ${doctor.rating}`} />
                <MetricCard title="Availability" value={doctor.status} />
              </div>
            </div>

            <div
              className="avoid-break"
              style={{
                background: "#f8fafc",
                color: "#0f172a",
                borderRadius: 26,
                padding: 22,
                boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
              }}
            >
              <div style={{ fontSize: 18, fontWeight: 800, marginBottom: 14 }}>
                Assignment Dashboard
              </div>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
                  gap: 12,
                }}
              >
                <SmallDashboardCard title="Total" value={String(assignmentStats.total)} tone="#e0f2fe" />
                <SmallDashboardCard title="Assigned" value={String(assignmentStats.assigned)} tone="#dbeafe" />
                <SmallDashboardCard title="In Follow-up" value={String(assignmentStats.followUp)} tone="#fef3c7" />
                <SmallDashboardCard title="Completed" value={String(assignmentStats.completed)} tone="#dcfce7" />
              </div>
            </div>

            <div
              className="avoid-break"
              style={{
                background: "#f8fafc",
                color: "#0f172a",
                borderRadius: 26,
                padding: 22,
                boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  gap: 12,
                  marginBottom: 12,
                }}
              >
                <div style={{ fontSize: 18, fontWeight: 800 }}>
                  Upcoming Appointments
                </div>

                <button
                  onClick={() =>
                    navigate(
                      `/appointments?doctorId=${encodeURIComponent(doctor.id)}&doctorName=${encodeURIComponent(doctor.name)}`
                    )
                  }
                  style={{
                    padding: "8px 12px",
                    borderRadius: 10,
                    border: "none",
                    background: "#2563eb",
                    color: "white",
                    cursor: "pointer",
                    fontWeight: 700,
                    fontSize: 12,
                  }}
                >
                  Open Appointments
                </button>
              </div>

              {appointments.length === 0 ? (
                <div style={{ color: "#64748b" }}>No upcoming appointments found.</div>
              ) : (
                <div style={{ display: "grid", gap: 10 }}>
                  {appointments.map((item) => {
                    const tone = appointmentTone(item.status)

                    return (
                      <div
                        key={item.id}
                        style={{
                          background: "white",
                          border: "1px solid #e2e8f0",
                          borderRadius: 16,
                          padding: 14,
                        }}
                      >
                        <div
                          style={{
                            display: "flex",
                            justifyContent: "space-between",
                            gap: 12,
                            flexWrap: "wrap",
                            alignItems: "start",
                          }}
                        >
                          <div>
                            <div style={{ fontWeight: 800 }}>{item.patient}</div>
                            <div style={{ color: "#64748b", marginTop: 4 }}>
                              {item.department}
                            </div>
                            <div style={{ color: "#64748b", marginTop: 4 }}>
                              {item.time}
                            </div>
                          </div>

                          <div
                            style={{
                              background: tone.bg,
                              color: tone.color,
                              padding: "6px 10px",
                              borderRadius: 999,
                              fontWeight: 800,
                              fontSize: 12,
                            }}
                          >
                            {item.status}
                          </div>
                        </div>
                      </div>
                    )
                  })}
                </div>
              )}
            </div>

            <div
              className="avoid-break"
              style={{
                background: "#f8fafc",
                color: "#0f172a",
                borderRadius: 26,
                padding: 22,
                boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
              }}
            >
              <div style={{ fontSize: 18, fontWeight: 800, marginBottom: 12 }}>
                Doctor Notes
              </div>

              {doctorNotes.length === 0 ? (
                <div style={{ color: "#64748b" }}>No quick notes yet.</div>
              ) : (
                <div style={{ display: "grid", gap: 10 }}>
                  {doctorNotes.map((note) => (
                    <div
                      key={note.id}
                      style={{
                        background: "white",
                        border: "1px solid #e2e8f0",
                        borderRadius: 16,
                        padding: 14,
                      }}
                    >
                      <div style={{ whiteSpace: "pre-wrap", lineHeight: 1.7 }}>
                        {note.text}
                      </div>
                      <div
                        style={{
                          marginTop: 10,
                          display: "flex",
                          justifyContent: "space-between",
                          gap: 12,
                          alignItems: "center",
                          flexWrap: "wrap",
                        }}
                      >
                        <div style={{ color: "#64748b", fontSize: 13 }}>
                          {note.createdAt}
                        </div>
                        <button
                          onClick={() => handleRemoveNote(note.id)}
                          style={smallActionButton("#b91c1c")}
                        >
                          Remove Note
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div
              className="avoid-break"
              style={{
                background: "#f8fafc",
                color: "#0f172a",
                borderRadius: 26,
                padding: 22,
                boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
              }}
            >
              <div style={{ fontSize: 18, fontWeight: 800, marginBottom: 12 }}>
                Assigned Patients
              </div>

              {assignments.length === 0 ? (
                <div style={{ color: "#64748b" }}>No assigned patients yet.</div>
              ) : (
                <div style={{ display: "grid", gap: 10 }}>
                  {assignments.map((item) => {
                    const tone = assignmentTone(item.status)

                    return (
                      <div
                        key={item.id}
                        style={{
                          background: "white",
                          border: "1px solid #e2e8f0",
                          borderRadius: 16,
                          padding: 14,
                        }}
                      >
                        <div
                          style={{
                            display: "flex",
                            justifyContent: "space-between",
                            gap: 12,
                            alignItems: "start",
                            flexWrap: "wrap",
                          }}
                        >
                          <div>
                            <div style={{ fontWeight: 800 }}>{item.patientName}</div>
                            <div style={{ color: "#64748b", marginTop: 4 }}>
                              {item.patientId} • {item.department ?? "No department"}
                            </div>
                            <div style={{ color: "#64748b", marginTop: 4 }}>
                              {item.condition ?? "No condition"}
                            </div>
                          </div>

                          <div
                            style={{
                              background: tone.bg,
                              color: tone.color,
                              padding: "6px 10px",
                              borderRadius: 999,
                              fontWeight: 800,
                              fontSize: 12,
                            }}
                          >
                            {item.status ?? "Assigned"}
                          </div>
                        </div>

                        <div
                          style={{
                            marginTop: 12,
                            display: "flex",
                            gap: 8,
                            flexWrap: "wrap",
                          }}
                        >
                          <button
                            onClick={() => handleStatusChange(item.id, "Assigned")}
                            disabled={busyId === item.id}
                            style={smallActionButton("#2563eb")}
                          >
                            Assigned
                          </button>

                          <button
                            onClick={() => handleStatusChange(item.id, "In Follow-up")}
                            disabled={busyId === item.id}
                            style={smallActionButton("#d97706")}
                          >
                            In Follow-up
                          </button>

                          <button
                            onClick={() => handleStatusChange(item.id, "Completed")}
                            disabled={busyId === item.id}
                            style={smallActionButton("#15803d")}
                          >
                            Completed
                          </button>

                          <button
                            onClick={() => handleRemove(item.id)}
                            disabled={busyId === item.id}
                            style={smallActionButton("#b91c1c")}
                          >
                            Remove
                          </button>
                        </div>
                      </div>
                    )
                  })}
                </div>
              )}
            </div>

            <div
              className="avoid-break"
              style={{
                background: "#ecfeff",
                color: "#0f172a",
                border: "1px solid #a5f3fc",
                borderRadius: 26,
                padding: 22,
              }}
            >
              <div style={{ fontSize: 18, fontWeight: 800, marginBottom: 12 }}>
                Recommended Actions
              </div>
              <ul style={{ margin: 0, paddingLeft: 18, lineHeight: 1.9, color: "#155e75" }}>
                <li>Review live schedule and on-call responsibilities.</li>
                <li>Open specialty dashboard for related department workflow.</li>
                <li>Monitor patient load and staffing balance.</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function InfoRow({ label, value }: { label: string; value: string }) {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        gap: 16,
        borderBottom: "1px solid #f1f5f9",
        paddingBottom: 10,
      }}
    >
      <div style={{ color: "#64748b" }}>{label}</div>
      <div style={{ fontWeight: 700, textAlign: "right" }}>{value}</div>
    </div>
  )
}

function MetricCard({ title, value }: { title: string; value: string }) {
  return (
    <div
      style={{
        background: "white",
        border: "1px solid #e2e8f0",
        borderRadius: 18,
        padding: 16,
      }}
    >
      <div style={{ color: "#64748b", marginBottom: 10 }}>{title}</div>
      <div style={{ fontSize: 26, fontWeight: 800 }}>{value}</div>
    </div>
  )
}

function SmallDashboardCard({
  title,
  value,
  tone,
}: {
  title: string
  value: string
  tone: string
}) {
  return (
    <div
      style={{
        background: tone,
        borderRadius: 18,
        padding: 16,
      }}
    >
      <div style={{ color: "#475569", marginBottom: 8 }}>{title}</div>
      <div style={{ fontSize: 26, fontWeight: 800 }}>{value}</div>
    </div>
  )
}

function smallActionButton(background: string) {
  return {
    padding: "8px 10px",
    borderRadius: 10,
    border: "none",
    background,
    color: "white",
    cursor: "pointer",
    fontWeight: 700,
    fontSize: 12,
  } as const
}

const inputStyle = {
  width: "100%",
  padding: "12px 14px",
  borderRadius: 12,
  border: "1px solid #cbd5e1",
  background: "white",
  color: "#0f172a",
} as const
