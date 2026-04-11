import SpecialtyDoctorsView from "@/components/specialties/SpecialtyDoctorsView"

export default function EmergencyPage() {
  return (
    <SpecialtyDoctorsView
      title="Emergency"
      icon="🚑"
      description="Emergency department dashboard for triage, urgent routing, rapid treatment, and active patient flow."
      specialtyName="Emergency"
    />
  )
}
