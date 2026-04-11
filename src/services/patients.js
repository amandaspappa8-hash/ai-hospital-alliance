import { apiGet } from "@/lib/api";
export function getPatients() {
    return apiGet("/patients");
}
