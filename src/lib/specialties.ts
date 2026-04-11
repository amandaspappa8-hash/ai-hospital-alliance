import { apiGet } from "@/lib/api"

export type SpecialtyRecord = {
  title: string
  subtitle: string
  icon: string
  route: string
  doctors: number
  activeCases: number
  tone: string
}

export async function getSpecialtiesSummary() {
  const data = await apiGet<SpecialtyRecord[]>("/specialties/summary")
  return Array.isArray(data) ? data : []
}
