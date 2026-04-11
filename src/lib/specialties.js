import { apiGet } from "@/lib/api";
export async function getSpecialtiesSummary() {
    const data = await apiGet("/specialties/summary");
    return Array.isArray(data) ? data : [];
}
