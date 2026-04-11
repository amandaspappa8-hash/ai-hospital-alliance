import { useState } from "react";
import { apiPost } from "../lib-api";

export default function Segmentation() {
  const [mask, setMask] = useState<any>(null);

  async function runSeg() {
    const res = await apiPost("/ai/segment", {
      path: "/path/to/image.png"
    });
    setMask(res.mask);
  }

  return (
    <div>
      <h1>UNet Tumor Segmentation</h1>

      <button onClick={runSeg}>Run Segmentation</button>

      {mask && <p>Segmentation completed ✅</p>}
    </div>
  );
}
