// src/lib/imaging-store.ts
export type Modality = "XRAY" | "CT" | "MRI" | "ULTRASOUND" | "ECG" | "EEG" | "PET"

export type ImagingOrder = {
  id: string
  patientId: string
  patientName: string
  modality: Modality
  studyDescription: string
  priority: "ROUTINE" | "URGENT"
  status: "ORDERED" | "SCHEDULED" | "IN_PROGRESS" | "COMPLETED"
  createdAt: string
}

export type ImagingStudy = {
  studyId: string
  orderId: string
  patientId: string
  patientName: string
  modality: Modality
  description: string
  status: "AVAILABLE" | "PROCESSING"
  studyDate: string
  seriesCount: number
  instanceCount: number
  viewerUrl?: string // later: OHIF / DICOMweb URL
}

const KEY_ORDERS = "aha_imaging_orders_v1"
const KEY_STUDIES = "aha_imaging_studies_v1"

function load<T>(key: string, fallback: T): T {
  try {
    const raw = localStorage.getItem(key)
    if (!raw) return fallback
    return JSON.parse(raw) as T
  } catch {
    return fallback
  }
}

function save<T>(key: string, value: T) {
  localStorage.setItem(key, JSON.stringify(value))
}

export function listOrders(): ImagingOrder[] {
  return load<ImagingOrder[]>(KEY_ORDERS, [])
}

export function listStudies(): ImagingStudy[] {
  return load<ImagingStudy[]>(KEY_STUDIES, [])
}

export function createOrder(input: Omit<ImagingOrder, "id" | "status" | "createdAt">): ImagingOrder {
  const orders = listOrders()
  const order: ImagingOrder = {
    ...input,
    id: String(Date.now()),
    status: "ORDERED",
    createdAt: new Date().toISOString(),
  }
  save(KEY_ORDERS, [order, ...orders])

  // Auto-create a demo study to simulate PACS arrival (later: real DICOM)
  const studies = listStudies()
  const study: ImagingStudy = {
    studyId: `STUDY-${order.id}`,
    orderId: order.id,
    patientId: order.patientId,
    patientName: order.patientName,
    modality: order.modality,
    description: order.studyDescription,
    status: "AVAILABLE",
    studyDate: new Date().toISOString(),
    seriesCount: Math.floor(Math.random() * 6) + 1,
    instanceCount: Math.floor(Math.random() * 300) + 50,
    viewerUrl: `/pacs?study=${encodeURIComponent(`STUDY-${order.id}`)}`,
  }
  save(KEY_STUDIES, [study, ...studies])

  return order
}

export function clearImagingDemo() {
  localStorage.removeItem(KEY_ORDERS)
  localStorage.removeItem(KEY_STUDIES)
}

export function getStudyById(studyId: string): ImagingStudy | undefined {
  return listStudies().find((s) => s.studyId === studyId)
}
