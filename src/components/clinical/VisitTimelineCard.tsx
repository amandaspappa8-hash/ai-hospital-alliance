import type { VisitTimelineItem } from "@/types/clinical"

export default function VisitTimelineCard({ items }: { items: VisitTimelineItem[] }) {
  return (
    <div style={cardStyle}>
      <h3 style={titleStyle}>Visit Timeline</h3>
      <div style={{ display: "grid", gap: 10 }}>
        {items.map((item) => (
          <div key={item.id} style={itemStyle}>
            <div style={{ fontWeight: 700 }}>{item.title}</div>
            <div style={{ fontSize: 12, opacity: 0.7 }}>{item.time}</div>
            <div style={{ marginTop: 4 }}>{item.description}</div>
            <div style={{ marginTop: 4, fontSize: 12, opacity: 0.7 }}>{item.status}</div>
          </div>
        ))}
      </div>
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

const itemStyle: React.CSSProperties = {
  background: "#0b1220",
  border: "1px solid #374151",
  borderRadius: 10,
  padding: 12,
}
