import { jsx as _jsx } from "react/jsx-runtime";
import SpecialtyDoctorsView from "@/components/specialties/SpecialtyDoctorsView";
export default function PediatricsPage() {
    return (_jsx(SpecialtyDoctorsView, { title: "Pediatrics", icon: "\uD83E\uDDD2", description: "Children care dashboard for pediatric visits, fever evaluation, growth checks, and family-centered workflow.", specialtyName: "Pediatrics" }));
}
