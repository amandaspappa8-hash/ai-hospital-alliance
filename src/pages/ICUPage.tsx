import SpecialtyDoctorsView from "@/components/specialties/SpecialtyDoctorsView"

export default function ICUPage() {
  return (
    <SpecialtyDoctorsView
      title="ICU"
      icon="🏥"
      description="Critical care dashboard for oxygen tracking, severe cases, continuous monitoring, and physician review."
      specialtyName="ICU"
    />
  )
}
