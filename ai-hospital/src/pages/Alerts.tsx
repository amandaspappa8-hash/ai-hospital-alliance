import { useEffect, useState } from "react";
import { apiGet } from "../lib-api";

export default function Alerts() {
  const [alerts, setAlerts] = useState<any[]>([]);

  useEffect(() => {
    apiGet("/alerts").then(setAlerts);
  }, []);

  return (
    <div>
      <h1>🚨 AI Alerts</h1>

      {alerts.length === 0 ? (
        <p>No alerts</p>
      ) : (
        alerts.map((a, i) => (
          <div key={i} style={{ background:"#fee2e2", padding:12, marginBottom:10 }}>
            ⚠️ {a.message} (Patient: {a.patient_id})
          </div>
        ))
      )}
    </div>
  );
}
