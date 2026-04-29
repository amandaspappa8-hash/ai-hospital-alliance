const TOKEN_KEY = "aiha_token";
const USER_KEY = "aiha_user";
function safeGet(key) {
    try {
        return localStorage.getItem(key);
    }
    catch {
        return null;
    }
}
function safeSet(key, value) {
    try {
        localStorage.setItem(key, value);
    }
    catch { }
}
function safeRemove(key) {
    try {
        localStorage.removeItem(key);
    }
    catch { }
}
export function saveAuth(token, user) {
    safeSet(TOKEN_KEY, token);
    safeSet(USER_KEY, JSON.stringify(user));
}
export function getToken() {
    return safeGet(TOKEN_KEY);
}
export function getUser() {
    const raw = safeGet(USER_KEY);
    if (!raw)
        return null;
    try {
        return JSON.parse(raw);
    }
    catch {
        return null;
    }
}
export function clearAuth() {
    safeRemove(TOKEN_KEY);
    safeRemove(USER_KEY);
}
