export const appEnv = import.meta.env.VITE_APP_ENV || "development";
export const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || "https://ai-hospital-alliance-production.up.railway.app";
export const monitoringEnabled = String(import.meta.env.VITE_ENABLE_MONITORING || "false") === "true";
export const isDevelopment = appEnv === "development";
export const isStaging = appEnv === "staging";
export const isProduction = appEnv === "production";
export function validateFrontendEnv() {
    const issues = [];
    if (!apiBaseUrl) {
        issues.push("VITE_API_BASE_URL is missing");
    }
    if (!/^https?:\/\//i.test(apiBaseUrl) && !apiBaseUrl.startsWith("/")) {
        issues.push("VITE_API_BASE_URL must start with http:// or https://");
    }
    if (!["development", "staging", "production"].includes(appEnv)) {
        issues.push("VITE_APP_ENV must be one of: development, staging, production");
    }
    return {
        ok: issues.length === 0,
        issues,
        appEnv,
        apiBaseUrl,
        monitoringEnabled,
        isDevelopment,
        isStaging,
        isProduction,
    };
}
