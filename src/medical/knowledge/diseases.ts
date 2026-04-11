export type DiseaseKnowledge = {
  name: string
  symptoms: string[]
  labs: string[]
  routing: string
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"
  medications: string[]
  alerts: string[]
}

export const DISEASE_DB: DiseaseKnowledge[] = [
  {
    name: "Acute Coronary Syndrome",
    symptoms: ["chest pain", "shortness of breath", "sweating", "nausea"],
    labs: ["Troponin", "CK-MB", "CBC", "CRP"],
    routing: "Cardiology",
    severity: "CRITICAL",
    medications: ["Aspirin"],
    alerts: ["Urgent cardiac evaluation required"],
  },
  {
    name: "Sepsis",
    symptoms: ["fever", "hypotension", "confusion", "tachycardia", "shock"],
    labs: ["CBC", "CRP", "Blood Culture", "Lactate", "ABG"],
    routing: "Emergency",
    severity: "CRITICAL",
    medications: ["Broad Spectrum Antibiotics"],
    alerts: ["Urgent escalation required"],
  },
  {
    name: "Upper Respiratory Infection",
    symptoms: ["fever", "cough", "sore throat"],
    labs: ["CBC", "CRP"],
    routing: "Internal Medicine",
    severity: "MEDIUM",
    medications: ["Paracetamol"],
    alerts: ["Assess infectious source before antibiotics"],
  },
  {
    name: "Pneumonia",
    symptoms: ["fever", "cough", "shortness of breath", "chest pain"],
    labs: ["CBC", "CRP", "ABG"],
    routing: "Internal Medicine",
    severity: "HIGH",
    medications: ["Paracetamol"],
    alerts: ["Consider chest imaging if respiratory symptoms worsen"],
  },
  {
    name: "Diabetes Mellitus",
    symptoms: ["polyuria", "polydipsia", "fatigue", "high sugar"],
    labs: ["Glucose", "HbA1c", "Creatinine"],
    routing: "Endocrinology",
    severity: "MEDIUM",
    medications: ["Metformin"],
    alerts: ["Review renal function before diabetic medication decisions"],
  },
  {
    name: "Urinary Tract Infection",
    symptoms: ["dysuria", "urine infection", "uti", "fever"],
    labs: ["Urinalysis", "Urine Culture", "CBC"],
    routing: "Internal Medicine",
    severity: "MEDIUM",
    medications: ["Paracetamol"],
    alerts: ["Confirm bacterial source before selecting antibiotics"],
  },
  {
    name: "Gastritis / GERD",
    symptoms: ["heartburn", "gerd", "epigastric", "gastric"],
    labs: ["CBC"],
    routing: "Gastroenterology",
    severity: "LOW",
    medications: ["Omeprazole"],
    alerts: ["Exclude cardiac causes if symptoms overlap with chest pain"],
  },
  {
    name: "Inflammatory Joint Disorder",
    symptoms: ["joint pain", "swelling", "inflammation"],
    labs: ["CRP", "ESR", "CBC"],
    routing: "Internal Medicine",
    severity: "MEDIUM",
    medications: ["Ibuprofen"],
    alerts: ["Avoid NSAIDs in renal disease or gastric ulcer"],
  }
]
