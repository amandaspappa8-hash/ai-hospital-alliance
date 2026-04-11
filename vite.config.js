import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
export default defineConfig({
    plugins: [react()],
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "./src"),
        },
    },
    server: {
        host: "0.0.0.0",
        port: 5173,
        proxy: {
            "/auth": "http://127.0.0.1:8000",
            "/patients": "http://127.0.0.1:8000",
            "/orders": "http://127.0.0.1:8000",
            "/appointments": "http://127.0.0.1:8000",
            "/notes": "http://127.0.0.1:8000",
            "/pacs": "http://127.0.0.1:8000",
            "/ai": "http://127.0.0.1:8000",
        },
    },
    build: {
        rollupOptions: {
            output: {
                manualChunks: {
                    react: ["react", "react-dom"],
                    router: ["react-router-dom"],
                    radix: [
                        "@radix-ui/react-avatar",
                        "@radix-ui/react-checkbox",
                        "@radix-ui/react-dialog",
                        "@radix-ui/react-dropdown-menu",
                        "@radix-ui/react-menubar",
                        "@radix-ui/react-navigation-menu",
                        "@radix-ui/react-popover",
                        "@radix-ui/react-scroll-area",
                        "@radix-ui/react-select",
                        "@radix-ui/react-separator",
                        "@radix-ui/react-slot",
                        "@radix-ui/react-switch",
                        "@radix-ui/react-tabs",
                        "@radix-ui/react-tooltip",
                    ],
                    charts: ["recharts"],
                },
            },
        },
    },
});
