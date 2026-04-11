export type DrugRisk = {
  drug: string
  risk: string
  severity: "LOW" | "MODERATE" | "HIGH" | "CRITICAL"
  recommendation: string
}

export function analyzeDrugIntelligence(
  meds: string[],
  age?: number,
  renal?: boolean,
  pregnant?: boolean,
): DrugRisk[] {

  const risks: DrugRisk[] = []

  const list = meds.map(m => m.toLowerCase())

  // NSAID + Aspirin bleeding
  if (list.includes("aspirin") && list.includes("ibuprofen")) {
    risks.push({
      drug: "Aspirin + Ibuprofen",
      risk: "Bleeding risk",
      severity: "HIGH",
      recommendation: "Avoid combination unless physician approves",
    })
  }

  // Renal risk
  if (renal && list.includes("metformin")) {
    risks.push({
      drug: "Metformin",
      risk: "Lactic acidosis risk in renal impairment",
      severity: "CRITICAL",
      recommendation: "Consider dose reduction or hold",
    })
  }

  // Elderly sedation
  if (age && age > 65 && list.includes("diazepam")) {
    risks.push({
      drug: "Diazepam",
      risk: "Fall / confusion risk",
      severity: "HIGH",
      recommendation: "Avoid in elderly if possible",
    })
  }

  // Pregnancy ACE inhibitor
  if (pregnant && list.includes("enalapril")) {
    risks.push({
      drug: "Enalapril",
      risk: "Fetal toxicity",
      severity: "CRITICAL",
      recommendation: "Stop immediately and switch therapy",
    })
  }

  // QT prolongation
  if (list.includes("azithromycin") && list.includes("ciprofloxacin")) {
    risks.push({
      drug: "Azithromycin + Ciprofloxacin",
      risk: "QT prolongation",
      severity: "HIGH",
      recommendation: "ECG monitoring required",
    })
  }

  return risks
}
