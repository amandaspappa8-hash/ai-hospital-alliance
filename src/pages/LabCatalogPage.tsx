import { useEffect, useMemo, useState } from "react"
import { Beaker, Microscope, Dna } from "lucide-react"
import SectionIconBadge from "@/components/app/SectionIconBadge"
import { apiGet, apiPost } from "@/lib/api"

type LabStatus = "Pending" | "Processing" | "Completed" | "Abnormal"
type LabSection = "classical" | "specialized" | "genetics"

type LabCatalog = {
  classical: string[]
  specialized: string[]
  genetics: string[]
}

type Patient = {
  id: string
  name: string
}

type LabOrder = {
  id: string
  patientId: string
  patientName: string
  section: LabSection
  tests: string[]
  priority: string
  status: LabStatus | string
  result?: string
}

function statusClasses(status: string) {
  switch (status) {
    case "Completed":
      return "bg-emerald-100 text-emerald-700 border border-emerald-200"
    case "Processing":
      return "bg-lime-100 text-lime-700 border border-lime-200"
    case "Pending":
      return "bg-green-100 text-green-700 border border-green-200"
    case "Abnormal":
      return "bg-rose-100 text-rose-700 border border-rose-200"
    default:
      return "bg-slate-100 text-slate-700 border border-slate-200"
  }
}

