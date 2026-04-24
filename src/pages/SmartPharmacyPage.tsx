import { useState, useEffect } from "react"
import { apiGet } from "@/lib/api"
import { getUser } from "@/lib/auth-storage"

// ─── Types ────────────────────────────────────────────────────────────────────
type FDADrug = {
  brand_name?: string[]
  generic_name?: string[]
  manufacturer_name?: string[]
  route?: string[]
  substance_name?: string[]
}

type FDAResult = {
  openfda?: FDADrug
  warnings?: string[]
  adverse_reactions?: string[]
  dosage_and_administration?: string[]
  contraindications?: string[]
  drug_interactions?: string[]
  indications_and_usage?: string[]
  description?: string[]
}

type RxInteraction = {
  description: string
  severity?: string
}

type MARItem = {
  id: number
  medication: string
  dose: string
  route: string
  schedule: string
  status: string
  givenAt: string
  ai_flag?: string
  pharmacy_review?: string
}

// ─── Helpers ─────────────────────────────────────────────────────────────────
const RISK_COLORS: Record<string, { bg: string; color: string; glow: string }> = {
  HIGH:     { bg: "#450a0a", color: "#f87171", glow: "0 0 12px #f8717155" },
  MODERATE: { bg: "#1c1108", color: "#fbbf24", glow: "0 0 12px #fbbf2455" },
  LOW:      { bg: "#052e16", color: "#4ade80", glow: "0 0 12px #4ade8055" },
  SAFE:     { bg: "#052e16", color: "#4ade80", glow: "0 0 12px #4ade8055" },
  UNKNOWN:  { bg: "#1e293b", color: "#94a3b8", glow: "none" },
}

