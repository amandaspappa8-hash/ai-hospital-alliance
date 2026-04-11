import { useEffect, useState } from "react";
import { apiGet } from "../lib-api";

export default function Dashboard() {
  const [patients, setPatients] = useState<any[]>([]);

  useEffect(() => {
    apiGet("/patients").then(setPatients);
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Dashboard</h1>
      <p>Total Patients: {patients.length}</p>
    </div>
  );
}
