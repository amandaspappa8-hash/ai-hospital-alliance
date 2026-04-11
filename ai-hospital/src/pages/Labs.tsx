const labs = [
  { patient: "Ahmed Ali", test: "CBC", status: "Pending", priority: "Routine" },
  { patient: "Sara Mohamed", test: "Troponin", status: "Urgent", priority: "High" },
  { patient: "John Smith", test: "HbA1c", status: "Completed", priority: "Routine" },
];

const cardStyle: React.CSSProperties = {
  background: "white",
  borderRadius: 18,
  padding: 20,
  boxShadow: "0 4px 16px rgba(0,0,0,0.06)",
};

export default function Labs() {
  return (
    <div>
      <h1 style={{ fontSize: 30, marginBottom: 8, color: "#0f172a" }}>Labs Workflow</h1>
      <p style={{ color: "#64748b", marginBottom: 20 }}>
        Track laboratory requests, urgency, and completion workflow.
      </p>

      <div style={{ display: "grid", gap: 14 }}>
        {labs.map((lab, index) => (
          <div key={index} style={cardStyle}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <h3 style={{ margin: 0 }}>{lab.test}</h3>
                <p style={{ margin: "8px 0", color: "#475569" }}>Patient: {lab.patient}</p>
              </div>

              <div
                style={{
                  padding: "8px 12px",
                  borderRadius: 999,
                  fontWeight: 700,
                  background:
                    lab.status === "Urgent"
                      ? "#fef2f2"
                      : lab.status === "Completed"
                      ? "#f0fdf4"
                      : "#fff7ed",
                  color:
                    lab.status === "Urgent"
                      ? "#dc2626"
                      : lab.status === "Completed"
                      ? "#16a34a"
                      : "#d97706",
                }}
              >
                {lab.status}
              </div>
            </div>

            <div
              style={{
                marginTop: 14,
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
                gap: 12,
              }}
            >
              <div style={{ background: "#f8fafc", borderRadius: 12, padding: 12 }}>
                <div style={{ color: "#64748b", fontSize: 13 }}>Priority</div>
                <div style={{ fontWeight: 700 }}>{lab.priority}</div>
              </div>

              <div style={{ background: "#eff6ff", borderRadius: 12, padding: 12 }}>
                <div style={{ color: "#1d4ed8", fontSize: 13 }}>Workflow Stage</div>
                <div style={{ fontWeight: 700, color: "#0f172a" }}>
                  {lab.status === "Completed"
                    ? "Reported"
                    : lab.status === "Urgent"
                    ? "Immediate Processing"
                    : "Queued"}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
