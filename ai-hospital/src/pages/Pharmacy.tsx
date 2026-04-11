import { useEffect, useState } from "react";
import { apiGet, apiPost } from "../lib-api";

type Patient = {
  id: string;
  name: string;
};

type MarItem = {
  medication?: string;
  dose?: string;
  status?: string;
  time?: string;
  pharmacy_review?: string;
  ai_flag?: string;
};

const cardStyle: React.CSSProperties = {
  background: "white",
  borderRadius: 18,
  padding: 20,
  boxShadow: "0 4px 16px rgba(0,0,0,0.06)",
};

export default function Pharmacy() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [selectedPatient, setSelectedPatient] = useState("P-1001");
  const [mar, setMar] = useState<MarItem[]>([]);

  async function loadData(patientId: string) {
    const [patientsData, marData] = await Promise.all([
      apiGet<Patient[]>("/patients"),
      apiGet<MarItem[]>(`/mar/${patientId}`)
    ]);

    setPatients(Array.isArray(patientsData) ? patientsData : []);
    setMar(Array.isArray(marData) ? marData : []);
  }

  useEffect(() => {
    loadData(selectedPatient).catch(console.error);
  }, [selectedPatient]);

  async function reviewItem(index: number, medication?: string) {
    const med = (medication || "").toLowerCase();
    const aiFlag = med.includes("warfarin") ? "High Risk" : "Safe";

    await apiPost(`/mar/${selectedPatient}/${index}/pharmacy-review`, {
      pharmacy_review: "Reviewed by Pharmacy",
      ai_flag: aiFlag
    });

    await loadData(selectedPatient);
  }

  return (
    <div>
      <h1 style={{ fontSize: 30, marginBottom: 8, color: "#0f172a" }}>Pharmacy AI Review</h1>
      <p style={{ color: "#64748b", marginBottom: 20 }}>
        Pharmacy verification and AI medication review workflow.
      </p>

      <div style={{ ...cardStyle, marginBottom: 20 }}>
        <label>Select Patient:</label>
        <select
          value={selectedPatient}
          onChange={(e) => setSelectedPatient(e.target.value)}
          style={{ marginLeft: 10, padding: 8, borderRadius: 8 }}
        >
          {patients.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name} ({p.id})
            </option>
          ))}
        </select>
      </div>

      <div style={cardStyle}>
        <h3>MAR Items for Pharmacy Review</h3>
        {mar.length === 0 ? (
          <p>No MAR items.</p>
        ) : (
          mar.map((item, i) => (
            <div key={i} style={{ background: "#f8fafc", padding: 12, borderRadius: 12, marginBottom: 10 }}>
              <p><b>Medication:</b> {item.medication ?? "-"}</p>
              <p><b>Dose:</b> {item.dose ?? "-"}</p>
              <p><b>Status:</b> {item.status ?? "-"}</p>
              <p><b>Review:</b> {item.pharmacy_review ?? "-"}</p>
              <p><b>AI Flag:</b> {item.ai_flag ?? "-"}</p>
              {!item.pharmacy_review && (
                <button onClick={() => reviewItem(i, item.medication)} style={{ padding: 8 }}>
                  Review with AI
                </button>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
