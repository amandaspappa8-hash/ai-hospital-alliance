import { useEffect, useState } from "react";
import { apiGet, apiPost } from "../lib-api";

type Study = {
  study?: string;
  status?: string;
  report?: string;
  ai?: any;
};

export default function Radiology() {
  const [studies, setStudies] = useState<Study[]>([]);

  async function load() {
    const data = await apiGet<Study[]>(`/radiology/P-1001`);
    setStudies(data);
  }

  useEffect(() => {
    load();
  }, []);

  async function runAI(index: number) {
    await apiPost(`/radiology/P-1001/${index}/analyze`, {});
    load();
  }

  return (
    <div>
      <h1>AI Radiology</h1>

      {studies.map((s, i) => (
        <div key={i} style={{ background:"#f1f5f9", padding:12, marginBottom:10 }}>
          <p><b>{s.study}</b></p>
          <p>Status: {s.status}</p>

          <button onClick={() => runAI(i)}>Run AI Analysis</button>

          {s.ai && (
            <div style={{ marginTop:10 }}>
              <p><b>AI Summary:</b> {s.ai.ai_summary}</p>
              {s.ai.findings.map((f:any, idx:number) => (
                <p key={idx}>
                  ⚠️ {f.type} - {f.risk}
                </p>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
