import type { SmartOrder } from "@/types/clinical"

export default function SmartOrdersCard({ orders }: { orders: SmartOrder[] }) {
  return (
    <div style={cardStyle}>
      <h3 style={titleStyle}>AI Smart Orders</h3>
      <div style={{ display: "grid", gap: 10 }}>
        {orders.map((order) => (
          <div key={order.id} style={itemStyle}>
            <div style={{ fontWeight: 700 }}>{order.name}</div>
            <div style={{ fontSize: 12, opacity: 0.7 }}>
              {order.department} • {order.priority} • {order.status}
            </div>
            <div style={{ marginTop: 4 }}>{order.note}</div>
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
