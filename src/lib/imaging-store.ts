export type Modality = "XRAY" | "CT" | "MRI" | "ULTRASOUND" | "ECG" | "EEG" | "PET"

export type ImagingOrder = {
  id: string; patientId: string; patientName: string
  modality: Modality; studyDescription: string
  priority: "ROUTINE" | "URGENT"
  status: "ORDERED" | "SCHEDULED" | "IN_PROGRESS" | "COMPLETED"
  createdAt: string
}

export type ImagingStudy = {
  studyId: string; orderId: string; patientId: string; patientName: string
  modality: Modality; description: string
  status: "AVAILABLE" | "PROCESSING"
  studyDate: string; seriesCount: number; instanceCount: number; viewerUrl?: string
}

const KEY_ORDERS = "aha_imaging_orders_v1"
const KEY_STUDIES = "aha_imaging_studies_v1"

function safeLoad<T>(key: string, fallback: T): T {
  try {
    const raw = localStorage.getItem(key)
    if (!raw) return fallback
    return JSON.parse(raw) as T
  } catch { return fallback }
}

function safeSave<T>(key: string, value: T) {
  try { localStorage.setItem(key, JSON.stringify(value)) } catch {}
}

export function listOrders(): ImagingOrder[] { return safeLoad<ImagingOrder[]>(KEY_ORDERS, []) }
export function listStudies(): ImagingStudy[] { return safeLoad<ImagingStudy[]>(KEY_STUDIES, []) }

export function createOrder(input: Omit<ImagingOrder, "id" | "status" | "createdAt">): ImagingOrder {
  const orders = listOrders()
  const order: ImagingOrder = {
    ...input, id: String(Date.now()), status: "ORDERED", createdAt: new Date().toISOString()
  }
  safeSave(KEY_ORDERS, [order, ...orders])
  const studies = listStudies()
  const study: ImagingStudy = {
    studyId: `STUDY-${order.id}`, orderId: order.id,
    patientId: order.patientId, patientName: order.patientName,
    modality: order.modality, description: order.studyDescription,
    status: "AVAILABLE", studyDate: new Date().toISOString(),
    seriesCount: Math.floor(Math.random() * 6) + 1,
    instanceCount: Math.floor(Math.random() * 300) + 50,
    viewerUrl: `/pacs?study=${encodeURIComponent(`STUDY-${order.id}`)}`,
  }
  safeSave(KEY_STUDIES, [study, ...studies])
  return order
}

export function clearImagingDemo() {
  try { localStorage.removeItem(KEY_ORDERS); localStorage.removeItem(KEY_STUDIES) } catch {}
}

export function getStudyById(studyId: string): ImagingStudy | undefined {
  return listStudies().find(s => s.studyId === studyId)
}
