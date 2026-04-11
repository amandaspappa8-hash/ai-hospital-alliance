import { jsx as _jsx } from "react/jsx-runtime";
import SpecialtyDoctorsView from "@/components/specialties/SpecialtyDoctorsView";
export default function ICUPage() {
    return (_jsx(SpecialtyDoctorsView, { title: "ICU", icon: "\uD83C\uDFE5", description: "Critical care dashboard for oxygen tracking, severe cases, continuous monitoring, and physician review.", specialtyName: "ICU" }));
}
