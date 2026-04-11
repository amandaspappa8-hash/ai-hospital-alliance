import { apiGet } from "@/lib/api"
import type { Patient } from "@/types/patient"

export function getPatients() {
  return apiGet<Patient[]>("/patients")
}
