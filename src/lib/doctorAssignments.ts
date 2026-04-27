import { apiGet, apiPost, apiDelete } from "@/lib/api"

export type DoctorAssignmentRecord = {
  id: number
  patientId: string
  patientName: string
  department?: string
  condition?: string
  status?: string
}

export async function getDoctorAssignments(doctorId: string) {
  const data = await apiGet<DoctorAssignmentRecord[]>(
    `/doctor-assignments/${encodeURIComponent(doctorId)}`
  )
  return Array.isArray(data) ? data : []
}

export async function createDoctorAssignment(
  doctorId: string,
  payload: {
    patientId: string
    patientName: string
    department?: string
    condition?: string
    status?: string
  }
) {
  return apiPost<DoctorAssignmentRecord>(
    `/doctor-assignments/${encodeURIComponent(doctorId)}`,
    payload
  )
}

export async function updateDoctorAssignmentStatus(
  doctorId: string,
  assignmentId: number,
  status: string
) {
  return apiPost<DoctorAssignmentRecord>(
    `/doctor-assignments/${encodeURIComponent(doctorId)}/${assignmentId}/status`,
    { status }
  )
}

export async function removeDoctorAssignment(
  doctorId: string,
  assignmentId: number
) {
  const res = await fetch(
    `http://192.168.0.106:8000/doctor-assignments/${encodeURIComponent(doctorId)}/${assignmentId}`,
    {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
    }
  )

  if (!res.ok) {
    throw new Error("Failed to delete assignment")
  }

  return res.json()
}
