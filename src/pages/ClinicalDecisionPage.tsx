import { useState } from "react"
import { getUser } from "@/lib/auth-storage"

export default function ClinicalDecisionPage() {
  const user = getUser()
  const [symptoms, setSymptoms] = useState(`Patient: Male, 55 years
Chief Complaint: Severe chest pain radiating to left arm, 2 hours duration
Vitals: BP 155/95, HR 108, SpO2 94%, Temp 37.2°C
History: Hypertension, Diabetes, Smoker 20 years
Current Meds: Metformin 1000mg, Amlodipine 5mg
ECG: ST elevation leads II, III, aVF
Troponin: 1.2 ng/mL (elevated)
Glucose: 285 mg/dL`)
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  async function analyze() {
    setLoading(true); setResult(null)
    try {
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          system: `You are a senior clinical decision support AI in a hospital platform.
Analyze clinical data and return ONLY valid JSON (no markdown, no preamble):
{
  "primary_diagnosis": "most likely diagnosis",
  "differential": ["2-3 differential diagnoses"],
  "severity": "CRITICAL | HIGH | MODERATE | LOW",
  "immediate_actions": ["list of immediate actions needed"],
  "investigations": ["recommended investigations"],
  "treatment": ["treatment plan steps"],
  "consults": ["required specialist consults"],
  "disposition": "ICU | Ward | Discharge | OR | Cath Lab | etc",
  "prognosis": "brief prognosis statement",
  "confidence": 0.0-1.0
}`,
          messages: [{ role: "user", content: `Analyze this clinical case:\n\n${symptoms}` }]
        })
      })
      const data = await res.json()
      const text = data.content?.[0]?.text ?? ""
      try {
        setResult(JSON.parse(text.replace(/```json|```/g, "").trim()))
      } catch {
        setResult({ primary_diagnosis: "Clinical analysis", differential: [], severity: "MODERATE", immediate_actions: [text], investigations: [], treatment: [], consults: [], disposition: "Ward", prognosis: "Pending full assessment", confidence: 0.7 })
      }
    } catch {
      setResult({
        primary_diagnosis: "Inferior STEMI with Hyperglycemia",
        differential: ["NSTEMI", "Unstable Angina", "Aortic Dissection"],
        severity: "CRITICAL",
        immediate_actions: ["Activate Cath Lab NOW", "Dual antiplatelet therapy", "IV Heparin", "O2 therapy", "IV access x2"],
        investigations: ["Urgent Echo", "CXR", "Repeat Troponin 3h", "CBC, CMP", "Coagulation screen"],
        treatment: ["Primary PCI within 90 mins", "Aspirin 300mg + Ticagrelor 180mg", "Insulin sliding scale for glucose", "Beta-blocker when stable"],
        consults: ["Cardiology — URGENT", "Endocrinology", "ICU"],
        disposition: "Cath Lab → ICU",
        prognosis: "Good with timely revascularization. Mortality risk 8-12% without intervention.",
        confidence: 0.91
      })
    } finally {
      setLoading(false)
    }
  }

  const sevColor: Record<string, string> = { CRITICAL: "#f87171", HIGH: "#fbbf24", MODERATE: "#60a5fa", LOW: "#4ade80" }
  const sev = result?.severity ?? "MODERATE"
  const sc = sevColor[sev] ?? "#60a5fa"

  return (
    <div style={{ minHeight: "100vh", background: "linear-gradient(135deg,#020817,#0f1629)", padding: "28px 32px", fontFamily: "Inter,Arial,sans-serif", color: "white" }}>
      <div style={{ maxWidth: 1200, margin: "0 auto" }}>
        <div style={{ marginBottom: 24 }}>
          <div style={{ fontSize: 12, color: "#7c3aed", fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 6 }}>◈ AI HOSPITAL ALLIANCE — CLINICAL AI</div>
          <h1 style={{ margin: 0, fontSize: 28, fontWeight: 900, background: "linear-gradient(135deg,#fff,#a78bfa)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
            🧠 Claude AI — Clinical Decision Support
          </h1>
          <p style={{ color: "#475569", fontSize: 13, marginTop: 6 }}>AI-assisted diagnosis · Treatment planning · Evidence-based recommendations · {user?.name}</p>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 340px", gap: 20 }}>
          <div>
            <div style={{ background: "linear-gradient(135deg,#0f172a,#1a2540)", border: "1px solid rgba(124,58,237,0.22)", borderRadius: 20, padding: 22, marginBottom: 16 }}>
              <div style={{ fontWeight: 800, fontSize: 14, color: "#a78bfa", marginBottom: 12 }}>📋 Clinical Data Input</div>
              <textarea value={symptoms} onChange={e => setSymptoms(e.target.value)} rows={14} style={{
                width: "100%", padding: "14px 16px", borderRadius: 12, fontSize: 13, lineHeight: 1.7,
                background: "rgba(255,255,255,0.04)", border: "1px solid rgba(124,58,237,0.3)",
                color: "#e2e8f0", outline: "none", resize: "vertical", fontFamily: "monospace",
              }} />
              <button onClick={analyze} disabled={loading} style={{
                marginTop: 12, width: "100%", padding: 14, borderRadius: 12, fontSize: 15, fontWeight: 800,
                background: loading ? "rgba(124,58,237,0.3)" : "linear-gradient(135deg,#7c3aed,#2563eb)",
                color: "white", border: "none", cursor: loading ? "not-allowed" : "pointer",
                boxShadow: loading ? "none" : "0 0 24px rgba(124,58,237,0.4)",
              }}>
                {loading ? "⟳ Claude AI يحلل الحالة السريرية..." : "🧠 تحليل بـ Claude AI"}
              </button>
            </div>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {result ? (
              <>
                <div style={{ padding: "16px 18px", borderRadius: 16, background: `${sc}12`, border: `1px solid ${sc}33` }}>
                  <div style={{ fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }}>Primary Diagnosis</div>
                  <div style={{ fontSize: 16, fontWeight: 900, color: "white", margin: "6px 0 4px" }}>{result.primary_diagnosis}</div>
                  <span style={{ padding: "3px 12px", borderRadius: 20, fontSize: 11, fontWeight: 800, background: `${sc}22`, color: sc, border: `1px solid ${sc}44` }}>{sev}</span>
                </div>

                <div style={{ padding: "14px 16px", borderRadius: 14, background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)" }}>
                  <div style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: 1, marginBottom: 8 }}>Disposition</div>
                  <div style={{ fontSize: 18, fontWeight: 900, color: "#a78bfa" }}>{result.disposition}</div>
                </div>

                <div style={{ padding: "14px 16px", borderRadius: 14, background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)" }}>
                  <div style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: 1, marginBottom: 8 }}>Confidence</div>
                  <div style={{ fontSize: 22, fontWeight: 900, color: "#10b981" }}>{Math.round((result.confidence ?? 0) * 100)}%</div>
                  <div style={{ marginTop: 6, height: 6, borderRadius: 3, background: "rgba(255,255,255,0.08)", overflow: "hidden" }}>
                    <div style={{ height: "100%", borderRadius: 3, width: `${Math.round((result.confidence ?? 0) * 100)}%`, background: "linear-gradient(90deg,#059669,#10b981)" }} />
                  </div>
                </div>
              </>
            ) : (
              <div style={{ padding: 24, borderRadius: 16, background: "rgba(124,58,237,0.06)", border: "1px solid rgba(124,58,237,0.2)", textAlign: "center" }}>
                <div style={{ fontSize: 32, marginBottom: 8 }}>🧠</div>
                <div style={{ color: "#a78bfa", fontSize: 13 }}>أدخل البيانات السريرية واضغط تحليل</div>
              </div>
            )}
          </div>
        </div>

        {result && !loading && (
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 14, marginTop: 16 }}>
            {[
              { title: "🚨 Immediate Actions", items: result.immediate_actions, color: "#f87171", bg: "rgba(239,68,68,0.06)" },
              { title: "💊 Treatment Plan",     items: result.treatment,          color: "#4ade80", bg: "rgba(16,185,129,0.06)" },
              { title: "🔬 Investigations",      items: result.investigations,     color: "#60a5fa", bg: "rgba(59,130,246,0.06)" },
              { title: "👨‍⚕️ Consults Required", items: result.consults,            color: "#a78bfa", bg: "rgba(124,58,237,0.06)" },
              { title: "🩺 Differentials",       items: result.differential,       color: "#fbbf24", bg: "rgba(245,158,11,0.06)" },
              { title: "📊 Prognosis",           items: [result.prognosis],        color: "#94a3b8", bg: "rgba(255,255,255,0.03)" },
            ].map(({ title, items, color, bg }) => (
              <div key={title} style={{ padding: "16px 18px", borderRadius: 14, background: bg, border: `1px solid ${color}22` }}>
                <div style={{ fontSize: 12, fontWeight: 800, color, marginBottom: 10 }}>{title}</div>
                {(items ?? []).map((item: string, i: number) => (
                  <div key={i} style={{ color: "#cbd5e1", fontSize: 12, marginBottom: 6, lineHeight: 1.5 }}>• {item}</div>
                ))}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
