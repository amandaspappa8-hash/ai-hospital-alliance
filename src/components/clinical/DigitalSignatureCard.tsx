import type { DigitalSignature } from "@/types/clinical"

export default function DigitalSignatureCard({ signature }: { signature: DigitalSignature }) {
  return (
    <div style={cardStyle}>
      <h3 style={titleStyle}>Digital Signature</h3>
      <div style={{ fontWeight: 700 }}>{signature.doctorName}</div>
      <div style={{ opacity: 0.8, marginTop: 4 }}>{signature.role}</div>
      <div style={{ marginTop: 12 }}>{signature.signatureText}</div>
      <div style={{ marginTop: 8, fontSize: 12, opacity: 0.7 }}>{signature.signedAt}</div>
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
