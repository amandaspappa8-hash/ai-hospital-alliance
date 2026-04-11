import { DISEASE_DB } from "./knowledge/diseases"

export type DiagnosisConfidence = {
  name: string
  confidence: number
  rank: number
}

export type ClinicalVitals = {
  hr: number
  sbp: number
  temp: number
  spo2: number
}

export type KnowledgeMatch = {
  diagnoses: string[]
  diagnosisScores: DiagnosisConfidence[]
  labs: string[]
  routing: string[]
  drugs: string[]
  alerts: string[]
  actions: string[]
  severity: "GREEN" | "YELLOW" | "RED"
  riskScore: number
  clinicalImpression: string
  recommendedPlan: string
  nextStepSummary: string
}

export function knowledgeEngine(
  input: string,
  vitals?: Partial<ClinicalVitals>
): KnowledgeMatch {
  const text = input.toLowerCase()

  const hr = Number(vitals?.hr ?? 80)
  const sbp = Number(vitals?.sbp ?? 120)
  const temp = Number(vitals?.temp ?? 37)
  const spo2 = Number(vitals?.spo2 ?? 98)

  const matches = DISEASE_DB
    .map((disease) => {
      const totalSymptoms = Math.max(disease.symptoms.length, 1)
      const matchedSymptoms = disease.symptoms.filter((symptom) =>
        text.includes(symptom.toLowerCase())
      ).length

      const confidence = Math.min(
        100,
        Math.round((matchedSymptoms / totalSymptoms) * 100)
      )

      return {
        disease,
        matchedSymptoms,
        confidence,
      }
    })
    .filter((item) => item.matchedSymptoms > 0)
    .sort((a, b) => {
      if (b.confidence !== a.confidence) return b.confidence - a.confidence
      return b.matchedSymptoms - a.matchedSymptoms
    })

  const diagnoses = new Set<string>()
  const labs = new Set<string>()
  const routing = new Set<string>()
  const drugs = new Set<string>()
  const alerts = new Set<string>()
  const actions = new Set<string>()
  const diagnosisScores: DiagnosisConfidence[] = []
  let riskScore = 0
  let severity: "GREEN" | "YELLOW" | "RED" = "GREEN"
  const topMatches = matches.slice(0, 3)

  topMatches.forEach((match, index) => {
    diagnoses.add(match.disease.name)

    diagnosisScores.push({
      name: match.disease.name,
      confidence: match.confidence,
      rank: index + 1,
    })

    match.disease.labs.forEach((lab) => labs.add(lab))
    routing.add(match.disease.routing)
    match.disease.medications.forEach((drug) => drugs.add(drug))
    match.disease.alerts.forEach((alert) => alerts.add(alert))

    const symptomScore = Math.min(match.matchedSymptoms * 15, 45)
    riskScore = Math.max(riskScore, symptomScore)

    if (match.disease.severity === "CRITICAL") {
      severity = "RED"
      riskScore = Math.max(riskScore, 90)
    } else if (match.disease.severity === "HIGH") {
      severity = "RED"
      riskScore = Math.max(riskScore, 75)
    } else if (match.disease.severity === "MEDIUM") {
      severity = "YELLOW"
      riskScore = Math.max(riskScore, 50)
    } else if (match.disease.severity === "LOW") {
      riskScore = Math.max(riskScore, 25)
    }
  })

  if (hr >= 130) {
    riskScore = Math.max(riskScore, 88)
    severity = "RED"
    alerts.add("Severe tachycardia")
    actions.add("Immediate Cardiac Monitoring")
  } else if (hr >= 110) {
    riskScore = Math.max(riskScore, 68)
    severity = "YELLOW"
    alerts.add("Tachycardia detected")
  }

  if (sbp <= 90) {
    riskScore = Math.max(riskScore, 92)
    severity = "RED"
    alerts.add("Hypotension / possible shock")
    actions.add("Immediate Emergency Management")
    actions.add("IV Access and Hemodynamic Support")
  } else if (sbp <= 100) {
    riskScore = Math.max(riskScore, 70)
    severity = "YELLOW"
    alerts.add("Low blood pressure")
  }

  if (temp >= 39.5) {
    riskScore = Math.max(riskScore, 80)
    severity = "YELLOW"
    alerts.add("High fever")
  } else if (temp >= 38) {
    riskScore = Math.max(riskScore, 55)
    if (severity === "GREEN") severity = "YELLOW"
    alerts.add("Fever present")
  }

  if (spo2 < 90) {
    riskScore = Math.max(riskScore, 95)
    severity = "RED"
    alerts.add("Critical hypoxia")
    actions.add("ICU")
    actions.add("Oxygen Support")
    actions.add("Immediate Respiratory Assessment")
  } else if (spo2 < 94) {
    riskScore = Math.max(riskScore, 78)
    severity = "YELLOW"
    alerts.add("Low oxygen saturation")
    actions.add("Supplemental Oxygen Consideration")
  }

  if (riskScore >= 90) {
    actions.add("ICU")
    actions.add("Immediate Emergency Management")
    actions.add("Continuous Monitoring")
    actions.add("Urgent Specialist Review")
  } else if (riskScore >= 70) {
    actions.add("Admit")
    actions.add("Urgent Workup")
    actions.add("Cardiac / Medical Monitoring")
    actions.add("Specialist Consultation")
  } else if (riskScore >= 40) {
    actions.add("Observe")
    actions.add("Order Labs")
    actions.add("Reassess in Short Interval")
  } else {
    actions.add("Discharge")
    actions.add("Outpatient Follow-up")
    actions.add("Symptomatic Treatment")
  }

  if (matches.length === 0) {
    diagnoses.add("General Clinical Review Needed")
    diagnosisScores.push({
      name: "General Clinical Review Needed",
      confidence: 35,
      rank: 1,
    })
    labs.add("CBC")
    routing.add("General Practice")
    drugs.add("Paracetamol")
    if (riskScore < 40) {
      actions.clear()
      actions.add("Discharge")
      actions.add("Outpatient Follow-up")
      severity = "GREEN"
      riskScore = Math.max(riskScore, 15)
    }
  }

  riskScore = Math.max(0, Math.min(100, riskScore))

  const topDiagnosis = diagnosisScores[0]?.name ?? "General Clinical Review Needed"
  const routingText = Array.from(routing).join(", ") || "General Practice"
  const labsText = Array.from(labs).join(", ") || "CBC"
  const drugsText = Array.from(drugs).join(", ") || "Supportive treatment"
  const actionsText = Array.from(actions).join(", ")

  const clinicalImpression = `Primary concern: ${topDiagnosis}. Severity is ${severity} with estimated risk score ${riskScore}/100.`
  const recommendedPlan = `Recommended routing: ${routingText}. Suggested labs: ${labsText}. Suggested medications: ${drugsText}.`
  const nextStepSummary = `Immediate next steps: ${actionsText}. Monitor vitals closely and reassess based on response and investigation results.`

  return {
    diagnoses: Array.from(diagnoses),
    diagnosisScores,
    labs: Array.from(labs),
    routing: Array.from(routing),
    drugs: Array.from(drugs),
    alerts: Array.from(alerts),
    actions: Array.from(actions),
    severity,
    riskScore,
    clinicalImpression,
    recommendedPlan,
    nextStepSummary,
  }
}
