import { useEffect, useState } from "react";
import { apiGet } from "../lib-api";
import { Loading, ErrorState } from "../components/AppState";

export default function PatientProfile() {
  const [patient, setPatient] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    apiGet("/patients/P-1001")
      .then(setPatient)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Loading />;
  if (error) return <ErrorState message={error} />;

  return (
    <div style={{ padding: 20 }}>
      <h1>{patient.name}</h1>
      <p>ID: {patient.id}</p>
      <p>Status: {patient.status}</p>
    </div>
  );
}
