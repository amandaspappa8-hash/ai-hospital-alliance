import { safeStorage } from "./safe-storage";
const TOKEN_KEY = "aiha_token";
const USER_KEY = "aiha_user";
export function getToken() {
    return safeStorage.get(TOKEN_KEY);
}
export function setToken(token) {
    safeStorage.set(TOKEN_KEY, token);
}
export function getUser() {
    const raw = safeStorage.get(USER_KEY);
    if (!raw)
        return null;
    try {
        return JSON.parse(raw);
    }
    catch {
        return null;
    }
}
export function setUser(user) {
    safeStorage.set(USER_KEY, JSON.stringify(user));
}
export function saveAuth(token, user) {
    setToken(token);
    setUser(user);
}
export function clearToken() {
    safeStorage.remove(TOKEN_KEY);
}
export function clearAuth() {
    safeStorage.remove(TOKEN_KEY);
    safeStorage.remove(USER_KEY);
}
export function logout() {
    clearAuth();
}
