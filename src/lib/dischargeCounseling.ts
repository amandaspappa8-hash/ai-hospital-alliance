export type DischargeMedicationInput = {
  name: string
  dose: string
  frequency: string
  duration: string
  route?: string
}

export type DischargeMedicationOutput = {
  name: string
  dose: string
  frequency: string
  duration: string
  route: string
  instructions: string[]
  warnings: string[]
  avoid: string[]
  doctorReview: string[]
}

function lower(value: string) {
  return value.trim().toLowerCase()
}

export function buildDischargeCounseling(
  meds: DischargeMedicationInput[],
): DischargeMedicationOutput[] {
  return meds.map((med) => {
    const name = lower(med.name)
    const route = med.route?.trim() || "PO"

    const item: DischargeMedicationOutput = {
      name: med.name,
      dose: med.dose,
      frequency: med.frequency,
      duration: med.duration,
      route,
      instructions: [],
      warnings: [],
      avoid: [],
      doctorReview: [],
    }

    if (name.includes("amoxicillin")) {
      item.instructions.push(
        "Take the antibiotic exactly on time every day.",
        "Complete the full course even if the patient feels better.",
        "Take after food if stomach upset occurs.",
      )
      item.warnings.push(
        "Stop and seek medical advice if rash, swelling, or breathing difficulty appears.",
        "Mild diarrhea can occur, but severe diarrhea needs medical review.",
      )
      item.avoid.push(
        "Do not skip doses.",
        "Do not stop early without medical advice.",
      )
      item.doctorReview.push(
        "Review urgently if allergy symptoms appear.",
        "Review if fever persists or symptoms worsen after 48-72 hours.",
      )
    } else if (name.includes("azithromycin")) {
      item.instructions.push(
        "Take once daily at the same time each day.",
        "Can be taken with food if nausea occurs.",
      )
      item.warnings.push(
        "Seek medical review for palpitations, severe diarrhea, or allergic reaction.",
      )
      item.avoid.push(
        "Avoid missing doses.",
      )
      item.doctorReview.push(
        "Review if chest symptoms worsen or high fever continues.",
      )
    } else if (name.includes("ibuprofen")) {
      item.instructions.push(
        "Take after food.",
        "Use the lowest effective dose for the shortest duration.",
      )
      item.warnings.push(
        "Stop if there is stomach pain, black stool, vomiting blood, or breathing worsening.",
      )
      item.avoid.push(
        "Avoid taking it on an empty stomach.",
        "Avoid combining with other NSAIDs unless prescribed.",
      )
      item.doctorReview.push(
        "Review if pain remains uncontrolled or stomach symptoms start.",
      )
    } else if (name.includes("paracetamol") || name.includes("acetaminophen")) {
      item.instructions.push(
        "Take only as prescribed.",
        "Keep the total daily dose within the prescribed limit.",
      )
      item.warnings.push(
        "Too much can seriously harm the liver.",
      )
      item.avoid.push(
        "Avoid taking multiple cold/flu medicines that also contain paracetamol.",
        "Avoid alcohol excess.",
      )
      item.doctorReview.push(
        "Review if pain or fever continues despite treatment.",
      )
    } else if (name.includes("metformin")) {
      item.instructions.push(
        "Take with meals.",
        "Continue hydration unless told otherwise by a clinician.",
      )
      item.warnings.push(
        "Seek review if severe vomiting, dehydration, unusual weakness, or trouble breathing develops.",
      )
      item.avoid.push(
        "Avoid skipping meals while taking it unless instructed.",
      )
      item.doctorReview.push(
        "Review if persistent diarrhea, vomiting, or poor oral intake develops.",
      )
    } else if (name.includes("insulin")) {
      item.instructions.push(
        "Take exactly as instructed.",
        "Check blood sugar as advised.",
        "Rotate injection sites.",
      )
      item.warnings.push(
        "Low blood sugar can cause sweating, shakiness, confusion, or fainting.",
      )
      item.avoid.push(
        "Avoid skipping meals after taking insulin unless specifically instructed.",
      )
      item.doctorReview.push(
        "Urgent review for repeated hypoglycemia or very high glucose readings.",
      )
    } else if (name.includes("amlodipine")) {
      item.instructions.push(
        "Take once daily at the same time.",
        "Rise slowly from sitting if dizziness occurs.",
      )
      item.warnings.push(
        "Leg swelling or severe dizziness should be reviewed.",
      )
      item.avoid.push(
        "Avoid stopping suddenly without medical advice.",
      )
      item.doctorReview.push(
        "Review if blood pressure stays high or swelling becomes significant.",
      )
    } else if (name.includes("furosemide")) {
      item.instructions.push(
        "Take in the morning.",
        "A second dose, if prescribed, is usually taken earlier in the day.",
      )
      item.warnings.push(
        "Can cause dehydration, low blood pressure, or low potassium.",
      )
      item.avoid.push(
        "Avoid taking late at night if possible because of frequent urination.",
      )
      item.doctorReview.push(
        "Review if dizziness, severe weakness, cramps, or reduced urine develops.",
      )
    } else if (name.includes("omeprazole")) {
      item.instructions.push(
        "Take before food, ideally before breakfast.",
      )
      item.warnings.push(
        "Persistent vomiting, weight loss, or black stool needs review.",
      )
      item.avoid.push(
        "Avoid unnecessary long-term use without follow-up.",
      )
      item.doctorReview.push(
        "Review if symptoms continue despite treatment.",
      )
    } else if (name.includes("salbutamol")) {
      item.instructions.push(
        "Use exactly as instructed.",
        "Use inhaler technique correctly.",
      )
      item.warnings.push(
        "If relief is short-lived or breathing worsens, seek urgent care.",
      )
      item.avoid.push(
        "Avoid relying on frequent rescue use without clinician review.",
      )
      item.doctorReview.push(
        "Urgent review if wheeze or shortness of breath increases.",
      )
    } else {
      item.instructions.push(
        "Take this medicine exactly as prescribed.",
        "Keep a regular schedule and do not miss doses.",
      )
      item.warnings.push(
        "Seek medical advice for allergy symptoms, severe side effects, or worsening condition.",
      )
      item.avoid.push(
        "Avoid changing the dose without medical advice.",
      )
      item.doctorReview.push(
        "Review if symptoms worsen or the medicine is not helping.",
      )
    }

    return item
  })
}
