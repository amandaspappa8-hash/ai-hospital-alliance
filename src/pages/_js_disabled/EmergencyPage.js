import { jsx as _jsx } from "react/jsx-runtime";
import SpecialtyDoctorsView from "@/components/specialties/SpecialtyDoctorsView";
export default function EmergencyPage() {
    return (_jsx(SpecialtyDoctorsView, { title: "Emergency", icon: "\uD83D\uDE91", description: "Emergency department dashboard for triage, urgent routing, rapid treatment, and active patient flow.", specialtyName: "Emergency" }));
}
