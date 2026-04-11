import { apiGet, apiPost } from "@/lib/api";
export async function getAppointments() {
    const data = await apiGet("/appointments");
    return Array.isArray(data) ? data : [];
}
export async function createAppointment(payload) {
    return apiPost("/appointments", payload);
}
