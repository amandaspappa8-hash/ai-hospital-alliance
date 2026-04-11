export default function App() {
  const drugs = [
    {
      name: "Warfarin 5mg",
      interactions: ["Aspirin", "Ibuprofen"],
      risk: "HIGH",
    },
    {
      name: "Metformin 1000mg",
      interactions: [],
      risk: "SAFE",
    },
  ];

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>💊 Smart Pharmacy</h1>

      {drugs.map((drug, index) => (
        <div
          key={index}
          style={{
            border: "1px solid #ccc",
            padding: 10,
            marginBottom: 10,
            borderRadius: 10,
          }}
        >
          <h3>{drug.name}</h3>

          <p>
            Risk:
            <b style={{ color: drug.risk === "HIGH" ? "red" : "green" }}>
              {drug.risk}
            </b>
          </p>

          {drug.interactions.length > 0 ? (
            <p>⚠ {drug.interactions.join(", ")}</p>
          ) : (
            <p>✅ No interactions</p>
          )}
        </div>
      ))}
    </div>
  );
}
