import { jsx as _jsx } from "react/jsx-runtime";
import SpecialtyDoctorsView from "@/components/specialties/SpecialtyDoctorsView";
export default function NeurologyPage() {
    return (_jsx(SpecialtyDoctorsView, { title: "Neurology", icon: "\uD83E\uDDE0", description: "Neurology center for stroke screening, brain monitoring, neuro consults, and specialist decision workflow.", specialtyName: "Neurology" }));
}
