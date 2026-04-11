export default function Landing() {
  return (
    <div style={{ padding: 40, fontFamily: "Inter" }}>
      <h1 style={{ fontSize: 48 }}>AI Hospital Alliance</h1>

      <p style={{ fontSize: 20, marginTop: 20 }}>
        AI-powered Operating System for Hospitals
      </p>

      <button style={{
        marginTop: 30,
        padding: "12px 20px",
        background: "#2563eb",
        color: "white",
        borderRadius: 10
      }}>
        Request Demo
      </button>

      <div style={{ marginTop: 60 }}>
        <h2>What we do</h2>
        <ul>
          <li>AI Radiology</li>
          <li>Smart Pharmacy</li>
          <li>Clinical Decision AI</li>
        </ul>
      </div>
    </div>
  );
}