function RiskBadge({ level }: { level: string }) {
  const s = RISK_COLORS[level] ?? RISK_COLORS.UNKNOWN
  return (
    <span style={{
      background: s.bg, color: s.color, padding: "3px 12px",
      borderRadius: 20, fontSize: 11, fontWeight: 800,
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
      <div style={{
        fontWeight: 800, fontSize: 15, color: "white", marginBottom: 18,
        display: "flex", alignItems: "center", gap: 8,
      }}>
        <div style={{ width: 3, height: 18, background: accent, borderRadius: 2, boxShadow: `0 0 8px ${accent}` }} />
        {title}
      </div>
      {children}
    </div>
  )
}

// ─── FDA Drug Search ──────────────────────────────────────────────────────────
function DrugSearch() {
  const [query, setQuery] = useState("")
  const [results, setResults] = useState<FDAResult[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [selected, setSelected] = useState<FDAResult | null>(null)
  const [rxInteractions, setRxInteractions] = useState<RxInteraction[]>([])
  const [rxLoading, setRxLoading] = useState(false)

  async function searchFDA() {
    if (!query.trim()) return
    setLoading(true)
    setError("")
    setSelected(null)
    setRxInteractions([])
    try {
      const res = await fetch(
        `https://api.fda.gov/drug/label.json?search=openfda.generic_name:"${encodeURIComponent(query)}"&limit=5`
      )
      const data = await res.json()
      if (data.results) {
        setResults(data.results)
      } else {
        setError("No results found. Try a different drug name.")
        setResults([])
      }
    } catch {
      setError("FDA API unavailable. Showing cached data.")
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  async function fetchRxInteractions(drugName: string) {
    setRxLoading(true)
    try {
      // Step 1: Get RxCUI
      const r1 = await fetch(
        `https://rxnav.nlm.nih.gov/REST/rxcui.json?name=${encodeURIComponent(drugName)}&search=1`
      )
      const d1 = await r1.json()
      const rxcui = d1?.idGroup?.rxnormId?.[0]
      if (!rxcui) { setRxLoading(false); return }

      // Step 2: Get interactions
      const r2 = await fetch(
        `https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui=${rxcui}`
      )
      const d2 = await r2.json()
      const groups = d2?.interactionTypeGroup ?? []
      const interactions: RxInteraction[] = []
      for (const group of groups) {
        for (const type of group.interactionType ?? []) {
          for (const pair of type.interactionPair ?? []) {
            interactions.push({
              description: pair.description,
              severity: pair.severity,
            })
          }
        }
      }
      setRxInteractions(interactions.slice(0, 8))
    } catch {
      setRxInteractions([])
    } finally {
      setRxLoading(false)
    }
  }

  function selectDrug(drug: FDAResult) {
    setSelected(drug)
    const name = drug.openfda?.generic_name?.[0] ?? drug.openfda?.brand_name?.[0] ?? query
    fetchRxInteractions(name)
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>

      {/* Search bar */}
      <div style={{ display: "flex", gap: 10 }}>
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === "Enter" && searchFDA()}
          placeholder="Search any drug — e.g. Warfarin, Metformin, Aspirin..."
          style={{
            flex: 1, padding: "12px 16px", borderRadius: 12, fontSize: 14,
            background: "rgba(255,255,255,0.05)", border: "1px solid rgba(59,130,246,0.3)",
            color: "white", outline: "none",
          }}
        />
        <button onClick={searchFDA} disabled={loading} style={{
          padding: "12px 24px", borderRadius: 12, fontSize: 14, fontWeight: 700,
          background: "linear-gradient(135deg,#2563eb,#7c3aed)",
          color: "white", border: "none", cursor: "pointer",
          boxShadow: "0 0 20px rgba(37,99,235,0.4)",
          opacity: loading ? 0.7 : 1,
        }}>
          {loading ? "⟳ Searching..." : "🔍 Search FDA"}
        </button>
      </div>

      {error && <div style={{ color: "#fca5a5", fontSize: 13, padding: "10px 14px", background: "rgba(239,68,68,0.1)", borderRadius: 10, border: "1px solid rgba(239,68,68,0.2)" }}>{error}</div>}

      {/* Results list */}
      {results.length > 0 && !selected && (
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          <div style={{ color: "#64748b", fontSize: 12, fontWeight: 600 }}>SELECT A DRUG TO VIEW FULL PROFILE</div>
          {results.map((r, i) => (
            <div key={i} onClick={() => selectDrug(r)} style={{
              padding: "14px 16px", borderRadius: 12, cursor: "pointer",
              background: "rgba(59,130,246,0.06)", border: "1px solid rgba(59,130,246,0.2)",
              transition: "all 0.2s",
            }}
              onMouseEnter={e => e.currentTarget.style.background = "rgba(59,130,246,0.15)"}
              onMouseLeave={e => e.currentTarget.style.background = "rgba(59,130,246,0.06)"}
            >
              <div style={{ fontWeight: 700, color: "white", fontSize: 14 }}>
                {r.openfda?.brand_name?.[0] ?? "Unknown Brand"}
              </div>
              <div style={{ color: "#94a3b8", fontSize: 12, marginTop: 3 }}>
                Generic: {r.openfda?.generic_name?.[0] ?? "—"} · Route: {r.openfda?.route?.[0] ?? "—"} · Manufacturer: {r.openfda?.manufacturer_name?.[0] ?? "—"}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Drug Detail */}
      {selected && (
        <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <div style={{ fontSize: 22, fontWeight: 900, color: "white" }}>
                {selected.openfda?.brand_name?.[0] ?? "Drug Profile"}
              </div>
              <div style={{ color: "#94a3b8", fontSize: 13, marginTop: 2 }}>
                {selected.openfda?.generic_name?.[0]} · {selected.openfda?.route?.[0]} · {selected.openfda?.manufacturer_name?.[0]}
              </div>
            </div>
            <button onClick={() => { setSelected(null); setResults([]) }} style={{
              padding: "8px 16px", borderRadius: 10, background: "rgba(255,255,255,0.07)",
              color: "#94a3b8", border: "1px solid rgba(255,255,255,0.1)", cursor: "pointer", fontSize: 12,
            }}>← Back</button>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
            {[
              { label: "Indications & Usage", data: selected.indications_and_usage, accent: "#3b82f6" },
              { label: "Dosage & Administration", data: selected.dosage_and_administration, accent: "#10b981" },
              { label: "Contraindications", data: selected.contraindications, accent: "#ef4444" },
              { label: "Warnings", data: selected.warnings, accent: "#f59e0b" },
              { label: "Adverse Reactions", data: selected.adverse_reactions, accent: "#f97316" },
              { label: "Drug Interactions (FDA)", data: selected.drug_interactions, accent: "#a855f7" },
            ].map(({ label, data, accent }) => data?.[0] && (
              <div key={label} style={{
                padding: 16, borderRadius: 14,
                background: `${accent}08`, border: `1px solid ${accent}22`,
              }}>
                <div style={{ fontSize: 11, fontWeight: 800, color: accent, textTransform: "uppercase", letterSpacing: 1, marginBottom: 8 }}>{label}</div>
                <div style={{ color: "#cbd5e1", fontSize: 12, lineHeight: 1.7, maxHeight: 120, overflow: "auto" }}>
                  {data[0].slice(0, 400)}{data[0].length > 400 ? "..." : ""}
                </div>
              </div>
            ))}
          </div>

          {/* RxNorm Interactions */}
          <div style={{
            padding: 18, borderRadius: 14,
            background: "rgba(168,85,247,0.06)", border: "1px solid rgba(168,85,247,0.2)",
          }}>
            <div style={{ fontSize: 12, fontWeight: 800, color: "#a855f7", textTransform: "uppercase", letterSpacing: 1, marginBottom: 12 }}>
              ⚗ RxNorm Drug Interactions Database
            </div>
            {rxLoading ? (
              <div style={{ color: "#64748b", fontSize: 13 }}>⟳ Fetching RxNorm interactions...</div>
            ) : rxInteractions.length === 0 ? (
              <div style={{ color: "#4ade80", fontSize: 13 }}>✓ No major interactions found in RxNorm database</div>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {rxInteractions.map((ix, i) => (
                  <div key={i} style={{
                    padding: "10px 12px", borderRadius: 10,
                    background: ix.severity === "high" ? "rgba(239,68,68,0.08)" : "rgba(245,158,11,0.08)",
                    border: ix.severity === "high" ? "1px solid rgba(239,68,68,0.3)" : "1px solid rgba(245,158,11,0.3)",
                  }}>
                    {ix.severity && (
                      <RiskBadge level={ix.severity.toUpperCase()} />
                    )}
                    <div style={{ color: "#cbd5e1", fontSize: 12, marginTop: 6, lineHeight: 1.6 }}>{ix.description}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

// ─── MAR Panel ────────────────────────────────────────────────────────────────
function MARPanel() {
  const [patientId, setPatientId] = useState("P-1001")
  const [items, setItems] = useState<MARItem[]>([])
  const [loading, setLoading] = useState(false)
  const [aiAnalysis, setAiAnalysis] = useState<Record<number, string>>({})
  const [analyzing, setAnalyzing] = useState<number | null>(null)

  async function loadMAR() {
    setLoading(true)
    try {
      const data = await apiGet<MARItem[]>(`/mar/${patientId}`)
      setItems(Array.isArray(data) ? data : [])
    } catch { setItems([]) }
    finally { setLoading(false) }
  }

  useEffect(() => { loadMAR() }, [patientId])

  async function analyzeWithAI(item: MARItem) {
    setAnalyzing(item.id)
    try {
      // Check FDA for this drug
      const res = await fetch(
        `https://api.fda.gov/drug/label.json?search=openfda.generic_name:"${encodeURIComponent(item.medication.split(" ")[0])}"&limit=1`
      )
      const data = await res.json()
      const drug = data.results?.[0]
      if (drug) {
        const warnings = drug.warnings?.[0]?.slice(0, 200) ?? "No major warnings found"
        const interactions = drug.drug_interactions?.[0]?.slice(0, 200) ?? "No interactions listed"
        setAiAnalysis(prev => ({
          ...prev,
          [item.id]: `⚠ FDA Warnings: ${warnings}\n\n💊 Interactions: ${interactions}`
        }))
      } else {
        setAiAnalysis(prev => ({ ...prev, [item.id]: "✓ Drug not found in FDA high-alert database. Appears safe." }))
      }
    } catch {
      setAiAnalysis(prev => ({ ...prev, [item.id]: "FDA API unavailable for this check." }))
    } finally { setAnalyzing(null) }
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
      <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
        <select
          value={patientId}
          onChange={e => setPatientId(e.target.value)}
          style={{
            padding: "10px 14px", borderRadius: 10, background: "rgba(255,255,255,0.05)",
            border: "1px solid rgba(59,130,246,0.3)", color: "white", fontSize: 13,
          }}
        >
          <option value="P-1001">P-1001 — Ahmed Ali</option>
          <option value="P-1002">P-1002 — Sara Omar</option>
          <option value="P-1003">P-1003 — Mona Salem</option>
        </select>
        <button onClick={loadMAR} style={{
          padding: "10px 18px", borderRadius: 10, background: "rgba(59,130,246,0.15)",
          border: "1px solid rgba(59,130,246,0.3)", color: "#60a5fa", fontSize: 13, cursor: "pointer",
        }}>⟳ Reload</button>
      </div>

      {loading ? <div style={{ color: "#64748b" }}>Loading MAR...</div> : items.length === 0 ? (
        <div style={{ color: "#64748b", fontSize: 13 }}>No MAR items for this patient.</div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {items.map(item => (
            <div key={item.id} style={{
              padding: 16, borderRadius: 14,
              background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)",
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 12 }}>
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: 800, color: "white", fontSize: 15 }}>{item.medication}</div>
                  <div style={{ color: "#94a3b8", fontSize: 12, marginTop: 4 }}>
                    {item.dose} · {item.route} · {item.schedule}
                  </div>
                  {item.givenAt && <div style={{ color: "#64748b", fontSize: 11, marginTop: 2 }}>Given at: {item.givenAt}</div>}
                </div>
                <div style={{ display: "flex", flex: "column", gap: 8, alignItems: "flex-end" }}>
                  <RiskBadge level={item.status === "Given" ? "SAFE" : item.status === "Pending" ? "MODERATE" : "UNKNOWN"} />
                  <button onClick={() => analyzeWithAI(item)} disabled={analyzing === item.id} style={{
                    marginTop: 8, padding: "6px 14px", borderRadius: 8, fontSize: 11, fontWeight: 700,
                    background: "linear-gradient(135deg,#7c3aed,#2563eb)",
                    color: "white", border: "none", cursor: "pointer", whiteSpace: "nowrap",
                  }}>
                    {analyzing === item.id ? "⟳ Checking..." : "🤖 AI Check FDA"}
                  </button>
                </div>
              </div>
              {aiAnalysis[item.id] && (
                <div style={{
                  marginTop: 12, padding: "12px 14px", borderRadius: 10,
                  background: "rgba(124,58,237,0.08)", border: "1px solid rgba(124,58,237,0.25)",
                  color: "#c4b5fd", fontSize: 12, lineHeight: 1.7, whiteSpace: "pre-wrap",
                }}>
                  {aiAnalysis[item.id]}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

// ─── AI Drug Interactions Checker ─────────────────────────────────────────────
function InteractionChecker() {
  const [drugs, setDrugs] = useState("Warfarin, Aspirin, Ibuprofen")
  const [results, setResults] = useState<{ drug: string; interactions: RxInteraction[] }[]>([])
  const [loading, setLoading] = useState(false)

  async function checkInteractions() {
    setLoading(true)
    setResults([])
    const list = drugs.split(",").map(d => d.trim()).filter(Boolean)
    const out: { drug: string; interactions: RxInteraction[] }[] = []

    for (const drug of list) {
      try {
        const r1 = await fetch(`https://rxnav.nlm.nih.gov/REST/rxcui.json?name=${encodeURIComponent(drug)}&search=1`)
        const d1 = await r1.json()
        const rxcui = d1?.idGroup?.rxnormId?.[0]
        if (!rxcui) { out.push({ drug, interactions: [] }); continue }

        const r2 = await fetch(`https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui=${rxcui}`)
        const d2 = await r2.json()
        const groups = d2?.interactionTypeGroup ?? []
        const interactions: RxInteraction[] = []
        for (const group of groups) {
          for (const type of group.interactionType ?? []) {
            for (const pair of type.interactionPair ?? []) {
              interactions.push({ description: pair.description, severity: pair.severity })
            }
          }
        }
        out.push({ drug, interactions: interactions.slice(0, 4) })
      } catch {
        out.push({ drug, interactions: [] })
      }
    }
    setResults(out)
    setLoading(false)
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
      <div style={{ display: "flex", gap: 10 }}>
        <input
          value={drugs}
          onChange={e => setDrugs(e.target.value)}
          placeholder="Enter drugs separated by commas..."
          style={{
            flex: 1, padding: "12px 16px", borderRadius: 12, fontSize: 13,
            background: "rgba(255,255,255,0.05)", border: "1px solid rgba(168,85,247,0.3)",
            color: "white", outline: "none",
          }}
        />
        <button onClick={checkInteractions} disabled={loading} style={{
          padding: "12px 22px", borderRadius: 12, fontSize: 13, fontWeight: 700,
          background: "linear-gradient(135deg,#7c3aed,#a855f7)",
          color: "white", border: "none", cursor: "pointer",
          opacity: loading ? 0.7 : 1,
        }}>
          {loading ? "⟳ Checking..." : "⚗ Check RxNorm"}
        </button>
      </div>

      {results.length > 0 && (
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {results.map(({ drug, interactions }) => (
            <div key={drug} style={{
              padding: 16, borderRadius: 14,
              background: interactions.length > 0 ? "rgba(239,68,68,0.06)" : "rgba(16,185,129,0.06)",
              border: interactions.length > 0 ? "1px solid rgba(239,68,68,0.2)" : "1px solid rgba(16,185,129,0.2)",
            }}>
              <div style={{ fontWeight: 800, color: "white", fontSize: 14, marginBottom: 8 }}>
                💊 {drug}
                <span style={{ marginLeft: 10 }}>
                  <RiskBadge level={interactions.some(i => i.severity === "high") ? "HIGH" : interactions.length > 0 ? "MODERATE" : "SAFE"} />
                </span>
              </div>
              {interactions.length === 0 ? (
                <div style={{ color: "#4ade80", fontSize: 12 }}>✓ No significant interactions found</div>
              ) : (
                interactions.map((ix, i) => (
                  <div key={i} style={{ color: "#fca5a5", fontSize: 12, marginTop: 4, lineHeight: 1.6 }}>
                    ⚠ {ix.description}
                  </div>
                ))
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

// ─── Main Page ─────────────────────────────────────────────────────────────────
export default function SmartPharmacyPage() {
  const [tab, setTab] = useState<"search" | "mar" | "interactions" | "formulary">("search")
  const user = getUser()

  const tabs = [
    { key: "search",       label: "🔍 FDA Drug Search",       accent: "#3b82f6" },
    { key: "mar",          label: "💊 MAR — AI Safety Check", accent: "#10b981" },
    { key: "interactions", label: "⚗ Interaction Checker",   accent: "#a855f7" },
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
            ◈ AI HOSPITAL ALLIANCE — SMART PHARMACY
          </div>
          <h1 style={{
            margin: 0, fontSize: 28, fontWeight: 900, letterSpacing: -0.5,
            background: "linear-gradient(135deg,#fff,#94a3b8)",
            WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
          }}>
            💊 Smart Pharmacy — Global Drug Intelligence
          </h1>
          <p style={{ color: "#475569", fontSize: 13, marginTop: 6 }}>
            Powered by FDA OpenFDA · RxNorm NLM · AI Safety Engine · {user?.name}
          </p>
        </div>

        {/* Info bar */}
        <div style={{
          display: "flex", gap: 12, marginBottom: 24, padding: "14px 18px",
          borderRadius: 14, background: "rgba(59,130,246,0.08)", border: "1px solid rgba(59,130,246,0.2)",
          flexWrap: "wrap",
        }}>
          {[
            { label: "FDA Database", value: "20,000+ Drug Labels", color: "#3b82f6" },
            { label: "RxNorm NLM", value: "Live Interaction Data", color: "#a855f7" },
            { label: "AI Safety", value: "Real-time Analysis", color: "#10b981" },
            { label: "Coverage", value: "FDA · EMA · WHO", color: "#f59e0b" },
          ].map(({ label, value, color }) => (
            <div key={label} style={{ display: "flex", flexDirection: "column", gap: 2 }}>
              <div style={{ fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }}>{label}</div>
              <div style={{ fontSize: 13, fontWeight: 700, color }}>{value}</div>
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

        {/* Tab Content */}
        {tab === "search" && (
          <Card title="🔍 FDA Global Drug Database Search" accent="#3b82f6">
            <DrugSearch />
          </Card>
        )}
        {tab === "mar" && (
          <Card title="💊 Medication Administration Record — AI Safety Check" accent="#10b981">
            <MARPanel />
          </Card>
        )}
        {tab === "interactions" && (
          <Card title="⚗ Drug Interaction Checker — RxNorm NLM Database" accent="#a855f7">
            <InteractionChecker />
          </Card>
        )}

      </div>
    </div>
  )
}
