import { useEffect, useState } from "react"
import { apiGet } from "@/lib/api"
import * as Sentry from "@sentry/react"

type Patient = {
  id: string
  name: string
}

type Appointment = {
  id: string
  patient: string
  status: string
}

type Report = {
  id: string
  title: string
  status: string
}

export default function Dashboard() {
  const [patientsCount, setPatientsCount] = useState(0)
  const [appointmentsCount, setAppointmentsCount] = useState(0)
  const [reportsCount, setReportsCount] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [patients, appointments, reports] = await Promise.all([
          apiGet<Patient[]>("/patients"),
          apiGet<Appointment[]>("/appointments"),
          apiGet<Report[]>("/reports"),
        ])

        setPatientsCount(Array.isArray(patients) ? patients.length : 0)
        setAppointmentsCount(Array.isArray(appointments) ? appointments.length : 0)
        setReportsCount(Array.isArray(reports) ? reports.length : 0)
      } catch (err) {
        console.error(err)
        setError("Failed to load dashboard data")
      } finally {
        setLoading(false)
      }
    }

    loadDashboard()
  }, [])

  return (
    <div style={{ padding: "24px", color: "white" }}>
      <h1 style={{ fontSize: "30px", marginBottom: "8px" }}>Smart Hospital Dashboard</h1>
      <p style={{ opacity: 0.8, marginBottom: "20px" }}>
        Welcome, System Admin — Admin
      </p>

      {error && <div style={{ color: "#fca5a5", marginBottom: "16px" }}>{error}</div>}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(260px,1fr))",
          gap: "16px",
        }}
      >
        <StatCard
          title="Patients"
          value={loading ? "..." : String(patientsCount)}
        />
        <StatCard
          title="Appointments"
          value={loading ? "..." : String(appointmentsCount)}
        />
        <StatCard
          title="Pending Reports"
          value={loading ? "..." : String(reportsCount)}
        />
      </div>
    </div>
  )
}

function StatCard({ title, value }: { title: string; value: string }) {
  return (
    <div
      style={{
        background: "#111827",
        border: "1px solid #374151",
        borderRadius: "14px",
        padding: "22px",
        minHeight: "140px",
      }}
    >
      <div style={{ opacity: 0.8, marginBottom: "18px" }}>{title}</div>
      <div style={{ fontSize: "42px", fontWeight: 700 }}>{value}</div>
    
      <button onClick={() => Sentry.captureException(new Error("Dashboard test"))}>Test Sentry</button>
</div>
  )
}