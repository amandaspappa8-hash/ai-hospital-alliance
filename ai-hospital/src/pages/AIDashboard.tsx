import { useEffect, useState } from "react";
import { apiGet } from "../lib-api";

type Patient = {
  id: string;
  name: string;
  status?: string;
};

const card = {
  background: "white",
  padding: 20,
  borderRadius: 18,
  boxShadow: "0 4px 16px rgba(0,0,0,0.06)"
};

export default function AIDashboard() {
  const [patients, setPatients] = useState<Patient[]>([]);

  useEffect(() => {
    apiGet<Patient[]>("/patients")
      .then(setPatients)
      .catch(console.error);
  }, []);

  const critical = patients.filter(p => p.status === "Critical");
  const stable = patients.filter(p => p.status === "Stable");

  return (
    <div>
      <h1 style={{ fontSize: 32 }}>AI Triage Dashboard</h1>
      <p style={{ color: "#64748b", marginBottom: 20 }}>
        Real-time patient risk prioritization.
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        <div style={card}>
          <h3 style={{ color: "#dc2626" }}>Critical Patients</h3>
          {critical.map(p => (
            <p key={p.id}>⚠️ {p.name}</p>
          ))}
        </div>

        <div style={card}>
          <h3 style={{ color: "#16a34a" }}>Stable Patients</h3>
          {stable.map(p => (
            <p key={p.id}>✅ {p.name}</p>
          ))}
        </div>
      </div>
    </div>
  );
}
