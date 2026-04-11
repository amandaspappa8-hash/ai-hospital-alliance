export function getRoleLabelKey(role?: string) {
  if (!role) return "user.noRole"

  switch (role) {
    case "Admin":
      return "role.Admin"
    case "Doctor":
      return "role.Doctor"
    case "Radiology":
      return "role.Radiology"
    case "Nurse":
      return "role.Nurse"
    case "Pharmacist":
      return "role.Pharmacist"
    case "Patient":
      return "role.Patient"
    default:
      return role
  }
}
