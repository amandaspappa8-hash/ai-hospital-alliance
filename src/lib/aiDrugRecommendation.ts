export type DrugAIRecommendation = {
  summary: string
  majorWarning: string
  contraindication: string
  recommendation: string
  counseling: string
}

export function buildDrugAIRecommendation(input: {
  drugName?: string
  indications?: string
  warnings?: string
  doNotUse?: string
  askDoctor?: string
  askPharmacist?: string
  stopUse?: string
}): DrugAIRecommendation {
  const name = (input.drugName || "").toLowerCase()
  const indications = input.indications || ""
  const warnings = input.warnings || ""
  const doNotUse = input.doNotUse || ""
  const askDoctor = input.askDoctor || ""
  const askPharmacist = input.askPharmacist || ""
  const stopUse = input.stopUse || ""

  if (name.includes("aspirin")) {
    return {
      summary: "Aspirin is commonly used as an antiplatelet drug or for pain relief depending on the dose.",
      majorWarning: warnings || "Major bleeding risk increases with NSAIDs, anticoagulants, steroids, alcohol use, and GI ulcer history.",
      contraindication: doNotUse || "Avoid in active bleeding, severe aspirin allergy, and uncontrolled GI bleeding risk unless clinician-approved.",
      recommendation: "Avoid combining aspirin with ibuprofen unless there is a strong clinical reason and bleeding risk has been reviewed.",
      counseling: "Take exactly as prescribed and seek urgent review if black stool, vomiting blood, unusual bleeding, or severe dizziness occurs.",
    }
  }

  if (name.includes("atorvastatin")) {
    return {
      summary: "Atorvastatin is used to reduce cholesterol and lower cardiovascular risk.",
      majorWarning: warnings || "Monitor for muscle pain, dark urine, liver symptoms, and major drug interactions.",
      contraindication: doNotUse || "Avoid in active liver disease or severe statin intolerance unless specialist review supports use.",
      recommendation: "Review liver risk, muscle symptoms, and interacting drugs if the patient reports weakness or pain.",
      counseling: "Take once daily as prescribed and report severe muscle pain, jaundice, or dark urine immediately.",
    }
  }

  if (name.includes("ibuprofen")) {
    return {
      summary: "Ibuprofen is an NSAID used for pain, inflammation, and fever control.",
      majorWarning: warnings || "GI bleeding, renal injury, and NSAID interaction risk may be clinically important.",
      contraindication: doNotUse || "Avoid in active GI bleeding, severe NSAID allergy, and certain renal-risk patients without clinical review.",
      recommendation: "Avoid combining ibuprofen with aspirin when possible because bleeding and GI risk can increase.",
      counseling: "Take after food and stop the medicine if severe stomach pain, bleeding, black stool, or allergy symptoms appear.",
    }
  }

  if (name.includes("metoprolol")) {
    return {
      summary: "Metoprolol is a beta blocker used for rate control, blood pressure, and cardiac protection.",
      majorWarning: warnings || "May cause bradycardia, hypotension, fatigue, or worsening symptoms in selected patients.",
      contraindication: doNotUse || "Avoid in severe bradycardia, cardiogenic shock, or unstable conduction problems unless specifically managed.",
      recommendation: "Review pulse, blood pressure, dizziness, and asthma history before continuing or escalating treatment.",
      counseling: "Do not stop suddenly. Seek review if fainting, severe dizziness, slow pulse, or breathing worsens.",
    }
  }

  return {
    summary: indications || "Drug information available but still needs clinical review.",
    majorWarning: warnings || "Review the full warning profile before prescribing or dispensing.",
    contraindication: doNotUse || "Review contraindications carefully before final medication decision.",
    recommendation: askDoctor || askPharmacist || "Use physician or pharmacist review before final medication use.",
    counseling: stopUse || "Educate the patient about side effects, red flags, and when to seek medical review.",
  }
}
