import type { UserRole } from "@/types/auth"

export type AppRoute =
  | "dashboard"
  | "overview"
  | "patients"
  | "reports"
  | "appointments"
  | "file-manager"
  | "medications"
  | "notes"
  | "prescriptions"
  | "lab-orders"
  | "labs"
  | "interactions"
  | "drug-formulary"
  | "pacs"
  | "ct-mri"
  | "imaging-orders"
  | "settings"

const rolePermissions: Record<UserRole, AppRoute[]> = {
  Admin: [
    "dashboard",
    "overview",
    "patients",
    "reports",
    "appointments",
    "file-manager",
    "medications",
    "notes",
    "prescriptions",
    "lab-orders",
    "labs",
    "interactions",
    "drug-formulary",
    "pacs",
    "ct-mri",
    "imaging-orders",
    "settings",
  ],
  Doctor: [
    "dashboard",
    "overview",
    "patients",
    "reports",
    "appointments",
    "notes",
    "labs",
    "medications",
  ],
  Radiology: [
    "dashboard",
    "overview",
    "reports",
    "pacs",
    "ct-mri",
    "imaging-orders",
    "file-manager",
    "labs",
    "medications",
  ],
}

export function hasAccess(role: UserRole, route: AppRoute) {
  return rolePermissions[role]?.includes(route) ?? false
}
