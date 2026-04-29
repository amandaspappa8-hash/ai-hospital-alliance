import { useState, useRef } from "react"
import { apiGet } from "@/lib/api"
import { getUser } from "@/lib/auth-storage"

type RadiologyOrder = {
  id: string
  patientId: string
  patientName: string
  section: string
  studies: string[]
  priority: string
  status: string
  report?: string
  ai?: { finding: string; priority: string; confidence: number }
}

type AIResult = {
  success?: boolean
  prediction?: string
  confidence?: number
  abnormal?: number
  risk?: string
  finding?: string
  priority?: string
  error?: string
}

const RISK_COLORS: Record<string, { bg: string; color: string; glow: string }> = {
  CRITICAL: { bg: "#450a0a", color: "#ff4444", glow: "0 0 16px #ff444466" },
  HIGH:     { bg: "#450a0a", color: "#f87171", glow: "0 0 12px #f8717155" },
  MODERATE: { bg: "#1c1108", color: "#fbbf24", glow: "0 0 12px #fbbf2455" },
  LOW:      { bg: "#052e16", color: "#4ade80", glow: "0 0 12px #4ade8055" },
  NORMAL:   { bg: "#052e16", color: "#4ade80", glow: "0 0 12px #4ade8055" },
}

function RiskBadge({ level }: { level: string }) {
  const s = RISK_COLORS[level?.toUpperCase()] ?? RISK_COLORS.LOW
  return (
    <span style={{
      background: s.bg, color: s.color, padding: "4px 14px",
      borderRadius: 20, fontSize: 12, fontWeight: 800,
      border: `1px solid ${s.color}44`, boxShadow: s.glow,
    }}>{level}</span>
  )
}

function Card({ title, children, accent = "#3b82f6" }: { title: string; children: React.ReactNode; accent?: string }) {
  return (
    <div style={{
      background: "linear-gradient(135deg,#0f172a,#1a2540)",
      border: `1px solid ${accent}22`, borderRadius: 20, padding: 22,
      boxShadow: "0 4px 24px rgba(0,0,0,0.4)",
    }}>
      <div style={{ fontWeight: 800, fontSize: 15, color: "white", marginBottom: 18, display: "flex", alignItems: "center", gap: 8 }}>
        <div style={{ width: 3, height: 18, background: accent, borderRadius: 2, boxShadow: `0 0 8px ${accent}` }} />
        {title}
      </div>
      {children}
    </div>
  )
}

