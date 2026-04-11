import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiGet } from "../lib-api";

type Patient = {
  id: string;
  name: string;
  age?: number;
  gender?: string;
  status?: string;
};

const cardStyle: React.CSSProperties = {
  background: "white",
  borderRadius: 18,
  padding: 20,
  boxShadow: "0 4px 16px rgba(0,0,0,0.06)",
  cursor: "pointer",
};

export default function Patients() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    apiGet<Patient[]>("/patients")
      .then((data) => setPatients(Array.isArray(data) ? data : []))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <h1 style={{ fontSize: 30, marginBottom: 8, color: "#0f172a" }}>Patients</h1>
      <p style={{ color: "#64748b", marginBottom: 20 }}>
        Live patient directory connected to the clinical backend.
      </p>

      {loading && <p>Loading patients...</p>}

      <div style={{ display: "grid", gap: 14 }}>
        {patients.map((patient) => (
          <div
            key={patient.id}
            style={cardStyle}
            onClick={() => navigate(`/patients/${patient.id}`)}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <h3 style={{ margin: 0 }}>{patient.name}</h3>
                <p style={{ margin: "8px 0", color: "#475569" }}>ID: {patient.id}</p>
              </div>

              <div
                style={{
                  padding: "8px 12px",
                  borderRadius: 999,
                  fontWeight: 700,
                  background:
                    patient.status === "Critical"
                      ? "#fef2f2"
                      : patient.status === "Stable"
                      ? "#f0fdf4"
                      : "#fff7ed",
                  color:
                    patient.status === "Critical"
                      ? "#dc2626"
                      : patient.status === "Stable"
                      ? "#16a34a"
                      : "#d97706",
                }}
              >
                {patient.status ?? "Unknown"}
              </div>
            </div>

            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
                gap: 12,
                marginTop: 16,
              }}
            >
              <div style={{ background: "#f8fafc", borderRadius: 12, padding: 12 }}>
                <div style={{ color: "#64748b", fontSize: 13 }}>Age</div>
                <div style={{ fontWeight: 700 }}>{patient.age ?? "-"}</div>
              </div>
              <div style={{ background: "#f8fafc", borderRadius: 12, padding: 12 }}>
                <div style={{ color: "#64748b", fontSize: 13 }}>Gender</div>
                <div style={{ fontWeight: 700 }}>{patient.gender ?? "-"}</div>
              </div>
              <div style={{ background: "#eff6ff", borderRadius: 12, padding: 12 }}>
                <div style={{ color: "#1d4ed8", fontSize: 13 }}>Action</div>
                <div style={{ fontWeight: 700, color: "#0f172a" }}>
                  Open full chart
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
