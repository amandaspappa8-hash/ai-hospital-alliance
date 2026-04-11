import { useEffect, useState } from "react"
import { useSearchParams } from "react-router-dom"
import { apiDelete, apiGet, apiPost, apiPut } from "@/lib/api"

type MARItem = {
  id: number
  medication: string
  dose: string
  route: string
  schedule: string
  status: string
  givenAt: string
  pharmacistNote?: string
  reviewedAt?: string
}

type DrugIntelResponse = {
  query: string
  rxnorm?: any
  openfda?: any
}

type InteractionFinding = {
  severity: string
  type: string
  title: string
  detail: string
}

type InteractionResponse = {
  patientId?: string
  count: number
  medications: string[]
  findings: InteractionFinding[]
  summary: {
    has_findings: boolean
    high_risk_count: number
    moderate_risk_count: number
  }
}

type DoseSafetyResponse = {
  patientId?: string
  age?: number | null
  count: number
  medications: string[]
  findings: InteractionFinding[]
  summary: {
    has_findings: boolean
    high_risk_count: number
    moderate_risk_count: number
  }
}

type RecommendationItem = {
  priority: string
  type: string
  title: string
  detail: string
  suggested_action: string
}


type ReconciliationFinding = {
  severity: string
  type: string
  title: string
  detail: string
}

type ReconciliationResponse = {
  patientId?: string
  homeMeds: string[]
  admissionMeds: string[]
  dischargeMeds: string[]
  findings: ReconciliationFinding[]
  summary: {
    high_risk_count: number
    moderate_risk_count: number
    has_findings: boolean
  }
}

type RecommendationResponse = {
  patientId?: string
  age?: number | null
  count: number
  medications: string[]
  recommendations: RecommendationItem[]
  summary: {
    has_recommendations: boolean
    high_priority_count: number
    moderate_priority_count: number
    low_priority_count: number
  }
}