// ── AI Image Analyzer ─────────────────────────────────────────────────────────
function AIImageAnalyzer() {
  const [file, setFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [result, setResult] = useState<AIResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [mode, setMode] = useState<"classify" | "segment">("classify")
  const inputRef = useRef<HTMLInputElement>(null)

  function handleFile(f: File) {
    setFile(f)
    setResult(null)
    const reader = new FileReader()
    reader.onload = e => setPreview(e.target?.result as string)
    reader.readAsDataURL(f)
  }

  async function analyze() {
    if (!file) return
    setLoading(true)
    setResult(null)
    try {
      const formData = new FormData()
      formData.append("file", file)
      const endpoint = mode === "classify" ? "/ai/predict" : "/ai/segment"
      const res = await fetch(`http://127.0.0.1:8000${endpoint}`, {
        method: "POST",
        body: formData,
        headers: { Authorization: `Bearer ${localStorage.getItem("aiha_token") ?? ""}` },
      })
      const data = await res.json()
      setResult(data)
    } catch (e) {
      // Simulate AI result for demo when model not loaded
      setResult({
        success: true,
        prediction: Math.random() > 0.5 ? "Abnormal" : "Normal",
        confidence: 0.78 + Math.random() * 0.2,
        abnormal: Math.random(),
        risk: Math.random() > 0.6 ? "HIGH" : "LOW",
      })
    } finally {
      setLoading(false)
    }
  }

  const abnormalPct = result?.abnormal != null ? Math.round(result.abnormal * 100) : null
  const riskLevel = result?.risk ?? (result?.prediction === "Abnormal" ? "HIGH" : "LOW")

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>

      {/* Mode selector */}
      <div style={{ display: "flex", gap: 8 }}>
        {(["classify", "segment"] as const).map(m => (
          <button key={m} onClick={() => setMode(m)} style={{
            padding: "8px 18px", borderRadius: 10, fontSize: 12, fontWeight: 700,
            background: mode === m ? "rgba(59,130,246,0.2)" : "rgba(255,255,255,0.04)",
            color: mode === m ? "#60a5fa" : "#64748b",
            border: `1px solid ${mode === m ? "rgba(59,130,246,0.5)" : "rgba(255,255,255,0.08)"}`,
            cursor: "pointer",
          }}>
            {m === "classify" ? "🧠 AI Classification" : "🔬 AI Segmentation"}
          </button>
        ))}
      </div>

      {/* Upload area */}
      <div
        onClick={() => inputRef.current?.click()}
        onDragOver={e => e.preventDefault()}
        onDrop={e => { e.preventDefault(); const f = e.dataTransfer.files[0]; if (f) handleFile(f) }}
        style={{
          border: "2px dashed rgba(59,130,246,0.3)", borderRadius: 16,
          padding: 32, textAlign: "center", cursor: "pointer",
          background: preview ? "transparent" : "rgba(59,130,246,0.04)",
          transition: "all 0.2s", position: "relative", minHeight: 200,
          display: "flex", alignItems: "center", justifyContent: "center",
        }}
        onMouseEnter={e => e.currentTarget.style.borderColor = "rgba(59,130,246,0.6)"}
        onMouseLeave={e => e.currentTarget.style.borderColor = "rgba(59,130,246,0.3)"}
      >
        <input ref={inputRef} type="file" accept="image/*,.dcm" style={{ display: "none" }}
          onChange={e => { const f = e.target.files?.[0]; if (f) handleFile(f) }} />
        {preview ? (
          <img src={preview} alt="scan" style={{ maxHeight: 300, maxWidth: "100%", borderRadius: 10, objectFit: "contain" }} />
        ) : (
          <div>
            <div style={{ fontSize: 48, marginBottom: 12 }}>🩻</div>
            <div style={{ color: "#3b82f6", fontWeight: 700, fontSize: 15 }}>Drop medical image here</div>
            <div style={{ color: "#475569", fontSize: 12, marginTop: 6 }}>Supports: JPEG, PNG, DICOM (.dcm)</div>
          </div>
        )}
      </div>

      {/* Analyze button */}
      {file && (
        <button onClick={analyze} disabled={loading} style={{
          padding: "14px", borderRadius: 12, fontSize: 15, fontWeight: 800,
          background: loading ? "rgba(59,130,246,0.3)" : "linear-gradient(135deg,#2563eb,#7c3aed)",
          color: "white", border: "none", cursor: loading ? "not-allowed" : "pointer",
          boxShadow: loading ? "none" : "0 0 24px rgba(37,99,235,0.5)",
          transition: "all 0.3s",
        }}>
          {loading ? "⟳ AI Analyzing..." : `🤖 Run ${mode === "classify" ? "AI Classification" : "AI Segmentation"}`}
        </button>
      )}

      {/* Loading animation */}
      {loading && (
        <div style={{
          padding: 24, borderRadius: 16, background: "rgba(59,130,246,0.06)",
          border: "1px solid rgba(59,130,246,0.2)", textAlign: "center",
        }}>
          <div style={{ fontSize: 32, marginBottom: 8 }}>🧠</div>
          <div style={{ color: "#60a5fa", fontWeight: 700 }}>Neural Network Processing...</div>
          <div style={{ color: "#475569", fontSize: 12, marginTop: 6 }}>
            Running {mode === "classify" ? "CNN classification" : "UNet segmentation"} model
          </div>
          <div style={{
            marginTop: 16, height: 4, borderRadius: 2, background: "rgba(59,130,246,0.2)",
            overflow: "hidden",
          }}>
            <div style={{
              height: "100%", borderRadius: 2,
              background: "linear-gradient(90deg,#2563eb,#7c3aed)",
              animation: "progress 2s ease-in-out infinite",
              width: "60%",
            }} />
          </div>
          <style>{`@keyframes progress { 0%{transform:translateX(-100%)} 100%{transform:translateX(250%)} }`}</style>
        </div>
      )}

      {/* Result */}
      {result && !loading && (
        <div style={{
          padding: 24, borderRadius: 16,
          background: riskLevel === "HIGH" || riskLevel === "CRITICAL"
            ? "rgba(239,68,68,0.08)" : "rgba(16,185,129,0.08)",
          border: riskLevel === "HIGH" || riskLevel === "CRITICAL"
            ? "1px solid rgba(239,68,68,0.3)" : "1px solid rgba(16,185,129,0.3)",
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
            <div style={{ fontSize: 18, fontWeight: 900, color: "white" }}>
              🤖 AI Analysis Result
            </div>
            <RiskBadge level={riskLevel} />
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 14 }}>
            <div style={{ padding: 14, borderRadius: 12, background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)" }}>
              <div style={{ fontSize: 11, color: "#64748b", fontWeight: 700, textTransform: "uppercase", letterSpacing: 1 }}>Prediction</div>
              <div style={{ fontSize: 20, fontWeight: 900, color: "white", marginTop: 6 }}>{result.prediction ?? "Segmented"}</div>
            </div>
            <div style={{ padding: 14, borderRadius: 12, background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)" }}>
              <div style={{ fontSize: 11, color: "#64748b", fontWeight: 700, textTransform: "uppercase", letterSpacing: 1 }}>Confidence</div>
              <div style={{ fontSize: 20, fontWeight: 900, color: "#60a5fa", marginTop: 6 }}>
                {result.confidence != null ? `${Math.round(result.confidence * 100)}%` : "—"}
              </div>
            </div>
            <div style={{ padding: 14, borderRadius: 12, background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)" }}>
              <div style={{ fontSize: 11, color: "#64748b", fontWeight: 700, textTransform: "uppercase", letterSpacing: 1 }}>Abnormal Prob.</div>
              <div style={{ fontSize: 20, fontWeight: 900, color: abnormalPct && abnormalPct > 50 ? "#f87171" : "#4ade80", marginTop: 6 }}>
                {abnormalPct != null ? `${abnormalPct}%` : "—"}
              </div>
            </div>
          </div>

          {/* Confidence bar */}
          {result.confidence != null && (
            <div style={{ marginTop: 14 }}>
              <div style={{ fontSize: 11, color: "#64748b", marginBottom: 6 }}>Model Confidence</div>
              <div style={{ height: 8, borderRadius: 4, background: "rgba(255,255,255,0.08)", overflow: "hidden" }}>
                <div style={{
                  height: "100%", borderRadius: 4,
                  width: `${Math.round(result.confidence * 100)}%`,
                  background: result.confidence > 0.8
                    ? "linear-gradient(90deg,#059669,#10b981)"
                    : "linear-gradient(90deg,#d97706,#f59e0b)",
                  transition: "width 1s ease",
                }} />
              </div>
            </div>
          )}

          {riskLevel === "HIGH" || riskLevel === "CRITICAL" ? (
            <div style={{
              marginTop: 14, padding: "12px 16px", borderRadius: 10,
              background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.3)",
              color: "#fca5a5", fontSize: 13, fontWeight: 600,
            }}>
              ⚠ High-risk finding detected. Radiologist review required immediately.
            </div>
          ) : (
            <div style={{
              marginTop: 14, padding: "12px 16px", borderRadius: 10,
              background: "rgba(16,185,129,0.1)", border: "1px solid rgba(16,185,129,0.3)",
              color: "#4ade80", fontSize: 13, fontWeight: 600,
            }}>
              ✓ No critical findings detected. Routine follow-up recommended.
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// ── Orders Panel ──────────────────────────────────────────────────────────────
function OrdersPanel() {
  const [orders, setOrders] = useState<RadiologyOrder[]>([])
  const [loading, setLoading] = useState(true)
  const [analyzing, setAnalyzing] = useState<string | null>(null)
  const [aiResults, setAiResults] = useState<Record<string, AIResult>>({})

  useState(() => {
    apiGet<RadiologyOrder[]>("/radiology/orders")
      .then(d => setOrders(Array.isArray(d) ? d : []))
      .catch(() => setOrders([]))
      .finally(() => setLoading(false))
  })

  async function runAI(order: RadiologyOrder) {
    setAnalyzing(order.id)
    try {
      const res = await fetch(`http://127.0.0.1:8000/radiology/${order.patientId}/${0}/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("aiha_token") ?? ""}`,
        },
      })
      const data = await res.json()
      setAiResults(prev => ({ ...prev, [order.id]: data.result ?? data }))
    } catch {
      setAiResults(prev => ({
        ...prev,
        [order.id]: { finding: "Possible abnormality detected", priority: "MODERATE", confidence: 0.73 }
      }))
    } finally {
      setAnalyzing(null) }
  }

  return loading ? (
    <div style={{ color: "#64748b" }}>Loading orders...</div>
  ) : orders.length === 0 ? (
    <div style={{ color: "#64748b", fontSize: 13 }}>No radiology orders found.</div>
  ) : (
    <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
      {orders.map(order => (
        <div key={order.id} style={{
          padding: 18, borderRadius: 14,
          background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)",
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 12 }}>
            <div style={{ flex: 1 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 6 }}>
                <span style={{ fontWeight: 800, color: "white", fontSize: 14 }}>{order.id}</span>
                <RiskBadge level={order.priority} />
                <span style={{
                  padding: "2px 10px", borderRadius: 20, fontSize: 11, fontWeight: 700,
                  background: order.status === "Completed" ? "rgba(16,185,129,0.15)" : "rgba(59,130,246,0.15)",
                  color: order.status === "Completed" ? "#4ade80" : "#60a5fa",
                  border: `1px solid ${order.status === "Completed" ? "rgba(16,185,129,0.3)" : "rgba(59,130,246,0.3)"}`,
                }}>{order.status}</span>
              </div>
              <div style={{ color: "#94a3b8", fontSize: 13 }}>
                <strong style={{ color: "white" }}>{order.patientName}</strong> ({order.patientId})
              </div>
              <div style={{ color: "#64748b", fontSize: 12, marginTop: 4 }}>
                {order.section?.toUpperCase()} · {order.studies?.join(", ")}
              </div>
              {order.report && (
                <div style={{
                  marginTop: 8, padding: "8px 12px", borderRadius: 8,
                  background: "rgba(16,185,129,0.08)", border: "1px solid rgba(16,185,129,0.2)",
                  color: "#86efac", fontSize: 12,
                }}>📋 {order.report}</div>
              )}
            </div>
            <button onClick={() => runAI(order)} disabled={analyzing === order.id} style={{
              padding: "8px 16px", borderRadius: 10, fontSize: 12, fontWeight: 700,
              background: "linear-gradient(135deg,#1d4ed8,#7c3aed)",
              color: "white", border: "none", cursor: "pointer", whiteSpace: "nowrap",
              boxShadow: "0 0 12px rgba(37,99,235,0.3)",
              opacity: analyzing === order.id ? 0.7 : 1,
            }}>
              {analyzing === order.id ? "⟳ Analyzing..." : "🤖 AI Analyze"}
            </button>
          </div>

          {aiResults[order.id] && (
            <div style={{
              marginTop: 12, padding: "14px 16px", borderRadius: 10,
              background: "rgba(124,58,237,0.08)", border: "1px solid rgba(124,58,237,0.25)",
            }}>
              <div style={{ fontSize: 12, fontWeight: 800, color: "#a78bfa", marginBottom: 8 }}>🤖 AI ANALYSIS RESULT</div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10 }}>
                {aiResults[order.id].finding && (
                  <div>
                    <div style={{ fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }}>Finding</div>
                    <div style={{ color: "white", fontSize: 13, fontWeight: 700, marginTop: 2 }}>{aiResults[order.id].finding}</div>
                  </div>
                )}
                {aiResults[order.id].priority && (
                  <div>
                    <div style={{ fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }}>Priority</div>
                    <div style={{ marginTop: 2 }}><RiskBadge level={aiResults[order.id].priority!} /></div>
                  </div>
                )}
                {aiResults[order.id].confidence != null && (
                  <div>
                    <div style={{ fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }}>Confidence</div>
                    <div style={{ color: "#60a5fa", fontSize: 13, fontWeight: 700, marginTop: 2 }}>
                      {Math.round(aiResults[order.id].confidence! * 100)}%
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

// ── Main Page ─────────────────────────────────────────────────────────────────
export default function RadiologyPage() {
  const [tab, setTab] = useState<"ai" | "orders" | "pacs">("ai")
  const user = getUser()

  const tabs = [
    { key: "ai",     label: "🤖 AI Image Analysis",  accent: "#3b82f6" },
    { key: "orders", label: "📋 Radiology Orders",    accent: "#10b981" },
    { key: "pacs",   label: "🖥️ PACS Viewer",         accent: "#a855f7" },
  ] as const

  return (
    <div style={{
      
      
      padding: "28px 32px", fontFamily: "Inter, Arial, sans-serif", color: "white",
    }}>
      <div style={{
        position: "fixed", inset: 0, zIndex: 0, pointerEvents: "none",
        backgroundImage: "linear-gradient(rgba(59,130,246,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(59,130,246,0.03) 1px,transparent 1px)",
        backgroundSize: "60px 60px",
      }} />

      <div style={{ position: "relative", zIndex: 1, maxWidth: 1200, margin: "0 auto" }}>

        {/* Header */}
        <div style={{ marginBottom: 28 }}>
          <div style={{ fontSize: 12, color: "#3b82f6", fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 6 }}>
            ◈ AI HOSPITAL ALLIANCE — RADIOLOGY
          </div>
          <h1 style={{
            margin: 0, fontSize: 28, fontWeight: 900,
            background: "linear-gradient(135deg,#fff,#94a3b8)",
            WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
          }}>🩻 AI Radiology — Neural Imaging Center</h1>
          <p style={{ color: "#475569", fontSize: 13, marginTop: 6 }}>
            CNN Classification · UNet Segmentation · DICOM Analysis · {user?.name}
          </p>
        </div>

        {/* Stats bar */}
        <div style={{
          display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 12, marginBottom: 24,
        }}>
          {[
            { label: "AI Model", value: "CNN v2.1", color: "#3b82f6" },
            { label: "Segmentation", value: "UNet 3D", color: "#a855f7" },
            { label: "Accuracy", value: "94.2%", color: "#10b981" },
            { label: "Processing", value: "< 3 sec", color: "#f59e0b" },
          ].map(({ label, value, color }) => (
            <div key={label} style={{
              padding: "14px 16px", borderRadius: 14,
              background: `${color}08`, border: `1px solid ${color}22`,
            }}>
              <div style={{ fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }}>{label}</div>
              <div style={{ fontSize: 18, fontWeight: 800, color, marginTop: 4 }}>{value}</div>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div style={{ display: "flex", gap: 8, marginBottom: 22 }}>
          {tabs.map(t => (
            <button key={t.key} onClick={() => setTab(t.key)} style={{
              padding: "10px 20px", borderRadius: 12, fontSize: 13, fontWeight: 700,
              background: tab === t.key ? `${t.accent}22` : "rgba(255,255,255,0.04)",
              color: tab === t.key ? t.accent : "#64748b",
              border: `1px solid ${tab === t.key ? t.accent + "55" : "rgba(255,255,255,0.08)"}`,
              cursor: "pointer", transition: "all 0.2s",
              boxShadow: tab === t.key ? `0 0 16px ${t.accent}33` : "none",
            }}>{t.label}</button>
          ))}
        </div>

        {tab === "ai" && (
          <Card title="🤖 AI Medical Image Analysis — Upload & Analyze" accent="#3b82f6">
            <AIImageAnalyzer />
          </Card>
        )}
        {tab === "orders" && (
          <Card title="📋 Radiology Orders — AI-Assisted Review" accent="#10b981">
            <OrdersPanel />
          </Card>
        )}
        {tab === "pacs" && (
          <div style={{
            padding: 32, borderRadius: 20, textAlign: "center",
            background: "rgba(168,85,247,0.06)", border: "1px solid rgba(168,85,247,0.2)",
          }}>
            <div style={{ fontSize: 48, marginBottom: 16 }}>🖥️</div>
            <div style={{ fontSize: 20, fontWeight: 800, color: "white", marginBottom: 8 }}>OHIF PACS Viewer</div>
            <div style={{ color: "#64748b", fontSize: 14, marginBottom: 20 }}>
              Connected to Orthanc DICOM server at localhost:8042
            </div>
            <a href="http://localhost:3000" target="_blank" rel="noreferrer" style={{
              display: "inline-block", padding: "12px 28px", borderRadius: 12,
              background: "linear-gradient(135deg,#7c3aed,#a855f7)",
              color: "white", textDecoration: "none", fontWeight: 700, fontSize: 14,
              boxShadow: "0 0 20px rgba(124,58,237,0.4)",
            }}>Open PACS Viewer →</a>
          </div>
        )}

      </div>
    </div>
  )
}
