import type { DecisionEngineResult } from "@/types/clinical"

export default function DecisionEngineCard({ result }: { result: DecisionEngineResult }) {
  return (
    <div style={cardStyle}>
      <h3 style={titleStyle}>Smart Decision Engine</h3>
      <div><b>Risk Level:</b> {result.riskLevel}</div>
      <div style={{ marginTop: 8 }}><b>Impression:</b> {result.impression}</div>
      <div style={{ marginTop: 8 }}><b>Plan:</b></div>
      <ul>
        {result.plan.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
      <div style={{ marginTop: 8 }}><b>Next Step:</b> {result.nextStep}</div>
    </div>
  )
}

const cardStyle: React.CSSProperties = {
  background: "#111827",
  border: "1px solid #374151",
  borderRadius: 12,
  padding: 16,
  color: "white",
}

const titleStyle: React.CSSProperties = {
  fontSize: 20,
  fontWeight: 700,
  marginBottom: 12,
}
