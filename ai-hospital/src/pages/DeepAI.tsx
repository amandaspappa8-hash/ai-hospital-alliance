import { useState } from "react";
import { apiPost } from "../lib-api";

export default function DeepAI() {
  const [result, setResult] = useState<any>(null);

  async function runAI() {
    const res = await apiPost("/ai/deep-radiology", {
      path: "/path/to/sample.dcm"
    });

    const report = await apiPost("/ai/deep-report", {
      prediction: res.prediction
    });

    setResult({ ...res, report: report.report });
  }

  return (
    <div>
      <h1>Deep AI Radiology</h1>

      <button onClick={runAI}>Run Deep AI</button>

      {result && (
        <div>
          <p>Abnormal: {result.prediction.abnormal}</p>
          <p>Risk: {result.risk}</p>
          <p>Report: {result.report}</p>
        </div>
      )}
    </div>
  );
}
