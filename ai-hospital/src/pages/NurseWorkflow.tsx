import { useEffect, useState } from "react";
import { apiGet, apiPost } from "../lib-api";

type Patient = {
  id: string;
  name: string;
};

type Vital = {
  bp?: string;
  hr?: number;
  temp?: number;
  spo2?: number;
  date?: string;
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

export default function NurseWorkflow() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [selectedPatient, setSelectedPatient] = useState("P-1001");
  const [vitals, setVitals] = useState<Vital[]>([]);
  const [mar, setMar] = useState<MarItem[]>([]);

  const [bp, setBp] = useState("");
  const [hr, setHr] = useState("");
  const [temp, setTemp] = useState("");
  const [spo2, setSpo2] = useState("");

  async function loadData(patientId: string) {
    const [patientsData, vitalsData, marData] = await Promise.all([
      apiGet<Patient[]>("/patients"),
      apiGet<Vital[]>(`/nursing/vitals/${patientId}`),
      apiGet<MarItem[]>(`/mar/${patientId}`)
    ]);

    setPatients(Array.isArray(patientsData) ? patientsData : []);
    setVitals(Array.isArray(vitalsData) ? vitalsData : []);
    setMar(Array.isArray(marData) ? marData : []);
  }

  useEffect(() => {
    loadData(selectedPatient).catch(console.error);
  }, [selectedPatient]);

  async function addVitals() {
    await apiPost(`/nursing/vitals/${selectedPatient}`, {
      bp,
      hr: hr ? Number(hr) : undefined,
      temp: temp ? Number(temp) : undefined,
      spo2: spo2 ? Number(spo2) : undefined,
      date: new Date().toISOString(),
    });

    setBp("");
    setHr("");
    setTemp("");
    setSpo2("");
    await loadData(selectedPatient);
  }

  async function markGiven(index: number) {
    await apiPost(`/mar/${selectedPatient}/${index}/status`, {
      status: "Given"
    });
    await loadData(selectedPatient);
  }

  return (
    <div>
      <h1 style={{ fontSize: 30, marginBottom: 8, color: "#0f172a" }}>Nurse Workflow</h1>
      <p style={{ color: "#64748b", marginBottom: 20 }}>
        Nursing station for vitals capture and medication administration.
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

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        <div style={cardStyle}>
          <h3>Record Vitals</h3>
          <div style={{ display: "grid", gap: 10 }}>
            <input placeholder="BP" value={bp} onChange={(e) => setBp(e.target.value)} />
            <input placeholder="HR" value={hr} onChange={(e) => setHr(e.target.value)} />
            <input placeholder="Temp" value={temp} onChange={(e) => setTemp(e.target.value)} />
            <input placeholder="SpO2" value={spo2} onChange={(e) => setSpo2(e.target.value)} />
            <button onClick={addVitals} style={{ padding: 10 }}>Save Vitals</button>
          </div>

          <div style={{ marginTop: 16 }}>
            {vitals.map((v, i) => (
              <div key={i} style={{ background: "#f8fafc", padding: 12, borderRadius: 12, marginBottom: 10 }}>
                <p><b>BP:</b> {v.bp ?? "-"}</p>
                <p><b>HR:</b> {v.hr ?? "-"}</p>
                <p><b>Temp:</b> {v.temp ?? "-"}</p>
                <p><b>SpO2:</b> {v.spo2 ?? "-"}</p>
              </div>
            ))}
          </div>
        </div>

        <div style={cardStyle}>
          <h3>Medication Administration Record (MAR)</h3>
          {mar.length === 0 ? (
            <p>No MAR items.</p>
          ) : (
            mar.map((item, i) => (
              <div key={i} style={{ background: "#f8fafc", padding: 12, borderRadius: 12, marginBottom: 10 }}>
                <p><b>Medication:</b> {item.medication ?? "-"}</p>
                <p><b>Dose:</b> {item.dose ?? "-"}</p>
                <p><b>Time:</b> {item.time ?? "-"}</p>
                <p><b>Status:</b> {item.status ?? "-"}</p>
                <p><b>Pharmacy Review:</b> {item.pharmacy_review ?? "-"}</p>
                <p><b>AI Flag:</b> {item.ai_flag ?? "-"}</p>
                {item.status !== "Given" && (
                  <button onClick={() => markGiven(i)} style={{ padding: 8 }}>
                    Mark Given
                  </button>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