export default function SmartPharmacyPage() {
  const [searchParams] = useSearchParams()
  const patientId = searchParams.get("patientId") ?? "P-1001"

  const [items, setItems] = useState<MARItem[]>([])
  const [medication, setMedication] = useState("")
  const [dose, setDose] = useState("")
  const [route, setRoute] = useState("")
  const [schedule, setSchedule] = useState("")
  const [search, setSearch] = useState("")
  const [intel, setIntel] = useState<DrugIntelResponse | null>(null)
  const [intelError, setIntelError] = useState("")
  const [interactionData, setInteractionData] = useState<InteractionResponse | null>(null)
  const [interactionError, setInteractionError] = useState("")
  const [doseSafety, setDoseSafety] = useState<DoseSafetyResponse | null>(null)
  const [doseSafetyError, setDoseSafetyError] = useState("")
  const [recommendations, setRecommendations] = useState<RecommendationResponse | null>(null)
  const [recommendationError, setRecommendationError] = useState("")
  const [patientAge, setPatientAge] = useState("45")
  const [reconciliation, setReconciliation] = useState<ReconciliationResponse | null>(null)
  const [reconciliationError, setReconciliationError] = useState("")
  const [noteText, setNoteText] = useState("")
  const [selectedItemId, setSelectedItemId] = useState<number | null>(null)

  const totalHighRisk =
    (interactionData?.summary.high_risk_count || 0) +
    (doseSafety?.summary.high_risk_count || 0)

  const totalModerateRisk =
    (interactionData?.summary.moderate_risk_count || 0) +
    (doseSafety?.summary.moderate_risk_count || 0)

  const hasCriticalRisk = totalHighRisk > 0

  function load() {
    apiGet<MARItem[]>(`/mar/${patientId}`).then((data) => {
      setItems(data)
      loadInteractions()
      loadDoseSafety()
      loadRecommendations()
      loadReconciliation()
    })
  }

  function loadInteractions() {
    apiGet<InteractionResponse>(`/drug-intel/interactions/${patientId}`)
      .then(setInteractionData)
      .catch((err) => {
        console.error(err)
        setInteractionError("Drug interaction analysis failed")
      })
  }

  function loadDoseSafety() {
    apiGet<DoseSafetyResponse>(`/drug-intel/dose-safety/${patientId}?age=${encodeURIComponent(patientAge || "45")}`)
      .then(setDoseSafety)
      .catch((err) => {
        console.error(err)
        setDoseSafetyError("Dose safety analysis failed")
      })
  }

  function loadRecommendations() {
    apiGet<RecommendationResponse>(`/drug-intel/recommendations/${patientId}?age=${encodeURIComponent(patientAge || "45")}`)
      .then(setRecommendations)
      .catch((err) => {
        console.error(err)
        setRecommendationError("Medication recommendation analysis failed")
      })
  }

  function loadReconciliation() {
    apiGet<ReconciliationResponse>(`/drug-intel/reconciliation/${patientId}`)
      .then(setReconciliation)
      .catch((err) => {
        console.error(err)
        setReconciliationError("Medication reconciliation failed")
      })
  }

  useEffect(() => {
    load()
  }, [patientId])

  function createItem() {
    apiPost(`/mar/${patientId}`, {
      medication,
      dose,
      route,
      schedule,
    }).then(() => {
      setMedication("")
      setDose("")
      setRoute("")
      setSchedule("")
      load()
    })
  }

  function give(id: number) {
    apiPut(`/mar/${patientId}/${id}/status`, {
      status: "Given",
      givenAt: new Date().toLocaleTimeString(),
    }).then(load)
  }

  function remove(id: number) {
    apiDelete(`/mar/${patientId}/${id}`).then(load)
  }

  function pharmacistReview(status: string) {
    if (!selectedItemId) return
    apiPut(`/mar/${patientId}/${selectedItemId}/pharmacist-review`, {
      status,
      note: noteText,
    }).then(() => {
      setNoteText("")
      setSelectedItemId(null)
      load()
    })
  }

  function searchDrug() {
    if (!search.trim()) return
    setIntelError("")
    apiGet<DrugIntelResponse>(`/drug-intel/search?q=${encodeURIComponent(search.trim())}`)
      .then(setIntel)
      .catch((err) => {
        console.error(err)
        setIntelError("Drug intelligence search failed")
      })
  }

  const rxConcepts =
    intel?.rxnorm?.drugGroup?.conceptGroup?.flatMap((group: any) => group.conceptProperties || []) || []

  const fdaResult = intel?.openfda?.results?.[0] || null

  const brandName = fdaResult?.openfda?.brand_name?.join(", ") || "-"
  const genericName = fdaResult?.openfda?.generic_name?.join(", ") || "-"
  const routeNames = fdaResult?.openfda?.route?.join(", ") || "-"
  const dosageForm = fdaResult?.openfda?.dosage_form?.join(", ") || "-"
  const manufacturer = fdaResult?.openfda?.manufacturer_name?.join(", ") || "-"
  const activeIngredient = fdaResult?.active_ingredient?.[0] || "-"
  const indications = fdaResult?.indications_and_usage?.[0] || "-"
  const dosageInfo = fdaResult?.dosage_and_administration?.[0] || "-"
  const warnings = fdaResult?.warnings?.[0] || "-"
  const doNotUse = fdaResult?.do_not_use?.[0] || "-"
  const askDoctor = fdaResult?.ask_doctor?.[0] || "-"
  const askPharmacist = fdaResult?.ask_doctor_or_pharmacist?.[0] || "-"
  const stopUse = fdaResult?.stop_use?.[0] || "-"

  return (
    <div style={{ padding: 30, color: "white", background: "#0b1220", minHeight: "100vh" }}>
      <h1 style={{ fontSize: 30, marginBottom: 20 }}>Smart Pharmacy</h1>

      <div
        style={{
          border: hasCriticalRisk ? "1px solid #ef4444" : "1px solid #f59e0b",
          background: hasCriticalRisk ? "rgba(127,29,29,0.35)" : "rgba(120,53,15,0.35)",
          borderRadius: 16,
          padding: 16,
          marginBottom: 20,
        }}
      >
        <div style={{ fontSize: 20, fontWeight: 800 }}>
          Clinical Pharmacy Risk Dashboard
        </div>

        <div style={{ marginTop: 10 }}>
          High Risk Findings: <strong>{totalHighRisk}</strong>
        </div>
        <div>
          Moderate Risk Findings: <strong>{totalModerateRisk}</strong>
        </div>

        <div style={{ marginTop: 12, color: "#facc15", fontWeight: 700 }}>
          {hasCriticalRisk
            ? "Immediate pharmacist / physician review recommended."
            : "No critical risk detected, but review is still recommended."}
        </div>
      </div>

      <div style={{ display: "grid", gap: 20 }}>
        <div style={card}>
          <h2 style={title}>Pharmacist Action Center</h2>

          <div style={{ display: "flex", gap: 12, flexWrap: "wrap", alignItems: "center" }}>
            <div style={badge}>Patient ID: {patientId}</div>
            <input
              style={{ ...input, maxWidth: 160 }}
              placeholder="Patient age"
              value={patientAge}
              onChange={(e) => setPatientAge(e.target.value)}
            />
            <button
              style={button}
              onClick={() => {
                loadDoseSafety()
                loadRecommendations()
              }}
            >
              Refresh Clinical Review
            </button>
          </div>

          <div style={{ marginTop: 16, display: "grid", gap: 10 }}>
            <select
              value={selectedItemId ?? ""}
              onChange={(e) => setSelectedItemId(e.target.value ? Number(e.target.value) : null)}
              style={input}
            >
              <option value="">Select medication for pharmacist action</option>
              {items.map((item) => (
                <option key={item.id} value={item.id}>
                  {item.medication} — {item.status}
                </option>
              ))}
            </select>

            <textarea
              style={{ ...input, minHeight: 110, resize: "vertical" }}
              placeholder="Pharmacist note"
              value={noteText}
              onChange={(e) => setNoteText(e.target.value)}
            />

            <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
              <button style={reviewButton} onClick={() => pharmacistReview("Reviewed")}>
                Review Medication Plan
              </button>
              <button style={holdButton} onClick={() => pharmacistReview("Held")}>
                Hold Medication
              </button>
              <button style={pharmacistButton} onClick={() => pharmacistReview("Needs Pharmacist Review")}>
                Needs Pharmacist Review
              </button>
            </div>
          </div>
        </div>

        <div style={card}>
          <h2 style={title}>Smart Medication Recommendation Layer</h2>

          {recommendationError ? <div style={{ color: "#fca5a5", marginBottom: 12 }}>{recommendationError}</div> : null}

          {recommendations ? (
            <div style={{ display: "grid", gap: 14 }}>
              <div style={section}>
                <div style={subTitle}>Recommendation Summary</div>
                <div style={row}>High priority: {recommendations.summary.high_priority_count}</div>
                <div style={row}>Moderate priority: {recommendations.summary.moderate_priority_count}</div>
                <div style={row}>Low priority: {recommendations.summary.low_priority_count}</div>
              </div>

              <div style={section}>
                <div style={subTitle}>Recommended Actions</div>
                {recommendations.recommendations.length === 0 ? (
                  <div style={{ opacity: 0.8 }}>No recommendations available</div>
                ) : (
                  recommendations.recommendations.map((item, idx) => (
                    <div
                      key={idx}
                      style={{
                        ...row,
                        borderColor:
                          item.priority === "high" ? "#ef4444" :
                          item.priority === "moderate" ? "#f59e0b" : "#243041",
                        background:
                          item.priority === "high" ? "rgba(127,29,29,0.22)" :
                          item.priority === "moderate" ? "rgba(120,53,15,0.22)" : "#0f172a",
                      }}
                    >
                      <div style={{ fontWeight: 800 }}>{item.title}</div>
                      <div style={{ marginTop: 6 }}>{item.detail}</div>
                      <div style={{ marginTop: 8, color: "#93c5fd" }}>
                        Suggested action: {item.suggested_action}
                      </div>
                      <div style={{ marginTop: 6, opacity: 0.8 }}>
                        Priority: {item.priority} • Type: {item.type}
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          ) : (
            <div style={{ opacity: 0.8 }}>Medication recommendations not loaded yet</div>
          )}
        </div>


        <div style={card}>
          <h2 style={title}>Medication Reconciliation Layer</h2>

          {reconciliationError ? (
            <div style={{ color: "#fca5a5", marginBottom: 12 }}>{reconciliationError}</div>
          ) : null}

          {reconciliation ? (
            <div style={{ display: "grid", gap: 14 }}>
              <div style={section}>
                <div style={subTitle}>Reconciliation Summary</div>
                <div style={row}>High risk findings: {reconciliation.summary.high_risk_count}</div>
                <div style={row}>Moderate risk findings: {reconciliation.summary.moderate_risk_count}</div>
                <div style={row}>Has findings: {reconciliation.summary.has_findings ? "Yes" : "No"}</div>
              </div>

              <div style={section}>
                <div style={subTitle}>Home Medications</div>
                {reconciliation.homeMeds.length === 0 ? (
                  <div style={{ opacity: 0.8 }}>No home medications</div>
                ) : (
                  reconciliation.homeMeds.map((med, idx) => <div key={idx} style={row}>{med}</div>)
                )}
              </div>

              <div style={section}>
                <div style={subTitle}>Admission Medications</div>
                {reconciliation.admissionMeds.length === 0 ? (
                  <div style={{ opacity: 0.8 }}>No admission medications</div>
                ) : (
                  reconciliation.admissionMeds.map((med, idx) => <div key={idx} style={row}>{med}</div>)
                )}
              </div>

              <div style={section}>
                <div style={subTitle}>Discharge Medications</div>
                {reconciliation.dischargeMeds.length === 0 ? (
                  <div style={{ opacity: 0.8 }}>No discharge medications</div>
                ) : (
                  reconciliation.dischargeMeds.map((med, idx) => <div key={idx} style={row}>{med}</div>)
                )}
              </div>

              <div style={section}>
                <div style={subTitle}>Reconciliation Alerts</div>
                {reconciliation.findings.length === 0 ? (
                  <div style={{ opacity: 0.8 }}>No reconciliation alerts detected</div>
                ) : (
                  reconciliation.findings.map((finding, idx) => (
                    <div
                      key={idx}
                      style={{
                        ...row,
                        borderColor: finding.severity === "high" ? "#ef4444" : "#f59e0b",
                        background: finding.severity === "high" ? "rgba(127,29,29,0.22)" : "rgba(120,53,15,0.22)",
                      }}
                    >
                      <div style={{ fontWeight: 800 }}>{finding.title}</div>
                      <div style={{ marginTop: 6 }}>{finding.detail}</div>
                      <div style={{ marginTop: 6, opacity: 0.8 }}>
                        Severity: {finding.severity} • Type: {finding.type}
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          ) : (
            <div style={{ opacity: 0.8 }}>Medication reconciliation not loaded yet</div>
          )}
        </div>

        <div style={card}>
          <h2 style={title}>Drug Intelligence Engine</h2>

          <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
            <input
              style={input}
              placeholder="Search medication name"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            <button style={button} onClick={searchDrug}>Search</button>
          </div>

          {intelError ? <div style={{ color: "#fca5a5", marginTop: 12 }}>{intelError}</div> : null}

          {intel ? (
            <div style={{ marginTop: 20, display: "grid", gap: 18 }}>
              <div style={section}>
                <div style={subTitle}>RxNorm Standard Matches</div>
                {rxConcepts.length === 0 ? (
                  <div style={{ opacity: 0.8 }}>No RxNorm matches</div>
                ) : (
                  rxConcepts.slice(0, 10).map((item: any, idx: number) => (
                    <div key={idx} style={row}>
                      <strong>{item.name || "-"}</strong>
                      <div>RXCUI: {item.rxcui || "-"}</div>
                      <div>TTY: {item.tty || "-"}</div>
                    </div>
                  ))
                )}
              </div>

              <div style={section}>
                <div style={subTitle}>Official Drug Snapshot</div>
                <div style={row}><strong>Brand:</strong> {brandName}</div>
                <div style={row}><strong>Generic:</strong> {genericName}</div>
                <div style={row}><strong>Route:</strong> {routeNames}</div>
                <div style={row}><strong>Dosage Form:</strong> {dosageForm}</div>
                <div style={row}><strong>Manufacturer:</strong> {manufacturer}</div>
                <div style={row}><strong>Active Ingredient:</strong> {activeIngredient}</div>
              </div>

              <div style={section}>
                <div style={subTitle}>Indications</div>
                <div style={textBlock}>{indications}</div>
              </div>

              <div style={section}>
                <div style={subTitle}>Dose Guidance</div>
                <div style={textBlock}>{dosageInfo}</div>
              </div>

              <div style={section}>
                <div style={subTitle}>Warnings</div>
                <div style={textBlock}>{warnings}</div>
              </div>

              <div style={section}>
                <div style={subTitle}>Contraindications / Do Not Use</div>
                <div style={textBlock}>{doNotUse}</div>
              </div>

              <div style={section}>
                <div style={subTitle}>Ask Doctor Before Use</div>
                <div style={textBlock}>{askDoctor}</div>
              </div>

              <div style={section}>
                <div style={subTitle}>Ask Doctor or Pharmacist</div>
                <div style={textBlock}>{askPharmacist}</div>
              </div>

              <div style={section}>
                <div style={subTitle}>Stop Use</div>
                <div style={textBlock}>{stopUse}</div>
              </div>
            </div>
          ) : null}
        </div>

        <div style={card}>
          <h2 style={title}>Unsafe Combinations</h2>

          <div style={{ display: "grid", gap: 12 }}>
            {interactionData?.findings?.length ? (
              interactionData.findings.map((finding, idx) => (
                <div
                  key={idx}
                  style={{
                    ...row,
                    borderColor: finding.severity === "high" ? "#ef4444" : "#f59e0b",
                    background: finding.severity === "high" ? "rgba(127,29,29,0.22)" : "rgba(120,53,15,0.22)",
                  }}
                >
                  <div style={{ fontWeight: 800 }}>{finding.title}</div>
                  <div style={{ marginTop: 6 }}>{finding.detail}</div>
                  <div style={{ marginTop: 6, opacity: 0.8 }}>
                    Severity: {finding.severity} • Type: {finding.type}
                  </div>
                </div>
              ))
            ) : (
              <div style={{ opacity: 0.8 }}>No unsafe combinations detected</div>
            )}
          </div>
        </div>

        <div style={card}>
          <h2 style={title}>Medication Administration Record</h2>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(4, minmax(0, 1fr)) auto", gap: 10 }}>
            <input style={input} placeholder="Medication" value={medication} onChange={e => setMedication(e.target.value)} />
            <input style={input} placeholder="Dose" value={dose} onChange={e => setDose(e.target.value)} />
            <input style={input} placeholder="Route" value={route} onChange={e => setRoute(e.target.value)} />
            <input style={input} placeholder="Schedule" value={schedule} onChange={e => setSchedule(e.target.value)} />
            <button style={button} onClick={createItem}>Add</button>
          </div>

          <div style={{ marginTop: 18, display: "grid", gap: 10 }}>
            {items.map((i) => (
              <div key={i.id} style={row}>
                <div><strong>{i.medication}</strong></div>
                <div>Dose: {i.dose}</div>
                <div>Route: {i.route}</div>
                <div>Schedule: {i.schedule}</div>
                <div>Status: {i.status}</div>
                <div>Given At: {i.givenAt || "-"}</div>
                <div>Reviewed At: {i.reviewedAt || "-"}</div>
                <div>Pharmacist Note: {i.pharmacistNote || "-"}</div>
                <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
                  <button style={miniButton} onClick={() => give(i.id)}>Give</button>
                  <button style={dangerButton} onClick={() => remove(i.id)}>Delete</button>
                </div>
              </div>
            ))}

            {items.length === 0 ? <div style={{ opacity: 0.8 }}>No MAR items</div> : null}
          </div>
        </div>
      </div>
    </div>
  )
}

const card: React.CSSProperties = {
  border: "1px solid #243041",
  borderRadius: 16,
  padding: 18,
  background: "#111827",
}

const section: React.CSSProperties = {
  border: "1px solid #243041",
  borderRadius: 12,
  padding: 14,
  background: "#0f172a",
}

const badge: React.CSSProperties = {
  padding: "10px 14px",
  borderRadius: 10,
  background: "#0f172a",
  border: "1px solid #334155",
  color: "#93c5fd",
  fontWeight: 700,
}

const title: React.CSSProperties = {
  margin: "0 0 12px 0",
  fontSize: 22,
}

const subTitle: React.CSSProperties = {
  fontSize: 16,
  fontWeight: 700,
  marginBottom: 10,
  color: "#93c5fd",
}

const input: React.CSSProperties = {
  padding: "12px 14px",
  borderRadius: 10,
  border: "1px solid #334155",
  background: "#0f172a",
  color: "white",
}

const button: React.CSSProperties = {
  padding: "12px 16px",
  borderRadius: 10,
  border: "none",
  background: "#0ea5e9",
  color: "white",
  cursor: "pointer",
}

const miniButton: React.CSSProperties = {
  padding: "8px 12px",
  borderRadius: 8,
  border: "none",
  background: "#22c55e",
  color: "white",
  cursor: "pointer",
}

const dangerButton: React.CSSProperties = {
  padding: "8px 12px",
  borderRadius: 8,
  border: "none",
  background: "#ef4444",
  color: "white",
  cursor: "pointer",
}

const reviewButton: React.CSSProperties = {
  padding: "10px 14px",
  borderRadius: 10,
  border: "none",
  background: "#0ea5e9",
  color: "white",
  cursor: "pointer",
  fontWeight: 700,
}

const holdButton: React.CSSProperties = {
  padding: "10px 14px",
  borderRadius: 10,
  border: "none",
  background: "#ef4444",
  color: "white",
  cursor: "pointer",
  fontWeight: 700,
}

const pharmacistButton: React.CSSProperties = {
  padding: "10px 14px",
  borderRadius: 10,
  border: "none",
  background: "#f59e0b",
  color: "white",
  cursor: "pointer",
  fontWeight: 700,
}

const row: React.CSSProperties = {
  border: "1px solid #243041",
  borderRadius: 12,
  padding: 12,
  background: "#0f172a",
}

const textBlock: React.CSSProperties = {
  whiteSpace: "pre-wrap",
  lineHeight: 1.7,
  color: "#e5e7eb",
}
