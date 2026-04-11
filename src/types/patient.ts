export type PatientDepartment =
  | "Cardiology"
  | "Neurology"
  | "Orthopedics"
  | "Radiology"
  | "ER"
  | "Lab"

export type PatientStatus =
  | "In care"
  | "Waiting"
  | "Discharged"

export interface Patient {
  id: string
  name: string
  department: PatientDepartment
  status: PatientStatus
}
