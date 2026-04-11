import { MEDICAL_DEPARTMENTS } from "./masterDepartments"

export function suggestDepartmentsFromText(input: string): string[] {
  const text = input.toLowerCase()
  const suggestions = new Set<string>()

  if (text.includes("chest pain") || text.includes("palpit") || text.includes("heart")) {
    suggestions.add("Cardiology")
    suggestions.add("Emergency")
  }

  if (text.includes("stroke") || text.includes("seizure") || text.includes("headache")) {
    suggestions.add("Neurology")
    suggestions.add("CT Scan")
    suggestions.add("MRI")
  }

  if (text.includes("fracture") || text.includes("trauma") || text.includes("joint")) {
    suggestions.add("Orthopedics")
    suggestions.add("X-Ray")
    suggestions.add("Emergency")
  }

  if (text.includes("cough") || text.includes("shortness of breath") || text.includes("pneumonia")) {
    suggestions.add("Pulmonology")
    suggestions.add("X-Ray")
    suggestions.add("CT Scan")
  }

  if (text.includes("pregnan") || text.includes("bleeding") || text.includes("pelvic pain")) {
    suggestions.add("Obstetrics")
    suggestions.add("Gynecology")
    suggestions.add("Ultrasound")
  }

  if (text.includes("depression") || text.includes("anxiety") || text.includes("panic")) {
    suggestions.add("Psychiatry")
    suggestions.add("Clinical Psychology")
  }

  if (text.includes("autism") || text.includes("adhd") || text.includes("behavior")) {
    suggestions.add("Child Psychology")
    suggestions.add("Behavioral Therapy")
  }

  if (text.includes("weakness") || text.includes("rehab") || text.includes("mobility")) {
    suggestions.add("Neurological Rehab")
    suggestions.add("Orthopedic Rehab")
  }

  if (text.includes("infection") || text.includes("fever")) {
    suggestions.add("Microbiology")
    suggestions.add("Clinical Chemistry")
  }

  if (text.includes("drug") || text.includes("interaction") || text.includes("dose")) {
    suggestions.add("Clinical Pharmacy")
  }

  return Array.from(suggestions)
}

export function getDepartmentGroups() {
  return MEDICAL_DEPARTMENTS
}
