import { useState } from "react";

const cardStyle: React.CSSProperties = {
  background: "white",
  borderRadius: 18,
  padding: 20,
  boxShadow: "0 4px 16px rgba(0,0,0,0.06)",
};

export default function AIAssistant() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function runAI() {
    setLoading(true);
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/ai/clinical-route", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          chief_complaint: "Chest pain",
          symptoms: ["Shortness of breath", "Sweating"],
          age: 58,
          gender: "Male",
          vitals: {
            bp: "150/95",
            hr: 110,
            spo2: 95,
            temp: 37.1
          }
        }),
      });

      const data = await res.json();
      setResult(data);
    } catch (e) {
      setResult({ error: String(e) });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1 style={{ fontSize: 30, marginBottom: 8, color: "#0f172a" }}>AI Assistant</h1>
      <p style={{ color: "#64748b", marginBottom: 20 }}>
        Clinical decision support powered by symptom routing and urgency scoring.
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1.2fr",
          gap: 16,
        }}
      >
        <div style={cardStyle}>
          <h3 style={{ marginBottom: 14 }}>Clinical Decision Panel</h3>
          <div style={{ display: "grid", gap: 12 }}>
            <div style={{ background: "#f8fafc", borderRadius: 12, padding: 14 }}>
              Complaint: Chest pain
            </div>
            <div style={{ background: "#f8fafc", borderRadius: 12, padding: 14 }}>
              Symptoms: Shortness of breath, Sweating
            </div>
            <div style={{ background: "#f8fafc", borderRadius: 12, padding: 14 }}>
              Vitals: BP 150/95, HR 110, SpO2 95%
            </div>
          </div>

          <button
            onClick={runAI}
            style={{
              marginTop: 18,
              background: "#2563eb",
              color: "white",
              border: "none",
              padding: "12px 18px",
              borderRadius: 12,
              cursor: "pointer",
              fontWeight: 700,
              width: "100%",
            }}
          >
            {loading ? "Running..." : "Run Clinical AI"}
          </button>
        </div>

        <div style={cardStyle}>
          <h3 style={{ marginBottom: 14 }}>AI Output</h3>
          {!result ? (
            <div
              style={{
                background: "#eff6ff",
                borderRadius: 12,
                padding: 16,
                color: "#1d4ed8",
                fontWeight: 700,
              }}
            >
              Waiting for AI execution...
            </div>
          ) : (
            <pre
              style={{
                whiteSpace: "pre-wrap",
                margin: 0,
                background: "#f8fafc",
                padding: 16,
                borderRadius: 12,
                overflow: "auto",
              }}
            >
              {JSON.stringify(result, null, 2)}
            </pre>
          )}
        </div>
      </div>
    </div>
  );
}
