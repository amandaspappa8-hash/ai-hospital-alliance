import { apiGet, apiPost } from "@/lib/api"

export type AppointmentRecord = {
  id: string
  patient: string
  department: string
  doctor: string
  time: string
  status: string
}

export async function getAppointments() {
  const data = await apiGet<AppointmentRecord[]>("/appointments")
  return Array.isArray(data) ? data : []
}

export async function createAppointment(payload: {
  patient: string
  department: string
  doctor: string
  time: string
  status?: string
}) {
  return apiPost<AppointmentRecord>("/appointments", payload)
}
