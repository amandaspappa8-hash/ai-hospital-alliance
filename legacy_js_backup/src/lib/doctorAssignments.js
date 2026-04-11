import { apiGet, apiPost } from "@/lib/api";
export async function getDoctorAssignments(doctorId) {
    const data = await apiGet(`/doctor-assignments/${encodeURIComponent(doctorId)}`);
    return Array.isArray(data) ? data : [];
}
export async function createDoctorAssignment(doctorId, payload) {
    return apiPost(`/doctor-assignments/${encodeURIComponent(doctorId)}`, payload);
}
export async function updateDoctorAssignmentStatus(doctorId, assignmentId, status) {
    return apiPost(`/doctor-assignments/${encodeURIComponent(doctorId)}/${assignmentId}/status`, { status });
}
export async function removeDoctorAssignment(doctorId, assignmentId) {
    const res = await fetch(`http://127.0.0.1:8000/doctor-assignments/${encodeURIComponent(doctorId)}/${assignmentId}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
    });
    if (!res.ok) {
        throw new Error("Failed to delete assignment");
    }
    return res.json();
}
