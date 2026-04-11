type SeverityLevel = "GREEN" | "YELLOW" | "RED"

type SuggestionResult = {
  labs: string[]
  drugs: string[]
  routing: string[]
  alerts: string[]
  severity: SeverityLevel
  diagnoses: string[]
}

export function getClinicalSuggestions(input: string): SuggestionResult {
  const text = input.toLowerCase()

  const labs = new Set<string>()
  const drugs = new Set<string>()
  const routing = new Set<string>()
  const alerts = new Set<string>()
  const diagnoses = new Set<string>()

  let severity: SeverityLevel = "GREEN"

  if (
    text.includes("chest pain") ||
    text.includes("shortness of breath") ||
    text.includes("palpit") ||
    text.includes("sweating")
  ) {
    labs.add("Troponin")
    labs.add("CK-MB")
    labs.add("CBC")
    labs.add("CRP")
    routing.add("Cardiology")
    routing.add("Emergency")
    alerts.add("Rule out acute coronary syndrome")
    diagnoses.add("Possible Acute Coronary Syndrome")
    severity = "RED"
  }

  if (
    text.includes("sepsis") ||
    text.includes("shock") ||
    text.includes("very ill")
  ) {
    labs.add("CBC")
    labs.add("CRP")
    labs.add("Blood Culture")
    labs.add("ABG")
    routing.add("Emergency")
    alerts.add("Urgent escalation required")
    diagnoses.add("Possible Sepsis")
    severity = "RED"
  }

  if (
    text.includes("fever") ||
    text.includes("infection") ||
    text.includes("sore throat") ||
    text.includes("cough")
  ) {
    labs.add("CBC")
    labs.add("CRP")
    labs.add("ESR")
    drugs.add("Paracetamol")
    routing.add("Internal Medicine")
    alerts.add("Assess for infectious source before antibiotics")
    diagnoses.add("Possible Infection")
    if (severity !== "RED") severity = "YELLOW"
  }

  if (
    text.includes("diabetes") ||
    text.includes("high sugar") ||
    text.includes("polyuria") ||
    text.includes("polydipsia")
  ) {
    labs.add("Glucose")
    labs.add("HbA1c")
    labs.add("Creatinine")
    routing.add("Endocrinology")
    drugs.add("Metformin")
    alerts.add("Review renal function before diabetic medication decisions")
    diagnoses.add("Possible Diabetes Mellitus")
    if (severity !== "RED") severity = "YELLOW"
  }

  if (
    text.includes("gastric") ||
    text.includes("heartburn") ||
    text.includes("gerd") ||
    text.includes("epigastric")
  ) {
    routing.add("Gastroenterology")
    drugs.add("Omeprazole")
    alerts.add("Exclude cardiac causes if upper abdominal/chest overlap exists")
    diagnoses.add("Possible Gastritis / GERD")
    if (severity === "GREEN") severity = "YELLOW"
  }

  if (
    text.includes("pain") ||
    text.includes("headache") ||
    text.includes("body ache")
  ) {
    drugs.add("Paracetamol")
  }

  if (
    text.includes("inflammation") ||
    text.includes("joint pain") ||
    text.includes("swelling")
  ) {
    drugs.add("Ibuprofen")
    labs.add("CRP")
    labs.add("ESR")
    alerts.add("Avoid NSAIDs in renal disease or gastric ulcer")
    diagnoses.add("Possible Inflammatory Condition")
    if (severity === "GREEN") severity = "YELLOW"
  }

  if (
    text.includes("uti") ||
    text.includes("urine infection") ||
    text.includes("dysuria")
  ) {
    labs.add("Urinalysis")
    labs.add("Urine Culture")
    routing.add("Internal Medicine")
    alerts.add("Confirm bacterial source before selecting antibiotics")
    diagnoses.add("Possible Urinary Tract Infection")
    if (severity === "GREEN") severity = "YELLOW"
  }

  return {
    labs: Array.from(labs),
    drugs: Array.from(drugs),
    routing: Array.from(routing),
    alerts: Array.from(alerts),
    severity,
    diagnoses: Array.from(diagnoses),
  }
}
