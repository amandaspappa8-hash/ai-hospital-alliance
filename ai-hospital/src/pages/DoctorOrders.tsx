import { useEffect, useState } from "react";
import { apiGet, apiPost } from "../lib-api";

type Patient = {
  id: string;
  name: string;
};

type Order = {
  type?: string;
  name?: string;
  status?: string;
  date?: string;
};

const cardStyle: React.CSSProperties = {
  background: "white",
  borderRadius: 18,
  padding: 20,
  boxShadow: "0 4px 16px rgba(0,0,0,0.06)",
};

export default function DoctorOrders() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [selectedPatient, setSelectedPatient] = useState("P-1001");
  const [orders, setOrders] = useState<Order[]>([]);
  const [orderType, setOrderType] = useState("Lab");
  const [orderName, setOrderName] = useState("");

  async function loadData(patientId: string) {
    const [patientsData, ordersData] = await Promise.all([
      apiGet<Patient[]>("/patients"),
      apiGet<Order[]>(`/orders/${patientId}`)
    ]);

    setPatients(Array.isArray(patientsData) ? patientsData : []);
    setOrders(Array.isArray(ordersData) ? ordersData : []);
  }

  useEffect(() => {
    loadData(selectedPatient).catch(console.error);
  }, [selectedPatient]);

  async function addOrder() {
    if (!orderName.trim()) return;

    await apiPost(`/orders/${selectedPatient}`, {
      type: orderType,
      name: orderName,
      status: "Pending",
      date: new Date().toISOString(),
    });

    if (orderType === "Medication") {
      await apiPost(`/mar/${selectedPatient}`, {
        medication: orderName,
        dose: "Standard dose",
        status: "Pending",
        time: "08:00"
      });
    }

    setOrderName("");
    await loadData(selectedPatient);
  }

  return (
    <div>
      <h1 style={{ fontSize: 30, marginBottom: 8, color: "#0f172a" }}>Doctor Order Entry</h1>
      <p style={{ color: "#64748b", marginBottom: 20 }}>
        Create clinical orders and medication orders linked to MAR.
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
        <h3>Create Order</h3>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 16 }}>
          <select value={orderType} onChange={(e) => setOrderType(e.target.value)}>
            <option value="Lab">Lab</option>
            <option value="Imaging">Imaging</option>
            <option value="Medication">Medication</option>
          </select>

          <input
            value={orderName}
            onChange={(e) => setOrderName(e.target.value)}
            placeholder="Order name"
          />

          <button onClick={addOrder} style={{ gridColumn: "span 2", padding: 10 }}>
            Add Order
          </button>
        </div>

        <h3>Current Orders</h3>
        {orders.length === 0 ? (
          <p>No orders.</p>
        ) : (
          orders.map((o, i) => (
            <div key={i} style={{ background: "#f8fafc", padding: 12, borderRadius: 12, marginBottom: 10 }}>
              <p><b>Type:</b> {o.type ?? "-"}</p>
              <p><b>Name:</b> {o.name ?? "-"}</p>
              <p><b>Status:</b> {o.status ?? "-"}</p>
              <p><b>Date:</b> {o.date ?? "-"}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
