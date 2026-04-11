export type PatientRiskResult = {
  score: number
  level: "LOW" | "MODERATE" | "HIGH" | "CRITICAL"
  summary: string
  recommendation: string
}

export function calculatePatientRisk(input: {
  highRiskFindings: number
  moderateRiskFindings: number
  hasUnsafeCombination: boolean
  missingOnDischarge: boolean
  age?: number
}): PatientRiskResult {
  let score = 0

  score += input.highRiskFindings * 30
  score += input.moderateRiskFindings * 10

  if (input.hasUnsafeCombination) score += 20
  if (input.missingOnDischarge) score += 25
  if ((input.age || 0) >= 65) score += 10

  if (score >= 90) {
    return {
      score,
      level: "CRITICAL",
      summary: "Critical medication-related risk detected.",
      recommendation:
        "Immediate physician/pharmacist escalation and consider monitored admission or ICU-level review.",
    }
  }

  if (score >= 60) {
    return {
      score,
      level: "HIGH",
      summary: "High medication safety risk detected.",
      recommendation:
        "Urgent pharmacist and physician review required before discharge.",
    }
  }

  if (score >= 30) {
    return {
      score,
      level: "MODERATE",
      summary: "Moderate medication-related risk detected.",
      recommendation:
        "Close review recommended with discharge verification.",
    }
  }

  return {
    score,
    level: "LOW",
    summary: "Low medication-related risk.",
    recommendation: "Routine monitoring and standard discharge counseling.",
  }
}
