import { useEffect, useMemo, useState } from "react"
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
} from "recharts"
import { apiGet } from "@/lib/api"
import { getDoctorsSummary, type DoctorRecord } from "@/lib/doctors"
import { getSpecialtiesSummary, type SpecialtyRecord } from "@/lib/specialties"
import { getDoctorAssignments } from "@/lib/doctorAssignments"

type Patient = {
  id: string
  name: string
}

type Appointment = {
  id: string
  patient: string
  department: string
  doctor: string
  time: string
  status: string
}

type Report = {
  id: string
  title: string
  status: string
}

export default function AdminOverviewPage() {
  const [doctors, setDoctors] = useState<DoctorRecord[]>([])
  const [specialties, setSpecialties] = useState<SpecialtyRecord[]>([])
  const [patientsCount, setPatientsCount] = useState(0)
  const [appointments, setAppointments] = useState<Appointment[]>([])
  const [reports, setReports] = useState<Report[]>([])
  const [assignedPatientsCount, setAssignedPatientsCount] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    async function loadOverview() {
      try {
        setLoading(true)
        setError("")

        const [doctorsData, specialtiesData, patientsData, appointmentsData, reportsData] =
          await Promise.all([
            getDoctorsSummary(),
            getSpecialtiesSummary(),
            apiGet<Patient[]>("/patients"),
            apiGet<Appointment[]>("/appointments"),
            apiGet<Report[]>("/reports"),
          ])

        setDoctors(doctorsData)
        setSpecialties(specialtiesData)
        setPatientsCount(Array.isArray(patientsData) ? patientsData.length : 0)
        setAppointments(Array.isArray(appointmentsData) ? appointmentsData : [])
        setReports(Array.isArray(reportsData) ? reportsData : [])

        const assignmentLists = await Promise.all(
          doctorsData.map((doctor) => getDoctorAssignments(doctor.id))
        )
        const totalAssigned = assignmentLists.reduce(
          (sum, items) => sum + items.length,
          0
        )
        setAssignedPatientsCount(totalAssigned)
      } catch (err) {
        console.error(err)
        setError("Failed to load admin overview")
      } finally {
        setLoading(false)
      }
    }

    loadOverview()
  }, [])

  const availableDoctors = useMemo(
    () => doctors.filter((doctor) => doctor.status === "Available").length,
    [doctors]
  )

  const onCallDoctors = useMemo(
    () => doctors.filter((doctor) => doctor.status === "On Call").length,
    [doctors]
  )

  const busyDoctors = useMemo(
    () =>
      doctors.filter(
        (doctor) => doctor.status === "In Surgery" || doctor.status === "Offline"
      ).length,
    [doctors]
  )

  const specialtyBreakdown = useMemo(() => {
    const map = new Map<string, number>()

    doctors.forEach((doctor) => {
      map.set(doctor.specialty, (map.get(doctor.specialty) ?? 0) + 1)
    })

    return Array.from(map.entries())
      .map(([name, count]) => ({ name, count }))
      .sort((a, b) => b.count - a.count)
  }, [doctors])

  const doctorStatusData = useMemo(() => {
    const available = doctors.filter((d) => d.status === "Available").length
    const onCall = doctors.filter((d) => d.status === "On Call").length
    const inSurgery = doctors.filter((d) => d.status === "In Surgery").length
    const offline = doctors.filter((d) => d.status === "Offline").length

    return [
      { name: "Available", value: available, color: "#22c55e" },
      { name: "On Call", value: onCall, color: "#f59e0b" },
      { name: "In Surgery", value: inSurgery, color: "#ef4444" },
      { name: "Offline", value: offline, color: "#94a3b8" },
    ]
  }, [doctors])

  const appointmentsStatusData = useMemo(() => {
    const map = new Map<string, number>()

    appointments.forEach((item) => {
      const key = item.status || "Unknown"
      map.set(key, (map.get(key) ?? 0) + 1)
    })

    return Array.from(map.entries()).map(([name, value], index) => ({
      name,
      value,
      color: ["#3b82f6", "#f59e0b", "#22c55e", "#94a3b8", "#a855f7"][index % 5],
    }))
  }, [appointments])

  const reportsStatusData = useMemo(() => {
    const map = new Map<string, number>()

    reports.forEach((item) => {
      const key = item.status || "Unknown"
      map.set(key, (map.get(key) ?? 0) + 1)
    })

    return Array.from(map.entries()).map(([name, value], index) => ({
      name,
      value,
      color: ["#8b5cf6", "#06b6d4", "#22c55e", "#f97316", "#94a3b8"][index % 5],
    }))
  }, [reports])

  const topSpecialties = useMemo(() => {
    return [...specialties]
      .sort((a, b) => b.activeCases - a.activeCases)
      .slice(0, 4)
  }, [specialties])

  return (
    <div style={{ padding: 24, color: "#e5eef8" }}>
      <div style={{ marginBottom: 22 }}>
        <div style={{ fontSize: 32, fontWeight: 800, marginBottom: 6 }}>
          Admin Overview
        </div>
        <div style={{ opacity: 0.8 }}>
          Executive hospital summary across doctors, specialties, patients, appointments, and reports
        </div>
      </div>

      {error && <div style={{ color: "#fecaca", marginBottom: 16 }}>{error}</div>}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
          gap: 16,
          marginBottom: 20,
        }}
      >
        <StatCard title="Doctors" value={loading ? "..." : String(doctors.length)} tone="#17212f" text="#ffffff" />
        <StatCard title="Specialties" value={loading ? "..." : String(specialties.length)} tone="#e0f2fe" text="#0f172a" />
        <StatCard title="Patients" value={loading ? "..." : String(patientsCount)} tone="#dcfce7" text="#0f172a" />
        <StatCard title="Appointments" value={loading ? "..." : String(appointments.length)} tone="#fef3c7" text="#0f172a" />
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
          gap: 16,
          marginBottom: 24,
        }}
      >
        <StatCard title="Reports" value={loading ? "..." : String(reports.length)} tone="#ede9fe" text="#0f172a" />
        <StatCard title="Assigned Patients" value={loading ? "..." : String(assignedPatientsCount)} tone="#fee2e2" text="#0f172a" />
        <StatCard title="Available Doctors" value={loading ? "..." : String(availableDoctors)} tone="#d1fae5" text="#0f172a" />
        <StatCard title="On Call / Busy" value={loading ? "..." : `${onCallDoctors} / ${busyDoctors}`} tone="#f8fafc" text="#0f172a" />
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1.25fr 1fr",
          gap: 20,
          marginBottom: 20,
        }}
      >
        <Panel title="Doctors by Specialty Chart">
          <div style={{ width: "100%", height: 320 }}>
            {!loading && specialtyBreakdown.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={specialtyBreakdown}>
                  <XAxis dataKey="name" tick={{ fill: "#475569", fontSize: 12 }} />
                  <YAxis tick={{ fill: "#475569", fontSize: 12 }} />
                  <Tooltip />
                  <Bar dataKey="count" radius={[8, 8, 0, 0]} fill="#60a5fa" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <CenteredState loading={loading} emptyText="No chart data available." />
            )}
          </div>
        </Panel>

        <Panel title="Doctor Status Distribution">
          <div style={{ width: "100%", height: 320 }}>
            {!loading && doctorStatusData.some((item) => item.value > 0) ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={doctorStatusData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={95}
                    innerRadius={55}
                    paddingAngle={3}
                  >
                    {doctorStatusData.map((entry) => (
                      <Cell key={entry.name} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <CenteredState loading={loading} emptyText="No status data available." />
            )}
          </div>

          <div style={{ display: "grid", gap: 10, marginTop: 10 }}>
            {doctorStatusData.map((item) => (
              <LegendRow key={item.name} color={item.color} name={item.name} value={item.value} />
            ))}
          </div>
        </Panel>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 20,
          marginBottom: 20,
        }}
      >
        <Panel title="Appointments Status Breakdown">
          <div style={{ width: "100%", height: 300 }}>
            {!loading && appointmentsStatusData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={appointmentsStatusData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={95}
                    innerRadius={52}
                    paddingAngle={3}
                  >
                    {appointmentsStatusData.map((entry) => (
                      <Cell key={entry.name} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <CenteredState loading={loading} emptyText="No appointment status data." />
            )}
          </div>

          <div style={{ display: "grid", gap: 10, marginTop: 10 }}>
            {appointmentsStatusData.map((item) => (
              <LegendRow key={item.name} color={item.color} name={item.name} value={item.value} />
            ))}
          </div>
        </Panel>

        <Panel title="Reports Status Breakdown">
          <div style={{ width: "100%", height: 300 }}>
            {!loading && reportsStatusData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={reportsStatusData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={95}
                    innerRadius={52}
                    paddingAngle={3}
                  >
                    {reportsStatusData.map((entry) => (
                      <Cell key={entry.name} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <CenteredState loading={loading} emptyText="No report status data." />
            )}
          </div>

          <div style={{ display: "grid", gap: 10, marginTop: 10 }}>
            {reportsStatusData.map((item) => (
              <LegendRow key={item.name} color={item.color} name={item.name} value={item.value} />
            ))}
          </div>
        </Panel>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1.2fr 1fr",
          gap: 20,
        }}
      >
        <div style={{ display: "grid", gap: 20 }}>
          <Panel title="Doctors by Specialty">
            {loading ? (
              <div>Loading...</div>
            ) : specialtyBreakdown.length === 0 ? (
              <div>No specialty data found.</div>
            ) : (
              <div style={{ display: "grid", gap: 10 }}>
                {specialtyBreakdown.map((item) => (
                  <div
                    key={item.name}
                    style={{
                      background: "white",
                      border: "1px solid #e2e8f0",
                      borderRadius: 16,
                      padding: 14,
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      gap: 12,
                    }}
                  >
                    <div style={{ fontWeight: 800 }}>{item.name}</div>
                    <div
                      style={{
                        background: "#eff6ff",
                        color: "#1d4ed8",
                        borderRadius: 999,
                        padding: "6px 10px",
                        fontWeight: 800,
                        fontSize: 12,
                      }}
                    >
                      {item.count} doctors
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Panel>

          <Panel title="Top Active Specialties">
            {loading ? (
              <div>Loading...</div>
            ) : topSpecialties.length === 0 ? (
              <div>No specialty activity found.</div>
            ) : (
              <div style={{ display: "grid", gap: 12 }}>
                {topSpecialties.map((item) => (
                  <div
                    key={item.title}
                    style={{
                      background: "white",
                      border: "1px solid #e2e8f0",
                      borderRadius: 18,
                      padding: 16,
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        gap: 12,
                        alignItems: "center",
                        marginBottom: 8,
                      }}
                    >
                      <div style={{ fontWeight: 800, fontSize: 17 }}>
                        {item.icon} {item.title}
                      </div>
                      <div
                        style={{
                          background: "#ecfeff",
                          color: "#0f766e",
                          borderRadius: 999,
                          padding: "6px 10px",
                          fontWeight: 800,
                          fontSize: 12,
                        }}
                      >
                        {item.activeCases} active cases
                      </div>
                    </div>

                    <div style={{ color: "#64748b", marginBottom: 10 }}>
                      {item.subtitle}
                    </div>

                    <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
                      <Badge text={`${item.doctors} doctors`} tone="#eff6ff" color="#1d4ed8" />
                      <Badge text={item.route} tone="#f8fafc" color="#334155" />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Panel>
        </div>

        <div style={{ display: "grid", gap: 20 }}>
          <Panel title="System Status">
            <div style={{ display: "grid", gap: 12 }}>
              <StatusRow label="Doctors Service" value="Operational" tone="#dcfce7" color="#166534" />
              <StatusRow label="Specialties Data" value="Synced" tone="#dbeafe" color="#1d4ed8" />
              <StatusRow label="Appointments" value="Live" tone="#fef3c7" color="#92400e" />
              <StatusRow label="Reports" value="Available" tone="#ede9fe" color="#6d28d9" />
              <StatusRow label="Assignments" value="Tracked" tone="#ecfeff" color="#0f766e" />
            </div>
          </Panel>

          <Panel title="Hospital Snapshot">
            <div style={{ display: "grid", gap: 12 }}>
              <SnapshotCard title="Average Appointments per Doctor" value={loading || doctors.length === 0 ? "..." : (appointments.length / doctors.length).toFixed(1)} />
              <SnapshotCard title="Average Assigned Patients per Doctor" value={loading || doctors.length === 0 ? "..." : (assignedPatientsCount / doctors.length).toFixed(1)} />
              <SnapshotCard title="Reports per Patient Ratio" value={loading || patientsCount === 0 ? "..." : (reports.length / patientsCount).toFixed(2)} />
            </div>
          </Panel>
        </div>
      </div>
    </div>
  )
}

function CenteredState({
  loading,
  emptyText,
}: {
  loading: boolean
  emptyText: string
}) {
  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        color: "#64748b",
        fontWeight: 600,
      }}
    >
      {loading ? "Loading..." : emptyText}
    </div>
  )
}

function LegendRow({
  color,
  name,
  value,
}: {
  color: string
  name: string
  value: number
}) {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        gap: 12,
        alignItems: "center",
        background: "white",
        border: "1px solid #e2e8f0",
        borderRadius: 14,
        padding: "10px 12px",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <span
          style={{
            width: 12,
            height: 12,
            borderRadius: 999,
            background: color,
            display: "inline-block",
          }}
        />
        <span style={{ fontWeight: 700 }}>{name}</span>
      </div>
      <span style={{ fontWeight: 800 }}>{value}</span>
    </div>
  )
}

function Panel({
  title,
  children,
}: {
  title: string
  children: React.ReactNode
}) {
  return (
    <div
      style={{
        background: "#f8fafc",
        color: "#0f172a",
        borderRadius: 26,
        padding: 22,
        boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
      }}
    >
      <div style={{ fontSize: 18, fontWeight: 800, marginBottom: 14 }}>
        {title}
      </div>
      {children}
    </div>
  )
}

function StatCard({
  title,
  value,
  tone,
  text,
}: {
  title: string
  value: string
  tone: string
  text: string
}) {
  return (
    <div
      style={{
        background: tone,
        color: text,
        borderRadius: 22,
        padding: 20,
        minHeight: 118,
        boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
      }}
    >
      <div style={{ opacity: 0.8, marginBottom: 18 }}>{title}</div>
      <div style={{ fontSize: 34, fontWeight: 800 }}>{value}</div>
    </div>
  )
}

function Badge({
  text,
  tone,
  color,
}: {
  text: string
  tone: string
  color: string
}) {
  return (
    <div
      style={{
        background: tone,
        color,
        borderRadius: 999,
        padding: "8px 12px",
        fontWeight: 700,
        fontSize: 13,
      }}
    >
      {text}
    </div>
  )
}

function StatusRow({
  label,
  value,
  tone,
  color,
}: {
  label: string
  value: string
  tone: string
  color: string
}) {
  return (
    <div
      style={{
        background: "white",
        border: "1px solid #e2e8f0",
        borderRadius: 16,
        padding: 14,
        display: "flex",
        justifyContent: "space-between",
        gap: 12,
        alignItems: "center",
      }}
    >
      <div style={{ fontWeight: 700 }}>{label}</div>
      <div
        style={{
          background: tone,
          color,
          borderRadius: 999,
          padding: "6px 10px",
          fontWeight: 800,
          fontSize: 12,
        }}
      >
        {value}
      </div>
    </div>
  )
}

function SnapshotCard({
  title,
  value,
}: {
  title: string
  value: string
}) {
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
      <div style={{ fontSize: 28, fontWeight: 800 }}>{value}</div>
    </div>
  )
}
