import { useMemo, useState } from "react"
import { buildDischargeCounseling, type DischargeMedicationInput } from "@/lib/dischargeCounseling"

type FormMed = {
  name: string
  dose: string
  frequency: string
  duration: string
  route: string
}

const emptyMed: FormMed = {
  name: "",
  dose: "",
  frequency: "",
  duration: "",
  route: "PO",
}

export default function DischargeMedicationPage() {
  const [patientId, setPatientId] = useState("")
  const [patientName, setPatientName] = useState("")
  const [diagnosis, setDiagnosis] = useState("")
  const [followUp, setFollowUp] = useState("")
  const [meds, setMeds] = useState<FormMed[]>([])
  const [form, setForm] = useState<FormMed>(emptyMed)

  function addMedication() {
    if (!form.name.trim()) return
    setMeds((prev) => [...prev, form])
    setForm(emptyMed)
  }

  function removeMedication(index: number) {
    setMeds((prev) => prev.filter((_, i) => i !== index))
  }

  const counseling = useMemo(() => {
    const payload: DischargeMedicationInput[] = meds.map((m) => ({
      name: m.name,
      dose: m.dose,
      frequency: m.frequency,
      duration: m.duration,
      route: m.route,
    }))
    return buildDischargeCounseling(payload)
  }, [meds])

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="mx-auto max-w-7xl space-y-6">
        <div className="rounded-2xl border bg-white p-6 shadow-sm">
          <h1 className="text-3xl font-bold tracking-tight">
            Discharge Medication Counseling Engine
          </h1>
          <p className="mt-2 text-sm text-slate-600">
            Clinical Pharmacy + Smart Recommendation + Discharge Layer
          </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <div className="rounded-2xl border bg-white p-6 shadow-sm space-y-4">
            <h2 className="text-xl font-semibold">Patient Discharge Info</h2>

            <input
              className="w-full rounded-xl border px-4 py-3"
              placeholder="Patient ID"
              value={patientId}
              onChange={(e) => setPatientId(e.target.value)}
            />

            <input
              className="w-full rounded-xl border px-4 py-3"
              placeholder="Patient Name"
              value={patientName}
              onChange={(e) => setPatientName(e.target.value)}
            />

            <input
              className="w-full rounded-xl border px-4 py-3"
              placeholder="Diagnosis"
              value={diagnosis}
              onChange={(e) => setDiagnosis(e.target.value)}
            />

            <input
              className="w-full rounded-xl border px-4 py-3"
              placeholder="Follow-up Plan"
              value={followUp}
              onChange={(e) => setFollowUp(e.target.value)}
            />
          </div>

          <div className="rounded-2xl border bg-white p-6 shadow-sm space-y-4">
            <h2 className="text-xl font-semibold">Add Medication</h2>

            <input
              className="w-full rounded-xl border px-4 py-3"
              placeholder="Medication name"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
            />

            <div className="grid gap-3 md:grid-cols-2">
              <input
                className="w-full rounded-xl border px-4 py-3"
                placeholder="Dose"
                value={form.dose}
                onChange={(e) => setForm({ ...form, dose: e.target.value })}
              />
              <input
                className="w-full rounded-xl border px-4 py-3"
                placeholder="Frequency"
                value={form.frequency}
                onChange={(e) => setForm({ ...form, frequency: e.target.value })}
              />
            </div>

            <div className="grid gap-3 md:grid-cols-2">
              <input
                className="w-full rounded-xl border px-4 py-3"
                placeholder="Duration"
                value={form.duration}
                onChange={(e) => setForm({ ...form, duration: e.target.value })}
              />
              <select
                className="w-full rounded-xl border px-4 py-3"
                value={form.route}
                onChange={(e) => setForm({ ...form, route: e.target.value })}
              >
                <option value="PO">PO</option>
                <option value="IV">IV</option>
                <option value="IM">IM</option>
                <option value="SC">SC</option>
                <option value="INH">INH</option>
                <option value="TOPICAL">TOPICAL</option>
              </select>
            </div>

            <button
              onClick={addMedication}
              className="rounded-xl bg-slate-900 px-5 py-3 text-white"
            >
              Add Medication
            </button>
          </div>
        </div>

        <div className="rounded-2xl border bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold">Medication List</h2>

          {meds.length === 0 ? (
            <p className="mt-4 text-sm text-slate-500">No medications added yet.</p>
          ) : (
            <div className="mt-4 grid gap-3">
              {meds.map((med, index) => (
                <div
                  key={`${med.name}-${index}`}
                  className="flex flex-col gap-3 rounded-2xl border p-4 md:flex-row md:items-center md:justify-between"
                >
                  <div>
                    <div className="font-semibold">{med.name}</div>
                    <div className="text-sm text-slate-600">
                      {med.dose} • {med.frequency} • {med.duration} • {med.route}
                    </div>
                  </div>
                  <button
                    onClick={() => removeMedication(index)}
                    className="rounded-xl border px-4 py-2 text-sm"
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="rounded-2xl border bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold">Discharge Counseling Output</h2>

          {counseling.length === 0 ? (
            <p className="mt-4 text-sm text-slate-500">
              Add medications to generate discharge counseling.
            </p>
          ) : (
            <div className="mt-6 grid gap-6">
              {counseling.map((item, index) => (
                <div key={`${item.name}-${index}`} className="rounded-2xl border p-5">
                  <div className="mb-3">
                    <h3 className="text-lg font-bold">{item.name}</h3>
                    <p className="text-sm text-slate-600">
                      {item.dose} • {item.frequency} • {item.duration} • {item.route}
                    </p>
                  </div>

                  <div className="grid gap-4 lg:grid-cols-2">
                    <div className="rounded-xl bg-slate-50 p-4">
                      <h4 className="font-semibold mb-2">Instructions</h4>
                      <ul className="list-disc pl-5 space-y-1 text-sm">
                        {item.instructions.map((line, i) => (
                          <li key={i}>{line}</li>
                        ))}
                      </ul>
                    </div>

                    <div className="rounded-xl bg-amber-50 p-4">
                      <h4 className="font-semibold mb-2">Warnings</h4>
                      <ul className="list-disc pl-5 space-y-1 text-sm">
                        {item.warnings.map((line, i) => (
                          <li key={i}>{line}</li>
                        ))}
                      </ul>
                    </div>

                    <div className="rounded-xl bg-rose-50 p-4">
                      <h4 className="font-semibold mb-2">What to Avoid</h4>
                      <ul className="list-disc pl-5 space-y-1 text-sm">
                        {item.avoid.map((line, i) => (
                          <li key={i}>{line}</li>
                        ))}
                      </ul>
                    </div>

                    <div className="rounded-xl bg-emerald-50 p-4">
                      <h4 className="font-semibold mb-2">When to Review Doctor</h4>
                      <ul className="list-disc pl-5 space-y-1 text-sm">
                        {item.doctorReview.map((line, i) => (
                          <li key={i}>{line}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="rounded-2xl border bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold">Discharge Summary</h2>
          <div className="mt-4 grid gap-3 text-sm text-slate-700">
            <div><span className="font-semibold">Patient ID:</span> {patientId || "-"}</div>
            <div><span className="font-semibold">Patient Name:</span> {patientName || "-"}</div>
            <div><span className="font-semibold">Diagnosis:</span> {diagnosis || "-"}</div>
            <div><span className="font-semibold">Follow-up:</span> {followUp || "-"}</div>
          </div>
        </div>
      </div>
    </div>
  )
}
