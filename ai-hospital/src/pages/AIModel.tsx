import { useState } from "react";
import { apiPost } from "../lib-api";

export default function AIModel() {
  const [result, setResult] = useState<any>(null);

  async function runAI() {
    const res = await apiPost("/ai/predict", {
      path: "/path/to/test.jpg"
    });
    setResult(res);
  }

  return (
    <div>
      <h1>Real AI Model</h1>

      <button onClick={runAI}>Run AI</button>

      {result && (
        <div>
          <p>Abnormal: {result.prediction.abnormal}</p>
          <p>Risk: {result.risk}</p>
        </div>
      )}
    </div>
  );
}
