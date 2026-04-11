import type { SmartOrder } from "@/types/clinical"

export function buildSmartOrders(patient: any): SmartOrder[] {
  const condition = String(patient?.condition ?? "").toLowerCase()

  if (condition.includes("chest") || condition.includes("card")) {
    return [
      {
        id: "ord-1",
        name: "ECG",
        priority: "high",
        department: "Cardiology",
        note: "Immediate cardiac screening",
        status: "draft",
      },
      {
        id: "ord-2",
        name: "Troponin",
        priority: "high",
        department: "Laboratory",
        note: "Rule out acute coronary syndrome",
        status: "draft",
      },
      {
        id: "ord-3",
        name: "Oxygen Monitoring",
        priority: "medium",
        department: "Emergency",
        note: "Continuous SpO2 observation",
        status: "draft",
      },
    ]
  }

  return [
    {
      id: "ord-1",
      name: "CBC",
      priority: "medium",
      department: "Laboratory",
      note: "Baseline screening",
      status: "draft",
    },
    {
      id: "ord-2",
      name: "Vital Signs Monitoring",
      priority: "medium",
      department: "Nursing",
      note: "Routine monitoring",
      status: "draft",
    },
  ]
}
