import { useEffect, useMemo, useState } from "react"
import { getDoctorsBySpecialty, type DoctorRecord } from "@/lib/doctors"

type Props = {
  title: string
  icon: string
  description: string
  specialtyName: string
}

function statusColor(status: DoctorRecord["status"]) {
  if (status === "Available") return { bg: "#dcfce7", color: "#166534" }
  if (status === "On Call") return { bg: "#fef3c7", color: "#92400e" }
  if (status === "In Surgery") return { bg: "#fee2e2", color: "#991b1b" }
  return { bg: "#e5e7eb", color: "#374151" }
}

export default function SpecialtyDoctorsView({
  title,
  icon,
  description,
  specialtyName,
}: Props) {
  const [doctors, setDoctors] = useState<DoctorRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    async function loadDoctors() {
      try {
        setLoading(true)
        setError("")
        const data = await getDoctorsBySpecialty(specialtyName)
        setDoctors(data)
      } catch (err) {
        console.error(err)
        setError(`Failed to load ${specialtyName} doctors`)
        setDoctors([])
      } finally {
        setLoading(false)
      }
    }

    loadDoctors()
  }, [specialtyName])

  const availableCount = useMemo(
    () => doctors.filter((d) => d.status === "Available").length,
    [doctors]
  )

  const totalPatients = useMemo(
    () => doctors.reduce((sum, d) => sum + d.patients, 0),
    [doctors]
  )

  const avgRating = useMemo(() => {
    if (doctors.length === 0) return "0.0"
    return (doctors.reduce((sum, d) => sum + d.rating, 0) / doctors.length).toFixed(1)
  }, [doctors])

  return (
    <div style={{ padding: 24, color: "#e5eef8" }}>
      <div
        style={{
          background: "#f8fafc",
          color: "#0f172a",
          borderRadius: 26,
          padding: 24,
          boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
        }}
      >
        <div style={{ fontSize: 44, marginBottom: 12 }}>{icon}</div>
        <div style={{ fontSize: 32, fontWeight: 800, marginBottom: 10 }}>{title}</div>
        <div style={{ color: "#64748b", marginBottom: 24 }}>{description}</div>

        {error && (
          <div style={{ color: "#b91c1c", marginBottom: 16 }}>{error}</div>
        )}

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
            gap: 16,
            marginBottom: 22,
          }}
        >
          <MiniCard title="Doctors" value={loading ? "..." : String(doctors.length)} />
          <MiniCard title="Available Now" value={loading ? "..." : String(availableCount)} />
          <MiniCard title="Patients Today" value={loading ? "..." : String(totalPatients)} />
          <MiniCard title="Average Rating" value={loading ? "..." : avgRating} />
        </div>

        <div
          style={{
            background: "white",
            border: "1px solid #e2e8f0",
            borderRadius: 22,
            padding: 18,
          }}
        >
          <div style={{ fontSize: 20, fontWeight: 800, marginBottom: 14 }}>
            {title} Doctors
          </div>

          {loading ? (
            <div>Loading doctors...</div>
          ) : doctors.length === 0 ? (
            <div>No doctors found for this specialty.</div>
          ) : (
            <div style={{ display: "grid", gap: 12 }}>
              {doctors.map((doctor) => {
                const tone = statusColor(doctor.status)

                return (
                  <div
                    key={doctor.id}
                    style={{
                      border: "1px solid #e2e8f0",
                      background: "#ffffff",
                      borderRadius: 18,
                      padding: 16,
                    }}
                  >
                    <div
                      style={{
                        display: "grid",
                        gridTemplateColumns: "64px 1fr auto",
                        alignItems: "center",
                        gap: 14,
                      }}
                    >
                      <div
                        style={{
                          width: 64,
                          height: 64,
                          borderRadius: "50%",
                          background: "#dbeafe",
                          color: "#1d4ed8",
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                          fontWeight: 800,
                          fontSize: 22,
                        }}
                      >
                        {doctor.name
                          .split(" ")
                          .slice(0, 2)
                          .map((p) => p[0])
                          .join("")}
                      </div>

                      <div>
                        <div style={{ fontWeight: 800, fontSize: 17 }}>{doctor.name}</div>
                        <div style={{ color: "#475569", marginTop: 4 }}>
                          {doctor.specialty} • {doctor.department}
                        </div>
                        <div style={{ color: "#64748b", marginTop: 6, fontSize: 13 }}>
                          Experience: {doctor.experience} • Schedule: {doctor.schedule}
                        </div>
                        <div style={{ color: "#64748b", marginTop: 4, fontSize: 13 }}>
                          Phone: {doctor.phone} • Patients today: {doctor.patients}
                        </div>
                      </div>

                      <div style={{ textAlign: "right" }}>
                        <div
                          style={{
                            display: "inline-block",
                            background: tone.bg,
                            color: tone.color,
                            padding: "6px 10px",
                            borderRadius: 999,
                            fontWeight: 800,
                            fontSize: 12,
                            marginBottom: 10,
                          }}
                        >
                          {doctor.status}
                        </div>
                        <div style={{ color: "#0f172a", fontWeight: 700 }}>
                          ⭐ {doctor.rating}
                        </div>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function MiniCard({ title, value }: { title: string; value: string }) {
  return (
    <div
      style={{
        background: "white",
        border: "1px solid #e2e8f0",
        borderRadius: 18,
        padding: 18,
      }}
    >
      <div style={{ color: "#64748b", marginBottom: 10 }}>{title}</div>
      <div style={{ fontSize: 28, fontWeight: 800 }}>{value}</div>
    </div>
  )
}
