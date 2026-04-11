export type DrugItem = {
  name: string
  category: string
  form: string
  adultDose: string
  pediatricDose: string
  frequency: string
  maxDose: string
  warnings: string[]
  notes: string[]
}

export const drugCatalog: DrugItem[] = [
  {
    name: "Paracetamol",
    category: "Analgesic / Antipyretic",
    form: "Tablet, Syrup, IV",
    adultDose: "500–1000 mg",
    pediatricDose: "10–15 mg/kg/dose",
    frequency: "Every 4–6 hours",
    maxDose: "4 g/day adult",
    warnings: ["Use caution in liver disease", "Avoid duplicate combination products"],
    notes: ["Common for fever and pain", "Often first-line for mild pain"],
  },
  {
    name: "Ibuprofen",
    category: "NSAID",
    form: "Tablet, Syrup",
    adultDose: "200–400 mg",
    pediatricDose: "5–10 mg/kg/dose",
    frequency: "Every 6–8 hours",
    maxDose: "2400 mg/day adult",
    warnings: ["Avoid in gastric ulcer", "Use caution in kidney disease"],
    notes: ["Useful for inflammatory pain", "Give after food"],
  },
  {
    name: "Amoxicillin",
    category: "Antibiotic",
    form: "Capsule, Suspension",
    adultDose: "500 mg",
    pediatricDose: "20–40 mg/kg/day",
    frequency: "Every 8 hours",
    maxDose: "Based on indication",
    warnings: ["Check penicillin allergy"],
    notes: ["Common in ENT and respiratory infections"],
  },
  {
    name: "Ceftriaxone",
    category: "Antibiotic",
    form: "IV, IM",
    adultDose: "1–2 g",
    pediatricDose: "50–100 mg/kg/day",
    frequency: "Once daily or divided",
    maxDose: "4 g/day",
    warnings: ["Assess allergy history", "Broad-spectrum use should be justified"],
    notes: ["Common inpatient antibiotic"],
  },
  {
    name: "Metformin",
    category: "Antidiabetic",
    form: "Tablet",
    adultDose: "500 mg starting dose",
    pediatricDose: "Specialist-guided",
    frequency: "1–2 times daily with meals",
    maxDose: "2000–2550 mg/day",
    warnings: ["Avoid in severe renal failure", "GI upset is common early"],
    notes: ["First-line in type 2 diabetes"],
  },
  {
    name: "Omeprazole",
    category: "PPI",
    form: "Capsule, IV",
    adultDose: "20–40 mg",
    pediatricDose: "Weight-based",
    frequency: "Once daily",
    maxDose: "Depends on indication",
    warnings: ["Review long-term use"],
    notes: ["Used for GERD and gastric protection"],
  },
]
