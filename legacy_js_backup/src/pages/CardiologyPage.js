import { jsx as _jsx } from "react/jsx-runtime";
import SpecialtyDoctorsView from "@/components/specialties/SpecialtyDoctorsView";
export default function CardiologyPage() {
    return (_jsx(SpecialtyDoctorsView, { title: "Cardiology", icon: "\u2764\uFE0F", description: "Heart center dashboard for cardiac workflow, ECG review, chest pain triage, and specialist monitoring.", specialtyName: "Cardiology" }));
}
