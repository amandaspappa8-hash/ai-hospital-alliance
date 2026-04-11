import { useEffect, useMemo, useState } from "react"
import { useNavigate } from "react-router-dom"
import { getDoctorsSummary, type DoctorRecord } from "@/lib/doctors"

function statusColor(status: DoctorRecord["status"]) {
  if (status === "Available") return { bg: "#dcfce7", color: "#166534" }
  if (status === "On Call") return { bg: "#fef3c7", color: "#92400e" }
  if (status === "In Surgery") return { bg: "#fee2e2", color: "#991b1b" }
  return { bg: "#e5e7eb", color: "#374151" }
}

export default function DoctorsPage() {
  const navigate = useNavigate()
  const [doctors, setDoctors] = useState<DoctorRecord[]>([])
  const [query, setQuery] = useState("")
  const [specialty, setSpecialty] = useState("All")
  const [selectedDoctorId, setSelectedDoctorId] = useState("")
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    async function loadDoctors() {
      try {
        setLoading(true)
        setError("")
        const data = await getDoctorsSummary()
        setDoctors(data)
        if (data.length > 0) {
          setSelectedDoctorId(data[0].id)
        }
      } catch (err) {
        console.error(err)
        setError("Failed to load doctors")
        setDoctors([])
      } finally {
        setLoading(false)
      }
    }

    loadDoctors()
  }, [])

  const specialties = useMemo(() => {
    const values = Array.from(new Set(doctors.map((d) => d.specialty)))
    return ["All", ...values]
  }, [doctors])

  const filteredDoctors = useMemo(() => {
    const q = query.trim().toLowerCase()

    return doctors.filter((doctor) => {
      const matchesQuery =
        !q ||
        doctor.name.toLowerCase().includes(q) ||
        doctor.specialty.toLowerCase().includes(q) ||
        doctor.department.toLowerCase().includes(q)

      const matchesSpecialty =
        specialty === "All" || doctor.specialty === specialty

      return matchesQuery && matchesSpecialty
    })
  }, [doctors, query, specialty])

  const selectedDoctor =
    filteredDoctors.find((doctor) => doctor.id === selectedDoctorId) ||
    doctors.find((doctor) => doctor.id === selectedDoctorId) ||
    filteredDoctors[0] ||
    null

  const availableCount = doctors.filter((d) => d.status === "Available").length
  const totalPatients = doctors.reduce((sum, d) => sum + d.patients, 0)
  const avgRating = doctors.length
    ? (doctors.reduce((sum, d) => sum + d.rating, 0) / doctors.length).toFixed(1)
    : "0.0"

  return (
    <div style={{ padding: 24, color: "#e5eef8" }}>
      <div style={{ marginBottom: 22 }}>
        <div style={{ fontSize: 32, fontWeight: 800, marginBottom: 6 }}>
          Doctors & Specialties
        </div>
        <div style={{ opacity: 0.8 }}>
          Smart clinical workforce dashboard for all departments
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
        <TopStatCard title="Total Doctors" value={loading ? "..." : String(doctors.length)} tone="dark" />
        <TopStatCard title="Available Now" value={loading ? "..." : String(availableCount)} tone="green" />
        <TopStatCard title="Patients Today" value={loading ? "..." : String(totalPatients)} tone="blue" />
        <TopStatCard title="Average Rating" value={loading ? "..." : String(avgRating)} tone="light" />
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "2fr 1fr",
          gap: 18,
          marginBottom: 18,
        }}
      >
        <div
          style={{
            background: "#f8fafc",
            borderRadius: 26,
            padding: 24,
            color: "#0f172a",
            boxShadow: "0 10px 30px rgba(15, 23, 42, 0.10)",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              gap: 14,
              flexWrap: "wrap",
              marginBottom: 20,
            }}
          >
            <div>
              <div style={{ fontSize: 18, fontWeight: 800 }}>Doctor Directory</div>
              <div style={{ color: "#64748b", marginTop: 4 }}>
                Search doctors by name, specialty, or department
              </div>
            </div>

            <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search doctor..."
                style={{
                  padding: "12px 14px",
                  borderRadius: 14,
                  border: "1px solid #dbeafe",
                  minWidth: 220,
                  background: "white",
                }}
              />
              <select
                value={specialty}
                onChange={(e) => setSpecialty(e.target.value)}
                style={{
                  padding: "12px 14px",
                  borderRadius: 14,
                  border: "1px solid #dbeafe",
                  minWidth: 180,
                  background: "white",
                }}
              >
                {specialties.map((item) => (
                  <option key={item}>{item}</option>
                ))}
              </select>
            </div>
          </div>

          <div style={{ display: "grid", gap: 12 }}>
            {loading ? (
              <div>Loading doctors...</div>
            ) : filteredDoctors.length === 0 ? (
              <div>No doctors found.</div>
            ) : (
              filteredDoctors.map((doctor) => {
                const tone = statusColor(doctor.status)
                const active = selectedDoctor?.id === doctor.id

                return (
                  <button
                    key={doctor.id}
                    onClick={() => setSelectedDoctorId(doctor.id)}
                    style={{
                      textAlign: "left",
                      width: "100%",
                      border: active ? "2px solid #93c5fd" : "1px solid #e2e8f0",
                      background: active ? "#eff6ff" : "white",
                      borderRadius: 18,
                      padding: 16,
                      cursor: "pointer",
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
                          Experience: {doctor.experience} • Patients today: {doctor.patients}
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
                  </button>
                )
              })
            )}
          </div>
        </div>

        <div
          style={{
            background: "#f8fafc",
            borderRadius: 26,
            padding: 20,
            color: "#0f172a",
            boxShadow: "0 10px 30px rgba(15, 23, 42, 0.10)",
          }}
        >
          <div style={{ fontSize: 18, fontWeight: 800, marginBottom: 14 }}>
            Featured Doctor
          </div>

          {!selectedDoctor ? (
            <div>No doctor selected.</div>
          ) : (
            <>
              <div
                style={{
                  background: "#eaffd0",
                  borderRadius: 22,
                  padding: 18,
                  marginBottom: 16,
                }}
              >
                <div
                  style={{
                    width: 140,
                    height: 140,
                    borderRadius: 24,
                    background: "white",
                    margin: "0 auto 16px auto",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 42,
                    fontWeight: 800,
                    color: "#0f172a",
                    border: "1px solid #d9f99d",
                  }}
                >
                  {selectedDoctor.name
                    .split(" ")
                    .slice(0, 2)
                    .map((p) => p[0])
                    .join("")}
                </div>

                <div style={{ textAlign: "center", fontWeight: 800, fontSize: 24 }}>
                  {selectedDoctor.name}
                </div>
                <div style={{ textAlign: "center", color: "#3f6212", marginTop: 6 }}>
                  {selectedDoctor.specialty}
                </div>
              </div>

              <div
                style={{
                  background: "white",
                  border: "1px solid #e2e8f0",
                  borderRadius: 18,
                  padding: 16,
                  display: "grid",
                  gap: 10,
                  marginBottom: 14,
                }}
              >
                <InfoRow label="Department" value={selectedDoctor.department} />
                <InfoRow label="Experience" value={selectedDoctor.experience} />
                <InfoRow label="Schedule" value={selectedDoctor.schedule} />
                <InfoRow label="Phone" value={selectedDoctor.phone} />
                <InfoRow label="Patients Today" value={String(selectedDoctor.patients)} />
                <InfoRow label="Rating" value={`⭐ ${selectedDoctor.rating}`} />
              </div>

              <button
                onClick={() => navigate(`/doctors/${selectedDoctor.id}`)}
                style={{
                  width: "100%",
                  padding: "14px 16px",
                  borderRadius: 999,
                  border: "none",
                  background: "#0f172a",
                  color: "white",
                  fontWeight: 800,
                  cursor: "pointer",
                }}
              >
                View Doctor Profile
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

function TopStatCard({
  title,
  value,
  tone,
}: {
  title: string
  value: string
  tone: "dark" | "green" | "blue" | "light"
}) {
  const styles =
    tone === "dark"
      ? { bg: "#17212f", color: "#ffffff", sub: "#cbd5e1" }
      : tone === "green"
        ? { bg: "#eaffd0", color: "#1f2937", sub: "#4b5563" }
        : tone === "blue"
          ? { bg: "#dff4ff", color: "#1f2937", sub: "#4b5563" }
          : { bg: "#f8fafc", color: "#1f2937", sub: "#64748b" }

  return (
    <div
      style={{
        background: styles.bg,
        color: styles.color,
        borderRadius: 22,
        padding: 20,
        minHeight: 120,
        boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
      }}
    >
      <div style={{ color: styles.sub, marginBottom: 18 }}>{title}</div>
      <div style={{ fontSize: 34, fontWeight: 800 }}>{value}</div>
    </div>
  )
}

function InfoRow({ label, value }: { label: string; value: string }) {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        gap: 14,
        borderBottom: "1px solid #f1f5f9",
        paddingBottom: 8,
      }}
    >
      <div style={{ color: "#64748b" }}>{label}</div>
      <div style={{ fontWeight: 700, textAlign: "right" }}>{value}</div>
    </div>
  )
}
