import { useEffect, useMemo, useState } from "react"
import { apiGet, apiPost } from "@/lib/api"

type Patient = {
  id: string
  name: string
  age?: number
  gender?: string
  department?: string
  status?: string
  condition?: string
}

type LabOrder = {
  id: string
  patientId: string
  patientName: string
  section: string
  tests: string[]
  priority: string
  status: string
  result?: string
}

export default function LabsPage() {
  const [patients, setPatients] = useState<Patient[]>([])
  const [selectedPatientId, setSelectedPatientId] = useState("")
  const [orders, setOrders] = useState<LabOrder[]>([])
  const [catalog, setCatalog] = useState<Record<string, string[]>>({})
  const [error, setError] = useState("")
  const [successMessage, setSuccessMessage] = useState("")

  const [form, setForm] = useState({
    section: "classical",
    tests: "",
    priority: "Routine",
  })
  const [selectedTests, setSelectedTests] = useState<string[]>([])
  const [labSearch, setLabSearch] = useState("")
  const [activeTab, setActiveTab] = useState<"orders" | "catalog" | "selected" | "results">("catalog")
  const [ordersStatusFilter, setOrdersStatusFilter] = useState<"all" | "Pending" | "Completed">("all")
  const [resultsFilter, setResultsFilter] = useState<"all" | "has_result" | "no_result">("all")
  const [resultsSearch, setResultsSearch] = useState("")

  useEffect(() => {
    setForm((prev) => ({
      ...prev,
      tests: selectedTests.join(", "),
    }))
  }, [selectedTests])

  useEffect(() => {
    if (!successMessage) return
    const t = setTimeout(() => setSuccessMessage(""), 2500)
    return () => clearTimeout(t)
  }, [successMessage])

  useEffect(() => {
    Promise.all([apiGet("/patients"), apiGet("/labs/catalog"), apiGet("/labs/orders")])
      .then(([p, c, o]) => {
        const patientsList = Array.isArray(p) ? p : []
        setPatients(patientsList)
        if (patientsList.length > 0) setSelectedPatientId(patientsList[0].id)
        setCatalog((c || {}) as Record<string, string[]>)
        setOrders(Array.isArray(o) ? o : [])
      })
      .catch(() => setError("Failed to load laboratory data"))
  }, [])

  const filteredCatalogTests = useMemo(() => {
    const items = catalog[form.section] || []
    const q = labSearch.trim().toLowerCase()
    if (!q) return items
    return items.filter((test) => test.toLowerCase().includes(q))
  }, [catalog, form.section, labSearch])

  const selectedPatient = useMemo(
    () => patients.find((p) => p.id === selectedPatientId),
    [patients, selectedPatientId]
  )

  const filteredOrders = useMemo(
    () => orders.filter((o) => !selectedPatientId || o.patientId === selectedPatientId),
    [orders, selectedPatientId]
  )
  const totalOrdersCount = filteredOrders.length
  const pendingOrdersCount = filteredOrders.filter((order) => order.status === "Pending").length
  const completedOrdersCount = filteredOrders.filter((order) => order.status === "Completed").length
  const resultsAvailableCount = filteredOrders.filter((order) => order.result).length

  const filteredOrdersByStatus = useMemo(() => {
    if (ordersStatusFilter === "all") return filteredOrders
    return filteredOrders.filter((order) => order.status === ordersStatusFilter)
  }, [filteredOrders, ordersStatusFilter])

  const filteredResults = useMemo(() => {
    let items = [...filteredOrders]

    if (resultsFilter === "has_result") {
      items = items.filter((order) => order.result)
    } else if (resultsFilter === "no_result") {
      items = items.filter((order) => !order.result)
    }

    const q = resultsSearch.trim().toLowerCase()
    if (q) {
      items = items.filter((order) =>
        order.tests.some((test) => test.toLowerCase().includes(q))
      )
    }

    return items
  }, [filteredOrders, resultsFilter, resultsSearch])


  const copySelectedTests = async () => {
    try {
      if (selectedTests.length === 0) return
      await navigator.clipboard.writeText(selectedTests.join(", "))
      setSuccessMessage("Selected tests copied to clipboard")
    } catch {
      setError("Failed to copy selected tests")
    }
  }

  const downloadFile = (filename: string, content: string, mimeType: string) => {
    const blob = new Blob([content], { type: mimeType })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const exportSelectedAsTxt = () => {
    if (selectedTests.length === 0) return
    downloadFile(
      `${form.section}-selected-tests.txt`,
      selectedTests.join("\n"),
      "text/plain;charset=utf-8"
    )
    setSuccessMessage("Selected tests exported as TXT")
  }

  const exportSelectedAsCsv = () => {
    if (selectedTests.length === 0) return
    const rows = ["section,test", ...selectedTests.map((test) => `"${form.section}","${test.replace(/"/g, '""')}"`)]
    downloadFile(
      `${form.section}-selected-tests.csv`,
      rows.join("\n"),
      "text/csv;charset=utf-8"
    )
    setSuccessMessage("Selected tests exported as CSV")
  }

  const exportResultsAsTxt = () => {
    if (filteredResults.length === 0) return
    const content = filteredResults
      .map((order) => {
        return [
          `Patient: ${order.patientName}`,
          `Tests: ${order.tests.join(", ")}`,
          `Status: ${order.status}`,
          `Result: ${order.result || "No result entered yet"}`,
          `Section: ${order.section}`,
          `Priority: ${order.priority}`,
          "------------------------------",
        ].join("\n")
      })
      .join("\n")

    const blob = new Blob([content], { type: "text/plain;charset=utf-8" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "lab-results.txt"
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    setSuccessMessage("Results exported as TXT")
  }

  const exportResultsAsCsv = () => {
    if (filteredResults.length === 0) return
    const rows = [
      "patientName,tests,status,result,section,priority",
      ...filteredResults.map((order) =>
        [
          `"${order.patientName.replace(/"/g, '""')}"`,
          `"${order.tests.join(" | ").replace(/"/g, '""')}"`,
          `"${order.status.replace(/"/g, '""')}"`,
          `"${(order.result || "No result entered yet").replace(/"/g, '""')}"`,
          `"${order.section.replace(/"/g, '""')}"`,
          `"${order.priority.replace(/"/g, '""')}"`
        ].join(",")
      ),
    ]

    const blob = new Blob([rows.join("\n")], { type: "text/csv;charset=utf-8" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "lab-results.csv"
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    setSuccessMessage("Results exported as CSV")
  }

  const printResults = () => {
    if (filteredResults.length === 0) return

    const html = `
      <html>
        <head>
          <title>Lab Results</title>
          <style>
            body { font-family: Arial, sans-serif; padding: 24px; }
            h1 { margin-bottom: 20px; }
            .card { border: 1px solid #ddd; border-radius: 10px; padding: 14px; margin-bottom: 12px; }
            .label { font-weight: bold; }
          </style>
        </head>
        <body>
          <h1>Laboratory Results</h1>
          ${filteredResults.map((order) => `
            <div class="card">
              <div><span class="label">Patient:</span> ${order.patientName}</div>
              <div><span class="label">Tests:</span> ${order.tests.join(", ")}</div>
              <div><span class="label">Status:</span> ${order.status}</div>
              <div><span class="label">Result:</span> ${order.result || "No result entered yet"}</div>
              <div><span class="label">Section:</span> ${order.section}</div>
              <div><span class="label">Priority:</span> ${order.priority}</div>
            </div>
          `).join("")}
        </body>
      </html>
    `

    const printWindow = window.open("", "_blank")
    if (!printWindow) {
      setError("Failed to open print window")
      return
    }

    printWindow.document.open()
    printWindow.document.write(html)
    printWindow.document.close()
    printWindow.focus()
    printWindow.print()
    setSuccessMessage("Print view opened")
  }

  const submitOrder = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedPatient) return

    try {
      await apiPost("/labs/orders", {
        patientId: selectedPatient.id,
        patientName: selectedPatient.name,
        section: form.section,
        tests: form.tests.split(",").map((t) => t.trim()).filter(Boolean),
        priority: form.priority,
        status: "Pending",
      })

      const refreshed = await apiGet("/labs/orders")
      setOrders(Array.isArray(refreshed) ? refreshed : [])
      setForm({
        section: form.section,
        tests: "",
        priority: "Routine",
      })
      setSelectedTests([])
      setSuccessMessage("Lab order added")
    } catch {
      setError("Failed to save lab order")
    }
  }

  return (
    <div style={pageStyle}>
      <div style={{ display: "grid", gap: 20 }}>
        <div>
          <h1 style={{ margin: 0, fontSize: 42, fontWeight: 800 }}>Laboratory • NEW UI • GLASS ACTIVE</h1>
          <div style={{ marginTop: 8, color: "#cbd5e1" }}>
            SMART LABORATORY WORKFLOW • GLASS ACTIVE
          </div>
        </div>

        {error && <div style={errorStyle}>{error}</div>}
        {successMessage && <div style={successStyle}>{successMessage}</div>}

        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          <button type="button" style={tabBtnStyle(activeTab === "catalog")} onClick={() => setActiveTab("catalog")}>
            Catalog
          </button>
          <button type="button" style={tabBtnStyle(activeTab === "selected")} onClick={() => setActiveTab("selected")}>
            Selected Tests
          </button>
          <button type="button" style={tabBtnStyle(activeTab === "orders")} onClick={() => setActiveTab("orders")}>
            Orders
          </button>
          <button type="button" style={tabBtnStyle(activeTab === "results")} onClick={() => setActiveTab("results")}>
            Results
          </button>
        </div>

        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          <div style={itemStyle}><strong>Total Orders:</strong> {totalOrdersCount}</div>
          <div style={itemStyle}><strong>Pending:</strong> {pendingOrdersCount}</div>
          <div style={itemStyle}><strong>Completed:</strong> {completedOrdersCount}</div>
          <div style={itemStyle}><strong>Results Available:</strong> {resultsAvailableCount}</div>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1.1fr 2fr", gap: 20 }}>
          <div style={cardStyle}>
            <h2 style={titleStyle}>Patients</h2>
            <div style={{ display: "grid", gap: 14 }}>
              {patients.map((patient) => (
                <button
                  key={patient.id}
                  onClick={() => setSelectedPatientId(patient.id)}
                  style={{
                    ...itemStyle,
                    textAlign: "left",
                    cursor: "pointer",
                    border:
                      selectedPatientId === patient.id
                        ? "1px solid rgba(56,189,248,0.95)"
                        : "1px solid rgba(148,163,184,0.22)",
                  }}
                >
                  <div style={{ fontSize: 18, fontWeight: 800 }}>{patient.name}</div>
                  <div style={{ marginTop: 6, color: "#cbd5e1" }}>{patient.id}</div>
                  <div style={{ marginTop: 6, color: "#e2e8f0" }}>
                    {patient.department ?? "General"} • {patient.condition ?? "-"}
                  </div>
                </button>
              ))}
            </div>
          </div>

          <div style={{ display: "grid", gap: 20 }}>
            <div style={cardStyle}>
              <h2 style={titleStyle}>Selected Patient</h2>
              {selectedPatient ? (
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
                  <div><strong>Name:</strong> {selectedPatient.name}</div>
                  <div><strong>ID:</strong> {selectedPatient.id}</div>
                  <div><strong>Department:</strong> {selectedPatient.department ?? "-"}</div>
                  <div><strong>Status:</strong> {selectedPatient.status ?? "-"}</div>
                  <div style={{ gridColumn: "1 / -1" }}><strong>Condition:</strong> {selectedPatient.condition ?? "-"}</div>
                </div>
              ) : (
                <div>No patient selected</div>
              )}
            </div>

            {activeTab === "catalog" && (
              <form onSubmit={submitOrder} style={cardStyle}>
                <h2 style={titleStyle}>Create Lab Order</h2>

                <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 10, marginBottom: 14 }}>
                  {Object.keys(catalog).map((section) => (
                    <button
                      key={section}
                      type="button"
                      onClick={() => {
                        setForm({ ...form, section })
                        setSelectedTests([])
                        setLabSearch("")
                      }}
                      style={{
                        ...itemStyle,
                        cursor: "pointer",
                        textTransform: "capitalize",
                        border: form.section === section
                          ? "1px solid rgba(56,189,248,0.95)"
                          : "1px solid rgba(96,165,250,0.26)",
                      }}
                    >
                      {section.replaceAll("_", " ")}
                    </button>
                  ))}
                </div>

                <div style={{ display: "grid", gridTemplateColumns: "1fr 2fr 1fr", gap: 10 }}>
                  <input style={inputStyle} value={form.section} readOnly placeholder="Section" />
                  <input style={inputStyle} placeholder="Selected tests" value={form.tests} readOnly />
                  <select
                    value={form.priority}
                    onChange={(e) => setForm({ ...form, priority: e.target.value })}
                    style={inputStyle}
                  >
                    <option value="Routine">Routine</option>
                    <option value="Urgent">Urgent</option>
                  </select>
                </div>

                <div style={{ marginTop: 16, ...itemStyle, maxHeight: 320, overflowY: "auto" }}>
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      gap: 10,
                      marginBottom: 12,
                      flexWrap: "wrap",
                    }}
                  >
                    <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
                      <div style={{ fontSize: 18, fontWeight: 800, textTransform: "capitalize" }}>
                        Available Tests — {form.section.replaceAll("_", " ")}
                      </div>
                      <span
                        style={{
                          display: "inline-block",
                          padding: "6px 10px",
                          borderRadius: 999,
                          fontSize: 12,
                          fontWeight: 800,
                          background: "rgba(14,165,233,0.18)",
                          border: "1px solid rgba(56,189,248,0.35)",
                          color: "#bae6fd",
                        }}
                      >
                        Selected: {selectedTests.length}
                      </span>
                    </div>

                    <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                      <button type="button" onClick={() => setSelectedTests(filteredCatalogTests)} style={secondaryBtn}>
                        Select All
                      </button>
                      <button type="button" onClick={() => setSelectedTests([])} style={secondaryBtn}>
                        Clear Selected
                      </button>
                      <button type="button" onClick={copySelectedTests} style={secondaryBtn}>
                        Copy Selected
                      </button>
                      <button type="button" onClick={exportSelectedAsTxt} style={secondaryBtn}>
                        Export TXT
                      </button>
                      <button type="button" onClick={exportSelectedAsCsv} style={secondaryBtn}>
                        Export CSV
                      </button>
                    </div>
                  </div>

                  <div style={{ marginBottom: 12 }}>
                    <input
                      style={inputStyle}
                      placeholder="Search tests in this section..."
                      value={labSearch}
                      onChange={(e) => setLabSearch(e.target.value)}
                    />
                  </div>

                  {filteredCatalogTests.length ? (
                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
                      {filteredCatalogTests.map((test) => (
                        <button
                          key={test}
                          type="button"
                          onClick={() =>
                            setSelectedTests((prev) =>
                              prev.includes(test)
                                ? prev.filter((item) => item !== test)
                                : [...prev, test]
                            )
                          }
                          style={{
                            textAlign: "left",
                            padding: "10px 12px",
                            borderRadius: 12,
                            border: selectedTests.includes(test)
                              ? "1px solid rgba(56,189,248,0.95)"
                              : "1px solid rgba(148,163,184,0.25)",
                            background: selectedTests.includes(test)
                              ? "linear-gradient(135deg, rgba(37,99,235,0.34), rgba(14,165,233,0.18))"
                              : "rgba(255,255,255,0.05)",
                            color: "#f8fafc",
                            cursor: "pointer",
                            fontWeight: selectedTests.includes(test) ? 800 : 500,
                          }}
                        >
                          {test}
                        </button>
                      ))}
                    </div>
                  ) : (
                    <div style={{ color: "#cbd5e1" }}>No tests match this search in the current section</div>
                  )}
                </div>

                <div style={{ marginTop: 14 }}>
                  <button type="submit" style={primaryBtn}>Add Lab Order</button>
                </div>
              </form>
            )}

            {activeTab === "selected" && (
              <div style={cardStyle}>
                <h2 style={titleStyle}>Selected Tests</h2>
                <div style={{ display: "grid", gap: 12 }}>
                  {selectedTests.length === 0 ? (
                    <div style={{ color: "#cbd5e1" }}>No tests selected yet</div>
                  ) : (
                    selectedTests.map((test) => (
                      <div key={test} style={itemStyle}>
                        {test}
                      </div>
                    ))
                  )}
                </div>
              </div>
            )}

            {activeTab === "orders" && (
              <div style={cardStyle}>
                <div style={{ display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap", alignItems: "center" }}>
                  <h2 style={titleStyle}>Lab Orders</h2>
                  <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                    <button
                      type="button"
                      style={tabBtnStyle(ordersStatusFilter === "all")}
                      onClick={() => setOrdersStatusFilter("all")}
                    >
                      All
                    </button>
                    <button
                      type="button"
                      style={tabBtnStyle(ordersStatusFilter === "Pending")}
                      onClick={() => setOrdersStatusFilter("Pending")}
                    >
                      Pending
                    </button>
                    <button
                      type="button"
                      style={tabBtnStyle(ordersStatusFilter === "Completed")}
                      onClick={() => setOrdersStatusFilter("Completed")}
                    >
                      Completed
                    </button>
                  </div>
                </div>

                <div style={{ marginTop: 12, color: "#cbd5e1" }}>
                  Current filter: {ordersStatusFilter === "all" ? "All" : ordersStatusFilter}
                </div>

                <div style={{ display: "grid", gap: 12, marginTop: 14 }}>
                  {filteredOrdersByStatus.length === 0 ? (
                    <div style={{ color: "#cbd5e1" }}>No lab orders for this filter</div>
                  ) : filteredOrdersByStatus.map((order) => (
                    <div key={order.id} style={itemStyle}>
                      <div style={{ fontSize: 18, fontWeight: 800 }}>{order.patientName}</div>
                      <div style={{ marginTop: 6, color: "#e2e8f0" }}>
                        {order.tests.join(" • ")}
                      </div>
                      <div style={{ marginTop: 8, color: "#cbd5e1" }}>
                        Section: {order.section} • Priority: {order.priority}
                      </div>
                      <div style={{ marginTop: 10 }}>
                        <span style={badgeStyle(order.status)}>{order.status}</span>
                      </div>
                      {order.result ? (
                        <div style={{ marginTop: 10, color: "#cbd5e1" }}>
                          Result: {order.result}
                        </div>
                      ) : null}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === "results" && (
              <div style={cardStyle}>
                <div style={{ display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap", alignItems: "center" }}>
                  <h2 style={titleStyle}>Results</h2>
                  <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                    <button
                      type="button"
                      style={tabBtnStyle(resultsFilter === "all")}
                      onClick={() => setResultsFilter("all")}
                    >
                      All Results
                    </button>
                    <button
                      type="button"
                      style={tabBtnStyle(resultsFilter === "has_result")}
                      onClick={() => setResultsFilter("has_result")}
                    >
                      Has Result
                    </button>
                    <button
                      type="button"
                      style={tabBtnStyle(resultsFilter === "no_result")}
                      onClick={() => setResultsFilter("no_result")}
                    >
                      No Result
                    </button>
                    <button
                      type="button"
                      style={secondaryBtn}
                      onClick={printResults}
                    >
                      Print Results
                    </button>
                    <button
                      type="button"
                      style={secondaryBtn}
                      onClick={exportResultsAsTxt}
                    >
                      Export TXT
                    </button>
                    <button
                      type="button"
                      style={secondaryBtn}
                      onClick={exportResultsAsCsv}
                    >
                      Export CSV
                    </button>
                  </div>
                </div>

                <div style={{ marginTop: 12 }}>
                  <input
                    style={inputStyle}
                    placeholder="Search by test name..."
                    value={resultsSearch}
                    onChange={(e) => setResultsSearch(e.target.value)}
                  />
                </div>

                <div style={{ marginTop: 12, color: "#cbd5e1" }}>
                  Current filter: {resultsFilter === "all" ? "All Results" : resultsFilter === "has_result" ? "Has Result" : "No Result"}
                </div>

                <div style={{ display: "grid", gap: 12, marginTop: 14 }}>
                  {filteredResults.length === 0 ? (
                    <div style={{ color: "#cbd5e1" }}>No results match this filter</div>
                  ) : (
                    filteredResults.map((order) => (
                      <div key={order.id} style={itemStyle}>
                        <div style={{ fontSize: 18, fontWeight: 800 }}>{order.patientName}</div>
                        <div style={{ marginTop: 6, color: "#e2e8f0" }}>
                          {order.tests.join(" • ")}
                        </div>
                        <div style={{ marginTop: 8 }}>
                          <span style={badgeStyle(order.status)}>{order.status}</span>
                        </div>
                        <div style={{ marginTop: 10, color: "#cbd5e1" }}>
                          Result: {order.result || "No result entered yet"}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

const pageStyle: React.CSSProperties = {
  minHeight: "100vh",
  background: "linear-gradient(180deg, #0f172a 0%, #111827 100%)",
  color: "#f8fafc",
  padding: 24,
}

const cardStyle: React.CSSProperties = {
  background: "linear-gradient(180deg, rgba(30,41,59,0.92), rgba(15,23,42,0.92))",
  border: "1px solid rgba(96,165,250,0.28)",
  borderRadius: 24,
  padding: 22,
  boxShadow: "0 10px 30px rgba(0,0,0,0.25)",
}

const itemStyle: React.CSSProperties = {
  background: "linear-gradient(180deg, rgba(37,99,235,0.18), rgba(15,23,42,0.30))",
  border: "1px solid rgba(96,165,250,0.26)",
  borderRadius: 18,
  padding: 16,
  boxShadow: "0 8px 18px rgba(0,0,0,0.18)",
}

const inputStyle: React.CSSProperties = {
  width: "100%",
  border: "1px solid rgba(148,163,184,0.35)",
  borderRadius: 14,
  padding: "12px 14px",
  background: "rgba(255,255,255,0.08)",
  color: "#f8fafc",
  outline: "none",
}


const secondaryBtn: React.CSSProperties = {
  border: "1px solid rgba(148,163,184,0.35)",
  borderRadius: 12,
  padding: "8px 12px",
  background: "rgba(255,255,255,0.08)",
  color: "#e5e7eb",
  fontWeight: 700,
  cursor: "pointer",
}

const primaryBtn: React.CSSProperties = {
  border: "none",
  borderRadius: 14,
  padding: "12px 16px",
  background: "linear-gradient(135deg, #0ea5e9, #2563eb)",
  color: "white",
  fontWeight: 700,
  cursor: "pointer",
}

const titleStyle: React.CSSProperties = {
  marginTop: 0,
  marginBottom: 16,
  fontSize: 28,
}

const errorStyle: React.CSSProperties = {
  background: "linear-gradient(180deg, rgba(127,29,29,0.5), rgba(69,10,10,0.55))",
  border: "1px solid rgba(248,113,113,0.45)",
  color: "#fecaca",
  borderRadius: 20,
  padding: 16,
}

const successStyle: React.CSSProperties = {
  background: "linear-gradient(180deg, rgba(20,83,45,0.5), rgba(5,46,22,0.55))",
  border: "1px solid rgba(74,222,128,0.45)",
  color: "#bbf7d0",
  borderRadius: 20,
  padding: 16,
}


const tabBtnStyle = (active: boolean): React.CSSProperties => ({
  border: active ? "1px solid rgba(56,189,248,0.95)" : "1px solid rgba(148,163,184,0.35)",
  borderRadius: 14,
  padding: "10px 14px",
  background: active
    ? "linear-gradient(135deg, rgba(37,99,235,0.34), rgba(14,165,233,0.18))"
    : "rgba(255,255,255,0.08)",
  color: "#e5e7eb",
  fontWeight: 800,
  cursor: "pointer",
})

const badgeStyle = (status: string): React.CSSProperties => ({
  display: "inline-block",
  padding: "6px 10px",
  borderRadius: 999,
  fontSize: 13,
  fontWeight: 800,
  background: status === "Completed" ? "#dcfce7" : status === "Processing" ? "#dbeafe" : "#fef3c7",
  color: status === "Completed" ? "#166534" : status === "Processing" ? "#1d4ed8" : "#92400e",
})