function OverviewLikeCard({
  title,
  value,
  selected,
  onClick,
  bg,
  border,
  icon,
}: {
  title: string
  value: string
  selected: boolean
  onClick: () => void
  bg: string
  border: string
  icon: React.ReactNode
}) {
  return (
    <button onClick={onClick} style={{ textAlign: "left", width: "100%" }}>
      <div
        style={{
          background: bg,
          border: selected ? "2px solid #93c5fd" : `1px solid ${border}`,
          borderRadius: "28px",
          padding: "22px",
          minHeight: "170px",
          boxShadow: "0 8px 24px rgba(15,23,42,0.10)",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          transition: "all 0.2s ease",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
          <div style={{ fontSize: 15, color: "#64748b", fontWeight: 600 }}>{title}</div>
          {icon}
        </div>
        <div style={{ fontSize: 56, fontWeight: 700, lineHeight: 1, color: "#334155" }}>{value}</div>
      </div>
    </button>
  )
}

export default function LabCatalogPage() {
  const [query, setQuery] = useState("")
  const [selectedOrderId, setSelectedOrderId] = useState("")
  const [selectedSection, setSelectedSection] = useState<LabSection>("classical")
  const [selectedTests, setSelectedTests] = useState<string[]>([])
  const [interpretation, setInterpretation] = useState(
    "Inflammatory marker is elevated. Clinical correlation is recommended."
  )
  const [resultText, setResultText] = useState("")
  const [catalog, setCatalog] = useState<LabCatalog>({
    classical: [],
    specialized: [],
    genetics: [],
  })
  const [patients, setPatients] = useState<Patient[]>([])
  const [selectedPatientId, setSelectedPatientId] = useState("")
  const [orders, setOrders] = useState<LabOrder[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [savingResult, setSavingResult] = useState(false)
  const [error, setError] = useState("")

  const selectedPatient =
    patients.find((p) => p.id === selectedPatientId) ?? patients[0]

  async function loadBaseData() {
    try {
      setLoading(true)
      setError("")

      const [catalogData, patientsData] = await Promise.all([
        apiGet<LabCatalog>("/labs/catalog"),
        apiGet<Patient[]>("/patients"),
      ])

      setCatalog(catalogData)
      setPatients(Array.isArray(patientsData) ? patientsData : [])

      if (Array.isArray(patientsData) && patientsData.length > 0) {
        setSelectedPatientId((current) => current || patientsData[0].id)
      }
    } catch (err) {
      console.error(err)
      setError("Failed to load laboratory base data")
    } finally {
      setLoading(false)
    }
  }

  async function loadPatientOrders(patientId: string) {
    try {
      const ordersData = await apiGet<LabOrder[]>(`/labs/orders/${patientId}`)
      setOrders(Array.isArray(ordersData) ? ordersData : [])
      if (Array.isArray(ordersData) && ordersData.length > 0) {
        setSelectedOrderId(ordersData[0].id)
      } else {
        setSelectedOrderId("")
        setResultText("")
      }
    } catch (err) {
      console.error(err)
      setError("Failed to load patient lab orders")
    }
  }

  useEffect(() => {
    loadBaseData()
  }, [])

  useEffect(() => {
    if (selectedPatientId) {
      loadPatientOrders(selectedPatientId)
    }
  }, [selectedPatientId])

  const classicalTests = catalog.classical ?? []
  const specializedTests = catalog.specialized ?? []
  const geneticsTests = catalog.genetics ?? []

  const filteredOrders = useMemo(() => {
    const q = query.trim().toLowerCase()
    if (!q) return orders
    return orders.filter(
      (order) =>
        order.id.toLowerCase().includes(q) ||
        order.patientId.toLowerCase().includes(q) ||
        order.patientName.toLowerCase().includes(q) ||
        order.tests.join(" ").toLowerCase().includes(q) ||
        order.section.toLowerCase().includes(q)
    )
  }, [orders, query])

  const selectedOrder =
    filteredOrders.find((o) => o.id === selectedOrderId) ??
    orders.find((o) => o.id === selectedOrderId) ??
    orders[0]

  useEffect(() => {
    setResultText(selectedOrder?.result ?? "")
  }, [selectedOrderId, selectedOrder?.result])

  function toggleTest(testName: string) {
    setSelectedTests((prev) =>
      prev.includes(testName)
        ? prev.filter((item) => item !== testName)
        : [...prev, testName]
    )
  }

  async function createLabOrder() {
    if (!selectedPatient) {
      setError("Select a patient first")
      return
    }

    if (selectedTests.length === 0) {
      setError("Select at least one test before creating a lab order")
      return
    }

    try {
      setSaving(true)
      setError("")

      const created = await apiPost<LabOrder>("/labs/orders", {
        patientId: selectedPatient.id,
        patientName: selectedPatient.name,
        section: selectedSection,
        tests: selectedTests,
        priority: "Urgent",
      })

      setOrders((prev) => [created, ...prev])
      setSelectedOrderId(created.id)
      setSelectedTests([])
    } catch (err) {
      console.error(err)
      setError("Failed to create lab order")
    } finally {
      setSaving(false)
    }
  }

  async function saveLabResult() {
    if (!selectedOrder) {
      setError("Select a lab order first")
      return
    }

    if (!resultText.trim()) {
      setError("Write a result before saving")
      return
    }

    try {
      setSavingResult(true)
      setError("")

      const updated = await apiPost<LabOrder>(`/labs/results/${selectedOrder.id}`, {
        result: resultText.trim(),
        status: "Completed",
      })

      setOrders((prev) =>
        prev.map((order) => (order.id === updated.id ? updated : order))
      )
      setSelectedOrderId(updated.id)
    } catch (err) {
      console.error(err)
      setError("Failed to save lab result")
    } finally {
      setSavingResult(false)
    }
  }

  function renderTestList(title: string, tests: string[]) {
    return (
      <div className="rounded-3xl border border-green-200 bg-white/95 p-6 shadow-sm">
        <div className="mb-4">
          <h2 className="text-2xl font-bold text-slate-700">{title}</h2>
          <p className="text-sm text-slate-500 mt-2">اختر التحاليل المطلوبة من المربعات التالية</p>
        </div>

        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
          {tests.map((test) => {
            const checked = selectedTests.includes(test)
            return (
              <label
                key={test}
                className={`flex items-center gap-3 rounded-2xl border p-4 cursor-pointer transition ${
                  checked
                    ? "border-emerald-400 bg-emerald-50 shadow-sm"
                    : "border-slate-200 bg-white hover:border-green-300"
                }`}
              >
                <input
                  type="checkbox"
                  checked={checked}
                  onChange={() => toggleTest(test)}
                  className="h-5 w-5"
                />
                <span className="font-medium text-slate-700">{test}</span>
              </label>
            )
          })}
        </div>
      </div>
    )
  }

  return (
    <div style={{ padding: "24px", color: "white" }}>
      <h1 style={{ fontSize: "30px", marginBottom: "8px" }}>Laboratory Dashboard</h1>
      <p style={{ opacity: 0.8, marginBottom: "20px" }}>
        Orders, specimen workflow, results review, and AI clinical interpretation
      </p>

      {error && <div style={{ color: "#fca5a5", marginBottom: "16px" }}>{error}</div>}

      <div
        style={{
          background: "#ffffff",
          border: "1px solid #d1fae5",
          borderRadius: "20px",
          padding: "16px",
          marginBottom: "24px",
          color: "#0f172a",
          display: "grid",
          gap: "12px",
        }}
      >
        <div style={{ fontWeight: 700, color: "#166534" }}>Patient Selection</div>
        <select
          value={selectedPatientId}
          onChange={(e) => setSelectedPatientId(e.target.value)}
          style={{
            border: "1px solid #bbf7d0",
            borderRadius: "12px",
            padding: "12px 14px",
            background: "#f0fdf4",
            color: "#0f172a",
          }}
        >
          {patients.map((patient) => (
            <option key={patient.id} value={patient.id}>
              {patient.name} ({patient.id})
            </option>
          ))}
        </select>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(12, minmax(0, 1fr))",
          gap: "16px",
          marginBottom: "24px",
        }}
      >
        <div style={{ gridColumn: "span 5" }}>
          <OverviewLikeCard
            title="Classical Lab Tests"
            value={loading ? "..." : String(classicalTests.length)}
            selected={selectedSection === "classical"}
            onClick={() => setSelectedSection("classical")}
            bg="#d9f2ff"
            border="#bfe7fb"
            icon={
              <SectionIconBadge
                icon={<Beaker size={20} strokeWidth={2} />}
                bg="rgba(16,185,129,0.15)"
                color="#065f46"
              />
            }
          />
        </div>

        <div style={{ gridColumn: "span 4" }}>
          <OverviewLikeCard
            title="Specialized Tests"
            value={loading ? "..." : String(specializedTests.length)}
            selected={selectedSection === "specialized"}
            onClick={() => setSelectedSection("specialized")}
            bg="#d8fbf4"
            border="#b8efe4"
            icon={
              <SectionIconBadge
                icon={<Microscope size={20} strokeWidth={2} />}
                bg="rgba(6,182,212,0.15)"
                color="#0e7490"
              />
            }
          />
        </div>

        <div style={{ gridColumn: "span 3" }}>
          <OverviewLikeCard
            title="Oncology, DNA & Genetic"
            value={loading ? "..." : String(geneticsTests.length)}
            selected={selectedSection === "genetics"}
            onClick={() => setSelectedSection("genetics")}
            bg="#f7ecff"
            border="#e9d1fb"
            icon={
              <SectionIconBadge
                icon={<Dna size={20} strokeWidth={2} />}
                bg="rgba(168,85,247,0.15)"
                color="#6d28d9"
              />
            }
          />
        </div>
      </div>

      <div className="mb-6">
        {selectedSection === "classical" && renderTestList("Classical Lab Tests", classicalTests)}
        {selectedSection === "specialized" && renderTestList("Specialized Tests", specializedTests)}
        {selectedSection === "genetics" && renderTestList("Oncology, DNA & Genetic Tests", geneticsTests)}
      </div>

      <div className="grid gap-6 xl:grid-cols-12">
        <div className="xl:col-span-4 space-y-6">
          <div className="rounded-2xl border border-green-200 bg-white/95 p-5 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-green-950">Selected Tests</h2>
              <span className="rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700">
                {selectedTests.length} selected
              </span>
            </div>

            {selectedTests.length === 0 ? (
              <div className="rounded-2xl border border-dashed border-green-200 bg-green-50 p-4 text-sm text-slate-600">
                لم يتم اختيار أي تحليل بعد
              </div>
            ) : (
              <div className="space-y-2">
                {selectedTests.map((test) => (
                  <div
                    key={test}
                    className="flex items-center justify-between rounded-xl border border-green-100 bg-green-50 p-3"
                  >
                    <span className="font-medium text-slate-800">{test}</span>
                    <button
                      onClick={() => toggleTest(test)}
                      className="rounded-lg bg-white px-2 py-1 text-xs text-rose-600 border border-rose-100"
                    >
                      Remove
                    </button>
                  </div>
                ))}
              </div>
            )}

            <button
              onClick={createLabOrder}
              disabled={saving}
              className="mt-4 w-full rounded-xl bg-green-600 px-4 py-3 font-semibold text-white hover:bg-green-700 disabled:opacity-60"
            >
              {saving ? "Creating..." : "Confirm Lab Request"}
            </button>
          </div>

          <div className="rounded-2xl border border-green-200 bg-white/95 p-5 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-green-950">Lab Orders Queue</h2>
              <span className="rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700">
                {filteredOrders.length} orders
              </span>
            </div>

            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search patient, order, test..."
              className="w-full rounded-xl border border-green-200 bg-green-50/60 px-4 py-3 outline-none focus:border-emerald-400"
            />

            <div className="mt-4 space-y-3">
              {filteredOrders.map((order) => (
                <button
                  key={order.id}
                  onClick={() => setSelectedOrderId(order.id)}
                  className={`w-full rounded-2xl border p-4 text-left transition ${
                    selectedOrderId === order.id
                      ? "border-emerald-400 bg-gradient-to-r from-green-50 to-emerald-50 shadow"
                      : "border-slate-200 bg-white hover:border-green-300 hover:bg-green-50/40"
                  }`}
                >
                  <div className="font-semibold text-slate-900">{order.patientName}</div>
                  <div className="mt-1 text-sm text-slate-600">
                    {order.tests.join(", ")}
                  </div>
                  <div className="mt-2 text-xs text-slate-500">
                    Order ID: {order.id} • {order.patientId} • {order.section}
                  </div>
                  <div className="mt-3 flex items-center gap-2">
                    <span className={`rounded-full px-2.5 py-1 text-[11px] font-semibold ${statusClasses(order.status)}`}>
                      {order.status}
                    </span>
                    <span className="rounded-full px-2.5 py-1 text-[11px] font-semibold bg-sky-100 text-sky-700 border border-sky-200">
                      {order.priority}
                    </span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="xl:col-span-5 space-y-6">
          <div className="rounded-2xl border border-green-200 bg-white/95 p-5 shadow-sm">
            <div className="mb-4">
              <h2 className="text-xl font-bold text-green-950">Selected Result</h2>
              <p className="mt-1 text-sm text-slate-600">
                Result details, sample status, and validation summary
              </p>
            </div>

            {selectedOrder ? (
              <div className="rounded-2xl border border-green-200 bg-gradient-to-br from-green-100 via-emerald-50 to-white p-5">
                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="rounded-xl bg-white p-4 border border-green-100">
                    <div className="text-sm text-slate-500">Patient</div>
                    <div className="font-semibold text-green-950">{selectedOrder.patientName}</div>
                  </div>
                  <div className="rounded-xl bg-white p-4 border border-green-100">
                    <div className="text-sm text-slate-500">Order ID</div>
                    <div className="font-semibold text-green-950">{selectedOrder.id}</div>
                  </div>
                  <div className="rounded-xl bg-white p-4 border border-green-100">
                    <div className="text-sm text-slate-500">Tests</div>
                    <div className="font-semibold text-green-950">{selectedOrder.tests.join(", ")}</div>
                  </div>
                  <div className="rounded-xl bg-white p-4 border border-green-100">
                    <div className="text-sm text-slate-500">Section</div>
                    <div className="font-semibold text-green-950">{selectedOrder.section}</div>
                  </div>
                  <div className="rounded-xl bg-white p-4 border border-green-100">
                    <div className="text-sm text-slate-500">Priority</div>
                    <div className="font-semibold text-green-950">{selectedOrder.priority}</div>
                  </div>
                  <div className="rounded-xl bg-white p-4 border border-green-100">
                    <div className="text-sm text-slate-500">Status</div>
                    <div className="font-semibold text-green-950">{selectedOrder.status}</div>
                  </div>
                </div>

                <div className="mt-4 rounded-xl bg-white p-4 border border-emerald-100">
                  <div className="text-sm text-slate-500">Result Summary</div>
                  <div className="mt-2 font-medium text-slate-800">
                    {selectedOrder.result?.trim() ? selectedOrder.result : "Result not available yet."}
                  </div>
                </div>
              </div>
            ) : (
              <div className="rounded-2xl border border-dashed border-green-200 bg-green-50 p-5 text-slate-600">
                No order selected.
              </div>
            )}
          </div>

          <div className="rounded-2xl border border-emerald-200 bg-gradient-to-br from-white to-green-50 p-5 shadow-sm">
            <h2 className="text-xl font-bold text-green-950 mb-4">Lab Result Entry</h2>

            <textarea
              value={resultText}
              onChange={(e) => setResultText(e.target.value)}
              className="min-h-[220px] w-full rounded-2xl border border-green-200 bg-white px-4 py-4 outline-none focus:border-emerald-400"
              placeholder="Write lab result..."
            />

            <div className="mt-4 flex flex-wrap gap-3">
              <button
                onClick={saveLabResult}
                disabled={savingResult || !selectedOrder}
                className="rounded-xl bg-green-600 px-4 py-2 font-semibold text-white hover:bg-green-700 disabled:opacity-60"
              >
                {savingResult ? "Saving..." : "Save Result"}
              </button>
              <button className="rounded-xl bg-emerald-600 px-4 py-2 font-semibold text-white hover:bg-emerald-700">
                Validate Result
              </button>
              <button className="rounded-xl bg-slate-800 px-4 py-2 font-semibold text-white hover:bg-slate-900">
                Send to EMR
              </button>
            </div>
          </div>

          <div className="rounded-2xl border border-emerald-200 bg-gradient-to-br from-white to-green-50 p-5 shadow-sm">
            <h2 className="text-xl font-bold text-green-950 mb-4">Clinical Interpretation</h2>

            <textarea
              value={interpretation}
              onChange={(e) => setInterpretation(e.target.value)}
              className="min-h-[160px] w-full rounded-2xl border border-green-200 bg-white px-4 py-4 outline-none focus:border-emerald-400"
              placeholder="Write lab interpretation..."
            />

            <div className="mt-4 flex flex-wrap gap-3">
              <button className="rounded-xl bg-green-600 px-4 py-2 font-semibold text-white hover:bg-green-700">
                Save Interpretation
              </button>
              <button className="rounded-xl bg-slate-800 px-4 py-2 font-semibold text-white hover:bg-slate-900">
                Review with Physician
              </button>
            </div>
          </div>
        </div>

        <div className="xl:col-span-3 space-y-6">
          <div className="rounded-2xl border border-green-200 bg-gradient-to-br from-green-100 to-white p-5 shadow-sm">
            <h2 className="text-xl font-bold text-green-950 mb-4">Department Load</h2>

            <div className="space-y-3">
              <div className="rounded-xl bg-white p-4 border border-green-100 flex items-center justify-between">
                <span className="text-slate-700">Classical</span>
                <span className="font-bold text-green-950">{classicalTests.length}</span>
              </div>
              <div className="rounded-xl bg-white p-4 border border-green-100 flex items-center justify-between">
                <span className="text-slate-700">Specialized</span>
                <span className="font-bold text-green-950">{specializedTests.length}</span>
              </div>
              <div className="rounded-xl bg-white p-4 border border-green-100 flex items-center justify-between">
                <span className="text-slate-700">Genetics</span>
                <span className="font-bold text-green-950">{geneticsTests.length}</span>
              </div>
              <div className="rounded-xl bg-white p-4 border border-green-100 flex items-center justify-between">
                <span className="text-slate-700">Orders</span>
                <span className="font-bold text-green-950">{orders.length}</span>
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-lime-200 bg-gradient-to-br from-lime-50 to-green-50 p-5 shadow-sm">
            <h2 className="text-xl font-bold text-green-950 mb-4">Quick Actions</h2>

            <div className="space-y-3">
              <button
                onClick={() => selectedPatientId && loadPatientOrders(selectedPatientId)}
                className="w-full rounded-xl bg-green-600 px-4 py-3 text-left font-semibold text-white hover:bg-green-700"
              >
                Refresh Patient Orders
              </button>
              <button className="w-full rounded-xl bg-emerald-600 px-4 py-3 text-left font-semibold text-white hover:bg-emerald-700">
                Open Analyzer Queue
              </button>
              <button className="w-full rounded-xl bg-slate-800 px-4 py-3 text-left font-semibold text-white hover:bg-slate-900">
                Review Abnormal Results
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
