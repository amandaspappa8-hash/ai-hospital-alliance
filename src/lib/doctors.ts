import { apiGet } from "@/lib/api"

export type DoctorRecord = {
  id: string
  name: string
  specialty: string
  department: string
  experience: string
  status: "Available" | "In Surgery" | "On Call" | "Offline"
  rating: number
  patients: number
  schedule: string
  phone: string
}

export async function getDoctorsSummary() {
  const data = await apiGet<DoctorRecord[]>("/doctors/summary")
  return Array.isArray(data) ? data : []
}

export async function getDoctorsBySpecialty(name: string) {
  const data = await apiGet<DoctorRecord[]>(
    `/doctors/by-specialty/${encodeURIComponent(name)}`
  )
  return Array.isArray(data) ? data : []
}

export async function getDoctorById(doctorId: string) {
  return apiGet<DoctorRecord>(`/doctors/${encodeURIComponent(doctorId)}`)
}
