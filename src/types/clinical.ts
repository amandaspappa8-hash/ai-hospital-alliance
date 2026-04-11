export type VisitTimelineItem = {
  id: string
  time: string
  title: string
  description: string
  status?: string
}

export type SmartOrder = {
  id: string
  name: string
  priority: "high" | "medium" | "low"
  department: string
  note?: string
  status?: string
}

export type DigitalSignature = {
  doctorName: string
  role: string
  signedAt: string
  signatureText: string
}

export type DecisionEngineResult = {
  impression: string
  plan: string[]
  nextStep: string
  riskLevel: "high" | "medium" | "low"
}
