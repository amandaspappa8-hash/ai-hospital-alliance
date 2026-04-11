import { apiGet } from "@/lib/api";
export async function getDoctorsSummary() {
    const data = await apiGet("/doctors/summary");
    return Array.isArray(data) ? data : [];
}
export async function getDoctorsBySpecialty(name) {
    const data = await apiGet(`/doctors/by-specialty/${encodeURIComponent(name)}`);
    return Array.isArray(data) ? data : [];
}
export async function getDoctorById(doctorId) {
    return apiGet(`/doctors/${encodeURIComponent(doctorId)}`);
}
