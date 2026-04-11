import { useEffect, useMemo, useState } from "react"
import { useSearchParams } from "react-router-dom"
import { apiGet, apiPost } from "@/lib/api"

type Appointment = {
  id: string
  patient: string
  department: string
  doctor: string
  time: string
  status: string
}

type AppointmentPayload = {
  patient: string
  department: string
  doctor: string
  time: string
  status: string
}

export default function AppointmentsPage() {
  const [searchParams] = useSearchParams()
  const doctorId = searchParams.get("doctorId") ?? ""
  const doctorName = searchParams.get("doctorName") ?? ""

  const [appointments, setAppointments] = useState<Appointment[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  const [showCreateForm, setShowCreateForm] = useState(false)
  const [saving, setSaving] = useState(false)

  const [form, setForm] = useState<AppointmentPayload>({
    patient: "",
    department: "",
    doctor: doctorName || "",
    time: "",
    status: "Scheduled",
  })

  useEffect(() => {
    setLoading(true)
    setError("")

    apiGet<Appointment[]>("/appointments")
      .then((data) => {
        setAppointments(Array.isArray(data) ? data : [])
      })
      .catch((err) => {
        setError(err instanceof Error ? err.message : "Failed to load appointments")
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  useEffect(() => {
    if (doctorName) {
      setForm((prev) => ({
        ...prev,
        doctor: doctorName,
      }))
    }
  }, [doctorName])

  const filteredAppointments = useMemo(() => {
    if (!doctorName && !doctorId) return appointments

    return appointments.filter((appointment) => {
      if (doctorName) {
        return appointment.doctor.toLowerCase() === doctorName.toLowerCase()
      }
      return true
    })
  }, [appointments, doctorId, doctorName])

  function handleChange(
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) {
    const { name, value } = e.target
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  async function handleCreateAppointment(e: React.FormEvent) {
    e.preventDefault()

    if (
      !form.patient.trim() ||
      !form.department.trim() ||
      !form.doctor.trim() ||
      !form.time.trim() ||
      !form.status.trim()
    ) {
      setError("Please fill in all appointment fields.")
      return
    }

    try {
      setSaving(true)
      setError("")

      const payload: AppointmentPayload = {
        patient: form.patient.trim(),
        department: form.department.trim(),
        doctor: form.doctor.trim(),
        time: form.time,
        status: form.status.trim(),
      }

      const created = await apiPost<Appointment>("/appointments", payload)

      setAppointments((prev) => [created, ...prev])

      setForm({
        patient: "",
        department: "",
        doctor: doctorName || "",
        time: "",
        status: "Scheduled",
      })

      setShowCreateForm(false)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create appointment")
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Appointments</h1>
          <p className="text-sm text-gray-500">
            {doctorName
              ? `Managing appointments for Dr. ${doctorName}`
              : "Manage all appointments from one page"}
          </p>
        </div>

        <button
          onClick={() => setShowCreateForm((prev) => !prev)}
          className="rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
        >
          {showCreateForm ? "Close Form" : "Create Appointment"}
        </button>
      </div>

      {error && (
        <div className="rounded-lg border border-red-300 bg-red-50 px-4 py-3 text-red-700">
          {error}
        </div>
      )}

      {showCreateForm && (
        <form
          onSubmit={handleCreateAppointment}
          className="grid gap-4 rounded-xl border bg-white p-5 shadow-sm md:grid-cols-2"
        >
          <div>
            <label className="mb-1 block text-sm font-medium">Patient Name</label>
            <input
              name="patient"
              value={form.patient}
              onChange={handleChange}
              placeholder="Enter patient name"
              className="w-full rounded-lg border px-3 py-2"
            />
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium">Department</label>
            <input
              name="department"
              value={form.department}
              onChange={handleChange}
              placeholder="Enter department"
              className="w-full rounded-lg border px-3 py-2"
            />
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium">Doctor</label>
            <input
              name="doctor"
              value={form.doctor}
              onChange={handleChange}
              placeholder="Enter doctor name"
              className="w-full rounded-lg border px-3 py-2"
            />
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium">Time</label>
            <input
              type="datetime-local"
              name="time"
              value={form.time}
              onChange={handleChange}
              className="w-full rounded-lg border px-3 py-2"
            />
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium">Status</label>
            <select
              name="status"
              value={form.status}
              onChange={handleChange}
              className="w-full rounded-lg border px-3 py-2"
            >
              <option value="Scheduled">Scheduled</option>
              <option value="Confirmed">Confirmed</option>
              <option value="Pending">Pending</option>
              <option value="Completed">Completed</option>
              <option value="Cancelled">Cancelled</option>
            </select>
          </div>

          <div className="md:col-span-2 flex gap-3">
            <button
              type="submit"
              disabled={saving}
              className="rounded-lg bg-green-600 px-4 py-2 text-white hover:bg-green-700 disabled:opacity-60"
            >
              {saving ? "Saving..." : "Save Appointment"}
            </button>

            <button
              type="button"
              onClick={() => setShowCreateForm(false)}
              className="rounded-lg border px-4 py-2 hover:bg-gray-50"
            >
              Cancel
            </button>
          </div>
        </form>
      )}

      <div className="rounded-xl border bg-white shadow-sm">
        {loading ? (
          <div className="p-6 text-sm text-gray-500">Loading appointments...</div>
        ) : filteredAppointments.length === 0 ? (
          <div className="p-6 text-sm text-gray-500">No appointments found.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full border-collapse text-sm">
              <thead>
                <tr className="border-b bg-gray-50 text-left">
                  <th className="px-4 py-3">Patient</th>
                  <th className="px-4 py-3">Department</th>
                  <th className="px-4 py-3">Doctor</th>
                  <th className="px-4 py-3">Time</th>
                  <th className="px-4 py-3">Status</th>
                </tr>
              </thead>
              <tbody>
                {filteredAppointments.map((appointment) => (
                  <tr key={appointment.id} className="border-b last:border-0">
                    <td className="px-4 py-3">{appointment.patient}</td>
                    <td className="px-4 py-3">{appointment.department}</td>
                    <td className="px-4 py-3">{appointment.doctor}</td>
                    <td className="px-4 py-3">{appointment.time}</td>
                    <td className="px-4 py-3">{appointment.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
