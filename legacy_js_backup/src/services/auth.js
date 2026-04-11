import { apiGet, apiPost } from "@/lib/api";
export function login(username, password) {
    return apiPost("/auth/login", { username, password });
}
export function getMe(token) {
    return apiGet(`/auth/me?token=${encodeURIComponent(token)}`);
}
