const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";
async function request(path, options) {
    const res = await fetch(`${API_BASE}${path}`, {
        headers: {
            "Content-Type": "application/json",
            ...(options?.headers ?? {}),
        },
        ...options,
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
export function apiPut(path, body) {
    return request(path, {
        method: "PUT",
        body: body ? JSON.stringify(body) : undefined,
    });
}
export function apiDelete(path) {
    return request(path, { method: "DELETE" });
}
