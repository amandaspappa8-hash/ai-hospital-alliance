import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { getSpecialtiesSummary, type SpecialtyRecord } from "@/lib/specialties"

export default function SpecialtiesPage() {
  const navigate = useNavigate()
  const [specialties, setSpecialties] = useState<SpecialtyRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    async function load() {
      try {
        setLoading(true)
        setError("")
        const data = await getSpecialtiesSummary()
        setSpecialties(data)
      } catch (err) {
        console.error(err)
        setError("Failed to load specialties")
        setSpecialties([])
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [])

  return (
    <div style={{ padding: 24, color: "#e5eef8" }}>
      <div style={{ marginBottom: 22 }}>
        <div style={{ fontSize: 32, fontWeight: 800, marginBottom: 6 }}>
          Medical Specialties
        </div>
        <div style={{ opacity: 0.8 }}>
          Explore hospital departments and open each specialty dashboard
        </div>
      </div>

      {error && <div style={{ color: "#fecaca", marginBottom: 16 }}>{error}</div>}
      {loading && <div style={{ marginBottom: 16 }}>Loading specialties...</div>}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
          gap: 18,
        }}
      >
        {specialties.map((item) => (
          <button
            key={item.title}
            onClick={() => navigate(item.route)}
            style={{
              textAlign: "left",
              background: "#f8fafc",
              color: "#0f172a",
              border: "1px solid #e2e8f0",
              borderRadius: 24,
              padding: 22,
              cursor: "pointer",
              boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
            }}
          >
            <div
              style={{
                width: 64,
                height: 64,
                borderRadius: 18,
                background: item.tone,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 28,
                marginBottom: 18,
              }}
            >
              {item.icon}
            </div>

            <div style={{ fontSize: 22, fontWeight: 800, marginBottom: 8 }}>
              {item.title}
            </div>

            <div
              style={{
                color: "#64748b",
                lineHeight: 1.6,
                marginBottom: 16,
                minHeight: 50,
              }}
            >
              {item.subtitle}
            </div>

            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                gap: 10,
                flexWrap: "wrap",
              }}
            >
              <div
                style={{
                  background: "#eff6ff",
                  color: "#1d4ed8",
                  borderRadius: 999,
                  padding: "8px 12px",
                  fontWeight: 700,
                  fontSize: 13,
                }}
              >
                {item.doctors} doctors
              </div>

              <div
                style={{
                  background: "#ecfeff",
                  color: "#0f766e",
                  borderRadius: 999,
                  padding: "8px 12px",
                  fontWeight: 700,
                  fontSize: 13,
                }}
              >
                {item.activeCases} active cases
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}
