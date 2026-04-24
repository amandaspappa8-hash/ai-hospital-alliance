import { getToken } from "@/lib/auth-storage";
const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";
function authHeaders() {
    const token = getToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
}
async function request(path, options) {
    const res = await fetch(`${API_BASE}${path}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...authHeaders(),
            ...(options?.headers ?? {}),
        },
    });
    if (!res.ok) {
        const text = await res.text();
        throw new Error(`${res.status} ${res.statusText}: ${text}`);
    }
    return res.json();
}
export function apiGet(path) {
    return request(path, { method: "GET" });
}
export function apiPost(path, body) {
    return request(path, {
        method: "POST",
        body: body ? JSON.stringify(body) : undefined,
    });
}
export async function apiPut(path, body) {
    return request(path, {
        method: "PUT",
        body: JSON.stringify(body),
    });
}
export async function apiDelete(path) {
    return request(path, { method: "DELETE" });
}
